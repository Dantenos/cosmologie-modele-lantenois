# Registre

**La falsification-as-code.** *Pre-commit pour les conclusions, pas seulement pour le code.*

> Un résultat n'est opposable que si son critère de succès a été gelé **avant** l'exécution.
> `registre` fige les critères par hash, vérifie qu'ils n'ont pas bougé après coup, et rend
> toute rétractation possible — mais publique.

---

## Démo en 30 secondes

```console
$ python3 outils/registre.py freeze scripts/voile_cisaillement.py scripts/frb_strategie.py outils/registre.py
[registre] gelé : scripts/voile_cisaillement.py  (11b036bf3483)
[registre] gelé : scripts/frb_strategie.py       (74ee54c0c0a6)
[registre] gelé : outils/registre.py            (10787c914430)   # il se gèle lui-même

$ python3 outils/registre.py verify
[registre] OK    scripts/voile_cisaillement.py
[registre] OK    scripts/frb_strategie.py
[registre] OK    outils/registre.py      # exit 0   (88 fichiers gelés au 24/08/2026)

$ sed -i 's/O(0,1-1)/O(0,01-10)/' scripts/voile_cisaillement.py   # on élargit un critère... après coup
$ python3 outils/registre.py verify scripts/voile_cisaillement.py
[registre] ÉCHEC scripts/voile_cisaillement.py  <- critère modifié APRÈS gel
# exit 1 — bloquant en CI
```

Sortie réelle, non éditée : le premier objet protégé par Registre est le corpus scientifique
qui l'a engendré — et Registre se protège lui-même.

## Pourquoi ça existe

Cet outil est né d'une campagne réelle de neuf jours en cosmologie (août 2026) : un modèle
d'énergie noire audité contre Pantheon+, DESI DR2 et Planck, avec un registre adversarial tenu
à la main — **116 entrées à la naissance de l'outil, 142 au 23/08/2026, dont 54 affirmations rétractées, la plupart produites par l'IA qui
assistait l'analyse**. Le motif mesuré : les erreurs allaient dans le sens de la thèse défendue,
et *aucune relecture ne les attrapait*. Ce qui les attrapait : des critères écrits avant le
calcul, et des garde-fous automatiques.

Le même problème existe dans toute équipe data : des seuils qui bougent après avoir vu les
résultats, des dashboards dont personne ne sait si la définition du succès a changé en route.
Les tests protègent le code. Rien ne protège les conclusions. Registre fait ça.

## Principe

1. **Le critère vit dans le docstring** du script d'analyse (« ce résultat est valide si… /
   n'est pas exploité si… »).
2. `freeze` le fige par SHA-256 dans `registre.lock`, avec horodatage.
3. `verify` échoue (exit 1) si le critère a été modifié après gel → **bloquant en CI**.
4. `freeze --amend` autorise l'amendement — en l'écrivant obligatoirement dans
   `RETRACTATIONS.md`. On ne peut pas tricher en silence ; on peut se corriger en public.

## Installation & usage

Zéro dépendance. Python ≥ 3.9.

```console
$ python3 outils/registre.py freeze scripts/mon_analyse.py   # avant d'exécuter l'analyse
$ python3 outils/registre.py verify                 # à tout moment, et en CI
$ python3 outils/registre.py log                    # état du gel
$ python3 outils/registre.py freeze --amend f.py    # amendement public
```

## Intégration CI (GitHub Actions)

```yaml
# .github/workflows/registre.yml
on: [push, pull_request]
jobs:
  criteres:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 outils/registre.py verify   # exit 1 = conclusion inopposable = build rouge
```

## Les règles dont il est fait

Héritées de la campagne, payées au prix de cinquante-quatre rétractations :

- Critères pré-enregistrés **avant** exécution, toujours.
- Tout écart > 3σ exige un contrôle d'équité (recalculer avec les valeurs de l'adversaire).
- Annoncer ce qu'un calcul **réduit**, jamais ce qu'il ferme.
- Valeur de substitution inventée = dans le sens **défavorable** à sa propre thèse.
- Jamais convertir l'ambigu en victoire : un contrôle sur deux échoué ⇒ rien n'est exploité.

## Feuille de route

- **v0** (ici) : freeze / verify / amend, CLI, zéro dépendance — validé sur corpus réel.
- v0.2 : bloc de critères structuré (YAML dans le docstring), `registre run` qui exécute et
  confronte la sortie aux seuils gelés, rapport HTML.
- v0.3 : hook pre-commit, badge de statut, multi-langages (R, notebooks).

## Provenance

Conçu et amorcé le 24 août 2026, en clôture de la campagne cosmologie
([corpus complet : papiers, scripts, MANQUEMENTS.md, TRIAGE_DES_ATTAQUES.md](./)).
Auteur : Édouard Lantenois — [@Dantenos](https://github.com/Dantenos) ·
[linkedin.com/in/edlanteno](https://linkedin.com/in/edlanteno)

*« Les tests empêchent le code de mentir. Registre empêche l'analyste. »*
