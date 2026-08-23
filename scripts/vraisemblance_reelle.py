#!/usr/bin/env python3
"""
vraisemblance_reelle.py — Fit sur DONNEES REELLES : DESI DR2 BAO + Pantheon+ SNe
Modeles : LCDM / w0waCDM (CPL) / Accretion parentale (auto-coherent)
BAO : 13 mesures DR2 (arXiv:2503.14738, table via 2604.11106), corr. DM-DH incluses
SNe : Pantheon+ (1701 SNe, covariance stat+sys complete), coupure zHD>0.01,
      calibrateurs exclus, marginalisation analytique sur M (et donc H0)
q = c/(H0 rd) profile analytiquement pour le BAO (tous les observables y sont lineaires)
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar

# ---------- Donnees BAO DESI DR2 ----------
# (z, type, valeur, sigma) ; type: V=DV/rd, M=DM/rd, H=DH/rd ; blocs correles (rho_MH)
BAO = [
 (0.295,'V', 7.942,0.075,None),
 (0.510,'M',13.588,0.167,-0.459),(0.510,'H',21.863,0.425,None),
 (0.706,'M',17.351,0.177,-0.404),(0.706,'H',19.455,0.330,None),
 (0.934,'M',21.576,0.152,-0.416),(0.934,'H',17.641,0.193,None),
 (1.321,'M',27.601,0.318,-0.434),(1.321,'H',14.176,0.221,None),
 (1.484,'M',30.512,0.760,-0.500),(1.484,'H',12.817,0.516,None),
 (2.330,'M',38.988,0.531,-0.431),(2.330,'H', 8.632,0.101,None),
]
d_bao = np.array([b[2] for b in BAO])
C_bao = np.zeros((13,13))
for i,b in enumerate(BAO): C_bao[i,i] = b[3]**2
for i,b in enumerate(BAO):
    if b[4] is not None:   # correlation avec la ligne suivante (DH du meme traceur)
        C_bao[i,i+1] = C_bao[i+1,i] = b[4]*b[3]*BAO[i+1][3]
Cinv_bao = np.linalg.inv(C_bao)

# ---------- Donnees Pantheon+ ----------
raw = np.genfromtxt('pantheon.dat', names=True, dtype=None, encoding=None)
z_sn_all = raw['zHD']; mb_all = raw['m_b_corr']; calib = raw['IS_CALIBRATOR']
cov_flat = np.loadtxt('pantheon_cov.cov', skiprows=1)
N = int(np.sqrt(cov_flat.size)); C_sn_full = cov_flat.reshape(N,N)
mask = (z_sn_all > 0.01) & (calib == 0)
z_sn, mb = z_sn_all[mask], mb_all[mask]
C_sn = C_sn_full[np.ix_(mask,mask)]
Cinv_sn = np.linalg.inv(C_sn)
one = np.ones(len(z_sn)); Cinv_one = Cinv_sn@one; oCo = one@Cinv_one
print(f"SNe retenues : {len(z_sn)} (z>0.01, hors calibrateurs)")

# ---------- Fond cosmologique ----------
ZEQ = 3387.0
zg = np.concatenate([np.linspace(0,2.6,4000), np.linspace(2.61,1100,2000)])

def E_lcdm(z, Om, w0=-1.0, wa=0.0):
    Or = Om/(1+ZEQ); Ode = 1-Om-Or
    fde = (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
    return np.sqrt(Om*(1+z)**3 + Or*(1+z)**4 + Ode*fde)

def E_acc(z, Om, beta, n_iter=4):
    """Modele d'accretion auto-coherent : rho_de = Ode*(t/t0)^beta / a^3."""
    Or = Om/(1+ZEQ); Ode = 1-Om-Or
    a = np.logspace(-6, 0, 25000)
    E2 = (Om + Ode)/a**3 + Or/a**4          # initialisation (pas critique)
    for _ in range(n_iter):
        E = np.sqrt(E2)
        integ = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])
        t = t/t[-1]                          # t(a=1)=1
        E2 = (Om + Ode*t**beta)/a**3 + Or/a**4
    az = 1/(1+z)
    return np.interp(az, a, np.sqrt(E2))

