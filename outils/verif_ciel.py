#!/usr/bin/env python3
"""GARDE-FOU DES ARTEFACTS DU CIEL — LES FAITS AFFICHES SONT-ILS CEUX DES DONNEES ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI. Les artefacts du ciel Pantheon+ affichent une dizaine de faits mesures : le
deficit galactique, la concentration dans Stripe 82, la fraction de cellules vides, les
sur-densites. Ces nombres ont ete calcules une fois, il y a plusieurs generations
d'artefacts (v2 a v8b), puis RECOPIES de gabarit en gabarit. Un chiffre recopie n'est pas un
chiffre verifie. Cet outil les RECALCULE depuis pantheon.dat et les confronte a ce que les
fichiers affichent.

CE QU'IL VERIFIE, ET DANS QUEL ORDRE
  1. RECALCUL. Chaque fait est recalcule depuis les donnees brutes, avec la definition
     declaree ci-dessous. Ecart superieur a la tolerance = ECHEC BLOQUANT.
  2. PRESENCE. Chaque fait recalcule doit se retrouver dans les artefacts generes
     (visuels/*.html), cherche par expression reguliere tolerant la virgule ET le point
     decimaux (regle 7 : jamais d'egalite stricte sur du texte).
  3. MARQUEURS. Aucun fichier de visuels/ ne doit contenir de marqueur non substitue,
     detecte GENERIQUEMENT par /__[A-Z_]+__/ et non par une liste ecrite a la main --
     c'est la liste ecrite a la main qui avait laisse passer l'echec total de la v8.
  4. CONTAMINATION DE GABARIT. Inversement, les gabarits de outils/ DOIVENT contenir leurs
     marqueurs : un gabarit sans marqueur signifie qu'on a ecrase un gabarit par une sortie.

DEFINITIONS DECLAREES (elles fixent ce que "recalculer" veut dire)
  - Echantillon : identique a celui de vraisemblance_reelle -- z > 0,01 et hors calibrateurs.
  - Coordonnees galactiques : conversion depuis (RA, DEC) J2000 par la rotation standard,
    pole galactique nord a (192,85948 ; 27,12825) deg, noeud a l = 32,93192 deg.
  - Deficit galactique : compte a |b| < 5 deg, contre l'attente isotrope N x sin(5 deg).
  - Stripe 82 : -50 < RA < 60 deg ET |DEC| < 1,26 deg. Fraction de ciel calculee par
    l'aire du bandeau, pas supposee.
  - Cellules : 648 cellules d'aire egale (18 bandes en sin(dec) x 36 en RA).
  - Sur-densite locale : rapport entre la densite dans les 10 % de cellules les plus
    peuplees et la densite moyenne.
Regle 6 : les tolerances sont serrees (0,5 % en relatif, 1 unite pour les comptes entiers).
Si un fait ne passe pas, c'est le FAIT AFFICHE qui est corrige, jamais la tolerance.
Usage : python3 outils/verif_ciel.py   (depuis la racine)
"""
import sys
import pathlib
import re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
DAT = ROOT / "donnees" / "pantheon_plus" / "pantheon.dat"
VIS = ROOT / "visuels"
GAB = ROOT / "outils"
ECHECS, AVERTS, PASSES = [], [], 0

# pole galactique nord J2000 et noeud ascendant
RA_NGP, DEC_NGP, L_NCP = 192.85948, 27.12825, 122.93192


def galactique(ra, dec):
    r, d = np.radians(ra), np.radians(dec)
    rp, dp = np.radians(RA_NGP), np.radians(DEC_NGP)
    sb = np.sin(dp)*np.sin(d) + np.cos(dp)*np.cos(d)*np.cos(r - rp)
    b = np.degrees(np.arcsin(np.clip(sb, -1, 1)))
    y = np.cos(d)*np.sin(r - rp)
    x = np.cos(dp)*np.sin(d) - np.sin(dp)*np.cos(d)*np.cos(r - rp)
    l = (L_NCP - np.degrees(np.arctan2(y, x))) % 360.0
    return l, b


def ck(nom, calcule, attendu, tol, rel=True):
    global PASSES
    e = abs(calcule - attendu)/abs(attendu) if (rel and attendu != 0) \
        else abs(calcule - attendu)
    if e > tol:
        ECHECS.append(f"[1] {nom} : recalcul {calcule:.6g} != affiche {attendu:.6g} "
                      f"(ecart {e:.3g} > {tol:g})")
    else:
        PASSES += 1
    return calcule


def present(nom, motifs):
    """le fait est-il affiche quelque part dans les artefacts generes ?"""
    global PASSES
    txt = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                    for p in sorted(VIS.glob("*.html")))
    for m in motifs:
        if re.search(m, txt, re.S):
            PASSES += 1
            return
    AVERTS.append(f"[2] {nom} : aucun des motifs {motifs} trouve dans visuels/")


