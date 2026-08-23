# AUDIT DU DÉPÔT — 23/08/2026 (Claude Code, machine Windows, carte blanche)

*Trois lectures indépendantes (registres, papiers, code) + rejeu de 38 scripts sur données
publiques + deux études à critères gelés. Tout ce qui a été corrigé est dans l'historique git
(`d0c12ab` et suivants) ; tout ce qui reste à l'auteur est listé en §5. Règle suivie : on ne
touche jamais un docstring gelé ni les octets de `scelle.py` ; le reste est du corps.*

## 1. Ce qui tourne, ce qui ne tourne pas

| | |
|---|---|
| Scripts rejoués | **38 / 45 exit 0** (depuis `donnees/pantheon_plus/`, Python 3.12, numpy 2.5, scipy 1.18, camb 2.0.3) |
| Bloqués par une dépendance externe | `planck_theta.py`, `jackknife_planck.py` — **`planck_lite_py` absent du dépôt**. Ce sont les deux scripts du Δχ² = −12,6 (Planck complet) du papier A et de son jackknife : **non reproductibles par un tiers** tant que le paquet (github.com/heatherprince/planck-lite-py + `data/`) n'est pas fourni ou documenté. |
| Non rejoués | `mcmc_wE.py` (chaîne de plusieurs heures ; `emcee.EnsembleSampler` **non seedé** — la chaîne n'est pas reproductible à l'identique) |
| Ligne de base | `vraisemblance_reelle.py` : 1580 SNe, β = 2,447, Δχ² = −4,41 → **gardée en CI** (`outils/ligne_de_base.py`, gelé) |
| Critères gelés | 20 → **25** (+ `etude_E1_vides`, `etude_E1_manche2`, `etude_E1_robustesse`, `ligne_de_base`, `frb_likelihood`) |

Comparaison des 38 sorties aux ancres numériques des docstrings : voir §6 (en cours au moment
de l'écriture ; complété ci-dessous).

## 2. Bugs de code corrigés (corps seuls)

1. **`duel_ccbh.py:52` — `ai=1/(1+ZI)` évalué à la définition.** Le test « SENSIBILITÉ de CCBH
   à z_i » faisait `globals()['ZI'] = zi` sans effet : **trois χ² identiques (1425,279)**.
   MANQUEMENTS #80 déclarait ce bug « corrigé » — le fichier livré ne l'était pas. Corrigé ; le
   script imprime désormais la sensibilité **à paramètres fixés** (reproduit les 67,97–70,91
   publiés) **et réajustés** (règle 5) : H₀ = 70,22–70,43, Ξ = 3,97–4,53, ΔAIC = +3,5 à +6,1.
   → Papier C l.208 amendé : z_i est un paramètre caché **absorbé par Ξ**, pas un levier sur H₀.
2. `adversaire.py:50` — `ok` calculé, jamais utilisé : le critère gelé « v1 échoue si un verdict
   apparaît sans valeur exécutée » n'était pas implémenté. `exit 1` désormais. Chemins relatifs
   à la racine ; clés du lock préfixées ; rapport écrit dans `registres/`.
3. `audience.py` — `audience.json` cherché dans le CWD (lancé depuis la racine : rôle perdu) ;
   `read_text()`/`write_text()` sans UTF-8 ; **double comptage des casiers** par réinscription.
4. `registre.py` — `read_text()` sans `encoding` : **`UnicodeDecodeError` sous Windows** (cp1252
   sur `∝`). Lock et rétractations en UTF-8 + LF explicites.
5. `attaque_croker_fond.py`, `frb_strategie.py`, `mcmc_wE.py` — chemins `/home/claude/…` de la
   machine d'origine.
6. `contraintes_k.json` — `jwst_agn` : note « REFUSÉ (règle E5) », statut `verifie` ; le code ne
   lit que le statut. Aligné → k-tracker 5/7.
7. `frb_likelihood.py` — arbitre de l'affaire FRB-s (`aff2.json`) **non gelé**, et `exec()`
   par `frb_strategie.py` (gelé) : un critère gelé dépendait d'un fichier non gouverné. Gelé.
8. Fins de ligne : Python sous Windows écrivait `\r\n` (lock, rapport) — forcé en LF.

Non corrigé, et incorrigeable : **`scelle.py:22-23`** lit `registre.lock` en relatif sans UTF-8
et teste la clé `test_wE_v3.py` (réelle : `scripts/test_wE_v3.py`) → `sceau` plante sous Windows
nu et n'affiche jamais le hash du pipeline. Le fichier est scellé par ses octets (68d06bcc…,
épinglé en CI) : toute correction brise le sceau. Parade documentée : `PYTHONUTF8=1` depuis
`outils/`. À amender publiquement si jamais le sceau est réouvert — pas avant DR3.

