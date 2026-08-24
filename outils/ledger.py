#!/usr/bin/env python3
"""GRAND LIVRE v1 — la comptabilite baryonique, par espece et par epoque. CRITERES
PRE-ENREGISTRES (geles AVANT la premiere execution, 24/08/2026).

PRINCIPE (theoreme #139) : le fond ne separe pas les modeles sources ; ce qu'ils
consomment laisse un trou dans un budget. Trois rangees :
  R1. FRB (z < 1,4) : 69 sursauts reels (Connor 2025), machinerie gelee d'E3 v1.
  R2. AMAS (z = 0,078-1,063) : 40 f_gas relaxes, Mantz et al. 2014 (MNRAS 440, 2077,
      arXiv:1402.6212, Table 2, coquille 0,8-1,2 r2500 ; donnees/amas_fgas/).
      Modele (leur eq. 2) : f_gas = K(z) Y(z) s(z) (Ob/Om) [d(z)/d_ref(z)]^(3/2), avec
      LEURS priors (Table 3) : K0 = 0,90 +/- 0,09 (calibration lentille WtG, Applegate
      2014 — le 0,96 +/- 9 % est Applegate 2016, note) ; K1 ~ U(-0,05;+0,05) ;
      Y0 ~ U(0,763;0,932) ; Y1 ~ U(-0,05;+0,05) ; dispersion intrinseque 7,4 % ;
      correction d'ouverture eta negligee (declare : elle vaut ~(dH)^0,44, ecarts de
      modeles <~ 1 %). d(z) est RECALCULE par modele (d ∝ (1/h) int dz/E) contre la
      reference du papier (LCDM plat h = 0,7, Om = 0,3) — pas fixe.
      Ligne PENTE : memes donnees, niveau libre (sans prior), K1 et Y1 libres dans leurs
      boites — ce qui reste discrimine la FORME s(z), plancher ~4 %/z (priors K1+Y1).
  R3. COHERENCE omega_b : BBN contre CMB. Deux lectures publiees du D/H, rapportees
      toutes deux : Cooke et al. 2018 (taux Marcucci) omega_b = 0,02166 +/- 0,00019
      (2,9 sigma du CMB) ; Schoeneberg 2024 (conservateur) 0,02218 +/- 0,00055
      (0,3 sigma). Aucun modele de l'atlas ne consomme avant la recombinaison : rangee
      declarative, en attente d'un modele qui le ferait.
S(z) PAR MODELE : CCBH calibre = trajectoire integree de sa propre EDO (frb_likelihood :
s = 1,00 a z = 10 ; 0,81 a z = 1 ; 0,70 a z = 0 — consommation recente, la pente teste).
Tous les autres modeles de l'atlas : s(z) = 1 (les echanges sombres des iLCDM : rangee
matiere sombre en v2, declare).
HYPOTHESE DECLAREE (decisive) : consommation UNIFORME en environnement (lecture (i)).
Si le gaz lie des halos est blinde (lecture (ii) — plausible si la consommation suit la
formation stellaire), la rangee R2 est NULLE et non falsifiante, et seul R1 (milieu
diffus) porte. Les deux lectures sont publiees avec le resultat ; R1 et R2 ne mesurent
le MEME s que sous (i).
REFERENCES : (Ob/Om)_CMB = 0,1564 +/- 0,0020 (Planck 2018 VI : omega_b 0,02237+/-0,00015,
omega_m 0,1430+/-0,0011).

CRITERES (exhaustifs, exclusifs).
  - VALIDATION R2 (etalon du papier, §5.1) : a s = 1, le fit doit donner chi2/40 < 1,5
    ET un (Ob/Om) prefere a moins de 2 sigma du CMB — l'equivalent, a nos priors, du
    h^(3/2) Ob/Om = 0,089 +/- 0,012 de Mantz. Sinon : R2 NON EXPLOITEE.
  - VALIDATION R1 : celle d'E3 v1 (f_d), re-executee.
  - Sortie par modele : Dchi2_R1, Dchi2_R2 (niveau) et Dchi2_R2_pente (forme seule),
    somme, nuisances poussees — rapportes TELS QUELS, favorables ou non. Pas de seuil de
    victoire : le Livre est une colonne de l'atlas (fusionnee dans atlas_leaderboard.json),
    pas un verdict. Ecritures : registres/ledger.json + registres/LEDGER.md (generes).
Usage : python3 outils/ledger.py   (depuis la racine ; il gere son CWD)
"""
import sys, os, csv, json, pathlib, datetime
import numpy as np
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT / "donnees" / "pantheon_plus")
import etude_E3_frb_reelles as E3
import frb_likelihood as F
os.chdir(ROOT)

