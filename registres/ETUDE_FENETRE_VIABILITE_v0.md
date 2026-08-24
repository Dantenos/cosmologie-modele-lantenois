# La fenêtre de viabilité des systèmes auto-consommateurs — Étude v0
**É. Lantenois, avec assistance IA — 18 août 2026**
*Méthodologie héritée du projet énergie-noire : règles figées avant les calculs, conditions de mort déclarées, sources étiquetées [SOURCE]/[ordre]/[NON VÉRIFIÉ], erratas publics.*

## 1. Question
Tout système qui se maintient en digérant sa propre substance semble posséder un taux
d'auto-consommation borné des deux côtés : trop lent → encrassement/gel ; trop vite →
auto-dévoration mortelle. Existe-t-il, une fois la variable adimensionnée, une fenêtre
de viabilité COMMUNE à travers les échelles — de la cellule à la hiérarchie d'univers ?

## 2. La variable, et le garde-fou anti-tautologie
**x ≡ τ_c / τ_s**, avec :
- **τ_s** = temps pour traiter UNE FOIS sa propre substance au taux courant (M/Ṁ_auto, ou E/Ė) ;
- **τ_c** = temps de renouvellement structurel REQUIS, défini **indépendamment** du flux
  d'auto-consommation (demi-vie de dégradation spontanée des composants, temps
  d'obsolescence, âge du système pour les objets cosmologiques).

