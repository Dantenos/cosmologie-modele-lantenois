#!/usr/bin/env python3
"""
gradient_fecondite.py — Le test de sélection, retourné.

QUESTION PRE-ENREGISTREE (ecrite AVANT execution, 19/08) :
  Si la selection cosmologique naturelle opere dans NOTRE version (seuil GSL a
  l'echelle des amas), alors les parametres observes doivent sieger pres d'un
  MAXIMUM de la fecondite F(Omega_m, sigma8, n_s). Le gradient est calculable.
  - Si |dlnF/dln theta| ~< 1 pour les trois : compatible avec un optimum -> le cadre survit.
  - Si un gradient est grand et sans borne : la selection-comme-maximisation est
    FAUSSE pour notre version. On l'ecrit tel quel. Pas de reinterpretation a posteriori.

NOUVEAUTE PAR RAPPORT A L'ESTIMATION DE LA VEILLE (+nu^2 = 6,2) :
  Le seuil M_cut n'est PAS une masse fixe. Il est defini par la condition spectrale
  n_eff(M_cut) = -2.08 (equivalente a beta = 4.35, la borne GSL du papier B).
  Quand on bouge Omega_m, l'echelle d'egalite bouge, donc n_eff(M) bouge, donc M_cut
  bouge. C'est exactement la "contre-pression" proposee. Elle est ici CALCULEE,
  pas postulee : on verra dans quel sens elle agit.

CONVENTIONS DECLAREES :
  - Transfert : Eisenstein & Hu 1998 sans oscillations (eq. 28-31), T_cmb = 2.7255 K.
  - n_eff(M) : convention "pente de sigma", n_eff = -6 dln sigma/dln M - 3.
    C'est celle deja utilisee dans le corpus (sigma(M) ~ M^{-(n_eff+3)/6}, controle
    Press-Schechter/Sheth-Tormen du 19/08). La convention alternative n_eff = dlnP/dlnk
    a k=1/R est calculee en controle.
  - Fecondite : densite comobile de halos au-dessus de M_cut, fonction de masse de
    Press-Schechter (valeur conservatrice du papier B ; Sheth-Tormen en controle).
  - Deux protocoles de variation, car ils ne disent pas la meme chose :
      (P1) a sigma8 FIXE  : on ne bouge que la forme du spectre.
      (P2) a amplitude primordiale FIXE (A_s) : protocole physiquement correct pour
           un argument de selection (A_s est fondamental, sigma8 est derive).
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- cosmologie de reference
# Planck 2018 TT,TE,EE+lowE+lensing, valeurs utilisees dans le corpus
REF = dict(Om=0.3153, Ob=0.04930, h=0.6736, ns=0.9649, s8=0.8111)
DELTA_C = 1.686
NEFF_CUT = -2.08          # borne GSL du papier B : beta < 4.35
RHO_CRIT = 2.775e11       # M_sun / (Mpc/h)^3  -> rho_m = RHO_CRIT * Om * h^0 (unites h)

def T_eh98(k, Om, Ob, h):
    """Transfert Eisenstein-Hu 1998 sans oscillations. k en h/Mpc."""
    theta = 2.7255 / 2.7
    omh2, obh2 = Om * h * h, Ob * h * h
    fb = Ob / Om
    s = 44.5 * np.log(9.83 / omh2) / np.sqrt(1.0 + 10.0 * obh2 ** 0.75)   # Mpc
    alpha = (1.0 - 0.328 * np.log(431.0 * omh2) * fb
             + 0.38 * np.log(22.3 * omh2) * fb ** 2)
    ks = k * h * s                                                        # sans dimension
    gamma_eff = Om * h * (alpha + (1.0 - alpha) / (1.0 + (0.43 * ks) ** 4))
    q = k * theta ** 2 / gamma_eff
    L0 = np.log(2.0 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)

def P_shape(k, Om, Ob, h, ns):
    """Spectre non normalise : k^ns T^2."""
    return k ** ns * T_eh98(k, Om, Ob, h) ** 2

def sigma_R(R, Om, Ob, h, ns):
    """sigma(R) non normalise, fenetre top-hat, R en Mpc/h."""
    def integrand(lnk):
        k = np.exp(lnk)
        x = k * R
        w = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return P_shape(k, Om, Ob, h, ns) * w * w * k ** 3
    val, _ = quad(integrand, np.log(1e-5), np.log(5e2), limit=250)
    return np.sqrt(val / (2.0 * np.pi ** 2))

def R_of_M(M, Om, h):
    """Rayon lagrangien (Mpc/h) d'une masse M (M_sun/h) pour un fond de matiere Om."""
    rho_m = RHO_CRIT * Om
    return (3.0 * M / (4.0 * np.pi * rho_m)) ** (1.0 / 3.0)

def sigma_M(M, Om, Ob, h, ns, norm):
    return norm * sigma_R(R_of_M(M, Om, h), Om, Ob, h, ns)

def normalisation(Om, Ob, h, ns, s8):
    """Facteur qui impose sigma(8 Mpc/h) = s8."""
    return s8 / sigma_R(8.0, Om, Ob, h, ns)

def n_eff_sigma(M, Om, Ob, h, ns, norm, dlnM=0.05):
    """n_eff = -6 dln sigma / dln M - 3 (convention du corpus)."""
    lp = np.log(sigma_M(M * np.exp(dlnM), Om, Ob, h, ns, norm))
    lm = np.log(sigma_M(M * np.exp(-dlnM), Om, Ob, h, ns, norm))
    return -6.0 * (lp - lm) / (2.0 * dlnM) - 3.0

