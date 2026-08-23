#!/usr/bin/env python3
"""
duel_ccbh.py — Le duel frontal, sur données identiques.

RIVAL IMPLEMENTE D'APRES LEURS EQUATIONS (Croker et al., JCAP 10 (2024) 094, arXiv:2405.12282,
section 2), lues et non reconstruites :
    rho_b = C w_b^proj/a^3            pour a < a_i
    rho_b = C w_b^proj/a^3 - (Xi/a^3) int_{a_i}^a psi da'/(H a')   pour a >= a_i     (2.2)
    d rho_DE/da = Xi psi /(H a^4),  avec w := -1                                     (2.5)
    rho_DE(a <= a_i) := 0
    H^2 = (8 pi G/3)[rho_b + rho_gamma + rho_nu + rho_DE + rho_c]                    (2.6)
=> H0 n'est PAS un parametre libre : il est DERIVE de la fermeture. C'est leur argument
   central (« meme chi2 que LCDM, deux parametres de moins que w0wa »).

psi : taux de formation stellaire comobile. J'utilise Madau & Dickinson 2014, qu'ils
designent eux-memes comme leur reference fiducielle (« Madau psi ») :
    psi(z) = 0.015 (1+z)^2.7 / [1 + ((1+z)/2.9)^5.6]   Msun/an/Mpc^3
Leur analyse principale utilise « Trinca psi » (plus de formation a z>4, informe par JWST) ;
je ne l'ai pas, et je le declare : mon CCBH est donc leur variante fiducielle, pas leur
variante principale.

DONNEES : identiques pour les trois modeles — Pantheon+ (1580 SNe, cov complete, M marginalise),
DESI DR2 BAO (13 points), distance-priors Planck 2018 (R, l_A, omega_b) avec covariance,
prior SH0ES. C'est le pipeline v3 deja valide sur LCDM (H0 = 68,66 ; Om = 0,2976).

CRITERE PRE-ENREGISTRE (avant execution) :
  - controle de sanite : le Xi ajuste doit etre du meme ordre que leur 1,40. Sinon mes
    unites sont fausses et je ne publie aucun chiffre.
  - comparaison par AIC, k compte les parametres libres REELLEMENT ajustes.
  - si CCBH bat le modele d'accretion, on l'ecrit. Pas de reinterpretation.
"""
import numpy as np, sys
from scipy.optimize import minimize
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
import vraisemblance_reelle as V
import test_wE_v3 as T

np.seterr(all='ignore')
C_KM = 299792.458
RHO100 = 2.775e11          # Msun/Mpc^3, densite critique pour H = 100 km/s/Mpc
KMS_PER_YR = 1.02271e-12   # 1 km/s/Mpc en 1/an
W_GAMMA = 2.47e-5
W_R = W_GAMMA*(1 + 0.2271*3.044)      # photons + neutrinos sans masse
W_NU_M = 0.06/93.14                    # un neutrino massif, compte en matiere
ZI = 20.0                              # premiere lumiere ; sensibilite testee

def psi_MD14(z):
    return 0.015*(1+z)**2.7/(1 + ((1+z)/2.9)**5.6)

AG = np.logspace(-7, 0, 30000)

def fond_ccbh(wc, wb_proj, Xi, ai=None):
    """Integre le systeme (2.7). Retourne z, E-equivalent, h derive, w_b(1)."""
    if ai is None: ai = 1/(1+ZI)   # resolu a l'appel : ZI peut etre modifie (test de sensibilite)
    a = AG
    wb = np.full_like(a, wb_proj)      # densite comobile de baryons
    wde = np.zeros_like(a)
    # integration avant en a, a partir de ai
    j0 = np.searchsorted(a, ai)
    for i in range(j0, len(a)):
        wm = wc + wb[i-1] + W_NU_M
        wtot = wm/a[i-1]**3 + W_R/a[i-1]**4 + wde[i-1]
        if wtot <= 0: return None
        H_yr = 100*np.sqrt(wtot)*KMS_PER_YR
        z = 1/a[i-1] - 1
        src = Xi*psi_MD14(z)/(H_yr*a[i-1]**4)/RHO100      # d w_DE/da
        da = a[i]-a[i-1]
        wde[i] = wde[i-1] + src*da
        wb[i] = wb[i-1] - src*a[i-1]**3*da
        if wb[i] <= 0: return None
    wm = wc + wb + W_NU_M
    wtot = wm/a**3 + W_R/a**4 + wde
    h2 = wtot[-1]
    if h2 <= 0: return None
    E = np.sqrt(wtot/h2)
    return (1/a - 1)[::-1], E[::-1], np.sqrt(h2), wb[-1]

