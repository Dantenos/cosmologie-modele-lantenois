# ÉTUDE κ₋Δv — le couplage dépend-il de la PROFONDEUR de vide ? (25/08/2026)

*Extension « profondeur » de E1. Script à critères pré-enregistrés `scripts/etude_kappa_deltav.py`
(gelé le 25/08 AVANT exécution, `f6cc47899ee1` ; docstring inchangé au run). Machinerie E1
réutilisée telle quelle (chargement 1580 SNe, géométrie des cordes, `fit_beta`, `delta_beta`,
contrôle par 200 rotations). Verse dans l'affaire Audience W-universel.*

## Question
E1 partage les SNe par la **fraction** de ligne de visée en vide. Ici on trie par la
**profondeur** Δv (contraste de densité central du catalogue). Lecture horloge : les SNe vues à
travers des vides plus **profonds** donnent un w plus négatif → β/k_eff plus grand →
Δβ = β_profond − β_reste > 0. Lecture goulet/CCBH : universalité stricte, Δβ = 0.

## Données (déjà dans le dépôt, empreintes `donnees/SHA256SUMS`)
- Pantheon+ (1580 SNe, coupures du corpus), positions RA/DEC.
- Anti-halos Stopyra et al. 2023 (Zenodo 10160612), `combined_catalogue_properties.csv`, colonne
  **« Central Density Contrast »** = Δv (150 vides, Δv ∈ [−0,91 ; −0,75]).
- **Un seul catalogue** ici → un SIGNAL est impossible par la spec mère (≥ 2 juges) ; au mieux
  un excès candidat en attente du 2ᵉ catalogue (DESIVAST/Douglass).

## Résultat (rapporté tel quel, favorable ou non — règle 3)
| étape | valeur |
|---|---|
| [0] β(1580 SNe, Ω_m=0,314) | 2,516 ± 0,124 (dans [2,2 ; 2,8] ✓) |
| [4] validation #116 | 553 SNe apex, Δβ = +0,24 ± 0,23 → **machinerie VALIDÉE** |
| [1] seuil de profondeur | P25 du catalogue = **Δv ≤ −0,880** |
| [2] bin profond | **175 SNe** (≥ 25 ✓ ; 623 SNe traversent ≥ 1 vide) |
| [3] β profond / reste | 2,563 ± 0,314 / 2,480 ± 0,128 |
| **[3] Δβ = β_profond − β_reste** | **+0,083 ± 0,340 (0,25σ)** |
| [5] contrôle d'équité (200 rotations) | ⟨Δβ⟩=−0,014, σ_rot=0,300, p=0,800 |

## Verdict (critères gelés)
**UNIVERSEL à cette précision — manche PROFONDEUR au goulet**, comme la manche fraction (E1,
#141-142). Δβ compatible avec zéro (0,25σ), p_rot = 0,80, σ_rot < 2·σ_Δ (pas de systématique de
ciel non traitée).

- **Ce que cela RÉDUIT** : l'amplitude d'un effet de profondeur de vide sur β, à |Δβ| < 0,68
  (2σ) sur un catalogue, d < 135 h⁻¹ Mpc.
- **Ce que cela ne FERME PAS** : un gradient plus fin, ou porté par des vides plus profonds /
  plus lointains ; et le verdict reste sous réserve du 2ᵉ juge (spec mère).

Reproduire : `PYTHONUTF8=1 python scripts/etude_kappa_deltav.py` (depuis la racine).
