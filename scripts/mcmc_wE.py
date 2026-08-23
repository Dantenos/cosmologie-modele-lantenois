#!/usr/bin/env python3
"""
mcmc_wE.py — Profil de vraisemblance ou posterieure marginalisee ?

CONSTAT : mon profil donne Dchi2(w_E = 0) = 1,0 dans PC1 ; Schiavone et al. publient une
exclusion a 4,7 sigma. Mais leur chiffre est une distance de POSTERIEURE MARGINALISEE
(w_E = -0,98 +0,21/-0,17, echantillonnage imbrique), pas un Dchi2 de profil. Dans un espace
degenere avec priors plats, les deux peuvent differer beaucoup : effet de volume.

HYPOTHESE A TESTER : mon pipeline reproduit leur exclusion SI on marginalise au lieu de
profiler. Si oui, le pipeline est adequat et le desaccord etait methodologique, pas
observationnel.

PRIORS : exactement les leurs (leur table II) pour PC1.
  h (0.4,0.9) ; Omega_m (0.1,0.5) ; w_E (-3,1) ; alpha (0,10) ; beta_PC (-2,2)
  + omega_b (0.02,0.025) comme eux (domine par BBN/CMB).
Pour notre loi : meme chose, avec beta (le parametre PHYSIQUE) plat sur (0,6) et
B = beta(1+w_E) — choix declare, la marginalisation depend du parametrage.

CRITERE PRE-ENREGISTRE :
  (V) si la posteriere marginalisee de w_E dans PC1 exclut 0 a >= 3 sigma -> hypothese
      confirmee, pipeline adequat, et on peut lire le resultat pour notre loi.
      Sinon -> mon pipeline reste non comparable au leur ; ne rien exploiter.
"""
import numpy as np, sys, time, emcee, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
OUT = HERE / 'sorties'; OUT.mkdir(exist_ok=True)
import test_wE_v2 as T

BORNES = dict(h=(0.4, 0.9), ob=(0.020, 0.025), Om=(0.1, 0.5), wE=(-3.0, 1.0),
              alpha=(0.0, 10.0), bPC=(-2.0, 2.0), beta=(0.0, 6.0))

def logp(p, famille):
    h, ob, Om, wE = p[:4]
    for v, k in zip((h, ob, Om, wE), ('h', 'ob', 'Om', 'wE')):
        lo, hi = BORNES[k]
        if not (lo < v < hi): return -np.inf
    if famille == 'PC1':
        b, al = p[4], p[5]
        if not (BORNES['bPC'][0] < b < BORNES['bPC'][1]): return -np.inf
        if not (BORNES['alpha'][0] < al < BORNES['alpha'][1]): return -np.inf
        par = (b, al)
    else:                                   # invt : beta physique plat, B = beta(1+wE)
        beta = p[4]
        if not (BORNES['beta'][0] < beta < BORNES['beta'][1]): return -np.inf
        par = beta*(1+wE)
        if par < 0: return -np.inf
    c = T.chi2(h, ob, Om, wE, par, famille)
    if not np.isfinite(c) or c > 1e8: return -np.inf
    return -0.5*c

def run(famille, ndim, p0c, nw=32, nb=400, ns=1400, tag=''):
    rng = np.random.default_rng(7)
    p0 = np.array(p0c) + 1e-3*rng.normal(size=(nw, ndim))*np.array(p0c)
    p0[:, 3] = np.clip(p0[:, 3] + 0.15*rng.normal(size=nw), -2.5, 0.8)
    s = emcee.EnsembleSampler(nw, ndim, logp, args=(famille,))
    s.random_state = np.random.RandomState(7).get_state()   # chaine reproductible (audit 23/08)
    t0 = time.time()
    st = s.run_mcmc(p0, nb, progress=False)
    s.reset()
    s.run_mcmc(st, ns, progress=False)
    ch = s.get_chain(flat=True)
    print(f"  [{famille}{tag}] {nw}x{ns} apres {nb} de rodage, "
          f"acceptation {np.mean(s.acceptance_fraction):.2f}, {time.time()-t0:.0f}s")
    return ch

if __name__ == '__main__':
    np.seterr(all='ignore')
    quoi = sys.argv[1] if len(sys.argv) > 1 else 'PC1'
    if quoi == 'PC1':
        ch = run('PC1', 6, [0.692, 0.02236, 0.299, -0.7, 0.8, 2.0])
    else:
        ch = run('invt', 5, [0.692, 0.02236, 0.300, -0.5, 2.4])
    np.save(OUT / f'chain_{quoi}.npy', ch)
    w = ch[:, 3]
    q = np.percentile(w, [16, 50, 84])
    print(f"\n  w_E marginalise : {q[1]:+.3f} (+{q[2]-q[1]:.3f}/-{q[1]-q[0]:.3f})")
    print(f"  fraction de la chaine avec w_E > 0 : {np.mean(w > 0)*100:.3f} %")
    sig_haut = (0 - q[1])/(q[2]-q[1])
    print(f"  distance de w_E = 0 en sigma (cote haut) : {sig_haut:.2f}")
    if quoi != 'PC1':
        b = ch[:, 4]; qb = np.percentile(b, [16, 50, 84])
        print(f"  beta marginalise : {qb[1]:.3f} (+{qb[2]-qb[1]:.3f}/-{qb[1]-qb[0]:.3f})")
    json.dump(dict(med=q[1], hi=q[2]-q[1], lo=q[1]-q[0], sig=sig_haut),
              open(OUT / f'marg_{quoi}.json', 'w'))
