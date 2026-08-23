#!/usr/bin/env python3
"""registre v0 — la falsification-as-code. Né du corpus cosmologie (116 entrées, août 2026).

PRINCIPE. Un résultat n'est opposable que si son critère de succès a été gelé AVANT
l'exécution. `registre` extrait le bloc de critères du docstring d'un script, le fige par
hash dans registre.lock, et `verify` échoue (exit 1, bloquant en CI) si le critère a bougé
après coup. Tout amendement est possible — mais public : il s'écrit dans RETRACTATIONS.md.

CRITÈRES PRÉ-ENREGISTRÉS DE CE PROJET (gelés par lui-même, commit 0) :
  - v0 réussit si : freeze puis verify passent sur >= 2 scripts réels du corpus, et si la
    falsification d'un critère est détectée (verify -> exit 1).
  - v0 échoue et n'est pas publié si : un faux positif apparaît sur un fichier non modifié.

Usage : registre.py freeze f1.py [f2.py ...] | verify [f...] | log
"""
import sys, json, hashlib, ast, datetime, pathlib

BASE = pathlib.Path(__file__).resolve().parent   # dossier de l'outil (outils/)
ROOT = BASE.parent                               # racine du depot
LOCK = BASE / "registre.lock"                    # le lock vit a cote de l'outil
RETR = ROOT / "RETRACTATIONS.md"                 # les retractations, a la racine du depot

def critere(path):
    p = pathlib.Path(path)
    if not p.is_absolute():
        p = ROOT / p                             # cles du lock relatives a la racine
    src = p.read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(src)) or ""
    if not doc.strip():
        sys.exit(f"[registre] {path}: aucun docstring — pas de critère à geler. REFUS.")
    return hashlib.sha256(doc.encode()).hexdigest(), doc

def charge():
    return json.loads(LOCK.read_text()) if LOCK.exists() else {}

def freeze(files, amend=False):
    lock = charge()
    for f in files:
        h, doc = critere(f)
        if f in lock and lock[f]["sha256"] != h:
            if not amend:
                sys.exit(f"[registre] {f}: critère DÉJÀ GELÉ et modifié depuis. "
                         f"Refus. (--amend pour amender publiquement)")
            with RETR.open("a", encoding="utf-8") as r:
                r.write(f"\n## {datetime.date.today()} — AMENDEMENT {f}\n"
                        f"ancien hash {lock[f]['sha256'][:12]} -> {h[:12]}. "
                        f"Justification à écrire ici, sinon l'amendement est nul.\n")
            print(f"[registre] {f}: amendé, consigné dans {RETR}")
        lock[f] = {"sha256": h, "gele_le": datetime.datetime.now().isoformat(timespec='seconds'),
                   "extrait": doc.strip().splitlines()[0][:80]}
        print(f"[registre] gelé : {f}  ({h[:12]})")
    LOCK.write_text(json.dumps(lock, indent=1, ensure_ascii=False))

def verify(files=None):
    lock = charge()
    cibles = files or list(lock)
    ko = 0
    for f in cibles:
        if f not in lock:
            print(f"[registre] {f}: NON GELÉ — tout résultat de ce script est inopposable."); ko += 1; continue
        h, _ = critere(f)
        ok = h == lock[f]["sha256"]
        print(f"[registre] {'OK   ' if ok else 'ÉCHEC'} {f}"
              + ("" if ok else "  <- critère modifié APRÈS gel"))
        ko += (not ok)
    sys.exit(1 if ko else 0)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd, rest = a[0], [x for x in a[1:] if x != "--amend"]
    if cmd == "freeze": freeze(rest, amend="--amend" in a)
    elif cmd == "verify": verify(rest or None)
    elif cmd == "log": print(json.dumps(charge(), indent=1, ensure_ascii=False))
    else: sys.exit(__doc__)
