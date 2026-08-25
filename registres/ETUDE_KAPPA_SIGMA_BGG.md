# ÉTUDE κ(σ) BGG — le couplage dépend-il de la dispersion de vitesse de l'hôte ? (25/08/2026)

*Spec à critères pré-enregistrés `scripts/etude_kappa_sigma_bgg.py` (gelée le 25/08, `70ed033cc3b0`).
Tentative d'exécution par assemblage de données publiques (option « je localise moi-même »).
Verse dans l'affaire k3-vs-0 ; éprouve P5 (papier A).*

## Question
Si le couplage cosmologique des trous noirs (M ∝ a^k) est réel, k est une propriété du **fond**
et ne doit pas dépendre des propriétés de l'hôte. Le discriminant direct : la dispersion de
vitesse σ des galaxies les plus brillantes de groupe/amas. Universalité (CCBH + notre P5) →
dk/dln σ = 0 ; croissance environnementale → k(σ) en pente.

## Recherche de données (25/08) — le mur, déclaré
La spec gère **exige la source primaire par hôte** (règle E5 : aucun k repris d'un résumé
secondaire) et **≥ 2 échantillons σ indépendants** pour un signal. Recherche menée :

- **Farrah et al. 2023** — mesure primaire, ApJ 944 L31 (arXiv:2302.07878) + compagnon ApJ 943
  133 (arXiv:2212.06854). C'est une **lettre de 10 p.** : la mesure de k est **agrégée** (les SMBH
  d'elliptiques quiescentes croissent d'un facteur 7–20 entre 0,7 ≲ z ≲ 2,5 et z ∼ 0, à masse
  stellaire constante). **Aucune table (σ, M_BH, z) par objet**, aucun dépôt Zenodo/VizieR,
  aucun catalogue par hôte (vérifié sur l'arXiv et par recherche : rien de public).
- Catalogues de dispersion d'elliptiques publics (VizieR) : ils donnent σ, **mais pas** la mesure
  d'évolution de M_BH par strate de σ — or c'est cette évolution redshift qui **définit** k. Les
  croiser reviendrait à fabriquer un k par la relation M_BH–σ, ce qui est **circulaire** (M_BH
  dériverait de σ) et interdit par la règle E5.

## Verdict (critères gelés)
**NON EXPLOITÉ — données publiques insuffisantes.** Le test dk/dln σ n'est pas exécutable sans
la table par hôte (σ, M_BH direct, z) de l'échantillon de Farrah, qui n'est pas publiée. Ce
n'est pas un nul physique : c'est l'absence de la donnée requise. Aucun nombre inventé (règle 6),
aucun résumé secondaire promu (règle E5), aucun ambigu converti en victoire (règle 9).

**Ce qu'il faudrait pour l'exécuter** (transmis à qui a l'accès) :
- soit la table par objet de Farrah 2023 (`z, σ, M_BH` dynamique/direct, `M_*`) — à demander aux
  auteurs, ou un futur relevé (Euclid/LSST spectro + M_BH directs) ;
- déposer sous `donnees/farrah2023_sigma_mbh.csv` (empreinte dans `SHA256SUMS`), puis la spec
  gelée tourne telle quelle. Le canal `bgg_sigma` du k-tracker reste `a_verifier`.

Statut d'affaire k3-vs-0 : inchangé — le canal le plus fort reste JWST 2025 (k=3 rejeté ~11σ,
`POSTERIEUR_K_v1.md`), non répliqué ici.
