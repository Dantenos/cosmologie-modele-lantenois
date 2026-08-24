# Enquêtes de pertinence auprès des revues (pre-submission inquiry)

> **À quoi ça sert.** Une enquête de pertinence coûte cinq lignes et une semaine d'attente, et
> évite trois mois de rejet pour hors-sujet. Elle est particulièrement utile ici parce que les
> deux papiers visent des lectorats **différents** : D est de la cosmologie, F est de la
> méta-science. Les envoyer au même endroit serait une erreur.
>
> **Ordre :** arXiv d'abord, revue ensuite. Un préprint arXiv daté protège l'antériorité
> pendant que la revue délibère, et aucune des revues visées ne l'interdit.

---

## A. Papier D — cosmologie

**Cible naturelle : JCAP.** C'est un résultat de méthode sur l'inférence cosmologique, pas une
mesure ; JCAP accueille ce registre plus facilement que MNRAS ou A&A, qui attendent plutôt un
résultat observationnel. MNRAS reste une bonne seconde option.

**Objet :** `Pre-submission inquiry — identifiability of the matter dilution exponent from compressed CMB priors`

> Dear Editor,
>
> I would like to ask whether the following would fall within the scope of [REVUE].
>
> **Title.** Pre-registered scientific criteria are not the subject; this is a cosmology
> methods result: *The matter dilution exponent is not identifiable from compressed CMB priors:
> a referent ambiguity, not a precision limit.*
>
> **Result.** In the family ρ_dm ∝ a^(−3+ε) with a genuine cosmological constant, the
> compressed CMB distance priors (R, ℓ_A, ω_b) and the standard fitting formulas for r_d, r_*
> and z_* each require a single value of ω_m. When ε ≠ 0 there are two — the present-day label
> and the value at recombination — and nothing in the data selects one. On identical data
> (Pantheon+, DESI DR2, Planck 2018 priors, SH0ES) this bookkeeping choice alone moves the
> recovered exponent from +0.0070 to −0.0120, a range of 0.019, while every configuration
> quotes σ ≈ 0.002.
>
> The paper then shows this is not an information-loss effect: the compressed priors constrain
> ω_c to σ = 0.0010, identical to what the full Planck TT,TE,EE+lowℓ likelihood delivers under
> the same fixed parameters. Published determinations obtained with a modified Boltzmann code
> cluster within 0.005; those obtained with compressed priors span 0.016.
>
> **What it does not claim.** No detection of ε, and no refutation of any published
> measurement. It is a warning with a number attached: a published ε from compressed priors
> carries an unquoted systematic of order 10⁻², an order of magnitude above the statistical
> error usually reported, unless the choice of ω_m is stated.
>
> Length ~10 pages. All analysis code and the frozen success criteria are public.
>
> Would this be of interest?
>
> Yours sincerely,
> Édouard Lantenois — independent researcher, Lille, France

---

## B. Papier F — méta-science

**Le lectorat n'est pas celui de la cosmologie.** Le papier affirme que les critères
pré-enregistrés sont des *spécifications* et héritent de leur pathologie connue — vacuité,
insatisfiabilité, dérive. Cibles plausibles, par ordre :

| revue | pourquoi | risque |
|---|---|---|
| **Royal Society Open Science** | publie déjà des audits d'adhésion au pré-enregistrement | large, donc concurrentiel |
| **AMPPS** | la revue de référence des méthodes ouvertes | très orientée psychologie |
| **PLOS ONE** | scope explicitement méthodologique, pas de critère de nouveauté | prestige moindre |
| **Un atelier de génie logiciel** (ICSE-NIER, workshops) | c'est le domaine qui a *nommé* la vacuité | lectorat qui connaîtra déjà la moitié du papier |

**Objet :** `Pre-submission inquiry — pre-registered criteria as specifications: eleven observed failures`

> Dear Editor,
>
> I would like to ask whether the following would fall within the scope of [REVUE].
>
> **Claim.** A pre-registered success criterion is a predicate a computation must satisfy for a
> claim to count as established — that is, a *specification*. It therefore inherits the known
> pathology of specifications. I report eleven criterion failures observed during one intensive
> computational-cosmology campaign (89 hash-frozen criteria, 201 register entries) and map each
> onto a class already named outside the field: vacuity, unsatisfiability, specification drift,
> parameter-on-a-boundary, flaky floating-point comparison, weak comparator, insufficient test
> sensitivity.
>
> **I explicitly claim no new failure mode.** One of the eleven — a validation passing at 10⁻⁴
> relative while the quantity it converted did not exist — is vacuity, named in 1997, whose
> canonical example is mine with a tolerance in place of a temporal operator. The contribution
> is the *transfer*, plus an empirical instance count.
>
> **What distinguishes it from existing work.** The published taxonomies of pre-registration
> failure are behavioural: they classify what a researcher does, and speak of malicious
> researchers. Every failure I report occurred with no misconduct whatever — each criterion was
> written by an analyst trying to be rigorous and passed a reading when frozen.
>
> The paper also reports one failure the protocol cannot catch: after three frozen designs
> blocked on the same question, a fourth would have passed. Writing it would have been p-hacking
> one level up. Hash-freezing protects each study; it does not protect the series.
>
> Length ~8 pages. The full register, including every retraction, is public.
>
> Would this be of interest?
>
> Yours sincerely,
> Édouard Lantenois — independent researcher, Lille, France

---

## Deux mises en garde de rédaction

1. **Ne jamais soumettre D et F au même endroit en même temps.** Ils partagent un corpus et une
   moitié de leurs mises en garde ; un même éditeur y verra une seule contribution découpée.
2. **Dans le message à une revue de méta-science, ne pas cacher que la moitié du papier est du
   déjà-nommé.** Le dire soi-même en deuxième phrase — comme ci-dessus — est ce qui rend le
   reste crédible. Un référé de méthodes formelles le verra en un paragraphe ; mieux vaut qu'il
   le lise dans ton résumé.
