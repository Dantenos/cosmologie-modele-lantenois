#!/usr/bin/env sh
# Récupère les données publiques d'E1 et vérifie les empreintes (donnees/SHA256SUMS).
set -e
cd "$(dirname "$0")"
P="https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR"
Z="https://zenodo.org/api/records/10160612/files"
mkdir -p pantheon_plus vides_stopyra2023
curl -sL -o pantheon_plus/Pantheon+SH0ES.dat "$P/Pantheon%2BSH0ES.dat"
curl -sL -o "pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov" "$P/Pantheon%2BSH0ES_STAT%2BSYS.cov"
for f in README combined_catalogue.csv combined_catalogue_properties.csv combined_catalogue_unfiltered.csv; do
  curl -sL -o "vides_stopyra2023/$f" "$Z/$f/content"
done
sha256sum -c SHA256SUMS
# noms attendus par vraisemblance_reelle.py
cp pantheon_plus/Pantheon+SH0ES.dat pantheon_plus/pantheon.dat
cp "pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov" pantheon_plus/pantheon_cov.cov