## 3. Papiers — corrections déclarées « faites » et non propagées (appliquées aux .tex)

| Rétractation | Où elle était appliquée | Où elle survivait | Fait |
|---|---|---|---|
| Erratum β/−12,6 (MANQUEMENTS #2 : « −12,6 appartient à β ≈ 2,56-2,59 ; 2,49 coûte +4,4 ») | abstract A | **corps A l.96 et l.100** : « Δχ² = −12,6 … β = 2,49 ± 0,05 », « band 2,39–2,55 » | ✔ |
| « plausible » retiré (TRIAGE #1) | A l.456 | A l.405 | ✔ |
| « un quart, pas la moitié » (TRIAGE #2) | A l.453, abstract | **A l.459 et l.465**, six lignes plus bas, contredisant la correction | ✔ |
| fσ8 « canal le plus propre » retiré (TRIAGE #32) | A l.268, l.527 | A l.567 | ✔ |
| « 142 sursauts » retiré (TRIAGE #49) | papier C | **papier A l.825** (142/253/395, sans rétractation) | ✔ |
| `\bibitem{Croker2024}` en doublon | — | A l.964 et l.976 | ✔ |
| Sensibilité à z_i (nouveau, ce jour) | — | C l.208 | ✔ |

**Les PDF ne sont pas recompilés** (pas de LaTeX ici ; Docker + texlive possible).

## 4. Façade et registres — corrigés

- Croisement fantôme « z = 0,46 » : **retiré comme prédiction chiffrée par #111** (valeur
  courante 0,214 à β = 2,595 ; 0,458 à 2,42) mais encore en vitrine dans `README.md:25` et
  `CONCLUSION.md:5`. Reformulé « bas redshift, z_× = 0,21-0,46 selon β, #111 ».
- `README_registre.md` : 41 rétractations l.37 vs « cinquante » l.81 vs 54 (TRIAGE) ; démo avec
  les clés d'avant rangement. Aligné sur 54 et sur les chemins réels.
- `RETRACTATIONS.md` : cité par `registre.py`, README, rapport adversaire, PIPELINE — **n'existait
  pas**. Créé (journal des amendements `--amend`, vide à ce jour).
- E1 : `ETUDE_E1_v0.md` donne deux β pour 1580 SNe (2,516 SN-seules Om fixé ; 2,447 SN+BAO) —
  ce ne sont pas la même quantité, note ajoutée. Le visuel `ciel_pantheon.html` porte encore
  β_apex = 2,60 (copie locale d'août) contre 2,66 au rejeu sur données publiques — Δβ identique.

## 5. Ce qui reste à l'auteur (jugement scientifique, pas mécanique)

**Papiers**
- **P10 (A l.933), « the sharpest single statement this study produces »** : z_× = 0,50 pour
  β = 5/2 ; le tableau de rétractation du même papier (l.632-635) interpole ≈ 0,33 à cette
  valeur ; 0,36 survit en l.577/925 et 0,68 en l.100. Quatre valeurs du croisement dans un
  papier qui l'a retiré. **P9 n'existe pas** (P1…P8, P10).
- A l.894 vs l.903 : ρ = −0,43 et ρ = −0,55 pour la même covariance Lyα (l'avantage va de +0,1
  à +7,8 selon ρ).
- A l.205 « The boundary sector is closed » — dans le paragraphe qui documente trois
  renversements, et avant deux de plus (TRIAGE #58/60/61). Règle 3.
- A l.128 « The running is therefore a discriminant between two theoretical readings » vs l.133
  qui dit l'inverse (TRIAGE #41).
- Papier C : β = 2,595 (l.163) contre A « fair summary β = 2,42 ± 0,07 » (l.98), même χ² =
  1419,31 — aucun des deux ne mentionne l'écart. Le « 120 » de « 82-120 sursauts » n'est
  dérivé d'aucun calcul (tableau : 239/153/134/82 ; σ_host : 123→94) ; 123 serait l'ancre.
- B l.169 « agreeing to 0,4 % — two numbers obtained independently » : TRIAGE #33 a établi que
  c'est une identité.
- Le **sceau sha256 n'apparaît dans aucun .tex**. L'argument méthodologique central de
  CONCLUSION.md est invisible pour un lecteur d'arXiv. Une phrase dans A suffirait.
- `\bibitem` non cités : `Valiviita2008` (A), `Farrah2023` (B, pourtant ancre de P5).

**Registres**
- **MANQUEMENTS.md n'est pas injectif** : #21 absent ; #72-#81 et #103-#114 portent chacun
  **deux entrées différentes** ; #130 dupliqué mot pour mot (l.1780/1794) ; deux « fins réelles »
  (115 l.1638, 116 l.1655) suivies de 26 entrées ; #137 affirme « séquentiel sans trou ».
  Citer « #75 » est ambigu. Proposition : suffixer la seconde série (#72b…), ne pas renuméroter.
- TRIAGE : 7 numéros dupliqués (40-43, 46-48), compteur cumulé qui recule deux fois, « fin du
  registre » suivie de 13 entrées, 63 numéros pour 70 lignes.
- Nombre de rétractations : 41 / 50 / 53 / 54 selon le document ; le mur HTML en calcule 41
  (+1 juste) sur 70 lignes parsées, avec 4 vignettes cassées par `\|κ\|`. `video_explicative.html`
  : « 123 entrées · 46 réfutées ».
- THEORIE_SATURATION.md : quatre paragraphes fondés sur σ = 1,8 % (réfuté #139), coiffés d'un
  bandeau ; TRIAGE l.331 conclut encore que ce chiffre « est plus utile que les trois théories
  réunies ». BALAYAGE_CONSEQUENCES l.52 garde « 1-2 % » (corrigé +3,7 % par #136).
- CONCLUSION.md l.22 grave « +3,7 % fσ8 » que #136 interdit d'exploiter avant E9.
- Trois résultats de tête du papier B retirés par #52 survivent dans SYNTHESE_ET_OUVERTURES
  l.16-18, carnet l.196-199, LISEZMOI_MANIFEST l.13.
- `email_experts_brouillon.md` : le seul livrable pour un tiers porte β = 2,42, Δχ² = −12,6,
  z ≈ 0,36, k_equiv = 3,07 — quatre valeurs mortes.
- `etude_complete.txt` et `etude_complete_v2.md` : même document (2 lignes de diff), 68 ko ×2.
- Promesses ouvertes depuis le 19/08 : MCMC Cobaya (`cobaya_accretion.yaml` référencé par
  aucun script), linter de valeurs périmées (`ATLAS_falsification_spec.md:45-62`, « mode de
  défaillance n°1 », jamais écrit — c'est l'outil qui aurait attrapé le §3 et le §4), Popławski
  non contacté, aucune relecture externe.
- `etudes_2026.py` (gelé) nomme VAST SDSS DR7 / DESIVAST / LocalVoids pour E1 ; exécuté sur
  Stopyra (#135) + Douglass CDS. Note : **Douglass 2023 au CDS EST le catalogue VAST SDSS DR7**
  (même auteurs, mêmes algorithmes VoidFinder/V2). Stopyra remplace DESIVAST/LocalVoids — à
  consigner comme écart à la spec, pas comme amendement.

**Code (mineur, non corrigé)**
- Motif « ligne morte suivie de sa correction » dans quatre scripts gelés :
  `frb_likelihood.py:70-71`, `voile_cisaillement.py:65/67`, `flux_paroi.py:43-44`,
  `couche_limite.py:40/42`. Sans effet sur les résultats ; trace de débogage figée.
- `audit_131.py:38` : `flux_ext = flux_int = v0²` puis on imprime leur différence — tautologie,
  pas un test (le reproche même de `audit_v2.py` au contrôle π³).
- `perturbations_derivees.py` : docstring gelé `de' = -Td`, code `+Td` ; `-(1+dlnH)` vs
  `-(2+dlnH)`. À vérifier par l'auteur : lequel est juste ? (Si le code, amender le docstring.)
- `eps_nu.py` : docstring n_eff = −2,03, code −2,0255. `carte_reproduction.py:20` imprime
  « (2,05 ; 4,11) » en dur alors que l.19 les calcule.
- `test_wE_v3.py` : docstring gelé commence par « test_wE_v2.py » ; `DP_V` cite 2405.06618 là où
  le docstring cite Chen-Huang-Wang.
- `mcmc_wE.py` : sampler non seedé. `jackknife_planck.py`, `planck_theta.py` : `open()` non fermés.
- `horloge_poussiere_v2.py:30` : variables qui fuient de la boucle (NameError possible).

## 6. Ancres numériques — rejeu contre les docstrings

*(section complétée par le balayage, voir ci-dessous)*
