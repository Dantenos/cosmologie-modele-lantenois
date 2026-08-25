#!/usr/bin/env python3
"""kappa-Delta_v — le couplage (k_eff = -3w, w = -beta/(3Ht)) depend-il de la PROFONDEUR de
vide Delta_v traversee ? CRITERES PRE-ENREGISTRES (geles par registre AVANT toute lecture,
25/08/2026). Extension de E1 (etude_E1_vides.py, gelee) : E1 partage a la MEDIANE de la
fraction de vide ; ici on trie par la PROFONDEUR Delta_v (contraste de sous-densite) et on
cherche un gradient de k_eff / beta. Spec mere : etudes_2026.py (gelee).

QUESTION. Lecture horloge : plus la ligne de visee traverse de vide PROFOND (Delta_v tres
negatif), plus w est negatif, donc beta / k_eff grand -> gradient dk_eff/dDelta_v != 0.
Lecture goulet/CCBH : universalite stricte, gradient nul. C'est la manche PROFONDEUR du duel
goulet/horloge, complementaire de la manche FRACTION (E1, verdict UNIVERSEL sur 2 juges,
#141-142). Delta_beta = beta_profond - beta_peu_profond > 0 signerait la lecture horloge.

PUISSANCE PRE-ENREGISTREE (le « >= 25 » de la file d'attente, gele avant lecture).
  Le levier de profondeur n'est opposable que si l'echantillon atteint un contraste suffisant :
  on EXIGE N >= 25 SNe dans le bin de vide PROFOND (Delta_v <= seuil, seuil fixe au quartile le
  plus creux du catalogue) AVANT lecture. En deca : DECLARE D'AVANCE puissance faible — un nul
  n'est PAS une exclusion de la lecture horloge, seulement une absence de signal a cette
  precision (cf. E4). Le seuil et N sont lus sur la geometrie, pas ajustes sur Delta_beta.

DONNEES (empreintes dans donnees/SHA256SUMS ; reutilise E1).
  - Pantheon+SH0ES.dat + STAT+SYS.cov (GitHub PantheonPlusSH0ES) : coupures du corpus
    (zHD > 0,01, calibrateurs exclus -> 1580 SNe), positions RA/DEC.
  - Catalogue de vides AVEC profondeur Delta_v : Stopyra et al. 2023 (Zenodo 10160612,
    combined_catalogue_properties.csv, colonne de sous-densite / contraste de densite).
    Replication VAST SDSS DR7 (Douglass au CDS) EXIGEE pour un SIGNAL (spec mere : >= 2
    catalogues independants). LIMITE DECLAREE : un seul catalogue -> au mieux CANDIDAT.

METHODE (rien ici ne sera ajuste apres avoir vu le gradient).
  1. Delta_v par SN = sous-densite la plus creuse (ou moyenne ponderee par la corde) des vides
     traverses ; geometrie E1 (LCDM plat Om = 0,30 en h-1 Mpc, vides spheriques, cordes sommees
     plafonnees a 1, segment [0 ; min(d_SN, portee catalogue)]).
  2. Bins de profondeur ; beta ajuste par bin (machinerie vraisemblance_reelle.py : E_acc,
     M marginalise, covariance pleine restreinte au sous-echantillon), SN SEULES comme #116,
     Om FIXE a 0,314. k_eff = -3w. Pente dk_eff/dDelta_v ; sigma par Delta_chi2 = 1 + bootstrap.
  3. VALIDATION DE LA MACHINERIE AVANT LECTURE (comme E1) : rejouer #116 (hemispheres du dipole
     CMB, apex RA = 167,9 Dec = -6,9). Attendu 553 / 1027 SNe (+/- 5) et Delta_beta a moins de
     0,10 de +0,22. Sinon E1-profondeur est rapporte mais ETIQUETE « machinerie non validee ».
  4. CONTROLE D'EQUITE (regle 2) et substitution DEFAVORABLE a l'horloge (regle 6), comme E1.

CRITERES.
  - SIGNAL = |dk_eff/dDelta_v| (ou |Delta_beta| profond-vs-peu-profond) > 2 sigma ET reproduit
    sur >= 2 catalogues independants ET N_profond >= 25 ; sinon UNIVERSEL, manche profondeur au
    goulet.
  - NON EXPLOITE si N_profond < 25, ou si les catalogues divergent entre eux > 2 sigma (regle 9),
    ou si la machinerie n'est pas validee (#116). Un controle sur deux echoue => rien exploite.
  - Verdict au format Adversaire ; verse dans l'affaire W-universel (Audience) au lancement.

Usage : etude_kappa_deltav.py spec | verdict <catalogue_vides.csv>
"""
import sys, pathlib


def spec():
    print(__doc__)
    print("[kappa-Delta_v] spec gelee. Aucune donnee ingeree : aucun verdict emis "
          "(regle 1 + regle 9).")


def verdict(p):
    if not pathlib.Path(p).exists():
        sys.exit(f"[kappa-Delta_v] {p} introuvable : le catalogue de vides n'est pas la. "
                 f"Aucun verdict sans donnees, et la machinerie #116 doit valider d'abord.")
    sys.exit("[kappa-Delta_v] execution du protocole gele NON IMPLEMENTEE dans la spec v0 : "
             "reutiliser la geometrie E1, trier par Delta_v, verifier N_profond >= 25, puis "
             "rapporter le gradient TEL QUEL. Rien ne se juge sans avoir tourne.")


if __name__ == "__main__":
    a = sys.argv[1:]
    {"spec": spec, "verdict": lambda: verdict(a[1])}.get(a[0] if a else "?",
                                                         lambda: sys.exit(__doc__))()
