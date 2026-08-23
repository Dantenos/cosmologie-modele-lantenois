#!/usr/bin/env python3
"""E3 BOOTSTRAP — le 2,2 sigma reel etait un tirage unique ; en voici la distribution.
CRITERES PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 23/08/2026).

POURQUOI. E3 v1 (gele b4db63303237) donne Dchi2(CCBH - LCDM) = +4,71 sur les 69 FRB reels —
un seul echantillon. L'audit reprochait aux mocks la meme chose (#99 : mediane de 12 tirages
contre un tirage unique a 2,6 sigma). Meme exigence pour le reel : bootstrap.

METHODE. 200 reechantillonnages avec remise des 69 FRB (graine 20260823), fits LCDM et CCBH
(la machinerie gelee de frb_likelihood via etude_E3_frb_reelles ; l'accretion est omise :
indiscernable de LCDM a -0,01, v1). Deux departs par fit (les deux meilleurs de v1).
Dchi2_k = 2(lnL_LCDM - lnL_CCBH) par tirage, distribution rapportee.

CRITERES (exhaustifs, exclusifs).
  - VALIDATION : le Dchi2 de l'echantillon complet (+4,71, v1) doit tomber dans l'intervalle
    [2,5 % ; 97,5 %] du bootstrap ; sinon NON EXPLOITE (bootstrap incoherent avec le point).
  - Sortie, rapportee TELLE QUELLE : mediane et quantiles 16/50/84 de Dchi2, fraction des
    tirages ou CCBH bat LCDM (Dchi2 < 0), et sigma_indicatif = sqrt(mediane).
  - Aucun seuil de victoire : c'est une barre d'erreur, pas un verdict. Le verdict du canal
    FRB reste au compte de sursauts a levier (82-120 pour 3 sigma, spec).
Usage : python3 scripts/etude_E3_bootstrap.py [n_tirages]
"""
import sys, pathlib
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import etude_E3_frb_reelles as V0
import frb_likelihood as F

def fit2(data, which):
    best = None
    for p0 in ([0.80, 0.11, np.log(120.), 0.55], [0.7, 0.2, np.log(150.), 0.6]):
        r = minimize(lambda p: -F.logL(data, which, p), p0, method="Nelder-Mead",
                     options=dict(xatol=1e-4, fatol=1e-4, maxiter=3000, maxfev=3000))
        if best is None or r.fun < best.fun: best = r
    return best.fun

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    data = V0.charge(); n = len(data)
    rng = np.random.default_rng(20260823)
    ds = []
    for k in range(N):
        idx = rng.integers(0, n, n)
        boot = [data[i] for i in idx]
        d = 2*(fit2(boot, "C") - fit2(boot, "L"))
        ds.append(d)
        if (k+1) % 20 == 0: print(f"[boot] {k+1}/{N}  mediane = {np.median(ds):+.2f}", flush=True)
    ds = np.array(ds); q = np.percentile(ds, [2.5, 16, 50, 84, 97.5])
    print(f"\n[boot] Dchi2(CCBH - LCDM), {N} tirages : mediane {q[2]:+.2f}  [16;84] = [{q[1]:+.2f} ; {q[3]:+.2f}]"
          f"  [2,5;97,5] = [{q[0]:+.2f} ; {q[4]:+.2f}]")
    ok = q[0] <= 4.71 <= q[4]
    print(f"[boot] VALIDATION : +4,71 (echantillon complet) dans [2,5;97,5] ? {'PASSE' if ok else 'ECHEC -> NON EXPLOITE'}")
    if ok:
        print(f"[boot] CCBH bat LCDM dans {np.mean(ds < 0)*100:.1f} % des tirages ; "
              f"sigma indicatif = sqrt(mediane) = {np.sqrt(max(q[2],0)):.1f}")
        print("[boot] Barre d'erreur, pas un verdict : le juge du canal reste 82-120 sursauts a levier.")
