# LE REGISTRE DES TENSIONS — généré par `outils/greffier.py`, ne pas éditer à la main

*2026-08-24 — 9 tensions : 7 ouvertes, 0 en jugement, 2 résolues. Règle du greffe : une tension ne se*
*résout que par l'arbitre nommé avant la résolution — on ne réécrit pas l'histoire d'une anomalie.*

## T1-beta-interne — OUVERTE <small>(ouverte le 2026-08-23)</small>

**β marginalisé du fond léger (2,42 ± 0,07) contre β marginalisé du Planck complet (2,603 +0,046/−0,053) — chaîne (β₀,β₁) servie (#159) : β₁ = −0,25 ± 0,26, NON CONCLUANT (signe hérédité à 1σ) ; running libéré, la tension se dissout dans la dégénérescence β₀-β₁ (+0,88)**  
magnitude : **2,1σ** · refs : #151, #159

Lectures rivales :
- systématique (calibration SNe / nuisances plik figées)
- running réel dβ/dlnt < 0 — la prédiction de l'EDO d'hérédité (β₁ = −0,42, heredite_edo.py)

**Arbitre (gravé d'avance)** : β₁(DR3) — déjà dans le verdict scellé ; l'hérédité prédit −0,42, le bruit prédit 0, la chaîne locale ne tranche pas (#159)

## T2-omega-b — OUVERTE <small>(ouverte le 2026-08-24)</small>

**ω_b BBN (D/H) contre ω_b CMB — l'écart dépend entièrement du taux nucléaire d(p,γ)³He adopté**  
magnitude : **2,9σ (Cooke 2018, taux Marcucci) ou 0,3σ (Schöneberg 2024, conservateur)** · refs : #152, LEDGER.md R3

Lectures rivales :
- taux théorique Marcucci sous-estimé (systématique nucléaire)
- vraie physique entre BBN et recombinaison (aucun modèle de l'atlas n'en propose)

**Arbitre (gravé d'avance)** : mesures directes du taux d(p,γ)³He aux énergies BBN (programme LUNA et successeurs) ; la rangée R3 du Grand Livre enregistre

## T3-FAP — OUVERTE <small>(ouverte le 2026-08-19)</small>

**F_AP(2,33) mesuré contre prédit : le modèle à −1,7σ, ΛCDM à −0,8σ, CPL à −1,9σ — toute la classe dynamique tire du même côté**  
magnitude : **−1,7σ (défaite déclarée, gravée au papier A)** · refs : TRIAGE #3, papier A l.885

Lectures rivales :
- fluctuation (partagée par la classe)
- tension interne DESI (DR2-IV préfère Ωm = 0,325, à 1,4σ des BAO)
- vraie géométrie contre w(z) dynamique à z > 1

**Arbitre (gravé d'avance)** : Lyα DR3 (F_AP re-mesuré) — le point joint AP+BAO du protocole de mise à jour du papier A

## T4-union3 — OUVERTE <small>(ouverte le 2026-08-21)</small>

**Union3 tire β vers le bas (2,31), résidus localisés z = 0,65-1,4 — la région du croisement, pas les bins suspects de calibration**  
magnitude : **1,2σ du β de synthèse, 2,0σ du β Planck ; fissure ≈ 1,4 offsets-Efstathiou** · refs : papier A l.98, carnet l.170

Lectures rivales :
- méthodologie Unity (hiérarchique bayésien, incomparable objet à objet)
- systématique SN commune (Efstathiou vs Vincenzi)
- vraie physique dans la zone motrice

**Arbitre (gravé d'avance)** : Rubin/LSST (~2027-28) : une seule photométrie, plus de guerre de compilations

## T5-zx-fenetre — OUVERTE <small>(ouverte le 2026-08-24)</small>

**si β = 2,60 (Planck marginalisé), le croisement prédit tombe à z× ≈ 0,22 — sous la fenêtre indiquée par DESI (0,4-0,5, qui correspond à β = 2,38-2,45)**  
magnitude : **naissante — dépend du verdict de T1** · refs : #145, #151, croisement_fantome.py

Lectures rivales :
- T1 se résout côté systématique et β = 2,42 tient (z× = 0,44, dans la fenêtre)
- β = 2,60 réel et la fenêtre DESI actuelle est un artefact w₀wₐ

**Arbitre (gravé d'avance)** : reconstruction non-paramétrique de w(z) sur DR3 : localisation directe de z× — le β-mètre secondaire du papier A

## T6-vides-algorithmes — RÉSOLUE <small>(ouverte le 2026-08-23)</small>

**VoidFinder (+0,52 ± 0,38) et VIDE (−0,40 ± 0,35) donnent des Δβ de signes opposés sur la même empreinte — écart 0,92 pour un seuil de divergence gelé à 1,04**  
magnitude : **1,8σ entre juges (sous le seuil NON EXPLOITÉ, de peu)** · refs : #142, ETUDE_E1_manche2.md, #155

Lectures rivales :
- le « vide » n'est pas univoque (Jaccard 0,33 : ils trient des SNe différentes — expliqué, pas contradictoire)
- fluctuations pures à N ≈ 228 par moitié

**Arbitre (gravé d'avance)** : manche 3 sur catalogue profond (DESI voids) avec les MÊMES algorithmes : si les signes restent opposés à grand N, la définition du vide devient elle-même l'objet

**Résolution** (2026-08-24, #155) : FLUCTUATIONS (bruit à petit N) — par le critère gelé de l'arbitre ; RÉSERVE : la branche ne conditionne pas sur la puissance (σ_Δ ≈ 0,7-1,0 ici) ; clause de réouverture : tout test des mêmes algorithmes à σ_Δ ≤ 0,4. Indice de soutien : Jaccard(VIDE,REVOLVER) = 0,97 sur DESIVAST contre 0,41 sur Douglass — par l'arbitre nommé.

## T7-epsilon-ilcdm — RÉSOLUE <small>(ouverte le 2026-08-24)</small>

**RÉSOLUTION RÉTRACTÉE (#166) — l'avance de l'iΛCDM sur l'atlas (ε ≈ +0,021, −9,8) est à 8,62/9,84 un ARTEFACT D'ÉTALONNAGE : même fond que wCDM (identité à 4,4e−16), mais r_d, z_*, r_* et R calculés avec l'étiquette Ω_m au lieu de la densité d'avant recombinaison Ω_m′. Le modèle cohérent gagne +1,21, derrière l'accrétion (+5,78) et CPL (+6,16). Les trois volets de l'arbitre (#154, #156, #158) ont tourné dans le pipeline vicié et ne valent plus. Question rouverte : reste-t-il UNE préférence pour un échange sombre à étalonnage cohérent ? À ce jour : +1,21, soit rien.**  
magnitude : **ΔAIC = −3 à −4 sur CCBH/accrétion — au tableau, pas au palmarès** · refs : #150, ATLAS.md, #154, #156, #158, #166, #167, #173

Lectures rivales :
- artefact de l'implémentation v1 (échange appliqué à toute la matière + fond tardif incohérent avec les distance-priors primordiaux — déclaré au gel)
- vraie préférence pour l'échange sombre (des indices similaires existent dans la littérature DESI)

**Arbitre (gravé d'avance)** : un atlas v2 dont l'étalonnage (r_d, z_*, r_*, R) est tiré de la densité de matière d'AVANT recombinaison pour chaque modèle, et non de son étiquette Ω_m ; plus une étude propre sur 'ilcdm_dm', dont la matière dérive de −4,76 % à a = 1e−3 (diagnostic #166, verdict non rendu)

**Résolution** (2026-08-24, #167) : PAR LA NÉGATIVE : à étalonnage cohérent (densité de matière d'AVANT recombinaison, et non l'étiquette Ω_m), l'iΛCDM 'de' gagne +1,21 sur un profil BILATÉRAL (les deux signes de ε accessibles) ; l'iΛCDM 'dm' voit sa contrainte se resserrer à |ε| ≲ 0,0005 et sa détection à +0,0071 disparaître. RÉSERVE PORTÉE (#173) : pour 'dm' la branche ε < 0 est inaccessible par construction (ρ_de → −∞ si l'on impose la conservation totale), donc son verdict est UNILATÉRAL — il vaut dans la moitié accessible, ce qui est aussi la seule moitié qu'avait explorée le fit d'origine de l'atlas. Il ne reste aucune préférence pour un échange sombre. L'accrétion (+5,78, un paramètre) redevient première à l'AIC — par rétractation du rival, ce qui ne lui ajoute aucun mérite propre. — par l'arbitre nommé.

## T8-patch-desivast — OUVERTE <small>(ouverte le 2026-08-24)</small>

**β ajusté sur les 227 SNe Pantheon+ de l'empreinte DESIVAST (deux calottes BGS, z médian 0,12) = 1,84 ± 0,31, contre 2,45 ± 0,22 pour des tirages aléatoires de même taille — le patch est bas, pas l'échantillonnage — disséqué #157 : le creux vit à z = 0,15-0,5 (−46 ± 15 mmag), porté à 82 % par les SNe SDSS, et DANS le même relevé le différentiel dans/hors zone est −52 mmag**  
magnitude : **1,9σ sous 2,42 (candidat, sous le seuil de 2σ — ouvert au greffe, pas affirmé)** · refs : #155, ETUDE_E1_manche3.md, #157

Lectures rivales :
- systématique de calibration localisée (patchs photométriques bas-z de Pantheon+)
- fluctuation (1,9σ, un patch parmi d'autres — effet de sélection du regard)
- vraie dépendance directionnelle/environnementale de w — la lecture horloge par la petite porte

**Arbitre (gravé d'avance)** : re-spécifié #157 (l'overlap DES est insuffisant : 40 SNe à z̄ 0,04, constaté) : structure de calibration de la bande 82 (über-cal/DR16) sur la zone des vides SGC ; recalibration croisée Dovekie SDSS-DES ; à défaut LSST

## T9-source-externe-vs-interne — OUVERTE <small>(ouverte le 2026-08-24)</small>

**les deux vainqueurs du corpus (accrétion β, échange ε) paramétrisent la MÊME fonction s(a) = d ln ρ_de/d ln a (#161, identité algébrique vérifiée à 1e-4) ; ils ne diffèrent que par la SOURCE — hors budget (matière intacte) ou interne (la matière encaisse). À paramètres égaux l'interne mène de Δχ² = +2,83 (~1,7σ), et n'a besoin d'aucun croisement ; l'externe exige une pente qui court (2,4σ par rapport de vraisemblance contre wCDM) et croise en z₀ = 0,240 [0,090 ; 0,340] — versé par critère gelé (#163) : sur Planck complet la même forme libre exige le running à 3,72σ (une pente CONSTANTE n'achète rien, +0,04) mais place le croisement en z₀ = 0,388 [0,377 ; 0,387], disjoint et de la bande rigide [0,218 ; 0,262] et de la mesure légère [0,090 ; 0,340] : le croisement est dominé par le systématique de forme, pas par les données — ATTENTION (#166) : le volet « la lecture interne mène de +2,83 » est RÉTRACTÉ, cet avantage était l'artefact d'étalonnage. L'identité algébrique entre les deux lectures tient (c'est de l'algèbre) ; le classement entre elles, non. À étalonnage cohérent, l'échange sombre ne mène plus rien.**  
magnitude : **Δχ² = 2,83 entre lectures, ~1,7σ — indécidable aujourd'hui ; mais le discriminant prédit est net : 1,70 % d'écart de matière entre la recombinaison et le bas redshift (interne) contre 0,00 % (externe)** · refs : #161, confluence.py, #150, #154, #163, #166

Lectures rivales :
- SOURCE EXTERNE (la thèse du corpus) : ρ_de est alimentée hors budget, la matière dilue exactement en a⁻³. Prix à payer : la pente s(a) doit courir et croiser zéro (2,4σ) ; ajustement moins bon de 2,83.
- ÉCHANGE INTERNE (le vainqueur de l'atlas) : le secteur sombre se transvase, ε ≈ 0,023 constant, aucun croisement requis, meilleur ajustement — mais la matière n'est plus conservée : −1,70 % à la recombinaison.
- NI L'UN NI L'AUTRE : les 2,83 unités séparant les deux lectures sont du bruit de systématiques SN/BAO à bas z (canal déjà identifié au #148 et à T8), et s(a) n'est pas mesurée du tout.
- LE CROISEMENT N'EST PAS MESURABLE AUJOURD'HUI (lecture ouverte par #163) : les quatre déterminations de z× (2 formes × 2 jeux) s'étalent de 0,23 à 0,44 sans tendance cohérente, pour des écarts de χ² inférieurs à 1,3 — tant que ce systématique de forme n'est pas maîtrisé, aucun z× publié, le nôtre compris, ne contraint quoi que ce soit.

**Arbitre (gravé d'avance)** : la dilution de la matière : tout jeu contraignant ω_m à mieux que ~1 % SIMULTANÉMENT à la recombinaison (Planck/ACT/SPT) et à bas redshift (DR3 BAO + amas + croissance). Si l'écart mesuré est compatible avec 0 à moins de 1 %, la lecture interne à ε ≈ 0,023 est exclue et l'externe survit ; s'il vaut 1,5-2 %, c'est l'inverse. Aucun des deux modèles n'a le droit de réajuster ε ou β après coup pour absorber l'écart (règle 5 : ils gardent h, ω_b, Ω_m, rien de plus)

