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
import sys, csv, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E1_vides as E1   # machinerie E1 GELEE et validee, reutilisee telle quelle
                             # (chargement 1580 SNe, geometrie, fit_beta, delta_beta, rotations)

VIDES = ROOT / "donnees" / "vides_stopyra2023" / "combined_catalogue_properties.csv"
SEUIL_PCT     = 25    # seuil de profondeur = quartile le plus creux du catalogue (spec gelee)
N_MIN_PROFOND = 25    # exigence de puissance pre-enregistree (le « >= 25 » de la file d'attente)


def charge_vides_profondeur():
    """centres, rayons ET profondeur Delta_v (Central Density Contrast, colonne 11)."""
    rows = [r for r in csv.reader(VIDES.open(encoding="utf-8")) if r and r[0].strip()][1:]
    R    = np.array([float(r[1]) for r in rows])
    vra  = np.radians([float(r[5]) for r in rows])
    vdec = np.radians([float(r[6]) for r in rows])
    dist = np.array([float(r[8]) for r in rows])
    dv   = np.array([float(r[11]) for r in rows])         # Central Density Contrast = Delta_v
    centres = dist[:, None] * np.stack([np.cos(vdec)*np.cos(vra),
                                        np.cos(vdec)*np.sin(vra), np.sin(vdec)], axis=1)
    return centres, R, dv


def profondeur_par_sn(centres, R, dv):
    """Delta_v_i = densite-contraste la plus creuse (min) parmi les vides que la ligne de visee
    [0, L_i] traverse REELLEMENT (corde > 0) ; 0 si aucun vide traverse. Meme geometrie qu'E1."""
    L  = np.minimum(E1.d_sn, E1.D_CAT)
    tc = E1.n_hat @ centres.T
    disc = R[None, :]**2 - ((centres**2).sum(1)[None, :] - tc**2)
    h  = np.sqrt(np.clip(disc, 0, None))
    t0 = np.clip(tc - h, 0, L[:, None]); t1 = np.clip(tc + h, 0, L[:, None])
    traverse = (disc > 0) & ((t1 - t0) > 0)               # (Nsn, Nv)
    m = np.where(traverse, dv[None, :], np.inf).min(axis=1)
    return np.where(np.isfinite(m), m, 0.0)


