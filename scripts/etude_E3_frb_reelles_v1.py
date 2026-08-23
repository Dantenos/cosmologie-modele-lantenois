#!/usr/bin/env python3
"""E3 v1 — FRB SUR DONNEES REELLES, critere de validation CORRIGE ET DECLARE.
CRITERES PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 23/08/2026).

POURQUOI UNE v1. Le critere de la spec mere (« le refit LCDM doit redonner f_IGM publie a
+/- 0,10 ») porte sur une variable NON IDENTIFIABLE dans la machinerie gelee : dans
frb_likelihood.py, f_IGM et f_X n'entrent que par leur somme f_d = f_IGM + f_X (verifie
numeriquement le 23/08 : logL identique a 10 decimales pour (0,80;0,11), (0,61;0,30),
(0,91;0,00) a somme fixee — leur partage vient d'une modelisation halo que cette
vraisemblance n'a pas). v0 (etude_E3_frb_reelles.py, gele 77e8bff5d7b5) a applique le
critere tel quel : ECHEC a 0,002 pres sur une coordonnee arbitraire du plateau ->
NON EXPLOITE, verdict conserve. Meme vice que le garde-fou #49 : critere ecrit sur la
mauvaise variable.
DECLARATION D'HONNETETE : la table des -lnL par fond de v0 a ete vue avant l'ecriture de
ce script (elle s'imprimait avant la porte de validation). La correction ci-dessous est
neanmoins structurelle — la degenerescence se prouve sans les donnees — et le present
docstring fige le critere avant toute nouvelle execution.

DONNEES ET METHODE : identiques a v0 (69 FRB de Connor et al. 2025, sha256 d3458b33... ;
trois fonds geles ; memes fits Nelder-Mead a quatre departs).

CRITERES v1 (exhaustifs, exclusifs).
  - VALIDATION : f_d(LCDM) = f_IGM + f_X du fit LCDM dans [0,81 ; 1,01] (leur total
    diffus 0,80 + 0,11 = 0,91, a +/- 0,10 — la transcription fidele de l'esprit de la
    spec sur la variable identifiable) ET exp(mu_host) dans [60 ; 250] pc/cm3 (leur
    mediane ~120-130). Sinon NON EXPLOITE.
  - Si la validation passe : Delta_chi2(CCBH - LCDM) et (accretion - LCDM) rapportes TELS
    QUELS (un tirage, significativite indicative sqrt(Dchi2)), avec les nuisances par fond
    et l'indicateur de bord f_d = 1. Aucun seuil de victoire.
  - Ecart au 2,1 sigma des mocks (#99) rapporte sans etre arbitre.
Usage : python3 scripts/etude_E3_frb_reelles_v1.py
"""
import sys, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E3_frb_reelles as V0   # reutilise charge() et fit() ; importe frb_likelihood

if __name__ == "__main__":
    data = V0.charge()
    print(f"E3 v1 — {len(data)} FRB reels (Connor et al. 2025), critere corrige (f_d), voir docstring\n")
    res = {}
    for which, nom in [("L", "LCDM"), ("A", "accretion b=2,595"), ("C", "CCBH calibre")]:
        r = V0.fit(data, which); res[which] = r
        f_, x_, mu, sig = r.x
        print(f"  {nom:>18s} : -lnL = {r.fun:9.3f} | f_d = {f_+x_:.3f}  exp(mu) = {np.exp(mu):6.1f}  sigma = {sig:.3f}")
    fd = res["L"].x[0] + res["L"].x[1]; mu = np.exp(res["L"].x[2])
    ok = 0.81 <= fd <= 1.01 and 60 <= mu <= 250
    print(f"\n  VALIDATION v1 : f_d(LCDM) = {fd:.3f} (publie 0,91 +/- 0,10) ; exp(mu) = {mu:.1f} -> "
          + ("PASSE" if ok else "ECHEC -> NON EXPLOITE"))
    if ok:
        dC = 2*(res["C"].fun - res["L"].fun); dA = 2*(res["A"].fun - res["L"].fun)
        bord = res["C"].x[0] + res["C"].x[1]
        print(f"  Dchi2(CCBH - LCDM)      = {dC:+.2f}   (~{np.sqrt(abs(dC)):.1f} sigma, un tirage ; mocks #99 : ~2,1 sigma en mediane)")
        print(f"  Dchi2(accretion - LCDM) = {dA:+.2f}   (~{np.sqrt(abs(dA)):.1f} sigma)")
        print(f"  CCBH pousse f_d au bord : f_d = {bord:.3f}" + (" = 1 -> le deficit baryonique n'est PAS absorbable par les nuisances" if bord > 0.98 else ""))
        print("  Rapporte tel quel. Substitution aux mocks du papier C : etape d'auteur (spec mere).")
