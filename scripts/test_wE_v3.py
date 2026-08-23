#!/usr/bin/env python3
"""
test_wE_v2.py — LE TEST, VERSION DIMENSIONNEE.

Le test precedent etait sous-dimensionne : je ne reproduisais pas l'exclusion de w_E = 0
publiee par Schiavone et al. (4,7 sigma dans PC1) meme dans LEUR famille (j'obtenais 0,03).
Diagnostic pose : mon profilage analytique de q = c/(H0 r_d) marginalisait exactement
l'information qui contraint w_E chez eux — le prior SH0ES sur H0 et omega_m du CMB.

CORRECTION : q est DE-PROFILE. r_d est calcule par CAMB (arriere-plan seul, exact a 0,01 %
contre Planck 2018 : 147,103 contre 147,09) sur une grille (omega_b, omega_m) interpolee.
Parametres libres : h, omega_b, Omega_m, + parametres de taux, + w_E.

DONNEES (protocole de Schiavone et al., a une exception declaree pres) :
  - Pantheon+ : 1580 SNe, covariance complete, M marginalise analytiquement
  - DESI DR2 BAO : 13 mesures, correlations D_M-D_H
  - CMB comprime : omega_b = 0,02236 +/- 0,00015 ; omega_m = 0,1430 +/- 0,0011 ;
                   D_M(z*)/r_d = 94,31 +/- 0,30   (traites comme independants : approximation
                   declaree, les correlations publiees ne sont pas incluses)
  - SH0ES : H0 = 73,04 +/- 1,04  (leur calibration de Pantheon+, traitee en prior sur H0)
  - EXCEPTION : je n'ai pas les 15 chronometres cosmiques ni leur covariance. Declare.

CRITERE DE VALIDATION PRE-ENREGISTRE (ecrit AVANT execution) — le test ne compte QUE si :
  (V1) LCDM retrouve H0 ~ 68,9 et Omega_m ~ 0,296 (leur table V : 68,85 +/- 0,43 ; 0,296)
  (V2) PC1 exclut w_E = 0 a AU MOINS 3 sigma (ils publient 4,7). Si j'obtiens moins,
       le pipeline reste sous-dimensionne et je l'ecris ainsi SANS exploiter le resultat
       sur notre propre loi de taux.
CRITERE DE LECTURE, si et seulement si V1 et V2 passent :
  - Dchi2(w_E = 0) > 9 pour Gamma ∝ 1/t  -> DEFAITE, ecrite comme telle.
  - Dchi2 < 1 -> l'exclusion publiee est bien un artefact de loi de taux. Resultat.
  - entre les deux -> ambigu, ecrit comme ambigu.
VERSION 3 (20/08, nuit) : le CMB comprime est remplace par les VRAIS distance-priors
Planck 2018 TT,TE,EE+lowE+lensing avec COVARIANCE COMPLETE (R, l_A, omega_b),
valeurs et matrice de arXiv:2405.06618 annexe E, coherentes avec Chen-Huang-Wang
(JCAP 02 (2019) 028, arXiv:1808.05724 : R=1,7502+/-0,0046 ; l_A=301,471+/-0,090 ;
omega_b=0,02236+/-0,00015 ; correlations 0,46 / -0,66 / -0,33).
Motif : l_A est mesure a 0,03 %, contre 0,32 % pour le D_M(z*)/r_d que j'utilisais.
"""
import numpy as np, sys
from scipy.optimize import minimize
from scipy.interpolate import RectBivariateSpline
sys.path.insert(0, '/home/claude/desi_fit')
import vraisemblance_reelle as V

C_KM = 299792.458
ZSTAR = 1089.91
# distance-priors Planck 2018 TT,TE,EE+lowE+lensing : v = (R, l_A, omega_b)
DP_V = np.array([1.74963, 301.80845, 0.02237])
DP_C = 1e-8*np.array([[1598.9554,   17112.007,  -36.311179],
                      [17112.007,   811208.45, -494.79813 ],
                      [ -36.311179, -494.79813,   2.1242182]])
DP_CI = np.linalg.inv(DP_C)
H0_SH, H0_SH_S = 73.04, 1.04

zg = np.concatenate([np.linspace(0.0, 2.6, 6000), np.linspace(2.6005, 1200, 4000)])
AG = np.logspace(-7, 0, 12000)

# ---------- r_d(omega_b, omega_m) par CAMB, tabule une fois ----------
def build_rd():
    import camb
    obs = np.linspace(0.0215, 0.0232, 7)
    oms = np.linspace(0.132, 0.155, 9)
    R = np.zeros((len(obs), len(oms), 3))
    for i, ob in enumerate(obs):
        for j, om in enumerate(oms):
            och2 = om - ob - 0.00064          # omega_nu pour mnu = 0,06 eV
            p = camb.set_params(H0=67.5, ombh2=ob, omch2=och2, mnu=0.06, tau=0.054,
                                As=2.1e-9, ns=0.965)
            d = camb.get_background(p).get_derived_params()
            R[i, j, 0] = d['rdrag']; R[i, j, 1] = d['rstar']; R[i, j, 2] = d['zstar']
    return [RectBivariateSpline(obs, oms, R[:, :, k], kx=3, ky=3) for k in range(3)]
