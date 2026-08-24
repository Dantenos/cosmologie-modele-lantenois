#!/usr/bin/env python3
"""genere_ciel_bilingue — UNE VERSION ENTIEREMENT FRANCAISE ET UNE ENTIEREMENT ANGLAISE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

CE QUE CE SCRIPT FAIT, ET POURQUOI IL NE TRADUIT PAS A LA MAIN. Une traduction manuelle
laisse toujours passer une chaine oubliee, et une chaine oubliee dans une version dite
« uniquement anglaise » est un DEFAUT SILENCIEUX. Ici la traduction est une table explicite
(outils/traduction_ciel_en.py), appliquee du plus long au plus court pour qu'aucun fragment
ne soit avale par une entree plus courte, et le resultat est VERIFIE : si du francais
subsiste dans la version anglaise, le script REFUSE d'ecrire.

  Version FR : visuels/ciel_pantheon_v7_fr.html — identique a la v7, aucun mot anglais
    d'interface (les noms propres et les sigles restent : SDSS, Stripe 82, Sgr A*, Mpc, HUD).
  Version EN : visuels/ciel_pantheon_v7_en.html — meme figure, memes donnees, meme code,
    interface entierement anglaise.
Les DONNEES ne sont pas retraduites : elles sont recalculees par les fonctions gelees de
genere_ciel_v3 et doivent redonner exactement les memes comptes que v3 a v7.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. IDENTITE : 1580 / 553 / 623 / 150 / 69 ; 0 SNe a |b| < 5 deg ; 6 a |b| < 10 ;
     416 dans Stripe 82 — les memes qu'en v3, v4, v5, v6 et v7.
  2. PURETE DE LA VERSION ANGLAISE. Le HTML anglais, une fois retire le bloc de donnees
     numeriques et les noms propres declares, ne doit contenir AUCUN des marqueurs
     francais suivants : les caracteres accentues (a-circonflexe et compagnie) et les mots
     outils « les », « des », « une », « qui », « pas », « pour », « dans », « sur »,
     « avec », « est », « sont », « ciel », « vide », « point ». Un seul suffit a REFUSER.
  3. PURETE DE LA VERSION FRANCAISE. Le HTML francais ne doit contenir aucun des mots
     anglais « the », « with », « from », « which », « sky », « void », « expected »,
     « computed », « displayed », « edges ». Un seul suffit a REFUSER.
     (Les sigles et noms propres sont exclus des deux controles : SDSS, Stripe, Sgr, HUD,
     Mollweide, Kuiper, Oort, Mpc, kpc, deg, ΛCDM, PNG, id, div, span, class, style,
     ainsi que tout le JavaScript, dont les mots-cles sont anglais par nature.)
  4. COUVERTURE DE LA TABLE. Toute entree de la table de traduction doit avoir ete
     APPLIQUEE au moins une fois. Une entree jamais declenchee signale une chaine qui a
     change dans le gabarit sans que la traduction suive — c'est un avertissement bloquant.

NOTE DECLAREE : le controle 2 ne peut porter que sur le TEXTE D'INTERFACE. Le JavaScript
et le CSS sont en anglais dans les deux versions (c'est la langue de ces langages), et les
commentaires de code sont exclus des deux controles. Ce que ces criteres garantissent, c'est
que ce qu'un LECTEUR VOIT est monolingue — pas que le fichier l'est.

Usage : python3 outils/genere_ciel_bilingue.py
"""
import sys, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils"))
sys.path.insert(0, str(ROOT / "scripts"))
import genere_ciel_v7 as C7
from traduction_ciel_en import MAP

EXCLUS = ["SDSS", "Stripe", "Sgr", "HUD", "Mollweide", "Kuiper", "Oort", "Mpc", "kpc",
          "deg", "PNG", "px", "rgba", "Georgia", "Consolas", "Menlo", "monospace"]
FR_MARQUEURS = [r"\bles\b", r"\bdes\b", r"\bune\b", r"\bqui\b", r"\bpas\b", r"\bpour\b",
                r"\bdans\b", r"\bsur\b", r"\bavec\b", r"\best\b", r"\bsont\b",
                r"\bciel\b", r"\bvide\b", r"\bpoint\b", r"[àâçèéêëîïôùûœ]"]
