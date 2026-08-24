#!/usr/bin/env python3
"""VERSIONS UNIQUEMENT ANGLAISE ET UNIQUEMENT FRANCAISE, POUR PLUSIEURS ARTEFACTS.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI UNE v2. `genere_ciel_bilingue.py` (gele fc8e0f3d2803) est cable sur
ciel_pantheon_v7.html et exige, par sa verif 4, que CHAQUE entree de la table de traduction
soit declenchee. Cette exigence etait juste tant qu'un seul artefact etait traduit : une
entree jamais declenchee y signalait un gabarit modifie sans sa traduction. Des que la table
sert DEUX artefacts, elle devient impossible a satisfaire -- les entrees propres a v8 ne
peuvent pas se declencher sur v7, et reciproquement.
La garantie n'est pas abandonnee, elle est DEPLACEE : elle porte desormais sur la table
ENTIERE, tous artefacts confondus. Une entree que AUCUN artefact ne declenche reste un
echec bloquant, et c'est le meme defaut qu'avant : du texte traduit qui n'existe plus.

--- CRITERES (exhaustifs) ---
  1. IDENTITE DES COMPTES. Chaque source doit contenir les comptes mesures 1580 et 416 ;
     leur absence signifie qu'on traduit un artefact perime. ECHEC BLOQUANT.
  2. PURETE ANGLAISE. La version _en ne doit contenir AUCUNE lettre accentuee francaise ni
     aucun mot francais temoin, cherches dans le texte visible ET dans les chaines JS
     (jamais dans les identifiants de code, jamais dans les tableaux numeriques).
     ECHEC BLOQUANT, artefact par artefact.
  3. PURETE FRANCAISE. La version _fr ne doit contenir aucun mot anglais temoin dans les
     memes zones. La version _fr est la source elle-meme : ce controle verifie donc que la
     source n'a pas ete contaminee par une traduction partielle anterieure.
  4. COUVERTURE DE LA TABLE. Apres traitement de TOUS les artefacts demandes, toute entree
     jamais declenchee est un ECHEC BLOQUANT, avec la liste. C'est la verif 4 de la v1,
     portee au niveau de la table.
  5. NON-REGRESSION DE TAILLE. Chaque sortie doit peser au moins 90 % de sa source. Une
     sortie beaucoup plus courte signifie qu'une substitution a mange du contenu -- defaut
     qu'aucun controle de purete n'attraperait.

REGLE 7 APPLIQUEE. Tous les controles textuels sont des expressions regulieres, jamais des
egalites strictes, et la detection des marqueurs residuels est GENERIQUE (/__[A-Z_]+__/) et
non une liste ecrite a la main -- c'est une telle liste qui avait laisse passer l'echec
total de la v8 du ciel.
Usage : python3 outils/genere_bilingue_v2.py [v7 v8 ...]   (depuis la racine)
"""
import sys
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
from traduction_ciel_en import MAP

VIS = ROOT / "visuels"
ACCENTS = r"[\u00e0\u00e2\u00e7\u00e8\u00e9\u00ea\u00eb\u00ee\u00ef\u00f4\u00f9\u00fb\u0153]"
FR_MOTS = [r"\bpour\b", r"\bdans\b", r"\bavec\b", r"\bsans\b", r"\bcette\b", r"\bqui\b",
           r"\bmais\b", r"\bciel\b", r"\bvide\b", r"\bnombre\b"]
EN_MOTS = [r"\bthe sky\b", r"\bexpected\b", r"\bneighbours\b", r"\bwithout\b",
           r"\bwhole sample\b", r"\bfixed seed\b"]


def _js(m):
    """dans un bloc <script>, ne garde que les litteraux de chaine.
    DEFAUT DE CORPS CORRIGE : les COMMENTAIRES sont retires D'ABORD. Une apostrophe
    francaise dans un commentaire (« pour l'animer ») ouvrait sinon un faux litteral qui
    avalait le commentaire entier, et le controle de purete signalait du francais la ou il
    n'y a que du code non affiche. Deux faux positifs sur v7 et v8 l'ont revele."""
    js = re.sub(r"/\*.*?\*/", " ", m.group(0), flags=re.S)
    js = re.sub(r"(?m)//[^\n]*$", " ", js)
    return " ".join(x or y for x, y in
                    re.findall(r'"([^"\\]{4,})"|\'([^\'\\]{4,})\'', js))


def zone(h):
    h = re.sub(r"<script[^>]*>.*?</script>", _js, h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"[-+0-9.,eE\[\]]{8,}", " ", h)


if __name__ == "__main__":
    noms = sys.argv[1:] or ["v7", "v8"]
    echecs, declenchees = [], {k: 0 for k in MAP}
    print("VERSIONS EN / FR (criteres geles)\n")

    for n in noms:
        src_p = VIS / f"ciel_pantheon_{n}.html"
        if not src_p.exists():
            echecs.append(f"[0] source absente : {src_p.name}")
            continue
        src = src_p.read_text(encoding="utf-8")
        print(f"  --- {src_p.name} ---")

        # critere 1
        manquants = [c for c in ("1580", "416") if c not in src]
        if manquants:
            echecs.append(f"[1] {src_p.name} : compte(s) {manquants} absent(s)")
            continue

        # traduction, du plus long au plus court
        en = src
        for k in sorted(MAP, key=len, reverse=True):
            c = en.count(k)
            if c:
                declenchees[k] += c
                en = en.replace(k, MAP[k])

        z_en, z_fr = zone(en), zone(src)
        acc = re.findall(ACCENTS, z_en)
        mots = [w for w in FR_MOTS if re.search(w, z_en, re.I)]
        if acc or mots:
            echecs.append(f"[2] {n}_en : {len(acc)} accent(s) {sorted(set(acc))[:6]} ; "
                          f"mots {mots}")
        else:
            print("     purete anglaise -> OK")
        tr = [w for w in EN_MOTS if re.search(w, z_fr, re.I)]
        if tr:
            echecs.append(f"[3] {n}_fr : mots anglais {tr}")
        else:
            print("     purete francaise -> OK")

        for suffixe, contenu in (("_en", en), ("_fr", src)):
            if len(contenu) < 0.90*len(src):
                echecs.append(f"[5] {n}{suffixe} : {len(contenu)} o pour une source de "
                              f"{len(src)} o — substitution destructrice")
                continue
            if re.search(r"__[A-Z_]+__", contenu):
                echecs.append(f"[2] {n}{suffixe} : marqueur non substitue")
                continue
            (VIS / f"ciel_pantheon_{n}{suffixe}.html").write_text(
                contenu, encoding="utf-8", newline="\n")
            print(f"     ecrit : ciel_pantheon_{n}{suffixe}.html ({len(contenu)//1024} ko)")

    print("\n  --- critere 4 : couverture de la table ---")
    mortes = [k for k, c in declenchees.items() if c == 0]
    if mortes:
        echecs.append(f"[4] {len(mortes)} entree(s) de la table jamais declenchee(s) sur "
                      f"aucun artefact")
        for k in mortes[:10]:
            print(f"     jamais declenchee : {k[:72]!r}")
    else:
        print(f"     {len(MAP)} entrees, toutes declenchees au moins une fois -> OK")

    if echecs:
        print(f"\n  {len(echecs)} ECHEC(S) BLOQUANT(S) :")
        for e in echecs:
            print(f"    - {e}")
        sys.exit(1)
    print("\n  aucun echec bloquant.")
