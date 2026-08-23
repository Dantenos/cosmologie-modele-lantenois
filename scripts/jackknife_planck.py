#!/usr/bin/env python3
"""
jackknife_planck.py — Le test qui reste : le Delta chi2 = -12.6 (Planck+BAO+SN complets)
tient-il si l'on retire chacune des 13 mesures BAO DR2 ?

USAGE (dans le repertoire desi_fit, a cote de planck_theta.py) :
    python3 jackknife_planck.py all 40        # 40 evaluations par tranche, reprenable
    python3 jackknife_planck.py 3  60         # ne traiter que le retrait n°3
    python3 jackknife_planck.py report        # afficher la table des resultats courants

MECANIQUE : pour chaque retrait k, on optimise LCDM (2 params) et ACC (3 params) par
recherche de motif a pas decroissant, en partant du best-fit COMPLET (depart chaud).
Etat sauve dans jk_state_{lcdm|acc}_{k}.json -> le script peut etre tue et relance.
Budget realiste : ~8-15 s par evaluation CAMB+Planck => ~1 h par retrait pour les deux
modeles a convergence grossiere. Les 13 retraits : une nuit.

LECTURE DU RESULTAT (criteres pre-enregistres, 19/08, AVANT execution) :
  - si Delta chi2(acc) reste <= -9 pour les 13 retraits : le signal CMB ne tient a aucun point.
  - si UN retrait fait remonter au-dessus de -7 : le resultat repose sur ce point -> ERRATUM
    majeur a publier, et le papier A doit le declarer en resume.
  - beta doit rester dans [2.2, 2.7] ; toute sortie = instabilite a signaler.
"""
import numpy as np, json, os, sys, time

sys.path.insert(0, '.'); sys.path.insert(0, 'planck-lite-py')
import planck_theta as pt
from vraisemblance_reelle import BAO, d_bao, C_bao, z_sn, mb, Cinv_sn, Cinv_one, oCo

REF_COMPLET = dict(lcdm=1998.6326, acc=1986.0297)   # etats converges connus (13 points)

def chi2_drop(omch2, ln10As, de, drop):
    """Copie de pt.chi2_full avec la mesure BAO d'indice `drop` retiree."""
    import camb
    H0 = pt.H0_from_theta(omch2, de)
    if H0 is None: return 1e10, None
    pars = pt.make_pars(H0, omch2, ln10As, de)
    pars.set_for_lmax(2600, lens_potential_accuracy=1)
    try: res = camb.get_results(pars)
    except Exception: return 1e10, None
    cl = res.get_cmb_power_spectra(pars, CMB_unit='muK')['total']
    chi2_cmb = -2*pt.planck.loglike(cl[2:2509,0], cl[2:2509,3], cl[2:2509,1], ellmin=2)
    rd = res.get_derived_params()['rdrag']
    zb = np.array([b[0] for b in BAO])
    DM = res.comoving_radial_distance(zb); DH = 299792.458/res.hubble_parameter(zb)
    u = np.array([{'M':DM[i], 'H':DH[i], 'V':(z*DM[i]**2*DH[i])**(1/3)}[t]/rd
                  for i,(z,t,_,_,_) in enumerate(BAO)])
    idx = [i for i in range(13) if i != drop] if drop is not None else list(range(13))
    Cinv = np.linalg.inv(C_bao[np.ix_(idx, idx)])
    rb = d_bao[idx] - u[idx]; chi2_bao = rb@Cinv@rb
    zs = np.linspace(1e-4, 2.6, 1500); Dc = res.comoving_radial_distance(zs)
    mu = 5*np.log10((1+z_sn)*np.interp(z_sn, zs, Dc)) + 25
    r = mb - mu; chi2_sn = r@Cinv_sn@r - (r@Cinv_one)**2/oCo
    return chi2_cmb + chi2_bao + chi2_sn, H0

CONF = {'lcdm': dict(x0=[0.1182, 3.039],         de=lambda x: ('lcdm',),   steps=[0.0006, 0.006]),
        'acc':  dict(x0=[0.11925, 3.0415, 2.589], de=lambda x: ('acc', x[2]), steps=[0.0006, 0.006, 0.05])}

def run(model, drop, budget):
    cf = CONF[model]; f = f"jk_state_{model}_{drop}.json"
    st = json.load(open(f)) if os.path.exists(f) else dict(x=cf['x0'], steps=cf['steps'], best=None, H0=None, done=False)
    x = np.array(st['x'], float); steps = np.array(st['steps'], float); de = cf['de']
    if st['best'] is None:
        st['best'], st['H0'] = chi2_drop(x[0], x[1], de(x), drop); budget -= 1
    nev = 0
    while nev < budget and not st['done']:
        improved = False
        for i in range(len(x)):
            for s in (+1, -1):
                if nev >= budget: break
                xt = x.copy(); xt[i] += s*steps[i]
                c, H0 = chi2_drop(xt[0], xt[1], de(xt), drop); nev += 1
                if c < st['best'] - 0.01:
                    st['best'], x, st['H0'], improved = c, xt, H0, True
        if not improved:
            steps = steps/2
            if steps[0] < 5e-5: st['done'] = True
        st['x'] = list(x); st['steps'] = list(steps)
        json.dump(st, open(f, 'w'))
        print(f"  [{model} drop={drop}] chi2={st['best']:.2f}  x={np.round(x,4)}  evals={nev}", flush=True)
    return st

def report():
    print(f"\n{'retrait':>16s} {'chi2_LCDM':>10s} {'chi2_ACC':>10s} {'Dchi2':>8s} {'beta':>6s} {'statut':>10s}")
    print(f"{'COMPLET (13 pts)':>16s} {REF_COMPLET['lcdm']:>10.2f} {REF_COMPLET['acc']:>10.2f} "
          f"{REF_COMPLET['acc']-REF_COMPLET['lcdm']:>8.2f} {2.589:>6.2f} {'reference':>10s}")
    ds = []
    for k,(z,t,_,_,_) in enumerate(BAO):
        try:
            sl = json.load(open(f"jk_state_lcdm_{k}.json")); sa = json.load(open(f"jk_state_acc_{k}.json"))
            d = sa['best']-sl['best']; ds.append(d)
            statut = "done" if (sl.get('done') and sa.get('done')) else "partiel"
            print(f"{f'z={z:.3f} {t}':>16s} {sl['best']:>10.2f} {sa['best']:>10.2f} {d:>8.2f} {sa['x'][2]:>6.2f} {statut:>10s}")
        except FileNotFoundError:
            print(f"{f'z={z:.3f} {t}':>16s} {'-':>10s} {'-':>10s} {'-':>8s} {'-':>6s} {'a faire':>10s}")
    if ds:
        print(f"\n  Dchi2 sur {len(ds)} retraits : [{min(ds):.2f}, {max(ds):.2f}]")
        print(f"  CRITERE PRE-ENREGISTRE : {'SIGNAL ROBUSTE (tous <= -9)' if max(ds)<=-9 else 'ATTENTION : un retrait remonte au-dessus de -9 -> voir la doc du script'}")

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv)>1 else 'report'
    if arg == 'report': report(); sys.exit()
    budget = int(sys.argv[2]) if len(sys.argv)>2 else 40
    drops = range(13) if arg == 'all' else [int(arg)]
    for k in drops:
        t0 = time.time()
        print(f"\n=== retrait {k} : z={BAO[k][0]} {BAO[k][1]} ===", flush=True)
        run('lcdm', k, budget); run('acc', k, budget)
        print(f"  (tranche {k} : {time.time()-t0:.0f}s)", flush=True)
    report()
