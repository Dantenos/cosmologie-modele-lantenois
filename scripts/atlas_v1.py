#!/usr/bin/env python3
"""ATLAS v1 — 19 modeles d'energie noire, un pipeline, un classement. CRITERES
PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 24/08/2026).
Realise le cahier des charges de registres/ATLAS_falsification_spec.md (liste v0 : 15
modeles a fond leger) + les 4 deja au tableau d'atlas_rivaux.py (Lombriser, CCBH, PC1,
Anton-Schmidt) = 19.

REGLES (spec, figees) :
  - donnees identiques pour tous : Pantheon+ (1580 SNe, cov complete, M marginalise),
    DESI DR2 BAO (13 pts, correlations), distance-priors Planck 2018, prior SH0ES —
    le pipeline v3 (test_wE_v3, ZCUT desactive), N = 1597 points ;
  - k = parametres reellement ajustes sur CES donnees, comptes pareil pour tous ;
  - metriques figees : chi2 min, AIC = chi2+2k, BIC = chi2+k ln(1597) — rien d'ajoute apres ;
  - classement par AIC ecrit TEL QUEL ; aucun modele retire parce qu'il nous depasse ;
  - chaque modele porte sa CONDITION DE MORT declaree, publiee avec le tableau ;
  - le leaderboard (registres/atlas_leaderboard.json) et registres/ATLAS.md sont GENERES
    par ce script, jamais ecrits a la main.
VALIDATION (sine qua non) : les 7 entrees d'atlas_rivaux.py doivent etre reproduites a
+/- 0,5 en chi2 (ancres du 23/08 : LCDM 1425,086 ; accretion 1419,309 ; CCBH 1420,309 ;
CPL 1418,927 ; PC1 1416,701 ; Anton-Schmidt 1419,515 ; Lombriser 1427,607). Sinon :
RIEN n'est publie, aucun fichier ecrit.
APPROXIMATIONS DECLAREES : HDE resout dOmega/dlna = Omega(1-Omega)(1+2 sqrt(Omega)/c)
(matiere+DE ; la radiation est ajoutee au fond, approximation declaree) ; Rh=ct pose
E = 1+z et ne garde Om que pour r_d (incoherence declaree : ce modele n'a pas de
secteur matiere separe — c'est precisement theta*/BAO qui le juge) ; les deux iLCDM
appliquent l'echange a TOUTE la matiere (baryons compris, simplification declaree) ;
JPS est la comptabilite d'accumulation effective (drho_de/dlna = -eps rho_m), pas leur
microphysique. Toute forme est normalisee a rho_de(a=1) = Omega_de.
Usage : python3 scripts/atlas_v1.py   (depuis donnees/pantheon_plus)
"""
import sys, json, pathlib, datetime
import numpy as np
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import test_wE_v3 as T, duel_ccbh as D
np.seterr(all='ignore')
T.ZCUT = None
AG = np.logspace(-7, 0, 12000)
N_DATA = 1597
ANCRES = {"LCDM": 1425.086, "ACCRETION (Gamma∝1/t)": 1419.309, "CCBH (Croker et al.)": 1420.309,
          "CPL = IDE degeneree": 1418.927, "PC1 (creation, w_E libre)": 1416.701,
          "Anton-Schmidt": 1419.515, "Lombriser (Om_de predit)": 1427.607}

# ---------- fonds generiques ----------
def fond_arrays(E2):
    if E2 is None or np.any(~np.isfinite(E2)) or np.any(E2 <= 0): return None
    return (1/AG-1)[::-1], np.sqrt(E2)[::-1]

def fond_gen(Om, g):
    Or = Om/3388.0; Ode = 1-Om-Or
    ga = g(AG)
    if ga is None or np.any(~np.isfinite(ga)) or np.any(ga < 0): return None
    return fond_arrays(Om/AG**3 + Or/AG**4 + Ode*ga)

def t_of_a(E2):
    E = np.sqrt(E2); integ = 1/(AG*E)
    t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(AG))])
    return t/t[-1]

