
#!/usr/bin/env python3
import argparse, json, logging, os, sys, urllib.error, urllib.request, urllib.parse

EXIT_OK=0
EXIT_ANOMALY=2
EXIT_USAGE=3
EXIT_REMOTE=4

logging.basicConfig(level=os.getenv('SUPPORT_TOOL_LOG_LEVEL','INFO'), format='%(levelname)s %(message)s')
log=logging.getLogger('support')

def fetch(url, api_key, timeout):
    req=urllib.request.Request(url, headers={'X-API-Key':api_key, 'Accept':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail=e.read().decode(errors='replace')
        raise RuntimeError(f'HTTP {e.code}: {detail}') from e
    except urllib.error.URLError as e:
        raise RuntimeError(f'connection error: {e.reason}') from e

def diagnose(tx):
    anomalies=[]
    if tx['status']=='PROCESSING': anomalies.append('transaction is still processing')
    if tx['status']=='FAILED': anomalies.append(f"failure_code={tx.get('failure_code') or 'unknown'}")
    callbacks=tx.get('callbacks',[])
    failures=[c for c in callbacks if c['callback_status']!='SUCCESS']
    if failures: anomalies.append(f'{len(failures)} failed callback attempt(s)')
    if tx['status']=='SUCCESS' and not any(c['callback_status']=='SUCCESS' for c in callbacks): anomalies.append('payment succeeded but callback success is missing')
    if anomalies:
        next_action='Check upstream/payment state and retry failed callbacks where policy permits.'
    else:
        next_action='No immediate anomaly detected. Continue normal monitoring.'
    return anomalies,next_action

def main():
    p=argparse.ArgumentParser(description='MiniPay L2 support diagnostic tool')
    p.add_argument('--transaction')
    p.add_argument('--health', action='store_true', help='check API health')
    p.add_argument('--json', action='store_true')
    p.add_argument('--base-url', default=os.getenv('MINIPAY_API_URL','http://127.0.0.1:8000'))
    p.add_argument('--api-key', default=os.getenv('MINIPAY_API_KEY',''))
    p.add_argument('--timeout', type=float, default=float(os.getenv('MINIPAY_TIMEOUT','5')))
    args=p.parse_args()
    try:
        if args.health:
            result=fetch(args.base_url.rstrip('/')+'/health',args.api_key,args.timeout)
            if args.json: print(json.dumps(result,indent=2))
            else: print(f"API health: {result.get('status')} / database: {result.get('database')}")
            return EXIT_OK
        if not args.transaction:
            p.error('--transaction or --health is required')
        txid=int(args.transaction) if args.transaction.isdigit() else None
        if txid is None:
            data=fetch(args.base_url.rstrip('/')+'/api/payments/search?transaction_ref='+urllib.parse.quote(args.transaction),args.api_key,args.timeout)
            if not data: raise RuntimeError('transaction not found')
            tx=data[0]
        else:
            tx=fetch(args.base_url.rstrip('/')+f'/api/payments/{txid}',args.api_key,args.timeout)
        anomalies,next_action=diagnose(tx)
        report={'transaction':tx,'anomalies':anomalies,'recommended_next_action':next_action}
        if args.json: print(json.dumps(report,default=str,indent=2))
        else:
            print(f"Transaction: {tx['id']} / {tx['transaction_ref']}")
            print(f"Customer: {tx['customer_id']}  Amount: {tx['amount']}  Status: {tx['status']}")
            print(f"Created: {tx['created_at']}  Completed: {tx.get('completed_at')}")
            callbacks=tx.get('callbacks',[])
            print(f"Callbacks: {len(callbacks)}")
            for cb in callbacks:
                print(f"  Attempt {cb['attempt_no']}: {cb['callback_status']} HTTP {cb.get('http_status')} at {cb['attempted_at']}")
            print('Anomalies: '+(', '.join(anomalies) if anomalies else 'none'))
            print('Next action: '+next_action)
        return EXIT_ANOMALY if anomalies else EXIT_OK
    except Exception as e:
        log.error('%s',e)
        return EXIT_REMOTE

if __name__=='__main__': sys.exit(main())
