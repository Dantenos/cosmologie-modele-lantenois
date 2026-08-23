#!/usr/bin/env python3
"""
test_wE.py — LE TEST EXTERNE : Gamma ∝ 1/t avec w_E LIBRE.

CONTEXTE. Schiavone et al. (arXiv:2601.14222, PRD 2026) excluent la creation de matiere
sans pression (w_E = 0) a 4,7-5,6 sigma DANS LEURS familles de taux (Gamma ∝ H^alpha,
∝ H, constant, somme). Notre modele EST w_E = 0, mais avec Gamma = Mdot/M = beta/t,
une cinquieme famille absente de leur tableau. Question : l'exclusion nous atteint-elle ?

FORMALISME (leur eq. 19) : g'(z) = 3(1+w_E)/(1+z) [1 - Gamma/(3H)] g(z), g(0)=1.
Avec Gamma = beta/t, l'integration donne analytiquement
        g(z) = (1+z)^{3(1+w_E)} (t/t0)^{beta(1+w_E)}
verifiee ci-dessous contre l'integration numerique de leur EDO. Pour w_E = 0 on retombe
sur rho_de ∝ t^beta / a^3, notre modele. Le couple (w_E, beta) est donc une extension a
DEUX parametres de notre modele a un parametre.

CRITERES PRE-ENREGISTRES (ecrits AVANT execution, 20/08) :
  - Si w_E = 0 est defavorise de Dchi2 > 9 (3 sigma, 1 ddl) par rapport au meilleur w_E :
    l'hypothese centrale du modele (masse accretee = sans pression) est en difficulte.
    On l'ecrit comme une DEFAITE, sans reinterpretation.
  - Si Dchi2 < 1 : w_E = 0 est compatible ; les exclusions publiees a 4,7-5,6 sigma sont
    alors un artefact de loi de taux, et c'est un resultat publiable.
  - Entre 1 et 9 : AMBIGU. On l'ecrit comme ambigu. Pas de conversion narrative.
  - Controle de sanite : le beta ajuste doit rester dans [1,5 ; 4,35] (bande GSL), sinon
    signaler l'instabilite.

DONNEES : Pantheon+ (1580 SNe, cov complete, M marginalise) + DESI DR2 BAO (13 pts,
correlations DM-DH) + le CMB traite comme un point BAO a z* (leur protocole exact).
q = c/(H0 rd) profile analytiquement.
"""
import numpy as np
from scipy.optimize import minimize
import sys
import vraisemblance_reelle as V

ZEQ = 3387.0
DECOMPOSE = False
ZSTAR = 1089.9
# CMB comprime traite en point BAO : D_M(z*)/r_d.
# theta* = 1.04109e-2 (Planck 2018) -> D_M/r_s* = 1/theta* = 96.05
# r_d/r_s* = 147.09/144.43 = 1.0184  ->  D_M(z*)/r_d = 94.31
DM_STAR, SIG_STAR = 94.31, 0.30

zg = np.concatenate([np.linspace(0.0, 2.6, 6000), np.linspace(2.6005, 1200, 3000)])

def fond(Om, wE, B, n_iter=6):
    """E(z) et H0*t(z) auto-coherents pour g = (1+z)^{3(1+wE)} (t/t0)^{B}.
       B = beta*(1+wE) est le parametre naturel ; beta = B/(1+wE)."""
    Or = Om/(1+ZEQ); Ode = 1-Om-Or
    a = np.logspace(-7, 0, 20000)
    zz = 1/a - 1
    E2 = Om/a**3 + Or/a**4 + Ode          # depart LCDM
    for _ in range(n_iter):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        integ = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])
        tn = t/t[-1]                       # t/t0
        g = (1/a)**(3*(1+wE)) * np.clip(tn, 1e-300, None)**B
        E2 = Om/a**3 + Or/a**4 + Ode*g
    E = np.sqrt(np.clip(E2, 1e-30, None))
    return zz[::-1], E[::-1], (t/t[-1])[::-1], t[-1]   # tries en z croissant

