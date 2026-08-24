#!/usr/bin/env python3
"""AUDIT DES DOMAINES v2 : QUELS « MINIMA » DE L'ATLAS SONT DES BORDS ?
CRITERES PRE-ENREGISTRES (geles AVANT execution de CETTE version, 24/08/2026).

POURQUOI UNE v2 (declaration, lignee #162, #165, #174). audit_domaines.py (gele 3ae3db8982de)
a REFUSE de publier sur sa propre validation : elle exigeait qu'un balayage de 41 points
retrouve le chi2 publie a +/- 0,3, ce qu'un balayage de pas 0,11 en beta ne peut pas faire
par construction — il a rendu 1419,754 contre l'ancre 1419,309. **J'avais gele deux exigences
mutuellement incompatibles** : la finesse du balayage et la tolerance sur le minimum.
Vice de MA conception, le sixieme de la journee. Valeur vue : 1419,754, qui n'apprend rien
sur la physique (c'est le pas de grille). Le taux lui-meme est un fait a consigner : six
criteres mal poses en un jour, tous arretes par le protocole avant publication.

LA CONCEPTION CORRIGEE separe deux roles qui n'auraient jamais du etre confondus :
  le BALAYAGE (41 points sur les bornes declarees) sert UNIQUEMENT a cartographier
  l'ACCESSIBILITE du domaine — quels points renvoient le sentinelle de rejet ;
  le FIT LIBRE sert a localiser le minimum. Aucun minimum n'est lu sur la grille.

METHODE. Balayage : 41 points, (h, omega_b, Om) reoptimises a chaque point ; un point est
INACCESSIBLE si son chi2 depasse 1e8 (les fonds rejetes renvoient 1e9). Fit libre : depuis
trois departs, avec les memes bornes.

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  Le FIT LIBRE (et non le balayage) doit retrouver a +/- 0,3 les chi2 publies (#150) :
  accretion 1419,309 ; wCDM 1423,843 ; ilcdm_de 1415,245 ; ilcdm_dm 1415,818.

--- CRITERES (exhaustifs, exclusifs, appliques a CHAQUE famille) ---
  MINIMUM DE BORD   si le parametre du fit libre est a DEUX PAS DE GRILLE ou moins d'un point
     inaccessible, OU a deux pas ou moins d'une borne declaree. Le chi2 de cette famille ne
     se lit alors PAS comme un minimum, et toute significativite qui en decoule est
     UNILATERALE et doit etre declaree telle.
  DOMAINE MUTILE    si moins de 60 % des 41 points sont accessibles — la borne annoncee par
     l'atlas surestime alors l'espace reellement explore, meme si le minimum est interieur.
  MINIMUM INTERIEUR sinon : le chi2 publie se lit sans cette reserve.
  Les deux premiers verdicts peuvent coexister ; on les dit tous les deux.
  CONSEQUENCE (regle 8) : toute famille MINIMUM DE BORD dont depend un resultat du corpus
  part en MANQUEMENTS numerote — Y COMPRIS la notre, et dans ce cas ecrite en premier.
Regle 3 : cet audit REDUIT la portee de chi2 publies ; il n'invalide aucune physique.
Usage : python3 scripts/audit_domaines_v2.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

B = [0.69, 0.02236, 0.31]
STARTS = [B, [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]
SENT = 1e8
N = 41
FAMILLES = [
    ("accretion (la notre)", 'invt',     (0.5, 5.0),   1419.309, [2.4, 2.0, 3.0]),
    ("wCDM",                 'wcdm',     (-2.0, -0.2), 1423.843, [-0.9, -1.1, -1.3]),
    ("iLCDM Q~rho_de",       'ilcdm_de', (-0.5, 0.5),  1415.245, [0.02, -0.02, 0.2]),
    ("iLCDM Q~rho_dm",       'ilcdm_dm', (-0.5, 0.5),  1415.818, [0.01, -0.01, 0.1]),
    ("JPS (creation)",       'jps',      (-0.5, 0.5),  None,     [0.02, -0.02, 0.2]),
    ("thawing",              'thaw',     (-1.0, 0.0),  None,     [-0.1, -0.5, -0.9]),
    ("holographique",        'hde',      (0.4, 1.6),   None,     [0.8, 1.0, 1.3]),
]

if __name__ == "__main__":
    print("AUDIT DES DOMAINES v2 — quels minima sont des bords ? (criteres geles)\n")

    print("  --- validation : le FIT LIBRE retrouve-t-il les chi2 publies ? ---")
    libres = {}
    for nom, fam, (lo, hi), ancre, deps in FAMILLES:
        r = A.fit(fam, 1, [s + [d] for s in STARTS[:1] for d in deps]
                  + [STARTS[1] + [deps[0]], STARTS[2] + [deps[0]]], bornes=[(lo, hi)])
        libres[fam] = (float(r.fun), float(r.x[3]))
        if ancre is not None:
            ok = abs(r.fun - ancre) < 0.3
            print(f"    {nom:<22s} fit libre {r.fun:9.3f}  ancre {ancre:9.3f}  "
                  f"-> {'OK' if ok else 'ECHEC'}")
            if not ok:
                sys.exit("    VALIDATION ECHOUE — rien n'est publie.")
    print("    -> le fit libre reproduit l'atlas\n")

    print("  --- cartographie de l'accessibilite (41 points) et verdicts ---")
    print(f"    {'famille':<22s} {'accessible':>11s} {'arg min':>9s} {'chi2':>10s}  verdict")
    bords = []
    for nom, fam, (lo, hi), ancre, deps in FAMILLES:
        xs = np.linspace(lo, hi, N)
        cs = np.array([A.fit(fam, 1, STARTS, fixpar=float(x)).fun for x in xs])
        acc = cs < SENT
        frac = float(acc.mean())
        cmin, pmin = libres[fam]
        pas = (hi - lo) / (N - 1)
        idx_bad = np.where(~acc)[0]
        d_bad = float(np.min(np.abs(xs[idx_bad] - pmin)) / pas) if idx_bad.size else 1e9
        d_bord = min(abs(pmin - lo), abs(pmin - hi)) / pas
        bord = (d_bad <= 2.0) or (d_bord <= 2.0)
        mutile = frac < 0.60
        v = ([] if not bord else ["MINIMUM DE BORD"]) + ([] if not mutile else ["DOMAINE MUTILE"])
        if not v:
            v = ["minimum interieur"]
        if bord:
            bords.append((nom, d_bad, d_bord))
        det = ""
        if bord:
            det = (f"  (rejet a {d_bad:.1f} pas)" if d_bad <= 2.0
                   else f"  (borne a {d_bord:.1f} pas)")
        print(f"    {nom:<22s} {100*frac:9.1f} % {pmin:9.4f} {cmin:10.3f}  "
              f"{' + '.join(v)}{det}")

    print()
    if bords:
        print(f"  CONSEQUENCE : {len(bords)} famille(s) a minimum de bord -> "
              f"MANQUEMENTS numerote du :")
        for n, a, b in bords:
            print(f"     - {n}")
        if any("notre" in n for n, _, _ in bords):
            print("     ATTENTION : NOTRE MODELE EN FAIT PARTIE — a ecrire en premier.")
        else:
            print("     Notre modele n'en fait pas partie.")
    else:
        print("  CONSEQUENCE : aucun minimum de bord parmi les familles testees.")
