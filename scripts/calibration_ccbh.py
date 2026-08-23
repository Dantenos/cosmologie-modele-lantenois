#!/usr/bin/env python3
"""
calibration_ccbh.py — Contourner l'absence de la compilation Trinca.

LE PROBLEME. Je ne peux pas reproduire leur triplet publie (Xi = 1,403 ; s = 0,70 ;
H0 = 69,94) parce que mon taux de formation stellaire a haut z est un doublement grossier
de Madau-Dickinson. Mon test FRB en depend entierement.

LA SORTIE, plus robuste que transcrire leur courbe. Le taux a haut z n'intervient dans le
resultat QUE par deux nombres : combien d'energie noire il produit (-> H0) et a quel cout
baryonique (-> s). Donc au lieu de deviner la courbe, on introduit UN facteur de rehaussement
B au-dela de z = 4 et on RESOUT le systeme 2x2 :
        s(Xi, B) = 0.70        H0(Xi, B) = 69.94
Si la solution donne Xi ~ 1,4 — leur valeur publiee, qui n'entre PAS dans le systeme — alors
le modele calibre est le leur dans tout ce qui est mesurable, et le test FRB devient un test
de LEUR modele, pas de mon approximation.

CRITERE PRE-ENREGISTRE (avant execution), et il est severe apres la semaine ecoulee :
  - VALIDATION : le Xi issu de la calibration doit tomber a moins de 30 % de leur 1,403.
    Sinon la forme de mon taux reste fausse et je n'exploite AUCUN chiffre FRB.
  - Si la validation passe : le test FRB est refait sur le modele calibre et son resultat
    est ecrit tel quel, favorable ou non.
  - Controle d'equite obligatoire (regle du 23/08) : tout ecart > 3 sigma doit etre recalcule
    avec leurs valeurs, pas les miennes, avant d'etre annonce.
"""
import numpy as np, sys
from scipy.optimize import fsolve, brentq
sys.path.insert(0, '/home/claude/desi_fit'); sys.path.insert(0, '/home/claude/selection')
import duel_ccbh as D
import test_wE_v3 as T
np.seterr(all='ignore')

WC, WBP = 0.1194, 0.02238
PSI0 = lambda z: 0.015*(1+z)**2.7/(1 + ((1+z)/2.9)**5.6)

def set_psi(B):
    D.psi_MD14 = lambda z: PSI0(z)*np.where(np.asarray(z) > 4.0, B, 1.0)

def profil(Xi, B, wc=WC, wbp=WBP):
    set_psi(B)
    wb = np.full_like(D.AG, wbp); wde = np.zeros_like(D.AG)
    j0 = np.searchsorted(D.AG, 1/21.0)
    for i in range(j0, len(D.AG)):
        wm = wc + wb[i-1] + D.W_NU_M
        wt = wm/D.AG[i-1]**3 + D.W_R/D.AG[i-1]**4 + wde[i-1]
        if wt <= 0 or wb[i-1] <= 0: return None
        Hy = 100*np.sqrt(wt)*D.KMS_PER_YR
        src = Xi*D.psi_MD14(1/D.AG[i-1]-1)/(Hy*D.AG[i-1]**4)/D.RHO100
        da = D.AG[i]-D.AG[i-1]
        wde[i] = wde[i-1] + src*da
        wb[i] = wb[i-1] - src*D.AG[i-1]**3*da
    if wb[-1] <= 0: return None
    wm = wc + wb + D.W_NU_M
    wt = wm/D.AG**3 + D.W_R/D.AG**4 + wde
    h = np.sqrt(wt[-1])
    return (1/D.AG-1)[::-1], np.sqrt(wt/h**2)[::-1], h, wb[::-1], wb[-1]/wbp

print("="*78)
print("  CALIBRATION : resoudre s = 0,70 et H0 = 69,94 pour (Xi, B)")
print("="*78)
def eqs(p):
    Xi, B = p
    if Xi <= 0 or B <= 0.5 or B > 60: return [1e3, 1e3]
    o = profil(Xi, B)
    if o is None: return [1e3, 1e3]
    return [o[4] - 0.70, 100*o[2] - 69.94]

sol = None
for g in ([1.4, 6.0], [1.0, 12.0], [2.0, 3.0], [0.8, 25.0]):
    r, info, ier, msg = fsolve(eqs, g, full_output=True)
    if ier == 1 and r[0] > 0 and 0.5 < r[1] < 60:
        o = profil(*r)
        if o and abs(o[4]-0.70) < 1e-3 and abs(100*o[2]-69.94) < 0.05:
            sol = r; break
if sol is None:
    print("  systeme non resolu -> aucun chiffre exploite"); sys.exit()
Xi_c, B_c = sol
o = profil(Xi_c, B_c)
zc, Ec, hc, wbc, s_c = o
print(f"  solution : Xi = {Xi_c:.3f}   B (rehaussement z>4) = {B_c:.2f}")
print(f"  controle : s = {s_c:.4f} (cible 0,70)   H0 = {100*hc:.2f} (cible 69,94)")
print(f"\n  VALIDATION : Xi calibre = {Xi_c:.3f} contre leur {1.403:.3f} publie"
      f"  ->  ecart {abs(Xi_c/1.403-1)*100:.0f} %")
