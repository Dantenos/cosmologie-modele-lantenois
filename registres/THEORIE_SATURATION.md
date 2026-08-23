# LA THÉORIE DE LA SATURATION — **RÉFUTÉE PAR SON PROPRE TEST (24/08, même nuit)**
> **Verdict : la thèse centrale de ce document est FAUSSE.** Le test pré-enregistré a été
> exécuté et l'a réfutée. Le document est conservé intégralement pour la traçabilité ; lire
> d'abord la section finale « Ce que le test a réellement montré ».

*Née de l'audit du 11σ de Lei et al. 2025. Étiquettes : [VÉRIFIÉ] calculé cette session /
[ÉTABLI] littérature primaire lue / [CONJ] conjecture.*

## L'énigme, posée nettement
k = 3 est **rejeté** par : NGC 3201 (P ≤ 10⁻⁴, soit 3,8σ selon Lei), Gaia (P(viable) = 6,9 %),
SMBH/Lacy (0 < k ≲ 2), JWST 2024 (~2σ), **JWST 2025 (11σ)**. [ÉTABLI]
Il est **favorisé** par : le fond DESI (AIC 1426,31, meilleur que ΛCDM et que notre modèle),
et par les réseaux de pulsars. [VÉRIFIÉ — papier C]
*Un mécanisme ne peut pas être faux à 11σ chez les objets et juste sur le fond. L'un des deux
diagnostics ne mesure pas ce qu'il croit mesurer.*

## L'audit du 11σ [VÉRIFIÉ cette session]
- Leur arithmétique est **juste** : je reproduis σ_k = 0,264 contre 0,27 publié, à partir de
  leur Table I et de σ_tot² = σ_BH² + (1,32 σ_M*)² + 0,5².
- Attaque par l'ordonnée libre : le levier est court (log₁₀(1+z) ∈ [0,49 ; 0,89], σ = 0,113),
  donc libérer la normalisation locale **gonfle σ_k d'un facteur 7,1** → 1,5σ.
