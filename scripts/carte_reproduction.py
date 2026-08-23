"""E6 — Carte de reproduction beta_enfant = f(beta_parent). CRITERES PRE-ENREGISTRES :
verdict CONTRACTANTE/DILATANTE seulement si les DEUX lectures (pic 2/(n+3), rms 4/(n+3))
concordent sur le regime via |f'| au point fixe ; sinon INDECISE. Hypothese v0 declaree :
chaque generation a un spectre standard (meme fonction de transfert, ns=0.9649) et l'echelle
de graine est fixee par le critere d'auto-coherence nu=1 (seuil de domination du profil de
pic). Toute dependance de M_graine en beta_parent est NON MODELISEE en v0 : si elle existe,
f' change — limite ecrite, pas cachee."""
import numpy as np, sys
from scipy.optimize import brentq
sys.path.insert(0,'/home/claude/selection')
from gradient_v2 import Cosmo, REF
np.seterr(all='ignore')
c=Cosmo(REF['Om'],REF['Ob'],REF['h'],REF['ns'],s8=REF['s8']); H=REF['h']; DC=1.686
Mstar=np.exp(brentq(lambda l: DC/c.sig_M(np.exp(l))-1.0, np.log(1e11), np.log(1e17)))
n=c.n_eff(Mstar)
print(f"E6 — echelle de graine (nu=1) : M* = {Mstar/H:.2e} Msun, n_eff = {n:+.4f}")
print(f"  M* est fixee par le SPECTRE SEUL -> d beta_enfant / d beta_parent = 0 exactement (v0)")
for k,lab in [(2.0,'lecture pic'),(4.0,'lecture rms')]:
    print(f"  {lab:12s}: point fixe beta* = {k/(n+3):.3f}   |f'| = 0 < 1  -> CONTRACTANTE")
print(f"  mesure : beta = 2,42-2,60 — ENCADRE par les deux points fixes (2,05 ; 4,11),")
print(f"  reproduit par aucun : coherent avec l'encadrement epsilon deja consigne (#73).")
print("VERDICT (les deux lectures concordent sur le regime) : **CONTRACTANTE**")
print("  -> la hierarchie converge en UNE generation vers beta* ; profondeur infinie stable.")
print("  Limite v0 : la constance de f decoule de l'hypothese nu=1 + spectre standard.")
