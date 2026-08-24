#!/usr/bin/env python3
"""etat v1 — l'état du dépôt, GÉNÉRÉ depuis les sources (23/08/2026). Jamais écrit à la main.
Tous les comptes qui vivaient en dur dans les façades (et que perime.py ne fait qu'attraper)
sortent d'ici : lock (critères gelés), INDEX_MANQUEMENTS (entrées, doublons), TRIAGE (bilan),
audience.json (affaires), SHA256SUMS (données), scripts/outils/visuels (fichiers), rapports
d'études (verdicts). Écrit registres/ETAT.md et imprime le résumé. exit 0 toujours.
Usage : python3 outils/etat.py
"""
import json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent

def main():
    lock = json.loads((ROOT / "outils/registre.lock").read_text(encoding="utf-8"))
    # regenere l'index du registre AVANT de le lire (sinon compte perime)
    import sys as _s, subprocess as _sp; _s.path.insert(0, str(ROOT / "outils"))
    import index_registre as _ir
    _n_ent = len(_ir.entrees())
    _sp.run([_s.executable, str(ROOT / "outils/index_registre.py")], capture_output=True)
    idx = (ROOT / "registres/INDEX_MANQUEMENTS.md")
    bilan = [l for l in idx.read_text(encoding="utf-8").splitlines() if l.startswith("**Bilan**")]
    m = re.search(r"(\d+) entrées", bilan[0]) if bilan else None
    n_entrees = m.group(1) if m else "?"
    tri = (ROOT / "registres/TRIAGE_DES_ATTAQUES.md").read_text(encoding="utf-8")
    mts = re.findall(r"Bilan[^:]*: (\d+) attaques justes, (\d+) affirmations", tri)
    mt = mts[-1] if mts else None
    aud = json.loads((ROOT / "outils/audience.json").read_text(encoding="utf-8"))
    shas = [l for l in (ROOT / "donnees/SHA256SUMS").read_text(encoding="utf-8").splitlines() if l.strip()]
    n_scripts = len(list((ROOT / "scripts").glob("*.py")))
    n_outils = len(list((ROOT / "outils").glob("*.py")))
    etudes = []
    for f in sorted((ROOT / "registres").glob("ETUDE_E*.md")):
        txt = f.read_text(encoding="utf-8")
        mv = re.search(r"## Verdict\s*\n\*{0,2}([^\n*]{5,120})", txt)
        etudes.append((f.name, (mv.group(1).strip() if mv else "(pas de section Verdict)")))
    L = [f"# ÉTAT DU DÉPÔT — généré par `outils/etat.py` le {datetime.date.today()} — ne pas éditer à la main", "",
         f"- **Critères gelés** : {len(lock)} (`outils/registre.lock`) — 0 amendé (`RETRACTATIONS.md`)",
         f"- **Registre** : {n_entrees} entrées numérotées (`INDEX_MANQUEMENTS.md`)",
         f"- **Triage** : {mt[0]} attaques justes, {mt[1]} affirmations réfutées (dernier bilan)" if mt else "- Triage : bilan introuvable",
         f"- **Affaires au rôle** : {len(aud['affaires'])} ({', '.join(aud['affaires'])})",
         f"- **Données publiques** : {len(shas)} fichiers sous empreinte (`donnees/SHA256SUMS`)",
         f"- **Scripts** : {n_scripts} dans `scripts/` ; **outils** : {n_outils} dans `outils/`",
         "", "## Études (verdicts, depuis les rapports)", ""]
    for n, v in etudes: L.append(f"- `{n}` — {v}")
    (ROOT / "registres/ETAT.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    # facades AUTO (corps, 24/08) : les comptes derives du lock sont REECRITS dans les facades —
    # trois fois cette session un compte recopie a la main a diverge ; plus jamais.
    import re as _re
    n = len(lock)
    for rel, subs in [("README.md", [(r"registre-\d+%20crit", f"registre-{n}%20crit"),
                                     (r"\d+ fichiers du corpus sont gelés", f"{n} fichiers du corpus sont gelés"),
                                     (r"# \d+ fichiers, exit 0", f"# {n} fichiers, exit 0")]),
                      ("outils/README_registre.md", [(r"\(\d+ fichiers gelés au [\d/]+\)", f"({n} fichiers gelés au {datetime.date.today():%d/%m/%Y})")])]:
        f2 = ROOT / rel; txt = f2.read_text(encoding="utf-8"); t0 = txt
        for pat, rep in subs: txt = _re.sub(pat, rep, txt)
        if txt != t0:
            f2.write_text(txt, encoding="utf-8", newline="\n"); print(f"[etat] façade mise à jour : {rel} -> {n}")
    vc = ROOT / "outils/valeurs_canoniques.json"; cv = json.loads(vc.read_text(encoding="utf-8"))
    for qte in cv["quantites"]:
        if qte["nom"] == "nombre d'entrées du registre":
            att2 = [rf"\\b(?!{_n_ent}\\b)1\\d\\d entrées(?! à la naissance)"]
            if not (qte["valeur_courante"].startswith(str(_n_ent)) and qte["valeurs_depreciees"] == att2):
                qte["valeur_courante"] = f"{_n_ent} ({datetime.date.today():%d/%m/%Y})"
                qte["valeurs_depreciees"] = att2
                vc.write_text(json.dumps(cv, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
                print(f"[etat] valeurs_canoniques : entrées du registre = {_n_ent}")
        if qte["nom"] == "critères gelés":
            attendu = [rf"\b(?!{n}\b)\d+ (critères|fichiers|scripts) (gelés|du corpus sont gelés)"]
            if qte["valeur_courante"].startswith(str(n)) and qte["valeurs_depreciees"] == attendu:
                continue
            qte["valeur_courante"] = f"{n} ({datetime.date.today():%d/%m/%Y})"
            qte["valeurs_depreciees"] = attendu
            vc.write_text(json.dumps(cv, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            print(f"[etat] valeurs_canoniques : critères gelés = {n}")
    print("\n".join(L[2:9]))
    print(f"[etat] écrit : registres/ETAT.md ({len(etudes)} études)")

if __name__ == "__main__":
    main()