OBOM, S_OBOM = 0.1564, 0.0020
K0, SK = 0.90, 0.09
Y0_LO, Y0_HI = 0.763, 0.932
B1_LO, B1_HI = -0.05, 0.05          # boites communes K1, Y1
SCAT = 0.074
WBP = 0.02245
WB_BBN_C, S_BBN_C = 0.02166, 0.00019   # Cooke 2018 (Marcucci)
WB_BBN_S, S_BBN_S = 0.02218, 0.00055   # Schoeneberg 2024 (conservateur)
WB_CMB, S_CMB = 0.02237, 0.00015

def charge_amas():
    rows = list(csv.DictReader((ROOT / "donnees/amas_fgas/mantz2014_fgas_r2500shell.csv").open(encoding="utf-8")))
    return (np.array([float(r["z"]) for r in rows]), np.array([float(r["fgas"]) for r in rows]),
            np.array([float(r["sigma_fgas"]) for r in rows]))

def s_ccbh(z): return np.interp(z, F.zc, F.wbc) / WBP

# distances : d ∝ (1/h) int dz/E ; reference du papier = LCDM plat h=0,7, Om=0,3
_zg = np.linspace(0, 1.3, 800)
def _dc(E_of_z, h):
    inv = 1/E_of_z(_zg)
    return np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(_zg))])/h
E_ref = lambda z: np.sqrt(0.3*(1+z)**3 + 0.7)
DC_REF = _dc(E_ref, 0.70)
DC_L   = _dc(F.E_l, F.h_l)          # LCDM du pipeline (fond ajuste)
DC_C   = _dc(F.E_c, F.hc)           # CCBH calibre
def dfac(z, which):
    dc = {"ref": DC_REF, "L": DC_L, "C": DC_C}[which]
    return (np.interp(z, _zg, dc)/np.interp(z, _zg, DC_REF))**1.5