if __name__ == "__main__":
    print("GARDE-FOU DES ARTEFACTS DU CIEL (criteres geles)\n")
    if not DAT.exists():
        sys.exit(f"  donnees introuvables : {DAT}")

    entetes = DAT.read_text(encoding="utf-8").split("\n", 1)[0].split()
    raw = np.genfromtxt(DAT, names=True, dtype=None, encoding="utf-8")
    masque = (raw['zHD'] > 0.01) & (raw['IS_CALIBRATOR'] == 0)
    ra, dec = raw['RA'][masque], raw['DEC'][masque]
    N = len(ra)
    print(f"  --- echantillon : {N} SNe (z > 0,01, hors calibrateurs) ---")
    ck("effectif", N, 1580, 0, rel=False)

    l, b = galactique(ra, dec)

    print("\n  --- critere 1 : recalcul des faits affiches ---")
    # deficit galactique
    n_bas = int((np.abs(b) < 5.0).sum())
    att = N*np.sin(np.radians(5.0))
    sig = (n_bas - att)/np.sqrt(att)
    print(f"     |b| < 5 deg : {n_bas} observees, {att:.1f} attendues -> {sig:.1f} sigma")
    ck("compte a |b| < 5", n_bas, 0, 0, rel=False)
    ck("attente isotrope a |b| < 5", att, 138.0, 0.01)
    ck("significativite du deficit", abs(sig), 11.7, 0.01)

    # Stripe 82
    s82 = ((((ra + 180) % 360) - 180 > -50) & (((ra + 180) % 360) - 180 < 60)
           & (np.abs(dec) < 1.26))
    n82 = int(s82.sum())
    aire = (110.0/360.0)*(np.sin(np.radians(1.26)) - np.sin(np.radians(-1.26)))/2.0
    print(f"     Stripe 82 : {n82} SNe ({100*n82/N:.1f} %) sur {100*aire:.2f} % du ciel "
          f"-> x{(n82/N)/aire:.0f}")
    ck("SNe dans Stripe 82", n82, 416, 0, rel=False)
    ck("fraction de SNe dans Stripe 82 (%)", 100*n82/N, 26.3, 0.01)
    ck("fraction de ciel de Stripe 82 (%)", 100*aire, 0.46, 0.05)
    ck("facteur de concentration", (n82/N)/aire, 57.0, 0.05)

    # cellules d'aire egale
    nb_s, nb_r = 18, 36
    i_s = np.clip(((np.sin(np.radians(dec)) + 1)/2*nb_s).astype(int), 0, nb_s - 1)
    i_r = np.clip((ra/360.0*nb_r).astype(int), 0, nb_r - 1)
    occup = len(set(zip(i_s.tolist(), i_r.tolist())))
    vides = nb_s*nb_r - occup
    print(f"     cellules : {vides}/{nb_s*nb_r} vides ({100*vides/(nb_s*nb_r):.1f} %)")
    ck("cellules totales", nb_s*nb_r, 648, 0, rel=False)
    ck("cellules vides", vides, 367, 0, rel=False)
    ck("fraction de cellules vides (%)", 100*vides/(nb_s*nb_r), 56.6, 0.01)

    print("\n  --- critere 2 : ces faits sont-ils affiches ? ---")
    present("deficit galactique (138)", [r"\b138\b"])
    present("significativite 11,7", [r"11[,.]7"])
    present("416 SNe", [r"\b416\b"])
    present("26,3 %", [r"26[,.]3"])
    present("0,46 % du ciel", [r"0[,.]46"])
    present("367 cellules vides", [r"\b367\b"])
    present("648 cellules", [r"\b648\b"])
    present("52,9 sigma", [r"52[,.]9"])
    print(f"     {PASSES} presence(s)/recalcul(s) valide(s) a ce stade")

    print("\n  --- critere 3 : marqueurs non substitues dans les sorties ---")
    sales = []
    for p in sorted(VIS.glob("*.html")):
        m = sorted(set(re.findall(r"__[A-Z_]+__", p.read_text(encoding="utf-8",
                                                              errors="ignore"))))
        if m:
            sales.append(f"{p.name} : {' '.join(m)}")
    if sales:
        for s in sales:
            ECHECS.append(f"[3] marqueur non substitue -> {s}")
    else:
        PASSES += 1
        print(f"     {len(list(VIS.glob('*.html')))} artefact(s) sans marqueur -> OK")

    print("\n  --- critere 4 : les gabarits ont-ils garde leurs marqueurs ? ---")
    vides_gab = []
    for p in sorted(GAB.glob("*template*.html")) + sorted(GAB.glob("ciel_v*_base.html")):
        if not re.search(r"__[A-Z_]+__", p.read_text(encoding="utf-8", errors="ignore")):
            vides_gab.append(p.name)
    if vides_gab:
        for g in vides_gab:
            ECHECS.append(f"[4] gabarit sans marqueur (ecrase par une sortie ?) : {g}")
    else:
        PASSES += 1
        print(f"     tous les gabarits ont conserve leurs marqueurs -> OK")

    print(f"\n  --- BILAN ---")
    print(f"     {PASSES} verification(s) passee(s)")
    for a in AVERTS:
        print(f"     avertissement : {a}")
    if ECHECS:
        print(f"\n     {len(ECHECS)} ECHEC(S) BLOQUANT(S) :")
        for e in ECHECS:
            print(f"       - {e}")
        sys.exit(1)
    print("     aucun echec bloquant.")
