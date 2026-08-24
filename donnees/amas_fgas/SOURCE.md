# Source des données f_gas — amas relaxés (Mantz et al. 2014)

## Papier

**Mantz, A. B., Allen, S. W., Morris, R. G., Rapetti, D. A., Applegate, D. E., Kelly, P. L.,
von der Linden, A., Schmidt, R. W.**,
« Cosmology and astrophysics from relaxed galaxy clusters — II. Cosmological constraints »,
*MNRAS* **440**, 2077–2098 (2014). DOI : 10.1093/mnras/stu368. arXiv : **1402.6212**.

Échantillon : **40 amas massifs, chauds (kT ≳ 5 keV), morphologiquement relaxés** (sélection
automatisée, papier I = Mantz et al. 2014a, arXiv:1502.06020 / « SPA »), observés par Chandra,
avec calibration de masse par lentillage faible (Weighing the Giants) pour un sous-échantillon.

## Fichiers

| Fichier | Origine | Contenu |
|---|---|---|
| `arxiv_1402.6212_src.tar.gz` | https://arxiv.org/e-print/1402.6212 (téléchargé le 2026-08-24, HTTP 200, 235 469 octets) | Source e-print complet (LaTeX + figures) |
| `arxiv_src/fgas_table.tex` | extrait du tarball ci-dessus | **Table 2 du papier** (`\label{tab:fgas}`) : nom, z, r2500_ref (kpc), M2500_ref (10^14 Msun), f_gas_ref dans la coquille 0,8–1,2 r2500 — 40 amas |
| `arxiv_src/fgas_cluster_table.tex` | extrait du tarball | Table 1 du papier (`\label{tab:targets}`) : coordonnées, N_H, temps d'exposition, appartenance WtG |
| `mantz2014_fgas_r2500shell.csv` | extrait par script `extraire_csv.py` (dans ce dossier) à partir de `fgas_table.tex` | Colonnes `nom, z, fgas, sigma_fgas` — 40 lignes, z ∈ [0,078 ; 1,063] |

Remarque : pas de catalogue VizieR/CDS pour ce papier (J/MNRAS/440/2077 inexistant) ; les pages
du groupe (slac.stanford.edu/~amantz) ne sont plus en ligne. Le source arXiv est donc le format
machine-réadable d'origine.

## Définition de la mesure (IMPORTANT)

- **Coquille radiale : 0,8–1,2 r2500** (coquille sphérique, PAS une sphère intégrée < r2500,
  PAS r500). r2500 = rayon où la densité moyenne = 2500 × densité critique à z de l'amas
  (~1/4 du rayon viriel).
- Valeurs `f_gas^ref` calculées pour la **cosmologie de référence** du papier : ΛCDM plate,
  h = 0,7, Ωm = 0,3 (les distances entrent via d(z)^{3/2} dans le modèle, éq. 4 du papier —
  toute analyse cosmologique doit re-échelonner par [d_ref(z)/d(z)]^{3/2}).
- Barres d'erreur : **68,3 % de confiance, incertitudes STATISTIQUES seulement**, marginalisées
  sur l'incertitude de r2500. Elles n'incluent PAS le décalage mesuré entre masses X et masses
  de lentillage ni son incertitude (paramètre de calibration K du papier, § 4.2).

## Mises en garde du papier

1. **Biais hydrostatique / calibration de masse** : les masses X sont recalibrées par lentillage
   faible (WtG). Le papier modélise K(z) = K0(1 + K1 z) avec K0 = 0,96 ± 0,09 (prior gaussien,
   d'Applegate et al.) et K1 uniforme ± 0,05. **K0 domine le budget d'erreur systématique** ;
   les σ du CSV ne le contiennent pas — à modéliser séparément dans toute chaîne cosmologique.
2. **Facteur de déplétion du gaz Υ(z) = Υ0(1 + Υ1 z)**, avec f_gas = K Υ (Ωb/Ωm) [·d^{3/2}] :
   prior **uniforme Υ0 ∈ (0,763 ; 0,932)**, centré sur **0,848** (moyenne des simulations
   refroidissement+rétroaction AGN de Battaglia et al. 2013 et Planelles et al. 2013, évaluées
   dans la coquille 0,8–1,2 r2500 ; largeur totale 20 %). Évolution : **Υ1 uniforme ∈ (−0,05 ;
   0,05)** (aucune évolution détectée dans les simulations). NB : ceci est la déplétion du GAZ
   chaud seul (pas baryonique totale) — c'est voulu : la coquille exclut le cœur, donc pas
   besoin d'ajouter la fraction stellaire.
3. **Dispersion intrinsèque** de f_gas dans la coquille : **7,4 ± 2,3 %** (log-normale),
   contrainte par les données ; à inclure en plus des σ statistiques du CSV.
4. Les redshifts des amas SPT viennent de Reichardt et al. (2013) et McDonald et al. (2013).
5. L'échantillon est sélectionné pour être relaxé : les priors de déplétion/non-thermique ne
   s'appliquent qu'à ce type d'amas ; ne pas réutiliser ces f_gas pour des amas quelconques.

## Empreintes SHA-256

```
01fa74966912dfe4e21cee8117979071dff2c95808d4a86865cbc63cad073891  arxiv_1402.6212_src.tar.gz
7255afe734e9be13d2971547f1607c343841b6efe01faaa70272b3f4cf6ca2e0  arxiv_src/fgas_table.tex
7c15251539ba6304e09006eb38c06352cf9f8807da82327df26746465b22aa46  arxiv_src/fgas_cluster_table.tex
2668b85746bcfeb3bb839b6d17964f5e882a91443f1ae75629ffd87245a72fc2  mantz2014_fgas_r2500shell.csv
```