**Les deux lectures de x (amendement 19/08, détecté par l'audit du rail)** : la variable admet
deux conventions, jusqu'ici mélangées sans le dire — **x_self** (strict : le système traite SA
substance — cellule, univers, feux, capital) et **x_débit** (throughput total normalisé au contenu
propre — mammifère, dont le τ_s basal est l'apport alimentaire). Chaque ligne porte désormais sa
lecture. Jonction physique des deux : quand le débit externe sature (plafond alimentaire), l'excès
devient nécessairement auto-consommation — les coureurs d'ultra-endurance puisent leur masse
[Science Adv. 2019] : le bord du régime débit est l'entrée du régime self. Là où les deux lectures
sont calculables (mammifère : turnover protéique propre ~33 j), elles concordent à un facteur ~2.

**Garde-fou (obligatoire)** : sont EXCLUS les systèmes où τ_c ne peut être défini que comme
« le temps que met le flux à tout renouveler » (épithéliums, etc.) — circularité. Pour chaque
système retenu, τ_c doit avoir une définition physique autonome, et un test de sensibilité
(choix alternatifs défendables de τ_c) doit borner le déplacement de x à moins d'une décade.

## 3. Conditions de mort (pré-enregistrées, AVANT les données)
L'hypothèse « fenêtre commune » est MORTE si :
- (M1) les x des systèmes auto-renouvelants s'étalent sur > 2 décades après garde-fou ;
- (M2) les contrôles (systèmes qui consomment sans se rebâtir, ou inertes) tombent DANS
  la fenêtre aussi souvent que dehors ;
- (M3) le test de sensibilité déplace un système à travers la fenêtre de > 1 décade ;
- (M4, ajoutée 19/08 AVANT toute nouvelle donnée, EXÉCUTÉE le jour même — §4 ter) : bords hauts
  soutenus de quatre classes indépendantes dans [1,3 ; 3,5], étalement 0,43 décade < 1 : **passée**.

## 4. Premières données (v0 — deux vérifiées à la source, cinq en ordre de grandeur)

| Système | τ_s | τ_c | **x** | Statut source |
|---|---|---|---|---|
| Cellule, autophagie basale (0,7 %/h) | 143 h | 53 h | **0,37** | [MIXTE : le basal ~0,5-1 %/h est un ordre (Mortimore) ; les nombres SOURCÉS sont l'incrément de privation +3 %/h (PMC3879708), les 2-3 %/4 h en privation (PMC6168274) et les ~20 % de calories (PMC6368412) ; τ_c = demi-vie médiane ~36 h/ln2 (Schwanhäusser 2011, ordre) — **RISQUE PIM DÉCLARÉ (relecture doctorant, 19/08)** : ces demi-vies sont mesurées machinerie ALLUMÉE, elles incluent le traitement — même entrelacement que le capital ; réparation par notre propre loi : **la route de réparation évidente ÉCHOUE (testée 19/08)** : l'inhibition protéasomale fait culminer les protéines polyubiquitinées à ~12 h [SOURCE : Circulation 2002, MG132 en CMLV ; confirmé par analogues GTP, LNCaP], mais (i) ce pic mesure le remplissage du pool RÉGULATEUR à demi-vie courte, pas l'horloge de dommage spontané, et (ii) MG132 est LÉSIONNEL (mort apoptotique, dysfonction mitochondriale, stress oxydatif — oligodendrocytes 2006), donc il échoue au critère « sans lésion » de notre propre loi des privations. Pris au pied de la lettre, 12 h donnerait x = 0,08, très sous la fenêtre — ce qui montre que la mesure est inadéquate, pas que la ligne est fausse. **τ_c cellulaire nu : TOUJOURS NON MESURÉ.** Piste restante : cinétique des protéines carbonylées (dommage oxydatif spécifique) ou taux d'oxydation in vitro] |
| Cellule affamée (+3 %/h) | 27 h | 53 h | **1,95** | [SOURCE : idem] |
| Mammifère entier (humain) *(lecture débit)* | 65 j | 17-50 j | **0,5** (0,26-0,77) | [τ_c SOURCÉ : turnover protéique 300-400 g/j (PubMed 22139560 ; Waterlow 1978), méthodes récentes jusqu'à 600 g/j (dépendance de méthode ×2 déclarée) ; caveat du fondateur : « aucune méthode de vérification n'existe » (Waterlow, Annu. Rev. Nutr. 1995) ; lecture self concordante à ×2] |
| Parc mitochondrial (mitophagie) | 2-26 j selon tissu | ~[ordre] | **~0,5-1** | [τ_s SOURCÉ : foie 1,8-4 j (PMC2659384 ; J Mol Med 2015), cœur 14 j, synaptique 25,7 j (Sci Rep 2023) — dispersion intra-classe ×10 déclarée, τ_c par privation (19/08) : PARTIELLE seulement — les rats PINK1-KO accumulent les anomalies en 4 mois, symptômes à 6, dégénérescence à 9 [PMC4710791], MAIS la mitophagie PINK1-indépendante continue pendant le KO [eLife 2018] : τ_c ≤ 4-6 mois est une BORNE SUP, pas une mesure → x ≤ 4-6, tension avec la fenêtre déclarée, confondant identifié (redondance génétique) ; modulations cohérentes : restriction alimentaire accélère, perte de parkin allonge] |
| Écosystème pyrophile adapté | 30 a | 25 a | **0,83** | [SOURCE : FRI historique 5-35 ans ≈ récupération du combustible, USFS 2023] |
| Capital économique | 20 a | 18 a | **0,90** | **SUSPENDUE — mais raison CORRIGÉE (19/08, audit des audits)** : j'avais écrit que la dépréciation est *dérivée* des durées de vie supposées. **Faux** : les taux du BEA viennent des prix de revente d'actifs d'occasion [SOURCE : Hulten & Wykoff 1981 ; BEA SCB juillet 1997 ; ~55 % de l'équipement durable couvert par des données de marché], donc τ_s est empirique et indépendant. La suspension tient pour deux autres raisons, plus étroites : (i) la pondération par les courbes de survie (Winfrey) réinjecte des durées de vie dans l'estimation ; (ii) surtout, **notre τ_c (obsolescence) n'est toujours pas mesuré indépendamment** — c'est là qu'est le vrai défaut, pas dans la dépréciation. Chemin de réparation précisé : τ_s = Hulten-Wykoff (revente), τ_c = données d'obsolescence technologique ou de défaillance d'ingénierie. Caveat annexe : l'OCDE signale une circularité quand le taux de rendement est calculé de façon endogène ; et des études récentes (Statistique Canada 2007/2015 ; Bokhari-Geltner 2019) trouvent des dépréciations plus rapides, surtout pour les structures |
| Neurone post-mitotique (jeune) | ~50 j | ~20 j | **~0,4** | [ordre ; contrainte unique : doit tenir x dans la fenêtre ~80 ans sans dilution mitotique] |
| **Univers-hiérarchie (β = 2,42)** | 5,7 Ga (t/β) | 4,8 Ga (1/3H, dilution) | **0,85** | [calculé ; définition conforme au garde-fou : la « dégradation » est la dilution — ancienne définition (t₀ vs M/Ṁ) : 1,66, conservée en sensibilité] |
| — fenêtre théorique (1 < β < 4,35) | | | **0,35 – 1,53** | [gel de profondeur + GSL, définition-dilution ; ancienne : 0,69–3,0] |
| *Contrôle : Soleil (brûle sans rebâtir)* | 1 400 Ga | 10 Ga | *0,007* | hors fenêtre ✓ |
| *Contrôle : montagne (érosion passive)* | ~∞ | — | *~10⁻⁷* | hors fenêtre ✓ |

## 4 bis. Les morts-par-taux (le test décisif du §6, exécuté)

