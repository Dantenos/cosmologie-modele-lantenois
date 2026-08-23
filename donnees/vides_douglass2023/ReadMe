J/ApJS/265/7            Void catalogs from SDSS DR7            (Douglass+, 2023)
================================================================================
Updated void catalogs of the SDSS DR7 main sample.
    Douglass K.A., Veyrat D., BenZvi S.
   <Astrophys. J. Suppl. Ser., 265, 7 (2023)>
   =2023ApJS..265....7D
================================================================================
ADC_Keywords: Intergalactic medium; Spectra, optical
Keywords: Voids ; Cosmic web ; Galaxy physics ;
          Large-scale structure of the universe ; Galaxy environments ;
          Extragalactic astronomy ; Sky surveys ; Catalogues

Abstract:
    We produce several public void catalogs using a volume-limited
    subsample of the Sloan Digital Sky Survey Data Release 7 (SDSS DR7).
    Using new implementations of three different void-finding algorithms,
    VoidFinder and two ZOBOV-based algorithms (VIDE and REVOLVER), we
    identify 1163, 531, and 518 cosmic voids with radii >10h^-1^Mpc,
    respectively, out to a redshift of z=0.114 assuming a Planck 2018
    cosmology, and 1184, 535, and 519 cosmic voids assuming a WMAP5
    cosmology. We compute effective radii and centers for all voids and
    find none with an effective radius >54h^-1^Mpc. The median void
    effective radius is 15-19h^-1^Mpc for all three algorithms. We extract
    and discuss several properties of the void populations, including
    radial density profiles, the volume fraction of the catalog contained
    within voids, and the fraction of galaxies contained within voids.
    Using 64 mock galaxy catalogs created from the Horizon Run 4 N-body
    simulation, we compare simulated and observed void properties and find
    good agreement between the SDSS DR7 and mock catalog results.

Description:
    Released in 2009, the SDSS DR7 (Abazajian et al. 2009) is a wide-field
    multiband imaging and spectroscopic survey conducted on the 2.5 m
    telescope at the Apache Point Observatory in New Mexico. Follow-up
    spectroscopy was performed on all galaxies with a Petrosian r-band
    magnitude m_r_<17.77 with two double fiber-fed spectrometers and fiber
    plug plates with a minimum fiber separation of 55". The observed
    wavelength range for the SDSS DR7 spectra is 3800-9200{AA} with a
    resolution R~1800.

    We use version 1.0.1 of the NSA (Blanton+ 2011AJ....142...31B), which
    contains 641,409 galaxies observed in SDSS DR7. See Section 2.

    We present void catalogs found with VoidFinder, V2 with VIDE pruning
    (V2/VIDE), and V2 with REVOLVER pruning (V2/REVOLVER) assuming two
    flat {Lambda}CDM cosmologies: WMAP5 ({Omega}_M_=0.258;
    Dunkley+ 2009ApJS..180..306D) and Planck 2018 ({Omega}_M_=0.315;
    Planck Collaboration+ 2020A&A...641A...6P), and assuming
    H_0_=100h.km.s^-1^Mpc^-1^. See Section 4.

File Summary:
--------------------------------------------------------------------------------
 FileName Lrecl Records Explanations
--------------------------------------------------------------------------------
ReadMe       80       . This file
table1.dat  181    2347 VoidFinder output: Maximal spheres for two cosmologies
table2.dat  105   80080 VoidFinder output: All spheres for two cosmologies
table3.dat  417    2101 V2 output: Voids for two prunings and two cosmologies
table4.dat   32    4146 V2 output: Zones for two prunings and two cosmologies
table5.dat   38  776500 V2 output: Galaxies for two prunings and two cosmologies
--------------------------------------------------------------------------------

