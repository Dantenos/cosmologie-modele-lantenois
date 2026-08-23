#!/usr/bin/env python3
"""rejouer v1 — « registre run » : les ancres numériques rejouées et confrontées (23/08/2026).
Feuille de route de README_registre (v0.2 : « registre run qui exécute et confronte la
sortie aux seuils gelés »), réalisée SANS toucher aux docstrings gelés : les ancres vivent
dans outils/ancres.json (versionné), une regex par quantité, des bornes déclarées.

PRINCIPE. Pour chaque script listé : exécution réelle (depuis donnees/pantheon_plus, comme
la convention du corpus), capture de la sortie, extraction de chaque ancre par regex,
comparaison aux bornes. ÉCHEC si : la regex ne matche pas (la sortie a changé de forme),
la valeur sort des bornes (le résultat a bougé), ou le script sort en erreur. exit 1 au
moindre échec — bloquant en CI : un résultat du corpus qui cesse de se reproduire fait
rougir le build, pas seulement un critère modifié.

CRITÈRE PRÉ-ENREGISTRÉ : v1 réussit si les 14 scripts du json passent sur le dépôt du
23/08 ; il échoue s'il produit un faux positif sur un script non modifié.
Usage : python3 outils/rejouer.py [scripts...]   (défaut : tous ceux d'ancres.json)
"""
import sys, re, json, subprocess, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "outils" / "ancres.json").read_text(encoding="utf-8"))
CWD = ROOT / CFG.get("cwd", ".")

def run(rel, spec):
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, str(ROOT / rel)], cwd=CWD, capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=spec.get("timeout", 600), env=None)
    except subprocess.TimeoutExpired:
        return [(rel, "(timeout)", None, None, None, False)], time.time() - t0
    out = (r.stdout or "") + (r.stderr or "")
    rows = []
    if r.returncode != 0:
        rows.append((rel, f"(exit {r.returncode})", None, None, None, False))
    for a in spec["ancres"]:
        m = re.search(a["regex"], out)
        if not m:
            rows.append((rel, a["nom"], None, a["min"], a["max"], False)); continue
        v = float(m.group(1).replace(",", "."))
        rows.append((rel, a["nom"], v, a["min"], a["max"], a["min"] <= v <= a["max"]))
    return rows, time.time() - t0

if __name__ == "__main__":
    cibles = sys.argv[1:] or list(CFG["scripts"])
    ko = 0
    print(f"{'script':<36s} {'ancre':<26s} {'valeur':>12s} {'bornes':>20s}  verdict")
    for rel in cibles:
        spec = CFG["scripts"].get(rel)
        if spec is None:
            print(f"{rel:<36s} (aucune ancre déclarée)"); continue
        rows, dt = run(rel, spec)
        for _, nom, v, lo, hi, ok in rows:
            vs = "—" if v is None else f"{v:.6g}"
            bs = "" if lo is None else f"[{lo} ; {hi}]"
            print(f"{pathlib.Path(rel).name:<36s} {nom:<26s} {vs:>12s} {bs:>20s}  {'OK' if ok else 'ÉCHEC'}"
                  + (f"  ({dt:.0f}s)" if nom == rows[-1][1] else ""))
            ko += (not ok)
    print(f"\n[rejouer] {ko} échec(s) sur {len(cibles)} script(s)")
    sys.exit(1 if ko else 0)
