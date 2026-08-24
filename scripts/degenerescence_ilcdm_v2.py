#!/usr/bin/env python3
"""L'AVANCE DU CHAMPION DE L'ATLAS EST-ELLE UN ARTEFACT DE COMPTABILITE DU RAYONNEMENT ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026). Suite de #164 (v1), dont le
verdict gele fut « CONTRADICTION NON RESOLUE, rien n'est exploite » — donc rien n'en est
repris comme acquis, sauf le fait etabli par son critere A, qui a passe a 3,3e-16 :

  FAIT ETABLI (algebre, #164 critere A) : C(a) a^-3 + Ode a^-eps identique a
  Om' a^-3 + Ode' a^-eps, avec Om' = Om - eps*Ode/(3-eps), Ode' = 3*Ode/(3-eps).
  La matiere EFFECTIVE de 'ilcdm_de' aux temps primordiaux est Om', pas Om.

  DIAGNOSTIC A TESTER (ce que le critere B de #164 a localise sans conclure) : l'atlas pose
  Or = Om/3388 pour TOUS les modeles — convention qui fixe l'equivalence matiere-rayonnement
  a z_eq = 3387. Pour 'ilcdm_de' cette convention lit Om (l'etiquette) et non Om' (la
  matiere reelle), ce qui lui donne z_eq = 3388*Om'/Om, soit ~1,7 % plus BAS que tous ses
  rivaux. L'ecart de fond mesure en #164 (|dE/E| = 8,46e-3 en regime radiatif) vaut
  exactement la moitie de dOr/Or = 1,68 % — signature quantitative du rayonnement, et de
  rien d'autre. Question : les 8,60 unites de chi2 qui separent ilcdm_de (1415,245) de
  wcdm (1423,843) viennent-elles de l'INTERACTION, ou de ce z_eq offert ?

--- VOLET 1 : LA MEME COMPTABILITE POUR TOUS ---
Refit complet de 'ilcdm_de' avec Or = Om'/3388 (z_eq = 3387 comme tout le monde ; Or et Om'
resolus ensemble par iteration, la boucle converge en 3 tours car Or ~ 3e-4 * Om).
  ARTEFACT DE RAYONNEMENT  si le gain sur LCDM (1425,086) tombe <= 3,0 ;
  GAIN REEL                si le gain reste >= 6,0 ;
  INTERMEDIAIRE            sinon. Ecrit tel quel dans les trois cas.

--- VOLET 2 : LE MEME PRIVILEGE AU RIVAL (regle 5) ---
Si la liberte en cause est celle de z_eq, elle n'appartient a personne en propre : on la
donne a wCDM. Famille 'wcdm_zeq' : Or = f * Om/3388, f libre dans [0,90 ; 1,10] (soit
z_eq entre 3079 et 3764), w libre. Deux parametres, comme CPL en a deux.
  GENERIQUE   si wcdm_zeq atteint <= 1416,0 — la liberte est celle de z_eq, disponible a
              n'importe quel modele, et l'interaction n'y est pour rien ;
  SPECIFIQUE  si wcdm_zeq reste > 1419,0 — seule l'interaction produit ce gain ;
  INTERMEDIAIRE sinon.
On rapporte aussi le f prefere et le z_eq correspondant : si la donnee veut vraiment
deplacer l'equivalence, c'est un resultat sur la DONNEE, pas sur un modele, et il vaut
d'etre dit meme s'il dessert la these de l'interaction.

--- VERDICT COMBINE (exhaustif, exclusif) ---
  ARTEFACT + GENERIQUE            -> RETRACTATION : le classement de l'atlas (#150) et la
     resolution de T7 (#158) reposent sur une convention, pas sur une physique. Depart
     immediat en MANQUEMENTS numerote ET en TRIAGE_DES_ATTAQUES (regle 8), sans attenuation.
  GAIN REEL + SPECIFIQUE          -> l'avance survit ; T7 tient ; on l'ecrit.
  toute autre combinaison         -> AMBIGU : regle 9, rien n'est exploite, versement au
     greffe tel quel.
Regle 3 : cette etude REDUIT ; elle ne ferme rien.
Usage : python3 scripts/degenerescence_ilcdm_v2.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

AG = A.AG
B = [0.69, 0.02236, 0.31]
CHI2_LCDM = 1425.086
CHI2_ATLAS_ILCDM = 1415.245
CHI2_ATLAS_WCDM = 1423.843


def bases_coherentes(Om, eps, n=6):
    """Or = Om'/3388 et Ode = 1-Om-Or resolus ensemble (z_eq = 3387 pour tout le monde)."""
    Or = Om / 3388.0
    for _ in range(n):
        Ode = 1 - Om - Or
        Om_p = Om - eps * Ode / (3 - eps)
        Or = Om_p / 3388.0
    return Or, 1 - Om - Or, Om_p