def chi2_amas(z, f, sig, s_of_z, which_d, niveau_libre=False):
    sz = s_of_z(z); dz = dfac(z, which_d)
    def cout(p):
        if niveau_libre:
            N, k1, y1 = p
            if not (0.01 < N < 1.0 and B1_LO < k1 < B1_HI and B1_LO < y1 < B1_HI): return 1e9
            pred = N*(1 + k1*z)*(1 + y1*z)*sz*dz; pen = 0.0
        else:
            K, k1, y0, y1, ob = p
            if not (Y0_LO < y0 < Y0_HI and B1_LO < y1 < B1_HI and B1_LO < k1 < B1_HI
                    and 0.5 < K < 1.5 and 0.10 < ob < 0.22): return 1e9
            pred = K*(1 + k1*z)*y0*(1 + y1*z)*sz*ob*dz
            pen = ((K - K0)/SK)**2 + ((ob - OBOM)/S_OBOM)**2
        s2 = sig**2 + (SCAT*pred)**2
        return float(np.sum((f - pred)**2/s2) + pen)
    starts = ([[0.118, 0.0, 0.0], [0.13, 0.02, -0.02]] if niveau_libre
              else [[K0, 0.0, 0.848, 0.0, OBOM], [1.0, 0.02, 0.80, 0.02, OBOM], [0.85, -0.02, 0.90, -0.02, OBOM]])
    best = None
    for p0 in starts:
        r = minimize(cout, p0, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-6, maxiter=6000, maxfev=6000))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == "__main__":
    print("GRAND LIVRE v1 — la comptabilite baryonique (criteres geles, voir docstring)\n")
    data = E3.charge()
    rL = E3.fit(data, "L"); rC = E3.fit(data, "C")
    fdL = rL.x[0] + rL.x[1]; okR1 = 0.81 <= fdL <= 1.01; dR1 = 2*(rC.fun - rL.fun)
    print(f"[R1 FRB]  validation f_d = {fdL:.3f} -> {'PASSE' if okR1 else 'ECHEC'} ; Dchi2(CCBH, s(z)) = {dR1:+.2f}")
    z, f, sig = charge_amas()
    un = lambda zz: np.ones_like(zz)
    b1 = chi2_amas(z, f, sig, un, "L")
    okR2 = b1.fun/len(z) < 1.5 and abs(b1.x[4] - OBOM) < 2*S_OBOM
    print(f"[R2 AMAS] validation s=1 : chi2/40 = {b1.fun/len(z):.2f}, Ob/Om = {b1.x[4]:.4f} (CMB {OBOM} ± {S_OBOM}) "
          f"-> {'PASSE' if okR2 else 'ECHEC — rangee non exploitee'}")
    res_amas = {}
    if okR2:
        bC = chi2_amas(z, f, sig, s_ccbh, "C")
        dR2 = bC.fun - b1.fun
        p1 = chi2_amas(z, f, sig, un, "L", niveau_libre=True)
        pC = chi2_amas(z, f, sig, s_ccbh, "C", niveau_libre=True)
        dR2p = pC.fun - p1.fun
        print(f"[R2 AMAS] Dchi2(CCBH) = {dR2:+.2f}  dont PENTE seule (niveau libre, K1+Y1 libres) = {dR2p:+.2f}")
        print(f"          nuisances poussees (CCBH) : K = {bC.x[0]:.3f} (prior 0,90±0,09), K1 = {bC.x[1]:+.3f}, "
              f"Y0 = {bC.x[2]:.3f} (boite 0,763-0,932), Y1 = {bC.x[3]:+.3f}, Ob/Om = {bC.x[4]:.4f}")
        res_amas = dict(dchi2=round(dR2, 2), dchi2_pente=round(dR2p, 2),
                        nuisances_ccbh=dict(K=round(float(bC.x[0]), 3), K1=round(float(bC.x[1]), 3),
                                            Y0=round(float(bC.x[2]), 3), Y1=round(float(bC.x[3]), 3),
                                            ObOm=round(float(bC.x[4]), 4)))
    e_c = (WB_CMB - WB_BBN_C)/np.hypot(S_BBN_C, S_CMB)
    e_s = (WB_CMB - WB_BBN_S)/np.hypot(S_BBN_S, S_CMB)
    print(f"[R3 wb]   BBN vs CMB : {e_c:.1f} sigma (Cooke 2018, taux Marcucci) / {e_s:.1f} sigma (Schoeneberg 2024) — "
          f"rapporte ; aucun modele de l'atlas ne consomme avant la recombinaison")
    tot = round(float(dR1) + res_amas.get("dchi2", 0.0), 2)
    lignes = dict(date=str(datetime.date.today()),
                  hypothese="(i) consommation uniforme en environnement — si halo blinde (ii), R2 nulle et non falsifiante, seul R1 porte",
                  R1_frb=dict(valide=bool(okR1), dchi2_ccbh=round(float(dR1), 2), n=69),
                  R2_amas=dict(valide=bool(okR2), n=40, **res_amas),
                  R3_wb=dict(cooke2018_sigma=round(float(e_c), 1), schoeneberg2024_sigma=round(float(e_s), 1), discriminant=False),
                  total_ccbh=tot)
    (ROOT / "registres/ledger.json").write_text(json.dumps(lignes, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    lb_p = ROOT / "registres/atlas_leaderboard.json"
    lb = json.loads(lb_p.read_text(encoding="utf-8"))
    for m in lb["modeles"]:
        if m["nom"].startswith("CCBH"):
            m["ledger"] = dict(dchi2=tot, detail=f"FRB {dR1:+.1f} ; amas {res_amas.get('dchi2', 0):+.1f} (pente {res_amas.get('dchi2_pente', 0):+.1f}) ; hypothese (i)")
        else:
            m["ledger"] = dict(dchi2=0.0, detail="s(z) = 1 : bilan baryonique neutre" + (" ; echange sombre en v2" if m["nom"].startswith("iLCDM") else ""))
    lb_p.write_text(json.dumps(lb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    L = ["# LE GRAND LIVRE — la comptabilité baryonique (généré par `outils/ledger.py`, ne pas éditer)", "",
         f"*{lignes['date']} — le fond ne sépare pas les modèles sourcés (#139) ; ce qu'ils consomment laisse un trou dans un budget.*",
         f"*Hypothèse déclarée : {lignes['hypothese']}.*", "",
         "| rangée | validation | Δχ²(CCBH, s(z)) | note |", "|---|---|---|---|",
         f"| R1 — FRB (69 réels) | f_d = {fdL:.3f} | **{dR1:+.2f}** | machinerie E3 v1 gelée |",
         (f"| R2 — amas (40 f_gas Mantz 2014) | χ²/40 = {b1.fun/len(z):.2f} | **{res_amas.get('dchi2', 0):+.2f}** dont pente {res_amas.get('dchi2_pente', 0):+.2f} | priors Mantz (K, K₁, Υ₀, Υ₁) profilés ; d(z) recalculé par modèle |"
          if okR2 else "| R2 — amas | ÉCHEC | — | non exploitée |"),
         f"| R3 — ω_b BBN/CMB | {e_c:.1f}σ (Cooke) / {e_s:.1f}σ (Schöneberg) | — | déclarative : nul modèle ne consomme avant la recombinaison |", "",
         f"**Total CCBH : Δχ²_ledger = {tot:+.2f}.** Tous les autres modèles de l'atlas : s(z) = 1, bilan neutre",
         "(échanges sombres iΛCDM : rangée matière sombre en v2). Colonne fusionnée dans `atlas_leaderboard.json`.",
         "", "Sources : Mantz+14 (1402.6212, éq. 2, Table 3) ; Applegate+14/16 ; Battaglia+13, Planelles+13 ;",
         "Cooke+18 (1710.11129) ; Schöneberg 24 (2401.15054) ; Planck 18 VI ; Connor+25. Données : `donnees/amas_fgas/SOURCE.md`."]
    (ROOT / "registres/LEDGER.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"\n[ledger] écrits : ledger.json, LEDGER.md ; colonne fusionnée (CCBH : {tot:+.2f})")
