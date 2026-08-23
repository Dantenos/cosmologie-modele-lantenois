#!/usr/bin/env python3
"""
beta_courant.py — #51 tranché par la littérature, et sa conséquence testée.

CE QUE DIT LA LITTÉRATURE (sources primaires lues) :
  - Hoffman & Shaham 1985 appliquent l'infall secondaire aux MAXIMA du champ lissé, en
    approximant le profil initial d'un pic par la FONCTION DE CORRÉLATION, delta(r) ~ xi(r)
    [confirmé par Ogiya & Hahn 2018 et les revues de Del Popolo]. Ils obtiennent
    rho ∝ r^-alpha avec alpha = 3(3+n)/(4+n), ce qui correspond, injecté dans la branche
    gamma = 9 eps/(1+3 eps) de FG84, à epsilon = (n+3)/3.
  - Donc la relation standard pour des halos nés de pics gaussiens est
        epsilon = (n+3)/3   =>   beta = 2/(3 eps) = 2/(n+3)      [lecture (B)]
    et NON epsilon = (n+3)/6 => beta = 4/(n+3)                   [lecture (A), papier B]
  - CAVEAT de la même littérature : « la forme radiale des pics est PLUS RAIDE que la
    fonction de corrélation » (Diemand et al.). Donc epsilon >= (n+3)/3, donc
        beta <= 2/(n+3)   : la lecture (B) est une BORNE SUPÉRIEURE, pas une égalité.
  - CAVEAT 2 : Del Popolo souligne que la conclusion de HS pour n < -1 est une hypothèse,
    pas un résultat du modèle. Or notre régime est justement n < -1.

CONSÉQUENCE NON REMARQUÉE, ET C'EST LE VRAI TEST : un spectre CDM réel n'est PAS une loi
de puissance. n_eff(M) court. Donc epsilon court, donc **beta n'est pas constant** : le
modèle prédit un beta VARIABLE, alors que le papier A ajuste un beta constant.
On calcule le taux de variation prédit, puis on le confronte aux données.
"""
import numpy as np, sys
from scipy.optimize import minimize
from gradient_v2 import Cosmo, REF
np.seterr(all='ignore')

c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])

print("="*80)
print("  1. LE COURANT PRÉDIT : dn_eff/dlnM sur un spectre CDM réel")
print("="*80)
print(f"  {'M [Msun/h]':>12s} {'n_eff':>8s} {'dn_eff/dlnM':>13s} {'beta (A)':>9s} {'beta (B)':>9s}")
Ms = np.array([1e11, 1e12, 1e13, 1e14, 1e15, 1e16])
for M in Ms:
    n = c.n_eff(M)
    d = (c.n_eff(M*np.e) - c.n_eff(M/np.e))/2.0
    print(f"  {M:>12.0e} {n:>8.3f} {d:>13.4f} {4/(n+3):>9.3f} {2/(n+3):>9.3f}")

print("\n" + "="*80)
print("  2. CE QUE CELA IMPOSE À beta(t)")
print("="*80)
print("  beta = k/(n_eff+3) avec k = 4 (A) ou 2 (B) ; dlnM_acc/dlnt = beta.")
print("  donc  dbeta/dlnt = beta x dbeta/dlnM = -beta x k/(n+3)^2 x dn_eff/dlnM")
for k, lab in [(4.0, '(A) papier B'), (2.0, '(B) littérature')]:
    for M in [1e12, 1e13, 1e14]:
        n = c.n_eff(M); d = (c.n_eff(M*np.e) - c.n_eff(M/np.e))/2.0
        b = k/(n+3); db = -b*k/(n+3)**2*d
        print(f"    {lab:16s} à M={M:.0e} : beta={b:.3f}, dbeta/dlnt = {db:+.3f} par e-pli de t")
print("\n  Sur la plage observée (t/t0 de 0,4 à 1, soit Dln t = 0,92), cela fait")
print("  un GLISSEMENT de beta de l'ordre de 0,3 à 0,8. Ce n'est pas une correction.")

