# LISEZMOI — MANIFEST DU CORPUS
**É. Lantenois & Claude — dernière mise à jour : 19 août 2026. 36 fichiers.**

## Par où commencer
1. `SYNTHESE_ET_OUVERTURES.md` — résumés des 5 études, conclusion en 3 niveaux, 6 versions alternatives.
2. `planche_corpus.png` et `planche_diagramme_unifie.png` — tout le corpus en deux images.
3. `carnet.md` — les images fondatrices, les errata, les règles de méthode, les intuitions.

---

## I. COSMOLOGIE — papiers A et B
- `papierA_fluide_source_externe.pdf` / `.tex` — **17 p., RÉVISÉ le 19/08** : ajout au résumé de la sensibilité de calibration SNe (±0,04 mag ⇒ ~30 unités de χ² contre 4,4 de signal) et d'une section « décomposition par lot + jackknife BAO ». La forme est robuste (β = 2,2-2,7) ; l'évidence basse-z est conditionnelle.
- `papierB_hierarchie.pdf` / `.tex` — 8 p. Hérédité spectrale, démographie (R ~ 10^7,6), borne GSL β < 4,35, grand livre de Penrose.
- `etude_complete_v2.md` (v4.9) et `etude_complete.txt` — le document maître, tous les audits.
- `revue_litterature_annexeA.md` — état de l'art et positionnement.
- `email_experts_brouillon.md` — brouillon pour Popławski (papier B en pièce jointe).
- `w_z_fit.png` — la courbe w(z) ajustée.
- Scripts : `fit_accretion_de.py`, `vraisemblance_reelle.py`, `cmb_evidence.py`, `planck_theta.py`, `cobaya_accretion.yaml`.

## II. FENÊTRE DE VIABILITÉ (étude sœur)
- `ETUDE_FENETRE_VIABILITE_v0.md` — document maître : protocole M1-M4, 11 membres décomptés, morts-par-taux, campagne de privations, diagramme (x, γ), stratification par qualité de source.
- `fenetre_viabilite_v1.pdf` / `.tex` — **le papier courant** (5 p., figure incluse).
- `fenetre_viabilite.pdf` / `.tex` — v0, conservée pour historique, **remplacée par la v1**.
- `fenetre_diagramme.png` — le diagramme de viabilité (x, γ).

## III. TAXONOMIE DES COSMOLOGIES
- `ETUDE_TAXONOMIE_COSMO_v0.md` — document maître (dictionnaire figé, M1-M3, adimensionnement D et R).
- `taxonomie_cosmo_v1.pdf` / `.tex` — le papier (3 p.).

## IV. ÉTUDE ADVERSARIALE (l'espace des rivaux)
- `PLAN_ETUDE_RIVAUX.md` — protocole complet, pilote SN+BAO, manche Planck, jackknife BAO.
- `jackknife_planck.py` — **le script à lancer** : jackknife des 13 BAO sur Planck complet, reprenable (voir V).

## V. TRANSVERSE
- `SYNTHESE_ET_OUVERTURES.md`, `planche_corpus.png`, `planche_diagramme_unifie.png`, `carnet.md`,
  `ATLAS_falsification_spec.md` (spécification de l'atlas public), `poster_*.png` (PÉRIMÉ, ne pas diffuser).

---

## CE QUI RESTE À FAIRE (par ordre de rendement)
0. ~~Réviser le papier A~~ **FAIT le 19/08** (caveat calibration au résumé + section décomposition).
1. **Lancer `jackknife_planck.py all 40`** (une nuit) — le seul test décisif encore à notre portée : le Δχ² = −12,60 tient-il au retrait de chaque BAO ? Critères pré-enregistrés dans l'en-tête du script.
2. **Envoyer le papier B à Popławski** (brouillon prêt) — un papier, un destinataire.
3. **Déposer le corpus sur GitHub** — condition de toute relecture externe.
4. MCMC Cobaya (β à ±0,05) ; F_AP exact depuis 2607.27410.
5. Fenêtre : τ_c cellulaire nu par inhibition protéasomale (répare la ligne fondatrice) ; veille sur le seuil d'autose ; bords M4 de classes neuves.
6. Rivaux : achever les 6 rivaux à convergence pleine + un étalon à largeur libre.
7. DR3 (2027) — le juge.

## RÈGLES DE MÉTHODE (le vrai héritage, détail dans `carnet.md`)
Conditions de mort pré-enregistrées · comparateurs flatteurs étiquetés · vérifier l'EFFET jamais l'opération · linter de valeurs périmées · privations totales/exogènes/sans lésion · stratifier au lieu de supprimer · l'objection la plus dangereuse d'abord.
