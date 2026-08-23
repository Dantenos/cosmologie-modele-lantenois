#!/usr/bin/env python3
"""
voile_cisaillement.py — Le canal que le corpus n'a jamais calcule : le cisaillement SOURCE.

CE QUE LE CORPUS AVAIT. Une borne STATIQUE : quadrupole de potentiel transmis (Laplace,
facteur 0,58), compare "aux anomalies a grand angle (~20 %)" -> epsilon <~ 0,35. Normalisation
douteuse, et surtout : c'est le mauvais canal. L'injection est CONTINUE. Une injection
anisotrope source du cisaillement de Bianchi I A CHAQUE INSTANT de l'ere d'energie noire,
et le quadrupole CMB integre ce cisaillement depuis la derniere diffusion.

CADRE ETABLI (Koivisto & Mota 2008 ; Campanelli et al. ; "Probing DE anisotropy" ;
"How isotropic is dark energy?", arXiv:2601.22351, PRD 2026) :
  - skewness delta de la pression d'energie noire -> cisaillement Sigma = sigma/H
  - (DT/T)_quadrupole ~ delta x J(Omega_m, w), J = O(1)
  - bornes publiees pour w constant : |delta| ~ 1e-4  <->  |Sigma_0| ~ 1e-5
  - le shear standard LCDM decroit en 1/volume (1e-9 aujourd'hui) ; un shear source
    APRES le decouplage echappe a cette dilution — c'est exactement notre cas.

METHODE PAR CALIBRATION (la seule qui evite mes facteurs O(1)) :
  sigma' + 3 H sigma = C x 8 pi G rho_de(t) delta        [meme C pour les deux histoires]
  K := int_{t_ls}^{t0} sigma dt / delta                  [reponse quadrupolaire par unite de delta]
  borne_notre = borne_publiee x K_std / K_notre
On ne fixe JAMAIS C ni la normalisation absolue du quadrupole : ils s'annulent dans le rapport.

CRITERE PRE-ENREGISTRE :
  - controle : pour w = -1 (rho_de constante), Sigma_0/delta doit etre O(0,1-1) et K_std O(0,1-1)
    en unites de Hubble ; sinon l'equation est fausse et rien n'est exploite.
  - le rapport K_notre/K_std decide de tout ; s'il est O(1), la borne publiee s'applique
    a nous quasi telle quelle.
"""
import numpy as np
np.seterr(all='ignore')

OM, BETA, ZEQ = 0.3113, 2.42, 3387.0
ZLS = 1090.0

def fond(beta=None, n=400000):
    Or = OM/(1+ZEQ); Ode = 1-OM-Or
    a = np.logspace(-7, 0, n)
    E2 = OM/a**3 + Or/a**4 + Ode
    if beta is not None:
        for _ in range(10):
            E = np.sqrt(E2); ig = 1/(a*E)
            t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
            E2 = OM/a**3 + Or/a**4 + Ode*np.clip(t, 1e-300, None)**beta/a**3
    E = np.sqrt(E2); ig = 1/(a*E)
    t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
    if beta is None:
        rho_de = np.full_like(a, Ode)
    else:
        rho_de = Ode*np.clip(t, 1e-300, None)**beta/a**3
    return a, E, t, rho_de   # rho_de en unites de rho_crit,0 ; E = H/H0 ; t en unites de t0

