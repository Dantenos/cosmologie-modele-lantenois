#!/usr/bin/env python3
"""
croissance.py — MANQUEMENT #4 : la prédiction fsigma8, calculée proprement.

Le corpus annonce « fsigma8 supprimé de 1,3-1,9 % (z = 0,15-0,5) » à partir d'un calcul de
perturbation ad hoc. Deux choses ont changé depuis :
  (1) le modèle est identifié comme un modèle de création de particules : la matière n'est PAS
      créée (Gamma_m = 0), donc sa croissance ne répond QU'AU FOND. Le calcul est donc propre
      et sans terme source dans le secteur matière — c'est une simplification, pas une
      approximation.
  (2) la composante injectée a été montrée lisse (agglomération < 1 %), donc elle ne contribue
      pas non plus par ses propres perturbations.

PROTOCOLE : comparer le modèle à LCDM à UNIVERS PRIMORDIAL IDENTIQUE — mêmes omega_b, omega_m,
h, n_s, A_s. Tout écart en sigma_8 aujourd'hui est alors imputable au seul fond tardif.
D(a) normalisée à D -> a en domination de matière (identique pour les deux par construction).

QUESTION DE FOND : le signe. Le modèle a moins d'énergie noire que LCDM à z > 0,5 (croissance
FAVORISÉE) et plus à z < 0,5 (croissance FREINÉE). Le résultat net n'est pas devinable, il se
calcule. S'il est négatif, il va dans le sens de la tension S8 observée — ce qui serait un actif
non remarqué. S'il est positif, il l'aggrave. On écrit ce qui sort.
"""
import numpy as np
from scipy.integrate import solve_ivp

OM, OB, H0, BETA = 0.3113, 0.0493, 68.85, 2.418     # meilleur ajustement v3 du modèle
ZEQ = 3387.0

def fond(Om, beta=None, n=400000):
    """E(a) auto-cohérent. beta=None -> LCDM."""
    Or = Om/(1+ZEQ); Ode = 1-Om-Or
    a = np.logspace(-7, 0, n)
    E2 = Om/a**3 + Or/a**4 + Ode
    if beta is not None:
        for _ in range(10):
            E = np.sqrt(E2); ig = 1/(a*E)
            t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
            E2 = Om/a**3 + Or/a**4 + Ode*np.clip(t, 1e-300, None)**beta/a**3
    return a, np.sqrt(E2)

def croissance(a, E):
    """D'' + (3/a + dlnE/da) D' - (3 Om(a)/(2 a^2)) D = 0, normalisée D -> a tôt."""
    lnE = np.log(E)
    dlnEdlna = np.gradient(lnE, np.log(a))
    Om_a = OM/a**3/E**2
    def f(la, y):
        A = np.exp(la)
        e = np.interp(la, np.log(a), dlnEdlna)
        om = np.interp(la, np.log(a), Om_a)
        D, Dp = y
        return [Dp, -(2 + e)*Dp + 1.5*om*D]      # en variable ln a
    la0 = np.log(a[0])
    s = solve_ivp(f, [la0, 0.0], [np.exp(la0), np.exp(la0)], rtol=1e-10, atol=1e-14,
                  dense_output=True, method='DOP853')
    return s

print("="*80)
print("  CROISSANCE : modèle d'accrétion contre LCDM, univers primordial IDENTIQUE")
print("="*80)
a_m, E_m = fond(OM, BETA)
a_l, E_l = fond(OM, None)
s_m, s_l = croissance(a_m, E_m), croissance(a_l, E_l)

def fs8(s, a, E, z, s8_norm):
    la = np.log(1/(1+z))
    D, Dp = s.sol(la)
    f = Dp/D                                   # dlnD/dlna
    return f*s8_norm*D/s.sol(0.0)[0]           # sigma8(z) = sigma8_0 D(z)/D(0)

D0_m, D0_l = s_m.sol(0.0)[0], s_l.sol(0.0)[0]
print(f"  D(a=1) modèle = {D0_m:.6f} | LCDM = {D0_l:.6f} | rapport = {D0_m/D0_l:.6f}")
print(f"  => à A_s identique, sigma_8 est modifié de {(D0_m/D0_l-1)*100:+.3f} %")
print(f"     et S_8 = sigma_8 sqrt(Om/0,3) du même facteur (Om identique) : {(D0_m/D0_l-1)*100:+.3f} %")

fl0 = s_l.sol(0.0)[1]/s_l.sol(0.0)[0]
print(f"  CONTROLE : f_LCDM(0) = {fl0:.4f} ; Om^0.55 = {OM**0.55:.4f} ; ecart {abs(fl0/OM**0.55-1)*100:.2f} %")
assert abs(fl0/OM**0.55-1) < 0.03, "equation de croissance fausse"
print("\n" + "="*80)
print("  fsigma_8(z) : modèle contre LCDM (sigma_8 = 0,811 imposé à LCDM)")
print("="*80)
S8L = 0.811
S8M = S8L*D0_m/D0_l
print(f"  {'z':>6s} {'fs8 LCDM':>10s} {'fs8 modèle':>11s} {'écart':>9s} {'f modèle':>9s} {'w(z)':>8s}")
# w(z) du modèle
Or = OM/(1+ZEQ); Ode = 1-OM-Or
E = E_m; ig = 1/(a_m*E)
t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a_m))]); t /= t[-1]
Ht = E*t/(E[-1]*t[-1])*0.9501
for z in [0.0, 0.15, 0.3, 0.5, 0.8, 1.0, 1.5]:
    A = 1/(1+z); la = np.log(A)
    Dm, Dpm = s_m.sol(la); Dl, Dpl = s_l.sol(la)
    fm, fl = Dpm/Dm, Dpl/Dl
    v_m = fm*S8M*Dm/D0_m; v_l = fl*S8L*Dl/D0_l
    w = -BETA/(3*np.interp(A, a_m, Ht))
    print(f"  {z:>6.2f} {v_l:>10.5f} {v_m:>11.5f} {(v_m/v_l-1)*100:>8.2f}% {fm:>9.4f} {w:>8.3f}")

print("\n" + "="*80)
print("  CONTRÔLE : le fond fait-il bien ce qu'on croit ?")
print("="*80)
print(f"  {'z':>6s} {'rho_de/rho_Lambda,0':>19s} {'LCDM (=1)':>10s} {'E modèle/E LCDM':>17s}")
for z in [0.0, 0.5, 1.0, 2.0, 3.0]:
    A = 1/(1+z)
    r = np.interp(A, a_m, np.clip(t, 1e-300, None)**BETA)/A**3
    Em = np.interp(A, a_m, E_m); El = np.interp(A, a_l, E_l)
    print(f"  {z:>6.2f} {r:>19.4f} {1.0:>10.1f} {Em/El:>17.6f}")
