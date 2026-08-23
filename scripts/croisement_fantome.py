#!/usr/bin/env python3
"""LE CROISEMENT FANTOME z_x(beta) — arbitrage entre quatre valeurs du papier A.
CRITERES PRE-ENREGISTRES (geles avant execution, 23/08/2026).

Le papier A porte quatre valeurs incompatibles du redshift ou w = -1 :
  (a) tableau de retractation l.632 : z_x = 0,458 / 0,345 / 0,253 / 0,214 a beta = 2,42 / 2,49 /
      2,56 / 2,60 (retire comme prediction chiffree, #111) ;
  (b) l.100 : z_x = 0,36 a beta = 2,59 (ancienne table) et 0,68 a beta = 2,42 ;
  (c) l.577 et l.925 : z_x = 0,36 utilise comme argument physique ;
  (d) P10 l.933 : z_x = 0,50 a beta = 5/2, « inside the DESI-indicated window ».
DEFINITION : w(z) = -beta/(3 H t) = -1  <=>  beta = 3 H(z_x) t(z_x), dans le fond auto-coherent
E_acc de vraisemblance_reelle.py (gele via test_wE_v3 ; meme machinerie que la ligne de base).
METHODE : z_x(beta) par brentq sur beta - 3Ht, pour beta = 2,42 / 2,49 / 2,50 / 2,56 / 2,595 /
2,60, a Om = 0,314 (ligne de base) et, en sensibilite, 0,30 et 0,33.
CRITERES :
  - La valeur (a) est REPRODUITE si |z_x - tableau| < 0,03 aux quatre beta a Om = 0,314 ;
  - chaque valeur (b)-(d) est CONFIRMEE ou INFIRMEE par le meme calcul ; une valeur infirmee est
    a corriger dans le papier (l'auteur tranche la formulation, pas le chiffre) ;
  - la sensibilite a Om est rapportee telle quelle ; si elle depasse 0,05 en z_x, le tableau (a)
    doit porter son Om.
Valeurs de substitution : aucune. Usage : python3 scripts/croisement_fantome.py (depuis donnees/pantheon_plus).
"""
import sys, pathlib, os
import numpy as np
from scipy.optimize import brentq
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts")); os.chdir(ROOT / "donnees" / "pantheon_plus")
import vraisemblance_reelle as VR

def Ht_of_z(z, Om, beta):
    """3 H(z) t(z) en unites ou H0 = 1 : t(z) = int_0^a da/(a E)."""
    a = np.logspace(-6, 0, 25000); E = VR.E_acc(1/a - 1, Om, beta)
    integ = 1/(a*E); t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])
    az = 1/(1+z)
    return 3*np.interp(az, a, E)*np.interp(az, a, t)

def z_x(Om, beta):
    f = lambda z: beta - Ht_of_z(z, Om, beta)
    return brentq(f, 0.0, 3.0, xtol=1e-4) if f(0.0)*f(3.0) < 0 else np.nan

if __name__ == "__main__":
    TAB = {2.42: 0.458, 2.49: 0.345, 2.56: 0.253, 2.60: 0.214}
    betas = [2.42, 2.49, 2.50, 2.56, 2.595, 2.60]
    print(f"{'beta':>6s} | {'Om=0,30':>8s} {'Om=0,314':>9s} {'Om=0,33':>8s} | tableau (a)")
    ok_a, dOm = True, 0.0
    for b in betas:
        zs = [z_x(om, b) for om in (0.30, 0.314, 0.33)]
        ref = TAB.get(b); s = f"{ref:.3f}" if ref else "  —  "
        if ref: ok_a &= abs(zs[1]-ref) < 0.03
        dOm = max(dOm, abs(zs[0]-zs[2]))
        print(f"{b:6.3f} | {zs[0]:8.3f} {zs[1]:9.3f} {zs[2]:8.3f} | {s}")
    z250 = z_x(0.314, 2.50); z242 = z_x(0.314, 2.42); z259 = z_x(0.314, 2.59)
    print(f"\n(a) tableau de retractation : {'REPRODUIT' if ok_a else 'NON REPRODUIT'} (|ecart| < 0,03 a Om = 0,314)")
    print(f"(b) l.100 : 0,68 a beta=2,42 -> calcule {z242:.3f} : {'CONFIRME' if abs(z242-0.68)<0.03 else 'INFIRME'} ; "
          f"0,36 a beta=2,59 -> calcule {z259:.3f} : {'CONFIRME' if abs(z259-0.36)<0.03 else 'INFIRME'}")
    print(f"(c) l.577/925 : 0,36 comme argument physique -> voir (b)")
    print(f"(d) P10 l.933 : 0,50 a beta=5/2 -> calcule {z250:.3f} : {'CONFIRME' if abs(z250-0.50)<0.03 else 'INFIRME'}")
    print(f"sensibilite a Om (0,30 -> 0,33) : jusqu'a {dOm:.3f} en z_x -> "
          + ("le tableau doit porter son Om" if dOm > 0.05 else "negligeable au niveau du tableau"))
