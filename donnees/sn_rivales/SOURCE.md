# Jeux de donnees SN rivales — DES-SN5YR et Union3

Telecharges le 2026-08-24 (curl, GitHub raw). Aucune cosmologie calculee ;
uniquement telechargement, conversion et verification (script : `scripts/build_csv.py`).

---

## 1. DES-SN5YR (Dark Energy Survey 5-Year SN)

- **Papier cle** : DES Collaboration, "The Dark Energy Survey: Cosmology Results With ~1500 New
  High-redshift Type Ia Supernovae Using The Full 5-year Dataset", arXiv:2401.02929.
  Hubble diagram et covariances construits dans Vincenzi et al. 2024 (arXiv:2401.02945).
- **Depot** : https://github.com/des-science/DES-SN5YR — **tag `1.3` "Vincenzi et al. 2024 Legacy Release"**.
  ATTENTION : la branche `main` du depot a ete remplacee par la re-calibration "Dovekie" (2025,
  fichiers `DES-Dovekie_*`, matrices **inverses** en .npz). Pour reproduire arXiv:2401.02929 il faut
  le tag 1.3, utilise ici.

### Fichiers bruts (`DES-SN5YR/raw/`)

| Fichier | URL exacte | sha256 |
|---|---|---|
| DES-SN5YR_HD.csv | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/4_DISTANCES_COVMAT/DES-SN5YR_HD.csv | 95ab1e9f5460a056de37d2b4e28df73ce0c7fd471baba9fb37f1667f41b7901c |
| DES-SN5YR_HD+MetaData.csv | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/4_DISTANCES_COVMAT/DES-SN5YR_HD+MetaData.csv | 80e081d13145a7ee66730b59826ed83e6414087fd1e26a5a206a196f650f02c5 |
| STAT+SYS.txt.gz | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/4_DISTANCES_COVMAT/STAT+SYS.txt.gz | 20bc94a881893235a94fc5a1b1c995f4b35bfae333996c2a0ce2696cb05381f2 |
| STATONLY.txt.gz | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/4_DISTANCES_COVMAT/STATONLY.txt.gz | 89f296a26f9bb500ccfebb173420d80deb609243e424534a31d8fe7befa05fda |
| README.md (dossier 4_DISTANCES_COVMAT, tag 1.3) | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/4_DISTANCES_COVMAT/README.md | 51608e967635573ae40fbc61d02b3f9d8b37194b21f082b85a62d906a75fc9b2 |
| DES-SN5YR_DES_HEAD.FITS.gz | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/0_DATA/DES-SN5YR_DES/DES-SN5YR_DES_HEAD.FITS.gz | 08c1fb41dfe8b4e8a969f205144f94c9f6838a1a895a0fedc75b837fb87fd00a |
| DES-SN5YR_LOWZ_HEAD.FITS.gz | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/0_DATA/DES-SN5YR_LOWZ/DES-SN5YR_LOWZ_HEAD.FITS.gz | ffac027fdab606fe5a0a34cd42abd22d749e70edf62b9e22f777315900aa3e4f |
| DES-SN5YR_Foundation_HEAD.FITS.gz | https://raw.githubusercontent.com/des-science/DES-SN5YR/1.3/0_DATA/DES-SN5YR_Foundation/DES-SN5YR_Foundation_HEAD.FITS.gz | ea94aec20cc181d8972a5974d8fd01eeb81a00ebaf4ac1e5dd6dc12569799ff1 |

### Hubble diagram : `des_sn5yr_hd.csv` (copie conforme de DES-SN5YR_HD.csv)

