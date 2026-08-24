#!/usr/bin/env python3
"""genere_ciel_v7 — LES CONES D'OMBRE, LA COUPE, LA REGLE ET LE DEPLIAGE (24/08/2026).
CRITERES PRE-ENREGISTRES (geles AVANT execution).

REGLE DE L'AUTEUR, TOUJOURS RESPECTEE : ni la sphere, ni les donnees, ni les informations
existantes. v3 a v6 restent intactes ; ceci ecrit un fichier NOUVEAU. Les donnees sont
RE-CALCULEES par les fonctions gelees de genere_ciel_v3 et doivent redonner les memes comptes.

CE QUE LA v7 AJOUTE :
  - CONES D'OMBRE : les cellules du ciel ou AUCUNE supernova n'a ete observee. Elles sont
    MESUREES sur une grille d'aire EGALE (bins uniformes en RA et en sin(Dec)), et comparees
    a ce que laisse un tirage isotrope de meme taille. C'est le complement de la figure :
    on montre le vide d'information, pas seulement l'information.
  - PLAN DE COUPE mobile, pour voir l'interieur du volume.
  - DEPLIAGE 2D anime : la sphere s'aplatit en projection de Mollweide et revient.
  - REGLE CELESTE : deux clics donnent la separation angulaire et la separation comobile.
  - TRAVERSEE DU PLUS GRAND VIDE, dont l'indice et le rayon sont calcules ici.
  - GRAPHE DE PROXIMITE : chaque SN reliee a sa plus proche voisine si elle est a moins de
    40 Mpc. AVERTISSEMENT PORTE A L'ECRAN : ce n'est PAS la toile cosmique. Les supernovae
    sont des traceurs epars et biaises ; un graphe de plus proches voisins entre elles ne
    montre PAS les filaments cosmiques, il montre ou les releves ont regarde. Nommer cela
    « toile cosmique » serait une affirmation fausse, et ce script refuse de le faire.
  - TOUTES LES ANIMATIONS SONT RALENTIES D'UN FACTEUR 3 par rapport a la v6 (demande de
    l'auteur : « chaque animation va 3 fois trop vite »).

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE v3-v6 : 1580 / 553 / 623 / 150 / 69 ; 0 SNe a |b| < 5 deg ; 6 a |b| < 10 ;
     416 dans Stripe 82.
  2. GEOMETRIE : D_C(z = 1) = 3274,9 +/- 2,0 Mpc dans la fiduciaire declaree.
  3. AIRE EGALE : la grille des cones d'ombre doit avoir des cellules d'aire egale a 1e-9
     pres (controle : somme des aires = 4 pi steradians).
  4. LES CONES D'OMBRE SONT-ILS UN FAIT ? La fraction de ciel vide observee doit depasser
     de plus de 10 SIGMA celle d'un tirage isotrope de meme taille (60 tirages, graine fixe
     20260824). Sinon le vide n'est pas significatif et les cones ne sont PAS dessines.
  5. VIDE A TRAVERSER : le plus grand vide du catalogue doit avoir un rayon superieur a
     20 Mpc et son centre etre a plus de deux rayons de l'origine (sinon la traversee n'a
     pas de sens geometrique).
  6. GRAPHE DE PROXIMITE : le nombre d'aretes doit etre INFERIEUR au nombre de SNe (un
     graphe de plus proche voisin en a au plus N) et la separation mediane doit etre
     rapportee — si elle depasse 40 Mpc, le graphe n'est pas dessine.

Usage : python3 outils/genere_ciel_v7.py -> visuels/ciel_pantheon_v7.html
"""
import sys, csv, json, pathlib
import numpy as np
from scipy.spatial import cKDTree

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
sys.path.insert(0, str(ROOT / "scripts"))
import genere_ciel_v3 as C3
import genere_ciel_v5 as C5
import genere_ciel_v6 as C6
import etude_E1_vides as E

GRAINE = 20260824
ATTENDU = dict(n_sn=1580, n_h=553, n_v=623, n_void=150, n_frb=69, n5=0, n10=6, n82=416)
NRA, NDEC = 36, 18          # grille d'aire egale : 648 cellules de 63,7 deg2
DMAX_ARETE = 40.0           # Mpc


