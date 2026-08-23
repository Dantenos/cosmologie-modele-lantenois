#!/usr/bin/env python3
"""
gradient_v2.py — version vectorisee : gradients de fecondite dans (Omega_m, sigma8, n_s).

Criteres pre-enregistres (identiques a la v1, ecrits avant execution) :
  - |dlnF/dln theta| <~ 1 pour les trois -> compatible avec un maximum -> le cadre survit.
  - un gradient grand et sans borne -> la selection-comme-maximisation est FAUSSE
    pour notre version. On l'ecrit tel quel.
Le seuil M_cut est RECALCULE a chaque jeu de parametres via n_eff(M_cut) = -2.08 :
  c'est la contre-pression proposee, mise a l'epreuve au lieu d'etre postulee.
"""
import numpy as np
from scipy.optimize import brentq

REF = dict(Om=0.3153, Ob=0.04930, h=0.6736, ns=0.9649, s8=0.8111)
DELTA_C, NEFF_CUT, RHO_CRIT = 1.686, -2.08, 2.775e11
LNK = np.linspace(np.log(1e-5), np.log(3e2), 4000)
K = np.exp(LNK)

def T_eh98(k, Om, Ob, h):
    theta = 2.7255 / 2.7
    omh2, obh2, fb = Om * h * h, Ob * h * h, Ob / Om
    s = 44.5 * np.log(9.83 / omh2) / np.sqrt(1.0 + 10.0 * obh2 ** 0.75)
    alpha = 1.0 - 0.328 * np.log(431.0 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    ks = k * h * s
    gam = Om * h * (alpha + (1.0 - alpha) / (1.0 + (0.43 * ks) ** 4))
    q = k * theta ** 2 / gam
    L0 = np.log(2.0 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)

class Cosmo:
    """Spectre + sigma(R) tabules une fois, puis interpoles : ~1000x plus rapide."""
    def __init__(self, Om, Ob, h, ns, s8=None, amp=None):
        self.Om, self.Ob, self.h, self.ns = Om, Ob, h, ns
        self.P = K ** ns * T_eh98(K, Om, Ob, h) ** 2
        self.lnR = np.linspace(np.log(0.005), np.log(1000.0), 600)
        Rg = np.exp(self.lnR)
        x = np.outer(Rg, K)
        W = np.where(x < 1e-3, 1.0 - x ** 2 / 10.0,
                     3.0 * (np.sin(x) - x * np.cos(x)) / np.where(x == 0, 1, x) ** 3)
        integ = self.P * K ** 3 / (2.0 * np.pi ** 2)
        self.sig_brut = np.sqrt(np.trapezoid(W ** 2 * integ, LNK, axis=1))
        self.lnsig_brut = np.log(self.sig_brut)
        s8_brut = np.exp(np.interp(np.log(8.0), self.lnR, self.lnsig_brut))
        self.amp = amp if amp is not None else s8 / s8_brut
        self.s8 = self.amp * s8_brut
        self.rho_m = RHO_CRIT * Om

    def R_of_M(self, M):  return (3.0 * M / (4.0 * np.pi * self.rho_m)) ** (1.0 / 3.0)
    def lnsig_M(self, M): return np.log(self.amp) + np.interp(np.log(self.R_of_M(M)), self.lnR, self.lnsig_brut)
    def sig_M(self, M):   return np.exp(self.lnsig_M(M))

    def n_eff(self, M, d=0.08):
        return -6.0 * (self.lnsig_M(M * np.exp(d)) - self.lnsig_M(M * np.exp(-d))) / (2.0 * d) - 3.0

    def n_eff_P(self, M, d=0.08):
        k = 1.0 / self.R_of_M(M)
        lnP = np.log(self.P)
        return (np.interp(np.log(k) + d, LNK, lnP) - np.interp(np.log(k) - d, LNK, lnP)) / (2.0 * d)

    def M_cut(self, cible=NEFF_CUT, conv='sigma'):
        f = (lambda lM: self.n_eff(np.exp(lM)) - cible) if conv == 'sigma' \
            else (lambda lM: self.n_eff_P(np.exp(lM)) - cible)
        lo, hi = np.log(1e8), np.log(1e18)
        if f(lo) > 0 or f(hi) < 0: return np.nan
        return np.exp(brentq(f, lo, hi, xtol=1e-3))

    def F(self, Mc, forme='PS', Mmax=1e17, n=400):
        """Densite comobile de halos au-dessus de Mc, en (Mpc/h)^-3."""
        lnM = np.linspace(np.log(Mc), np.log(Mmax), n)
        M = np.exp(lnM)
        s = self.sig_M(M); nu = DELTA_C / s
        d = 0.05
        dls = (self.lnsig_M(M * np.exp(d)) - self.lnsig_M(M * np.exp(-d))) / (2.0 * d)
        if forme == 'PS':
            f = np.sqrt(2.0 / np.pi) * nu * np.exp(-nu ** 2 / 2.0)
        else:
            a, p, A = 0.707, 0.3, 0.3222
            f = A * np.sqrt(2 * a / np.pi) * (1 + (a * nu ** 2) ** (-p)) * nu * np.exp(-a * nu ** 2 / 2)
        return np.trapezoid(f * (self.rho_m / M) * np.abs(dls), lnM)

def etat(Om=None, Ob=None, h=None, ns=None, s8=None, amp=None, forme='PS', conv='sigma'):
    c = Cosmo(REF['Om'] if Om is None else Om, REF['Ob'] if Ob is None else Ob,
              REF['h'] if h is None else h, REF['ns'] if ns is None else ns,
              s8=(REF['s8'] if (s8 is None and amp is None) else s8), amp=amp)
    Mc = c.M_cut(conv=conv)
    return c, Mc, c.F(Mc, forme)

if __name__ == '__main__':
    np.seterr(all='ignore')
    c0, Mc0, F0 = etat()
    amp0 = c0.amp
    print("=" * 80)
    print("  ETAT DE REFERENCE (Planck 2018, convention sigma, Press-Schechter)")
    print("=" * 80)
    print(f"  sigma8 = {c0.s8:.4f} | M_cut(n_eff=-2.08) = {Mc0:.3e} M_sun/h")
    print(f"  sigma(M_cut) = {c0.sig_M(Mc0):.4f} | nu = {DELTA_C/c0.sig_M(Mc0):.3f}")
    print(f"  F = n(>M_cut) = {F0:.4e} (Mpc/h)^-3")
    print(f"  controle : n(>1e14) = {c0.F(1e14):.4e} ; n(>2.5e14) = {c0.F(2.5e14):.4e} (Mpc/h)^-3")

    print("\n" + "=" * 80)
    print("  GRADIENTS : dlnF/dln(theta), differences centrees a +/-2 %")
    print("=" * 80)
    eps = 0.02
    grads_P1 = []
    for proto, kw_lo, kw_hi, label in [
        ('P1 sigma8 fixe', dict(Om=REF['Om']*(1-eps)), dict(Om=REF['Om']*(1+eps)), 'Omega_m'),
        ('P1 sigma8 fixe', dict(s8=REF['s8']*(1-eps)), dict(s8=REF['s8']*(1+eps)), 'sigma_8'),
        ('P1 sigma8 fixe', dict(ns=REF['ns']*(1-eps)), dict(ns=REF['ns']*(1+eps)), 'n_s'),
    ]:
        _, Mlo, Flo = etat(**kw_lo); _, Mhi, Fhi = etat(**kw_hi)
        g = (np.log(Fhi) - np.log(Flo)) / (2 * eps)
        gM = (np.log(Mhi) - np.log(Mlo)) / (2 * eps)
        print(f"  [{proto}] dlnF/dln {label:8s} = {g:+8.2f}    (dln M_cut/dln {label:8s} = {gM:+7.2f})")
        grads_P1.append((label, g))
    trop = [f"{l} ({g:+.2f})" for l, g in grads_P1 if abs(g) > 1.0]
    print("  VERDICT (critere gele : |dlnF/dln theta| <~ 1 pour les trois) : "
          + ("le cadre survit" if not trop else "ECHEC pour " + ", ".join(trop)
             + " -> la selection-comme-maximisation est FAUSSE pour notre version. Ecrit tel quel."))

    print()
    for kw_lo, kw_hi, label in [
        (dict(Om=REF['Om']*(1-eps), amp=amp0), dict(Om=REF['Om']*(1+eps), amp=amp0), 'Omega_m'),
        (dict(amp=amp0*(1-eps)),               dict(amp=amp0*(1+eps)),               'A_s^(1/2)'),
        (dict(ns=REF['ns']*(1-eps), amp=amp0), dict(ns=REF['ns']*(1+eps), amp=amp0), 'n_s'),
    ]:
        _, Mlo, Flo = etat(**kw_lo); _, Mhi, Fhi = etat(**kw_hi)
        g = (np.log(Fhi) - np.log(Flo)) / (2 * eps)
        gM = (np.log(Mhi) - np.log(Mlo)) / (2 * eps)
        print(f"  [P2 amplitude primordiale fixe] dlnF/dln {label:10s} = {g:+8.2f}"
              f"    (dln M_cut/dln {label:10s} = {gM:+7.2f})")

    print("\n" + "=" * 80)
    print("  BALAYAGE : y a-t-il un MAXIMUM interieur en Omega_m ?  (sigma8 fixe)")
    print("=" * 80)
    print(f"  {'Omega_m':>8s} {'M_cut':>11s} {'nu(M_cut)':>10s} {'F':>12s} {'F/F_0':>10s}")
    for Om in [0.10, 0.15, 0.20, 0.25, 0.3153, 0.40, 0.50, 0.70, 1.00]:
        try:
            c, Mc, F = etat(Om=Om)
            print(f"  {Om:8.4f} {Mc:11.3e} {DELTA_C/c.sig_M(Mc):10.3f} {F:12.4e} {F/F0:10.3f}")
        except Exception as e:
            print(f"  {Om:8.4f}  echec : {e}")

    print("\n" + "=" * 80)
    print("  BALAYAGE en sigma_8 et n_s (Omega_m fixe)")
    print("=" * 80)
    for s8 in [0.5, 0.65, 0.8111, 1.0, 1.3]:
        c, Mc, F = etat(s8=s8)
        print(f"  sigma8 = {s8:5.3f} -> M_cut = {Mc:.3e}  F = {F:.4e}  F/F0 = {F/F0:.3g}")
    print()
    for ns in [0.85, 0.92, 0.9649, 1.00, 1.05]:
        c, Mc, F = etat(ns=ns)
        print(f"  n_s = {ns:5.3f} -> M_cut = {Mc:.3e}  F = {F:.4e}  F/F0 = {F/F0:.3g}")
