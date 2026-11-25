import os
os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'
import sys, pathlib, csv, platform
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from src.search import *
OUT=pathlib.Path(__file__).resolve().parents[1]/'results'
if __name__=='__main__':
 with open(OUT/'runs.csv','w',newline='') as f,open(OUT/'curves.csv','w',newline='') as g:
  w=csv.writer(f); c=csv.writer(g); w.writerow(['method','dimension','budget','seed','error','ms','hit99']); c.writerow(['method','dimension','budget','seed','evaluation','best'])
  for d,m,s in product([2,3,4],['Grid','Random','BO'],range(30)):
   for b in ([50,100,200,500] if m=='Grid' else [500]):
    y,t=run(m,d,b,s); assert len(y)==b and np.all(np.diff(y)>=0)
    for n in ([b] if m=='Grid' else [50,100,200,500]):
     w.writerow([m,d,n,s,100-y[n-1],t[n-1],next((i+1 for i,v in enumerate(y[:n]) if v>=99),n+1)]); c.writerows([m,d,n,s,i+1,v] for i,v in enumerate(y[:n]))
   f.flush()
 with open(OUT/'grid_scaling.csv','w',newline='') as f:
  w=csv.writer(f); w.writerow(['m','calls','seed','ms','error'])
  for m,s in product([5,10,20],range(30)):
   t=perf_counter(); best=max(quality(np.array(x)) for x in product(np.linspace(0,1,m),repeat=3)); w.writerow([m,m**3,s,(perf_counter()-t)*1000,100-best])
 print('Completed 1080 budget records; 90 grid scaling runs',platform.platform(),sys.version)
