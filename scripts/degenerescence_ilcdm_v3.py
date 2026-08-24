#!/usr/bin/env python3
"""D'OU VIENT VRAIMENT L'AVANCE DU CHAMPION DE L'ATLAS ? L'ETALONNAGE, PAS LE FOND.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

DECLARATION D'HONNETETE (ce que j'ai deja vu avant d'ecrire ces criteres — cf. #162).
J'ai vu : ilcdm_de = 1415,245 et wcdm = 1423,843 (atlas #150) ; l'identite EXACTE des deux
fonds au point image, max|dE/E| = 3,33e-16 (#164 critere A, passe) ; l'ecart de 240,15 en
chi2 entre ces deux fonds IDENTIQUES ; et la lecture du corps de test_wE_v3.chi2, qui
calcule om = Om*h*h, rd = r_drag(ob, om), z_star/r_star(ob, om) et surtout
R = sqrt(Om)*Dc(z*) — quatre etalonnages tires de l'ETIQUETTE Om. Or la matiere de
'ilcdm_de' a la recombinaison vaut Om' = Om - eps*Ode/(3-eps), inferieure de ~1,7 %.
L'hypothese est donc DEJA formee et l'issue analytiquement previsible : cette etude ne
DECOUVRE pas, elle CONFIRME par construction explicite et elle CHIFFRE. C'est declare.

CE QUI EST ETABLI (n'est pas re-teste) : au niveau du fond, 'ilcdm_de'(Om, eps) est
rigoureusement 'wcdm'(Om', w') avec Om' = Om - eps*Ode/(3-eps) et w' = eps/3 - 1.
CE QUI EST EN CAUSE : le fond est le meme, mais chi2 etalonne r_d, z_*, r_* et R avec Om
(l'etiquette, densite AUJOURD'HUI) au lieu de Om' (la densite AVANT recombinaison, seule
pertinente pour un horizon sonore et pour le parametre de decalage). Le modele obtient
ainsi une densite de matiere pour son expansion et une AUTRE pour son etalonnage. R est
contraint a ~0,2 % : 1,7 % sur Om, c'est ~0,85 % sur sqrt(Om), plusieurs sigma offerts.

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  L'identite des fonds doit tenir a max|dE/E| < 1e-12 en QUATRE points (Om, eps) declares :
  (0,2981 ; +0,0213), (0,32 ; +0,05), (0,28 ; -0,03), (0,35 ; +0,10). Une identite qui ne
  tiendrait qu'au point optimal serait une coincidence, pas une algebre.

--- VOLET 1 : LE MINIMUM HONNETE DE wCDM (contre le soupcon de minimum local) ---
Profil complet en w sur [-1,10 ; -0,90], 21 valeurs, (h, omega_b, Om) reoptimises a chaque
valeur — pas de Nelder-Mead multidimensionnel a qui l'on puisse reprocher de s'etre coince.
  ARTEFACT D'ETALONNAGE CONFIRME  si min du profil >= 1421,0 (gain <= 4,1 sur LCDM :
     l'essentiel des 9,84 vient de l'etalonnage, pas de l'interaction) ;
  ARTEFACT REFUTE                 si min du profil <= 1417,0 (gain >= 8,1 : alors c'etait
     le fit wcdm de l'atlas qui etait coince, les deux modeles sont le meme et doivent
     FIGURER A EGALITE — le classement est faux, mais pour une autre raison) ;
  INTERMEDIAIRE                   sinon, ecrit tel quel.

--- VOLET 2 : L'ARTEFACT, CHIFFRE COMME FONCTION DE eps ---
Pour eps dans (-0,05 ; -0,02 ; 0 ; +0,0213 ; +0,05 ; +0,08), les DEUX chi2 aux memes fonds :
etalonnage-etiquette (famille 'ilcdm_de', a eps fixe) contre etalonnage-coherent (famille
'wcdm', a w' = eps/3-1 fixe), (h, omega_b, Om) reoptimises des deux cotes. L'ecart est
l'artefact. A eps = 0 les deux doivent coincider a moins de 0,05 (controle interne :
sans echange, il n'y a pas d'ecart entre l'etiquette et la densite reelle).
  Rapporte tel quel, favorable ou non.

--- VOLET 3 : DIAGNOSTIC SUR L'AUTRE iLCDM (aucun verdict rendu ici) ---
'ilcdm_dm' pose rho_m = Om a^(eps-3) : sa densite de matiere a la recombinaison vaut
Om*a^eps, soit a a = 1e-3 un facteur (1e-3)^eps. On rapporte ce facteur au meilleur eps
publie, pour dire si la meme question se pose — sans y repondre : ce serait une autre
etude, avec ses propres criteres.

--- VERDICT ET CONSEQUENCE (regle 8) ---
Si ARTEFACT CONFIRME : RETRACTATION due, numerotee en MANQUEMENTS et portee a
TRIAGE_DES_ATTAQUES, touchant #150 (classement de l'atlas), #154, #156, #158 (les trois
volets de l'arbitre de T7, tous passes dans le meme pipeline), la RESOLUTION de T7, et le
verdict 2c de #161. Sans attenuation et sans delai.
Regle 3 : cette etude REDUIT ; elle ne ferme rien — l'echange sombre n'est pas refute, c'est
la MESURE de son avantage qui l'est.
Usage : python3 scripts/degenerescence_ilcdm_v3.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import test_wE_v3 as T

AG = A.AG
B = [0.69, 0.02236, 0.31]
CHI2_LCDM = 1425.086
CHI2_ATLAS_ILCDM = 1415.245
CHI2_ATLAS_WCDM = 1423.843
POINTS_VALID = [(0.2981, 0.0213), (0.32, 0.05), (0.28, -0.03), (0.35, 0.10)]
STARTS = [B, [0.68, 0.0224, 0.28], [0.70, 0.0223, 0.33], [0.685, 0.02245, 0.305]]


def image(Om, eps):
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    return Om - eps * Ode / (3 - eps), eps / 3.0 - 1.0


if __name__ == "__main__":
    print("L'AVANCE VIENT-ELLE DE L'ETALONNAGE ? (criteres geles)\n")

    print("  --- validation : l'identite des fonds en quatre points ---")
    pire = 0.0
    for Om, eps in POINTS_VALID:
        Omp, wp = image(Om, eps)
        za, Ea = A.CUSTOM['ilcdm_de'](Om, eps)
        zb, Eb = A.CUSTOM['wcdm'](Omp, wp)
        e = float(np.max(np.abs(Eb / Ea - 1)))
        pire = max(pire, e)
        print(f"    (Om = {Om:.4f}, eps = {eps:+.4f}) -> (Om' = {Omp:.5f}, w' = {wp:.5f}) : "
              f"max |dE/E| = {e:.3e}")
    if pire >= 1e-12:
        sys.exit(f"    VALIDATION ECHOUE (pire = {pire:.3e}) — rien n'est publie.")
    print(f"    -> identite ALGEBRIQUE confirmee (pire = {pire:.3e})\n")

    print("  --- VOLET 1 : profil complet en w de wCDM (21 valeurs, h/ob/Om reoptimises) ---")
    best, w_best = 1e18, None
    for w in np.linspace(-1.10, -0.90, 21):
        c = A.fit('wcdm', 1, STARTS, fixpar=float(w)).fun
        if c < best:
            best, w_best = c, float(w)
    print(f"    minimum du profil : chi2 = {best:.3f} a w = {w_best:.4f}  "
          f"(l'atlas publiait {CHI2_ATLAS_WCDM})")
    gain = CHI2_LCDM - best
    if best >= 1421.0:
        v1 = "ARTEFACT D'ETALONNAGE CONFIRME"
    elif best <= 1417.0:
        v1 = "ARTEFACT REFUTE — le fit wcdm de l'atlas etait coince"
    else:
        v1 = "INTERMEDIAIRE"
    print(f"    gain du modele COHERENT sur LCDM = {gain:+.3f}  (l'atlas annonce +9,84)")
    print(f"    VERDICT VOLET 1 : {v1}")

    print("\n  --- VOLET 2 : l'artefact comme fonction de eps ---")
    print(f"    {'eps':>8s} {'etiquette':>11s} {'coherent':>11s} {'artefact':>10s}")
    for eps in (-0.05, -0.02, 0.0, 0.0213, 0.05, 0.08):
        c_lab = A.fit('ilcdm_de', 1, STARTS, fixpar=float(eps)).fun
        c_coh = A.fit('wcdm', 1, STARTS, fixpar=float(eps / 3.0 - 1.0)).fun
        print(f"    {eps:+8.4f} {c_lab:11.3f} {c_coh:11.3f} {c_coh - c_lab:+10.3f}"
              + ("   <- controle : doit etre ~0" if eps == 0.0 else ""))

    print("\n  --- VOLET 3 : diagnostic sur 'ilcdm_dm' (aucun verdict) ---")
    r_dm = A.fit('ilcdm_dm', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    e_dm = r_dm.x[3]
    fac = (1e-3) ** e_dm
    print(f"    meilleur eps = {e_dm:+.5f} ; sa matiere a a = 1e-3 vaut Om*(1e-3)^eps = "
          f"{fac:.4f} * Om, soit {100*(fac-1):+.2f} %")
    print(f"    -> la meme question se pose{' (ecart plus grand encore)' if abs(fac-1) > 0.017 else ''} ; "
          f"elle appartient a une autre etude, avec ses propres criteres.")

    print()
    if v1 == "ARTEFACT D'ETALONNAGE CONFIRME":
        print(f"  VERDICT : RETRACTATION DUE. L'avance de l'iLCDM 'de' ne vient pas de "
              f"l'interaction mais de\n            l'etalonnage : meme fond, deux densites de "
              f"matiere. Part imputable a l'etalonnage =\n            "
              f"{best - CHI2_ATLAS_ILCDM:.2f} des {CHI2_LCDM - CHI2_ATLAS_ILCDM:.2f} unites. "
              f"Retracter #150, #154, #156, #158, la\n            resolution de T7 et le "
              f"verdict 2c de #161 (regle 8 : MANQUEMENTS + TRIAGE).")
    elif v1.startswith("ARTEFACT REFUTE"):
        print("  VERDICT : le fit wcdm de l'atlas etait coince — les deux modeles sont LE MEME "
              "et doivent\n            figurer a egalite. Le classement reste faux, mais "
              "l'avance est reelle. Retractation\n            du seul classement.")
    else:
        print(f"  VERDICT : INTERMEDIAIRE (min = {best:.3f}) — regle 9 : rien n'est exploite, "
              f"versement au greffe.")
