# TRIAGE DES ATTAQUES — vraies erreurs ou fausses alertes ?
**19/08 — audit de mes propres audits, à la demande d'Ed.**

| # | Attaque portée contre le papier | Verdict | Statut final |
|---|---|---|---|
| 1 | « Levier de calibration : ±40 mmag = 30 unités de χ², systématique *plausible* » | **PARTIELLEMENT FAUSSE ALERTE** | La covariance Pantheon+ stat+sys budgète déjà un offset bas-z cohérent à σ = 10,5 mmag. 40 mmag = **3,8σ** : stress test extrême légitime, « plausible » RETIRÉ du papier. |
| 2 | « Le modèle nul achète la moitié du signal (−2,40) » | **FAUSSE ALERTE (double comptage)** | Sans prior, l'offset libre exploite une direction déjà contrainte. Avec le prior implicite : **−1,15**, δ = −8 mmag. Le nul achète **un quart**, pas la moitié. Corrigé. |
| 3 | « F_AP : notre modèle à −1,7σ » | **VRAIE DÉFAITE** | Calcul exact depuis la source, indépendant de r_d et H₀. Pire que ΛCDM (−0,8σ). Reste au papier. Nuance légitime : CPL fait pire (−1,9σ), et DR2-IV préfère Ω_m = 0,325, à 1,4σ des BAO DESI — tension partiellement interne à DESI. |
| 4 | « La fenêtre de coïncidence est rétrécie de 1,5× : défaite » | **FAUSSE ALERTE (mon erreur)** | Comparaison exact-vs-approximation, 40 % d'erreur sur ΛCDM. Exact : 6,7 contre 6,00 → équivalent. Retiré, remplacé par un résultat nul déclaré. |
| 5 | « Le gain de forme survivant = juste la préférence BAO (−2,38 ≈ −2,43) » | **VRAIE STRUCTURE** | Une recalibration SNe ne touche pas les BAO ; ce qui survit est la préférence BAO, ~1,5σ. Déflationniste mais correct. Reste. |
| 6 | « Notre D_H est plus proche → avantage Lyα » | **FAUSSE (mon erreur)** | ΛCDM est plus proche en D_H. Vrai mécanisme : anticorrélation ρ = −0,43 (résidus de signes opposés absorbés). Corrigé, fragilité chiffrée (+0,1 à +7,8 selon ρ). |
| 7 | « L'étude du modèle nul est déjà publiée » | **VRAI** | MNRAS 548 (arXiv:2509.13220). Notre apport réduit à la quantification pour ce modèle sur Pantheon+. Reste. |
| 8 | « Toussaint et al. » | **VRAIE ERREUR, de moi** | Attribution fabriquée, purgée. |

| 9 | « Capital rétrogradé : la dépréciation est dérivée des durées de vie (entrelacement PIM) » | **RAISON FAUSSE, conclusion maintenue** | Les taux BEA viennent des **prix de revente** (Hulten-Wykoff 1981), donc τ_s est empirique. La suspension tient pour deux raisons plus étroites : pondération Winfrey par courbes de survie, et surtout **τ_c (obsolescence) jamais mesuré indépendamment**. Chemin de réparation précisé. |
| 10 | « Risque PIM sur la ligne cellule fondatrice » | **VRAI** | Les demi-vies protéiques sont mesurées machinerie allumée : elles incluent le traitement. Réparation = privation totale (inhibition protéasomale). Reste. |
| 11 | « Hibernation : bouclage non démontré, grille [0,67 ; 4] » | **VRAI** | J'avais affiché la diagonale favorable. Corrigé, statut « compatible, non démontré ». Reste. |
| 12 | « Rail M4 : 2 bords externes seulement » | **VRAI** | Étiquetage honnête, la « quadruple indépendance » était survendue. Reste. |