def chi2_ccbh(wc, wb_proj, Xi):
    if not (0.05 < wc < 0.35 and 0.019 < wb_proj < 0.026 and 0.0 < Xi < 20): return 1e9
    out = fond_ccbh(wc, wb_proj, Xi)
    if out is None: return 1e9
    zz, Ea, h, wb1 = out
    if not (0.55 < h < 0.85): return 1e9
    Ez = np.interp(T.zg, zz, Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return 1e9
    inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(T.zg))])
    DH0 = C_KM/(100*h)
    om_early = wc + wb_proj + W_NU_M          # matiere au decouplage
    rd = T.r_drag(wb_proj, om_early); rs = T.r_star(wb_proj, om_early)
    zs = T.z_star(wb_proj, om_early)
    mu = 5*np.log10((1+V.z_sn)*np.interp(V.z_sn, T.zg, Dc))
    r = V.mb - mu
    c_sn = r@V.Cinv_sn@r - (r@V.Cinv_one)**2/V.oCo
    u = np.zeros(13)
    for i, (z, typ, _, _, _) in enumerate(V.BAO):
        DM_ = np.interp(z, T.zg, Dc)*DH0; DH_ = DH0/np.interp(z, T.zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]/rd
    rb = V.d_bao - u
    c_bao = rb@V.Cinv_bao@rb
    Dcs = np.interp(zs, T.zg, Dc)
    Om_eff = om_early/h**2
    dv = np.array([np.sqrt(Om_eff)*Dcs, np.pi*Dcs*DH0/rs, wb_proj]) - T.DP_V
    c_cmb = dv@T.DP_CI@dv
    c_h0 = ((100*h - T.H0_SH)/T.H0_SH_S)**2
    return c_sn + c_bao + c_cmb + c_h0

if __name__ == '__main__':
    print("="*76); print("  CONTROLE DE SANITE : mes unites donnent-elles leur Xi ~ 1,4 ?"); print("="*76)
    for Xi in [0.5, 1.0, 1.4, 2.0, 3.0]:
        o = fond_ccbh(0.1237, 0.02238, Xi)
        if o is None: print(f"    Xi={Xi}: echec"); continue
        zz, Ea, h, wb1 = o
        s = wb1/0.02238
        print(f"    Xi = {Xi:.2f} -> H0 = {100*h:.2f}, survie baryonique s = {s:.3f}"
              f"   (eux : Xi=1,403 -> H0=69,94, s~0,70)")

    print("\n" + "="*76); print("  AJUSTEMENTS, DONNEES IDENTIQUES"); print("="*76)
    T.ZCUT = None
    res = {}
    rl = T.fit('lcdm'); res['LCDM'] = (rl.fun, 3, f"H0={100*rl.x[0]:.2f} Om={rl.x[2]:.4f}")
    r0 = T.fit('invt', wE=0.0, npar=1, depart=[[2.4],[1.6],[3.4]])
    res['ACCRETION (Gamma∝1/t)'] = (r0.fun, 4, f"H0={100*r0.x[0]:.2f} Om={r0.x[2]:.4f} beta={r0.x[3]:.3f}")
    best = None
    for s0 in ([0.1237, 0.02238, 1.40], [0.115, 0.0224, 2.0], [0.130, 0.0222, 0.9]):
        rr = minimize(lambda p: chi2_ccbh(*p), s0, method='Nelder-Mead',
                      options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000))
        if best is None or rr.fun < best.fun: best = rr
    o = fond_ccbh(*best.x)
    hcc = o[2] if o else np.nan
    # CONTROLE DE SANITE (critere gele) : le Xi ajuste doit etre du meme ordre que leur 1,40.
    sanite = 0.5 < best.x[2]/1.403 < 2.0
    print(f"\n  CONTROLE DE SANITE : Xi ajuste = {best.x[2]:.3f} contre leur 1,403 -> "
          + ("OK" if sanite else "ECHEC : taux NON CALIBRE (le CCBH publie, papier C, est la version "
             "calibree A=1,551 B=3,119 de atlas_rivaux.py : Xi=1,382, chi2=1420,31)"))
    res['CCBH (Madau psi)'] = (best.fun, 3,
        f"H0={100*hcc:.2f} (derive) wc={best.x[0]:.4f} Xi={best.x[2]:.3f}")
    base = min(c+2*k for c, k, _ in res.values())
    print(f"  {'modele':>24s} {'k':>2s} {'chi2':>10s} {'AIC':>10s} {'dAIC':>7s}   parametres")
    for n, (c, k, d) in sorted(res.items(), key=lambda kv: kv[1][0]+2*kv[1][1]):
        print(f"  {n:>24s} {k:>2d} {c:>10.3f} {c+2*k:>10.3f} {c+2*k-base:>+7.3f}   {d}")

    print("\n  SENSIBILITE de CCBH a l'epoque de premiere lumiere z_i :")
    print("    (a) a (wc, wb, Xi) FIXES au fit z_i=20 ; (b) REAJUSTES a chaque z_i (regle 5 :"
          " ce que le rival a le droit de reajuster, on le lui accorde)")
    for zi in [10.0, 20.0, 30.0]:
        globals()['ZI'] = zi
        c = chi2_ccbh(*best.x); o = fond_ccbh(*best.x); h_fixe = 100*o[2] if o else np.nan
        rr = minimize(lambda p: chi2_ccbh(*p), best.x, method='Nelder-Mead',
                      options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000))
        o2 = fond_ccbh(*rr.x); h_re = 100*o2[2] if o2 else np.nan
        print(f"    z_i = {zi:>4.0f} -> (a) fixes : chi2 = {c:.3f}, H0 = {h_fixe:.2f}   "
              f"(b) reajustes : chi2 = {rr.fun:.3f}, H0 = {h_re:.2f}, Xi = {rr.x[2]:.3f}")
    globals()['ZI'] = 20.0
