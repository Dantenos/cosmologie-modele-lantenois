#!/usr/bin/env python3
"""genere_ciel v1 — generateur de visuels/ciel_pantheon_v2.html (23/08/2026).
CRITERES PRE-ENREGISTRES (geles) : le fichier n'est ECRIT que si les comptes verifient
exactement les registres — 1580 SNe (dont 553 dans l'hemisphere du dipole, #116/#141),
623 SNe avec un vide de Stopyra sur la ligne de visee (E1, #141), 150 vides, 69 FRB
(Connor 2025, #148). Sinon : REFUS, aucun HTML emis. Zero dependance reseau dans la
sortie ; tous les chiffres affiches viennent des rejeux consignes (#141, #142, #148).
Usage : python3 outils/genere_ciel.py
"""
import sys, csv, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E   # charge Pantheon+ (1580), n_hat, fraction_vide, charge_vides

def flat(a, nd=3):
    return "[" + ",".join(f"{v:.{nd}f}".rstrip("0").rstrip(".") for v in a) + "]"

def main():
    # SNe : vecteurs unitaires + drapeaux (hemisphere du dipole ; vide Stopyra sur la ligne de visee)
    apex = np.radians([167.9, -6.9])
    a_hat = np.array([np.cos(apex[1])*np.cos(apex[0]), np.cos(apex[1])*np.sin(apex[0]), np.sin(apex[1])])
    hemi = (E.n_hat @ a_hat) > 0
    centres, R = E.charge_vides()
    f = E.fraction_vide(centres, R)
    vide = f > 0
    n_sn, n_h, n_v = len(E.z_sn), int(hemi.sum()), int(vide.sum())
    # vides : vecteurs unitaires + rayon angulaire
    dist = np.linalg.norm(centres, axis=1); u = centres / dist[:, None]
    angr = np.arcsin(np.clip(R / dist, 0, 1))
    # FRB
    rows = list(csv.DictReader((ROOT / "donnees/frb_connor2025/frbsample_connor0924.csv").open(encoding="utf-8")))
    fra = np.radians([float(r["ra"]) for r in rows]); frd = np.radians([float(r["dec"]) for r in rows])
    dm = np.array([float(r["dm_exgal"]) for r in rows])
    fu = np.stack([np.cos(frd)*np.cos(fra), np.cos(frd)*np.sin(fra), np.sin(frd)], 1)
    dms = 0.25 + 0.75*(dm - dm.min())/(dm.max() - dm.min())
    if not (n_sn == 1580 and n_h == 553 and n_v == 623 and len(R) == 150 and len(rows) == 69):
        sys.exit(f"[ciel] REFUS : comptes {n_sn}/{n_h}/{n_v}/{len(R)}/{len(rows)} != 1580/553/623/150/69")
    P = flat(np.column_stack([E.n_hat, hemi*2 + vide]).ravel())
    V = flat(np.column_stack([u, angr]).ravel())
    F = flat(np.column_stack([fu, dms]).ravel())
    tpl = (ROOT / "outils" / "ciel_v2_template.html").read_text(encoding="utf-8")
    out = tpl.replace("__P__", P).replace("__V__", V).replace("__F__", F)
    dest = ROOT / "visuels" / "ciel_pantheon_v2.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"[ciel] ecrit : {dest.name} ({dest.stat().st_size//1024} ko) — comptes verifies 1580/553/623/150/69")

if __name__ == "__main__":
    main()
