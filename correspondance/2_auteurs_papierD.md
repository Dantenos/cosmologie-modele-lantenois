# Messages aux auteurs engagés par le papier D

> **Pourquoi écrire avant de soumettre, et pas après.** Le papier D discute des résultats
> publiés par quatre groupes. Deux raisons de les prévenir : c'est la courtoisie normale, et
> surtout un auteur prévenu qui te corrige **avant** soumission t'épargne un référé hostile
> qui te corrigera après. Sur ce corpus, trois vérifications ont déjà démoli des affirmations
> que j'étais prêt à publier — mieux vaut que la quatrième vienne d'un e-mail que d'un rapport.
>
> **Règle de rédaction :** dire exactement ce que le papier affirme *et* ce qu'il n'affirme
> pas. Ne jamais laisser croire à une réfutation quand il s'agit d'une mise en garde de méthode.

---

## A. Kumar, Ajith & Verma — arXiv:2504.14419

*Leur mesure PL18+DESI DR2 est la référence en vraisemblance complète du papier D.*

**Objet :** `Your w_dm = 0.00077 ± 0.00038 used as a full-likelihood reference — a check on my conversion`

> Dear Dr Kumar, Dr Ajith, Dr Verma,
>
> I am an independent researcher in Lille. Your ΛwDM constraint from PL18+DESI DR2 plays a
> load-bearing role in a methods paper I am preparing, and I would rather have you check one
> step than discover I got it wrong in review.
>
> **The conversion.** My family is written ρ_dm ∝ a^(−3+ε) with Λ constant, which the Bianchi
> identity forces to be a fluid with w = −ε/3. I therefore read your
> w_dm = +0.00077 ± 0.00038 as **ε = −3w_dm = −0.00231 ± 0.00114**, on dark matter only, with
> baryons at a^−3. Is that the reading you would endorse?
>
> **What the paper claims.** Not a measurement. It shows that on identical data, four
> bookkeeping choices in the *compressed* distance priors move ε over a range of 0.019 while
> each quotes σ ≈ 0.002 — and that this is not information loss, since the compressed priors
> constrain ω_c as tightly as the full Planck likelihood does. Your measurement appears as one
> of six full-likelihood determinations that, by contrast, cluster within 0.005.
>
> **What it does not claim.** It does not question your result. It does record, from your own
> abstract, that DESI+DESY5 gives w_dm = −0.084 ± 0.035 while PL18+DESI gives +0.00077 —
> opposite sign, two orders of magnitude — because a sign reversal between datasets inside one
> paper is directly relevant to my point about how fragile this parameter is. I hope that is a
> fair reading of what you yourselves flag as a tension.
>
> Two caveats I state in the paper and would welcome correction on: your w_dm carries a
> perturbation prescription (c_s² = 0, c_a² = w_dm) that a background-only ε does not, so the
> numerical value is arguably not transferable; and your paper does not name the Planck
> likelihood variant, so I describe it as "P18 + lensing" without further precision.
>
> Manuscript and code: [LIEN] — I would send the PDF directly if that is easier.
>
> With thanks,
> Édouard Lantenois

---

## B. Yang, Dai & Wang — arXiv:2505.09879

