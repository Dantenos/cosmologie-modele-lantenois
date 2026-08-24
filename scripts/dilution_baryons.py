#!/usr/bin/env python3
"""LA FAMILLE DU #188 FAISAIT DILUER LES BARYONS. ELLE N'AURAIT PAS DU.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

LE DEFAUT, TROUVE EN RELISANT NOTRE PROPRE DEFINITION DE FAMILLE.
Le fond du #188 et du #190 s'ecrit  E^2 = Om a^(eps-3) + Or/a^4 + lam, ou Om est la matiere
TOTALE. Les BARYONS y diluent donc en a^(eps-3) comme le reste. Or le meme chi2 :
  (i) compare ob au prior Planck omega_b = 0,02237 +/- 0,00015, mesure en supposant a^-3 ;
  (ii) integre r_s avec R_b = (3 omega_b / 4 omega_gamma) a, forme qui suppose rho_b ~ a^-3 ;
       si les baryons diluaient vraiment en a^(eps-3), il faudrait R_b ~ a^(1+eps).
Le modele dilue les baryons d'un cote et les traite comme standard des deux autres.

SONDE PREALABLE (hors corpus, declaree, elle a servi a fixer les seuils ci-dessous) :
  - incoherence (ii) : entre R_b ~ a et R_b ~ a^(1+eps), r_s bouge de 22e-4 a |eps| = 0,003
    et de 45e-4 a |eps| = 0,006, soit **7,5 et 15,1 sigma sur l_A**. PLUS GRAND QUE TOUT CE
    QUE LE #188 ET LE #190 ONT MESURE.
  - incoherence (i) : omega_b a la recombinaison s'ecarte du prior Planck de 4,8 sigma a
    eps = -0,003 et de 8,1 sigma a eps = -0,006.
  - fraction baryonique a l'optimum gele : 0,1611.

CE QUE LA CORRECTION FAIT, ET CE QU'ELLE REVELE. On pose la famille CORRIGEE :
    rho_c = (Om - Ob) a^(eps-3)   [matiere noire seule]
    rho_b = Ob a^-3               [baryons EXACTEMENT standard]
    Lambda constante
Les trois incoherences disparaissent d'un coup : R_b ~ a redevient exact, omega_b redevient
comparable au prior, et le modele cesse de violer la conservation du nombre baryonique.
ET SURTOUT : cette famille corrigee est, AU NIVEAU DU FOND, exactement celle de
Kumar, Ajith & Verma (arXiv:2504.14419) avec w_dm = -eps/3 -- rho_dm ~ a^(-3(1+w)) est la
meme courbe. Leur mesure en vraisemblance complete (CAMB modifie, Planck 2018 + DESI DR2)
devient donc DIRECTEMENT comparable a la notre, SANS facteur de conversion. C'est ce que le
#191 n'avait pu faire qu'avec un facteur f = 0,8389 approximatif.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. A eps = 0 la famille corrigee doit redonner l'ancre gelee LCDM 1425,086 a 1e-3 pres :
     sans dilution, separer baryons et matiere noire ne change rien.
  B. LA CORRECTION NE DOIT PAS ETRE COSMETIQUE. A eps = +0,006 et -0,006, le chi2 de la
     famille corrigee doit differer de celui de l'ancienne d'au moins 0,5 unite. Si l'ecart
     est plus petit, la correction ne change rien d'observable et on l'ecrit tel quel au
     lieu d'en faire une decouverte.
  C. Les deux signes de eps doivent rester accessibles a >= 90 % de chaque cote.

--- CRITERES (exhaustifs, exclusifs) ---
  1. MESURE DANS LA FAMILLE CORRIGEE, quatre configurations, les memes que le #190 :
     (table r_s, etiquette) / (table r_s, coherent) / (r_s direct, R retire) /
     (r_s direct, R par recombinaison). eps, sigma par profil, ET sigma de Wilks
     (sqrt du gain) -- le #190 a montre que les deux divergent quand le profil s'aplatit,
     donc on rapporte les deux d'emblee et LE PLUS PETIT est l'opposable.
  2. LE RENVERSEMENT DE SIGNE SURVIT-IL A LA CORRECTION ?
     RENVERSEMENT PERSISTANT si les configurations 1 et 2 gardent des signes opposes avec
        chacune >= 2 sigma opposables ;
     RENVERSEMENT SUPPRIME si elles s'accordent en signe ;
     PLUS DE DETECTION si aucune des deux n'atteint 2 sigma opposables.
  3. TAILLE DE L'ERREUR ANCIENNE. Pour chaque configuration, on rapporte le deplacement de
     eps entre l'ancienne famille et la corrigee, en sigma de la corrigee. Si un deplacement
     depasse 1 sigma, les nombres correspondants du #188 et du #190 sont declares NON
     OPPOSABLES et retires -- pas nuances, retires.
  4. CONFRONTATION DIRECTE, sans facteur de conversion. Kumar, Ajith & Verma
     (arXiv:2504.14419), PL18 + DESI DR2 : w_dm = +0,00077 +/- 0,00038, donc
     eps = -3 w_dm = -0,00231 +/- 0,00114 dans NOTRE convention corrigee, exactement.
     On rapporte l'ecart en sigma combines pour chaque configuration.
     COMPATIBLE < 2 sigma ; TENSION 2-3 ; DESACCORD >= 3.
  5. CE QUI RESTE DU #190. Son acquis etait methodologique : "eps n'est pas identifiable par
     des priors comprimes". La correction AJOUTE une quatrieme source d'ambiguite (le
     traitement des baryons) au lieu d'en retirer une. On rapporte l'etendue des quatre
     configurations corrigees et on la compare a celle du #190 (0,0160).
     ACQUIS RENFORCE si l'etendue corrigee reste >= 0,005 ; ACQUIS AFFAIBLI sinon.

REGLE 6. Cette etude corrige un defaut A MOI et pourrait servir a sauver la face. Les seuils
vont donc contre : la validation B exige que la correction soit VISIBLE (sinon elle n'est pas
une decouverte), le critere 3 RETIRE au lieu de nuancer, et le critere 5 peut declarer mon
propre acquis affaibli.
REGLE 5, accorde d'avance : le fond corrige est celui de Kumar et al., mais les PERTURBATIONS
ne le sont pas -- eux propagent une matiere noire de pression non nulle dans un code de
Boltzmann, nous ne propageons rien du tout. Notre comparaison porte sur le fond seul, et
aucune de nos configurations n'est une vraisemblance complete.
Regle 3 : cette etude REDUIT le nombre de nos chiffres opposables ; elle n'en cree aucun.
Usage : python3 scripts/dilution_baryons.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import dilution_arbitre as D
import test_wE_v3 as T
import vraisemblance_reelle as V

AG = A.AG
A_STAR = D.A_STAR
CHI2_LCDM = 1425.086
STARTS = D.STARTS
# Kumar, Ajith & Verma (arXiv:2504.14419), PL18+DESI DR2, w_dm constant, c_s^2 = 0
EPS_KUMAR, SIG_KUMAR = -3.0*0.00077, 3.0*0.00038


def fond_cor(Om, ob, h, eps):
    """matiere noire en a^(eps-3), BARYONS EXACTEMENT en a^-3, Lambda constante."""
    Ob = ob/(h*h)
    Oc = Om - Ob
    if Oc <= 0:
        return None
    Or = Om/3388.0
    lam = 1 - Om - Or
    if lam <= 0:
        return None
    return A.fond_arrays(Oc*AG**(eps - 3) + Ob/AG**3 + Or/AG**4 + lam)


def rs_cor(a_hi, Om, ob, h, eps):
    """r_s dans le fond corrige. R_b ~ a y est EXACT puisque les baryons sont standard."""
    if not np.isfinite(a_hi) or a_hi <= 0:
        return np.nan
    om = Om*h*h
    lna = np.linspace(np.log(D.A_LO), np.log(a_hi), D.NA)
    a = np.exp(lna)
    h2E2 = ((om - ob - D.W_NU_M)*a**(eps - 3.0) + ob/a**3
            + D.W_RAD/a**4 + (h*h - om - D.W_RAD))
    if np.any(h2E2 <= 0):
        return np.nan
    Rb = (3.0*ob/(4.0*D.W_G))*a
    return float(np.trapezoid(D.C_KM/(a*100*np.sqrt(h2E2)*np.sqrt(3.0*(1.0 + Rb))), lna))


def chi2_cor(h, ob, Om, eps, cfg):
    if not (0.55 < h < 0.85 and 0.0200 < ob < 0.0245 and 0.15 < Om < 0.55):
        return 1e9
    om = Om*h*h
    Ob = ob/(h*h)
    # densite de matiere A LA RECOMBINAISON, en equivalent a^-3 : MN diluee + baryons intacts
    om_rec = ((Om - Ob)*A_STAR**eps + Ob)*h*h
    om_tab = om_rec if cfg['zs'] == 'coh' else om
    if not (0.132 < om_tab < 0.155):
        return 1e9
    fo = fond_cor(Om, ob, h, eps)
    if fo is None:
        return 1e9
    zz, Ea = fo
    Ez = np.interp(T.zg, zz, Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0):
        return 1e9
    inv = 1.0/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:] + inv[:-1])*np.diff(T.zg))])
    DH0 = D.C_KM/(100*h)

    zs = T.z_star(ob, om_tab)
    if cfg['rs'] == 'table':
        rd, rs = T.r_drag(ob, om_tab), T.r_star(ob, om_tab)
    else:
        rd = rs_cor(1.0/(1.0 + D.z_drag(ob, om_tab)), Om, ob, h, eps)
        rs = rs_cor(1.0/(1.0 + zs), Om, ob, h, eps)
    if not (np.isfinite(rd) and np.isfinite(rs) and rd > 0 and rs > 0):
        return 1e9

    mu = 5*np.log10((1 + V.z_sn)*np.interp(V.z_sn, T.zg, Dc))
    r = V.mb - mu
    c_sn = r@V.Cinv_sn@r - (r@V.Cinv_one)**2/V.oCo

    u = np.zeros(13)
    for i, (z, typ, _, _, _) in enumerate(V.BAO):
        DM_ = np.interp(z, T.zg, Dc)*DH0
        DH_ = DH0/np.interp(z, T.zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]/rd
    rb = V.d_bao - u
    c_bao = rb@V.Cinv_bao@rb

    Dc_star = np.interp(zs, T.zg, Dc)
    lAth = np.pi*Dc_star*DH0/rs
    if cfg['R'] == 'aucun':
        dv = np.array([lAth, ob]) - D.DP_V2
        c_cmb = dv@D.DP_CI2@dv
    else:
        Om_R = Om if cfg['R'] == 'etiq' else om_rec/(h*h)
        dv = np.array([np.sqrt(Om_R)*Dc_star, lAth, ob]) - T.DP_V
        c_cmb = dv@T.DP_CI@dv

    c_h0 = ((100*h - T.H0_SH)/T.H0_SH_S)**2
    v = c_sn + c_bao + c_cmb + c_h0
    return float(v) if np.isfinite(v) else 1e9


def departs(eps, cfg):
    """meme correction de parametrage qu'au #190 : sous l'etalonnage coherent la borne
    porte sur om_rec, pas sur l'etiquette."""
    f = A_STAR**(-eps) if cfg['zs'] == 'coh' else 1.0
    return [[s[0], s[1], s[2]*f] for s in STARTS]


