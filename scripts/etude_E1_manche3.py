#!/usr/bin/env python3
"""E1 MANCHE 3 — DESIVAST DR1 x PANTHEON+ : le troisieme juge, et l'ARBITRE DE T6.
CRITERES PRE-ENREGISTRES (geles AVANT la premiere execution, 24/08/2026).
Ferme la liste de donnees de la spec mere (etudes_2026.py, gelee), qui nommait DESIVAST
DR1 BGS des l'origine. Manches 1-2 : universel (goulet 2-0, #141-142). T6 (greffe) : sur
Douglass, VoidFinder (+0,52) et VIDE (-0,40) donnaient des signes OPPOSES — arbitre grave :
« manche 3 sur catalogue profond avec les MEMES algorithmes ».

DONNEES (sha256 dans donnees/SHA256SUMS ; source donnees/vides_desivast/SOURCE.md).
  DESIVAST DR1 BGS VOLLIM (Rincon et al. 2025, ApJ 982, 38 ; portail public DESI, VAC v1.0),
  deux calottes NGC+SGC (~2900 deg2), z < 0,24, cosmologie d'en-tete Om = 0,315, Mpc/h :
    VoidFinder : 3765 spheres maximales (ra, dec, dist, reff) — une par vide (l'union des
      HOLES reste dans les FITS ; approximation declaree) ;
    V2/VIDE : 1478 et V2/REVOLVER : 1992 (ra, dec, z, reff) — spheres de rayon effectif
      (approximation declaree), distance comobile calculee a Om = 0,315 (leur en-tete).
  SNe RETENUES : direction a moins de 3 deg d'un centre VoidFinder — 227 comptees AVANT
  gel (taille, pas un resultat). ~114 par moitie -> sigma_Delta attendu ~0,6-0,7 : TEST
  FAIBLE, DECLARE. Plancher : 80 par sous-echantillon. Profondeur : min(d_SN, 675 h-1 Mpc).

METHODE : identique a la manche 2 (fraction de ligne de visee dans l'union des spheres,
partage a la mediane — ou f>0/f=0 si mediane nulle —, beta SN-seules a Om = 0,314 fixe par
sous-echantillon, machinerie gelee de etude_E1_vides ; controle par 200 permutations de f,
graine 20260824).

CRITERES (exhaustifs, exclusifs).
  A. MANCHE 3 DU DUEL (spec mere) : par catalogue, ECART si |Delta_beta| > 2 sigma_Delta ET
     p_perm < 0,05 ; NUL sinon. NON EXPLOITE si un sous-echantillon < 80, ou sigma_perm >
     2 sigma_Delta, ou les trois algorithmes divergent par paire > 2 sigma. Verdict du duel :
     UNIVERSEL si tous NUL (trois juges, goulet 3-0) ; CANDIDAT si ECART coherent.
  B. ARBITRAGE DE T6 (le point neuf) — sur les signes VoidFinder contre VIDE :
     - NON-UNIVOCITE REPRODUITE si signes opposes ET chacun a >= 1 sigma de 0 : T6 se resout
       « le vide n'est pas univoque » — la definition du vide devient l'objet ;
     - FLUCTUATIONS si les deux sont a < 1 sigma de 0 : T6 se resout « bruit a petit N » ;
     - sinon T6 RESTE OUVERTE, ecrit tel quel (le test est faible, c'etait declare).
     La resolution eventuelle de T6 passe par le greffier (arbitre nomme = ce script).
  Le Jaccard des tris est rapporte (manche 2 : 0,33). Valeurs de substitution : aucune.
Usage : python3 scripts/etude_E1_manche3.py   (depuis la racine)
"""
import sys, csv, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E
import etude_E1_manche2 as M2

DV = ROOT / "donnees" / "vides_desivast"
OM_CAT = 0.315; D_CAT = 675.0; THETA = 3.0; N_PERM = 200; GRAINE = 20260824; PLANCHER = 80

_zg = np.linspace(0, 0.5, 3000); _Ez = np.sqrt(OM_CAT*(1+_zg)**3 + 1-OM_CAT)
_Dc = E.C_SUR_H0*np.concatenate([[0], np.cumsum(0.5*(1/_Ez[1:]+1/_Ez[:-1])*np.diff(_zg))])

def uv(ra, dec):
    ra = np.radians(np.asarray(ra) % 360.0); dec = np.radians(np.asarray(dec))
    return np.stack([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)], 1)

def charge():
    cat = {}
    rows = list(csv.DictReader((DV / "DESIVAST_BGS_VOLLIM_VoidFinder_voids.csv").open(encoding="utf-8")))
    d = np.array([float(r["dist"]) for r in rows])
    u = uv([float(r["ra"]) for r in rows], [float(r["dec"]) for r in rows])
    cat["VoidFinder"] = (d[:, None]*u, np.array([float(r["reff"]) for r in rows]))
    for nom, f in [("VIDE", "DESIVAST_BGS_VOLLIM_V2_VIDE_voids.csv"),
                   ("REVOLVER", "DESIVAST_BGS_VOLLIM_V2_REVOLVER_voids.csv")]:
        rows = list(csv.DictReader((DV / f).open(encoding="utf-8")))
        z = np.array([float(r["z"]) for r in rows])
        d = np.interp(z, _zg, _Dc)
        u = uv([float(r["ra"]) for r in rows], [float(r["dec"]) for r in rows])
        cat[nom] = (d[:, None]*u, np.array([float(r["reff"]) for r in rows]))
    return cat

