# ÉTUDE E1 v0 — VIDES × PANTHEON+ : duel goulet/horloge, manche 2 (23/08/2026)

*Critères gelés avant exécution : `scripts/etude_E1_vides.py` (registre `8f3c54a31b58`).
Spec mère : `scripts/etudes_2026.py` (gelée). Données : `donnees/SHA256SUMS`.*

## Verdict
**UNIVERSEL à cette précision — manche 2 au goulet.**
Δβ = β_vides − β_murs = **+0,096 ± 0,236 (0,41σ)**. Contrôle d'équité par 200 rotations du
catalogue : σ_rot = 0,229, p = 0,695. Le signe (+, sens de l'horloge) n'est PAS interprété.

**Ce que cela réduit :** |Δβ| < 0,47 (2σ) pour un effet d'environnement porté par les vides
à d < 135 h⁻¹ Mpc, un seul catalogue.
**Ce que cela ne ferme pas :** un effet plus fin ; un effet porté par des vides plus lointains ;
la manche sur ≥ 2 catalogues indépendants exigée par la spec mère reste à jouer (SDSS DR7
Douglass au CDS J/ApJS/265/7 ; Malandrino 2026).

## Sortie réelle, non éditée
```
SNe retenues : 1580 (z>0.01, hors calibrateurs)
[0] beta(1580 SNe, Om=0.314) = 2.516 +/- 0.124
[4] #116 rejoue : apex 553 SNe beta=2.66+/-0.18 | anti 1027 SNe beta=2.43+/-0.15 | Delta_beta = +0.24 +/- 0.23
    attendu 553/1027, +0,22+/-0,23 -> machinerie VALIDEE
[1] 150 vides, R = 10-21 h-1 Mpc, d <= 135
    f : mediane=0.000 moyenne=0.092 f>0 pour 623 SNe ; partage f>0 / f=0
[3] vides 623 SNe : beta = 2.556 +/- 0.183
    murs  957 SNe : beta = 2.460 +/- 0.150
    Delta_beta = +0.096 +/- 0.236  (0.41 sigma)
[5] 200 rotations : <Delta_beta> = -0.019, sigma_rot = 0.229, p(|null| >= |obs|) = 0.695
VERDICT E1 v0 : UNIVERSEL a cette precision — manche 2 au goulet
```
Durée : 153 s. Python 3.12.10, numpy 2.5.2, scipy 1.18.1.
*Note (audit 23/08) : 2,516 ± 0,124 est β SN-seules à Ω_m = 0,314 fixé (machinerie #116) ; 2,447 est β du fit joint SN+BAO avec Ω_m libre. Deux quantités, pas une contradiction.*

## Ce qui a été validé en chemin
- **Ligne de base rejouée sur données publiques fraîches** (`vraisemblance_reelle.py`,
  Pantheon+ GitHub + DESI DR2) : 1580 SNe, β = 2,447, Δχ² = −4,41 vs ΛCDM. Le corpus
  se reproduit hors de la machine d'origine.
- **#116 reproduit** : 553/1027, Δβ = +0,24 ± 0,23. La machinerie des sous-échantillons
  (covariance pleine restreinte, M marginalisé, Om fixé) est la même.
- **La covariance Pantheon+ ne cache pas de systématique d'empreinte** : σ_rot ≈ σ_Δ.
  Ce point manquait en #116.

## Limites déclarées avant le calcul (docstring)
1. Un seul catalogue (Stopyra 2023, 150 anti-halos, R = 10-21 h⁻¹ Mpc). Verdict « SIGNAL »
   interdit par construction.
2. Profondeur 135 h⁻¹ Mpc (z < 0,045) : pour 1300+ SNe, f ne décrit que le segment local.
3. Médiane de f nulle → partage f > 0 / f = 0 (cas prévu au critère 2).
4. SN seules, Om fixé à 0,314 : test faible, comme #116. σ(β) ≈ 0,15-0,18 par moitié.

## Suite (ordre de la spec mère)
Manche 2 complète = même pipeline sur Douglass DR7 (VoidFinder/VIDE/REVOLVER) et Malandrino
2026. Puis E4 → E3 → E2.