| Mort | Système | x au moment fatal | Issue | Statut |
|---|---|---|---|---|
| **Par le bas** (encrassement) | Forêts sèches de l'Ouest US, un siècle de suppression | ~0,15–0,3 (intervalle étiré 3-6×) | 2,9–13,6× plus de feux destructeurs-de-peuplement ; conversions vers le non-forêt | [SOURCE : USFS/Parks et al. 2023 ; Fire Ecology 2026] |
| — contrôle naturel | Gila Wilderness (feux non supprimés, x maintenu ~0,8) | ~0,8 | seulement 1,8× — le régime adapté survit | [SOURCE : idem — **expérience naturelle avec contrôle**] |
| **Par le haut** (sur-consommation) | Forêt boréale, intervalles < 30 ans (récupération 70-130 ans) | ~3–4 | échec de régénération, source de C, transition hors-forêt | [SOURCE : Fire Ecology 2025, PMC12511247] |
| **Par le bas** (dérive du vieillissement) | Neurones âgés / neurodégénérescence | x décline avec l'âge | agrégats toxiques (α-syn, Aβ, tau), cercle vicieux sénescence↔autophagie, mort neuronale ; dose-réponse génétique (LRRK2) ; réversible par rapamycine | [SOURCE : Neuron 2024 (S0896-6273(24)00663-9) ; PMC6928047 ; PMC4702340 — « ne peuvent diluer le dommage par mitose »] |
| **Par le haut** (autose) | Cellules en privation soutenue | bord à ~2 (affamée = 1,95) | mort dose-dépendante, ~1 % des cellules affamées, bloquée par inhibition d'autophagie | [SOURCE : Liu et al. PNAS 2013 ; seuil quantitatif non publié — borne : « x soutenu ≳ 2 »] |
| **Par le haut** (thermodynamique) | Hiérarchie, β > 4,35 | > 3,0 | enfants GSL-non-viables | [calculé, étude énergie-noire] |

**Lecture** : les morts encadrent la fenêtre par les deux côtés (≲ 0,2 et ≳ 2–3), le vivant mesuré
tient dans [0,37 ; 1,95], et l'expérience naturelle de la Gila fournit le contrôle que le biais de
survivant réclamait : à conditions égales, garder x dans la fenêtre = survivre, en sortir = mourir.
La condition de mort M2 est doublement passée (contrôles inertes hors fenêtre + morts-par-taux hors fenêtre).

## 4 ter. M4 exécuté : le rail des bords hauts (19/08)
Quatre classes indépendantes, quatre mécanismes, un rail :

| Classe | x_max soutenu | Mécanisme | Source |
|---|---|---|---|
| Mammifère *(lecture débit)* | **1,3** (2,5× basal, durée indéfinie) | plafond alimentaire/dissipation — au-delà, l'excès est de l'auto-consommation par définition | [SOURCE : Science Advances 2019 (aaw0341) ; Hammond-Diamond, Nature 386, 457 : 7× en pointe ; ancêtre : Drent & Daan 1980, « parent prudent », ~4×] |
| Cosmologie | **1,53** (β < 4,35) | GSL sur l'entropie totale | [calculé] |
| Cellule | **~1,9** (faillite budgétaire ; autose) | budget énergétique | [SOURCE : 20 % cal. + Liu PNAS 2013] |
| Écosystème boréal | **~3,5** (échec de régénération) | récupération du combustible | [SOURCE : Fire Ecol. 2025 — bord le plus fragile] |

