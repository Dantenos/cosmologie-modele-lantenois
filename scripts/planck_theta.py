#!/usr/bin/env python3
"""
planck_theta.py — Vraisemblance Planck complete, version sequencable.
H0 est resolu a chaque point par la contrainte theta* (fond CAMB seul, rapide),
les spectres complets ne sont calcules qu'aux points de l'optimiseur externe.
Etat sauvegarde sur disque -> relançable par tranches de <5 min.
Usage : python3 planck_theta.py <lcdm|cpl|acc> <n_evals_max>
"""
import numpy as np, sys, json, os, time
sys.path.insert(0, 'planck-lite-py')
from planck_lite_py import PlanckLitePy
import camb
from vraisemblance_reelle import BAO, d_bao, Cinv_bao, z_sn, mb, Cinv_sn, Cinv_one, oCo

planck = PlanckLitePy(data_directory='planck-lite-py/data', year=2018,
                      spectra='TTTEEE', use_low_ell_bins=True)
OMB_H2, NS, TAU = 0.02237, 0.9649, 0.0544
THETASTAR = 1.04109e-2
z_bao = np.array([b[0] for b in BAO])

def w_of_a_acc(a_tab, Om, beta, n_iter=4):
    Or = 4.15e-5/0.68**2; Ode = 1-Om-Or
    a = np.logspace(-7, 0, 30000)
    E2 = (Om+Ode)/a**3 + Or/a**4
    for _ in range(n_iter):
        E = np.sqrt(E2); integ = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))]); t = t/t[-1]
        E2 = (Om + Ode*np.clip(t,1e-30,None)**beta)/a**3 + Or/a**4
    w = -(beta/3.0)/np.clip(np.sqrt(E2)*t, 1e-10, None)
    return np.interp(a_tab, a, np.clip(w, -20, 0.9))

def make_pars(H0, omch2, ln10As, de):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=OMB_H2, omch2=omch2, tau=TAU)
    pars.InitPower.set_params(As=np.exp(ln10As)*1e-10, ns=NS)
    if de[0] == 'cpl':
        pars.set_dark_energy(w=de[1], wa=de[2], dark_energy_model='ppf')
    elif de[0] == 'acc':
        h = H0/100.0; Om = (OMB_H2+omch2)/h**2 + 0.06/93.14/h**2
        a_tab = np.logspace(-6, 0, 300)
        pars.set_dark_energy_w_a(a_tab, w_of_a_acc(a_tab, Om, de[1]), dark_energy_model='ppf')
    return pars

def H0_from_theta(omch2, de, lo=55., hi=80.):
    """Resout theta*(H0) = theta*_Planck par bissection (fond seul, rapide)."""
    def theta(H0):
        try:
            r = camb.get_background(make_pars(H0, omch2, 3.044, de))
            return r.get_derived_params()['thetastar']/100.0
        except Exception:
            return np.nan
    for _ in range(28):
        mid = 0.5*(lo+hi); t = theta(mid)
        if not np.isfinite(t): return None
        if t < THETASTAR: lo = mid
        else: hi = mid
        if hi-lo < 0.003: break
    return 0.5*(lo+hi)

def chi2_full(omch2, ln10As, de):
    H0 = H0_from_theta(omch2, de)
    if H0 is None: return 1e10, None
    pars = make_pars(H0, omch2, ln10As, de)
    pars.set_for_lmax(2600, lens_potential_accuracy=1)
    try:
        res = camb.get_results(pars)
    except Exception:
        return 1e10, None
    cl = res.get_cmb_power_spectra(pars, CMB_unit='muK')['total']
    Dltt = cl[2:2509,0]; Dlee = cl[2:2509,1]; Dlte = cl[2:2509,3]
    chi2_cmb = -2*planck.loglike(Dltt, Dlte, Dlee, ellmin=2)
    rd = res.get_derived_params()['rdrag']
    DM = res.comoving_radial_distance(z_bao); DH = 299792.458/res.hubble_parameter(z_bao)
    u = np.array([{'M':DM[i],'H':DH[i],'V':(z*DM[i]**2*DH[i])**(1/3)}[t]/rd
                  for i,(z,t,_,_,_) in enumerate(BAO)])
    rb = d_bao - u; chi2_bao = rb@Cinv_bao@rb
    zs = np.linspace(1e-4, 2.6, 1500)
    Dc = res.comoving_radial_distance(zs)
    mu = 5*np.log10((1+z_sn)*np.interp(z_sn, zs, Dc)) + 25
    r = mb - mu; chi2_sn = r@Cinv_sn@r - (r@Cinv_one)**2/oCo
    return chi2_cmb + chi2_bao + chi2_sn, H0

# --- optimisation par recherche de motif (pattern search), reprenable sur disque ---
CONF = {
 'lcdm': dict(x0=[0.1200, 3.044],              de=lambda x: ('lcdm',),
              steps=[0.0008, 0.008]),
 'cpl':  dict(x0=[0.1195, 3.041, -0.84, -0.60], de=lambda x: ('cpl', x[2], x[3]),
              steps=[0.0008, 0.008, 0.06, 0.25]),
 'acc':  dict(x0=[0.1195, 3.041, 2.42],         de=lambda x: ('acc', x[2]),
              steps=[0.0008, 0.008, 0.15]),
}

def pattern_search(model, budget):
    cf = CONF[model]; state_f = f"state_{model}.json"
    if os.path.exists(state_f):
        st = json.load(open(state_f))
    else:
        st = dict(x=cf['x0'], steps=cf['steps'], best=None, H0=None, done=False)
    x = np.array(st['x']); steps = np.array(st['steps'])
    de = cf['de']
    if st['best'] is None:
        st['best'], st['H0'] = chi2_full(x[0], x[1], de(x)); budget -= 1
    nev = 0
    while nev < budget and not st['done']:
        improved = False
        for i in range(len(x)):
            for s in (+1, -1):
                if nev >= budget: break
                xt = x.copy(); xt[i] += s*steps[i]
                c, H0 = chi2_full(xt[0], xt[1], de(xt)); nev += 1
                if c < st['best'] - 1e-3:
                    x, st['best'], st['H0'], improved = xt, c, H0, True
                    break
            if improved: break
        if not improved:
            steps = steps/2.0
            if np.all(steps < np.array(cf['steps'])/16.0): st['done'] = True
        st['x'] = list(x); st['steps'] = list(steps)
        json.dump(st, open(state_f,'w'))
    json.dump(st, open(state_f,'w'))
    print(f"[{model}] chi2={st['best']:.2f} H0={st['H0']:.2f} x={np.round(x,4)} "
          f"steps={np.round(steps,5)} done={st['done']}", flush=True)

if __name__ == '__main__':
    pattern_search(sys.argv[1], int(sys.argv[2]))
