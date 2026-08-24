# ATLAS v2 — le palmares corrige

> Genere par `scripts/atlas_v2.py` (gele). **Ce fichier remplace le palmares de l'atlas v1 (#150)**, qui portait deux lignes retractees.

> **Retractations appliquees :** #166 (iLCDM Q∼ρ_de : l'avance de +9,84 etait a 8,62 un artefact d'etalonnage — chi2 corrige 1423,874) · #167 (iLCDM Q∼ρ_dm : s'effondre exactement sur LCDM, gain 0,000).

> **Annotations :** #175 (minima de bord) · #177 (six lois a un parametre de la litterature 2025-2026, meme pipeline, memes donnees).


**Notre loi (accretion) est 4e a l'AIC. La devancent : K4 (Kessler et al. 2025, Eq. 8), CCBH (Croker et al.), K3 (Kessler et al. 2025, Eq. 7).**


| rang | modele | k | chi2 | AIC | provenance / note |
|---|---|---|---|---|---|
| 1 | K4 (Kessler et al. 2025, Eq. 8) | 4 | 1415.398 | 1423.398 | banc a un parametre (w0 = -0,9916) |
| 2 | CCBH (Croker et al.) | 3 | 1420.309 | 1426.309 | #150 |
| 3 | K3 (Kessler et al. 2025, Eq. 7) | 4 | 1418.426 | 1426.426 | banc a un parametre (w0 = -0,9081) |
| 4 | **ACCRETION (Gamma∝1/t)** | 4 | 1419.309 | 1427.309 | #150 |
| 5 | SR w0/sqrt(a) (Borghetto et al. 2026) | 4 | 1419.361 | 1427.361 | banc a un parametre (w0 = -0,8844) |
| 6 | ACCRETION 5/2 (0 param.) | 3 | 1421.527 | 1427.527 | #150 |
| 7 | w log(a) (Efstathiou) | 5 | 1418.079 | 1428.079 | #150 |
| 8 | PC1 (creation, w_E libre) | 6 | 1416.701 | 1428.701 | #150 |
| 9 | CPL = IDE degeneree | 5 | 1418.927 | 1428.927 | #150 |
| 10 | Anton-Schmidt | 5 | 1419.515 | 1429.515 | #150 |
| 11 | K1 (Kessler et al. 2025, Eq. 5) | 4 | 1421.742 | 1429.742 | banc a un parametre (w0 = -0,8362) |
| 12 | LCDM | 3 | 1425.086 | 1431.086 | #150 |
| 13 | Lombriser (Om_de predit) | 2 | 1427.607 | 1431.607 | #150 |
| 14 | wCDM | 4 | 1423.843 | 1431.843 | #150 |
| 15 | iLCDM Q=eps H rho_de | 4 | 1423.874 | 1431.874 | RETRACTE-CORRIGE (#166, degenerescence_ilcdm_v4.py) |
| 16 | iLCDM Q=eps H rho_dm | 4 | 1425.086 | 1433.086 | RETRACTE-CORRIGE (#167, etalonnage_dm.py) · MINIMUM DE BORD (#175) |
| 17 | Quintessence thawing (Linder) | 4 | 1425.107 | 1433.107 | MINIMUM DE BORD (#175) |
| 18 | F83 w0 exp(1-a) (Borghetto et al. 2026) | 4 | 1425.199 | 1433.199 | banc a un parametre (w0 = -0,8078) |
| 19 | JPS / unimodulaire (accum.) | 4 | 1426.117 | 1434.117 | MINIMUM DE BORD (#175) |
| 20 | Chaplygin generalise (GCG) | 5 | 1433.176 | 1443.176 | #150 |
| 21 | K2 (Kessler et al. 2025, Eq. 6) | 4 | 1438.116 | 1446.116 | banc a un parametre (w0 = -0,7438) |
| 22 | PEDE (emergente, 0 param.) | 3 | 1460.906 | 1466.906 | #150 |
| 23 | Holographique (horizon futur) | 4 | 1476.522 | 1484.522 | #150 |
| 24 | Bondi sature (M'∝M²) | 4 | 4023.068 | 4031.068 | #150 |
| 25 | Rh = ct | 2 | 7621960.093 | 7621964.093 | #150 |

**Lecture.** Une ligne marquee MINIMUM DE BORD affiche un chi2 qui **ne se lit pas comme un minimum** : une partie de son domaine est inaccessible (le fond y est rejete) ou son optimum tombe sur la borne du prior. Trois familles sont dans ce cas (#175).

**Ce que ce palmares ne dit pas.** Il classe des ajustements sur une seule vraisemblance (BAO DR2 + theta_* + Pantheon+, N = 1597). Il ne dit rien des perturbations, rien de la physique, et rien de la robustesse aux systematiques de calibration des supernovae — dont #170 montre qu'elles deplacent nos gains de 10 a 17 % a elles seules.

