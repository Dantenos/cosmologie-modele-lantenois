#!/usr/bin/env python3
"""
horloge_vaidya.py — La ligne manquante : g(t) dérivé au lieu d'être paramétré.

MONTAGE. Extérieur : Vaidya entrant, ds^2 = -(1-2M(v)/r)dv^2 + 2 dv dr + r^2 dOmega^2.
Intérieur : FLRW plat, R = a(t) chi_b l'aire-rayon de la surface de raccordement.

PREMIERE CONDITION DE JONCTION (Darmois) : la métrique induite doit coïncider.
Côté intérieur, le temps propre sur Sigma est t. Côté extérieur, avec r = R(t) :
        (1 - 2M/R) vdot^2 - 2 Rdot vdot = 1.
Résoudre pour vdot :
        vdot = [Rdot +/- sqrt(Rdot^2 + 1 - 2M/R)] / (1 - 2M/R).

L'IDENTITE QUI SIMPLIFIE TOUT. En FLRW, la masse de Misner-Sharp vaut M = H^2 R^3 / 2,
donc 2M/R = H^2 R^2 ; et Rdot = H R. Donc
        Rdot^2 + 1 - 2M/R = H^2R^2 + 1 - H^2R^2 = 1   EXACTEMENT.
La racine disparaît, et avec x = H R (rayon en unités de rayon de Hubble) :
        vdot = (x + 1)/(1 - x^2) = 1/(1 - x).

        ****  dv/dt = 1/(1 - H R_b)  ****

Contrôles : x -> 0 donne dv/dt -> 1 (temps avancé = temps propre au centre) ;
x -> 1 (horizon apparent, R = 2M) donne une divergence.

CE QUE CELA DONNE POUR g. Si l'accrétion du parent est une loi de puissance dans SON temps,
M ∝ v^{beta_p}, alors  dlnM/dlnt = beta_p x (t/v)(dv/dt) = beta_p g(t), avec
        g(t) = (t/v) / (1 - x(t)),   v(t) = int dt'/(1 - x(t')).
et la courbure d'horloge mesurée est kappa = dln g/dln t evaluee a t0.
"""
import numpy as np

OM, BETA, ZEQ = 0.3113, 2.418, 3387.0
np.seterr(all='ignore')

# --- fond du modèle, en unités H0 = 1 ---
a = np.logspace(-7, 0, 200000)
Or = OM/(1+ZEQ); Ode = 1-OM-Or
E2 = OM/a**3 + Or/a**4 + Ode
for _ in range(12):
    E = np.sqrt(E2); ig = 1/(a*E)
    t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
    E2 = OM/a**3 + Or/a**4 + Ode*np.clip(t, 1e-300, None)**BETA/a**3
E = np.sqrt(E2)
t0H0 = 0.9501                      # H0 t0 du corpus
T = t*t0H0                          # temps en unités 1/H0
H = E                               # H/H0

print("="*76)
print("  CONTROLE 1 : l'identite Rdot^2 + 1 - 2M/R = 1 tient-elle numeriquement ?")
print("="*76)
for chi in [0.1, 0.3]:
    R = a*chi; Rd = H*R; MS = H**2*R**3/2
    q = Rd**2 + 1 - 2*MS/R
    j = np.argmin(np.abs(a-0.5))
    print(f"    chi_b = {chi}: a=0.5 -> Rdot^2+1-2M/R = {q[j]:.12f}   (attendu 1)")

print("\n" + "="*76)
print("  CONTROLE 2 : la surface reste-t-elle SOUS l'horizon apparent (x < 1) ?")
print("="*76)
print(f"  {'chi_b':>7s} {'x(a=1e-4)':>11s} {'x min':>9s} {'a(x min)':>10s} {'x(a=1)':>9s}  verdict")
for chi in [0.01, 0.05, 0.1, 0.3, 0.5]:
    x = H*a*chi
    m = a > 1e-6
    print(f"  {chi:>7.2f} {x[np.argmin(np.abs(a-1e-4))]:>11.2f} {x[m].min():>9.4f}"
          f" {a[m][np.argmin(x[m])]:>10.2e} {x[-1]:>9.4f}   "
          f"{'x>1 tot ou tard' if x[m].max()>1 else 'toujours sous-horizon'}")
print("\n  x = H a chi_b croit vers le passe (H a ∝ a^-1/2 en matiere) : TOUTE coquille comobile")
print("  est super-horizon assez tot. Il n'existe donc pas de raccordement comobile qui reste")
print("  sous l'horizon a tout instant. C'est une contrainte de structure, pas un detail.")

print("\n" + "="*76)
print("  CALCUL DE kappa POUR UNE COQUILLE SOUS-HORIZON DEPUIS a_i")
print("="*76)
print("  On integre v a partir de a_i = 1e-3 (apres l'entree dans l'horizon), et on evalue")
print("  kappa = dln g/dln t en t0. Le choix de a_i est declare, et sa sensibilite testee.")
print(f"\n  {'chi_b':>7s} {'x0=H0R0':>9s} {'a_i':>7s} {'g(t0)':>8s} {'kappa':>9s}  |kappa|<0,24 ?")
for chi in [0.02, 0.05, 0.10, 0.20, 0.35, 0.50]:
    for ai in [1e-3]:
        x = H*a*chi
        m = (a >= ai) & (x < 0.999)
        if m.sum() < 100: 
            print(f"  {chi:>7.2f} {x[-1]:>9.4f} {ai:>7.0e}   coquille super-horizon a a_i")
            continue
        Tm, xm = T[m], x[m]
        dv = 1/(1-xm)
        v = np.concatenate([[1e-12], np.cumsum(0.5*(dv[1:]+dv[:-1])*np.diff(Tm))])
        g = (Tm/np.clip(v,1e-30,None))*dv
        lng, lnt = np.log(np.clip(g,1e-30,None)), np.log(Tm)
        k = np.gradient(lng, lnt)[-1]
        ok = "OUI" if abs(k) < 0.24 else "NON"
        print(f"  {chi:>7.2f} {x[-1]:>9.4f} {ai:>7.0e} {g[-1]:>8.4f} {k:>9.4f}  {ok}")

print("\n" + "="*76)
print("  SENSIBILITE AU CHOIX DE a_i (l'origine de v)")
print("="*76)
chi = 0.10
for ai in [3e-4, 1e-3, 3e-3, 1e-2]:
    x = H*a*chi; m = (a >= ai) & (x < 0.999)
    Tm, xm = T[m], x[m]; dv = 1/(1-xm)
    v = np.concatenate([[1e-12], np.cumsum(0.5*(dv[1:]+dv[:-1])*np.diff(Tm))])
    g = (Tm/np.clip(v,1e-30,None))*dv
    k = np.gradient(np.log(np.clip(g,1e-30,None)), np.log(Tm))[-1]
    print(f"    a_i = {ai:.0e} -> kappa = {k:+.4f}")
print("\n  Si kappa depend fortement de a_i, l'origine du temps avance est un parametre")
print("  physique du modele, pas une convention : a declarer comme tel.")
