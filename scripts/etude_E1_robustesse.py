#!/usr/bin/env python3
"""E1 ROBUSTESSE — deux doutes sur la manche 2, creuses avant d'etre crus. CRITERES
PRE-ENREGISTRES (geles par registre AVANT execution, 23/08/2026).

DOUTE 1 — Om FIXE. Les quatre partages d'E1 (Stopyra ; Douglass VoidFinder / VIDE / REVOLVER)
  ajustent beta SN-seules a Om = 0,314 fixe. Si Delta_beta bougeait avec Om, le verdict
  UNIVERSEL serait un artefact du choix. Test : Delta_beta a Om = 0,30 / 0,314 / 0,33 (la
  plage des ajustements du corpus), memes sous-echantillons.
  CRITERE : ROBUSTE si, pour les quatre partages, |Delta_beta(Om) - Delta_beta(0,314)| <
  0,5 sigma_Delta aux deux Om extremes ; sinon FRAGILE, et le verdict E1 est ETIQUETE
  « dependant de Om » dans les registres (pas retire : un nul a tous les Om reste un nul).

DOUTE 2 — SIGNES OPPOSES VoidFinder (+0,52) / VIDE (-0,40). Soit les deux algorithmes
  mesurent la meme chose et se contredisent (grave : le test n'est pas reproductible), soit
  ils trient des SNe DIFFERENTES (l'environnement « vide » n'est pas univoque, ce qui est
  un fait, pas une contradiction). Test : indice de Jaccard entre les sous-echantillons
  « vides » des trois algorithmes (memes 455 SNe de l'empreinte), et Delta_beta sur les
  SNe que VoidFinder ET VIDE classent toutes deux « vides » contre celles qu'ils classent
  toutes deux « murs » (le coeur commun).
  CRITERE : si Jaccard(VF, VIDE) < 0,5, les signes opposes sont EXPLIQUES par des tris
  differents et ne constituent pas une incoherence ; le Delta_beta du coeur commun est
  rapporte tel quel, avec son sigma, sans verdict (echantillon reduit, declare d'avance
  trop petit pour un verdict : ~100-150 SNe par cote).
  Si Jaccard >= 0,5 : les algorithmes trient les memes SNe et donnent des signes opposes
  -> INCOHERENCE a consigner, manche 2 Douglass ETIQUETEE « non reproductible entre
  algorithmes » (la spec mere prevoit NON EXPLOITE si les juges divergent > 2 sigma ;
  ici ils ne divergent pas a 2 sigma, d'ou l'etiquette plutot que le retrait).
Valeurs de substitution : aucune. Rien ici ne modifie un verdict gele ; tout s'ajoute.

Usage : python3 scripts/etude_E1_robustesse.py  (depuis la racine du depot)
"""
import sys, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E
import etude_E1_manche2 as M

def fit_beta_om(idx, om):
    E.OM_FIXE = om
    return E.fit_beta(idx)

def delta_om(idx, sel, om):
    bv, sv = fit_beta_om(idx[sel], om); bm, sm = fit_beta_om(idx[~sel], om)
    return bv - bm, float(np.hypot(sv, sm))

if __name__ == "__main__":
    print("E1 ROBUSTESSE (criteres geles, voir docstring)\n")
    # les quatre partages, reconstruits a l'identique
    centres, R = E.charge_vides(); f0 = E.fraction_vide(centres, R)
    sel0 = f0 > 0; idx0 = np.arange(len(E.z_sn))
    cat, vf_dir = M.charge()
    ang = np.degrees(np.arccos(np.clip((E.n_hat @ vf_dir.T).max(1), -1, 1)))
    idx = np.where(ang < M.THETA)[0]
    partages = {"Stopyra": (idx0, sel0)}
    for nom, (c, r) in cat.items():
        f = M.fraction_union(c, r, idx); s, _ = M.partage(f); partages[nom] = (idx, s)

    # DOUTE 1
    print("[1] Delta_beta en fonction de Om fixe")
    fragile = []
    for nom, (ix, s) in partages.items():
        d314, s314 = delta_om(ix, s, 0.314)
        ligne = f"    {nom:10s} Om=0,314 : {d314:+.3f} +/- {s314:.3f}"
        for om in (0.30, 0.33):
            d, _ = delta_om(ix, s, om)
            ligne += f" | Om={om:.2f} : {d:+.3f} ({(d-d314)/s314:+.2f} sigma_D)"
            if abs(d - d314) >= 0.5*s314: fragile.append(f"{nom} a Om={om}")
        print(ligne)
    E.OM_FIXE = 0.314
    print("    ->", "ROBUSTE" if not fragile else "FRAGILE : " + ", ".join(fragile))

    # DOUTE 2
    print("\n[2] Recouvrement des sous-echantillons « vides » (455 SNe de l'empreinte)")
    noms = list(cat); S = {n: partages[n][1] for n in noms}
    for i in range(3):
        for j in range(i+1, 3):
            a, b = S[noms[i]], S[noms[j]]
            jac = (a & b).sum() / (a | b).sum()
            print(f"    Jaccard({noms[i]}, {noms[j]}) = {jac:.3f}   (communs {(a&b).sum()}, union {(a|b).sum()})")
    a, b = S["VoidFinder"], S["VIDE"]
    jac_vf_vide = (a & b).sum() / (a | b).sum()
    coeur_v = a & b; coeur_m = ~a & ~b
    print(f"    coeur commun VF et VIDE : vides {coeur_v.sum()} SNe, murs {coeur_m.sum()} SNe")
    sub = idx[coeur_v | coeur_m]; sel = coeur_v[coeur_v | coeur_m]
    bv, sv = E.fit_beta(sub[sel]); bm, sm = E.fit_beta(sub[~sel])
    print(f"    Delta_beta(coeur) = {bv-bm:+.3f} +/- {np.hypot(sv,sm):.3f}  (sans verdict : echantillon reduit)")
    print("    ->", "EXPLIQUE : tris differents, pas d'incoherence" if jac_vf_vide < 0.5
          else "INCOHERENCE : memes SNe, signes opposes -> etiquette « non reproductible entre algorithmes »")
