#!/usr/bin/env python3
"""
derivation_beta.py — Le manquement #25, dérivé au lieu d'être choisi.

QUESTION : le papier B pose beta = 4/(n_eff+3) et évalue n_eff via un appariement k <-> M
(R = pi/k), d'où un facteur pi^3 = 31 sur toutes les masses de graines et trois résultats de
tête suspendus à une convention non déclarée. Il fallait DÉRIVER la relation.

SOURCES PRIMAIRES LUES :
  - Fillmore & Goldreich 1984, ApJ 281, 1 : perturbation initiale caractérisée par
    delta M_i / M_i = (M_i/M_0)^{-epsilon}, où M_i = (4/3) pi rho_H r_i^3 est la masse
    NON PERTURBÉE dans r_i.  [arXiv:astro-ph/9904364 §2.1 reproduit la définition]
  - En EdS, ce profil implique une croissance en loi de puissance m ∝ a^s avec s = 1/epsilon
    [arXiv:1603.07183 §2, citant FG84]
  - Bertschinger 1985, ApJS 58, 39 : le rayon de retournement croît en t^{8/9} et la masse
    en t^{2/3}.  -> ANCRAGE DE VÉRIFICATION (cas epsilon = 1)

DÉRIVATION : EdS, a ∝ t^{2/3} ; M ∝ a^{1/epsilon} = t^{2/(3 epsilon)}. Donc
        beta = 2/(3 epsilon).
Vérification : epsilon = 1 -> beta = 2/3, soit M ∝ t^{2/3}. C'est exactement Bertschinger.

LE POINT DÉCISIF POUR LA CONVENTION : epsilon est défini comme une pente logarithmique
EN MASSE (delta M/M en fonction de la masse enfermée). Aucun nombre d'onde n'intervient.
La question « R = 1/k ou pi/k ou 2pi/k ? » ne se pose donc PAS : elle a été créée en
évaluant dlnP/dlnk à un k assigné à une masse, étape que la dérivation n'exige jamais.

LA VRAIE AMBIGUÏTÉ, elle, est ailleurs et vaut un facteur 2 sur beta lui-même :
  (A) si delta M/M au seuil de masse M est la fluctuation RMS : sigma(M) ∝ M^{-(n+3)/6},
      donc epsilon = (n+3)/6 et beta = 4/(n+3)   <- la relation du papier B
  (B) si c'est le profil MOYEN autour d'un pic, qui suit la fonction de corrélation
      xi_barre ∝ sigma^2 ∝ M^{-(n+3)/3}, alors epsilon = (n+3)/3 et beta = 2/(n+3)
"""
import numpy as np, sys
from gradient_v2 import Cosmo, REF
from scipy.optimize import brentq

np.seterr(all='ignore')
c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
H = REF['h']

print("="*80)
print("  1. LA FORMULE, ET SON ANCRAGE SUR BERTSCHINGER 1985")
print("="*80)
print("     beta = 2/(3 epsilon)")
for eps, att in [(1.0, "Bertschinger : M ∝ t^{2/3}"), (2/3, "bord FG du profil r^-2"), (0.5, "-")]:
    print(f"     epsilon = {eps:.4f} -> beta = {2/(3*eps):.4f}   {att}")
print("     epsilon = 1 redonne 2/3 EXACTEMENT. La formule est ancrée.")

print("\n" + "="*80)
print("  2. LES DEUX LECTURES DE epsilon, ET LE FACTEUR 2 SUR beta")
print("="*80)
print(f"     {'n_eff':>7s} {'(A) rms: beta=4/(n+3)':>23s} {'(B) pic: beta=2/(n+3)':>23s}")
for n in [-2.5, -2.08, -2.0, -1.5, -1.347, -1.0, 0.0, 0.9649, 1.0]:
    print(f"     {n:>7.3f} {4/(n+3):>23.4f} {2/(n+3):>23.4f}")

print("\n" + "="*80)
print("  3. CE QUE DEVIENT NOTRE beta = 2,42 MESURÉ")
print("="*80)
for lab, k in [("(A) rms  [papier B]", 4.0), ("(B) pic  [corrélation]", 2.0)]:
    for b in [2.42, 2.56, 4.35]:
        n = k/b - 3
        print(f"     {lab:24s} beta = {b:.2f} -> n_eff = {n:+.4f}")
    print()

print("="*80)
print("  4. OÙ CES n_eff TOMBENT EN MASSE (convention sigma, la seule requise)")
print("="*80)
def M_de_neff(cible):
    f = lambda lM: c.n_eff(np.exp(lM)) - cible
    try: return np.exp(brentq(f, np.log(1e6), np.log(1e18), xtol=1e-3))
    except ValueError: return np.nan
print(f"     {'lecture':>22s} {'beta':>6s} {'n_eff':>8s} {'M [Msun/h]':>12s} {'M [Msun]':>12s}")
for lab, k in [("(A) rms", 4.0), ("(B) pic", 2.0)]:
    for b, nom in [(2.42, "notre beta"), (4.35, "bord GSL")]:
        n = k/b - 3; M = M_de_neff(n)
        print(f"     {lab+' '+nom:>22s} {b:>6.2f} {n:>8.3f} {M:>12.3e} {M/H:>12.3e}")
print(f"\n     Pour mémoire, le papier B annonce : graines a 5/2 = 1,4e16 Msun ;"
      f" M_cut = 2,5e14 Msun.")

print("\n" + "="*80)
print("  5. CONSÉQUENCE SUR LA FERMETURE TEMPORELLE (résultat (i) du papier B)")
print("="*80)
V = 6.225e12       # volume implicite du papier B, (Mpc/h)^3
for lab, k in [("(A) rms", 4.0), ("(B) pic", 2.0)]:
    n = k/2.5 - 3                       # graines a beta = 5/2
    M = M_de_neff(n)
    N = c.F(M)*V
    print(f"     {lab} : graines a beta=5/2 -> n_eff={n:+.3f}, M={M:.2e} Msun/h,"
          f" N(z=0) = {N:.3e}")
print(f"     Le papier B annonce N(z=0) = 0,007, d'où « elles n'existent pas encore ».")

print("\n" + "="*80)
print("  6. LA LIMITE SUPER-HORIZON (résultat (ii) du papier B)")
print("="*80)
print("     Le papier : une graine de masse-univers voit le spectre primordial nu, n_eff -> n_s,")
print("     donc beta -> 4/(n_s+3) = 1,009 pour n_s = 0,9649, et beta = 1 EXACTEMENT si n_s = 1.")
for lab, k in [("(A) rms", 4.0), ("(B) pic", 2.0)]:
    print(f"     {lab} : beta(n_s=0,9649) = {k/(REF['ns']+3):.4f} ; beta(n_s=1) = {k/4:.4f}")
print("     -> l'identité « invariance d'échelle primordiale <=> beta = 1 » n'existe QUE")
print("        sous la lecture (A). Sous (B) elle donne 1/2. Elle est conventionnelle.")
