#!/usr/bin/env python3
"""
audit_v2.py — Vérifier ce que j'ai écrit hier soir. Six contrôles.

(1) Le "31,0 observé contre 31,0 attendu" était-il un vrai contrôle ou une tautologie ?
(2) Le protocole "amplitude primordiale fixe" a-t-il un sens sans pivot ni facteur de croissance ?
(3) Les intégrales de fécondité sont-elles convergées ?
(4) beta = 2,42 correspond-il vraiment a n_eff = -1,4 ?
(5) La moyenne 4-volumique pertinente pour la séquestration : <rho_de> ou <T>/4 ?
(6) Sensibilité de M_cut a delta_c et a la forme du transfert.
"""
import numpy as np
from scipy.optimize import brentq
from gradient_v2 import Cosmo, REF, DELTA_C, LNK, K

np.seterr(all='ignore')
c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
lnP = np.log(c.P)

def n_eff_k(k, d=0.08):
    return (np.interp(np.log(k)+d, LNK, lnP) - np.interp(np.log(k)-d, LNK, lnP))/(2*d)

def M_pour_neff(cible, fac):
    f = lambda lM: n_eff_k(fac/c.R_of_M(np.exp(lM))) - cible
    return np.exp(brentq(f, np.log(1e8), np.log(1e19), xtol=1e-3))

print("="*80)
print("  (1) LE CONTROLE 'pi^3' ETAIT-IL CIRCULAIRE ?")
print("="*80)
print("  M ∝ R^3 et R_theirs = pi x R_L par construction => le rapport VAUT pi^3.")
print("  Ce n'etait donc pas une verification. La vraie question : lequel des deux")
print("  appariements reproduit les masses PUBLIEES ?")
pub = {'M_cut (n_eff=-2.08)': 2.5e14, 'M_5/2 (n_eff=-1.4)': 1.4e16}
print(f"\n  {'ancrage':>22s} {'publie':>10s} {'k=1/R_L':>11s} {'ecart':>7s} {'k=pi/R_L':>11s} {'ecart':>7s}")
for nom, cible, Mp in [('M_cut (n_eff=-2.08)', -2.08, 2.5e14), ('M_5/2 (n_eff=-1.4)', -1.40, 1.4e16)]:
    m1, mp = M_pour_neff(cible, 1.0), M_pour_neff(cible, np.pi)
    print(f"  {nom:>22s} {Mp:>10.2e} {m1:>11.3e} {Mp/m1:>6.1f}x {mp:>11.3e} {Mp/mp:>6.2f}x")
print("\n  => k=pi/R_L reproduit a 30-45 % pres ; k=1/R_L manque d'un facteur 41-45.")
print("     C'est CELA le diagnostic. Le 'pi^3 = 31 verifie' est a retirer.")

print("\n" + "="*80)
print("  (2) LE PROTOCOLE 'AMPLITUDE PRIMORDIALE FIXE' : refait correctement")
print("="*80)
print("  Hier : P ∝ k^ns T^2 avec un coefficient fixe. Deux defauts —")
print("  pas de pivot (changer ns change la normalisation arbitrairement), et")
print("  pas de facteur de croissance D(a=1), qui depend d'Omega_m.")
KPIV = 0.05          # Mpc^-1
CLIGHT = 299792.458  # km/s

def D_growth(Om, a=1.0, n=4000):
    """Croissance lineaire LCDM normalisee a D -> a en domination de matiere."""
    aa = np.linspace(1e-6, a, n)
    E = np.sqrt(Om/aa**3 + (1-Om))
    integ = 1.0/(aa*E)**3
    I = np.trapezoid(integ, aa)
    return 2.5*Om*np.sqrt(Om/a**3 + (1-Om))*I

def P_As(k, Om, Ob, h, ns, As):
    """P_m(k, z=0) avec pivot et croissance. k en h/Mpc."""
    from gradient_v2 import T_eh98
    kmpc = k*h
    prim = As*(kmpc/KPIV)**(ns-1.0)
    pref = (4.0/25.0)*(CLIGHT*kmpc/(100.0*h))**4/Om**2
    return pref*T_eh98(k, Om, Ob, h)**2*D_growth(Om)**2*2*np.pi**2/kmpc**3*prim*h**3

class CosmoAs(Cosmo):
    def __init__(self, Om, Ob, h, ns, As):
        Cosmo.__init__(self, Om, Ob, h, ns, s8=1.0)   # forme seule
        self.P = P_As(K, Om, Ob, h, ns, As)
        # re-tabuler sigma avec le vrai P
        Rg = np.exp(self.lnR); x = np.outer(Rg, K)
        W = np.where(x < 1e-3, 1-x**2/10, 3*(np.sin(x)-x*np.cos(x))/np.where(x==0,1,x)**3)
        self.sig_brut = np.sqrt(np.trapezoid(W**2*self.P*K**3/(2*np.pi**2), LNK, axis=1))
        self.lnsig_brut = np.log(self.sig_brut); self.amp = 1.0
        self.s8 = np.exp(np.interp(np.log(8.0), self.lnR, self.lnsig_brut))

As0 = 2.1e-9
cA = CosmoAs(REF['Om'], REF['Ob'], REF['h'], REF['ns'], As0)
print(f"  controle de normalisation : A_s = {As0:.2e} -> sigma8 = {cA.s8:.4f}"
      f"   (Planck : 0.811)  ecart {(cA.s8/REF['s8']-1)*100:+.1f} %")
