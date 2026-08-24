#!/usr/bin/env python3
"""CONTROLE D'EQUITE (regle 2) — NOTRE eps CONTRE LA SEULE MESURE EN VRAISEMBLANCE COMPLETE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI. L'arbitre grave de T10 est "la vraisemblance CMB complete appliquee a cette meme
famille". Verification faite dans la litterature : **elle existe deja**, pour le cousin
CONSERVE de notre famille. Tsiapi & Basilakos, MNRAS 485 (2019) 2505 (arXiv:1810.12902),
modifient CAMB et confrontent aux spectres de puissance Planck 2015 TT,TE,EE+lowP -- pas aux
priors comprimes. Leur modele Lambda(H)CDM2 pose Q = 3 nu H rho_dm, d'ou
rho_dm = rho_dm,0 a^(-3(1-nu)). La regle 2 exige de recalculer avec LEURS valeurs publiees.

LES VALEURS PUBLIEES, RECOPIEES SANS RETOUCHE (leurs tables 1 et 2, colonne Lambda(H)CDM2) :
    Planck seul                  nu x 10^3 = +0,59 (+1,0 / -1,0)
    joint CMB+BAO+SNIa+H0        nu x 10^3 = -0,08 (+0,72 / -0,78)
Leur conclusion, citee : "We find that Lambda(H)CDM2 and Lambda(H)CDM3 do not show
deviations from the LCDM case."

LES TROIS ECARTS DE MODELE QU'IL FAUT ACCORDER AVANT DE COMPARER (regle 5) :
  (i) leur nu porte sur la MATIERE NOIRE SEULE, le notre sur la matiere TOTALE. Les baryons
      restent en a^-3 chez eux. La conversion honnete n'est donc PAS eps = 3 nu mais
      eps = 3 nu x (rho_dm/rho_m) = 3 nu (1 - omega_b/omega_m).
  (ii) leur nu force AUSSI le vide a evoluer (leur eq. 15) et entre dans E^2 avec un facteur
      1/(1-nu) (leur eq. 16). Notre famille garde Lambda constante. Ce sont deux modeles
      differents, et la conversion ne porte QUE sur l'exposant.
  (iii) leurs donnees sont Planck 2015 + JLA + BOSS/WiggleZ + Riess 2018 ; les notres
      Pantheon+ + DESI DR2 + priors Planck 2018 + SH0ES. Aucun recouvrement complet.
On accorde les trois. La comparaison qui suit ne prouve donc RIEN sur leur modele : elle
mesure seulement de combien notre nombre s'ecarte du seul nombre publie du meme voisinage.

--- CRITERES (exhaustifs, exclusifs) ---
  1. CONVERSION. On convertit leurs deux valeurs en eps equivalent par la formule (i), avec
     omega_b/omega_m pris a NOTRE optimum LCDM gele -- et non au leur, qu'on n'a pas.
     On rapporte la valeur de ce facteur : s'il sort de [0,80 ; 0,88], la conversion est
     declaree non fiable et le critere 3 est rapporte SANS conclusion.
  2. ECART. On rapporte l'ecart entre notre critere 3 (eps = -0,0100 +/- 0,0020) et leur
     valeur jointe convertie, en sigma combines (quadrature des deux incertitudes).
  3. VERDICT, et il ne peut prendre que ces quatre formes :
     COMPATIBLE si l'ecart est < 2 sigma ;
     TENSION si 2 <= ecart < 3 sigma ;
     DESACCORD si l'ecart >= 3 sigma ;
     et dans les trois cas on ajoute NOTRE PROPRE SYSTEMATIQUE : le controle 7b de
     dilution_arbitre.py deplace notre eps de 4,0 sigma a lui seul (convention de
     rayonnement dans r_s). Si ce deplacement DEPASSE l'ecart mesure au critere 2, alors le
     verdict est ecrase par la mention obligatoire : DESACCORD CONTENU DANS NOTRE PROPRE
     SYSTEMATIQUE -- c'est-a-dire que le desaccord ne nous appartient pas comme resultat.
  4. TRADUCTION PHYSIQUE, dans les deux sens. On rapporte, pour notre eps et pour le leur
     converti, l'ecart relatif entre la densite de matiere d'aujourd'hui et celle
     qu'implique la recombinaison : Om(a_*)/Om(1) = a_*^eps. C'est le nombre que T9 compare.

REGLE 6. Les valeurs de substitution vont dans le sens DEFAVORABLE a notre these : quand
leur intervalle est asymetrique on retient la borne qui les rapproche de zero (donc qui
AUGMENTE notre desaccord), et le facteur de conversion est pris a sa valeur qui REDUIT leur
eps (donc qui augmente encore l'ecart).
Regle 3 : ce controle REDUIT l'opposabilite de notre nombre ; il n'etablit rien sur le leur.
Usage : python3 scripts/equite_dilution.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_arbitre as D

# --- leurs valeurs publiees, recopiees sans retouche (x 10^-3)
NU_PLANCK = (+0.59, +1.0, -1.0)
NU_JOINT = (-0.08, +0.72, -0.78)
# --- notre critere 3
EPS_NOUS, SIG_NOUS = -0.0100, 0.0020
DEPL_7B = 4.0          # deplacement en sigma du controle 7b (rayonnement)

if __name__ == "__main__":
    print("CONTROLE D'EQUITE (criteres geles)\n")

    # ---- critere 1 : conversion
    r0 = D.profil(0.0, D.CFG['1_table_etiq'])
    h, ob, Om = (float(v) for v in r0.x)
    om = Om*h*h
    f = 1.0 - ob/om
    print("  --- critere 1 : conversion nu -> eps ---")
    print(f"     notre optimum LCDM gele : h = {h:.5f}  omega_b = {ob:.5f}  omega_m = {om:.5f}")
    print(f"     fraction de matiere noire rho_dm/rho_m = {f:.4f}")
    fiable = 0.80 <= f <= 0.88
    print(f"     -> {'conversion fiable' if fiable else 'CONVERSION NON FIABLE'}")

    def conv(t):
        c, sp, sm = t
        return 3e-3*c*f, 3e-3*abs(sp)*f, 3e-3*abs(sm)*f

    ep, epp, epm = conv(NU_PLANCK)
    ej, ejp, ejm = conv(NU_JOINT)
    print(f"     Planck seul : nu = {NU_PLANCK[0]:+.2f}e-3  ->  "
          f"eps = {ep:+.5f} +{epp:.5f}/-{epm:.5f}")
    print(f"     joint       : nu = {NU_JOINT[0]:+.2f}e-3  ->  "
          f"eps = {ej:+.5f} +{ejp:.5f}/-{ejm:.5f}")

    # ---- critere 2 : ecart (regle 6 : on prend la borne qui NOUS dessert)
    sig_eux = ejp if ej > EPS_NOUS else ejm       # celle qui rapproche leur valeur de zero
    ecart = abs(EPS_NOUS - ej)/np.sqrt(SIG_NOUS**2 + sig_eux**2)
    print("\n  --- critere 2 : ecart avec la mesure en vraisemblance complete ---")
    print(f"     nous  eps = {EPS_NOUS:+.5f} +/- {SIG_NOUS:.5f}   (critere 3 de l'arbitre)")
    print(f"     eux   eps = {ej:+.5f} +/- {sig_eux:.5f}   (converti, borne defavorable)")
    print(f"     ecart = {ecart:.2f} sigma combines")

    # ---- critere 3 : verdict
    print("\n  --- critere 3 : VERDICT ---")
    if ecart < 2:
        v = "COMPATIBLE"
    elif ecart < 3:
        v = "TENSION"
    else:
        v = "DESACCORD"
    print(f"     {v} ({ecart:.2f} sigma)")
    if DEPL_7B > ecart:
        print(f"     MAIS notre propre controle 7b deplace eps de {DEPL_7B:.1f} sigma, soit")
        print(f"     PLUS que l'ecart mesure ({ecart:.2f} sigma). Mention obligatoire :")
        print("     -> DESACCORD CONTENU DANS NOTRE PROPRE SYSTEMATIQUE.")
        print("        Le desaccord ne nous appartient pas comme resultat.")
    else:
        print(f"     (controle 7b : {DEPL_7B:.1f} sigma, inferieur a l'ecart : le verdict tient)")

    # ---- critere 4 : traduction physique
    print("\n  --- critere 4 : traduction en densites ---")
    a_s = D.A_STAR
    for nom, e in (("nous (arbitre)", EPS_NOUS), ("eux (joint, converti)", ej)):
        rap = a_s**e
        print(f"     {nom:<22s} eps = {e:+.5f}  ->  Om(recombinaison)/Om(aujourd'hui) = "
              f"{rap:.4f}")
        print(f"     {'':<22s} soit la matiere d'aujourd'hui {100*(1/rap - 1):+.2f} % "
              f"par rapport a ce qu'implique la recombinaison")
    print(f"\n     (rappel : le discriminant scelle de T9 vaut 1,70 %)")