# formes fermees g(a) = rho_de(a)/rho_de(1)
g_wcdm = lambda w: (lambda a: a**(-3*(1+w)))
g_logw = lambda w0, wl: (lambda a: a**(-3*(1+w0))*np.exp(-1.5*wl*np.log(a)**2))
g_thaw = lambda w0: (lambda a: np.exp((1+w0)*(1-a**3)))
g_pede = lambda a: 1 + np.tanh(np.log10(a))
def g_gcg(As, al):
    def f(a):
        v = As + (1-As)*a**(-3*(1+al))
        return np.where(v > 0, v**(1/(1+al)), np.nan)
    return f
def g_cpl(w0, wa): return lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def g_as(n, L0):
    def f(a):
        num = (L0-3*np.log(a))/(n+1) + 1/(n+1)**2; den = L0/(n+1) + 1/(n+1)**2
        if den <= 0: return None
        return np.where(num > 0, a**(3*n)*num/den, np.nan)
    return f

# fonds custom (matiere modifiee ou structure propre)
def fond_jps(Om, eps):
    Or = Om/3388.0; Ode = 1-Om-Or
    rho_de = Ode - (eps/3.0)*Om*(AG**-3 - 1)
    if np.any(rho_de < 0): return None
    return fond_arrays(Om/AG**3 + Or/AG**4 + rho_de)

def fond_ilcdm_dm(Om, eps):
    if abs(eps-3) < 1e-3: return None
    Or = Om/3388.0; Ode = 1-Om-Or
    rho_m = Om*AG**(-3+eps)
    rho_de = Ode - eps*Om*(AG**(eps-3) - 1)/(eps-3)
    if np.any(rho_de < 0): return None
    return fond_arrays(rho_m + Or/AG**4 + rho_de)

def fond_ilcdm_de(Om, eps):
    if abs(eps-3) < 1e-3: return None
    Or = Om/3388.0; Ode = 1-Om-Or
    rho_de = Ode*AG**(-eps)
    C = Om + eps*Ode*(AG**(3-eps) - 1)/(3-eps)
    if np.any(C < 0): return None
    return fond_arrays(C*AG**-3 + Or/AG**4 + rho_de)

def fond_hde(Om, c):
    Or = Om/3388.0; Ode = 1-Om-Or
    lna = np.log(AG); Omg = np.empty_like(AG); Omg[-1] = Ode
    for i in range(len(AG)-1, 0, -1):
        O = Omg[i]
        dO = O*(1-O)*(1 + 2*np.sqrt(max(O, 1e-12))/c)
        Omg[i-1] = O - dO*(lna[i]-lna[i-1])
        if not (1e-12 < Omg[i-1] < 1-1e-12): Omg[:i] = np.clip(Omg[i-1], 1e-12, 1-1e-12); break
    return fond_arrays((Om/AG**3 + Or/AG**4)/(1-Omg))

def fond_rhct(Om):
    return fond_arrays(AG**-2.0)

def fond_bondi(Om, xs):
    if not (0 < xs < 0.999): return None
    Or = Om/3388.0; Ode = 1-Om-Or
    E2 = (Om+Ode)/AG**3 + Or/AG**4
    for _ in range(6):
        t = t_of_a(E2)
        m = (1-xs)/np.clip(1-xs*t, 1e-6, None)
        E2 = (Om + Ode*m)/AG**3 + Or/AG**4
    return fond_arrays(E2)

# ---------- branchement dans le pipeline v3 ----------
CUSTOM = {}
_fond = T.fond
def fond_patch(Om, wE, par, famille, n_iter=7):
    if famille in CUSTOM: return CUSTOM[famille](Om, par)
    return _fond(Om, wE, par, famille, n_iter)
