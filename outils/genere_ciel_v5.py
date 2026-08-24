#!/usr/bin/env python3
"""genere_ciel_v5 — LES TROIS ECHELLES SUBLIMEES + LE PHARE DU CENTRE GALACTIQUE (24/08/2026).
CRITERES PRE-ENREGISTRES (geles AVANT execution).

REGLE DE L'AUTEUR, TOUJOURS RESPECTEE : on ne touche NI a la sphere, NI aux donnees, NI aux
informations existantes. visuels/ciel_pantheon_v3.html et v4.html ne sont PAS modifies ;
cette v5 ecrit un fichier NOUVEAU. Les donnees sont RE-CALCULEES par les memes fonctions
gelees (genere_ciel_v3) et doivent redonner EXACTEMENT les memes comptes qu'en v3 et v4.

CE QUE LA v5 AJOUTE — de la SCENOGRAPHIE aux trois premieres echelles, et un outil :
  Etape 1, la Terre : axe de rotation incline de l'obliquite REELLE (23,439 deg entre le
    pole celeste et le pole de l'ecliptique), equateur celeste et axe des poles traces.
    C'est ce qui ancre les coordonnees (RA, Dec) sur la rotation de la planete.
  Etape 2, le Systeme solaire : disque de l'ECLIPTIQUE, perpendiculaire au pole ecliptique
    (RA 270 deg, Dec +66,561 deg), et orbites planetaires.
  Etape 3, la Voie lactee : disque spiral en particules, Soleil marque a 8,2 kpc du centre,
    et l'ANGLE ENTRE PLAN GALACTIQUE ET ECLIPTIQUE, calcule ici et affiche.
  Le PHARE Sgr A* : aligne la camera sur le vecteur Terre -> centre galactique et trace ce
    vecteur a travers toute la sphere. Il pointe au milieu du trou d'observation.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE v3/v4 : 1580 SNe, 553 hemisphere du dipole, 623 avec vide sur la visee,
     150 vides, 69 FRB, 0 SNe a |b| < 5 deg, 6 a |b| < 10 deg, 416 dans Stripe 82.
  2. GEOMETRIE : D_C(z = 1) = 3274,9 +/- 2,0 Mpc dans la fiduciaire declaree.
  3. ANGLES, calcules ici et non affirmes :
     a. obliquite = angle(pole celeste, pole ecliptique) = 23,44 +/- 0,05 deg ;
     b. angle(plan galactique, plan ecliptique) = 60,2 +/- 0,3 deg — c'est le basculement
        de repere qui explique que la zone d'evitement traverse le ciel en biais ;
     c. angle(direction Sgr A*, plan galactique) = 0,0 +/- 0,2 deg (par construction :
        le centre galactique est a b = 0 ; si ce controle echoue, nos vecteurs sont faux).
  4. LE PHARE EST-IL LEGITIME ? Le nombre de SNe a moins de 15 deg de la direction Sgr A*
     doit etre STRICTEMENT INFERIEUR a 5 % de l'attente isotrope pour ce cone. Sinon la
     phrase « il n'y a rien dans cette direction » serait fausse et le mode n'est pas ecrit.

NOTE DE PRUDENCE PORTEE A L'ECRAN (et non dans le code) : l'absence de supernovae vers le
centre galactique tient a DEUX causes qu'il ne faut pas confondre — l'extinction par la
poussiere, et le fait que les releves EVITENT deliberement le plan. Ecrire « la matiere
bloque 100 % de la lumiere » serait faux : c'est extinction + strategie d'observation.

Usage : python3 outils/genere_ciel_v5.py -> visuels/ciel_pantheon_v5.html
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
POLE_ECL = (270.0, 66.56071)      # pole nord de l'ecliptique, J2000
SGR_A = (266.405, -28.936)        # Sgr A*, J2000


def uvec(ra_deg, dec_deg):
    ra, de = np.radians(ra_deg), np.radians(dec_deg)
    return np.array([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)])


def angle(u, v):
    return float(np.degrees(np.arccos(np.clip(abs(float(u @ v)), -1, 1))))


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
    ngp = uvec(C3.RA_NGP, C3.DEC_NGP)
    b = np.degrees(np.arcsin(np.clip(n @ ngp, -1, 1)))
    dec = np.degrees(np.arcsin(np.clip(n[:, 2], -1, 1)))
    ra = np.degrees(np.arctan2(n[:, 1], n[:, 0])) % 360
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))
    got = dict(n_sn=len(z), n_h=int(hemi.sum()), n_v=int(vide.sum()), n_void=len(R),
               n_frb=len(rows), n5=int(np.sum(np.abs(b) < 5)),
               n10=int(np.sum(np.abs(b) < 10)), n82=int(s82.sum()))
    if got != ATTENDU:
        sys.exit(f"[ciel5] REFUS verif 1 : {got} != {ATTENDU}")

    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3274.9) < 2.0:
        sys.exit(f"[ciel5] REFUS verif 2 : D_C(z=1) = {d1:.1f}")
    dc = C3.dc_fiduciel(z)

    pole_cel = np.array([0.0, 0.0, 1.0])
    pole_ecl = uvec(*POLE_ECL)
    sgr = uvec(*SGR_A)
    obliq = angle(pole_cel, pole_ecl)
    gal_ecl = angle(ngp, pole_ecl)
    sgr_b = 90.0 - angle(sgr, ngp)
    if not abs(obliq - 23.44) < 0.05:
        sys.exit(f"[ciel5] REFUS verif 3a : obliquite = {obliq:.3f} deg")
    if not abs(gal_ecl - 60.2) < 0.3:
        sys.exit(f"[ciel5] REFUS verif 3b : galactique/ecliptique = {gal_ecl:.3f} deg")
    if not abs(sgr_b) < 0.2:
        sys.exit(f"[ciel5] REFUS verif 3c : Sgr A* a b = {sgr_b:.3f} deg")

    cos15 = np.cos(np.radians(15.0))
    n_sgr = int(np.sum((n @ sgr) > cos15))
    att_sgr = len(z) * (1 - cos15) / 2.0
    if not n_sgr < 0.05 * att_sgr:
        sys.exit(f"[ciel5] REFUS verif 4 : {n_sgr} SNe a moins de 15 deg de Sgr A* "
                 f"pour {att_sgr:.1f} attendues — le phare ne serait pas honnete")

    rng = np.random.default_rng(GRAINE)
    u = rng.normal(size=(len(z), 3))
    iso = u / np.linalg.norm(u, axis=1)[:, None]

    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fra = np.radians([float(r["ra"]) for r in rows])
    frd = np.radians([float(r["dec"]) for r in rows])
    fu = np.stack([np.cos(frd) * np.cos(fra), np.cos(frd) * np.sin(fra), np.sin(frd)], 1)
    z_frb = np.clip(dm / 900.0, 0.02, 1.2)
    d_frb = np.clip(C3.dc_fiduciel(z_frb), 500.0, 4000.0)

    SN = np.column_stack([n * dc[:, None], hemi * 4 + vide * 2 + s82, z, b]).ravel()
    VD = np.column_stack([centres, R]).ravel()
    FR = np.column_stack([fu * d_frb[:, None], np.clip(dm / dm.max(), 0.1, 1),
                          z_frb, dm]).ravel()
    ISO = (iso * float(np.median(dc))).ravel()

    aire82 = np.sin(np.radians(1.25)) * (120.0 / 360.0)
    att10 = len(z) * np.sin(np.radians(10.0))
    MES = dict(**got, att5=round(float(len(z) * np.sin(np.radians(5.0))), 1),
               att10=round(float(att10), 1),
               sig10=round(float((got["n10"] - att10) / np.sqrt(att10)), 1),
               att82=round(float(len(z) * aire82), 1),
               fac82=round(float(got["n82"] / (len(z) * aire82)), 1),
               pc82=round(100.0 * got["n82"] / len(z), 1),
               aire82=round(100.0 * aire82, 2),
               zmed82=round(float(np.median(z[s82])), 3),
               zmed=round(float(np.median(z[~s82])), 3),
               zmin=round(float(z.min()), 4), zmax=round(float(z.max()), 3),
               n_bas=int(np.sum(z <= 0.1)), dmax=round(float(dc.max()), 0),
               om=C3.OM_FID, h0=C3.H0_FID, dc1=round(d1, 1), graine=GRAINE,
               obliq=round(obliq, 2), gal_ecl=round(gal_ecl, 1), sgr_b=round(sgr_b, 3),
               n_sgr=n_sgr, att_sgr=round(float(att_sgr), 1),
               ngp=list(map(float, ngp)), gc=list(map(float, sgr)),
               pecl=list(map(float, pole_ecl)))

    tpl = (ROOT / "outils" / "ciel_v5_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 3)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 2)).replace("__ISO__", C3.flat(ISO, 1))
              .replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v5.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel5] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        identite v3/v4 : {got}")
    print(f"        angles mesures : obliquite {obliq:.2f} deg | galactique-ecliptique "
          f"{gal_ecl:.1f} deg | Sgr A* a b = {sgr_b:.3f} deg")
    print(f"        phare : {n_sgr} SNe a moins de 15 deg de Sgr A* pour {att_sgr:.1f} "
          f"attendues si isotrope")


if __name__ == "__main__":
    main()
