#!/usr/bin/env python3
"""L'AVANCE DU CHAMPION DE L'ATLAS VIENT-ELLE DE L'ETALONNAGE ? — VALIDATION CORRIGEE.
CRITERES PRE-ENREGISTRES (geles AVANT execution de CETTE version, 24/08/2026).

POURQUOI UNE v4 (declaration, lignee #162). La v3 (gelee e8b21204edac) a ECHOUE SA
VALIDATION et n'a rien publie : je comparais 'ilcdm_de' a CUSTOM['wcdm'], qui RECALCULE
Or a partir de Om' — je remettais donc dans la comparaison l'ecart de rayonnement que
j'avais moi-meme diagnostique. Vice de MA conception, le quatrieme de la journee (#148,
#158, #162, #165). Valeurs vues avant d'ecrire cette v4 : les |dE/E| de 8,4e-3 a 3,3e-2 de
la v3, et rien d'autre — la v3 s'est arretee avant tout resultat scientifique.

LE BON COMPARANT. 'ilcdm_coh' (gele dans degenerescence_ilcdm_v2, 00deaf7745d8) pose
Or = Om'/3388 : son fond est ALORS rigoureusement fond_gen(Om', w'), meme Or, meme Ode,
meme E(z) — c'est ce que cette validation verifie. Les deux ne different plus que par
l'ETALONNAGE : chi2 tire r_d, z_*, r_* et R = sqrt(Om)*Dc(z*) de l'etiquette Om pour
'ilcdm_coh', et de Om' pour 'wcdm'. Or la densite de matiere de ce modele avant
recombinaison est Om', pas Om. FAIT DEJA ACQUIS ET DECLARE (#164 volet 1) : 'ilcdm_coh'
vaut 1415,251, gain +9,835. Ce qui reste inconnu est le minimum HONNETE de wCDM, et donc
la part imputable a l'etalonnage.

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  max |dE/E| entre CUSTOM['ilcdm_coh'](Om, eps) et CUSTOM['wcdm'](Om', w') < 1e-12, en
  QUATRE points declares : (0,2981 ; +0,0213), (0,32 ; +0,05), (0,28 ; -0,03), (0,35 ; +0,10).
  Quatre points, pour qu'une identite ne puisse pas etre une coincidence.

--- VOLET 1 : LE MINIMUM HONNETE DE wCDM ---
Profil complet en w sur [-1,10 ; -0,90], 21 valeurs, (h, omega_b, Om) reoptimises a chaque
valeur — aucun optimiseur multidimensionnel a qui reprocher de s'etre coince.
  ARTEFACT D'ETALONNAGE CONFIRME  si min du profil >= 1421,0 (le modele coherent gagne
     <= 4,1 sur LCDM : l'essentiel des 9,84 vient de l'etalonnage) ;
  ARTEFACT REFUTE                 si min du profil <= 1417,0 (gain >= 8,1 : le fit wcdm de
     l'atlas etait coince ; les deux modeles sont le meme et doivent figurer A EGALITE) ;
  INTERMEDIAIRE                   sinon, ecrit tel quel.

--- VOLET 2 : L'ARTEFACT CHIFFRE, A FONDS IDENTIQUES ---
Pour eps dans (-0,05 ; -0,02 ; 0 ; +0,0213 ; +0,05 ; +0,08), les deux chi2 sur les MEMES
fonds : 'ilcdm_coh' a eps fixe (etalonnage-etiquette) contre 'wcdm' a w' = eps/3-1 fixe
(etalonnage-coherent), (h, omega_b, Om) reoptimises des deux cotes.
  CONTROLE INTERNE : a eps = 0 l'ecart doit etre < 0,05 (sans echange, l'etiquette EST la
  densite reelle). Si ce controle echoue, le volet 2 n'est pas interprete.

--- VOLET 3 : DIAGNOSTIC SUR 'ilcdm_dm' (aucun verdict rendu) ---
Sa matiere vaut Om*a^eps a l'epoque du drag : on rapporte le facteur (1e-3)^eps au meilleur
eps, pour dire si la meme question se pose. Y repondre serait une autre etude.

--- CONSEQUENCE (regle 8) ---
Si ARTEFACT CONFIRME : RETRACTATION numerotee en MANQUEMENTS et portee a
TRIAGE_DES_ATTAQUES, touchant #150, #154, #156, #158, la RESOLUTION de T7 et le verdict 2c
de #161 — sans attenuation ni delai.
Regle 3 : l'echange sombre n'est pas refute ; c'est la MESURE de son avantage qui l'est.
Usage : python3 scripts/degenerescence_ilcdm_v4.py   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import atlas_v1 as A
import degenerescence_ilcdm_v2 as D2

B = [0.69, 0.02236, 0.31]
CHI2_LCDM = 1425.086
CHI2_ATLAS_ILCDM = 1415.245
CHI2_ATLAS_WCDM = 1423.843
CHI2_ILCDM_COH = 1415.251
POINTS = [(0.2981, 0.0213), (0.32, 0.05), (0.28, -0.03), (0.35, 0.10)]
STARTS = [B, [0.68, 0.0224, 0.28], [0.70, 0.0223, 0.33], [0.685, 0.02245, 0.305]]


def image_coh(Om, eps):
    """(Om', w') du fond a rayonnement coherent (bases_coherentes est gelee en v2)."""
    _, _, Omp = D2.bases_coherentes(Om, eps)
    return Omp, eps / 3.0 - 1.0


if __name__ == "__main__":
    print("L'AVANCE VIENT-ELLE DE L'ETALONNAGE ? v4, validation corrigee (criteres geles)\n")

    print("  --- validation : fonds identiques en quatre points ---")
    pire = 0.0
    for Om, eps in POINTS:
        Omp, wp = image_coh(Om, eps)
        za, Ea = A.CUSTOM['ilcdm_coh'](Om, eps)
        zb, Eb = A.CUSTOM['wcdm'](Omp, wp)
        e = float(np.max(np.abs(Eb / Ea - 1)))
        pire = max(pire, e)
        print(f"    (Om = {Om:.4f}, eps = {eps:+.4f}) -> (Om' = {Omp:.5f}, w' = {wp:.5f}) : "
              f"max |dE/E| = {e:.3e}")
    if pire >= 1e-12:
        sys.exit(f"    VALIDATION ECHOUE (pire = {pire:.3e}) — rien n'est publie.")
    print(f"    -> les deux familles ont LE MEME fond (pire = {pire:.3e}). "
          f"Seul l'etalonnage differe.\n")

    print("  --- VOLET 1 : profil complet en w de wCDM (21 valeurs) ---")
    best, w_best = 1e18, None
    for w in np.linspace(-1.10, -0.90, 21):
        c = A.fit('wcdm', 1, STARTS, fixpar=float(w)).fun
        if c < best:
            best, w_best = c, float(w)
    gain = CHI2_LCDM - best
    print(f"    minimum du profil : chi2 = {best:.3f} a w = {w_best:.4f} "
          f"(l'atlas publiait {CHI2_ATLAS_WCDM})")
    print(f"    gain du modele COHERENT sur LCDM = {gain:+.3f}   "
          f"(etalonnage-etiquette : +{CHI2_LCDM - CHI2_ILCDM_COH:.3f})")
    if best >= 1421.0:
        v1 = "ARTEFACT D'ETALONNAGE CONFIRME"
    elif best <= 1417.0:
        v1 = "ARTEFACT REFUTE — le fit wcdm de l'atlas etait coince"
    else:
        v1 = "INTERMEDIAIRE"
    print(f"    VERDICT VOLET 1 : {v1}")

    print("\n  --- VOLET 2 : l'artefact a fonds identiques ---")
    print(f"    {'eps':>8s} {'etiquette':>11s} {'coherent':>11s} {'artefact':>10s}")
    art0 = None
    for eps in (-0.05, -0.02, 0.0, 0.0213, 0.05, 0.08):
        c_lab = A.fit('ilcdm_coh', 1, STARTS, fixpar=float(eps)).fun
        c_coh = A.fit('wcdm', 1, STARTS, fixpar=float(eps / 3.0 - 1.0)).fun
        if eps == 0.0:
            art0 = c_coh - c_lab
        print(f"    {eps:+8.4f} {c_lab:11.3f} {c_coh:11.3f} {c_coh - c_lab:+10.3f}"
              + ("   <- controle interne" if eps == 0.0 else ""))
    print(f"    controle interne a eps = 0 : ecart = {art0:+.4f} -> "
          f"{'OK' if abs(art0) < 0.05 else 'ECHEC — volet 2 NON INTERPRETE'}")

    print("\n  --- VOLET 3 : diagnostic sur 'ilcdm_dm' (aucun verdict) ---")
    r_dm = A.fit('ilcdm_dm', 1, [B + [0.02], B + [-0.02]], bornes=[(-0.5, 0.5)])
    e_dm = float(r_dm.x[3])
    fac = (1e-3) ** e_dm
    print(f"    meilleur eps = {e_dm:+.5f} ; matiere a a = 1e-3 = {fac:.4f} * Om "
          f"({100*(fac-1):+.2f} %) -> la meme question se pose ; autre etude, autres criteres.")

    print()
    if v1 == "ARTEFACT D'ETALONNAGE CONFIRME":
        part = best - CHI2_ILCDM_COH
        print(f"  VERDICT : RETRACTATION DUE. Fond identique, deux densites de matiere : "
              f"l'expansion suit Om',\n            l'etalonnage (r_d, z_*, r_*, R) suit Om. "
              f"Part imputable a l'etalonnage = {part:.2f} des\n            "
              f"{CHI2_LCDM - CHI2_ILCDM_COH:.2f} unites d'avance. Retracter #150, #154, #156, "
              f"#158, la resolution de T7\n            et le verdict 2c de #161 "
              f"(regle 8 : MANQUEMENTS + TRIAGE_DES_ATTAQUES).")
    elif v1.startswith("ARTEFACT REFUTE"):
        print("  VERDICT : le fit wcdm de l'atlas etait coince — les deux modeles sont LE MEME "
              "et doivent\n            figurer a egalite. Classement faux, avance reelle ; "
              "retractation du seul classement.")
    else:
        print(f"  VERDICT : INTERMEDIAIRE (min = {best:.3f}) — regle 9 : rien n'est exploite.")
