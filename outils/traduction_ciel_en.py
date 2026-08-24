# -*- coding: utf-8 -*-
"""Table de traduction FR -> EN du ciel v7. Ordonnee du plus long au plus court a
l'application, pour qu'aucun fragment ne soit avale par une entree plus courte."""

MAP = {
 # --- message de panne auto-diagnostique (ajoute apres les captures d ecran ;
 #     jamais entre dans la table, ce qui a fait refuser le generateur bilingue)
 "PANNE DE RENDU.": "RENDER FAILURE.",
 "La boucle a levé : ": "The loop threw: ",
 "Signale ce message : il nomme la cause. Utilise « réinitialiser la vue » pour repartir.":
   "Report this message: it names the cause. Use “reset view” to start again.",
 # --- entete et cadre
 "Le Cône d'Observation — le vide d'information": "The Observation Cone — the information void",
 "Le Cône d'Observation": "The Observation Cone",
 "· le vide d'information": "· the information void",
 "Chaque nombre affiché est calculé avant d'être dessiné.":
   "Every number shown is computed before it is drawn.",
 "glisser pour tourner · molette pour zoomer · survoler pour la ligne de visée · règle céleste : cliquer deux points · coupe : Maj + molette":
   "drag to rotate · wheel to zoom · hover for the line of sight · celestial ruler: click two points · clipping: Shift + wheel",
 "filtres": "filters", "outils": "tools", "repère &amp; capture": "frame &amp; capture",
 "rayon de vue": "view radius", "vue interne": "interior view",
 "visible à l'écran": "visible on screen", "vides": "voids",
 "profondeur : z ≤ ": "depth: z ≤ ", "curseur logarithmique": "logarithmic slider",
 # --- etapes et boutons
 "1 · Terre": "1 · Earth", "2 · Système solaire": "2 · Solar System",
 "3 · Voie lactée": "3 · Milky Way", "4 · Sphère": "4 · Sphere",
 "▶ visite guidée": "▶ guided tour", "🔦 phare Sgr A*": "🔦 Sgr A* beacon",
 "◉ scan radar": "◉ radar scan", "Stripe 82 seule": "Stripe 82 only",
 "sans Stripe 82": "without Stripe 82", "|b| < 10° seul": "|b| < 10° only",
 "masquer |b| < 10°": "hide |b| < 10°", "ciel isotrope": "isotropic sky",
 "vue observateur": "observer view", "balayage Stripe 82": "Stripe 82 sweep",
 "cônes d’ombre": "shadow cones", "graphe de proximité": "proximity graph",
 "déplier en 2D": "unfold to 2D", "plan de coupe": "clipping plane",
 "règle céleste": "celestial ruler", "traverser un vide": "fly through a void",
 "repère galactique": "galactic frame", "⤓ image sans HUD": "⤓ image without HUD",
 # --- textes des etapes
 "<b>r = 0.</b> Axe incliné de <b>": "<b>r = 0.</b> Axis tilted by <b>",
 "°</b> (calculé). L'anneau bleu est l'équateur céleste — il définit la déclinaison. L'anneau ambré est l'orbite terrestre : <b>":
   "°</b> (computed). The blue ring is the celestial equator — it defines declination. The amber ring is Earth's orbit: <b>",
 " km/s</b>, dérivée de 2πUA/an. Rotation et révolution fixent ensemble le calendrier des campagnes d'observation au sol.":
   " km/s</b>, derived from 2πAU/yr. Rotation and revolution together set the schedule of ground-based observing campaigns.",
 "obliquité mesurée entre pôle céleste et pôle écliptique (RA 270°, Dec +66,561°)":
   "obliquity measured between celestial pole and ecliptic pole (RA 270°, Dec +66.561°)",
 "Disque ambré : le <b>plan de l'écliptique</b>. Le semis extérieur est la <b>ceinture de Kuiper</b> (30–50 UA), qui s'estompe vers le <b>nuage de Oort</b> (2 000 – 100 000 UA, déclaré). C'est la frontière physique du système avant le vide interstellaire.":
   "Amber disc: the <b>ecliptic plane</b>. The outer scatter is the <b>Kuiper Belt</b> (30–50 AU), fading toward the <b>Oort Cloud</b> (2,000 – 100,000 AU, declared). This is the physical edge of the system before interstellar emptiness.",
 "rayons logarithmiques · aucune SN du catalogue ici":
   "logarithmic radii · no catalogue SN lies here",
 "Spirale à quatre bras, Soleil à <b>8,2 kpc</b> (≈ 26 700 al). La bulle translucide est la <b>Bulle Locale</b> : coquille IRRÉGULIÈRE, entre ~50 et ~150 pc du Soleil selon la direction (cartographie 3D de la poussière). Plan galactique / écliptique : <b>":
   "Four-armed spiral, Sun at <b>8.2 kpc</b> (≈ 26,700 ly). The translucent bubble is the <b>Local Bubble</b>: an IRREGULAR shell, ~50 to ~150 pc from the Sun depending on direction (3D dust mapping). Galactic / ecliptic plane angle: <b>",
 "°</b>, calculé.": "°</b>, computed.",
 "dessiner une sphère nette serait faux : la cavité n'en est pas une":
   "drawing a clean sphere would be false: the cavity is not one",
 # --- sphere
 " supernovae</b>, ": " supernovae</b>, ",
 " vides, ": " voids, ",
 " sursauts radio. Cône rouge : zone d'évitement, <b>": " radio bursts. Red cone: zone of avoidance, <b>",
 " SNe</b> à |b| &lt; 5° pour ": " SNe</b> at |b| &lt; 5° where ",
 " attendues. Pinceau doré : <b>SDSS Stripe 82</b>, ": " are expected. Golden beam: <b>SDSS Stripe 82</b>, ",
 " SNe (": " SNe (",
 " %) sur ": " %) over ",
 " % du ciel.": " % of the sky.",
 "évitement ": "avoidance ",
 "σ · Stripe 82 ×": "σ · Stripe 82 ×",
 " · z médian ": " · median z ",
 " contre ": " versus ",
 "fiduciaire déclarée ΛCDM plat Ω_m=": "declared fiducial: flat ΛCDM Ω_m=",
 " — PAS le modèle étudié": " — NOT the model under study",
 # --- phare, radar, ombre, graphe, vide
 "<b>Phare Sgr A*.</b> Tu regardes le cœur de la galaxie, b = ":
   "<b>Sgr A* beacon.</b> You are facing the heart of the galaxy, b = ",
 "° (contrôlé). Dans les 15° autour : <b>": "° (checked). Within 15° of it: <b>",
 " supernova</b>, pour ": " supernova</b>, where ",
 " attendues si le ciel était isotrope.": " are expected if the sky were isotropic.",
 "DEUX causes à ne pas confondre : l'extinction par la poussière ET l'évitement délibéré du plan par les relevés.":
   "TWO causes not to be conflated: dust extinction AND the deliberate avoidance of the plane by surveys.",
 "<b>Scan radar.</b> Une impulsion partie de la Terre, à la vitesse de la lumière. Elle atteint Neptune en 4 h, le bord de la Bulle Locale en 490 ans, Sgr A* en 26 700 ans — et les supernovae les plus lointaines après <b>":
   "<b>Radar scan.</b> A pulse leaving Earth at the speed of light. It reaches Neptune in 4 h, the edge of the Local Bubble in 490 years, Sgr A* in 26,700 years — and the most distant supernovae after <b>",
 " milliards d'années</b>, sur un univers qui en a ": " billion years</b>, in a universe that is only ",
 "regarder loin, c'est regarder tôt · temps calculés dans la fiduciaire déclarée":
   "to look far is to look early · times computed in the declared fiducial",
 "<b>Cônes d’ombre.</b> Chaque disque sombre est une cellule du ciel de ":
   "<b>Shadow cones.</b> Each dark disc is a sky cell of ",
 " deg² où <b>aucune</b> supernova n’a été observée. Il y en a ":
   " deg² in which <b>no</b> supernova was ever observed. There are ",
 " sur ": " out of ",
 " : <b>": ": <b>",
 " % du ciel</b>. Un tirage isotrope de même taille n’en laisserait que ":
   " % of the sky</b>. An isotropic draw of the same size would leave only ",
 " %.": " %.",
 "écart mesuré : ": "measured excess: ",
 "σ · grille d’aire égale (RA uniforme, sin(Dec) uniforme)":
   "σ · equal-area grid (uniform in RA, uniform in sin(Dec))",
 "ce n’est pas l’Univers qui est vide là : c’est nous qui n’y avons pas regardé":
   "it is not the Universe that is empty there: it is we who never looked",
 "<b>Graphe de proximité</b> — ": "<b>Proximity graph</b> — ",
 " arêtes, séparation médiane ": " edges, median separation ",
 " Mpc. <b>ATTENTION : ce n’est PAS la toile cosmique.</b> Les supernovae sont des traceurs épars et sélectionnés ; relier chacune à sa plus proche voisine dessine <b>où les relevés ont regardé</b>, pas où sont les filaments.":
   " Mpc. <b>WARNING: this is NOT the cosmic web.</b> Supernovae are sparse, selected tracers; joining each to its nearest neighbour draws <b>where the surveys looked</b>, not where the filaments are.",
 "affiché parce que c’est instructif, étiqueté parce que ce serait faux autrement":
   "displayed because it is instructive, labelled because it would be false otherwise",
 "<b>Traversée du plus grand vide</b> du catalogue Stopyra : le n°":
   "<b>Fly-through of the largest void</b> in the Stopyra catalogue: number ",
 ", rayon <b>": ", radius <b>",
 " Mpc</b>, centre à ": " Mpc</b>, centre at ",
 " Mpc. La caméra s’aligne dessus et le traverse.":
   " Mpc. The camera aligns with it and passes through.",
 "rayon et indice calculés, pas choisis à l’œil":
   "radius and index computed, not picked by eye",
 # --- visite guidee
 "<b>Visite 1/4 — le masque.</b> Le cône rouge marque |b| = 5° et 10°. Compte les points dedans : il n'y en a pas.":
   "<b>Tour 1/4 — the mask.</b> The red cone marks |b| = 5° and 10°. Count the points inside it: there are none.",
 " SNe à |b|&lt;5° pour ": " SNe at |b|&lt;5° where ",
 " attendues": " are expected",
 "<b>Visite 2/4 — le pinceau.</b> Le faisceau balaye SDSS Stripe 82 : un quart de l'échantillon dans 2,5° de large.":
   "<b>Tour 2/4 — the beam.</b> The sweep runs along SDSS Stripe 82: a quarter of the sample inside a 2.5°-wide band.",
 " SNe sur ": " SNe over ",
 " % du ciel = ×": " % of the sky = ×",
 "<b>Visite 3/4 — le nul.</b> En filigrane, 1580 directions tirées uniformément, graine fixe.":
   "<b>Tour 3/4 — the null.</b> Faintly overlaid, 1580 directions drawn uniformly, fixed seed.",
 "graine ": "seed ",
 "<b>Visite 4/4 — la profondeur.</b> Le curseur remonte le temps ; les lointains sont dans les pinceaux.":
   "<b>Tour 4/4 — depth.</b> The slider walks back in time; the distant ones live inside the beams.",
 " SNe à z ≤ 0,1 · z max ": " SNe at z ≤ 0.1 · z max ",
 # --- etiquettes dans le canevas
 "orbite terrestre · ": "Earth's orbit · ",
 "vous êtes ici · 8,2 kpc · Bulle Locale 50–150 pc":
   "you are here · 8.2 kpc · Local Bubble 50–150 pc",
 "Sgr A* · centre galactique": "Sgr A* · galactic centre",
 "front lumineux : ": "light front: ",
 "Mollweide · galactique · ● Sgr A*": "Mollweide · galactic · ● Sgr A*",
 "supernova<br>z = ": "supernova<br>z = ",
 "<b>dans SDSS Stripe 82</b><br>": "<b>in SDSS Stripe 82</b><br>",
 "vide sur la ligne de visée": "void on the line of sight",
 "pas de vide sur la visée": "no void on the line of sight",
 " Mpc comobiles": " comoving Mpc",
 # --- unites de temps
 " heures-lumière": " light-hours", " jours-lumière": " light-days",
 " années-lumière": " light-years", " milliers d’années": " thousand years",
 " millions d’années": " million years", " milliards d’années": " billion years",
}
