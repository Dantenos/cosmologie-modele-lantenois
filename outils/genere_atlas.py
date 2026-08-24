#!/usr/bin/env python3
"""genere_atlas v1 — le visuel de l'atlas, GÉNÉRÉ depuis atlas_leaderboard.json (24/08/2026).
CRITERES PRE-ENREGISTRES (geles) : le HTML n'est ECRIT que si le leaderboard existe, contient
exactement 19 modeles, et que ses chiffres de tete correspondent au registre (#150 : les deux
iLCDM en tete, accretion chi2 = 1419,309 +/- 0,01). Sinon REFUS — le visuel ne doit jamais
diverger du JSON, qui lui-meme n'est ecrit que par atlas_v1.py (gele) apres validation.
Zero dependance reseau dans la sortie. Usage : python3 outils/genere_atlas.py
"""
import sys, re, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAD = ROOT / "registres" / "atlas_leaderboard.json"

def main():
    if not LEAD.exists(): sys.exit("[atlas-visuel] REFUS : leaderboard absent (lancer scripts/atlas_v1.py)")
    d = json.loads(LEAD.read_text(encoding="utf-8"))
    noms = [m["nom"] for m in d["modeles"]]
    acc = next(m for m in d["modeles"] if m["nom"].startswith("ACCRETION (Gamma"))
    if not (len(d["modeles"]) == 19 and noms[0].startswith("iLCDM") and noms[1].startswith("iLCDM")
            and abs(acc["chi2"] - 1419.309) < 0.01):
        sys.exit(f"[atlas-visuel] REFUS : leaderboard inattendu ({len(d['modeles'])} modeles, tete {noms[0]!r}, acc {acc['chi2']})")
    tpl = (ROOT / "outils" / "atlas_template.html").read_text(encoding="utf-8")
    out = tpl.replace("__DATA__", json.dumps(d, ensure_ascii=False)).replace("__DATE__", d["date"])
    # bandeau de retractation : une facade ne doit jamais montrer un resultat retracte (#166)
    ret = [m for m in d["modeles"] if "RETRACTE" in m]
    if ret:
        ban = ("<div style=\"background:#3a1414;border:1px solid #c96a4a;color:#f2e2d8;"
               "padding:14px 18px;margin:0 0 10px;font:14px/1.5 Georgia,serif\">"
               "<b>&#9888; R&Eacute;TRACTATION (#166)</b> &mdash; les "
               + str(len(ret)) + " lignes <b>i&#923;CDM</b> de cet atlas sont INVALIDES : "
               "leur &chi;&sup2; a &eacute;t&eacute; &eacute;talonn&eacute; "
               "(r_d, z_*, r_*, R) avec l&rsquo;&eacute;tiquette &Omega;_m au lieu de la "
               "densit&eacute; de mati&egrave;re d&rsquo;avant recombinaison "
               "&Omega;_m&prime;. 8,62 des 9,84 unit&eacute;s d&rsquo;avance sont "
               "fabriqu&eacute;es ; le mod&egrave;le coh&eacute;rent gagne <b>+1,21</b>, "
               "derri&egrave;re l&rsquo;accr&eacute;tion et CPL. "
               "<b>Le classement ci-dessous n&rsquo;est plus le bon.</b></div>")
        out = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + ban, out, count=1)
    dest = ROOT / "visuels" / "atlas.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[atlas-visuel] ecrit : {dest.name} ({dest.stat().st_size//1024} ko) — 19 modeles, tete iLCDM, accretion 1419,309 : conformes #150")

if __name__ == "__main__":
    main()
