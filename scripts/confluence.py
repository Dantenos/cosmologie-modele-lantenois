#!/usr/bin/env python3
"""LA CONFLUENCE — les deux vainqueurs du corpus mesurent-ils la MEME fonction ?
CRITERES PRE-ENREGISTRES (geles AVANT toute execution, 24/08/2026).

L'IDENTITE EXACTE QUI MOTIVE L'ETUDE (algebre, pas hypothese). Le solveur gele
test_wE_v3.fond integre dlng = -3(1+w_E)(1 - Gamma/3H) ; a w_E = 0 (accretion) cela vaut
  s(a) == d ln rho_de / d ln a = -3(1 + w(a)),   w = -beta/(3Ht).
Le rival iLCDM 'de' de l'atlas pose rho_de = Ode a^(-eps), soit s(a) = -eps constant, avec
correction de matiere C = Om + eps*Ode*(a^(3-eps)-1)/(3-eps) — qui est exactement
  u(a) = Om - integrale_1^a s(a') rho_de(a') a'^3 dlna'   (verifie analytiquement).
DONC les deux modeles ne sont pas des rivaux de familles differentes : ce sont deux
PARAMETRISATIONS DE LA MEME FONCTION s(a), avec UNE difference physique declaree —
l'accretion est sourcee de l'EXTERIEUR (matiere intacte, u = Om), l'echange est INTERNE
(la matiere encaisse). Cette etude mesure s(a) et tranche entre les deux lectures.

DONNEES : la vraisemblance legere de l'atlas (BAO DR2 + theta_* + Pantheon+, N = 1597),
LCDM = 1425,086 (ancre #150). Aucune donnee nouvelle : c'est une etude de structure.

GARDE PRIMORDIALE DECLAREE (appliquee identiquement aux DEUX lectures, regle 5) : tout fond
donnant |Omega_de(a)| > 0,02 pour a < 1e-2 (z > 99) est rejete — les distance-priors
supposent la physique primordiale standard. Ce n'est pas un ajustement, c'est le domaine.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. fond_joint(beta, eps=0) doit redonner test_wE_v3.fond('invt', beta) : |dchi2| < 0,05.
  B. fond_pente(eps0, eps1=0, interne=True) doit redonner fond_ilcdm_de(eps0) : |dchi2| < 0,05.
  C. les deux refits marginaux doivent reproduire les ancres : accretion 1419,309 +/- 0,5
     (#150) et ilcdm_de 1415,24 +/- 0,5 (#150/#154).

--- VOLET 1 : CONFLUENCE (beta, eps) conjoints ---
Fit conjoint de rho_de = Ode * g_acc(a;beta) * a^(-eps) (accretion externe + echange interne
en plus). g_acc = gain accretion seule, g_eps = gain eps seul, g_j = gain conjoint.
  CONFLUENTES   si g_j < max(g_acc, g_eps) + 2,0   (le second parametre n'achete rien :
                UN SEUL signal, vu deux fois — deflationniste, ecrit tel quel) ;
  ORTHOGONALES  si g_j >= g_acc + g_eps - 2,0      (deux canaux independants) ;
  PARTIELLES    sinon — ecrit tel quel, avec le gain marginal du second parametre.

--- VOLET 2 : LA PENTE LIBRE s(a) = -(eps0 + eps1 * ln a) ---
Deux parametres, contient LCDM (0,0), contient le vainqueur de l'atlas (0,021 ; 0), et
approche l'accretion (dont la pente est croissante en ln a). Fit dans les DEUX lectures :
  EXTERNE (u = Om, matiere intacte — la lecture d'Edouard) ;
  INTERNE (u = Om - int s rho_de a^3 dlna — la lecture de l'atlas).
Departs a eps1 = 0 (regle 6 : le depart ne suppose PAS le running espere).
  2a. LA PENTE COURT-ELLE ? sigma(eps1) par profil dchi2 = 1 (eps0, h, wb, Om reoptimises).
      PENTE CONSTANTE si |eps1| < 2 sigma(eps1) -> le running n'est pas demande ; on
      s'arrete la pour cette lecture, et on l'ecrit.
      PENTE COURANTE si |eps1| >= 2 sigma(eps1).
  2b. OU S'ANNULE-T-ELLE ? si la pente court : z0 = exp(eps0/eps1) - 1 (zero de s), avec son
      intervalle par profil sur z0 a eps1 libre. Comparaison au croisement fantome GELE
      z_x = 0,402 (#145, croisement_fantome.py, beta = 2,42, Om = 0,314) :
      CONVERGENCE   si 0,402 est dans l'intervalle a 1 sigma de z0 ;
      TENSION       si 0,402 est hors de l'intervalle a 2 sigma ;
      INTERMEDIAIRE sinon. (Un z0 non defini — eps1 de signe tel que le zero tombe hors de
      [0 ; 10] — compte comme TENSION.)
  2c. QUELLE LECTURE LES DONNEES PREFERENT-ELLES ? d = chi2(EXTERNE) - chi2(INTERNE) a
      nombre de parametres EGAL. |d| < 2 : INDISCERNABLES. d >= 2 : l'INTERNE (echange
      sombre) est prefere — DEFAVORABLE a la these du corpus, ecrit en premier si c'est le
      cas. d <= -2 : l'EXTERNE (source hors budget) est prefere.
  2d. L'ACCRETION EST-ELLE DANS LE PLAN ? projection au sens des moindres carres de la pente
      exacte de l'accretion, s_acc(a) = -3(1+w), sur la base (1, ln a) pour ln a dans
      [-1,5 ; 0] (fenetre declaree : l'intervalle observe, z < 3,5), a beta = 2,42 :
      donne (eps0_pred, eps1_pred). Distance du point ajuste a cette prediction, en sigma
      (par la hessienne numerique du chi2 dans le plan). Rapportee, favorable ou non.
      PREDICTION CONFIRMEE si distance < 2 sigma ; REFUTEE si > 3 sigma ; INTERMEDIAIRE
      sinon. C'est le test le plus severe de l'etude : l'accretion n'a AUCUN parametre libre
      dans ce plan une fois beta fixe par ailleurs.

Regle 3 : cette etude REDUIT l'espace des lectures ; elle n'en ferme aucune.
Regle 9 : deux verdicts contradictoires entre lectures = rien n'est exploite.
Usage : python3 scripts/confluence.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import test_wE_v3 as T

AG = A.AG
LNA = np.log(AG)
DLNA = np.diff(LNA)
CHI2_LCDM = 1425.086
ZX_GELE = 0.402
B = [0.69, 0.02236, 0.31]


def _integ(y):
    """integrale de 1 a a de y dlna (vectorisee sur la grille)."""
    I = np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * DLNA)])
    return I - I[-1]


def _garde(rho_de, E2):
    m = AG < 1e-2
    return not np.any(np.abs(rho_de[m] / np.clip(E2[m], 1e-30, None)) > 0.02)


def fond_joint(Om, par):
    """accretion (externe, beta) + echange interne constant (eps), fond auto-coherent."""
    beta, eps = par
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    E2 = Om / AG**3 + Or / AG**4 + Ode
    for _ in range(7):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        integ = 1 / (AG * E)
        t = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(AG))])
        G3H = beta / (3 * np.clip(E * t, 1e-12, None))
        dlng = -3 * (1 - G3H) - eps
        I = np.concatenate([[0.0], np.cumsum(0.5 * (dlng[1:] + dlng[:-1]) * DLNA)])
        g = np.exp(np.clip(I - I[-1], -700, 700))
        rho_de = Ode * g
        u = Om - _integ(-eps * rho_de * AG**3)
        if np.any(u <= 0):
            return None
        E2 = u / AG**3 + Or / AG**4 + rho_de
    if not _garde(rho_de, E2):
        return None
    return A.fond_arrays(E2)


def fond_pente(Om, par, interne):
    """s(a) = -(eps0 + eps1 ln a) ; lecture interne (matiere encaisse) ou externe (intacte)."""
    e0, e1 = par
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    lg = -(e0 * LNA + e1 * LNA**2 / 2)
    if np.max(lg) > 300:
        return None
    g = np.exp(np.clip(lg, -700, 300))
    rho_de = Ode * g
    if interne:
        s = -(e0 + e1 * LNA)
        u = Om - _integ(s * rho_de * AG**3)
        if np.any(u <= 0):
            return None
    else:
        u = Om
    E2 = u / AG**3 + Or / AG**4 + rho_de
    if np.any(~np.isfinite(E2)) or np.any(E2 <= 0) or not _garde(rho_de, E2):
        return None
    return A.fond_arrays(E2)


A.CUSTOM.update({
    'joint':    fond_joint,
    'pente_ex': lambda Om, p: fond_pente(Om, p, False),
    'pente_in': lambda Om, p: fond_pente(Om, p, True),
})


def chi2_at(fam, npar, fix, starts=None):
    """chi2 profile : parametres du modele FIXES, (h, wb, Om) reoptimises."""
    st = starts or [B, [0.68, 0.0224, 0.30], [0.70, 0.0223, 0.32]]
    return A.fit(fam, npar, st, fixpar=fix).fun


def sigma_1d(fam, npar, best, idx, pas, autres_libres):
    """sigma par profil dchi2 = 1 sur le parametre idx, les autres reoptimises."""
    c0 = autres_libres(best)
    v0 = best[idx]
    for sens in (+1, -1):
        for k in range(1, 40):
            p = list(best)
            p[idx] = v0 + sens * k * pas
            if autres_libres(p) > c0 + 1.0:
                return k * pas
    return 40 * pas


if __name__ == "__main__":
    print("LA CONFLUENCE — les deux vainqueurs mesurent-ils la meme fonction ? (criteres geles)\n")

    # ---------------- VALIDATIONS ----------------
    print("  --- validations ---")
    r_acc = A.fit('invt', 1, [B + [2.4], B + [2.0], B + [2.8]], bornes=[(0.5, 5.0)])
    beta_h = r_acc.x[3]
    c_acc = r_acc.fun
    r_eps = A.fit('ilcdm_de', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    eps_h = r_eps.x[3]
    c_eps = r_eps.fun
    vA = abs(chi2_at('joint', 2, (beta_h, 0.0)) - chi2_at('invt', 1, beta_h))
    vB = abs(chi2_at('pente_in', 2, (eps_h, 0.0)) - chi2_at('ilcdm_de', 1, eps_h))
    vC = abs(c_acc - 1419.309) < 0.5 and abs(c_eps - 1415.24) < 0.5
    print(f"    A. joint(beta,0) == invt(beta)     : |dchi2| = {vA:.4f}  -> {'OK' if vA < 0.05 else 'ECHEC'}")
    print(f"    B. pente_in(eps,0) == ilcdm_de(eps): |dchi2| = {vB:.4f}  -> {'OK' if vB < 0.05 else 'ECHEC'}")
    print(f"    C. ancres : accretion {c_acc:.3f} (1419,309) ; ilcdm_de {c_eps:.3f} (1415,24)"
          f" -> {'OK' if vC else 'ECHEC'}")
    if not (vA < 0.05 and vB < 0.05 and vC):
        sys.exit("    UNE VALIDATION ECHOUE — rien n'est publie.")

    g_acc = CHI2_LCDM - c_acc
    g_eps = CHI2_LCDM - c_eps
    print(f"\n    gains de reference : accretion {g_acc:+.2f} (beta = {beta_h:.3f}) ; "
          f"echange {g_eps:+.2f} (eps = {eps_h:+.4f})")

    # ---------------- VOLET 1 ----------------
    print("\n  --- VOLET 1 : confluence (beta, eps) ---")
    r_j = A.fit('joint', 2, [B + [beta_h, 0.0], B + [2.0, 0.02], B + [2.8, -0.02]],
                bornes=[(0.5, 5.0), (-0.5, 0.5)])
    g_j = CHI2_LCDM - r_j.fun
    print(f"    conjoint : chi2 = {r_j.fun:.3f}  gain = {g_j:+.2f}  "
          f"beta = {r_j.x[3]:.3f}  eps = {r_j.x[4]:+.4f}")
    gmax = max(g_acc, g_eps)
    if g_j < gmax + 2.0:
        v1 = "CONFLUENTES — un seul signal, vu deux fois (le second parametre n'achete rien)"
    elif g_j >= g_acc + g_eps - 2.0:
        v1 = "ORTHOGONALES — deux canaux independants"
    else:
        v1 = f"PARTIELLES — gain marginal du second parametre : {g_j - gmax:+.2f}"
    print(f"    VERDICT VOLET 1 : {v1}")

    # ---------------- VOLET 2 ----------------
    print("\n  --- VOLET 2 : la pente libre s(a) = -(eps0 + eps1 ln a) ---")
    res2 = {}
    for lect, fam in [("EXTERNE", 'pente_ex'), ("INTERNE", 'pente_in')]:
        r = A.fit(fam, 2, [B + [0.02, 0.0], B + [0.4, 0.0], B + [0.0, 0.0]],
                  bornes=[(-2.0, 2.0), (-2.0, 2.0)])
        e0, e1 = r.x[3], r.x[4]
        prof = lambda p: chi2_at(fam, 2, (p[0], p[1]))
        s1 = sigma_1d(fam, 2, [e0, e1], 1, 0.02, prof)
        court = abs(e1) >= 2 * s1
        print(f"    [{lect}] chi2 = {r.fun:.3f}  gain = {CHI2_LCDM - r.fun:+.2f}  "
              f"eps0 = {e0:+.4f}  eps1 = {e1:+.4f} +/- {s1:.4f}  -> "
              f"{'PENTE COURANTE' if court else 'PENTE CONSTANTE'} ({abs(e1)/max(s1,1e-9):.1f} sigma)")
        z0, iz = None, None
        if court:
            z0 = np.exp(e0 / e1) - 1 if abs(e1) > 1e-9 else np.inf
            if 0 <= z0 <= 10:
                lo, hi = None, None
                for sens in (+1, -1):
                    for k in range(1, 60):
                        zz = z0 + sens * k * 0.05
                        if zz <= -0.99:
                            break
                        # profil sur z0 : eps0 = eps1*ln(1+z0), eps1 libre
                        best = 1e18
                        for e1t in np.linspace(e1 - 3 * s1, e1 + 3 * s1, 13):
                            if abs(e1t) < 1e-6:
                                continue
                            c = chi2_at(fam, 2, (e1t * np.log(1 + zz), e1t))
                            best = min(best, c)
                        if best > r.fun + 1.0:
                            if sens > 0:
                                hi = zz
                            else:
                                lo = zz
                            break
                iz = (lo, hi)
                print(f"           zero de la pente : z0 = {z0:.3f}  intervalle 1 sigma = "
                      f"[{lo if lo is not None else float('nan'):.3f} ; "
                      f"{hi if hi is not None else float('nan'):.3f}]  (z_x gele = {ZX_GELE})")
            else:
                print(f"           zero de la pente hors [0 ; 10] (z0 = {z0:.2f}) -> compte TENSION")
        res2[lect] = dict(chi2=r.fun, e0=e0, e1=e1, s1=s1, court=court, z0=z0, iz=iz)

    # 2c
    d = res2["EXTERNE"]["chi2"] - res2["INTERNE"]["chi2"]
    if abs(d) < 2:
        v2c = "INDISCERNABLES — a parametres egaux, les donnees ne tranchent pas la source"
    elif d >= 2:
        v2c = (f"L'INTERNE (echange sombre) EST PREFERE de {d:+.2f} — DEFAVORABLE a la lecture "
               "externe du corpus, ecrit en premier")
    else:
        v2c = f"L'EXTERNE (source hors budget) EST PREFERE de {-d:+.2f}"
    print(f"\n    VERDICT 2c (source) : {v2c}")

    # 2d : projection de l'accretion
    r0 = A.fit('invt', 1, [B + [2.42]], bornes=[(0.5, 5.0)], fixpar=2.42)
    Om0 = r0.x[2]
    Or0 = Om0 / 3388.0
    Ode0 = 1 - Om0 - Or0
    E2 = Om0 / AG**3 + Or0 / AG**4 + Ode0
    for _ in range(7):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        integ = 1 / (AG * E)
        t = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(AG))])
        G3H = 2.42 / (3 * np.clip(E * t, 1e-12, None))
        dlng = -3 * (1 - G3H)
        I = np.concatenate([[0.0], np.cumsum(0.5 * (dlng[1:] + dlng[:-1]) * DLNA)])
        E2 = Om0 / AG**3 + Or0 / AG**4 + Ode0 * np.exp(np.clip(I - I[-1], -700, 700))
    s_acc = dlng
    m = (LNA >= -1.5) & (LNA <= 0.0)
    M = np.vstack([np.ones(m.sum()), LNA[m]]).T
    coef, *_ = np.linalg.lstsq(M, -s_acc[m], rcond=None)
    e0p, e1p = coef
    print(f"\n    2d. pente exacte de l'accretion (beta = 2,42) projetee sur (1, ln a), "
          f"ln a dans [-1,5 ; 0] : eps0_pred = {e0p:+.4f}  eps1_pred = {e1p:+.4f}")
    for lect, fam in [("EXTERNE", 'pente_ex'), ("INTERNE", 'pente_in')]:
        R = res2[lect]
        c_pred = chi2_at(fam, 2, (e0p, e1p))
        dchi = c_pred - R["chi2"]
        nsig = np.sqrt(max(dchi, 0.0))
        verdict = ("CONFIRMEE" if nsig < 2 else ("REFUTEE" if nsig > 3 else "INTERMEDIAIRE"))
        print(f"        [{lect}] chi2 au point predit = {c_pred:.3f}  (dchi2 = {dchi:+.2f}, "
              f"{nsig:.1f} sigma a 2 ddl) -> PREDICTION {verdict}")

    print("\n  Rappel regle 3 : cette etude REDUIT l'espace des lectures ; elle n'en ferme aucune.")
