#!/usr/bin/env python3
"""genere_ciel_v6 — LE VERTIGE DES ECHELLES : BULLE LOCALE, KUIPER, REPERES, SCAN RADAR.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

REGLE DE L'AUTEUR, TOUJOURS RESPECTEE : ni la sphere, ni les donnees, ni les informations
existantes ne sont touchees. v3, v4 et v5 restent intactes ; ceci ecrit un fichier NOUVEAU.
Les donnees sont RE-CALCULEES par les fonctions gelees de genere_ciel_v3 et doivent redonner
EXACTEMENT les memes comptes.

CE QUE LA v6 AJOUTE, et chaque nombre affiche est calcule ici :
  - orbite terrestre et sa vitesse orbitale, DERIVEE (v = 2*pi*UA/an), non recopiee ;
  - ceinture de Kuiper (30-50 UA) et nuage de Oort (declare : 2 000 - 100 000 UA) ;
  - BULLE LOCALE. Valeur declaree et sourcee : la cavite fait ~1 000 al de large, soit un
    rayon de ~150 pc, mais elle est IRREGULIERE — la coquille est entre ~50 et ~150 pc du
    Soleil selon la direction (Zucker et al. 2022 ; cartographie 3D de la poussiere). On
    dessine donc une coquille irreguliere entre ces deux bornes, pas une sphere parfaite,
    et l'ecart est ecrit a l'ecran. Dessiner une sphere nette serait une affirmation fausse.
  - BASCULEUR DE REPERE equatorial <-> galactique, par rotation animee ;
  - SCAN RADAR a la vitesse de la lumiere, avec les TEMPS DE TRAJET calcules dans la
    fiduciaire declaree ;
  - vue observateur : halo tamise sur Sgr A*, coordonnees galactiques (l, b) au reticule,
    ligne de visee au survol, export d'image sans HUD.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE v3/v4/v5 : 1580 / 553 / 623 / 150 / 69 ; 0 SNe a |b| < 5 deg ; 6 a |b| < 10 ;
     416 dans Stripe 82.
  2. GEOMETRIE : D_C(z = 1) = 3274,9 +/- 2,0 Mpc dans la fiduciaire declaree.
  3. ANGLES : obliquite 23,44 +/- 0,05 deg ; galactique-ecliptique 60,2 +/- 0,3 deg ;
     Sgr A* a b = 0,0 +/- 0,2 deg.
  4. VITESSE ORBITALE derivee : 2*pi*UA / (1 an sideral) = 29,8 +/- 0,2 km/s. Si le calcul
     ne redonne pas la valeur connue, nos constantes sont fausses.
  5. TEMPS DE TRAJET : le temps de trajet de la lumiere jusqu'au z maximal de l'echantillon
     doit etre INFERIEUR a l'age de l'univers dans la meme fiduciaire (controle de coherence
     elementaire), et l'age doit valoir 13,3 +/- 0,3 milliards d'annees.
  6. BASCULEUR DE REPERE : la matrice equatorial -> galactique doit etre orthogonale a 1e-12
     et de determinant +1 (rotation propre, pas de reflexion).

Usage : python3 outils/genere_ciel_v6.py -> visuels/ciel_pantheon_v6.html
"""
import sys, csv, json, pathlib
import numpy as np
from scipy.integrate import quad

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
sys.path.insert(0, str(ROOT / "scripts"))
import genere_ciel_v3 as C3
import genere_ciel_v5 as C5
import etude_E1_vides as E

GRAINE = 20260824
ATTENDU = dict(n_sn=1580, n_h=553, n_v=623, n_void=150, n_frb=69, n5=0, n10=6, n82=416)
AN_SID = 3.155815e7      # seconde
UA_M = 1.495978707e11
C_MS = 2.99792458e8
GYR = 3.1557e16          # seconde
PC_M = 3.0856776e16


