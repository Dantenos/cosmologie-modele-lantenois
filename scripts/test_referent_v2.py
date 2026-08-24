#!/usr/bin/env python3
"""REFERENT OU PRECISION, v2 — LE PLANCHER DE GRILLE LEVE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI UNE v2, ET CE QU'ELLE NE CHANGE PAS.
La v1 (gelee, voir registre) s'est ARRETEE SUR SA PROPRE VALIDATION B : elle exigeait que le
sigma median retrecisse d'un facteur 0,7k a 1,4k, et a k = 4 elle a mesure 2,00 au lieu des
2,8 a 5,6 attendus. La cause n'est pas physique : le balayage se fait au pas de 0,001, donc
un sigma lu par marche de grille NE PEUT PAS descendre sous 0,001. A k = 4 le vrai sigma vaut
~0,0005 et la grille le plafonne. La validation a donc correctement refuse de conclure sur
une mesure que son propre maillage ne pouvait pas rendre.

CE QUE LA v2 CORRIGE, ET RIEN D'AUTRE : apres le balayage grossier, un balayage FIN de pas
0,0001 sur +/-0,004 autour du minimum donne le sigma. La resolution passe de 1e-3 a 1e-4,
soit dix fois mieux que le sigma le plus serre attendu. Les criteres, les seuils, les
configurations et les donnees sont INCHANGES. Le raffinement agit identiquement a tous les k,
donc il ne peut pas biaiser le rapport E(4)/E(1) dans un sens ou dans l'autre -- c'est la
raison pour laquelle il est licite de le faire APRES avoir vu le blocage.

CE QUE LA v1 A DEJA MONTRE, ET QUI N'EST PAS REPRIS ICI COMME ACQUIS : a k = 1, 2 et 4, les
quatre valeurs de eps sont LITTERALEMENT identiques (+0,00700 / -0,00400 / -0,01200 /
-0,00400) et les gains suivent k^2 a la troisieme decimale (+9,36 -> +37,43 -> +149,72, soit
x4,00 puis x16,00). Ce second fait prouve que la mise a l'echelle etait bien operante. Mais
la validation B demandait autre chose, et on ne substitue pas une preuve a une autre :
c'est la v2 qui doit passer la validation telle qu'elle est ecrite.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. A k = 1, les quatre configurations doivent redonner les valeurs du #192 :
     +0,00700 / -0,00400 / -0,01200 / -0,00400.
  B. LA MISE A L'ECHELLE DOIT ETRE OPERANTE, et on l'exige maintenant DEUX FOIS :
     b1. le sigma median doit retrecir d'un facteur compris entre 0,7k et 1,4k ;
     b2. le gain median sur LCDM doit croitre d'un facteur compris entre 0,8k^2 et 1,25k^2.
     Les deux, sinon on ne teste rien. Le second controle est ajoute parce que c'est lui
     qui, dans la v1, montrait l'operativite quand le premier etait aveugle.
  C. Les deux signes de eps restent accessibles a chaque k.
  D. RESOLUTION SUFFISANTE : le sigma le plus petit mesure doit valoir au moins 5 pas fins
     (5e-4). Sinon le plancher est simplement deplace et non leve, et on s'arrete.

--- CRITERES (exhaustifs, exclusifs) ---
  1. E(k) = max(eps) - min(eps) sur les quatre configurations, et S(k) le sigma median,
     pour k = 1, 2, 4.
  2. LE TEST : r = E(4)/E(1).
     REFERENT CONFIRME si r >= 0,75 ; PRECISION (donc REFERENT REFUTE) si r <= 0,35 ;
     INDETERMINE entre les deux, et alors la lecture du #193 reste NON ETABLIE.
  3. SIGNATURE CROISEE : E(k)/S(k). Croissante -> referent ; constante -> precision.
  4. CONSEQUENCE : a quel niveau de sigma les etalonnages etiquette et coherent se
     contredisent, pour chaque k.

REGLE 6. La branche qui me refute est testee AVANT celle qui me confirme, le seuil de
confirmation est 0,75 et non 0,5, et deux validations distinctes peuvent m'arreter.
REGLE 5 : diviser uniformement toutes les incertitudes est une idealisation ; de vraies
donnees futures ameliorent certains jeux plus que d'autres et introduiraient des
systematiques nouvelles. Ce test dit ce que fait la STATISTIQUE seule.
Regle 3 : il REDUIT le nombre de lectures possibles ; il ne mesure pas eps.
Usage : python3 scripts/test_referent_v2.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_baryons as B
import test_wE_v3 as T
import vraisemblance_reelle as V

KS = (1.0, 2.0, 4.0)
PAS_FIN, DEMI = 0.0001, 0.004
ATTENDU_192 = {'table_etiq': +0.00700, 'table_coh': -0.00400,
               'direct_sansR': -0.01200, 'direct_Rcoh': -0.00400}

_S = (V.Cinv_sn.copy(), V.Cinv_one.copy(), float(V.oCo), V.Cinv_bao.copy(),
      T.DP_CI.copy(), B.D.DP_CI2.copy(), float(T.H0_SH_S))


def echelle(k):
    """divise toutes les incertitudes par k, EN MEMOIRE. Aucun fichier gele n'est touche."""
    V.Cinv_sn, V.Cinv_one, V.oCo = _S[0]*k*k, _S[1]*k*k, _S[2]*k*k
    V.Cinv_bao = _S[3]*k*k
    T.DP_CI, B.D.DP_CI2 = _S[4]*k*k, _S[5]*k*k
    T.H0_SH_S = _S[6]/k


