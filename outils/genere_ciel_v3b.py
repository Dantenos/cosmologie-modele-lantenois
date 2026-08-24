#!/usr/bin/env python3
"""genere_ciel_v3b — LE CONE D'OBSERVATION ET LE DEZOOM COSMIQUE, CONTROLE CORRIGE.
CRITERES PRE-ENREGISTRES (geles AVANT execution de CETTE version, 24/08/2026).

POURQUOI UNE v3b (declaration d'honnetete, lignee #162, #165). genere_ciel_v3.py
(gele 71474adaf64d) a REFUSE D'ECRIRE sur sa propre verification 4 : elle exigeait
D_C(z = 1) = 3395 +/- 15 Mpc dans la fiduciaire DECLAREE LCDM plat Om = 0,315, H0 = 70.
Ce nombre est FAUX : 3401 Mpc est la valeur a H0 = 67,4 (Planck), pas a H0 = 70. J'avais
inscrit dans le critere une constante prise a un autre H0 que celui que je declarais.
Vice de MA conception, le cinquieme de la journee (#148, #158, #162, #165, celui-ci).
Le CODE, lui, etait juste : il a rendu 3274,9 Mpc. Valeurs vues avant d'ecrire cette v3b :
3274,9 (par le script) puis 3274,93 par deux methodes independantes (quadrature adaptative
scipy, et trapeze sur 200 001 points). Aucune de ces valeurs ne porte sur la physique
etudiee : c'est une constante de dessin.

VERIFICATION 4 CORRIGEE : dans la fiduciaire declaree (LCDM plat, Om = 0,315, H0 = 70),
D_C(z = 1) doit valoir 3274,9 +/- 2,0 Mpc. Tolerance resserree de 15 a 2 Mpc parce que la
valeur est desormais connue et verifiee : un controle doit etre serre quand il le peut.

TOUT LE RESTE est REPRIS SANS CHANGEMENT de genere_ciel_v3.py, dont les fonctions sont
importees telles quelles (non modifiees) : verifications 1 (comptes 1580/553/623/150/69),
2 (zone d'evitement mesuree : moins de 10 % de l'attente isotrope a |b| < 10 deg),
3 (pinceau Stripe 82 : plus de dix fois l'attente isotrope), 5 (FRB en ordre de grandeur
declare), et la doctrine : une facade n'affirme que ce qu'elle mesure ici meme, et les
nombres affiches a l'ecran sont ceux calcules par ce script, jamais des constantes ecrites
a la main.

Usage : python3 outils/genere_ciel_v3b.py -> visuels/ciel_pantheon_v3.html
"""
import sys, csv, json, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
sys.path.insert(0, str(ROOT / "scripts"))
import genere_ciel_v3 as C3
import etude_E1_vides as E

DC1_ATTENDU, DC1_TOL = 3274.9, 2.0


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
    n_sn, n_h, n_v = len(z), int(hemi.sum()), int(vide.sum())
    if not (n_sn == 1580 and n_h == 553 and n_v == 623 and len(R) == 150 and len(rows) == 69):
        sys.exit(f"[ciel3b] REFUS verif 1 : {n_sn}/{n_h}/{n_v}/{len(R)}/{len(rows)}")

    ap, dp = np.radians(C3.RA_NGP), np.radians(C3.DEC_NGP)
    zg = np.array([np.cos(dp) * np.cos(ap), np.cos(dp) * np.sin(ap), np.sin(dp)])
    b = np.degrees(np.arcsin(np.clip(n @ zg, -1, 1)))
    n10, att10 = int(np.sum(np.abs(b) < 10)), n_sn * np.sin(np.radians(10.0))
    if not n10 < 0.10 * att10:
        sys.exit(f"[ciel3b] REFUS verif 2 : {n10} pour {att10:.0f} attendues")
    n5, att5 = int(np.sum(np.abs(b) < 5)), n_sn * np.sin(np.radians(5.0))

    dec = np.degrees(np.arcsin(np.clip(n[:, 2], -1, 1)))
    ra = np.degrees(np.arctan2(n[:, 1], n[:, 0])) % 360
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))
    aire = np.sin(np.radians(1.25)) * (120.0 / 360.0)
    att82 = n_sn * aire
    if not int(s82.sum()) > 10 * att82:
        sys.exit(f"[ciel3b] REFUS verif 3 : {int(s82.sum())} pour {att82:.1f}")

    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - DC1_ATTENDU) < DC1_TOL:
        sys.exit(f"[ciel3b] REFUS verif 4 : D_C(z=1) = {d1:.1f} "
                 f"(attendu {DC1_ATTENDU} +/- {DC1_TOL})")
    dc = C3.dc_fiduciel(z)

    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    d_frb = np.clip(C3.dc_fiduciel(np.clip(dm / 900.0, 0.02, 1.2)), 500.0, 4000.0)

    SN = np.column_stack([n * dc[:, None], hemi * 4 + vide * 2 + s82]).ravel()
    VD = np.column_stack([centres, R]).ravel()
    FR = np.column_stack([fu * d_frb[:, None], np.clip(dm / dm.max(), 0.1, 1)]).ravel()
    MES = dict(n_sn=n_sn, n_h=n_h, n_v=n_v, n_void=len(R), n_frb=len(rows),
               n5=n5, att5=round(float(att5), 1), n10=n10, att10=round(float(att10), 1),
               sig10=round(float((n10 - att10) / np.sqrt(att10)), 1),
               n82=int(s82.sum()), att82=round(float(att82), 1),
               fac82=round(float(s82.sum() / att82), 1),
               pc82=round(100.0 * float(s82.sum()) / n_sn, 1),
               aire82=round(100.0 * aire, 2),
               zmed82=round(float(np.median(z[s82])), 3),
               zmed=round(float(np.median(z[~s82])), 3),
               dmax=round(float(dc.max()), 0),
               om=C3.OM_FID, h0=C3.H0_FID, dc1=round(d1, 1))

    tpl = (ROOT / "outils" / "ciel_v3_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 1)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 1)).replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v3.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel3b] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko) ; "
          f"D_C(z=1) = {d1:.1f} Mpc")
    print(f"         evitement : {n5} SNe a |b|<5 deg pour {att5:.0f} attendues ; "
          f"{n10} a |b|<10 pour {att10:.0f} ({MES['sig10']:+.1f} sigma)")
    print(f"         Stripe 82 : {MES['n82']} SNe ({MES['pc82']} %) sur {MES['aire82']} % du "
          f"ciel = x{MES['fac82']} ; z median {MES['zmed82']} contre {MES['zmed']}")


if __name__ == "__main__":
    main()