def profil(eps, cfg):
    def f(p):
        return chi2_cor(p[0], p[1], p[2], eps, cfg)
    best = None
    for s in departs(eps, cfg):
        r = minimize(f, s, method='Nelder-Mead',
                     options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000, maxfev=4000))
        if best is None or r.fun < best.fun:
            best = r
    return best


def mesure(cfg, lo=-0.050, hi=0.050, pas=0.001):
    xs = np.arange(lo, hi + 1e-12, pas)
    cs = np.array([profil(float(x), cfg).fun for x in xs])
    ok = cs < 1e8
    i = int(np.argmin(np.where(ok, cs, np.inf)))
    c0, e0 = float(cs[i]), float(xs[i])

    def bord(sens):
        j = i
        while 0 <= j + sens < len(xs):
            j += sens
            if not ok[j] or cs[j] > c0 + 1.0:
                return abs(float(xs[j]) - e0)
        return abs(float(xs[-1 if sens > 0 else 0]) - e0)

    i0 = int(np.argmin(np.abs(xs)))
    sp, sm = bord(+1), bord(-1)
    gain = float(cs[i0]) - c0
    sig_loc = abs(e0)/max(min(sp, sm), 1e-9)
    sig_wilks = float(np.sqrt(max(gain, 0.0)))
    return dict(eps=e0, chi2=c0, sp=sp, sm=sm, xs=xs, cs=cs, ok=ok, gain=gain,
                lcdm=float(cs[i0]), sig_loc=sig_loc, sig_wilks=sig_wilks,
                sig=min(sig_loc, sig_wilks))


