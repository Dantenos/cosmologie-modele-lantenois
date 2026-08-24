#!/usr/bin/env python3
"""LE CHAMPION DE L'ATLAS EST-IL wCDM DEGUISE ? CRITERES PRE-ENREGISTRES (geles AVANT
execution, 24/08/2026). Verification d'une IMPOSSIBILITE, au sens de confronteur.py.

L'ALGEBRE QUI DECLENCHE L'ALERTE. fond_ilcdm_de pose
  E^2 = C(a) a^-3 + Or a^-4 + Ode a^-eps,   C(a) = Om + eps*Ode*(a^(3-eps)-1)/(3-eps).
En developpant C(a) a^-3 :
  C a^-3 + Ode a^-eps = [Om - eps*Ode/(3-eps)] a^-3 + [3*Ode/(3-eps)] a^-eps
                      = Om' a^-3 + Ode' a^-eps,
avec Om' = Om - eps*Ode/(3-eps) et Ode' = 3*Ode/(3-eps), et l'on verifie Om' + Ode' =
Om + Ode. Or a^-eps == a^(-3(1+w')) pour w' = eps/3 - 1, c'est-a-dire EXACTEMENT g_wcdm(w')
de l'atlas. Donc, au niveau du FOND (le seul niveau ou l'atlas juge), la famille
'ilcdm_de' est CONTENUE dans la famille 'wcdm' — ce n'est pas une interaction, c'est une
reparametrisation. Une famille contenue ne peut pas battre celle qui la contient.
ATLAS (#150) : ilcdm_de = 1415,245 ; wcdm = 1423,843. Ecart de 8,60 dans le sens IMPOSSIBLE.
Une des deux valeurs est fausse. Cette etude dit laquelle.
(La famille 'ilcdm_dm' NE se reduit PAS a wCDM — son exposant de matiere devient a^(eps-3) ;
elle n'est pas concernee et n'est pas jugee ici.)

--- CRITERES (exhaustifs, exclusifs) ---
  A. IDENTITE EXACTE. E^2 reconstruit a la main (meme Or que fond_ilcdm_de, pour ne pas
     melanger la comptabilite du rayonnement) contre fond_ilcdm_de, sur AG entier :
     max |dE/E| < 1e-12 attendu. Si l'identite ECHOUE -> BUG D'IMPLEMENTATION, localise et
     ecrit ; les criteres B et C ne sont pas evalues.
  B. IDENTITE DANS L'ATLAS. Meme comparaison mais contre CUSTOM['wcdm'](Om', w'), qui
     recalcule Or a partir de Om' : un residu de l'ordre de (Om-Om')/3388 ~ 1,5e-6 relatif
     est ATTENDU et declare. Critere : max |dE/E| < 1e-5 ET |dchi2| < 0,05 aux memes
     (h, omega_b). Sinon INCOHERENCE DE COMPTABILITE, ecrite telle quelle.
  C. LE VERDICT. Refit COMPLET de la famille 'wcdm' en partant du point image (h, ob, Om',
     w') du meilleur ilcdm_de, plus les departs d'origine de l'atlas (regle 5 : le rival
     garde tout ce qu'il a le droit de reajuster) :
       CLASSEMENT DE L'ATLAS FAUX  si le refit atteint <= 1416,0 — alors le 1423,843 publie
         est un MINIMUM LOCAL, l'ordre du palmares est un artefact d'optimisation, et
         #150/#154/#156/#158 ainsi que la resolution de T7 doivent etre RETRACTES ;
       CONTRADICTION NON RESOLUE  si le refit reste > 1416,0 alors que A et B passent —
         ecrit tel quel, rien n'est exploite (regle 9), et l'etude est versee au greffe ;
       (aucun troisieme cas : A, B et C epuisent les possibilites.)
  Regle 3 : cette verification REDUIT ; elle ne ferme rien.
  Regle 8 : si le verdict est « classement faux », la retractation part en MANQUEMENTS
  numerotee ET en TRIAGE_DES_ATTAQUES, sans delai et sans attenuation.
Usage : python3 scripts/degenerescence_ilcdm.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import test_wE_v3 as T

AG = A.AG
B = [0.69, 0.02236, 0.31]
CHI2_ATLAS_ILCDM = 1415.245
CHI2_ATLAS_WCDM = 1423.843


def image(Om, eps):
    """(Om', w') : le point wCDM image du point iLCDM (Om, eps)."""
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    Om_p = Om - eps * Ode / (3 - eps)
    Ode_p = 3 * Ode / (3 - eps)
    return Om_p, Ode_p, Or, eps / 3.0 - 1.0


def fond_main(Om, eps):
    """E^2 reconstruit a la main depuis la decomposition, meme Or que fond_ilcdm_de."""
    Om_p, Ode_p, Or, _ = image(Om, eps)
    return Om_p / AG**3 + Or / AG**4 + Ode_p * AG**(-eps)


if __name__ == "__main__":
    print("LE CHAMPION DE L'ATLAS EST-IL wCDM DEGUISE ? (criteres geles)\n")

    r_i = A.fit('ilcdm_de', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    h_i, ob_i, Om_i, eps_i = r_i.x
    print(f"  meilleur iLCDM 'de' : chi2 = {r_i.fun:.3f}  (atlas {CHI2_ATLAS_ILCDM})  "
          f"h = {h_i:.4f}  Om = {Om_i:.4f}  eps = {eps_i:+.5f}")
    Om_p, Ode_p, Or, w_p = image(Om_i, eps_i)
    print(f"  point image wCDM    : Om' = {Om_p:.6f}  Ode' = {Ode_p:.6f}  w' = {w_p:.6f}")

    # --- critere A ---
    z_ref, E_ref = A.CUSTOM['ilcdm_de'](Om_i, eps_i)
    E_main = np.sqrt(fond_main(Om_i, eps_i))[::-1]
    eA = float(np.max(np.abs(E_main / E_ref - 1)))
    okA = eA < 1e-12
    print(f"\n  A. identite exacte (meme Or)      : max |dE/E| = {eA:.3e} -> "
          f"{'OK' if okA else 'ECHEC — BUG D IMPLEMENTATION'}")
    if not okA:
        i = int(np.argmax(np.abs(E_main / E_ref - 1)))
        print(f"     ecart maximal a a = {AG[::-1][i]:.3e} ; B et C non evalues.")
        sys.exit(1)

    # --- critere B ---
    z_w, E_w = A.CUSTOM['wcdm'](Om_p, w_p)
    eB = float(np.max(np.abs(E_w / E_ref - 1)))
    c_i = T.chi2(h_i, ob_i, Om_i, 0.0, eps_i, 'ilcdm_de')
    c_w = T.chi2(h_i, ob_i, Om_p, 0.0, w_p, 'wcdm')
    okB = eB < 1e-5 and abs(c_w - c_i) < 0.05
    print(f"  B. identite dans l'atlas          : max |dE/E| = {eB:.3e} ; "
          f"chi2 iLCDM = {c_i:.4f} vs wCDM image = {c_w:.4f} (d = {c_w - c_i:+.4f}) -> "
          f"{'OK' if okB else 'INCOHERENCE DE COMPTABILITE'}")

    # --- critere C ---
    starts = [[h_i, ob_i, Om_p, w_p], B + [-0.9], B + [-1.1], B + [-0.99], B + [-0.95]]
    r_w = A.fit('wcdm', 1, starts, bornes=[(-2, -0.2)])
    print(f"\n  C. refit complet de wCDM (depart = point image + departs d'origine) :")
    print(f"     chi2 = {r_w.fun:.3f}  h = {r_w.x[0]:.4f}  Om = {r_w.x[2]:.4f}  "
          f"w = {r_w.x[3]:.5f}   (atlas publiait {CHI2_ATLAS_WCDM})")
    if r_w.fun <= 1416.0:
        print(f"\n  VERDICT : CLASSEMENT DE L'ATLAS FAUX — le wCDM publie ({CHI2_ATLAS_WCDM}) "
              f"est un MINIMUM LOCAL ;\n            le refit atteint {r_w.fun:.3f}, soit "
              f"{r_w.fun - CHI2_ATLAS_WCDM:+.3f}. L'ordre du palmares est un artefact\n"
              f"            d'optimisation. RETRACTATION due : #150, #154, #156, #158, T7.")
    else:
        print(f"\n  VERDICT : CONTRADICTION NON RESOLUE — A et B passent (les deux fonds sont "
              f"le meme),\n            mais le refit wCDM reste a {r_w.fun:.3f} > 1416,0. "
              f"Regle 9 : rien n'est exploite ;\n            l'anomalie est versee au greffe "
              f"telle quelle.")