def n_eff_P(M, Om, Ob, h, ns, dlnk=0.05):
    """Controle : n_eff = dlnP/dlnk evalue a k = 1/R(M)."""
    k = 1.0 / R_of_M(M, Om, h)
    lp = np.log(P_shape(k * np.exp(dlnk), Om, Ob, h, ns))
    lm = np.log(P_shape(k * np.exp(-dlnk), Om, Ob, h, ns))
    return (lp - lm) / (2.0 * dlnk)

def M_cut(Om, Ob, h, ns, norm, cible=NEFF_CUT, conv='sigma'):
    """Masse ou n_eff atteint la borne GSL. n_eff DECROIT quand M decroit."""
    f = ((lambda lM: n_eff_sigma(np.exp(lM), Om, Ob, h, ns, norm) - cible)
         if conv == 'sigma' else
         (lambda lM: n_eff_P(np.exp(lM), Om, Ob, h, ns) - cible))
    lo, hi = np.log(1e10), np.log(1e18)
    if f(lo) > 0 or f(hi) < 0:
        return np.nan
    return np.exp(brentq(f, lo, hi, xtol=1e-4))

def f_PS(nu):
    return np.sqrt(2.0 / np.pi) * nu * np.exp(-nu * nu / 2.0)

def f_ST(nu, a=0.707, p=0.3, A=0.3222):
    return A * np.sqrt(2.0 * a / np.pi) * (1.0 + (a * nu * nu) ** (-p)) * nu * np.exp(-a * nu * nu / 2.0)

def fecondite(Om, Ob, h, ns, norm, Mc, forme='PS'):
    """Densite comobile de halos au-dessus de Mc (Mpc/h)^-3. n(M) dM = f(nu) (rho_m/M) |dln sigma/dlnM| dlnM."""
    rho_m = RHO_CRIT * Om
    ff = f_PS if forme == 'PS' else f_ST
    def integrand(lnM):
        M = np.exp(lnM)
        s = sigma_M(M, Om, Ob, h, ns, norm)
        nu = DELTA_C / s
        d = 0.05
        dlnsdlnM = (np.log(sigma_M(M * np.exp(d), Om, Ob, h, ns, norm))
                    - np.log(sigma_M(M * np.exp(-d), Om, Ob, h, ns, norm))) / (2.0 * d)
        return ff(nu) * (rho_m / M) * abs(dlnsdlnM)
    val, _ = quad(integrand, np.log(Mc), np.log(1e17), limit=200)
    return val

def etat(Om=None, Ob=None, h=None, ns=None, s8=None, As_fixe=None, forme='PS'):
    """Calcule (M_cut, F) pour un jeu de parametres.
    Si As_fixe est fourni, la normalisation est portee par l'amplitude primordiale
    (protocole P2) au lieu de sigma8 (protocole P1)."""
    Om = REF['Om'] if Om is None else Om
    Ob = REF['Ob'] if Ob is None else Ob
    h = REF['h'] if h is None else h
    ns = REF['ns'] if ns is None else ns
    s8 = REF['s8'] if s8 is None else s8
    norm = As_fixe if As_fixe is not None else normalisation(Om, Ob, h, ns, s8)
    Mc = M_cut(Om, Ob, h, ns, norm)
    F = fecondite(Om, Ob, h, ns, norm, Mc, forme)
    s8_eff = norm * sigma_R(8.0, Om, Ob, h, ns)
    return dict(Mc=Mc, F=F, s8=s8_eff, nu=DELTA_C / (norm * sigma_R(R_of_M(Mc, Om, h), Om, Ob, h, ns)))


if __name__ == '__main__':
    np.seterr(all='ignore')
    R = REF
    norm0 = normalisation(R['Om'], R['Ob'], R['h'], R['ns'], R['s8'])

    print("=" * 78)
    print("  VERIFICATION 1 : les deux ancrages du papier B sont-ils dans la meme convention ?")
    print("=" * 78)
    print("  Le papier B affirme deux choses :")
    print("    (a) n_eff = -1.4  (notre beta = 2.42)  a  M ~ 1.4e16 M_sun, 30-40 Mpc/h")
    print("    (b) n_eff = -2.08 (borne GSL)          a  M_cut ~ 2.5e14 M_sun")
    for conv, fn in [('sigma  (n_eff = -6 dlnsigma/dlnM - 3)',
                      lambda M: n_eff_sigma(M, R['Om'], R['Ob'], R['h'], R['ns'], norm0)),
                     ('P(k)   (n_eff = dlnP/dlnk a k=1/R)',
                      lambda M: n_eff_P(M, R['Om'], R['Ob'], R['h'], R['ns']))]:
        print(f"\n  --- convention {conv}")
        for M in [1e13, 1e14, 2.5e14, 1e15, 1e16, 1.4e16, 1e17]:
            print(f"      M = {M:8.1e} M_sun/h   ->  n_eff = {fn(M):+.3f}"
                  f"   (R = {R_of_M(M, R['Om'], R['h']):6.2f} Mpc/h)")

    print("\n" + "=" * 78)
    print("  VERIFICATION 2 : ou tombe reellement le seuil GSL n_eff = -2.08 ?")
    print("=" * 78)
    for conv in ['sigma', 'P']:
        Mc = M_cut(R['Om'], R['Ob'], R['h'], R['ns'], norm0, conv=conv)
        print(f"  convention {conv:6s} : M_cut = {Mc:.3e} M_sun/h"
              f"   (papier B annonce 2.5e14)   ecart = x{Mc/2.5e14:.2g}")
