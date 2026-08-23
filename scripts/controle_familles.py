#!/usr/bin/env python3
"""
controle_familles.py — Le profil plat en w_E vient-il de la LOI DE TAUX ou de la FAIBLESSE
                       de mes donnees ?

Le test precedent donne Dchi2(w_E = 0) = 0,66, soit 0,8 sigma, avec Gamma ∝ 1/t.
Schiavone et al. excluent w_E = 0 a 4,7-5,6 sigma avec Gamma ∝ H^alpha, ∝ 3 gamma H0, etc.
Deux lectures possibles, et une seule est interessante :
  (A) la loi de taux fait la difference  -> alors dans MON pipeline, leurs familles doivent
      exclure w_E = 0 nettement plus fort que la mienne. C'est un resultat.
  (B) mes donnees sont simplement plus faibles que les leurs -> alors AUCUNE famille
      n'exclura w_E = 0 chez moi, et le test precedent ne prouve rien.

CRITERE PRE-ENREGISTRE (avant execution) :
  - Si PC1 et/ou PC3 excluent w_E = 0 a plus de 3 sigma dans mon pipeline alors que
    Gamma ∝ 1/t reste sous 1,5 sigma : lecture (A), la loi de taux est bien le facteur.
  - Si aucune famille n'atteint 2 sigma : lecture (B), mon test est NON CONCLUANT et je
    dois l'ecrire ainsi, sans m'appuyer sur le 0,8 sigma.
  - Cas intermediaire : declare intermediaire.
NOTE DE PROTOCOLE : eux coupent la creation a z > 3 (retour a LCDM). Je ne l'applique a
AUCUN modele, pour que la comparaison isole la loi de taux. Difference declaree.
"""
import numpy as np, sys
from scipy.optimize import minimize
import vraisemblance_reelle as V
from test_wE import zg, ZEQ, ZSTAR, DM_STAR, SIG_STAR

AG = np.logspace(-7, 0, 12000)

def fond_famille(Om, wE, par, famille, n_iter=7):
    """E(z) auto-coherent pour une famille de Gamma donnee.
       g' = 3(1+wE)/(1+z) [1 - Gamma/(3H)] g, integree en ln a depuis a=1 (g=1)."""
    Or = Om/(1+ZEQ); Ode = 1-Om-Or
    a = AG; lna = np.log(a)
    E2 = Om/a**3 + Or/a**4 + Ode
    for _ in range(n_iter):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        if famille == 'invt':                      # Gamma = beta/t  (le notre)
            integ = 1/(a*E)
            t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])
            Ht = E*t                               # en unites H0 = 1 : H0 t = E * t_int
            G3H = par/(3*np.clip(Ht, 1e-12, None))
        elif famille == 'PC1':                     # Gamma = 3 b H0 E^alpha
            b, al = par
            G3H = b*E**(al-1)
        elif famille == 'PC3':                     # Gamma = 3 gamma H0
            G3H = par/E
        else:
            raise ValueError(famille)
        # dln g/dln a = -3(1+wE)[1 - Gamma/3H]   (car d/dz -> -d/dln a x ...)
        dlng = -3*(1+wE)*(1-G3H)
        # integrer depuis a=1 (g=1) vers le passe
        I = np.concatenate([[0], np.cumsum(0.5*(dlng[1:]+dlng[:-1])*np.diff(lna))])
        lng = I - I[-1]
        g = np.exp(np.clip(lng, -700, 700))
        E2 = Om/a**3 + Or/a**4 + Ode*g
    E = np.sqrt(np.clip(E2, 1e-30, None))
    z = 1/a - 1
    return z[::-1], E[::-1]

def chi2_f(Om, wE, par, famille):
    if not (0.05 < Om < 0.7): return 1e9
    try: zz, Ea = fond_famille(Om, wE, par, famille)
    except Exception: return 1e9
    Ez = np.interp(zg, zz, Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0): return 1e9
    inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])
    mu = 5*np.log10((1+V.z_sn)*np.interp(V.z_sn, zg, Dc))
    r = V.mb - mu
    chi2_sn = r@V.Cinv_sn@r - (r@V.Cinv_one)**2/V.oCo
    n = 14; u = np.zeros(n); d = np.zeros(n); C = np.zeros((n, n))
    for i, (z, typ, _, _, _) in enumerate(V.BAO):
        DM_ = np.interp(z, zg, Dc); DH_ = 1/np.interp(z, zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]
    d[:13] = V.d_bao; C[:13, :13] = V.C_bao
    u[13] = np.interp(ZSTAR, zg, Dc); d[13] = DM_STAR; C[13, 13] = SIG_STAR**2
    Ci = np.linalg.inv(C); q = (u@Ci@d)/(u@Ci@u); rb = d - q*u
    return chi2_sn + rb@Ci@rb

