import importlib.util
from pathlib import Path
import math
import numpy as np

spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('run.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_exact_repetition_formula():
    for n in [3,5,7]:
        for p in [.001,.01,.1,.2]:
            expected=sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n//2+1,n+1))
            assert abs(m.exact_rate(n,p,'iid','minimum_weight')-expected)<1e-14

def test_syndrome_and_optimality():
    for n in [3,5,7]:
        for model in m.CONFIG['models']:
            e,pr,_=m.prior(n,.1,model)
            assert abs(pr.sum()-1)<1e-14
            s=e[:,:-1]^e[:,1:]
            for name in ['minimum_weight','maximum_likelihood','geometric_calibrated','geometric_uncalibrated']:
                c=m.decode(s,name,.1,model)
                assert np.array_equal(c[:,:-1]^c[:,1:],s)
                assert m.exact_rate(n,.1,model,'maximum_likelihood')<=m.exact_rate(n,.1,model,name)+1e-14

def test_geometric_likelihood_equivalence():
    for model in m.CONFIG['models']:
        assert abs(m.exact_rate(5,.1,model,'maximum_likelihood')-m.exact_rate(5,.1,model,'geometric_calibrated'))<1e-14

def test_pauli_limits_and_intervals():
    assert m.pauli_reference(0)==0
    assert abs(m.pauli_reference(.75)-.75)<1e-14
    lo,hi=m.wilson(0,60000)
    assert lo<1e-12 and hi>0

def test_graph_regularization_stationarity():
    spec=importlib.util.spec_from_file_location('calibration',Path(__file__).with_name('calibration.py'))
    c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    y=np.array([-3.,-2.,-1.,-2.,-3.,-2.,-1.]); D=np.diff(np.eye(7),axis=0)
    fitted=c.smooth_logits(y,2.)
    assert np.allclose(fitted-y+2*D.T@D@fitted,0,atol=1e-14)
    assert np.allclose(c.smooth_logits(y,0),y)