**Étalement du rail : 0,43 décade — M4 passée.** Étiquetage honnête : deux bords sont EXTERNES et mesurés (mammifère 1,3 ; boréal ~3,5 — à eux seuls : 0,43 décade), deux sont DÉRIVÉS de nos propres cadres (GSL 1,53 ; budget cellulaire 1,85) — la concordance interne-externe est le contenu, la « quadruple indépendance » d'une version antérieure était survendue (corrigé). Et une structure à deux
étages émerge : le plafond **décroît avec la durée d'exposition** — mesuré chez l'humain (7× sur
des jours → 2,5× indéfini), observé chez la cellule (affamée 1,95 transitoire survivable, soutenu
= autose), imposé en cosmologie (la GSL borne l'attracteur, donc le régime soutenu par définition).
Les excursions transitoires vivent à ~2-4 ; le bord soutenu, le vrai bord de la fenêtre, à ~1,3-2.
Quatre mécanismes indépendants, tous de la famille débit/budget : la concordance n'est pas
numérique seulement, elle est mécanistique.

## 4 quater. L'hibernation : la solution périodique (19/08 — le stress test le plus dur, passé)
L'hibernant supprime son métabolisme à 1-5 % du basal pendant des mois — x s'effondre sous la
fenêtre — et survit. Contre-exemple ? Non : **cycle limite à travers la fenêtre.** *(i)* Pendant la
torpeur, la machinerie d'auto-traitement s'arrête (protéasome, autophagie inactifs à froid
[Physiology 2015]) mais la dégradation continue, ralentie par Q10 (f_d ~ 0,05-0,15) : la dette
d'encrassement s'accumule — stress oxydatif, dommages neuronaux, immunosuppression [PBZ 2003].
*(ii)* « Il y a une limite à la durée de torpeur survivable » (Carey) — l'énoncé même de la fenêtre.
*(iii)* Les réveils inter-épisodes — 12 h toutes les ~2 semaines, 70-80 % du budget hivernal, « le
plus grand mystère de l'hibernation » — sont les remboursements : la métabolomique montre les
métabolites accumulés en torpeur restaurés à CHAQUE réveil [Physiol. Genomics 2011], et parmi les
processus restaurés, la dégradation protéasomale elle-même. *(iv)* Le bilan du cycle est *compatible* avec l'équilibre : sur la grille complète des paramètres plausibles (f_d ∈ [0,05 ; 0,15], traitement au réveil 2-4× basal), le rapport remboursement/dette couvre [0,67 ; 4] — cohérence, pas bouclage démontré (une version antérieure n'affichait que la diagonale favorable : corrigé). *(v)* Attribution : l'hypothèse de restauration d'homéostasie est l'explication dominante DÉJÀ PUBLIÉE des réveils (Carey et al. 2003 ; Epperson 2011 ; métabolomique Physiol. Genomics 2011) — la relation durée-température lui appartient ; l'apport de la fenêtre est la comptabilité adimensionnée qui place ce mécanisme sur le même axe que l'autose et la GSL, rien de plus. Le système qui ne peut pas résider dans la fenêtre la traverse périodiquement.

## 5. Verdict v0
**Huit systèmes auto-renouvelants, ~32 ordres de grandeur de masse : x ∈ [0,37 ; 1,95] —
0,7 décade de dispersion.** Les deux contrôles tombent à 10⁻² et 10⁻⁷, hors fenêtre comme
prédit. Les deux fenêtres — biologique mesurée [0,37 ; 1,95] et cosmologique dérivée (0,35 ; 1,53], définition-dilution — **se recouvrent presque exactement**, et leurs bords hauts INDÉPENDANTS (autose ~2 ; GSL 1,53) ne diffèrent que de ~30 % : première concordance de bords inter-classes, le test que M4 réclame. Aucune condition de mort déclenchée. Le motif tient — et le §5 bis le DÉRIVE d'un modèle minimal à deux ingrédients, dont la borne haute depuis un nombre sourcé indépendant (accord 5 %).

## 5 bis. Le modèle minimal : la fenêtre se DÉRIVE (v0.3)