def profil(famille, npar, bornes, depart):
    """Profil en w_E : a chaque w_E, minimise sur Om et les parametres de taux."""
    out = []
    for w in [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4]:
        def f(p):
            for v, (lo, hi) in zip(p[1:], bornes):
                if not (lo < v < hi): return 1e9
            par = p[1] if npar == 1 else tuple(p[1:])
            return chi2_f(p[0], w, par, famille)
        best = None
        for dp in depart:
            r = minimize(f, [0.31]+list(dp), method='Nelder-Mead',
                         options=dict(xatol=1e-4, fatol=1e-3, maxiter=2500))
            if best is None or r.fun < best.fun: best = r
        out.append((w, best.fun, best.x))
    cmin = min(o[1] for o in out)
    return out, cmin

if __name__ == '__main__':
    np.seterr(all='ignore')
    print("="*78)
    print("  CONTROLE DE COHERENCE : la routine famille reproduit-elle test_wE ?")
    print("="*78)
    import test_wE as T
    for Om, b in [(0.3113, 2.418), (0.307, 2.30)]:
        print(f"    Om={Om} beta={b} : famille='invt' {chi2_f(Om,0.0,b,'invt'):.3f}"
              f" | test_wE {T.chi2(Om,0.0,b):.3f}")

    print("\n" + "="*78)
    print("  PROFILS EN w_E, TROIS LOIS DE TAUX, MEMES DONNEES, MEME PIPELINE")
    print("="*78)
    familles = [('invt  (Gamma = beta/t : NOTRE loi)', 'invt', 1, [(0.2, 12)], [[2.4], [1.5], [3.5]]),
                ('PC3   (Gamma = 3 gamma H0)',        'PC3',  1, [(0.0, 8)],  [[0.8], [1.4], [0.3]]),
                ('PC1   (Gamma = 3 b H0 E^alpha)',    'PC1',  2, [(0.0, 6), (-2, 8)], [[0.6, 2.1], [1.0, 1.0], [0.3, 4.0]])]
    resume = []
    for nom, fam, npar, bornes, depart in familles:
        out, cmin = profil(fam, npar, bornes, depart)
        d0 = [o[1] for o in out if o[0] == 0.0][0] - cmin
        wbest = out[int(np.argmin([o[1] for o in out]))][0]
        resume.append((nom, d0, np.sqrt(max(d0, 0)), cmin, wbest))
        print(f"\n  --- {nom}")
        print(f"      {'w_E':>7s} {'chi2':>11s} {'Dchi2':>8s}   parametres de taux")
        for w, c, x in out:
            pp = " ".join(f"{v:.3f}" for v in x[1:])
            print(f"      {w:>7.2f} {c:>11.3f} {c-cmin:>8.3f}   Om={x[0]:.4f}  [{pp}]")

    print("\n" + "="*78)
    print("  VERDICT selon le critere PRE-ENREGISTRE")
    print("="*78)
    print(f"  {'loi de taux':>36s} {'Dchi2(w_E=0)':>13s} {'sigma':>7s} {'chi2 min':>10s} {'w_E pref.':>10s}")
    for nom, d0, sg, cmin, wb in resume:
        print(f"  {nom:>36s} {d0:>13.3f} {sg:>7.2f} {cmin:>10.3f} {wb:>10.2f}")
    inv = resume[0][2]; autres = max(r[2] for r in resume[1:])
    if autres > 3 and inv < 1.5:
        print("\n  LECTURE (A) : la loi de taux est bien le facteur discriminant.")
    elif autres < 2:
        print("\n  LECTURE (B) : AUCUNE famille n'exclut w_E = 0 avec mes donnees.")
        print("  => Mon test precedent est NON CONCLUANT. Le 0,8 sigma ne prouve rien :")
        print("     il mesure la faiblesse de mon CMB comprime, pas la robustesse du modele.")
    else:
        print("\n  LECTURE INTERMEDIAIRE : a ecrire telle quelle, sans trancher.")
