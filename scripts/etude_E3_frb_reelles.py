#!/usr/bin/env python3
"""E3 v0 — FRB SUR DONNEES REELLES : la table de Connor et al. 2025, plus les mocks.
CRITERES PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 23/08/2026).
Spec mere : etudes_2026.py (gelee) : « validation d'abord — le refit LCDM doit redonner
f_IGM publie a +/- 0,10, sinon rien n'est exploite ; puis Dchi2(CCBH) rapporte TEL QUEL,
favorable ou non ».

DONNEES. frbsample_connor0924.csv (github liamconnor/frb_baryon_connor2024, la table de
« A gas-rich cosmic web... », Nature Astronomy 2025) ; empreinte sha256 d3458b33864623ec...
dans donnees/SHA256SUMS. 69 sursauts localises, tous redshift spectroscopique, tous
baryon_sample=True ; z = 0,001-1,354 ; DM exgal 40-1427 pc/cm3. On prend (dm_exgal,
redshift), SANS coupure (leur drapeau d'echantillon fait la selection).

METHODE. La machinerie GELEE de frb_likelihood.py est importee telle quelle : memes trois
fonds (LCDM ; accretion beta = 2,595 ; CCBH calibre A = 1,551, B = 3,119, Xi = 1,382),
meme vraisemblance (DM_cos log-normale de largeur F z^-1/2, hote log-normal / (1+z),
priors durs f_IGM + f_X <= 1). Seule différence : data = la table reelle, plus un tirage.
Ajustement : maximisation de logL sur (f_IGM, f_X, mu_host, sigma_host), Nelder-Mead,
quatre departs, par fond. Delta_chi2 = 2 (lnL_fond - lnL_LCDM).

CRITERES (exhaustifs, exclusifs).
  - VALIDATION (spec mere) : le fit LCDM sur la table reelle doit donner f_IGM dans
    [0,70 ; 0,90] (leur 0,80 +0,08/-0,09) ET f_X < 0,3. Sinon : NON EXPLOITE — la
    machinerie ou la table ne reproduit pas l'analyse publiee, rien d'autre n'est lu.
  - Si la validation passe : Delta_chi2(CCBH - LCDM) et (accretion - LCDM) rapportes TELS
    QUELS, avec les nuisances preferees par fond. Aucun seuil de victoire n'est declare
    ici : c'est une MESURE (la significativite se lit en sqrt(Dchi2), un seul tirage de
    donnees, pas de mediane de mocks). Le signe et l'amplitude vont au registre quel que
    soit leur sens.
  - La substitution aux mocks dans le papier C (exigee par la spec mere) est un acte
    d'ecriture separee : consignee comme prochaine etape, pas faite par ce script.
Valeurs de substitution : aucune. Usage : python3 scripts/etude_E3_frb_reelles.py
"""
import sys, csv, pathlib
import numpy as np
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import os; os.chdir(ROOT / "donnees" / "pantheon_plus")
import frb_likelihood as F

CSV = ROOT / "donnees" / "frb_connor2025" / "frbsample_connor0924.csv"

def charge():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    return [(float(r["dm_exgal"]), float(r["redshift"])) for r in rows]

def fit(data, which):
    best = None
    for p0 in ([0.80, 0.11, np.log(120.), 0.55], [0.6, 0.3, np.log(180.), 0.8],
               [0.9, 0.05, np.log(80.), 0.4], [0.7, 0.2, np.log(150.), 0.6]):
        r = minimize(lambda p: -F.logL(data, which, p), p0, method="Nelder-Mead",
                     options=dict(xatol=1e-4, fatol=1e-4, maxiter=4000, maxfev=4000))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == "__main__":
    data = charge()
    print(f"E3 v0 — table reelle : {len(data)} FRB (Connor et al. 2025), z max {max(z for _, z in data):.3f}\n")
    res = {}
    for which, nom in [("L", "LCDM"), ("A", "accretion b=2,595"), ("C", "CCBH calibre")]:
        r = fit(data, which); res[which] = r
        f_, x_, mu, sig = r.x
        print(f"  {nom:>18s} : -lnL = {r.fun:9.3f} | f_IGM = {f_:.3f}  f_X = {x_:.3f}  "
              f"exp(mu) = {np.exp(mu):6.1f} pc/cm3  sigma = {sig:.3f}  f_IGM+f_X = {f_+x_:.3f}")
    fL, xL = res["L"].x[0], res["L"].x[1]
    ok = 0.70 <= fL <= 0.90 and xL < 0.3
    print(f"\n  VALIDATION (f_IGM(LCDM) dans [0,70;0,90] et f_X < 0,3) : "
          + (f"PASSE (f_IGM = {fL:.3f}, publie 0,80 +0,08/-0,09)" if ok else f"ECHEC (f_IGM = {fL:.3f}, f_X = {xL:.3f}) -> RIEN N'EST EXPLOITE"))
    if ok:
        dC = 2*(res["C"].fun - res["L"].fun); dA = 2*(res["A"].fun - res["L"].fun)
        print(f"  Dchi2(CCBH - LCDM)      = {dC:+.2f}  (~{np.sqrt(abs(dC)):.1f} sigma, un tirage)")
        print(f"  Dchi2(accretion - LCDM) = {dA:+.2f}  (~{np.sqrt(abs(dA)):.1f} sigma)")
        print(f"  bord f_IGM + f_X = 1 atteint en CCBH : {'OUI (deficit non absorbable)' if res['C'].x[0]+res['C'].x[1] > 0.98 else 'non'}")
        print("  Rapporte tel quel ; substitution aux mocks du papier C = etape d'auteur.")
