"""Isolated local runs with a single atomic publication pointer."""
from pathlib import Path
import argparse, contextlib, datetime, hashlib, json, os, shutil, sqlite3, subprocess, sys, uuid
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
sys.path.insert(0,str(ROOT))

def require_history_complete(coverage):
    if coverage.get('missing') or coverage.get('treasury_failures'):
        raise RuntimeError('历史覆盖未完成，已保留抓取产物但停止发布：'+json.dumps({'missing':coverage.get('missing',[]),'source_failures':coverage.get('treasury_failures',[])},ensure_ascii=False))

def prepare_research(latest, previous_package=None, fetch=False):
    from scripts.investment_facts import enrich_package, build_market_context
    package=read(latest/'model_input.json')
    snapshot=read(latest/'snapshot.json')
    old_context=read(latest/'investment_market_context.json') if (latest/'investment_market_context.json').exists() else None
    context=build_market_context(package['generated_at_bjt'],fetch=fetch,previous_context=old_context)
    atomic(latest/'investment_market_context.json',context)
    coverage_path=latest.parent/'history_coverage.json'
    if coverage_path.exists():
        coverage=read(coverage_path)
        coverage['series']=[r for r in coverage['series'] if r['kind']!='market']
        for sid,rows in context.get('price_history',{}).items():
            coverage['series'].append({'kind':'market','id':sid,'source':'FRED public source history','observations':len(rows),'first':rows[0]['date'] if rows else None,'last':rows[-1]['date'] if rows else None,'status':'history_available' if len(rows)>1 else 'missing_history'})
        coverage['missing']=[r['id'] for r in coverage['series'] if r['status']=='missing_history']
        atomic(coverage_path,coverage)
        dashboard=read(latest/'dashboard_data.json');dashboard['history_coverage']=coverage;atomic(latest/'dashboard_data.json',dashboard)

    snapshot['investment_market_context']=context
    package=enrich_package(package,snapshot,previous_package)
    package['research_version']='3.0'
    package['analysis_prompt']=(ROOT/'prompts/usd_liquidity_prompt.md').read_text(encoding='utf-8')+'\n\n'+(ROOT/'prompts/investment_research_prompt.md').read_text(encoding='utf-8')
    contract=package.setdefault('output_contract',{})
    contract['fact_scope_rule']='唯一事实为data.facts；含investment趋势、日历、市场确认、比较及覆盖事实。历史价格数组不进入模型。'
    contract['claim_rule']='旧key_takeaways只写observed；旧risk_flags支持inference/scenario；投资推断和对称情景进入investment_assessment。全部引用合法fact_ids。'
    contract['number_format_rule']='模型定性解释，不手抄市场数值；所有市场数值由程序按结构化事实展示。'
    fields=contract.setdefault('required_top_level_fields',[])
    if 'investment_assessment' not in fields:fields.append('investment_assessment')
    atomic(latest/'model_input.json',package)
    return package,context