def main():
    print("kappa-Delta_v v1 — extension PROFONDEUR de E1 (criteres geles, voir docstring)\n")
    non_exploite = []

    # [0] la machinerie SN-seule retrouve-t-elle le corpus ?
    b_tot, s_tot = E1.fit_beta(np.arange(len(E1.z_sn)))
    print(f"[0] beta(1580 SNe, Om={E1.OM_FIXE}) = {b_tot:.3f} +/- {s_tot:.3f}")
    if not (2.2 <= b_tot <= 2.8):
        non_exploite.append("beta total hors [2,2 ; 2,8] (machinerie ne retrouve pas le corpus)")

    # [4] VALIDATION machinerie AVANT lecture : #116 hemispheres du dipole CMB (identique a E1)
    apex = np.radians([167.9, -6.9])
    a_hat = np.array([np.cos(apex[1])*np.cos(apex[0]), np.cos(apex[1])*np.sin(apex[0]), np.sin(apex[1])])
    _, _, _, _, dB116, sD116, nv116, _ = E1.delta_beta((E1.n_hat @ a_hat) > 0)
    machinerie_ok = abs(nv116 - 553) <= 5 and abs(dB116 - 0.22) < 0.10
    print(f"[4] #116 rejoue : {nv116} SNe apex, Delta_beta = {dB116:+.2f} +/- {sD116:.2f} "
          f"-> machinerie {'VALIDEE' if machinerie_ok else 'NON VALIDEE'}")
    if not machinerie_ok:
        non_exploite.append("machinerie non validee sur #116")

    # [1-2] profondeur par SN + seuil au quartile le plus creux du catalogue
    centres, R, dv = charge_vides_profondeur()
    prof  = profondeur_par_sn(centres, R, dv)
    seuil = np.percentile(dv, SEUIL_PCT)
    sel   = prof <= seuil                                  # bin de vide PROFOND
    n_prof = int(sel.sum())
    print(f"\n[1] {len(R)} vides ; Delta_v (central) de {dv.min():.2f} a {dv.max():.2f} ; "
          f"seuil P{SEUIL_PCT} = {seuil:.3f}")
    print(f"[2] {(prof < 0).sum()} SNe traversent >= 1 vide ; bin PROFOND (Delta_v <= {seuil:.3f}) "
          f"= {n_prof} SNe")
    if n_prof < N_MIN_PROFOND:
        non_exploite.append(f"N_profond = {n_prof} < {N_MIN_PROFOND} (puissance insuffisante, "
                            f"declaree d'avance : un nul n'est pas une exclusion)")

    # [3] Delta_beta profond vs reste, rapporte TEL QUEL (k_eff = -3w, lineaire en beta)
    bv, sv, bm, sm, dB, sD, nv, nm = E1.delta_beta(sel)
    print(f"\n[3] PROFOND {nv} SNe : beta = {bv:.3f} +/- {sv:.3f}")
    print(f"    RESTE   {nm} SNe : beta = {bm:.3f} +/- {sm:.3f}")
    print(f"    Delta_beta = {dB:+.3f} +/- {sD:.3f}  ({abs(dB)/sD:.2f} sigma)  "
          f"[Delta k_eff ~ {-3*(bv-bm)/3:+.3f} en convention w=-beta/(3Ht)]")

    # [5] CONTROLE D'EQUITE (regle 2) : rotations rigides du catalogue -> distribution nulle
    rng = np.random.default_rng(E1.GRAINE)
    nulls = []
    for k in range(E1.N_ROT):
        pk = profondeur_par_sn(centres @ E1.rotation_aleatoire(rng).T, R, dv)
        sk = pk <= seuil
        if min(sk.sum(), (~sk).sum()) < 50:
            continue
        nulls.append(E1.delta_beta(sk, sigma=False)[4])
        if (k + 1) % 50 == 0:
            print(f"    rotations {k+1}/{E1.N_ROT}", flush=True)
    nulls = np.array(nulls)
    s_rot = nulls.std(ddof=1) if len(nulls) > 1 else float("inf")
    p_rot = (np.abs(nulls) >= abs(dB)).mean() if len(nulls) else 1.0
    print(f"[5] {len(nulls)} rotations : <Delta_beta> = {nulls.mean():+.3f}, sigma_rot = {s_rot:.3f}, "
          f"p(|null| >= |obs|) = {p_rot:.3f}")
    if s_rot > 2 * sD:
        non_exploite.append(f"sigma_rot {s_rot:.2f} > 2 sigma_Delta {sD:.2f} (systematique de ciel)")

    # ---------- verdict (criteres geles ; un seul catalogue -> SIGNAL impossible, spec mere) ----------
    print("\n" + "=" * 72)
    if non_exploite:
        verdict = "NON EXPLOITE — " + " ; ".join(non_exploite)
    elif abs(dB) > 2 * sD and p_rot < 0.05:
        verdict = ("EXCES A 1 CATALOGUE (candidat) — PAS un SIGNAL : la spec mere exige >= 2 "
                   "catalogues independants. Signe rapporte, non interprete ; 2e juge (DESIVAST/"
                   "Douglass) requis.")
    else:
        verdict = "UNIVERSEL a cette precision — manche PROFONDEUR au goulet (comme la manche fraction, E1)"
    print(f"VERDICT kappa-Delta_v v1 : {verdict}")
    print(f"Ce que cela REDUIT : |Delta_beta(profond vs reste)| < {2*sD:.2f} (2 sigma) sur 1 catalogue, "
          f"d < {E1.D_CAT:.0f} h-1 Mpc. Ce que cela ne FERME pas : un gradient plus fin, ou porte "
          f"par des vides plus profonds/lointains.")
    print("=" * 72)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "spec":
        print(__doc__)
    else:
        main()