See also:
 II/294  : The SDSS Photometric Catalog, Release 7 (Adelman-McCarthy+, 2009)
 V/154   : Sloan Digital Sky Surveys (SDSS), Release 16 (DR16) (Ahumada+, 2020)
 J/MNRAS/269/301  : Superclusters and voids (Einasto+, 1994)
 J/AJ/119/32      : Survey of galaxies within nearby voids. II (Grogin+, 2000)
 J/ApJ/744/82     : Catalog of cosmic voids from the SDSS-DR7 (Varela+, 2012)
 J/A+A/570/A106   : VIPERS. Searching for cosmic voids (Micheletti+, 2014)
 J/MNRAS/440/1248 : SDSS DR7 voids and superclusters (Nadathur+, 2014)
 J/ApJ/799/95     : Structure in 3D galaxy distribution. II. Voids (Way+, 2015)
 J/ApJ/834/186    : Metallicity of MPA-JHU SDSS-DR7 dwarf gal. (Douglass+, 2017)
 J/ApJ/835/161    : A cosmic void cat. of SDSS DR12 BOSS galaxies (Mao+, 2017)
 J/ApJ/837/42     : N/O ratio of dwarf galaxies from SDSS (Douglass+, 2017)
 J/ApJ/864/144    : N/O and Ne/O ratios of SDSS dwarf galaxies (Douglass+, 2018)
 J/ApJ/861/60     : z~2.3 cosmic voids in the COSMOS field (Krolewski+, 2018)
 J/MNRAS/482/4329 : Void galaxies in the nearby Universe (Pustilnik+, 2019)
 J/MNRAS/502/4815 : Very young galaxies in the local Universe (Trevisan+, 2021)
 http://www.sdss.org/ : SDSS home page

Byte-by-byte Description of file: table1.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label  Explanations
--------------------------------------------------------------------------------
  1-  10 A10    ---       Cosmo  Cosmology, Plank 2018 or WMAP5 (G1)
 12-  31 F20.15 h-1.Mpc   x      [-324.3/-13.9] Cartesian, x coordinate, of
                                  maximal sphere
 33-  54 F22.17 h-1.Mpc   y      [-292.1/266.6] Cartesian, y coordinate, of
                                  maximal sphere
 56-  76 F21.17 h-1.Mpc   z      [-10/294.8] Cartesian, z coordinate, of
                                  maximal sphere
 78-  95 F18.15 h-1.Mpc   Rad    [10/22.6] Radius of maximal sphere
 97- 100 I4     ---       void   [0/1183]? Unique sequential identifier for that
                                  cosmology
     102 I1     ---       edge   [0/2] Flag identifying whether any part of the
                                  void falls outside of the survey mask
104- 122 F19.15 h-1.Mpc   s      [27.37/327.5] Comoving distance of maximal
                                  sphere center
124- 141 F18.14 deg       RAdeg  [112.2/259.1] Right Ascension of maximal
                                  sphere center (J2000)
143- 162 F20.17 deg       DEdeg  [-2.1/67] Declination of maximal sphere center
                                  (J2000)
164- 181 F18.15 h-1.Mpc   Reff   [10.17/30.74] Effective radius of the void to
                                  which the maximal sphere belongs
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label  Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---     Cosmo  Cosmology, Plank 2018 or WMAP5 (G1)
  12- 31 F20.15 h-1.Mpc x      [-328.4/-13.9] Cartesian, x coordinate, of sphere
  33- 57 F25.20 h-1.Mpc y      [-295.2/271.5] Cartesian, y coordinate, of sphere
  59- 80 F22.18 h-1.Mpc z      [-15.1/300.1] Cartesian, z coordinate, of sphere
  82-100 F19.16 h-1.Mpc Rad    [3.64/22.6] Radius of sphere
 102-105 I4     ---     void   [0/1183]? Unique sequential identifier of the
                                void for that cosmology (1)
--------------------------------------------------------------------------------
Note (1): The union of all spheres with the same unique identifier form
          one void.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table3.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label  Explanations
--------------------------------------------------------------------------------
  1-  10 A10    ---        Cosmo  Cosmology, Plank 2018 or WMAP5 (G1)
 12-  19 A8     ---        Prune  Pruning, VIDE or REVOLVER
 21-  40 F20.15 h-1.Mpc    x      [-320.2/-29.9] Cartesian, x coordinate, of
                                   void's weighted center
 42-  63 F22.17 h-1.Mpc    y      [-279/267] Cartesian, y coordinate, of void's
                                   weighted center
 65-  85 F21.17 h-1.Mpc    Z      [-7/286.5] Cartesian, z coordinate, of void's
                                   weighted center
 87- 106 F20.18 ---        z      [0.014/0.11] Redshift of the void's weighted
                                   center
