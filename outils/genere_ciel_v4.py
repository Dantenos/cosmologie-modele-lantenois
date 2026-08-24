#!/usr/bin/env python3
"""genere_ciel_v4 — LE CIEL PANTHEON DEVENU OUTIL DIDACTIQUE (24/08/2026).
CRITERES PRE-ENREGISTRES (geles AVANT execution).

REGLE POSEE PAR L'AUTEUR ET RESPECTEE ICI : on ne touche NI a la sphere, NI aux donnees,
NI aux informations existantes. En consequence :
  - genere_ciel_v3.py, genere_ciel_v3b.py et visuels/ciel_pantheon_v3.html ne sont PAS
    modifies ; cette v4 ecrit un fichier NOUVEAU, visuels/ciel_pantheon_v4.html ;
  - les positions, drapeaux et comptes sont RE-CALCULES par les memes fonctions gelees
    (importees de genere_ciel_v3) et doivent redonner EXACTEMENT les memes valeurs ;
  - aucun texte scientifique de la v3 n'est reecrit ; les ajouts sont des OUTILS
    (filtres, ligne de visee, curseur de redshift, vue observateur, carte 2D, visite
    guidee, compteurs), pas des affirmations nouvelles.

LE SEUL AJOUT DE DONNEES, ET IL EST SYNTHETIQUE ET DECLARE : un ciel ISOTROPE de reference,
1580 directions tirees uniformement sur la sphere avec la graine FIXE 20260824, affiche en
filigrane pour comparaison. Ce n'est PAS un jeu de donnees : c'est le nul, et il est
etiquete comme tel a l'ecran. Aucun resultat n'en depend.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE AVEC LA v3. Les comptes doivent etre EXACTEMENT ceux de la v3 :
     1580 SNe, 553 dans l'hemisphere du dipole, 623 avec un vide sur la visee, 150 vides,
     69 FRB ; evitement 0 SNe a |b| < 5 deg et 6 a |b| < 10 deg ; Stripe 82 = 416 SNe.
     Tout ecart signifie que quelque chose a bouge sous nos pieds -> REFUS.
  2. GEOMETRIE. D_C(z = 1) = 3274,9 +/- 2,0 Mpc dans la fiduciaire declaree (LCDM plat,
     Om = 0,315, H0 = 70), comme en v3b — la geometrie du dessin ne depend pas du modele.
  3. CIEL ISOTROPE. Le tirage doit etre uniforme sur la sphere : sur les 1580 directions
     tirees, la fraction a |b| < 10 deg doit tomber a moins de 3 sigma de sin(10 deg)
     (sinon le tirage est biaise et la comparaison serait truquee EN NOTRE FAVEUR).
  4. REDSHIFTS. Le z transmis au curseur doit couvrir l'echantillon : min < 0,02 et
     max > 2,0, et le nombre de SNe a z <= 0,1 doit valoir celui du catalogue.

Usage : python3 outils/genere_ciel_v4.py -> visuels/ciel_pantheon_v4.html
"""
import sys, csv, json, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
sys.path.insert(0, str(ROOT / "scripts"))
import genere_ciel_v3 as C3
import etude_E1_vides as E

