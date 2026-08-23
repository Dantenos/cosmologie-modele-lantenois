# L'ESPACE DES RIVAUX — plan d'étude A→Z (conçu le 19/08, avec tout le savoir acquis)
**Question unique : le Δχ² ≈ −12,6 de A récompense-t-il SA forme, ou n'importe quel croisement ?**

## Phase 0 — AVANT tout contact avec les données (les leçons câblées)
- canonical_values.json + linter dès le jour 0 (leçon : les fossiles de valeurs).
- Conditions de mort PRÉ-ENREGISTRÉES : (K1) si ≥ 30 % des rivaux à 1 paramètre atteignent
  Δχ² ≤ −11 (à 1,5 unité du nôtre), la spécificité de forme est MORTE — A n'est qu'un membre
  quelconque de la classe « croisements » ; (K2) si UN rival fait strictement mieux (Δχ² < −13),
  A est DÉTRÔNÉ ; (K3) si les rivaux généreusement aidés (z_× offert) ne rattrapent pas A,
  la forme porte du contenu. Seuils gravés avant le premier fit.
- Tout paramètre/définition passe le garde-fou d'indépendance AVANT d'entrer en table
  (leçon capital/cellule : pas de τ entrelacé, pas de rival avantagé en douce).
- Ordre d'exécution anti-ancrage : les RIVAUX d'abord, notre modèle EN DERNIER.
- Générosité déclarée envers l'adversaire : les rivaux reçoivent GRATUITEMENT le redshift de
  croisement (z_× = 0,45 fixé au best-fit observé) — ils n'ont à fournir que la forme.
  Notre modèle doit produire z_× ET la forme avec son unique β. Asymétrie EN NOTRE DÉFAVEUR,
  déclarée : si A gagne quand même, la victoire est plus dure donc plus vraie.

## Phase 1 — La famille des rivaux (1 paramètre de forme chacun, même machinerie, même data)
R1 linéaire-en-a : w = −1 + s·(a − a_×)            [la pente nue]
R2 tanh raide    : w = −1 + A·tanh((a − a_×)/0,05)  [la marche]
R3 tanh doux     : w = −1 + A·tanh((a − a_×)/0,25)  [le S]
R4 exponentiel   : w = −1 + A·(1 − e^{−(a−a_×)/0,15}) pour a>a_×, miroir dessous [l'asymétrique]
R5 loi de puissance en t : w = −1 + A·[(t/t_×)^0,5 − 1]  [le cousin structurel]
R6 CPL contraint 1-param : w0 libre, wa = −2,8·(1+w0) [la diagonale DESI]
(+ le nôtre : w = −β/(3Ht), z_× émergent — évalué en dernier)

## Phase 2 — Pipeline identique, vérification d'effet à chaque étape
Fond standard w(a) générique → distances → χ² sur BAO DR2 (13 valeurs, lintées) + SNe + prior
CMB (θ*), la même vraisemblance que A. Chaque fit : convergence vérifiée par l'EFFET (χ² recalculé
indépendamment au best-fit), jamais par le code de retour (leçon des sept str-replace).

## Phase 3 — Les trois temps de vérification en procédure NOMMÉE, puis le doctorant
Passe ligne-à-ligne ; passe cohérence/dégradations ; passe littérature (les rivaux ont des
ancêtres : chaque forme citée à sa famille publiée). Puis la relecture-doctorant comme phase
OBLIGATOIRE du protocole, pas comme faveur de fin de semaine.

## Phase 4 — Livrables sous conditions
Verdict quel qu'il soit → carnet. Papier SEULEMENT si K1-K3 rendent un verdict net dans un sens
ou l'autre (y compris contre nous : « A est une paramétrisation quelconque » est un résultat
publiable et serait publié). Mail aux externes à J+2, pas J+7 (leçon de la boucle fermée).

