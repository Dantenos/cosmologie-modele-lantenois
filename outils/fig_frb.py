#!/usr/bin/env python3
"""fig_frb v1 — la figure du canal FRB sur donnees reelles (papier C). CRITERES
PRE-ENREGISTRES (geles) : la figure n'est ecrite que si les ajustements refaits ici
redonnent les valeurs consignees en #148 (f_d(LCDM) = 0,905 +/- 0,01 ; Dchi2(CCBH-LCDM)
= 4,71 +/- 0,1) — sinon REFUS (la figure ne doit jamais diverger du registre).
Contenu : mediane de DM_ex(z) par fond, chacun A SES nuisances preferees (l'honnetete du
test est la : les nuisances ont le droit d'absorber), + les 69 FRB reels. Palette
Okabe-Ito (sure pour la vision des couleurs), un seul axe, etiquettes directes.
Usage : python3 outils/fig_frb.py   ->  papiers/fig_frb_reelles.png
"""
import sys, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import etude_E3_frb_reelles as V0
import frb_likelihood as F

data = V0.charge()
z = np.array([d[1] for d in data]); dm = np.array([d[0] for d in data])
res = {w: V0.fit(data, w) for w in ("L", "A", "C")}
fdL = res["L"].x[0] + res["L"].x[1]
dC = 2*(res["C"].fun - res["L"].fun)
if not (abs(fdL - 0.905) < 0.01 and abs(dC - 4.71) < 0.1):
    sys.exit(f"[fig_frb] REFUS : f_d = {fdL:.3f}, Dchi2 = {dC:.2f} != registre #148 (0,905 ; 4,71)")

zg = np.linspace(0.01, 1.45, 300)
COL = {"L": "#000000", "A": "#0072B2", "C": "#D55E00"}
LAB = {"L": "$\\Lambda$CDM", "A": "accretion ($s=1$, $\\beta=2.595$)", "C": "CCBH (calibrated, $\\Xi=1.382$)"}
fig, ax = plt.subplots(figsize=(7.0, 4.6), dpi=200)
for w in ("L", "A", "C"):
    fI, fX, mu, sig = res[w].x
    med = (fI + fX)*np.interp(zg, F.ZG, {"L": F.DM_L, "A": F.DM_A, "C": F.DM_C}[w]) + np.exp(mu)/(1+zg)
    ls = "--" if w == "A" else "-"
    ax.plot(zg, med, ls, color=COL[w], lw=1.6 if w != "A" else 1.2, zorder=3)
    import numpy as _np
    yl = {"L": 1330.0, "A": 1210.0, "C": 1180.0}[w]
    i = int(_np.argmin(_np.abs(med - yl)))
    dx, dy = {"L": (-64, 8), "A": (-150, 10), "C": (10, -12)}[w]
    ax.annotate(LAB[w], (zg[i], med[i]), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color=COL[w], va="center")
ax.scatter(z, dm, s=14, c="#555555", alpha=0.75, zorder=4, lw=0)
ax.set_xlabel("redshift $z$"); ax.set_ylabel("extragalactic DM  [pc cm$^{-3}$]")
ax.set_xlim(0, 1.72); ax.set_ylim(0, 1500)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(alpha=0.15, lw=0.5)
ax.set_title("69 localized FRBs (Connor et al. 2025) against the three backgrounds,\n"
             "each at its own preferred nuisances", fontsize=9.5, loc="left")
txt = (f"$\\Lambda$CDM : $f_d={fdL:.3f}$ (published $0.91$), host $123$ pc cm$^{{-3}}$\n"
       f"CCBH : $f_d = 1.00$ (boundary), host $170$ pc cm$^{{-3}}$\n"
       f"$\\Delta\\chi^2(\\mathrm{{CCBH}}-\\Lambda\\mathrm{{CDM}}) = +{dC:.1f}$ ($\\sim$2.2$\\sigma$) ; "
       f"accretion $-0.0$")
ax.text(0.985, 0.04, txt, transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.45", fc="#f7f5f0", ec="#cccccc", lw=0.6))
fig.tight_layout()
out = ROOT / "papiers" / "fig_frb_reelles.png"
fig.savefig(out)
print(f"[fig_frb] ecrit : {out.name} ({out.stat().st_size//1024} ko) ; f_d = {fdL:.3f}, Dchi2 = {dC:.2f} — conformes #148")
