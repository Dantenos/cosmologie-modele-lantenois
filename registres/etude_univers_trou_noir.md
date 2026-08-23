# L'énergie noire comme signature d'accrétion d'un trou noir parent : un modèle falsifiable

**Étude exploratoire — É. Lantenois, avec l'assistance de Claude (Anthropic)**
**Version 1.0 — 14 août 2026**

---

## Résumé

Nous examinons l'hypothèse selon laquelle notre univers observable est l'intérieur d'un trou noir formé dans un univers parent (cosmologie de rebond, cadre Einstein-Cartan de Popławski). Nous en dérivons une conséquence testable inédite : si le trou noir parent continue d'accréter de la matière, cette masse-énergie apparaît de l'intérieur comme une composante d'énergie sombre dont l'équation d'état est entièrement déterminée par l'histoire d'accrétion, **w(z) = -(1/3) · [dln M_acc/dln t] / (H(z)·t(z))**. Trois tests d'ordre de grandeur sont menés : (i) la coïncidence de Schwarzschild (rapport R_s/R_obs ≈ 10) ; (ii) la compatibilité du taux d'accrétion requis avec la limite d'Eddington du parent (0,6 % de la limite aujourd'hui, < 1 % sur toute l'histoire) ; (iii) la confrontation aux indications DESI DR2 d'une énergie noire évolutive. Un ajustement à un paramètre (M_acc ∝ t^β, β = 2,39 ± 0,13) reproduit les trois signatures qualitatives de DESI DR2 — w fantôme dans le passé, w > -1 aujourd'hui, wₐ < 0 — et surpasse ΛCDM sur les pseudo-données (χ²/dof = 3,6/5 contre 15,6/6). La variante Bondi à zéro paramètre libre reproduit le taux d'accrétion actuel à 10 % près mais prédit le mauvais sens d'évolution de w et est défavorisée. Le modèle produit quatre prédictions falsifiables et un protocole de mise à jour est fourni (script `fit_accretion_de.py`) pour confronter la forme rigide de w(z) aux reconstructions futures (DESI DR3, Euclid, LSST).

**Avertissement.** Ceci est une étude d'ordres de grandeur menée en dehors du cadre académique, sans relecture par des pairs. Elle vise à formuler des questions calculables, pas à revendiquer un résultat.

---

## 1. Introduction

### 1.1 Contexte

