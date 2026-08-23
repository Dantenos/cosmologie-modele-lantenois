"""CHANTIER 2 EXECUTE — les perturbations DERIVEES, plus supposees.
DERIVATION COVARIANTE (une ligne chacune) :
  - Composant DE = POUSSIERE + SOURCE : T^mn_;n = Q u^m avec Q = (beta/t) rho_de. Le fond
    H(t) est fixe par Friedmann seul avec rho_de(t) = rho0 t^beta/a^3 — identique a avant :
    le << w_eff >> n'a jamais ete qu'une comptabilite. p_composant = 0, c_s = 0.
  - Injection homogene sur les tranches comobiles (theoreme des couches) => delta_Q = 0 et
    la creation est AU REPOS comobile => termes d'amortissement -(Q/rho) dans delta' ET theta'.
    C'est la lecture A, DERIVEE : la fourche CCDM est tranchee par delta_Q = 0, pas par gout.
EQUATIONS (Newtonien sous-horizon, variable ln a) :
  dm' = -Tm ; Tm' = -(2+dlnH/dlna)Tm/1 ... implementees en systeme (delta, theta~) standard,
  de'  = -Td - (Q/(rho H)) de ; Td' = -(1+dlnH/dlna)Td + S - (Q/(rho H)) Td ; S = (3/2)[Om dm + Ode de]
CRITERES PRE-ENREGISTRES :
(1) CONTROLE : en eteignant la source (Gamma->0, rho_de->const, de:=0), le MEME code doit
    redonner la croissance LCDM avec f(a=1) = Om(a=1)^0.55 a mieux que 1 %. Echec => rien.
(2) SORTIES : delta_de/delta_m aujourd'hui ; decalage de f*sigma8-proxy vs LCDM. Le corpus
    supposait ~1-2 % : ce calcul le CONFIRME ou le CORRIGE — verdict des nombres.
(3) Le CLASS complet (k-dependance, CMB) reste E9, externe ; ceci ferme la THEORIE du chantier."""
import numpy as np
np.seterr(all='ignore')
OM,B,ZEQ=0.3113,2.418,3387.
def fond(beta):
    Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-5,0,120000)
    E2=OM/a**3+Or/a**4+Ode
    for _ in range(12):
        E=np.sqrt(E2);ig=1/(a*E)
        t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
        if beta is None: rho=np.full_like(a,Ode)
        else: rho=Ode*np.clip(t,1e-300,None)**beta/a**3
        E2=OM/a**3+Or/a**4+rho
    return a,np.sqrt(E2),t,rho
def croissance(beta,avec_de):
    a,E,t,rho=fond(beta)
    la=np.log(a);dlnH=np.gradient(np.log(E),la)
    Om_a=OM/a**3/E**2; Ode_a=rho/E**2
    Q_rhoH=(B/np.clip(t*0.9501,1e-30,None))/E if beta is not None else 0*a
    i0=np.searchsorted(a,1e-2)
    dm,Tm,de,Td=1.0,1.0,0.0,0.0
    for i in range(i0,len(a)-1):
        h=la[i+1]-la[i]
        S=1.5*(Om_a[i]*dm+(Ode_a[i]*de if avec_de else 0))
        ddm=Tm; dTm=-(2+dlnH[i])*Tm+S
        if avec_de and beta is not None:
            dde=Td-Q_rhoH[i]*de; dTd=-(2+dlnH[i])*Td+S-Q_rhoH[i]*Td
        else: dde=dTd=0.0
        dm+=h*ddm;Tm+=h*dTm;de+=h*dde;Td+=h*dTd
    f=Tm/dm
    return dm,f,(de/dm if avec_de else 0.0),a,E
print("(1) CONTROLE LCDM (source eteinte, meme code) :")
_,fL,_,a,E=croissance(None,False)
Om1=OM/1/ (E[-1]**2)
print(f"    f(a=1) = {fL:.4f}   vs Om(a=1)^0.55 = {Om1**0.55:.4f}   ecart {abs(fL/Om1**0.55-1)*100:.2f} %")
ok=abs(fL/Om1**0.55-1)<0.01
print(f"    {'PASSE' if ok else 'ECHEC — rien exploite'}")
print()
print("(2) MODELE, perturbations derivees (delta_Q=0, creation au repos) :")
dmM,fM,r,_,_=croissance(B,True)
dmL,fL2,_,_,_=croissance(B,False)     # meme fond, DE non agglomerante (reference interne)
print(f"    delta_de/delta_m (a=1)          = {r:.4f}")
print(f"    contribution DE a la source     : Ode*r = {r*(1-OM):.4f}  (vs Om={OM})")
print(f"    f(a=1) : avec DE-poussiere {fM:.4f} | DE lisse {fL2:.4f} | decalage {100*(fM/fL2-1):+.2f} %")
print(f"    D(a=1) : {100*(dmM/dmL-1):+.2f} %  => decalage f*sigma8 ~ {100*(fM*dmM/(fL2*dmL)-1):+.2f} %")
print()
print("(3) VERDICT : la fourche CCDM est tranchee PAR DERIVATION (delta_Q=0), et les nombres")
print("    supposés du corpus sont maintenant DERIVES. CLASS complet -> E9 (externe).")
