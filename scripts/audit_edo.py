#!/usr/bin/env python3
"""
audit_edo.py — Quatre contrôles sur l'EDO d'hérédité.

(1) INVARIANCE : j'ai intégré l'EDO avec le spectre de NOTRE univers, alors que le calcul du
    parent exige omega_m ~ 1e-5. Incohérent ? A vérifier : si le spectre du parent n'est que
    le nôtre étiré en masse, dn_eff/dlnM à n_eff donné est invariant, et beta_1 aussi.
(2) COHÉRENCE INTERNE : j'ai cité beta(t0) = 2,418 puis 2,62 dans le même document, d'où deux
    masses-graines différentes (7,4e11 et 2,4e11 Msun). A trancher et à borner.
(3) EXTRAPOLATION : j'ai annoncé une "sortie de bande" à 1,3e4 Ga en intégrant l'EDO vers le
    futur. Or le festin s'arrête à t_end = 16-36 Ga, après quoi dlnM/dlnt = 0. L'extrapolation
    est-elle valide ?
(4) LE CONTRÔLE DUR : l'EDO prédit qu'un halo de masse M croît à dlnM/dlnt = beta. Ce taux est
    MESURÉ en simulation. Formule analytique de Correa, Wyithe, Schaye & Duffy (MNRAS 450, 1521,
    2015), calibrée sur simulations :
        M(z) = M0 (1+z)^{alpha f} exp(-f z)
        alpha = 1.686 sqrt(2/pi) dD/dz|_0 + 1
        f(M0) = 1/sqrt(S(M0/q) - S(M0)),  S = sigma^2
        q = 4.137 zf^-0.9476,  zf = -0.0064 (log10 M0)^2 + 0.0237 log10 M0 + 1.8837
    d'où dlnM/dlna|_0 = f(1-alpha) et beta_sim = dlnM/dlnt = (Ht) f (1-alpha).
    SI beta_sim(M0) != beta_EDO(M0), la relation d'hérédité est en conflit avec les simulations.
"""
import numpy as np, sys
from scipy.optimize import brentq
sys.path.insert(0, '/home/claude/selection')
from gradient_v2 import Cosmo, REF
np.seterr(all='ignore')

H, HT0 = REF['h'], 0.951
c = Cosmo(REF['Om'], REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])

print("="*78)
print("  (1) L'EDO est-elle invariante si le parent a un autre omega_m ?")
print("="*78)
print("  Si le spectre du parent est le nôtre ÉTIRÉ en masse (même n_s, même f_b), alors")
print("  n_eff(M) = F(M/M_eq) et dn_eff/dlnM à n_eff FIXÉ est le même. Test numérique :")
print(f"  {'omega_m':>9s} {'M(n_eff=-2,17)':>16s} {'dn_eff/dlnM la':>16s}")
for om in [0.1430, 0.0715, 0.0286, 0.0143]:
    h2 = om/(REF['h']**2)
    cc = Cosmo(h2, REF['Ob'], REF['h'], REF['ns'], s8=REF['s8'])
    try:
        M = np.exp(brentq(lambda lM: cc.n_eff(np.exp(lM))+2.1729, np.log(1e2), np.log(1e19), xtol=1e-4))
        d = (cc.n_eff(M*np.e) - cc.n_eff(M/np.e))/2.0
        print(f"  {om:>9.4f} {M:>16.3e} {d:>16.5f}")
    except Exception as e:
        print(f"  {om:>9.4f}  hors plage")
print("  => si la dernière colonne est stable, beta_1 ne dépend pas de omega_m du parent.")

print("\n" + "="*78)
print("  (2) SENSIBILITÉ À beta(t0) : quelle masse-graine, quel beta_1 ?")
print("="*78)
def M_de_beta(b, k=2.0):
    return np.exp(brentq(lambda lM: c.n_eff(np.exp(lM)) - (k/b-3.0), np.log(1e4), np.log(1e18), xtol=1e-4))
def beta1_de(b, k=2.0):
    M = M_de_beta(b, k); d = 0.10
    return b*(k/(c.n_eff(M*np.exp(d))+3) - k/(c.n_eff(M*np.exp(-d))+3))/(2*d), M
