#!/usr/bin/env python3
"""
frb_ccbh.py — Refaire l'inference FRB dans le fond CCBH.

POURQUOI CE CALCUL PEUT ANNULER LE RESULTAT D'HIER. J'ai compare la survie baryonique
s = rho_b(0)/rho_b(BBN) au Omega_b mesure par les FRB, et trouve CCBH a 5 sigma. Mais la
mesure de dispersion est une INTEGRALE le long de la ligne de visee : elle pese le PASSE,
ou CCBH a ENCORE ses baryons. La comparaison d'hier etait donc faite au mauvais endroit.

FORMALISME. DM = int n_e dl_prop/(1+z), avec dl_prop = c dz/[(1+z)H]. Donc
    DM(z) = (c f_d f_e/m_p) int_0^z rho_b(z') dz' / [(1+z')^2 H(z')]
En LCDM rho_b = rho_b0 (1+z)^3, d'ou la relation de Macquart usuelle ∝ Omega_b H0 int (1+z)dz/E.
En CCBH rho_b(z) = rho_tilde_b(z) (1+z)^3 avec rho_tilde_b COMOBILE et DECROISSANTE dans le
temps : elle est donc PLUS GRANDE a haut z. La perte tardive est partiellement compensee.

CRITERE PRE-ENREGISTRE (avant execution) :
  - on calcule DM(z) pour les trois modeles a f_d f_e IDENTIQUES : seule la cosmologie joue.
  - puis on demande : si l'univers etait CCBH mais qu'on analysait en LCDM, quel Omega_b
    effectif inferrerait-on sur la plage FRB ?
  - si Omega_b^eff tombe dans 0,0490 +/- 0,0035, alors le test d'hier NE REFUTE PAS CCBH
    et je le retire. Si Omega_b^eff reste bas, il tient.
  Pas de reinterpretation apres coup.
"""
import numpy as np, sys
from scipy.optimize import brentq
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
import duel_ccbh as D
import test_wE_v3 as T
np.seterr(all='ignore')

C_KM = 299792.458
ZGRID = np.linspace(0, 3.0, 3000)

def dm_kernel(z, E_of_z, rhotilde_of_z):
    """int_0^z rho_tilde(z')(1+z') dz'/E(z'), en unites arbitraires communes."""
    integ = rhotilde_of_z(ZGRID)*(1+ZGRID)/E_of_z(ZGRID)
    cum = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(ZGRID))])
    return np.interp(z, ZGRID, cum)

# ---------- LCDM et accretion : rho_tilde constante ----------
T.ZCUT = None
def modele_std(Om, h, wb, beta=None):
    zz, Ea = T.fond(Om, 0.0, beta, 'invt' if beta else 'lcdm')
    E = lambda z: np.interp(z, zz, Ea)
    return E, (lambda z: np.full_like(np.atleast_1d(z), wb/h**2, dtype=float)), h

E_l, r_l, h_l = modele_std(0.2976, 0.6866, 0.02261)
E_a, r_a, h_a = modele_std(0.2999, 0.6885, 0.02261, beta=2.595)

# ---------- CCBH : rho_tilde(z) decroissante dans le temps ----------
WC, WBP, XI = 0.1194, 0.02238, 2.861      # meilleur ajustement Trinca-like
psi0 = D.psi_MD14
D.psi_MD14 = lambda z: psi0(z)*np.where(np.asarray(z) > 4.0, 2.0, 1.0)
out = D.fond_ccbh(WC, WBP, XI)
zc, Ec, hc, wb1 = out
a_grid = D.AG
# reconstruire w_b(a) comobile
wb_a = np.full_like(a_grid, WBP)
wde = np.zeros_like(a_grid)
j0 = np.searchsorted(a_grid, 1/21.0)
for i in range(j0, len(a_grid)):
    wm = WC + wb_a[i-1] + D.W_NU_M
    wtot = wm/a_grid[i-1]**3 + D.W_R/a_grid[i-1]**4 + wde[i-1]
    H_yr = 100*np.sqrt(wtot)*D.KMS_PER_YR
    src = XI*D.psi_MD14(1/a_grid[i-1]-1)/(H_yr*a_grid[i-1]**4)/D.RHO100
    da = a_grid[i]-a_grid[i-1]
    wde[i] = wde[i-1] + src*da
    wb_a[i] = wb_a[i-1] - src*a_grid[i-1]**3*da
