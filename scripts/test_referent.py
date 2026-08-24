#!/usr/bin/env python3
"""L'AMBIGUITE EST-ELLE DE REFERENT OU DE PRECISION ? — LE TEST QUI TRANCHE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

L'ENJEU. Le #193 a REFUTE mon explication precedente (perte d'information d'amplitude) et
laisse a sa place une lecture que j'ai explicitement declaree NON ETABLIE :
   "l'ambiguite n'est pas de precision, elle est de REFERENT : R et les formules de
    r_d / r_* / z_* reclament UN omega_m, cette famille en a DEUX, et rien dans les donnees
    ne dit lequel."
Je me suis trompe pendant deux entrees en repetant une explication sans la tester. Celle-ci
fait une PREDICTION FALSIFIABLE, et c'est la seule raison de l'ecrire :

   SI l'ambiguite est de REFERENT, alors AMELIORER LES DONNEES NE LA REDUIT PAS.
   Chaque configuration verra son sigma retrecir, mais l'ECART ENTRE CONFIGURATIONS restera.
   SI au contraire elle est de PRECISION, l'etendue retrecira comme les sigma.

C'est une prediction qui peut echouer, et si elle echoue la lecture du #193 tombe comme est
tombee celle du #190. Aucune reformulation de secours n'est prevue.

LE PROTOCOLE. On reprend la famille CORRIGEE du #192 (baryons en a^-3, gele 863df81e97bd) et
ses quatre configurations. On divise toutes les incertitudes des donnees par un facteur k,
c'est-a-dire qu'on multiplie les inverses de covariance par k^2 : Cinv_sn, Cinv_bao, la
covariance des priors comprimes, et le prior H0 de SH0ES. AUCUN fichier gele n'est modifie ;
la mise a l'echelle est faite EN MEMOIRE et declaree ici. k = 1, 2, 4 -- soit des donnees
jusqu'a 4 fois meilleures que celles qui existent, ce qui depasse tout releve prevu.
C'est deliberement genereux : si l'etendue survit a k = 4, elle survivra a la realite.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. A k = 1, les quatre configurations doivent redonner EXACTEMENT les valeurs du #192 :
     +0,00700 / -0,00400 / -0,01200 / -0,00400. Sinon la mise a l'echelle a change autre
     chose que les incertitudes, et la comparaison est nulle.
  B. LA MISE A L'ECHELLE DOIT MARCHER. Le sigma moyen des quatre configurations doit
     retrecir d'un facteur compris entre 0,7k et 1,4k quand on passe de 1 a k. Si les sigma
     ne retrecissent pas, on ne teste rien du tout et on s'arrete -- c'est le controle qui
     empeche de conclure sur une manipulation inoperante.
  C. Les deux signes de eps doivent rester accessibles a chaque k.

--- CRITERES (exhaustifs, exclusifs) ---
  1. ETENDUE EN FONCTION DE k. On rapporte E(k) = max(eps) - min(eps) sur les quatre
     configurations, pour k = 1, 2, 4. Et le sigma median S(k).
  2. LE TEST. On forme le rapport r = E(4)/E(1).
     REFERENT CONFIRME si r >= 0,75 -- l'ambiguite ne se laisse pas reduire par les donnees ;
     PRECISION (donc REFERENT REFUTE) si r <= 0,35 -- c'est-a-dire si E retrecit au moins
        aussi vite que 1/k ; la lecture du #193 tombe et on l'ecrit ;
     INDETERMINE si 0,35 < r < 0,75 -- et alors la lecture du #193 reste NON ETABLIE, ce
        qu'elle etait deja : aucun progres, et on le dit sans le maquiller.
  3. CONTROLE CROISE, qui est la vraie signature. On rapporte le rapport E(k)/S(k) pour
     chaque k. Si l'ambiguite est de referent, ce rapport CROIT avec k -- l'ecart entre
     lectures devient de plus en plus significatif a mesure que les donnees s'ameliorent.
     Si elle est de precision, il reste CONSTANT. On rapporte la valeur a k = 1 et a k = 4,
     et on nomme laquelle des deux signatures est observee.
  4. CONSEQUENCE CHIFFREE. Si le referent est confirme, on rapporte a quel niveau de sigma
     les deux etalonnages (etiquette et coherent) se contrediraient avec des donnees k fois
     meilleures. C'est le nombre qui dit a partir de quand la question devient bloquante pour
     la classe entiere de ces mesures.

REGLE 6. Cette etude teste une lecture A MOI, apres qu'une precedente a ete refutee. Les
seuils vont donc contre : le seuil de confirmation est 0,75 et non 0,5 ; la branche qui me
refute est testee AVANT celle qui me confirme dans le code ; et la validation B peut
m'arreter parce que ma propre manipulation serait inoperante.
REGLE 5, accorde d'avance : diviser uniformement toutes les incertitudes est une idealisation
-- de vraies donnees futures ameliorent certains jeux plus que d'autres, et introduiraient
des systematiques nouvelles. Ce test dit ce que fait la STATISTIQUE seule, pas ce que fera
DR3. Un contradicteur a le droit d'exiger une simulation realiste ; nous ne la faisons pas.
Regle 3 : ce test REDUIT le nombre de lectures possibles du #193 ; il ne mesure pas eps.
Usage : python3 scripts/test_referent.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_baryons as B
import test_wE_v3 as T
import vraisemblance_reelle as V

KS = (1.0, 2.0, 4.0)
ATTENDU_192 = {'table_etiq': +0.00700, 'table_coh': -0.00400,
               'direct_sansR': -0.01200, 'direct_Rcoh': -0.00400}

# --- copies des inverses de covariance a l'etat gele, pour pouvoir les remettre
_Cinv_sn0 = V.Cinv_sn.copy()
_Cinv_one0 = V.Cinv_one.copy()
_oCo0 = float(V.oCo)
_Cinv_bao0 = V.Cinv_bao.copy()
_DP_CI0 = T.DP_CI.copy()
_DP_CI20 = B.D.DP_CI2.copy()
_H0S0 = float(T.H0_SH_S)


def echelle(k):
    """divise toutes les incertitudes par k, EN MEMOIRE. Aucun fichier gele n'est touche."""
    k2 = k*k
    V.Cinv_sn = _Cinv_sn0*k2
    V.Cinv_one = _Cinv_one0*k2
    V.oCo = _oCo0*k2
    V.Cinv_bao = _Cinv_bao0*k2
    T.DP_CI = _DP_CI0*k2
    B.D.DP_CI2 = _DP_CI20*k2
    T.H0_SH_S = _H0S0/k


