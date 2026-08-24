#!/usr/bin/env python3
"""L'EPREUVE DE LRG2 — la critique 2026 la plus forte, appliquee a NOS modeles.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

LA CRITIQUE. Kim, Mota & Tamosiunas (arXiv:2607.28918) appliquent un e-process
« anytime-valid » a DESI DR2 et concluent que l'evidence pour l'energie noire evolutive
tient essentiellement A UN SEUL BIN : retirer LRG2 fait tomber leur e-value de 33,97 a 0,49.
C'est, avec la recalibration Dovekie (arXiv:2511.07517, 4,2 sigma -> 3,2 sigma) et le
traitement des SNe a bas z (arXiv:2502.04212, arXiv:2512.10585, < 2 sigma), l'attaque la
plus serieuse contre le signal dont TOUT notre corpus depend (avertissement liminaire du
papier A). Question posee ici : notre preference tient-elle au meme bin ?

CE QUI EST DEJA ACQUIS ET N'EST PAS REFAIT : le jackknife Planck complet (#160) a retire
chacun des 13 points BAO avec reoptimisation totale ; retirer LRG2 (z = 0,706, D_M) y donne
le retrait le PLUS defavorable, Dchi2 = -9,29, contre -12,60 complet. Ce script traite la
vraisemblance LEGERE, ou l'information BAO pese bien plus lourd, et y ajoute les rivaux.

METHODE. LRG2 = les deux points a z = 0,706 (D_M et D_H) des 13 BAO DR2. Retrait par
DEPONDERATION (sigma x 1e3, correlations coupees), comme au #156 : le pipeline scelle fixe
u = 13, on ne touche pas a ses formes. Refit COMPLET a chaque fois (regle 5 : chaque modele
garde tout ce qu'il a le droit de reajuster). Modeles : LCDM (reference), accretion (le
notre, 1 parametre), CPL (2 parametres, le modele de la critique), wCDM (1 parametre).

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  Les quatre chi2 SANS retrait doivent reproduire les ancres de l'atlas #150 a +/- 0,3 :
  LCDM 1425,086 ; accretion 1419,309 ; CPL 1418,927 ; wCDM 1423,843.

--- CRITERES (exhaustifs, exclusifs) ---
  1. NOTRE MODELE. g = gain de l'accretion sur LCDM apres retrait de LRG2 (complet : +5,78).
     PORTE PAR LRG2      si g < 1,0 — notre signal est le leur, ecrit EN PREMIER ;
     ROBUSTE A LRG2      si g >= 3,0 ;
     AFFAIBLI            sinon, avec le pourcentage perdu, ecrit tel quel.
  2. LA CRITIQUE SE REPRODUIT-ELLE ? Meme mesure pour CPL (gain complet +6,16).
     REPRODUITE          si le gain de CPL tombe sous 1,0 ;
     NON REPRODUITE      si CPL garde >= 3,0 ;
     PARTIELLE           sinon. Ceci teste la critique, pas nous : si elle ne se reproduit
     pas dans notre pipeline, c'est notre pipeline qui differe du leur (donnees legeres,
     pas d'e-process), et on le dit — on n'en tire AUCUN argument contre eux.
  3. COMPARAISON HONNETE : pourcentage du gain perdu par chaque modele. Si l'accretion perd
     PLUS que CPL, c'est ecrit en premier et sans adoucissement.
Regle 3 : cette etude REDUIT ; elle ne ferme rien. Regle 9 : criteres 1 et 2 contradictoires
(nous robustes ET critique reproduite a l'identique) ne s'excluent pas — ce serait meme le
resultat interessant ; aucune ambiguite a arbitrer ici.
Usage : python3 scripts/epreuve_lrg2.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import vraisemblance_reelle as V

B = [0.69, 0.02236, 0.31]
ANCRES = {"LCDM": 1425.086, "ACCRETION": 1419.309, "CPL": 1418.927, "wCDM": 1423.843}
LRG2 = [3, 4]                      # les deux points a z = 0,706 (D_M, D_H)
SAV_BAO, SAV_CI = V.BAO, V.Cinv_bao


def cov_bao(bao):
    C = np.zeros((len(bao), len(bao)))
    for i, b in enumerate(bao):
        C[i, i] = b[3] ** 2
    for i, b in enumerate(bao):
        if b[4] is not None and i + 1 < len(bao):
            C[i, i + 1] = C[i + 1, i] = b[4] * b[3] * bao[i + 1][3]
    return C


def deponderer(idx):
    C = cov_bao(SAV_BAO).copy()
    for i in idx:
        C[i, :] = 0.0
        C[:, i] = 0.0
        C[i, i] = (SAV_BAO[i][3] * 1e3) ** 2
    V.Cinv_bao = np.linalg.inv(C)


def restaurer():
    V.Cinv_bao = SAV_CI


def ajuste():
    import test_wE_v3 as T
    return {
        "LCDM":      T.fit('lcdm').fun,
        "ACCRETION": A.fit('invt', 1, [B + [2.4], B + [2.0], B + [2.8]],
                           bornes=[(0.5, 5.0)]).fun,
        "CPL":       A.fit('cpl', 2, [B + [-0.9, -0.3], B + [-0.84, -0.6], B + [-1.0, 0.0]],
                           bornes=[(-2.0, 0.0), (-3.0, 2.0)]).fun,
        "wCDM":      A.fit('wcdm', 1, [B + [-0.9], B + [-1.1], B + [-1.02]],
                           bornes=[(-2.0, -0.2)]).fun,
    }


if __name__ == "__main__":
    print("L'EPREUVE DE LRG2 (criteres geles)\n")
    print(f"  point retire : z = {SAV_BAO[LRG2[0]][0]}, types "
          f"{SAV_BAO[LRG2[0]][1]} et {SAV_BAO[LRG2[1]][1]} — LRG2 de DESI DR2\n")

    plein = ajuste()
    ok = all(abs(plein[k] - ANCRES[k]) < 0.3 for k in ANCRES)
    print("  [validation] sans retrait :")
    for k in ANCRES:
        print(f"     {k:<10s} {plein[k]:9.3f}  (ancre {ANCRES[k]})")
    if not ok:
        sys.exit("     ECHEC — rien n'est publie.")
    print("     -> OK\n")

    deponderer(LRG2)
    sans = ajuste()
    restaurer()

    print("  --- sans LRG2 (refits complets) ---")
    print(f"    {'modele':<11s} {'chi2':>10s} {'gain':>8s} {'gain plein':>11s} {'perdu':>8s}")
    perdu = {}
    for k in ["ACCRETION", "CPL", "wCDM"]:
        g = sans["LCDM"] - sans[k]
        g0 = plein["LCDM"] - plein[k]
        pc = 100 * (1 - g / g0) if g0 > 0 else float('nan')
        perdu[k] = (g, g0, pc)
        print(f"    {k:<11s} {sans[k]:10.3f} {g:+8.3f} {g0:+11.3f} {pc:7.1f} %")

    g_acc = perdu["ACCRETION"][0]
    if g_acc < 1.0:
        v1 = "PORTE PAR LRG2 — notre signal est le leur"
    elif g_acc >= 3.0:
        v1 = "ROBUSTE A LRG2"
    else:
        v1 = f"AFFAIBLI ({perdu['ACCRETION'][2]:.0f} % du gain perdu)"
    g_cpl = perdu["CPL"][0]
    if g_cpl < 1.0:
        v2 = "REPRODUITE — CPL s'effondre sans LRG2, comme le dit arXiv:2607.28918"
    elif g_cpl >= 3.0:
        v2 = "NON REPRODUITE dans notre pipeline (vraisemblance legere, pas d'e-process)"
    else:
        v2 = "PARTIELLE"
    print(f"\n  VERDICT 1 (nous)      : {v1}")
    print(f"  VERDICT 2 (critique)  : {v2}")
    da, dc = perdu["ACCRETION"][2], perdu["CPL"][2]
    if da > dc:
        print(f"  VERDICT 3 (honnete)   : l'accretion perd PLUS que CPL "
              f"({da:.0f} % contre {dc:.0f} %) — ecrit en premier.")
    else:
        print(f"  VERDICT 3 (honnete)   : l'accretion perd {da:.0f} %, CPL {dc:.0f} %.")
    print("\n  Rappel : le jackknife Planck complet (#160) donne -9,29 sans LRG2 D_M, "
          "contre -12,60 complet.")