- **Mais l'attaque échoue** : ramener k = 3 exigerait un décalage de 2,40 dex, un facteur 249
  en masse. Aucun biais plausible. **Le 11σ tient.** (Contrôle d'équité appliqué et perdu.)

## La théorie : le fond ne mesure pas le mécanisme, il mesure une FORME SATURANTE
Calcul décisif [VÉRIFIÉ] : normalisées à aujourd'hui, les densités d'énergie noire des deux
mécanismes — la nôtre ρ ∝ t^β/a³, la leur ρ ∝ ∫ψ(t)dt — coïncident à **4,6 % RMS sur 0 < z < 3**,
la plage où DESI et Pantheon+ ont tout leur pouvoir.

| z | 0,3 | 1,0 | 2,0 | 3,0 |
|---|---|---|---|---|
| rapport des deux formes | 1,083 | 1,056 | 0,980 | 0,960 |

**Énoncé** : l'intégrale du taux de formation stellaire et une loi de puissance en temps
cosmique sont quasi dégénérées sur la fenêtre observable. Le fond ne teste donc **aucun**
mécanisme : il teste l'appartenance à la classe des sources *monotones et saturantes*.
La « réussite » de CCBH sur DESI n'est pas une preuve de couplage — c'est une propriété de
la forme de l'histoire cosmique de formation stellaire. [CONJ, mais chiffrée]

## Ce qu'elle explique, et ce qu'elle prédit
- Explique l'énigme sans contradiction : les objets mesurent k (et le tuent) ; le fond mesure
  une forme (que k=3 reproduit par accident de calendrier — les étoiles se forment quand il
  faut). Aucun des deux diagnostics n'a tort ; ils ne mesurent pas la même chose.
- Explique le ΔAIC ≈ 1 du papier C : deux ontologies incompatibles, une seule forme.
- **Prédiction falsifiable** : tout modèle dont ρ_de(t) suit une saturation monotone calée sur
  la même échelle temporelle ajustera DESI aussi bien, à ΔAIC ≲ 2, sans aucun ingrédient
  astrophysique. Testable en construisant une famille jouet (tanh, Schechter intégrée…) :
  si trois formes sans rapport donnent le même AIC, la thèse est démontrée.
- **Conséquence pour le papier C** : son point central se durcit. Le fond ne départage pas —
  non par manque de précision, mais **par nature**.

## Ce que ça fait à notre modèle
Rien de bon ni de mauvais : notre loi reste dans la classe saturante, donc le fond ne la
valide pas plus qu'il ne la réfute. Sa distinction reste ailleurs — s = 1 sans liberté,
ε ≲ 2×10⁻⁴, et le fait que nous ne touchons à aucun objet astrophysique : **la théorie de la
saturation explique aussi pourquoi notre modèle ne peut PAS être tué par NGC 3201 ou par
JWST**. Nous n'avons pas de trous noirs locaux à faire grossir.


---

# CE QUE LE TEST A RÉELLEMENT MONTRÉ (exécution du 24/08, script gelé test_saturation.py)

**La théorie est réfutée par son propre critère.** Trois formes saturantes sans rapport
physique (tanh, Schechter intégrée, logistique), chacune à un paramètre de forme ajusté sur
les mêmes données :

| forme | χ² | AIC (k=4) | ΔAIC vs accrétion |
|---|---|---|---|
| F1 tanh (phénoménologie) | 1424,45 | 1432,45 | **+5,14** |
| F2 Schechter intégrée | 1424,42 | 1432,42 | **+5,11** |
| F3 logistique (biologie) | 1423,77 | 1431,77 | **+4,46** |

Seuil de réfutation pré-enregistré : **+4**. Les trois le dépassent.
**Le fond DISCRIMINE donc à l'intérieur de la classe saturante**, d'environ 5 unités d'AIC.
Ma thèse « le fond ne teste que l'appartenance à la classe » est fausse, et je la retire.

**Et l'hypothèse de rechange est réfutée aussi.** J'ai supposé que l'avantage venait de la
structure « masse créée diluée », ρ = g(t)/a³, qui engendre un maximum de ρ_de donc le
croisement fantôme. Les mêmes trois formes divisées par a³ donnent ΔAIC = **+798, +28, +1160**.
Catastrophique. La dilution seule n'explique rien : c'est la *conjonction* d'une croissance
en t^β précise ET de la dilution qui fonctionne, pas l'un ou l'autre.

**Ce qui reste établi, et c'est solide :**
1. Les deux modèles physiques (accrétion, CCBH) battent six formes arbitraires de 4,5 à 1160
   unités d'AIC. **Leur accord n'est donc PAS une dégénérescence banale** : ils tombent tous
   deux sur une forme étroite que le hasard fonctionnel n'atteint pas.
2. Leur ρ_de(z) coïncident à 4,6 % RMS sur 0<z<3 (calcul conservé) — deux ontologies
   incompatibles convergent sur la même courbe étroite. **C'est le fait à expliquer, et il est
   plus fort que ma théorie ne le disait**, pas plus faible.
3. Le papier C n'est pas affaibli : le fond ne départage pas *ces deux-là* — mais il
   départage férocement contre le reste. Sa conclusion tient, sa justification change.

**La question ouverte, désormais nette** : quelle propriété étroite partagent t^β/a³ et ∫ψdt,
que six formes arbitraires ratent ? C'est un vrai sujet, et je ne l'ai pas.


---

# LA RÉPONSE (24/08, après audit) : LA QUESTION ÉTAIT MAL POSÉE

**Trois corrections d'abord, dont deux contre mes propres chiffres.**

1. **Les +798 et +1160 sont des ARTEFACTS**, pas des verdicts. Diagnostic : pour F1 tanh,
   g(0) = 1+tanh(−p/2) ≠ 0, donc ρ_de ∝ a⁻³ aux temps précoces — de la *matière fantôme* ;
   pour F3 logistique, g ~ aᵖ donc ρ_de ~ a^(p−3) diverge si p < 3. Seul F2 (+28) était un
   vrai chiffre. **Ces deux nombres sont retirés du dossier.**
2. **Le test « à maximum ajustable » échoue aussi** : une bosse log-normale dont le maximum
   (donc le croisement de w = −1) est libre donne ΔAIC = **+29,6**, maximum ajusté à z = 0,26.
   Donc « avoir un croisement fantôme » n'est **pas** la propriété partagée. Hypothèse retirée.
3. **Et la question elle-même était mal posée.** Mesure directe : en déformant f(z) par un
   facteur multiplicatif borné, nul en z = 0, le χ² répond quadratiquement avec
   **σ(déformation) = 1,8 %**. [historique — réfuté #139 : σ(tilt) = 0,67 %, voir la correction finale]

**Conséquence, et c'est la réponse.** Les données ne sélectionnent pas une *propriété* : elles
**mesurent une courbe**, f(z) = ρ_de(z)/ρ_de(0), à 1,8 % près. Il n'y a donc aucune structure
cachée à trouver. Le compte se referme exactement :
- accrétion vs CCBH : écart 4,6 % RMS → coût ≈ 6 en χ², soit ~1 unité d'AIC après le
  paramètre en moins de CCBH. **C'est précisément le ΔAIC = 1 du papier C, expliqué.**
- les six formes jouets dévient de ~4 % ou plus → coût ~5 en AIC. **Exactement l'écart mesuré.**

**Ce qui reste vrai, et ce qui tombe.** Tombe : « le fond ne teste que la classe saturante »
(réfutée), « c'est la dilution » (réfutée), « c'est le croisement fantôme » (réfutée), et
l'idée qu'une propriété structurelle profonde relie t^β/a³ à ∫ψdt. Reste : le fond **mesure
f(z) à 1,8 %**, et deux familles à un paramètre contiennent cette courbe là où six autres ne
la contiennent pas. La convergence des deux ontologies n'est pas un mystère — c'est le fait
ordinaire que deux familles assez souples contiennent la réponse mesurée.

**Et le papier C n'en sort pas affaibli, il en sort quantifié** : le fond ne départage pas
accrétion et CCBH *parce que* leur écart (4,6 %) est sous le seuil de trois écarts-types de
ce que les données résolvent (1,8 %). Ce n'est plus une observation, c'est un calcul. [historique — réfuté #139]


---
# CORRECTION FINALE (#139) : LE 1,8 % ÉTAIT FAUX — LA RÉSOLUTION EST DIRECTIONNELLE
Refait autour du vrai minimum : σ(tilt) = **0,67 %** (mon 1,8 % moyennait des courbures
incompatibles autour d'un point hors minimum — malpractice statistique, retirée). Et la mesure
le long de la direction inter-modèles exacte donne **Δχ²(λ:0→1) = +1,06** : le match nul ne
vient PAS de « 4,6 % < résolution » mais d'UNE direction quasi-plate de la vraisemblance —
structure en composantes principales, exhibée entre deux modèles physiques. Creux médian −7,5
(2,7σ) consigné, non exploité. Les six familles témoins et leurs pénalités restent valides.
