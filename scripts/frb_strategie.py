#!/usr/bin/env python3
"""
frb_strategie.py — D'ou vient le pouvoir discriminant ? Du NOMBRE ou du LEVIER ?

CE QUE J'AI AFFIRME SANS LE VERIFIER dans le papier C : << Dchi2 croit avec la taille de
l'echantillon, donc 142 sursauts donnent 3 sigma >>. Deux choses non testees la-dedans :
  (a) la linearite en N ;
  (b) l'hypothese implicite que tous les sursauts se valent.

OR IL Y A UNE RAISON STRUCTURELLE DE PENSER QUE NON. A un redshift unique, DM_cos(z) et
DM_host/(1+z) sont PARFAITEMENT degeneres : on ne peut pas les separer. Le pouvoir vient
donc du LEVIER EN REDSHIFT, pas du nombre brut. Un echantillon concentre a bas z devrait
etre presque aveugle, quel que soit N.

Si c'est vrai, la recommandation observationnelle change : ce n'est pas << 142 sursauts >>
qu'il faut, c'est << des sursauts LOINTAINS >>.

CRITERE PRE-ENREGISTRE :
  - on compare quatre distributions en z a N EGAL. Si l'ecart entre elles depasse un
    facteur 2 en Dchi2, alors le nombre n'est pas la bonne variable et le papier C doit
    etre corrige.
  - on verifie separement la linearite en N a distribution fixe (N = 69 contre N = 140).
"""
import numpy as np, sys
from scipy.optimize import minimize
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
exec(open('/home/claude/selection/frb_likelihood.py').read().split('if __name__')[0])
np.seterr(all='ignore')

TRUE = dict(fIGM=0.80, fX=0.11, mu=np.log(120.0), sig=0.55)

def mock(zs, seed):
    rng = np.random.default_rng(seed)
    dat = []
    for zi in zs:
        mc = dmcos(zi, 'L', TRUE['fIGM']+TRUE['fX'])
        c = mc*np.exp(rng.normal(0, F_SCAT/np.sqrt(max(zi, 0.02))))
        h = np.exp(rng.normal(TRUE['mu'], TRUE['sig']))/(1+zi)
        dat.append((c+h, zi))
    return dat

def fit(dat, which):
    best = None
    for s in ([0.8, 0.1, np.log(120), 0.55], [0.6, 0.3, np.log(200), 0.7]):
        r = minimize(lambda p: -logL(dat, which, p), s, method='Nelder-Mead',
                     options=dict(xatol=1e-4, fatol=1e-4, maxiter=2500))
        if best is None or r.fun < best.fun: best = r
    return best

def d2(dat):
    return 2*(fit(dat, 'C').fun - fit(dat, 'L').fun)

def tirage(kind, N, rng):
    if kind == 'bas z (0,05-0,4)':        return rng.uniform(0.05, 0.40, N)
    if kind == 'actuel (median 0,32)':    return np.clip(rng.gamma(2.0, 0.16, N), 0.03, 1.35)
    if kind == 'etendu (median 0,55)':    return np.clip(rng.gamma(2.6, 0.22, N), 0.05, 1.8)
    if kind == 'bimodal (levier max)':    return np.concatenate([rng.uniform(0.05,0.20,N//2),
                                                                rng.uniform(0.9,1.5,N-N//2)])
    if kind == 'haut z seul (0,9-1,5)':   return rng.uniform(0.9, 1.5, N)

print("="*78)
print("  (1) A N EGAL (69), QUATRE DISTRIBUTIONS EN REDSHIFT")
print("="*78)
print(f"  {'distribution':>26s} {'z median':>9s} {'Dchi2 median':>13s} {'sigma':>7s} {'par sursaut':>12s}")
NR = 6
resume = {}
for kind in ['bas z (0,05-0,4)', 'actuel (median 0,32)', 'etendu (median 0,55)',
             'haut z seul (0,9-1,5)', 'bimodal (levier max)']:
    vals, zm = [], []
    for s in range(NR):
        rng = np.random.default_rng(1000+s)
        zs = tirage(kind, 69, rng)
        zm.append(np.median(zs))
        vals.append(d2(mock(zs, 2000+s)))
    v = np.median(vals); resume[kind] = v
    print(f"  {kind:>26s} {np.mean(zm):>9.2f} {v:>13.2f} {np.sqrt(max(v,0)):>7.1f}"
          f" {v/69:>12.4f}", flush=True)

print("\n  RAPPORT entre la meilleure et la pire distribution : "
      f"{max(resume.values())/max(min(resume.values()),1e-3):.1f}x")

print("\n" + "="*78)
print("  (2) LINEARITE EN N, a distribution ACTUELLE fixe")
print("="*78)
print(f"  {'N':>6s} {'Dchi2 median':>13s} {'Dchi2/N':>10s} {'attendu si lineaire':>20s}")
base = None
for N in [35, 69, 140]:
    vals = []
    for s in range(4):
        rng = np.random.default_rng(3000+s)
        zs = tirage('actuel (median 0,32)', N, rng)
        vals.append(d2(mock(zs, 4000+s)))
    v = np.median(vals)
    if N == 69: base = v
    att = base*N/69 if base else float('nan')
    print(f"  {N:>6d} {v:>13.2f} {v/N:>10.4f} {att:>20.2f}", flush=True)
print("\n  Si Dchi2/N est constant, l'extrapolation du papier C tient.")
