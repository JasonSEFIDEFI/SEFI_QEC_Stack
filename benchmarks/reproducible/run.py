"""Syndrome-only repetition-code experiments. No transmitted message enters a decoder."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import platform
import subprocess
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CONFIG = dict(seeds=[1701, 1702, 1703], shots_per_seed=20000,
              distances=[3, 5, 7], probabilities=[.001, .01, .05, .1, .2],
              models=['iid', 'heterogeneous', 'burst'], burst_mixture=.1)

def patterns(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.uint8)

def prior(n, p, model):
    ps = np.full(n, p) if model != 'heterogeneous' else p * np.linspace(.3, 1.7, n)
    e = patterns(n)
    prob = np.prod(np.where(e, ps, 1-ps), axis=1)
    if model == 'burst':
        # Mixture: iid background or exactly one adjacent pair. p remains the
        # background probability, not the mixture's marginal physical error rate.
        burst = np.zeros(len(e))
        for j in range(n-1):
            mask = np.zeros(n, dtype=np.uint8); mask[j:j+2] = 1
            burst[np.all(e == mask, axis=1)] += 1/(n-1)
        prob = .9*prob + .1*burst
    return e, prob, ps

def candidates(syndrome):
    z = np.zeros((len(syndrome), 1), dtype=np.uint8)
    return np.concatenate([z, np.bitwise_xor.accumulate(syndrome, axis=1)], axis=1)

def decode(syndrome, name, p, model):
    n = syndrome.shape[1]+1
    a = candidates(syndrome)
    if name == 'minimum_weight':
        choose = a.sum(axis=1) > n/2
    elif name == 'geometric_uncalibrated':
        # Hypothesis: spatially weighted distance helps. Same syndrome only;
        # fixed arbitrary metric, explicitly not a derived SEFI prediction.
        w = np.linspace(.2, 1.8, n)
        choose = a @ w > w.sum()/2
    else:
        e, prob, ps = prior(n, p, model)
        if name == 'geometric_calibrated' and model != 'burst':
            w = np.log((1-ps)/ps)
            choose = a @ w > w.sum()/2
        else:
            # Exact pattern likelihood, including correlated mixture.
            index = a @ (2**np.arange(n-1, -1, -1))
            choose = prob[(2**n-1)-index] > prob[index]
    return a ^ choose[:, None].astype(np.uint8)

def wilson(k, n):
    z=1.959963984540054; q=k/n; d=1+z*z/n
    c=(q+z*z/(2*n))/d; h=z*math.sqrt(q*(1-q)/n+z*z/(4*n*n))/d
    return [max(0, c-h), min(1, c+h)]

def exact_rate(n, p, model, decoder):
    e, prob, _ = prior(n,p,model)
    correction = decode(e[:,:-1]^e[:,1:], decoder,p,model)
    residual = e^correction
    assert np.all(residual == residual[:, :1])
    return float(prob @ residual[:,0])

def pauli_reference(p):
    # Three-qubit bit-flip code: ZZ checks correct X but cannot detect logical Z.
    total=0.
    for word in itertools.product(range(4), repeat=3):
        x=np.array([v in (1,2) for v in word]); z=sum(v in (2,3) for v in word)%2
        prob=math.prod(1-p if v==0 else p/3 for v in word)
        if x.sum()>=2 or z: total+=prob
    return total

def main(out=None):
    out=out or Path(__file__).parent/'results'; out.mkdir(parents=True,exist_ok=True)
    (out/'config.json').write_text(json.dumps(CONFIG,indent=2))
    rows=[]; raw={}; started=time.perf_counter()
    names=['minimum_weight','maximum_likelihood','geometric_calibrated','geometric_uncalibrated']
    for n,p,model in itertools.product(CONFIG['distances'],CONFIG['probabilities'],CONFIG['models']):
        e, prob, _ = prior(n,p,model)
        all_fail={name:[] for name in names}; elapsed={name:0. for name in names}
        for seed in CONFIG['seeds']:
            rng=np.random.default_rng(seed)
            errors=e[rng.choice(len(e), CONFIG['shots_per_seed'],p=prob)]
            syndrome=errors[:,:-1]^errors[:,1:]
            for name in names:
                t=time.perf_counter(); correction=decode(syndrome,name,p,model)
                elapsed[name]+=time.perf_counter()-t
                fail=(errors^correction)[:,0].astype(np.int8)
                all_fail[name].append(fail)
        base=np.concatenate(all_fail['minimum_weight'])
        for name in names:
            fail=np.concatenate(all_fail[name]); k=int(fail.sum()); shots=len(fail)
            delta=fail-base; se=float(delta.std(ddof=1)/math.sqrt(shots))
            truth=exact_rate(n,p,model,name)
            row=dict(distance=n,background_p=p,model=model,decoder=name,shots=shots,
                     failures=k,rate=k/shots,ci95=wilson(k,shots),exact_rate=truth,
                     paired_delta_vs_minimum_weight=float(delta.mean()),paired_delta_se=se,
                     seconds=elapsed[name],decode_shots_per_second=shots/elapsed[name],
                     physical_marginal=float(prob @ e.mean(axis=1)))
            rows.append(row)
            raw[f'n{n}_p{p}_{model}_{name}']=np.stack(all_fail[name])
    # Existing implementation diagnostics: explicitly labelled oracle control.
    from quantum.qec_pipeline import simple_recover
    from quantum.noise import phase_flip
    tx=[0,1]*10; rx=[1-x for x in tx]
    diagnostics={'oracle_all_bits_restored':simple_recover(tx,rx)==tx,
                 'phase_flip_p1_unchanged':phase_flip(tx,1)==tx,
                 'depolarizing_pauli_3qubit':[{ 'p':p,'logical_pauli_failure':pauli_reference(p)} for p in CONFIG['probabilities']]}
    (out/'results.json').write_text(json.dumps(rows,indent=2))
    (out/'diagnostics.json').write_text(json.dumps(diagnostics,indent=2))
    np.savez_compressed(out/'paired_failures.npz',**raw)
    metadata=dict(python=sys.version, platform=platform.platform(),numpy=np.__version__,
                  source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  elapsed_seconds=time.perf_counter()-started)
    (out/'environment.json').write_text(json.dumps(metadata,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(13,4))
    for ax,model in zip(axes,CONFIG['models']):
        for name in names:
            r=[x for x in rows if x['distance']==5 and x['model']==model and x['decoder']==name]
            ax.plot([x['background_p'] for x in r],[x['exact_rate'] for x in r],marker='o',label=name)
        ax.set(xscale='log',yscale='log',xlabel='Background bit error probability',ylabel='Exact logical X failure',title=f'd=5: {model}')
    axes[-1].legend(fontsize=6); fig.tight_layout(); fig.savefig(out/'logical_error.png',dpi=160); plt.close(fig)
    print(json.dumps(dict(cells=len(rows),sampled_error_patterns=45*60000,decoder_evaluations=len(rows)*60000,diagnostics=diagnostics,metadata=metadata),indent=2))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path); args=parser.parse_args()
    main(args.output)