print(f"  {'beta0':>7s} {'source':>26s} {'M0 [Msun]':>12s} {'beta_1':>9s}")
for b, src in [(2.418, 'fond v3 (croissance.py)'), (2.49, 'papier A, post-verif'),
               (2.56, 'profil Planck complet'), (2.595, 'ajustement v3'), (2.62, 'ajustement avec running')]:
    b1, M = beta1_de(b)
    print(f"  {b:>7.3f} {src:>26s} {M/H:>12.3e} {b1:>+9.4f}")
print("  => beta_1 varie de ~15 % sur la plage plausible de beta0. A citer avec cette barre.")

print("\n" + "="*78)
print("  (3) L'EXTRAPOLATION VERS LE FUTUR EST-ELLE LÉGITIME ?")
print("="*78)
print("  Le festin s'arrête à t_end = t0 (M_res/M_acc)^(1/beta) = 16-36 Ga (corpus).")
print("  Après t_end : M_acc gèle, donc dlnM/dlnt = 0, donc beta chute à 0 — il ne DÉCLINE pas")
print("  lentement jusqu'à 1. L'EDO ne gouverne beta que PENDANT le festin.")
for te in [16.0, 36.0]:
    print(f"    t_end = {te:.0f} Ga = {te/13.8:.2f} t0  ->  beta y vaut encore "
          f"{2.418 + (-0.478)*np.log(te/13.8):.3f} avant de tomber à 0")
print("  => ma 'sortie de bande à 1,3e4 Ga' extrapolait l'EDO bien au-delà de sa validité.")
print("     RETIRÉ. Il n'y a pas deux horloges de fin à réconcilier : il n'y en a qu'une, t_end.")

print("\n" + "="*78)
print("  (4) CONTRÔLE DUR : l'EDO contre la croissance des halos mesurée en simulation")
print("="*78)
# facteur de croissance et dD/dz en z=0
def D_and_dDdz(Om, n=200000):
    a = np.linspace(1e-6, 1.0, n)
    E = np.sqrt(Om/a**3 + (1-Om))
    I = np.concatenate([[0], np.cumsum(0.5*(1/(a[1:]*E[1:])**3 + 1/(a[:-1]*E[:-1])**3)*np.diff(a))])
    D = 2.5*Om*E*I
    D0 = D[-1]
    fgrow = REF['Om']**0.55
    return D0, -D0*fgrow      # dD/dz|_0 = -D0 * f  (D normalisé à sa valeur en a=1)
D0, dDdz = D_and_dDdz(REF['Om'])
alpha = 1.686*np.sqrt(2/np.pi)*(dDdz/D0) + 1.0
print(f"  alpha = 1,686 sqrt(2/pi) dD/dz|0 + 1 = {alpha:.4f}   (dD/dz|0 / D0 = {dDdz/D0:.4f})")

def beta_sim(M0_msun):
    """beta = dlnM/dlnt en z=0 selon Correa et al. 2015. M0 en Msun."""
    l = np.log10(M0_msun)
    zf = -0.0064*l**2 + 0.0237*l + 1.8837
    q = 4.137*zf**(-0.9476)
    Mh = M0_msun*H                      # -> Msun/h pour sigma
    S1 = c.sig_M(Mh/q)**2; S2 = c.sig_M(Mh)**2
    if S1 <= S2: return np.nan
    f = 1/np.sqrt(S1-S2)
    return HT0*f*(1-alpha)

print(f"\n  {'M0 [Msun]':>12s} {'beta_sim (Correa)':>18s} {'beta EDO requis':>16s}")
for M0 in [1e11, 2.4e11, 1e12, 1e13, 1e14, 8.2e14, 1e15, 1e16]:
    bs = beta_sim(M0)
    be = 2.0/(c.n_eff(M0*H)+3)
    print(f"  {M0:>12.1e} {bs:>18.3f} {be:>16.3f}")
print("\n  Et : existe-t-il une masse où la simulation donne beta = 2,42-2,62 ?")
for cible in [2.418, 2.62]:
    try:
        Ms = np.exp(brentq(lambda lM: beta_sim(np.exp(lM))-cible, np.log(1e10), np.log(1e17), xtol=1e-3))
        print(f"    beta_sim = {cible:.3f} atteint à M = {Ms:.3e} Msun")
    except Exception:
        print(f"    beta_sim = {cible:.3f} : AUCUNE masse dans 1e10-1e17 Msun ne l'atteint")
print(f"    beta_sim maximal sur la plage : {max(beta_sim(m) for m in np.logspace(10,17,60)):.3f}")
