#!/usr/bin/env python3
"""AUDIT iLCDM, VOLET 3 — LA TRILOGIE SN. CRITERES PRE-ENREGISTRES (geles AVANT execution,
24/08/2026). Dernier volet de l'arbitre de T7 (apres #154 : variantes coherentes ; #156 :
ROBUSTE-LOO + split-z coherent). Question : le gain de 'ilcdm_de_ct' (eps ~ +0,022,
Dchi2 ~ -9,8) survit-il quand on remplace Pantheon+ par DES-SN5YR, puis par Union3 ?

DONNEES (empreintes dans donnees/SHA256SUMS ; sources donnees/sn_rivales/SOURCE.md).
  DES-SN5YR (tag 1.3, Vincenzi et al. 2024) : 1829 SNe, MU (H0 = 70) + C_tot = C_sys +
  diag(MUERR_FINAL^2) — le module de distance remplace mb, l'offset (donc H0) est
  marginalise analytiquement comme M : rien d'autre ne change dans le pipeline.
  Union3 (Rubin et al., UNITY 1.5) : 22 bins (z, mu) + covariance (l'inverse fournie,
  inversee et verifiee definie positive par l'agent).
  CAVEAT DECLARE : les trois compilations partagent des SNe (low-z, Foundation, DES3YR) —
  ce volet teste la robustesse aux CHOIX de calibration/compilation, pas l'independance
  statistique. BAO et distance-priors inchanges.

METHODE : swap des globales SN de vraisemblance_reelle (z_sn, mb := MU, Cinv_sn, Cinv_one,
oCo), puis refit COMPLET de LCDM et de l'iLCDM coherent (regle 5), gain = difference.

CRITERES (exhaustifs, exclusifs).
  - VALIDATION par jeu : le refit LCDM doit donner chi2/N dans [0,5 ; 1,5] (DES : N = 1829 ;
    Union3 : N = 22). Sinon ce jeu est NON EXPLOITE (mauvais branchement, pas un resultat).
  - TRILOGIE CONFIRMEE si gain >= 3 sur les DEUX jeux valides ; NON CONFIRMEE si un jeu
    valide donne gain < 1 ; MIXTE sinon — ecrit tel quel, avec les eps preferes.
  - Verse a T7 quel que soit le sens. Apres ce volet, l'arbitre grave de T7 est SERVI en
    entier (variantes, LOO, split, trilogie) : la resolution devient possible au greffe.
Usage : python3 scripts/audit_ilcdm_v3.py   (depuis donnees/pantheon_plus)
"""
import sys, csv, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audit_ilcdm as A1
import atlas_v1 as A
import vraisemblance_reelle as V

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAM = 'ilcdm_de_ct'
B0 = [0.69, 0.02236, 0.31]
SAV = dict(z_sn=V.z_sn, mb=V.mb, Cinv_sn=V.Cinv_sn, Cinv_one=V.Cinv_one, oCo=V.oCo)

def swap(z, mu, C):
    Ci = np.linalg.inv(C)
    V.z_sn = z; V.mb = mu; V.Cinv_sn = Ci
    one = np.ones(len(z)); V.Cinv_one = Ci@one; V.oCo = float(one@(Ci@one))

def restore():
    for k, v in SAV.items(): setattr(V, k, v)

def charge_des():
    rows = list(csv.DictReader((ROOT / "donnees/sn_rivales/DES-SN5YR/des_sn5yr_hd.csv").open(encoding="utf-8")))
    z = np.array([float(r["zHD"]) for r in rows])
    mu = np.array([float(r["MU"]) for r in rows])
    err = np.array([float(r["MUERR_FINAL"]) for r in rows])
    C = np.load(ROOT / "donnees/sn_rivales/DES-SN5YR/des_sn5yr_covsys_1829x1829.npy") + np.diag(err**2)
    return z, mu, C

def charge_u3():
    rows = list(csv.DictReader((ROOT / "donnees/sn_rivales/Union3/union3_bins.csv").open(encoding="utf-8")))
    z = np.array([float(r["z"]) for r in rows])
    mu = np.array([float(r["mu"]) for r in rows])
    C = np.loadtxt(ROOT / "donnees/sn_rivales/Union3/union3_cov_22x22.csv", delimiter=",")
    return z, mu, C

def gains():
    rl = A.T.fit('lcdm')
    ri = A.fit(FAM, 1, [B0+[0.02], B0+[0.005]], bornes=[(-0.5, 0.5)])
    return rl.fun, ri.fun, rl.fun - ri.fun, ri.x[3]

if __name__ == "__main__":
    print("AUDIT iLCDM VOLET 3 — la trilogie SN (criteres geles)\n")
    verdicts = {}
    for nom, charge, N in [("DES-SN5YR", charge_des, 1829), ("Union3", charge_u3, 22)]:
        z, mu, C = charge()
        swap(z, mu, C)
        cl, ci, g, e = gains()
        restore()
        # chi2/N du LCDM : retirer la part BAO+CMB+SH0ES ? Le chi2 total inclut tout ; on
        # rapporte chi2_total/(N + 17) (13 BAO + 3 priors + 1 SH0ES) — approximation declaree.
        red = cl/(N + 17)
        ok = 0.5 <= red <= 1.5
        verdicts[nom] = (ok, g, e)
        print(f"  [{nom:9s}] LCDM chi2 = {cl:9.2f} (chi2/(N+17) = {red:.2f}) -> {'VALIDE' if ok else 'NON EXPLOITE'} ; "
              f"gain iLCDM = {g:+6.2f}  eps = {e:+.4f}")
    ok_sets = [k for k, (ok, _, _) in verdicts.items() if ok]
    if len(ok_sets) < 2:
        print(f"\n  VERDICT : INCOMPLET — jeu(x) valide(s) : {ok_sets} ; rien n'est tranche.")
    else:
        gains_ok = [verdicts[k][1] for k in ok_sets]
        if all(g >= 3 for g in gains_ok): v = "TRILOGIE CONFIRMEE — le gain survit aux trois compilations"
        elif any(g < 1 for g in gains_ok): v = "NON CONFIRMEE — au moins une compilation ne le voit pas"
        else: v = "MIXTE — ecrit tel quel"
        print(f"\n  VERDICT TRILOGIE : {v}")
    print("  L'arbitre grave de T7 est desormais servi en entier (variantes, LOO, split, trilogie).")