if __name__ == "__main__":
    print("E1 MANCHE 3 — DESIVAST DR1 x Pantheon+ (criteres geles ; arbitre de T6)\n")
    M2.D_CAT = D_CAT
    cat = charge()
    vf_dir = cat["VoidFinder"][0]/np.linalg.norm(cat["VoidFinder"][0], axis=1)[:, None]
    ang = np.degrees(np.arccos(np.clip((E.n_hat @ vf_dir.T).max(1), -1, 1)))
    idx = np.where(ang < THETA)[0]
    print(f"[0] SNe dans l'empreinte (theta < {THETA} deg) : {len(idx)}")
    for nom, (c, r) in cat.items():
        print(f"    {nom:10s} {len(r):5d} vides, reff = {r.min():.1f}-{r.max():.1f}, d <= {np.linalg.norm(c,axis=1).max():.0f} h-1 Mpc")

    non_exploite, res, sels = [], {}, {}
    rng = np.random.default_rng(GRAINE)
    for nom, (c, r) in cat.items():
        f = M2.fraction_union(c, r, idx); sel, med = M2.partage(f)
        sels[nom] = sel
        nv, nm = int(sel.sum()), int((~sel).sum())
        if min(nv, nm) < PLANCHER: non_exploite.append(f"{nom} : {nv}/{nm} < {PLANCHER}")
        bv, sv, bm, sm, dB, sD = M2.delta(idx, sel)
        nulls = []
        for _ in range(N_PERM):
            fp = rng.permutation(f); sp, _m = M2.partage(fp)
            if min(sp.sum(), (~sp).sum()) < 40: continue
            nulls.append(M2.delta(idx, sp, sigma=False)[4])
        nulls = np.array(nulls); s_perm = nulls.std(ddof=1); p_perm = float((np.abs(nulls) >= abs(dB)).mean())
        if s_perm > 2*sD: non_exploite.append(f"{nom} : sigma_perm {s_perm:.2f} > 2 sigma_D {sD:.2f}")
        ecart = abs(dB) > 2*sD and p_perm < 0.05
        res[nom] = dict(dB=float(dB), sD=float(sD), p=p_perm, ecart=ecart)
        print(f"\n[{nom}] mediane f = {med:.3f} ; partage {'mediane' if med > 0 else 'f>0/f=0'} -> {nv}/{nm}")
        print(f"    vides beta = {bv:.3f} +/- {sv:.3f} | murs beta = {bm:.3f} +/- {sm:.3f}")
        print(f"    Delta_beta = {dB:+.3f} +/- {sD:.3f} ({abs(dB)/sD:.2f} sigma) | perms : sigma = {s_perm:.3f}, "
              f"p = {p_perm:.3f} -> {'ECART' if ecart else 'NUL'}")
    noms = list(res)
    for i in range(3):
        for j in range(i+1, 3):
            a, b = res[noms[i]], res[noms[j]]
            if abs(a['dB']-b['dB']) > 2*np.hypot(a['sD'], b['sD']):
                non_exploite.append(f"{noms[i]}/{noms[j]} divergent > 2 sigma")
    jac = {}
    for i in range(3):
        for j in range(i+1, 3):
            a, b = sels[noms[i]], sels[noms[j]]
            jac[f"{noms[i]}-{noms[j]}"] = float((a & b).sum()/max((a | b).sum(), 1))
    print("\n[recouvrement] " + " ; ".join(f"Jaccard({k}) = {v:.2f}" for k, v in jac.items()) + "  (manche 2 : 0,33)")

    print("\n" + "="*72)
    if non_exploite:
        print("VERDICT MANCHE 3 : NON EXPLOITE — " + " ; ".join(non_exploite))
    elif all(r['ecart'] for r in res.values()):
        print("VERDICT MANCHE 3 : CANDIDAT — les trois algorithmes en ECART")
    else:
        print("VERDICT MANCHE 3 : UNIVERSEL — trois juges, goulet 3-0" if not any(r['ecart'] for r in res.values())
              else "VERDICT MANCHE 3 : MIXTE — ecrit tel quel")
    # arbitrage T6
    dv, dV = res["VoidFinder"], res["VIDE"]
    nv_, nV = abs(dv['dB'])/dv['sD'], abs(dV['dB'])/dV['sD']
    opp = np.sign(dv['dB']) != np.sign(dV['dB'])
    if opp and nv_ >= 1 and nV >= 1:
        t6 = "NON-UNIVOCITE REPRODUITE : signes opposes a >= 1 sigma chacun — T6 se resout « le vide n'est pas univoque »"
    elif nv_ < 1 and nV < 1:
        t6 = "FLUCTUATIONS : les deux compatibles avec 0 a < 1 sigma — T6 se resout « bruit a petit N » (manche 2 comprise)"
    else:
        t6 = "T6 RESTE OUVERTE : configuration mixte, le test est faible (declare) — ecrit tel quel"
    print(f"ARBITRAGE T6 : VF {dv['dB']:+.2f} ({nv_:.1f} sig) vs VIDE {dV['dB']:+.2f} ({nV:.1f} sig), "
          f"{'signes opposes' if opp else 'meme signe'} -> {t6}")
    print("="*72)