CFG = {
    'table_etiq':  dict(rs='table',  R='etiq',  zs='etiq'),
    'table_coh':   dict(rs='table',  R='coh',   zs='coh'),
    'direct_sansR': dict(rs='direct', R='aucun', zs='coh'),
    'direct_Rcoh': dict(rs='direct', R='coh',   zs='coh'),
}
ANCIEN = {'table_etiq': +0.0060, 'table_coh': -0.0030,
          'direct_sansR': -0.0100, 'direct_Rcoh': -0.0030}


if __name__ == "__main__":
    import json
    print("LA FAMILLE CORRIGEE : BARYONS STANDARD (criteres geles)\n")

    print("  --- validation A : eps = 0 doit redonner LCDM ---")
    c0 = profil(0.0, CFG['table_etiq']).fun
    print(f"     chi2 = {c0:.4f}   ancre = {CHI2_LCDM}   ecart = {abs(c0-CHI2_LCDM):.5f}"
          f"   -> {'OK' if abs(c0-CHI2_LCDM) < 1e-3 else 'ECHEC'}")
    if abs(c0 - CHI2_LCDM) >= 1e-3:
        sys.exit("     rien n'est publie.")

    print("\n  --- validation B : la correction est-elle visible ? ---")
    visible = False
    for eps in (+0.006, -0.006):
        cn = profil(eps, CFG['table_etiq']).fun
        ca = D.profil(eps, D.CFG['1_table_etiq']).fun
        print(f"     eps = {eps:+.3f}   ancienne famille {ca:10.3f}   corrigee {cn:10.3f}"
              f"   ecart {abs(cn-ca):8.3f}")
        if abs(cn - ca) >= 0.5:
            visible = True
    print(f"     -> {'CORRECTION VISIBLE' if visible else 'CORRECTION COSMETIQUE'}")

    print("\n  --- critere 1 : mesure dans la famille corrigee ---")
    M = {}
    print(f"     {'configuration':<14s} {'eps':>10s} {'sig local':>10s} {'sig Wilks':>10s} "
          f"{'opposable':>10s} {'gain':>8s}")
    for k, cfg in CFG.items():
        M[k] = mesure(cfg)
        m = M[k]
        print(f"     {k:<14s} {m['eps']:+10.5f} {m['sig_loc']:10.2f} {m['sig_wilks']:10.2f} "
              f"{m['sig']:10.2f} {m['gain']:+8.2f}")

    print("\n  --- validation C : les deux signes restent-ils accessibles ? ---")
    okC = True
    for k, m in M.items():
        neg = float(m['ok'][m['xs'] < 0].mean())
        pos = float(m['ok'][m['xs'] > 0].mean())
        if not (neg > 0.90 and pos > 0.90):
            okC = False
        print(f"     {k:<14s} eps<0 : {100*neg:5.1f} %   eps>0 : {100*pos:5.1f} %")
    if not okC:
        sys.exit("     VALIDATION C ECHOUE : mesure unilaterale, rien n'est publie.")

    print("\n  --- critere 2 : le renversement de signe survit-il ? ---")
    e1, e2 = M['table_etiq'], M['table_coh']
    d1, d2 = e1['sig'] >= 2, e2['sig'] >= 2
    if d1 and d2 and np.sign(e1['eps']) != np.sign(e2['eps']):
        v2 = "RENVERSEMENT PERSISTANT"
    elif d1 and d2:
        v2 = "RENVERSEMENT SUPPRIME (les deux etalonnages s'accordent en signe)"
    elif not d1 and not d2:
        v2 = "PLUS DE DETECTION (aucun etalonnage n'atteint 2 sigma opposables)"
    else:
        v2 = "RENVERSEMENT SUPPRIME (un seul etalonnage detecte)"
    print(f"     etiquette {e1['eps']:+.5f} ({e1['sig']:.1f} sig)   "
          f"coherent {e2['eps']:+.5f} ({e2['sig']:.1f} sig)")
    print(f"     -> {v2}")

    print("\n  --- critere 3 : taille de l'erreur ancienne ---")
    retires = []
    for k, m in M.items():
        s = max(min(m['sp'], m['sm']), 1e-9)
        dep = abs(ANCIEN[k] - m['eps'])/s
        if dep > 1.0:
            retires.append(k)
        print(f"     {k:<14s} ancien {ANCIEN[k]:+.5f} -> corrige {m['eps']:+.5f}   "
              f"deplacement {dep:5.2f} sigma  {'-> RETIRE' if dep > 1.0 else ''}")
    if retires:
        print(f"     -> {len(retires)}/4 nombres du #188 et du #190 sont NON OPPOSABLES "
              f"et retires (pas nuances).")

    print("\n  --- critere 4 : confrontation DIRECTE, sans facteur de conversion ---")
    print(f"     Kumar 2025 (PL18 + DESI DR2, vraisemblance complete) : "
          f"eps = {EPS_KUMAR:+.5f} +/- {SIG_KUMAR:.5f}")
    conf = {}
    for k, m in M.items():
        s = np.sqrt(max(min(m['sp'], m['sm']), 1e-9)**2 + SIG_KUMAR**2)
        ec = abs(m['eps'] - EPS_KUMAR)/s
        lab = "COMPATIBLE" if ec < 2 else ("TENSION" if ec < 3 else "DESACCORD")
        conf[k] = (ec, lab)
        print(f"     {k:<14s} eps = {m['eps']:+.5f}   ecart = {ec:5.2f} sigma   {lab}")

    print("\n  --- critere 5 : ce qui reste de l'acquis du #190 ---")
    vals = np.array([m['eps'] for m in M.values()])
    E = float(vals.max() - vals.min())
    v5 = "ACQUIS RENFORCE" if E >= 0.005 else "ACQUIS AFFAIBLI"
    print(f"     etendue des quatre configurations corrigees = {E:.5f}   "
          f"(#190 : 0,01600)")
    print(f"     -> {v5} : le traitement des baryons est une QUATRIEME source d'ambiguite,")
    print(f"        elle s'ajoute aux trois du #190 au lieu d'en retirer une.")

    out = {k: {q: float(m[q]) for q in ('eps', 'chi2', 'sp', 'sm', 'gain', 'sig_loc',
                                        'sig_wilks', 'sig')} for k, m in M.items()}
    out['_validation_B'] = "visible" if visible else "cosmetique"
    out['_verdict_renversement'] = v2
    out['_retires'] = retires
    out['_kumar'] = [EPS_KUMAR, SIG_KUMAR]
    out['_confrontation'] = {k: [float(v[0]), v[1]] for k, v in conf.items()}
    out['_etendue'] = E
    out['_verdict_acquis'] = v5
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "dilution_baryons.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/dilution_baryons.json")