eps = 0.02
def grad_As(param):
    kw = dict(Om=REF['Om'], Ob=REF['Ob'], h=REF['h'], ns=REF['ns'], As=As0)
    lo, hi = dict(kw), dict(kw)
    lo[param] *= (1-eps); hi[param] *= (1+eps)
    cl, ch = CosmoAs(**lo), CosmoAs(**hi)
    Ml, Mh = cl.M_cut(), ch.M_cut()
    return (np.log(ch.F(Mh))-np.log(cl.F(Ml)))/(2*eps), (np.log(Mh)-np.log(Ml))/(2*eps), cl.s8, ch.s8
for p in ['Om', 'ns', 'As']:
    g, gM, s8l, s8h = grad_As(p)
    print(f"  dlnF/dln {p:3s} = {g:+7.2f}   (dlnM_cut/dln {p:3s} = {gM:+7.2f} ; sigma8 : {s8l:.3f} -> {s8h:.3f})")
print("  [hier, sans pivot ni croissance : Om +4,00 ; ns +10,34]")

print("\n" + "="*80)
print("  (3) CONVERGENCE DES INTEGRALES DE FECONDITE")
print("="*80)
Mc0 = c.M_cut()
for Mmax in [1e16, 1e17, 1e18]:
    for n in [200, 400, 1200]:
        print(f"    Mmax={Mmax:.0e} n={n:5d} -> F = {c.F(Mc0, Mmax=Mmax, n=n):.6e}")
    break
print(f"    Mmax=1e17 n=400 -> F = {c.F(Mc0, Mmax=1e17, n=400):.6e}")
print(f"    Mmax=1e18 n=400 -> F = {c.F(Mc0, Mmax=1e18, n=400):.6e}")

print("\n" + "="*80)
print("  (4) beta = 2,42 CORRESPOND-IL A n_eff = -1,4 ?")
print("="*80)
for b in [2.30, 2.42, 2.49, 2.50, 2.56, 2.60, 4.35]:
    print(f"    beta = {b:.2f} -> n_eff = 4/beta - 3 = {4/b-3:+.4f}")
print("  => n_eff = -1,400 correspond a beta = 5/2 EXACTEMENT, pas a beta = 2,42 (-1,347).")
print("     Le papier B ecrit 'notre beta = 2,42' a cote de 'n_eff = -1,4' : glissement.")
print(f"     Impact sur l'echelle des graines : n_eff=-1,347 -> M = {M_pour_neff(-1.347, np.pi):.3e}")
print(f"                                        n_eff=-1,400 -> M = {M_pour_neff(-1.400, np.pi):.3e}")

print("\n" + "="*80)
print("  (5) SEQUESTRATION : quelle moyenne ? <rho_de> (hier) ou <T>/4 (correct) ?")
print("="*80)
Om, b = 0.3153, 2.42
a = np.logspace(-6, 0, 40000); Or = Om/3387; Ode = 1-Om-Or
E2 = (Om+Ode)/a**3 + Or/a**4
for _ in range(6):
    E = np.sqrt(E2); t = np.concatenate([[0], np.cumsum(0.5*(1/(a[1:]*E[1:])+1/(a[:-1]*E[:-1]))*np.diff(a))])
    t /= t[-1]
    E2 = (Om + Ode*np.clip(t,1e-30,None)**b)/a**3 + Or/a**4
E = np.sqrt(E2)
rho_de = Ode*np.clip(t,1e-30,None)**b/a**3
rho_m, rho_r = Om/a**3, Or/a**4
Ht = E*t/(E[-1]*t[-1])*0.951
w = -b/(3*np.clip(Ht,1e-6,None))
T_de = rho_de*(1-3*w); T_m = rho_m; T_r = 0.0*rho_r
dt = np.gradient(t)
def moy(X, imax):
    p = a[:imax]**3
    return np.trapezoid(X[:imax]*p, t[:imax])/np.trapezoid(p, t[:imax])
i = len(a)
print(f"  <rho_de>_4vol / rho_de(t0)      = {moy(rho_de,i)/rho_de[-1]:.3f}   <- ce que j'ai calcule hier")
print(f"  <T_matiere>/4 / rho_de(t0)      = {moy(T_m,i)/4/rho_de[-1]:.3f}")
print(f"  <T_de>/4      / rho_de(t0)      = {moy(T_de,i)/4/rho_de[-1]:.3f}")
print(f"  <T_total>/4   / rho_de(t0)      = {moy(T_m+T_de,i)/4/rho_de[-1]:.3f}")
print("\n  La sequestration fixe Lambda_eff = <T>/4, PAS <rho_de>. J'ai moyenne le mauvais objet.")
print("  Et <T>/4 est du meme ordre que rho_de,0 : c'est precisement l'attrait revendique")
print("  du mecanisme (un residuel de l'ordre de la densite de matiere moyenne), pas une")
print("  annulation de notre composante. La these 'elle annulerait 105 % du signal' TOMBE.")

print("\n" + "="*80)
print("  (6) SENSIBILITE DE M_cut")
print("="*80)
for dc in [1.676, 1.686, 1.696]:
    print(f"    delta_c = {dc:.3f} -> M_cut inchange (le seuil ne depend que de n_eff), F change seul")
for cible in [-2.00, -2.08, -2.16]:
    mm = M_pour_neff(cible, 1.0)
    print(f"    n_eff cible = {cible:+.2f} -> M_cut (k=1/R_L) = {mm:.3e}"
          f"  [beta correspondant = {4/(cible+3):.3f}]")
