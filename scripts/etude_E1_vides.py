#!/usr/bin/env python3
"""E1 v0 — VIDES x PANTHEON+ : duel goulet/horloge, manche 2. CRITERES PRE-ENREGISTRES
(geles par registre AVANT la premiere execution, 23/08/2026). Spec mere : etudes_2026.py (gelee).

QUESTION. L'horloge predit que les SNe vues a travers plus de vides donnent un w plus negatif,
donc un beta plus grand (w = -beta/(3Ht)) : Delta_beta = beta_vides - beta_murs > 0. Le goulet
predit l'universalite stricte : Delta_beta = 0.

DONNEES (empreintes dans donnees/SHA256SUMS).
  - Pantheon+SH0ES.dat + STAT+SYS.cov (GitHub PantheonPlusSH0ES/DataRelease). Coupures
    IDENTIQUES au corpus : zHD > 0,01, calibrateurs exclus -> 1580 SNe. Positions RA/DEC.
  - Catalogue d'anti-halos Stopyra et al. 2023, Zenodo 10160612, combined_catalogue_properties
    .csv : 150 vides, R > 10 h-1 Mpc, a moins de 135 h-1 Mpc (z < 0,045). Tous retenus.
  LIMITE DECLAREE : un seul catalogue est disponible ici (SDSS DR7 Douglass au CDS et
  Malandrino 2026 non recuperes). La spec mere exige >= 2 catalogues independants pour un
  signal. DONC LE VERDICT v0 NE PEUT PAS ETRE "SIGNAL" : au mieux CANDIDAT.
  LIMITE DECLAREE : le catalogue s'arrete a 135 h-1 Mpc ; pour les SNe plus lointaines, la
  fraction de vide ne caracterise que le segment local de la ligne de visee.

METHODE (rien ici ne sera ajuste apres avoir vu Delta_beta).
  1. Geometrie : distance comobile LCDM plat Om = 0,30 en h-1 Mpc ; vides = spheres
     (RA, Dec, distance, rayon) du catalogue ; f = longueur de la ligne de visee dans les
     vides / longueur du segment [0 ; min(d_SN, 135)] (chords sommees, plafonnees a 1).
  2. Partage : a la MEDIANE de f (vides : f >= med ; murs : f < med). Si la mediane vaut 0,
     partage f > 0 / f = 0.
  3. Ajustement : machinerie de vraisemblance_reelle.py (E_acc, M marginalise analytiquement,
     covariance pleine restreinte au sous-echantillon), SN SEULES comme en #116, Om FIXE a
     0,314 (meilleur ajustement joint SN+BAO de la ligne de base rejouee ce jour : beta =
     2,447). sigma(beta) par Delta_chi2 = 1 sur le profil. sigma_Delta = sqrt(s1^2 + s2^2).
  4. VALIDATION DE LA MACHINERIE, AVANT LECTURE D'E1 : rejouer #116 (hemispheres du dipole
     CMB, apex RA = 167,9 Dec = -6,9). Attendu : 553 / 1027 SNe (+/- 5) et Delta_beta a
     moins de 0,10 de +0,22. Sinon, E1 est rapporte mais ETIQUETE "machinerie non validee".
  5. CONTROLE D'EQUITE (regle 2, systematique d'empreinte au ciel non traitee en #116) :
     200 rotations aleatoires rigides du catalogue de vides (graine 20260823), meme
     pipeline -> distribution nulle de Delta_beta -> sigma_rot et p-valeur empirique
     bilaterale.

CRITERES (exhaustifs, exclusifs).
  - NON EXPLOITE si : beta(1580 SNe, Om fixe) sort de [2,2 ; 2,8] (la machinerie SN-seule
    ne retrouve pas le corpus) ; OU un sous-echantillon compte < 200 SNe ; OU sigma_rot >
    2 x sigma_Delta (les rotations revelent une systematique que la covariance ignore :
    le desaccord des juges n'est pas un verdict).
  - CANDIDAT si : |Delta_beta| > 2 sigma_Delta ET p_rot < 0,05. Pas un signal : en attente
    du deuxieme catalogue (spec mere). Le SIGNE est rapporte mais n'est pas interprete.
  - UNIVERSEL (a cette precision) sinon : manche 2 au goulet, comme la manche 1. Ce que
    cela REDUIT : l'amplitude d'un effet d'environnement sur beta, a sigma_Delta pres. Ce
    que cela ne ferme PAS : un effet plus fin, ou porte par des vides au-dela de 135 h-1 Mpc.
  Verse dans l'affaire Audience W-universel. Valeurs de substitution : aucune.

Usage : python3 scripts/etude_E1_vides.py  (depuis la racine du depot)
"""
import sys, os, pathlib, csv
import numpy as np
from scipy.optimize import minimize_scalar, brentq

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "donnees" / "pantheon_plus"
VIDES = ROOT / "donnees" / "vides_stopyra2023" / "combined_catalogue_properties.csv"