def mesure_fine(cfg):
    """balayage grossier pour situer le minimum, puis balayage FIN pour le sigma."""
    m = B.mesure(cfg)
    e0 = m['eps']
    xs = np.arange(e0 - DEMI, e0 + DEMI + 1e-12, PAS_FIN)
    cs = np.array([B.profil(float(x), cfg).fun for x in xs])
    ok = cs < 1e8
    i = int(np.argmin(np.where(ok, cs, np.inf)))
    c0, ef = float(cs[i]), float(xs[i])

    def bord(sens):
        j = i
        while 0 <= j + sens < len(xs):
            j += sens
            if not ok[j] or cs[j] > c0 + 1.0:
                return abs(float(xs[j]) - ef)
        return DEMI
    return dict(eps=e0, eps_fin=ef, sigma=min(bord(+1), bord(-1)),
                gain=m['gain'], ok=m['ok'], xs=m['xs'])


if __name__ == "__main__":
    import json
    print("REFERENT OU PRECISION, v2 (criteres geles)\n")
    R = {}
    for k in KS:
        echelle(k)
        print(f"  --- k = {k:.0f} ---")
        M = {n: mesure_fine(c) for n, c in B.CFG.items()}
        for n, m in M.items():
            print(f"     {n:<14s} eps = {m['eps']:+.5f}   sigma(fin) = {m['sigma']:.5f}"
                  f"   gain = {m['gain']:+9.2f}")
        v = np.array([m['eps'] for m in M.values()])
        s = np.array([m['sigma'] for m in M.values()])
        g = np.array([m['gain'] for m in M.values()])
        acc = all(float(m['ok'][m['xs'] < 0].mean()) > 0.90
                  and float(m['ok'][m['xs'] > 0].mean()) > 0.90 for m in M.values())
        R[k] = dict(eps={n: float(m['eps']) for n, m in M.items()},
                    E=float(v.max() - v.min()), S=float(np.median(s)),
                    G=float(np.median(g)), smin=float(s.min()), acces=bool(acc))
        print(f"     E({k:.0f}) = {R[k]['E']:.5f}   S({k:.0f}) = {R[k]['S']:.5f}   "
              f"gain median = {R[k]['G']:+.2f}   deux signes : {acc}")
    echelle(1.0)

    print("\n  --- validation A ---")
    okA = all(abs(R[1.0]['eps'][n] - a) < 1e-9 for n, a in ATTENDU_192.items())
    for n, a in ATTENDU_192.items():
        print(f"     {n:<14s} attendu {a:+.5f}   obtenu {R[1.0]['eps'][n]:+.5f}")
    if not okA:
        sys.exit("     ECHEC : rien n'est publie.")

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

    print("\n  --- validations C et D ---")
    okC = all(R[k]['acces'] for k in KS)
    smin = min(R[k]['smin'] for k in KS)
    okD = smin >= 5*PAS_FIN
    print(f"     deux signes accessibles partout : {okC}")
    print(f"     sigma le plus petit = {smin:.5f} pour un pas fin de {PAS_FIN} "
          f"({smin/PAS_FIN:.0f} pas)  -> {'OK' if okD else 'ECHEC : plancher deplace'}")
    if not (okC and okD):
        sys.exit("     ECHEC : rien n'est publie.")

    print("\n  --- criteres 1 et 2 : LE TEST ---")
    for k in KS:
        print(f"     k = {k:.0f}   E = {R[k]['E']:.5f}   S = {R[k]['S']:.5f}")
    r = R[4.0]['E']/R[1.0]['E']
    print(f"     E(4)/E(1) = {r:.3f}")
    if r <= 0.35:
        v2 = ("PRECISION — la lecture du #193 est REFUTEE : l'etendue retrecit avec les "
              "donnees")
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

    out = {str(int(k)): R[k] for k in KS}
    out['_verdict2'], out['_verdict3'], out['_rapport'] = v2, v3, float(r)
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "test_referent_v2.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/test_referent_v2.json")
