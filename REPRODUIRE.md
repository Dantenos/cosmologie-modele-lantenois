# REPRODUIRE — chaque chiffre de tête, sa commande, son temps

Prérequis : Python ≥ 3.10, `pip install -r requirements.txt`, puis `sh donnees/TELECHARGER.sh`
(données publiques, empreintes SHA-256 vérifiées ; ~35 Mo). Sous Windows : `$env:PYTHONUTF8 = "1"`.
Les scripts de calcul se lancent **depuis `donnees/pantheon_plus/`** (ils lisent `pantheon.dat`
dans le répertoire courant) ; les outils se lancent depuis la racine.

| chiffre publié | commande (racine sauf mention) | attendu | durée* |
|---|---|---|---|
| intégrité des critères gelés | `python outils/registre.py verify` | tous OK, exit 0 (compte courant : `registres/ETAT.md`) | 1 s |
| sceau DR3 | `sha256sum outils/scelle.py` | `68d06bcc…45a2` | 1 s |
| β = 2,447, Δχ² = −4,41 (fond léger) | `python outils/ligne_de_base.py` | `REPRODUIT` | 10 s |
| 16 ancres numériques (14 scripts) | `python outils/rejouer.py` | 0 échec | 35 s |
| valeurs périmées | `python outils/perime.py` | 0 occurrence | 1 s |
| Δχ² = −12,60, β = 2,589 (Planck complet) | dans `donnees/pantheon_plus/` : `python ../../scripts/planck_theta.py lcdm 600` puis `acc 600` (reprenable) | χ² 1998,63 / 1986,03 | ~40 min |
| β marginalisé = 2,603 +0,046/−0,053 | idem : `python ../../scripts/mcmc_planck_beta.py 400` (reprenable) | validation puis quantiles | ~4 h |
| E1 vides (UNIVERSEL, 2 juges) | `python scripts/etude_E1_vides.py` puis `scripts/etude_E1_manche2.py` | Δβ = +0,10 ± 0,24 ; 3× NUL | 3 + 5 min |
| E3 FRB réels (+4,71, ~2,2σ) | `python scripts/etude_E3_frb_reelles_v1.py` | validation PASSE, Δχ² +4,71 | 10 s |
| bootstrap E3 (médiane +4,67) | dans `donnees/pantheon_plus/` : `python ../../scripts/etude_E3_bootstrap.py 200` | [16;84] = [+1,9 ; +8,5] | ~40 min |
| audit iΛCDM (3 volets : variantes, LOO/split, trilogie) | idem : `python ../../scripts/audit_ilcdm.py` puis `_v2.py`, `_v3.py` | gains +9,5 à +11,3 partout | 25 s + 2 min + 20 s |
| le Grand Livre (CCBH doit +14,2) | `python outils/ledger.py` | R1 +4,71 ; R2 +9,48 | 15 s |
| manches vides 1-2-3 (duel 2-0) | `python scripts/etude_E1_manche3.py` (DESIVAST) | NON EXPLOITÉ (plancher) ; T6 | 3,5 min |
| histoire Ω et attracteur w* = −0,70 | `python outils/fig_omega.py` | validation E_acc + z× puis PNG | 30 s |
| l'atlas (19 modèles) | dans `donnees/pantheon_plus/` : `python ../../scripts/atlas_v1.py` | tête iΛCDM, accrétion +4,06 | ~2 min |
| duel CCBH (Ξ = 1,382 calibré) | idem : `python ../../scripts/atlas_rivaux.py` | tableau des 7 | ~90 s |
| visuels (ciel, ciel des modèles) | `python outils/genere_ciel.py` ; `python outils/genere_atlas.py` | refus si les comptes divergent | 1 min |
| l'état du dépôt, généré | `python outils/etat.py` | `registres/ETAT.md` | 2 s |

\* machine de référence : portable Windows 2026, Python 3.12. Les longues chaînes (`planck_theta`,
`mcmc_planck_beta`, `jackknife_planck`) sauvent leur état et reprennent où elles en étaient.

Un chiffre ne se reproduit pas ? C'est soit une dérive d'environnement (versions dans
`requirements.txt`), soit une vraie erreur : dans les deux cas, ouvrez une entrée — le format
est dans `registres/MANQUEMENTS.md`, et `registres/POUR_2027.md` dit comment juger sans nous.