# ---------- machinerie du corpus, reutilisee telle quelle ----------
os.chdir(DATA)                       # vraisemblance_reelle lit pantheon.dat dans le CWD
sys.path.insert(0, str(ROOT / "scripts"))
import vraisemblance_reelle as VR    # charge les 1580 SNe, construit C_sn, definit E_acc
os.chdir(ROOT)

OM_FIXE  = 0.314
D_CAT    = 135.0                     # h-1 Mpc, profondeur du catalogue
C_SUR_H0 = 2997.92458                # h-1 Mpc
N_ROT    = 200
GRAINE   = 20260823

raw  = VR.raw; mask = VR.mask
ra   = np.radians(raw['RA'][mask]); dec = np.radians(raw['DEC'][mask])
z_sn = VR.z_sn; mb = VR.mb; C_sn = VR.C_sn
n_hat = np.stack([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)], axis=1)

# distance comobile LCDM plat Om=0,30, en h-1 Mpc
_zg = np.linspace(0, 3, 6000)
_E  = np.sqrt(0.30*(1+_zg)**3 + 0.70)
_Dc = C_SUR_H0*np.concatenate([[0], np.cumsum(0.5*(1/_E[1:]+1/_E[:-1])*np.diff(_zg))])
d_sn = np.interp(z_sn, _zg, _Dc)

# ---------- catalogue de vides ----------
def charge_vides():
    rows = list(csv.reader(VIDES.open(encoding="utf-8")))
    V = np.array([[float(x) for x in r[:9]] for r in rows[1:] if r and r[0].strip()])
    R = V[:,1]; vra = np.radians(V[:,5]); vdec = np.radians(V[:,6]); dist = V[:,8]
    centres = dist[:,None]*np.stack([np.cos(vdec)*np.cos(vra), np.cos(vdec)*np.sin(vra),
                                     np.sin(vdec)], axis=1)
    return centres, R

def fraction_vide(centres, R):
    """f_i = longueur de [0, L_i] n_i dans l'union (sommee, plafonnee) des spheres."""
    L = np.minimum(d_sn, D_CAT)
    tc = n_hat @ centres.T                                  # (Nsn, Nv) projection du centre
    b2 = (centres**2).sum(1)[None,:] - tc**2                # distance^2 perpendiculaire
    disc = R[None,:]**2 - b2
    h = np.sqrt(np.clip(disc, 0, None))
    t0 = np.clip(tc - h, 0, L[:,None]); t1 = np.clip(tc + h, 0, L[:,None])
    chord = np.where(disc > 0, t1 - t0, 0.0).sum(1)
    return np.minimum(chord/L, 1.0)

# ---------- ajustement beta, SN seules, Om fixe ----------
def _prep(idx):
    C = C_sn[np.ix_(idx, idx)]; Ci = np.linalg.inv(C)
    one = np.ones(len(idx)); Cio = Ci@one
    return Ci, Cio, one@Cio

def chi2_sn(beta, idx, prep):
    Ci, Cio, oCo = prep
    Ez = VR.E_acc(VR.zg, OM_FIXE, beta); inv = 1/Ez
    Dc = np.concatenate([[0], np.cumsum(0.5*(inv[1:]+inv[:-1])*np.diff(VR.zg))])
    mu = 5*np.log10((1+z_sn[idx])*np.interp(z_sn[idx], VR.zg, Dc))
    r = mb[idx] - mu
    A = r@Ci@r; B = r@Cio
    return A - B*B/oCo

def fit_beta(idx, sigma=True):
    prep = _prep(idx)
    f = lambda b: chi2_sn(b, idx, prep)
    res = minimize_scalar(f, bounds=(0.5, 6.0), method='bounded', options=dict(xatol=1e-3))
    b0, c0 = res.x, res.fun
    if not sigma: return b0, None
    g = lambda b: f(b) - c0 - 1.0
    try:    hi = brentq(g, b0, b0 + 3.0, xtol=1e-3)
    except ValueError: hi = b0 + 3.0
    try:    lo = brentq(g, max(b0 - 3.0, 0.5), b0, xtol=1e-3)
    except ValueError: lo = max(b0 - 3.0, 0.5)
    return b0, 0.5*(hi - lo)

def delta_beta(sel, sigma=True):
    iv = np.where(sel)[0]; im = np.where(~sel)[0]
    bv, sv = fit_beta(iv, sigma); bm, sm = fit_beta(im, sigma)
    s = np.hypot(sv, sm) if sigma else None
    return bv, sv, bm, sm, bv - bm, s, len(iv), len(im)