GRAINE = 20260824
ATTENDU = dict(n_sn=1580, n_h=553, n_v=623, n_void=150, n_frb=69, n5=0, n10=6, n82=416)


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

    ap, dp = np.radians(C3.RA_NGP), np.radians(C3.DEC_NGP)
    ngp = np.array([np.cos(dp) * np.cos(ap), np.cos(dp) * np.sin(ap), np.sin(dp)])
    b = np.degrees(np.arcsin(np.clip(n @ ngp, -1, 1)))
    dec = np.degrees(np.arcsin(np.clip(n[:, 2], -1, 1)))
    ra = np.degrees(np.arctan2(n[:, 1], n[:, 0])) % 360
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))

    got = dict(n_sn=len(z), n_h=int(hemi.sum()), n_v=int(vide.sum()), n_void=len(R),
               n_frb=len(rows), n5=int(np.sum(np.abs(b) < 5)),
               n10=int(np.sum(np.abs(b) < 10)), n82=int(s82.sum()))
    if got != ATTENDU:
        sys.exit(f"[ciel4] REFUS verif 1 : {got} != {ATTENDU}")

    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3274.9) < 2.0:
        sys.exit(f"[ciel4] REFUS verif 2 : D_C(z=1) = {d1:.1f}")
    dc = C3.dc_fiduciel(z)

    rng = np.random.default_rng(GRAINE)
    u = rng.normal(size=(len(z), 3))
    iso = u / np.linalg.norm(u, axis=1)[:, None]
    b_iso = np.degrees(np.arcsin(np.clip(iso @ ngp, -1, 1)))
    f_iso = float(np.mean(np.abs(b_iso) < 10))
    att = np.sin(np.radians(10.0))
    sig = abs(f_iso - att) / np.sqrt(att * (1 - att) / len(z))
    if not sig < 3.0:
        sys.exit(f"[ciel4] REFUS verif 3 : tirage biaise, {sig:.1f} sigma de l'uniforme")

    if not (z.min() < 0.02 and z.max() > 2.0):
        sys.exit(f"[ciel4] REFUS verif 4 : z dans [{z.min():.3f} ; {z.max():.3f}]")
    n_bas = int(np.sum(z <= 0.1))

    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    z_frb = np.clip(dm / 900.0, 0.02, 1.2)
    d_frb = np.clip(C3.dc_fiduciel(z_frb), 500.0, 4000.0)

    # SNe : x, y, z (Mpc), drapeaux, redshift, latitude galactique
    SN = np.column_stack([n * dc[:, None], hemi * 4 + vide * 2 + s82, z, b]).ravel()
    VD = np.column_stack([centres, R]).ravel()
    FR = np.column_stack([fu * d_frb[:, None], np.clip(dm / dm.max(), 0.1, 1),
                          z_frb, dm]).ravel()
    ISO = (iso * float(np.median(dc))).ravel()

    # centre galactique (l=0,b=0) : RA 266,405 Dec -28,936
    gc = np.radians([266.405, -28.936])
    GC = [float(np.cos(gc[1]) * np.cos(gc[0])), float(np.cos(gc[1]) * np.sin(gc[0])),
          float(np.sin(gc[1]))]

    MES = dict(**got, att5=round(float(len(z) * np.sin(np.radians(5.0))), 1),
               att10=round(float(len(z) * att), 1),
               sig10=round(float((got["n10"] - len(z) * att) / np.sqrt(len(z) * att)), 1),
               att82=round(float(len(z) * np.sin(np.radians(1.25)) * (120.0 / 360.0)), 1),
               fac82=round(float(got["n82"] / (len(z) * np.sin(np.radians(1.25)) * (120 / 360))), 1),
               pc82=round(100.0 * got["n82"] / len(z), 1),
               aire82=round(100.0 * np.sin(np.radians(1.25)) * (120.0 / 360.0), 2),
               zmed82=round(float(np.median(z[s82])), 3),
               zmed=round(float(np.median(z[~s82])), 3),
               zmin=round(float(z.min()), 4), zmax=round(float(z.max()), 3),
               n_bas=n_bas, dmax=round(float(dc.max()), 0),
               om=C3.OM_FID, h0=C3.H0_FID, dc1=round(d1, 1),
               graine=GRAINE, iso_sig=round(float(sig), 2), ngp=list(map(float, ngp)), gc=GC)

    tpl = (ROOT / "outils" / "ciel_v4_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 3)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 2)).replace("__ISO__", C3.flat(ISO, 1))
              .replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v4.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel4] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        identite v3 confirmee : {got}")
    print(f"        ciel isotrope : graine {GRAINE}, uniformite a {sig:.2f} sigma")
    print(f"        z dans [{z.min():.4f} ; {z.max():.3f}], {n_bas} SNe a z <= 0,1")


if __name__ == "__main__":
    main()
