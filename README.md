# Externally sourced dark energy — corpus, judges, and tools

**🇬🇧 English first · 🇫🇷 [Version française plus bas](#-version-française--french-version).**

> *"Once Zhuangzi dreamt he was a butterfly. On waking, he no longer knew whether he was
> a man who had dreamt he was a butterfly, or a butterfly dreaming he was a man."*
> — Zhuangzi, 4th c. BCE

> **140 registry entries. 54 claims fallen — most of them produced by the assistant.**
> — [`registres/CONCLUSION.md`](registres/CONCLUSION.md)

[![registre](https://img.shields.io/badge/registre-91%20frozen%20criteria-blue)](outils/README_registre.md)
[![CI](https://github.com/Dantenos/cosmologie-modele-lantenois/actions/workflows/registre.yml/badge.svg)](https://github.com/Dantenos/cosmologie-modele-lantenois/actions/workflows/registre.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22095425.svg)](https://doi.org/10.5281/zenodo.22095425)

## In a nutshell — for the curious

**The question.** The universe's expansion is speeding up, and physicists blame a mysterious
"dark energy" that makes up about 70% of everything. Nobody knows what it is. This project tests
one concrete, *falsifiable* guess at **where it comes from** — that guess is **Paper A**.

**The idea: the energy comes from outside.** Suppose our entire universe is the *inside* of a
black hole living in some larger "parent" universe. Black holes grow by swallowing matter. Seen
from within, the mass-energy the parent keeps swallowing has to appear *somewhere* — and it shows
up as energy spread evenly through our space. The crucial point: this energy is injected **from
outside our own budget**. Ordinary matter keeps thinning out as space expands (exactly as it
should); meanwhile the injected component accumulates and pushes the expansion faster. *That*
injected energy is the dark energy.

**One number sets everything.** If the parent's mass grows as a power of time, M ∝ t^β, then a
single exponent — β ≈ 2.4 — fixes the entire history of dark energy:

> **w(z) = −β / (3 H t)**

One parameter, no fine-tuning. And on its own it reproduces something the data seem to want: dark
energy that was *"phantom"* (pushing harder than a cosmological constant) in the distant past and
eases off today — the very pattern the DESI survey's 2024–2025 results hint at, which normally
takes *two* parameters to fit.

**The journey, honestly.** This is a fringe idea, and most of the work here is the discipline of
*not fooling ourselves* about it. Over nine days, every success criterion was written down
**before** each computation was run; 54 claims were then retracted — most produced by the AI
assisting the analysis, whose errors leaned, measurably, toward the conclusion we hoped for. The
safeguard is mechanical: each criterion is frozen by a cryptographic hash, and the build turns red
if it changes afterward. The verdict for the next dataset (DESI DR3, 2027) is **already sealed** —
nobody, ourselves included, can quietly rewrite it once the data arrive.

**Does this prove we live in a black hole?** No — nothing here does. What it does is turn a poetic
idea into a *falsifiable* one and hold it to a hard standard. If dark energy turns out to be a plain
cosmological constant after all, this stands as a pre-registered null result that worked — and the
method is the real result.

*Nine days (16–24 August 2026), audited against Pantheon+, DESI DR2 and Planck, with an adversarial
registry kept by hand and judges summoned on fixed dates. Everything is here, the errors included.*

---

## I. The scientific corpus

### The three papers

| | Paper | Status | Source |
|---|---|---|---|
| **A** | *Externally sourced dark energy: a one-parameter fluid tested against Planck, DESI DR2 and three supernova compilations* (33 pp.) — the law, β, the low-redshift phantom crossing (z_× = 0.21–0.46 depending on β, #111), the DR3 targets | → arXiv | [`papiers/papierA_fluide_source_externe.pdf`](papiers/papierA_fluide_source_externe.pdf) · [tex](papiers/papierA_fluide_source_externe.tex) |
| **B** | *The nested-hierarchy reading of externally sourced dark energy* (14 pp.) — appendix: parent accretion, constraint sheet (ε ≲ 2×10⁻⁴ ; x₀ ≲ 0.30 ; conversion ≥ 97 %) | appendix | [`papiers/papierB_hierarchie.pdf`](papiers/papierB_hierarchie.pdf) · [tex](papiers/papierB_hierarchie.tex) |
| **C** | *Two sourced dark-energy models on identical data* (8 pp.) — accretion vs. cosmologically-coupled black holes (CCBH), FRB channel: 82–120 localised bursts for 3σ | → priority submission | [`papiers/papierC_comparaison.pdf`](papiers/papierC_comparaison.pdf) · [tex](papiers/papierC_comparaison.tex) |

Satellite studies: [viability taxonomy](papiers/taxonomie_cosmo_v1.pdf) ·
[shared viability window](papiers/fenetre_viabilite_v2.pdf).

### The DR3 seal

The analysis that will judge β on DESI DR3 is **written, frozen and sealed before the data
arrive**. Thresholds, verdicts (VALIDATED / REFUTED / INDECISIVE — and INDECISIVE is not
VALIDATED), pipeline: nothing moves. Anyone comparing this hash to the file in 2027 verifies
that the analysis was not retouched after seeing the data.

```
sha256(outils/scelle.py) = 68d06bcccbecf2276919c05dc841c6d878ca2516427e533af38d64344aed45a2
frozen pipeline (test_wE_v3.py) = 30c7a96430333e8c…
```

The hash is pinned in CI ([`.github/workflows/registre.yml`](.github/workflows/registre.yml)) and
archived under Zenodo DOI [10.5281/zenodo.22095425](https://doi.org/10.5281/zenodo.22095425): any
change to the arbiter breaks the build. Ourselves included.

### The judges, dated

Four cases on the [Audience](outils/audience.json) docket, seven defendants — including two
theories and an AI with a record.
**Visual tracker: [`visuels/le_role.html`](visuels/le_role.html)** (the orbital sky) ·
[`le_role_tableau.html`](visuels/le_role_tableau.html) (the table version, timeline + cards).

| Case | Claim under judgment | Judge | Deadline |
|---|---|---|---|
| **DR3-β** | β ∈ [2.42 ; 2.60], β₁ = +0.06 ± 0.31, \|κ\| < 0.24 | DESI DR3 | **2027** |
| **FRB-s** | baryon survival s = 1 (accretion) vs. s = 0.70 (CCBH) | localised-FRB catalogue N ≥ 120 | 2027–2028 |
| **W-universal** | w(z) universal across environments (Bottleneck) vs. void/wall dependence (Clock) — round 1: Δβ = +0.22 ± 0.23 | Pantheon+ × void catalogue | open |
| **k3-vs-0** | cosmological coupling k = 3 (CCBH) vs. k = 0 — living posterior | GWOSC O4 + Gaia + AGN | ongoing |

### The registries

Everything that fell, numbered, dated, with the mechanism of the fall:
[`MANQUEMENTS.md`](registres/MANQUEMENTS.md) (140 entries) ·
[`TRIAGE_DES_ATTAQUES.md`](registres/TRIAGE_DES_ATTAQUES.md) ·
[`CONCLUSION.md`](registres/CONCLUSION.md) ·
[`ATLAS.md`](registres/ATLAS.md) (**19 models, one pipeline, one ranking — generated**, #150) ·
[`TENSIONS.md`](registres/TENSIONS.md) (**the tensions registry**, arbiters carved in advance, #153) ·
[`AUDIT_2308.md`](registres/AUDIT_2308.md) (repository audit of 23/08).

---

## II. The tooling ecosystem

Twelve tools born from the campaign's scars, in [`outils/`](outils/). Zero dependencies,
Python ≥ 3.9. They will outlive the verdict, whatever it is.
*On Windows: `$env:PYTHONUTF8 = 1` before running them (the registries are UTF-8).*

| Tool | What it prevents | Usage |
|---|---|---|
| [**Registre**](outils/README_registre.md) | changing a success criterion after seeing the result | `python3 outils/registre.py freeze f.py` · `verify` · `freeze --amend` |
| **Adversaire** | complacent review — automated adversarial audit of a paper | `python3 outils/adversaire.py audit manifeste.json` |
| **Audience** | undated predictions — the public docket, actors and records | `python3 outils/audience.py inscrire aff.json` · `role` · `verdict <id>` |
| **k-tracker** | the frozen posterior — living combination of bounds on the coupling k | `python3 outils/ktracker.py etat contraintes_k.json` |
| **Scellé** | the analysis retouched after the data — the DR3 arbiter under hash | `python3 outils/scelle.py sceau` · `verdict <dr3_data>` |
| **Ligne de base** | the corpus that stops reproducing unnoticed — β re-run in CI on public data | `python3 outils/ligne_de_base.py` |
| **Périmé** | dead numbers surviving in documents — linter, blocking in CI | `python3 outils/perime.py [--tout]` |
| **Rejouer** | results that stop reproducing — 14 scripts replayed against `ancres.json` | `python3 outils/rejouer.py` |
| **État** | hand-copied counts that drift — ETAT.md generated | `python3 outils/etat.py` |
| **Grand Livre** | models that consume without paying — the baryon budget per row | `python3 outils/ledger.py` |
| **Greffier** | anomalies whose history gets rewritten — the living-tensions registry | `python3 outils/greffier.py` |
| **Confronteur** | two computations of the same quantity that silently diverge | `python3 outils/confronteur.py` |

**Registre** is the foundation: the criterion lives in the script's docstring, `freeze` pins it
by SHA-256 in [`registre.lock`](outils/registre.lock), `verify` fails (exit 1, blocking in CI)
if it has moved. Amendment is possible — but public, in `RETRACTATIONS.md`.
91 files of the corpus are frozen, Registre included: it protects itself.

---

## For future researchers

- [`registres/POUR_2027.md`](registres/POUR_2027.md) — **the letter to whoever opens the seal**: what to check first, how to judge each case, the β warning written before DR3.
- [`REPRODUIRE.md`](REPRODUIRE.md) — every headline number, its command, its expected value, its runtime.
- License: code MIT, texts and visuals CC-BY 4.0 ([`LICENSE`](LICENSE)); citation: [`CITATION.cff`](CITATION.cff) · DOI [10.5281/zenodo.22095425](https://doi.org/10.5281/zenodo.22095425).

## Structure

```
CLAUDE.md        project constitution: the nine rules, applied every session
papiers/         tex, pdf, and the figures they include
outils/          registre, adversaire, audience, ktracker, scelle + registre.lock + .json
scripts/         the 50 computation scripts (pre-registered criteria in the docstring)
registres/       MANQUEMENTS, TRIAGE, CONCLUSION, theories, notebook
visuels/         interactive html (predictions tracker, ranking, data), plates
donnees/         public data (Pantheon+, Stopyra 2023 and Douglass DR7 voids) + SHA256SUMS + TELECHARGER.sh
.github/         CI: registre verify + pinned seal
```

## The rules it is made of

Paid for at the price of fifty-four retractions ([`CLAUDE.md`](CLAUDE.md)):

- Pre-registered criteria **before** execution, always.
- Any departure > 3σ undergoes a fairness check: recompute with the rival's published values.
- Announce what a computation **reduces**, never what it closes.
- An invented placeholder value = in the direction **unfavourable** to one's own thesis.
- Never turn the ambiguous into a victory: one check of two failed ⇒ nothing is exploited.

---

Édouard Lantenois — [@Dantenos](https://github.com/Dantenos) ·
[linkedin.com/in/edlanteno](https://linkedin.com/in/edlanteno)

<br>

---
---

# 🇫🇷 Version française — French version

**🇫🇷 Version française · 🇬🇧 [English above](#externally-sourced-dark-energy--corpus-judges-and-tools).**

> *« Tchouang-tseu rêva qu'il était un papillon. À son réveil, il ne savait plus s'il était
> un homme qui avait rêvé qu'il était un papillon, ou un papillon qui rêvait qu'il était un homme. »*
> — Tchouang-tseu (Zhuangzi), IVᵉ s. av. J.-C.

> **140 entrées de registre. 54 affirmations tombées — la plupart produites par l'assistant.**
> — [`registres/CONCLUSION.md`](registres/CONCLUSION.md)

## En bref — pour les curieux

**La question.** L'expansion de l'univers s'accélère, et les physiciens en accusent une
mystérieuse « énergie noire » qui représenterait environ 70 % de tout ce qui existe. Personne ne
sait ce que c'est. Ce projet teste une hypothèse concrète et *falsifiable* sur **son origine** —
c'est le **papier A**.

**L'idée : l'énergie vient de l'extérieur.** Supposons que notre univers tout entier soit
l'*intérieur* d'un trou noir situé dans un « univers parent » plus grand. Les trous noirs
grossissent en avalant de la matière. Vue de l'intérieur, la masse-énergie que le parent continue
d'avaler doit bien apparaître *quelque part* — et elle se manifeste comme une énergie répartie
uniformément dans notre espace. Le point crucial : cette énergie est injectée **de l'extérieur de
notre propre budget**. La matière ordinaire continue de se diluer à mesure que l'espace s'étend
(exactement comme elle le doit) ; pendant ce temps, la composante injectée s'accumule et pousse
l'expansion plus vite. *Cette* énergie injectée, c'est l'énergie noire.

**Un seul nombre fixe tout.** Si la masse du parent croît comme une puissance du temps, M ∝ t^β,
alors un unique exposant — β ≈ 2,4 — fixe toute l'histoire de l'énergie noire :

> **w(z) = −β / (3 H t)**

Un paramètre, aucun réglage fin. Et à lui seul il reproduit ce que les données semblent vouloir :
une énergie noire « fantôme » (poussant plus fort qu'une constante cosmologique) dans le passé
lointain, qui s'atténue aujourd'hui — précisément le motif suggéré par les résultats 2024-2025 du
relevé DESI, qu'il faut normalement *deux* paramètres pour ajuster.

**Le cheminement, honnêtement.** C'est une idée marginale, et l'essentiel du travail ici est la
discipline de *ne pas se mentir* à son sujet. En neuf jours, chaque critère de succès a été écrit
**avant** de lancer le calcul ; 54 affirmations ont ensuite été rétractées — la plupart produites
par l'IA qui assistait l'analyse, dont les erreurs penchaient, de façon mesurable, vers la
conclusion espérée. Le garde-fou est mécanique : chaque critère est gelé par un hash
cryptographique, et le build devient rouge s'il change après coup. Le verdict pour le prochain jeu
de données (DESI DR3, 2027) est **déjà scellé** — personne, nous compris, ne peut le réécrire
discrètement une fois les données arrivées.

**Est-ce que ça prouve qu'on vit dans un trou noir ?** Non — rien ici ne le prouve. Ce que ça
fait, c'est transformer une idée poétique en une idée *falsifiable* et la soumettre à un standard
dur. Si l'énergie noire s'avère n'être qu'une simple constante cosmologique, ceci restera un test
nul pré-enregistré qui a fonctionné — et la méthode est le vrai résultat.

*Neuf jours (16-24 août 2026), audité contre Pantheon+, DESI DR2 et Planck, avec un registre
adversarial tenu à la main et des juges convoqués à date fixe. Le tout est ici, y compris les
erreurs.*

---

## I. Le corpus scientifique

### Les trois papiers

| | Papier | Statut | Source |
|---|---|---|---|
| **A** | *Externally sourced dark energy: a one-parameter fluid tested against Planck, DESI DR2 and three supernova compilations* (33 p.) — la loi, β, le croisement fantôme à bas redshift (z_× = 0,21-0,46 selon β, #111), les cibles DR3 | → arXiv | [`papiers/papierA_fluide_source_externe.pdf`](papiers/papierA_fluide_source_externe.pdf) · [tex](papiers/papierA_fluide_source_externe.tex) |
| **B** | *The nested-hierarchy reading of externally sourced dark energy* (14 p.) — annexe : accrétion parente, feuille de contraintes (ε ≲ 2×10⁻⁴ ; x₀ ≲ 0,30 ; conversion ≥ 97 %) | annexe | [`papiers/papierB_hierarchie.pdf`](papiers/papierB_hierarchie.pdf) · [tex](papiers/papierB_hierarchie.tex) |
| **C** | *Two sourced dark-energy models on identical data* (8 p.) — duel accrétion / trous noirs couplés (CCBH), canal FRB : 82-120 sursauts localisés pour 3σ | → soumission prioritaire | [`papiers/papierC_comparaison.pdf`](papiers/papierC_comparaison.pdf) · [tex](papiers/papierC_comparaison.tex) |

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

Le hash est épinglé dans la CI ([`.github/workflows/registre.yml`](.github/workflows/registre.yml))
et archivé sous le DOI Zenodo [10.5281/zenodo.22095425](https://doi.org/10.5281/zenodo.22095425) :
toute modification de l'arbitre casse le build. Nous compris.

### Les juges, datés

Quatre affaires au rôle d'[Audience](outils/audience.json), sept prévenus — dont deux théories et
une IA avec casier. **Suivi visuel : [`visuels/le_role.html`](visuels/le_role.html)** (le ciel
orbital) · [`le_role_tableau.html`](visuels/le_role_tableau.html) (la version tableau).

| Affaire | Affirmation sous jugement | Juge | Échéance |
|---|---|---|---|
| **DR3-β** | β ∈ [2,42 ; 2,60], β₁ = +0,06 ± 0,31, \|κ\| < 0,24 | DESI DR3 | **2027** |
| **FRB-s** | survie baryonique s = 1 (accrétion) contre s = 0,70 (CCBH) | catalogue FRB localisées N ≥ 120 | 2027-2028 |
| **W-universel** | w(z) universel (Goulet) contre dépendance vides/murs (Horloge) — manche 1 : Δβ = +0,22 ± 0,23 | Pantheon+ × catalogue de vides | ouverte |
| **k3-vs-0** | couplage cosmologique k = 3 (CCBH) contre k = 0 — postérieur vivant | GWOSC O4 + Gaia + AGN | continue |

### Les registres

Tout ce qui est tombé, numéroté, daté, avec le mécanisme de la chute :
[`MANQUEMENTS.md`](registres/MANQUEMENTS.md) (140 entrées) ·
[`TRIAGE_DES_ATTAQUES.md`](registres/TRIAGE_DES_ATTAQUES.md) ·
[`CONCLUSION.md`](registres/CONCLUSION.md) ·
[`ATLAS.md`](registres/ATLAS.md) (**19 modèles, un pipeline, un classement — généré**, #150) ·
[`TENSIONS.md`](registres/TENSIONS.md) (**le registre des tensions**, arbitres gravés d'avance, #153) ·
[`AUDIT_2308.md`](registres/AUDIT_2308.md) (audit du dépôt du 23/08).

---

## II. L'écosystème d'outils

Douze outils nés des cicatrices de la campagne, dans [`outils/`](outils/). Zéro dépendance,
Python ≥ 3.9. Ils survivront au verdict, quel qu'il soit.
*Sous Windows : `$env:PYTHONUTF8 = 1` avant de les lancer (les registres sont en UTF-8).*

| Outil | Ce qu'il empêche | Usage |
|---|---|---|
| [**Registre**](outils/README_registre.md) | modifier un critère de succès après avoir vu le résultat | `python3 outils/registre.py freeze f.py` · `verify` · `freeze --amend` |
| **Adversaire** | la relecture complaisante — audit contradictoire automatisé | `python3 outils/adversaire.py audit manifeste.json` |
| **Audience** | les prédictions sans date — l'échéancier public | `python3 outils/audience.py inscrire aff.json` · `role` · `verdict <id>` |
| **k-tracker** | le postérieur figé — combinaison vivante des bornes sur k | `python3 outils/ktracker.py etat contraintes_k.json` |
| **Scellé** | l'analyse retouchée après les données — l'arbitre DR3 sous hash | `python3 outils/scelle.py sceau` · `verdict <donnees_dr3>` |
| **Ligne de base** | le corpus qui cesse de se reproduire sans qu'on le voie | `python3 outils/ligne_de_base.py` |
| **Périmé** | les chiffres morts qui survivent dans les documents — linter, bloquant en CI | `python3 outils/perime.py [--tout]` |
| **Rejouer** | les résultats qui cessent de se reproduire — 14 scripts rejoués | `python3 outils/rejouer.py` |
| **État** | les comptes recopiés à la main qui divergent | `python3 outils/etat.py` |
| **Grand Livre** | les modèles qui consomment sans payer — le bilan baryonique | `python3 outils/ledger.py` |
| **Greffier** | les anomalies dont on réécrit l'histoire — le registre des tensions | `python3 outils/greffier.py` |
| **Confronteur** | deux calculs de la même quantité qui divergent en silence | `python3 outils/confronteur.py` |

**Registre** est le socle : le critère vit dans le docstring du script, `freeze` le fige par
SHA-256 dans [`registre.lock`](outils/registre.lock), `verify` échoue (exit 1, bloquant en CI)
s'il a bougé. L'amendement est possible — mais public, dans `RETRACTATIONS.md`.
91 fichiers du corpus sont gelés, Registre compris : il se protège lui-même.

---

## Pour les chercheurs futurs

- [`registres/POUR_2027.md`](registres/POUR_2027.md) — **la lettre à qui ouvrira le sceau** : quoi vérifier d'abord, comment juger chaque affaire, l'avertissement β écrit avant DR3.
- [`REPRODUIRE.md`](REPRODUIRE.md) — chaque chiffre de tête, sa commande, sa valeur attendue, son temps.
- Licence : code MIT, textes et visuels CC-BY 4.0 ([`LICENSE`](LICENSE)) ; citation : [`CITATION.cff`](CITATION.cff) · DOI [10.5281/zenodo.22095425](https://doi.org/10.5281/zenodo.22095425).

## Les règles dont c'est fait

Payées au prix de cinquante-quatre rétractations ([`CLAUDE.md`](CLAUDE.md)) :

- Critères pré-enregistrés **avant** exécution, toujours.
- Tout écart > 3σ subit un contrôle d'équité : recalculer avec les valeurs du rival.
- Annoncer ce qu'un calcul **réduit**, jamais ce qu'il ferme.
- Valeur de substitution inventée = dans le sens **défavorable** à sa propre thèse.
- Jamais convertir l'ambigu en victoire : un contrôle sur deux échoué ⇒ rien n'est exploité.

---

Édouard Lantenois — [@Dantenos](https://github.com/Dantenos) ·
[linkedin.com/in/edlanteno](https://linkedin.com/in/edlanteno)
