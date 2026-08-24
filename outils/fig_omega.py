#!/usr/bin/env python3
"""fig_omega v1 — l'histoire du budget Omega sous la loi w = -beta/(3Ht). CRITERES
PRE-ENREGISTRES (geles) : la figure n'est ECRITE que si (1) le fond auto-coherent resolu ici
reproduit E_acc de vraisemblance_reelle a mieux que 1e-3 relatif sur z dans [0 ; 1100] ;
(2) Omega_de(a=1) = 1 - Om - Or a 1e-3 pres ; (3) le croisement z_x lu sur la courbe w(z)
tombe a moins de 0,02 du calcul gele de croisement_fantome.py au meme (Om, beta). Sinon
REFUS. Parametres : la ligne de base (Om = 0,314, beta = 2,447). Contenu : les fractions
Omega_i(a) (rayonnement, matiere, energie noire injectee rho_de ∝ t^beta/a^3) de a = 1e-5 au
futur profond a = 30, LCDM en pointilles ; panneau w(z) avec le croisement et l'attracteur
futur w* (limite numerique a -> infini, celle d'E7). Style maison (toile sombre), palette
sure CVD. Usage : python3 outils/fig_omega.py -> visuels/omega_histoire.png
"""
import sys, os, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT / "donnees" / "pantheon_plus")
import vraisemblance_reelle as VR
import croisement_fantome as CF
os.chdir(ROOT)

OM, BETA = 0.314, 2.447
ZEQ = 3387.0

def fond(a_max=30.0, n=60000):
    a = np.logspace(-6, np.log10(a_max), n)
    Or = OM/(1+ZEQ); Ode = 1-OM-Or
    E2 = (OM + Ode)/a**3 + Or/a**4
    for _ in range(6):
        E = np.sqrt(E2); integ = 1/(a*E)
        tr = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))])   # temps PHYSIQUE (H0=1)
        i1 = np.searchsorted(a, 1.0); t = tr/tr[i1]                                     # temps NORMALISE (densite)
        E2 = (OM + Ode*np.clip(t, 1e-30, None)**BETA)/a**3 + Or/a**4
    rho_r = Or/a**4; rho_m = OM/a**3; rho_de = Ode*np.clip(t, 1e-30, None)**BETA/a**3
    tot = rho_r + rho_m + rho_de
    Ht = np.sqrt(E2)*tr                                                                 # w veut le temps physique
    w = -(BETA/3.0)/np.clip(Ht, 1e-10, None)
    return a, t, rho_r/tot, rho_m/tot, rho_de/tot, w, np.sqrt(E2)

if __name__ == "__main__":
    a, t, fr_, fm, fde, w, E = fond()
    # (1) validation contre E_acc gele
    zt = np.linspace(0, 1100, 400)
    Ea = VR.E_acc(zt, OM, BETA); Eici = np.interp(1/(1+zt), a, E)
    err = np.max(np.abs(Eici/Ea - 1))
    # (2) budget aujourd'hui
    i1 = np.searchsorted(a, 1.0)
    Ode_num = fde[i1]; Ode_att = 1 - OM - OM/(1+ZEQ)
    # (3) croisement
    m = (a > 0.2) & (a < 1.0)
    zx = 1/np.interp(-1.0, w[m], a[m]) - 1
    zx_ref = CF.z_x(OM, BETA)
    ok = err < 1e-3 and abs(Ode_num - Ode_att) < 1e-3 and abs(zx - zx_ref) < 0.02
    print(f"[omega] validation : |dE/E| max = {err:.1e} ; Omega_de(1) = {Ode_num:.4f} (attendu {Ode_att:.4f}) ; "
          f"z_x = {zx:.3f} (gele {zx_ref:.3f}) -> {'PASSE' if ok else 'REFUS'}")
    if not ok: sys.exit(1)
    w_inf = w[-1]
    FOND, ENC = "#0d0c0a", "#14120f"
    plt.rcParams.update({"font.family": "serif", "text.color": "#efe9dc", "axes.edgecolor": "#3a352c",
                         "axes.labelcolor": "#cfc8b8", "xtick.color": "#8f8878", "ytick.color": "#8f8878"})
    fig, (ax, aw) = plt.subplots(2, 1, figsize=(8.6, 7.2), dpi=200, sharex=True,
                                 gridspec_kw=dict(height_ratios=[2.1, 1.0], hspace=0.07))
    fig.patch.set_facecolor(FOND)
    for AX in (ax, aw): AX.set_facecolor(ENC)
    ax.plot(a, fr_, color="#d9b96a", lw=1.8, label="rayonnement")
    ax.plot(a, fm, color="#7fa3b8", lw=1.8, label="matière")
    ax.plot(a, fde, color="#c96a4a", lw=2.2, label=r"énergie noire injectée  $\rho_{de}\propto t^{\beta}/a^3$")
    OdeL = 1 - OM - OM/(1+ZEQ)
    totL = OM/a**3 + (OM/(1+ZEQ))/a**4 + OdeL
    ax.plot(a, OdeL/totL, color="#c96a4a", lw=1.0, ls="--", alpha=0.55, label=r"$\Lambda$CDM ($\Lambda$ constant)")
    for xv, lab in [(1/(1+ZEQ), "égalité"), (1/1101, "recombinaison"), (1/(1+zx), "croisement"), (1.0, "aujourd'hui")]:
        ax.axvline(xv, color="#3a352c", lw=0.8)
        if lab: ax.text(xv, 0.52, lab, rotation=90, ha="right", va="center", fontsize=7.5, color="#8f8878")
    ax.set_xscale("log"); ax.set_xlim(1e-5, 30); ax.set_ylim(0, 1.02)
    ax.set_ylabel(r"fraction du budget  $\Omega_i(a)$")
    ax.legend(loc="center left", fontsize=8.5, frameon=False)
    ax.set_title(f"Le budget de l'univers sous  w = −β/(3Ht)   (β = {BETA}, Ω_m = {OM} — la ligne de base)",
                 fontsize=10.5, loc="left", color="#efe9dc")
    aw.plot(a, w, color="#c96a4a", lw=2.0)
    aw.axhline(-1, color="#6f6a5e", lw=0.8, ls=":")
    aw.axhline(w_inf, color="#8faf7f", lw=0.9, ls="--")
    aw.text(20, w_inf + 0.03, f"attracteur  w* ≈ {w_inf:.2f}", fontsize=8.5, color="#8faf7f", ha="right")
    aw.annotate(f"z× = {zx:.2f}", (1/(1+zx), -1.0), xytext=(8, -14), textcoords="offset points",
                fontsize=8.5, color="#e0d6c2")
    aw.plot([1/(1+zx)], [-1.0], "o", ms=5, color="#efe9dc")
    aw.set_xlabel("facteur d'échelle  a   (passé ← 1 → futur)")
    aw.set_ylabel("w(a)"); aw.set_ylim(-1.45, -0.35)
    for AX in (ax, aw): AX.grid(alpha=0.10, lw=0.5)
    fig.text(0.995, 0.005, "généré par outils/fig_omega.py (gelé) · validation contre E_acc et croisement_fantome",
             ha="right", fontsize=6.5, color="#6f6a5e")
    out = ROOT / "visuels" / "omega_histoire.png"
    fig.savefig(out, facecolor=FOND, bbox_inches="tight")
    print(f"[omega] écrit : {out.name} ({out.stat().st_size//1024} ko) ; w* = {w_inf:.3f}, z_x = {zx:.3f}")
