#!/usr/bin/env python3
"""L'ETALONNAGE COMPRIME EST-IL SEULEMENT APPLICABLE A 'ilcdm_dm' ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026). Deuxieme volet de la
retractation #166, dont le diagnostic sur 'ilcdm_dm' avait ete POSE SANS VERDICT.

LE CONTRASTE STRUCTUREL QUI MOTIVE L'ETUDE.
  'ilcdm_de' : rho_m(a) = C(a) a^-3 avec C(a) -> Om' = Om - eps*Ode/(3-eps) quand a -> 0.
     La densite de matiere effective est CONSTANTE avant recombinaison : il existe UN omega_m
     correct, et l'etalonnage est reparable (c'est ce qu'a montre #166 : gain +1,21).
  'ilcdm_dm' : rho_m(a) = Om a^(eps-3), soit Om_eff(a) = Om * a^eps — la densite effective
     DEPEND de l'epoque. Les formules d'ajustement de r_d et le parametre de decalage
     R = sqrt(Om) D_c(z_*) supposent une matiere en a^-3 : aucun omega_m unique ne represente
     ce modele. La question n'est donc plus « quelle valeur corriger » mais « la correction
     a-t-elle seulement un sens ».

METHODE. On decouple l'etalonnage du fond sans toucher a test_wE_v3.chi2 (gele) : la famille
personnalisee recoit Om_cal (celui que chi2 utilisera pour r_d, z_*, r_*, R) et reconstruit
le fond avec Om_bg = Om_cal * a_ref^(-eps), de sorte que Om_eff(a_ref) = Om_cal exactement.
Deux choix d'epoque de reference, tous deux DEFENDABLES et declares :
  a_* = 1/1091 (recombinaison — ce que R et z_* veulent) ;
  a_eq = 1/3388 (equivalence — ce que r_d integre sur la plus grande part de son support).
Le fond n'est PAS modifie autrement : la convention de rayonnement reste celle de l'atlas
(#164 volet 1 a montre qu'elle n'est pas le moteur de l'ecart).

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  Le refit de 'ilcdm_dm' tel quel doit redonner l'ancre de l'atlas, 1415,818 +/- 0,3 (#150).

--- CRITERES (exhaustifs, exclusifs) ---
  1. AMBIGUITE. d = |chi2(a_*) - chi2(a_eq)|, les deux refittes completement.
     ETALONNAGE INAPPLICABLE  si d >= 3,0 — deux choix egalement defendables donnent des
        chi2 incompatibles : aucun nombre ne peut etre publie pour ce modele avec des priors
        comprimes, et l'entree #150 doit etre RETIREE, pas corrigee ;
     ETALONNAGE ROBUSTE       si d < 1,0 — la correction a un sens ; on publie le gain
        corrige (moyenne des deux, ecart en barre d'erreur) ;
     INTERMEDIAIRE            sinon, ecrit tel quel.
  2. LE GAIN CORRIGE, dans les deux choix, rapporte quel que soit le verdict 1 :
     gain = 1425,086 - chi2. On dira s'il reste devant ou derriere l'accretion (+5,78).
  3. CONTROLE INTERNE : a eps = 0 les trois versions (etiquette, a_*, a_eq) doivent coincider
     a moins de 0,05 — sans echange, Om_eff ne depend plus de l'epoque. Si ce controle
     echoue, l'etude entiere n'est pas interpretee.
  Regle 3 : cette etude REDUIT ; elle ne ferme rien. Regle 8 : tout retrait supplementaire
  part en MANQUEMENTS numerote et en TRIAGE_DES_ATTAQUES.
Usage : python3 scripts/etalonnage_dm.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

B = [0.69, 0.02236, 0.31]
CHI2_LCDM = 1425.086
ANCRE_DM = 1415.818
GAIN_ACC = 5.777
A_STAR = 1.0 / 1091.0
A_EQ = 1.0 / 3388.0
STARTS = [B, [0.68, 0.0224, 0.28], [0.70, 0.0223, 0.33], [0.685, 0.02245, 0.305]]


def fond_cal(Om_cal, eps, a_ref):
    """fond de 'ilcdm_dm' tel que Om_eff(a_ref) = Om_cal (l'etalonnage de chi2 sera juste)."""
    if abs(eps - 3) < 1e-3:
        return None
    Om_bg = Om_cal * a_ref ** (-eps)
    if not (0.05 < Om_bg < 0.95):
        return None
    return A.CUSTOM['ilcdm_dm'](Om_bg, eps)


A.CUSTOM.update({
    'dm_star': lambda Om, p: fond_cal(Om, p, A_STAR),
    'dm_eq':   lambda Om, p: fond_cal(Om, p, A_EQ),
})

if __name__ == "__main__":
    print("L'ETALONNAGE COMPRIME EST-IL APPLICABLE A 'ilcdm_dm' ? (criteres geles)\n")

    r0 = A.fit('ilcdm_dm', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    ok = abs(r0.fun - ANCRE_DM) < 0.3
    print(f"  [validation] refit tel quel : chi2 = {r0.fun:.3f} (ancre {ANCRE_DM}) -> "
          f"{'OK' if ok else 'ECHEC'}   eps = {r0.x[3]:+.5f}")
    if not ok:
        sys.exit("    rien n'est publie.")

    print("\n  --- controle interne a eps = 0 ---")
    c_lab0 = A.fit('ilcdm_dm', 1, STARTS, fixpar=0.0).fun
    c_st0 = A.fit('dm_star', 1, STARTS, fixpar=0.0).fun
    c_eq0 = A.fit('dm_eq', 1, STARTS, fixpar=0.0).fun
    ec = max(abs(c_st0 - c_lab0), abs(c_eq0 - c_lab0))
    print(f"    etiquette {c_lab0:.3f} | a_* {c_st0:.3f} | a_eq {c_eq0:.3f} -> "
          f"ecart max {ec:.4f} -> {'OK' if ec < 0.05 else 'ECHEC — RIEN N EST INTERPRETE'}")
    if ec >= 0.05:
        sys.exit("    l'etude n'est pas interpretee (critere 3).")

    print("\n  --- refits complets ---")
    r_st = A.fit('dm_star', 1, [s + [0.01] for s in STARTS] + [B + [-0.01]],
                 bornes=[(-0.5, 0.5)])
    r_eq = A.fit('dm_eq', 1, [s + [0.01] for s in STARTS] + [B + [-0.01]],
                 bornes=[(-0.5, 0.5)])
    for nom, r in [("etiquette (atlas)", r0), ("coherent a a_*", r_st), ("coherent a a_eq", r_eq)]:
        print(f"    {nom:<20s} chi2 = {r.fun:9.3f}  gain = {CHI2_LCDM - r.fun:+7.3f}  "
              f"eps = {r.x[3]:+.5f}")

    d = abs(r_st.fun - r_eq.fun)
    if d >= 3.0:
        v = "ETALONNAGE INAPPLICABLE"
    elif d < 1.0:
        v = "ETALONNAGE ROBUSTE"
    else:
        v = "INTERMEDIAIRE"
    print(f"\n  VERDICT 1 (ambiguite) : |chi2(a_*) - chi2(a_eq)| = {d:.3f} -> {v}")

    gm = CHI2_LCDM - 0.5 * (r_st.fun + r_eq.fun)
    print(f"  VERDICT 2 (gain corrige) : {gm:+.3f} +/- {d/2:.3f} — "
          f"{'DEVANT' if gm > GAIN_ACC else 'DERRIERE'} l'accretion (+{GAIN_ACC:.2f})")

    print()
    if v == "ETALONNAGE INAPPLICABLE":
        print("  CONSEQUENCE : l'entree 'iLCDM Q=eps H rho_dm' de l'atlas doit etre RETIREE,")
        print("                pas corrigee — aucun omega_m unique ne represente ce modele,")
        print("                donc aucun chi2 a priors comprimes ne lui est attribuable.")
    elif v == "ETALONNAGE ROBUSTE":
        print(f"  CONSEQUENCE : l'entree peut etre CORRIGEE a {CHI2_LCDM - gm:.3f} "
              f"(gain {gm:+.3f}).")
    else:
        print(f"  CONSEQUENCE : ambiguite de {d:.2f} unites a porter comme incertitude "
              f"declaree\n                sur toute valeur publiee pour ce modele.")