## Ce que je ferais différemment de cette semaine (auto-critique câblée)
Pré-enregistrer avant le premier fit, pas après ; une langue par corpus ; l'objection la plus
dangereuse PLANIFIÉE en tête et non rencontrée par accident ; zéro adjectif dans les sections
de résultats ; le manifest mis à jour le jour même de chaque fichier.

## PILOTE EXÉCUTÉ (19/08, séance même — rivaux d'abord, nôtre en dernier)
SN+BAO réels (1580 SNe + 13 BAO DR2) : LCDM 1400,67 ; les six rivaux Δχ² ∈ [−5,08 ; −4,62] ;
**le nôtre −4,41 — DERNIER des sept formes croissantes.** K1 DÉCLENCHÉE (6/6 rivaux à ≤ 1,5) ;
K2 déclenchée à la lettre — MAIS erratum de protocole détecté par sa propre exécution : K2 ne
prévoyait aucun tampon de bruit (les écarts 0,2-0,7 unités de χ² sont indiscernables) — le
protocole était mal écrit, et c'est le pilote qui l'a montré. **Verdict honnête du pilote :
au niveau SN+BAO, TOUTES les formes croisantes à 1 paramètre sont dégénérées, la nôtre
comprise — la spécificité de forme de A n'existe PAS dans les distances basses-z.**
Portée déclarée : le −12,6 titre venait de Planck-complet ; la manche décisive est
« rivaux + Planck » (les rivaux devront alors payer θ* que z_× offert ne couvre plus).
Implication pour A : son contenu distinctif, s'il existe, vit dans le secteur CMB-complet et
dans les structures dérivées (neutrinos, couplages, hérédité de B) — pas dans les distances.
C'est une perte réelle, enregistrée le jour de la conception de l'étude. La méthode marche :
elle nous a coûté quelque chose en trois heures.

## MANCHE DÉCISIVE — rivaux + Planck complet (19/08, deux tranches, budget déclaré)
Départs chauds depuis les états convergés, H0 résolu par θ*, 25 évaluations complètes par rival
(bornes SUPÉRIEURES, optimisation non convergée — déclaré) :
| Modèle (k_forme = 1 chacun) | Δχ² vs ΛCDM (Planck+BAO+SN complets) |
|---|---|
| R6 diagonale-CPL (wa = −2,8(1+w0)) | **≤ −7,86** — distancé de ~4,7 ; le CPL libre lui-même fuit la diagonale (wa = −0,60 vs −0,44), et la fuite coûte |
| R2 tanh-raide (vainqueur du pilote) | **≤ −9,79** — intermédiaire, ~2,8 derrière |
| **NOTRE forme (β)** | **−12,60** (état convergé) |

**Verdict de la manche (portée déclarée : 2 rivaux sur 6, bornes non convergées)** :
au niveau CMB-complet, K1 et K2 NE se déclenchent PAS — la forme reprend ses droits exactement
là où le test wCDM-complet les avait localisés. Synthèse des deux manches : *le contenu
distinctif de A n'est pas dans les distances basses-z (pilote : toutes formes dégénérées,
nôtre dernière par bruit) ; il est dans le secteur CMB, où SA forme spécifique vaut ~3-5 unités
de χ² sur des croisements génériques à paramètres égaux.* Caveats symétriques : les rivaux ont
des choix cachés figés (largeur du tanh, a_×) — mais notre forme aussi a sa structure figée par
la théorie ; et 2,8 unités à bornes non convergées = indice, pas verdict. Reste de la manche :
les 4 autres rivaux, convergence pleine, et un rival à largeur LIBRE (k=2) comme étalon.

## JACKKNIFE BAO DR2 (19/08) — le signal ne tient pas à un point
Retrait un à un des 13 mesures (q = c/H₀r_d reprofilé à chaque fois), SN+BAO :
- **Δχ²(accrétion) reste dans [−5,67 ; −3,50]** pour les 13 retraits (complet : −4,41) —
  **aucun point ne porte le signal** ; erreur jackknife ±1,6.
- **β est remarquablement stable : [2,42 ; 2,49], étendue 0,07** — la valeur centrale du modèle
  ne dépend d'aucune mesure BAO particulière.
