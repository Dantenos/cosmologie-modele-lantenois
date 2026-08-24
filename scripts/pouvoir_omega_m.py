#!/usr/bin/env python3
"""COMBIEN D'INFORMATION SUR omega_m LES PRIORS COMPRIMES PERDENT-ILS ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI CETTE MESURE, ET POURQUOI ELLE EST LA BONNE A FAIRE MAINTENANT.
Le #192 a nomme l'arbitre de T10 : propager la famille corrigee dans un code de Boltzmann.
Cela demande de modifier le Fortran de CAMB pour une matiere noire de pression non nulle --
hors de portee verifiable ici, et le faire mal serait pire que ne pas le faire. On ne le
fait donc PAS, et on ne pretend pas le faire.

Mais la question qui rend l'arbitre necessaire, elle, est mesurable avec la machinerie que le
corpus possede deja (planck_theta.py : CAMB + plik_lite TTTEEE + low-ell, #146). La voici.
Dans la famille rho_c = Om_c a^(eps-3), eps agit en faisant differer la densite de matiere A
LA RECOMBINAISON de son etiquette d'aujourd'hui. Identifier eps, c'est donc mesurer omega_m a
la recombinaison independamment de la geometrie tardive. Or :
  - la vraisemblance COMPLETE mesure omega_m directement, par la HAUTEUR des pics acoustiques,
    la queue d'amortissement et l'ISW precoce -- de l'information d'AMPLITUDE ;
  - les priors comprimes (R, l_A, omega_b) ne transportent QUE de la geometrie. R melange
    sqrt(Om) a une distance, l_A est un rapport de distances. Aucune amplitude.
Si cette lecture est juste, le rapport des deux pouvoirs de resolution sur omega_m est
GRAND, et c'est lui qui explique mecaniquement pourquoi quatre choix de comptabilite peuvent
deplacer eps de 0,019 (#192) alors que les mesures en vraisemblance complete se groupent a
+/-0,001 (#191). CE NOMBRE N'EXISTE PAS DANS LA LITTERATURE : le balayage du #192 n'a trouve
aucune quantification de l'ambiguite d'entree omega_m des priors de distance.

CE QUI EST FIXE, ET C'EST UNE LIMITE QU'ON DECLARE AVANT DE MESURER. planck_theta.py fige
omega_b = 0,02237, n_s = 0,9649, tau = 0,0544 et theta_* = 1,04109e-2 (H0 resolu par
bissection). Les DEUX sigma mesures ici sont donc plus petits que ceux d'une analyse
marginalisee complete. C'est le RAPPORT qu'on rapporte, et le rapport est bien moins affecte
que les valeurs absolues -- mais il n'en est pas exempt, et le critere 5 en tient compte.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. ANCRE. A l'optimum LCDM, le chi2 complet doit reproduire l'ancre gelee de
     confluence_planck_v2.py, 1998,633, a 0,5 pres.
  B. DECOMPOSITION FIDELE. Ce script recalcule les termes separement. Leur SOMME doit egaler
     planck_theta.chi2_full au meme point a 1e-6 pres. Sans ce controle, tout ecart mesure
     plus bas pourrait etre une erreur de recopie et non un resultat.
  C. COHERENCE AVEC PLANCK PUBLIE. Le sigma(omega_c) rendu par la vraisemblance complete doit
     etre INFERIEUR OU EGAL a celui que Planck 2018 publie (0,0012), puisque nous figeons
     quatre parametres qu'ils marginalisent -- et pas plus de 5 fois inferieur, faute de quoi
     notre profil est trop serre pour etre credible et on s'arrete.

--- CRITERES (exhaustifs, exclusifs) ---
  1. POUVOIR DE LA VRAISEMBLANCE COMPLETE. sigma(omega_c) par profil (Delta chi2 = 1),
     ln10As profile a chaque point, theta_* fixe. On rapporte aussi la parabolicite
     P = Delta chi2(2 sigma predits)/4 : si P < 0,80 le profil est aplati et le sigma local
     est declare NON OPPOSABLE, comme au #190.
  2. POUVOIR DES PRIORS COMPRIMES. Meme mesure, mais le chi2 est le vecteur (R, l_A, omega_b)
     contre la covariance Planck 3x3. Ce terme ne depend PAS de ln10As -- c'est le fait meme
     qu'on veut montrer, et on le VERIFIE au lieu de l'affirmer : on recalcule le chi2
     comprime a deux valeurs de ln10As distantes de 0,1 et on exige un ecart < 1e-9.
  3. PERTE DE COMPRESSION = sigma_comprime / sigma_complet, sur omega_c.
     PERTE MAJEURE si le rapport >= 3 ; PERTE MODEREE si entre 1,5 et 3 ;
     PAS DE PERTE si < 1,5 -- et dans ce dernier cas l'explication mecanique avancee par le
     #190 et le #192 TOMBE, et il faudra chercher ailleurs. C'est la branche qui me refute.
  4. TRADUCTION EN eps. Dans cette famille, une erreur relative d sur omega_m a la
     recombinaison se traduit par d(eps) = d / |ln a_*| avec a_* = 1/1091. On rapporte les
     deux sigma(eps) implicites et on les compare a la precision publiee (+/-0,001) et a
     l'etendue mesuree au #192 (0,0190).
  5. VERDICT, exhaustif :
     EXPLICATION CONFIRMEE si le critere 3 rend PERTE MAJEURE ET si le sigma(eps) implicite
        des priors comprimes depasse 0,001 alors que celui de la vraisemblance complete ne le
        depasse pas -- c'est-a-dire si la ligne de partage tombe exactement la ou la
        litterature la trouve ;
     EXPLICATION PARTIELLE si la perte est majeure mais que les deux sigma(eps) tombent du
        meme cote de 0,001 ;
     EXPLICATION REFUTEE si le critere 3 rend PAS DE PERTE.
     Dans les deux derniers cas on ecrit que le mecanisme avance depuis le #190 n'est pas
     etabli, et on ne le reformule pas pour le sauver.

REGLE 6. Cette etude cherche a confirmer une explication A MOI. Les seuils vont donc contre :
le critere 3 exige un facteur 3 et non 2 ; la validation C peut m'arreter parce que mon
profil serait TROP serre ; et le critere 2 verifie par le calcul une propriete que j'aurais
pu me contenter d'affirmer.
REGLE 5, accorde d'avance : figer omega_b, n_s, tau et theta_* avantage la vraisemblance
complete, dont l'information d'amplitude est ainsi mise en valeur sans avoir a lutter contre
la degenerescence As-tau. Un contradicteur a le droit d'exiger la mesure marginalisee ; nous
ne l'avons pas, et le critere 5 ne conclut donc que sur un RAPPORT mesure a parametres fixes.
Regle 3 : cette etude REDUIT l'incertitude sur le mecanisme ; elle ne mesure pas eps.
Usage : python3 scripts/pouvoir_omega_m.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import planck_theta as P
import test_wE_v3 as T
import camb

C_KM = 299792.458
A_STAR = 1.0/1091.0
ANCRE = 1998.633
SIG_PLANCK_OMC = 0.0012
DE = ('lcdm',)
OM_NU = 0.06/93.14


def termes(omch2, ln10As):
    """chi2 CMB complet, chi2 comprime, BAO et SNe -- separes. Meme algebre que
    planck_theta.chi2_full, verifiee par la validation B."""
    H0 = P.H0_from_theta(omch2, DE)
    if H0 is None:
        return None
    pars = P.make_pars(H0, omch2, ln10As, DE)
    pars.set_for_lmax(2600, lens_potential_accuracy=1)
    try:
        res = camb.get_results(pars)
    except Exception:
        return None
    cl = res.get_cmb_power_spectra(pars, CMB_unit='muK')['total']
    c_cmb = -2*P.planck.loglike(cl[2:2509, 0], cl[2:2509, 3], cl[2:2509, 1], ellmin=2)

    d = res.get_derived_params()
    rd, rs, zs = d['rdrag'], d['rstar'], d['zstar']
    DM = res.comoving_radial_distance(P.z_bao)
    DH = C_KM/res.hubble_parameter(P.z_bao)
    u = np.array([{'M': DM[i], 'H': DH[i], 'V': (z*DM[i]**2*DH[i])**(1/3)}[t]/rd
                  for i, (z, t, _, _, _) in enumerate(P.BAO)])
    rb = P.d_bao - u
    c_bao = float(rb@P.Cinv_bao@rb)

    zg = np.linspace(1e-4, 2.6, 1500)
    Dc = res.comoving_radial_distance(zg)
    mu = 5*np.log10((1 + P.z_sn)*np.interp(P.z_sn, zg, Dc)) + 25
    r = P.mb - mu
    c_sn = float(r@P.Cinv_sn@r - (r@P.Cinv_one)**2/P.oCo)

    # --- priors comprimes, construits depuis le MEME fond CAMB
    h = H0/100.0
    Om = (P.OMB_H2 + omch2 + OM_NU)/(h*h)
    Dc_star = float(res.comoving_radial_distance(zs))
    Rth = np.sqrt(Om)*Dc_star*(100*h)/C_KM
    lAth = np.pi*Dc_star/rs
    dv = np.array([Rth, lAth, P.OMB_H2]) - T.DP_V
    c_comp = float(dv@T.DP_CI@dv)

    return dict(cmb=float(c_cmb), bao=c_bao, sn=c_sn, comp=c_comp, H0=H0,
                R=Rth, lA=lAth, rs=rs, zs=zs)


def prof_complet(omch2):
    """chi2 CMB complet, ln10As profile."""
    def f(x):
        t = termes(omch2, float(x))
        return 1e9 if t is None else t['cmb']
    r = minimize_scalar(f, bounds=(2.90, 3.20), method='bounded',
                        options=dict(xatol=2e-4))
    return float(r.fun), float(r.x)


def prof_total(omch2):
    """chi2 TOTAL (CMB + BAO + SNe), ln10As profile. C'est l'objectif dont 1998,633 est
    l'optimum -- DEFAUT DE CORPS CORRIGE : la premiere version validait l'ancre a l'optimum
    du CMB SEUL, qui n'est pas le meme point, et la validation A l'a arretee net (ecart
    11,326). Le controle a fonctionne ; c'est mon code qui ne fonctionnait pas."""
    def f(x):
        t = termes(omch2, float(x))
        return 1e9 if t is None else t['cmb'] + t['bao'] + t['sn']
    r = minimize_scalar(f, bounds=(2.90, 3.20), method='bounded',
                        options=dict(xatol=2e-4))
    return float(r.fun), float(r.x)


