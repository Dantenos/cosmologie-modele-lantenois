#!/usr/bin/env python3
"""kappa(sigma) BGG — le couplage cosmologique depend-il de la dispersion de vitesse de l'hote ?
CRITERES PRE-ENREGISTRES (geles par registre AVANT toute ingestion de donnees, 25/08/2026).
Spec mere : etudes_2026.py (gelee). Verse dans l'affaire k3-vs-0 et EPROUVE P5 (papier A).

QUESTION. Le couplage cosmologique des trous noirs (M propto a^k ; Farrah 2023, Croker 2024)
est, s'il est reel, une propriete du FOND : k ne doit PAS dependre des proprietes de l'hote.
Le discriminant le plus direct est la dispersion de vitesse sigma des galaxies les plus
brillantes de groupe/amas (BGG/BCG) : croissance cosmologique -> k universel, dk/dln sigma = 0 ;
croissance astrophysique (fusions seches, accretion locale) -> k(sigma) en pente. Notre modele
(papier A, prediction P5, k_eff = -3w) predit l'universalite : la lecture goulet exige
dk/dln sigma = 0. Une pente mesuree serait defavorable A LA FOIS a CCBH et a notre P5.

DONNEES (empreintes a verser dans donnees/SHA256SUMS AVANT lecture).
  - Echantillon primaire Farrah et al. 2023 (ApJ 944 L31 ; ApJL 943 L2) : ellipticals SDSS
    locales, M_BH et sigma publies ; k mesure par bins de sigma. SOURCE PRIMAIRE seulement
    (regle E5 : aucun k repris d'un resume secondaire ; statut refuse sinon).
  - Replication requise sur >= 1 echantillon sigma independant (p.ex. MaNGA/SDSS BCG, ou
    l'echantillon JWST elargi 2506.19589 stratifie par sigma) pour qu'un SIGNAL soit opposable.
  LIMITE DECLAREE : un seul echantillon = au mieux CANDIDAT, jamais SIGNAL (spec mere exige
  >= 2 echantillons independants).

METHODE (rien ici ne sera ajuste apres avoir vu dk/dln sigma).
  1. Bins de sigma a effectifs egaux (>= 3 bins) ; k ajuste independamment par bin, machinerie
     k-tracker (outils/ktracker.py + contraintes_k.json) inchangee.
  2. Pente dk/dln sigma par moindres carres ponderes ; sigma_pente par bootstrap des hotes.
  3. CONTROLE D'EQUITE (regle 2) : refaire la pente avec le binning et les k PUBLIES du camp
     k=3 (Farrah/Croker), jamais les miens ; l'ecart n'est retenu que s'il survit a leur binning.
  4. Valeur de substitution manquante (regle 6) : inventee dans le sens DEFAVORABLE a
     l'universalite (on prete au signal environnemental le benefice du doute, pas a soi).

CRITERES.
  - SIGNAL (dependance environnementale, CONTRE universalite/CCBH et contre P5) = |dk/dln sigma|
    incompatible avec 0 a > 2 sigma ET reproduit sur >= 2 echantillons sigma independants.
  - UNIVERSEL (manche au goulet/CCBH gagnee) si dk/dln sigma compatible avec 0 sur >= 2
    echantillons.
  - NON EXPLOITE si un seul echantillon, ou si les echantillons divergent entre eux > 2 sigma
    (desaccord des juges n'est pas un verdict, regle 9), ou si le k d'un bin vient d'un resume
    secondaire (regle E5). Un controle sur deux echoue => rien n'est exploite.
  - Verdict au format Adversaire ; inscription Audience (affaire k3-vs-0) au lancement.

Usage : etude_kappa_sigma_bgg.py spec | verdict <bgg_sigma_k.csv>
"""
import sys, pathlib


def spec():
    print(__doc__)
    print("[kappa-sigma-BGG] spec gelee. Aucune donnee ingeree : aucun verdict emis "
          "(regle 1 + regle 9).")


def verdict(p):
    if not pathlib.Path(p).exists():
        sys.exit(f"[kappa-sigma-BGG] {p} introuvable : le juge (echantillon sigma) n'est pas "
                 f"arrive. Aucun verdict sans donnees relues contre la source primaire.")
    sys.exit("[kappa-sigma-BGG] execution du protocole gele NON IMPLEMENTEE dans la spec v0 : "
             "brancher la machinerie k-tracker sur les bins de sigma, puis rapporter dk/dln sigma "
             "TEL QUEL (favorable ou non). Rien ne se juge sans avoir tourne.")


if __name__ == "__main__":
    a = sys.argv[1:]
    {"spec": spec, "verdict": lambda: verdict(a[1])}.get(a[0] if a else "?",
                                                         lambda: sys.exit(__doc__))()
