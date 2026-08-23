# RÉTRACTATIONS — le journal des amendements de critères gelés

Ce fichier est écrit par `outils/registre.py freeze --amend` : chaque fois qu'un critère
pré-enregistré (docstring d'un script gelé dans `outils/registre.lock`) est modifié **après**
son gel, l'ancien et le nouveau hash sont consignés ici, avec une justification obligatoire.
Sans justification, l'amendement est nul.

Les rétractations *scientifiques* (affirmations tombées, erreurs de calcul, fausses alertes)
vivent dans `registres/MANQUEMENTS.md` (numérotées) et `registres/TRIAGE_DES_ATTAQUES.md`.
Ici ne vit que la trace des critères eux-mêmes.

Au 23/08/2026 : **aucun critère gelé n'a été amendé.** Les 24 entrées du lock ont le hash de
leur premier gel. Les corrections de corps de script (chemins, encodage, bug d'argument par
défaut dans `duel_ccbh.py`) ne touchent pas aux docstrings et ne passent donc pas par ici ;
elles sont dans l'historique git et dans MANQUEMENTS #143.
