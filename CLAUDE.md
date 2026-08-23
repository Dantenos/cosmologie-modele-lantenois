# CLAUDE.md — projet cosmologie (constitution héritée de la campagne d'août 2026, 142 entrées au 23/08)

## Règles absolues (violées = session invalide)
1. Tout script commence par ses CRITÈRES PRÉ-ENREGISTRÉS en en-tête, écrits avant exécution.
2. Tout écart > 3σ subit un CONTRÔLE D'ÉQUITÉ avant écriture : recalculer avec les valeurs
   publiées du rival, jamais les miennes.
3. Annoncer ce qu'un calcul RÉDUIT, jamais ce qu'il ferme.
4. Avant de convertir un Δχ² en prévision : identifier de quelle VARIABLE il dépend (pas
   seulement de combien de points).
5. Énumérer ce que l'adversaire a le droit de réajuster — et le lui accorder.
6. Valeurs de substitution : les inventer dans le sens DÉFAVORABLE à la thèse défendue.
7. Garde-fous textuels insensibles aux sauts de ligne (regex, pas d'égalité stricte).
8. Toute rétractation va dans MANQUEMENTS.md (numérotée) et TRIAGE_DES_ATTAQUES.md.
9. Jamais convertir l'ambigu en victoire. Un contrôle sur deux échoué = rien n'est exploité.

## État du corpus (24/08/2026)
- Papier A (33 p.) : loi w=−β/(3Ht), β=2,42-2,60 ; cibles DR3 : β, β₁, |κ|<0,24. → arXiv.
- Papier C (8 p.) : duel CCBH + FRB (82-120 sursauts pour 3σ ; table réelle : 2,2σ, #148). → soumission prioritaire.
- Papier B (14 p.) : annexe. Feuille de contraintes (ε≲2e−4 ; x₀≲0,30 ; conversion ≥97 %).
- THEORIE_GOULET / THEORIE_HORLOGE : discriminant = universalité environnementale de w
  (1re manche hémisphères : Δβ=+0,22±0,23, universel).
- Scripts : ancres numériques en tête ; les rejouer en CI (ligne de base gardée : outils/ligne_de_base.py).
- Lancer les scripts depuis donnees/pantheon_plus/ (vraisemblance_reelle.py lit pantheon.dat dans le CWD) ; sous Windows PYTHONUTF8=1.
- Avant tout commit : python3 outils/perime.py (valeurs périmées) et outils/registre.py verify.
- Ne jamais toucher un docstring gelé (outils/registre.lock) ni les octets de outils/scelle.py ; corps seulement, et RETRACTATIONS.md via freeze --amend.

## File d'attente
[x] MCMC Planck sur β : 2,603 +0,046/−0,053 (#151 ; Cobaya complet reste)  [x] Atlas v1 : 19 modèles (#150, ATLAS.md)  [x] planck_lite_py fourni, −12,6 reproduit (#146)  [ ] AUDIT_2308.md §5 (P10, numérotation, sceau dans A)
[x] voids×Pantheon+ : UNIVERSEL sur 2 juges (#141-142)  [ ] κ(σ) BGG  [ ] κ₋Δv ≳ 25
