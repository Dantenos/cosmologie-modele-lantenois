# LES TROIS CHANTIERS DE COMPLÉTUDE — état après la nuit du 24/08

## Chantier 1 — le bord : **CLOS (#134, E8-v2 après correction)**
Horloge exacte (contraction GR vérifiée 10⁻¹²) : **dτ_p/dt = [(1−s)+x·v_ff]/[(1−s)²−x²]**.
Le raccourci SR de #133 (γ(v_ff)) est RÉTRACTÉ — terme croisé de la paroi perdu. Résultats :
(a) **la borne historique est RÉHABILITÉE** : x₀ ≲ 0,30 (nulle) / 0,32 (poussière) — robuste
au choix d'extérieur à 7 %, elle mesurait la physique ; mon #59 (« 0,65 ») est retiré.
(b) Sur la bande basse tension, DEUX régimes : x₀ ≲ 0,15 → κ = 0,02-0,06 (prédiction : running
nul au-delà du spectre) ; x₀ = 0,2-0,3 → κ = 0,13-0,22 (**mesurable par β₁**).
(c) **β₁(DR3) devient une sonde directe du rayon du bord** : un nul confine x₀ ≲ 0,15, une
détection le localise.

## Chantier 2 — perturbations : **THÉORIE CLOSE, CHIFFRES DÉRIVÉS (#136) — E9 = CLASS**
Dérivation covariante exécutée (perturbations_derivees.py, gelé d3a41118) : composant =
POUSSIÈRE + SOURCE, δQ = 0 par le théorème des couches, création au repos comobile →
amortissements −(Q/ρ) dans δ' ET θ'. **La fourche CCDM est tranchée par dérivation.**
Contrôle ΛCDM passé (f = 0,5236 vs Ω^0,55 = 0,5263, 0,52 %). RÉSULTATS DÉRIVÉS :
δ_de/δ_m(a=1) = 0,055 ; contribution de source Ω_de·r = 0,038 ; **décalage fσ8-proxy = +3,7 %**
contre le ~1-2 % que le corpus SUPPOSAIT — nombre du corpus corrigé par le calcul, et la
direction (croissance accrue) va PLUTÔT CONTRE le modèle côté S8 : signalé tel quel.
Reste E9 (externe) : CLASS complet, k-dépendance, S8/lentillage — le papier A ne sera amendé
qu'après E9, pas sur un calcul sous-horizon.

## Chantier 3 — ε(ν) : **LA LITTÉRATURE A DÉJÀ CONSTRUIT LE PONT**
Recherche du 24/08 : le programme « profil de pic → profil de halo » existe et est actif :
- Dalal, Lithwick & Kuhlen 2010 (1010.2539) : l'origine des profils par contraction adiabatique
  des pics gaussiens ; étendu aux pics triaxiaux (Lithwick & Dalal 2011, → NFW).
- Delos, Bruff & Erickcek 2019 : « le profil d'un halo est uniquement relié aux propriétés de
  son pic précurseur », pour **spectre arbitraire**.
- Diemer & Kravtsov 2014 : la dépendance en hauteur de pic ν est mesurée en simulation.
- Et l'ancre exacte circule toujours : δM/M ∝ M^−ε autour d'un pic, ε relié au spectre.
Ce qui manque n'est donc PAS le formalisme — c'est sa **transposition** : calculer
ε(ν) = −dln(δM/M)/dlnM sur le profil moyen de pic BBKS à hauteur ν (formule exacte avec les
corrections γ,θ), puis β = 2/(3ε). Calcul borné, ingrédients nommés, une source (P(k)).
Le jour où il tourne, β cesse d'être une mesure : **le spectre du parent devient testable
contre 2,42-2,60.** Coût : jours. Spec à geler avant exécution.

## Bilan
Un chantier résolu (1 : forme fermée + κ(σ) chiffré), un tranché sur le papier et spécifié
(2 : covariance → lecture A dérivée ; CLASS reste à tourner), un fermé par la littérature et
réduit à une transposition bornée (3). La complétude n'est plus une liste de manques :
c'est une liste de calculs, chacun avec son coût et son juge.
