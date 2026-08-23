"""ÉTUDES 2026 — les six specs, gelées ensemble (24/08/2026). Fichier .py pour que
registre fige ce docstring ; aucune étude ne commence sans que son critère soit déjà là.

E1 — VIDES × PANTHEON+ (duel goulet/horloge, manche 2)
  Données : VAST SDSS DR7 (Zenodo 7406035) + DESIVAST DR1 BGS + LocalVoids (CSV GitHub).
  Méthode : fraction de ligne de visée en vide par SN -> deux sous-échantillons -> profil β
  (machinerie du test des hémisphères, réutilisée telle quelle).
  CRITÈRES : signal = |Δβ| > 2σ ET reproduit sur ≥ 2 catalogues de vides indépendants ;
  sinon UNIVERSEL, manche 2 au goulet. NON EXPLOITÉ si les catalogues divergent entre eux
  > 2σ (le désaccord des juges n'est pas un verdict). Coût : 3-5 j. Verse dans l'affaire
  Audience W-universel.

E2 — CALIBRATION DOVEKIE (juge de la branche 1)
  Données : recalibrations open-source Dovekie (arXiv:2506.05471) appliquées à Pantheon+.
  CRITÈRES : le corpus tient si β recalibré reste dans [2,42 ; 2,60] ; ALERTE BRANCHE 1
  consignée si sortie > 2σ ; NON EXPLOITÉ si la chaîne Dovekie n'est pas reproductible
  localement (on ne juge pas sur un outil qu'on ne fait pas tourner). Coût : 1 semaine.

E3 — FRB SUR DONNÉES RÉELLES (papier C, montée de gamme)
  Données : table publique de sursauts localisés (N, z, DM_ex) la plus récente.
  CRITÈRES : validation d'abord — le refit ΛCDM doit redonner f_IGM publié à ±0,10, sinon
  rien n'est exploité ; puis Δχ²(CCBH) rapporté TEL QUEL, favorable ou non, et substitué
  aux mocks dans le papier avec mention explicite du changement. Coût : 3-5 j.

E4 — HÉMISPHÈRES SUR DESI DR2 (prédiction de la branche 3)
  Données : catalogues LSS publics DESI ; 13 points BAO scindés par moitié de ciel.
  CRITÈRES : signal = incompatibilité (w0,wa) ou β entre moitiés > 2σ ; DÉCLARÉ D'AVANCE :
  puissance faible (13 points), un nul n'est PAS une exclusion de la branche 3, seulement
  une absence de signal à cette précision. Coût : 2-3 j.

E5 — k-TRACKER : PREMIÈRE COMBINAISON RÉELLE
  Méthode : relire les 5 sources primaires (Gaia, NGC 3201, JWST AGN, Lacy, pulsars),
  passer chaque statut à "verifie" avec citation exacte + valeur + relecteur + date.
  CRITÈRES : le postérieur v1 n'est émis que si ≥ 4/5 vérifiées ; toute valeur reprise d'un
  résumé secondaire = statut refusé. Coût : 2-3 j. Verse dans l'affaire k3-vs-0.

E6 — CARTE DE REPRODUCTION (Galton-Watson / point fixe RG)
  Méthode : β_enfant = f(β_parent) via Fillmore-Goldreich sous l'ENCADREMENT ε (les deux
  lectures), |f'| au point fixe.
  CRITÈRES : verdict = CONTRACTANTE / DILATANTE seulement si les deux lectures concordent
  sur le régime ; sinon INDÉCISE, écrite comme telle (pas de moyenne des lectures). Coût :
  une après-midi. Seule ligne vivante du papier B.

ORDRE RECOMMANDÉ (coût croissant, valeur d'abord) : E6 -> E5 -> E1 -> E3 -> E4 -> E2.
Chaque étude, à son lancement : registre freeze de son script, inscription Audience si un
rival est en cause, verdict au format Adversaire. Rien ne se juge sans avoir tourné.
"""