def K_reponse(a, E, t, rho_de, t0H0):
    """Resout sigma' + 3H sigma = 8 pi G rho_de delta (C=1, delta=1), integre depuis a_ls.
       Unites : temps en 1/H0. 8 pi G rho_de / (3 H0^2) = Omega_de(t) x ... -> source = 3 rho_de
       (rho_de en unites critiques : 8 pi G rho / 3 H0^2 = rho/rho_c0). On pose source = 3*rho_de."""
    T = t*t0H0
    m = a > 1/(1+ZLS)
    Tm, Em, Rm = T[m], E[m], rho_de[m]
    sig = np.zeros_like(Tm)
    for i in range(1, len(Tm)):
        dt = Tm[i]-Tm[i-1]
        src = 3*Rm[i-1]                      # x delta, x C : identiques entre modeles
        sig[i] = sig[i-1] + dt*(src - 3*Em[i-1]*sig[i-1])
        # implicite si raideur
        sig[i] = (sig[i-1] + dt*src)/(1 + 3*Em[i]*dt)
    K = np.trapezoid(sig, Tm)               # (DT/T)_2 par unite de delta (a C pres)
    return K, sig[-1]                        # K et Sigma_0 = sigma(t0)/H0

print("="*78)
print("  CANAL DE CISAILLEMENT SOURCE : reponse quadrupolaire par unite de skewness")
print("="*78)
a1, E1, t1, r1 = fond(None)      # Lambda : rho_de constante (le cas des bornes publiees)
a2, E2, t2, r2 = fond(BETA)      # notre injection
K1, S1 = K_reponse(a1, E1, t1, r1, 0.951)
K2, S2 = K_reponse(a2, E2, t2, r2, 0.951)
print(f"  w constant (-1), rho_de constante : K_std   = {K1:.4f}   Sigma_0/delta = {S1:.4f}")
print(f"  accretion beta = {BETA}             : K_notre = {K2:.4f}   Sigma_0/delta = {S2:.4f}")
print(f"  CONTROLE pre-enregistre : K_std et Sigma/delta doivent etre O(0,1-1) : "
      f"{'PASSE' if 0.05 < K1 < 3 and 0.05 < S1 < 3 else 'ECHEC — rien exploite'}")
print(f"\n  RAPPORT K_notre/K_std = {K2/K1:.3f}")
print(f"  -> notre histoire (energie noire plus faible dans le passe) répond "
      f"{'MOINS' if K2 < K1 else 'PLUS'} au meme delta.")

print("\n" + "="*78)
print("  TRADUCTION EN BORNES")
print("="*78)
b_std = 1e-4                                 # |delta| ~ 1e-4 publie (w constant, quadrupole)
b_our = b_std*K1/K2
print(f"  borne publiee (w constant)        : |delta| <~ {b_std:.0e}")
print(f"  borne pour NOTRE histoire         : |delta| <~ {b_our:.1e}")
print(f"  cisaillement residuel aujourd'hui : |Sigma_0| <~ {b_our*S2:.1e}")
print()
print("  La skewness interieure delta est alimentee par l'asymetrie du flux d'accretion du")
print("  parent, epsilon, via le bord (transmission O(1) pour l = 2, cf. le 0,58 du corpus).")
print(f"  ->  epsilon <~ {b_our/0.58:.0e}   [contre epsilon <~ 0,35 par le canal statique]")
print(f"  ->  RESSERREMENT : {0.35/(b_our/0.58):.0e} — plus de trois ordres de grandeur.")

print("\n" + "="*78)
print("  COROLLAIRES, LES DEUX SENS")
print("="*78)
print(f"  (1) MORT DE L'OBSERVABLE : le voile borne a delta <~ {b_our:.0e} donne un ecart")
print(f"      croissance/lentillage (Phi != Psi) <~ {b_our:.0e} — inaccessible a E_G (~5-10 %).")
print("      Le canal 'voile detecte' est ferme. Ce qui nait a la place est une CONTRAINTE.")
print("  (2) La skewness ne peut pas etre contournee chez nous : arXiv:2601.22351 montre que")
print("      l'anisotropie constante est exclue par le quadrupole ISW et ne survit que par des")
print("      profils temporels ajustes annulant l'integrale du cisaillement. Notre profil")
print("      temporel est FIXE par rho_de(t) = rho_0 (t/t0)^beta / a^3 : aucune liberte")
print("      d'annulation. La borne s'applique pleinement — c'est une force du modele, pas")
print("      une faiblesse : il ne peut pas se cacher.")
