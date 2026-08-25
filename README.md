# Externally sourced dark energy — corpus, judges, and tools

*Version française : [`README.fr.md`](README.fr.md).*

> *"Once Zhuangzi dreamt he was a butterfly. On waking, he no longer knew whether he was
> a man who had dreamt he was a butterfly, or a butterfly dreaming he was a man."*
> — Zhuangzi, 4th c. BCE

> **140 registry entries. 54 claims fallen — most of them produced by the assistant.**
> — [`registres/CONCLUSION.md`](registres/CONCLUSION.md)

Nine days (16–24 August 2026). A one-parameter law, **w(z) = −β/(3Ht)**, β = 2.42–2.60,
audited against Pantheon+, DESI DR2 and Planck, with an adversarial registry kept by hand,
criteria frozen before every computation, and judges summoned on fixed dates. Everything is
here, the errors included.

[![registre](https://img.shields.io/badge/registre-91%20frozen%20criteria-blue)](outils/README_registre.md)
[![CI](https://github.com/Dantenos/cosmologie-modele-lantenois/actions/workflows/registre.yml/badge.svg)](https://github.com/Dantenos/cosmologie-modele-lantenois/actions/workflows/registre.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22095425.svg)](https://doi.org/10.5281/zenodo.22095425)

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

The hash is pinned in CI ([`.github/workflows/registre.yml`](.github/workflows/registre.yml)):
any change to the arbiter breaks the build. Ourselves included.

### The judges, dated

Four cases on the [Audience](outils/audience.json) docket, seven defendants — including two
theories and an AI with a record.
**Visual tracker: [`visuels/le_role.html`](visuels/le_role.html)** (the orbital sky) ·
[`le_role_tableau.html`](visuels/le_role_tableau.html) (the table version, timeline + cards) —
the judges' timeline, the three β on the sealed band, the FRB counter, the rounds, the k bounds.

| Case | Claim under judgment | Judge | Deadline |
|---|---|---|---|
| **DR3-β** | β ∈ [2.42 ; 2.60], β₁ = +0.06 ± 0.31, \|κ\| < 0.24 | DESI DR3 | **2027** |
| **FRB-s** | baryon survival s = 1 (accretion) vs. s = 0.70 (CCBH) | localised-FRB catalogue N ≥ 120 | 2027–2028 |
| **W-universal** | w(z) universal across environments (Bottleneck) vs. void/wall dependence (Clock) — round 1: Δβ = +0.22 ± 0.23 | Pantheon+ × void catalogue | open |
| **k3-vs-0** | cosmological coupling k = 3 (CCBH) vs. k = 0 — living posterior | GWOSC O4 + Gaia + AGN | ongoing |

### The registries

Everything that fell, numbered, dated, with the mechanism of the fall:
[`MANQUEMENTS.md`](registres/MANQUEMENTS.md) (140 entries) ·
[`TRIAGE_DES_ATTAQUES.md`](registres/TRIAGE_DES_ATTAQUES.md) (real errors or false alarms) ·
[`TROIS_CHANTIERS.md`](registres/TROIS_CHANTIERS.md) ·
[`THEORIE_GOULET.md`](registres/THEORIE_GOULET.md) / [`THEORIE_HORLOGE.md`](registres/THEORIE_HORLOGE.md) ·
[`CONCLUSION.md`](registres/CONCLUSION.md) ·
[`ATLAS.md`](registres/ATLAS.md) (**19 models, one pipeline, one ranking — generated**, #150) ·
[`ETAT.md`](registres/ETAT.md) (generated, never written by hand) ·
[`LEDGER.md`](registres/LEDGER.md) (**the Ledger**: the baryon budget, #152) ·
[`TENSIONS.md`](registres/TENSIONS.md) (**the tensions registry**: living tensions with their arbiters carved in advance, #153) ·
[`AUDIT_2308.md`](registres/AUDIT_2308.md) (repository audit of 23/08: 38 scripts re-run, one published check found inert, six corrections propagated, what remains to do).

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
| **Périmé** | dead numbers surviving in documents (failure mode #1) — linter against `valeurs_canoniques.json`, blocking in CI | `python3 outils/perime.py [--tout]` |
| **Rejouer** | results that stop reproducing unnoticed — 14 scripts replayed against `ancres.json`, blocking in CI | `python3 outils/rejouer.py` |
| **État** | hand-copied counts that drift — ETAT.md generated from lock, index, triage, audience | `python3 outils/etat.py` |
| **Grand Livre** | models that consume without paying — the baryon budget per row (FRB, clusters, ω_b), an atlas column | `python3 outils/ledger.py` |
| **Greffier** | anomalies whose history gets rewritten — the living-tensions registry, arbiter carved before resolution | `python3 outils/greffier.py` |
| **Confronteur** | two computations of the same quantity that silently diverge — 5 independent pairs confronted | `python3 outils/confronteur.py` |

**Registre** is the foundation: the criterion lives in the script's docstring, `freeze` pins it
by SHA-256 in [`registre.lock`](outils/registre.lock), `verify` fails (exit 1, blocking in CI)
if it has moved. Amendment is possible — but public, in `RETRACTATIONS.md`.
91 files of the corpus are frozen, Registre included: it protects itself.

```console
$ python3 outils/registre.py verify
[registre] OK    scripts/voile_cisaillement.py
[registre] OK    outils/registre.py
[registre] OK    outils/scelle.py
…                                          # 91 files, exit 0
```

---

## For future researchers

- [`registres/POUR_2027.md`](registres/POUR_2027.md) — **the letter to whoever opens the seal**: what to check first, how to judge each case, the β warning written before DR3.
- [`REPRODUIRE.md`](REPRODUIRE.md) — every headline number, its command, its expected value, its runtime.
- License: code MIT, texts and visuals CC-BY 4.0 ([`LICENSE`](LICENSE)); citation: [`CITATION.cff`](CITATION.cff) (Zenodo DOI at the first tag).

## Structure

```
CLAUDE.md        project constitution: the nine rules, applied every session
papiers/         tex, pdf, and the figures they include
outils/          registre, adversaire, audience, ktracker, scelle + registre.lock + .json
scripts/         the 50 computation scripts (pre-registered criteria in the docstring)
registres/       MANQUEMENTS, TRIAGE, TROIS_CHANTIERS, CONCLUSION, theories, notebook
visuels/         interactive html (le_role.html: predictions and their tracking; atlas.html: the ranking; ciel_pantheon_v2: the data), plates
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

## What next

The six 2026 studies are specified and frozen in [`scripts/etudes_2026.py`](scripts/etudes_2026.py).
**E1 v0 run (23/08)**: [`registres/ETUDE_E1_v0.md`](registres/ETUDE_E1_v0.md) — Stopyra: Δβ = +0.10 ± 0.24; [round 2 Douglass DR7](registres/ETUDE_E1_manche2.md): three algorithms, all null (< 1.4σ, opposite signs). **UNIVERSAL across two judges.** [E3 on the real table](registres/ETUDE_E3_v1.md) (69 FRBs, Connor 2025): validation passed, **Δχ²(CCBH) = +4.7 (~2.2σ), f_d saturated at the edge**; accretion indistinguishable from ΛCDM — Paper C's mocks now have their real counterpart (#148). Then E4 → E2 (E3 closed in v1, #148). E5, E6, E7 closed. κ₋Δv also run (25/08): UNIVERSAL ([`registres/ETUDE_KAPPA_DELTAV.md`](registres/ETUDE_KAPPA_DELTAV.md)).

Public data: `sh donnees/TELECHARGER.sh` (fingerprints verified). Baseline re-run: β = 2.447 (SN+BAO); **full Planck re-run: Δχ² = −12.60, β = 2.589** (`planck_theta.py`, ~40 min, #146).

---

Édouard Lantenois — [@Dantenos](https://github.com/Dantenos) ·
[linkedin.com/in/edlanteno](https://linkedin.com/in/edlanteno)
