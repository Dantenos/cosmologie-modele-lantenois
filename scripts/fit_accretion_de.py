#!/usr/bin/env python3
"""
fit_accretion_de.py — Cadre de test du modèle "énergie noire par accrétion parentale"
=====================================================================================
Hypothèse testée : notre univers est l'intérieur d'un trou noir ; l'énergie noire
est la masse-énergie accrétée par le trou noir parent, répartie uniformément.

Le modèle prédit une équation d'état rigide :

    w(z) = -(1/3) * dln(M_acc)/dln(t)  /  (H(z) * t(z))

Deux variantes :
  - 'powerlaw' : M_acc(t) ∝ t^beta            (1 paramètre libre : beta)
  - 'bondi'    : dM/dt = A M², M(0)=M_matière (0 paramètre libre — tout est fixé
                 par les conditions aux limites cosmologiques)

Usage :
  python3 fit_accretion_de.py                        # test avec DESI DR2 intégré
  python3 fit_accretion_de.py mesures_wz.csv         # fit sur données w(z)
                                                     # CSV : colonnes z,w,sigma_w
Sortie : paramètres ajustés, chi², comparaison ΛCDM, graphique w_z_fit.png

Pourquoi ce script : transformer l'hypothèse en équation qui peut PERDRE.
Chaque nouvelle publication (DESI DR3, Euclid, LSST) fournit soit des couples
(w0, wa), soit une reconstruction w(z) : on les injecte ici et on regarde si
la forme rigide du modèle survit.
"""
import sys
import numpy as np

# ---------------------------------------------------------------------------
# Fond cosmologique — on utilise ΛCDM comme approximation du fond pour a(t),
# car l'écart induit par w(z)≠-1 sur H(z) est de second ordre pour ce test.
# ---------------------------------------------------------------------------
class Fond:
    def __init__(self, Om=0.315):
        self.Om, self.Ol = Om, 1.0 - Om
        # table t(a) en unités H0=1 (intégration trapèzes, suffisant ici)
        a = np.linspace(1e-4, 2.0, 40000)
        integrand = 1.0 / (a * self._E(a))
        t = np.concatenate([[0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(a))])
        self._a, self._t = a, t

    def _E(self, a):
        return np.sqrt(self.Om/a**3 + self.Ol)

    def E(self, z):      return self._E(1.0/(1.0+np.asarray(z, float)))
    def t_of_z(self, z): return np.interp(1.0/(1.0+np.asarray(z, float)), self._a, self._t)
    @property
    def t0(self):        return float(np.interp(1.0, self._a, self._t))


# ---------------------------------------------------------------------------
# Le modèle : w(z) pour chaque variante
# ---------------------------------------------------------------------------
class ModeleAccretion:
    def __init__(self, fond=None, variante="powerlaw"):
        self.fond = fond or Fond()
        self.variante = variante

    def w_of_z(self, z, beta=2.2, Ode=0.685):
        """Équation d'état effective prédite par le modèle.
        beta : exposant M_acc ∝ t^beta (variante powerlaw, ignoré en bondi)
        Ode  : fraction d'énergie noire aujourd'hui (fixe la variante bondi)"""
        f = self.fond
        t, E = f.t_of_z(z), f.E(z)
        if self.variante == "powerlaw":
            dlnM_dlnt = beta
        else:  # bondi : dM/dt = A M² ⇒ M(t) = M_m/(1 - A M_m t)
            # A fixé pour que M(t0) = M_total : aucun paramètre libre.
            # dln(M_acc)/dln(t) = t·Ṁ/(M - M_m) avec Ṁ = A M².
            Om_frac = 1.0 - Ode
            x = (Ode * (t / f.t0))          # A·M_m·t = Ode·t/t0 (adimensionné)
            M_rel = Om_frac / (1.0 - x) / Om_frac  # M/M_m = 1/(1-x)
            Mdot_rel = x/t * M_rel**2               # (A M_m)·M_rel², en 1/t
            dlnM_dlnt = t * Mdot_rel / (M_rel - 1.0)
        return -(dlnM_dlnt/3.0) / (E * t)

    def w0_wa(self, **kw):
        """Projection sur la paramétrisation CPL w(a)=w0+wa(1-a), pour comparer
        directement aux publications qui ne donnent que (w0, wa)."""
        da = 1e-4
        z_de = lambda a: 1.0/a - 1.0
        w0 = float(self.w_of_z(0.0, **kw))
        wa = -float(self.w_of_z(z_de(1+da), **kw) - self.w_of_z(z_de(1-da), **kw)) / (2*da)
        return w0, wa


