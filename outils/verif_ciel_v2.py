#!/usr/bin/env python3
"""GARDE-FOU DES ARTEFACTS DU CIEL, v2 — AVEC LA DEFINITION DU CORPUS, ET APRES LE #194.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI UNE v2, ET CE QU'ELLE CORRIGE DE LA v1.
La v1 (gelee e3708ce14cd8) a trouve le defaut du #194 -- la fraction de ciel de Stripe 82
etait calculee avec une formule PLATE, Ddec/180, la ou l'angle solide vaut
(sin dec_max - sin dec_min)/2 : un facteur pi/2 exactement. Ce constat tient, et il a ete
verifie separement avec la selection du corpus.
MAIS la v1 portait un defaut a elle, dans son propre docstring gele : elle declarait
Stripe 82 comme -50 < RA < 60 et |dec| < 1,26, alors que le corpus emploie partout
(RA > 300 OU RA < 60) et |dec| < 1,25. Dix degres de RA d'ecart, d'ou 412 SNe comptees au
lieu de 416. Un critere gele ne se reecrit pas : la v1 reste au registre telle quelle, et
cette v2 la remplace en service. C'est le meme geste que pour le #188 -- la trace demeure,
l'outil change.

DEFINITIONS DECLAREES (celles du corpus, verifiees dans genere_ciel_v3 a v8b)
  - Echantillon : z > 0,01 et hors calibrateurs, comme vraisemblance_reelle.
  - Stripe 82 : |DEC| < 1,25 deg ET (RA > 300 deg OU RA < 60 deg) -- 120 deg de large.
  - Fraction de ciel : (largeur_RA/360) x (sin dec_max - sin dec_min)/2. C'EST LA FORMULE
    CORRIGEE ; la v1 des generateurs employait (2 x dec_max / 180) x (largeur_RA/360).
  - Coordonnees galactiques : rotation J2000, pole nord (192,85948 ; 27,12825) deg.
  - Cellules : 648 cellules d'aire egale (18 bandes en sin(dec) x 36 en RA).

--- CRITERES (exhaustifs) ---
  1. RECALCUL. Chaque fait affiche est recalcule depuis pantheon.dat. Ecart superieur a la
     tolerance = ECHEC BLOQUANT. Les valeurs attendues sont celles d'APRES le #194 :
     416 SNe, 0,727 % du ciel, facteur 36,2, attente isotrope 11,5 SNe dans la bande.
  2. AUCUN ARTEFACT NE DOIT PLUS PORTER L'ANCIENNE VALEUR. On cherche dans visuels/*.html
     les motifs de l'ancien calcul ("aire82": 0.46 et "fac82": 56.9) par expression
     reguliere. Une seule occurrence est un ECHEC BLOQUANT -- c'est le controle qui verifie
     que la correction a bien atteint TOUTES les sorties, y compris les versions bilingues,
     qui etaient restees en arriere au premier passage.
  3. LA VALEUR CORRIGEE DOIT ETRE PRESENTE. Chaque artefact du ciel portant un champ fac82
     doit porter 36.2. Absence = ECHEC BLOQUANT.
  4. MARQUEURS. Aucun fichier de visuels/ ne contient de marqueur non substitue, detecte
     GENERIQUEMENT par /__[A-Z_]+__/ -- jamais par une liste ecrite a la main, c'est cette
     liste qui avait laisse passer l'echec total de la v8.
  5. CONTAMINATION DE GABARIT. Inversement, chaque gabarit de outils/ DOIT contenir ses
     marqueurs : un gabarit sans marqueur signifie qu'une sortie l'a ecrase.
  6. PURETE DES VERSIONS DE LANGUE. ciel_pantheon_v7_en.html ne doit contenir aucune lettre
     accentuee francaise ; ciel_pantheon_v7_fr.html ne doit contenir aucun des mots anglais
     temoins declares. Recherche restreinte au texte visible et aux chaines JS, pour ne pas
     compter les identifiants de code.

REGLE 6. Cet outil verifie MON travail apres que j'ai corrige MON erreur. Le critere 2 est
donc ecrit pour echouer si la correction est incomplete, et non pour confirmer qu'elle est
faite. Aucune tolerance n'est elargie apres coup.
Usage : python3 outils/verif_ciel_v2.py   (depuis la racine)
"""
import sys
import pathlib
import re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAT = ROOT / "donnees" / "pantheon_plus" / "pantheon.dat"
VIS, GAB = ROOT / "visuels", ROOT / "outils"
RA_NGP, DEC_NGP, L_NCP = 192.85948, 27.12825, 122.93192
MOTS_EN = [r"\bthe sky\b", r"\bexpected\b", r"\bShadow cones\b", r"\bvoid\b",
           r"\bsight\b", r"\brender failure\b"]