def rotation_aleatoire(rng):
    q = rng.normal(size=4); q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                     [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])

# ---------- execution ----------
if __name__ == "__main__":
    print("E1 v0 — vides x Pantheon+ (criteres geles, voir docstring)\n")
    non_exploite = []

    # 0. la machinerie SN-seule retrouve-t-elle le corpus ?
    b_tot, s_tot = fit_beta(np.arange(len(z_sn)))
    print(f"[0] beta(1580 SNe, Om={OM_FIXE}) = {b_tot:.3f} +/- {s_tot:.3f}")
    if not (2.2 <= b_tot <= 2.8): non_exploite.append("beta total hors [2,2 ; 2,8]")

    # 4. validation : rejouer #116
    apex = np.radians([167.9, -6.9])
    a_hat = np.array([np.cos(apex[1])*np.cos(apex[0]), np.cos(apex[1])*np.sin(apex[0]), np.sin(apex[1])])
    hemi = (n_hat @ a_hat) > 0
    bv, sv, bm, sm, dB, sD, nv, nm = delta_beta(hemi)
    print(f"[4] #116 rejoue : apex {nv} SNe beta={bv:.2f}+/-{sv:.2f} | anti {nm} SNe "
          f"beta={bm:.2f}+/-{sm:.2f} | Delta_beta = {dB:+.2f} +/- {sD:.2f}")
    machinerie_ok = abs(nv - 553) <= 5 and abs(dB - 0.22) < 0.10
    print(f"    attendu 553/1027, +0,22+/-0,23 -> machinerie {'VALIDEE' if machinerie_ok else 'NON VALIDEE'}\n")

    # 1-2. fraction de vide et partage
    centres, R = charge_vides()
    print(f"[1] {len(R)} vides, R = {R.min():.0f}-{R.max():.0f} h-1 Mpc, d <= {np.linalg.norm(centres,axis=1).max():.0f}")
    f = fraction_vide(centres, R)
    med = np.median(f)
    sel = (f >= med) if med > 0 else (f > 0)
    print(f"    f : mediane={med:.3f} moyenne={f.mean():.3f} f>0 pour {(f>0).sum()} SNe ; "
          f"partage {'a la mediane' if med > 0 else 'f>0 / f=0'}")

    # 3. Delta_beta
    bv, sv, bm, sm, dB, sD, nv, nm = delta_beta(sel)
    print(f"[3] vides {nv} SNe : beta = {bv:.3f} +/- {sv:.3f}")
    print(f"    murs  {nm} SNe : beta = {bm:.3f} +/- {sm:.3f}")
    print(f"    Delta_beta = {dB:+.3f} +/- {sD:.3f}  ({abs(dB)/sD:.2f} sigma)")
    if min(nv, nm) < 200: non_exploite.append(f"sous-echantillon < 200 SNe ({nv}/{nm})")

    # 5. controle d'equite : rotations du catalogue
    rng = np.random.default_rng(GRAINE)
    nulls = []
    for k in range(N_ROT):
        fk = fraction_vide(centres @ rotation_aleatoire(rng).T, R)
        mk = np.median(fk); sk = (fk >= mk) if mk > 0 else (fk > 0)
        if min(sk.sum(), (~sk).sum()) < 50: continue
        nulls.append(delta_beta(sk, sigma=False)[4])
        if (k+1) % 50 == 0: print(f"    rotations {k+1}/{N_ROT}", flush=True)
    nulls = np.array(nulls)
    s_rot = nulls.std(ddof=1)
    p_rot = (np.abs(nulls) >= abs(dB)).mean()
    print(f"[5] {len(nulls)} rotations : <Delta_beta> = {nulls.mean():+.3f}, sigma_rot = {s_rot:.3f}, "
          f"p(|null| >= |obs|) = {p_rot:.3f}")
    if s_rot > 2*sD: non_exploite.append(f"sigma_rot {s_rot:.2f} > 2 sigma_Delta {sD:.2f}")

    # verdict
    print("\n" + "="*72)
    if non_exploite:
        verdict = "NON EXPLOITE — " + " ; ".join(non_exploite)
    elif abs(dB) > 2*sD and p_rot < 0.05:
        verdict = "CANDIDAT (pas un signal : un seul catalogue) — signe non interprete"
    else:
        verdict = "UNIVERSEL a cette precision — manche 2 au goulet"
    print(f"VERDICT E1 v0 : {verdict}")
    if not machinerie_ok: print("ETIQUETTE : machinerie non validee sur #116")
    print(f"Ce que cela reduit : |Delta_beta| < {2*sD:.2f} (2 sigma) sur 1 catalogue, d < 135 h-1 Mpc.")
    print("="*72)
