#!/usr/bin/env python3
"""genere_ciel_v8 — INTERFACE REORGANISEE, INSPECTEUR, LECTURE DU TEMPS, CONTRASTE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

REGLE DE L'AUTEUR, TOUJOURS RESPECTEE : ni la sphere, ni les donnees, ni les informations
existantes. v3 a v7 restent intactes ; ceci ecrit un fichier NOUVEAU. Les comptes sont
RE-CALCULES par les fonctions gelees de genere_ciel_v3 et doivent redonner les memes valeurs.

CE QUE LA v8 AJOUTE :
  - INTERFACE en trois zones (navigation en haut, outils a gauche, filtres et mesures a
    droite), panneaux repliables — reorganisation ergonomique, aucune affirmation nouvelle ;
  - INSPECTEUR : au survol, rayon depuis la Terre + fiche (z, distance comobile, (l, b),
    vide sur la visee, appartenance a Stripe 82) ;
  - LECTURE DU TEMPS : le curseur de redshift s'anime, de z = 0 vers z max ;
  - CONTRASTE DE SELECTION : la taille des points suit leur DENSITE LOCALE, mesuree ici
    comme le nombre de voisines dans un rayon angulaire de 3 degres ;
  - CAPTURE HD (x2) sans interface, et RACCLAGES de camera au clavier (P poles, G axe
    galactique, E par la tranche).

LA DONNEE NOUVELLE EST MESUREE, PAS SUPPOSEE. La densite locale de chaque supernova est le
nombre de ses voisines a moins de 3 degres (corde 2 sin(1,5 deg)), calculee par arbre k-d.
Elle sert UNIQUEMENT a moduler la taille des points ; aucun resultat n'en depend.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE v3-v7 : 1580 / 553 / 623 / 150 / 69 ; 0 SNe a |b| < 5 deg ; 6 a |b| < 10 ;
     416 dans Stripe 82.
  2. GEOMETRIE : D_C(z = 1) = 3274,9 +/- 2,0 Mpc dans la fiduciaire declaree.
  3. LE CONTRASTE EST-IL UN FAIT ? La densite locale MEDIANE dans Stripe 82 doit valoir plus
     de TROIS FOIS celle du reste de l'echantillon. Sinon le curseur de contraste montrerait
     un effet qui n'existe pas, et il n'est PAS ecrit. Le rapport reel est rapporte, quel
     qu'il soit — c'est lui qui sera affiche a l'ecran, pas un chiffre rond.
  4. COHERENCE DU COMPTE : la densite d'une supernova compte ses voisines, elle-meme exclue ;
     la somme des densites doit donc etre PAIRE (chaque paire comptee deux fois). Un total
     impair signalerait une erreur d'indexation.
  5. LECTURE DU TEMPS : le curseur doit couvrir tout l'echantillon, z_min < 0,02 et
     z_max > 2,0.

Usage : python3 outils/genere_ciel_v8.py -> visuels/ciel_pantheon_v8.html
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
RAYON_DEG = 3.0


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
        sys.exit(f"[ciel8] REFUS verif 1 : {got} != {ATTENDU}")
    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3274.9) < 2.0:
        sys.exit(f"[ciel8] REFUS verif 2 : D_C(z=1) = {d1:.1f}")
    dc = C3.dc_fiduciel(z)

    corde = 2 * np.sin(np.radians(RAYON_DEG) / 2)
    tree = cKDTree(n)
    dens = np.array([len(v) - 1 for v in tree.query_ball_point(n, corde)])
    if int(dens.sum()) % 2 != 0:
        sys.exit(f"[ciel8] REFUS verif 4 : somme des densites impaire ({dens.sum()})")
    d82, dho = float(np.median(dens[s82])), float(np.median(dens[~s82]))
    rap = d82 / max(dho, 1e-9)
    if not rap > 3.0:
        sys.exit(f"[ciel8] REFUS verif 3 : contraste de densite {rap:.2f}x seulement "
                 f"({d82:.0f} contre {dho:.0f})")
    if not (z.min() < 0.02 and z.max() > 2.0):
        sys.exit(f"[ciel8] REFUS verif 5 : z dans [{z.min():.3f} ; {z.max():.3f}]")

    dn = dens / max(dens.max(), 1)
    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    z_frb = np.clip(dm / 900.0, 0.02, 1.2)
    d_frb = np.clip(C3.dc_fiduciel(z_frb), 500.0, 4000.0)
    rng = np.random.default_rng(GRAINE)
    u = rng.normal(size=(len(z), 3))
    iso = u / np.linalg.norm(u, axis=1)[:, None]

    SN = np.column_stack([n * dc[:, None], hemi * 4 + vide * 2 + s82, z, b, dn]).ravel()
    VD = np.column_stack([centres, R]).ravel()
    FR = np.column_stack([fu * d_frb[:, None], np.clip(dm / dm.max(), 0.1, 1),
                          z_frb, dm]).ravel()
    ISO = (iso * float(np.median(dc))).ravel()

    aire82 = (2 * 1.25 / 180.0) * (120.0 / 360.0)
    att10 = len(z) * np.sin(np.radians(10.0))
    cos15 = np.cos(np.radians(15.0))
    sgr = C5.uvec(*C5.SGR_A)
    gp = sgr - float(sgr @ ngp) * ngp
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
               sgr_b=round(90.0 - C5.angle(sgr, ngp), 3),
               n_sgr=int(np.sum((n @ sgr) > cos15)),
               att_sgr=round(float(len(z) * (1 - cos15) / 2.0), 1),
               v_orb=round(2 * np.pi * C6.UA_M / C6.AN_SID / 1000.0, 1),
               age=13.28, t_max=round(float(C6.tlb(float(z.max()))), 2),
               ray=RAYON_DEG, d82=round(d82, 1), dho=round(dho, 1), rap=round(rap, 1),
               dmaxloc=int(dens.max()),
               ngp=list(map(float, ngp)), gc=list(map(float, sgr)),
               pecl=list(map(float, C5.uvec(*C5.POLE_ECL))),
               Q=[list(map(float, r)) for r in Q])

    tpl = (ROOT / "outils" / "ciel_v8_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 3)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 2)).replace("__ISO__", C3.flat(ISO, 1))
              .replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v8.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel8] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        identite v3-v7 : {got}")
    print(f"        densite locale (rayon {RAYON_DEG} deg) : mediane {d82:.0f} dans "
          f"Stripe 82 contre {dho:.0f} ailleurs = x{rap:.1f} ; maximum {dens.max()}")


if __name__ == "__main__":
    main()
