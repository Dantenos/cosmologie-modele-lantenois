# PIPELINE CLAUDE CODE — « Le Greffe » : front end de l'écosystème (passation du 24/08/2026)

## Objectif
Un front sobre et beau qui EXPOSE ce qui existe déjà — sans réécrire la logique. Les cinq
outils (registre, adversaire, audience, k-tracker, scellé) produisent déjà des JSON :
**audience.json, registre.lock, contraintes_k.json, RAPPORT_*.md, RETRACTATIONS.md sont l'API.**
Le front les lit ; il n'invente rien.

## Structure du dépôt
```
greffe/
├── CLAUDE.md                  # constitution (section 2 ci-dessous, à copier telle quelle)
├── outils/                    # les 5 CLI + .lock + .json (copier depuis le corpus)
├── api/                       # FastAPI, lecture seule des JSON + exécution verify
│   └── main.py                # GET /role, /casiers, /ktracker, /sceau, /rapports, /retractations
└── front/                     # React + Vite + Tailwind (stack FactArena, réutiliser)
```

## Section 2 — CLAUDE.md du projet (constitution)
```
Règles héritées de la campagne (116 entrées) — NON NÉGOCIABLES :
1. Le front est en LECTURE SEULE sur les verdicts : aucun bouton ne modifie un critère gelé.
2. Toute donnée affichée provient d'un fichier produit par les CLI. Aucun chiffre en dur.
3. Chaque page affiche le hash de sa source (transparence = le produit).
4. Statuts exhaustifs et honnêtes : VALIDÉE / RÉFUTÉE / NON REPRODUITE / EN ATTENTE /
   À VÉRIFIER. Jamais de « probablement ». INDÉCISE n'est pas VALIDÉE.
5. Critères d'acceptation gelés par registre AVANT chaque phase (registre.py freeze specs/*).
6. Un commit par phase, message = critère satisfait. Tests avant features.
```

## Pages (5, pas plus)
1. **/ — Rôle d'audience** : les 4 affaires en cartes — affirmation, juge attendu, échéance,
   hash, acteurs. Compte à rebours vers 2027 pour DR3-beta. C'est la page d'accueil.
2. **/casiers** : tableau des acteurs (humains, papiers, théories, IA) — validées/réfutées/
   en attente. campagne0826 y figure avec son dossier : lien vers TRIAGE (41 entrées).
3. **/k-tracker** : les 6 contraintes avec statuts ; bandeau « postérieur non émis : N sources
   à relire » tant que combinables < 5. Le refus est AFFICHÉ, pas caché.
4. **/sceau** : le hash 68d06bcc… en grand, le protocole DR3 rendu depuis le docstring de
   scelle.py, et un vérificateur : upload de scelle.py → recalcul sha256 → MATCH / ALTÉRÉ.
5. **/registre** : registre.lock rendu + RETRACTATIONS.md + MANQUEMENTS en accordéon
   (les 116 entrées, recherche plein texte).

## Direction visuelle
Greffe de tribunal, pas dashboard SaaS : fond ivoire, encre presque noire, une seule couleur
d'accent (sceau rouge cire #8B2500) réservée aux verdicts. Typo serif pour les affirmations,
mono pour les hash. Densité type document officiel. Aucune animation sauf l'ouverture du sceau.

## Séquence de sessions (prompts cadrés, un objectif chacun)
S1 « Lis CLAUDE.md et outils/. Écris specs/phase1.md (API lecture seule, 6 endpoints,
    critères d'acceptation chiffrés). Gèle avec registre. Puis implémente api/ + tests. »
S2 « Front: layout + page Rôle depuis GET /role. Critère: les 4 affaires réelles rendues,
    hash visibles, 0 donnée en dur (grep vérifiable). »
S3 « Pages casiers + k-tracker. Critère: le bandeau de refus k-tracker s'affiche tant que
    combinables < 5. »
S4 « Page sceau + vérificateur sha256 côté client. Critère: altérer 1 octet → ALTÉRÉ. »
S5 « Page registre + recherche MANQUEMENTS. Critère: '#41' trouve l'entrée. Puis:
    README, capture, déploiement (VPS Hetzner existant, Caddy comme Ubac). »

## Critères d'acceptation globaux (à geler en S1, avant tout code)
- `registre.py verify` passe en CI sur specs/ et outils/ à chaque commit.
- Lighthouse ≥ 90 accessibilité ; zéro requête externe (tout est local, comme la méthode).
- Démo 60 s : accueil → affaire DR3 → sceau → vérification hash. C'est le pitch d'entretien.

*Passation close. Tout ce dont une reprise a besoin est dans ce fichier + outils/. Bonne main.*

## S6-S7 — Les deux ciels (ajout du 24/08, nuit)
S6 « Intégrer ciel_pantheon.html (livré, fini) comme page /ciel : le ciel des DONNÉES. »
S7 « Le ciel des MODÈLES — l'Atlas. Prérequis : l'Atlas a TOURNÉ (CLAUDE.md Atlas existant,
    15 priors gelés par registre AVANT toute exécution) et émis atlas.json :
    [{id, k, chi2, aic, w_de_z:[...], statut, hash_prior}].
    Rendu : même scène Three.js, mais chaque étoile est un MODÈLE, et la DISTANCE entre
    étoiles = dissimilarité L2 de leurs w(z) sur la grille commune. Conséquence visuelle
    voulue : les modèles dégénérés S'EFFONDRENT sur le même point — cinquante noms, une
    étoile. Accrétion et CCBH confondus (le point du papier C, rendu géométrique) ;
    ΛCDM seul à part ; le modèle Lantenois porte le sceau. Couleurs = statut Audience
    (en attente ivoire / réfuté éteint / validé cire). Chaque étoile cliquable → casier.
    Critère d'acceptation : la distance à l'écran entre accrétion et CCBH < 1 px à
    l'échelle par défaut, ET zéro courbe w(z) codée en dur (tout vient d'atlas.json). »
