#!/usr/bin/env python3
"""
cmb_evidence.py — Le test qui peut tuer le modele + evidences bayesiennes
1) Ajout de la contrainte geometrique CMB (theta* de Planck, 0.03%) a la
   vraisemblance BAO+SN. Notre modele eteint son energie noire en t^beta aux
   hauts z : theta* teste si la forme bas-z compatible BAO+SN reste compatible
   avec la distance a la recombinaison. r* et rd sont inchanges (physique
   pre-recombinaison intacte, rho_de/rho_m ~ 1e-11 a z*).
2) Evidences bayesiennes par integration directe sur les priors (dimensions
   faibles : 1D/2D/3D), M et q profiles analytiquement (approx. de Laplace
   pour q, exacte pour M).
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from vraisemblance_reelle import (BAO, d_bao, Cinv_bao, C_bao, z_sn, mb,
                                   Cinv_sn, Cinv_one, oCo, one, zg,
                                   E_lcdm, E_acc, ZEQ)

# ---- Contrainte CMB compressee (Planck 2018) ----
# 100*theta* = 1.04109 +/- 0.00030 ; r* = 144.43 Mpc ; rd = 147.09 Mpc
# => point effectif a z*=1089 : DM/rd = (1/theta*)*(r*/rd) = 94.32 +/- 0.027
ZSTAR = 1089.0
CMB_VAL = (1/0.0104109)*(144.43/147.09)
CMB_SIG = CMB_VAL*(0.00030/1.04109)

# covariance jointe BAO+CMB (bloc diagonal) pour le profilage de q
C14 = np.zeros((14,14)); C14[:13,:13] = C_bao; C14[13,13] = CMB_SIG**2
Cinv14 = np.linalg.inv(C14)
d14 = np.concatenate([d_bao,[CMB_VAL]])

def chi2_tot(Efunc, use_cmb=True):
    Ez = Efunc(zg); inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(zg))])
    mu = 5*np.log10((1+z_sn)*np.interp(z_sn, zg, Dc))
    r = mb - mu
    chi2_sn = r@Cinv_sn@r - (r@Cinv_one)**2/oCo
    u = np.zeros(14)
    for i,(z,typ,_,_,_) in enumerate(BAO):
        DM_ = np.interp(z, zg, Dc); DH_ = 1/np.interp(z, zg, Ez)
        u[i] = {'M':DM_,'H':DH_,'V':(z*DM_**2*DH_)**(1/3)}[typ]
    u[13] = np.interp(ZSTAR, zg, Dc)
    if use_cmb:
        q = (u@Cinv14@d14)/(u@Cinv14@u); rb = d14 - q*u
        return chi2_sn + rb@Cinv14@rb
    q = (u[:13]@Cinv_bao@d_bao)/(u[:13]@Cinv_bao@u[:13]); rb = d_bao - q*u[:13]
    return chi2_sn + rb@Cinv_bao@rb

# ---------- Fits avec CMB ----------
print("=== BAO + SN + CMB(theta*) ===")
f_l = lambda Om: chi2_tot(lambda z: E_lcdm(z,Om))
rl = minimize_scalar(f_l, bounds=(0.25,0.40), method='bounded')
c_l = rl.fun; print(f"LCDM      Om={rl.x:.4f}                          chi2={c_l:.2f}")

f_c = lambda p: chi2_tot(lambda z: E_lcdm(z,p[0],p[1],p[2]))
rc = minimize(f_c, x0=[0.32,-0.80,-0.7], method='Nelder-Mead',
              options=dict(xatol=1e-3,fatol=1e-3,maxiter=500))
c_c = rc.fun
print(f"w0waCDM   Om={rc.x[0]:.4f} w0={rc.x[1]:+.3f} wa={rc.x[2]:+.3f}  chi2={c_c:.2f}  Dchi2={c_c-c_l:+.2f}")

f_a = lambda p: chi2_tot(lambda z: E_acc(z,p[0],p[1]))
ra = minimize(f_a, x0=[0.32,2.4], method='Nelder-Mead',
              options=dict(xatol=1e-3,fatol=1e-3,maxiter=300))
c_a = ra.fun
print(f"Accretion Om={ra.x[0]:.4f} beta={ra.x[1]:.3f}            chi2={c_a:.2f}  Dchi2={c_a-c_l:+.2f}")
print(f"\nAIC : LCDM={c_l+2:.2f}  CPL={c_c+6:.2f}  ACC={c_a+4:.2f}")

# ---------- Evidences bayesiennes (integration directe) ----------
print("\n=== Evidences bayesiennes (priors uniformes) ===")
print("Priors : Om~U(0.25,0.40) ; w0~U(-2,0) ; wa~U(-3,2) ; beta~U(0.5,5)")
cmin = min(c_l, c_c, c_a)

# LCDM : 1D
Oms = np.linspace(0.25,0.40,120)
L = np.exp(-0.5*(np.array([f_l(o) for o in Oms])-cmin))
Z_l = np.trapezoid(L,Oms)/0.15

# CPL : 3D (grille centree sur le best-fit, bornee au prior)
o0,w00,wa0 = rc.x
og = np.linspace(max(0.25,o0-0.03),min(0.40,o0+0.03),16)
wg = np.linspace(max(-2,w00-0.45),min(0,w00+0.45),18)
ag = np.linspace(max(-3,wa0-1.8),min(2,wa0+1.8),18)
Lc = np.zeros((len(og),len(wg),len(ag)))
for i,o in enumerate(og):
    for j,w in enumerate(wg):
        for k,a in enumerate(ag):
            Lc[i,j,k] = np.exp(-0.5*(chi2_tot(lambda z: E_lcdm(z,o,w,a))-cmin))
Z_c = np.trapezoid(np.trapezoid(np.trapezoid(Lc,ag,axis=2),wg,axis=1),og)/(0.15*2.0*5.0)

# ACC : 2D
oa0,b0 = ra.x
og2 = np.linspace(max(0.25,oa0-0.03),min(0.40,oa0+0.03),20)
bg  = np.linspace(max(0.5,b0-1.2),min(5,b0+1.2),24)
La = np.zeros((len(og2),len(bg)))
for i,o in enumerate(og2):
    for j,b in enumerate(bg):
        La[i,j] = np.exp(-0.5*(chi2_tot(lambda z: E_acc(z,o,b))-cmin))
Z_a = np.trapezoid(np.trapezoid(La,bg,axis=1),og2)/(0.15*4.5)

lnB_al = np.log(Z_a/Z_l); lnB_cl = np.log(Z_c/Z_l); lnB_ac = np.log(Z_a/Z_c)
print(f"ln B(ACC/LCDM) = {lnB_al:+.2f}")
print(f"ln B(CPL/LCDM) = {lnB_cl:+.2f}")
print(f"ln B(ACC/CPL)  = {lnB_ac:+.2f}")
print("(Jeffreys : |lnB|<1 non concluant ; 1-2.5 faible ; 2.5-5 modere ; >5 fort)")