# ---------- Vraisemblances ----------
def chi2_total(Efunc):
    Ez = Efunc(zg)
    inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])  # (c/H0)^-1 * DM
    # --- SNe : mu = 5log10[(1+z)*Dc] + cste ; M et H0 marginalises analytiquement
    mu = 5*np.log10((1+z_sn)*np.interp(z_sn, zg, Dc))
    r = mb - mu
    A = r@Cinv_sn@r; B = r@Cinv_one
    chi2_sn = A - B*B/oCo
    # --- BAO : observables lineaires en q = c/(H0 rd) -> q profile analytiquement
    u = np.zeros(13)
    for i,(z,typ,_,_,_) in enumerate(BAO):
        DM_ = np.interp(z, zg, Dc); DH_ = 1/np.interp(z, zg, Ez)
        u[i] = {'M':DM_, 'H':DH_, 'V':(z*DM_**2*DH_)**(1/3)}[typ]
    q = (u@Cinv_bao@d_bao)/(u@Cinv_bao@u)
    rb = d_bao - q*u
    chi2_bao = rb@Cinv_bao@rb
    return chi2_sn, chi2_bao, q

# ---------- Ajustements ----------
def fit_lcdm():
    f = lambda Om: sum(chi2_total(lambda z: E_lcdm(z,Om))[:2])
    res = minimize_scalar(f, bounds=(0.20,0.45), method='bounded')
    Om = res.x; s,b,q = chi2_total(lambda z: E_lcdm(z,Om))
    return dict(nom='LCDM', k=1, Om=Om, chi2_sn=s, chi2_bao=b, q=q)

def fit_cpl():
    f = lambda p: sum(chi2_total(lambda z: E_lcdm(z,p[0],p[1],p[2]))[:2])
    res = minimize(f, x0=[0.32,-0.85,-0.5], method='Nelder-Mead',
                   options=dict(xatol=1e-3,fatol=1e-3,maxiter=400))
    Om,w0,wa = res.x; s,b,q = chi2_total(lambda z: E_lcdm(z,Om,w0,wa))
    return dict(nom='w0waCDM', k=3, Om=Om, w0=w0, wa=wa, chi2_sn=s, chi2_bao=b, q=q)

def fit_acc():
    f = lambda p: sum(chi2_total(lambda z: E_acc(z,p[0],p[1]))[:2])
    res = minimize(f, x0=[0.33,2.4], method='Nelder-Mead',
                   options=dict(xatol=1e-3,fatol=1e-3,maxiter=300))
    Om,beta = res.x; s,b,q = chi2_total(lambda z: E_acc(z,Om,beta))
    return dict(nom='Accretion', k=2, Om=Om, beta=beta, chi2_sn=s, chi2_bao=b, q=q)

if __name__ == '__main__':
    ndata = len(z_sn) + 13
    print(f"Points de donnees : {len(z_sn)} SNe + 13 BAO = {ndata}\n")
    res = [fit_lcdm(), fit_cpl(), fit_acc()]
    ref = res[0]['chi2_sn'] + res[0]['chi2_bao']
    for r in res:
        tot = r['chi2_sn'] + r['chi2_bao']
        extra = ''
        if 'w0' in r: extra = f" w0={r['w0']:+.3f} wa={r['wa']:+.3f}"
        if 'beta' in r: extra = f" beta={r['beta']:.3f}"
        print(f"{r['nom']:10s} Om={r['Om']:.3f}{extra}")
        print(f"           chi2_SN={r['chi2_sn']:.2f}  chi2_BAO={r['chi2_bao']:.2f}  "
              f"TOTAL={tot:.2f}  Dchi2={tot-ref:+.2f}  AIC={tot+2*r['k']:.2f}")
        # H0*rd implicite : q = c/(H0 rd)
        print(f"           H0*rd = c/q = {299792.458/r['q']:.0f} km/s\n")