print("\n" + "="*80)
print("  3. LES DONNÉES TOLÈRENT-ELLES UN beta VARIABLE ?")
print("="*80)
print("  Paramétrisation : beta(t) = beta0 + beta1 ln(t/t0). Alors")
print("     ln M_acc = int beta dln t  =>  M_acc ∝ t^{beta0} exp(beta1 ln^2(t/t0)/2)")
print("     w(z) = -beta(t)/(3Ht)   (la définition de w ne change pas)")

import test_wE_v3 as T
T.ZCUT = None
AG = np.logspace(-7, 0, 12000)

def fond_run(Om, b0, b1, n_iter=8):
    Or = Om/3388.0; Ode = 1-Om-Or
    a = AG
    E2 = Om/a**3 + Or/a**4 + Ode
    for _ in range(n_iter):
        E = np.sqrt(np.clip(E2, 1e-30, None)); ig = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
        L = np.log(np.clip(t, 1e-300, None))
        g = np.exp(np.clip(b0*L + 0.5*b1*L**2, -700, 700))   # M_acc/M_acc(t0)
        E2 = Om/a**3 + Or/a**4 + Ode*g/a**3
    E = np.sqrt(np.clip(E2, 1e-30, None))
    return (1/a - 1)[::-1], E[::-1]

_fond = T.fond
def fond_patch(Om, wE, par, famille, n_iter=7):
    if famille == 'run':
        return fond_run(Om, par[0], par[1])
    return _fond(Om, wE, par, famille, n_iter)
T.fond = fond_patch

def chi2r(p):
    h, ob, Om, b0, b1 = p
    if not (0.0 < b0 < 8 and -6 < b1 < 6): return 1e9
    return T.chi2(h, ob, Om, 0.0, (b0, b1), 'run')

print(f"\n  {'modèle':>28s} {'chi2':>10s} {'beta0':>8s} {'beta1':>8s} {'Dchi2':>8s}")
r0 = minimize(lambda p: chi2r([p[0], p[1], p[2], p[3], 0.0]), [0.69, 0.02236, 0.30, 2.6],
              method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-4, maxiter=4000))
c0 = r0.fun
print(f"  {'beta constant (papier A)':>28s} {c0:>10.3f} {r0.x[3]:>8.3f} {0.0:>8.3f} {0.0:>8.3f}")
best = None
for s in ([0.69, 0.02236, 0.30, 2.6, 0.0], [0.69, 0.02236, 0.30, 2.6, -0.8],
          [0.69, 0.02236, 0.30, 3.0, -1.5], [0.69, 0.02236, 0.30, 2.2, 0.8]):
    r = minimize(chi2r, s, method='Nelder-Mead',
                 options=dict(xatol=1e-5, fatol=1e-4, maxiter=6000, maxfev=6000))
    if best is None or r.fun < best.fun: best = r
print(f"  {'beta1 libre':>28s} {best.fun:>10.3f} {best.x[3]:>8.3f} {best.x[4]:>8.3f}"
      f" {best.fun-c0:>8.3f}")
for b1fix in [-0.8, -0.5, -0.3, 0.3]:
    rr = minimize(lambda p: chi2r([p[0], p[1], p[2], p[3], b1fix]), [0.69, 0.02236, 0.30, 2.6],
                  method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-4, maxiter=4000))
    print(f"  {'beta1 = %+.1f imposé' % b1fix:>28s} {rr.fun:>10.3f} {rr.x[3]:>8.3f}"
          f" {b1fix:>8.3f} {rr.fun-c0:>8.3f}")
print("\n  LECTURE : si le beta1 prédit (-0,3 à -0,8) coûte peu, la théorie et les données")
print("  sont compatibles. S'il coûte cher, la relation d'hérédité est en tension avec")
print("  l'ajustement du papier A — et c'est un vrai résultat négatif du papier B.")
