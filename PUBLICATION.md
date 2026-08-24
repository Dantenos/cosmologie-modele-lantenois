# Publier le dépôt et le sceau — procédure

**Objectif :** que le sceau `68d06bcc…` soit **opposable à un sceptique en 2027**, c'est-à-dire
qu'un tiers puisse vérifier tout seul que l'analyse n'a pas bougé après l'arrivée de DESI DR3.

Un dépôt GitHub seul ne suffit pas : les dates de commit git sont **falsifiables** (`git commit
--date=…` accepte n'importe quoi). Il faut un horodatage que tu ne contrôles pas. D'où les deux
étapes.

---

## 1. Le dépôt sur GitHub

```bash
cd D:/COSMOLOGIE_Model_Lantenois
git remote add origin https://github.com/Dantenos/<nom-du-depot>.git
git push -u origin main
```

**Avant de pousser, trois vérifications :**

```bash
git status --porcelain          # doit être vide
python outils/registre.py verify   # 89 critères, 0 échec
python outils/perime.py            # 0 occurrence
```

Le `.gitignore` exclut déjà la covariance Pantheon+ (33 Mo), les états MCMC intermédiaires et
les produits de compilation LaTeX. Les PDF des papiers sont versionnés **volontairement** :
ils sont l'objet publié.

---

## 2. Le DOI Zenodo — c'est lui qui donne la force probante

Zenodo horodate le dépôt à une date que **tu ne contrôles pas**, et lui attribue un DOI
citable. C'est exactement ce que font les préenregistrements de cosmologie que la vérification
littérature a trouvés (dépôts SHA-256 + attestation, 2026).

1. Aller sur <https://zenodo.org>, se connecter **avec le compte GitHub**.
2. Menu *GitHub* → activer le dépôt (l'interrupteur passe à **ON**).
3. Sur GitHub : *Releases* → *Create a new release* → tag `v1.0-sceau`.
4. Zenodo capture automatiquement l'archive et émet un DOI.
5. **Reporter ce DOI dans le papier A**, section données, à côté du sceau.

> Le DOI « concept » (sans version) pointe toujours vers la dernière version ; le DOI
> **versionné** pointe vers l'archive figée. **C'est le versionné qu'il faut citer** à côté du
> sceau : c'est lui qui prouve l'antériorité.

---

## 3. Le sceau lui-même

```
sha256(outils/scelle.py) = 68d06bcccbecf2276919c05dc841c6d878ca2516427e533af38d64344aed45a2
```

**Ce qu'il couvre** — verdicts exhaustifs et exclusifs, seuils non modifiables :

| verdict | condition |
|---|---|
| **VALIDÉE** | β(DR3) ∈ [2,42 ; 2,60] à 1σ **ET** \|κ\| < 0,24 maintenu |
| **RÉFUTÉE** | β(DR3) exclut [2,42 ; 2,60] à >3σ, **OU** ΔAIC > +6 contre ΛCDM, **OU** β₁ exclut +0,06±0,31 à >3σ |
| **INDÉCISE** | sinon — et *indécise n'est pas validée* |

**Où le publier :** dans le résumé ou la section données du papier A, dans le README du dépôt,
et dans le texte de la release Zenodo. Un hash qui ne circule pas ne prouve rien : il faut
qu'il soit **antérieur et public**.

### Renforcement optionnel : OpenTimestamps

Ancre le hash dans la chaîne Bitcoin — gratuit, et l'horodatage devient infalsifiable
indépendamment de Zenodo.

```bash
pip install opentimestamps-client
ots stamp outils/scelle.py        # produit outils/scelle.py.ots
git add outils/scelle.py.ots && git commit -m "Horodatage OpenTimestamps du scelle"
```

L'attestation Bitcoin se complète en quelques heures. `ots verify outils/scelle.py.ots`
vérifie ensuite la date sans faire confiance à personne — ni à toi, ni à Zenodo, ni à GitHub.

---

## 4. Ce qui reste à faire avant de dire « publié »

| tâche | état | bloquant ? |
|---|---|---|
| Dépôt propre, garde-fous verts | **fait** | — |
| Remote GitHub configuré | **à faire** (aucun remote) | oui |
| DOI Zenodo | à faire après le push | oui pour le sceau |
| Endossement arXiv (astro-ph.CO) | à faire | **oui pour arXiv** |
| Papier F, édition française | à faire | non |
| Papiers A/B/C, éditions françaises | non entamé | non |
| Convention θ\* / θ_MC (#195) | mesurée, non corrigée | **à décider avant soumission** |
| Lecture « référent » (#193) | non établie, arrêt déclaré | non — c'est un statut, pas une dette |

**Le point qui mérite une décision, pas un oubli :** le décalage de convention −0,54σ sur
`l_A` (#195) est présent dans chaque évaluation de la vraisemblance. Il est *déclaré* dans la
section « ce que nous ne revendiquons pas » du papier D. Le corriger déplacerait tous les
nombres de la campagne. Le laisser déclaré est défendable ; le laisser **non déclaré** ne le
serait pas. C'est fait — mais il faut le savoir avant qu'un référé le trouve.