ok = abs(Xi_c/1.403 - 1) < 0.30
print(f"  {'PASSE' if ok else 'ECHEC'} (seuil 30 %)")
if not ok:
    print("\n  -> la forme de mon taux reste fausse. Aucun chiffre FRB exploite (critere gele).")
    # --- Procedure de #91 (ajoutee 23/08, audit) : elle n'est PAS le critere gele ci-dessus. ---
    # On impose leur Xi = 1,403 et on resout (A, B) : normalisation globale et rehaussement z > 4.
    # Xi n'est plus derive, donc ceci ne VALIDE rien sur Xi ; c'est la calibration utilisee par
    # atlas_rivaux.py / attaque_croker_fond.py (A = 1,551, B = 3,119, jusqu'ici en dur). Le vrai
    # controle est le reajustement LIBRE du modele calibre (atlas_rivaux : Xi = 1,382, 1,5 %).
    print("\n" + "="*78)
    print("  PROCEDURE #91 (hors critere gele) : Xi IMPOSE = 1,403, omega_c = 0,1237 (les leurs), resoudre (A, B)")
    print("="*78)
    def set_psi_AB(A, B):
        D.psi_MD14 = lambda z: A*PSI0(z)*np.where(np.asarray(z) > 4.0, B, 1.0)
    def eqs_AB(p):
        A, B = p
        if A <= 0 or B <= 0.5 or B > 60: return [1e3, 1e3]
        set_psi_AB(A, B); o = profil_raw(1.403, wc=0.1237)   # leur omega_c publie (attaque_croker_fond)
        if o is None: return [1e3, 1e3]
        return [o[4] - 0.70, 100*o[2] - 69.94]
    def profil_raw(Xi, wc=WC, wbp=WBP):
        wb = np.full_like(D.AG, wbp); wde = np.zeros_like(D.AG)
        j0 = np.searchsorted(D.AG, 1/21.0)
        for i in range(j0, len(D.AG)):
            wm = wc + wb[i-1] + D.W_NU_M
            wt = wm/D.AG[i-1]**3 + D.W_R/D.AG[i-1]**4 + wde[i-1]
            if wt <= 0 or wb[i-1] <= 0: return None
            Hy = 100*np.sqrt(wt)*D.KMS_PER_YR
            src = Xi*D.psi_MD14(1/D.AG[i-1]-1)/(Hy*D.AG[i-1]**4)/D.RHO100
            da = D.AG[i]-D.AG[i-1]
            wde[i] = wde[i-1] + src*da; wb[i] = wb[i-1] - src*D.AG[i-1]**3*da
        if wb[-1] <= 0: return None
        wt = (wc + wb + D.W_NU_M)/D.AG**3 + D.W_R/D.AG**4 + wde
        return None, None, np.sqrt(wt[-1]), None, wb[-1]/wbp
    solAB = None
    for g in ([1.5, 3.0], [2.0, 2.0], [1.0, 6.0]):
        r, info, ier, msg = fsolve(eqs_AB, g, full_output=True)
        if ier == 1:
            set_psi_AB(*r); o = profil_raw(1.403, wc=0.1237)
            if o and abs(o[4]-0.70) < 1e-3 and abs(100*o[2]-69.94) < 0.05: solAB = r; break
    if solAB is None: print("  systeme (A, B) non resolu")
    else:
        print(f"  A = {solAB[0]:.3f}   B = {solAB[1]:.3f}   (atlas_rivaux / attaque_croker_fond : 1,551 / 3,119)")
        print("  Xi impose -> ceci n'est pas une validation de Xi. Le controle qui compte : reajustement")
        print("  libre du modele calibre sur nos donnees (atlas_rivaux.py) : Xi = 1,382 contre 1,403.")
    sys.exit()

print("\n" + "="*78)
print("  TEST FRB SUR LE MODELE CALIBRE")
print("="*78)
ZG = np.linspace(0, 3.0, 3000)
T.ZCUT = None
zl, El = T.fond(0.2976, 0.0, None, 'lcdm')
E_l = lambda z: np.interp(z, zl, El)
h_l, wb_l = 0.6866, 0.02261
E_c = lambda z: np.interp(z, zc, Ec)
r_c = lambda z: np.interp(z, zc, wbc)/hc**2

def kern(z, E, r):
    ig = r(ZG)*(1+ZG)/E(ZG)
    cum = np.concatenate([[0], np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(ZG))])
    return np.interp(z, ZG, cum)

un = lambda z: np.full_like(np.atleast_1d(z), 1.0, dtype=float)
for zlo, zhi, lab in [(0.05, 0.5, 'Macquart 2020'), (0.05, 1.0, 'DSA-110/Connor'), (0.05, 1.5, 'etendue')]:
    zs = np.linspace(zlo, zhi, 60)
    num = np.array([kern(z, E_c, r_c)/hc for z in zs])
    den = np.array([kern(z, E_l, un)/h_l for z in zs])
    ob = np.sum(num*den)/np.sum(den*den)
    fd = 0.049*0.85/ob
    print(f"  {lab:>16s} : Omega_b^eff = {ob:.5f}  ecart = {abs(0.049-ob)/0.0035:.1f} sigma"
          f"   f_d requis = {fd:.3f} {'IMPOSSIBLE' if fd > 1 else ''}")

print("\n" + "="*78)
print("  LE MODELE CALIBRE TIENT-IL ENCORE SUR LES DONNEES DE FOND ?")
print("="*78)
c = D.chi2_ccbh(WC, WBP, Xi_c)
print(f"  chi2 CCBH calibre = {c:.3f}  (accretion 1419,31 ; LCDM 1425,09 ; CCBH libre 1421,48)")
print(f"  AIC = {c+6:.3f}  contre accretion 1427,31")