- **N = 1829 SNe** (1830 lignes avec en-tete). zHD : min 0.02509, max 1.12132.
- Colonnes : `CID` (identifiant), `IDSURVEY` (10=DES [1635 SNe], 5=CSP [8], 63=CFA3S [15],
  64=CFA3K [31], 65=CFA4p2 [19], 66=CFA4p3 [3], 150=Foundation [118]),
  `zCMB` (redshift corrige CMB), `zHD` (**redshift Hubble diagram, corrections CMB + vitesses
  particulieres — c'est le z a utiliser**), `zHEL` (heliocentrique),
  `MU` (**module de distance, convention H0=70 ; PAS mB** — deja standardise, bias-corrige, BEAMS),
  `MUERR_FINAL` (incertitude **statistique** par SN, renormalisee BEAMS).
- sha256 : 95ab1e9f5460a056de37d2b4e28df73ce0c7fd471baba9fb37f1667f41b7901c

### Covariance : `STAT+SYS.txt.gz` -> `des_sn5yr_covsys_1829x1829.npy`

- Format brut : texte gzip, 1re ligne = 1829 (N), puis N*N = 3 345 241 valeurs, **ligne par ligne**,
  dans **l'ordre exact des lignes de DES-SN5YR_HD.csv** (le README du tag 1.3 le confirme ; le
  fichier HD+MetaData a un ordre different et NE DOIT PAS etre utilise avec la matrice).
- C'est la **covariance systematique seule** (malgre le nom STAT+SYS) : la partie statistique est
  dans MUERR_FINAL. Verifie : STATONLY.txt.gz = matrice entierement nulle (0 valeurs non nulles).
  Covariance totale a construire : C_tot = C_sys + diag(MUERR_FINAL^2).
- C'est bien la covariance directe (PAS l'inverse — l'inverse ne concerne que les .npz Dovekie
  de la branche main).
- Verification : matrice 1829x1829, exactement symetrique (max|C-C^T| = 0),
  diagonale de 9.28e-05 a 1.46e-01 mag^2.
- `des_sn5yr_covsys_1829x1829.npy` : float64, np.load -> (1829, 1829), meme ordre que le CSV.
  sha256 : a375109c800ad9f51749d4cc843684f71d9b838e3155bf5d801305d3b257f5d4

### RA/DEC : DISPONIBLES — `des_sn5yr_radec.csv`

- Les tables du dossier 4_DISTANCES_COVMAT ne donnent PAS la position des SNe
  (seulement HOST_RA/HOST_DEC dans DES-SN5YR_HD+MetaData.csv, renseignees pour les 1635 DES
  uniquement, -999 sinon).
- Les **positions des SNe** sont dans le dossier `0_DATA` du meme depot (tag 1.3) : fichiers SNANA
  `*_HEAD.FITS.gz` (colonnes SNID, RA, DEC en degres J2000) pour DES (19706 candidats),
  LOWZ (342) et Foundation (185).
- `des_sn5yr_radec.csv` : cross-match par CID = SNID -> **1829/1829 SNe du Hubble diagram
  apparies**. Colonnes : CID, IDSURVEY, zHD, RA_SN, DEC_SN (deg), SRC_HEAD (DES/LOWZ/Foundation),
  HOST_RA, HOST_DEC. Meme ordre de lignes que des_sn5yr_hd.csv.
  sha256 : 6a47dee628177d826c81969af3e829ceeeef388a2641fe5810ae34c652c9d93d

---

## 2. Union3 (Rubin et al. 2023)

- **Papier** : Rubin et al., "Union Through UNITY: Cosmology with 2,000 SNe Using a Unified
  Bayesian Framework", arXiv:2311.12098. 2087 SNe compressees en **22 bins** de module de distance
  (nodes de spline) par le framework bayesien UNITY1.5.
- **Depot officiel** : https://github.com/rubind/union3_release (D. Rubin).

### Fichiers bruts (`Union3/raw/`)

