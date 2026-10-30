"""Offline publication tests: one bundle, immutable record, failure retention."""
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'eval'))
from scripts import pipeline
from scripts.analysis_validator import validate_analysis
from test_investment_contract import sample_assessment


class Publication(unittest.TestCase):
    def setUp(self):
        (ROOT / 'output').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='test_research_', dir=ROOT / 'output')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to((ROOT / 'output').resolve()))
        for directory in ('scripts', 'prompts', 'frontend'):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns('__pycache__'))
        pointer_path = ROOT / 'output/current.json'
        fixture_latest = ROOT / 'output/latest'
        if pointer_path.exists():
            pointer = json.loads(pointer_path.read_text(encoding='utf-8-sig'))
            fixture_latest = ROOT / 'output' / pointer['directory'] / 'work/output/latest'
        shutil.copytree(fixture_latest, self.root / 'output/latest')
        self.fail = False

    def tearDown(self):
        self.assertTrue(self.root.is_relative_to((ROOT / 'output').resolve()))
        self.temp.cleanup()

    def model_call(self, args, **kwargs):
        script = Path(args[5])
        self.assertEqual('codex_analysis.py', script.name)
        if self.fail:
            raise subprocess.CalledProcessError(1, args)
        latest = script.parents[1] / 'output/latest'
        package = pipeline.read(latest / 'model_input.json')
        analysis = pipeline.read(latest / 'analysis.json')
        analysis['meta'].pop('status', None)
        research = sample_assessment()
        research['expectations']['fact_ids'] = ['coverage:direct_expectations']
        analysis['investment_assessment'] = research
        self.assertEqual([], validate_analysis(analysis, package))
        analysis['meta']['status'] = 'published'
        pipeline.atomic(latest / 'analysis.json', analysis)
        return subprocess.CompletedProcess(args, 0)

    def run_pipeline(self):
        with patch.object(pipeline, 'ROOT', self.root), patch.object(pipeline, 'OUT', self.root / 'output'), \
             patch.object(pipeline.subprocess, 'run', side_effect=self.model_call):
            return pipeline.run('reanalyze')

    def test_bundle_and_artifacts_share_research_and_manifest(self):
        self.assertEqual(0, self.run_pipeline())
        pointer = pipeline.read(self.root / 'output/current.json')
        directory = self.root / 'output' / pointer['directory']
        bundle = pipeline.read(directory / 'bundle.json')
        record = pipeline.read(directory / 'research_record.json')
        manifest = pipeline.read(directory / 'manifest.json')
        self.assertEqual(bundle['analysis']['investment_assessment'], record['assessment'])
        self.assertEqual(pointer['published_at_bjt'], record['published_at_bjt'])
        self.assertEqual('3.0', manifest['method_version'])
        self.assertEqual('collecting', bundle['research_review']['status'])
        self.assertIn('metric:SOFR', bundle['investment_facts']['catalog'])
        self.assertEqual(6, len(bundle['research_review']['records']))
        self.assertEqual(pointer['manifest_sha256'], hashlib.sha256((directory / 'manifest.json').read_bytes()).hexdigest())
        for name, digest in manifest['files'].items():
            self.assertEqual(digest, hashlib.sha256((directory / name).read_bytes()).hexdigest())
        offline = (directory / 'dashboard.html').read_text(encoding='utf-8')
        self.assertIn('window.INVESTMENT_FACTS=', offline)
        self.assertIn('window.RESEARCH_REVIEW=', offline)
        self.assertNotIn('src="./app.js', offline)
        self.assertNotIn('href="./styles.css', offline)
        self.assertIn('失效条件', (directory / 'brief.md').read_text(encoding='utf-8'))

    def test_failed_next_run_keeps_published_pointer(self):
        self.run_pipeline()
        before = (self.root / 'output/current.json').read_bytes()
        self.fail = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_pipeline()
        self.assertEqual(before, (self.root / 'output/current.json').read_bytes())
        self.assertEqual('failed', pipeline.read(self.root / 'output/latest_attempt.json')['status'])

    def test_required_status_failure_cannot_publish(self):
        self.run_pipeline()
        before = (self.root / 'output/current.json').read_bytes()
        real_atomic = pipeline.atomic
        def fail_required_status(path, value):
            if path.name == 'latest_attempt.json' and value.get('status') == 'succeeded':
                raise OSError('Simulated status disk failure')
            return real_atomic(path, value)
        with patch.object(pipeline, 'atomic', side_effect=fail_required_status):
            with self.assertRaises(OSError):
                self.run_pipeline()
        self.assertEqual(before, (self.root / 'output/current.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