Deux ingrédients suffisent à produire la fenêtre depuis les premiers principes :
- **Borne basse — l'encrassement.** Composants endommagés au taux 1/τ_c, auto-traitement au
  taux x/τ_c avec sélectivité σ (préférence pour l'abîmé). État stationnaire de la fraction
  endommagée : (1−d)(σd+1−d) = xσd. Sous x_min, d* sature vers 1 (effondrement de la fraction intacte) ; le *cercle vicieux* observé dans le vieillissement neuronal correspond à la rétroaction machinerie (capacité de traitement ∝ fraction intacte), amplificateur biologique déclaré hors du modèle minimal. Pour σ ∈ [3;10] et tolérance d_max ∈ [0,5;0,7] :
  **x_min = 0,31–0,66** (illustratif, paramètres post-hoc plausibles).
- **Borne haute — le budget, avec le nombre SOURCÉ** (désormais à double appui : le coût énergétique du turnover protéique corps-entier vaut lui aussi ~20 % du métabolisme de repos [PubMed 22139560] — deux comptabilités voisines mais distinctes convergent sur m_basal ~ 0,2 ; noté sans y voir plus qu'une cohérence d'échelle). Coût de maintenance linéaire
  m(x) = m_basal·x/x_basal ; avec m_basal = 20 % à x_basal = 0,37 [SOURCE : PMC6368412],
  tout le budget est dévoré par l'auto-traitement à **x_max = 0,37/0,20 = 1,85** — et le bord de mort observé (autose, ~1,95) se trouve 5 % *au-delà* du point de faillite : mourir juste après avoir dépassé 100 % du budget est exactement la physique attendue (excursions transitoires possibles, régime soutenu impossible). **Accord d'ordre depuis un nombre indépendant** (le « 5 % » nominal est du théâtre de précision : ±30 % réels de part et d'autre) — avec le caveat de niveau déclaré : le 20 % est organismal, appliqué ici au cellulaire (cohérent en ordre).

**Fenêtre dérivée [0,33 ; 1,85] contre mesurée [0,37 ; 1,95].** La fenêtre n'est plus une
coïncidence : c'est le corridor entre l'encrassement et la faillite énergétique. Honnêteté :
la borne basse est illustrative (σ, d_max choisis) ; la borne haute est la vraie prédiction.

## 5 quater. L'identité x = −w (19/08)
Avec la définition conforme au garde-fou (τ_c = temps de dilution 1/3H ; τ_s = temps d'injection
t/β), la variable de viabilité de l'univers vaut **x = β/(3Ht) = −w exactement** — et l'identité est GÉNÉRALE *sous une convention déclarée* : la substance nue, non maintenue, se dilue sans pression (a⁻³) — alors −w est la fraction de cette dilution que la maintenance compense (ρ ∝ a^{−3(1+w)}). La cartographie β→w utilise Ht fixé au best-fit (variation ~10-15 % sur la fenêtre). Dictionnaire : **Λ = maintenance exactement critique (x = 1)** ;
fantôme = sur-maintenance (côté autotique) ; quintessence = sous-maintenance (côté encrassement) ;
**le croisement fantôme = le passage par la criticité** — l'univers sur-maintenait, il sous-maintient
depuis z ≈ 0,4-0,5, et il siège aujourd'hui à x = 0,85, au cœur du peloton vivant.
*Parenté formelle (19/08)* : une reconstruction thermodynamique récente écrit w = −1 + Ṡ_h/(3H·S_h) (arXiv:2604.18723) — même famille (w = rapport de taux thermodynamiques), côté horizon quand la nôtre est côté substance ; la stabilité thermodynamique classique exige w ≥ −1 par positivité d'entropie du fluide (Duarte & Silva, EPJC 2019) — notre borne GSL (−1,53), portant sur l'entropie TOTALE, est plus permissive, différence contentful ; et le croisement de −1 est thermodynamiquement régulier, crossover lisse et non transition de phase (CQG) — compatible avec la lecture « passage par la criticité ». **La trajectoire de vie (19/08, calculée)** : x(z) = −w(z) sur le fond au best-fit — l'univers naît à
x ≈ 1,35 (88 % de son bord soutenu GSL, frôlé jamais franchi), traverse la criticité à z = 0,46, siège
à 0,85 aujourd'hui, s'installe sur l'attracteur à 0,55 : une vie entière DANS la fenêtre soutenue —
proche du bord dans la jeunesse, au cœur du peloton dans l'âge. (Correction en passant : une première
estimation de tête donnait 1,6 au lieu de 1,35 — le calcul a tranché avant propagation.)



**PROPAGATION DE L'ERRATUM β (19/08)** : le profil Planck complet donne β = 2,56 (+0,08/−0,02) contre 2,42 ± 0,07 marginalisé sur la vraisemblance légère. Pour la fenêtre : x aujourd'hui vaut **0,85 (β = 2,42) ou 0,90 (β = 2,56)** — les deux dans la fenêtre [0,35 ; 1,53] ; la borne GSL et l'appartenance au peloton sont inchangées. Les valeurs de trajectoire citées ici (1,35 → 0,85 → 0,55) sont celles de β = 2,42 ; à β = 2,56 elles deviennent ~1,43 → 0,90 → 0,56, soit un passé légèrement plus proche du bord GSL. Aucune conclusion de l'étude ne bascule.

*Les deux faces, déclarées* : (i) l'identité est en partie définitionnelle (w ~ −1 ⇒ x ~ 1 par
construction — le danger tautologique revient par ici) ; (ii) son contenu réel est que les bornes
de la fenêtre deviennent des bornes sur w — **viabilité ⇔ w ∈ [−1,53 ; −0,35]** (GSL + gel de
profondeur), l'énergie noire observée siégeant à −0,85, en plein milieu — et que le vocabulaire
de la maintenance (encrassement, autose, criticité) devient un vocabulaire d'équation d'état.

