#!/usr/bin/env python3
"""ATLAS v2 — LE PALMARES CORRIGE, CONSOLIDE ET ANNOTE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI. Le palmares de l'atlas v1 (#150) porte encore, en fichier, deux lignes iLCDM
RETRACTEES (#166, #167) avec un simple bandeau, et il ignore trois faits etablis depuis :
les minima de bord (#175), le classement du banc a un parametre (#177), et les valeurs
coherentes des deux lignes fautives. Un palmares qui affiche un chiffre retracte est une
facade fausse, meme avec un avertissement au-dessus.

CE QUE CE SCRIPT N'EST PAS. Ce n'est PAS un re-calcul des 19 modeles : atlas_v1.py est gele
avec ses ancres, et le rejouer redonnerait les memes valeurs fautives sur les deux lignes en
cause. C'est une CONSOLIDATION : elle prend les valeurs deja etablies et VALIDEES par des
scripts geles, les corrige la ou une retractation l'exige, les annote la ou un domaine est
mutile, et y adjoint les modeles du banc. Chaque nombre importe ici a une provenance nommee.

PROVENANCES (aucune valeur n'est inventee ici) :
  - les 19 chi2 de base : registres/atlas_leaderboard.json (#150, atlas_v1.py gele) ;
  - iLCDM Q~rho_de corrige : 1423,874 (#166, degenerescence_ilcdm_v4.py gele) ;
  - iLCDM Q~rho_dm corrige : 1425,086 (#167, etalonnage_dm.py gele) ;
  - drapeaux de domaine : #175 (audit_domaines_v2.py gele) ;
  - six lois a un parametre : #177 (banc_un_parametre_v2.py gele).

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  1. Le leaderboard source doit contenir EXACTEMENT 19 modeles.
  2. Les DEUX lignes iLCDM doivent y porter le drapeau RETRACTE — sinon la retractation
     #166/#167 n'a pas ete appliquee au fichier, et consolider serait blanchir.
  3. LCDM doit y valoir 1425,086 et l'accretion 1419,309 (a 1e-3) : ce sont les deux
     ancres qui rattachent ce palmares a tout le reste du corpus.
  4. Le chi2 corrige de iLCDM 'dm' doit valoir EXACTEMENT celui de LCDM (le #167 a montre
     que son eps prefere tombe a zero, ou le modele EST LCDM). Si l'ecart depasse 1e-3,
     l'un des deux resultats a bouge et il faut le savoir avant de publier.

--- CRITERES (exhaustifs) ---
  1. CLASSEMENT par AIC = chi2 + 2k. Chaque ligne porte sa provenance et, le cas echeant,
     la mention RETRACTE-CORRIGE ou MINIMUM DE BORD.
  2. UNE LIGNE A MINIMUM DE BORD N'EST PAS CLASSEE COMME LES AUTRES : son chi2 est affiche
     mais suivi de la mention « bord », et le texte rappelle qu'il ne se lit pas comme un
     minimum. Trois familles sont concernees (#175) : iLCDM 'dm', JPS, thawing.
  3. LE RANG DE NOTRE MODELE est ecrit tel quel. S'il n'est pas premier, les modeles qui le
     battent sont NOMMES dans la premiere phrase du fichier genere.
  4. Le fichier genere porte en tete la liste des retractations qui l'ont produit.
Regle 3 : cette consolidation REDUIT les affirmations du palmares ; elle n'en ajoute aucune.
Usage : python3 scripts/atlas_v2.py   (depuis la racine)
"""
import sys, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAD = ROOT / "registres" / "atlas_leaderboard.json"

CORRIGES = {"de": (1423.874, "#166", "degenerescence_ilcdm_v4.py"),
            "dm": (1425.086, "#167", "etalonnage_dm.py")}
BORD = {"iLCDM Q=eps H rho_dm": "#175", "JPS": "#175", "thawing": "#175"}
BANC = [("K4 (Kessler et al. 2025, Eq. 8)", 4, 1415.398, "w0 = -0,9916", "#177"),
        ("K3 (Kessler et al. 2025, Eq. 7)", 4, 1418.426, "w0 = -0,9081", "#177"),
        ("SR w0/sqrt(a) (Borghetto et al. 2026)", 4, 1419.361, "w0 = -0,8844", "#177"),
        ("K1 (Kessler et al. 2025, Eq. 5)", 4, 1421.742, "w0 = -0,8362", "#177"),
        ("F83 w0 exp(1-a) (Borghetto et al. 2026)", 4, 1425.199, "w0 = -0,8078", "#177"),
        ("K2 (Kessler et al. 2025, Eq. 6)", 4, 1438.116, "w0 = -0,7438", "#177")]
NOTRE = "ACCRETION (Gamma"


def norm(s):
    return s.lower().replace("λ", "l").replace("Λ", "l")