T.fond = fond_patch
CUSTOM.update({
 'wcdm':  lambda Om, p: fond_gen(Om, g_wcdm(p)),
 'logw':  lambda Om, p: fond_gen(Om, g_logw(*p)),
 'thaw':  lambda Om, p: fond_gen(Om, g_thaw(p)),
 'pede':  lambda Om, p: fond_gen(Om, g_pede),
 'gcg':   lambda Om, p: fond_gen(Om, g_gcg(*p)),
 'cpl':   lambda Om, p: fond_gen(Om, g_cpl(*p)),
 'as':    lambda Om, p: fond_gen(Om, g_as(*p)),
 'lomb':  lambda Om, p: fond_gen(Om, lambda a: np.ones_like(a)),
 'jps':   fond_jps, 'ilcdm_dm': fond_ilcdm_dm, 'ilcdm_de': fond_ilcdm_de,
 'hde':   fond_hde, 'rhct': lambda Om, p: fond_rhct(Om), 'bondi': fond_bondi,
})

def chi2(p, fam, npar, fixOm=None, fixpar=None):
    h, ob = p[0], p[1]
    Om = fixOm if fixOm is not None else p[2]
    i0 = 2 if fixOm is not None else 3
    par = fixpar if fixpar is not None else (None if npar == 0 else (p[i0] if npar == 1 else tuple(p[i0:i0+npar])))
    c = T.chi2(h, ob, Om, 0.0, par, fam)
    return c if np.isfinite(c) else 1e9

def fit(fam, npar, starts, bornes=None, fixOm=None, fixpar=None):
    def f(p):
        if bornes:
            i0 = 2 if fixOm is not None else 3
            for j, (lo, hi) in enumerate(bornes):
                if not (lo < p[i0+j] < hi): return 1e9
        return chi2(p, fam, npar, fixOm, fixpar)
    best = None
    for s in starts:
        r = minimize(f, s, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-4, maxiter=6000, maxfev=6000))
        if best is None or r.fun < best.fun: best = r
    return best

B = [0.69, 0.02236, 0.31]   # depart commun h, wb, Om

