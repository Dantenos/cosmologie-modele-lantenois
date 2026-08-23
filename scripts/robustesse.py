#!/usr/bin/env python3
"""
robustesse.py — Le resultat en sigma_8 tient-il, ou est-ce un artefact du seuil ?

Trois epreuves :
  (1) Decomposer chaque gradient en [effet sigma a seuil fige] + [deplacement du seuil].
      -> repond a : la "contre-pression" proposee agit-elle dans le bon sens ?
  (2) Refaire le balayage sigma_8 pour PLUSIEURS valeurs du seuil, dont celle
      annoncee par le papier B (2.5e14) et celle que donne le calcul (2.1e12).
      -> le maximum est-il un fait, ou une consequence du seuil choisi ?
  (3) Refaire avec Sheth-Tormen au lieu de Press-Schechter.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from gradient_v2 import Cosmo, etat, REF, DELTA_C, NEFF_CUT

np.seterr(all='ignore')
c0, Mc0, F0 = etat()
amp0, eps = c0.amp, 0.02

print("=" * 82)
print("  (1) DECOMPOSITION DES GRADIENTS : la contre-pression agit-elle dans le bon sens ?")
print("=" * 82)
print(f"  {'parametre':>10s} {'total':>9s} {'seuil fige':>11s} {'part du seuil':>14s}   verdict")
for label, kwlo, kwhi in [
    ('Omega_m', dict(Om=REF['Om']*(1-eps)), dict(Om=REF['Om']*(1+eps))),
    ('sigma_8', dict(s8=REF['s8']*(1-eps)), dict(s8=REF['s8']*(1+eps))),
    ('n_s',     dict(ns=REF['ns']*(1-eps)), dict(ns=REF['ns']*(1+eps))),
]:
    clo, Mlo, Flo = etat(**kwlo); chi, Mhi, Fhi = etat(**kwhi)
    g_tot = (np.log(Fhi) - np.log(Flo)) / (2 * eps)
    g_fig = (np.log(chi.F(Mc0)) - np.log(clo.F(Mc0))) / (2 * eps)   # seuil bloque a Mc0
    g_seuil = g_tot - g_fig
    verdict = ("AGGRAVE la pression" if g_seuil * g_fig > 0 else
               "s'oppose a la pression" if g_seuil * g_fig < 0 else "neutre")
    print(f"  {label:>10s} {g_tot:>+9.2f} {g_fig:>+11.2f} {g_seuil:>+14.2f}   {verdict}")

print("\n" + "=" * 82)
print("  (2) LE MAXIMUM EN sigma_8 DEPEND-IL DU SEUIL ?")
print("=" * 82)
print("  On refait le balayage a seuil FIXE, pour quatre valeurs du seuil.")
print(f"  {'M_cut fixe':>12s} {'nu(Mcut)':>9s} | " + " ".join(f"{s:>7.2f}" for s in [0.5,0.65,0.8111,1.0,1.3])
      + f" | {'argmax':>8s} {'dlnF/dlns8':>11s}")
for Mfix in [2.05e12, 1e13, 1e14, 2.5e14, 1e15]:
    ligne, ref = [], None
    for s8 in [0.5, 0.65, 0.8111, 1.0, 1.3]:
        c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=s8)
        v = c.F(Mfix)
        if s8 == 0.8111: ref = v
        ligne.append(v)
    ligne = np.array(ligne) / ref
    # maximum et gradient local en sigma8
    f = lambda s: -np.log(Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=s).F(Mfix))
    r = minimize_scalar(f, bounds=(0.2, 3.0), method='bounded')
    clo = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8']*(1-eps))
    chi = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8']*(1+eps))
    g = (np.log(chi.F(Mfix)) - np.log(clo.F(Mfix))) / (2*eps)
    nu = DELTA_C / c0.sig_M(Mfix)
    print(f"  {Mfix:>12.2e} {nu:>9.2f} | " + " ".join(f"{v:>7.3f}" for v in ligne)
          + f" | {r.x:>8.3f} {g:>+11.2f}")
print("\n  LECTURE : si l'argmax en sigma_8 traverse la valeur observee (0,811) quand le")
print("  seuil bouge, alors 'nos parametres sont au maximum' n'est PAS un fait sur le")
print("  monde mais une consequence du seuil retenu. Le seuil devient la question centrale.")

print("\n" + "=" * 82)
print("  (3) SHETH-TORMEN au lieu de Press-Schechter (seuil auto-coherent)")
print("=" * 82)
for forme in ['PS', 'ST']:
    c, Mc, F = etat(forme=forme)
    gs, gO, gn = [], [], []
    for kwlo, kwhi, dest in [
        (dict(s8=REF['s8']*(1-eps)), dict(s8=REF['s8']*(1+eps)), gs),
        (dict(Om=REF['Om']*(1-eps)), dict(Om=REF['Om']*(1+eps)), gO),
        (dict(ns=REF['ns']*(1-eps)), dict(ns=REF['ns']*(1+eps)), gn)]:
        _, _, Flo = etat(forme=forme, **kwlo); _, _, Fhi = etat(forme=forme, **kwhi)
        dest.append((np.log(Fhi) - np.log(Flo)) / (2*eps))
    print(f"  {forme} : M_cut = {Mc:.3e}  F = {F:.4e}   "
          f"dlnF/dln[sigma8, Om, ns] = [{gs[0]:+.2f}, {gO[0]:+.2f}, {gn[0]:+.2f}]")

print("\n" + "=" * 82)
print("  (4) OU EST EXACTEMENT LE MAXIMUM EN sigma_8 (seuil auto-coherent) ?")
print("=" * 82)
def negF(s8):
    _, _, F = etat(s8=s8)
    return -np.log(F)
r = minimize_scalar(negF, bounds=(0.3, 2.0), method='bounded')
print(f"  argmax sigma_8 = {r.x:.4f}   contre sigma_8 observe = {REF['s8']:.4f}")
print(f"  ecart relatif  = {(REF['s8']-r.x)/r.x*100:+.1f} %")
print(f"  Planck 2018 donne sigma_8 = 0.8111 +/- 0.0060 -> ecart en sigma :"
      f" {(REF['s8']-r.x)/0.0060:+.1f} sigma")