def research_brief(analysis,investment,review):
    value=analysis.get('investment_assessment')
    if not value:return []
    lines=['','## 美股与BTC中期投资研究',value['summary'],'','相对上次：'+value['change_summary']]
    for key,title in (('equities','美股'),('bitcoin','BTC')):
        item=value[key]
        lines+=['','### '+title+'：'+item['liquidity_bias']+'（'+item['horizon']+'，'+item['confidence']+'置信度）']
        for field,label in (('summary','判断'),('transmission','传导'),('confirmation','市场确认'),('invalidation','失效条件'),('coverage_limits','覆盖边界')):
            lines.append(label+'：'+item[field])
        lines.append('事实引用：'+', '.join(item['fact_ids']))
    lines+=['','### 市场预期覆盖',value['expectations']['status']+'：'+value['expectations']['summary']]
    for key,title in (('base','基准'),('upside','改善'),('downside','恶化')):
        item=value['scenarios'][key]
        lines+=['','### '+title+'情景',item['path'],'触发：'+item['trigger'],'失效：'+item['invalidation'],'事实引用：'+', '.join(item['fact_ids'])]
    lines+=['','### 下一轮核查',*('- '+s for s in value['next_checks'])]
    lines+=['','### 中期趋势（有效观测数，日频与周频分开）']
    for fact in investment.get('trend_facts',[]):
        lines.append(f"- {fact.get('name',fact.get('id',fact.get('fact_id')))}：{fact.get('previous_as_of','未知')} 至 {fact.get('as_of','未知')}；{fact.get('window_observations','?')}期；变化 {fact.get('change','未知')} {fact.get('unit','')}；状态 {fact.get('status','未知')}；{fact.get('fact_id')}")
    lines+=['','### 已公告结算日历（毛额，不等于净融资）']
    for fact in investment.get('calendar_facts',[]):
        lines.append('- '+json.dumps(fact,ensure_ascii=False))
    lines+=['','### 判断验证记录',review.get('methodology_note','尚在积累观察样本。')]
    for row in review.get('records',[]):lines.append('- '+json.dumps(row,ensure_ascii=False))
    return lines
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
        def stage(s):state.update(stage=s);atomic(OUT/'latest_attempt.json',state);atomic(OUT/'state'/ (rid+'.json'),state);print('[pipeline]',s,flush=True)
        try:
            stage('preparing')
            for folder in ('scripts','prompts','frontend'):
                shutil.copytree(ROOT/folder,work/folder,ignore=shutil.ignore_patterns('__pycache__'))
            cache=ROOT/'.workbuddy/cache'
            if cache.exists():shutil.copytree(cache,work/'.workbuddy/cache')
            current=read(OUT/'current.json') if (OUT/'current.json').exists() else None
            previous=OUT/current['directory']/'work/output/latest' if current else OUT/'latest'
            if source_run:
                source=(OUT/'runs'/source_run).resolve()
                if source.parent != (OUT/'runs').resolve():raise ValueError('Invalid source run')
                previous=source/'work/output/latest'
            previous_cache=previous.parents[1]/'.workbuddy/cache'
            if previous_cache.exists():shutil.copytree(previous_cache,work/'.workbuddy/cache',dirs_exist_ok=True)
            if previous.exists():shutil.copytree(previous,work/'output/latest')
            previous_package=read(previous/'model_input.json') if (previous/'model_input.json').exists() else None
            db=previous.parent/'usd_liquidity.db' if (current or source_run) else OUT/'usd_liquidity.db'
            (work/'output').mkdir(exist_ok=True)
            if (previous.parent/'history_coverage.json').exists():shutil.copy2(previous.parent/'history_coverage.json',work/'output/history_coverage.json')
            if db.exists():
                with sqlite3.connect(str(db)) as source,sqlite3.connect(str(work/'output/usd_liquidity.db')) as target:source.backup(target)
            env=os.environ.copy()
            key=ROOT/'.workbuddy/secrets/fred_api_key'
            if not env.get('FRED_API_KEY') and key.exists():env['FRED_API_KEY']=key.read_text(encoding='utf-8-sig').strip()
            def call(script,*args):subprocess.run([sys.executable,'-B','-X','utf8','-u',str(work/'scripts'/script),*args],cwd=work,env=env,check=True)
            if mode=='update':stage('fetching');call('run.py','更新美元流动性数据','--json')
            latest=work/'output/latest'
            if mode=='history':stage('refreshing_missing_histories');call('run.py','补齐历史','--input-json',str(latest/'snapshot.json'),'--json')
            if not (latest/'model_input.json').exists():raise RuntimeError('没有可分析的事实包，请先更新数据。')
            if mode=='reanalyze' and not source_run and not candidate:
                package=read(latest/'model_input.json')
                package['analysis_prompt']=(ROOT/'prompts/usd_liquidity_prompt.md').read_text(encoding='utf-8')
                package['output_contract']['number_format_rule']='市场数值仅通过evidence_refs由程序呈现；定性叙述不手抄数值。'
                package['prompt_version']='2.0'
                atomic(latest/'model_input.json',package)
            if source_run and not candidate and mode!='history':
                stage('rebuilding_facts');call('rebuild_facts.py')
            if not candidate:
                stage('preparing_investment_research')
                prepare_research(latest,previous_package,fetch=(mode in ('update','history')))
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
                review=build_research_review(load_published_records(OUT)+[record],context.get('price_history',{}),published_at)
                atomic(dest/'research_review.json',review)
            bundle={'run_id':rid,'input_sha256':digest,'dashboard':dashboard,'analysis':analysis,'investment_facts':investment,'research_review':review}
            atomic(dest/'bundle.json',bundle)
            lines=['# 美元流动性分析',analysis['meta']['generated_at_bjt'],'',analysis['stance']['label'],analysis['stance']['one_liner']]
            lines+=research_brief(analysis,investment,review)
            for group in ('key_takeaways','risk_flags'):
                for item in analysis[group]:lines+=['','## '+item['title'],item['text'],*item['evidence']]
            (dest/'brief.md').write_text('\n'.join(lines),encoding='utf-8')
            front=work/'frontend/usd-liquidity-monitor'
            def safe_json(value):return json.dumps(value,ensure_ascii=False).replace('<','\\u003c')
            inline='window.DASHBOARD_DATA='+safe_json(dashboard)+';window.ANALYSIS_DATA='+safe_json(analysis)+';window.INVESTMENT_FACTS='+safe_json(investment)+';window.RESEARCH_REVIEW='+safe_json(review)+';'
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
