#!/usr/bin/env python3
"""
frb_likelihood.py — La vraisemblance FRB complete, refittee DANS chaque fond.

CE QUE LES TESTS PRECEDENTS NE FAISAIENT PAS. Jusqu'ici je comparais des DM MOYENNES et
demandais << quel Omega_b un analyste LCDM inferrerait >>. Cela laisse une echappatoire non
testee : la contribution de l'HOTE est un parametre libre, et un deficit cosmique pourrait
etre absorbe en remontant mu_host. Il faut donc refitter f_IGM, f_X, mu_host et sigma_host
SIMULTANEMENT dans chaque fond, comme le fait l'analyse publiee.

JE N'AI PAS LEUR TABLE DE SURSAUTS. Je construis donc un echantillon synthetique et je le
CALIBRE : la vraisemblance doit, ajustee en LCDM, redonner leur posterieure publiee
(f_IGM = 0,80 +0,08/-0,09 ; f_X = 0,11). Si elle ne la redonne pas, je n'exploite rien.
C'est un test de la MACHINERIE d'inference, pas de leurs donnees : la question posee est
<< les nuisances peuvent-elles absorber le deficit CCBH ? >>, et elle ne depend pas des
valeurs particulieres mesurees.

MODELE (leur eq. 1-2) :
  DM_ex = DM_cos(z) + DM_host/(1+z)
  <DM_cos> = 1085 z f_d (Omega_b h70 / 0.04703)  pour z <~ 1, generalise a
             K int_0^z rho_tilde_b(z')(1+z') f_e dz'/E(z')   pour un fond quelconque
  dispersion de ligne de visee : log-normale de largeur F z^-1/2 (Macquart et al.)
  hote : log-normale (mu_host, sigma_host), divisee par (1+z)
  priors : f_IGM, f_X ~ U(0,1) AVEC f_IGM + f_X <= 1   [leur contrainte dure]

CRITERE PRE-ENREGISTRE :
  - VALIDATION : l'ajustement LCDM doit redonner f_IGM = 0,80 +/- 0,10 et f_X < 0,3.
    Sinon rien n'est exploite.
  - Puis : Dchi2 entre fonds, et valeurs de f_IGM/f_X/mu_host preferees en CCBH.
  - Si le CCBH atteint le bord f_IGM + f_X = 1, c'est le signe que le deficit n'est PAS
    absorbable. Si au contraire mu_host monte et Dchi2 reste petit, il l'est, et je l'ecris.
"""
import numpy as np, sys
from scipy.optimize import minimize
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
import duel_ccbh as D, test_wE_v3 as T
np.seterr(all='ignore')

F_E, F_SCAT = 0.875, 0.32          # electrons par baryon ; largeur de dispersion IGM
ZG = np.linspace(0, 2.0, 2000)

# ---------- fonds ----------
T.ZCUT = None
zl, El = T.fond(0.2976, 0.0, None, 'lcdm')
E_l = lambda z: np.interp(z, zl, El); h_l, wb_l = 0.6866, 0.02261
za, Ea_ = T.fond(0.2999, 0.0, 2.595, 'invt')
E_a = lambda z: np.interp(z, za, Ea_); h_a, wb_a = 0.6885, 0.02261

PSI0 = lambda z: 0.015*(1+z)**2.7/(1+((1+z)/2.9)**5.6)
A, B, XI, WC, WBP = 1.551, 3.119, 1.382, 0.1189, 0.02245
D.psi_MD14 = lambda z: A*PSI0(z)*np.where(np.asarray(z) > 4.0, B, 1.0)
oc = D.fond_ccbh(WC, WBP, XI)
wb_arr = np.full_like(D.AG, WBP); wde = np.zeros_like(D.AG)
for i in range(np.searchsorted(D.AG, 1/21.), len(D.AG)):
    wm = WC+wb_arr[i-1]+D.W_NU_M
    wt = wm/D.AG[i-1]**3+D.W_R/D.AG[i-1]**4+wde[i-1]
    Hy = 100*np.sqrt(wt)*D.KMS_PER_YR
    src = XI*D.psi_MD14(1/D.AG[i-1]-1)/(Hy*D.AG[i-1]**4)/D.RHO100
    da = D.AG[i]-D.AG[i-1]; wde[i] = wde[i-1]+src*da; wb_arr[i] = wb_arr[i-1]-src*D.AG[i-1]**3*da
zc = (1/D.AG-1)[::-1]; wbc = wb_arr[::-1]; hc = oc[2]
E_c = lambda z: np.interp(z, zc, oc[1])
Ob_c = lambda z: np.interp(z, zc, wbc)/hc**2

def dm_shape(E, Ob_of_z, h):
    """int rho_tilde_b (1+z) f_e dz/E, x h ; normalise pour redonner 1085 z f_d a bas z en LCDM."""
    ig = Ob_of_z(ZG)*(1+ZG)*F_E/E(ZG)*h
    return np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(ZG))])

