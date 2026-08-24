#!/usr/bin/env python3
"""perime v0 — le linter de valeurs périmées, écrit le 23/08/2026 d'après la spec de
registres/ATLAS_falsification_spec.md (règle 7 : « mode de défaillance n°1 constaté »).

PRINCIPE. Un corpus qui grandit par accrétion finit par citer des chiffres morts. Chaque
quantité publiée vit dans outils/valeurs_canoniques.json avec sa valeur courante et ses
valeurs dépréciées (regex). Ce linter greppe les documents de FAÇADE contre les dépréciées
et échoue (exit 1) si une occurrence n'est pas dans un contexte de rétractation : marque
`[historique]` sur la ligne, ou un mot de rétractation (retiré, erratum, earlier draft,
withdraw, supersédé…). Les registres historiques (MANQUEMENTS, TRIAGE, carnet,
etude_complete*) ne sont scannés qu'avec --tout : ils ont le droit de citer le passé.

CRITÈRE PRÉ-ENREGISTRÉ : v0 réussit s'il retrouve, sur le dépôt au 23/08 avant corrections,
les six occurrences non propagées relevées par l'audit (AUDIT_2308.md §3) ; il échoue s'il
produit un faux positif sur une ligne qui est elle-même une rétractation.

Usage : python3 outils/perime.py [--tout] [fichiers...]
"""
import sys, re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CV = json.loads((ROOT / "outils" / "valeurs_canoniques.json").read_text(encoding="utf-8"))
FACADE = ["README.md", "CLAUDE.md", "RETRACTATIONS.md", "REPRODUIRE.md", "registres/POUR_2027.md", "outils/README_registre.md",
          "registres/CONCLUSION.md", "registres/SYNTHESE_FINALE.md", "registres/SYNTHESE_ET_OUVERTURES.md",
          "registres/LISEZMOI_MANIFEST.md", "registres/TROIS_CHANTIERS.md", "registres/THEORIE_GOULET.md",
          "registres/THEORIE_HORLOGE.md", "registres/THEORIE_SATURATION.md", "registres/BALAYAGE_CONSEQUENCES.md",
          "registres/email_experts_brouillon.md", "registres/email_creation_particules.md",
          "registres/ETUDE_E1_v0.md", "registres/ETUDE_E1_manche2.md", "registres/ETUDE_E7.md",
          "registres/POSTERIEUR_K_v1.md", "registres/RACHAT_DES_DETTES.md",
          "papiers/papierA_fluide_source_externe.tex", "papiers/papierB_hierarchie.tex", "papiers/papierC_comparaison.tex",
          "visuels/le_role.html", "visuels/ciel_pantheon.html", "visuels/mur_retractations.html", "visuels/saga_du_bord.html", "visuels/video_explicative.html"]
HISTORIQUE = ["registres/MANQUEMENTS.md", "registres/TRIAGE_DES_ATTAQUES.md", "registres/carnet.md",
              "registres/etude_complete_v2.md", "registres/etude_complete.txt", "registres/revue_litterature_annexeA.md",
              "registres/etude_univers_trou_noir.md", "registres/PLAN_ETUDE_RIVAUX.md", "registres/ATLAS_falsification_spec.md",
              "registres/PIPELINE_CLAUDE_CODE.md", "registres/INTERJONCTIONS.md", "registres/ETUDE_FENETRE_VIABILITE_v0.md",
              "registres/ETUDE_TAXONOMIE_COSMO_v0.md", "registres/AUDIT_2308.md",
              "papiers/parent_bh_dark_energy.tex", "papiers/fenetre_viabilite.tex", "papiers/fenetre_viabilite_v1.tex",
              "papiers/fenetre_viabilite_v2.tex", "papiers/taxonomie_cosmo_v1.tex"]
# une ligne qui est elle-même une rétractation a le droit de citer la valeur morte
CONTEXTE = re.compile(r"\[historique\]|retir|rétract|retract|withdraw|erratum|ancien|earlier (draft|figure|version|statement)"
                      r"|first (called|reading|version|draft)|supersed|supersédé|superséd|old table|was itself|\bfaux\b|miscalibrated"
                      r"|once listed|nominally|not the plausible|périm|perim|v1 faux|Horloge v1|à la naissance|#111|#139|#52"
                      r"|déprécié|deprecated|corrigé|corrected|correction|refait|RETIRÉ|\bfausse\b|ne tient pas|n'est pas une prédiction", re.I)

def scan(files):
    fautes = []
    for rel in files:
        p = ROOT / rel
        if not p.exists(): continue
        for i, ligne in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if rel.endswith(".html") and len(ligne) > 1500: continue   # tableaux de données inlinés
            if CONTEXTE.search(ligne): continue
            for q in CV["quantites"]:
                for v in q["valeurs_depreciees"]:
                    m = re.search(v, ligne)
                    if m:
                        fautes.append(f"{rel}:{i} : « {m.group(0)} » périmé — {q['nom']} ; courant : {q['valeur_courante']} ({q['source']})")
    return fautes

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    files = a or (FACADE + HISTORIQUE if "--tout" in sys.argv else FACADE)
    f = scan(files)
    print("\n".join(f) if f else "[perime] aucune valeur périmée hors contexte de rétractation")
    print(f"[perime] {len(f)} occurrence(s) sur {len(files)} fichier(s)")
    sys.exit(1 if f else 0)
