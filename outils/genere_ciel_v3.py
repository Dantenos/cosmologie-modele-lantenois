#!/usr/bin/env python3
"""genere_ciel_v3 — LE CONE D'OBSERVATION ET LE DEZOOM COSMIQUE (24/08/2026).
CRITERES PRE-ENREGISTRES (geles AVANT execution). Le HTML n'est ECRIT que si TOUTES les
verifications passent ; sinon REFUS et aucun fichier n'est emis. Zero dependance reseau.

CE QUE CETTE FIGURE A LE DROIT DE MONTRER. Une facade n'affirme que ce qui est mesure ici
meme. Les deux structures dessinees — la zone d'evitement galactique et le pinceau SDSS
Stripe 82 — ne sont PAS des decors : elles sont mesurees sur l'echantillon avant d'etre
tracees, et les nombres affiches a l'ecran sont ceux calcules ci-dessous, jamais des
constantes ecrites a la main.

  VERIF 1 (comptes, comme genere_ciel v1) : 1580 SNe, dont 553 dans l'hemisphere du dipole
    (#116/#141) et 623 avec un vide de Stopyra sur la ligne de visee (#141) ; 150 vides ;
    69 FRB (Connor 2025, #148). Tout ecart -> REFUS.
  VERIF 2 (zone d'evitement) : la latitude galactique est calculee depuis (RA, Dec) J2000
    par le pole nord galactique (RA 192,85948 ; Dec +27,12825). Le nombre de SNe a
    |b| < 10 deg doit etre INFERIEUR A 10 % de l'attente isotrope N sin(10 deg). Si ce
    n'est pas le cas, la zone d'evitement N'EST PAS DESSINEE (elle ne serait pas un fait).
  VERIF 3 (pinceau Stripe 82) : le nombre de SNe dans |Dec| < 1,25 deg et RA hors
    [60 ; 300] deg doit depasser DIX FOIS l'attente isotrope pour la meme aire. Sinon le
    pinceau n'est pas dessine.
  VERIF 4 (geometrie declaree) : les distances comobiles sont calculees dans une cosmologie
    FIDUCIELLE DECLAREE — LCDM plat, Omega_m = 0,315, H0 = 70 — et NON dans le modele
    etudie : la geometrie du dessin ne doit pas dependre de la these defendue. Le controle
    est que la distance comobile a z = 1 vaut 3395 +/- 15 Mpc dans cette fiduciaire.
  VERIF 5 (FRB) : les FRB n'ont pas de distance mesuree ici ; leur rayon est un ORDRE issu
    de DM_exgal via une relation de Macquart grossiere, DECLARE comme tel a l'ecran et
    borne a [500 ; 4000] Mpc. Aucune conclusion n'en depend.

CE QUE LA FIGURE MONTRE, et pourquoi c'est le sujet et non l'illustration : Pantheon+ n'est
pas un echantillon isotrope. C'est un ciel troue au plan galactique et perce de pinceaux
profonds. Le plus dense de ces pinceaux est la bande SDSS Stripe 82 — precisement la region
que la tension T8 du greffe accuse de porter un differentiel d'etalonnage de -49 +/- 17 mmag
(#157). Le dezoom (Terre -> Systeme solaire -> Voie lactee -> sphere cosmologique) sert a
rendre visible d'ou vient cette geometrie : elle est imposee par l'endroit d'ou l'on regarde.

Usage : python3 outils/genere_ciel_v3.py -> visuels/ciel_pantheon_v3.html
"""
import sys, csv, json, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E

C_KM = 299792.458
OM_FID, H0_FID = 0.315, 70.0
RA_NGP, DEC_NGP = 192.85948, 27.12825


def dc_fiduciel(z):
    """distance comobile LCDM plat fiduciel (Mpc) — geometrie du DESSIN, pas du modele."""
    zg = np.linspace(0, max(3.0, float(np.max(z)) * 1.05), 4000)
    Ez = np.sqrt(OM_FID * (1 + zg) ** 3 + (1 - OM_FID))
    integ = 1.0 / Ez
    I = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(zg))])
    return np.interp(z, zg, (C_KM / H0_FID) * I)


def flat(a, nd=2):
    return "[" + ",".join(f"{v:.{nd}f}".rstrip("0").rstrip(".") or "0" for v in a) + "]"


def main():
    n = E.n_hat
    z = E.z_sn
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
        sys.exit(f"[ciel3] REFUS verif 1 : {n_sn}/{n_h}/{n_v}/{len(R)}/{len(rows)}")

    # --- verif 2 : la zone d'evitement, mesuree
    ap, dp = np.radians(RA_NGP), np.radians(DEC_NGP)
    zg = np.array([np.cos(dp) * np.cos(ap), np.cos(dp) * np.sin(ap), np.sin(dp)])
    b = np.degrees(np.arcsin(np.clip(n @ zg, -1, 1)))
    n10 = int(np.sum(np.abs(b) < 10))
    att10 = n_sn * np.sin(np.radians(10.0))
    if not n10 < 0.10 * att10:
        sys.exit(f"[ciel3] REFUS verif 2 : {n10} SNe a |b|<10 deg pour {att10:.0f} attendues")
    n5 = int(np.sum(np.abs(b) < 5))
    att5 = n_sn * np.sin(np.radians(5.0))

    # --- verif 3 : le pinceau Stripe 82, mesure
    dec = np.degrees(np.arcsin(np.clip(n[:, 2], -1, 1)))
    ra = np.degrees(np.arctan2(n[:, 1], n[:, 0])) % 360
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))
    aire = (2 * 1.25 / 180.0) * (120.0 / 360.0)
    att82 = n_sn * aire
    if not int(s82.sum()) > 10 * att82:
        sys.exit(f"[ciel3] REFUS verif 3 : {int(s82.sum())} dans la bande pour {att82:.1f}")

    # --- verif 4 : geometrie fiducielle declaree
    d1 = float(dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3395.0) < 15.0:
        sys.exit(f"[ciel3] REFUS verif 4 : D_C(z=1) = {d1:.1f} Mpc (attendu 3395 +/- 15)")
    dc = dc_fiduciel(z)

    # --- verif 5 : FRB, ordre de grandeur declare
    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    z_frb = np.clip(dm / 900.0, 0.02, 1.2)          # Macquart grossier, declare a l'ecran
    d_frb = np.clip(dc_fiduciel(z_frb), 500.0, 4000.0)

    dist_v = np.linalg.norm(centres, axis=1)
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
               dmax=round(float(dc.max()), 0), dvmax=round(float(dist_v.max()), 0),
               om=OM_FID, h0=H0_FID, dc1=round(d1, 0))

    tpl = (ROOT / "outils" / "ciel_v3_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", flat(SN, 1)).replace("__VD__", flat(VD, 1))
              .replace("__FR__", flat(FR, 1)).replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v3.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel3] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        evitement : {n5} SNe a |b|<5 deg pour {att5:.0f} attendues ; "
          f"{n10} a |b|<10 pour {att10:.0f} ({MES['sig10']:+.1f} sigma)")
    print(f"        Stripe 82 : {MES['n82']} SNe ({MES['pc82']} %) sur {MES['aire82']} % du "
          f"ciel = x{MES['fac82']} ; z median {MES['zmed82']} contre {MES['zmed']}")


if __name__ == "__main__":
    main()
