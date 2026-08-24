#!/usr/bin/env python3
"""AUDIT iLCDM, VOLET 2 — LOO traceurs BAO et partage en redshift. CRITERES PRE-ENREGISTRES
(geles AVANT execution, 24/08/2026). Suite de #154 (volet 1 : le gain survit aux variantes
coherentes). Ici : le gain de la variante ROBUSTE (Q = eps H rho_de, CDM seul, echange
tardif z < 3 — fam 'ilcdm_de_ct') est-il PORTE par un traceur BAO unique, et l'echange
prefere-t-il le meme eps a bas et haut redshift ?

METHODE.
  LOO : les 13 points BAO DR2 groupes par traceur (BGS ; LRG1 ; LRG2 ; LRG3 ; ELG ; QSO ;
  Lya — 7 groupes, comme le jackknife du papier A). Pour chaque retrait : reconstruction de
  d_bao/Cinv_bao (correlations DM-DH conservees), refit COMPLET de LCDM et de l'iLCDM
  (regle 5), gain g = chi2_LCDM - chi2_iLCDM.
  SPLIT-z : SNe partagees a z = 0,6 (comme P8) — covariance pleine restreinte, M marginalise ;
  refit des deux fonds sur chaque moitie (BAO complets conserves, declare : c'est le canal SN
  qui est partage) ; comparaison des eps preferes.
  VALIDATION d'abord : le refit plein doit redonner le gain de #154 (9,85 +/- 0,3) et
  eps = +0,0215 +/- 0,002. Sinon rien n'est publie.

CRITERES (exhaustifs, exclusifs).
  - LOO : ROBUSTE-LOO si le gain reste >= 5 pour TOUS les retraits ET si aucun retrait ne
    reduit le gain de plus de 50 % ; PORTE-PAR-UN-TRACEUR si un retrait fait tomber g < 3
    (le traceur est nomme) ; INTERMEDIAIRE sinon.
  - SPLIT : COHERENT si eps(z<0,6) et eps(z>=0,6) sont compatibles a < 2 sigma (somme
    quadratique des erreurs de profil grossier) ; sinon TENSION D'ECHELLE, ecrite telle
    quelle (et versee a T7).
  - Tout est rapporte, favorable ou non. Le volet 3 (trilogie SN : DES-SN5YR, Union3) reste
    du apres ce volet — donnees en cours de recuperation.
Usage : python3 scripts/audit_ilcdm_v2.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audit_ilcdm as A1          # enregistre les fonds coherents dans atlas_v1.CUSTOM
import atlas_v1 as A
import vraisemblance_reelle as V

FAM = 'ilcdm_de_ct'
GROUPES = [("BGS", [0]), ("LRG1", [1, 2]), ("LRG2", [3, 4]), ("LRG3", [5, 6]),
           ("ELG", [7, 8]), ("QSO", [9, 10]), ("Lya", [11, 12])]
B0 = [0.69, 0.02236, 0.31]

# sauvegardes des globales patchees
SAV = dict(BAO=V.BAO, d_bao=V.d_bao, Cinv_bao=V.Cinv_bao,
           z_sn=V.z_sn, mb=V.mb, Cinv_sn=V.Cinv_sn, Cinv_one=V.Cinv_one, oCo=V.oCo)

def cov_bao(bao):
    C = np.zeros((len(bao), len(bao)))
    for i, b in enumerate(bao): C[i, i] = b[3]**2
    for i, b in enumerate(bao):
        if b[4] is not None and i+1 < len(bao):
            C[i, i+1] = C[i+1, i] = b[4]*b[3]*bao[i+1][3]
    return C

def drop_bao(indices):
    # deponderation (sigma x 1e3, correlations coupees) : equivalent au retrait, sans changer
    # les formes internes du pipeline scelle (u = 13 fixe dans test_wE_v3)
    C = cov_bao(SAV["BAO"]).copy()
    for i in indices:
        C[i, :] = 0.0; C[:, i] = 0.0; C[i, i] = (SAV["BAO"][i][3]*1e3)**2
    V.Cinv_bao = np.linalg.inv(C)

def split_sn(masque):
    idx = np.where(masque)[0]
    C = SAV["Cinv_sn"]  # attention : il faut la covariance, pas l'inverse
    # reconstruire depuis la covariance pleine conservee par vraisemblance ? V.C_sn existe
    Csub = V.C_sn[np.ix_(idx, idx)] if hasattr(V, "C_sn") else None
    Ci = np.linalg.inv(Csub)
    V.z_sn = SAV["z_sn"][idx]; V.mb = SAV["mb"][idx]; V.Cinv_sn = Ci
    one = np.ones(len(idx)); V.Cinv_one = Ci@one; V.oCo = one@(Ci@one)

def restore():
    for k, v in SAV.items(): setattr(V, k, v)

def gains():
    rl = A.T.fit('lcdm')
    ri = A.fit(FAM, 1, [B0+[0.02], B0+[0.005]], bornes=[(-0.5, 0.5)])
    return rl.fun, ri.fun, rl.fun - ri.fun, ri.x[3]

if __name__ == "__main__":
    print("AUDIT iLCDM VOLET 2 — LOO traceurs + split-z (criteres geles)\n")
    cl, ci, g0, e0 = gains()
    ok = abs(g0 - 9.85) < 0.3 and abs(e0 - 0.0215) < 0.002
    print(f"  [validation] plein : gain = {g0:+.2f} (attendu 9,85 ± 0,3), eps = {e0:+.4f} -> {'PASSE' if ok else 'ECHEC'}")
    if not ok: sys.exit("  rien n'est publie.")
    print("\n  --- LOO traceurs BAO (LCDM et iLCDM refittes a chaque retrait) ---")
    pire, gmin = None, 1e9
    for nom, idxs in GROUPES:
        drop_bao(idxs)
        _, _, g, e = gains()
        restore()
        print(f"    sans {nom:5s} : gain = {g:+6.2f}  eps = {e:+.4f}")
        if g < gmin: gmin, pire = g, nom
    if gmin >= 5 and gmin >= 0.5*g0: vloo = "ROBUSTE-LOO"
    elif gmin < 3: vloo = f"PORTE-PAR-UN-TRACEUR ({pire})"
    else: vloo = f"INTERMEDIAIRE (minimum {gmin:+.2f} sans {pire})"
    print(f"  VERDICT LOO : {vloo}")
    print("\n  --- split-z des SNe a 0,6 (BAO complets, declare) ---")
    eps_moities = {}
    for lab, m in [("z<0,6", SAV["z_sn"] < 0.6), ("z>=0,6", SAV["z_sn"] >= 0.6)]:
        split_sn(m)
        _, _, g, e = gains()
        # erreur de profil grossiere : pas de 0,005 jusqu'a Dchi2=1
        c_at = lambda ee: A.fit(FAM, 1, [B0], fixpar=ee).fun
        base = A.fit(FAM, 1, [B0+[e]], bornes=[(-0.5, 0.5)]).fun
        se = 0.005
        for k in range(1, 10):
            if c_at(e + k*0.005) > base + 1.0: se = k*0.005; break
        restore()
        eps_moities[lab] = (e, se)
        print(f"    {lab:7s} : gain = {g:+6.2f}  eps = {e:+.4f} ± {se:.4f} (profil grossier)")
    (e1, s1), (e2, s2) = eps_moities["z<0,6"], eps_moities["z>=0,6"]
    nsig = abs(e1 - e2)/np.hypot(s1, s2)
    print(f"  VERDICT SPLIT : |Deps| = {abs(e1-e2):.4f} -> {nsig:.1f} sigma -> "
          + ("COHERENT" if nsig < 2 else "TENSION D'ECHELLE — versee a T7, ecrite telle quelle"))
    print("\n  volet 3 (trilogie SN) : du — donnees DES-SN5YR / Union3 en cours de recuperation.")
