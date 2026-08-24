#!/usr/bin/env python3
"""CONTROLE POST-HOC DE L'ARBITRE — LA SIGNIFICATIVITE ANNONCEE EST-ELLE REELLE ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI CE CONTROLE EXISTE, ET IL FAUT LE DIRE : IL N'ETAIT PAS PREVU.
Le critere 3 de dilution_arbitre.py (gele 83b148f19fe1) a rendu eps = -0,0100 +/-0,0020,
que son propre code annonce a 5,0 sigma -- alors que son gain sur LCDM vaut +9,81, soit
sqrt(9,81) = 3,13 sigma par rapport de vraisemblance. LES DEUX NE CONCORDENT PAS. Pour un
profil parabolique de demi-largeur 0,0020, un minimum a 0,0100 de zero devrait coder
(0,0100/0,0020)^2 = 25 unites de chi2, pas 9,81. Le profil est donc NON PARABOLIQUE, et le
sigma local sous-estime l'incertitude vers zero. Ce controle mesure de combien.

REGLE 6, ET C'EST LE POINT. Ce controle ne peut qu'AFFAIBLIR le resultat qu'il examine :
il remplace une significativite locale par une significativite integrale toujours <= a elle
des que le profil s'aplatit. On l'ecrit avant de le lancer pour qu'on ne puisse pas dire
qu'il a ete ajoute apres coup dans le sens favorable -- il l'a ete apres coup, mais dans le
sens DEFAVORABLE, et c'est verifiable en lisant ce qu'il calcule.

--- CRITERES (exhaustifs, exclusifs) ---
  1. SIGNIFICATIVITE HONNETE. On rapporte les DEUX nombres pour les configurations 1, 2 et 3 :
     sigma_local = |eps|/demi-largeur a Delta chi2 = 1 ;
     sigma_rapport = sqrt(chi2(eps=0) - chi2(min)), la statistique de Wilks a 1 ddl.
     LE NOMBRE OPPOSABLE EST LE PLUS PETIT DES DEUX, systematiquement, dans les trois cas.
  2. DIAGNOSTIC DE PARABOLICITE. On rapporte le rapport
     P = [chi2(0) - chi2(min)] / (|eps|/sigma_local)^2, qui vaut 1 pour une parabole.
     PROFIL SAIN si P >= 0,80 ; PROFIL APLATI si P < 0,80 -- et dans ce cas le sigma local
     est declare NON OPPOSABLE pour cette configuration, definitivement.
  3. D'OU VIENT LA CONTRAINTE ? Decomposition du chi2 en (SNe, BAO, CMB, H0) au minimum de
     l'arbitre et a eps = 0. Si un SEUL terme fournit plus de 80 % du gain, il est nomme, et
     le resultat est declare PORTE PAR UN SEUL JEU -- ce qui est une fragilite, pas une force.
  4. INTERVALLE PAR WILKS. Intervalle a Delta chi2 = 4 (2 sigma, 1 ddl) sur la configuration
     3, lu sur la grille fine. C'est lui qui remplace le critere 6 de l'etude arbitre si le
     critere 2 ci-dessus declare le profil aplati.
  5. ZERO EST-IL EXCLU ? On rapporte Delta chi2 (eps = 0) sous la configuration 3 et sa
     traduction en sigma de Wilks. EXCLU A >= 3 SIGMA / ENTRE 2 ET 3 SIGMA / NON EXCLU.
     Aucun autre libelle n'est disponible.

CE QUE CE CONTROLE NE FAIT PAS. Il ne re-mesure pas eps et ne change aucune configuration :
il relit les memes profils avec une statistique moins flatteuse. Si les deux statistiques
s'accordent, il ne reste rien de lui ; s'il elles divergent, c'est la plus basse qui vaut.
Regle 3 : ce controle REDUIT la significativite opposable ; il n'etablit rien de neuf.
Usage : python3 scripts/dilution_arbitre_forme.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_arbitre as D
import test_wE_v3 as T
import vraisemblance_reelle as V


def decompose(h, ob, Om, eps, cfg):
    """meme algebre que chi2_cfg, mais rendue terme a terme."""
    om = Om*h*h
    om_tab = om*D.A_STAR**eps if cfg['zs'] == 'coh' else om
    zz, Ea = D.fond_arb(Om, eps)
    Ez = np.interp(T.zg, zz, Ea)
    inv = 1.0/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:] + inv[:-1])*np.diff(T.zg))])
    DH0 = D.C_KM/(100*h)
    zs = T.z_star(ob, om_tab)
    if cfg['rs'] == 'table':
        rd, rs = T.r_drag(ob, om_tab), T.r_star(ob, om_tab)
    else:
        rd = D.rs_direct(1.0/(1.0 + D.z_drag(ob, om_tab)), Om, ob, h, eps, cfg['ray'])
        rs = D.rs_direct(1.0/(1.0 + zs), Om, ob, h, eps, cfg['ray'])
    mu = 5*np.log10((1 + V.z_sn)*np.interp(V.z_sn, T.zg, Dc))
    r = V.mb - mu
    c_sn = float(r@V.Cinv_sn@r - (r@V.Cinv_one)**2/V.oCo)
    u = np.zeros(13)
    for i, (z, typ, _, _, _) in enumerate(V.BAO):
        DM_ = np.interp(z, T.zg, Dc)*DH0
        DH_ = DH0/np.interp(z, T.zg, Ez)
        u[i] = {'M': DM_, 'H': DH_, 'V': (z*DM_**2*DH_)**(1/3)}[typ]/rd
    rb = V.d_bao - u
    c_bao = float(rb@V.Cinv_bao@rb)
    Dc_star = np.interp(zs, T.zg, Dc)
    lAth = np.pi*Dc_star*DH0/rs
    if cfg['R'] == 'aucun':
        dv = np.array([lAth, ob]) - D.DP_V2
        c_cmb = float(dv@D.DP_CI2@dv)
    else:
        Om_R = Om if cfg['R'] == 'etiq' else Om*D.A_STAR**eps
        dv = np.array([np.sqrt(Om_R)*Dc_star, lAth, ob]) - T.DP_V
        c_cmb = float(dv@T.DP_CI@dv)
    c_h0 = float(((100*h - T.H0_SH)/T.H0_SH_S)**2)
    return dict(SNe=c_sn, BAO=c_bao, CMB=c_cmb, H0=c_h0)


if __name__ == "__main__":
    print("CONTROLE DE FORME DU PROFIL (criteres geles)\n")
    CLES = ['1_table_etiq', '2_table_coh', '3_arbitre']
    M = {}
    for k in CLES:
        M[k] = D.mesure(D.CFG[k])

    print("  --- critere 1 : les deux significativites ---")
    print(f"  {'configuration':<16s} {'eps':>10s} {'sig local':>10s} {'sig Wilks':>10s} "
          f"{'opposable':>10s}")
    OPP = {}
    for k in CLES:
        m = M[k]
        sw = float(np.sqrt(max(m['gain'], 0.0)))
        OPP[k] = min(m['sig'], sw)
        print(f"  {k:<16s} {m['eps']:+10.5f} {m['sig']:10.2f} {sw:10.2f} "
              f"{OPP[k]:10.2f}")

    print("\n  --- critere 2 : parabolicite ---")
    APLATI = {}
    for k in CLES:
        m = M[k]
        att = (m['sig'])**2
        P = m['gain']/att if att > 0 else np.nan
        APLATI[k] = P < 0.80
        print(f"  {k:<16s} attendu {att:7.2f}   observe {m['gain']:7.2f}   "
              f"P = {P:5.2f}  -> {'APLATI (sigma local NON OPPOSABLE)' if APLATI[k] else 'sain'}")

    print("\n  --- critere 3 : d'ou vient la contrainte ? ---")
    m3 = M['3_arbitre']
    cfg3 = D.CFG['3_arbitre']
    p_min = D.profil(m3['eps'], cfg3).x
    p_zer = D.profil(0.0, cfg3).x
    d_min = decompose(p_min[0], p_min[1], p_min[2], m3['eps'], cfg3)
    d_zer = decompose(p_zer[0], p_zer[1], p_zer[2], 0.0, cfg3)
    print(f"  {'terme':<6s} {'a eps=0':>12s} {'au minimum':>12s} {'gain':>10s} {'part':>8s}")
    tot = sum(d_zer[q] - d_min[q] for q in d_zer)
    part = {}
    for q in ('SNe', 'BAO', 'CMB', 'H0'):
        g = d_zer[q] - d_min[q]
        part[q] = g/tot if tot != 0 else 0.0
        print(f"  {q:<6s} {d_zer[q]:12.3f} {d_min[q]:12.3f} {g:+10.3f} {100*part[q]:7.1f} %")
    dom = max(part, key=part.get)
    seul = part[dom] > 0.80
    print(f"  total {sum(d_zer.values()):12.3f} {sum(d_min.values()):12.3f} {tot:+10.3f}")
    print(f"  -> {'PORTE PAR UN SEUL JEU : ' + dom + ' (fragilite, pas force)' if seul else 'contrainte repartie'}")

    print("\n  --- criteres 4 et 5 : intervalle de Wilks et exclusion de zero ---")
    sel = m3['ok'] & (m3['cs'] <= m3['chi2'] + 4.0)
    lo, hi = float(m3['xs'][sel].min()), float(m3['xs'][sel].max())
    dchi0 = m3['gain']
    sw = float(np.sqrt(max(dchi0, 0.0)))
    if sw >= 3:
        lab = "ZERO EXCLU A >= 3 SIGMA"
    elif sw >= 2:
        lab = "ZERO ENTRE 2 ET 3 SIGMA"
    else:
        lab = "ZERO NON EXCLU"
    print(f"  intervalle Wilks 2 sigma : eps dans [{lo:+.4f} ; {hi:+.4f}]")
    print(f"  Delta chi2(eps = 0) = {dchi0:.2f}  ->  {sw:.2f} sigma de Wilks  ->  {lab}")
    if APLATI['3_arbitre']:
        print("  (le critere 2 a declare ce profil APLATI : cet intervalle-ci REMPLACE")
        print("   le critere 6 de l'etude arbitre, et le sigma local y est sans valeur.)")
