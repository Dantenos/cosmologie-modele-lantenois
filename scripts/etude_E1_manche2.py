#!/usr/bin/env python3
"""E1 MANCHE 2 — DOUGLASS DR7 x PANTHEON+ : le deuxieme catalogue de vides. CRITERES
PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 23/08/2026).
Spec mere : etudes_2026.py (gelee). Manche 2 v0 : etude_E1_vides.py (gele) -> Stopyra 2023,
Delta_beta = +0,096 +/- 0,236, UNIVERSEL.

DONNEES (empreintes dans donnees/SHA256SUMS).
  - Pantheon+ : memes coupures que le corpus (zHD > 0,01, calibrateurs exclus, 1580 SNe).
  - Douglass, Veyrat & BenZvi 2023, CDS J/ApJS/265/7, cosmologie Planck 2018 (Om = 0,315) :
      VoidFinder : table2, TOUTES les spheres (39 735), un vide = union de ses spheres ;
      VIDE (531) et REVOLVER (518) : table3, centre pondere + rayon effectif, traites
      comme des SPHERES (approximation declaree : les vides ZOBOV ne sont pas spheriques).
    Les trois partagent le MEME echantillon de galaxies SDSS DR7 : ils comptent pour UN juge
    (Douglass), avec controle de coherence interne. Stopyra 2023 est le second juge.
  - Empreinte : le catalogue ne couvre que SDSS NGC (RA 112-259, Dec -2..67, z < 0,114).
    SNe RETENUES = celles dont la direction est a moins de 3 deg d'un centre VoidFinder
    (table1) : 455 SNe comptees AVANT gel (taille d'echantillon, pas un resultat).
    Profondeur : segment [0 ; min(d_SN, 330 h-1 Mpc)], distances LCDM plat Om = 0,315.

METHODE (identique a la manche 2 v0, sauf ce qui est dit ici).
  1. f = longueur de ligne de visee dans l'UNION des vides / longueur du segment, par
     catalogue (intervalles fusionnes, pas de double comptage des spheres qui se recouvrent).
  2. Partage a la mediane de f parmi les SNe retenues ; si mediane nulle, f > 0 / f = 0.
  3. beta par sous-echantillon : SN seules, Om fixe 0,314, M marginalise, covariance pleine
     restreinte, sigma par Delta_chi2 = 1 (fit_beta de etude_E1_vides.py, reutilise).
  4. CONTROLE D'EQUITE : les rotations sont impossibles (empreinte limitee). A la place,
     200 permutations de f parmi les SNe retenues (graine 20260823) -> sigma_perm, p_perm.
  DECLARE D'AVANCE : ~230 SNe par moitie -> sigma_Delta attendu ~0,5. Test faible. Un nul
  ici ne ferme rien en dessous de ~1 en Delta_beta ; il est rapporte comme tel.

CRITERES (exhaustifs, exclusifs).
  - NON EXPLOITE si : un sous-echantillon < 150 SNe ; OU les trois algorithmes divergent
    entre eux (|Delta_beta_i - Delta_beta_j| > 2 sqrt(s_i^2 + s_j^2) pour une paire) — le
    desaccord des juges n'est pas un verdict ; OU sigma_perm > 2 sigma_Delta.
  - Verdict Douglass : ECART si les trois algorithmes donnent |Delta_beta| > 2 sigma_Delta
    ET p_perm < 0,05 ; NUL sinon.
  - VERDICT MANCHE 2 (spec mere, deux juges) :
      SIGNAL    si Stopyra ET Douglass donnent ECART de meme signe — impossible ici,
                Stopyra a donne 0,4 sigma ; ecrit pour l'exhaustivite.
      CANDIDAT  si Douglass seul donne ECART : en attente d'un troisieme catalogue
                (Malandrino 2026). Le signe est rapporte, pas interprete.
      UNIVERSEL si Douglass donne NUL : manche 2 au goulet, sur deux juges.
  Ce que cela REDUIT, dans tous les cas : |Delta_beta| au niveau de 2 sigma_Delta, dans
  l'empreinte SDSS, d < 330 h-1 Mpc. Ce que cela ne ferme PAS : un effet < sigma_Delta.
  Verse dans l'affaire Audience W-universel. Valeurs de substitution : aucune.

Usage : python3 scripts/etude_E1_manche2.py  (depuis la racine du depot)
"""
import sys, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E          # charge Pantheon+, n_hat, z_sn, fit_beta, machinerie

DD = ROOT / "donnees" / "vides_douglass2023"
OM_CAT = 0.315; D_CAT = 330.0; THETA = 3.0; N_PERM = 200; GRAINE = 20260823; PLANCHER = 150

# distances comobiles des SNe dans la cosmologie du catalogue
_zg = np.linspace(0, 3, 6000); _Ez = np.sqrt(OM_CAT*(1+_zg)**3 + 1-OM_CAT)
_Dc = E.C_SUR_H0*np.concatenate([[0], np.cumsum(0.5*(1/_Ez[1:]+1/_Ez[:-1])*np.diff(_zg))])
d_sn = np.interp(E.z_sn, _zg, _Dc)

def lignes(t):
    return [l for l in (DD / t).open(encoding="utf-8") if l.startswith("Planck")]

def charge():
    """Retourne {nom: (centres xyz, rayons)} et les centres VoidFinder (empreinte)."""
    t1 = lignes("table1.dat")
    ra = np.radians([float(l[123:141]) for l in t1]); de = np.radians([float(l[142:162]) for l in t1])
    vf_dir = np.stack([np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)], 1)
    t2 = lignes("table2.dat")
    vf_c = np.array([[float(l[11:31]), float(l[32:57]), float(l[58:80])] for l in t2])
    vf_r = np.array([float(l[81:100]) for l in t2])
    t3 = lignes("table3.dat")
    cat = {"VoidFinder": (vf_c, vf_r)}
    for prune in ("VIDE", "REVOLVER"):
        sel = [l for l in t3 if l[11:19].strip() == prune]
        c = np.array([[float(l[20:40]), float(l[41:63]), float(l[64:85])] for l in sel])
        r = np.array([float(l[147:165]) for l in sel])
        cat[prune] = (c, r)
    return cat, vf_dir