_SP = build_rd()
def r_drag(ob, om): return float(_SP[0](ob, om)[0, 0])
def r_star(ob, om): return float(_SP[1](ob, om)[0, 0])
def z_star(ob, om): return float(_SP[2](ob, om)[0, 0])

# ---------- fond ----------
ZCUT = 3.0        # leur protocole : g(z>ZCUT) = 1 (LCDM impose). None = desactive.

def fond(Om, wE, par, famille, n_iter=7):
    """E(z) auto-coherent. par : beta (invt) | gamma (PC3) | (b, alpha) (PC1)."""
    Or = Om/3388.0; Ode = 1-Om-Or
    a = AG; lna = np.log(a)
    E2 = Om/a**3 + Or/a**4 + Ode
    for _ in range(n_iter):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        if famille == 'lcdm':
            g = np.ones_like(a)
            E2 = Om/a**3 + Or/a**4 + Ode*g
            continue
        if famille == 'invt':
            integ = 1/(a*E)
            t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])
            G3H = par/(3*np.clip(E*t, 1e-12, None))
        elif famille == 'PC3':
            G3H = par/E
        elif famille == 'PC1':
            b, al = par; G3H = b*E**(al-1)
        else: raise ValueError(famille)
        dlng = -3*(1+wE)*(1-G3H)
        if ZCUT is not None:
            dlng = np.where(a < 1.0/(1.0+ZCUT), 0.0, dlng)   # gel de g au-dela de ZCUT
        I = np.concatenate([[0], np.cumsum(0.5*(dlng[1:]+dlng[:-1])*np.diff(lna))])
        g = np.exp(np.clip(I - I[-1], -700, 700))
        if ZCUT is not None:
            g = np.where(a < 1.0/(1.0+ZCUT), 1.0, g)         # LCDM exact au-dela
        E2 = Om/a**3 + Or/a**4 + Ode*g
    E = np.sqrt(np.clip(E2, 1e-30, None))
    return (1/a - 1)[::-1], E[::-1]

def chi2(h, ob, Om, wE, par, famille):
    if not (0.55 < h < 0.85 and 0.0200 < ob < 0.0245 and 0.15 < Om < 0.55): return 1e9
    om = Om*h*h
    if not (0.132 < om < 0.155): return 1e9
    try: zz, Ea = fond(Om, wE, par, famille)
    except Exception: return 1e9
    Ez = np.interp(zg, zz, Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return 1e9
    inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])   # en c/H0
    DH0 = C_KM/(100*h)                                                          # Mpc
    rd = r_drag(ob, om)
    # SNe : M marginalise -> seule la forme compte
    mu = 5*np.log10((1+V.z_sn)*np.interp(V.z_sn, zg, Dc))
    r = V.mb - mu
    c_sn = r@V.Cinv_sn@r - (r@V.Cinv_one)**2/V.oCo
    # BAO : plus de profilage, r_d predit
    u = np.zeros(13)
    for i, (z, typ, _, _, _) in enumerate(V.BAO):
        DM_ = np.interp(z, zg, Dc)*DH0; DH_ = DH0/np.interp(z, zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]/rd
    rb = V.d_bao - u
    c_bao = rb@V.Cinv_bao@rb
    # distance-priors CMB (R, l_A, omega_b) avec covariance + SH0ES
    zs = z_star(ob, om); rs = r_star(ob, om)
    Dc_star = np.interp(zs, zg, Dc)                 # sans dimension (c/H0)
    Rth = np.sqrt(Om)*Dc_star
    lAth = np.pi*Dc_star*DH0/rs
    dv = np.array([Rth, lAth, ob]) - DP_V
    c_cmb = dv@DP_CI@dv
    c_h0 = ((100*h - H0_SH)/H0_SH_S)**2
    return c_sn + c_bao + c_cmb + c_h0

def fit(famille, wE=None, npar=0, depart=None):
    def f(p):
        w = wE if wE is not None else p[3]
        k = 3 + (wE is None)
        par = None if npar == 0 else (p[k] if npar == 1 else tuple(p[k:k+2]))
        if npar == 1 and not (0.0 <= p[k] < 14): return 1e9
        if npar == 2 and not (0.0 <= p[k] < 8 and -3 < p[k+1] < 9): return 1e9
        return chi2(p[0], p[1], p[2], w, par, famille)
    best = None
    for d in (depart or [[]]):
        p0 = [0.690, 0.02236, 0.300] + ([-0.5] if wE is None else []) + list(d)
        for _ in range(3):
            r = minimize(f, p0, method='Nelder-Mead',
                         options=dict(xatol=1e-5, fatol=1e-4, maxiter=6000, maxfev=6000))
            p0 = r.x
        if best is None or r.fun < best.fun: best = r
    return best