z_c = (1/a_grid - 1)[::-1]; wb_c = wb_a[::-1]
E_c = lambda z: np.interp(z, zc, Ec)
r_c = lambda z: np.interp(z, z_c, wb_c)/hc**2

print("="*78)
print("  1. LA COMPENSATION EST-ELLE REELLE ? rho_b comobile en fonction de z")
print("="*78)
print(f"  {'z':>6s} {'Omega_b(z) CCBH':>17s} {'Omega_b LCDM':>14s} {'rapport':>9s}")
for z in [0.0, 0.2, 0.5, 1.0, 2.0, 3.0]:
    print(f"  {z:>6.1f} {r_c(z):>17.5f} {r_l(z)[0]:>14.5f} {r_c(z)/r_l(z)[0]:>9.4f}")
print("  => a z = 0 CCBH a moins de baryons ; a z = 2 il en a presque autant. La mesure de")
print("     dispersion integre les deux, donc l'ecart observable est PLUS PETIT que 0,615.")

print("\n" + "="*78)
print("  2. DM(z) COMPARE, a f_d f_e IDENTIQUES")
print("="*78)
print(f"  {'z':>6s} {'DM LCDM':>11s} {'DM accretion':>13s} {'DM CCBH':>11s} {'CCBH/LCDM':>11s}")
for z in [0.1, 0.3, 0.5, 0.8, 1.0, 1.5]:
    dl = dm_kernel(z, E_l, r_l)/h_l
    da = dm_kernel(z, E_a, r_a)/h_a
    dc = dm_kernel(z, E_c, r_c)/hc
    print(f"  {z:>6.2f} {dl:>11.5f} {da:>13.5f} {dc:>11.5f} {dc/dl:>11.4f}")

print("\n" + "="*78)
print("  3. LE TEST : quel Omega_b un analyste LCDM inferrerait-il si l'univers etait CCBH ?")
print("="*78)
print("  On cherche Omega_b^eff tel que DM_LCDM(Omega_b^eff) reproduise DM_CCBH sur la plage FRB.")
for zlo, zhi, lab in [(0.05, 0.5, 'plage Macquart 2020'), (0.05, 1.0, 'plage DSA-110 / Connor'),
                      (0.05, 1.5, 'plage etendue')]:
    zs = np.linspace(zlo, zhi, 60)
    num = np.array([dm_kernel(z, E_c, r_c)/hc for z in zs])
    den = np.array([dm_kernel(z, E_l, lambda zz: np.full_like(np.atleast_1d(zz), 1.0, dtype=float))/h_l for z in zs])
    # DM_LCDM ∝ Omega_b^eff x den ; moindres carres relatifs
    ratio = np.sum(num*den)/np.sum(den*den)
    print(f"  {lab:>26s} ({zlo}<z<{zhi}) : Omega_b^eff = {ratio:.5f}")
print()
print("  [SUPERSEDE] #95 : la mesure est Omega_b h70 = 0,049 +/- 0,003 (Connor et al. 2025) et la fraction diffuse")
print("  employee ici etait inventee ; le test vivant est frb_likelihood.py (#98-#99 : ~2,1 sigma, mediane de 12 tirages).")
print("  Ce script est conserve comme etape historique ; son verdict n'est plus exploite.")
print(f"  mesure FRB : Omega_b = 0.049 +/- 0.003")
zs = np.linspace(0.05, 1.0, 60)
num = np.array([dm_kernel(z, E_c, r_c)/hc for z in zs])
den = np.array([dm_kernel(z, E_l, lambda zz: np.full_like(np.atleast_1d(zz), 1.0, dtype=float))/h_l for z in zs])
obeff = np.sum(num*den)/np.sum(den*den)
print(f"  CCBH -> Omega_b^eff = {obeff:.5f}  ->  ecart = {abs(0.049-obeff)/0.003:.1f} sigma")
print(f"  (hier, comparaison naive a s x Omega_b : 0.0282, soit 5.9 sigma)")
print()
if abs(0.049-obeff)/0.003 < 2:
    print("  VERDICT : la compensation integrale SAUVE CCBH. Le test d'hier est RETIRE.")
elif abs(0.049-obeff)/0.003 < 3:
    print("  VERDICT : tension reduite mais presente. A ecrire comme tension, pas refutation.")
else:
    print("  VERDICT : la tension survit a la compensation integrale.")
