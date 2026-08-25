#!/usr/bin/env python3
"""
convention.py — Sous quel appariement k <-> M les nombres du papier B sont-ils vrais ?

Le papier B fixe deux ancrages spectraux :
   (a) n_eff = -1.4  (notre beta)      a  M ~ 1.4e16 M_sun, "30-40 Mpc/h", k = 0.08-0.1 h/Mpc
   (b) n_eff = -2.08 (borne GSL)       a  M_cut ~ 2.5e14 M_sun
et en tire trois resultats de tete : R ~ 10^7.6 enfants viables, "la thermodynamique
elimine 99,6 %", et la fermeture TEMPORELLE (les graines a 5/2 n'existent pas encore,
N(z=0) = 0,007, donc la reproduction exige la fin du festin).

Tout cela passe par le rayon associe a un nombre d'onde. Trois appariements sont
defendables dans la litterature. On les teste tous les trois.
"""
import numpy as np
from scipy.optimize import brentq
from gradient_v2 import Cosmo, REF, DELTA_C, LNK, K

np.seterr(all='ignore')
c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
lnP = np.log(c.P)

def n_eff_k(k, d=0.08):
    return (np.interp(np.log(k) + d, LNK, lnP) - np.interp(np.log(k) - d, LNK, lnP)) / (2 * d)

def M_pour_neff(cible, facteur):
    """Masse dont le rayon lagrangien R_L verifie n_eff(k = facteur/R_L) = cible."""
    f = lambda lM: n_eff_k(facteur / c.R_of_M(np.exp(lM))) - cible
    return np.exp(brentq(f, np.log(1e8), np.log(1e19), xtol=1e-3))

# volume implicite du papier B : il annonce 2e8 halos au-dessus de 1e14
V_papier = 2e8 / c.F(1e14)
V_horizon = 4 * np.pi / 3 * 9400.0 ** 3          # horizon des particules ~ 9400 Mpc/h

print("=" * 84)
print("  APPARIEMENT k <-> M : trois conventions defendables, trois mondes differents")
print("=" * 84)
print(f"  volume implicite du papier B = {V_papier:.3e} (Mpc/h)^3"
      f"   [horizon des particules : {V_horizon:.3e}]")
print(f"\n  {'convention':>16s} {'M(n_eff=-2.08)':>15s} {'M(n_eff=-1.4)':>14s} "
      f"{'N(>M_cut)':>11s} {'N(>M_5/2)':>11s} {'elimine':>9s}")
lignes = []
for nom, fac in [('k = 1/R_L', 1.0), ('k = pi/R_L', np.pi), ('k = 2pi/R_L', 2 * np.pi)]:
    try:
        Mcut = M_pour_neff(-2.08, fac); M52 = M_pour_neff(-1.40, fac)
    except ValueError:
        print(f"  {nom:>16s}   hors plage de masse tabulee (echelle trop grande)"); continue
    N_cut = c.F(Mcut) * V_papier
    N_52 = c.F(M52) * V_papier
    N_naif = c.F(1e8) * V_papier                      # tous les halos hotes de trou noir
    elim = 1.0 - N_cut / N_naif
    lignes.append((nom, Mcut, M52, N_cut, N_52, elim))
    print(f"  {nom:>16s} {Mcut:>15.3e} {M52:>14.3e} {N_cut:>11.3e} {N_52:>11.3e} {elim*100:>8.2f}%")

print("\n  Le papier B annonce : M_cut = 2,5e14 ; M_5/2 = 1,4e16 ; N(>M_cut) = 4e7 ;")
print("                        N(>M_5/2) = 0,007 ; elimination = 99,6 %")
print("\n  --> l'appariement qui reproduit les nombres publies est celui du milieu (k = pi/R_L).")

print("\n" + "=" * 84)
print("  CE QUI CHANGE SI L'ON PREND k = 1/R_L (appariement le plus courant pour n_eff)")
print("=" * 84)
n1, n2 = lignes[0], lignes[1]
print(f"  M_cut          : {n2[1]:.2e}  ->  {n1[1]:.2e}     (facteur {n1[1]/n2[1]:.3g})")
print(f"  R (enfants)    : 10^{np.log10(n2[3]):.1f}       ->  10^{np.log10(n1[3]):.1f}")
print(f"  elimination    : {n2[5]*100:.2f} %     ->  {n1[5]*100:.2f} %")
print(f"  N(> M_5/2)     : {n2[4]:.3g}      ->  {n1[4]:.3g}")
print("\n  Consequence sur la FERMETURE TEMPORELLE (resultat (i) du papier B) :")
if n1[4] > 1:
    print(f"     sous k = 1/R_L, il existe deja {n1[4]:.3g} environnements-graines a 5/2")
    print("     dans le volume observable. L'argument 'ils n'existent pas encore, donc la")
    print("     reproduction exige la fin du festin' NE TIENT PLUS sous cette convention.")
print("\n  Consequence sur la SELECTION THERMODYNAMIQUE (resultat (i), seconde moitie) :")
print(f"     'la thermodynamique elimine 99,6 %' devient '{n1[5]*100:.1f} %' : la coupure")
print("     descend a l'echelle des groupes, et le tri thermodynamique perd sa force.")

print("\n" + "=" * 84)
print("  DIAGNOSTIC")
print("=" * 84)
print("  Les deux ancrages du papier B sont MUTUELLEMENT COHERENTS : ils utilisent tous")
print("  deux R = pi/k. Il n'y a donc pas de faute de calcul interne.")
print("  Mais ce rayon est ensuite injecte dans sigma(M) et dans Press-Schechter, qui sont")
print("  definis avec le rayon lagrangien top-hat R_L = (3M/4 pi rho_m)^(1/3).")
print("  Melanger les deux deplace toutes les masses de graines d'un facteur pi^3 = 31.")
print(f"  Verification : {n2[1]/n1[1]:.1f} observe contre {np.pi**3:.1f} attendu.")
print("  [NOTE audit §6.5] ce rapport EST l'identite de conversion entre les deux conventions,")
print("  PAS une verification independante (audit_v2 l'a declare circulaire) : conserve comme")
print("  illustration du facteur, non compte comme un test.")
print("  Le corpus ne declare nulle part quelle convention il retient, ni ne teste la")
print("  sensibilite. Trois resultats de tete en dependent. C'est un manquement, pas")
print("  necessairement une erreur : la litterature admet 1/R, pi/R et 2 pi/R.")
