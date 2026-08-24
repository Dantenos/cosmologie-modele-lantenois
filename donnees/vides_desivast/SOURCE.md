# DESIVAST DR1 BGS — Catalogues de vides (VAST : VoidFinder + V2/VIDE + V2/REVOLVER)

Téléchargé le 2026-08-24 depuis le portail public DESI (aucune authentification requise).

## Papier
- Hernan Rincon, Segev BenZvi, Kelly Douglass, Dahlia Veyrat, J. N. Aguilar, S. Ahlen, et al. (collab. DESI),
  « DESIVAST: Catalogs of Low-redshift Voids Using Data from the DESI Data Release 1 Bright Galaxy Survey »,
  arXiv:2411.00148, ApJ 982, 38 (2025), DOI 10.3847/1538-4357/adb559.
- Value-Added Catalog DESI DR1 : https://data.desi.lbl.gov/doc/releases/dr1/vac/desivast/
- Code : https://github.com/hbrincon/DESIVAST — boîte à outils VAST : https://vast.readthedocs.io/

## URLs exactes (répertoire v1.0)
Base : https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1.0/
- DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits  (3.9 Mo) — téléchargé intégralement
- DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits  (0.6 Mo) — téléchargé intégralement
- DESIVAST_BGS_VOLLIM_V2_VIDE_NGC.fits (459 Mo) / _SGC.fits (62 Mo) — seul le HDU « VOIDS » a été
  extrait (lecture HTTP par plages via astropy+fsspec) -> *_VOIDS_extract.fits
- DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits (612 Mo) / _SGC.fits (87 Mo) — idem, extraits « VOIDS »
- README.md et dr1_vac_dr1_desivast_v1.0.sha256sum (sommes officielles DESI)

Intégrité : les deux FITS VoidFinder vérifiés OK contre le fichier .sha256sum officiel DESI.
(Les gros fichiers V2 complets n'ont pas été conservés — ~1.2 Go, surtout des HDU de triangulation
des surfaces de vides ; le HDU VOIDS extrait contient toutes les propriétés par vide.)

## Algorithmes
- VoidFinder (VAST) : sphères maximales fusionnées en vides ; fichier = HDU MAXIMALS (1 sphère
  maximale par vide) + HDU HOLES (toutes les sphères).
- V2 (Vsquared, VAST) = ZOBOV/watershed avec élagage VIDE ou REVOLVER ; HDU VOIDS = 1 ligne par vide.

## Cosmologie supposée (en-têtes FITS)
- LCDM plat, OMEGAM = 0.315, h = 1.0 (distances en Mpc/h), METRIC = comoving.
- Échantillon limité en volume : BGS Bright, M_r < -20.0, 0 < z < 0.24 (D_c < 677.4 Mpc/h).

## Empreinte du relevé (mesurée sur les catalogues)
- Deux calottes : NGC et SGC (colonne « cap » dans les CSV).
- VoidFinder : NGC RA [-89.9, 270.0] deg (RA négatif = RA+360), Dec [-9.8, +70.0] ;
  SGC RA [-51.4, +73.1], Dec [-8.2, +30.0]. Distance comobile des centres : 67.3 – 671.2 Mpc/h.
- V2 (RA dans [0,360)) : RA [48.6, 336.3], Dec [-9.1, +68.7], z centres 0.0343 – 0.2364.
- Couverture ciel (en-tête NGC VoidFinder) : 2446 deg^2 NGC (+ SGC plus petit), 364 058 galaxies NGC.

## Nombre de vides
| Catalogue | N total (NGC+SGC) | dont « intérieurs » | R_eff (Mpc/h) |
|---|---|---|---|
| VoidFinder (MAXIMALS) | 3765 (3241+524) | 1489 (EDGE==0) [papier : 1461] | 9.97 – 31.69 |
| V2/VIDE (VOIDS) | 1478 (1258+220) | 111 (EDGE_AREA==0) [papier : 295 « interior »] | 10.00 – 55.88 |
| V2/REVOLVER (VOIDS) | 1992 (1692+300) | 139 (EDGE_AREA==0) [papier : 420 « interior »] | 10.00 – 43.50 |

Nota : la définition « interior » du papier ne coïncide pas exactement avec les drapeaux bruts
(EDGE==0 ; EDGE_AREA==0 est plus strict que le critère du papier) — filtrer selon vos besoins.

## CSV convertis (virgule, en-tête ; unités : deg, Mpc/h)
- DESIVAST_BGS_VOLLIM_VoidFinder_voids.csv : cap, void_id, ra, dec, dist (D_c comobile Mpc/h),
  reff (Mpc/h), reff_uncert, edge (0=intérieur, 1=bord, 2=coupé par le masque).
  PAS de redshift par vide dans ce fichier : utiliser dist (aucune conversion cosmologique effectuée).
- DESIVAST_BGS_VOLLIM_V2_VIDE_voids.csv / _V2_REVOLVER_voids.csv : cap, void_id, ra, dec, z
  (redshift du centre), reff (= RADIUS, rayon effectif Mpc/h), tot_area, edge_area ((Mpc/h)^2).

## sha256 (fichiers livrés ici)
c69f2f7b2b1fed4554527475dd96584169b1ead5bbcd0c152164200e6a2f34c8  DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits
47c43b9b446f4bcb47cbc023115ac5297f9afb0045aea96d853649a80d7219c1  DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits
66c95b4f3b65b76d7c6b0f56b5b679006c1922974849a2e31b4cdcabd5eb5b4d  DESIVAST_BGS_VOLLIM_V2_VIDE_NGC_VOIDS_extract.fits
827b5b0fe6f9eaba837533f06b04f0518e3d0495fd132e550a27c60ce2597c80  DESIVAST_BGS_VOLLIM_V2_VIDE_SGC_VOIDS_extract.fits
cbbc24b14faddba5be6e3f7faa0ca1508e1da46c331f1b11165271deed84b534  DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC_VOIDS_extract.fits
465c9aefc99a516ea1b6b76d15f879fa276cef8ea670863f06410cb17d3d0481  DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC_VOIDS_extract.fits
dd912a5af564808e42a8a20cc0d85d55baf0345c92bdaf0918b3a9b262520305  DESIVAST_BGS_VOLLIM_VoidFinder_voids.csv
b161ba78b571db1ecee3da7aa65498be5677e0a1aab77db4b0d4783e5d700369  DESIVAST_BGS_VOLLIM_V2_VIDE_voids.csv
e467bb576a63d5eef66b807b9062fddd591b56127a5b05b472a152a96380893d  DESIVAST_BGS_VOLLIM_V2_REVOLVER_voids.csv