## 5 bis-2. Le diagramme de viabilité (v0.6 — 19/08)
Le modèle minimal étendu d'un terme de croissance-dilution (γ = g·τ_c, matière neuve intacte) :
d′ = (1−d) − xσd/(σd+1−d) − γd. La fenêtre 1D devient un **diagramme 2D (x, γ)** dont la
frontière basse x_min(γ) décroît de 0,33 (γ=0) à 0 à **γ_crit = (1−d_max)/d_max ≈ 0,43**
(analytique) : au-delà, la dilution pure suffit. Les trois stratégies sont les régions du plan :
résidence (γ≈0, x dans la fenêtre — neurone, cellule, os), dilution (γ > γ_crit, x libre —
bactérie exponentielle, bord prolifératif de tumeur), transit (cycle limite vertical — hibernant).
**La zone morte du diagramme (γ=0, x<x_min) est observée en clinique : le cœur nécrotique des
tumeurs** — privé d'approvisionnement, sans division ni traitement, d*→1. Cas structurellement
distinct déclaré : l'univers — son « g » (l'expansion) dilue la substance *maintenue*, pas les
dommages : g effectif négatif, hors du plan biologique, cohérent avec sa position historique côté
vorace. Honnêteté : σ et d_max hérités du modèle 1D (post-hoc plausibles) ; le diagramme est une
extension du même modèle illustratif, pas une loi indépendante — sa valeur est d'unifier les trois
stratégies en une équation et de prédire la nécrose de cœur comme région, pas un chiffre.

## 5 ter. Parenté ancienne (le motif a des ancêtres)
La fenêtre trans-échelles a deux ancêtres classiques, à citer et à dépasser : la **rate of
living** (Pearl 1928 ; réévaluation critique Speakman 2005) — l'énergie dissipée par gramme
et par vie serait quasi constante — dont notre x est la version corrigée (rapportée au temps
de maintenance requis, pas à la vie entière) ; et le **soma jetable** (Kirkwood 1977) —
l'organisme arbitre son budget entre maintenance et fonction — dont notre borne haute est
la version quantitative : x_max est le point où l'arbitrage devient impossible. [classiques,
cités de mémoire — références canoniques à confirmer en rédaction]

## 5 quinquies. Stratification par qualité de source (19/08 — au lieu de la suppression)
Question posée : faut-il éliminer les lignes [ordre] ? **Réponse calculée : non — stratifier.**

| Strate | n | x | dispersion | attendu sous H₀ (tirage uniforme-log sur 2 décades) |
|---|---|---|---|---|
| A : deux horloges sourcées | 2 | 0,83–1,17 | 0,15 déc. | 0,67 déc. — **peu informatif (petit n)** |
| A+B : ≥ une horloge sourcée | 6 | 0,50–1,95 | 0,59 déc. | 1,42 déc. — informatif |
| A+B+C : tout | 9 | 0,37–1,95 | 0,72 déc. | 1,60 déc. — **le plus informatif** |

**Le piège** : une plage se rétrécit *mécaniquement* quand n baisse. Purger les [ordre] donnerait
une fenêtre plus étroite et **moins** significative — l'apparence de rigueur contre la substance.
Deux dangers supplémentaires nommés : (i) le *source shopping* — chercher jusqu'à trouver le
nombre publié qui tombe dans la fenêtre (parade : décider AVANT quelle mesure on accepterait) ;
(ii) le *biais de littérature* — ne garder que le bien étudié, c'est ne garder que la biomédecine
humaine et perdre les 32 ordres de grandeur, qui sont l'argument central. **Règle adoptée** :
aucune ligne n'est supprimée pour cause d'[ordre] ; toute conclusion est rapportée par strate ;
une ligne n'est suspendue que pour violation du garde-fou (capital) ou bracket non contraignant
(foie).

## 6. Réserves (déclarées, non négociables)
- Quatre à cinq systèmes sur huit restent en [ordre de grandeur] (dont le basal cellulaire, à étiquette mixte) : la clusterisation peut refléter en
  partie le fait que « viable » sélectionne x ~ O(1) par définition douce (biais de
  survivant + choix humain des τ_c). Le test décisif des morts-par-taux est EXÉCUTÉ (§4 bis) :
  cinq cas documentés, les morts encadrent la fenêtre des deux côtés, et la Gila fournit
  l'expérience naturelle avec contrôle. Reste : le seuil quantitatif de l'autose (non publié).
- La sensibilité (M3) est EXÉCUTÉE sur quatre systèmes (cellule, mammifère, univers, feux) : choix alternatifs défendables de τ_c → étalement maximal ~0,5 décade, aucun système ne traverse la fenêtre. **M3 passée.**
- Le contrôle « Soleil » teste « consommer sans rebâtir » ; il faut aussi un contrôle
  « rebâtir sans consommer de soi » (cristal en croissance ?) pour isoler les deux moitiés.