def fond_ilcdm_coh(Om, eps):
    if abs(eps - 3) < 1e-3:
        return None
    Or, Ode, _ = bases_coherentes(Om, eps)
    rho_de = Ode * AG**(-eps)
    C = Om + eps * Ode * (AG**(3 - eps) - 1) / (3 - eps)
    if np.any(C < 0) or Or <= 0:
        return None
    return A.fond_arrays(C * AG**-3 + Or / AG**4 + rho_de)


def fond_wcdm_zeq(Om, par):
    w, f = par
    Or = f * Om / 3388.0
    Ode = 1 - Om - Or
    if Or <= 0 or Ode <= 0:
        return None
    return A.fond_arrays(Om / AG**3 + Or / AG**4 + Ode * AG**(-3 * (1 + w)))


A.CUSTOM.update({'ilcdm_coh': fond_ilcdm_coh, 'wcdm_zeq': fond_wcdm_zeq})

if __name__ == "__main__":
    print("ARTEFACT DE COMPTABILITE ? (criteres geles)\n")

    r0 = A.fit('ilcdm_de', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    Om0, e0 = r0.x[2], r0.x[3]
    Or0 = Om0 / 3388.0
    Ode0 = 1 - Om0 - Or0
    Omp0 = Om0 - e0 * Ode0 / (3 - e0)
    print(f"  rappel atlas : ilcdm_de = {r0.fun:.3f} (Om = {Om0:.4f}, eps = {e0:+.5f}) ; "
          f"matiere effective Om' = {Omp0:.4f}")
    print(f"  -> z_eq effectif offert par la convention : {3388*Omp0/Om0:.0f} "
          f"(au lieu de 3387 pour tous les autres, soit {100*(Omp0/Om0-1):+.2f} %)\n")

    # --- VOLET 1 ---
    r1 = A.fit('ilcdm_coh', 1, [B + [0.02], B + [-0.02], B + [0.0]], bornes=[(-0.5, 0.5)])
    g1 = CHI2_LCDM - r1.fun
    if g1 <= 3.0:
        v1 = "ARTEFACT DE RAYONNEMENT"
    elif g1 >= 6.0:
        v1 = "GAIN REEL"
    else:
        v1 = "INTERMEDIAIRE"
    print(f"  VOLET 1 — meme comptabilite pour tous (Or = Om'/3388) :")
    print(f"    chi2 = {r1.fun:.3f}  (etait {CHI2_ATLAS_ILCDM})  eps = {r1.x[3]:+.5f}  "
          f"gain sur LCDM = {g1:+.3f}")
    print(f"    VERDICT VOLET 1 : {v1}")

    # --- VOLET 2 ---
    r2 = A.fit('wcdm_zeq', 2, [B + [-0.99, 1.0], B + [-1.02, 0.98], B + [-0.95, 1.02]],
               bornes=[(-2.0, -0.2), (0.90, 1.10)])
    w2, f2 = r2.x[3], r2.x[4]
    if r2.fun <= 1416.0:
        v2 = "GENERIQUE"
    elif r2.fun > 1419.0:
        v2 = "SPECIFIQUE"
    else:
        v2 = "INTERMEDIAIRE"
    print(f"\n  VOLET 2 — le meme privilege au rival (regle 5) :")
    print(f"    wcdm_zeq : chi2 = {r2.fun:.3f}  (wCDM fige = {CHI2_ATLAS_WCDM})  "
          f"w = {w2:.5f}  f = {f2:.5f}  -> z_eq = {3387*f2**-1:.0f}")
    print(f"    VERDICT VOLET 2 : {v2}")

    # --- VERDICT COMBINE ---
    print()
    if v1 == "ARTEFACT DE RAYONNEMENT" and v2 == "GENERIQUE":
        print(f"  VERDICT : RETRACTATION. L'avance de {CHI2_ATLAS_ILCDM:.1f} du champion de "
              f"l'atlas repose sur une\n            convention de rayonnement, pas sur une "
              f"interaction. #150, #154, #156, #158\n            et la resolution de T7 "
              f"doivent etre retractes (regle 8 : MANQUEMENTS + TRIAGE).")
    elif v1 == "GAIN REEL" and v2 == "SPECIFIQUE":
        print("  VERDICT : L'AVANCE SURVIT — elle n'est ni une convention ni une liberte "
              "generique.\n            T7 tient en l'etat.")
    else:
        print(f"  VERDICT : AMBIGU ({v1} + {v2}) — regle 9 : rien n'est exploite, "
              f"versement au greffe tel quel.")
