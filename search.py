import numpy as np
from itertools import product
from scipy.linalg import solve_triangular
from scipy.special import ndtr
from time import perf_counter

def quality(x):
    z=np.asarray(x)-np.array([.57,.36,.68,.43])[:len(x)]
    return 100*np.exp(-np.sum(z*z)-.4*(z[0]-z[1])**2-.035*np.sum(1-np.cos(12*z)))

def run(method,d,b,seed):
    rng=np.random.default_rng(seed); start=perf_counter(); X=[]; Y=[]; times=[]
    if method=='Grid':
        m=int(np.ceil(b**(1/d))); candidates=np.array(list(product(np.linspace(0,1,m),repeat=d))); candidates=candidates[np.linspace(0,len(candidates)-1,b,dtype=int)]
    elif method=='Random': candidates=rng.random((b,d))
    for i in range(b):
        if method!='BO': x=candidates[i]
        elif i<8: x=rng.random(d)
        else:
            a=np.array(X); y=np.array(Y); idx=np.argsort(np.sum((a-a[y.argmax()])**2,axis=1))[:32]; a=a[idx]; y=(y[idx]-70)/30
            pool=rng.random((128,d)); pool[:64]=np.clip(a[y.argmax()]+rng.normal(0,.07,(64,d)),0,1)
            def k(a,b): return np.exp(-np.sum((a[:,None]-b[None,:])**2,axis=2)/(2*.23**2))
            L=np.linalg.cholesky(k(a,a)+1e-6*np.eye(len(a))); v=solve_triangular(L,k(a,pool),lower=True); alpha=solve_triangular(L,y,lower=True); mu=v.T@alpha; sd=np.sqrt(np.maximum(1e-12,1-np.sum(v*v,axis=0))); delta=mu-y.max()-.005; z=delta/sd; x=pool[np.argmax(delta*ndtr(z)+sd*np.exp(-z*z/2)/np.sqrt(2*np.pi))]
        X.append(x); Y.append(quality(x)); times.append((perf_counter()-start)*1000)
    return np.maximum.accumulate(Y),np.array(times)