def E_of_z(Om, wE, B):
    zz, E, tn, _ = fond(Om, wE, B)
    return np.interp(zg, zz, E)

def chi2(Om, wE, B, use_cmb=True):
    if not (0.05 < Om < 0.7): return 1e9
    Ez = E_of_z(Om, wE, B)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return 1e9
    inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])
    # --- SNe : M marginalise analytiquement ---
    mu = 5*np.log10((1+V.z_sn)*np.interp(V.z_sn, zg, Dc))
    r = V.mb - mu
    A = r@V.Cinv_sn@r; Bl = r@V.Cinv_one
    chi2_sn = A - Bl*Bl/V.oCo
    # --- BAO (+ CMB comme point BAO) : q = c/(H0 rd) profile ---
    n = 13 + (1 if use_cmb else 0)
    u = np.zeros(n); d = np.zeros(n); C = np.zeros((n, n))
    for i, (z, typ, val, sig, _) in enumerate(V.BAO):
        DM_ = np.interp(z, zg, Dc); DH_ = 1/np.interp(z, zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]
    d[:13] = V.d_bao; C[:13, :13] = V.C_bao
    if use_cmb:
        u[13] = np.interp(ZSTAR, zg, Dc); d[13] = DM_STAR; C[13, 13] = SIG_STAR**2
    Ci = np.linalg.inv(C)
    q = (u@Ci@d)/(u@Ci@u)
    rb = d - q*u
    if DECOMPOSE: return chi2_sn, rb@Ci@rb
    return chi2_sn + rb@Ci@rb

