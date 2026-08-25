# Brouillon — demande de données à l'équipe Farrah (test κ(σ) BGG)

*Pour toi, Édouard : email prêt à envoyer (en anglais, destinataires anglophones). But :
obtenir la table par hôte (z, σ, M_BH, M_*) que κ(σ) BGG exige et qui n'est pas publique.
Destinataires suggérés : Duncan Farrah (auteur principal, Univ. Hawaï / Virginia Tech) et
Kevin Croker (théorie du couplage cosmologique). CC possible : Gregory Tarlé, Sara Petty.*

---

**Subject:** Data request — per-galaxy velocity dispersions for a k(σ) universality test of cosmological coupling

Dear Prof. Farrah, Prof. Croker,

I am an independent researcher working on a one-parameter, externally-sourced dark-energy model whose equation of state reduces to the Croker–Weiner cosmological-coupling relation applied to a parent black hole, w(z) = −k_eff(z)/3. A cross-level consistency test in that work compares the cosmologically-inferred coupling to the k ≈ 3 you measure for black holes within our universe (Farrah et al. 2023, ApJ 944, L31), and the central values are strikingly close.

I would like to run one discriminating test that your published letters, being aggregate, do not settle: **does the inferred coupling k depend on the host velocity dispersion σ?** If the coupling is genuinely cosmological (a background property), k should be independent of σ (dk/dlnσ = 0); a measured k(σ) trend would instead favour an astrophysical/environmental growth channel. This would sharpen — or falsify — both your result and my model's prediction P5.

To do this properly I need the **per-object** data underlying your samples, rather than a secondary summary:

- galaxy identifier, redshift z,
- **velocity dispersion σ** (and its uncertainty),
- black-hole mass M_BH (preferably direct/dynamical, and the method used),
- stellar mass M_* (and the aperture/photometry),
- sample membership (which of your samples each object belongs to).

The analysis is pre-registered: the success/failure criteria are frozen (by cryptographic hash) **before** I see the data — I bin by σ at equal counts, fit k independently per bin, report dk/dlnσ as measured (favourable or not), and cross-check with your own binning. I am happy to share the frozen protocol, run it jointly, or acknowledge the data however you prefer. Any per-object table, even partial, would let the test proceed.

Thank you for the work — it is one of the cleanest falsifiable claims in the field, which is exactly why I would like to stress it one notch further.

With respect,
Édouard Lantenois — github.com/Dantenos

---

*Note interne : une fois la table reçue, la déposer en `donnees/farrah2023_sigma_mbh.csv`,
l'empreinter dans `donnees/SHA256SUMS`, et la spec gelée `scripts/etude_kappa_sigma_bgg.py`
(70ed033cc3b0) tourne telle quelle. Voir `registres/ETUDE_KAPPA_SIGMA_BGG.md`.*