| Fichier | URL exacte | sha256 |
|---|---|---|
| mu_mat_union3_cosmo=2_mu.fits (**nominal**, UNITY1.5 = papier 2311.12098) | https://raw.githubusercontent.com/rubind/union3_release/main/mu_mat_union3_cosmo%3D2_mu.fits | ef98b7dde1025ee7134f3242aaea3f1f0ed3f2b29a718458c550a8e4e24d0349 |
| mu_mat_union3.1_UNITY1.7_template_cosmo=2_0_mu.fits (variante Union3.1, non utilisee ici) | https://raw.githubusercontent.com/rubind/union3_release/main/mu_mat_union3.1_UNITY1.7_template_cosmo%3D2_0_mu.fits | ce1cc90f9206d98c2398e79885c612777e679cf9a5cbf041ce8d420920afbc2e |
| mu_mat_union3.1_UNITY1.8_template_cosmo=2_0_mu.fits (variante Union3.1, non utilisee ici) | https://raw.githubusercontent.com/rubind/union3_release/main/mu_mat_union3.1_UNITY1.8_template_cosmo%3D2_0_mu.fits | bfebb15f64f2c39eb33fca91a6b370cfaebbe8946fcdd58c8d1019ea302482b9 |
| README_union3_release.md | https://raw.githubusercontent.com/rubind/union3_release/main/README.md | a6e877690ca7cc406550f723b179a71ee092bf99541202d184e4a81d20729319 |

### Format du FITS nominal (documente par le README du depot)

Image FITS 23x23 (float64). **Premiere ligne (data[0,1:]) = redshifts des 22 bins ;
premiere colonne (data[1:,0]) = modules de distance mu ; le bloc data[1:,1:] (22x22) = matrice de
covariance INVERSE** (stat+sys, issue de la chaine UNITY). data[0,0] = 0 (non utilise).
Le zero-point absolu de mu est arbitraire (degenerescence M_B/H0 marginalisee) : seule la forme
compte ; a fitter avec un offset libre (convention Delta-mu de DESI).

### CSV derives (`Union3/`)

- `union3_bins.csv` : **N = 22 bins**, colonnes `bin` (1-22), `z` (redshift du node ; min 0.05000,
  max 2.26226), `mu` (module de distance ; min 36.6304, max 45.9972),
  `sigma_mu_from_cov_diag` (= sqrt(diag(inv(invcov))), de 0.089 a 0.340 — indicatif seulement,
  les bins sont correles).
  sha256 : 6384a9d6380e3fb1de89edc6cba12d7f66333a3c6c9a5453d18df77404a2650e
- `union3_inv_cov_22x22.csv` : matrice inverse telle que fournie, ordre = ordre des bins
  (z croissant, identique a union3_bins.csv), separateur virgule, 22 lignes x 22 colonnes.
  sha256 : 97702ff86d07cceaebc25e68afdcb3f9774ca872d7abf2dc17530dee7f62fe4b
- `union3_cov_22x22.csv` : covariance = inverse numerique (np.linalg.inv) de la precedente,
  symetrisee ; meme ordre.
  sha256 : 69e5b85cec31a3c4eb90b196cdc398f23c94bb8cec07eb3362017e4c96809acc
- Verifications : invcov symetrique (asymetrie max 4e-11), definie positive
  (valeurs propres de 5.12 a 7026), 22 bins.

---

## Caveats

1. DES `MU` suppose H0=70 (offset absolu arbitraire) ; Union3 mu a un zero-point arbitraire :
   dans les deux cas, marginaliser sur un offset (comme M_B pour Pantheon+).
2. DES STAT+SYS.txt.gz = covariance SYSTEMATIQUE seule ; ajouter diag(MUERR_FINAL^2) pour C_tot.
3. Ne jamais apparier la matrice DES avec HD+MetaData.csv (ordre de lignes different) ;
   seul DES-SN5YR_HD.csv est dans le bon ordre.
4. Union3 est une compression en 22 nodes de spline correles (pas des SNe individuelles) ;
   la matrice fournie est l'INVERSE de la covariance ; pas de RA/DEC (bins).
5. Overlap d'echantillons : DES-SN5YR, Union3 et Pantheon+ partagent des SNe (low-z, Foundation,
   DES3YR dans Union3) — ne pas les combiner comme jeux independants.
