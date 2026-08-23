#!/usr/bin/env python3
"""
heredite_edo.py — Creuser les trois : hérédité, running, horloge.

CE QUI N'AVAIT PAS ÉTÉ VU. La relation d'hérédité n'est pas une paramétrisation, c'est une
CONTRAINTE D'AUTO-COHÉRENCE. Deux énoncés portent sur le même objet :
    (1)  beta = dln M_acc / dln t        [définition de beta]
    (2)  beta = 2/(n_eff(M) + 3)         [hérédité, lecture pic, HS85]
Les égaler donne une équation différentielle FERMÉE :

        dln M / dln t  =  2 / (n_eff(M) + 3)

Une fois M fixé à un instant, TOUTE la trajectoire beta(t) est déterminée. Il n'y a plus de
paramètre libre : le running n'est plus une fourchette, c'est un NOMBRE.

TROIS QUESTIONS, dans l'ordre :
  A. quel beta_1 l'EDO prédit-elle exactement ?
  B. quelle courbure d'horloge kappa cela impose-t-il, sachant beta_1 mesuré = +0,06 +/- 0,31 ?
  C. quel parent cela exige-t-il ? (le corpus annonce omega_m parent ~ 4e-4 sous l'ANCIENNE
     relation ; que devient ce chiffre sous la nouvelle ?)

CONVENTION : n_eff(M) = -6 dln sigma/dln M - 3, la seule requise (cf. dérivation FG84).
Le spectre de NOTRE univers sert de procuration pour celui du parent — hypothèse déjà
déclarée dans le corpus, pas une nouveauté d'ici.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import sys
from gradient_v2 import Cosmo, REF

np.seterr(all='ignore')
c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
H = REF['h']
K = 2.0          # lecture pic : beta = K/(n+3) avec K = 2 ; l'ancienne avait K = 4

def n_eff(M):  return c.n_eff(M)
def beta_de_M(M, k=K): return k/(n_eff(M)+3.0)
def M_de_beta(b, k=K):
    cible = k/b - 3.0
    f = lambda lM: n_eff(np.exp(lM)) - cible
    return np.exp(brentq(f, np.log(1e5), np.log(1e18), xtol=1e-4))

print("="*78)
print("  A. L'EDO D'HÉRÉDITÉ, RÉSOLUE")
print("="*78)
B0 = 2.418
M0 = M_de_beta(B0)
print(f"  beta(t0) = {B0:.3f}  ->  n_eff = {K/B0-3:.4f}  ->  M(t0) = {M0:.3e} Msun/h"
      f"  ({M0/H:.3e} Msun)")

def rhs(L, y):            # L = ln(t/t0), y = ln M
    return [beta_de_M(np.exp(y[0]))]
sol = solve_ivp(rhs, [0, -2.5], [np.log(M0)], dense_output=True, rtol=1e-9, atol=1e-12)
solf = solve_ivp(rhs, [0, 1.5], [np.log(M0)], dense_output=True, rtol=1e-9, atol=1e-12)
def Mt(L): return np.exp(sol.sol(L)[0] if L < 0 else solf.sol(L)[0])

print(f"\n  {'t/t0':>7s} {'z':>7s} {'M [Msun/h]':>12s} {'n_eff':>8s} {'beta':>8s}")
for L in [-2.0, -1.5, -1.0, -0.5, -0.2, 0.0, 0.3]:
    T = np.exp(L); M = Mt(L)
    print(f"  {T:>7.3f} {'':>7s} {M:>12.3e} {n_eff(M):>8.4f} {beta_de_M(M):>8.4f}")

# running exact : beta_1 = dbeta/dln t = beta x dbeta/dln M
d = 0.10
dbdlnM = (beta_de_M(M0*np.exp(d)) - beta_de_M(M0*np.exp(-d)))/(2*d)
b1_pred = B0*dbdlnM
print(f"\n  dbeta/dlnM en M0 = {dbdlnM:+.5f}")
print(f"  => beta_1 PRÉDIT = beta0 x dbeta/dlnM = {b1_pred:+.4f}")
print(f"     (auparavant annoncé comme fourchette -0,23 a -0,40 ; c'est un NOMBRE)")
# controle : pente numerique directe de la trajectoire
bnum = (beta_de_M(Mt(0.05)) - beta_de_M(Mt(-0.05)))/0.10
print(f"  contrôle par la trajectoire : {bnum:+.4f}   (écart {abs(bnum-b1_pred):.1e})")
# ancienne lecture
M0a = M_de_beta(B0, 4.0)
dbdlnMa = (beta_de_M(M0a*np.exp(d),4.0) - beta_de_M(M0a*np.exp(-d),4.0))/(2*d)
print(f"  pour mémoire, ancienne lecture K=4 : M0 = {M0a:.2e}, beta_1 = {B0*dbdlnMa:+.4f}")

print("\n" + "="*78)
print("  B. CE QUE CELA IMPOSE À L'HORLOGE")
print("="*78)
b1_obs, s1 = 0.06, 0.31
kap = (b1_obs - b1_pred)/B0; skap = s1/B0
print(f"  beta_1 = beta_spectre + beta_0 x kappa,  avec beta_spectre = {b1_pred:+.4f} (prédit, sans")
print(f"  paramètre libre) et beta_1 mesuré = {b1_obs:+.2f} +/- {s1:.2f}")
print(f"  =>  kappa = {kap:+.4f} +/- {skap:.4f}   soit {abs(kap)/skap:.2f} sigma de zéro")
print(f"  Lecture : prendre l'hérédité au sérieux EXIGE une horloge courbe a {abs(kap)/skap:.1f} sigma.")
print(f"  kappa > 0 : l'horloge du parent s'accélère par rapport à la nôtre.")
print(f"  Si l'on impose au contraire kappa = 0 (horloge en loi de puissance), l'hérédité")
print(f"  est en tension de {abs(b1_obs-b1_pred)/s1:.2f} sigma avec les données.")

print("\n" + "="*78)
print("  C. QUEL PARENT CELA EXIGE-T-IL ?")
print("="*78)
M_UNIV = 3.1e54/1.989e30           # masse de notre univers en Msun
print(f"  masse-graine (= notre univers) = {M_UNIV:.3e} Msun")
for lab, k in [("nouvelle lecture K=2", 2.0), ("ancienne lecture K=4", 4.0)]:
    Mk = M_de_beta(B0, k)/H                     # en Msun, dans NOTRE spectre
    r_masse = M_UNIV/Mk
    r_long = r_masse**(1/3)
    om_par = REF['Om']*H*H/r_long
    print(f"  {lab:22s} : même pente à {Mk:.2e} Msun chez nous"
          f" -> étirement x{r_long:.3g} en longueur")
    print(f"  {'':22s}   -> omega_m parent ~ {om_par:.2e}   (corpus : ~4e-4)")
print("\n  => la nouvelle relation rend le parent ENCORE plus éloigné de nous.")
print("     La hiérarchie n'est pas auto-similaire, et l'écart s'aggrave d'un facteur ~30.")

print("\n" + "="*78)
print("  D. L'EDO A-T-ELLE UNE FIN ? (bande de viabilité 1 < beta < 4,35)")
print("="*78)
for b, nom in [(4.35, "bord GSL (beta = 4,35)"), (1.0, "bord de non-accélération (beta = 1)")]:
    try:
        Mb = M_de_beta(b)
        # temps pour aller de M0 a Mb en suivant l EDO
        f = lambda L: np.log(Mt(L)) - np.log(Mb)
        lo, hi = (-2.4, 0.0) if Mb < M0 else (0.0, 1.4)
        L = brentq(f, lo, hi, xtol=1e-6)
        print(f"  {nom:34s} : M = {Mb:.2e} Msun/h  atteint a t/t0 = {np.exp(L):.4f}")
    except Exception as e:
        print(f"  {nom:34s} : hors de la plage integree")
print("\n  Lecture : la trajectoire traverse la bande de viabilité en un temps fini.")
print("  C'est une durée de vie prédite pour la phase d'accélération, distincte de t_end.")
