# Courrier aux auteurs du cadre de création de particules — brouillon

**Destinataires** : Tiziano Schiavone (SISSA/INFN, tiziano.schiavone@sissa.it),
Giovanni Montani (ENEA/Sapienza, giovanni.montani@enea.it),
Eleonora Di Valentino (Sheffield, e.divalentino@sheffield.ac.uk),
Mariaveronica De Angelis (UCM), Luis A. Escamilla (ITU)

**Référence** : arXiv:2601.14222, *Revisiting the Matter Creation Process* (PRD 2026)

**Statut** : à relire par Ed avant envoi. Ton : question technique, pas revendication.
Ne rien affirmer sur leur analyse au-delà de ce qui est vérifié.

---

**Objet** : A closed-form Γ ∝ 1/t in your particle-creation framework, and a question about
the w_E constraint

Dear Dr Schiavone, dear colleagues,

I am an independent researcher working on a dark-energy component sourced externally rather
than internally, and your recent paper resolved something for me: the model I had been treating
as an exotic construction turns out to be a special case of your framework. I would like to
report the identity, and then ask you one technical question.

**1. The identity.** Your Eq. (48), w_DE^eff = w_E − (Γ/3H)(1 + w_E), with w_E = 0 (pressureless
created mass) and Γ = Ṁ/M = β/t, returns w(z) = −β/(3Ht) — the equation of state I had derived
from a completely different starting point. The two continuity equations coincide exactly, since
Γ ρ_E a³ = (Ṁ/M) M = Ṁ.

**2. A fifth rate law, with a closed-form solution.** For Γ = β/t, your Eq. (19) integrates
analytically:

  g(z) = (1+z)^{3(1+w_E)} · (t/t₀)^{β(1+w_E)}

which I have verified against direct numerical integration of your ODE to 1.4 × 10⁻⁶ over
0 < z < 5. This is not among the four parametrisations of your Table I, and three of those four
require a numerical solution. It may be worth adding to the family. Its interest, relative to
your closing remark that "the parametrisation of the particle-creation rate remains
phenomenological", is that here Γ is not parametrised at all: it is the accretion rate of an
external reservoir, so β is inherited rather than fitted as a free rate.

**3. The question.** I tried to reproduce your constraint on w_E in an independent pipeline
(Pantheon+ with the full covariance, DESI DR2 BAO, Planck 2018 distance priors (R, l_A, ω_b)
with their covariance, a SH0ES H₀ prior, and a forecast for the cosmic chronometers). The
pipeline reproduces your ΛCDM fit closely — I obtain H₀ = 68.7 and Ω_m0 = 0.298 against your
68.85 ± 0.43 and 0.296 ± 0.005 — but for PC1 I find only Δχ²(w_E = 0) ≈ 0.3 in the profile
likelihood, where you report an exclusion at 4.7σ.

Chasing the difference, I found that in PC1 the present-day effective equation of state is
w_eff(0) = w_E − b(1 + w_E), so for any target value c the equation b = (w_E − c)/(1 + w_E) has a
solution for every w_E ≠ −1. The profile likelihood is therefore flat in w_E at z = 0 by
construction, and I verify this numerically: along my whole profile, w_eff(0) stays at
−0.945 ± 0.002 while w_E runs from −1.5 to 0. Conversely, your Table VI reports
w_DE^eff(0) = −0.99 (+0.02/−0.03), and combined with the same algebra a 2 % constraint on
w_eff(0) does force w_E → −1 quite sharply.

My question is simply: what breaks this degeneracy in your analysis? Is the w_E constraint
carried by the higher-redshift shape through α, by prior volume in the marginalisation over
(α, β), or by something in the pipeline I am failing to reproduce? I ask because the answer
determines whether your exclusion of pressureless creation (w_E = 0) applies to rate laws
outside your four families — which is exactly the case for the model above.

I would be very glad to share my scripts, and grateful for any comment, or for the chains if
you are willing.

With thanks and best regards,

Édouard Lantenois
github.com/Dantenos

---

## Notes internes (à retirer avant envoi)

- **Ne pas affirmer** que leur résultat est un artefact. La dégénérescence est démontrée ;
  son effet sur *leur* chiffre ne l'est pas, faute d'accès à leur pipeline.
- **Vérifié avant envoi** : identité (écart 0,00), solution analytique (1,4e−6),
  V1 (H₀ = 68,66 / Ω_m = 0,2976), dégénérescence (w_eff(0) = −0,945 ± 0,002 sur le profil),
  et l'élimination des cinq explications alternatives (profilage de q, marginalisation,
  coupure z < 3, précision du CMB, chronomètres).
- **Non vérifié, ne pas prétendre** : que les chronomètres réels (et non ma prévision) ne
  changent rien ; que la covariance CMB corrélée est identique à la leur.
- Ce courrier est indépendant de celui à Popławski (question sur les e-plis de vorticité) :
  ne pas les fusionner, les destinataires n'ont rien à voir.