## 6 bis. Nouveaux systèmes (v0.5 — 19/08, régime sobre)
Quatre membres ajoutés, tous [ordre], définitions explicites : **os** (remodelage ~10 %/an [ordre standard] vs microfissures de fatigue : x ~ 0,8 — **mort basse SOURCÉE à quatre références** : la suppression prolongée du remodelage par bisphosphonates cause l'accumulation de microdommages non réparés et les fractures fémorales atypiques [PMC12681184 ; NEJM NEJMc1107029 ; PMC4480549], avec accumulation qualifiée d'*exponentielle* par la littérature elle-même [PMC6174857] — la dynamique de saturation du modèle d'encrassement, décrite indépendamment ; incidence 3-9,8/100 000 p-a, seuil > 5 ans [PMC9852062] ; mort haute SOURCÉE (19/08) : le turnover excessif crée des cavités de résorption « concentrateurs de contrainte », perfore les travées, et prédit la fracture INDÉPENDAMMENT de la densité — résorption au-dessus de la gamme préménopausique ⇔ risque ~doublé, hanche et vertèbres, suivis 1,8-5 ans [Mayo Clin. Proc. 2005 ; NIHR HTA ; Medscape/OFELY] ; hétérogénéité des études déclarée [PMC5995756] — bord haut osseux : x soutenu ≳ 1,5-2, concordant avec le rail) ; **foie** (**RÉVISÉ 19/08, facteur 5 déclaré** : mon τ_s initial ~300 j était une échelle murine — l'humain, mesuré au radiocarbone sur donneurs de 20-84 ans, se renouvelle à 19 %/an jeune, 17 %/an âgé, âge moyen hépatocytaire < 3 ans [SOURCE : Heinke et al., Cell Systems 13, 499 (2022)] → τ_s ≈ 5 a ; τ_c par privation (19/08) : IMPURE — la maladie chronique confond lésion et arrêt du renouvellement ; deux acquis quand même : « un foie cirrhotique montre plus de sénescence que le foie d'un centenaire sain » [J. Hepatol. 2010] — l'horloge nue de sénescence en santé est > 100 ans, c'est le renouvellement qui la tient ; et une tension de méthode τ_s interne au champ : télomères ~1 an [Ozturk 2009] vs radiocarbone ~5 ans, ×5 déclarée ; τ_c reste [ordre-large, 2-20 a] → x ∈ [0,4 ; 4], la ligne la plus incertaine de la table, SUSPENDUE du décompte M1 (relecture doctorant 19/08 : un bracket qui couvre toute la fenêtre ne contraint rien) ; fait sourcé notable, consigné sans plus : le turnover est INVARIANT avec l'âge — l'organe qui tient son x constant résiste au vieillissement, là où le neurone, dont le flux décline, le conduit ; la régénération post-hépatectomie = excursion transitoire) ;
**ville** (stock bâti — **PROMUE, et sauvée là où le capital est tombé** : τ_s empirique via les démolitions OBSERVÉES — durée de vie moyenne 71 ± 28 ans sur ~15 000 bâtiments, Kaplan-Meier [Buildings & Cities, 10.5334/bc.588] ; τ_c : la privation (abandon) révèle un EMBALLEMENT par rétroaction, pas une constante nue — « chaque brèche invite plus d'eau... intacts quelques années puis détérioration dramatique » [ScienceInsights 2026] : 3-15 ans jusqu'à l'irréparable selon climat [Exovations], mais c'est le temps de fuite de la boucle (4e observation indépendante de la rétroaction machinerie, après neurone/os/érythrocyte) ; le τ_c d'état-intact reste borné par la toiture (20-30 ans) et la conception (50 ans) [ordre-borné] → x ∈ [0,3 ; 0,7] : deux horloges de deux littératures distinctes, le champ critiquant lui-même la confusion conception/réel — x ~ 0,7, dispersion inter-régions déclarée : Japon 38 a / US 67 / UK 81, dépréciation 6 %/an vs 1 % [Sci. Direct 2022] ; mort basse documentée — décroissance urbaine ; mort haute non documentée, asymétrie déclarée) ; **population érythrocytaire** (**DÉ-SUSPENDUE 19/08 — la circularité brisée par la privation** : le sang stocké est un renouvellement strictement nul, où la dégradation se montre nue ; le critère réglementaire (≥ 75 % de survie 24 h post-transfusion à 42 jours ; ~17 % de perte de potence à péremption [SOURCE : FDA/UE ; JCI 2017 ; Haematologica 2018]) donne τ_c = 42/ln(1/0,75) ≈ 146 j — mesuré hors du corps, littérature transfusionnelle sans lien avec le retrait in vivo ; τ_s = 125 j (0,8 %/j) → **x ≈ 1,17**, dans la fenêtre. La « lésion de stockage » décrit un cercle vicieux ATP↓ → glycolyse↓ → ATP↓ [Anaesthesia 2015] : la rétroaction machinerie du §5 bis, observée indépendamment pour la troisième fois après le neurone et l'os). Une **exclusion** : la colonie d'abeilles (τ_c non
indépendant — le garde-fou travaille). Et le candidat-casseur le plus sérieux : la **bactérie en
croissance exponentielle**, x_self ~ 0,1, sous la fenêtre et viable — mécanisme : la
croissance-dilution REMPLACE l'auto-traitement (troisième stratégie après la résidence et le
transit périodique) ; test de cohérence [classique] : en phase stationnaire, dilution nulle, la
protéolyse doit monter — c'est le résultat de Mandelstam (turnover ×4-5). C'est exactement
l'option qui manque au neurone (« cannot dilute through mitosis », Neuron 2024). Bilan : fenêtre
M1 : [0,37 ; 1,95] sur 11 membres décomptés (capital ET foie suspendus ; érythrocyte dé-suspendu) ; pas de casseur, mais une taxonomie des stratégies qui
s'enrichit : résider / transiter / diluer.