CST_l = dm_shape(E_l, lambda z: np.full_like(np.atleast_1d(z), wb_l/h_l**2, dtype=float), h_l)
NORM = 1085.0*0.02/np.interp(0.02, ZG, CST_l)*(wb_l/h_l**2*h_l/0.7)/0.04703
NORM = 1085.0*0.02/np.interp(0.02, ZG, CST_l)   # ancrage direct sur leur formule a z=0.02
DM_L = NORM*CST_l
DM_A = NORM*dm_shape(E_a, lambda z: np.full_like(np.atleast_1d(z), wb_a/h_a**2, dtype=float), h_a)
DM_C = NORM*dm_shape(E_c, Ob_c, hc)

def dmcos(z, which, fd):
    tab = {'L': DM_L, 'A': DM_A, 'C': DM_C}[which]
    return fd*np.interp(z, ZG, tab)

# ---------- vraisemblance ----------
DMGRID = np.linspace(1.0, 4000.0, 1600)
def logL_one(dmex, z, which, fIGM, fX, mu, sig):
    fd = fIGM+fX
    mc = dmcos(z, which, fd)
    if mc <= 0: return -1e9
    sc = F_SCAT/np.sqrt(max(z, 0.02))
    # composante cosmique log-normale de mediane mc, largeur sc
    x = DMGRID
    p_cos = np.exp(-0.5*(np.log(x/mc)/sc)**2)/(x*sc)
    rest = dmex - x
    ok = rest > 1.0
    p_host = np.zeros_like(x)
    r = rest[ok]*(1+z)
    p_host[ok] = np.exp(-0.5*((np.log(r)-mu)/sig)**2)/(r*sig)
    v = np.trapezoid(p_cos*p_host, x)
    return np.log(v) if v > 0 else -1e9

def logL(data, which, p):
    fIGM, fX, mu, sig = p
    if not (0 < fIGM < 1 and 0 <= fX < 1 and fIGM+fX <= 1 and 0 < mu < 7 and 0.05 < sig < 2.0):
        return -1e9
    return sum(logL_one(d, z, which, fIGM, fX, mu, sig) for d, z in data)

if __name__ == '__main__':
    rng = np.random.default_rng(11)
    N = 69
    z = np.clip(rng.gamma(2.0, 0.16, N), 0.03, 1.35)
    TRUE = dict(fIGM=0.80, fX=0.11, mu=np.log(120.0), sig=0.55)
    dat = []
    for zi in z:
        mc = dmcos(zi, 'L', TRUE['fIGM']+TRUE['fX'])
        c = mc*np.exp(rng.normal(0, F_SCAT/np.sqrt(max(zi, 0.02))))
        hst = np.exp(rng.normal(TRUE['mu'], TRUE['sig']))/(1+zi)
        dat.append((c+hst, zi))
    print("="*76)
    print(f"  ECHANTILLON SYNTHETIQUE : N = {N}, z de {z.min():.2f} a {z.max():.2f}, median {np.median(z):.2f}")
    print(f"  verite : f_IGM={TRUE['fIGM']}, f_X={TRUE['fX']}, mediane hote={np.exp(TRUE['mu']):.0f} pc/cm3")
    print("="*76)
    res = {}
    for which, lab in [('L', 'LCDM'), ('A', 'ACCRETION'), ('C', 'CCBH')]:
        best = None
        for s in ([0.8, 0.1, np.log(120), 0.55], [0.6, 0.3, np.log(200), 0.7], [0.95, 0.04, np.log(60), 0.4]):
            r = minimize(lambda p: -logL(dat, which, p), s, method='Nelder-Mead',
                         options=dict(xatol=1e-4, fatol=1e-4, maxiter=3000))
            if best is None or r.fun < best.fun: best = r
        res[lab] = best
        fI, fX, mu, sg = best.x
        bord = "BORD" if fI+fX > 0.995 else ""
        print(f"  {lab:>10s} : -lnL = {best.fun:9.3f}  f_IGM={fI:.3f} f_X={fX:.3f} (somme {fI+fX:.3f} {bord})"
              f"  hote median={np.exp(mu):6.1f}  sigma={sg:.3f}")
    v = res['LCDM'].x
    ok = abs(v[0]-0.80) < 0.10 and v[1] < 0.3
    print(f"\n  VALIDATION (LCDM doit redonner f_IGM = 0,80 +/- 0,10 et f_X < 0,3) : "
          f"{'PASSE' if ok else 'ECHEC'}")
    if not ok:
        print("  -> machinerie non validee, rien exploite."); sys.exit()
    print("\n" + "="*76)
    print("  LES NUISANCES ABSORBENT-ELLES LE DEFICIT CCBH ?")
    print("="*76)
    for lab in ['ACCRETION', 'CCBH']:
        d2 = 2*(res[lab].fun - res['LCDM'].fun)
        print(f"    {lab:>10s} : Dchi2 vs LCDM = {d2:+8.2f}  -> {np.sqrt(max(d2,0)):.1f} sigma")
    print("\n  Lecture : si CCBH sature f_IGM+f_X = 1 ET garde un Dchi2 important, le deficit")
    print("  n'est pas absorbable par les nuisances. Si l'hote monte et Dchi2 ~ 0, il l'est.")