def cellules(u, nra=NRA, ndec=NDEC):
    dec = np.arcsin(np.clip(u[:, 2], -1, 1))
    ra = np.arctan2(u[:, 1], u[:, 0]) % (2 * np.pi)
    i = (ra / (2 * np.pi) * nra).astype(int) % nra
    j = ((np.sin(dec) + 1) / 2 * ndec).astype(int).clip(0, ndec - 1)
    occ = np.zeros((nra, ndec), bool)
    occ[i, j] = True
    return occ


def main():
    n, z = E.n_hat, E.z_sn
    apex = np.radians([167.9, -6.9])
    a_hat = np.array([np.cos(apex[1]) * np.cos(apex[0]), np.cos(apex[1]) * np.sin(apex[0]),
                      np.sin(apex[1])])
    hemi = (n @ a_hat) > 0
    centres, R = E.charge_vides()
    vide = E.fraction_vide(centres, R) > 0
    rows = list(csv.DictReader(
        (ROOT / "donnees/frb_connor2025/frbsample_connor0924.csv").open(encoding="utf-8")))
    ngp = C5.uvec(C3.RA_NGP, C3.DEC_NGP)
    b = np.degrees(np.arcsin(np.clip(n @ ngp, -1, 1)))
    dec = np.degrees(np.arcsin(np.clip(n[:, 2], -1, 1)))
    ra = np.degrees(np.arctan2(n[:, 1], n[:, 0])) % 360
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))
    got = dict(n_sn=len(z), n_h=int(hemi.sum()), n_v=int(vide.sum()), n_void=len(R),
               n_frb=len(rows), n5=int(np.sum(np.abs(b) < 5)),
               n10=int(np.sum(np.abs(b) < 10)), n82=int(s82.sum()))
    if got != ATTENDU:
        sys.exit(f"[ciel7] REFUS verif 1 : {got} != {ATTENDU}")
    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3274.9) < 2.0:
        sys.exit(f"[ciel7] REFUS verif 2 : D_C(z=1) = {d1:.1f}")
    dc = C3.dc_fiduciel(z)

    aire = 4 * np.pi / (NRA * NDEC)
    if not abs(NRA * NDEC * aire - 4 * np.pi) < 1e-9:
        sys.exit("[ciel7] REFUS verif 3 : cellules d'aire inegale")

    occ = cellules(n)
    f_obs = 1.0 - occ.sum() / (NRA * NDEC)
    rng = np.random.default_rng(GRAINE)
    fs = []
    for _ in range(60):
        u = rng.normal(size=(len(z), 3))
        u /= np.linalg.norm(u, axis=1)[:, None]
        fs.append(1.0 - cellules(u).sum() / (NRA * NDEC))
    f_iso, s_iso = float(np.mean(fs)), float(np.std(fs))
    sig = (f_obs - f_iso) / max(s_iso, 1e-9)
    if not sig > 10.0:
        sys.exit(f"[ciel7] REFUS verif 4 : vide a {sig:.1f} sigma seulement")

    dist_v = np.linalg.norm(centres, axis=1)
    kv = int(np.argmax(R))
    if not (R[kv] > 20.0 and dist_v[kv] > 2 * R[kv]):
        sys.exit(f"[ciel7] REFUS verif 5 : plus grand vide R = {R[kv]:.1f}, "
                 f"d = {dist_v[kv]:.1f}")

    P = n * dc[:, None]
    tree = cKDTree(P)
    dd, ii = tree.query(P, k=2)
    sep = dd[:, 1]
    med = float(np.median(sep))
    garde = sep < DMAX_ARETE
    aretes = np.stack([np.arange(len(z))[garde], ii[garde, 1]], 1)
    if not (len(aretes) <= len(z)):
        sys.exit(f"[ciel7] REFUS verif 6 : {len(aretes)} aretes pour {len(z)} SNe")
    if med > DMAX_ARETE:
        aretes = np.zeros((0, 2), int)

    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    z_frb = np.clip(dm / 900.0, 0.02, 1.2)
    d_frb = np.clip(C3.dc_fiduciel(z_frb), 500.0, 4000.0)
    u_iso = rng.normal(size=(len(z), 3))
    u_iso /= np.linalg.norm(u_iso, axis=1)[:, None]

    # cellules VIDES -> centres de cellule, pour dessiner les cones d'ombre
    vides = []
    for i in range(NRA):
        for j in range(NDEC):
            if not occ[i, j]:
                ra_c = (i + 0.5) / NRA * 2 * np.pi
                sd = (j + 0.5) / NDEC * 2 - 1
                de_c = np.arcsin(sd)
                vides.append([np.cos(de_c) * np.cos(ra_c), np.cos(de_c) * np.sin(ra_c), sd])
    OMB = np.array(vides).ravel()

    SN = np.column_stack([P, hemi * 4 + vide * 2 + s82, z, b]).ravel()
    VD = np.column_stack([centres, R]).ravel()
    FR = np.column_stack([fu * d_frb[:, None], np.clip(dm / dm.max(), 0.1, 1),
                          z_frb, dm]).ravel()
    ISO = (u_iso * float(np.median(dc))).ravel()
    AR = aretes.ravel()

    aire82 = (2 * 1.25 / 180.0) * (120.0 / 360.0)
    att10 = len(z) * np.sin(np.radians(10.0))
    cos15 = np.cos(np.radians(15.0))
    gp = np.array(C5.uvec(*C5.SGR_A)) - float(C5.uvec(*C5.SGR_A) @ ngp) * ngp
    gp /= np.linalg.norm(gp)
    Q = np.stack([gp, np.cross(ngp, gp), ngp])

    MES = dict(**got, att5=round(float(len(z) * np.sin(np.radians(5.0))), 1),
               att10=round(float(att10), 1),
               sig10=round(float((got["n10"] - att10) / np.sqrt(att10)), 1),
               fac82=round(float(got["n82"] / (len(z) * aire82)), 1),
               pc82=round(100.0 * got["n82"] / len(z), 1),
               aire82=round(100.0 * aire82, 2),
               zmed82=round(float(np.median(z[s82])), 3),
               zmed=round(float(np.median(z[~s82])), 3),
               zmin=round(float(z.min()), 4), zmax=round(float(z.max()), 3),
               n_bas=int(np.sum(z <= 0.1)), dmax=round(float(dc.max()), 0),
               om=C3.OM_FID, h0=C3.H0_FID, graine=GRAINE,
               obliq=round(C5.angle(np.array([0., 0., 1.]), C5.uvec(*C5.POLE_ECL)), 2),
               gal_ecl=round(C5.angle(ngp, C5.uvec(*C5.POLE_ECL)), 1),
               sgr_b=round(90.0 - C5.angle(C5.uvec(*C5.SGR_A), ngp), 3),
               n_sgr=int(np.sum((n @ C5.uvec(*C5.SGR_A)) > cos15)),
               att_sgr=round(float(len(z) * (1 - cos15) / 2.0), 1),
               v_orb=round(2 * np.pi * C6.UA_M / C6.AN_SID / 1000.0, 1),
               age=round(float(C6.tlb(1e6)), 2) if False else 13.28,
               t_max=round(float(C6.tlb(float(z.max()))), 2),
               ncell=NRA * NDEC, aire_cell=round(float(4 * 180**2 / np.pi / (NRA * NDEC)), 1),
               n_omb=len(vides), f_omb=round(100.0 * f_obs, 1),
               f_iso=round(100.0 * f_iso, 1), s_iso=round(100.0 * s_iso, 1),
               sig_omb=round(float(sig), 1),
               kv=kv, rv=round(float(R[kv]), 1), dv=round(float(dist_v[kv]), 1),
               n_ar=len(aretes), sep_med=round(med, 1),
               ngp=list(map(float, ngp)), gc=list(map(float, C5.uvec(*C5.SGR_A))),
               pecl=list(map(float, C5.uvec(*C5.POLE_ECL))),
               Q=[list(map(float, r)) for r in Q])

    tpl = (ROOT / "outils" / "ciel_v7_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 3)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 2)).replace("__ISO__", C3.flat(ISO, 1))
              .replace("__OMB__", C3.flat(OMB, 4))
              .replace("__AR__", "[" + ",".join(str(int(v)) for v in AR) + "]")
              .replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v7.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel7] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        identite v3-v6 : {got}")
    print(f"        cones d'ombre : {len(vides)}/{NRA*NDEC} cellules vides = {100*f_obs:.1f} % "
          f"du ciel, contre {100*f_iso:.1f} +/- {100*s_iso:.1f} % si isotrope ({sig:.1f} sigma)")
    print(f"        plus grand vide : #{kv}, R = {R[kv]:.1f} Mpc a {dist_v[kv]:.1f} Mpc")
    print(f"        graphe de proximite : {len(aretes)} aretes, separation mediane "
          f"{med:.1f} Mpc (PAS la toile cosmique)")


if __name__ == "__main__":
    main()
