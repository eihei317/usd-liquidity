"""Bounded parallel source fetches with deterministic order and durable timings."""
import concurrent.futures
import json
import threading
import time
from .utils import OUTPUT_DIR

def run_jobs(jobs, workers=6, report_path=None):
    report_path=report_path or OUTPUT_DIR/'fetch_timings.json'
    started=time.monotonic()
    report={'requested_workers':workers,'observed_concurrency':0,'jobs':[]}
    active=0
    guard=threading.Lock()
    def run(index,name,job):
        nonlocal active
        begin=time.monotonic()
        with guard:
            active+=1
            report['observed_concurrency']=max(active,report['observed_concurrency'])
        print(f'[fetch] start {name}',flush=True)
        row={'name':name,'index':index}
        try:
            result=job()
            values=list(result.values()) if isinstance(result,dict) else result if isinstance(result,list) else [result]
            failed=[getattr(m,'id','unknown') for m in values if getattr(m,'status',None) in ('error','unavailable')]
            row.update(status='source_error' if failed or not values else 'ok',failed_metrics=failed)
            return result
        except BaseException:
            row['status']='exception'
            raise
        finally:
            row['seconds']=round(time.monotonic()-begin,3)
            with guard:
                active-=1
                report['jobs'].append(row)
            print(f'[fetch] done {name} {row["seconds"]:.2f}s {row["status"]}',flush=True)
    result=[None]*len(jobs)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            pending={pool.submit(run,i,name,job):i for i,(name,job) in enumerate(jobs)}
            while pending:
                done,_=concurrent.futures.wait(pending,timeout=15,return_when=concurrent.futures.FIRST_COMPLETED)
                if not done:
                    print('[fetch] waiting '+', '.join(jobs[i][0] for i in pending.values())+f' ({time.monotonic()-started:.0f}s elapsed)',flush=True)
                for future in done:
                    result[pending.pop(future)]=future.result()
    finally:
        report['seconds']=round(time.monotonic()-started,3)
        report['jobs'].sort(key=lambda r:r['index'])
        report_path.parent.mkdir(parents=True,exist_ok=True)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return result