## 6 ter. Le chantier des privations — CLOS (19/08), avec sa loi de méthode
Six privations tentées pour extraire les τ_c nus : **deux propres** (érythrocyte stocké : privation
totale, exogène, hors du corps → τ_c = 146 j, ligne dé-suspendue ; os/bisphosphonates : suppression
pharmacologique quantifiée → mort basse sourcée ×4), **une sourcée par l'épidémiologie** (os côté
haut : résorption élevée ⇔ fracture ×2, indépendant de la densité), **une partielle** (mitochondrie :
le PINK1-KO laisse tourner la mitophagie de secours → borne sup seulement, x ≤ 4-6, tension
déclarée), **une en emballement** (ville : l'abandon mesure le temps de fuite de la rétroaction, pas
la constante nue), **une impure** (foie : confondant lésionnel ; mais l'horloge saine > 100 ans est
établie par contraste centenaire/cirrhose). **Loi de méthode, gravée pour la suite : un bon
τ_c-mètre exige une privation TOTALE, EXOGÈNE et SANS LÉSION** — le stockage et le médicament
mesurent, le mutant borne, la maladie brouille. Et la rétroaction machinerie du §5 bis est
maintenant observée indépendamment par QUATRE littératures (neurone, os, érythrocyte, bâtiment).

## 7. État du programme (mis à jour 19/08 — l'ancienne liste était devenue un fossile)
**FAIT — l'intégralité de la liste v0 :** ✓ les lignes [ordre] vérifiées à la source (mitophagie,
feux, mammifère, foie, ville, érythrocyte, os — et capital : RÉTROGRADÉ par sa vérification,
entrelacement PIM) ; ✓ les morts-par-taux documentées (autose — seuil quantitatif non publié,
borné « x soutenu ≳ 2 » ; feux post-suppression 2,9-13,6× avec le contrôle Gila ; β > 4,35 ;
plus neurodégénérescence, boréale, nécrose tumorale) ; ✓ systèmes ajoutés (ville, colonie —
exclue par garde-fou, foie, neurone, os, érythrocyte, bactérie) ; ✓ M1-M4 toutes passées ;
✓ rédaction courte v0 (fenetre_viabilite.pdf, 5 p.) ; ✓ chantier des privations clos avec sa
loi de méthode. **Dernier item traité (19/08)** : la binaire X — τ_s ~ 10⁹ ans mais AUCUN τ_c
(le transfert est piloté par l'évolution orbitale, rien n'est reconstruit) : exclusion par le
garde-fou, deuxième contrôle de la classe « consommation sans reconstruction » après le Soleil —
M2 renforcée.

**RESTE (la vraie liste, courte) :**
1. **La rédaction est en retard sur le document** : le PDF v0 (5 p.) ne contient ni le diagramme
   de viabilité (x, γ), ni les trois stratégies, ni les nouveaux systèmes, ni la loi des
   privations — une passe de révision v1 est le premier travail.
2. Le seuil quantitatif de l'autose (non publié — veille).
3. Un τ_c mitochondrial par privation TOTALE (modèle à double KO des voies de secours, s'il existe).
4. M4 : bords soutenus de classes supplémentaires (le rail n'a que 4 points, dont 2 internes).
5. Relecture externe — le seul audit structurellement impossible d'ici.