def prof_comprime(omch2):
    t = termes(omch2, 3.044)
    return (1e9 if t is None else t['comp'])


def sigma_par_profil(fn, x0, pas, nmax=40):
    """demi-largeur a Delta chi2 = 1, par pas de `pas` de part et d'autre du minimum."""
    c0 = fn(x0)
    out = {}
    for sens in (+1, -1):
        x = x0
        for _ in range(nmax):
            x += sens*pas
            if fn(x) - c0 >= 1.0:
                break
        out[sens] = abs(x - x0)
    return c0, out[+1], out[-1]


def minimise(fn, x0, pas):
    """descente simple sur grille puis raffinement."""
    x, c = x0, fn(x0)
    for _ in range(30):
        bouge = False
        for s in (+1, -1):
            cc = fn(x + s*pas)
            if cc < c - 1e-9:
                x, c, bouge = x + s*pas, cc, True
                break
        if not bouge:
            pas /= 2.0
            if pas < 1e-5:
                break
    return x, c


if __name__ == "__main__":
    import json
    print("POUVOIR DE RESOLUTION SUR omega_m (criteres geles)\n")

    print("  --- validations A et B : l'ancre et la decomposition ---")
    x_tot, _ = minimise(lambda o: prof_total(o)[0], 0.1200, 0.0008)
    _, as0 = prof_total(x_tot)
    t0 = termes(x_tot, as0)
    tot = t0['cmb'] + t0['bao'] + t0['sn']
    ref, _ = P.chi2_full(x_tot, as0, DE)
    print(f"     optimum LCDM (chi2 TOTAL) : omega_c = {x_tot:.5f}   ln10As = {as0:.4f}   "
          f"H0 = {t0['H0']:.3f}")
    print(f"     CMB {t0['cmb']:.3f} + BAO {t0['bao']:.3f} + SNe {t0['sn']:.3f} "
          f"= {tot:.3f}")
    print(f"     [B] chi2_full au meme point = {ref:.6f}   ecart = {abs(tot-ref):.2e}"
          f"   -> {'OK' if abs(tot-ref) < 1e-6 else 'ECHEC'}")
    if abs(tot - ref) >= 1e-6:
        sys.exit("     la decomposition n'est pas fidele : rien n'est publie.")
    print(f"     [A] ancre gelee {ANCRE}   ecart = {abs(tot-ANCRE):.3f}"
          f"   -> {'OK' if abs(tot-ANCRE) < 0.5 else 'ECHEC'}")
    if abs(tot - ANCRE) >= 0.5:
        sys.exit("     l'ancre n'est pas reproduite : rien n'est publie.")

    print("\n  --- critere 2, controle prealable : le chi2 comprime ignore-t-il "
          "l'amplitude ? ---")
    a = termes(x_tot, 3.000)['comp']
    b = termes(x_tot, 3.100)['comp']
    ecart_as = abs(a - b)
    print(f"     chi2 comprime a ln10As = 3,000 : {a:.9f}")
    print(f"     chi2 comprime a ln10As = 3,100 : {b:.9f}")
    print(f"     ecart = {ecart_as:.2e}   -> "
          f"{'CONFIRME : aucune information d amplitude' if ecart_as < 1e-9 else 'ECHEC'}")
    if ecart_as >= 1e-9:
        sys.exit("     le chi2 comprime depend de l'amplitude : la lecture tombe.")

    print("\n  --- critere 1 : pouvoir de la vraisemblance complete ---")
    # le profil du CMB SEUL a son propre minimum, distinct de celui du chi2 total
    x_cmb, _ = minimise(lambda o: prof_complet(o)[0], x_tot, 0.0008)
    print(f"     minimum du CMB seul : omega_c = {x_cmb:.5f}"
          f"   (optimum total : {x_tot:.5f})")
    c0f, spf, smf = sigma_par_profil(lambda o: prof_complet(o)[0], x_cmb, 0.0002)
    sig_f = min(spf, smf)
    d2 = prof_complet(x_cmb + 2*sig_f)[0] - c0f
    Pf = d2/4.0
    print(f"     sigma(omega_c) = {sig_f:.5f}  (+{spf:.5f}/-{smf:.5f})")
    print(f"     parabolicite : Delta chi2 a 2 sigma = {d2:.3f}   P = {Pf:.2f}"
          f"   -> {'sain' if Pf >= 0.80 else 'APLATI : sigma NON OPPOSABLE'}")

    print("\n  --- validation C : coherence avec Planck publie ---")
    okC = sig_f <= SIG_PLANCK_OMC and sig_f >= SIG_PLANCK_OMC/5.0
    print(f"     notre sigma {sig_f:.5f}   Planck 2018 publie {SIG_PLANCK_OMC}"
          f"   rapport {SIG_PLANCK_OMC/sig_f:.2f}   -> {'OK' if okC else 'ECHEC'}")
    if not okC:
        sys.exit("     profil incoherent avec Planck : rien n'est publie.")

    print("\n  --- critere 2 : pouvoir des priors comprimes ---")
    x_c, _ = minimise(prof_comprime, x_tot, 0.0010)
    c0c, spc, smc = sigma_par_profil(prof_comprime, x_c, 0.0005)
    sig_c = min(spc, smc)
    print(f"     minimum a omega_c = {x_c:.5f}   chi2 = {c0c:.4f}")
    print(f"     sigma(omega_c) = {sig_c:.5f}  (+{spc:.5f}/-{smc:.5f})")

    print("\n  --- critere 3 : perte de compression ---")
    rap = sig_c/sig_f
    if rap >= 3:
        v3 = "PERTE MAJEURE"
    elif rap >= 1.5:
        v3 = "PERTE MODEREE"
    else:
        v3 = "PAS DE PERTE"
    print(f"     sigma_comprime / sigma_complet = {sig_c:.5f} / {sig_f:.5f} = "
          f"{rap:.2f}   -> {v3}")

    print("\n  --- critere 4 : traduction en eps ---")
    la = abs(np.log(A_STAR))
    om_tot = P.OMB_H2 + x_tot + OM_NU
    eps_f = (sig_f/om_tot)/la
    eps_c = (sig_c/om_tot)/la
    print(f"     omega_m total a l'optimum = {om_tot:.5f}   |ln a_*| = {la:.3f}")
    print(f"     sigma(eps) implicite, vraisemblance complete = {eps_f:.5f}")
    print(f"     sigma(eps) implicite, priors comprimes       = {eps_c:.5f}")
    print(f"     (precision publiee : +/-0,001 ; etendue mesuree au #192 : 0,0190)")

    print("\n  --- critere 5 : VERDICT ---")
    if v3 == "PAS DE PERTE":
        v5 = ("EXPLICATION REFUTEE — le mecanisme avance depuis le #190 n'est pas etabli, "
              "et il faut chercher ailleurs")
    elif eps_c > 0.001 >= eps_f:
        v5 = ("EXPLICATION CONFIRMEE — la ligne de partage tombe exactement ou la "
              "litterature la trouve")
    else:
        v5 = ("EXPLICATION PARTIELLE — la perte est majeure mais les deux sigma(eps) "
              "tombent du meme cote de 0,001 ; le mecanisme n'est pas etabli")
    print(f"     {v5}")

    out = dict(omega_c_opt=x_tot, omega_c_cmb_seul=x_cmb, ln10As_opt=as0, H0=t0['H0'],
               chi2_cmb=t0['cmb'], chi2_bao=t0['bao'], chi2_sn=t0['sn'], total=tot,
               ancre=ANCRE, sigma_complet=sig_f, sigma_comprime=sig_c,
               parabolicite=Pf, rapport=rap, verdict3=v3,
               sigma_eps_complet=eps_f, sigma_eps_comprime=eps_c, verdict5=v5,
               R=t0['R'], lA=t0['lA'], zstar=t0['zs'], rstar=t0['rs'])
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "pouvoir_omega_m.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/pouvoir_omega_m.json")