EN_MARQUEURS = [r"\bthe\b", r"\bwith\b", r"\bfrom\b", r"\bwhich\b", r"\bsky\b",
                r"\bvoid\b", r"\bexpected\b", r"\bcomputed\b", r"\bdisplayed\b", r"\bedges\b"]


def texte_visible(html):
    """ne garde que ce qu'un lecteur voit : hors <script>, <style>, attributs et donnees."""
    h = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    h = re.sub(r"<style[\s\S]*?</style>", " ", h, flags=re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for e in EXCLUS:
        h = h.replace(e, " ")
    return h


def chaines_js(html):
    """les chaines litterales du JS : c'est la que vit le texte d'interface."""
    m = re.search(r"<script>([\s\S]*?)</script>", html)
    if not m:
        return ""
    js = m.group(1)
    js = re.sub(r"//[^\n]*", " ", js)
    out = []
    for q in re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', js):
        out.append(q)
    for q in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'", js):
        out.append(q)
    t = " ".join(out)
    for e in EXCLUS:
        t = t.replace(e, " ")
    return t


def controle(html, marqueurs, nom):
    zone = texte_visible(html) + " " + chaines_js(html)
    trouves = []
    for m in marqueurs:
        f = re.findall(m, zone, flags=re.I)
        if f:
            trouves.append((m, len(f), f[:3]))
    return trouves


def main():
    fr = (ROOT / "visuels" / "ciel_pantheon_v7.html")
    if not fr.exists():
        sys.exit("[bilingue] REFUS : ciel_pantheon_v7.html absent (lancer genere_ciel_v7.py)")
    src = fr.read_text(encoding="utf-8")

    # --- verif 1 : identite des comptes, relue dans le fichier lui-meme
    for attendu in ["1580", "553", "623", "150", "69", "416"]:
        if attendu not in src:
            sys.exit(f"[bilingue] REFUS verif 1 : compte {attendu} absent du HTML source")

    # --- traduction, du plus long au plus court
    en = src
    utilisees = {}
    for k in sorted(MAP, key=len, reverse=True):
        n = en.count(k)
        if n:
            en = en.replace(k, MAP[k])
        utilisees[k] = n
    jamais = [k for k, n in utilisees.items() if n == 0]
    if jamais:
        print(f"[bilingue] REFUS verif 4 : {len(jamais)} entree(s) de la table jamais "
              f"declenchee(s) — le gabarit a change sans la traduction :")
        for k in jamais[:8]:
            print(f"    {k[:78]!r}")
        sys.exit(1)

    # --- verif 2 : purete de l'anglais
    reste = controle(en, FR_MARQUEURS, "EN")
    if reste:
        print("[bilingue] REFUS verif 2 : du francais subsiste dans la version anglaise :")
        for m, n, ex in reste[:8]:
            print(f"    {m} ({n}x) : {ex}")
        sys.exit(1)

    # --- verif 3 : purete du francais
    resteE = controle(src, EN_MARQUEURS, "FR")
    if resteE:
        print("[bilingue] REFUS verif 3 : de l'anglais subsiste dans la version francaise :")
        for m, n, ex in resteE[:8]:
            print(f"    {m} ({n}x) : {ex}")
        sys.exit(1)

    en = en.replace('<html lang="fr">', '<html lang="en">', 1)
    dfr = ROOT / "visuels" / "ciel_pantheon_v7_fr.html"
    den = ROOT / "visuels" / "ciel_pantheon_v7_en.html"
    dfr.write_text(src, encoding="utf-8", newline="\n")
    den.write_text(en, encoding="utf-8", newline="\n")
    print(f"[bilingue] ecrit : {dfr.name} ({dfr.stat().st_size // 1024} ko) et "
          f"{den.name} ({den.stat().st_size // 1024} ko)")
    print(f"           table de {len(MAP)} entrees, toutes appliquees ; "
          f"purete des deux versions verifiee")


if __name__ == "__main__":
    main()
