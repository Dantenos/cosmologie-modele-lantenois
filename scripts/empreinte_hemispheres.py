#!/usr/bin/env python3
"""LE #116 PORTAIT-IL DE LA SIGNIFICATIVITE FABRIQUEE PAR L'EMPREINTE AU CIEL ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

D'OU VIENT CETTE QUESTION, ET ELLE NE VIENT PAS DE MOI.
Une verification de litterature commandee pour savoir si la fonction de selection angulaire
de Pantheon+ valait un article a rendu un verdict net : elle ne le vaut pas, tout est publie
depuis 2015. Mais elle a rapporte au passage un fait qui, lui, nous vise :
  Bengaly, Andrade & Alcaniz (arXiv:1810.04966, EPJC 79, 768) mesurent que l'EMPREINTE SEULE
  deplace une statistique hemispherique de H0 de 3,4 a 2,7 sigma, tout le reste egal --
  c'est-a-dire qu'une couverture non uniforme FABRIQUE environ 0,7 sigma de significativite
  apparente.
Et la litterature va plus loin : Colin, Mohayaee, Rameez & Sarkar (arXiv:1808.04597) ecrivent
« Due to the anisotropic sky coverage of the dataset, it would be hard to find n-hat from the
data, so we choose it to be along the CMB dipole direction » -- ils ABANDONNENT un parametre
libre a l'empreinte. Bengaly, Bernui & Alcaniz (arXiv:1503.01413) : « it is not possible to
determine any violation of the CP, in this redshift range, with the limitation of the current
datasets. »

CE QUE LE CORPUS FAIT DEJA BIEN, ET CE QU'IL NE FAIT PAS.
  - `etude_E1_vides.py` (#141-142) fait tourner le CATALOGUE DE VIDES en gardant les SNe a
    leur position observee : nul PRESERVANT L'EMPREINTE, celui que la litterature recommande.
  - `etude_E1_manche2/3` permutent les etiquettes PARMI LES SNe OBSERVEES : meme garantie,
    c'est le « shuffle test » de Bengaly 2015.
  - Le #116 -- la premiere manche des hemispheres, Delta_beta = +0,22 +/- 0,23 -- n'a AUCUN
    de ces controles. Le docstring gele d'`etude_E1_vides` le dit lui-meme :
    « systematique d'empreinte au ciel non traitee en #116 ». C'est le seul point expose,
    et c'est celui-ci qu'on ferme.

LE PROTOCOLE. On garde les 1580 SNe a leur position observee -- on ne les bouge JAMAIS -- et
on fait tourner l'AXE DE PARTAGE : N_AXES directions tirees uniformement sur la sphere, meme
pipeline, meme beta SN-seules a Om fixe. La distribution des Delta_beta ainsi obtenue est le
nul preservant l'empreinte. On y situe la valeur du #116 (axe du dipole CMB).

--- VALIDATIONS (si l'une echoue, RIEN n'est publie) ---
  A. REJEU DU #116. L'axe du dipole CMB (RA = 167,9 ; Dec = -6,9) doit rendre 553 SNe d'un
     cote (+/- 5) et un Delta_beta a moins de 0,10 de +0,22. C'est la meme validation que le
     critere 4 d'`etude_E1_vides`, et elle garantit qu'on teste bien le #116 et pas autre
     chose.
  B. L'ECHANTILLONNAGE DOIT ETRE ISOTROPE. Les N_AXES directions doivent avoir une moyenne
     vectorielle de norme < 3/sqrt(N_AXES) : sinon le tirage est biaise et le nul ne vaut
     rien.
  C. Chaque axe retenu doit laisser au moins 150 SNe de chaque cote, comme le PLANCHER des
     manches 2 et 3. Les axes plus desequilibres sont ecartes et COMPTES.

--- CRITERES (exhaustifs, exclusifs) ---
  1. LARGEUR DU NUL. sigma_axe = ecart-type des Delta_beta sur les axes retenus, a comparer
     au sigma_Delta = 0,23 que la covariance annonce au #116.
  2. VERDICT SUR LA COVARIANCE, calque sur le critere bloquant d'`etude_E1_vides` :
     COVARIANCE SOUS-ESTIMEE si sigma_axe > 2 x sigma_Delta -- l'empreinte revele une
        systematique que la covariance ignore, et le #116 doit etre re-derive ;
     COVARIANCE CONSERVATRICE si sigma_axe < 0,5 x sigma_Delta ;
     COVARIANCE FIDELE entre les deux -- le #116 tient tel quel.
  3. LE #116 EST-IL SPECIAL ? p-valeur empirique bilaterale de |Delta_beta(dipole CMB)|
     dans la distribution des axes aleatoires.
     BANAL si p > 0,05 -- la valeur du #116 est ce que l'empreinte produit pour un axe
        quelconque, et son verdict « universel » est CONFORTE, pas menace ;
     REMARQUABLE si p <= 0,05, et alors il faut expliquer pourquoi cet axe-la.
  4. AMPLEUR FABRIQUEE. On rapporte le quantile a 68 % de |Delta_beta| sur les axes
     aleatoires, en unites de sigma_Delta. C'est la traduction directe du chiffre de
     Bengaly et al. dans NOTRE pipeline : combien de sigma apparents l'empreinte seule
     peut-elle produire ici ?

REGLE 6. Ce controle peut condamner un resultat du corpus (le #116 alimente la premiere
manche d'E1 et le papier A). Les seuils vont donc contre nous : la branche
« COVARIANCE SOUS-ESTIMEE » est testee AVANT les autres, et le critere 3 declare BANAL --
donc rassurant -- seulement si p depasse 0,05, pas l'inverse.
REGLE 5, accorde d'avance : faire tourner l'axe n'explore pas toutes les facons dont
l'empreinte peut tromper (elle correle aussi position et redshift, ce que ce test ne touche
pas). Un contradicteur a le droit d'exiger des mocks a fonction de selection reconstruite ;
la litterature note qu'AUCUNE analyse SN Ia ne le fait, et nous non plus.
Regle 3 : ce controle REDUIT l'incertitude sur le #116 ; il ne mesure pas beta.
Usage : python3 scripts/empreinte_hemispheres.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import etude_E1_vides as EV
import vraisemblance_reelle as VR

N_AXES = 300
GRAINE = 20260824
PLANCHER = 150
SIG_116 = 0.23
DB_116 = 0.22
APEX_RA, APEX_DEC = 167.9, -6.9


def directions_sn():
    """vecteurs unitaires des 1580 SNe, a leur position OBSERVEE. Jamais deplaces."""
    raw = np.genfromtxt(pathlib.Path(VR.__file__).parent.parent / "donnees" /
                        "pantheon_plus" / "pantheon.dat", names=True, dtype=None,
                        encoding="utf-8")
    m = (raw['zHD'] > 0.01) & (raw['IS_CALIBRATOR'] == 0)
    ra, dec = np.radians(raw['RA'][m]), np.radians(raw['DEC'][m])
    return np.column_stack([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])


def axe(ra_deg, dec_deg):
    r, d = np.radians(ra_deg), np.radians(dec_deg)
    return np.array([np.cos(d)*np.cos(r), np.cos(d)*np.sin(r), np.sin(d)])


if __name__ == "__main__":
    import json
    print("EMPREINTE AU CIEL ET HEMISPHERES (criteres geles)\n")
    n = directions_sn()
    print(f"  {len(n)} SNe a leur position observee ; elles ne bougeront pas.\n")

    print("  --- validation A : rejeu du #116 ---")
    sel = (n @ axe(APEX_RA, APEX_DEC)) > 0
    n1 = int(sel.sum())
    res = EV.delta_beta(sel, sigma=True)
    db = float(res[4])
    okA = abs(n1 - 553) <= 5 and abs(db - DB_116) < 0.10
    print(f"     axe du dipole CMB : {n1} / {len(n)-n1} SNe   (attendu 553 / 1027 +/- 5)")
    print(f"     Delta_beta = {db:+.3f}   (#116 : {DB_116:+.3f})   "
          f"-> {'OK' if okA else 'ECHEC'}")
    if not okA:
        sys.exit("     on ne teste pas le #116 : rien n'est publie.")

    print("\n  --- validation B : le tirage d'axes est-il isotrope ? ---")
    rng = np.random.default_rng(GRAINE)
    A = rng.normal(size=(N_AXES, 3))
    A /= np.linalg.norm(A, axis=1)[:, None]
    norme = float(np.linalg.norm(A.mean(axis=0)))
    seuil = 3.0/np.sqrt(N_AXES)
    print(f"     moyenne vectorielle de {N_AXES} axes : {norme:.4f}   "
          f"(seuil {seuil:.4f})  -> {'OK' if norme < seuil else 'ECHEC'}")
    if norme >= seuil:
        sys.exit("     tirage biaise : rien n'est publie.")

    print("\n  --- balayage des axes (nul preservant l'empreinte) ---")
    nulls, ecartes = [], 0
    for i, a in enumerate(A):
        s = (n @ a) > 0
        if min(int(s.sum()), int((~s).sum())) < PLANCHER:
            ecartes += 1
            continue
        nulls.append(float(EV.delta_beta(s, sigma=False)[4]))
        if (i + 1) % 50 == 0:
            print(f"     {i+1}/{N_AXES} axes", flush=True)
    nulls = np.array(nulls)
    print(f"     {len(nulls)} axes retenus, {ecartes} ecartes "
          f"(moins de {PLANCHER} SNe d'un cote)")

    print("\n  --- critere 1 : largeur du nul ---")
    s_axe = float(nulls.std(ddof=1))
    print(f"     sigma_axe = {s_axe:.4f}   contre sigma_Delta = {SIG_116:.4f} "
          f"annonce au #116   rapport {s_axe/SIG_116:.2f}")

    print("\n  --- critere 2 : VERDICT SUR LA COVARIANCE ---")
    if s_axe > 2*SIG_116:
        v2 = ("COVARIANCE SOUS-ESTIMEE — l'empreinte revele une systematique que la "
              "covariance ignore ; le #116 doit etre re-derive avant le papier A")
    elif s_axe < 0.5*SIG_116:
        v2 = "COVARIANCE CONSERVATRICE — le sigma annonce au #116 est trop large"
    else:
        v2 = "COVARIANCE FIDELE — le #116 tient tel quel"
    print(f"     {v2}")

    print("\n  --- critere 3 : le #116 est-il special ? ---")
    p = float((np.abs(nulls) >= abs(db)).mean())
    v3 = ("BANAL — la valeur du #116 est ce que l'empreinte produit pour un axe quelconque ; "
          "son verdict « universel » en sort CONFORTE"
          if p > 0.05 else
          "REMARQUABLE — il faut expliquer pourquoi cet axe-la")
    print(f"     p-valeur bilaterale de |Delta_beta| = {abs(db):.3f} : p = {p:.3f}")
    print(f"     -> {v3}")

    print("\n  --- critere 4 : ampleur fabriquee par l'empreinte ---")
    q68 = float(np.quantile(np.abs(nulls), 0.68))
    print(f"     quantile 68 % de |Delta_beta| sur axes aleatoires = {q68:.4f}")
    print(f"     soit {q68/SIG_116:.2f} sigma_Delta apparents produits par la seule")
    print(f"     empreinte  (Bengaly et al. mesurent ~0,7 sigma sur leur statistique)")

    out = dict(n_sne=len(n), db_116=db, n1=n1, sigma_axe=s_axe, sigma_116=SIG_116,
               verdict_covariance=v2, p_valeur=p, verdict_special=v3, q68=q68,
               axes_retenus=len(nulls), axes_ecartes=ecartes)
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "empreinte_hemispheres.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/empreinte_hemispheres.json")
