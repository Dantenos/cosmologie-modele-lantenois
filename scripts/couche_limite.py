"""LA COUCHE LIMITE — mecanisme, identite, domaine. CRITERES PRE-REGISTRES :
(1) IDENTITE (analytique, verifiee numeriquement au 1e-12) : le flux d'injection attribue au
    bord donne P_ram/|p_de| = x * v0, avec v0 la vitesse d'arrivee au bord interieur.
    Mon intuition d'hier (= x) etait le point v0=1 ; le MECANISME invoque (la pression de
    creation freine) etait FAUX DE SIGNE : une tension (p<0) n'oppose pas de poussee. A ecrire.
(2) LE VRAI FREIN, sans force : la friction de Hubble, v = v0 a_e/a. VALIDE si le domaine
    << couche mince >> est non vide : profondeur d(90% de freinage)/R < 0,3 pour v0 <= x/3,
    calcule sur NOTRE fond (pas d'estimation). REFUTE si d >= R partout.
(3) RETRO-REACTION : energie cinetique de couche / rho_de < 5% sur le domaine retenu, sinon
    l'hypothese d'homogeneite du corpus (H2/H3) est violee et le domaine est reduit d'autant.
Si (2) et (3) passent : la branche sigma-const de #130 gagne un DOMAINE DE VALIDITE nomme
(v0 <~ x/3), le mecanisme est la friction de Hubble, et v0 devient le parametre borne."""
import numpy as np
np.seterr(all='ignore')
OM,B,ZEQ=0.3113,2.418,3387.
Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-7,0,300000)
E2=OM/a**3+Or/a**4+Ode
for _ in range(12):
    E=np.sqrt(E2);ig=1/(a*E)
    t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
    E2=OM/a**3+Or/a**4+Ode*np.clip(t,1e-300,None)**B/a**3
E=np.sqrt(E2);T=t*0.9501;H=E
rho=Ode*np.clip(t,1e-300,None)**B/a**3
print("(1) IDENTITE P_ram/|p_de| = x*v0 — verification numerique du bilan")
for x0 in [0.1,0.3]:
    for v0 in [1.0,0.05]:
        i=len(a)-1; R=x0/H[i]
        Mdot=(4*np.pi/3)*R**3*rho[i]*(B/T[i])       # dM_de/dt attribue au bord
        Pram=Mdot/(4*np.pi*R**2)*v0
        pde=(B/(3*H[i]*T[i]))*rho[i]
        print(f"   x0={x0} v0={v0:>4} : ratio = {Pram/pde:.6f}  vs x*v0 = {x0*v0:.6f}")
print("   -> exacte. L'intuition tenait par la comptabilite, pas par le mecanisme.")
print()
print("(2) FRICTION DE HUBBLE : profondeur de freinage a 90% (v -> v0/10, soit a -> 10 a_e)")
print(f"   {'z_entree':>9} {'v0':>6} {'d/R (x0=0.1)':>13} {'d/R (x0=0.3)':>13}")
res={}
for ze in [2.0,1.0,0.5]:
    ie=np.argmin(np.abs(1/a-1-ze)); ae=a[ie]
    m=(a>=ae)&(a<=min(10*ae,1.0))
    chi_d=np.trapezoid(1.0*ae/a[m]**2/ (a[m]*H[m]) * a[m], T[m]*0+1)  # placeholder
    # proprement : dchi = v/a dt, v=v0*ae/a  -> chi_d = v0*ae * int dt/a^2
    I=np.trapezoid(1/a[m]**2, T[m][m*0==0] if False else T[m])
    for v0 in [0.05,0.10,0.30]:
        chi=v0*ae*I
        ia=np.argmin(np.abs(a-min(10*ae,1.0)))
        for x0 in [0.1,0.3]:
            Rc=x0/(a[ia]*H[ia])          # chi_b = x0/(a H) a l'instant final
            res[(ze,v0,x0)]=chi/Rc
    print(f"   {ze:>9.1f} {'0.05':>6} {res[(ze,0.05,0.1)]:>13.3f} {res[(ze,0.05,0.3)]:>13.3f}")
    print(f"   {'':>9} {'0.10':>6} {res[(ze,0.10,0.1)]:>13.3f} {res[(ze,0.10,0.3)]:>13.3f}")
    print(f"   {'':>9} {'0.30':>6} {res[(ze,0.30,0.1)]:>13.3f} {res[(ze,0.30,0.3)]:>13.3f}")
print()
print("(3) RETRO-REACTION : (1/2) v0^2 x (fraction de masse dans la couche ~ 3 d/R)")
for v0 in [0.05,0.10,0.30]:
    dR=res[(1.0,v0,0.1)]
    ek=0.5*v0**2*3*dR
    print(f"   v0={v0} : E_cin/rho_de ~ {ek*100:.2f} %  {'OK (<5%)' if ek<0.05 else 'TROP — domaine reduit'}")