if __name__ == "__main__":
    import json
    print("REFERENT OU PRECISION ? (criteres geles)\n")
    R = {}

    for k in KS:
        echelle(k)
        print(f"  --- k = {k:.0f} (incertitudes divisees par {k:.0f}) ---")
        M = {}
        for nom, cfg in B.CFG.items():
            m = B.mesure(cfg)
            M[nom] = m
            print(f"     {nom:<14s} eps = {m['eps']:+.5f}   sigma = "
                  f"{min(m['sp'], m['sm']):.5f}   gain = {m['gain']:+8.2f}")
        vals = np.array([m['eps'] for m in M.values()])
        sigs = np.array([min(m['sp'], m['sm']) for m in M.values()])
        acc = all(float(m['ok'][m['xs'] < 0].mean()) > 0.90
                  and float(m['ok'][m['xs'] > 0].mean()) > 0.90 for m in M.values())
        R[k] = dict(eps={n: float(m['eps']) for n, m in M.items()},
                    E=float(vals.max() - vals.min()),
                    S=float(np.median(sigs)), acces=bool(acc))
        print(f"     etendue E({k:.0f}) = {R[k]['E']:.5f}   sigma median S({k:.0f}) = "
              f"{R[k]['S']:.5f}   deux signes accessibles : {acc}")

    echelle(1.0)   # on remet l'etat gele

    print("\n  --- validation A : k = 1 redonne-t-il le #192 ? ---")
    okA = True
    for nom, att in ATTENDU_192.items():
        got = R[1.0]['eps'][nom]
        bon = abs(got - att) < 1e-9
        okA = okA and bon
        print(f"     {nom:<14s} attendu {att:+.5f}   obtenu {got:+.5f}   "
              f"-> {'OK' if bon else 'ECHEC'}")
    if not okA:
        sys.exit("     la mise a l'echelle a change autre chose : rien n'est publie.")

    print("\n  --- validation B : la mise a l'echelle est-elle operante ? ---")
    okB = True
    for k in KS[1:]:
        fact = R[1.0]['S']/R[k]['S']
        bon = 0.7*k <= fact <= 1.4*k
        okB = okB and bon
        print(f"     k = {k:.0f} : sigma median passe de {R[1.0]['S']:.5f} a "
              f"{R[k]['S']:.5f}, facteur {fact:.2f}  (attendu {0.7*k:.1f}-{1.4*k:.1f})"
              f"  -> {'OK' if bon else 'ECHEC'}")
    if not okB:
        sys.exit("     la manipulation est inoperante : on ne teste rien, rien n'est publie.")

    print("\n  --- validation C : les deux signes restent accessibles ---")
    okC = all(R[k]['acces'] for k in KS)
    print(f"     -> {'OK' if okC else 'ECHEC'}")
    if not okC:
        sys.exit("     une branche s'est fermee : rien n'est publie.")

    print("\n  --- critere 1 : etendue en fonction de k ---")
    for k in KS:
        print(f"     k = {k:.0f}   E = {R[k]['E']:.5f}   S = {R[k]['S']:.5f}")

    print("\n  --- critere 2 : LE TEST ---")
    r = R[4.0]['E']/R[1.0]['E'] if R[1.0]['E'] > 0 else np.nan
    print(f"     E(4)/E(1) = {R[4.0]['E']:.5f} / {R[1.0]['E']:.5f} = {r:.3f}")
    if r <= 0.35:
        v2 = ("PRECISION — la lecture du #193 est REFUTEE : l'etendue retrecit avec les "
              "donnees, l'ambiguite etait bien statistique")
    elif r >= 0.75:
        v2 = ("REFERENT CONFIRME — ameliorer les donnees ne reduit pas l'ambiguite")
    else:
        v2 = ("INDETERMINE — la lecture du #193 reste NON ETABLIE, exactement comme avant "
              "ce test ; aucun progres")
    print(f"     -> {v2}")

    print("\n  --- critere 3 : la signature croisee ---")
    for k in KS:
        print(f"     k = {k:.0f}   E/S = {R[k]['E']/R[k]['S']:.2f}")
    q1, q4 = R[1.0]['E']/R[1.0]['S'], R[4.0]['E']/R[4.0]['S']
    if q4 > 1.3*q1:
        v3 = "E/S CROIT — signature du referent"
    elif q4 < 0.77*q1:
        v3 = "E/S DECROIT — signature contraire, non prevue par les deux lectures"
    else:
        v3 = "E/S CONSTANT — signature de la precision"
    print(f"     de {q1:.2f} a {q4:.2f}  -> {v3}")

    print("\n  --- critere 4 : consequence chiffree ---")
    for k in KS:
        de = abs(R[k]['eps']['table_etiq'] - R[k]['eps']['table_coh'])
        print(f"     k = {k:.0f} : etiquette et coherent se contredisent a "
              f"{de/R[k]['S']:.1f} sigma")

    out = {str(int(k)): R[k] for k in KS}
    out['_verdict2'] = v2
    out['_verdict3'] = v3
    out['_rapport'] = float(r)
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "test_referent.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/test_referent.json")
