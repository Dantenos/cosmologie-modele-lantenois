#!/usr/bin/env python3
"""AUDIT DES DOMAINES : QUELS « MINIMA » DE L'ATLAS SONT DES BORDS ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI. Le #173, declenche par le soupcon d'Edouard (« trop beau pour etre vrai »), a
montre que le minimum de 'ilcdm_dm' a eps = 0 etait un MINIMUM DE BORD : toute la moitie
eps < 0 renvoie le sentinelle 1e9 parce que rho_de y diverge vers -infini. Un optimiseur
qui s'arrete sur une frontiere rend une frontiere, pas un minimum — et AUCUN critere gele du
corpus ne testait cela. Cet audit generalise le controle a TOUTES les familles a un
parametre de l'atlas, y compris la notre.

METHODE. Pour chaque famille, balayage de 41 points sur les bornes DECLAREES par l'atlas
(#150), avec (h, omega_b, Om) reoptimises a chaque point. Un point est dit INACCESSIBLE si
son chi2 depasse 1e8 (les fonds rejetes renvoient 1e9). On rapporte : la fraction accessible,
la position du meilleur point, et sa distance a la premiere region inaccessible.

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  Le balayage doit retrouver, a +/- 0,3, les chi2 publies (#150) pour les familles dont
  l'atlas donne le minimum : accretion 1419,309 ; wCDM 1423,843 ; ilcdm_de 1415,245 ;
  ilcdm_dm 1415,818. Sinon le balayage ne mesure pas ce que l'atlas a mesure.

--- CRITERES (exhaustifs, exclusifs, appliques a CHAQUE famille) ---
  MINIMUM DE BORD   si le meilleur point est a DEUX pas ou moins d'un point inaccessible,
     ou s'il tombe sur la premiere/derniere valeur du balayage. Le chi2 de cette famille ne
     peut alors PAS etre lu comme un minimum, et toute significativite qui en decoule doit
     etre declaree unilaterale.
  DOMAINE MUTILE    si moins de 60 % des points declares sont accessibles, meme si le
     minimum est interieur : la borne annoncee dans l'atlas surestime alors l'espace
     reellement explore.
  MINIMUM INTERIEUR si le meilleur point est interieur ET plus de 60 % du domaine est
     accessible. C'est le seul cas ou le chi2 publie se lit sans reserve.
  Une famille peut etre a la fois MINIMUM DE BORD et DOMAINE MUTILE ; les deux sont dits.

  CONSEQUENCE (regle 8) : toute famille classee MINIMUM DE BORD dont un resultat du corpus
  depend part en MANQUEMENTS numerote. Cela vaut AUSSI pour l'accretion si elle y tombe —
  et c'est ecrit en premier dans ce cas.
Regle 3 : cet audit REDUIT la portee des chi2 publies ; il n'invalide aucune physique.
Usage : python3 scripts/audit_domaines.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

B = [0.69, 0.02236, 0.31]
STARTS = [B, [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]
SENTINELLE = 1e8
N = 41
# (nom, famille, bornes declarees dans atlas_v1.py, ancre #150 ou None)
FAMILLES = [
    ("accretion (la notre)", 'invt',     (0.5, 5.0),   1419.309),
    ("wCDM",                 'wcdm',     (-2.0, -0.2), 1423.843),
    ("iLCDM Q~rho_de",       'ilcdm_de', (-0.5, 0.5),  1415.245),
    ("iLCDM Q~rho_dm",       'ilcdm_dm', (-0.5, 0.5),  1415.818),
    ("JPS (creation)",       'jps',      (-0.5, 0.5),  None),
    ("thawing",              'thaw',     (-1.0, 0.0),  None),
    ("holographique",        'hde',      (0.4, 1.6),   None),
    ("Bondi (0 param. lib.)", 'bondi',   (0.0, 1.0),   None),
]

if __name__ == "__main__":
    print("AUDIT DES DOMAINES — quels minima sont des bords ? (criteres geles)\n")

    print("  --- validation : le balayage retrouve-t-il les chi2 publies ? ---")
    res = {}
    for nom, fam, (lo, hi), ancre in FAMILLES:
        xs = np.linspace(lo, hi, N)
        cs = np.array([A.fit(fam, 1, STARTS, fixpar=float(x)).fun for x in xs])
        res[fam] = (nom, xs, cs, lo, hi, ancre)
        if ancre is not None:
            ok = abs(cs.min() - ancre) < 0.3
            print(f"    {nom:<22s} balayage {cs.min():9.3f}  ancre {ancre:9.3f}  "
                  f"-> {'OK' if ok else 'ECHEC'}")
            if not ok:
                sys.exit("    VALIDATION ECHOUE — rien n'est publie.")
    print("    -> le balayage mesure bien ce que l'atlas a mesure\n")

    print("  --- verdicts par famille ---")
    print(f"    {'famille':<22s} {'accessible':>11s} {'arg min':>9s} {'chi2 min':>10s}  verdict")
    bords = []
    for fam, (nom, xs, cs, lo, hi, ancre) in res.items():
        acc = cs < SENTINELLE
        frac = float(acc.mean())
        i = int(np.argmin(cs))
        pas = (hi - lo) / (N - 1)
        # distance (en pas) du meilleur point a la premiere valeur inaccessible
        idx_bad = np.where(~acc)[0]
        d_bad = int(np.min(np.abs(idx_bad - i))) if idx_bad.size else N
        bord = (d_bad <= 2) or (i == 0) or (i == N - 1)
        mutile = frac < 0.60
        v = []
        if bord:
            v.append("MINIMUM DE BORD")
        if mutile:
            v.append("DOMAINE MUTILE")
        if not v:
            v.append("minimum interieur")
        if bord:
            bords.append(nom)
        print(f"    {nom:<22s} {100*frac:9.1f} % {xs[i]:9.4f} {cs[i]:10.3f}  "
              f"{' + '.join(v)}"
              + (f"  (bord a {d_bad} pas)" if bord and idx_bad.size else ""))

    print()
    if bords:
        print(f"  CONSEQUENCE : {len(bords)} famille(s) a minimum de bord -> "
              f"MANQUEMENTS numerote du.")
        for n in bords:
            print(f"     - {n}")
        if any("notre" in n for n in bords):
            print("     ATTENTION : NOTRE MODELE EN FAIT PARTIE — a ecrire en premier.")
    else:
        print("  CONSEQUENCE : aucun minimum de bord — les chi2 publies se lisent sans "
              "cette reserve.")
