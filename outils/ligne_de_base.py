#!/usr/bin/env python3
"""ligne_de_base v1 — la reproduction du corpus, en CI. CRITERES PRE-ENREGISTRES (geles).

Rejoue scripts/vraisemblance_reelle.py sur les donnees publiques (donnees/TELECHARGER.sh,
empreintes SHA256 verifiees) et compare aux ancres du corpus :
  - SNe retenues = 1580 exactement (zHD > 0,01, calibrateurs exclus) ;
  - beta(Accretion, SN + BAO) dans [2,42 ; 2,60] — la plage publiee du papier A ;
  - Delta_chi2(Accretion - LCDM) < 0 (le modele fait au moins aussi bien que LCDM).
Sortie : exit 0 si les trois tiennent, exit 1 sinon — build rouge : le corpus ne se
reproduit plus sur les donnees publiques, et rien d'autre n'a de sens tant que ce n'est
pas compris. Valeur de reference le 23/08/2026 : beta = 2,447, Delta_chi2 = -4,41.

Usage : python3 outils/ligne_de_base.py  (depuis la racine du depot)
"""
import sys, re, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "donnees" / "pantheon_plus"
for f in ("pantheon.dat", "pantheon_cov.cov"):
    if not (DATA / f).exists():
        sys.exit(f"[ligne_de_base] {f} absent : lancer sh donnees/TELECHARGER.sh")
r = subprocess.run([sys.executable, str(ROOT / "scripts" / "vraisemblance_reelle.py")],
                   cwd=DATA, capture_output=True, text=True, encoding="utf-8", timeout=1800)
print(r.stdout)
if r.returncode != 0:
    sys.exit(f"[ligne_de_base] vraisemblance_reelle.py : exit {r.returncode}\n{r.stderr}")
n = int(re.search(r"SNe retenues : (\d+)", r.stdout).group(1))
m = re.search(r"Accretion\s+Om=[\d.]+ beta=([\d.]+)\n.*?Dchi2=([+-][\d.]+)", r.stdout)
beta, dchi2 = float(m.group(1)), float(m.group(2))
ko = []
if n != 1580:               ko.append(f"SNe = {n} (attendu 1580)")
if not 2.42 <= beta <= 2.60: ko.append(f"beta = {beta} hors [2,42 ; 2,60]")
if dchi2 >= 0:              ko.append(f"Delta_chi2 = {dchi2:+} >= 0")
print(f"[ligne_de_base] SNe = {n}, beta = {beta}, Delta_chi2 = {dchi2:+}  -> "
      + ("REPRODUIT" if not ko else "ECHEC : " + " ; ".join(ko)))
sys.exit(1 if ko else 0)
