#!/usr/bin/env python3
"""
atlas_rivaux.py — La comparaison multi-modeles, un seul pipeline, cinq familles.

DONNEES IDENTIQUES pour tous : Pantheon+ (1580 SNe, cov complete, M marginalise),
DESI DR2 BAO (13 pts), distance-priors Planck 2018 (R, l_A, omega_b) avec covariance,
prior SH0ES. Pipeline v3, valide sur LCDM (H0 = 68,66 ; Om = 0,2976).

FAMILLES, avec ce que chacune apporte :
  LCDM                     k=3   reference
  Lombriser                k=2   LCDM avec Omega_de PREDIT = 0,697 (sequestration dans les
                                 structures effondrees) : zero parametre d energie noire
  accretion Gamma ∝ 1/t    k=4   notre modele
  CCBH                     k=3   trous noirs couples, H0 derive (Croker et al. 2024)
  CPL / IDE degeneree      k=5   arXiv:2508.17955 est construit EXACTEMENT degenere avec CPL
                                 au niveau du fond : ajuster CPL, c est ajuster ce rival
  PC1 (creation)           k=6   Gamma = 3 b H0 E^alpha, w_E libre
  Anton-Schmidt            k=5   P = A (rho/rho_*)^-n ln(rho/rho_*)  [forme publiee]
                                 -> rho_de(a) ∝ a^{3n}[(L0 - 3 ln a)/(n+1) + 1/(n+1)^2]
                                 VARIANTE SECTEUR SOMBRE SEUL, declaree : leur traitement
                                 unifie (un seul fluide) n est pas reproduit ici.

CRITERE PRE-ENREGISTRE : classement par AIC, ecrit tel quel. Aucun modele n est retire
du tableau parce qu il nous depasse. Les k sont comptes de la meme facon pour tous
(parametres reellement ajustes sur CES donnees).
"""
import numpy as np, sys
from scipy.optimize import minimize
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
import test_wE_v3 as T, duel_ccbh as D
np.seterr(all='ignore')
T.ZCUT = None
AG = np.logspace(-7, 0, 12000)

def fond_gen(Om, rho_de_of_a):
    """E(z) pour une densite d energie noire donnee (normalisee a 1 en a=1)."""
    Or = Om/3388.0; Ode = 1-Om-Or
    g = rho_de_of_a(AG)
    if g is None or not np.all(np.isfinite(g)) or np.any(g < 0): return None
    E2 = Om/AG**3 + Or/AG**4 + Ode*g
    if np.any(E2 <= 0): return None
    return (1/AG-1)[::-1], np.sqrt(E2)[::-1]

def g_cpl(w0, wa):
    return lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))

def g_as(n, L0):
    def f(a):
        num = (L0 - 3*np.log(a))/(n+1) + 1/(n+1)**2
        den = L0/(n+1) + 1/(n+1)**2
        if den <= 0: return None
        v = a**(3*n)*num/den
        return np.where(num > 0, v, np.nan)
    return f

_fond = T.fond
def fond_patch(Om, wE, par, famille, n_iter=7):
    if famille == 'cpl':  return fond_gen(Om, g_cpl(*par))
    if famille == 'as':   return fond_gen(Om, g_as(*par))
    if famille == 'lomb': return fond_gen(Om, lambda a: np.ones_like(a))
    return _fond(Om, wE, par, famille, n_iter)
T.fond = fond_patch

def chi2(p, fam, npar):
    h, ob, Om = p[0], p[1], p[2]
    par = None if npar == 0 else (p[3] if npar == 1 else tuple(p[3:3+npar]))
    return T.chi2(h, ob, Om, 0.0, par, fam)

