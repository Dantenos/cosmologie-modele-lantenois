#!/usr/bin/env python3
"""confronteur v1 — la cohérence croisée as code (24/08/2026). CRITERES PRE-ENREGISTRES.

La leçon de l'audit du 23/08 : les erreurs ne vivaient pas dans les calculs mais ENTRE deux
calculs de la même quantité (deux χ² pour un modèle, A=1,551 dérivé nulle part, deux fσ8 de
signes opposés, deux β pour 1580 SNe). `rejouer` confronte un script à ses ancres ; le
confronteur confronte les scripts ENTRE EUX : chaque paire de outils/confrontations.json
est deux calculs independants de la meme quantite (ou un calcul contre une constante
embarquee ailleurs, avec sa source), executes reellement, extraits par regex, compares a
tolerance declaree. ECHEC (exit 1) si : une regex ne matche plus, un script sort en erreur,
ou |a-b|/|b| depasse tol_rel — une divergence silencieuse entre deux implementations est
une erreur de la classe la plus dangereuse du corpus (#150 : deux implementations du rival,
deux verdicts). CRITERE : v1 reussit si les 5 paires du json passent sur le depot du 24/08 ;
faux positif sur depot non modifie = echec de l'outil.
Usage : python3 outils/confronteur.py [noms...]
"""
import sys, re, json, subprocess, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "outils/confrontations.json").read_text(encoding="utf-8"))
CWD = ROOT / CFG.get("cwd", ".")
_cache = {}

def valeur(cote):
    if "constante" in cote:
        return float(cote["constante"]), "constante"
    rel = cote["script"]
    if rel not in _cache:
        t0 = time.time()
        r = subprocess.run([sys.executable, str(ROOT / rel)], cwd=CWD, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=cote.get("timeout", 600))
        _cache[rel] = ((r.stdout or "") + (r.stderr or ""), r.returncode, time.time() - t0)
    out, rc, dt = _cache[rel]
    if rc != 0: return None, f"exit {rc}"
    m = re.search(cote["regex"], out)
    return (float(m.group(1)) if m else None), f"{dt:.0f}s"

if __name__ == "__main__":
    cibles = [p for p in CFG["paires"] if not sys.argv[1:] or any(a in p["nom"] for a in sys.argv[1:])]
    ko = 0
    for p in cibles:
        va, ia = valeur(p["a"]); vb, ib = valeur(p["b"])
        if va is None or vb is None:
            print(f"ÉCHEC  {p['nom']} : extraction impossible (a: {ia}, b: {ib})"); ko += 1; continue
        ecart = abs(va - vb)/abs(vb) if vb else abs(va - vb)
        ok = ecart <= p["tol_rel"]
        print(f"{'OK    ' if ok else 'ÉCHEC '} {p['nom']}")
        print(f"        a = {va:.6g}  b = {vb:.6g}  écart = {ecart*100:.2f} %  (tol {p['tol_rel']*100:.2f} %)")
        ko += (not ok)
    print(f"\n[confronteur] {ko} divergence(s) sur {len(cibles)} paire(s)")
    sys.exit(1 if ko else 0)