def fit(wE=None, B=None, use_cmb=True, starts=None):
    """Minimise sur les parametres libres. wE/B fixes si fournis."""
    libres = [n for n, v in (('wE', wE), ('B', B)) if v is None]
    def f(p):
        i = 0
        w = wE if wE is not None else p[1+i]; i += (wE is None)
        b = B if B is not None else p[1+i]
        bb = b if B is None else B
        if not (-1e-9 <= bb < 12): return 1e9
        return chi2(p[0], w, b)
    starts = starts or [[0.31, 2.4], [0.30, 1.5], [0.33, 3.2]]
    best = None
    for s in starts:
        p0 = [s[0]] + ([-0.5] if wE is None else []) + ([s[1]] if B is None else [])
        r = minimize(f, p0, method='Nelder-Mead',
                     options=dict(xatol=1e-4, fatol=1e-3, maxiter=3000))
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == '__main__':
    np.seterr(all='ignore')
    print("="*80)
    print("  CONTROLE 0 : la solution analytique reproduit-elle leur EDO ?")
    print("="*80)
    Om, wE, B = 0.315, -0.4, 1.5
    zz, E, tn, _ = fond(Om, wE, B)
    g_ana = (1+zz)**(3*(1+wE)) * np.clip(tn, 1e-300, None)**B
    # integration directe de g' = 3(1+wE)/(1+z) [1 - beta/(3 E H0t)] g depuis z=0
    beta = B/(1+wE)
    m = (zz >= 0) & (zz <= 5)
    zs, Es, ts = zz[m], E[m], tn[m]
    t0H0 = None
    # H0*t(z) : tn * (H0 t0). On recupere H0t0 par la relation t' = -1/((1+z)E)
    dt = np.gradient(ts, zs); H0t0 = np.median(-1/((1+zs)*Es)/np.clip(dt, -1e9, -1e-30))
    Ht = Es*ts*H0t0
    lng = np.log(np.clip(g_ana[m], 1e-300, None))
    lhs = np.gradient(lng, zs)
    rhs = 3*(1+wE)/(1+zs)*(1 - beta/(3*Ht))
    ok = np.nanmax(np.abs(lhs[5:-5]-rhs[5:-5]))
    print(f"  ecart max |dln g/dz - leur second membre| sur 0<z<5 : {ok:.2e}   (H0*t0 = {H0t0:.4f})")

    print("\n" + "="*80)
    print("  AJUSTEMENTS  (Pantheon+ 1580 SNe + DESI DR2 BAO 13 pts + CMB comprime)")
    print("="*80)
    # LCDM = limite wE = -1 (g == 1)
    r_l = fit(wE=-1.0, B=0.0)          # g = (1+z)^0 (t/t0)^0 = 1  <=> LCDM exact
    c_l = r_l.fun
    print(f"  LCDM (wE=-1, B=0)            k=1 : chi2 = {c_l:10.3f}   Om = {r_l.x[0]:.4f}")
    # validation du pipeline contre un resultat connu du corpus (SN+BAO seuls)
    from scipy.optimize import minimize as _m
    l_nc = _m(lambda p_: chi2(p_[0], -1.0, 0.0, use_cmb=False), [0.31],
              method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-4)).fun
    cand = [_m(lambda p_: chi2(p_[0], 0.0, p_[1], use_cmb=False), [0.314, s0],
               method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-4))
            for s0 in (2.0, 2.45, 3.0)]
    a_nc = min(cand, key=lambda r: r.fun)
    print(f"  [VALIDATION SN+BAO seuls, sans CMB] Dchi2(accretion) = {a_nc.fun-l_nc:+.2f}"
          f"  beta = {a_nc.x[1]:.3f}   (corpus : -4.41, beta = 2.45)")
    r_0 = fit(wE=0.0)
    print(f"  NOTRE MODELE (wE=0 impose)   k=2 : chi2 = {r_0.fun:10.3f}   Om = {r_0.x[0]:.4f}"
          f"  beta = {r_0.x[1]:.3f}   Dchi2 = {r_0.fun-c_l:+.3f}")
    r_f = fit()
    wE_b, B_b = r_f.x[1], r_f.x[2]
    beta_b = B_b/(1+wE_b) if abs(1+wE_b) > 1e-6 else np.nan
    print(f"  wE LIBRE                     k=3 : chi2 = {r_f.fun:10.3f}   Om = {r_f.x[0]:.4f}"
          f"  wE = {wE_b:+.3f}  B = {B_b:.3f}  (beta = {beta_b:.3f})   Dchi2 = {r_f.fun-c_l:+.3f}")

    print("\n" + "="*80)
    print("  LE TEST : profil de vraisemblance en w_E  (Om et B reoptimises a chaque point)")
    print("="*80)
    print(f"  {'w_E':>8s} {'chi2':>11s} {'Dchi2 vs meilleur':>19s} {'Om':>7s} {'beta':>8s}")
    grille = [-1.0, -0.8, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.34]
    res = []
    for w in grille:
        rr = fit(wE=w)
        b = rr.x[1]/(1+w) if abs(1+w) > 1e-6 else np.inf
        res.append((w, rr.fun, rr.x[0], b))
    cmin = min(r[1] for r in res)
    for w, c, om, b in res:
        print(f"  {w:>8.2f} {c:>11.3f} {c-cmin:>19.3f} {om:>7.4f} {b:>8.3f}")

    c_wE0 = [r[1] for r in res if r[0] == 0.0][0]
    d = c_wE0 - cmin
    print("\n" + "="*80)
    print("  VERDICT selon les criteres PRE-ENREGISTRES")
    print("="*80)
    print(f"  Dchi2(w_E = 0) par rapport au meilleur w_E = {d:.3f}  ->  {np.sqrt(max(d,0)):.2f} sigma (1 ddl)")
    if d > 9:   verdict = "DEFAITE : w_E = 0 defavorise a plus de 3 sigma."
    elif d < 1: verdict = "w_E = 0 COMPATIBLE : l'exclusion publiee ne se transfere pas."
    else:       verdict = "AMBIGU : ni compatible ni exclu. A ecrire tel quel."
    print(f"  {verdict}")
    bb = [r[3] for r in res if r[0] == 0.0][0]
    print(f"  Controle de sanite : beta(w_E=0) = {bb:.3f} -> "
          f"{'dans la bande GSL [1,5 ; 4,35]' if 1.5 <= bb <= 4.35 else 'HORS BANDE, a signaler'}")
