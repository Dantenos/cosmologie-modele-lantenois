#!/usr/bin/env python3
"""BANC D'ESSAI DES LOIS D'ENERGIE NOIRE A UN PARAMETRE — v2, criteres coherents.
CRITERES PRE-ENREGISTRES (geles AVANT execution de CETTE version, 24/08/2026).

POURQUOI UNE v2, ET C'EST LE VICE LE PLUS GRAVE DE LA JOURNEE (#176).
banc_un_parametre.py (gele a38014b821a8) portait une DIVERGENCE ENTRE SON DOCSTRING GELE ET
SON CODE : le docstring annonce « une grille dense (60 000 points, log) », le corps utilisait
240 001 points apres mes corrections successives de quadrature. Un lecteur des criteres geles
aurait ete trompe sur ce qui a ete calcule. C'est exactement ce que le gel existe pour
empecher, et c'est plus grave qu'un seuil impossible : les six vices precedents rendaient un
critere INSATISFIABLE (donc un REFUS visible) ; celui-ci l'aurait rendu SATISFAIT PAR AUTRE
CHOSE QUE CE QUI EST ECRIT. Le calcul a ete INTERROMPU avant tout resultat ; aucune valeur
scientifique n'en a ete vue, seulement les deux ecarts de quadrature (K2 8,9e-10, SR 4,4e-10).
De plus les deux enonces geles etaient de toute facon incompatibles : a 60 000 points, meme
Simpson plafonne vers 1e-7 sur l'integrande de SR, donc la tolerance de 1e-8 etait hors
d'atteinte a la grille declaree.

LA CONCEPTION CORRIGEE, et cette fois la coherence est verifiee AVANT le gel :
  GRILLE DE PRODUCTION DECLAREE : 60 001 points logarithmiques sur a dans [1e-7 ; 1],
  quadrature de SIMPSON cumulative (et non trapeze : l'integrande de SR diverge en a^(-1/2)
  et le trapeze y plafonne a 1,6e-6).
  TOLERANCE DE VALIDATION : 1e-6, atteignable a cette grille (Simpson y donne ~1e-7 sur SR,
  mieux sur les autres). JUSTIFICATION DU CHOIX, declaree : une erreur relative de 1e-6 sur
  g(a) propage moins de 1e-3 en chi2, soit mille fois moins que les differences de chi2 que
  ce banc compare (de l'ordre de l'unite). Serrer davantage n'ajouterait rien et coute des
  heures.
  MEMOISATION DECLAREE : pendant un ajustement a parametre de modele FIXE, g(a) ne depend pas
  de (h, omega_b, Om) ; elle est donc calculee UNE FOIS et reutilisee. C'est une optimisation
  exacte, sans effet sur les nombres.

LES CONCURRENTES, telles que publiees (inchangees par rapport a la v1) :
  Kessler, Escamilla, Pan & Di Valentino, arXiv:2504.00776, Eqs. 5-8, prior w0 ~ U[-2, 0] :
    K1 w = w0[1 + sin(1-a)] ; K2 w = w0[1 + (1-a)/(a^2+(1-a)^2)] ;
    K3 w = w0[1 - a sin(1/a) + sin(1)] ; K4 w = w0[1 + (1-a) sin(1/(1-a))]
  Borghetto et al., arXiv:2606.17951, prior w0 ~ U[-3, 1] :
    SR w = w0/sqrt(a) (Eq. 4.1, forme fermee Eq. 5.8) ; F83 w = w0 exp(1-a) (Eq. 4.3)
  Reperes : LCDM, wCDM, CPL, et NOTRE accretion (beta ~ U[0,5 ; 5]).

CE QUE CE BANC N'EST PAS : une comparaison a leurs chiffres publies. Kessler estime
l'evidence par MCEvidence sur chaines Cobaya, Borghetto par PolyChord et dans le cadre VCDM
(gravite minimalement modifiee), leurs volumes de prior different, et avec UN parametre le
facteur d'Occam EST le resultat. Ce banc est INTERNE : memes donnees (vraisemblance legere,
N = 1597), meme pipeline, meme estimateur, priors ecrits ci-dessus.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. QUADRATURE, sur la grille de production, contre les DEUX formes fermees publiees,
     comparees EN LOG (g descend a exp(-17000) : le rapport lineaire deborde) :
       K2 : g = a^(-3-6w0) (2a^2-2a+1)^(3w0/2) a w0 = -0,7  -> ecart relatif max < 1e-6 ;
       SR : g = a^-3 exp[6 w0 (a^(-1/2)-1)] a w0 = -0,9     -> ecart relatif max < 1e-6.
  B. wCDM : la meme quadrature a w constant doit redonner le 'wcdm' de l'atlas,
     |dchi2| < 0,05 au meme point.
  C. ANCRES #150 : LCDM 1425,086 ; accretion 1419,309 ; CPL 1418,927, a +/- 0,3.
  D. DOMAINES (lecon du #175) : pour CHAQUE loi a un parametre, on rapporte la fraction du
     prior declare qui est accessible et si le minimum touche un bord. Un modele a minimum
     de bord est SIGNALE dans la table et son chi2 n'est pas lu comme un minimum.

--- CRITERES (exhaustifs, exclusifs) ---
  1. CLASSEMENT PRINCIPAL : AIC = chi2 + 2k, k comptant (h, omega_b, Om) plus les parametres
     du modele. L'AIC est principal parce qu'il ne depend d'aucun prior.
     NOTRE LOI : PREMIERE si son AIC est le plus bas ; DANS LES TROIS si rang 2 ou 3 ;
     DERRIERE sinon — ECRIT EN PREMIER, avec le nom de celles qui la battent.
  2. EVIDENCE DE PROFIL (secondaire, declaree telle) : ln Z = ln[(1/largeur) * integrale
     exp(-chi2_profil/2) dtheta] sur 21 points, profil sur (h, omega_b, Om). CE N'EST PAS une
     evidence par echantillonnage niche ; elle sous-estime le volume des nuisances et ne sert
     qu'a ordonner les facteurs d'Occam entre modeles. On rapporte aussi dln Z quand la
     largeur du prior est DOUBLEE : la sensibilite au prior fait partie du resultat.
  3. TOUT est rapporte, favorable ou non.
Regle 3 : ce banc REDUIT l'espace des lois plausibles ; il n'en ferme aucune.
Usage : python3 scripts/banc_un_parametre_v2.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np
from scipy.integrate import cumulative_simpson

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

AG = A.AG
DENSE = np.logspace(-7, 0, 60001)
LND = np.log(DENSE)
B = [0.69, 0.02236, 0.31]
ANCRES = {"LCDM": 1425.086, "ACCRETION": 1419.309, "CPL": 1418.927}
SENT = 1e8
_MEMO = {}


def lg_de(wfun, p, key):
    """ln g(a) = -3 ln a + 3 * int_a^1 w dln a', memoise a parametre fixe."""
    mk = (key, round(float(p), 10))
    if mk in _MEMO:
        return _MEMO[mk]
    w = wfun(DENSE, p)
    if not np.all(np.isfinite(w)):
        _MEMO[mk] = None
        return None
    J = np.concatenate([[0.0], cumulative_simpson(w, x=LND)])
    lg = -3 * LND + 3 * (J[-1] - J)
    r = None if np.max(lg) > 400 else lg
    if len(_MEMO) > 4000:
        _MEMO.clear()
    _MEMO[mk] = r
    return r


