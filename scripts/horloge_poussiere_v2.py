"""E8-v2 — CORRECTION DE #133 APRES AUDIT. L'erreur d'hier : j'ai pris dtau_p/dt = gamma(v_ff)
en confondant << vitesse de chute vs observateur STATIQUE >> et << vitesse relative vs la PAROI >>
(qui, elle, monte a Rdot = x). Le raccourci SR a perdu le terme croise.
DERIVATION EXACTE (gauge synchrone : grad tau_p = -u_dust, donc dtau_p/dt = -u_paroi . u_dust) :
  exterieur quasi-statique de masse M_out, f = 1 - 2M/R = (1-s)^2 - x^2 ;
  poussiere parabolique entrante : u_d = (1/f, -v_ff),  v_ff = sqrt(x^2+s(2-s)) ;
  paroi comobile sortante :        u_w = ((1-s)/f, +x).
  =>  dtau_p/dt = [(1-s) + x*v_ff] / [(1-s)^2 - x^2]     [pole d'ordre 1 en x=1-s, comme Vaidya]
CRITERES PRE-ENREGISTRES :
(1) CONTROLE GR : la contraction numerique -g_mn u_w^m u_d^n doit redonner la formule a 1e-12
    sur une grille (x,s). Echec => rien exploite.
(2) Recalcul de kappa (bande #132 + colonne s=0) et de x0_max(|kappa|=0,24). Le VERDICT
    (prediction kappa~0 / instrument / exclusion partielle) est celui des NOMBRES, quel qu'il soit.
(3) La formule et les chiffres de #133 sont SUPERSEDES ; consignation publique obligatoire."""
import numpy as np
np.seterr(all='ignore')
def rate(x,s):
    f=(1-s)**2-x**2; vff=np.sqrt(x**2+s*(2-s))
    return ((1-s)+x*vff)/f
print("(1) CONTROLE GR — contraction -u_w.u_d dans g=diag(-f,1/f) :")
ok=True
for x in [0.1,0.3,0.55]:
    for s in [0.0,0.05,0.2]:
        if x+s>=1: continue
        f=(1-s)**2-x**2; vff=np.sqrt(x**2+s*(2-s))
        ud=np.array([1/f,-vff]); uw=np.array([(1-s)/f,x])
        gam=-(-f*uw[0]*ud[0]+(1/f)*uw[1]*ud[1])
        ok&=abs(gam-rate(x,s))<1e-12
print(f"   9 couples : {'PASSE (1e-12)' if ok else 'ECHEC'}")
print(f"   normalisations : u_d.u_d = {(-f*ud[0]**2+ud[1]**2/f):+.1e}, u_w.u_w = {(-f*uw[0]**2+uw[1]**2/f):+.1e}  (attendu -1)")
print()
OM,B,ZEQ=0.3113,2.418,3387.
Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-7,0,200000)
E2=OM/a**3+Or/a**4+Ode
for _ in range(12):
    E=np.sqrt(E2);ig=1/(a*E)
    t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
    E2=OM/a**3+Or/a**4+Ode*np.clip(t,1e-300,None)**B/a**3
E=np.sqrt(E2);T=t*0.9501;H=E
def kappa(x0,s0):
    x=H*a*x0; s=s0*a
    m=(a>=1e-3)&(x+s<0.995)
    Tm=T[m]; r=rate(x[m],s[m])
    tp=np.concatenate([[1e-12],np.cumsum(0.5*(r[1:]+r[:-1])*np.diff(Tm))])
    g=(Tm/tp)*r
    return np.gradient(np.log(g),np.log(Tm))[-1]
print("(2) kappa CORRIGE")
print(f"   {'x0':>5} {'s0':>6} {'kappa_v2':>9} {'v1 (faux)':>10} {'Vaidya':>8}")
v1={(0.10,0.0):0.0052,(0.30,0.0):0.0464,(0.05,0.048):0.0268,(0.10,0.046):0.0301,(0.20,0.030):0.0379,(0.30,0.004):0.0489}
vd={(0.10,0.0):0.0516,(0.30,0.0):0.2408}
for k_ in [(0.10,0.0),(0.30,0.0),(0.05,0.048),(0.10,0.046),(0.20,0.030),(0.30,0.004)]:
    print(f"   {k_[0]:>5.2f} {k_[1]:>6.3f} {kappa(*k_):>9.4f} {v1[k_]:>10.4f} {vd.get(k_,float('nan')):>8}")
bande=[(0.05,0.048),(0.10,0.046),(0.20,0.030),(0.30,0.004)]
kb=[kappa(*k_) for k_ in bande]
print(f"   VERDICT sur le critere herite de v1 (kappa < 0,12 partout sur la bande -> PREDICTION) : "
      + ("TENU" if max(kb) < 0.12 else f"NON TENU (max {max(kb):.3f} a x0={bande[int(np.argmax(kb))][0]}) : la bande se scinde, "
         "l'horloge n'est une prediction que pour x0 <~ 0,2"))
lo,hi=0.05,0.95
for _ in range(40):
    mid=(lo+hi)/2
    if kappa(mid,0.0)<0.24: lo=mid
    else: hi=mid
print(f"   x0_max(|kappa|=0,24, s=0) = {lo:.3f}   [v1 faux : 0,648 ; Vaidya : 0,30]")
