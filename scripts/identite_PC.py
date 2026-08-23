#!/usr/bin/env python3
"""
identite_PC.py — Le modele d'accretion est-il un modele de creation de particules ?

CADRE DE REFERENCE (source primaire lue : Schiavone, De Angelis, Escamilla, Montani,
Di Valentino, arXiv:2601.14222, PRD 2026 ; formalisme de Prigogine et al. 1989,
Calvao-Lima-Waga 1992) :
    continuite     : rho_E' + 3H(rho_E + p_E) = Gamma (rho_E + p_E)     [leur eq. 9]
    pression de creation : Pi = -(Gamma/3H)(rho_E + p_E)                [leur eq. 16]
    EoS effective  : w_DE^eff = w_E - (Gamma/3H)(1 + w_E)               [leur eq. 48]

NOTRE MODELE : rho_de = M_acc/V avec M_acc ∝ t^beta, d'ou w = -beta/(3Ht).

TEST 1 : avec w_E = 0 (particules creees sans pression = masse pure), leur eq. 48 donne
         w_DE^eff = -Gamma/(3H). Notre w = -(beta/t)/(3H). Donc Gamma = beta/t = Mdot/M ?
TEST 2 : nos deux equations de continuite coincident-elles exactement ?
TEST 3 : ou tombe notre Gamma dans leur espace de parametrisations (PC1-PC4) ?
TEST 4 : leur exclusion de w_E = 0 a 4.7-5.6 sigma s'applique-t-elle a nous ?
"""
import numpy as np
from scipy.optimize import curve_fit

BETA, OM, T0H0 = 2.42, 0.3153, 0.951     # Ht aujourd'hui, cf. corpus

# ---------- fond auto-coherent du modele d'accretion (meme routine que le corpus) ----------
a = np.logspace(-6, 0, 60000)
Or = OM/3387; Ode = 1-OM-Or
E2 = (OM+Ode)/a**3 + Or/a**4
for _ in range(8):
    E = np.sqrt(E2)
    integ = 1/(a*E)
    t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))]); t /= t[-1]
    E2 = (OM + Ode*np.clip(t, 1e-30, None)**BETA)/a**3 + Or/a**4
E = np.sqrt(E2); z = 1/a - 1
Ht = E*t/(E[-1]*t[-1])*T0H0          # H t en unites ou (Ht)_0 = 0.951
rho_de = Ode*np.clip(t, 1e-30, None)**BETA/a**3
w_nous = -BETA/(3*np.clip(Ht, 1e-9, None))

print("="*80)
print("  TEST 1 : leur w_DE^eff = w_E - (Gamma/3H)(1+w_E) avec w_E = 0")
print("="*80)
Gamma_sur_3H = BETA/(3*Ht)            # = beta/(3Ht)  <=>  Gamma = beta/t
w_PC = 0 - Gamma_sur_3H*(1+0)
i0 = -1
print(f"  Gamma = beta/t = Mdot/M  ->  Gamma/(3H) aujourd'hui = {Gamma_sur_3H[i0]:.5f}")
print(f"  leur w_DE^eff (w_E=0)    = {w_PC[i0]:.6f}")
print(f"  notre w = -beta/(3Ht)    = {w_nous[i0]:.6f}")
print(f"  ecart maximal sur 0<z<5  = {np.max(np.abs(w_PC-w_nous)[(z>=0)&(z<=5)]):.2e}  -> IDENTITE EXACTE")

print("\n" + "="*80)
print("  TEST 2 : les deux equations de continuite coincident-elles ?")
print("="*80)
print("  Eux (w_E=0)      : d(rho_E a^3)/dt = Gamma rho_E a^3")
print("  Nous             : d(rho_de V)/dt  = Mdot")
print("  Avec Gamma = Mdot/M et rho_de V = M_acc, le membre de droite vaut (Mdot/M) x M = Mdot.")
M = rho_de*a**3
dMdt = np.gradient(M, t)
src = (BETA/np.clip(t,1e-30,None))*M
m = (z>=0)&(z<=5)
err = np.max(np.abs(dMdt[m]-src[m])/np.abs(src[m]))
print(f"  verification numerique : ecart relatif max sur 0<z<5 = {err:.2e}  -> MEME EQUATION")
print("  => notre 'injection externe' est exactement leur 'creation adiabatique' avec")
print("     une pression de creation Pi = -(Gamma/3H) rho_de. Le tenseur total est conserve.")