# ---------------------------------------------------------------------------
# Ajustement sur données w(z) et comparaison des modèles
# ---------------------------------------------------------------------------
def chi2(w_model, w_data, sigma):
    return float(np.sum(((w_model - w_data)/sigma)**2))

def fit(z, w, sigma, modele):
    """Fit de beta par balayage fin — robuste, sans dépendance à scipy.optimize,
    pour rester portable (42, VPS, etc.)."""
    if modele.variante == "bondi":
        return None, chi2(modele.w_of_z(z), w, sigma)   # rien à ajuster
    betas = np.linspace(0.5, 5.0, 2251)
    chis = [chi2(modele.w_of_z(z, beta=b), w, sigma) for b in betas]
    i = int(np.argmin(chis))
    # incertitude 1σ : Δchi² = 1
    ok = betas[np.array(chis) <= chis[i] + 1.0]
    return (betas[i], float(ok.min()), float(ok.max())), chis[i]

def main(argv):
    fond = Fond()
    if len(argv) > 1:
        # Données utilisateur : CSV z,w,sigma_w (reconstruction w(z) publiée)
        z, w, s = np.loadtxt(argv[1], delimiter=",", skiprows=1, unpack=True)
        source = argv[1]
    else:
        # Jeu de test : pseudo-données dérivées de DESI DR2+CMB+SN (CPL)
        # w0≈-0.70, wa≈-1.0, incertitudes indicatives — À REMPLACER par les
        # chaînes publiques dès qu'une reconstruction w(z) est disponible.
        z = np.array([0.0, 0.3, 0.6, 1.0, 1.5, 2.3])
        a = 1/(1+z)
        w = -0.70 + (-1.0)*(1-a)
        s = np.array([0.10, 0.10, 0.12, 0.15, 0.20, 0.30])
        source = "pseudo-données DESI DR2 (CPL w0=-0.70, wa=-1.0)"

    print(f"Source de données : {source}\n")
    resultats = {}
    for variante in ("powerlaw", "bondi"):
        m = ModeleAccretion(fond, variante)
        best, c2 = fit(z, w, s, m)
        dof = len(z) - (1 if variante == "powerlaw" else 0)
        if variante == "powerlaw":
            b, blo, bhi = best
            w0, wa = m.w0_wa(beta=b)
            print(f"[powerlaw]  beta = {b:.2f}  (+{bhi-b:.2f}/-{b-blo:.2f})"
                  f"   chi2/dof = {c2:.1f}/{dof}   → w0={w0:+.2f}, wa={wa:+.2f}")
            resultats[variante] = (m, {"beta": b})
        else:
            w0, wa = m.w0_wa()
            print(f"[bondi]     0 paramètre libre"
                  f"            chi2/dof = {c2:.1f}/{dof}   → w0={w0:+.2f}, wa={wa:+.2f}")
            resultats[variante] = (m, {})
    # Référence ΛCDM : w = -1 partout
    c2_lcdm = chi2(np.full_like(z, -1.0), w, s)
    print(f"[ΛCDM]      w = -1 fixe                chi2/dof = {c2_lcdm:.1f}/{len(z)}")
    print("\nVerdict : le modèle survit si son chi2/dof ≲ celui de ΛCDM ;"
          "\nil est falsifié si une reconstruction w(z) précise s'écarte de sa forme rigide.")

    # Graphique
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        zz = np.linspace(0, 2.5, 300)
        plt.figure(figsize=(7, 4.5))
        plt.errorbar(z, w, yerr=s, fmt="o", color="k", label="données", zorder=5)
        for (variante, (m, kw)), style in zip(resultats.items(), ("-", "--")):
            plt.plot(zz, m.w_of_z(zz, **kw), style, label=f"modèle ({variante})")
        plt.axhline(-1, color="gray", lw=0.8, label="ΛCDM (w=-1)")
        plt.xlabel("z"); plt.ylabel("w(z)"); plt.legend(); plt.tight_layout()
        plt.savefig("w_z_fit.png", dpi=150)
        print("\nGraphique : w_z_fit.png")
    except Exception as e:
        print(f"(pas de graphique : {e})")

if __name__ == "__main__":
    main(sys.argv)