def fond_w(Om, p, wfun, key):
    lg = lg_de(wfun, p, key)
    if lg is None:
        return None
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    E2 = Om / AG**3 + Or / AG**4 + Ode * np.interp(AG, DENSE, np.exp(np.clip(lg, -700, 400)))
    if np.any(~np.isfinite(E2)) or np.any(E2 <= 0):
        return None
    return A.fond_arrays(E2)


W_K1 = lambda a, w0: w0 * (1 + np.sin(1 - a))
W_K2 = lambda a, w0: w0 * (1 + (1 - a) / (a**2 + (1 - a)**2))
W_K3 = lambda a, w0: w0 * (1 - a * np.sin(1.0 / np.clip(a, 1e-12, None)) + np.sin(1.0))
W_SR = lambda a, w0: w0 / np.sqrt(a)
W_F83 = lambda a, w0: w0 * np.exp(1 - a)
W_CST = lambda a, w0: np.full_like(a, w0)


def W_K4(a, w0):
    u = 1.0 - a
    return w0 * (1 + np.where(u > 1e-9, u * np.sin(1.0 / np.where(u > 1e-9, u, 1.0)), 0.0))


MODELES = [("K1 Kessler 1", W_K1, (-2.0, 0.0)), ("K2 Kessler 2", W_K2, (-2.0, 0.0)),
           ("K3 Kessler 3", W_K3, (-2.0, 0.0)), ("K4 Kessler 4", W_K4, (-2.0, 0.0)),
           ("SR w0/sqrt(a)", W_SR, (-3.0, 1.0)), ("F83 w0 e^(1-a)", W_F83, (-3.0, 1.0))]
