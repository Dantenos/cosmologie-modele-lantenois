#!/usr/bin/env sh
# Récupère les données publiques du corpus et vérifie les empreintes (donnees/SHA256SUMS).
# Idempotent : un fichier déjà présent n'est pas retéléchargé. Les catalogues de vides
# (petits) sont versionnés dans le dépôt ; seule la covariance Pantheon+ (33 Mo, GitHub)
# manque après un clone. Zenodo et le CDS ne sont contactés qu'en dernier recours.
set -e
cd "$(dirname "$0")"
P="https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR"
Z="https://zenodo.org/api/records/10160612/files"
B="https://cdsarc.cds.unistra.fr/ftp/J/ApJS/265/7"
mkdir -p pantheon_plus vides_stopyra2023 vides_douglass2023
get() {  # get <fichier local> <url> [gunzip]
  [ -s "$1" ] && return 0
  echo "[donnees] $1"
  if [ "$3" = "gunzip" ]; then
    curl -sfL --retry 6 --retry-all-errors --retry-delay 8 "$2" | gunzip > "$1"
  else
    curl -sfL --retry 6 --retry-all-errors --retry-delay 8 -o "$1" "$2"
  fi
}
# Pantheon+ (Scolnic et al. 2022 ; Brout et al. 2022)
get pantheon_plus/Pantheon+SH0ES.dat            "$P/Pantheon%2BSH0ES.dat"
get "pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov" "$P/Pantheon%2BSH0ES_STAT%2BSYS.cov"
# Anti-halos du super-volume local (Stopyra et al. 2023, Zenodo 10160612)
for f in README combined_catalogue.csv combined_catalogue_properties.csv; do
  get "vides_stopyra2023/$f" "$Z/$f/content"
done
# Vides SDSS DR7 (Douglass, Veyrat & BenZvi 2023, CDS J/ApJS/265/7 = VAST)
get vides_douglass2023/ReadMe     "$B/ReadMe"
get vides_douglass2023/table1.dat "$B/table1.dat"
get vides_douglass2023/table2.dat "$B/table2.dat.gz" gunzip
get vides_douglass2023/table3.dat "$B/table3.dat.gz" gunzip


# Vraisemblance Planck 2018 compressée (Prince & Dunkley) — planck_theta.py et jackknife_planck.py
# (le Δχ² = −12,6 « Planck complet » du papier A). Dépôt externe, cloné à côté des données.
if [ ! -f pantheon_plus/planck-lite-py/planck_lite_py.py ]; then
  echo "[donnees] planck-lite-py (git clone)"
  git clone -q --depth 1 https://github.com/heatherprince/planck-lite-py pantheon_plus/planck-lite-py
fi

sha256sum -c --ignore-missing --quiet SHA256SUMS && echo "[donnees] empreintes OK"
# noms attendus par scripts/vraisemblance_reelle.py (lus dans le CWD)
cp pantheon_plus/Pantheon+SH0ES.dat pantheon_plus/pantheon.dat
cp "pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov" pantheon_plus/pantheon_cov.cov
echo "[donnees] OK"