print("\n" + "="*80)
print("  TEST 3 : ou tombe notre Gamma dans LEUR espace de parametrisations ?")
print("="*80)
mm = (z>=0)&(z<=3)
Ez, Gz = E[mm]/E[-1], (BETA/t[mm])
# PC1 : Gamma = 3 beta_PC H0 (H/H0)^alpha  ->  Gamma/H0 = 3 beta_PC E^alpha
H0u = E[-1]*T0H0/t[-1]     # H0 dans les memes unites que Gamma
y = Gz/H0u
def pc1(Ex, b, al): return 3*b*Ex**al
popt, _ = curve_fit(pc1, Ez, y, p0=[0.8, 1.0], maxfev=20000)
res = np.max(np.abs(pc1(Ez, *popt)-y)/y)
print(f"  ajustement PC1 (Gamma = 3 beta_PC H0 E^alpha) sur 0<z<3 :")
print(f"     beta_PC = {popt[0]:.3f}   alpha = {popt[1]:.3f}   residu relatif max = {res*100:.1f} %")
print(f"  leurs contraintes PC1 (jeu complet) : beta_PC = 0.62 (+0.75/-0.43), alpha = 2.1 (+1.2/-1.8)")
lo_b, hi_b = 0.62-0.43, 0.62+0.75
lo_a, hi_a = 2.1-1.8, 2.1+1.2
print(f"     -> beta_PC dans l'intervalle 68 % ? {'OUI' if lo_b<=popt[0]<=hi_b else 'NON'}"
      f"   alpha dans l'intervalle 68 % ? {'OUI' if lo_a<=popt[1]<=hi_a else 'NON'}")
# PC2 equivalent instantane
mu_eq = Gamma_sur_3H[i0]
xi_eq = 3*(1+0)*(1-mu_eq)
print(f"\n  equivalent PC2 instantane (Gamma = 3 mu H) : mu = {mu_eq:.3f}, xi = 3(1+w_E)(1-mu) = {xi_eq:.3f}")
print(f"     -> w_DE^eff = -1 + xi/3 = {-1+xi_eq/3:.4f}   (notre w0 publie : -0.848)")
print(f"     leur contrainte PC2 : xi = -0.011 +/- 0.073  ->  notre xi = {xi_eq:.3f} est a"
      f" {(xi_eq+0.011)/0.073:.1f} sigma")

print("\n" + "="*80)
print("  TEST 4 : leur exclusion de w_E = 0 nous atteint-elle ?")
print("="*80)
print("  Ils excluent la creation de matiere SANS PRESSION (w_E = 0) a 4.7 / 5.6 / 5.4 sigma")
print("  dans PC1 / PC3 / PC4. Or notre modele EST w_E = 0. Deux remarques, dans l'ordre :")
print("  (a) leur exclusion est obtenue A L'INTERIEUR de leurs familles de Gamma. Notre")
print("      Gamma = beta/t n'y figure pas ; l'ajustement PC1 ci-dessus montre a quel point")
print("      il en est proche ou loin.")
print("  (b) leur PC2 avec w_E = 0 exige mu = 1 - xi/3 ~ 1.004 : leur xi ~ 0 est compatible")
print("      avec w_E = 0 SI Gamma ~ 3H. Notre mu = %.3f en est a %.0f %% pres." % (mu_eq, abs(mu_eq-1)*100))
print("  => l'exclusion n'est PAS automatiquement transferable, mais elle est le premier")
print("     test externe serieux que le modele doit passer. Statut : A FAIRE, non acquis.")

print("\n" + "="*80)
print("  EVOLUTION DE Gamma/3H : la signature qui nous distingue de leurs quatre familles")
print("="*80)
print(f"  {'z':>6s} {'Ht':>8s} {'Gamma/3H':>10s} {'w_eff':>9s}  {'PC2 (mu const) predirait':>26s}")
for zz in [0.0, 0.3, 0.5, 1.0, 2.0, 3.0]:
    j = np.argmin(np.abs(z-zz))
    print(f"  {zz:>6.1f} {Ht[j]:>8.4f} {Gamma_sur_3H[j]:>10.4f} {w_nous[j]:>9.4f}  {-1+xi_eq/3:>26.4f}")
print("\n  Gamma/3H = beta/(3Ht) DECROIT vers le passe (Ht -> 2/3 en domination de matiere,")
print("  donc Gamma/3H -> beta/2 = %.2f) et CROIT vers le futur : c'est une cinquieme famille," % (BETA/2))
print("  Gamma ∝ 1/t, absente de leur tableau I — et la seule dont le taux soit DERIVE")
print("  (Gamma = Mdot/M du parent) au lieu d'etre postule.")
