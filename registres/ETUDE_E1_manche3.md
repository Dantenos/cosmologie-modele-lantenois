# ÉTUDE E1 MANCHE 3 — DESIVAST DR1 × PANTHEON+ (24/08/2026)

*Critères gelés avant exécution : `scripts/etude_E1_manche3.py` (096c986f8ec1). Données :
DESIVAST DR1 BGS VOLLIM (Rincon et al. 2025, ApJ 982, 38 — VAC public DESI, ramené par agent,
sha256 vérifiés) : VoidFinder 3765 / VIDE 1478 / REVOLVER 1992 vides, z < 0,24, ~2900 deg².
Ferme la liste de données de la spec mère, qui nommait DESIVAST dès l'origine.*

## Verdict A (duel goulet/horloge) : NON EXPLOITÉ
227 SNe dans l'empreinte (le BGS DR1 est petit) ; les partages V2 tombent à 66 SNe côté vides —
sous le plancher gelé de 80. **Le duel reste 2-0 (manches 1-2) ; la manche 3 ne compte pas.**
| algorithme | partage | Δβ | σ | perms p |
|---|---|---|---|---|
| VoidFinder | 110/117 | −0,091 | 0,705 | 0,88 |
| VIDE | 66/161 | +0,342 | 0,991 | 0,51 |
| REVOLVER | 66/161 | +0,399 | 1,010 | 0,52 |

## Verdict B (arbitrage de T6) : FLUCTUATIONS — avec réserve consignée
Le critère gelé : signes opposés chacun ≥ 1σ → non-univocité ; les deux < 1σ → fluctuations.
Résultat : VF −0,09 (0,1σ) vs VIDE +0,34 (0,3σ) → **branche FLUCTUATIONS**.
**Réserve, consignée en #155** : cette branche ne conditionne pas sur la puissance — avec
σ_Δ ≈ 0,7-1,0 (contre 0,36 sur Douglass), y entrer était presque garanti. Même famille de vice
que le critère d'E3 v0 (#148). La résolution est donc inscrite au greffe **avec clause de
réouverture** : tout test des mêmes algorithmes à σ_Δ ≤ 0,4 peut rouvrir T6.
**L'indice indépendant qui soutient la lecture « bruit »** : Jaccard(VIDE, REVOLVER) = **0,97**
sur DESIVAST (0,41 sur Douglass) et Jaccard(VF, V2) = 0,59 (0,33) — sur un catalogue moderne,
les algorithmes trient presque les mêmes SNe : la non-univocité de Douglass ressemble à un
artefact de son époque plus qu'à un fait sur les vides.

## Sortie réelle (extraits) et durée
205 s ; graine 20260824 ; 200 permutations par algorithme ; verify 45 critères OK.