- Point le plus *contraire* au modèle : **z = 0,706 (D_M)** — son retrait AMÉLIORE le fit
  (−3,50 → le point tire contre nous, pas pour nous).
- Point le plus *porteur* : **z = 0,510 (D_M)** — son retrait fait passer à −5,67, c'est-à-dire
  qu'il **contraint** le modèle plutôt qu'il ne le nourrit.
- CPL réagit de façon corrélée mais non identique (r = 0,60) : les deux modèles ne s'appuient
  pas exactement sur les mêmes points.
**Conclusion** : la crainte standard (« tout repose sur les LRG à z ≈ 0,51-0,71 ») ne s'applique
pas à notre fit basse-z — au contraire, ces deux points sont ceux qui nous résistent le plus.
À refaire sur Planck-complet, où le −12,6 vit (assignment ouvert).

## DÉCOMPOSITION PAR LOT (19/08) — le résultat le plus important de la journée
**Qui achète le croisement ?** Δχ²(accrétion) sur SN+BAO :
| Lot | Δχ² | β |
|---|---|---|
| BAO seuls | **−2,43** | 2,30 |
| SNe seules | **−0,12** | 2,64 |
| SN + BAO | **−4,41** | 2,45 |
La somme des parties (−2,55) est INFÉRIEURE au tout (−4,41) : ~1,9 unité du signal basse-z
**n'appartient à aucun lot — elle naît de la TENSION ENTRE LOTS.** Les SNe seules ne préfèrent
rien (−0,12) ; les BAO seuls préfèrent faiblement ; c'est leur désaccord sous ΛCDM que la forme
croisante réconcilie. Corollaire dur : le signal basse-z est un diagnostic de **cohérence
inter-jeux**, pas une mesure directe de w(z).

**Retrait par tranche SNe** (BAO conservés) : sans z<0,1 → −3,54 (+0,87) ; sans z>0,3 → −5,47
(−1,07). Aucune tranche ne porte le signal.

**Test d'Efstathiou (offset systématique des SNe z<0,1) : LE POINT DE FRAGILITÉ MAJEUR.**
Un décalage de ±0,04 mag — l'ordre de grandeur du désaccord inter-compilations discuté dans la
littérature (Efstathiou 2408.07175) — fait passer Δχ² de −4,41 à **+6,36** (δ = −0,04 : le
modèle est REJETÉ) ou à **−23,49** (δ = +0,04). Soit une amplitude de ~30 unités de χ² pour un
effet systématique plausible, contre 4,4 de signal. **Sur SN+BAO, la calibration photométrique
basse-z domine complètement le résultat.** β bouge peu (2,23-2,68), la forme est robuste, mais
l'ÉVIDENCE ne l'est pas.
**Conséquence à porter dans le papier A** : le Δχ² basse-z doit être présenté conditionnellement
à la calibration SNe, avec cette sensibilité explicitement chiffrée. C'est une réserve majeure
qu'aucun de nos 25 audits précédents n'avait quantifiée — trouvée en allant plus loin.

## LE MODÈLE NUL DE TENSION (19/08, soir) — l'étude que je voulais faire, faite
**Question** : un simple paramètre de nuisance photométrique (offset des SNe z<0,1, aucune
physique nouvelle) achète-t-il autant qu'un w(z) évolutif ?

| Modèle | k | χ² | Δχ² | AIC |
|---|---|---|---|---|
| ΛCDM | 1 | 1400,67 | — | 1402,67 |
| **ΛCDM + offset bas-z libre** | 2 | 1398,27 | **−2,40** (δ = −17 mmag) | 1402,27 |
| Accrétion w(z) | 2 | 1396,26 | −4,41 (β = 2,45) | 1400,26 |
| Accrétion + offset libre | 3 | 1395,89 | −4,78 (β = 2,40, δ = +8 mmag) | 1401,89 |
| CPL | 3 | 1395,83 | −4,84 | 1401,83 |