def tlb(z, Om=C3.OM_FID, H0=C3.H0_FID):
    """temps de trajet de la lumiere (Gyr) dans la fiduciaire DECLAREE."""
    Hs = H0 * 1000.0 / (PC_M * 1e6)
    return quad(lambda x: 1 / ((1 + x) * np.sqrt(Om * (1 + x) ** 3 + 1 - Om)), 0, z)[0] / Hs / GYR


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
        sys.exit(f"[ciel6] REFUS verif 1 : {got} != {ATTENDU}")
    d1 = float(C3.dc_fiduciel(np.array([1.0]))[0])
    if not abs(d1 - 3274.9) < 2.0:
        sys.exit(f"[ciel6] REFUS verif 2 : D_C(z=1) = {d1:.1f}")
    dc = C3.dc_fiduciel(z)

    pecl = C5.uvec(*C5.POLE_ECL)
    sgr = C5.uvec(*C5.SGR_A)
    obliq = C5.angle(np.array([0.0, 0.0, 1.0]), pecl)
    gal_ecl = C5.angle(ngp, pecl)
    sgr_b = 90.0 - C5.angle(sgr, ngp)
    if not (abs(obliq - 23.44) < 0.05 and abs(gal_ecl - 60.2) < 0.3 and abs(sgr_b) < 0.2):
        sys.exit(f"[ciel6] REFUS verif 3 : {obliq:.3f} / {gal_ecl:.3f} / {sgr_b:.3f}")

    v_orb = 2 * np.pi * UA_M / AN_SID / 1000.0
    if not abs(v_orb - 29.8) < 0.2:
        sys.exit(f"[ciel6] REFUS verif 4 : v_orb = {v_orb:.3f} km/s")

    t_max = tlb(float(z.max()))
    Hs = C3.H0_FID * 1000.0 / (PC_M * 1e6)
    age = quad(lambda a: 1 / (a * np.sqrt(C3.OM_FID / a**3 + 1 - C3.OM_FID)), 1e-8, 1)[0] / Hs / GYR
    if not (t_max < age and abs(age - 13.3) < 0.3):
        sys.exit(f"[ciel6] REFUS verif 5 : t_max = {t_max:.2f}, age = {age:.2f}")

    gp = np.array(sgr) - float(sgr @ ngp) * ngp
    gp /= np.linalg.norm(gp)
    gq = np.cross(ngp, gp)
    Q = np.stack([gp, gq, ngp])
    if not (np.max(np.abs(Q @ Q.T - np.eye(3))) < 1e-12 and abs(np.linalg.det(Q) - 1) < 1e-12):
        sys.exit(f"[ciel6] REFUS verif 6 : matrice non orthogonale ou reflexion")

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
    aire82 = (2 * 1.25 / 180.0) * (120.0 / 360.0)
    att10 = len(z) * np.sin(np.radians(10.0))
    cos15 = np.cos(np.radians(15.0))

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
               om=C3.OM_FID, h0=C3.H0_FID, dc1=round(d1, 1), graine=GRAINE,
               obliq=round(obliq, 2), gal_ecl=round(gal_ecl, 1), sgr_b=round(sgr_b, 3),
               n_sgr=int(np.sum((n @ sgr) > cos15)),
               att_sgr=round(float(len(z) * (1 - cos15) / 2.0), 1),
               v_orb=round(float(v_orb), 1), age=round(float(age), 2),
               t_max=round(float(t_max), 2), t_z01=round(float(tlb(0.1)), 2),
               t_z05=round(float(tlb(0.5)), 2), t_z1=round(float(tlb(1.0)), 2),
               t_min=round(float(tlb(float(z.min())) * 1000), 0),
               ngp=list(map(float, ngp)), gc=list(map(float, sgr)),
               pecl=list(map(float, pecl)), Q=[list(map(float, r)) for r in Q])

    tpl = (ROOT / "outils" / "ciel_v6_template.html").read_text(encoding="utf-8")
    out = (tpl.replace("__SN__", C3.flat(SN, 3)).replace("__VD__", C3.flat(VD, 1))
              .replace("__FR__", C3.flat(FR, 2)).replace("__ISO__", C3.flat(ISO, 1))
              .replace("__MES__", json.dumps(MES)))
    dest = ROOT / "visuels" / "ciel_pantheon_v6.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel6] ecrit : {dest.name} ({dest.stat().st_size // 1024} ko)")
    print(f"        identite v3/v4/v5 : {got}")
    print(f"        derives : v_orb = {v_orb:.2f} km/s | age = {age:.2f} Gyr | "
          f"t(z_max) = {t_max:.2f} Gyr")
    print(f"        matrice de repere orthogonale, det = {np.linalg.det(Q):.12f}")


if __name__ == "__main__":
    main()
