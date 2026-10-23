from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    out=Path(__file__).parent/'results'
    calibration=json.loads((out/'confirmation/calibration_summary.json').read_text())
    surface=json.loads((out/'surface/results.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    methods=['independent_jeffreys','geometric_laplacian','conventional_graph_regularization']
    labels=['Independent estimates','Geometric smoothing','Conventional graph smoothing']
    x=np.arange(2);width=.24
    for j,(method,label) in enumerate(zip(methods,labels)):
        vals=[next(r['mean_exact_risk'] for r in calibration if r['shape']==shape and r['method']==method) for shape in ['smooth','alternating']]
        axes[0].bar(x+(j-1)*width,np.array(vals)*100,width,label=label)
    axes[0].set(xticks=x,xticklabels=['Smooth noise','Alternating noise'],ylabel='Mean exact logical error (%)',title='Fresh-seed confirmation: 200 calibration datasets')
    for method,label in [('matched_mwpm','Matched MWPM'),('matched_correlated_mwpm','Conventional correlated MWPM'),('geometric_temporal_0.5','Geometric temporal factor 0.5'),('geometric_temporal_2.0','Geometric temporal factor 2')]:
        r=[r for r in surface if r['distance']==5 and r['basis']=='x' and r['model']=='uniform' and r['decoder']==method]
        axes[1].loglog([r['p'] for r in r],[r['logical_memory_failure'] for r in r],'o-',label=label)
    axes[1].set(xlabel='Circuit noise parameter p',ylabel='Logical memory failure per experiment',title='Surface memory: d=5, five rounds, X basis')
    for ax in axes:ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(out/'advantage_search.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()
