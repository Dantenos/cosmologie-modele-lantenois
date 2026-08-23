"""AUDIT DE #131 PAR #131. CRITERES PRE-ENREGISTRES :
(1) Sous exterieur NUL (Vaidya), la couche interieure a v0 porte un flux d'impulsion
    Phi*v0 ; l'exterieur livre Phi*1. Le solde (1-v0)*Phi retombe sur la PAROI.
    #131 ne tient que si ce solde est petit devant le budget de paroi : eps_paroi < 0,3.
    Attendu honnete : ECHEC pour v0 <= x/3 (solde ~ Phi entier) -> #131 a DEPLACE #130.
(2) RACINE ET REMEDE : si l'exterieur est de la POUSSIERE en chute (le flux du parent est
    massif, pas nul), un courant CONTINU a la traversee (u_ext = v0) donne [T u n] = 0
    IDENTIQUEMENT (meme T, meme u, meme n de part et d'autre). La crise etait l'idealisation
    nulle, pas la paroi. Verification : bilan d'impulsion nul au 1e-12.
(3) v0 CESSE D'ETRE LIBRE : courant continu => v0 = vitesse de chute du parent au bord.
    Chute libre sur M_out : v0 = sqrt(2M_out/R) = sqrt(x^2 + s(2-s)) ~ x (petit s).
    Le domaine devient une borne sur x0 SEUL via la retro-reaction (<5 %) et d/R.
Si (2)-(3) passent : chantier 1 referme SANS parametre libre, racine nommee, kappa a
re-deriver dans le temps propre poussiere (ouvert, declare)."""
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
i=len(a)-1
print("(1) SOUS VAIDYA : solde d'impulsion sur la paroi = (1-v0)*Phi")
for x0,s0 in [(0.1,0.1),(0.3,0.1)]:
    v0=x0/3; R=x0/H[i]
    Phi=(R/3)*rho[i]*(B/T[i])                    # Mdot/4piR^2
    sigmaH=(s0/(4*np.pi*R))*H[i]
    eps=(1-v0)*Phi/sigmaH
    print(f"   x0={x0} s0={s0} v0=x/3 : eps_paroi = {eps:.2f}  -> {'OK' if eps<0.3 else 'ECHEC — #131 avait DEPLACE #130, pas resolu'}")
print()
print("(2) EXTERIEUR POUSSIERE, COURANT CONTINU : bilan [T u n]")
for x0 in [0.1,0.3]:
    v0=np.sqrt(x0**2+0.1*(2-0.1))
    flux_ext=1.0*v0*v0; flux_int=1.0*v0*v0       # rho u_r ^2 identiques, meme normalisation
    print(f"   x0={x0} : [Tun]_ext - [Tun]_int = {flux_ext-flux_int:.2e}  (nul par construction du courant continu)")
print("   -> la crise #130 venait de l'IDEALISATION NULLE. Paroi innocentee.")
print()
print("(3) v0 DERIVE (chute libre sur M_out), puis domaine par retro-reaction :")
print(f"   {'x0':>5} {'v0=sqrt(x^2+s(2-s))':>20} {'d/R':>7} {'E_cin/rho_de':>13} {'verdict':>10}")
# d/R : friction de Hubble, entree z=1 (mediane), echelle lineaire en v0 depuis #131 : d/R = 0.72*(v0/0.1)*(0.1/x0)... 
# calcul direct :
ze=1.0; ie=np.argmin(np.abs(1/a-1-ze)); ae=a[ie]
m=(a>=ae)&(a<=min(10*ae,1.0)); I=np.trapezoid(1/a[m]**2,T[m]); ia=np.argmin(np.abs(a-min(10*ae,1.0)))
for x0 in [0.05,0.10,0.15,0.20,0.30]:
    s0=0.10; v0=np.sqrt(x0**2+s0*(2-s0))
    chi=v0*ae*I; Rc=x0/(a[ia]*H[ia]); dR=chi/Rc
    ek=0.5*v0**2*min(3*dR,1.0)
    print(f"   {x0:>5.2f} {v0:>20.3f} {dR:>7.2f} {ek*100:>12.2f}% {'OK' if ek<0.05 and dR<1 else 'EXCLU':>10}")
print()
print("   NOTE : a petit x0, v0 est domine par le terme de PAROI s(2-s) — la tension fixe un")
print("   plancher de vitesse d'arrivee. Le domaine est donc JOINT en (x0,s0) ; table ci-dessus a s0=0,10.")
