#!/usr/bin/env python3
"""greffier v1 — le registre des tensions vivantes (24/08/2026). CRITERES PRE-ENREGISTRES.

MANQUEMENTS tient le passe (les erreurs), l'Audience tient le futur promis (les predictions
datees) ; le greffier tient le PRESENT ANORMAL : les tensions, matiere premiere des
decouvertes (la chaine beta_1 est nee de T1 traitee ainsi). Chaque tension de
outils/tensions.json DOIT porter : magnitude chiffree, lectures rivales (>= 2), ARBITRE
pre-enregistre, statut. REGLE DU GREFFE (le critere de cet outil) : une tension ne passe a
« resolue » que si son champ « resolution » cite (a) l'arbitre nomme AVANT la resolution
(le meme que le champ arbitre), (b) la date, (c) l'entree de registre — sinon exit 1 :
il est interdit de reecrire l'histoire d'une anomalie. Schema viole = exit 1, rien n'est
genere. Sortie : registres/TENSIONS.md, genere, jamais ecrit a la main.
Usage : python3 outils/greffier.py
"""
import sys, json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ["id", "ouverte_le", "statut", "enonce", "magnitude", "lectures", "arbitre", "refs"]
STATUTS = {"ouverte", "en_jugement", "resolue"}

def main():
    d = json.loads((ROOT / "outils/tensions.json").read_text(encoding="utf-8"))
    fautes = []
    for t in d["tensions"]:
        for k in REQ:
            if not t.get(k): fautes.append(f"{t.get('id','?')} : champ manquant ou vide « {k} »")
        if t.get("statut") not in STATUTS: fautes.append(f"{t.get('id')} : statut inconnu")
        if len(t.get("lectures", [])) < 2: fautes.append(f"{t.get('id')} : moins de deux lectures rivales")
        if t.get("statut") == "resolue":
            r = t.get("resolution") or {}
            if not (r.get("arbitre") and r.get("date") and r.get("registre")):
                fautes.append(f"{t['id']} : resolue sans resolution complete (arbitre, date, registre)")
            elif r["arbitre"] not in t["arbitre"]:
                fautes.append(f"{t['id']} : resolue par un arbitre non nomme d'avance — interdit")
    if fautes:
        print("[greffier] REFUS :\n  " + "\n  ".join(fautes)); sys.exit(1)
    n = {s: sum(1 for t in d["tensions"] if t["statut"] == s) for s in ("ouverte", "en_jugement", "resolue")}
    L = ["# LE REGISTRE DES TENSIONS — généré par `outils/greffier.py`, ne pas éditer à la main", "",
         f"*{datetime.date.today()} — {len(d['tensions'])} tensions : {n['ouverte']} ouvertes, "
         f"{n['en_jugement']} en jugement, {n['resolue']} résolues. Règle du greffe : une tension ne se*",
         "*résout que par l'arbitre nommé avant la résolution — on ne réécrit pas l'histoire d'une anomalie.*", ""]
    for t in d["tensions"]:
        badge = {"ouverte": "OUVERTE", "en_jugement": "⚖ EN JUGEMENT", "resolue": "RÉSOLUE"}[t["statut"]]
        L += [f"## {t['id']} — {badge} <small>(ouverte le {t['ouverte_le']})</small>", "",
              f"**{t['enonce']}**  ", f"magnitude : **{t['magnitude']}** · refs : {', '.join(t['refs'])}", "",
              "Lectures rivales :"]
        L += [f"- {l}" for l in t["lectures"]]
        L += ["", f"**Arbitre (gravé d'avance)** : {t['arbitre']}", ""]
        if t["statut"] == "resolue":
            r = t["resolution"]
            L += [f"**Résolution** ({r['date']}, {r['registre']}) : {r.get('verdict', '')} — par l'arbitre nommé.", ""]
    (ROOT / "registres/TENSIONS.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"[greffier] {len(d['tensions'])} tensions greffées -> registres/TENSIONS.md "
          f"({n['ouverte']} ouvertes, {n['en_jugement']} en jugement, {n['resolue']} résolues)")

if __name__ == "__main__":
    main()
