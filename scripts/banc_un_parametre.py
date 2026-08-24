#!/usr/bin/env python3
"""BANC D'ESSAI DES LOIS D'ENERGIE NOIRE A UN PARAMETRE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI. Il existe en 2025-2026 une conversation active sur les w(z) a UN parametre, dont
la conclusion commune est que les donnees preferent la BASSE COMPLEXITE. Notre loi
w = -beta/(3Ht) en est un membre et n'a jamais figure dans ce comparatif (#172).

LES CONCURRENTES, implementees telles que publiees (equations citees) :
  Kessler, Escamilla, Pan & Di Valentino, arXiv:2504.00776, Eqs. 5-8, prior w0 ~ U[-2, 0] :
    K1  w(a) = w0 [1 + sin(1-a)]
    K2  w(a) = w0 [1 + (1-a)/(a^2 + (1-a)^2)]
    K3  w(a) = w0 [1 - a sin(1/a) + sin(1)]
    K4  w(a) = w0 [1 + (1-a) sin(1/(1-a))]
  Borghetto et al., arXiv:2606.17951, prior w0 ~ U[-3, 1] :
    SR  w(a) = w0 / sqrt(a)          (Eq. 4.1 ; forme fermee Eq. 5.8)
    F83 w(a) = w0 exp(1-a)           (Eq. 4.3)
  Reperes : LCDM (0 param.), wCDM (1), CPL (2), et NOTRE accretion (1, beta ~ U[0,5 ; 5]).

TOUTES sont integrees par la MEME quadrature : g(a) = rho_de(a)/rho_de(1) =
a^-3 exp(3 * integrale_a^1 w dln a'), sur une grille dense (60 000 points, log) puis
interpolee sur celle de l'atlas. Aucune forme fermee n'est utilisee dans le fit : les formes
fermees publiees servent UNIQUEMENT a valider la quadrature (critere A).

CE QUE CE BANC N'EST PAS. Ce n'est PAS une comparaison a leurs chiffres publies, et aucun
Delta ln B publie n'est cite comme comparant. Raisons declarees (#172) : Kessler estime
l'evidence par MCEvidence sur chaines Cobaya, Borghetto par PolyChord et dans le cadre VCDM
(gravite minimalement modifiee) et non en RG ; leurs volumes de prior different (U[-2,0]
contre U[-3,1]) ; et avec UN parametre le facteur d'Occam EST le resultat, donc un prior non
declare est un resultat non declare. Ce banc est INTERNE : memes donnees (notre
vraisemblance legere, N = 1597), meme pipeline, meme estimateur, priors ecrits ci-dessus.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. QUADRATURE. Le g(a) numerique doit reproduire les DEUX formes fermees publiees a
     mieux que 1e-8 en ecart relatif maximal :
       K2  : g = a^(-3-6w0) (2a^2 - 2a + 1)^(3w0/2)     a w0 = -0,7 ;
       SR  : g = a^-3 exp[6 w0 (a^(-1/2) - 1)]          a w0 = -0,9   (Eq. 5.8).
  B. wCDM. La meme quadrature a w constant doit redonner le 'wcdm' de l'atlas :
     |dchi2| < 0,05 au meme point.
  C. ANCRES. LCDM 1425,086 ; accretion 1419,309 ; CPL 1418,927 (atlas #150), a +/- 0,3.

--- CRITERES (exhaustifs, exclusifs) ---
  1. CLASSEMENT PRINCIPAL : l'AIC (chi2 + 2k), k comptant les parametres LIBRES du fit
     (h, omega_b, Om, plus ceux du modele). L'AIC est retenu comme mesure principale parce
     qu'il ne depend d'aucun prior — contrairement a l'evidence, dont on sait qu'elle EST le
     prior quand il n'y a qu'un parametre.
     Verdict sur NOTRE loi :
       PREMIERE            si son AIC est le plus bas de la table ;
       DANS LES TROIS      si son rang est 2 ou 3 ;
       DERRIERE            sinon — ECRIT EN PREMIER, avec le nom de celles qui la battent.
  2. EVIDENCE DE PROFIL (secondaire, et declaree comme telle) :
     ln Z = ln [ (1/largeur du prior) * integrale exp(-chi2_profil(theta)/2) dtheta ], le
     profil etant pris sur (h, omega_b, Om) a chaque valeur de theta, sur 21 points.
     CE N'EST PAS une evidence par echantillonnage niche : c'est une approximation de
     profil, elle sous-estime le volume des parametres de nuisance, et elle est rapportee
     UNIQUEMENT pour ordonner les facteurs d'Occam entre modeles a priors comparables.
     On rapporte aussi, pour chaque modele, dln Z si l'on DOUBLE la largeur du prior — la
     sensibilite au prior fait partie du resultat.
  3. TOUT EST RAPPORTE, favorable ou non : chi2, parametre ajuste, AIC, rang, ln Z.
Regle 3 : ce banc REDUIT l'espace des lois plausibles ; il n'en ferme aucune.
Usage : python3 scripts/banc_un_parametre.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scipy.integrate import cumulative_simpson
import atlas_v1 as A

AG = A.AG
DENSE = np.logspace(-7, 0, 240001)   # densite choisie pour que le trapeze passe sous 1e-8
LND = np.log(DENSE)
DLN = np.diff(LND)
B = [0.69, 0.02236, 0.31]
ANCRES = {"LCDM": 1425.086, "ACCRETION": 1419.309, "CPL": 1418.927}


def g_de(wfun, p):
    """g(a) = rho_de(a)/rho_de(1) = a^-3 exp(3 * int_a^1 w dln a')."""
    w = wfun(DENSE, p)
    if not np.all(np.isfinite(w)):
        return None
    # Simpson cumulatif : l integrande de SR diverge en a^(-1/2) et le trapeze y plafonne
    # a 1,6e-6 (erreur en (dlna)^2) ; Simpson descend a 4,4e-10 sur la meme grille.
    J = np.concatenate([[0.0], cumulative_simpson(w, x=LND)])
    lg = -3 * LND + 3 * (J[-1] - J)
    if np.max(lg) > 400:
        return None
    return np.exp(np.clip(lg, -700, 400)), lg


def fond_w(Om, p, wfun):
    r = g_de(wfun, p)
    if r is None:
        return None
    g = r[0]
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    E2 = Om / AG**3 + Or / AG**4 + Ode * np.interp(AG, DENSE, g)
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


MODELES = [("K1  Kessler 1", W_K1, (-2.0, 0.0)), ("K2  Kessler 2", W_K2, (-2.0, 0.0)),
           ("K3  Kessler 3", W_K3, (-2.0, 0.0)), ("K4  Kessler 4", W_K4, (-2.0, 0.0)),
           ("SR  w0/sqrt(a)", W_SR, (-3.0, 1.0)), ("F83 w0 exp(1-a)", W_F83, (-3.0, 1.0))]
for nom, wf, _ in MODELES:
    A.CUSTOM[nom] = (lambda wf: (lambda Om, p: fond_w(Om, p, wf)))(wf)
A.CUSTOM['wq_cst'] = lambda Om, p: fond_w(Om, p, W_CST)

STARTS = [B, [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]


def profil(fam, npar, val):
    return A.fit(fam, npar, STARTS, fixpar=val).fun


def lnZ(fam, lo, hi, n=21):
    xs = np.linspace(lo, hi, n)
    cs = np.array([profil(fam, 1, float(x)) for x in xs])
    c0 = cs.min()
    L = np.exp(-0.5 * (cs - c0))
    I = np.trapezoid(L, xs) if hasattr(np, "trapezoid") else np.trapz(L, xs)
    return -0.5 * c0 + np.log(I / (hi - lo)), xs[int(np.argmin(cs))], c0


if __name__ == "__main__":
    print("BANC D'ESSAI DES LOIS A UN PARAMETRE (criteres geles)\n")

    print("  --- validation A : la quadrature contre les formes fermees publiees ---")
    # comparaison en LOG : g descend a exp(-17000) aux petits a, le rapport lineaire
    # deborde (0/0). |dg/g| = |exp(dln g) - 1| ~ |dln g| : meme quantite, calculee stablement.
    lg2 = g_de(W_K2, -0.7)[1]
    lf2 = (-3 - 6 * (-0.7)) * LND + (3 * (-0.7) / 2) * np.log(2 * DENSE**2 - 2 * DENSE + 1)
    e2 = float(np.max(np.abs(np.expm1(lg2 - lf2))))
    lgs = g_de(W_SR, -0.9)[1]
    lfs = -3 * LND + 6 * (-0.9) * (DENSE**-0.5 - 1)
    es = float(np.max(np.abs(np.expm1(lgs - lfs))))
    print(f"    K2 (forme fermee)  : max |dg/g| = {e2:.3e}")
    print(f"    SR (Eq. 5.8)       : max |dg/g| = {es:.3e}")
    if not (e2 < 1e-8 and es < 1e-8):
        sys.exit("    VALIDATION A ECHOUE — rien n'est publie.")

    cw1 = A.fit('wq_cst', 1, STARTS, fixpar=-0.95).fun
    cw2 = A.fit('wcdm', 1, STARTS, fixpar=-0.95).fun
    print(f"    wCDM par quadrature = {cw1:.4f} vs atlas {cw2:.4f} (d = {cw1-cw2:+.4f})")
    if abs(cw1 - cw2) >= 0.05:
        sys.exit("    VALIDATION B ECHOUE — rien n'est publie.")

    import test_wE_v3 as T
    ref = {"LCDM": T.fit('lcdm').fun,
           "ACCRETION": A.fit('invt', 1, [B + [2.4], B + [2.0], B + [2.8]],
                              bornes=[(0.5, 5.0)]).fun,
           "CPL": A.fit('cpl', 2, [B + [-0.9, -0.3], B + [-0.84, -0.6]],
                        bornes=[(-2.0, 0.0), (-3.0, 2.0)]).fun}
    okC = all(abs(ref[k] - ANCRES[k]) < 0.3 for k in ANCRES)
    print(f"    ancres : LCDM {ref['LCDM']:.3f} | accretion {ref['ACCRETION']:.3f} | "
          f"CPL {ref['CPL']:.3f} -> {'OK' if okC else 'ECHEC'}")
    if not okC:
        sys.exit("    VALIDATION C ECHOUE — rien n'est publie.")

    print("\n  --- ajustements ---")
    table = [("LCDM", 3, ref["LCDM"], None, None),
             ("ACCRETION beta", 4, ref["ACCRETION"], None, (0.5, 5.0)),
             ("CPL", 5, ref["CPL"], None, None)]
    r = A.fit('invt', 1, [B + [2.4]], bornes=[(0.5, 5.0)])
    table[1] = ("ACCRETION beta", 4, r.fun, r.x[3], (0.5, 5.0))
    for nom, wf, (lo, hi) in MODELES:
        rr = A.fit(nom, 1, [B + [-0.8], B + [-1.0], B + [-0.6]], bornes=[(lo, hi)])
        table.append((nom, 4, rr.fun, rr.x[3], (lo, hi)))
    rw = A.fit('wcdm', 1, [B + [-0.9], B + [-1.1]], bornes=[(-2.0, -0.2)])
    table.append(("wCDM", 4, rw.fun, rw.x[3], (-2.0, 0.0)))

    table.sort(key=lambda t: t[2] + 2 * t[1])
    print(f"    {'rang':>4s} {'modele':<17s} {'k':>2s} {'chi2':>10s} {'AIC':>10s} "
          f"{'param':>9s}")
    rang_acc = None
    for i, (nom, k, c, p, _) in enumerate(table, 1):
        if nom.startswith("ACCRETION"):
            rang_acc = i
        print(f"    {i:>4d} {nom:<17s} {k:>2d} {c:10.3f} {c + 2*k:10.3f} "
              f"{('%9.4f' % p) if p is not None else '        —'}")

    if rang_acc == 1:
        v = "PREMIERE"
    elif rang_acc <= 3:
        v = f"DANS LES TROIS (rang {rang_acc})"
    else:
        devant = ", ".join(t[0] for t in table[:rang_acc - 1])
        v = f"DERRIERE (rang {rang_acc}) — la battent : {devant}"
    print(f"\n  VERDICT 1 (AIC) : notre loi est {v}")

    print("\n  --- VERDICT 2 : evidence de profil (secondaire, prior declare) ---")
    print(f"    {'modele':<17s} {'prior':>14s} {'dlnZ/LCDM':>10s} {'dlnZ prior x2':>14s}")
    lz_l = -0.5 * ref["LCDM"]
    for nom, k, c, p, bornes in table:
        if bornes is None or nom == "LCDM":
            continue
        fam = 'invt' if nom.startswith("ACCRETION") else ('wcdm' if nom == "wCDM" else nom)
        lo, hi = bornes
        z1, _, _ = lnZ(fam, lo, hi)
        mid = 0.5 * (lo + hi)
        z2, _, _ = lnZ(fam, mid - (hi - lo), mid + (hi - lo))
        print(f"    {nom:<17s} [{lo:+.1f} ; {hi:+.1f}] {z1 - lz_l:10.2f} {z2 - z1:+14.2f}")
    print("\n  Rappel gele : ceci n'est PAS une evidence par echantillonnage niche, et aucun")
    print("  Delta ln B publie n'est comparable a ces nombres (protocoles et priors differents).")
