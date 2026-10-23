"""Circuit-level surface memory reference and exploratory geometric edge weights.

Stim example circuits are benchmark fixtures, not hardware predictions. All
decoders see the same detector events. Logical observables are scoring-only.
"""
from pathlib import Path
import importlib.util
import json
import platform
import sys
import time
import numpy as np
import stim
import pymatching

spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('run.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CONFIG=dict(distances=[3,5,7],probabilities=[.001,.003,.01],bases=['x','z'],
            models=['uniform','measurement_heavy'],seeds=[501,502,503],shots_per_seed=10000,
            temporal_weight_factors=[.5,2.])

def circuit(d,p,basis,model):
    return stim.Circuit.generated('surface_code:rotated_memory_'+basis,distance=d,rounds=d,
        after_clifford_depolarization=p,after_reset_flip_probability=p,
        before_measure_flip_probability=p*(3 if model=='measurement_heavy' else 1),
        before_round_data_depolarization=p)

def geometric_matching(dem,coords,factor):
    ref=pymatching.Matching.from_detector_error_model(dem)
    graph=pymatching.Matching()
    # Preserve every edge and logical label; alter only its temporal cost.
    for u,v,data in ref.edges():
        temporal=False
        if v is not None and len(coords.get(u,[]))>=3 and len(coords.get(v,[]))>=3:
            temporal=abs(coords[u][2]-coords[v][2])>0
        weight=data['weight']*(factor if temporal else 1.)
        kwargs=dict(fault_ids=data['fault_ids'],weight=weight,error_probability=data['error_probability'])
        if v is None: graph.add_boundary_edge(u,**kwargs)
        else: graph.add_edge(u,v,**kwargs)
    return graph

def smoke_test():
    c=circuit(3,0,'x','uniform'); dem=c.detector_error_model(decompose_errors=True)
    det,obs=c.compile_detector_sampler(seed=10).sample(100,separate_observables=True)
    pred=pymatching.Matching.from_detector_error_model(dem).decode_batch(det)
    assert not np.any(obs^pred)
    c=circuit(3,.003,'x','uniform'); dem=c.detector_error_model(decompose_errors=True)
    det,obs=c.compile_detector_sampler(seed=11).sample(1000,separate_observables=True)
    ref=pymatching.Matching.from_detector_error_model(dem).decode_batch(det)
    geo=geometric_matching(dem,c.get_detector_coordinates(),1.).decode_batch(det)
    assert np.array_equal(ref,geo)

def main():
    smoke_test()
    out=Path(__file__).parent/'results'/'surface'; out.mkdir(exist_ok=True)
    (out/'config.json').write_text(json.dumps(CONFIG,indent=2)); rows=[]
    import itertools
    for d,p,basis,model in itertools.product(CONFIG['distances'],CONFIG['probabilities'],CONFIG['bases'],CONFIG['models']):
        c=circuit(d,p,basis,model); dem=c.detector_error_model(decompose_errors=True)
        tag=f'd{d}_p{p}_{basis}_{model}'
        (out/(tag+'.stim')).write_text(str(c)); (out/(tag+'.dem')).write_text(str(dem))
        start=time.perf_counter()
        decoders={'matched_mwpm':pymatching.Matching.from_detector_error_model(dem),
                  'mismatched_uniform_mwpm':pymatching.Matching.from_detector_error_model(circuit(d,p,basis,'uniform').detector_error_model(decompose_errors=True))}
        for f in CONFIG['temporal_weight_factors']:
            decoders[f'geometric_temporal_{f}']=geometric_matching(dem,c.get_detector_coordinates(),f)
        # Correlated matching is a conventional stronger reference where available.
        decoders['matched_correlated_mwpm']=pymatching.Matching.from_detector_error_model(dem,enable_correlations=True)
        setup=time.perf_counter()-start
        failures={name:[] for name in decoders}; timing={name:0. for name in decoders}; sample_seconds=0.; raw={}
        for seed in CONFIG['seeds']:
            start=time.perf_counter(); det,obs=c.compile_detector_sampler(seed=seed).sample(CONFIG['shots_per_seed'],separate_observables=True)
            sample_seconds+=time.perf_counter()-start
            raw[f'detectors_{seed}']=np.packbits(det,axis=1,bitorder='little')
            raw[f'observables_{seed}']=obs
            # Rotate order by seed; these are throughput observations, not precise latency claims.
            for name in np.random.default_rng(seed).permutation(list(decoders)):
                start=time.perf_counter()
                pred=decoders[name].decode_batch(det,enable_correlations=name=='matched_correlated_mwpm')
                timing[name]+=time.perf_counter()-start
                fail=np.any(pred!=obs,axis=1).astype(np.int8); failures[name].append(fail)
                raw[f'{name}_{seed}']=fail
        base=np.concatenate(failures['matched_mwpm'])
        for name in decoders:
            fail=np.concatenate(failures[name]); delta=fail-base; shots=len(fail); k=int(fail.sum())
            rows.append(dict(distance=d,p=p,basis=basis,model=model,rounds=d,decoder=name,
                shots=shots,failures=k,logical_memory_failure=k/shots,ci95=m.wilson(k,shots),
                paired_delta_vs_matched_mwpm=float(delta.mean()),paired_delta_se=float(delta.std(ddof=1)/np.sqrt(shots)),
                decode_seconds=timing[name],decode_shots_per_second=shots/timing[name],
                all_decoder_setup_seconds=setup,sample_seconds=sample_seconds,
                detectors=c.num_detectors,qubits=c.num_qubits,saved_detector_bits=c.num_detectors))
        np.savez_compressed(out/(tag+'.npz'),**raw)
        (out/'results.json').write_text(json.dumps(rows,indent=2))
        print(tag,{name:int(np.concatenate(failures[name]).sum()) for name in decoders},flush=True)
    env=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,stim=stim.__version__,pymatching=pymatching.__version__)
    (out/'environment.json').write_text(json.dumps(env,indent=2))
    print(json.dumps(dict(cells=len(rows),circuit_shots=36*30000,environment=env)))

if __name__=='__main__': main()
