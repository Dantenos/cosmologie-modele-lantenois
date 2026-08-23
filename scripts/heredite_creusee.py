#!/usr/bin/env python3
"""
heredite_creusee.py — Trois questions, dans l'ordre où elles mordent.

Q1. Où tombe l'échelle de nourrissage sous la relation CORRIGÉE beta = 2/(n_eff+3) ?
    (l'ancienne, 4/(n+3), donnait 1,4e16 Msun : plus gros que tout ce qui existe)
Q2. À cette échelle, les graines sont-elles des PICS RARES ? Car la correction d'hier repose
    sur le profil moyen d'un pic (~ xi). Si nu ~ 1 à cette échelle, la justification
    s'effondre sur elle-même : CIRCULARITÉ à vérifier.
Q3. Peut-on SÉPARER le running spectral de la courbure d'horloge ? Ils sont dégénérés au
    premier ordre (beta1 = beta_spectre + beta0 kappa). Mais l'hérédité prédit une forme
    NON LINÉAIRE de beta(ln t), alors qu'une courbure d'horloge simple est linéaire.
    La dérivée seconde beta2 serait donc le discriminant. On la calcule.
"""
import numpy as np, sys
from scipy.optimize import brentq
from gradient_v2 import Cosmo, REF
np.seterr(all='ignore')

c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
H, DC = REF['h'], 1.686

def n_of_M(M):  return c.n_eff(M)
def M_of_n(cible):
    f = lambda lM: c.n_eff(np.exp(lM)) - cible
    return np.exp(brentq(f, np.log(1e6), np.log(1e18), xtol=1e-4))

print("="*78)
print("  Q1. L'ÉCHELLE DE NOURRISSAGE SOUS LA RELATION CORRIGÉE")
print("="*78)
print(f"  {'beta':>7s} {'n_eff = 2/beta-3':>17s} {'M [Msun/h]':>13s} {'M [Msun]':>12s} {'sigma(M)':>9s} {'nu':>6s}")
for b, lab in [(2.42, 'ajustement SN+BAO'), (2.49, 'post-vérification'), (2.56, 'profil Planck'),
               (2.595, 'v3 distance-priors'), (4.35, 'bord GSL')]:
    n = 2/b - 3
    M = M_of_n(n); s = c.sig_M(M)
    print(f"  {b:>7.3f} {n:>17.4f} {M:>13.3e} {M/H:>12.3e} {s:>9.3f} {DC/s:>6.2f}   {lab}")
print()
print("  Rappel : l'ANCIENNE relation 4/(n+3) plaçait la graine à 1,4e16 Msun —")
print("  plus massif que le plus gros amas connu. La correction ramène l'échelle")
print("  à celle d'un halo de galaxie.")
for M in [1e12, 1.5e12]:
    print(f"    repère : halo de la Voie lactée ~ {M:.1e} Msun  ->  n_eff = {n_of_M(M*H):+.3f},"
          f" beta = {2/(n_of_M(M*H)+3):.3f}")

print("\n" + "="*78)
print("  Q2. CIRCULARITÉ ? Les graines sont-elles des pics RARES à cette échelle ?")
print("="*78)
print("  La correction d'hier repose sur : profil initial d'un pic ~ fonction de corrélation.")
print("  Cette approximation (BBKS) est bonne pour nu >> 1. Vérifions nu à l'échelle obtenue.")
n0 = 2/2.42 - 3; M0 = M_of_n(n0); s0 = c.sig_M(M0); nu0 = DC/s0
print(f"    échelle de la graine : M = {M0/H:.2e} Msun, sigma = {s0:.3f}, nu = {nu0:.2f}")
if nu0 < 1.5:
    print(f"    -> nu = {nu0:.2f} : ce ne sont PAS des pics rares. Ce sont des fluctuations typiques.")
    print("    -> l'approximation 'profil de pic ~ xi', qui justifiait la correction, est")
    print("       MAL FONDÉE à l'échelle que cette même correction désigne. CIRCULARITÉ.")
else:
    print(f"    -> nu = {nu0:.2f} : pics rares, l'approximation tient.")
print()
print("  Contre-épreuve : à quelle masse a-t-on nu >= 2,5 (vrais pics rares) ?")
f = lambda lM: DC/c.sig_M(np.exp(lM)) - 2.5
Mrare = np.exp(brentq(f, np.log(1e11), np.log(1e17), xtol=1e-4))
print(f"    nu = 2,5 à M = {Mrare/H:.2e} Msun, où n_eff = {n_of_M(Mrare):+.3f}")
print(f"    -> beta y vaudrait {2/(n_of_M(Mrare)+3):.3f} (lecture pic)"
      f" ou {4/(n_of_M(Mrare)+3):.3f} (lecture rms)")
print(f"    -> mesuré : 2,42-2,60. Comparer.")

print("\n" + "="*78)
print("  Q3. SÉPARER LE RUNNING SPECTRAL DE LA COURBURE D'HORLOGE")
print("="*78)
print("  beta = 2/(n+3) ; dlnM/dlnt = beta. En posant n' = dn/dlnM, n'' = d2n/dlnM^2 :")
print("     dbeta/dlnt   = -(beta^3/2) n'")
print("     d2beta/dln2t = (3 beta^5 /4) n'^2 - (beta^4/2) n''")
print("  Une courbure d'horloge simple donne beta LINÉAIRE en ln t : d2beta/dln2t = 0.")
print("  La dérivée seconde est donc le DISCRIMINANT.")
print()
d = 0.35
print(f"  {'M [Msun]':>11s} {'n_eff':>8s} {'n1':>8s} {'n2':>9s} {'beta':>7s} {'beta1':>8s} {'beta2':>9s}")
for M in [3e11, 5e11, 7e11, 1e12, 3e12, 1e13]:
    Mh = M*H
    n = n_of_M(Mh)
    n1 = (n_of_M(Mh*np.exp(d)) - n_of_M(Mh*np.exp(-d)))/(2*d)
    n2 = (n_of_M(Mh*np.exp(d)) - 2*n + n_of_M(Mh*np.exp(-d)))/d**2
    b = 2/(n+3)
    b1 = -(b**3/2)*n1
    b2 = (3*b**5/4)*n1**2 - (b**4/2)*n2
    print(f"  {M:>11.1e} {n:>8.3f} {n1:>8.4f} {n2:>9.4f} {b:>7.3f} {b1:>8.3f} {b2:>9.3f}")
print()
print("  Mesure actuelle : beta1 = +0,06 +/- 0,31.  beta2 : non contraint (non ajusté).")
print("  Pour que beta2 soit un test, il faut sigma(beta2) < |beta2 prédit|.")