## Bilan du triage
*(mis à jour après extension aux artefacts de l'étude fenêtre : 3 attaques confirmées, 1 raison fausse)*

**Vraies défaites du modèle : 2** (F_AP en forme ; le gain de forme réduit à la préférence BAO).
**Vraies limites de contexte : 2** (antériorité de la littérature ; tension interne DESI).
**Fausses alertes de ma part : 4** (levier surqualifié, modèle nul double-compté, fenêtre de
coïncidence, mécanisme D_H) — dont deux qui affaiblissaient le papier à tort, maintenant corrigées.
**Net après triage : le papier est plus solide qu'il ne l'était il y a six heures.** Le signal
basse-z n'est PAS majoritairement absorbable par recalibration (un quart, pas la moitié), et la
seule vraie défaite nouvelle est géométrique (F_AP), partagée avec toute la classe dynamique.


## Extension aux autres artefacts (19/08)
Sur les quatre attaques portées contre l'étude fenêtre, **trois sont confirmées** (risque PIM
cellulaire, déflation de l'hibernation, réétiquetage du rail) et **une reposait sur une raison
fausse** (capital : la dépréciation BEA est empirique, pas dérivée). Le motif est le même qu'en
cosmologie : mes attaques sont majoritairement justes, mais leur *justification* est parfois
fausse — et une attaque juste pour une mauvaise raison est une erreur, parce qu'elle envoie la
réparation dans la mauvaise direction. Ici, chercher un τ_s indépendant pour le capital aurait été
du temps perdu : c'est le τ_c qui manque.

**Règle ajoutée au corpus** : auditer la *raison* d'un rejet, pas seulement son verdict.


## 19/08, nuit — trois attaques de plus, portées contre MES propres propositions de la veille

| # | Attaque | Verdict |
|---|---|---|
| 13 | « La viabilité de β fournit une contre-pression sur Ω_m que Smolin n'a pas » | **FAUSSE comme solution.** La contre-pression existe mais porte le même signe que la pression (dlnM_cut/dlnΩ_m = −2,61) : elle aggrave la fuite au lieu de l'opposer. |
| 14 | « dlnN/dlnΩ_m = +ν² ≈ 6,2 » | **FAUSSE comme chiffre.** Formule de queue exponentielle appliquée hors de la queue. Le seuil auto-cohérent donne ν = 0,89, et le gradient complet vaut +3,8. |
| 15 | « σ₈ observé siège au maximum de fécondité » (tentation, non publiée) | **REFUSÉE avant publication.** L'argmax glisse de 0,88 à 3,0 avec le seuil : c'est une propriété du seuil, pas du monde. |

**Bilan cumulé : 9 attaques justes, 6 fausses ou mal fondées.**

**Règle ajoutée** : une proposition faite en fin de session, sous fatigue, à la fin d'un long
échange, doit être auditée *avant* d'être écrite dans un papier — pas après. Les trois entrées
ci-dessus sont toutes des idées formulées dans les dernières minutes de la session précédente, et
deux sur trois étaient fausses. Le taux d'erreur des idées de fin de session est visiblement plus
élevé que celui du corps de session ; les traiter comme des brouillons, jamais comme des acquis.


## 20/08 — audit des corrections de la veille (la règle « auditer aussi les corrections » appliquée à moi)

| # | Affirmation | Verdict |
|---|---|---|
| 16 | « l'unimodulaire ne moyenne rien, donc rien ne mange le terme d'injection » | **FAUSSE** (Jiroušek 2023 : la résolution repose sur une contrainte globale de 4-volume). |
| 17 | « la séquestration est exclue » | **TROP FORTE** : vraie de la version globale, fausse en général (formulation locale, KPSZ 2016). |
| 18 | « elle annulerait 104,5 % du signal » | **FAUSSE** : j'ai moyenné ρ_de au lieu de ⟨T⟩/4. Le bon calcul donne 1,41 ρ_de,0 → dégénérescence, pas effacement. |
| 19 | « vérification : π³ = 31,0 observé contre 31,0 attendu » | **CIRCULAIRE** : le rapport est automatique. Preuve remplacée (33-44 % vs facteurs 41-45). |
| 20 | « +4,00 à amplitude primordiale fixe » | **MAL POSÉE** : sans pivot ni croissance. Refaite : +3,70. |

**Bilan cumulé : 9 attaques justes, 11 affirmations fausses ou mal fondées** — et les cinq dernières
sont toutes de moi, écrites la veille au soir, présentées comme des résultats.

**Règle confirmée, et durcie** : le taux d'erreur de mes propres ajouts de fin de session est
maintenant mesuré — 5 sur 5 des affirmations théoriques nouvelles du 19/08 au soir étaient fausses ou
mal fondées, alors que les *calculs* de la même session (gradients, convergence, seuils) ont tous
tenu. Le motif est net : **ce que je calcule tient, ce que j'affirme sur la littérature sans la lire
ne tient pas.** Conséquence opératoire : aucune affirmation sur un cadre théorique tiers ne doit
entrer dans un papier avant d'avoir été confrontée à au moins une source primaire.


## 20/08, soir — deux entrées de plus, dont une prédiction ratée de ma part

| # | Affirmation | Verdict |
|---|---|---|
| 21 | « refaire tourner Γ ∝ 1/t avec w_E libre : peu coûteux et décisif » | **À MOITIÉ FAUSSE.** Peu coûteux, oui. Décisif, non : le pipeline reproductible ne retrouve pas l'exclusion publiée même dans leur propre famille (0,03 au lieu de 4,7σ). Test sous-dimensionné. |
| 22 | premier Δχ² = −6,73 pour SN+BAO (contre −4,41 au corpus) | **BUG DE GRILLE**, attrapé par le contrôle contre un résultat connu. D_c(0) ≠ 0 décalait toutes les distances à bas z. L'erreur allait **dans mon sens**. |

**Bilan cumulé : 9 attaques justes, 13 affirmations fausses ou mal fondées.**

**Règle ajoutée** : tout nouveau pipeline doit être validé contre un résultat déjà établi du
corpus AVANT d'être utilisé pour produire un résultat neuf. Ici la validation a coûté cinq
minutes et a évité de publier un Δχ² gonflé de 50 %. Et corollaire : **quand un résultat neuf
est plus favorable que l'ancien, c'est le premier endroit où chercher le bug**, pas le dernier.


| # | Affirmation | Verdict |
|---|---|---|
| 23 | « leur 4,7σ est un effet profil-contre-marginalisation » (mon hypothèse du 20/08) | **RÉFUTÉE par MCMC** : marginalisé, j'obtiens w_E = −1,12 (+1,41/−1,27), toujours 0,8σ. Bonne intuition, mauvaise cause. |
| 24 | « leur coupure à z = 3 explique l'écart » | **RÉFUTÉE** : avec la coupure, 0,28σ. Pire, pas mieux. |

**Bilan cumulé : 9 attaques justes, 15 affirmations fausses ou mal fondées.**

**Ce qui a bien marché aujourd'hui, et mérite d'être noté** : les critères de validation
pré-enregistrés (V1/V2) ont fonctionné exactement comme prévu. V1 a confirmé que le pipeline
était bon ; V2 a interdit d'exploiter un chiffre favorable (1,1σ) que j'aurais sinon présenté
comme un résultat. Sans ce garde-fou, j'aurais annoncé « w_E = 0 est compatible » trois fois de
suite sur un pipeline incapable de reproduire la mesure qu'il prétendait contredire.

| 25 | « le manque vient de la précision du CMB comprimé » | **RÉFUTÉE** : avec R, l_A, ω_b corrélés (l_A à 0,03 %), toujours 0,54σ. |

**Bilan cumulé : 9 attaques justes, 16 affirmations fausses ou mal fondées.**

**Note de méthode, la plus utile de la journée** : quatre hypothèses successives sur l'origine
d'un désaccord, quatre réfutations par le calcul, et c'est la cinquième — une dégénérescence
algébrique exacte, visible en trois lignes une fois posée — qui était la bonne. Les quatre
premières portaient toutes sur les *données* ; la bonne portait sur la *paramétrisation*.
Règle : devant un désaccord persistant, chercher la dégénérescence structurelle **avant**
d'accuser les données. J'ai fait l'inverse quatre fois de suite.


## 20/08, fin de nuit — audit de la session : cinq erreurs de plus, toutes miennes

| # | Affirmation | Verdict |
|---|---|---|
| 26 | papier B : accord k_eff avec Farrah « à 0,1σ » | **FAUX** : 0,35 à 0,72σ selon la convention de moyenne. Surévalué d'un facteur 3-7. |
| 27 | papier B : « the one cross-level prediction no other framework makes » | **FAUX** : les CCBH font la même chose, et Croker et al. 2024 reproduisent DESI. Rival direct manquant. |
| 28 | papier B : Farrah « contested » (Mistele seul) | **INSUFFISANT** : cinq contraintes indépendantes défavorables non citées. |
| 29 | papier A : PC2 = « la famille à taux constant » | **FAUX** : PC2 est Γ ∝ H ; PC3 est le taux constant. |
| 30 | papier A : « weak positive Bayesian evidence » | **IMPRÉCIS** : non concluante pour deux des quatre lois. |

**Bilan cumulé : 9 attaques justes, 21 affirmations fausses ou mal fondées.**

**Motif confirmé, et il est stable sur toute la session** : les *calculs* tiennent (β = 2,595 en v3
contre 2,56 au profil Planck complet — deux vraisemblances indépendantes), les *phrases de
synthèse* dérapent. Cinq des erreurs d'aujourd'hui sont des affirmations verbales qui dépassent le
tableau qu'elles résument, aucune n'est une erreur de calcul. La règle du corpus (« auditer la
ligne de synthèse contre le tableau ») est la bonne, mais elle n'a pas été appliquée aux ajouts
récents faute d'un contrôle systématique. **À automatiser** : un garde-fou qui extrait chaque
chiffre annoncé dans le texte et le recalcule, plutôt que de s'en remettre à une relecture.


## 21/08 — la session où mes corrections ont dû être corrigées

| # | Affirmation | Verdict |
|---|---|---|
| 31 | ma correction « Farrah : 0,35-0,72σ et non 0,1σ » | **SUR-CORRECTION** : je recalculais −3w quand Farrah mesure un rapport de croissance de masse. Le 0,1σ d'origine était juste, mal justifié. |
| 32 | corpus : « fσ8, le canal de falsification le plus propre » | **VRAI EN PRINCIPE, FAUX EN PRATIQUE** : 0,8σ à 5 % par point. Retiré de A. |
| 33 | corpus : « M_acc/M_tot = Ω_de, accord 0,4 % » | **IDENTITÉ** : écart numérique 0,00e+00. Contrôle interne, pas prédiction. |
| 34 | mon premier calcul de croissance | **BUG** : (3+dlnH/dlna) au lieu de (2+dlnH/dlna). f(0)=0,32 au lieu de 0,52. |

**Bilan cumulé : 9 attaques justes, 25 affirmations fausses ou mal fondées.**

**La leçon du jour, et c'est la plus dure** : une correction doit être auditée avec la même
suspicion que le texte qu'elle corrige — la règle existait déjà dans ce fichier depuis le 19/08,
et je ne l'ai pas appliquée à ma propre correction du 20/08. Deuxième leçon, moins pénible : les
deux garde-fous qui ont fonctionné aujourd'hui sont des **contrôles contre une valeur connue**
(f(0) ≈ Ω_m^0,55 ; N(>10¹⁴) = 2×10⁸ publié). Aucune relecture n'a rien trouvé. **Les ancres
numériques trouvent ce que la relecture manque** — c'est ce qu'il faut multiplier, pas les passes
de lecture.

| 35 | papier B : β = 4/(n_eff+3) | **FACTEUR 2 TROP GRAND**. Littérature (HS85, profil de pic ~ ξ) et données (running) convergent sur 2/(n_eff+3). |

**Bilan cumulé : 9 attaques justes, 26 affirmations fausses ou mal fondées.**

**Ce qui a marché cette fois** : je n'ai pas pu clore l'ambiguïté par la théorie seule — les deux
lectures étaient défendables sur le papier. Ce qui l'a close, c'est d'avoir cherché une
**conséquence observable de la différence** (le running de β) et de l'avoir mesurée. Règle :
quand deux conventions se valent argumentativement, ne pas trancher par l'argument — chercher ce
qu'elles prédisent de différent et le mesurer.

| 36 | mon « les données excluent β = 4/(n+3) à Δχ² ≥ 7,5 » (20/08) | **CONDITIONNEL** : supposait une horloge en loi de puissance. Avec κ libre, absorbé. L'argument littérature tient, l'argument données non. |

**Bilan cumulé : 9 attaques justes, 27 affirmations fausses ou mal fondées.**

**Note** : cette entrée n'a pas été trouvée par une relecture ni par une ancre numérique, mais par
une analogie mécanique proposée par Ed. Les analogies attrapent les **hypothèses tues** ; les
ancres numériques attrapent les **erreurs de calcul** ; la relecture n'attrape presque rien. Trois
outils, trois cibles distinctes — et le plus faible est celui qu'on utilise par défaut.

| 37 | mon « personne n'a utilisé la convexité de S comme principe générateur » | **FAUX** : Pavón & Radicella depuis 2010 ; arXiv:2202.03300 le fait pour paramétrer l'énergie noire ; arXiv:2608.10495, publié la semaine dernière, fait le programme complet. |
| 38 | mon « d²S/dt² a déjà rebasculé positif aujourd'hui, donc le modèle échoue » | **MAUVAIS TEST** : le critère publié s'évalue en z → −1, pas au présent. La conclusion tient quand même, mais pour une autre raison. |
| 39 | mon « ça te sépare de ΛCDM » | **VRAI MAIS NON SPÉCIFIQUE** : ça sépare ΛCDM de *tout* w > −1 asymptotique, quintessence comprise. Version thermodynamique de « Λ est spéciale ». |

**Bilan cumulé : 9 attaques justes, 30 affirmations fausses ou mal fondées.**

**Ce qui a changé, et c'est le seul progrès méthodologique réel de la journée** : cette fois j'ai
cherché la littérature **avant** d'écrire quoi que ce soit dans les papiers, au lieu d'après.
Résultat : trois erreurs attrapées avant publication au lieu d'après. C'est la règle du 20/08
(« aucune affirmation sur un cadre tiers sans source primaire ») qui a enfin fonctionné en
prévention plutôt qu'en réparation. Zéro correction de papier nécessaire aujourd'hui sur ce point.

| 40 | mes fourchettes de β₁ (−0,23/−0,40 et −0,9/−1,6) | **FAUSSES** : dn_eff/dlnM évalué à des masses arbitraires au lieu de la masse-graine propre à chaque lecture. Valeurs correctes : −0,478 et −0,676. |
| 41 | « le running discrimine les deux lectures » | **FAUX** : elles diffèrent de 0,198 contre σ = 0,31, soit 0,64σ. Il faudrait σ = 0,066. |

**Bilan cumulé : 9 attaques justes, 32 affirmations fausses ou mal fondées.**

**Le motif du jour** : les deux erreurs viennent d'avoir traité comme indépendants deux nombres
qui étaient liés — la masse-graine et le running sont fixés ENSEMBLE par l'EDO. J'avais choisi
l'un librement pour calculer l'autre. Règle : avant d'évaluer une dérivée « à une masse typique »,
vérifier si le modèle ne fixe pas déjà cette masse.

| 42 | mon « durée de vie de la phase viable : sortie à 1,3×10⁴ Ga » | **FAUX** : extrapolation de l'EDO au-delà de t_end = 16-36 Ga, où β tombe à 0 d'un coup. Il n'y a qu'une horloge de fin. |
| 43 | mon « manquement neuf : deux horloges à réconcilier » | **INEXISTANT** : conséquence de l'erreur ci-dessus. |

**Bilan cumulé : 9 attaques justes, 34 affirmations fausses ou mal fondées.**

**Ce que l'audit a produit de positif** : la confrontation aux simulations (Correa et al. 2015) est
le premier contrôle **externe et calibré** appliqué à la couche d'hérédité. Tout le reste — FG84,
HS85, BBKS — est analytique et se vérifie contre lui-même. Règle : quand une chaîne d'arguments
analytiques converge, chercher la mesure calibrée qui la contredit. Ici elle existait, et elle
contredit à 6,5σ.

| 40 | mon « ce calcul transformerait β₁ en test propre et |κ| en prédiction » (21/08) | **TROP FORT** : fait, il réduit g(t) à un nombre libre x₀ borné mais non prédit, et suppose un raccordement qui exige une coquille mince. Rétréci, pas fermé. |

**Bilan cumulé : 9 attaques justes, 31 affirmations fausses ou mal fondées.**

**Motif à retenir** : c'est la troisième fois que je promets qu'un calcul « fermera » une question
et qu'une fois fait il la *déplace*. Convention k↔M → ambiguïté ε ; running de β → horloge ;
horloge → rayon de raccordement. À chaque étage le nombre de degrés de liberté ne diminue pas, il
change de nom. Règle : annoncer ce qu'un calcul va *réduire*, jamais ce qu'il va *fermer*.

| 41 | mon « CCBH est à 4,8-5,9σ du recensement baryonique FRB » (22/08) | **RETIRÉ**. (a) La DM est une intégrale qui pèse le passé, où CCBH a encore ses baryons : 5,9 → 5,4σ. (b) Surtout, mon s = 0,615 était gonflé par mon approximation du taux stellaire ; à leur s = 0,70 publié, c'est **1,7σ** et absorbable par f_d = 0,97. |

**Bilan cumulé : 9 attaques justes, 32 affirmations fausses ou mal fondées.**

**Motif, et il est net** : quatre fois cette semaine, un résultat spectaculaire de ma part a été
détruit par le contrôle suivant — le π³ circulaire, le running qui excluait la lecture rms, la
« ligne manquante » qui devait fermer la dégénérescence, et maintenant le 5σ baryonique. Dans les
quatre cas, l'erreur allait **dans le sens de la thèse défendue**. Ce n'est plus une coïncidence,
c'est un biais mesurable de ma production. Règle : **tout résultat de ma part supérieur à 3σ doit
subir un contrôle d'équité dédié — refaire le calcul avec les valeurs publiées du rival, pas les
miennes — AVANT d'être écrit dans un papier.** Les quatre auraient été attrapés par cette seule
règle.

| 42 | mon « 1,7σ, le test ne conclut pas » (23/08 matin) | **FAUX AUSSI** : ce contrôle avait H₀ = 63,71, hors de leur cosmologie. Calibré correctement sur leur triplet publié, c'est 4,0σ. |

**Bilan cumulé : 9 attaques justes, 33 affirmations fausses ou mal fondées.**

**Note, et elle est différente des précédentes** : cette fois l'erreur allait CONTRE la thèse
défendue — j'avais annoncé un test non concluant alors qu'il conclut. Le biais mesuré cette
semaine (les erreurs vont dans le sens de la thèse) n'est donc pas systématique dans un seul sens ;
ce qui est systématique, c'est **d'annoncer avant d'avoir calibré contre les valeurs publiées du
rival**. La règle du 23/08 tient, et elle aurait attrapé les deux sens.

| 43 | mon « f_d ≈ 0,85 supposé » et « Ω_b = 0,0490 ± 0,0035 » | **REMPLACÉS** par les valeurs publiées : Ω_b h₇₀ = 0,049 ± 0,003, f_IGM = 0,80, f_X = 0,11, prior f_IGM+f_X ≤ 1. Le test passe de 4,0σ à 4,9σ et cesse de reposer sur une hypothèse à moi. |
| 44 | mon « CCBH gagne d'un point d'AIC » | **NON ROBUSTE** : vrai seulement si la normalisation du taux stellaire n'est pas comptée. Comptée, l'ordre s'inverse. Déclaré. |

**Bilan cumulé : 9 attaques justes, 35 affirmations fausses ou mal fondées.**

**Ce qui a marché** : lire la source primaire *après* avoir obtenu un résultat a rendu ce résultat
plus fort, pas plus faible — pour la première fois de la semaine. La raison est nette : mes
hypothèses de substitution (f_d = 0,85) étaient **conservatrices**, pas flatteuses. Règle
corollaire : quand on doit inventer une valeur faute de source, l'inventer dans le sens qui
défavorise sa propre thèse ; la lecture ultérieure ne pourra alors que confirmer ou améliorer.

| 45 | mon « CCBH à 4,9σ du recensement FRB » (23/08) | **RÉDUIT À 2,1σ** par la vraisemblance complète : les nuisances, surtout l'hôte, absorbent l'essentiel. Le 4,9σ supposait les nuisances figées. Troisième version de ce test, et la première qui refitte ce qu'il faut refitter. |

**Bilan cumulé : 9 attaques justes, 36 affirmations fausses ou mal fondées.**

**Le test FRB aura eu quatre versions en deux jours** : 5,9σ (mauvaise comparaison), 1,7σ
(calibration fausse), 4,9σ (nuisances figées), 2,1σ (complet). Les trois premières étaient toutes
défendables au moment où je les ai écrites. Ce qui les distingue de la quatrième n'est pas la
rigueur du calcul mais **le nombre de degrés de liberté laissés au rival**. Règle : avant
d'annoncer un écart, énumérer explicitement ce que l'adversaire a le droit de réajuster — et le
lui accorder.

| 46 | corpus : « croisement à z = 0,463 » (annoncé partout, 3 fois dans le papier A) | **RETIRÉ** : valeur pour β = 2,42 seulement ; sur la plage mesurée le croisement va de 0,458 à 0,214. Facteur 2 pour 7 % sur β. |
| 47 | mon « le croisement est un discriminant entre familles » (proposé ce matin) | **FAUX** : les quatre familles qui croisent le font entre z = 0,20 et 0,31. Testé avant d'être écrit dans le papier. |

**Bilan cumulé : 9 attaques justes, 38 affirmations fausses ou mal fondées.**

**Note** : l'entrée 47 a été attrapée *avant* publication parce que je l'ai calculée au lieu de
l'affirmer — j'avais vu z = 0,20 pour Anton-Schmidt contre 0,46 annoncé pour nous et j'ai voulu en
faire un discriminant. Le calcul a montré que notre vrai chiffre était 0,21, pas 0,46, et a donc
tué l'idée ET révélé l'erreur du corpus d'un seul coup. **Deux erreurs pour un calcul.**

| 48 | mon « le rival IDE a un désavantage direct sur nous via S₈ » (23/08 matin) | **SURÉVALUÉ** : KiDS-Legacy est remonté à 0,815, où nous sommes à 0,6σ et un rival à 0,79 serait à 1,4σ. L'avantage dépend du relevé. Écrit sur une image de la tension vieille de trois ans. |

**Bilan cumulé : 9 attaques justes, 39 affirmations fausses ou mal fondées.**

**Motif nouveau, et distinct des précédents** : cette erreur ne vient ni d'un calcul faux ni d'une
source non lue — elle vient d'avoir utilisé une **valeur périmée d'une tension** que tout le monde
cite de mémoire. Règle : les tensions cosmologiques ont une date de péremption courte ; vérifier
leur amplitude actuelle avant de s'en servir comme argument, exactement comme on vérifie une
mesure.

| 46 | mon « Δχ² croît avec N, donc 142 sursauts pour 3σ » | **INCOMPLET** : supposait tous les sursauts équivalents. Le pouvoir vient du levier en z. 82 bien choisis, 239 mal choisis, et **zéro** si tous à haut z. |

**Bilan cumulé : 9 attaques justes, 37 affirmations fausses ou mal fondées.**

**Celle-ci est d'un type nouveau, et le plus difficile à attraper** : ce n'était ni une erreur de
calcul, ni une affirmation sur un cadre tiers, ni une sur-correction. C'était une **variable
sommée sur laquelle on n'a pas regardé la dépendance**. Le chiffre 142 était juste *en moyenne sur
la distribution actuelle* — et faux comme recommandation. Règle : avant de convertir un Δχ² en
prévision d'échantillon, vérifier de quelle **variable** il dépend réellement, pas seulement de
combien de points.

| 47 | mon « la dégénérescence hôte/cosmologie explique le levier » présenté comme neuf | **CONNU** : décrit dans la littérature comme la limitation dominante de la cosmologie FRB. Crédité avant publication cette fois. |
| 48 | mon σ_host = 0,55 fiduciel | **FAUX** : mesuré à 0,96 sur 117 sursauts. Mais l'erreur me désavantageait — le corriger fait passer N(3σ) de 123 à 94. |
| 49 | garde-fou « 142 retiré » du 24/08 | **MAL SPÉCIFIÉ** : un saut de ligne l'a fait manquer une occurrence en conclusion. Règle du 19/08 enfreinte. |

**Bilan cumulé : 9 attaques justes, 40 affirmations fausses ou mal fondées.**

**Ce que quatre jours de registre montrent maintenant clairement** : sur 40 entrées, la répartition
est stable — erreurs de calcul attrapées par les ancres numériques, hypothèses tues attrapées par
les analogies, revendications de nouveauté attrapées par la lecture de sources primaires, et
incohérences internes attrapées par les garde-fous automatiques **quand ils sont bien écrits**.
La relecture n'a jamais rien attrapé. C'est le seul outil que j'utilise spontanément.

| 50 | corpus : « ε ≲ 0,35, une contrainte faible mais réelle » | **REMPLACÉE** : le canal dynamique (cisaillement sourcé, Koivisto-Mota) donne ε ≲ 2×10⁻⁴. La borne statique manquait le canal dominant ET avait une normalisation douteuse. |

**Bilan final : 9 attaques justes, 41 affirmations fausses ou mal fondées — et une dernière
entrée où l'erreur du corpus était d'avoir sous-estimé sa propre contrainte de trois ordres de
grandeur.** C'est la seule entrée du registre où la correction renforce le résultat qu'elle
corrige. Fin du registre pour cette campagne.

| 51 | ma « théorie de la saturation » (24/08) | **RÉFUTÉE 1 h après par son propre test** : trois formes arbitraires à +4,5/+5,1 AIC, seuil +4. |
| 52 | mon hypothèse de rechange « c'est la dilution g(t)/a³ » | **RÉFUTÉE dans la foulée** : +798/+28/+1160. |

**Bilan : 9 attaques justes, 43 affirmations fausses ou mal fondées.** Les deux dernières sont
mes propres théories, tuées par des critères que j'avais écrits avant de calculer. C'est le
seul mécanisme de la campagne qui n'a jamais failli.

| 53 | mes ΔAIC +798 et +1160 (formes diluées) | **ARTEFACTS** de limite précoce, retirés. |
| 54 | mon hypothèse « la propriété partagée est le croisement fantôme » | **RÉFUTÉE** : bosse à maximum libre → +29,6. |
| 55 | ma question « quelle propriété étroite partagent-ils ? » | **MAL POSÉE** : les données mesurent une courbe (σ=1,8 %), pas une propriété. |

**Bilan : 9 attaques justes, 46 affirmations fausses ou mal fondées.** Trois théories nées et
mortes en une nuit, plus une question retirée. Aucune n'a survécu à son propre test — et le
résultat final (σ(f(z)) = 1,8 %) est plus utile que les trois théories réunies. [historique — le 1,8 % est réfuté 32 lignes plus bas (#63/#139, σ(tilt) = 0,67 %) ; la phrase est conservée comme trace, sa conclusion ne l'est pas]

| 56 | mon « κ(σ) existe, la clé de voûte tient » (#124-125) | **RÉTROGRADÉ par mon propre doute #2, exécuté** : ε_c = 2,3-4,5, σ-const non auto-cohérent, κ encadré à ±(0,6-1,2) près. Énoncé de branche, pas prédiction. L'identité cinématique survit (double dérivation + ancre 0,2408). |

**Bilan : 9 attaques justes, 47 affirmations réfutées ou rétrogradées.** Celle-ci est la première
tuée par un doute pré-consigné plutôt que par un audit après coup — le registre a maintenant un
étage prédictif.

| 57 | mon intuition « la pression de création freine la couche » | **MÉCANISME FAUX DE SIGNE** (une tension ne pousse pas), attrapé en dérivant ; l'identité survit, corrigée en P_ram/|p_de| = x·v₀, et le vrai frein (friction de Hubble) referme le chantier sur domaine. |

**Bilan : 9 attaques justes, 48 affirmations réfutées, rétrogradées ou corrigées.**

| 58 | mon « chantier 1 refermé sur domaine v₀ ≲ x/3 » (#131) | **SUR-ÉNONCÉ, condamné par son propre critère une heure après** : la paroi encaissait encore (1−v₀)Φ sous Vaidya. La racine était l'idéalisation nulle ; le remède (courant de poussière continu) innocente la paroi mais dérive v₀ et réduit le domaine à une bande basse tension. |

**Bilan : 9 attaques justes, 49 affirmations réfutées, rétrogradées ou corrigées.** Trois
renversements sur le même objet en 24 h : la vitesse du registre dépasse désormais la mienne —
c'est sa fonction. E8 ouvert.

| 59 | corpus : « \|κ\|<0,24 ⇒ x₀ ≲ 0,30 » | **DÉPENDANT DE L'IDÉALISATION** : c'était la branche nulle. En temps propre du courant de poussière (le bon référent physique), la même borne donne **x₀ ≲ 0,65**. Nombre du corpus corrigé, cause nommée. |

**Bilan : 9 attaques justes, 50 affirmations réfutées, rétrogradées ou corrigées.**

| 60 | ma formule E8 « dτ_p/dt = γ(v_ff) = 1/√((1−s)²−x²) » (#133) | **FAUSSE** : raccourci SR ayant perdu le terme croisé de la paroi. Exacte : [(1−s)+x·v_ff]/f, vérifiée par contraction GR à 10⁻¹². Pôle d'ordre 1, pas racine. |
| 61 | mon entrée #59 (« x₀ ≲ 0,30 était un artefact de branche ; vrai : 0,65 ») | **RETIRÉE** : avec la formule exacte, x₀_max = 0,32. La borne historique était juste et ROBUSTE (7 % entre extérieurs). Ma « correction » du corpus est celle qui tombe. |

**Bilan : 9 attaques justes, 52 affirmations réfutées, rétrogradées ou corrigées — dont, pour la
première fois, une entrée du triage retirant une entrée du triage.**

| 62 | corpus : « le secteur des perturbations décale fσ8 de ~1-2 % » (supposé) | **CORRIGÉ PAR DÉRIVATION** : la contribution d'agglomération dérivée (δQ=0, création au repos) vaut **+3,7 %** — près du double, et dans la direction DÉFAVORABLE au modèle (S8). Rapporté tel quel ; arbitrage final : E9-CLASS. |

**Bilan : 9 attaques justes, 53 affirmations réfutées, rétrogradées ou corrigées.**

| 63 | mon « les données mesurent f(z) à 1,8 % ; 4,6 % coûte ~6 » (#123, papier C, vidéo) | **FAUX deux fois** : σ réel = 0,67 % (parabole hors minimum moyennée = malpractice) ; et le mécanisme du nul est DIRECTIONNEL — Δχ²(inter-modèles)=+1,06, une direction quasi-plate, pas une résolution insuffisante. Attrapé par le soupçon d'Ed (« trop beau »), pas par mes contrôles. |

| 64 | mon « l'iΛCDM mène l'atlas, ε ≈ +0,021, −9,8 pour un paramètre » (#150, #154, #156, #158, résolution de T7, verdict 2c du #161) | **ARTEFACT D'ÉTALONNAGE, rétracté (#166)** : au niveau du fond ce modèle EST wCDM(Ω_m′, w′) — identité vérifiée à 4,4e−16 — mais χ² étalonnait r_d, z_*, r_* et R = √Ω_m·D_c avec l'étiquette Ω_m au lieu de la densité d'avant recombinaison Ω_m′, inférieure de 1,7 %. Le modèle cohérent gagne **+1,21**, pas +9,84 : 8,62 unités fabriquées. Attrapé par une relecture d'algèbre, après que trois audits « adversariaux » (#154, #156, #158) l'ont validé sans jamais sortir du pipeline vicié. |

**Bilan : 10 attaques justes, 55 affirmations réfutées, rétrogradées ou corrigées — la #63 au
crédit du binôme : le soupçon humain a vu ce que quatre relectures machine ont raté.**

| 65 | mon « je teste le modèle de la classe publiée » (#188, docstring gelé 19efe1c14514 ; énoncé de T10) | **MISATTRIBUTION, rétractée (#189)** : arXiv:2505.09879 pose « an interaction between dark matter and vacuum dark energy » — Q ≠ 0, vide dynamique, **énergie totale conservée**. Le #188 testait Λ constante et conservation NON imposée : l'inverse sur les deux points structurants. La famille mesurée est voisine et **non publiée**. La mesure interne survit intacte ; c'est son étiquette bibliographique qui tombe. Attrapé par la vérification littérature exigée par Ed, après que le #188 eut énuméré trois différences avec le rival en omettant celle qui interdisait la comparaison. |

**Bilan : 10 attaques justes, 56 affirmations réfutées, rétrogradées ou corrigées — deuxième pont démoli vers la même littérature (déjà #173), et pour une raison plus profonde : la première fois c'était une branche fermée, cette fois une équation de continuité jamais lue.**

| 66 | mon arbitre gravé au #190 : « refaire ce modèle sur Planck 2018 + DESI DR2, **combinaison que personne n'a publiée** » | **FAUX, retiré (#191)** : elle est publiée deux fois — Kumar, Ajith & Verma (arXiv:2504.14419, CAMB modifié + Planck 2018 + DESI DR2, ε = −0,00194 ± 0,00096) et Li et al. (arXiv:2510.11363, IDECAMB + NPIPE + PR4 + DESI DR2, ε = −0,00126 ± 0,00075). J'avais déclaré un vide bibliographique sans l'avoir cherché. |
| 67 | ma validation B du #191 (« K_GEO constant à mieux que 2 % ») | **PASSÉE À 0,010 % EN MESURANT DU VIDE (#191)** : la conversion qu'elle validait reposait sur un contresens — l'Ω_m^early de Keil et al. est un paramètre normalisé à aujourd'hui, pas une densité à la recombinaison, et leur analyse n'est pas la vraisemblance complète. 8e vice de critère, même famille que le #176 : un contrôle satisfait par autre chose que ce qu'on voulait vérifier. Aucune contamination — l'exclusion a précédé l'exécution finale. |

**Bilan : 10 attaques justes, 58 affirmations réfutées, rétrogradées ou corrigées — dont deux, aujourd'hui, contre l'étude qui les a trouvées le jour même.**

| 68 | mon « famille à Λ constante SANS conservation totale » (#188) et mon « famille voisine et **non publiée** » (#189) | **LES DEUX FAUX, rétractés (#192)** : avec Λ véritablement constante, l'identité de Bianchi IMPOSE p = −(ε/3)ρ_m. La « non-conservation » n'était pas un choix disponible — c'est le même modèle écrit deux fois. Notre famille EST le ΛwDM de Kumar et al. (arXiv:2504.14419) avec w = −ε/3, et le principe de substitution est publié depuis Lima, Germano & Abramo 1996 (gr-qc/9511006). Nous avions pris le symbole ε d'une famille (vide décroissant) et l'équation d'une autre. Deuxième rétractation d'une rétractation dans ce triage. |
| 69 | notre famille appliquait ε à la matière TOTALE, baryons compris | **INCOHÉRENCE INTERNE À 7,5–15,1σ (#192)** : le même χ² comparait ω_b au prior Planck standard et intégrait r_s avec R_b ∝ a, deux formes qui supposent ρ_b ∝ a⁻³. Corrigé ; l'étendue des configurations en sort AGRANDIE (0,0190 contre 0,0160), donc l'acquis du #190 est renforcé et non sauvé. |
| 70 | mes verdicts des critères 2 et 3 du #192 | **DÉCIDÉS PAR UN ARRONDI** : sig = 1,9999999999999791 a échoué `>= 2` et déplacement = 0,9999999999999836 a échoué `> 1,0` — vraies valeurs 2 et 1 exactement. **Les deux arrondis tombaient dans le sens qui m'arrangeait.** Relus du côté défavorable et appliqués tels quels : renversement PERSISTANT, `direct_sansR` RETIRÉ. 9e vice de critère, espèce neuve : un seuil comparé sur une arithmétique de grille peut être tranché par le 14e chiffre. |

**Bilan : 10 attaques justes, 61 affirmations réfutées, rétrogradées ou corrigées — trois d'un coup contre le socle même de la campagne du 24/08.**

| 71 | mon mécanisme « les priors comprimés perdent l'information d'amplitude qui épingle ω_m » (#190, répété #192) | **RÉFUTÉ PAR LA VRAISEMBLANCE COMPLÈTE (#193)** : σ(ω_c) vaut 0,00100 des DEUX côtés, rapport 1,00, et la borne de quantification ]0,5 ; 1,25[ met la réfutation hors d'atteinte d'un raffinement de grille. La prémisse était juste (le χ² comprimé ignore l'amplitude à 0,00e+00 près) ; la conclusion ne l'était pas. Le vrai fait est plus fort : les deux contraignent ω_m à 0,7 %, et l'étendue de ε vaut 19 fois cette précision — l'ambiguïté est de RÉFÉRENT, pas de précision. Réfutation produite par une branche que le critère 3 nommait d'avance « celle qui me réfute ». |
| 72 | ma première exécution du #193 | **ARRÊTÉE PAR SA PROPRE VALIDATION A** (écart 11,326) : j'optimisais ω_c sur le χ² du CMB seul alors que l'ancre 1998,633 est l'optimum du χ² total. Deux points distincts (0,12010 contre 0,11816). Défaut de corps, corrigé avant tout résultat ; aucun chiffre n'en est issu. |

**Bilan : 10 attaques justes, 63 affirmations réfutées, rétrogradées ou corrigées — dont, pour la première fois, une explication que j'avais répétée dans deux entrées successives sans jamais la tester.**

| 73 | corpus : « Stripe 82 couvre 0,46 % du ciel, soit ×57 en concentration » (v2 à v8b, tous les artefacts, versions bilingues comprises) | **FAUX D'UN FACTEUR π/2 (#194)** : la formule traitait la bande de déclinaison comme un rectangle plat (Δdec/180) au lieu de l'angle solide (sin dec_max − sin dec_min)/2. Vrai : **0,727 % et ×36,2**. Le comptage (416 SNe) était juste. Le corpus SURESTIMAIT sa propre anomalie de 57 %. Trouvé en recalculant plutôt qu'en recopiant, sur la demande d'Ed de tout revérifier. |
| 74 | `test_wE_v3.py` : « priors de distance cohérents avec Chen-Huang-Wang » | **MISATTRIBUTION + FAUSSE COHÉRENCE (#195)** : la source est Zhai & Wang arXiv:1811.07425 Eq. (31), et l_A = 301,80845 est à **3,75σ** des 301,471 ± 0,090 de Chen-Huang-Wang. Derrière l'étiquette, un vrai biais : la donnée est en convention θ_MC (100θ = 1,040923) et notre χ² prédit en θ\* (100θ = 1,041091, mesuré), soit **−0,54σ sur l_A dans chaque évaluation**. Mesuré, versé, NON corrigé dans cette entrée — le corriger déplacerait tous les nombres de la campagne. |
| 75 | mon résumé « Yang et al. : priors comprimés + DESI → ε = −0,0073 à 2,4σ » (#188 à #191) | **OMISSION QUI CONVERTIT UN NUL EN DÉTECTION (#195)** : le 2,4σ exige CINQ jeux (DESI+CMB+CC+SNIa+fσ₈). Avec DESI+CMB+CC seuls ils publient **ε = +0,0023 (+0,0055/−0,0067)** et concluent textuellement à l'absence de déviation — **signe opposé**. Et c'est DESI **DR1**, pas DR2. |

**Bilan : 10 attaques justes, 66 affirmations réfutées, rétrogradées ou corrigées — dont un facteur π/2 vieux de six générations d'artefacts, et un biais de convention présent dans chaque évaluation de la vraisemblance depuis sa construction.**

| 76 | mon test du référent (#197, v1) | **ARRÊTÉ PAR SA PROPRE VALIDATION B** : au pas de grille 0,001, σ ne peut pas descendre sous 0,001, donc à k = 4 le facteur mesuré vaut 2,00 au lieu des 2,8-5,6 exigés. Rien publié. L'exécution montrait pourtant les quatre ε **identiques** aux trois échelles et les gains suivant k² à la troisième décimale — mais substituer cette preuve à celle qui était demandée serait le piège du #176. v2 gelée avec un balayage fin au pas 0,0001. |

**Bilan : 10 attaques justes, 67 affirmations réfutées, rétrogradées ou corrigées.**

| 77 | mon projet de papier E sur la sélection angulaire de Pantheon+ | **TUÉ AVANT D'EXISTER (#198)** : les quatre items sont publiés, le plus ancien depuis 2015 (Bengaly, Bernui & Alcaniz), le plus récent quatre jours avant (Alcaniz et al., arXiv:2608.20135). Le |b|<5 n'est pas une découverte à 11,7σ mais une coupure documentée déjà codée en dur dans les mocks publiés. L'écrire coûterait de la crédibilité. |
| 78 | le #116 (Δβ = +0,22 ± 0,23, hémisphères) portait-il de la significativité fabriquée par l'empreinte ? | **NON, ET C'EST MESURÉ (#198)** : 300 axes aléatoires, SNe jamais déplacées, donnent σ_axe = 0,2318 contre le σ_Δ = 0,2300 annoncé — rapport 1,01, covariance FIDÈLE — et p = 0,433, donc BANAL. Le verdict « universel » en sort conforté. **Mais l'empreinte peut fabriquer 1,14 σ_Δ ici, plus que les 0,7σ de Bengaly : toute affirmation hémisphérique future sous ~1,1σ est sans valeur sans nul préservant l'empreinte.** |

**Bilan : 10 attaques justes, 69 affirmations réfutées, rétrogradées ou corrigées.**