if __name__ == "__main__":
    print("ATLAS v2 — consolidation du palmares (criteres geles)\n")
    d = json.loads(LEAD.read_text(encoding="utf-8"))
    mods = d["modeles"] if isinstance(d, dict) and "modeles" in d else d
    if len(mods) != 19:
        sys.exit(f"  REFUS verif 1 : {len(mods)} modeles au lieu de 19")
    ilc = [m for m in mods if "ilcdm" in norm(m["nom"])]
    if len(ilc) != 2 or not all("RETRACTE" in m for m in ilc):
        sys.exit("  REFUS verif 2 : les lignes iLCDM ne portent pas le drapeau RETRACTE")
    par = {m["nom"]: m for m in mods}
    lcdm = next(m for m in mods if m["nom"] == "LCDM")
    acc = next(m for m in mods if m["nom"].startswith(NOTRE))
    if abs(lcdm["chi2"] - 1425.086) > 1e-3 or abs(acc["chi2"] - 1419.309) > 1e-3:
        sys.exit(f"  REFUS verif 3 : ancres {lcdm['chi2']} / {acc['chi2']}")
    if abs(CORRIGES["dm"][0] - lcdm["chi2"]) > 1e-3:
        sys.exit(f"  REFUS verif 4 : iLCDM 'dm' corrige {CORRIGES['dm'][0]} != LCDM "
                 f"{lcdm['chi2']}")
    print(f"  validations : 19 modeles, 2 lignes retractees, ancres LCDM {lcdm['chi2']:.3f} "
          f"et accretion {acc['chi2']:.3f} -> OK\n")

    table = []
    for m in mods:
        nom, k, c = m["nom"], m["k"], m["chi2"]
        note, src = "", "#150"
        if "ilcdm" in norm(nom):
            cle = "de" if "rho_de" in nom else "dm"
            c, src, out = CORRIGES[cle][0], CORRIGES[cle][1], CORRIGES[cle][2]
            note = f"RETRACTE-CORRIGE ({src}, {out})"
        for b in BORD:
            if norm(b) in norm(nom):
                note = (note + " · " if note else "") + "MINIMUM DE BORD (#175)"
        table.append(dict(nom=nom, k=k, chi2=round(float(c), 3), note=note, src=src))
    for nom, k, c, p, src in BANC:
        table.append(dict(nom=nom, k=k, chi2=c, note=f"banc a un parametre ({p})", src=src))

    table.sort(key=lambda t: t["chi2"] + 2 * t["k"])
    rang = 1 + next(i for i, t in enumerate(table) if t["nom"].startswith(NOTRE))
    devant = [t["nom"] for t in table[:rang - 1]]

    lignes = []
    lignes.append("# ATLAS v2 — le palmares corrige\n")
    lignes.append("> Genere par `scripts/atlas_v2.py` (gele). **Ce fichier remplace le "
                  "palmares de l'atlas v1 (#150)**, qui portait deux lignes retractees.\n")
    lignes.append("> **Retractations appliquees :** #166 (iLCDM Q∼ρ_de : l'avance de "
                  "+9,84 etait a 8,62 un artefact d'etalonnage — chi2 corrige 1423,874) · "
                  "#167 (iLCDM Q∼ρ_dm : s'effondre exactement sur LCDM, gain 0,000).\n")
    lignes.append("> **Annotations :** #175 (minima de bord) · #177 (six lois a un "
                  "parametre de la litterature 2025-2026, meme pipeline, memes donnees).\n")
    if rang == 1:
        lignes.append("\n**Notre loi (accretion) est premiere a l'AIC.**\n")
    else:
        lignes.append(f"\n**Notre loi (accretion) est {rang}e a l'AIC. La devancent : "
                      f"{', '.join(devant)}.**\n")
    lignes.append("\n| rang | modele | k | chi2 | AIC | provenance / note |")
    lignes.append("|---|---|---|---|---|---|")
    for i, t in enumerate(table, 1):
        gras = "**" if t["nom"].startswith(NOTRE) else ""
        lignes.append(f"| {i} | {gras}{t['nom']}{gras} | {t['k']} | {t['chi2']:.3f} | "
                      f"{t['chi2'] + 2*t['k']:.3f} | {t['note'] or t['src']} |")
    lignes.append("\n**Lecture.** Une ligne marquee MINIMUM DE BORD affiche un chi2 qui "
                  "**ne se lit pas comme un minimum** : une partie de son domaine est "
                  "inaccessible (le fond y est rejete) ou son optimum tombe sur la borne "
                  "du prior. Trois familles sont dans ce cas (#175).\n")
    lignes.append("**Ce que ce palmares ne dit pas.** Il classe des ajustements sur une "
                  "seule vraisemblance (BAO DR2 + theta_* + Pantheon+, N = 1597). Il ne dit "
                  "rien des perturbations, rien de la physique, et rien de la robustesse aux "
                  "systematiques de calibration des supernovae — dont #170 montre qu'elles "
                  "deplacent nos gains de 10 a 17 % a elles seules.\n")
    out = ROOT / "registres" / "ATLAS_V2.md"
    out.write_text("\n".join(lignes) + "\n", encoding="utf-8", newline="\n")

    d2 = dict(source="scripts/atlas_v2.py", remplace="atlas_leaderboard.json (#150)",
              retractations=["#166", "#167"], annotations=["#175", "#177"],
              rang_accretion=rang, modeles=table)
    (ROOT / "registres" / "atlas_v2_leaderboard.json").write_text(
        json.dumps(d2, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    print(f"  ecrit : ATLAS_V2.md et atlas_v2_leaderboard.json ({len(table)} lignes)")
    print(f"  notre loi : rang {rang} sur {len(table)}"
          + (f" — devancee par {', '.join(devant)}" if devant else " — premiere"))
    for t in table[:6]:
        print(f"    {t['chi2'] + 2*t['k']:9.3f}  {t['nom'][:44]:<44s} {t['note'][:28]}")