def fraction_union(centres, R, idx):
    """f_i pour les SNe idx : mesure de l'union des chords dans [0, L_i]."""
    L = np.minimum(d_sn[idx], D_CAT); out = np.zeros(len(idx))
    c2 = (centres**2).sum(1)
    for k, i in enumerate(idx):
        tc = centres @ E.n_hat[i]; disc = R**2 - (c2 - tc**2)
        m = disc > 0
        if not m.any(): continue
        h = np.sqrt(disc[m]); t0 = np.clip(tc[m]-h, 0, L[k]); t1 = np.clip(tc[m]+h, 0, L[k])
        keep = t1 > t0
        if not keep.any(): continue
        a = np.sort(np.stack([t0[keep], t1[keep]], 1), axis=0)[np.argsort(t0[keep])]
        tot, cur0, cur1 = 0.0, a[0,0], a[0,1]
        for s, e in a[1:]:
            if s > cur1: tot += cur1-cur0; cur0, cur1 = s, e
            else: cur1 = max(cur1, e)
        tot += cur1-cur0
        out[k] = min(tot/L[k], 1.0)
    return out

def partage(f):
    med = np.median(f)
    return (f >= med) if med > 0 else (f > 0), med

def delta(idx, sel, sigma=True):
    bv, sv = E.fit_beta(idx[sel], sigma); bm, sm = E.fit_beta(idx[~sel], sigma)
    return bv, sv, bm, sm, bv-bm, (np.hypot(sv, sm) if sigma else None)

if __name__ == "__main__":
    print("E1 MANCHE 2 — Douglass DR7 x Pantheon+ (criteres geles, voir docstring)\n")
    cat, vf_dir = charge()
    ang = np.degrees(np.arccos(np.clip((E.n_hat @ vf_dir.T).max(1), -1, 1)))
    idx = np.where(ang < THETA)[0]
    print(f"[0] SNe dans l'empreinte (theta < {THETA} deg) : {len(idx)} ; "
          f"z < 0,114 : {(E.z_sn[idx] < 0.114).sum()}")
    for nom, (c, r) in cat.items():
        print(f"    {nom:10s} {len(r):6d} spheres, R = {r.min():.1f}-{r.max():.1f}, d <= {np.linalg.norm(c,axis=1).max():.0f}")

    non_exploite, res = [], {}
    rng = np.random.default_rng(GRAINE)
    for nom, (c, r) in cat.items():
        f = fraction_union(c, r, idx); sel, med = partage(f)
        nv, nm = sel.sum(), (~sel).sum()
        if min(nv, nm) < PLANCHER: non_exploite.append(f"{nom} : sous-echantillon {nv}/{nm} < {PLANCHER}")
        bv, sv, bm, sm, dB, sD = delta(idx, sel)
        nulls = []
        for _ in range(N_PERM):
            fp = rng.permutation(f); sp, _m = partage(fp)
            if min(sp.sum(), (~sp).sum()) < 50: continue
            nulls.append(delta(idx, sp, sigma=False)[4])
        nulls = np.array(nulls); s_perm = nulls.std(ddof=1); p_perm = (np.abs(nulls) >= abs(dB)).mean()
        if s_perm > 2*sD: non_exploite.append(f"{nom} : sigma_perm {s_perm:.2f} > 2 sigma_Delta {sD:.2f}")
        ecart = abs(dB) > 2*sD and p_perm < 0.05
        res[nom] = dict(dB=dB, sD=sD, ecart=ecart)
        print(f"\n[{nom}] f : mediane={med:.3f} moyenne={f.mean():.3f} f>0 : {(f>0).sum()} ; "
              f"partage {'mediane' if med > 0 else 'f>0 / f=0'} -> {nv}/{nm}")
        print(f"    vides beta = {bv:.3f} +/- {sv:.3f} | murs beta = {bm:.3f} +/- {sm:.3f}")
        print(f"    Delta_beta = {dB:+.3f} +/- {sD:.3f} ({abs(dB)/sD:.2f} sigma) | "
              f"{len(nulls)} permutations : sigma_perm = {s_perm:.3f}, p = {p_perm:.3f} -> "
              f"{'ECART' if ecart else 'NUL'}")

    # coherence interne des trois algorithmes
    noms = list(res)
    for i in range(3):
        for j in range(i+1, 3):
            a, b = res[noms[i]], res[noms[j]]
            if abs(a['dB']-b['dB']) > 2*np.hypot(a['sD'], b['sD']):
                non_exploite.append(f"{noms[i]} et {noms[j]} divergent > 2 sigma")

    print("\n" + "="*72)
    if non_exploite:
        v = "NON EXPLOITE — " + " ; ".join(non_exploite)
    elif all(r['ecart'] for r in res.values()):
        v = "CANDIDAT — Douglass ECART, Stopyra nul : en attente d'un troisieme catalogue"
    else:
        v = "UNIVERSEL — manche 2 au goulet, sur deux juges (Stopyra 2023, Douglass 2023)"
    sDmax = max(r['sD'] for r in res.values())
    print(f"VERDICT E1 MANCHE 2 : {v}")
    print(f"Ce que cela reduit : |Delta_beta| < {2*sDmax:.2f} (2 sigma) dans l'empreinte SDSS, d < {D_CAT:.0f} h-1 Mpc.")
    print("="*72)