if __name__ == '__main__':
    np.seterr(all='ignore')
    print("="*80); print("  CONTROLE r_d"); print("="*80)
    print(f"  r_d(0.02237, 0.1430) = {r_drag(0.02237, 0.1430):.3f} Mpc   (Planck 2018 : 147,09)")

    print("\n" + "="*80)
    print("  V1 : LCDM retrouve-t-il leurs valeurs ? (leur table V : H0=68,85+/-0,43 ; Om=0,296)")
    print("="*80)
    rl = fit('lcdm')
    h, ob, Om = rl.x[:3]
    print(f"  LCDM : H0 = {100*h:.2f}   omega_b = {ob:.5f}   Omega_m = {Om:.4f}"
          f"   omega_m = {Om*h*h:.4f}   chi2 = {rl.fun:.3f}")
    v1 = abs(100*h - 68.85) < 1.5 and abs(Om - 0.296) < 0.020
    print(f"  V1 : {'PASSE' if v1 else 'ECHEC'}")

    print("\n" + "="*80)
    print("  V2 : PC1 exclut-il w_E = 0 a au moins 3 sigma ? (ils publient 4,7)")
    print("="*80)
    dep1 = [[0.62, 2.1], [0.9, 1.3], [0.3, 4.0]]
    out1 = []
    for w in [-1.5, -1.2, -0.98, -0.7, -0.4, -0.2, 0.0]:
        rr = fit('PC1', wE=w, npar=2, depart=dep1)
        out1.append((w, rr.fun, rr.x))
        print(f"    w_E = {w:>6.2f} : chi2 = {rr.fun:10.3f}  H0 = {100*rr.x[0]:.2f}"
              f"  Om = {rr.x[2]:.4f}  b = {rr.x[3]:.3f}  alpha = {rr.x[4]:.3f}")
    c1 = min(o[1] for o in out1)
    d1 = [o[1] for o in out1 if o[0] == 0.0][0] - c1
    print(f"  Dchi2(w_E=0) dans PC1 = {d1:.2f}  ->  {np.sqrt(max(d1,0)):.2f} sigma"
          f"   (publie : 4,7)")
    v2 = d1 > 9
    print(f"  V2 : {'PASSE' if v2 else 'ECHEC'}")

    print("\n" + "="*80)
    print("  NOTRE LOI : Gamma ∝ 1/t, profil en w_E")
    print("="*80)
    dep2 = [[2.4], [1.6], [3.4]]
    out2 = []
    for w in [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2]:
        rr = fit('invt', wE=w, npar=1, depart=dep2)
        b = rr.x[3]/(1+w) if abs(1+w) > 1e-6 else np.inf
        out2.append((w, rr.fun, b, rr.x))
        print(f"    w_E = {w:>6.2f} : chi2 = {rr.fun:10.3f}  H0 = {100*rr.x[0]:.2f}"
              f"  Om = {rr.x[2]:.4f}  B = {rr.x[3]:.3f}  beta = {b:.3f}")
    inst = [o[0] for o in out2 if not (1.5 <= o[2] <= 4.35)]
    if inst: print(f"    INSTABILITE signalee (controle : beta hors [1,5 ; 4,35]) a w_E = {inst} -> "
                   "la parametrisation en w_E degenere vers w_E = -1 ; seul w_E >= -0,4 est lu.")
    c2 = min(o[1] for o in out2)
    d2 = [o[1] for o in out2 if o[0] == 0.0][0] - c2
    b0 = [o[2] for o in out2 if o[0] == 0.0][0]

    print("\n" + "="*80); print("  VERDICT"); print("="*80)
    print(f"  V1 {'PASSE' if v1 else 'ECHEC'} | V2 {'PASSE' if v2 else 'ECHEC'}")
    if not (v1 and v2):
        print("  => pipeline TOUJOURS sous-dimensionne (ou biaise). Le resultat sur notre loi")
        print("     de taux N'EST PAS EXPLOITABLE. Ecrire l'echec, ne pas exploiter le chiffre.")
    else:
        print(f"  Dchi2(w_E = 0) pour Gamma ∝ 1/t = {d2:.2f}  ->  {np.sqrt(max(d2,0)):.2f} sigma")
        print(f"  beta(w_E=0) = {b0:.3f} -> {'dans la bande GSL' if 1.5<=b0<=4.35 else 'HORS BANDE'}")
        if d2 > 9:   print("  DEFAITE : w_E = 0 defavorise a plus de 3 sigma.")
        elif d2 < 1: print("  RESULTAT : l'exclusion publiee est un artefact de loi de taux.")
        else:        print("  AMBIGU. Ecrit tel quel.")
    print(f"\n  [pour information, non exploitable si V2 echoue] Dchi2(w_E=0 | invt) = {d2:.2f}")