if __name__ == "__main__":
    res = []  # (nom, k, chi2, params, mort, note)
    def add(nom, k, c, params, mort, note=""):
        res.append(dict(nom=nom, k=k, chi2=round(float(c), 3), aic=round(float(c)+2*k, 3),
                        bic=round(float(c)+k*np.log(N_DATA), 3), params=params, mort=mort, note=note))
        print(f"  [{len(res):2d}/19] {nom:<28s} chi2 = {c:9.3f}", flush=True)

    # --- les 7 du tableau (validation) ---
    r = T.fit('lcdm'); add("LCDM", 3, r.fun, f"H0={100*r.x[0]:.2f} Om={r.x[2]:.4f}",
        "reference ; mort si une alternative atteint dAIC > 10 et survit aux audits")
    b = fit('lomb', 0, [[0.69, 0.02236]], fixOm=1-0.697)
    add("Lombriser (Om_de predit)", 2, b.fun, f"H0={100*b.x[0]:.2f} Om=0.3030 (impose)",
        "mort si Omega_de mesure exclut 0,697 (la prediction est le modele)")
    r0 = T.fit('invt', wE=0.0, npar=1, depart=[[2.4], [1.6], [3.4]])
    add("ACCRETION (Gamma∝1/t)", 4, r0.fun, f"H0={100*r0.x[0]:.2f} beta={r0.x[3]:.3f}",
        "mort si beta(DR3) exclut [2,42;2,60] a 3 sigma, ou dAIC > +6 vs LCDM (scelle)")
    PSI0 = lambda z: 0.015*(1+z)**2.7/(1+((1+z)/2.9)**5.6)
    D.psi_MD14 = lambda z: 1.551*PSI0(z)*np.where(np.asarray(z) > 4.0, 3.119, 1.0)
    bb = None
    for s0 in ([0.1237, 0.02238, 1.40], [0.119, 0.0224, 1.0]):
        rr = minimize(lambda p: D.chi2_ccbh(*p), s0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000))
        if bb is None or rr.fun < bb.fun: bb = rr
    oc = D.fond_ccbh(*bb.x)
    add("CCBH (Croker et al.)", 3, bb.fun, f"H0={100*oc[2]:.2f} (derive) Xi={bb.x[2]:.3f}",
        "mort si s != 0,70 (FRB : deja 2,2 sigma contre, #148) ou k != 3 (JWST 2025 : 11 sigma contre)")
    bc = fit('cpl', 2, [B+[-0.85, -0.6], B+[-0.9, -0.3]], bornes=[(-3, 1), (-6, 4)])
    add("CPL = IDE degeneree", 5, bc.fun, f"H0={100*bc.x[0]:.2f} w0={bc.x[3]:.3f} wa={bc.x[4]:.3f}",
        "mort si la reconstruction sort de la famille lineaire en (1-a)")
    rp = T.fit('PC1', wE=None, npar=2, depart=[[0.62, 2.1], [0.9, 1.3]])
    add("PC1 (creation, w_E libre)", 6, rp.fun, f"H0={100*rp.x[0]:.2f} b={rp.x[4]:.3f}",
        "mort si w_E = 0 exige (PC3 deja a 2,7 sigma) ou si k = 6 jamais paye par les donnees")
    ba = fit('as', 2, [B+[0.0, 1.0], B+[-0.3, 3.0], B+[0.2, 0.5]], bornes=[(-0.999, 5), (-10, 10)])
    add("Anton-Schmidt", 5, ba.fun, f"H0={100*ba.x[0]:.2f} n={ba.x[3]:.3f} L0={ba.x[4]:.3f}",
        "forme publiee (secteur sombre seul, declare) ; mort si (n, L0) fuient au bord")
    # --- VALIDATION avant les 12 nouveaux ---
    ko = [f"{r_['nom']} {r_['chi2']} vs {ANCRES[r_['nom']]}" for r_ in res if abs(r_['chi2'] - ANCRES[r_['nom']]) > 0.5]
    if ko: sys.exit("[atlas] VALIDATION ECHOUEE, rien n'est publie : " + " ; ".join(ko))
    print("  [validation] les 7 ancres reproduites a +/- 0,5 -> les 12 nouveaux entrent\n")

    # --- les 12 de la liste v0 ---
    r = fit('wcdm', 1, [B+[-0.9], B+[-1.1]], bornes=[(-2, -0.2)])
    add("wCDM", 4, r.fun, f"w={r.x[3]:.3f}", "mort si un croisement de w = -1 est etabli (w constant ne croise pas)")
    r = fit('logw', 2, [B+[-0.9, 0.1], B+[-0.85, -0.2]], bornes=[(-2, 0), (-2, 2)])
    add("w log(a) (Efstathiou)", 5, r.fun, f"w0={r.x[3]:.3f} wl={r.x[4]:.3f}", "mort si la reconstruction sort de la famille log")
    r = T.fit('invt', wE=0.0, npar=1, depart=[[2.5]])
    c25 = fit('lcdm', 0, [B]) if False else None
    r25 = fit('invt', 0, [B], fixpar=2.5)
    add("ACCRETION 5/2 (0 param.)", 3, r25.fun, "beta=2.5 (fixe)",
        "mort si beta = 5/2 exclu a 3 sigma par le profil (le point distingue est le modele)")
    r = fit('jps', 1, [B+[0.05], B+[-0.05]], bornes=[(-0.5, 0.5)])
    add("JPS / unimodulaire (accum.)", 4, r.fun, f"eps={r.x[3]:+.4f}",
        "comptabilite effective declaree ; mort si eps = 0 prefere (le papier A l'a deja rejetee a dchi2 = +4,9)")
    r = fit('ilcdm_dm', 1, [B+[0.02], B+[-0.02]], bornes=[(-0.5, 0.5)])
    add("iLCDM Q=eps H rho_dm", 4, r.fun, f"eps={r.x[3]:+.4f}", "mort si eps incompatible avec 0 sans gain d'AIC")
    r = fit('ilcdm_de', 1, [B+[0.02], B+[-0.02]], bornes=[(-0.5, 0.5)])
    add("iLCDM Q=eps H rho_de", 4, r.fun, f"eps={r.x[3]:+.4f}", "mort si eps incompatible avec 0 sans gain d'AIC")
    r = fit('pede', 0, [B])
    add("PEDE (emergente, 0 param.)", 3, r.fun, "aucun (forme rigide)",
        "zero echappatoire : mort si dAIC > 10 vs le meilleur (forme figee par construction)")
    r = fit('hde', 1, [B+[0.7], B+[1.1]], bornes=[(0.3, 2.5)])
    add("Holographique (horizon futur)", 4, r.fun, f"c={r.x[3]:.3f}",
        "mort si c >= 1 exige sans acceleration suffisante, ou dAIC > 10 (approx. radiation declaree)")
    r = fit('thaw', 1, [B+[-0.9], B+[-0.7]], bornes=[(-0.999, -0.3)])
    add("Quintessence thawing (Linder)", 4, r.fun, f"w0={r.x[3]:.3f}",
        "mort si w0 < -1 exige : la famille interdit le fantome, donc le croisement la tue")
    r = fit('gcg', 2, [B+[0.8, 0.2], B+[0.95, 1.0]], bornes=[(0.01, 0.999), (-0.8, 5)])
    add("Chaplygin generalise (GCG)", 5, r.fun, f"As={r.x[3]:.3f} alpha={r.x[4]:.3f}",
        "secteur sombre seul (declare) ; mort si alpha -> 0 sans gain (degenere a LCDM)")
    r = fit('rhct', 0, [B[:2]+[0.30]])
    add("Rh = ct", 2, r.fun, f"H0={100*r.x[0]:.2f} (Om fixe 0,30, r_d seul — incoherence declaree)",
        "mort par theta* et BAO : E = 1+z n'a ni ere de matiere ni acceleration — ecrit tel quel")
    r = fit('bondi', 1, [B+[0.5], B+[0.8]], bornes=[(0.01, 0.999)])
    add("Bondi sature (M'∝M²)", 4, r.fun, f"x_s=t0/t_s={r.x[3]:.3f}",
        "mort si x_s -> 1 (saturation avant aujourd'hui) ou si la forme perd sur ACC libre a k egal")

    # --- publication (generee, jamais a la main) ---
    base = min(m["aic"] for m in res)
    for m in res: m["daic"] = round(m["aic"] - base, 3)
    res.sort(key=lambda m: m["aic"])
    lead = dict(date=str(datetime.date.today()), donnees="Pantheon+ 1580 + DESI DR2 BAO 13 + distance-priors Planck + SH0ES (pipeline v3, ZCUT off)",
                N=N_DATA, metriques="chi2 min, AIC=chi2+2k, BIC=chi2+k ln N", modeles=res)
    (ROOT / "registres/atlas_leaderboard.json").write_text(json.dumps(lead, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    L = ["# ATLAS — 19 modèles, un pipeline, un classement (généré par `scripts/atlas_v1.py`, ne pas éditer)", "",
         f"*{lead['date']} — données : {lead['donnees']} ; N = {N_DATA}. Classement par AIC, écrit tel quel ;*",
         "*aucun modèle n'est retiré parce qu'il nous dépasse. ΔAIC < 2 : indiscernable ; 2-7 : préférence faible ; > 10 : forte.*", "",
         "| # | modèle | k | χ² | AIC | ΔAIC | BIC | paramètres | condition de mort |", "|---|---|---|---|---|---|---|---|---|"]
    for i, m in enumerate(res, 1):
        L.append(f"| {i} | **{m['nom']}** | {m['k']} | {m['chi2']:.2f} | {m['aic']:.2f} | {m['daic']:+.2f} | {m['bic']:.2f} | {m['params']} | {m['mort']} |")
    L += ["", "Approximations déclarées : voir le docstring de `scripts/atlas_v1.py` (gelé). Validation : les 7",
          "entrées d'`atlas_rivaux.py` reproduites à ±0,5 en χ² avant toute publication des 12 nouveaux."]
    (ROOT / "registres/ATLAS.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n" + "\n".join(L[5:7+len(res)]))
    print(f"\n[atlas] publiés : registres/atlas_leaderboard.json + registres/ATLAS.md")
