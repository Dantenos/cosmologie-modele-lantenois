#!/usr/bin/env python3
"""LA CONFLUENCE SUR PLANCK COMPLET, v2 — VALIDATION CORRIGEE.
CRITERES PRE-ENREGISTRES (geles AVANT toute execution de CETTE version, 24/08/2026).

POURQUOI UNE v2, ET CE QUE J'AI DEJA VU (declaration d'honnetete, cf. E3 v0 -> v1).
confluence_planck.py (gele 74bf63bdcc2a) a ECHOUE SA PROPRE VALIDATION et n'a donc rien
publie — c'est le protocole qui a fonctionne, pas une donnee qui a parle. Le vice est de MA
conception : je comparais chi2('pente', 0, 0) evalue au point de DEPART (omch2 = 0,1200 ;
ln10As = 3,044) a une reference LCDM OPTIMISEE (1998,63). Un point non optimise contre un
minimum : la validation ne pouvait que echouer. Valeur vue avant d'ecrire cette v2 :
2009,02. Elle ne renseigne en RIEN sur eps1 ni sur z0 — la question scientifique est
intacte — mais elle est declaree. Aucun critere scientifique n'est modifie ci-dessous :
seule la validation l'est. Le vice est verse a MANQUEMENTS (#162), lignee #148/#158.

VALIDATION CORRIGEE (si elle echoue, RIEN n'est publie) :
  chi2('pente', eps0 = 0, eps1 = 0) evalue AU MINIMUM LCDM lui-meme — (omch2, ln10As) =
  (0,1182 ; 3,039), produit par planck_theta.py gele et lu dans state_lcdm.json — doit
  reproduire 1998,633 a +/- 0,5. C'est le vrai controle : la branche PPF a w = -1 doit
  redonner LCDM AU MEME POINT. Un ecart signerait un defaut de branchement, seule chose
  que cette validation a jamais eu vocation a tester.

Tout le reste (modele, branchement declare, garde primordiale, bornes, depart a eps1 = 0
par regle 6, criteres 1 a 4, bande rigide predite [0,218 ; 0,262], intervalle leger
[0,090 ; 0,340]) est REPRIS SANS CHANGEMENT de confluence_planck.py, dont le code est
importe tel quel — il n'est pas modifie, il est reutilise.

RAPPEL DES CRITERES SCIENTIFIQUES (inchanges, recopies pour que ce fichier se suffise) :
  1. LE RUNNING. d = chi2(eps1 = 0) - chi2_min a 1 ddl (eps1 = 0 est exactement wCDM) :
     DEMANDE si d >= 4,0 ; NE DEMANDE PAS si d < 1,0 ; INTERMEDIAIRE sinon. La
     significativite rapportee est le rapport de vraisemblance, jamais la courbure locale.
  2. LOCALISATION. Profil sur eps1 (grille declaree 0,0 ; 0,2 ; 0,4 ; 0,6 ; 0,8 ; 1,0 ;
     1,4 ; 2,0), (omch2, ln10As, eps0) reoptimises ; z0 = exp(eps0/eps1) - 1 ; intervalle
     1 sigma = les z0 des points a dchi2 <= 1. Si 1 est negatif : NON LOCALISE, stop.
  3. CONVERGENCE RIGIDE si [0,218 ; 0,262] coupe l'intervalle 1 sigma de z0 ; TENSION si
     disjoint a 2 sigma ; INTERMEDIAIRE sinon.
  4. CONVERGENCE INDEPENDANTE si l'intervalle coupe [0,090 ; 0,340] (#161) ; sinon
     DIVERGENCE ENTRE JEUX, versee a T9.
  Regle 9 : criteres 3 et 4 en desaccord = rien n'est exploite.
  Regle 3 : cette etude REDUIT l'espace des formes ; elle n'en ferme aucune.

Usage : python3 ../../scripts/confluence_planck_v2.py <budget>   (depuis
donnees/pantheon_plus ; reprenable, etat dans state_confluence_v2.json).
"""
import sys, os, json, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import confluence_planck as C1

C1.STATE = "state_confluence_v2.json"
LCDM_X = [0.1182, 3.039]
LCDM_REF = 1998.633


def main():
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    st = C1.charge()
    st.setdefault('x', LCDM_X + [0.02, 0.0])
    st.setdefault('steps', [0.0008, 0.008, 0.05, 0.20])

    if st['valid'] is None:
        c = C1.chi2_pente(LCDM_X + [0.0, 0.0])
        st['valid'] = c
        st['nev'] += 1
        C1.sauve(st)
        print(f"[validation v2] pente(0,0) au minimum LCDM = {c:.3f} vs {LCDM_REF} -> "
              f"{'OK' if abs(c - LCDM_REF) < 0.5 else 'ECHEC'}", flush=True)
    if abs(st['valid'] - LCDM_REF) >= 0.5:
        sys.exit(f"  VALIDATION ECHOUE ({st['valid']:.3f}) — rien n'est publie.")

    if st['best'] is None:
        st['x'] = LCDM_X + [0.02, 0.0]
        st['best'] = C1.chi2_pente(st['x'])
        st['nev'] += 1
        C1.sauve(st)

    if st['phase'] == 0:
        x, steps, best, nev, fini = C1.motif(st['x'], st['steps'], st['best'],
                                             [0, 1, 2, 3], budget, st)
        print(f"[phase1] chi2 = {best:.3f}  x = {np.round(x, 4)}  evals = {st['nev']}  "
              f"fini = {fini}", flush=True)
        if fini:
            st['phase'] = 1
            st['x0_prof'] = list(x)
            st['best_global'] = float(best)
        C1.sauve(st)
        return

    for e1 in C1.GRILLE_E1:
        k = str(e1)
        if k in st['profil']:
            continue
        x0 = list(st.get('x0_prof', st['x']))
        x0[3] = e1
        c0 = C1.chi2_pente(x0)
        st['nev'] += 1
        x, steps, best, nev, fini = C1.motif(x0, [0.0008, 0.008, 0.05, 0.0], c0,
                                             [0, 1, 2], budget, st)
        st['profil'][k] = best
        st['prof_x'][k] = list(np.round(x, 6))
        C1.sauve(st)
        print(f"[profil] eps1 = {e1}  chi2 = {best:.3f}  eps0 = {x[2]:+.4f}  "
              f"evals = {st['nev']}  fini = {fini}", flush=True)
        if not fini:
            return
        break
    else:
        st['done'] = True
        C1.sauve(st)
        C1.verdicts(st)


if __name__ == "__main__":
    main()
