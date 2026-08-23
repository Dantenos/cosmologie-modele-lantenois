"""E8 — L'HORLOGE REFONDEE DANS LE TEMPS PROPRE DU COURANT DE POUSSIERE.
DERIVATION (une ligne) : la paroi comobile (temps propre t) voit defiler les coquilles de
poussiere du parent, chacune etiquetee par SON temps propre tau_p (= temps cosmique du parent,
la poussiere etant geodesique). Normalisation LTB synchrone + vitesse relative v0 continue :
   d(tau_p)/dt = gamma(v0) = 1/sqrt(1 - v0^2),  v0^2 = 2M_out/R = x^2 + s(2-s)
   =>  d(tau_p)/dt = 1/sqrt((1-s)^2 - x^2)
CRITERES PRE-ENREGISTRES :
(1) CONTROLES : v0->0 => taux -> 1 exactement ; meme lieu singulier x = 1-s que Vaidya
    (coherence de lignee), avec approche en racine (plus douce). Echec de l'un = rien exploite.
(2) kappa recalcule sur la BANDE SURVIVANTE de #132 : si kappa < 0,12 (sensibilite beta_1)
    partout sur la bande, l'horloge cesse d'etre un instrument et devient une PREDICTION :
    DR3 doit trouver beta_1 compatible avec kappa ~ 0.
(3) L'ANCRE HISTORIQUE REINTERPRETEE : l'ancienne borne |kappa|<0,24 -> x0<~0,30 etait un
    enonce de la branche VAIDYA. Nouvelle borne x0 en temps-poussiere calculee et publiee ;
    l'ecart est consigne comme correction d'un nombre du corpus, pas cache."""
import numpy as np
np.seterr(all='ignore')
OM,B,ZEQ=0.3113,2.418,3387.
Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-7,0,200000)
E2=OM/a**3+Or/a**4+Ode
for _ in range(12):
    E=np.sqrt(E2);ig=1/(a*E)
    t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
    E2=OM/a**3+Or/a**4+Ode*np.clip(t,1e-300,None)**B/a**3
E=np.sqrt(E2);T=t*0.9501;H=E
def kappa(x0,s0):
    chi=x0; x=H*a*chi; s=s0*a
    m=(a>=1e-3)&(((1-s)**2-x**2)>1e-6)
    Tm=T[m]; rate=1/np.sqrt((1-s[m])**2-x[m]**2)
    tp=np.concatenate([[1e-12],np.cumsum(0.5*(rate[1:]+rate[:-1])*np.diff(Tm))])
    g=(Tm/tp)*rate
    return np.gradient(np.log(g),np.log(Tm))[-1]
print("(1) CONTROLES")
print(f"   v0->0 : taux(x=1e-6,s=0) = {1/np.sqrt(1-1e-12):.12f}  (attendu 1)")
print(f"   lieu singulier : (1-s)^2-x^2 = 0 en x=1-s, comme Vaidya ; approche en racine. OK")
print()
print("(2) kappa EN TEMPS-POUSSIERE — colonne s=0 puis bande #132")
print(f"   {'x0':>5} {'s0':>6} {'kappa_poussiere':>16} {'kappa_Vaidya(ref)':>18}")
ref={(0.10,0.0):0.0516,(0.30,0.0):0.2408}
for x0,s0 in [(0.10,0.0),(0.30,0.0),(0.05,0.048),(0.10,0.046),(0.20,0.030),(0.30,0.004)]:
    k=kappa(x0,s0)
    rv=ref.get((x0,s0),float('nan'))
    print(f"   {x0:>5.2f} {s0:>6.3f} {k:>16.4f} {rv:>18}")
print()
print("(3) NOUVELLE BORNE : x0 tel que kappa_poussiere(x0,0) = 0,24")
lo,hi=0.3,0.99
for _ in range(40):
    mid=(lo+hi)/2
    if kappa(mid,0.0)<0.24: lo=mid
    else: hi=mid
print(f"   x0_max(temps-poussiere) = {lo:.3f}   [contre 0,30 sur la branche Vaidya]")
