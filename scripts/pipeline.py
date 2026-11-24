"""Isolated local runs with a single atomic publication pointer."""
from pathlib import Path
import argparse, contextlib, datetime, gzip, hashlib, json, os, shutil, sqlite3, subprocess, sys, uuid, time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
sys.path.insert(0,str(ROOT))

def require_history_complete(coverage):
    if coverage.get('missing') or coverage.get('treasury_failures'):
        raise RuntimeError('历史覆盖未完成，已保留抓取产物但停止发布：'+json.dumps({'missing':coverage.get('missing',[]),'source_failures':coverage.get('treasury_failures',[])},ensure_ascii=False))

def verified_json_bytes(path, digest, *, exported=False):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() == digest:
        return raw
    if exported:  # Git normalized some early JSON exports before .gitattributes was installed.
        lf = raw.replace(b'\r\n', b'\n')
        for original in (lf, lf.replace(b'\n', b'\r\n')):
            if hashlib.sha256(original).hexdigest() == digest:
                return original
    raise ValueError('已归档事实文件哈希不符：' + path.name)


def restore_archived_capture(run, work):
    """Restore a pruned run's frozen inputs into the new work directory only."""
    archive = ROOT / '.sync/repository/artifacts/runs' / run.name
    manifest = read(run / 'manifest.json')
    if manifest.get('run_id') != run.name:
        raise ValueError('归档清单与源运行不符')
    restored = set()
    for name, digest in manifest['files'].items():
        parts = name.replace('\\', '/').split('/')
        if parts[:3] == ['work', 'output', 'latest'] and len(parts) == 4 and parts[-1].endswith('.json'):
            src = archive / parts[-1]
        elif parts == ['work', 'output', 'history_coverage.json']:
            src = archive / parts[-1]
        elif parts == ['work', 'output', 'usd_liquidity.db']:
            src = archive / 'history.sqlite.gz'
        else:
            continue
        target = work.joinpath(*parts[1:])
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.suffix == '.db':
            with gzip.open(src, 'rb') as stream, target.open('wb') as dest:
                shutil.copyfileobj(stream, dest)
            with target.open('rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != digest:
                    raise ValueError('归档源文件哈希不符：' + target.name)
        else:
            target.write_bytes(verified_json_bytes(src, digest, exported=True))
        restored.add(target.name)
    if not {'model_input.json', 'snapshot.json', 'usd_liquidity.db'} <= restored:
        raise ValueError('归档缺少回放所需的事实包、原始快照或冻结数据库')


def comparison_baseline(head_run, capture_time):
    """Find a strictly earlier capture on the published branch, including after a replay."""
    from scripts.investment_review import _timestamp
    cutoff = _timestamp(capture_time)
    visited = set()
    while head_run:
        directory = (OUT / 'runs' / head_run).resolve()
        if directory.parent != (OUT / 'runs').resolve() or head_run in visited:
            raise ValueError('比较基准的发布链无效')
        visited.add(head_run)
        manifest_path = directory / 'manifest.json'
        if not manifest_path.is_file():
            break
        manifest = read(manifest_path)
        if manifest.get('run_id') != head_run:
            raise ValueError('比较基准清单与运行标识不符')
        latest = directory / 'work/output/latest'
        exported = not (latest / 'model_input.json').is_file()
        if exported:
            latest = ROOT / '.sync/repository/artifacts/runs' / head_run
        package_path = latest / 'model_input.json'
        if not package_path.is_file():
            break
        raw = verified_json_bytes(package_path, manifest.get('input_sha256'), exported=exported)
        package = json.loads(raw)
        if _timestamp(package['generated_at_bjt']) < cutoff:
            return package, latest / 'snapshot.json'
        head_run = manifest.get('previous_run_id')
    return None, None


def market_context_for_capture(stamp, old_context, fetch):
    from scripts.investment_facts import build_market_context
    from scripts.investment_review import _timestamp
    if not fetch and old_context:
        if old_context.get('generated_at_bjt') == stamp:
            return old_context  # This capture includes its original source statuses.
        try:
            captured = _timestamp(old_context['generated_at_bjt'])
            retrieved = _timestamp(old_context['retrieved_at_bjt'])
            if max(captured, retrieved) > _timestamp(stamp):
                old_context = None
        except (KeyError, ValueError):
            old_context = None
    return build_market_context(stamp, fetch=fetch, previous_context=old_context)


def prepare_research(latest, previous_package=None, fetch=False, previous_snapshot=None):
    from scripts.analysis import analysis_output_contract
    from scripts.investment_facts import MARKET_SERIES, enrich_package
    package=read(latest/'model_input.json')
    snapshot=read(latest/'snapshot.json')
    old_context=read(latest/'investment_market_context.json') if (latest/'investment_market_context.json').exists() else None
    context = market_context_for_capture(package['generated_at_bjt'], old_context, fetch)
    atomic(latest/'investment_market_context.json',context)
    coverage_path=latest.parent/'history_coverage.json'
    if coverage_path.exists():
        coverage=read(coverage_path)
        coverage['series']=[r for r in coverage['series'] if r['kind']!='market']
        for sid in MARKET_SERIES:
            rows = context.get('price_history', {}).get(sid, [])
            source_status = context.get('series', {}).get(sid, {}).get('status', 'missing')
            coverage['series'].append({'kind':'market','id':sid,'source':'FRED public source history','source_status':source_status,'observations':len(rows),'first':rows[0]['date'] if rows else None,'last':rows[-1]['date'] if rows else None,'status':'history_available' if len(rows)>1 else 'missing_history'})
        coverage['missing']=[r['id'] for r in coverage['series'] if r['status']=='missing_history']
        atomic(coverage_path,coverage)
        dashboard=read(latest/'dashboard_data.json');dashboard['history_coverage']=coverage;atomic(latest/'dashboard_data.json',dashboard)

    snapshot['investment_market_context']=context
    package=enrich_package(package,snapshot,previous_package,history_db=latest.parent/'usd_liquidity.db',
                           previous_snapshot=previous_snapshot)
    package['research_version']='3.1'
    package['prompt_version']='3.1'
    package['analysis_prompt']=(ROOT/'prompts/usd_liquidity_prompt.md').read_text(encoding='utf-8')+'\n\n'+(ROOT/'prompts/investment_research_prompt.md').read_text(encoding='utf-8')
    contract=package.setdefault('output_contract',{})
    contract.update(analysis_output_contract())
    fields=contract.setdefault('required_top_level_fields',[])
    if 'investment_assessment' not in fields:fields.append('investment_assessment')
    atomic(latest/'model_input.json',package)
    return package,context

def atomic(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    with tmp.open('w',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
@contextlib.contextmanager
def lock():
    import msvcrt
    OUT.mkdir(exist_ok=True)
    with (OUT/'pipeline.lock').open('a+b') as f:
        f.seek(0);f.write(b'0');f.flush();f.seek(0)
        try:msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
        except OSError:raise RuntimeError('已有更新或分析正在运行，请查看状态。')
        try:yield
        finally:f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
def run(mode, source_run=None, candidate=None):
    with lock():
        now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        rid=now.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8]
        dest=OUT/'runs'/rid;work=dest/'work';work.mkdir(parents=True)
        state={'run_id':rid,'mode':mode,'started_at_bjt':now.isoformat(),'status':'running'}
        stage_started=time.monotonic()
        def stage(s):
            nonlocal stage_started
            now_mono=time.monotonic()
            if state.get('stage'):
                state.setdefault('stage_seconds',{})[state['stage']]=round(now_mono-stage_started,3)
            state.update(stage=s,stage_started_at_bjt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat())
            stage_started=now_mono
            atomic(OUT/'latest_attempt.json',state);atomic(OUT/'state'/(rid+'.json'),state)
            print('[pipeline]',s,flush=True)
        try:
            stage('preparing')
            for folder in ('scripts','prompts','frontend'):
                shutil.copytree(ROOT/folder,work/folder,ignore=shutil.ignore_patterns('__pycache__'))
            cache=ROOT/'.workbuddy/cache'
            if cache.exists():shutil.copytree(cache,work/'.workbuddy/cache')
            current=read(OUT/'current.json') if (OUT/'current.json').exists() else None
            previous=OUT/current['directory']/'work/output/latest' if current else OUT/'latest'
            restored = False
            if source_run:
                source=(OUT/'runs'/source_run).resolve()
                if source.parent != (OUT/'runs').resolve():raise ValueError('Invalid source run')
                previous=source/'work/output/latest'
                if not (previous/'model_input.json').is_file():
                    restore_archived_capture(source, work)
                    restored = True
            previous_cache=previous.parents[1]/'.workbuddy/cache'
            if previous_cache.exists():shutil.copytree(previous_cache,work/'.workbuddy/cache',dirs_exist_ok=True)
            if previous.exists() and not restored:shutil.copytree(previous,work/'output/latest')
            db=previous.parent/'usd_liquidity.db' if (current or source_run) else OUT/'usd_liquidity.db'
            (work/'output').mkdir(exist_ok=True)
            if not restored and (previous.parent/'history_coverage.json').exists():shutil.copy2(previous.parent/'history_coverage.json',work/'output/history_coverage.json')
            incremental_state=previous.parent/'history_incremental_state.json'
            if incremental_state.exists() and not restored:shutil.copy2(incremental_state,work/'output/history_incremental_state.json')
            if db.exists() and not restored:
                with sqlite3.connect(str(db)) as source_db,sqlite3.connect(str(work/'output/usd_liquidity.db')) as target:source_db.backup(target)
            env=os.environ.copy()
            key=ROOT/'.workbuddy/secrets/fred_api_key'
            if not env.get('FRED_API_KEY') and key.exists():env['FRED_API_KEY']=key.read_text(encoding='utf-8-sig').strip()
            def call(script,*args):subprocess.run([sys.executable,'-B','-X','utf8','-u',str(work/'scripts'/script),*args],cwd=work,env=env,check=True)
            if mode=='history':env['LIQUIDITY_FULL_HISTORY']='1'
            if mode=='update':stage('fetching');call('run.py','更新美元流动性数据','--json')
            latest=work/'output/latest'
            timing=work/'output/fetch_timings.json'
            if mode=='update' and timing.exists():shutil.copy2(timing,latest/'fetch_timings.json')
            if mode=='history':stage('refreshing_missing_histories');call('run.py','补齐历史','--input-json',str(latest/'snapshot.json'),'--json')
            if not (latest/'model_input.json').exists():raise RuntimeError('没有可分析的事实包，请先更新数据。')
            if mode=='reanalyze' and not candidate:
                stage('rebuilding_facts');call('rebuild_facts.py')
            if not candidate:
                stage('preparing_investment_research')
                head_run = current['run_id'] if current else None
                if source_run and (source/'manifest.json').exists():
                    head_run = source_run
                capture_time = read(latest/'model_input.json')['generated_at_bjt']
                baseline, baseline_snapshot = comparison_baseline(head_run, capture_time)
                prepare_research(latest,baseline,fetch=(mode in ('update','history')),previous_snapshot=baseline_snapshot)
            if (ROOT/'github_sync.json').exists() and mode in ('update','history'):
                stage('syncing_capture')
                from scripts.sync_to_github import sync
                sync(dest,'capture')
            if mode in ('update','history') and (work/'output/history_coverage.json').exists():
                require_history_complete(read(work/'output/history_coverage.json'))
            stage('analyzing')
            if candidate:
                sys.path.insert(0,str(ROOT))
                from scripts.analysis_validator import materialize_evidence,validate_analysis
                source_candidate=Path(candidate).resolve()
                if not source_candidate.is_relative_to((OUT/'runs').resolve()):raise ValueError('Candidate must belong to captured runs')
                original=source_candidate.parent/'model_input.json'
                if original.read_bytes() != (latest/'model_input.json').read_bytes():raise ValueError('Candidate input does not match frozen facts')
                value=materialize_evidence(read(source_candidate),read(latest/'model_input.json'))
                errors=validate_analysis(value,read(latest/'model_input.json'))
                if errors:raise ValueError(json.dumps(errors,ensure_ascii=False))
                value.setdefault('meta',{})['status']='published';atomic(latest/'analysis.json',value)
            else:call('codex_analysis.py')
            if candidate:
                from scripts.display_history import fill
                fill(work,latest,read(latest/'model_input.json'))
            stage('rendering')
            dashboard=read(latest/'dashboard_data.json');analysis=read(latest/'analysis.json')
            if analysis.get('meta',{}).get('status')!='published':raise RuntimeError('模型未通过发布校验')
            digest=hashlib.sha256((latest/'model_input.json').read_bytes()).hexdigest()
            package=read(latest/'model_input.json')
            from scripts.analysis_validator import _collect_facts
            investment={**package.get('data',{}).get('facts',{}).get('investment',{}),
                        'catalog':_collect_facts(package)[0]}
            published_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
            review={}
            if analysis.get('investment_assessment'):
                from scripts.investment_review import create_research_record,build_research_review,load_published_records
                record=create_research_record(rid,analysis,package,published_at,digest)
                record['previous_run_id']=current['run_id'] if current else None
                atomic(dest/'research_record.json',record)
                context=read(latest/'investment_market_context.json') if (latest/'investment_market_context.json').exists() else {}
                history_gaps=[]
                records=load_published_records(OUT,history_gaps=history_gaps)
                review=build_research_review(records+[record],context.get('price_history',{}),published_at)
                review['history_complete']=not history_gaps
                review['history_gaps']=history_gaps
                if history_gaps:
                    review['methodology_note']+='早期研究归档不完整，缺失运行 '+', '.join(row['run_id'] for row in history_gaps)+' 及其更早链路。当前统计覆盖通过清单校验的记录。'
                atomic(dest/'research_review.json',review)
            from scripts.daily_brief import build_daily_brief, brief_markdown
            daily_brief = build_daily_brief(analysis, investment)
            bundle={'run_id':rid,'input_sha256':digest,'dashboard':dashboard,'analysis':analysis,'investment_facts':investment,'research_review':review,'daily_brief':daily_brief}
            atomic(dest/'bundle.json',bundle)
            (dest/'brief.md').write_text(brief_markdown(daily_brief),encoding='utf-8')
            front=work/'frontend/usd-liquidity-monitor'
            def safe_json(value):return json.dumps(value,ensure_ascii=False).replace('<','\\u003c')
            inline='window.STANDALONE_REPORT=true;window.DASHBOARD_DATA='+safe_json(dashboard)+';window.ANALYSIS_DATA='+safe_json(analysis)+';window.INVESTMENT_FACTS='+safe_json(investment)+';window.RESEARCH_REVIEW='+safe_json(review)+';window.DAILY_BRIEF='+safe_json(daily_brief)+';'
            (front/'data.js').write_text(inline,encoding='utf-8')
            html=(front/'index.html').read_text(encoding='utf-8')
            import re
            html=re.sub(r'<link[^>]+href=["\'](?:\./)?styles\.css(?:\?[^"\']*)?["\'][^>]*>',lambda m:'<style>'+(front/'styles.css').read_text(encoding='utf-8')+'</style>',html)
            for name in ('chart.min.js','data.js','app.js'):
                html=re.sub(r'<script[^>]+src=["\'](?:\./)?'+re.escape(name)+r'[^"\']*["\'][^>]*>\s*</script>',lambda m:'<script>'+(front/name).read_text(encoding='utf-8').replace('</script','<' + chr(92) + '/script')+'</script>',html)
            (dest/'dashboard.html').write_text(html,encoding='utf-8')
            files={str(q.relative_to(dest)):hashlib.sha256(q.read_bytes()).hexdigest() for q in dest.rglob('*') if q.is_file()}
            atomic(dest/'manifest.json',{'run_id':rid,'input_sha256':digest,'method_version':package.get('research_version','2.0'),'previous_run_id':current['run_id'] if current else None,'files':files})
            if (ROOT/'github_sync.json').exists():
                stage('syncing_result')
                from scripts.sync_to_github import sync
                sync(dest,'result')
            stage('publishing')
            pointer={'run_id':rid,'directory':'runs/'+rid,'previous_run_id':current['run_id'] if current else None,'published_at_bjt':published_at,'manifest_sha256':hashlib.sha256((dest/'manifest.json').read_bytes()).hexdigest()}
            state.update(status='succeeded');atomic(OUT/'latest_attempt.json',state);atomic(OUT/'state'/(rid+'.json'),state)
            # The publication pointer is the final fallible state mutation.
            # A required status write must not fail after replacing the result.
            atomic(OUT/'current.json',pointer)
        except BaseException as exc:
            state.update(status='failed',error=str(exc));atomic(OUT/'latest_attempt.json',state);atomic(OUT/'state'/(rid+'.json'),state);raise
        print(json.dumps(pointer,ensure_ascii=False),flush=True)
        return 0
def rollback():
    with lock():
        current=read(OUT/'current.json');previous=current.get('previous_run_id')
        if not previous:raise RuntimeError('没有上一份成功版本')
        selected=(OUT/'runs'/previous).resolve()
        if selected.parent!=(OUT/'runs').resolve():raise ValueError('Invalid rollback target')
        manifest=read(selected/'manifest.json')
        for name,digest in manifest['files'].items():
            f=(selected/name).resolve()
            if not f.is_relative_to(selected) or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise ValueError('Rollback manifest verification failed')
        pointer={'run_id':previous,'directory':'runs/'+previous,'previous_run_id':current['run_id'],'published_at_bjt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'manifest_sha256':hashlib.sha256((selected/'manifest.json').read_bytes()).hexdigest()}
        atomic(OUT/'current.json',pointer);print(json.dumps(pointer,ensure_ascii=False));return 0

def main():
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['update','history','reanalyze','status','rollback']);a.add_argument('--source-run');a.add_argument('--candidate');args=a.parse_args()
    if args.mode=='rollback':return rollback()
    if args.mode=='status':
        print(json.dumps({x:read(OUT/x) if (OUT/x).exists() else None for x in ('current.json','latest_attempt.json')},ensure_ascii=False));return 0
    return run(args.mode,args.source_run,args.candidate)
if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:print('[pipeline] failed:',exc,file=sys.stderr);raise SystemExit(1)