ECHECS, PASSES = [], 0


def ck(nom, calc, att, tol, rel=True):
    global PASSES
    e = abs(calc - att)/abs(att) if (rel and att != 0) else abs(calc - att)
    if e > tol:
        ECHECS.append(f"[1] {nom} : recalcul {calc:.6g} != attendu {att:.6g} "
                      f"(ecart {e:.3g} > {tol:g})")
    else:
        PASSES += 1


def _js_chaines(m):
    """dans un bloc <script>, ne garde que les litteraux de chaine d'au moins 4 signes."""
    return " ".join(x or y for x, y in
                    re.findall(r'"([^"\\]{4,})"|\'([^\'\\]{4,})\'', m.group(0)))


def zone_texte(h):
    """texte visible + chaines JS, sans les identifiants de code ni les tableaux."""
    h = re.sub(r"<script[^>]*>.*?</script>", _js_chaines, h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"[-+0-9.,eE\[\]]{8,}", " ", h)


if __name__ == "__main__":
    print("GARDE-FOU DES ARTEFACTS DU CIEL v2 (criteres geles)\n")
    raw = np.genfromtxt(DAT, names=True, dtype=None, encoding="utf-8")
    m = (raw['zHD'] > 0.01) & (raw['IS_CALIBRATOR'] == 0)
    ra, dec = raw['RA'][m], raw['DEC'][m]
    N = int(m.sum())

    print("  --- critere 1 : recalcul avec la definition DU CORPUS ---")
    ck("effectif", N, 1580, 0, rel=False)
    s82 = (np.abs(dec) < 1.25) & ((ra > 300) | (ra < 60))
    n82 = int(s82.sum())
    aire = (120.0/360.0)*np.sin(np.radians(1.25))
    fac = (n82/N)/aire
    print(f"     Stripe 82 : {n82} SNe ({100*n82/N:.1f} %) sur {100*aire:.3f} % du ciel "
          f"-> x{fac:.1f}   (attente isotrope {N*aire:.1f} SNe)")
    ck("SNe dans Stripe 82", n82, 416, 0, rel=False)
    ck("fraction de ciel (%)", 100*aire, 0.727, 0.005)
    ck("facteur de concentration", fac, 36.2, 0.005)
    ck("attente isotrope dans la bande", N*aire, 11.5, 0.01)
    # l'ancienne formule, pour memoire : le facteur pi/2 exactement
    ck("rapport ancienne/nouvelle formule d'aire",
       aire/((2*1.25/180.0)*(120.0/360.0)), np.pi/2, 1e-3)

    rp, dp = np.radians(RA_NGP), np.radians(DEC_NGP)
    r, d = np.radians(ra), np.radians(dec)
    b = np.degrees(np.arcsin(np.clip(
        np.sin(dp)*np.sin(d) + np.cos(dp)*np.cos(d)*np.cos(r - rp), -1, 1)))
    ck("SNe a |b| < 5 deg", int((np.abs(b) < 5).sum()), 0, 0, rel=False)
    ck("attente isotrope a |b| < 5", N*np.sin(np.radians(5.0)), 138.0, 0.01)
    i_s = np.clip(((np.sin(np.radians(dec)) + 1)/2*18).astype(int), 0, 17)
    i_r = np.clip((ra/360.0*36).astype(int), 0, 35)
    vides = 648 - len(set(zip(i_s.tolist(), i_r.tolist())))
    ck("cellules vides", vides, 367, 0, rel=False)

    print("\n  --- critere 2 : l'ancienne valeur a-t-elle disparu de TOUTES les sorties ? ---")
    restes = []
    for p in sorted(VIS.glob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'"aire82"\s*:\s*0\.46|"fac82"\s*:\s*56\.9', t):
            restes.append(p.name)
    if restes:
        for x in restes:
            ECHECS.append(f"[2] ancienne valeur encore presente : {x}")
    else:
        PASSES += 1
        print("     aucune sortie ne porte plus 0,46 % ni x56,9 -> OK")

    print("\n  --- critere 3 : la valeur corrigee est-elle presente ? ---")
    n_ok = 0
    for p in sorted(VIS.glob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        if '"fac82"' in t:
            if re.search(r'"fac82"\s*:\s*36\.2', t):
                n_ok += 1
            else:
                ECHECS.append(f"[3] fac82 present mais != 36,2 dans {p.name}")
    PASSES += 1
    print(f"     {n_ok} artefact(s) portent fac82 = 36,2 -> OK")

    print("\n  --- criteres 4 et 5 : marqueurs ---")
    sales = [f"{p.name} : {sorted(set(re.findall(r'__[A-Z_]+__', p.read_text(encoding='utf-8', errors='ignore'))))}"
             for p in sorted(VIS.glob("*.html"))
             if re.search(r"__[A-Z_]+__", p.read_text(encoding="utf-8", errors="ignore"))]
    for s in sales:
        ECHECS.append(f"[4] marqueur non substitue -> {s}")
    if not sales:
        PASSES += 1
        print("     aucune sortie ne porte de marqueur -> OK")
    vg = [p.name for p in list(GAB.glob("*template*.html")) + list(GAB.glob("ciel_v*_base.html"))
          if not re.search(r"__[A-Z_]+__", p.read_text(encoding="utf-8", errors="ignore"))]
    for g in vg:
        ECHECS.append(f"[5] gabarit sans marqueur : {g}")
    if not vg:
        PASSES += 1
        print("     tous les gabarits ont garde leurs marqueurs -> OK")

    print("\n  --- critere 6 : purete des versions de langue ---")
    en_f = VIS / "ciel_pantheon_v7_en.html"
    fr_f = VIS / "ciel_pantheon_v7_fr.html"
    if en_f.exists():
        acc = re.findall(r"[\u00e0\u00e2\u00e7\u00e8\u00e9\u00ea\u00eb\u00ee\u00ef\u00f4\u00f9\u00fb\u0153]",
                         zone_texte(en_f.read_text(encoding="utf-8")))
        if acc:
            ECHECS.append(f"[6] {len(acc)} lettre(s) accentuee(s) dans la version EN : "
                          f"{sorted(set(acc))}")
        else:
            PASSES += 1
            print("     version EN : aucune lettre accentuee -> OK")
    else:
        ECHECS.append("[6] ciel_pantheon_v7_en.html absent")
    if fr_f.exists():
        z = zone_texte(fr_f.read_text(encoding="utf-8"))
        tr = [w for w in MOTS_EN if re.search(w, z, re.I)]
        if tr:
            ECHECS.append(f"[6] mots anglais dans la version FR : {tr}")
        else:
            PASSES += 1
            print("     version FR : aucun mot temoin anglais -> OK")
    else:
        ECHECS.append("[6] ciel_pantheon_v7_fr.html absent")

    print(f"\n  --- BILAN ---\n     {PASSES} verification(s) passee(s)")
    if ECHECS:
        print(f"\n     {len(ECHECS)} ECHEC(S) BLOQUANT(S) :")
        for e in ECHECS:
            print(f"       - {e}")
        sys.exit(1)
    print("     aucun echec bloquant.")
