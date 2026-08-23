"""Attaque exécutable — Croker et al. 2024, classe « fond cosmologique ».
CRITÈRE PRÉ-ENREGISTRÉ : reproduire (H0 dérivé, survie s) à leur Xi=1,403 avec le taux
calibré (A=1,551, B=3,119) et leurs omega publiés. Aucune valeur imprimée = attaque nulle."""
import sys, os, pathlib, numpy as np
_R = pathlib.Path(__file__).resolve().parent.parent   # racine du depot
sys.path.insert(0, str(_R / 'scripts')); os.chdir(_R / 'donnees' / 'pantheon_plus')
import duel_ccbh as D
np.seterr(all='ignore')
P0=lambda z:0.015*(1+z)**2.7/(1+((1+z)/2.9)**5.6)
D.psi_MD14=lambda z:1.551*P0(z)*np.where(np.asarray(z)>4.0,3.119,1.0)
o=D.fond_ccbh(0.1237,0.02238,1.403)
print(f"ADVERSAIRE: H0_derive {100*o[2]:.3f}")
print(f"ADVERSAIRE: survie_s {o[3]/0.02238:.4f}")
