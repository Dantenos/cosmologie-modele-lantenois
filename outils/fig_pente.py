#!/usr/bin/env python3
"""fig_pente — LA FONCTION QUE TOUT LE CORPUS MESURE : s(a) = d ln rho_de / d ln a.
CRITERES PRE-ENREGISTRES (geles). La figure n'est ECRITE que si (1) la pente exacte de
l'accretion recalculee ici, s = -3(1+w), coincide avec -3(1+w) tire du solveur gele
test_wE_v3.fond a mieux que 1e-6 sur a dans [1e-3 ; 1] ; (2) le zero de cette pente tombe
a moins de 0,005 du croisement gele croisement_fantome.z_x au meme (Om, beta). Sinon REFUS.

CE QU'ELLE MONTRE (une seule fonction, quatre lectures) :
  - LCDM             : s = 0 partout (droite) ;
  - le vainqueur de l'atlas (echange interne) : s = -eps, constant = -0,0227 (#161) ;
  - l'accretion      : s(a) = -3 + beta/(H t), RIGIDE, un seul parametre — sa courbe ;
  - la mesure libre  : bande s(a) = -(eps0 + eps1 ln a) avec les valeurs ajustees, plus le
    zero mesure z0 et son intervalle.
Les valeurs ajustees sont LUES dans registres/pente_mesures.json (ecrit par les etudes
gelees #161/#163) — la figure n'ajuste rien elle-meme et ne peut donc rien embellir.
Style maison (toile sombre), palette sure CVD.
Usage : python3 outils/fig_pente.py -> visuels/pente_sa.png
"""
import sys, os, json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT / "donnees" / "pantheon_plus")
import test_wE_v3 as T
import croisement_fantome as CF
os.chdir(ROOT)

# CONVENTION : l'atlas et l'etude #161 travaillent SANS gel primordial de g ; le defaut du
# module est ZCUT = 3 (LCDM exact au-dela de z = 3). On aligne, sinon on compare deux fonds.
T.ZCUT = None

OM, BETA = 0.314, 2.447
FOND, ENC = "#0d0c0a", "#14120f"


def pente_accretion(Om, beta, n_iter=7):
    """s(a) = -3(1+w) recalculee ici, meme schema que le solveur gele."""
    a = T.AG
    Or = Om / 3388.0
    Ode = 1 - Om - Or
    E2 = Om / a**3 + Or / a**4 + Ode
    for _ in range(n_iter):
        E = np.sqrt(np.clip(E2, 1e-30, None))
        integ = 1 / (a * E)
        t = np.concatenate([[0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(a))])
        G3H = beta / (3 * np.clip(E * t, 1e-12, None))
        dlng = -3 * (1 - G3H)
        lna = np.log(a)
        I = np.concatenate([[0], np.cumsum(0.5 * (dlng[1:] + dlng[:-1]) * np.diff(lna))])
        E2 = Om / a**3 + Or / a**4 + Ode * np.exp(np.clip(I - I[-1], -700, 700))
    # s doit etre lue sur le fond CONVERGE, pas sur l'avant-derniere iteration
    E = np.sqrt(np.clip(E2, 1e-30, None))
    integ = 1 / (a * E)
    t = np.concatenate([[0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(a))])
    return a, -3 * (1 - beta / (3 * np.clip(E * t, 1e-12, None)))


