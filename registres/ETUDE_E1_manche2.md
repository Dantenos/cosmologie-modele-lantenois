# ÉTUDE E1 MANCHE 2 — DOUGLASS DR7 × PANTHEON+ : le deuxième juge (23/08/2026)

*Critères gelés avant exécution : `scripts/etude_E1_manche2.py` (registre `ec458a2cf766`).
Premier juge : Stopyra 2023, `ETUDE_E1_v0.md` (Δβ = +0,096 ± 0,236). Données :
`donnees/vides_douglass2023/` (CDS J/ApJS/265/7), empreintes dans `donnees/SHA256SUMS`.*

## Verdict
**UNIVERSEL — manche 2 au goulet, sur deux juges (Stopyra 2023, Douglass 2023).**
La spec mère exigeait un signal reproduit sur ≥ 2 catalogues indépendants : aucun des deux
n'en montre. Les trois algorithmes de Douglass donnent NUL, avec des signes **opposés** :

| Algorithme | partage | β_vides | β_murs | Δβ | σ | permutations p |
|---|---|---|---|---|---|---|
| VoidFinder (union de 39 735 sphères) | 228/227 | 2,912 ± 0,290 | 2,391 ± 0,250 | **+0,521 ± 0,383** (1,4σ) | 0,319 | 0,110 |
| VIDE (531, sphères R_eff) | 228/227 | 2,422 ± 0,228 | 2,820 ± 0,269 | **−0,399 ± 0,352** (1,1σ) | 0,279 | 0,150 |
| REVOLVER (518, sphères R_eff) | 228/227 | 2,535 ± 0,255 | 2,576 ± 0,250 | **−0,041 ± 0,357** (0,1σ) | 0,324 | 0,915 |

**Ce que cela réduit :** |Δβ| < 0,77 (2σ) dans l'empreinte SDSS NGC, d < 330 h⁻¹ Mpc ;
|Δβ| < 0,47 (Stopyra, vides locaux). **Ce que cela ne ferme pas :** un effet < σ_Δ ≈ 0,36.

## À dire sans l'adoucir
- VoidFinder et VIDE diffèrent de 0,92 pour un seuil de divergence gelé à 2·√(σ²+σ²) = 1,04.
  Juste en dessous : exploitable par le critère, de peu. Les deux définitions du « vide »
  (sphères creuses vs cellules de Voronoï) ne trient pas les mêmes SNe — l'environnement
  « vide » n'est pas une quantité univoque à ce niveau de précision.
- Le signe de Stopyra (+, horloge) n'est reproduit que par VoidFinder, et contredit par VIDE.
  Aucun signe n'est interprété.
- Test faible, déclaré d'avance : 455 SNe dans l'empreinte, ~228 par moitié.

## Sortie réelle, non éditée
```
[0] SNe dans l'empreinte (theta < 3.0 deg) : 455 ; z < 0,114 : 221
    VoidFinder  39735 spheres, R = 3.8-22.4, d <= 328
    VIDE          531 spheres, R = 10.0-53.1, d <= 321
    REVOLVER      518 spheres, R = 14.1-40.9, d <= 320
[VoidFinder] f : mediane=0.122 moyenne=0.139 f>0 : 447 ; partage mediane -> 228/227
    Delta_beta = +0.521 +/- 0.383 (1.36 sigma) | 200 permutations : sigma_perm = 0.319, p = 0.110 -> NUL
[VIDE] f : mediane=0.120 moyenne=0.158 f>0 : 401 ; partage mediane -> 228/227
    Delta_beta = -0.399 +/- 0.352 (1.13 sigma) | 200 permutations : sigma_perm = 0.279, p = 0.150 -> NUL
[REVOLVER] f : mediane=0.214 moyenne=0.245 f>0 : 424 ; partage mediane -> 228/227
    Delta_beta = -0.041 +/- 0.357 (0.12 sigma) | 200 permutations : sigma_perm = 0.324, p = 0.915 -> NUL
VERDICT E1 MANCHE 2 : UNIVERSEL — manche 2 au goulet, sur deux juges (Stopyra 2023, Douglass 2023)
```
Durée : 270 s.

## État du duel goulet/horloge
Manche 1 (#116, hémisphères) : universel, 1,0σ. Manche 2 (E1, deux catalogues de vides) :
universel, < 1,4σ partout, signes incohérents. **Deux manches au goulet.** L'horloge n'est
pas tuée — son discriminant est simplement hors de portée des SNe actuelles à ~0,4 près sur β.
Troisième catalogue possible : Malandrino 2026 (100 vides bayésiens). Valeur attendue : faible,
même empreinte de SNe.
