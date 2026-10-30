import sys,tempfile,json,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import sync_to_github as sync
class Export(unittest.TestCase):
    def test_exports_and_verifies_remote(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as temp:
            root=Path(temp);repo=root/'.sync/repository';(repo/'.git').mkdir(parents=True)
            for folder in ('scripts','prompts','frontend','eval'):(root/folder).mkdir()
            run=root/'output/runs/test';latest=run/'work/output/latest';latest.mkdir(parents=True)
            (latest/'snapshot.json').write_text('{"data":123}',encoding='utf-8')
            calls=[]
            def git(*args):
                calls.append(args)
                if args[:3]==('remote','get-url','origin'):return sync.REMOTE
                if args[:2]==('branch','--show-current'):return 'main'
                if args[:2]==('rev-parse','HEAD'):return 'a'*40
                if args[0]=='ls-remote':return 'a'*40+' refs/heads/main'
                return ''
            with patch.object(sync,'ROOT',root),patch.object(sync,'REPO',repo),patch.object(sync,'git',side_effect=git):
                value=sync.sync(run,'capture')
            self.assertEqual('a'*40,value['commit'])
            self.assertIn(('push','origin','main'),calls)
            manifest=json.loads((repo/'artifacts/runs/test/export_manifest.json').read_text(encoding='utf-8'))
            self.assertIn('snapshot.json',manifest['files'])
    def test_scanner_source_does_not_contain_its_own_literal(self):
        marker=b'-----BEGIN '+b'OPENSSH PRIVATE KEY-----'
        self.assertNotIn(marker,Path(sync.__file__).read_bytes())
if __name__=='__main__':unittest.main()
