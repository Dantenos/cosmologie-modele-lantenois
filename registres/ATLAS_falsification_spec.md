# Atlas de falsification uniforme — cahier des charges v0

## Principe
Un dépôt public où N modèles d'énergie noire passent le MÊME pipeline : mêmes vraisemblances,
mêmes priors-policy, mêmes métriques, même batterie adversariale. Re-exécuté à chaque data release.
Sortie : un tableau vivant (site statique) où chaque modèle a ses chiffres, ses tests de robustesse
et sa condition de mort. Ce qui existe déjà (papiers de comparaison, DESI extended-DE ~10 modèles)
est ponctuel et hétérogène ; la valeur de l'atlas = uniformité + ré-exécution + audits + ouverture.

## Architecture
```
atlas/
  engine/
    likelihoods.py      # BAO DR2 (+corr), theta*, Pantheon+/DES-SN5YR/Union3 — DEJA ECRIT (vraisemblance_reelle.py generalise)
    metrics.py          # chi2, AIC, BIC, lnZ (integration directe sur priors), DIC (chaine emcee)
    audits.py           # decomposition par sonde, leave-one-out traceurs, split bas-z/haut-z (running),
                        # hors-echantillon (fit z<0.8 -> predire Lya), stabilite inter-compilations SN
    runner.py           # boucle modeles x datasets -> results/*.json
  models/               # UN FICHIER = UN MODELE (plugin)
    _template.py        # expose: name, params (noms, priors, n), E(z, **params), notes/condition de mort
    lcdm.py  cpl.py  wcdm.py  acc.py  acc52.py (0 param DE)  jps.py  ilcdm_eps.py  ...
  data/
    dr2/  (snapshot tagge, checksums)   # une release = un dossier fige, jamais modifie
  results/
    dr2/leaderboard.json
  site/                 # generation statique du tableau (le README suffit en v0)
  canonical_values.json # LA verite courante (une valeur = une entree datee) + valeurs depreciees
  tools/
    stale_linter.py     # linter de valeurs perimees (voir regle 7)
  .github/workflows/ci.yml   # re-run complet sur PR et sur nouveau tag de data release + stale_linter
  Dockerfile
```

## Règles du jeu (le vrai différenciateur — à figer AVANT de coder)
1. **Priors-policy unique** : bornes larges declarees dans _template, identiques en esprit pour tous ;
   toute exception justifiee dans le fichier du modele.
2. **Metriques pre-enregistrees** : chi2 min, AIC, BIC, lnZ, DIC — figees en v0, jamais ajoutees apres coup.
3. **Batterie adversariale obligatoire** (celle developpee dans l'etude) : decomposition, LOO BAO,
   trilogie SN, split-z (running des params), hors-echantillon Lya. Un modele sans audit n'entre pas.
4. **Condition de mort declaree** : chaque fichier modele contient la phrase "ce modele est falsifie si ...".
5. **Ajout par PR** avec template fixe ; le CI fait tourner tout l'atlas ; pas de resultat manuel.
6. **Versionnage des donnees** : les chiffres ne changent qu'a l'arrivee d'un tag de release (DR2 -> DR2+LyaAP -> DR3).
7. **Linter de valeurs perimees (obligatoire, bloque le merge)** : tout document du depot qui grandit par
   accretion finit par citer des chiffres morts — c'est le mode de defaillance n°1 constate sur l'etude
   d'origine (3 errata sur 8). Parade : `canonical_values.json` contient chaque quantite publiee sous la
   forme {nom, valeur_courante, valeurs_depreciees[], date} ; `tools/stale_linter.py` greppe chaque .md/.tex
   du depot contre les valeurs depreciees a chaque commit et echoue si une occurrence n'est pas marquee
   `[historique]` sur sa ligne. Le leaderboard est genere DEPUIS le json (jamais ecrit a la main) : une
   valeur ne peut donc etre mise a jour qu'a un seul endroit. Esquisse (~30 lignes) :
   ```python
   import json, re, sys, pathlib
   cv = json.load(open('canonical_values.json'))
   fautes = []
   for f in pathlib.Path('.').rglob('*.[mt][de]*'):   # .md, .tex
       for i, ligne in enumerate(f.read_text(errors='ignore').splitlines(), 1):
           if '[historique]' in ligne: continue
           for q in cv['quantites']:
               for v in q['valeurs_depreciees']:
                   if re.search(re.escape(v), ligne):
                       fautes.append(f'{f}:{i} : "{v}" perime (courant : {q["valeur_courante"]})')
   if fautes: print('\n'.join(fautes)); sys.exit(1)
   ```

## Liste v0 (15 modeles, tous a fond leger — pas de CAMB en v0)
LCDM · wCDM · CPL(w0,wa) · logarithmic w(a) · ACC beta libre · ACC 5/2 (0 param) ·
JPS/unimodulaire (accumulation) · iLCDM Q=epsHrho_dm · iLCDM Q=epsHrho_de · PEDE (emergent, 0 param) ·
holographique (c) · Bondi sature · quintessence thawing (param 1D) · GCG (gaz de Chaplygin) · Rh=ct.
(v1 : couche CAMB/planck-lite pour le sous-ensemble survivant, + profil neutrinos.)

## Ce qui est déjà écrit (a extraire des scripts de l'étude)
- likelihoods : vraisemblance_reelle.py (BAO+SN+theta*, offsets marginalises, covariances completes)
- lnZ : cmb_evidence.py (integration directe)
- DIC/chaines : bloc emcee de la session MCMC
- audits : les blocs decomposition / LOO / split-z / hors-echantillon / trilogie SN, tous ecrits
- modeles deja codes : lcdm, cpl, acc, jps, ilcdm, bondi — 6/15

## Effort estime
v0 fonctionnel (moteur + 15 modeles + CI + leaderboard markdown) : 3-5 jours a temps plein.
C'est un projet portfolio backend/data complet : plugins, CI/CD, Docker, donnees versionnees,
site genere — et un objet scientifique citable (DOI via Zenodo au premier tag).

## Premier jalon concret
1. repo `atlas-falsification` ; 2. extraire likelihoods.py depuis vraisemblance_reelle.py ;
3. _template.py + lcdm.py + cpl.py + acc.py ; 4. runner -> leaderboard.json -> tableau README ;
5. CI GitHub Actions ; 6. ajouter les 12 autres modeles un par un, avec leur condition de mort.
