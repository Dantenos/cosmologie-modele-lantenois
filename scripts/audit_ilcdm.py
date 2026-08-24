#!/usr/bin/env python3
"""AUDIT DES iLCDM — l'arbitre de la tension T7, premier volet. CRITERES PRE-ENREGISTRES
(geles AVANT execution, 24/08/2026).

LA QUESTION. Les deux iLCDM d'interaction menent l'atlas (#150 : chi2 = 1415,2/1415,8,
-9,8 sur LCDM pour UN parametre) sur une implementation declaree suspecte au gel :
(a) l'echange etait applique a TOUTE la matiere (baryons compris — contraint par ailleurs) ;
(b) le facteur a^(eps-3) modifie la matiere jusqu'a la recombinaison alors que les
distance-priors supposent la physique primordiale standard — le fit peut exploiter cette
incoherence. Cet audit rejoue le rival dans des implementations COHERENTES :
  V1  (reproduction)   : l'implementation de l'atlas, telle quelle — validation.
  V2a (CDM seul)       : les baryons (Omega_b = 0,0493 fixe, Planck ; h varie de ~2 %,
      declare) sont conserves ; seul le CDM echange. Pour Q = eps H rho_de la correction
      de matiere est inchangee (elle ne depend que de rho_de) ; pour Q = eps H rho_dm,
      rho_cdm = (Om - Ob) a^(eps-3).
  V2b (CDM seul + TARDIF) : l'echange n'opere qu'a z < 3 (gel au-dela, comme le ZCUT du
      pipeline) — la variante entierement compatible avec les priors primordiaux. C'est
      LA variante cohérente au sens de T7.
Chaque variante : fit complet (h, omega_b, Om, eps), memes donnees, memes departs multiples
(regle 5 : le rival garde tout ce qu'il a le droit de reajuster). Puis sigma(eps) par profil
Delta_chi2 = 1 sur la meilleure variante coherente.

CRITERES (exhaustifs, exclusifs).
  - VALIDATION : V1 doit reproduire les chi2 de l'atlas (#150) a +/- 0,3 : 1415,24 (Q~rho_de)
    et 1415,82 (Q~rho_dm). Sinon rien n'est publie.
  - Verdict sur le gain g = chi2(LCDM = 1425,086) - chi2(V2b), par couplage :
      ARTEFACT       si g < 3   (le -9,8 venait de l'incoherence primordiale) ;
      ROBUSTE        si g >= 6  ET |eps| >= 2 sigma(eps) ;
      INTERMEDIAIRE  sinon — ecrit tel quel.
  - Tout est rapporte, favorable ou non, y compris si V2b fait MIEUX que V1.
  - Ceci est le PREMIER VOLET de l'arbitre de T7 (grave au greffe) ; la batterie complete
    (LOO traceurs, split-z, trilogie SN) reste due avant toute resolution de T7 — le statut
    de T7 passe a « en_jugement », pas a « resolue ».
Usage : python3 scripts/audit_ilcdm.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A          # fournit fond_arrays, AG, CUSTOM, fit, T (fond patche)

OB = 0.0493
A_GEL = 0.25                  # z = 3

def _base(Om):
    Or = Om/3388.0; return Or, 1-Om-Or

def fond_de_cdm(Om, eps, tardif=False):
    """Q = eps H rho_de, CDM seul (correction de matiere independante de rho_dm)."""
    if abs(eps-3) < 1e-3: return None
    Or, Ode = _base(Om)
    a = A.AG
    if tardif:
        rho_de = np.where(a >= A_GEL, Ode*a**(-eps), Ode*A_GEL**(-eps))
        corr = np.where(a >= A_GEL, eps*Ode*(a**(3-eps) - 1)/(3-eps),
                        eps*Ode*(A_GEL**(3-eps) - 1)/(3-eps))
    else:
        rho_de = Ode*a**(-eps)
        corr = eps*Ode*(a**(3-eps) - 1)/(3-eps)
    C = (Om - OB) + corr
    if np.any(C < 0) or np.any(rho_de < 0): return None
    return A.fond_arrays((C + OB)*a**-3 + Or/a**4 + rho_de)

def fond_dm_cdm(Om, eps, tardif=False):
    """Q = eps H rho_dm, CDM seul : rho_cdm = (Om-Ob) a^(eps-3), baryons conserves."""
    if abs(eps-3) < 1e-3: return None
    Or, Ode = _base(Om)
    a = A.AG; cdm0 = Om - OB
    if tardif:
        rho_cdm = np.where(a >= A_GEL, cdm0*a**(eps-3), cdm0*A_GEL**eps*a**-3)
        rho_de = np.where(a >= A_GEL, Ode - eps*cdm0*(a**(eps-3) - 1)/(eps-3),
                          Ode - eps*cdm0*(A_GEL**(eps-3) - 1)/(eps-3))
    else:
        rho_cdm = cdm0*a**(eps-3)
        rho_de = Ode - eps*cdm0*(a**(eps-3) - 1)/(eps-3)
    if np.any(rho_de < 0): return None
    return A.fond_arrays(rho_cdm + OB*a**-3 + Or/a**4 + rho_de)

A.CUSTOM.update({
 'ilcdm_de_c':  lambda Om, p: fond_de_cdm(Om, p, False),
 'ilcdm_de_ct': lambda Om, p: fond_de_cdm(Om, p, True),
 'ilcdm_dm_c':  lambda Om, p: fond_dm_cdm(Om, p, False),
 'ilcdm_dm_ct': lambda Om, p: fond_dm_cdm(Om, p, True),
})
B0 = [0.69, 0.02236, 0.31]
LCDM_REF = 1425.086
ANCRES = {'ilcdm_de': 1415.245, 'ilcdm_dm': 1415.818}

def fit_eps(fam):
    return A.fit(fam, 1, [B0+[0.02], B0+[-0.02], B0+[0.005]], bornes=[(-0.5, 0.5)])

def sigma_eps(fam, e_hat, c_hat):
    def cfix(e):
        return A.fit(fam, 1, [B0], fixpar=e).fun
    pas = max(abs(e_hat)*0.5, 0.004)
    hi = e_hat
    for _ in range(12):
        hi += pas
        if cfix(hi) > c_hat + 1.0: break
    lo = e_hat
    for _ in range(12):
        lo -= pas
        if cfix(lo) > c_hat + 1.0: break
    return 0.5*(hi - lo)/1.0   # approximation lineaire declaree (profil grossier, pas ~0,5 sigma)

if __name__ == "__main__":
    print("AUDIT iLCDM — arbitre T7, premier volet (criteres geles)\n")
    # VALIDATION : reproduction de l'atlas
    ok = True
    for fam, ref in ANCRES.items():
        r = fit_eps(fam)
        d = abs(r.fun - ref)
        print(f"  [V1 {fam:9s}] chi2 = {r.fun:9.3f} (atlas {ref}) eps = {r.x[3]:+.4f} -> {'OK' if d < 0.3 else 'ECHEC'}")
        ok &= d < 0.3
    if not ok: sys.exit("  VALIDATION ECHOUEE — rien n'est publie.")
    print()
    res = {}
    for lab, fam in [("V2a Q~rho_de CDM seul", 'ilcdm_de_c'), ("V2b Q~rho_de CDM+tardif", 'ilcdm_de_ct'),
                     ("V2a Q~rho_dm CDM seul", 'ilcdm_dm_c'), ("V2b Q~rho_dm CDM+tardif", 'ilcdm_dm_ct')]:
        r = fit_eps(fam)
        g = LCDM_REF - r.fun
        res[fam] = (r, g)
        print(f"  [{lab:24s}] chi2 = {r.fun:9.3f}  gain vs LCDM = {g:+6.2f}  eps = {r.x[3]:+.4f}")
    print()
    for cpl, fam in [("Q~rho_de", 'ilcdm_de_ct'), ("Q~rho_dm", 'ilcdm_dm_ct')]:
        r, g = res[fam]
        s = sigma_eps(fam, r.x[3], r.fun)
        nsig = abs(r.x[3])/s if s > 0 else 0
        if g < 3: v = "ARTEFACT (le gain venait de l'incoherence primordiale)"
        elif g >= 6 and nsig >= 2: v = "ROBUSTE — a verser a la litterature apres la batterie complete"
        else: v = "INTERMEDIAIRE"
        print(f"  VERDICT {cpl} (variante coherente V2b) : gain = {g:+.2f}, eps = {r.x[3]:+.4f} ± {s:.4f} "
              f"({nsig:.1f} sigma) -> {v}")
    print("\n  T7 : premier volet execute ; LOO / split-z / trilogie SN restent dus avant resolution.")
