#!/usr/bin/env python3
"""
convexite_entropie.py — Le critère de Pavón-Radicella appliqué au modèle.

CE QUE J'AI CRU NEUF ET QUI NE L'EST PAS. Le critère « S' > 0 ET S'' < 0 » est celui de
Pavón & Radicella : pour qu'un système tende vers l'équilibre thermodynamique, son entropie
doit croître ET son évolution être convexe. Il est utilisé comme critère de sélection depuis
au moins 2010, y compris pour paramétrer l'énergie noire (arXiv:2202.03300, « Thermodynamic
parametrization of dark energy »), et un papier de la semaine dernière (arXiv:2608.10495) en
fait exactement le programme que j'annonçais comme non exploré. Ma seule contribution possible
est donc de l'APPLIQUER à ce modèle, ce qui n'a pas été fait.

FORME CORRECTE DU CRITÈRE (telle que publiée, et plus faible que celle que j'appliquais) :
la convexité est exigée dans le FUTUR LOINTAIN, z -> -1, pas à tout instant.
S_total = S_horizon + S_fluide, sur l'HORIZON APPARENT (la surface où les lois de la
thermodynamique sont satisfaites) : S_h = pi/(G H^2) en univers plat.

DEUX RÉGIMES À TESTER DANS NOTRE MODÈLE, car le festin s'arrête :
  (1) attracteur w* = -beta/(beta+2) = -0,548  tant que l'accrétion dure
  (2) après t_end (16-36 Ga), M_acc gèle -> rho_de ∝ a^-3 : le fluide redevient de la matière
Si les deux donnent S'' > 0, la conclusion ne dépend pas du sort du festin.
"""
import numpy as np

print("="*78)
print("  1. LIMITE ASYMPTOTIQUE ANALYTIQUE  (S ∝ 1/H^2)")
print("="*78)
print("  Univers dominé par w constant : a ∝ t^n avec n = 2/(3(1+w)), H = n/t, S ∝ t^2/n^2")
print("  => S'' = 2/n^2 > 0 pour TOUT w > -1.  S'' -> 0^- seulement si w -> -1.")
print()
for lab, w in [("LCDM", -1.0),
               ("accretion, attracteur w* (beta=2,42)", -2.42/4.42),
               ("accretion, apres le festin (w -> 0)", 0.0),
               ("quintessence limite w = -0,9", -0.9)]:
    if w == -1.0:
        print(f"  {lab:38s} : H -> cte, S -> CONSTANTE, S'' -> 0^-   CONCAVE  [PASSE]")
    else:
        n = 2/(3*(1+w))
        print(f"  {lab:38s} : n = {n:.3f}, S ∝ t^2, S'' = {2/n**2:+.3f}   CONVEXE  [ECHOUE]")
print()
print("  => notre modèle échoue par DEUX routes indépendantes : pendant le festin (attracteur)")
print("     et après (retour matière). Le résultat ne dépend donc pas du sort du festin.")

print("\n" + "="*78)
print("  2. CALCUL NUMÉRIQUE, ENTROPIE TOTALE, AVEC ARRÊT DU FESTIN")
print("="*78)
OM, BETA, ZEQ = 0.3113, 2.418, 3387.0

def evolue(beta, t_end=None, N=300000, amax=60.0):
    """Intègre a(t) vers le futur. t_end en unités de t0 (None = festin sans fin)."""
    Or = OM/(1+ZEQ); Ode = 1-OM-Or
    # fond auto-cohérent jusqu'à a=1 pour fixer t0
    a = np.logspace(-7, 0, 60000)
    E2 = OM/a**3 + Or/a**4 + Ode
    for _ in range(10):
        E = np.sqrt(E2); ig = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]); t /= t[-1]
        E2 = OM/a**3 + Or/a**4 + Ode*np.clip(t,1e-300,None)**beta/a**3
    # intégration vers le futur en t
    dt = amax/N
    tt = 1.0 + np.arange(N)*dt*0.001
    aa = np.zeros(N); aa[0] = 1.0
    for i in range(1, N):
        T = tt[i-1]; A = aa[i-1]
        f = T if (t_end is None or T < t_end) else t_end
        E = np.sqrt(OM/A**3 + Or/A**4 + Ode*f**beta/A**3)
        aa[i] = A + A*E*(tt[i]-tt[i-1])
    E = np.array([np.sqrt(OM/A**3 + Or/A**4 + Ode*(min(T,t_end) if t_end else T)**beta/A**3)
                  for T, A in zip(tt, aa)])
    return tt, aa, E

for lab, beta, te in [("LCDM", None, None), ("accretion, festin sans fin", BETA, None),
                      ("accretion, festin fini a t=2,6 t0", BETA, 2.6)]:
    if beta is None:
        Or = OM/(1+ZEQ); Ode = 1-OM-Or
        tt = 1.0 + np.arange(300000)*60.0/300000*0.001
        aa = np.zeros_like(tt); aa[0] = 1.0
        for i in range(1, len(tt)):
            A = aa[i-1]; E = np.sqrt(OM/A**3 + Or/A**4 + Ode)
            aa[i] = A + A*E*(tt[i]-tt[i-1])
        E = np.sqrt(OM/aa**3 + Or/aa**4 + Ode)
    else:
        tt, aa, E = evolue(beta, te)
    S = 1/E**2
    dS = np.gradient(S, tt); d2S = np.gradient(dS, tt)
    print(f"\n  --- {lab}")
    print(f"      {'t/t0':>7s} {'z':>8s} {'S/S0':>10s} {'dS/dt':>10s} {'d2S/dt2':>11s}")
    for T in [1.0, 1.5, 2.0, 3.0, 6.0, 12.0]:
        j = np.argmin(np.abs(tt-T))
        if j >= len(tt)-2: continue
        print(f"      {T:>7.1f} {1/aa[j]-1:>8.3f} {S[j]/S[0]:>10.3f} {dS[j]:>10.3f} {d2S[j]:>+11.4f}")

print("\n" + "="*78)
print("  3. VERDICT")
print("="*78)
print("  Critère publié : S' > 0 et S'' < 0 quand z -> -1.")
print("  LCDM : S sature, S'' -> 0^- .................................. PASSE")
print("  accretion : S ∝ t^2 sans borne, S'' > 0 pour toujours ........ ECHOUE")
print("  et il échoue que le festin s'arrête ou non.")
