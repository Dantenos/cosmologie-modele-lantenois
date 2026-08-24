#!/usr/bin/env python3
"""REFERENT OU PRECISION, v3 — UN SIGMA SANS RESOLUTION DE GRILLE, ET QUI SE VALIDE LUI-MEME.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI UNE v3, ET POURQUOI CE N'EST PAS UN TROISIEME RAFFINEMENT.
La v1 s'est arretee sur sa validation B (le pas de grille 0,001 plafonnait sigma). La v2 a
raffine a 0,0001, a passe la validation B deux fois -- sigma x1,86 puis x3,71, gains x4,00
puis x16,00 -- et s'est arretee sur sa validation D : le sigma le plus petit valait 2 pas
fins au lieu des 5 exiges. Le plancher n'avait pas ete leve, il avait ete DEPLACE.
Le #199 a nomme la cause avant d'ecrire cette v3, et elle est structurelle : un estimateur
de sigma PAR MARCHE DE GRILLE ne peut pas suivre une incertitude qui retrecit sans borne --
chaque raffinement repousse le blocage d'un facteur k, indefiniment. Une v3 plus fine ne
resoudrait rien. **Ce qui change ici n'est donc pas le maillage mais l'ESTIMATEUR.**

CE QUE FAIT LA v3. On ajuste une PARABOLE au voisinage du minimum :
    chi2(eps) ~= chi2_min + A (eps - eps_0)^2   ->   sigma = 1/sqrt(A).
Cet estimateur n'a aucune resolution de grille : sigma peut valoir 1e-6 sans que rien ne
plafonne. Les seuils, les configurations, les donnees et les criteres 1 a 4 sont INCHANGES
par rapport a la v2 ; seule la fabrique du sigma change, et pour la raison ecrite ci-dessus.

MAIS UNE PARABOLE EST UN MENSONGE SUR UN PROFIL APLATI, ET NOUS LE SAVONS DEJA.
Le #190 a mesure sur ce meme corpus un profil dont la parabolicite valait 0,39 : y ajuster
une parabole donnerait un sigma trois fois trop petit et une significativite fabriquee.
L'estimateur doit donc SE VALIDER LUI-MEME, et c'est la validation D ci-dessous : on evalue
le chi2 REEL au point que la parabole predit a Delta chi2 = 1, et on exige que la prediction
tienne. Une configuration qui echoue voit son sigma declare NON OPPOSABLE et EXCLU du sigma
median -- mais son eps reste compte dans l'etendue, parce que l'etendue est ce qu'on mesure
et qu'en retirer une valeur genante serait le choix confortable.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. A k = 1, les quatre configurations redonnent les valeurs du #192 :
     +0,00700 / -0,00400 / -0,01200 / -0,00400.
  B. OPERATIVITE, exigee DEUX FOIS comme en v2 :
     b1. sigma median x k a +/-40 % ;  b2. gain median x k^2 a +/-25 %.
  C. Les deux signes de eps restent accessibles a >= 90 % de chaque cote, a chaque k.
  D. PARABOLICITE VERIFIEE PAR EVALUATION, pas supposee. Pour chaque configuration et chaque
     k, on evalue le chi2 aux deux points eps_0 +/- sigma_parabole et on exige
     Delta chi2 dans [0,85 ; 1,15]. Une configuration qui echoue est declaree NON OPPOSABLE,
     exclue du sigma median, et NOMMEE dans la sortie. Si PLUS D'UNE des quatre echoue a un
     k quelconque, l'etude s'arrete : un estimateur faux sur la moitie des configurations ne
     vaut pas mieux que le plancher qu'il remplace.

--- CRITERES (exhaustifs, exclusifs) — IDENTIQUES A LA v2 ---
  1. E(k) = max(eps) - min(eps) sur les quatre configurations ; S(k) = sigma median sur les
     configurations OPPOSABLES. Pour k = 1, 2, 4.
  2. LE TEST : r = E(4)/E(1).
     REFERENT CONFIRME si r >= 0,75 ; PRECISION (donc #193 REFUTE) si r <= 0,35 ;
     INDETERMINE entre les deux, et la lecture du #193 reste NON ETABLIE.
  3. SIGNATURE CROISEE : E(k)/S(k) croissante -> referent ; constante -> precision.
  4. CONSEQUENCE : a quel niveau de sigma etiquette et coherent se contredisent, par k.

REGLE 6. Troisieme tentative sur une lecture qui m'appartient : les seuils ne bougent pas
d'un chiffre par rapport a la v2, la branche qui me refute est testee avant celle qui me
confirme, et la validation D peut arreter l'etude en declarant mon nouvel estimateur faux.
Changer d'estimateur apres deux blocages n'est licite QUE parce que la cause a ete nommee au
#199 AVANT que cette v3 soit ecrite, et parce que le nouvel estimateur est soumis a un
controle que l'ancien n'avait pas.
REGLE 5 : diviser uniformement toutes les incertitudes reste une idealisation ; ce test dit
ce que fait la statistique seule, pas ce que fera un relevé futur.
Regle 3 : il REDUIT le nombre de lectures possibles ; il ne mesure pas eps.
Usage : python3 scripts/test_referent_v3.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_baryons as B
import test_wE_v3 as T
import vraisemblance_reelle as VR

KS = (1.0, 2.0, 4.0)
LO, HI, PAS = -0.030, 0.030, 0.002        # balayage grossier : accessibilite + minimum
N_PAR = 9                                  # points de l'ajustement parabolique
TOL_PARAB = 0.15                           # validation D
ATTENDU_192 = {'table_etiq': +0.00700, 'table_coh': -0.00400,
               'direct_sansR': -0.01200, 'direct_Rcoh': -0.00400}

_S = (VR.Cinv_sn.copy(), VR.Cinv_one.copy(), float(VR.oCo), VR.Cinv_bao.copy(),
      T.DP_CI.copy(), B.D.DP_CI2.copy(), float(T.H0_SH_S))


def echelle(k):
    VR.Cinv_sn, VR.Cinv_one, VR.oCo = _S[0]*k*k, _S[1]*k*k, _S[2]*k*k
    VR.Cinv_bao = _S[3]*k*k
    T.DP_CI, B.D.DP_CI2 = _S[4]*k*k, _S[5]*k*k
    T.H0_SH_S = _S[6]/k


def sigma_parabole(cfg, e0, demi):
    """ajuste chi2 = c + A (eps-e0')^2 sur N_PAR points ; rend sigma = 1/sqrt(A), le sommet,
    et les deux points de controle de la validation D."""
    xs = np.linspace(e0 - demi, e0 + demi, N_PAR)
    cs = np.array([B.profil(float(x), cfg).fun for x in xs])
    bon = cs < 1e8
    if bon.sum() < 5:
        return None
    A2, A1, A0 = np.polyfit(xs[bon], cs[bon], 2)
    if A2 <= 0:
        return None
    sommet = -A1/(2*A2)
    return dict(sigma=float(1.0/np.sqrt(A2)), sommet=float(sommet),
                cmin=float(A0 - A1*A1/(4*A2)), A=float(A2))


def valide_parabole(cfg, p):
    """VALIDATION D : le chi2 REEL aux points +/- sigma doit valoir Delta = 1."""
    c0 = B.profil(p['sommet'], cfg).fun
    ds = []
    for s in (+1, -1):
        c = B.profil(p['sommet'] + s*p['sigma'], cfg).fun
        if c > 1e8:
            return None
        ds.append(float(c - c0))
    return ds


if __name__ == "__main__":
    import json
    print("REFERENT OU PRECISION, v3 — sigma parabolique auto-valide (criteres geles)\n")
    R = {}
    for k in KS:
        echelle(k)
        print(f"  --- k = {k:.0f} ---")
        M, non_opp = {}, []
        for nom, cfg in B.CFG.items():
            m = B.mesure(cfg, lo=LO, hi=HI, pas=PAS)
            # demi-largeur de l'ajustement : proportionnelle a la largeur attendue
            demi = max(3.0*PAS/k, 0.0006)
            p = sigma_parabole(cfg, m['eps'], demi)
            if p is None:
                non_opp.append(nom)
                M[nom] = dict(eps=m['eps'], sigma=np.nan, gain=m['gain'], ok=m['ok'],
                              xs=m['xs'], d=None)
                print(f"     {nom:<14s} eps = {m['eps']:+.5f}   AJUSTEMENT IMPOSSIBLE")
                continue
            d = valide_parabole(cfg, p)
            bon = d is not None and all(abs(x - 1.0) <= TOL_PARAB for x in d)
            if not bon:
                non_opp.append(nom)
            M[nom] = dict(eps=m['eps'], sigma=p['sigma'], gain=m['gain'], ok=m['ok'],
                          xs=m['xs'], d=d, opposable=bon)
            dd = "n/a" if d is None else f"[{d[0]:+.3f} ; {d[1]:+.3f}]"
            print(f"     {nom:<14s} eps = {m['eps']:+.5f}   sigma = {p['sigma']:.6f}   "
                  f"gain = {m['gain']:+9.2f}   Dchi2(+/-sigma) = {dd}"
                  f"{'' if bon else '   -> NON OPPOSABLE'}")
        v = np.array([m['eps'] for m in M.values()])
        s_opp = [m['sigma'] for n, m in M.items() if n not in non_opp]
        g = np.array([m['gain'] for m in M.values()])
        acc = all(float(m['ok'][m['xs'] < 0].mean()) > 0.90
                  and float(m['ok'][m['xs'] > 0].mean()) > 0.90 for m in M.values())
        R[k] = dict(eps={n: float(m['eps']) for n, m in M.items()},
                    E=float(v.max() - v.min()),
                    S=float(np.median(s_opp)) if s_opp else float('nan'),
                    G=float(np.median(g)), acces=bool(acc), non_opposables=non_opp)
        print(f"     E({k:.0f}) = {R[k]['E']:.5f}   S({k:.0f}) = {R[k]['S']:.6f}   "
              f"gain median = {R[k]['G']:+.2f}   non opposables : {len(non_opp)}/4")
    echelle(1.0)

    print("\n  --- validation A ---")
    okA = all(abs(R[1.0]['eps'][n] - a) < 1e-9 for n, a in ATTENDU_192.items())
    for n, a in ATTENDU_192.items():
        print(f"     {n:<14s} attendu {a:+.5f}   obtenu {R[1.0]['eps'][n]:+.5f}")
    if not okA:
        sys.exit("     ECHEC : rien n'est publie.")

    print("\n  --- validation D : l'estimateur parabolique est-il fiable ? ---")
    okD = True
    for k in KS:
        n = len(R[k]['non_opposables'])
        if n > 1:
            okD = False
        print(f"     k = {k:.0f} : {n}/4 configuration(s) non opposable(s)"
              f"{' — ' + ', '.join(R[k]['non_opposables']) if n else ''}"
              f"   {'OK' if n <= 1 else 'ECHEC'}")
    if not okD:
        sys.exit("     ECHEC : un estimateur faux sur la moitie des configurations ne vaut "
                 "pas mieux que le plancher qu'il remplace. Rien n'est publie.")

    print("\n  --- validation B : operativite, deux fois ---")
    okB = True
    for k in KS[1:]:
        f1 = R[1.0]['S']/R[k]['S']
        f2 = R[k]['G']/R[1.0]['G']
        b1, b2 = 0.7*k <= f1 <= 1.4*k, 0.8*k*k <= f2 <= 1.25*k*k
        okB = okB and b1 and b2
        print(f"     k = {k:.0f} : sigma x{f1:.2f} (exige {0.7*k:.1f}-{1.4*k:.1f}) "
              f"{'OK' if b1 else 'ECHEC'} ; gain x{f2:.2f} "
              f"(exige {0.8*k*k:.1f}-{1.25*k*k:.1f}) {'OK' if b2 else 'ECHEC'}")
    if not okB:
        sys.exit("     ECHEC : on ne teste rien, rien n'est publie.")

    print("\n  --- validation C ---")
    okC = all(R[k]['acces'] for k in KS)
    print(f"     deux signes accessibles partout : {okC}")
    if not okC:
        sys.exit("     ECHEC : rien n'est publie.")

    print("\n  --- criteres 1 et 2 : LE TEST ---")
    for k in KS:
        print(f"     k = {k:.0f}   E = {R[k]['E']:.5f}   S = {R[k]['S']:.6f}")
    r = R[4.0]['E']/R[1.0]['E']
    print(f"     E(4)/E(1) = {r:.3f}")
    if r <= 0.35:
        v2 = ("PRECISION — la lecture du #193 est REFUTEE : l'etendue retrecit avec les "
              "donnees, l'ambiguite etait statistique")
    elif r >= 0.75:
        v2 = "REFERENT CONFIRME — ameliorer les donnees ne reduit pas l'ambiguite"
    else:
        v2 = "INDETERMINE — la lecture du #193 reste NON ETABLIE"
    print(f"     -> {v2}")

    print("\n  --- critere 3 : signature croisee ---")
    for k in KS:
        print(f"     k = {k:.0f}   E/S = {R[k]['E']/R[k]['S']:.1f}")
    q1, q4 = R[1.0]['E']/R[1.0]['S'], R[4.0]['E']/R[4.0]['S']
    v3 = ("E/S CROIT — signature du referent" if q4 > 1.3*q1 else
          "E/S DECROIT — signature contraire" if q4 < 0.77*q1 else
          "E/S CONSTANT — signature de la precision")
    print(f"     de {q1:.1f} a {q4:.1f}  -> {v3}")

    print("\n  --- critere 4 : consequence ---")
    for k in KS:
        d = abs(R[k]['eps']['table_etiq'] - R[k]['eps']['table_coh'])
        print(f"     k = {k:.0f} : etiquette et coherent se contredisent a "
              f"{d/R[k]['S']:.1f} sigma")

    out = {str(int(k)): {q: R[k][q] for q in ('eps', 'E', 'S', 'G', 'acces',
                                              'non_opposables')} for k in KS}
    out['_verdict2'], out['_verdict3'], out['_rapport'] = v2, v3, float(r)
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "test_referent_v3.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/test_referent_v3.json")
