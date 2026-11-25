from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1]/'results'; r=pd.read_csv(p/'runs.csv'); c=pd.read_csv(p/'curves.csv'); g=pd.read_csv(p/'grid_scaling.csv'); s=r.groupby(['dimension','budget','method']).agg(error=('error','mean'),sd=('error','std'),ms=('ms','mean')).reset_index(); s.to_csv(p/'summary.csv',index=False)
for d in [2,3,4]:
 fig,ax=plt.subplots(figsize=(7,3.4));
 for m,a in s[s.dimension==d].groupby('method'): ax.errorbar(a.budget,a.error,yerr=a.sd,marker='o',capsize=3,label=m)
 ax.set(xlabel='Evaluation budget',ylabel='Final error (mean ± SD)',title=f'{d} dimensions'); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(p/f'error{d}.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(7,3.4));
for m,a in c[(c.dimension==3)&(c.budget==500)].groupby('method'): ax.plot(a.groupby('evaluation').best.mean(),label=m)
ax.set(xlabel='Evaluations',ylabel='Best score',title='3D convergence (500-call runs)'); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(p/'convergence.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(7,3.4));
for m,a in s[s.dimension==3].groupby('method'): ax.plot(a.budget,a.ms,marker='o',label=m)
ax.set(xlabel='Budget',ylabel='Runtime (ms, log scale)',yscale='log'); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(p/'runtime.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(7,3.4)); a=g.groupby('m').mean(); ax.loglog(a.index,a.ms,marker='o',label='Measured'); ax.loglog(a.index,a.ms.iloc[0]*(a.index/5)**3,linestyle='--',label='Cubic reference'); ax.set(xlabel='Grid levels per axis',ylabel='Runtime (ms)',xticks=[5,10,20]); ax.set_xticklabels(['5','10','20']); ax.legend(); fig.tight_layout(); fig.savefig(p/'scaling.png',dpi=150)
