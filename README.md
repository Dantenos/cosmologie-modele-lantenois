# Énergie noire à source externe — corpus, juges et outils

> **140 entrées de registre. 54 affirmations tombées — la plupart produites par l'assistant.**
>
> *La science n'est pas d'avoir raison. C'est d'écrire, avant de savoir, ce qui prouverait
> qu'on a tort — et de tenir le registre quand ça arrive. Cent quarante fois.*
> — [`registres/CONCLUSION.md`](registres/CONCLUSION.md)

Neuf jours (16-24 août 2026). Une loi à un paramètre, **w(z) = −β/(3Ht)**, β = 2,42-2,60,
auditée contre Pantheon+, DESI DR2 et Planck, avec un registre adversarial tenu à la main, des
critères gelés avant chaque calcul, et des juges convoqués à date fixe. Le tout est ici, y
compris les erreurs.

[![registre](https://img.shields.io/badge/registre-25%20crit%C3%A8res%20gel%C3%A9s-blue)](outils/README_registre.md)
<!-- une fois le dépôt en ligne : ![CI](https://github.com/ORG/REPO/actions/workflows/registre.yml/badge.svg) -->

---

## I. Le corpus scientifique

### Les trois papiers

| | Papier | Statut | Source |
|---|---|---|---|
| **A** | *Externally sourced dark energy: a one-parameter fluid tested against Planck, DESI DR2 and three supernova compilations* (33 p.) — la loi, β, le croisement fantôme à bas redshift (z_× = 0,21-0,46 selon β, #111), les cibles DR3 | → arXiv | [`papiers/papierA_fluide_source_externe.pdf`](papiers/papierA_fluide_source_externe.pdf) · [tex](papiers/papierA_fluide_source_externe.tex) |
| **B** | *The nested-hierarchy reading of externally sourced dark energy* (14 p.) — annexe : accrétion parente, feuille de contraintes (ε ≲ 2×10⁻⁴ ; x₀ ≲ 0,30 ; conversion ≥ 97 %) | annexe | [`papiers/papierB_hierarchie.pdf`](papiers/papierB_hierarchie.pdf) · [tex](papiers/papierB_hierarchie.tex) |
| **C** | *Two sourced dark-energy models on identical data* (7 p.) — duel accrétion / trous noirs couplés (CCBH), canal FRB : 82-120 sursauts localisés pour 3σ | → soumission prioritaire | [`papiers/papierC_comparaison.pdf`](papiers/papierC_comparaison.pdf) · [tex](papiers/papierC_comparaison.tex) |

Études satellites : [taxonomie de viabilité](papiers/taxonomie_cosmo_v1.pdf) ·
[fenêtre de viabilité commune](papiers/fenetre_viabilite_v2.pdf).

### Le sceau DR3

L'analyse qui jugera β sur DESI DR3 est **écrite, gelée et scellée avant l'arrivée des
données**. Seuils, verdicts (VALIDÉE / RÉFUTÉE / INDÉCISE — et INDÉCISE n'est pas VALIDÉE),
pipeline : rien ne bouge. Quiconque compare ce hash au fichier en 2027 vérifie que l'analyse
n'a pas été retouchée après avoir vu les données.

```
sha256(outils/scelle.py) = 68d06bcccbecf2276919c05dc841c6d878ca2516427e533af38d64344aed45a2
pipeline gelé (test_wE_v3.py) = 30c7a96430333e8c…
```

Le hash est épinglé dans la CI ([`.github/workflows/registre.yml`](.github/workflows/registre.yml)) :
toute modification de l'arbitre casse le build. Nous compris.

### Les juges, datés

Quatre affaires au rôle d'[Audience](outils/audience.json), sept prévenus — dont deux
théories et une IA avec casier.

| Affaire | Affirmation sous jugement | Juge | Échéance |
|---|---|---|---|
| **DR3-β** | β ∈ [2,42 ; 2,60], β₁ = +0,06 ± 0,31, \|κ\| < 0,24 | DESI DR3 | **2027** |
| **FRB-s** | survie baryonique s = 1 (accrétion) contre s = 0,70 (CCBH) | catalogue FRB localisées N ≥ 120 | 2027-2028 |
| **W-universel** | w(z) universel par environnement (Goulet) contre dépendance vides/murs (Horloge) — manche 1 : Δβ = +0,22 ± 0,23 | Pantheon+ × catalogue de vides | ouverte |
| **k3-vs-0** | couplage cosmologique k = 3 (CCBH) contre k = 0 — postérieur vivant | GWOSC O4 + Gaia + AGN | continue |

### Les registres

Tout ce qui est tombé, numéroté, daté, avec le mécanisme de la chute :
[`MANQUEMENTS.md`](registres/MANQUEMENTS.md) (140 entrées) ·
[`TRIAGE_DES_ATTAQUES.md`](registres/TRIAGE_DES_ATTAQUES.md) (vraies erreurs ou fausses alertes) ·
[`TROIS_CHANTIERS.md`](registres/TROIS_CHANTIERS.md) ·
[`THEORIE_GOULET.md`](registres/THEORIE_GOULET.md) / [`THEORIE_HORLOGE.md`](registres/THEORIE_HORLOGE.md) ·
[`CONCLUSION.md`](registres/CONCLUSION.md) ·
[`AUDIT_2308.md`](registres/AUDIT_2308.md) (audit du dépôt du 23/08 : 38 scripts rejoués, un contrôle publié inopérant, six corrections propagées, ce qui reste à faire).

---

## II. L'écosystème d'outils

Cinq outils nés des cicatrices de la campagne, dans [`outils/`](outils/). Zéro dépendance,
Python ≥ 3.9. Ils survivront au verdict, quel qu'il soit.
*Sous Windows : `$env:PYTHONUTF8 = 1` avant de les lancer (les registres sont en UTF-8).*

| Outil | Ce qu'il empêche | Usage |
|---|---|---|
| [**Registre**](outils/README_registre.md) | modifier un critère de succès après avoir vu le résultat | `python3 outils/registre.py freeze f.py` · `verify` · `freeze --amend` |
| **Adversaire** | la relecture complaisante — audit contradictoire automatisé d'un papier | `python3 outils/adversaire.py audit manifeste.json` |
| **Audience** | les prédictions sans date — l'échéancier public, acteurs et casiers | `python3 outils/audience.py inscrire aff.json` · `role` · `verdict <id>` |
| **k-tracker** | le postérieur figé — combinaison vivante des bornes sur le couplage k | `python3 outils/ktracker.py etat contraintes_k.json` |
| **Scellé** | l'analyse retouchée après les données — l'arbitre DR3 sous hash | `python3 outils/scelle.py sceau` · `verdict <donnees_dr3>` |

**Registre** est le socle : le critère vit dans le docstring du script, `freeze` le fige par
SHA-256 dans [`registre.lock`](outils/registre.lock), `verify` échoue (exit 1, bloquant en CI)
s'il a bougé. L'amendement est possible — mais public, dans `RETRACTATIONS.md`.
25 fichiers du corpus sont gelés, Registre compris : il se protège lui-même.

```console
$ python3 outils/registre.py verify
[registre] OK    scripts/voile_cisaillement.py
[registre] OK    outils/registre.py
[registre] OK    outils/scelle.py
…                                          # 25 fichiers, exit 0
```

---

## Structure

```
CLAUDE.md        constitution du projet : les neuf règles, appliquées à chaque session
papiers/         tex, pdf, et les figures qu'ils incluent
outils/          registre, adversaire, audience, ktracker, scelle + registre.lock + .json
scripts/         les 45 scripts de calcul (critères pré-enregistrés en docstring)
registres/       MANQUEMENTS, TRIAGE, TROIS_CHANTIERS, CONCLUSION, théories, carnet
visuels/         html interactifs, planches
donnees/         données publiques (Pantheon+, vides Stopyra 2023 et Douglass DR7) + SHA256SUMS + TELECHARGER.sh
.github/         CI : registre verify + sceau épinglé
```

## Les règles dont c'est fait

Payées au prix de cinquante-quatre rétractations ([`CLAUDE.md`](CLAUDE.md)) :

- Critères pré-enregistrés **avant** exécution, toujours.
- Tout écart > 3σ subit un contrôle d'équité : recalculer avec les valeurs du rival.
- Annoncer ce qu'un calcul **réduit**, jamais ce qu'il ferme.
- Valeur de substitution inventée = dans le sens **défavorable** à sa propre thèse.
- Jamais convertir l'ambigu en victoire : un contrôle sur deux échoué ⇒ rien n'est exploité.

## Et ensuite

Les six études 2026 sont spécifiées et gelées dans [`scripts/etudes_2026.py`](scripts/etudes_2026.py).
**E1 v0 exécutée (23/08)** : [`registres/ETUDE_E1_v0.md`](registres/ETUDE_E1_v0.md) — Stopyra : Δβ = +0,10 ± 0,24 ; [manche 2 Douglass DR7](registres/ETUDE_E1_manche2.md) : trois algorithmes, tous nuls (< 1,4σ, signes opposés). **UNIVERSEL sur deux juges.** Puis E4 → E3 → E2. E5, E6, E7 closes.

Données publiques : `sh donnees/TELECHARGER.sh` (empreintes vérifiées). Ligne de base rejouée : β = 2,447.

---

Édouard Lantenois — [@Dantenos](https://github.com/Dantenos) ·
[linkedin.com/in/edlanteno](https://linkedin.com/in/edlanteno)

*« Les tests empêchent le code de mentir. Registre empêche l'analyste. »*
