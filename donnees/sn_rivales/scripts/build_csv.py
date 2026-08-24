# -*- coding: utf-8 -*-
"""Construit les CSV lisibles pour DES-SN5YR (tag 1.3) et Union3, et verifie les tables.
Aucune cosmologie n'est calculee : uniquement lecture, conversion, verification."""
import gzip, csv, shutil
import numpy as np
from astropy.io import fits

BASE = r"D:/COSMOLOGIE_Model_Lantenois/donnees/sn_rivales"
DES = BASE + "/DES-SN5YR"
U3  = BASE + "/Union3"

# ---------------- DES-SN5YR ----------------
with open(DES + "/raw/DES-SN5YR_HD.csv", newline="", encoding="utf-8") as f:
    hd = list(csv.DictReader(f))
n_hd = len(hd)
zhd = np.array([float(r["zHD"]) for r in hd])
mu_des = np.array([float(r["MU"]) for r in hd])
ids = [r["IDSURVEY"] for r in hd]
from collections import Counter
print(f"[DES] HD: N={n_hd}  zHD min={zhd.min():.5f} max={zhd.max():.5f}  MU min={mu_des.min():.3f} max={mu_des.max():.3f}")
print(f"[DES] surveys: {dict(Counter(ids))}")

with gzip.open(DES + "/raw/STAT+SYS.txt.gz", "rt") as f:
    n = int(f.readline())
    assert n == n_hd, (n, n_hd)
    covsys = np.fromstring(f.read(), sep=" ")
assert covsys.size == n * n, covsys.size
covsys = covsys.reshape(n, n)
asym = np.max(np.abs(covsys - covsys.T))
print(f"[DES] COVSYS: shape={covsys.shape}, max|C-C^T|={asym:.3e}, diag min={covsys.diagonal().min():.3e} max={covsys.diagonal().max():.3e}")
np.save(DES + "/des_sn5yr_covsys_1829x1829.npy", covsys)

with gzip.open(DES + "/raw/STATONLY.txt.gz", "rt") as f:
    nst = int(f.readline()); covstat_vals = np.fromstring(f.read(), sep=" ")
print(f"[DES] STATONLY: N={nst}, valeurs non nulles={np.count_nonzero(covstat_vals)} (attendu 0 : stat deja dans MUERR_FINAL)")

shutil.copyfile(DES + "/raw/DES-SN5YR_HD.csv", DES + "/des_sn5yr_hd.csv")

with open(DES + "/raw/DES-SN5YR_HD+MetaData.csv", newline="", encoding="utf-8") as f:
    meta = list(csv.DictReader(f))
meta_by_cid = {r["CID"].strip(): r for r in meta}

pos = {}
for s in ["DES", "LOWZ", "Foundation"]:
    with fits.open(DES + f"/raw/DES-SN5YR_{s}_HEAD.FITS.gz") as h:
        d = h[1].data
        cols = h[1].columns.names
        dec_col = "DEC" if "DEC" in cols else "DECL"
        for snid, ra, dec in zip(d["SNID"], d["RA"], d[dec_col]):
            pos[str(snid).strip()] = (float(ra), float(dec), s)
        print(f"[DES] HEAD {s}: {len(d)} SNe (colonnes: RA/{dec_col})")

n_match = n_miss = 0
miss = []
with open(DES + "/des_sn5yr_radec.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["CID", "IDSURVEY", "zHD", "RA_SN", "DEC_SN", "SRC_HEAD", "HOST_RA", "HOST_DEC"])
    for r in hd:
        cid = r["CID"].strip()
        p = pos.get(cid)
        m = meta_by_cid.get(cid)
        host_ra  = m["HOST_RA"]  if m else ""
        host_dec = m["HOST_DEC"] if m else ""
        if p:
            w.writerow([cid, r["IDSURVEY"], r["zHD"], f"{p[0]:.6f}", f"{p[1]:.6f}", p[2], host_ra, host_dec])
            n_match += 1
        else:
            w.writerow([cid, r["IDSURVEY"], r["zHD"], "", "", "", host_ra, host_dec])
            n_miss += 1; miss.append(cid)
print(f"[DES] RA/DEC SN : {n_match}/{n_hd} apparies via HEAD, {n_miss} manquants")
if miss[:10]: print("[DES] exemples manquants:", miss[:10])
host_ra_ok = sum(1 for r in hd if r["CID"].strip() in meta_by_cid and float(meta_by_cid[r["CID"].strip()]["HOST_RA"]) > -400)
print(f"[DES] HOST_RA renseigne pour {host_ra_ok}/{n_hd}")

# ---------------- Union3 ----------------
with fits.open(U3 + "/raw/mu_mat_union3_cosmo=2_mu.fits") as h:
    m = h[0].data.astype(np.float64)
print(f"[U3] matrice: shape={m.shape}, [0,0]={m[0,0]}")
z  = m[0, 1:]
mu = m[1:, 0]
invcov = m[1:, 1:]
nb = z.size
print(f"[U3] N bins={nb}  z min={z.min():.5f} max={z.max():.5f}")
print(f"[U3] z bins = {np.array2string(z, precision=4)}")
print(f"[U3] mu min={mu.min():.4f} max={mu.max():.4f}")
asym = np.max(np.abs(invcov - invcov.T))
ev = np.linalg.eigvalsh(0.5 * (invcov + invcov.T))
print(f"[U3] invcov: max|A-A^T|={asym:.3e}, vp min={ev.min():.3e} max={ev.max():.3e} (PD={ev.min()>0})")
cov = np.linalg.inv(0.5 * (invcov + invcov.T))
sig = np.sqrt(cov.diagonal())
print(f"[U3] sigma_mu (diag cov): min={sig.min():.4f} max={sig.max():.4f}")

with open(U3 + "/union3_bins.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bin", "z", "mu", "sigma_mu_from_cov_diag"])
    for i in range(nb):
        w.writerow([i + 1, f"{z[i]:.6f}", f"{mu[i]:.6f}", f"{sig[i]:.6f}"])

np.savetxt(U3 + "/union3_inv_cov_22x22.csv", invcov, delimiter=",", fmt="%.10e")
np.savetxt(U3 + "/union3_cov_22x22.csv", cov, delimiter=",", fmt="%.10e")
print("[U3] CSV ecrits.")
print("OK")