*C'est le message le plus délicat : mon corpus a d'abord mal résumé leur résultat, et je l'ai
rétracté au greffe (#195). Le message doit le dire.*

**Objet :** `A correction I made to my own summary of your ε constraint`

> Dear Prof. Yang, Dr Dai, Dr Wang,
>
> I am an independent researcher in Lille, preparing a methods paper on the identifiability of
> the dark-matter dilution exponent from compressed CMB priors. Your constraint
> ε = −0.0073 (+0.0029/−0.0033) is discussed in it, and I am writing partly to correct
> something on my side.
>
> **My error, now retracted in my own record.** In earlier working notes I summarised your
> result as "compressed priors + DESI give ε = −0.0073 at 2.4σ". That was an omission that
> converted a null into a detection: the 2.4σ requires five datasets, and your paper states
> plainly that DESI+CMB+CC alone gives ε = +0.0023 (+0.0055/−0.0067), concluding there is no
> significant deviation. The corrected reading is now in my public register, and the paper
> quotes both of your values.
>
> **What my paper argues.** In this family the compressed priors and the fitting formulas for
> r_d, r_*, z_* each need one ω_m, and when ε ≠ 0 there are two — the present-day label and
> the value at recombination. I measure that this choice alone moves ε by 0.019 on fixed data.
> I note that your Eq. (11) defines R with a symbol Ω_M that is never reconciled with the
> 3Ω_dm,0/(3−ε) coefficient in your own Friedmann equation, and that your z_* comes from
> Hu & Sugiyama, which assumes ρ_m ∝ a^−3. I raise this as a question about the method, not as
> a claim that your number is wrong — my data, pipeline and nuisance treatment all differ from
> yours, and I say so explicitly.
>
> **One thing I could not resolve** and would be grateful for a word on: your abstract and
> conclusion write ρ_m ∝ (1+z)^(3−ε) while the body writes ρ_dm. The difference matters for
> anyone converting your ε — it is a factor ρ_dm/ρ_m ≈ 0.84. Which is intended?
>
> If you think I have misread anything, I would much rather hear it now than from a referee.
>
> Respectfully,
> Édouard Lantenois

---

## C. Tsiapi & Basilakos — arXiv:1810.12902

*Leur article est le seul en vraisemblance complète sur le cousin conservé ; le papier D
l'emploie avec une réserve déclarée.*

**Objet :** `Your Λ(H)CDM2 constraint used in a methods comparison — a declared caveat`

> Dear Dr Tsiapi, Prof. Basilakos,
>
> I am an independent researcher in Lille. Your Λ(H)CDM2 constraints — ν×10³ = 0.59 ± 1.0
> (Planck alone) and −0.08 (+0.72/−0.78) (joint) — appear in a methods paper I am preparing,
> as two of six determinations obtained with a modified Boltzmann code and a full CMB
> likelihood, rather than with compressed distance priors.
>
> **The caveat I state, and would like to be sure I state correctly.** I convert your ν to a
> dilution exponent via ε = 3ν, then multiply by the dark-matter mass fraction to express it on
> total matter. But your Eq. (15) makes ρ_Λ run, and Eq. (16) carries a Ω_dm/(1−ν) prefactor —
> so at equal ε your H(z) is not that of a constant-Λ law. The paper therefore says the
> conversion reproduces the *matter dilution rate and nothing else*, and that your interval is
> not transferable to a background-only law. Is that the limitation you would place on it?
>
> I also record your conclusion verbatim: "We find that Λ(H)CDM2 and Λ(H)CDM3 do not show
> deviations from the ΛCDM case."
>
> Your paper is, as far as I can find, the only full-CMB-power-spectrum treatment of this model
> class — every other analysis I located uses SNe, BAO, H(z) or a compressed CMB. If you are
> aware of a more recent one I have missed, I would be glad to know.
>
> With thanks,
> Édouard Lantenois

---

## D. Bengaly, Andrade & Alcaniz — arXiv:1810.04966

*Ce message-là est un remerciement, pas une discussion : leur résultat a fermé un trou réel
dans mon corpus.*

**Objet :** `Your footprint result closed a real hole in my analysis — and a number you may want`

> Dear Dr Bengaly, Dr Andrade, Prof. Alcaniz,
>
> I am an independent researcher in Lille. I am writing to thank you concretely, and to offer a
> number back.
>
> Your finding that a non-uniform footprint alone moves a hemispherical H₀ statistic from 3.4σ
> to 2.7σ prompted me to audit my own null ensembles. Two of them already preserved the SN
> angular positions (rotating a void catalogue, and permuting labels among the observed
> supernovae). One did not — an early hemispheric test — and I had never checked it.
>
> **The number.** I re-ran it with 300 randomly oriented split axes, the 1580 Pantheon+
> positions never moved. The null width came out at σ = 0.2318 against the 0.2300 my covariance
> had claimed (ratio 1.01), and the observed value sits at p = 0.433 — entirely ordinary. My
> result survived. But the 68% quantile of |Δβ| over random axes is **1.14σ**, i.e. in my
> pipeline the footprint alone can manufacture appreciably more apparent signal than the ~0.7σ
> you measure in yours. Any future hemispheric claim of mine below ~1.1σ is therefore worthless
> without a footprint-preserving null. That threshold exists because of your paper.
>
> I mention this in case a second independent estimate of footprint-manufactured significance
> is of any use to you. Your MC-iso1/MC-iso2 prescriptions are cited in my work.
>
> With thanks,
> Édouard Lantenois
