"""Publish explicitly selected code and captured artifacts to the authorized private repo."""
import argparse,gzip,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REMOTE='git@github.com:eihei317/usd-liquidity.git'
REPO=ROOT/'.sync/repository'
def git(*args):
    env=os.environ.copy();env['GIT_TERMINAL_PROMPT']='0'
    wrapper=Path(r'C:\Users\Administrator\Downloads\推特信息自动化\.runtime\git-ssh.exe')
    if wrapper.exists():env.update(GIT_SSH=str(wrapper),GIT_SSH_VARIANT='ssh');env.pop('GIT_SSH_COMMAND',None)
    p=subprocess.run(['git','-c','safe.directory='+REPO.as_posix(),*args],cwd=REPO if REPO.exists() else ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    if p.returncode:raise RuntimeError(p.stderr.strip())
    return p.stdout.strip()
def sync(run,phase):
    run=Path(run).resolve()
    if not run.is_relative_to((ROOT/'output/runs').resolve()):raise ValueError('Invalid captured run')
    REPO.parent.mkdir(exist_ok=True)
    if not (REPO/'.git').exists():git('clone',REMOTE,str(REPO))
    if git('remote','get-url','origin')!=REMOTE:raise RuntimeError('Unexpected sync remote')
    if git('branch','--show-current')!='main':raise RuntimeError('Expected main branch')
    git('pull','--ff-only','origin','main')
    for folder in ('scripts','prompts','frontend','eval'):
        shutil.copytree(ROOT/folder,REPO/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','data.js','*.db'))
    for name in ('local_app.py','requirements.txt','投资辅助升级方案.txt','github_sync.json','AGENTS.md'):
        if (ROOT/name).exists():shutil.copy2(ROOT/name,REPO/name)
    dest=REPO/'artifacts/runs'/run.name;dest.mkdir(parents=True,exist_ok=True)
    latest=run/'work/output/latest'
    for p in latest.glob('*.json'):shutil.copy2(p,dest/p.name)
    for name in ('bundle.json','brief.md','dashboard.html','manifest.json','research_record.json','research_review.json'):
        if (run/name).exists():shutil.copy2(run/name,dest/name)
    coverage=run/'work/output/history_coverage.json'
    if coverage.exists():shutil.copy2(coverage,dest/'history_coverage.json')
    db=run/'work/output/usd_liquidity.db'
    if db.exists():
        with db.open('rb') as src,gzip.open(dest/'history.sqlite.gz','wb') as out:shutil.copyfileobj(src,out)
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file() and p.name!='export_manifest.json'}
    (dest/'export_manifest.json').write_text(json.dumps({'run_id':run.name,'phase':phase,'files':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    (REPO/'artifacts/latest.json').write_text(json.dumps({'run_id':run.name,'phase':phase},ensure_ascii=False),encoding='utf-8')
    git('add','scripts','prompts','frontend','eval','local_app.py','requirements.txt','投资辅助升级方案.txt','github_sync.json','AGENTS.md','artifacts')
    staged=git('diff','--cached','--name-only').splitlines()
    for name in staged:
        if any(part in {'.workbuddy','.runtime','.repair','secrets','config','.sync'} for part in Path(name).parts):raise RuntimeError('Protected path in staged export')
        path=REPO/name
        if path.exists() and path.suffix not in {'.gz'}:
            body=path.read_bytes()
            if (b'-----BEGIN '+b'OPENSSH PRIVATE KEY-----') in body:raise RuntimeError('Credential found in export')
    if git('diff','--cached','--name-only'):
        git('-c','user.name=Codex','-c','user.email=codex@localhost','commit','-m',f'Capture {run.name}: {phase}')
    git('push','origin','main')
    head=git('rev-parse','HEAD');remote=git('ls-remote','origin','refs/heads/main').split()[0]
    if head!=remote:raise RuntimeError('Remote verification failed')
    print('[github] pushed and verified '+head,flush=True)
    return {'repository':'https://github.com/eihei317/usd-liquidity','commit':head,'phase':phase}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--run',required=True);a.add_argument('--phase',choices=['capture','result'],required=True);v=a.parse_args();sync(v.run,v.phase)
