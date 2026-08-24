#!/usr/bin/env python3
"""L'ARBITRE DE T10 — SUPPRIMER LE CHOIX D'ETALONNAGE, PAS L'ARBITRER.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

CE QUE T10 DEMANDE, ET CE QUE CETTE ETUDE FAIT A LA PLACE.
Le #188 a etabli un fait genant : dans la famille rho_m = Om a^(eps-3) a Lambda constante,
le SEUL choix de l'Om qui alimente les priors comprimes fait passer eps de +0,0060 a
-0,0030, les deux a 3,0 sigma. L'arbitre grave de T10 est "la vraisemblance CMB complete,
qui n'emploie aucun prior comprime et ne laisse donc aucun choix d'etalonnage".
CAMB ne sait pas propager une matiere non-a^-3 : cet arbitre-la n'est pas implementable ici,
et cette etude NE LE REMPLACE PAS. Elle attaque la meme cause par l'autre bout, et il faut
dire lequel : au lieu d'arbitrer entre deux valeurs d'Om, elle SUPPRIME l'entree Om.

LE MECANISME EXACT DU CHOIX (etabli en lisant test_wE_v3).
r_drag, r_star et z_star y sont une table CAMB indexee par (omega_b, omega_m), et
R = sqrt(Om) D_c(z_*) porte un Om explicite. Le "choix d'etalonnage" est donc, litteralement,
le omega_m qu'on donne a cette table. Or r_s est une integrale :
    r_s(z) = INT_0^a(z) c da / (a^2 H(a) sqrt(3(1+R_b))) ,  R_b = (3 omega_b / 4 omega_gamma) a
qui ne demande PAS de omega_m : elle demande H(a), que le modele fournit. En integrant
directement dans le fond du modele, l'entree ambigue disparait. Il reste R, dont le sqrt(Om)
n'a aucune definition dans une famille ou la matiere ne dilue pas en a^-3 : on le traite
separement, et c'est le critere 4.

SONDE DE FAISABILITE PREALABLE (declaree : elle a servi a fixer le seuil du critere A).
Trois sondes hors corpus ont mesure le rapport r_s(direct)/r_s(CAMB). Avec la composition
naive l'ecart varie de 1,1e-2 le long de omega_m (37 sigma sur l_A : inutilisable). Avec
N_eff = 3,046 et le retrait de omega_nu massif (0,00064) de la matiere, il tombe a 1e-6 en
variation. Le seuil du critere A est fixe a 3e-4 -- 300 fois plus lache que la sonde -- pour
que le critere reste un test et non un constat.

COMPOSITION DECLAREE DE L'INTEGRATEUR r_s (c'est elle qui egale CAMB, on l'ecrit) :
    non relativiste : Om h^2 a^(eps-3) - W_NU_M a^-3
    relativiste     : W_G (1 + 0,2271 x 3,046) a^-4
    Lambda          : h^2 - Om h^2 - w_rad
Le fond des DISTANCES reste celui, gele, de l'atlas (Or = Om/3388) : on n'y touche pas.
L'incoherence entre les deux est heritee du pipeline gele, identique dans LCDM et dans le
modele, donc annulee dans un Delta chi2 -- et le critere 7b la mesure au lieu de la supposer.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A0. LE chi2 EST RECONSTRUIT DANS CE FICHIER : il faut prouver qu'il n'a pas change de
     vraisemblance en chemin. Dans la configuration (table, etiquette, etiquette) et a
     eps = 0, il doit redonner l'ancre gelee LCDM 1425,086 a 1e-3 pres. Sans ce controle,
     tout ecart mesure plus bas pourrait etre une erreur de recopie et non un resultat.
  A. L'integrateur direct reproduit r_star de la table CAMB sur la grille declaree
     (omega_b dans {0,0218 ; 0,02236 ; 0,0230} x omega_m dans {0,132 ... 0,155}) avec une
     VARIATION du rapport < 3e-4, soit < 1 sigma sur l_A. C'est la validation dont tout le
     reste depend : sans elle, l'integration directe n'a pas le droit de remplacer la table.
     AVERTISSEMENT D'HONNETETE, ecrit avant execution : le meme test sur r_drag serait
     CIRCULAIRE, puisque z_drag est justement obtenu en inversant notre integrateur contre
     le r_drag de CAMB — l'accord y serait exact par construction et ne prouverait rien.
     A la place on exige de z_drag deux choses verifiables : qu'il tombe dans [1000 ; 1100]
     partout sur la grille, et qu'il reste sous 1085 (il doit preceder z_star ~ 1090).
  B. A eps = 0, l'optimum LCDM du nouveau chi2 doit rester celui du corpus :
     |Delta Om| < 0,02 et |Delta h| < 0,01. Sinon le changement de statistique a deplace le
     modele et aucune comparaison avec le #188 n'est legitime.
  C. Les deux signes de eps restent accessibles a >= 90 % de chaque cote sur la grille.

AVERTISSEMENT DE COMPARABILITE (gele). Le critere 3 retire R du vecteur de donnees : ses
chi2 ABSOLUS ne sont pas comparables a ceux du #188. Seuls les Delta chi2 contre LCDM
CALCULES DANS LA MEME CONFIGURATION le sont. Aucun AIC n'est rapporte ici.

--- CRITERES (exhaustifs, exclusifs) ---
  1. REPRODUCTION DU #188, etalonnage-etiquette, pipeline inchange. Doit redonner
     eps = +0,0060 a +/-0,0010 pres. Si non : l'etude s'arrete, le desaccord est le resultat.
  2. REPRODUCTION DU #188, etalonnage-coherent. Doit redonner -0,0030 a +/-0,0010 pres.
     Meme consequence.
  3. L'ARBITRE : r_s par integration directe, R RETIRE du vecteur (on garde (l_A, omega_b)
     avec la covariance marginale 2x2 de Planck, obtenue en inversant le bloc 2x2 de la
     COVARIANCE -- pas en tronquant son inverse). Dans cette configuration il n'existe
     AUCUNE entree omega_m ambigue. On rapporte eps, sigma par profil, gain sur LCDM.
  4. DECOMPOSITION -- quel ingredient portait le renversement ? r_s direct, mais R CONSERVE,
     alimente successivement par l'etiquette et par la densite a la recombinaison.
     Si les deux donnent alors le MEME signe : le renversement vivait dans r_s, et
        l'integration directe l'a tue.
     S'ils donnent encore des signes OPPOSES : le renversement vit dans R, dont le sqrt(Om)
        n'est pas defini dans cette famille, et le critere 3 est le seul nombre licite.
     C'est le contenu scientifique de l'etude : il ne suffit pas de trancher, il faut savoir
     ce qui trompait.
  5. VERDICT SUR T10 (nomme les trois lectures gravees) :
     LECTURE 1 SELECTIONNEE (l'etalonnage coherent etait le bon ; la classe publiee porte un
        signe faux) si le critere 3 rend eps <= -2 sigma ;
     LECTURE 2 SELECTIONNEE (l'etalonnage-etiquette est defendable ; notre reformulation
        etait l'artefact) si le critere 3 rend eps >= +2 sigma ;
     LECTURE 3 SELECTIONNEE (rien de mesurable ici) si |eps| < 2 sigma au critere 3 ;
     T10 NON RESOLUE si le critere 4 laisse une ambiguite residuelle >= 2 sigma sur eps :
        dans ce cas le verdict ci-dessus est rapporte mais NON applique, et T10 reste ouverte
        avec un enonce retreci. Regle 9 : l'ambigu ne devient pas une victoire.
  6. CONTRAINTE PUBLIABLE : intervalle bilateral a 2 sigma sur eps sous le critere 3.
  7. CONTROLES DE ROBUSTESSE, rapportes meme s'ils sont bons :
     a. z_* alimente par l'etiquette au lieu de la densite a la recombinaison. Si eps bouge
        de >= 0,5 sigma, le choix de z_* est declare ambiguite residuelle et verse au 5.
     b. rayonnement de l'atlas (Or = Om/3388) au lieu du rayonnement physique dans r_s.
        Meme seuil, meme consequence.

REGLE 6 APPLIQUEE. Cette etude defend implicitement que l'etalonnage coherent (#166) etait
le bon. Les seuils sont donc choisis DEFAVORABLEMENT a cette these : le seuil de detection
est 2 sigma dans les deux sens, la lecture 2 a exactement le meme droit que la lecture 1, et
le critere 4 peut invalider les deux.
Regle 3 : cette etude REDUIT le nombre de lectures possibles ; elle ne ferme pas T10.
Usage : python3 scripts/dilution_arbitre.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import test_wE_v3 as T
import vraisemblance_reelle as V

AG = A.AG
C_KM = T.C_KM
W_G = 2.4735e-5                       # Omega_gamma h^2, T_CMB = 2,7255 K
W_RAD = W_G*(1.0 + 0.2271*3.046)      # + 3,046 neutrinos sans masse
W_NU_M = 0.00064                      # omega_nu massif, tel que la table CAMB a ete batie
A_STAR = 1.0/1091.0
NA, A_LO = 4000, 1e-10        # maillage log ; sonde 4 : fidelite 1,3e-6, borne basse
                              # convergee a 2e-6. Le lineaire a 300 000 pts donne le meme
                              # nombre pour 86 fois le cout.
STARTS = [[0.69, 0.02236, 0.31], [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]
EPS_188_ETIQ, EPS_188_COH = +0.0060, -0.0030
TOL_188 = 0.0010

# covariance marginale 2x2 sur (l_A, omega_b) : bloc de la COVARIANCE puis inversion
DP_V2 = T.DP_V[1:]
DP_CI2 = np.linalg.inv(T.DP_C[1:, 1:])


# ---------------------------------------------------------------- integrateur direct
def rs_direct(a_hi, Om, ob, h, eps, ray='phys'):
    """r_s en Mpc, integre dans le fond du modele. AUCUNE entree omega_m."""
    if not np.isfinite(a_hi) or a_hi <= 0:
        return np.nan
    om = Om*h*h
    w_rad = W_RAD if ray == 'phys' else om/3388.0
    nu = W_NU_M if ray == 'phys' else 0.0
    lna = np.linspace(np.log(A_LO), np.log(a_hi), NA)
    a = np.exp(lna)
    h2E2 = om*a**(eps - 3.0) - nu/a**3 + w_rad/a**4 + (h*h - om - w_rad)
    if np.any(h2E2 <= 0):
        return np.nan
    Hz = 100.0*np.sqrt(h2E2)
    Rb = (3.0*ob/(4.0*W_G))*a
    return float(np.trapezoid(C_KM/(a*Hz*np.sqrt(3.0*(1.0 + Rb))), lna))


# ---------------------------------------------------------------- z_drag par inversion
def _table_zdrag():
    """z_drag n'est pas tabule par le corpus. On le RECUPERE en inversant notre integrateur
    contre le r_drag de CAMB, a LCDM, sur la grille meme ou la table CAMB a ete batie ;
    c'est licite parce que la validation A montre que les deux integrateurs sont le meme.
    z_drag est ensuite traite comme z_star : une quantite de recombinaison, fonction de
    (omega_b, omega_m A CETTE EPOQUE) et non de eps."""
    from scipy.interpolate import RectBivariateSpline
    obs = np.linspace(0.0215, 0.0232, 7)
    oms = np.linspace(0.132, 0.155, 9)
    Z = np.zeros((len(obs), len(oms)))
    h_ref = 0.675                                    # H0 de construction de la table CAMB
    for i, ob in enumerate(obs):
        for j, om in enumerate(oms):
            cible = T.r_drag(ob, om)
            lo, hi = 900.0, 1250.0
            for _ in range(45):
                mid = 0.5*(lo + hi)
                r = rs_direct(1.0/(1.0 + mid), om/(h_ref*h_ref), ob, h_ref, 0.0)
                if r > cible:
                    lo = mid
                else:
                    hi = mid
            Z[i, j] = 0.5*(lo + hi)
    return RectBivariateSpline(obs, oms, Z, kx=3, ky=3)


_SPZD = _table_zdrag()


def z_drag(ob, om):
    return float(_SPZD(ob, om)[0, 0])


# ---------------------------------------------------------------- fond des distances
def fond_arb(Om, eps):
    """fond des DISTANCES : celui, gele, de l'atlas. On n'y touche pas."""
    Or = Om/3388.0
    lam = 1 - Om - Or
    if lam <= 0:
        return None
    return A.fond_arrays(Om*AG**(eps - 3) + Or/AG**4 + lam)


A.CUSTOM['dil_arb'] = fond_arb


# ---------------------------------------------------------------- chi2 reconstruit
def chi2_cfg(h, ob, Om, eps, cfg):
    """cfg : dict(rs='table'|'direct', R='etiq'|'coh'|'aucun', zs='coh'|'etiq', ray=...)"""
    if not (0.55 < h < 0.85 and 0.0200 < ob < 0.0245 and 0.15 < Om < 0.55):
        return 1e9
    om = Om*h*h
    om_rec = om*A_STAR**eps                      # densite de matiere A LA RECOMBINAISON
    om_tab = om_rec if cfg['zs'] == 'coh' else om
    if not (0.132 < om_tab < 0.155):
        return 1e9
    fo = fond_arb(Om, eps)
    if fo is None:
        return 1e9
    zz, Ea = fo
    Ez = np.interp(T.zg, zz, Ea)
    if not np.all(np.isfinite(Ez)) or np.any(Ez <= 0):
        return 1e9
    inv = 1.0/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:] + inv[:-1])*np.diff(T.zg))])
    DH0 = C_KM/(100*h)

    zs = T.z_star(ob, om_tab)
    if cfg['rs'] == 'table':
        rd, rs = T.r_drag(ob, om_tab), T.r_star(ob, om_tab)
    else:
        zd = z_drag(ob, om_tab)
        rd = rs_direct(1.0/(1.0 + zd), Om, ob, h, eps, cfg['ray'])
        rs = rs_direct(1.0/(1.0 + zs), Om, ob, h, eps, cfg['ray'])
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
        dv = np.array([lAth, ob]) - DP_V2
        c_cmb = dv@DP_CI2@dv
    else:
        Om_R = Om if cfg['R'] == 'etiq' else Om*A_STAR**eps
        dv = np.array([np.sqrt(Om_R)*Dc_star, lAth, ob]) - T.DP_V
        c_cmb = dv@T.DP_CI@dv

    c_h0 = ((100*h - T.H0_SH)/T.H0_SH_S)**2
    v = c_sn + c_bao + c_cmb + c_h0
    return float(v) if np.isfinite(v) else 1e9


def departs(eps, cfg):
    """DEFAUT DE PARAMETRAGE CORRIGE AVANT TOUT RESULTAT (corps seulement, criteres intacts).
    Sous l'etalonnage coherent le parametre ajuste est l'ETIQUETTE Om, mais la borne
    0,132 < om_tab < 0,155 porte sur om a_*^eps. A |eps| >~ 0,025 les trois departs geles
    tombent donc tous hors domaine et le profil est PERDU -- ce qui aurait fait echouer la
    validation C pour une raison de parametrage et non de physique (sonde 5 hors corpus :
    0/3 departs finis a eps = -0,05). On decale donc le depart de Om par a_*^(-eps), ce qui
    est exactement la reparametrisation qu'employait le #188 (ou le parametre ajuste etait
    deja Om_cal). Aucun critere, aucune borne et aucune donnee ne changent."""
    f = A_STAR**(-eps) if cfg['zs'] == 'coh' else 1.0
    return [[s[0], s[1], s[2]*f] for s in STARTS]


def profil(eps, cfg):
    def f(p):
        return chi2_cfg(p[0], p[1], p[2], eps, cfg)
    best = None
    for s in departs(eps, cfg):
        r = minimize(f, s, method='Nelder-Mead',
                     options=dict(xatol=1e-6, fatol=1e-4, maxiter=4000, maxfev=4000))
        if best is None or r.fun < best.fun:
            best = r
    return best


def mesure(cfg, lo=-0.030, hi=0.030, pas=0.0010):
    xs = np.arange(lo, hi + 1e-12, pas)
    out = [profil(float(x), cfg) for x in xs]
    cs = np.array([o.fun for o in out])
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
    return dict(eps=e0, chi2=c0, sp=sp, sm=sm, xs=xs, cs=cs, ok=ok,
                lcdm=float(cs[i0]), par0=out[i0].x,
                sig=abs(e0)/max(min(sp, sm), 1e-9), gain=float(cs[i0]) - c0)


# ---------------------------------------------------------------- configurations gelees
CFG = {
    '1_table_etiq':  dict(rs='table',  R='etiq',  zs='etiq', ray='phys'),
    '2_table_coh':   dict(rs='table',  R='coh',   zs='coh',  ray='phys'),
    '3_arbitre':     dict(rs='direct', R='aucun', zs='coh',  ray='phys'),
    '4a_direct_R_e': dict(rs='direct', R='etiq',  zs='coh',  ray='phys'),
    '4b_direct_R_c': dict(rs='direct', R='coh',   zs='coh',  ray='phys'),
    '7a_zs_etiq':    dict(rs='direct', R='aucun', zs='etiq', ray='phys'),
    '7b_ray_atlas':  dict(rs='direct', R='aucun', zs='coh',  ray='atlas'),
}


if __name__ == "__main__":
    import json
    print("L'ARBITRE DE T10 (criteres geles)\n")
    ECHEC = []

    # ---------------- validation A0 : le chi2 reconstruit est-il le chi2 gele ?
    print("  --- validation A0 : le chi2 reconstruit est-il celui du corpus ? ---")
    r0 = profil(0.0, CFG['1_table_etiq'])
    ecart = abs(r0.fun - 1425.086)
    print(f"     chi2(LCDM) reconstruit = {r0.fun:.4f}   ancre gelee = 1425.086   "
          f"ecart = {ecart:.5f}  -> {'OK' if ecart < 1e-3 else 'ECHEC'}")
    if ecart >= 1e-3:
        sys.exit("     le chi2 a change de vraisemblance : rien n'est publie.")
    h_ref, ob_ref, Om_ref = (float(v) for v in r0.x)
    print(f"     optimum gele : h = {h_ref:.5f}  ob = {ob_ref:.5f}  Om = {Om_ref:.5f}")

    # ---------------- validation A : l'integrateur direct EST l'integrateur de CAMB
    print("\n  --- validation A : integration directe contre table CAMB (r_star) ---")
    rap = []
    for ob in (0.0218, 0.02236, 0.0230):
        for om in np.linspace(0.132, 0.155, 9):
            Om_x = om/(0.675**2)
            zs_x = T.z_star(ob, om)
            rap.append(rs_direct(1.0/(1.0 + zs_x), Om_x, ob, 0.675, 0.0)/T.r_star(ob, om))
    rap = np.array(rap)
    var = float(rap.max() - rap.min())
    print(f"     rapport moyen {rap.mean():.6f}   variation {1e4*var:.3f} x 1e-4  "
          f"({1e4*var/3.0:.2f} sigma sur l_A)  -> {'OK' if var < 3e-4 else 'ECHEC'}")
    if var >= 3e-4:
        sys.exit("     l'integration directe n'a pas le droit de remplacer la table.")
    zds = np.array([z_drag(ob, om) for ob in (0.0218, 0.02236, 0.0230)
                    for om in np.linspace(0.132, 0.155, 9)])
    ok_zd = bool(zds.min() > 1000 and zds.max() < 1085)
    print(f"     z_drag inferes : [{zds.min():.2f} ; {zds.max():.2f}]  "
          f"(exige [1000 ; 1085], et z_star ~ 1090)  -> {'OK' if ok_zd else 'ECHEC'}")
    if not ok_zd:
        sys.exit("     z_drag non physique : rien n'est publie.")

    # ---------------- les sept mesures
    print("\n  --- balayage (7 configurations) ---")
    M = {}
    for k, c in CFG.items():
        M[k] = mesure(c)
        m = M[k]
        print(f"     [{k:<14s}] eps = {m['eps']:+.5f} +{m['sp']:.5f}/-{m['sm']:.5f}  "
              f"({m['sig']:4.1f} sigma)  gain = {m['gain']:+.2f}")

    # ---------------- validation B
    print("\n  --- validation B : l'optimum LCDM a-t-il bouge sous le nouveau chi2 ? ---")
    p3 = M['3_arbitre']['par0']
    dh, dOm = abs(float(p3[0]) - h_ref), abs(float(p3[2]) - Om_ref)
    okB = dh < 0.01 and dOm < 0.02
    print(f"     arbitre : h = {p3[0]:.5f} (ecart {dh:.5f})   "
          f"Om = {p3[2]:.5f} (ecart {dOm:.5f})  -> {'OK' if okB else 'ECHEC'}")
    if not okB:
        sys.exit("     le changement de statistique a deplace le modele : rien n'est publie.")

    # ---------------- validation C
    print("\n  --- validation C : les deux signes restent-ils accessibles ? ---")
    m3 = M['3_arbitre']
    neg = float(m3['ok'][m3['xs'] < 0].mean())
    pos = float(m3['ok'][m3['xs'] > 0].mean())
    okC = neg > 0.90 and pos > 0.90
    print(f"     eps < 0 : {100*neg:.1f} %   eps > 0 : {100*pos:.1f} %  "
          f"-> {'OK' if okC else 'ECHEC'}")
    if not okC:
        sys.exit("     une branche est fermee : la mesure serait unilaterale (cf. #173).")

    # ---------------- criteres 1 et 2 : reproduction du #188
    print("\n  --- criteres 1 et 2 : le #188 est-il reproduit ? ---")
    rep = {}
    for tag, k, cible in (("1", '1_table_etiq', EPS_188_ETIQ),
                          ("2", '2_table_coh', EPS_188_COH)):
        d = abs(M[k]['eps'] - cible)
        rep[tag] = d <= TOL_188
        print(f"     [{tag}] mesure {M[k]['eps']:+.5f}   #188 {cible:+.5f}   "
              f"ecart {d:.5f}  -> {'REPRODUIT' if rep[tag] else 'NON REPRODUIT'}")
    if not (rep["1"] and rep["2"]):
        ECHEC.append("le #188 n'est pas reproduit : le desaccord EST le resultat, "
                     "et l'arbitrage ne porte plus sur ce qu'il pretendait arbitrer")
        print("     -> " + ECHEC[-1])

    # ---------------- critere 3 : l'arbitre
    print("\n  --- critere 3 : L'ARBITRE (aucune entree omega_m ambigue) ---")
    print(f"     eps = {m3['eps']:+.5f} +{m3['sp']:.5f}/-{m3['sm']:.5f}   "
          f"{m3['sig']:.1f} sigma   gain sur LCDM = {m3['gain']:+.2f}")

    # ---------------- critere 4 : decomposition
    print("\n  --- critere 4 : quel ingredient portait le renversement ? ---")
    e4a, e4b = M['4a_direct_R_e']['eps'], M['4b_direct_R_c']['eps']
    sig3 = max(min(m3['sp'], m3['sm']), 1e-9)
    amb = abs(e4a - e4b)/sig3
    meme_signe = (np.sign(e4a) == np.sign(e4b)) or e4a == 0 or e4b == 0
    print(f"     r_s direct, R par etiquette : eps = {e4a:+.5f}")
    print(f"     r_s direct, R par recombin. : eps = {e4b:+.5f}")
    print(f"     ecart residuel = {amb:.2f} sigma (unite : sigma du critere 3)")
    if meme_signe:
        v4 = ("LE RENVERSEMENT VIVAIT DANS r_s — l'integration directe l'a tue, "
              "les deux lectures de R donnent desormais le meme signe")
    else:
        v4 = ("LE RENVERSEMENT VIT DANS R — dont le sqrt(Om) n'est pas defini dans cette "
              "famille ; le critere 3 est alors le seul nombre licite")
    print(f"     -> {v4}")

    # ---------------- critere 7 : controles
    print("\n  --- critere 7 : controles de robustesse ---")
    ctrl = {}
    for tag, k, quoi in (("7a", '7a_zs_etiq', "z_* par l'etiquette"),
                         ("7b", '7b_ray_atlas', "rayonnement de l'atlas dans r_s")):
        d = abs(M[k]['eps'] - m3['eps'])/sig3
        ctrl[tag] = d
        print(f"     [{tag}] {quoi:<34s} eps = {M[k]['eps']:+.5f}   "
              f"deplacement {d:.2f} sigma  -> {'stable' if d < 0.5 else 'AMBIGUITE RESIDUELLE'}")
    amb_tot = max([amb] + [v for v in ctrl.values() if v >= 0.5])

    # ---------------- critere 5 : verdict sur T10
    print("\n  --- critere 5 : VERDICT SUR T10 ---")
    if m3['sig'] >= 2 and m3['eps'] < 0:
        lect = ("LECTURE 1 SELECTIONNEE : l'etalonnage coherent etait le bon ; la classe "
                "publiee de ces mesures porte un signe defendable et notre #188 le confirme")
    elif m3['sig'] >= 2 and m3['eps'] > 0:
        lect = ("LECTURE 2 SELECTIONNEE : le signe positif survit a la suppression du choix ; "
                "c'est notre reformulation coherente qui etait l'artefact")
    else:
        lect = ("LECTURE 3 SELECTIONNEE : sans priors comprimes il n'y a rien de mesurable "
                "ici — les deux detections a 3 sigma du #188 etaient produites par "
                "l'etalonnage, pas par les donnees")
    bloque = (amb >= 2.0) or bool(ECHEC)
    print(f"     {lect}")
    if bloque:
        print("\n     T10 NON RESOLUE : ambiguite residuelle "
              f"{amb:.2f} sigma au critere 4"
              + ("" if not ECHEC else " ; et : " + " ; ".join(ECHEC)))
        print("     Le verdict ci-dessus est RAPPORTE mais NON APPLIQUE (regle 9).")
        verdict = "T10 NON RESOLUE — " + lect.split(" : ")[0]
    else:
        print("\n     T10 RESOLUE par ce critere, sous les limites declarees en en-tete "
              "(ceci n'est PAS la vraisemblance CMB complete).")
        verdict = "T10 TRANCHEE — " + lect.split(" : ")[0]

    # ---------------- critere 6 : contrainte publiable
    sel = m3['ok'] & (m3['cs'] <= m3['chi2'] + 4.0)
    lo2, hi2 = float(m3['xs'][sel].min()), float(m3['xs'][sel].max())
    print(f"\n  CRITERE 6 (contrainte publiable) : eps dans [{lo2:+.4f} ; {hi2:+.4f}] "
          f"a 2 sigma (bilateral), sous le critere 3")
    print(f"     zero {'EXCLU' if (lo2 > 0 or hi2 < 0) else 'INCLUS'} par cet intervalle")

    print("\n  Rappel gele : cette etude ne remplace pas l'arbitre de T10 (CAMB ne propage")
    print("  pas une matiere non-a^-3). Elle supprime le choix d'etalonnage au lieu de")
    print("  l'arbitrer. Regle 3 : elle REDUIT le nombre de lectures ; elle ne ferme rien.")

    out = {k: {q: (float(v) if isinstance(v, (int, float, np.floating)) else None)
               for q, v in m.items() if q in ('eps', 'chi2', 'sp', 'sm', 'sig', 'gain',
                                              'lcdm')}
           for k, m in M.items()}
    out['_verdict'] = verdict
    out['_critere4'] = v4
    out['_intervalle'] = [lo2, hi2]
    out['_ambiguite_sigma'] = float(amb)
    out['_controles'] = {k: float(v) for k, v in ctrl.items()}
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "dilution_arbitre.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/dilution_arbitre.json")