La coïncidence est connue depuis Pathria (1972) : la densité moyenne de l'univers observable est de l'ordre de la densité qu'aurait un trou noir de même rayon. La cosmologie de rebond de Popławski (2010–2016) donne un cadre dynamique à cette observation : dans la théorie d'Einstein-Cartan (relativité générale + torsion de l'espace-temps, couplée au spin des fermions), l'effondrement d'une étoile massive ne produit pas de singularité mais un rebond — qui, vu de l'intérieur, présente les caractéristiques d'un Big Bang, y compris une phase d'expansion rapide analogue à l'inflation.

Ce cadre laisse toutefois un problème majeur sans réponse quantitative : **l'énergie noire**. Pourquoi l'expansion accélère-t-elle, et pourquoi la densité d'énergie noire semble-t-elle constante (ou presque) alors que l'espace s'étend ?

### 1.2 L'hypothèse examinée

Si notre univers est l'intérieur d'un trou noir, celui-ci vit dans un univers parent et peut continuer d'**accréter de la matière**. Vue de l'intérieur, cette masse-énergie entrante constitue un apport « venant de nulle part », que nous supposons réparti uniformément (hypothèse H3, §2). Nous posons la question : *cet apport peut-il rendre compte de l'énergie noire observée — en quantité ET en évolution temporelle ?*

L'actualité observationnelle rend la question urgente : les analyses DESI DR2 combinées au CMB et aux supernovae indiquent une déviation d'environ 3σ par rapport à ΛCDM, avec une préférence pour le quadrant (w₀ > -1, wₐ < 0) — une équation d'état fantôme dans le passé transitionnant vers w > -1 aujourd'hui (DESI Collaboration, arXiv:2503.14743). La préférence atteint 4,2σ dans certaines combinaisons (DESI+CMB+DES-Y5). Elle n'atteint pas le seuil de découverte de 5σ et reste débattue (le fit à deux paramètres supplémentaires est mécaniquement avantagé ; voir Siegel 2025 pour une lecture critique), mais elle définit précisément la cible que tout modèle alternatif doit viser.

---

## 2. Cadre théorique et hypothèses

Le modèle repose sur quatre hypothèses explicites. Chacune est un point de rupture possible.

- **H1 (rebond).** L'univers observable est l'intérieur d'un trou noir de masse M_p dans un univers parent ; le Big Bang correspond au rebond Einstein-Cartan de l'effondrement initial, qui a apporté la masse de matière M_m.
- **H2 (accrétion continue).** Le parent accrète ensuite au taux Ṁ(t) ; la masse totale du parent est M_p(t) = M_m + M_acc(t).
- **H3 (répartition uniforme).** Vue de l'intérieur, la masse-énergie accrétée est répartie de façon homogène et isotrope, se comportant comme un fluide parfait de densité ρ_de(t) = M_acc(t)/V(t). *C'est l'hypothèse la plus fragile du modèle : rien ne garantit a priori que l'apport traversant l'horizon se thermalise uniformément plutôt que de rester localisé.*
- **H4 (correspondance temporelle).** Le temps propre pertinent pour l'histoire d'accrétion et le temps cosmologique intérieur s'écoulent à des rythmes proportionnels. *À travers un horizon, cette correspondance est précisément ce que la relativité générale classique ne définit pas ; elle doit être justifiée par la dynamique du rebond (Einstein-Cartan) et constitue la principale dette théorique du modèle.*

### 2.1 Dérivation de l'équation d'état effective

Pour un fluide dont l'énergie totale dans le volume comobile évolue par injection, la conservation modifiée s'écrit d(ρV)/dt = Ṁ(t), d'où :

ρ_de(t) = M_acc(t) / V(t)

L'équation d'état effective d'un fluide de densité ρ(a) est w_eff = -1 - (1/3)·dln ρ/dln a. Avec dln ρ/dln a = dln M_acc/dln a - 3 et dln a = H dt :

> **w(z) = -(1/3) · [dln M_acc / dln t] / (H(z) · t(z))**   (Équation 1)

C'est l'équation centrale de l'étude. Elle est **rigide** : une fois l'histoire d'accrétion M_acc(t) spécifiée, la fonction w(z) est entièrement déterminée — aucune liberté de forme, contrairement à la paramétrisation CPL w(a) = w₀ + wₐ(1-a) qui est une droite ajustable.

Trois propriétés structurelles en découlent immédiatement :

1. **Régime fantôme naturel.** En ère de matière, H·t = 2/3 ; donc w < -1 dès que dln M_acc/dln t > 2. Le modèle produit du « phantom » sans champ scalaire exotique ni violation ad hoc des conditions d'énergie internes : l'énergie entre depuis l'extérieur.
2. **Affaiblissement structurel.** H·t croît avec le temps (2/3 en ère de matière → ∞ en ère de Sitter). À histoire d'accrétion en loi de puissance, w remonte donc mécaniquement vers 0 : l'affaiblissement de l'énergie noire n'est pas ajusté, il est prédit.
3. **Croisement fantôme.** Le passage w < -1 → w > -1 (le « phantom crossing » suggéré par DESI, notoirement difficile à obtenir avec un unique champ scalaire) est automatique.

---

## 3. Tests d'ordre de grandeur

Paramètres : H₀ = 67,7 km/s/Mpc, Ω_m = 0,315, Ω_Λ = 0,685, R_obs = 4,40×10²⁶ m, t₀ = 13,8 Ga. Masse-énergie totale de l'univers observable : M_p = 3,09×10⁵⁴ kg (1,6×10²⁴ M_☉), dont M_m = 9,7×10⁵³ kg de matière et M_de = 2,1×10⁵⁴ kg d'énergie noire.

### 3.1 Test 1 — Coïncidence de Schwarzschild

R_s = 2GM_p/c² = 4,59×10²⁷ m, contre R_obs = 4,40×10²⁶ m : **rapport ≈ 10**. La condition dimensionnelle « être à l'intérieur » (R_obs < R_s) est satisfaite avec un ordre de grandeur de marge. Statut : cohérence nécessaire, non suffisante (la coïncidence découle en partie de la platitude, ρ ≈ ρ_c).

### 3.2 Test 2 — Budget énergétique et limite d'Eddington

Maintenir ρ_de constante pendant l'expansion exige un taux d'injection Ṁ_requis = ρ_Λ · 4πR²·(dR/dt) ≈ **1,4×10³⁷ kg/s** (≈ 7×10⁶ M_☉/s). La limite d'Eddington du parent (ε = 0,1) est Ṁ_Edd ≈ 2,2×10³⁹ kg/s.

> **Ṁ_requis / Ṁ_Edd ≈ 0,006.**

Le régime requis représente 0,6 % de la limite d'Eddington aujourd'hui, et reste inférieur à 1 % sur toute l'histoire (0,24 % à t₀/10). Le parent n'a pas besoin d'un régime catastrophique : un grignotage sub-Eddington ordinaire, typique des trous noirs supermassifs réels, suffit. **Le test énergétique est passé.** (Si le ratio était sorti à 10⁶, le modèle était mort ici.)

### 3.3 Test 3 — Confrontation à DESI DR2 (variante loi de puissance)

Variante minimale : M_acc(t) ∝ t^β, un seul paramètre libre. L'Équation 1 donne alors w(z) = -(β/3)/(H·t). Ajustement sur pseudo-données CPL représentatives de DESI DR2+CMB+SN (w₀ = -0,70, wₐ = -1,0, incertitudes indicatives) :

| Modèle | Paramètres libres | χ²/dof | w₀ | wₐ |
|---|---|---|---|---|
| **Accrétion, loi de puissance** | 1 (β = 2,39 ± 0,13) | **3,6 / 5** | -0,84 | -0,49 |
| ΛCDM (w = -1) | 0 | 15,6 / 6 | -1 | 0 |
| Accrétion, Bondi (§3.4) | 0 | 60,2 / 6 | -1,11 | +1,90 |

Les trois signatures qualitatives de DESI DR2 sont reproduites : w(z=2,3) ≈ -1,1 (fantôme passé), w₀ > -1 (affaibli aujourd'hui), wₐ < 0. La magnitude de wₐ sort à environ la moitié de la valeur CPL centrale — écart d'un facteur 2, notable mais non rédhibitoire pour un modèle à un paramètre, et en partie artefact de la projection d'une forme courbée sur une paramétrisation linéaire.

### 3.4 Test 4 — Mécanisme physique de l'accrétion (branche A)

Quelle physique produit M_acc ∝ t^~2,4 ? Le candidat naturel est l'**accrétion de Bondi**, Ṁ = 4πG²M²ρ_amb/c_s³ ∝ M², dont la solution M(t) = M_m/(1 - A·M_m·t) est entièrement fixée par les conditions aux limites cosmologiques (M(0) = M_m, M(t₀) = M_p) : zéro paramètre libre.

Résultats :
- **Taux actuel : Ṁ_Bondi(t₀) = 1,54×10³⁷ kg/s, soit 1,10× le taux requis par l'énergie noire.** Une cohérence à 10 % sans paramètre ajusté — le résultat le plus frappant de l'étude, à tempérer : la masse totale accrétée étant imposée par les conditions aux limites, seul le *profil temporel* (et donc le taux instantané) est réellement prédit.
- **Sous-Eddington partout** : Ṁ/Ṁ_Edd croît de 0,24 % à 0,7 % entre t₀/10 et t₀.
- **Mais la forme w(z) échoue.** L'accrétion de Bondi *accélère* (β_eff croît de 1,2 à 3,2 entre 0,25 t₀ et t₀), ce qui fait *descendre* w récemment : le modèle Bondi prédit wₐ > 0, à l'opposé de la tendance DESI (χ²/dof = 60,2/6, pire que ΛCDM). **La variante Bondi pure est défavorisée.**
- Corollaire dramatique : la solution Bondi diverge (runaway) à 1,46 t₀, soit dans ≈ 6 Ga. Physiquement, l'accrétion saturerait avant (déplétion de l'environnement, limite d'Eddington), ce qui ramène précisément au comportement décélérant requis par DESI.

**Synthèse des branches.** Les données exigent une accrétion dont la croissance *décélère* (β passant sous ~2,4) : environnement du parent en déplétion, fin d'une phase de fusion, ou saturation Eddington locale — scénarios standards de l'astrophysique des trous noirs supermassifs. Le désaccord Bondi n'est donc pas fatal au cadre : il sélectionne la classe d'histoires d'accrétion admissibles, ce qui est exactement le rôle d'un test.

---

## 4. Prédictions falsifiables

- **P1 — Forme rigide de w(z).** Le modèle impose w(z) = -(β/3)/(H·t), une courbe spécifique non linéaire en (1-a). Toute reconstruction non paramétrique de w(z) (DESI DR3, Euclid, LSST) qui s'écarte significativement de cette famille à un paramètre falsifie la variante loi de puissance. Test opérationnel : χ² du modèle contre χ² de ΛCDM et de CPL sur les mêmes données (script fourni).
- **P2 — Poursuite de l'affaiblissement.** w(z) doit continuer de croître vers 0 aux bas redshifts futurs, sans retour vers -1. Une stabilisation confirmée à w = -1 exactement (ΛCDM à 5σ) falsifie le modèle.
- **P3 — Pas de champ scalaire.** L'énergie noire de ce modèle n'a pas de perturbations propres de type quintessence ; les contraintes sur la vitesse du son effective de l'énergie noire (c_s² ≠ 1) sont un discriminant, à quantifier dans une version 2.
- **P4 — Corrélat de torsion.** Le cadre parent (Einstein-Cartan) prédit indépendamment des signatures de torsion : asymétrie statistique du sens de rotation des galaxies (indications JWST débattues, biais d'observation possible lié à notre propre mouvement) et empreintes dans les modes B primordiaux. Le modèle d'accrétion hérite de ces tests.

---

## 5. Limites et dettes théoriques

1. **H4 (temps).** La correspondance des horloges parent/intérieur est posée, non dérivée. C'est la faiblesse centrale : tout le budget énergétique (§3.2) en dépend. Travail requis : dérivation dans la métrique de rebond Einstein-Cartan.
2. **H3 (uniformité).** La thermalisation uniforme de la masse accrétée est postulée. Une alternative (apport localisé « aux bords ») donnerait une phénoménologie différente, peut-être anisotrope — ce qui serait d'ailleurs testable (anomalies d'isotropie du CMB).
3. **Fond approximé.** Le calcul de w(z) utilise un fond ΛCDM pour a(t) ; une version auto-cohérente (rétroaction de w(z) sur H(z)) est nécessaire avant toute comparaison à des chaînes MCMC réelles. Effet attendu de second ordre, à vérifier.
4. **Pseudo-données.** Le fit du §3.3 utilise des points dérivés de la paramétrisation CPL publiée, pas les chaînes DESI publiques. La priorité de la version 2 est d'injecter les vraies données (protocole §6).
5. **Signal à 3–4σ.** L'énergie noire évolutive elle-même n'est pas établie ; si DESI DR3 la résorbe, le modèle perd sa motivation observationnelle principale (mais pas sa cohérence énergétique, §3.2).
6. **Degré de nouveauté.** La piste « énergie noire par accrétion du parent » est évoquée qualitativement dans la littérature de black hole cosmology ; à notre connaissance, la dérivation de l'Équation 1 et sa confrontation quantitative à DESI DR2 ne sont pas publiées. Une revue de littérature systématique (arXiv : Popławski 2016–2026, « dark energy black hole cosmology ») est requise avant toute rédaction formelle.

---

## 6. Protocole de mise à jour (paramétrage des nouvelles données)

Le script compagnon **`fit_accretion_de.py`** implémente l'Équation 1 et le pipeline de test. Usage :

```bash
# Test intégré (pseudo-données DESI DR2) :
python3 fit_accretion_de.py

# Nouvelles données — CSV à trois colonnes z,w,sigma_w :
python3 fit_accretion_de.py mesures_wz.csv
```

À chaque publication pertinente (DESI DR3 attendu ~2026–2027, Euclid, LSST) :

1. **Si la publication donne une reconstruction w(z)** (binned ou gaussian process) : extraire les points (z, w, σ_w) en CSV, lancer le script. Lire le verdict : le modèle survit si χ²/dof(powerlaw) ≲ χ²/dof(ΛCDM) ; il est falsifié si l'écart de forme est significatif.
2. **Si la publication ne donne que (w₀, wₐ)** : comparer aux projections du modèle via `ModeleAccretion.w0_wa()` ; noter que la projection CPL d'une courbe non linéaire introduit un biais (documenté §3.3).
3. **Journal de bord.** Consigner chaque confrontation (date, dataset, β ajusté, χ², verdict) — la *stabilité de β* d'un dataset à l'autre est elle-même un test : si β dérive significativement entre datasets, la forme rigide est en difficulté.
4. **Extensions prévues** (version 2) : fond auto-cohérent, variante « Bondi saturé » (Bondi + coupure Eddington/déplétion, 1 paramètre), vraisemblance sur chaînes MCMC publiques plutôt que pseudo-points.

---

## 7. Conclusion

L'hypothèse « notre univers est l'intérieur d'un trou noir accrétant » a été transformée en un modèle à une équation (Équation 1) et un paramètre, confronté à trois tests quantitatifs. Elle passe le test énergétique (0,6 % d'Eddington), reproduit les trois signatures qualitatives des indications DESI DR2 avec un paramètre de moins que la paramétrisation standard, et sa variante la plus contrainte (Bondi) est déjà falsifiée dans sa forme pure — preuve que le cadre est réfutable, donc scientifique au sens de Popper. Les dettes théoriques (correspondance temporelle H4, uniformité H3) sont identifiées et localisées. Le modèle est désormais en position d'attente de données : DESI DR3 et Euclid trancheront si la forme rigide w(z) = -(β/3)/(H·t) survit.

Rien ici ne « prouve » que nous vivons dans un trou noir. Mais la question est passée du statut de vertige métaphysique à celui d'équation qui peut perdre — et c'est le seul chemin connu vers une démonstration.

---

## Références

- Pathria, R. K. (1972). *The Universe as a Black Hole*. Nature 240, 298.
- Popławski, N. J. (2010). *Cosmology with torsion: An alternative to cosmic inflation*. Phys. Lett. B 694, 181. (arXiv:1007.0587)
- Popławski, N. J. (2016). *Universe in a black hole in Einstein–Cartan gravity*. ApJ 832, 96. (arXiv:1410.3881)
- Smolin, L. (1997). *The Life of the Cosmos*. Oxford University Press. (sélection naturelle cosmologique)
- DESI Collaboration (2025). *DESI DR2: Extended Dark Energy analysis using DESI DR2 BAO measurements*. arXiv:2503.14743.
- DESI Collaboration (2025). *DESI DR2 Results: Cosmological constraints*. (préférence w₀wₐCDM jusqu'à 4,2σ avec CMB+DES-Y5)
- Siegel, E. (2025). *Is dark energy weakening? DESI's results are ambiguous*. Big Think, 26 mars 2025. (lecture critique)
- Shamir, L. (2024–2025). Travaux sur l'asymétrie du sens de rotation des galaxies (JWST) — indications débattues.

---

*Document généré dans le cadre d'une exploration personnelle. Toute utilisation académique requiert vérification indépendante des calculs (reproductibles via le script compagnon) et revue de littérature complète.*