def fit(fam, npar, starts, fixOm=None):
    def f(p):
        q = list(p)
        if fixOm is not None: q.insert(2, fixOm)
        if fam == 'as' and not (-1.0 < q[4] < 5.0 and abs(q[3]+1) > 1e-3): return 1e9
        if fam == 'cpl' and not (-3 < q[3] < 1 and -6 < q[4] < 4): return 1e9
        c = chi2(q, fam, npar)
        return c if np.isfinite(c) else 1e9
    best = None
    for s in starts:
        s2 = list(s)
        if fixOm is not None: s2.pop(2)
        r = minimize(f, s2, method='Nelder-Mead',
                     options=dict(xatol=1e-6, fatol=1e-4, maxiter=6000, maxfev=6000))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == '__main__':
    res = {}
    r = T.fit('lcdm'); res['LCDM'] = (r.fun, 3, f"H0={100*r.x[0]:.2f} Om={r.x[2]:.4f}")
    # Lombriser : Omega_de = 0.697 predit -> Om fixe par platitude
    Om_l = 1-0.697-0.0
    b = fit('lomb', 0, [[0.69, 0.02236, Om_l]], fixOm=Om_l)
    res['Lombriser (Om_de predit)'] = (b.fun, 2, f"H0={100*b.x[0]:.2f} Om={Om_l:.4f} (impose)")
    r0 = T.fit('invt', wE=0.0, npar=1, depart=[[2.4],[1.6],[3.4]])
    res['ACCRETION (Gamma∝1/t)'] = (r0.fun, 4, f"H0={100*r0.x[0]:.2f} beta={r0.x[3]:.3f}")
    PSI0 = lambda z: 0.015*(1+z)**2.7/(1+((1+z)/2.9)**5.6)
    D.psi_MD14 = lambda z: 1.551*PSI0(z)*np.where(np.asarray(z) > 4.0, 3.119, 1.0)
    bb = None
    for s0 in ([0.1237, 0.02238, 1.40], [0.119, 0.0224, 1.0]):
        rr = minimize(lambda p: D.chi2_ccbh(*p), s0, method='Nelder-Mead',
                      options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000))
        if bb is None or rr.fun < bb.fun: bb = rr
    oc = D.fond_ccbh(*bb.x)
    res['CCBH (Croker et al.)'] = (bb.fun, 3, f"H0={100*oc[2]:.2f} (derive) Xi={bb.x[2]:.3f}")
    bc = fit('cpl', 2, [[0.69, 0.02236, 0.31, -0.85, -0.6], [0.69, 0.02236, 0.32, -0.9, -0.3]])
    res['CPL = IDE degeneree'] = (bc.fun, 5, f"H0={100*bc.x[0]:.2f} w0={bc.x[3]:.3f} wa={bc.x[4]:.3f}")
    rp = T.fit('PC1', wE=None, npar=2, depart=[[0.62, 2.1], [0.9, 1.3]])
    res['PC1 (creation, w_E libre)'] = (rp.fun, 6, f"H0={100*rp.x[0]:.2f} b={rp.x[4]:.3f}")
    ba = fit('as', 2, [[0.69, 0.02236, 0.31, 0.0, 1.0], [0.69, 0.02236, 0.31, -0.3, 3.0],
                       [0.69, 0.02236, 0.30, 0.2, 0.5]])
    res['Anton-Schmidt'] = (ba.fun, 5, f"H0={100*ba.x[0]:.2f} n={ba.x[3]:.3f} L0={ba.x[4]:.3f}")

    base = min(c+2*k for c, k, _ in res.values())
    print("="*92)
    print("  ATLAS DES RIVAUX — donnees identiques, pipeline unique, classement par AIC")
    print("="*92)
    print(f"  {'modele':>28s} {'k':>2s} {'chi2':>10s} {'AIC':>10s} {'dAIC':>7s}   parametres")
    for n_, (c, k, d) in sorted(res.items(), key=lambda kv: kv[1][0]+2*kv[1][1]):
        print(f"  {n_:>28s} {k:>2d} {c:>10.3f} {c+2*k:>10.3f} {c+2*k-base:>+7.3f}   {d}")
    print("\n  Lecture : dAIC < 2 = indiscernable ; 2-7 = preference faible ; > 10 = forte.")