if __name__ == "__main__":
    a, s_acc = pente_accretion(OM, BETA)
    zz, Ea = T.fond(OM, 0.0, BETA, 'invt')
    a_ref = 1 / (1 + zz[::-1])
    E_ref = Ea[::-1]
    tr = np.concatenate([[0], np.cumsum(0.5 * (1 / (a_ref[1:] * E_ref[1:]) +
                                               1 / (a_ref[:-1] * E_ref[:-1])) * np.diff(a_ref))])
    s_ref = -3 * (1 - BETA / (3 * np.clip(E_ref * tr, 1e-12, None)))
    m = (a > 1e-3) & (a <= 1.0)
    err = np.max(np.abs(np.interp(a[m], a_ref, s_ref) - s_acc[m]))
    i = np.where(m)[0]
    zx_fig = 1 / np.interp(0.0, s_acc[i][::-1], a[i][::-1]) - 1
    zx_ref = CF.z_x(OM, BETA)
    ok = err < 1e-6 and abs(zx_fig - zx_ref) < 0.005
    print(f"[pente] validation : |ds| max = {err:.2e} ; zero = {zx_fig:.4f} "
          f"(gele {zx_ref:.4f}) -> {'PASSE' if ok else 'REFUS'}")
    if not ok:
        sys.exit(1)

    mes = {}
    f = ROOT / "registres" / "pente_mesures.json"
    if f.exists():
        mes = json.loads(f.read_text(encoding="utf-8"))

    plt.rcParams.update({"font.family": "serif", "text.color": "#efe9dc",
                         "axes.edgecolor": "#3a352c", "axes.labelcolor": "#cfc8b8",
                         "xtick.color": "#8f8878", "ytick.color": "#8f8878"})
    fig, ax = plt.subplots(figsize=(9.0, 5.6), dpi=200)
    fig.patch.set_facecolor(FOND)
    ax.set_facecolor(ENC)
    lna = np.log(a)
    w = (lna >= -2.2) & (lna <= 0.0)

    ax.axhline(0, color="#6f6a5e", lw=1.0, ls=":")
    ax.text(-2.15, 0.03, r"$\Lambda$CDM : $s\equiv 0$", fontsize=8.5, color="#8f8878")

    for k, lab, col in [("leger", "mesure libre — vraisemblance légère (#161)", "#7fa3b8"),
                        ("planck", "mesure libre — Planck complet (#163)", "#d9b96a")]:
        if k in mes:
            e0, e1 = mes[k]["eps0"], mes[k]["eps1"]
            ax.plot(lna[w], -(e0 + e1 * lna[w]), color=col, lw=2.0, label=lab)
            z0 = mes[k].get("z0")
            if z0 is not None:
                ax.plot([-np.log(1 + z0)], [0.0], "o", ms=7, color=col,
                        markeredgecolor="#efe9dc", zorder=5)
            iv = mes[k].get("ic")
            if iv:
                ax.axvspan(-np.log(1 + iv[1]), -np.log(1 + iv[0]), color=col, alpha=0.10)

    if "eps_atlas" in mes:
        e = mes["eps_atlas"]
        ax.plot(lna[w], np.full(w.sum(), -e), color="#a98fc0", lw=2.0, ls="-.",
                label=f"échange sombre interne — atlas : $s=-{e:.4f}$ (constant)")

    ax.plot(lna[w], s_acc[w], color="#c96a4a", lw=2.6,
            label=r"accrétion $w=-\beta/(3Ht)$ — RIGIDE, un seul paramètre")
    ax.plot([-np.log(1 + zx_ref)], [0.0], "*", ms=15, color="#c96a4a",
            markeredgecolor="#efe9dc", zorder=6)
    ax.annotate(f"croisement prédit\n$z_\\times$ = {zx_ref:.3f}", (-np.log(1 + zx_ref), 0.0),
                xytext=(14, -34), textcoords="offset points", fontsize=8.5, color="#e0d6c2",
                arrowprops=dict(arrowstyle="-", color="#6f6a5e", lw=0.7))

    ax.set_xlabel(r"$\ln a$   (passé ← 0 = aujourd'hui)")
    ax.set_ylabel(r"$s(a)=\mathrm{d}\ln\rho_{de}/\mathrm{d}\ln a\;=\;-3(1+w)$")
    ax.set_xlim(-2.2, 0.08)
    ax.set_title("La seule fonction que le corpus mesure — et les quatre façons de la lire",
                 fontsize=11, loc="left", color="#efe9dc")
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    ax.grid(alpha=0.10, lw=0.5)
    ax.text(-2.15, -0.30, "s > 0 : fantôme (w < −1)", fontsize=8, color="#8f8878")
    ax.text(-2.15, 0.34, "s < 0 : quintessence (w > −1)", fontsize=8, color="#8f8878")
    fig.text(0.995, 0.005, "généré par outils/fig_pente.py (gelé) · valeurs lues dans "
             "registres/pente_mesures.json, aucune n'est ajustée ici",
             ha="right", fontsize=6.5, color="#6f6a5e")
    out = ROOT / "visuels" / "pente_sa.png"
    fig.savefig(out, facecolor=FOND, bbox_inches="tight")
    print(f"[pente] écrit : {out.name} ({out.stat().st_size // 1024} ko)")