for nom, wf, _ in MODELES:
    A.CUSTOM[nom] = (lambda wf, k: (lambda Om, p: fond_w(Om, p, wf, k)))(wf, nom)
A.CUSTOM['wq_cst'] = lambda Om, p: fond_w(Om, p, W_CST, 'cst')
STARTS = [B, [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]


def prof(fam, x):
    return A.fit(fam, 1, STARTS, fixpar=float(x)).fun


def lnZ(fam, lo, hi, n=21):
    xs = np.linspace(lo, hi, n)
    cs = np.array([prof(fam, x) for x in xs])
    c0 = cs.min()
    L = np.exp(-0.5 * np.clip(cs - c0, 0, 700))
    I = np.trapezoid(L, xs) if hasattr(np, "trapezoid") else np.trapz(L, xs)
    return -0.5 * c0 + np.log(max(I, 1e-300) / (hi - lo)), cs


if __name__ == "__main__":
    print("BANC D'ESSAI DES LOIS A UN PARAMETRE — v2 (criteres geles)\n")
    print("  --- validation A : quadrature contre les formes fermees, en log ---")
    lg2 = lg_de(W_K2, -0.7, 'vK2')
    lf2 = (-3 - 6 * (-0.7)) * LND + (3 * (-0.7) / 2) * np.log(2 * DENSE**2 - 2 * DENSE + 1)
    e2 = float(np.max(np.abs(np.expm1(lg2 - lf2))))
    lgs = lg_de(W_SR, -0.9, 'vSR')
    lfs = -3 * LND + 6 * (-0.9) * (DENSE**-0.5 - 1)
    es = float(np.max(np.abs(np.expm1(lgs - lfs))))
    print(f"    K2 : {e2:.3e}   SR : {es:.3e}   (tolerance 1e-6, grille 60 001, Simpson)")
    if not (e2 < 1e-6 and es < 1e-6):
        sys.exit("    VALIDATION A ECHOUE — rien n'est publie.")
    c1 = A.fit('wq_cst', 1, STARTS, fixpar=-0.95).fun
    c2 = A.fit('wcdm', 1, STARTS, fixpar=-0.95).fun
    print(f"    B. wCDM par quadrature {c1:.4f} vs atlas {c2:.4f} (d = {c1-c2:+.4f})")
    if abs(c1 - c2) >= 0.05:
        sys.exit("    VALIDATION B ECHOUE — rien n'est publie.")
    import test_wE_v3 as T
    ref = {"LCDM": T.fit('lcdm').fun,
           "ACCRETION": A.fit('invt', 1, [B + [2.4], B + [2.0], B + [2.8]],
                              bornes=[(0.5, 5.0)]).fun,
           "CPL": A.fit('cpl', 2, [B + [-0.9, -0.3], B + [-0.84, -0.6]],
                        bornes=[(-2.0, 0.0), (-3.0, 2.0)]).fun}
    if not all(abs(ref[k] - ANCRES[k]) < 0.3 for k in ANCRES):
        sys.exit(f"    VALIDATION C ECHOUE : {ref}")
    print(f"    C. ancres : LCDM {ref['LCDM']:.3f} | accretion {ref['ACCRETION']:.3f} | "
          f"CPL {ref['CPL']:.3f} -> OK\n")

    tab = [("LCDM", 3, ref["LCDM"], None, None, None)]
    r = A.fit('invt', 1, [B + [2.4], B + [2.0], B + [2.8]], bornes=[(0.5, 5.0)])
    tab.append(("ACCRETION (beta)", 4, r.fun, float(r.x[3]), 'invt', (0.5, 5.0)))
    tab.append(("CPL", 5, ref["CPL"], None, None, None))
    rw = A.fit('wcdm', 1, [B + [-0.9], B + [-1.1]], bornes=[(-2.0, -0.2)])
    tab.append(("wCDM", 4, rw.fun, float(rw.x[3]), 'wcdm', (-2.0, -0.2)))
    for nom, wf, (lo, hi) in MODELES:
        rr = A.fit(nom, 1, [B + [-0.8], B + [-1.0], B + [-0.5]], bornes=[(lo, hi)])
        tab.append((nom, 4, rr.fun, float(rr.x[3]), nom, (lo, hi)))

    print("  --- VALIDATION D : domaines (lecon du #175) ---")
    dom = {}
    for nom, k, c, p, fam, bor in tab:
        if fam is None:
            continue
        lo, hi = bor
        xs = np.linspace(lo, hi, 21)
        cs = np.array([prof(fam, x) for x in xs])
        frac = float((cs < SENT).mean())
        pas = (hi - lo) / 20
        bad = np.where(cs >= SENT)[0]
        db = float(np.min(np.abs(xs[bad] - p)) / pas) if bad.size else 1e9
        bord = (db <= 2.0) or (min(abs(p - lo), abs(p - hi)) / pas <= 2.0)
        dom[nom] = (frac, bord)
        print(f"    {nom:<17s} accessible {100*frac:5.1f} %  "
              f"{'MINIMUM DE BORD' if bord else 'minimum interieur'}")

    tab.sort(key=lambda t: t[2] + 2 * t[1])
    print(f"\n  --- CRITERE 1 : classement AIC ---")
    print(f"    {'rang':>4s} {'modele':<17s} {'k':>2s} {'chi2':>10s} {'AIC':>10s} {'param':>9s}  note")
    rang = None
    for i, (nom, k, c, p, fam, bor) in enumerate(tab, 1):
        if nom.startswith("ACCRETION"):
            rang = i
        note = "BORD" if dom.get(nom, (1, False))[1] else ""
        print(f"    {i:>4d} {nom:<17s} {k:>2d} {c:10.3f} {c+2*k:10.3f} "
              f"{('%9.4f' % p) if p is not None else '        —'}  {note}")
    v = ("PREMIERE" if rang == 1 else (f"DANS LES TROIS (rang {rang})" if rang <= 3
         else f"DERRIERE (rang {rang}) — la battent : "
              + ", ".join(t[0] for t in tab[:rang-1])))
    print(f"\n  VERDICT 1 (AIC) : notre loi est {v}")

    print("\n  --- CRITERE 2 : evidence de profil (secondaire, prior declare) ---")
    lzl = -0.5 * ref["LCDM"]
    print(f"    {'modele':<17s} {'prior':>14s} {'dlnZ/LCDM':>10s} {'prior x2':>10s}")
    for nom, k, c, p, fam, bor in tab:
        if fam is None:
            continue
        lo, hi = bor
        z1, _ = lnZ(fam, lo, hi)
        mid = 0.5 * (lo + hi)
        z2, _ = lnZ(fam, mid - (hi - lo), mid + (hi - lo))
        print(f"    {nom:<17s} [{lo:+.1f};{hi:+.1f}] {z1-lzl:10.2f} {z2-z1:+10.2f}")
    print("\n  Rappel gele : ceci n'est PAS une evidence par echantillonnage niche, et aucun")
    print("  Delta ln B publie n'est comparable a ces nombres (protocoles et priors differents).")
