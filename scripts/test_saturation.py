"""TEST DE LA THEORIE DE LA SATURATION. CRITERE PRE-ENREGISTRE (gele avant execution) :
la these << le fond ne teste que l'appartenance a la classe saturante >> est CONFIRMEE si
trois formes rho_de(t) sans aucun rapport physique entre elles, chacune a UN parametre de
forme ajuste, atteignent un AIC a moins de 2 unites de celui du modele d'accretion sur les
memes donnees (Pantheon+ + DESI DR2 + distance-priors + SH0ES).
Elle est REFUTEE si une seule des trois s'ecarte de plus de 4 unites d'AIC.
Formes choisies AVANT tout ajustement, pour n'avoir aucun lien avec l'accretion ni avec CCBH :
  F1 tanh    : rho ∝ [1+tanh(p(t/t0-1/2))]  (transition lisse, phenomenologie pure)
  F2 Schechter integree : rho ∝ int_0^t s^p exp(-s) ds  (fonction de luminosite, hors sujet)
  F3 logistique en ln a : rho ∝ 1/(1+(a/0,5)^-p)  (croissance en biologie, hors sujet)
Aucune n'a de justification cosmologique. C'est le point."""
import numpy as np, sys
from scipy.optimize import minimize
from scipy.special import gammainc
sys.path.insert(0,'/home/claude/desi_fit'); sys.path.insert(0,'/home/claude/selection')
import vraisemblance_reelle as V, test_wE_v3 as T
np.seterr(all='ignore'); T.ZCUT=None
C_KM=299792.458; OM0,ZEQ=0.3113,3387.

def fond_forme(Om,h,p,forme,n=20000):
    Or=Om/(1+ZEQ); Ode=1-Om-Or; a=np.logspace(-6,0,n)
    E2=Om/a**3+Or/a**4+Ode
    for _ in range(14):
        E=np.sqrt(E2); ig=1/(a*E)
        t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t/=t[-1]
        if forme=='tanh':  f=1+np.tanh(p*(t-0.5))
        elif forme=='schechter': f=gammainc(p+1,np.clip(t*4,1e-12,None))
        else: f=1/(1+(a/0.5)**(-p))
        f=np.clip(f,1e-12,None); f=f/f[-1]
        E2=Om/a**3+Or/a**4+Ode*f
    return (1/a-1)[::-1], np.sqrt(E2)[::-1]

def chi2(par,forme):
    h,ob,Om,p=par
    if not(0.55<h<0.85 and 0.019<ob<0.026 and 0.15<Om<0.45 and 0.05<p<40): return 1e9
    zz,Ea=fond_forme(Om,h,p,forme)
    Ez=np.interp(T.zg,zz,Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez<=0): return 1e9
    inv=1/Ez; Dc=np.concatenate([[0],np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(T.zg))])
    DH0=C_KM/(100*h); om=Om*h**2
    rd=T.r_drag(ob,om); rs=T.r_star(ob,om); zs=T.z_star(ob,om)
    mu=5*np.log10((1+V.z_sn)*np.interp(V.z_sn,T.zg,Dc)); r=V.mb-mu
    c=r@V.Cinv_sn@r-(r@V.Cinv_one)**2/V.oCo
    u=np.zeros(13)
    for i,(z,typ,_,_,_) in enumerate(V.BAO):
        DM=np.interp(z,T.zg,Dc)*DH0; DH=DH0/np.interp(z,T.zg,Ez)
        u[i]={'M':DM,'H':DH,'V':(z*DM**2*DH)**(1/3)}[typ]/rd
    rb=V.d_bao-u; c+=rb@V.Cinv_bao@rb
    Dcs=np.interp(zs,T.zg,Dc)
    dv=np.array([np.sqrt(om/h**2)*Dcs,np.pi*Dcs*DH0/rs,ob])-T.DP_V
    return c+dv@T.DP_CI@dv+((100*h-T.H0_SH)/T.H0_SH_S)**2

if __name__=='__main__':
    print(f"  {'forme':>26s} {'chi2':>9s} {'AIC(k=4)':>9s} {'dAIC vs accretion':>18s}")
    ref=1427.31
    ecarts=[]
    for forme,lab,p0 in [('tanh','F1 tanh (phenomeno)',[3.]),('schechter','F2 Schechter integree',[1.5]),
                         ('logistique','F3 logistique (biologie)',[2.])]:
        best=None
        for s in ([0.687,0.0226,0.30]+p0,[0.70,0.0224,0.32,p0[0]*2],[0.68,0.0227,0.29,p0[0]/2]):
            r=minimize(lambda q:chi2(q,forme),s,method='Nelder-Mead',
                       options=dict(xatol=1e-6,fatol=1e-4,maxiter=6000))
            if best is None or r.fun<best.fun: best=r
        aic=best.fun+8
        print(f'  {lab:>26s} {best.fun:>9.2f} {aic:>9.2f} {aic-ref:>+18.2f}',flush=True)
        ecarts.append(aic-ref)
    v = ("CONFIRMEE (les trois a < 2 AIC : le fond ne discrimine pas la forme)" if all(abs(e) < 2 for e in ecarts)
         else "REFUTEE (au moins une forme a > 4 AIC : le fond DISCRIMINE)" if any(abs(e) > 4 for e in ecarts)
         else "INDECISE (entre 2 et 4 AIC)")
    print(f"\n  VERDICT (critere gele) : THEORIE DE LA SATURATION {v}")
