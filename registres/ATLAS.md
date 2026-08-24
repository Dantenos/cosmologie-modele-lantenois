> ⚠ **RÉTRACTATION (#166, 24/08/2026)** — les deux lignes **iΛCDM** de ce tableau sont INVALIDES.
> Leur χ² a été étalonné (r_d, z_*, r_*, R) avec l'étiquette Ω_m au lieu de la densité de matière
> d'avant recombinaison Ω_m′ : 8,62 des 9,84 unités d'avance sont fabriquées. Valeur cohérente
> pour 'de' : **1423,874, gain +1,21** — derrière l'accrétion et CPL. Ce fichier est régénéré
> par `atlas_v1.py`, GELÉ avec les ancres fausses : **ne pas le rejouer** pour ces deux lignes
> tant que l'atlas v2 n'existe pas. Voir MANQUEMENTS #164-#166.

# ATLAS — 19 modèles, un pipeline, un classement (généré par `scripts/atlas_v1.py`, ne pas éditer)

*2026-08-23 — données : Pantheon+ 1580 + DESI DR2 BAO 13 + distance-priors Planck + SH0ES (pipeline v3, ZCUT off) ; N = 1597. Classement par AIC, écrit tel quel ;*
*aucun modèle n'est retiré parce qu'il nous dépasse. ΔAIC < 2 : indiscernable ; 2-7 : préférence faible ; > 10 : forte.*

| # | modèle | k | χ² | AIC | ΔAIC | BIC | paramètres | condition de mort |
|---|---|---|---|---|---|---|---|---|
| 1 | **iLCDM Q=eps H rho_de** | 4 | 1415.24 | 1423.24 | +0.00 | 1444.75 | eps=+0.0213 | mort si eps incompatible avec 0 sans gain d'AIC |
| 2 | **iLCDM Q=eps H rho_dm** | 4 | 1415.82 | 1423.82 | +0.57 | 1445.32 | eps=+0.0071 | mort si eps incompatible avec 0 sans gain d'AIC |
| 3 | **CCBH (Croker et al.)** | 3 | 1420.31 | 1426.31 | +3.06 | 1442.44 | H0=69.61 (derive) Xi=1.382 | mort si s != 0,70 (FRB : deja 2,2 sigma contre, #148) ou k != 3 (JWST 2025 : 11 sigma contre) |
| 4 | **ACCRETION (Gamma∝1/t)** | 4 | 1419.31 | 1427.31 | +4.06 | 1448.81 | H0=68.85 beta=2.595 | mort si beta(DR3) exclut [2,42;2,60] a 3 sigma, ou dAIC > +6 vs LCDM (scelle) |
| 5 | **ACCRETION 5/2 (0 param.)** | 3 | 1421.53 | 1427.53 | +4.28 | 1443.65 | beta=2.5 (fixe) | mort si beta = 5/2 exclu a 3 sigma par le profil (le point distingue est le modele) |
| 6 | **w log(a) (Efstathiou)** | 5 | 1418.08 | 1428.08 | +4.83 | 1454.96 | w0=-0.930 wl=0.323 | mort si la reconstruction sort de la famille log |
| 7 | **PC1 (creation, w_E libre)** | 6 | 1416.70 | 1428.70 | +5.46 | 1460.96 | H0=68.95 b=0.851 | mort si w_E = 0 exige (PC3 deja a 2,7 sigma) ou si k = 6 jamais paye par les donnees |
| 8 | **CPL = IDE degeneree** | 5 | 1418.93 | 1428.93 | +5.68 | 1455.81 | H0=68.95 w0=-0.921 wa=-0.441 | mort si la reconstruction sort de la famille lineaire en (1-a) |
| 9 | **Anton-Schmidt** | 5 | 1419.52 | 1429.52 | +6.27 | 1456.39 | H0=68.96 n=0.346 L0=1.612 | forme publiee (secteur sombre seul, declare) ; mort si (n, L0) fuient au bord |
| 10 | **LCDM** | 3 | 1425.09 | 1431.09 | +7.84 | 1447.21 | H0=68.66 Om=0.2976 | reference ; mort si une alternative atteint dAIC > 10 et survit aux audits |
| 11 | **Lombriser (Om_de predit)** | 2 | 1427.61 | 1431.61 | +8.36 | 1442.36 | H0=68.24 Om=0.3030 (impose) | mort si Omega_de mesure exclut 0,697 (la prediction est le modele) |
| 12 | **wCDM** | 4 | 1423.84 | 1431.84 | +8.60 | 1453.35 | w=-1.024 | mort si un croisement de w = -1 est etabli (w constant ne croise pas) |
| 13 | **Quintessence thawing (Linder)** | 4 | 1425.11 | 1433.11 | +9.86 | 1454.61 | w0=-0.999 | mort si w0 < -1 exige : la famille interdit le fantome, donc le croisement la tue |
| 14 | **JPS / unimodulaire (accum.)** | 4 | 1426.12 | 1434.12 | +10.87 | 1455.62 | eps=-0.0000 | comptabilite effective declaree ; mort si eps = 0 prefere (le papier A l'a deja rejetee a dchi2 = +4,9) |
| 15 | **Chaplygin generalise (GCG)** | 5 | 1433.18 | 1443.18 | +19.93 | 1470.06 | As=0.999 alpha=0.193 | secteur sombre seul (declare) ; mort si alpha -> 0 sans gain (degenere a LCDM) |
| 16 | **PEDE (emergente, 0 param.)** | 3 | 1460.91 | 1466.91 | +43.66 | 1483.03 | aucun (forme rigide) | zero echappatoire : mort si dAIC > 10 vs le meilleur (forme figee par construction) |
| 17 | **Holographique (horizon futur)** | 4 | 1476.52 | 1484.52 | +61.28 | 1506.03 | c=0.672 | mort si c >= 1 exige sans acceleration suffisante, ou dAIC > 10 (approx. radiation declaree) |
| 18 | **Bondi sature (M'∝M²)** | 4 | 4023.07 | 4031.07 | +2607.82 | 4052.57 | x_s=t0/t_s=0.925 | mort si x_s -> 1 (saturation avant aujourd'hui) ou si la forme perd sur ACC libre a k egal |
| 19 | **Rh = ct** | 2 | 7621960.09 | 7621964.09 | +7620540.85 | 7621974.84 | H0=85.00 (Om fixe 0,30, r_d seul — incoherence declaree) | mort par theta* et BAO : E = 1+z n'a ni ere de matiere ni acceleration — ecrit tel quel |

Approximations déclarées : voir le docstring de `scripts/atlas_v1.py` (gelé). Validation : les 7
entrées d'`atlas_rivaux.py` reproduites à ±0,5 en χ² avant toute publication des 12 nouveaux.