**Résultats, sans emphase :**
1. Le modèle nul MORD : un offset de nuisance achète **−2,40**, soit **54 % du gain de w(z)**.
   Une part majoritaire du signal basse-z est absorbable par une recalibration plausible
   (δ = −17 mmag, contre ~40 mmag de désaccords publiés inter-compilations).
2. Mais il ne dissout pas tout : à nombre de paramètres égal (k=3), accrétion+offset (−4,78)
   garde **−2,38 de gain propre** sur ΛCDM+offset (−2,40). Le signal n'est PAS entièrement
   réductible à une calibration.
3. Dégénérescence partagée démontrée : en présence de w(z), l'offset préféré tombe de −17 à
   +8 mmag — les deux effets se disputent la même structure de résidus.
4. AIC : ΛCDM+offset (1402,27) fait presque aussi bien que ΛCDM (1402,67) ; accrétion reste
   première (1400,26). L'ordre du classement survit, l'écart se réduit.

**Verdict** : le signal basse-z se décompose en ~54 % « absorbable par calibration » et ~46 %
« forme ». Ni dissolution, ni innocence — une dégénérescence chiffrée, à porter dans A et à
généraliser (matrice de tension par paire de sondes, étude proposée).

## AUDIT DU MODÈLE NUL (19/08, passe complète) — trois prises, dont une grave
**Prise 1 — le triangle des −2,4 était suspect : c'est une STRUCTURE, pas un bug.** Trois nombres
coïncident (BAO seuls −2,43 ; gain de l'offset −2,40 ; gain de forme survivant −2,38). Explication :
une recalibration SNe ne peut pas toucher le secteur BAO, donc *ce qui survit à la nuisance EST la
préférence BAO*. Écart 0,05 unité. Conséquence déflationniste : le « gain de forme » du modèle
basse-z se réduit à la préférence BAO seule, soit ~1,5σ.
**Prise 2 — « 54 % » était du théâtre de précision.** Un gain de 2,4 pour un paramètre vaut
p ≈ 0,12 (~1,2σ), et l'erreur jackknife sur Δχ² est ±1,8. La seule phrase honnête :
*« environ moitié-moitié, chaque moitié à ~1σ »*. Corrigé partout (papier A résumé + section).
**Prise 3 — GRAVE : attribution fabriquée.** Dans ma propre correction, j'avais écrit
« Toussaint et al. » pour l'étude bayésienne — nom **inventé** (la source ne donnait que titre et
référence). Purgé et remplacé par la citation vérifiable (*Dynamic or systematic?*, MNRAS 548,
arXiv:2509.13220). L'interdit le plus strict du corpus, violé dans un tour de correction : preuve
que la vigilance doit porter aussi sur les corrections elles-mêmes.

**Confrontation littérature (19/08)** — notre test n'est PAS neuf, et c'est dit dans le papier :
- Efstathiou 2024/2025 (MNRAS 538, 875 ; arXiv:2408.07175) : offset ~0,04 mag bas-z/haut-z ;
  **Pantheon+ seul ne préfère pas l'énergie noire évolutive** — cohérent avec notre SNe seules −0,12.
- Vincenzi et al. 2025 (MNRAS 541, 2585) : réponse DES — écarts pleine-échantillon ~0,01 mag,
  les 0,04 s'expliquent par modélisation d'hôte, SALT, biais de sélection. Débat ouvert.
- *Dynamic or systematic?* (MNRAS 548, arXiv:2509.13220) : **traitement bayésien formel de
  l'alternative w(z)-vs-systématiques — exactement l'étude que j'avais proposée. Elle existe.**
- Notari, Redi & Tesi 2025 ; Dhawan, Popovic & Goobar 2025 ; recalibration Dovekie (DES 2026,
  qui trouve TOUJOURS une préférence évolutive) ; DEBASS DR0.5 (échantillon bas-z même instrument).
**Notre apport réel, réduit à sa juste taille** : la quantification pour CE modèle sur Pantheon+.
Rien de plus.
