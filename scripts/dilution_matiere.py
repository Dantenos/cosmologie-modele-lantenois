#!/usr/bin/env python3
"""LA MATIERE DILUE-T-ELLE EN a^-3 ? — MESURE BILATERALE, ET LE TEST D'UNE CLASSE PUBLIEE.
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

POURQUOI CETTE ETUDE, ET CE QU'ELLE REPARE.
Le #167 a mesure l'exposant de dilution de la matiere avec un etalonnage coherent et obtenu
une contrainte tres serree — mais le #173 a montre que ce verdict etait UNILATERAL : dans
l'implementation de l'atlas, la branche eps < 0 est inaccessible, parce que ce modele-la
impose la conservation totale du secteur sombre et que rho_de y diverge vers -infini quand
eps < 0. Or **le signe negatif est precisement celui qu'annonce la litterature** :
Yang, Dai & Wang (arXiv:2505.09879) contraignent rho_dm ~ (1+z)^(3-eps) avec les priors de
distance Planck et annoncent eps = -0,0073 +0,0029/-0,0033, soit ~2,4 sigma.
Le #171 avait rapproche les deux ; le #173 a RETIRE ce rapprochement, precisement parce que
leur branche nous etait fermee. Cette etude ouvre la branche et rend la comparaison possible.

LE MODELE, ET EN QUOI IL DIFFERE DU NOTRE (declare). On pose ici, comme la classe publiee :
    rho_m(a) = Om a^(eps-3)      et      rho_Lambda = 1 - Om - Or   CONSTANTE,
SANS imposer la conservation totale du secteur sombre. C'est ce qui rend les deux signes
accessibles, et c'est aussi ce qui distingue cette famille de 'ilcdm_dm' : la notre compense
dans rho_de, la leur ne compense pas. On ne prete donc a personne un modele qu'il n'a pas.

L'ENJEU D'ETALONNAGE (etabli au #166, confirme au #167). chi2 tire r_d, z_*, r_* et
R = sqrt(Om) D_c(z_*) d'un SEUL Om. Or dans cette famille la densite de matiere aux temps
primordiaux vaut Om a^eps, et non Om. Utiliser l'etiquette Om — ce que fait la classe
publiee, qui emploie les priors comprimes et la formule de Hu-Sugiyama — donne au modele
une densite pour son expansion et une autre pour son etalonnage.
  ETALONNAGE-ETIQUETTE : chi2 recoit Om (ce que fait la litterature).
  ETALONNAGE-COHERENT  : chi2 recoit Om_cal = Om a_*^eps, la densite a la recombinaison,
    obtenue en construisant le fond avec Om = Om_cal a_*^(-eps). Epoque de reference
    a_* = 1/1091, avec un controle de sensibilite a a_eq = 1/3388.

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. A eps = 0 les deux etalonnages doivent redonner LCDM a 1e-3 pres (1425,086) : sans
     echange, l'etiquette EST la densite reelle.
  B. LES DEUX SIGNES doivent etre accessibles : sur la grille declaree
     eps dans [-0,05 ; +0,05], au moins 90 % des points doivent rendre un chi2 fini des
     DEUX cotes de zero. C'est exactement le controle qui manquait au #167, et c'est la
     raison d'etre de cette etude — s'il echoue, elle n'a pas lieu d'etre.
  C. Le balayage doit etre assez fin pour resoudre l'echelle annoncee par la litterature
     (|eps| ~ 0,007) : pas <= 0,001.

--- CRITERES (exhaustifs, exclusifs) ---
  1. ETALONNAGE-ETIQUETTE. eps prefere et Delta chi2 contre LCDM, avec sigma par profil.
     DETECTION REPRODUITE si |eps| >= 2 sigma ET de signe NEGATIF (comme la classe publiee) ;
     DETECTION DE SIGNE OPPOSE si |eps| >= 2 sigma mais positif ;
     PAS DE DETECTION si |eps| < 2 sigma. Ecrit tel quel dans les trois cas.
  2. ETALONNAGE-COHERENT. Meme mesure. C'est le resultat de l'etude.
  3. VERDICT CROISE, qui est la question posee :
     ARTEFACT D'ETALONNAGE CONFIRME si le critere 1 donne une detection (>= 2 sigma) ET le
        critere 2 n'en donne pas (< 2 sigma) ;
     DETECTION ROBUSTE si les deux donnent une detection de MEME SIGNE ;
     PAS DE DETECTION DU TOUT si aucun des deux ;
     AMBIGU sinon (regle 9 : rien n'est exploite, versement au greffe).
  4. CONTRAINTE PUBLIABLE. Quel que soit le verdict, on rapporte l'intervalle a 2 sigma sur
     eps sous l'etalonnage coherent, BILATERAL. C'est le nombre que le corpus n'a pas.
  5. SENSIBILITE A L'EPOQUE. On refait le critere 2 a a_eq et on rapporte l'ecart. S'il
     depasse 1,0 en chi2 au minimum, l'etalonnage est declare AMBIGU pour cette famille et
     le critere 4 est rapporte avec cette incertitude ajoutee.

CE QUE CETTE ETUDE NE FERA PAS. Elle ne refute pas arXiv:2505.09879 : leurs donnees,
leur pipeline et leurs nuisances different des notres. Elle mesure, dans NOTRE pipeline, si
le choix d'etalonnage suffit a produire une detection de la taille annoncee. C'est tout, et
c'est deja un fait verifiable.
Regle 3 : cette etude REDUIT ; elle ne ferme rien.
Usage : python3 scripts/dilution_matiere.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A

AG = A.AG
B0 = [0.69, 0.02236, 0.31]
STARTS = [B0, [0.68, 0.0224, 0.29], [0.70, 0.0223, 0.33]]
CHI2_LCDM = 1425.086
A_STAR, A_EQ = 1.0 / 1091.0, 1.0 / 3388.0
SENT = 1e8


def fond_etiq(Om, eps):
    """rho_m = Om a^(eps-3), Lambda constante. Etalonnage : chi2 recevra Om (l'etiquette)."""
    Or = Om / 3388.0
    lam = 1 - Om - Or
    if lam <= 0:
        return None
    E2 = Om * AG**(eps - 3) + Or / AG**4 + lam
    return A.fond_arrays(E2)


def fond_coh(Om_cal, eps, a_ref):
    """meme fond, mais parametre par la densite A LA RECOMBINAISON : Om_eff(a_ref) = Om_cal,
    donc Om = Om_cal a_ref^(-eps). chi2 recevra Om_cal, qui est alors la bonne densite."""
    Om = Om_cal * a_ref**(-eps)
    if not (0.05 < Om < 0.95):
        return None
    return fond_etiq(Om, eps)


A.CUSTOM.update({
    'dil_etiq': fond_etiq,
    'dil_coh': lambda Om, p: fond_coh(Om, p, A_STAR),
    'dil_coh_eq': lambda Om, p: fond_coh(Om, p, A_EQ),
})


def profil(fam, eps):
    return A.fit(fam, 1, STARTS, fixpar=float(eps)).fun


def mesure(fam, lo=-0.05, hi=0.05, pas=0.001):
    xs = np.arange(lo, hi + 1e-12, pas)
    cs = np.array([profil(fam, x) for x in xs])
    ok = cs < SENT
    i = int(np.argmin(np.where(ok, cs, np.inf)))
    c0, e0 = float(cs[i]), float(xs[i])
    # sigma par profil dchi2 = 1, de part et d'autre
    def bord(sens):
        j = i
        while 0 <= j + sens < len(xs):
            j += sens
            if not ok[j] or cs[j] > c0 + 1.0:
                return abs(xs[j] - e0)
        return abs(xs[-1 if sens > 0 else 0] - e0)
    return e0, c0, bord(+1), bord(-1), xs, cs, ok


if __name__ == "__main__":
    print("LA MATIERE DILUE-T-ELLE EN a^-3 ? (criteres geles)\n")

    print("  --- validation A : eps = 0 doit redonner LCDM ---")
    for nom, fam in [("etiquette", 'dil_etiq'), ("coherent a_*", 'dil_coh')]:
        c = profil(fam, 0.0)
        print(f"     {nom:<14s} chi2(eps=0) = {c:.3f}  (LCDM {CHI2_LCDM})  "
              f"-> {'OK' if abs(c - CHI2_LCDM) < 1e-3 else 'ECHEC'}")
        if abs(c - CHI2_LCDM) >= 1e-3:
            sys.exit("     rien n'est publie.")

    e1, c1, sp1, sm1, xs1, cs1, ok1 = mesure('dil_etiq')
    e2, c2, sp2, sm2, xs2, cs2, ok2 = mesure('dil_coh')

    print("\n  --- validation B : les DEUX signes sont-ils accessibles ? ---")
    for nom, xs, ok in [("etiquette", xs1, ok1), ("coherent", xs2, ok2)]:
        neg = ok[xs < 0].mean() if (xs < 0).any() else 0.0
        pos = ok[xs > 0].mean() if (xs > 0).any() else 0.0
        print(f"     {nom:<12s} eps < 0 : {100*neg:5.1f} % accessible ; "
              f"eps > 0 : {100*pos:5.1f} %")
        if not (neg > 0.90 and pos > 0.90):
            sys.exit("     VALIDATION B ECHOUE — la branche manquante rend l'etude sans objet.")
    print("     -> les deux branches sont ouvertes : c'est ce que le #173 n'avait pas\n")

    print("  --- criteres 1 et 2 ---")
    res = {}
    for tag, nom, e, c, sp, sm in [("1", "etiquette", e1, c1, sp1, sm1),
                                    ("2", "coherent", e2, c2, sp2, sm2)]:
        sig = abs(e) / max(min(sp, sm), 1e-9)
        d = CHI2_LCDM - c
        if sig >= 2 and e < 0:
            v = "DETECTION REPRODUITE (negative, comme la classe publiee)"
        elif sig >= 2:
            v = "DETECTION DE SIGNE OPPOSE (positive)"
        else:
            v = "PAS DE DETECTION"
        res[nom] = (e, sig, v)
        print(f"     [{tag}] {nom:<10s} eps = {e:+.5f} +{sp:.5f}/-{sm:.5f}  "
              f"({sig:.1f} sigma)  gain = {d:+.2f}")
        print(f"          -> {v}")

    d1 = res["etiquette"][1] >= 2
    d2 = res["coherent"][1] >= 2
    if d1 and not d2:
        v3 = "ARTEFACT D'ETALONNAGE CONFIRME"
    elif d1 and d2 and np.sign(res["etiquette"][0]) == np.sign(res["coherent"][0]):
        v3 = "DETECTION ROBUSTE"
    elif not d1 and not d2:
        v3 = "PAS DE DETECTION DU TOUT"
    else:
        v3 = "AMBIGU — regle 9, rien n'est exploite"
    print(f"\n  VERDICT 3 (croise) : {v3}")

    # critere 4 : intervalle a 2 sigma, bilateral, sous l'etalonnage coherent
    m = ok2 & (cs2 <= c2 + 4.0)
    lo2, hi2 = float(xs2[m].min()), float(xs2[m].max())
    print(f"\n  CRITERE 4 (contrainte publiable) : sous etalonnage coherent,")
    print(f"     eps dans [{lo2:+.4f} ; {hi2:+.4f}] a 2 sigma (bilateral)")

    # critere 5 : sensibilite a l'epoque de reference
    e3, c3, sp3, sm3, _, _, _ = mesure('dil_coh_eq')
    dd = abs(c3 - c2)
    print(f"\n  CRITERE 5 (sensibilite) : a a_eq, eps = {e3:+.5f}, chi2 = {c3:.3f} "
          f"(ecart {dd:.3f})")
    print(f"     -> {'ETALONNAGE AMBIGU pour cette famille' if dd > 1.0 else 'stable'}")
    print("\n  Rappel gele : cette etude ne refute pas arXiv:2505.09879. Elle mesure, dans")
    print("  NOTRE pipeline, si le choix d'etalonnage suffit a produire une detection de la")
    print("  taille annoncee.")