108- 125 F18.14 deg        RAdeg  [113.7/257.6] Right Ascension of void's
                                   weighted center (J2000)
127- 146 F20.17 deg        DEdeg  [-1.3/66.7] Declination of void's weighted
                                   center (J2000)
148- 165 F18.15 h-1.Mpc    Reff   [10/53.3] Effective radius of the void
167- 186 F20.16 h-1.Mpc    x1     [-19.3/25.1] Cartesian, x coordinate, of
                                   void's first ellipsoid axis
188- 210 F23.19 h-1.Mpc    y1     [-19.7/14.5] Cartesian, y coordinate, of
                                   void's first ellipsoid axis
212- 234 F23.19 h-1.Mpc    z1     [-14.3/18.3] Cartesian, z coordinate, of
                                   void's first ellipsoid axis
236- 256 F21.17 h-1.Mpc    x2     [-71/59.2] Cartesian, x coordinate, of void's
                                   second ellipsoid axis
258- 280 F23.19 h-1.Mpc    y2     [-48.8/64.1] Cartesian, y coordinate, of
                                   void's second ellipsoid axis
282- 302 F21.17 h-1.Mpc    z2     [-54/50.1] Cartesian, z coordinate, of void's
                                   second ellipsoid axis
304- 326 F23.19 h-1.Mpc    x3     [-34.8/46.2] Cartesian, x coordinate, of
                                   void's third ellipsoid axis
328- 349 F22.18 h-1.Mpc    y3     [-67.2/56] Cartesian, y coordinate, of void's
                                   third ellipsoid axis
351- 371 F21.17 h-1.Mpc    z3     [-25.5/72.5] Cartesian, z coordinate, of
                                   void's third ellipsoid axis
373- 392 F20.13 h-2.Mpc2   area   [2447/174107] Total surface area of the void
394- 417 F24.18 h-2.Mpc2   edge   [0/17639] Surface area of the void which is
                                   adjacent to boundary cells
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table4.dat
--------------------------------------------------------------------------------
   Bytes Format Units Label   Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---   Cosmo   Cosmology, Plank 2018 or WMAP5 (G1)
  12- 19 A8     ---   Prune   Pruning, VIDE or REVOLVER
  21- 24 I4     ---   zone    [0/1036] Unique zone identifier for a given
                               cosmology and pruning
  26- 28 I3     ---   void0   [0/723]?=-1 Unique identifier of the smallest void
                               to which the zone belongs
  30- 32 I3     ---   void1   [0/723]?=-1 Unique identifier of the largest void
                               to which the zone belongs
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table5.dat
--------------------------------------------------------------------------------
   Bytes Format Units Label   Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---   Cosmo   Cosmology, Plank 2018 or WMAP5 (G1)
  12- 19 A8     ---   Prune   Pruning, VIDE or REVOLVER
  21- 26 I6     ---   NSAID   [5/641389] Galaxy NSA v1.0.1 identifier
  28- 31 I4     ---   zone    [0/1036] Unique identifier for the zone to
                               which the galaxy belongs
  33- 34 I2     ---   depth   [0/13] Number of adjacent Voronoi cells (1)
  36- 36 I1     ---   edge    [0/1] Boolean, is galaxy at the edge of the
                               survey mask
  38- 38 I1     ---   out     [0] Boolean, is galaxy outside the survey mask
--------------------------------------------------------------------------------
Note (1): Number of adjacent Voronoi cells between the galaxy's Voronoi cell
          and the edge of the zone to which it belongs.
--------------------------------------------------------------------------------

Global notes:
Note (G1):
    We present void catalogs found with VoidFinder, V2 with VIDE pruning
    (V2/VIDE), and V2 with REVOLVER pruning (V2/REVOLVER) assuming two
    flat {Lambda}CDM cosmologies: WMAP5 ({Omega}_M_=0.258;
    Dunkley+ 2009ApJS..180..306D) and Planck 2018 ({Omega}_M_=0.315;
    Planck Collaboration+ 2020A&A...641A...6P), and assuming
    H_0_=100h.km.s^-1^Mpc^-1^. See Section 4.
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                    Prepared by [AAS], Emmanuelle Perret [CDS]  14-Apr-2023
