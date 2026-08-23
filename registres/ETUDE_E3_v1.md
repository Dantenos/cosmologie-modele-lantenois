# ÉTUDE E3 — FRB SUR DONNÉES RÉELLES : la table de Connor et al. 2025 (23/08/2026)

*Critères gelés avant exécution : v0 `scripts/etude_E3_frb_reelles.py` (77e8bff5d7b5),
v1 `scripts/etude_E3_frb_reelles_v1.py` (b4db63303237). Données : 69 FRB localisés
(spectroscopiques) de « A gas-rich cosmic web… », Nature Astronomy 2025 —
`donnees/frb_connor2025/frbsample_connor0924.csv`, sha256 dans `donnees/SHA256SUMS`.
Machinerie : `frb_likelihood.py` (gelée), trois fonds (ΛCDM ; accrétion β = 2,595 ;
CCBH calibré A = 1,551, B = 3,119, Ξ = 1,382).*

## v0 : le critère de la spec, appliqué tel quel — NON EXPLOITÉ
La spec mère exigeait f_IGM(ΛCDM) = 0,80 ± 0,10. Le fit donne 0,698 → ÉCHEC à 0,002 près.
**Mais le critère portait sur une variable non identifiable** : dans la vraisemblance gelée,
f_IGM et f_X n'entrent que par leur somme (vérifié : logL identique à 10 décimales à somme
fixée). Le verdict v0 est conservé ; le vice est du même type que le garde-fou #49.

## v1 : critère corrigé et déclaré (variable identifiable f_d = f_IGM + f_X)
| fond | −lnL | f_d | hôte médian | σ_host |
|---|---|---|---|---|
| ΛCDM | 337,633 | **0,905** | 123,2 | 0,624 |
| accrétion (s = 1) | 337,626 | 0,912 | 123,4 | 0,624 |
| CCBH calibré | 339,989 | **1,000 (bord)** | 169,6 | 0,675 |

**VALIDATION PASSE** : f_d = 0,905 contre 0,91 publié (0,5 %), hôte 123 contre ~120.

**Résultat, rapporté tel quel (un tirage, pas de seuil de victoire déclaré) :**
- **Δχ²(CCBH − ΛCDM) = +4,71 (~2,2σ)** — cohérent avec la médiane des mocks (#99 : ~2,1σ).
- Δχ²(accrétion − ΛCDM) = −0,01 : **s = 1 indiscernable de ΛCDM**, comme prédit.
- Le CCBH pousse f_d au bord = 1 avec un hôte gonflé à 170 pc/cm³ : la signature
  pré-enregistrée « le déficit baryonique n'est PAS absorbable par les nuisances ».

## Ce que cela change
Le canal FRB du papier C reposait sur des mocks calibrés ; il repose maintenant aussi sur
la table réelle, avec le même verdict à la même amplitude. Ce que cela réduit : l'échappatoire
« les nuisances absorberont le déficit » (le fit la teste, elle sature le bord). Ce que cela
ne ferme pas : 2,2σ n'est pas 3σ — le compte de sursauts à levier reste le juge (82-120, spec).
**Substitution aux mocks dans le papier C : étape d'auteur** (la spec mère l'exige avec mention
explicite du changement ; les chiffres sont prêts ci-dessus).
