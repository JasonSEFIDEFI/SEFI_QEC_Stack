"""Frozen exploratory protocol: finite calibration, spatial prior, and model shift.

All fitted methods receive the identical known-probe calibration bit errors.
Evaluation uses syndrome only. Exact risk enumerates independent held-out errors;
uncertainty is across independent calibration datasets, not test-shot noise.
"""
from pathlib import Path
import importlib.util
import json
import math
import time
import numpy as np

spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('run.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CONFIG=dict(distance=7,base_p=[.05,.15],shapes=['smooth','alternating'],
            shifts=['none','reverse','burst'],calibration_shots=[10,50,500],
            seeds=list(range(3100,3150)),laplacian_penalty=2.,bootstrap_seed=812,
            bootstrap_resamples=2000,burst_mixture=.03)

def smooth_logits(logits, penalty):
    n=len(logits); D=np.diff(np.eye(n),axis=0)
    return np.linalg.solve(np.eye(n)+penalty*(D.T@D),logits)

def risk(weights, e, prob):
    s=e[:,:-1]^e[:,1:]; a=m.candidates(s)
    corr=a ^ ((a@weights > weights.sum()/2)[:,None]).astype(np.uint8)
    return float(prob@((e^corr)[:,0]))

def main(out=None):
    out=out or Path(__file__).parent/'results'; out.mkdir(exist_ok=True)
    (out/'calibration_config.json').write_text(json.dumps(CONFIG,indent=2))
    rows=[]; start=time.perf_counter(); n=CONFIG['distance']; e=m.patterns(n)
    for base in CONFIG['base_p']:
        for shape in CONFIG['shapes']:
            field=np.linspace(-1.5,1.5,n) if shape=='smooth' else 1.5*(-1.)**np.arange(n)
            training_ps=1/(1+np.exp(-(math.log(base/(1-base))+field)))
            for shots in CONFIG['calibration_shots']:
                for seed in CONFIG['seeds']:
                    rng=np.random.default_rng(seed)
                    k=(rng.random((shots,n))<training_ps).sum(axis=0)
                    ps=(k+.5)/(shots+1) # Jeffreys posterior mean; finite log odds.
                    logits=np.log(ps/(1-ps))
                    smooth=smooth_logits(logits,CONFIG['laplacian_penalty'])
                    D=np.diff(np.eye(n),axis=0)
                    eigen,vectors=np.linalg.eigh(D.T@D)
                    conventional=vectors@((vectors.T@logits)/(1+CONFIG['laplacian_penalty']*eigen))
                    weights={'pooled':np.full(n,-math.log((k.sum()+.5)/(shots*n-k.sum()+.5))),
                             'independent_jeffreys':-logits,
                             'geometric_laplacian':-smooth,
                             'conventional_graph_regularization':-conventional}
                    for shift in CONFIG['shifts']:
                        deploy=training_ps[::-1] if shift=='reverse' else training_ps
                        prob=np.prod(np.where(e,deploy,1-deploy),axis=1)
                        if shift=='burst':
                            burst=np.zeros(len(e))
                            for j in range(n-1):
                                mask=np.zeros(n,dtype=np.uint8);mask[j:j+2]=1
                                burst[np.all(e==mask,axis=1)]=1/(n-1)
                            prob=.97*prob+.03*burst
                        a=m.candidates(e[:,:-1]^e[:,1:]); idx=a@(2**np.arange(n-1,-1,-1))
                        oracle_corr=a^((prob[2**n-1-idx]>prob[idx])[:,None]).astype(np.uint8)
                        lower=float(prob@((e^oracle_corr)[:,0]))
                        for name,w in weights.items():
                            rows.append(dict(base_p=base,shape=shape,shift=shift,calibration_shots=shots,
                                seed=seed,method=name,exact_risk=risk(w,e,prob),
                                known_deployment_model_lower_bound=lower))
    groups={}
    for row in rows:
        key=(row['base_p'],row['shape'],row['shift'],row['calibration_shots'])
        groups.setdefault(key,{}).setdefault(row['method'],[]).append(row['exact_risk'])
    summaries=[]; rng=np.random.default_rng(CONFIG['bootstrap_seed'])
    for key,values in groups.items():
        base=np.array(values['independent_jeffreys'])
        ix=rng.integers(0,len(base),size=(CONFIG['bootstrap_resamples'],len(base)))
        for name,x in values.items():
            x=np.array(x); delta=x-base
            summaries.append(dict(base_p=key[0],shape=key[1],shift=key[2],calibration_shots=key[3],
                method=name,mean_exact_risk=float(x.mean()),paired_delta_vs_independent=float(delta.mean()),
                paired_bootstrap_ci95=np.quantile(delta[ix].mean(axis=1),[.025,.975]).tolist()))
    (out/'calibration_trials.json').write_text(json.dumps(rows,indent=2))
    (out/'calibration_summary.json').write_text(json.dumps(summaries,indent=2))
    (out/'calibration_timing.json').write_text(json.dumps(dict(seconds=time.perf_counter()-start,rows=len(rows)),indent=2))
    print(json.dumps(dict(rows=len(rows),conditions=len(groups),seconds=time.perf_counter()-start)))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--confirm',action='store_true'); args=parser.parse_args()
    if args.confirm:
        CONFIG.update(base_p=[.05],shapes=['smooth','alternating'],shifts=['none'],calibration_shots=[10],
                      seeds=list(range(9100,9300)),bootstrap_resamples=10000)
        main(Path(__file__).parent/'results'/'confirmation')
    else: main()
