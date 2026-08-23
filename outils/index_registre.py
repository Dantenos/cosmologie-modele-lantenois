#!/usr/bin/env python3
"""index_registre v1 — l'index citable de MANQUEMENTS.md (23/08/2026).

MANQUEMENTS.md n'est pas injectif : 22 numéros portent deux entrées (les plages #72-#81 et
#103-#114 ont été réutilisées), #21 n'existe pas, #130 est physiquement dupliqué. On ne
renumérote PAS l'histoire (les papiers et registres citent ces numéros) ; on rend
l'ambiguïté visible : ce script balaie les en-têtes d'entrée, suffixe a/b les doublons dans
l'ordre du fichier, et écrit registres/INDEX_MANQUEMENTS.md (numéro, suffixe, ligne, date,
titre). Toute citation nouvelle doit utiliser le suffixe quand il existe.

Sortie : l'index, plus un bilan (présents, absents, dupliqués). Exit 0 toujours — c'est un
index, pas un garde-fou ; le garde-fou est que l'index est régénérable et versionné.
Usage : python3 outils/index_registre.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "registres" / "MANQUEMENTS.md"
OUT = ROOT / "registres" / "INDEX_MANQUEMENTS.md"

def entrees():
    rx = re.compile(r"^(?:##\s+(?P<date>[\d/]+)?[^#\n]*#(?P<n1>\d+)\s+(?P<t1>.*)|\*\*#(?P<n2>\d+)\s*(?:[—-]|\.)\s*(?P<t2>[^*]*)\*\*)")
    out = []
    for i, ligne in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
        m = rx.match(ligne)
        if m:
            n = int(m.group("n1") or m.group("n2"))
            titre = (m.group("t1") or m.group("t2") or "").strip().rstrip("*").strip()
            date = m.group("date") or ""
            out.append((n, i, date, titre[:110]))
    return out

if __name__ == "__main__":
    e = entrees()
    vus = {}
    lignes = ["# INDEX DE MANQUEMENTS.md — généré par `outils/index_registre.py`, ne pas éditer à la main",
              "",
              "*La numérotation historique n'est pas injective (plages #72-#81 et #103-#114 réutilisées,",
              "#130 dupliqué, #21 absent). Les doublons sont suffixés a/b dans l'ordre du fichier ;*",
              "*toute citation nouvelle utilise le suffixe.*",
              "", "| entrée | ligne | date | titre |", "|---|---|---|---|"]
    for n, i, date, titre in e:
        vus.setdefault(n, []).append(i)
        suf = chr(ord('a') + len(vus[n]) - 1) if True else ""
        tag = f"#{n}{suf if len([x for x in e if x[0] == n]) > 1 else ''}"
        lignes.append(f"| {tag} | {i} | {date} | {titre.replace('|', '\\|')} |")
    nums = sorted(vus)
    absents = [k for k in range(22, max(nums)+1) if k not in vus]   # 1-20 = liste initiale par artefact (l.5-38), hors numerotation
    doubles = {k: v for k, v in vus.items() if len(v) > 1}
    lignes += ["", f"**Bilan** : {len(e)} entrées numérotées (les points 1-20 + 8 bis vivent en liste initiale l.5-38) ; numéros {min(nums)}-{max(nums)} ; "
               f"absents : {absents or 'aucun'} ; dupliqués ({len(doubles)}) : "
               + (", ".join(f"#{k} (l.{', l.'.join(map(str, v))})" for k, v in sorted(doubles.items())) or "aucun") + "."]
    OUT.write_text("\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
    print(f"[index] {len(e)} entrées -> {OUT.name} ; absents {absents} ; {len(doubles)} numéros dupliqués")
