# LE GRAND LIVRE — la comptabilité baryonique (généré par `outils/ledger.py`, ne pas éditer)

*2026-08-24 — le fond ne sépare pas les modèles sourcés (#139) ; ce qu'ils consomment laisse un trou dans un budget.*
*Hypothèse déclarée : (i) consommation uniforme en environnement — si halo blinde (ii), R2 nulle et non falsifiante, seul R1 porte.*

| rangée | validation | Δχ²(CCBH, s(z)) | note |
|---|---|---|---|
| R1 — FRB (69 réels) | f_d = 0.905 | **+4.71** | machinerie E3 v1 gelée |
| R2 — amas (40 f_gas Mantz 2014) | χ²/40 = 0.96 | **+9.48** dont pente +0.70 | priors Mantz (K, K₁, Υ₀, Υ₁) profilés ; d(z) recalculé par modèle |
| R3 — ω_b BBN/CMB | 2.9σ (Cooke) / 0.3σ (Schöneberg) | — | déclarative : nul modèle ne consomme avant la recombinaison |

**Total CCBH : Δχ²_ledger = +14.19.** Tous les autres modèles de l'atlas : s(z) = 1, bilan neutre
(échanges sombres iΛCDM : rangée matière sombre en v2). Colonne fusionnée dans `atlas_leaderboard.json`.

Sources : Mantz+14 (1402.6212, éq. 2, Table 3) ; Applegate+14/16 ; Battaglia+13, Planelles+13 ;
Cooke+18 (1710.11129) ; Schöneberg 24 (2401.15054) ; Planck 18 VI ; Connor+25. Données : `donnees/amas_fgas/SOURCE.md`.
