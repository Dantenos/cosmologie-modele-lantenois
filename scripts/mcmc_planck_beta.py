#!/usr/bin/env python3
"""MCMC PLANCK COMPLET SUR beta — le manquement #2, ferme : marginalisation, pas profil.
CRITERES PRE-ENREGISTRES (geles par registre AVANT la premiere execution, 23/08/2026).

CE QUI MANQUAIT. Le -12,6 Planck complet du papier A repose sur un PROFIL (#2 : « le MCMC
complet (marginalisation, pas profil) reste souhaitable » ; papier A : « fully marginalised
errors await the MCMC run »). Le profil donne beta = 2,56 +0,08/-0,02, fortement asymetrique.

METHODE. emcee (graine 20260823) sur la vraisemblance de planck_theta.py (gelee ; CAMB,
plik_lite TTTEEE + low-l, BAO DR2, Pantheon+, H0 resolu par theta*), parametres
(omega_c h2, ln 10^10 As, beta), priors plats [0,10;0,14] x [2,9;3,2] x [1,5;4,0],
omega_b, ns, tau fixes comme dans le profil (declare : ce MCMC marginalise les DEUX
nuisances profilees, pas les parametres fixes — c'est l'objet exact de #2).
8 marcheurs, initialisation en boule autour du minimum du profil (0,1192 ; 3,0415 ; 2,589).
Chaine reprenable : mcmc_acc_chain.npy / mcmc_acc_lnp.npy dans le CWD, tranches de 10 pas.

CRITERES (exhaustifs, exclusifs).
  - VALIDATION : le min de chi2 visite par la chaine doit atteindre <= 1987,0 (profil :
    1986,03) ET la chaine doit compter >= 150 pas par marcheur apres rodage (rodage = la
    premiere moitie, jetee). Sinon : CHAINE INSUFFISANTE — on continue, rien n'est lu.
  - Si validation : beta marginalise = quantiles 16/50/84 de la seconde moitie, rapportes
    TELS QUELS, compares au profil 2,56 +0,08/-0,02 et a la bande publiee [2,42 ; 2,60].
    Si la mediane sort de la bande, c'est ecrit tel quel (pas de reinterpretation).
  - L'autocorrelation est rapportee a titre indicatif (chaine courte declaree).
Usage : python3 scripts/mcmc_planck_beta.py <n_pas_cible>   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np
import emcee

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import planck_theta as P

CH, LN = pathlib.Path("mcmc_acc_chain.npy"), pathlib.Path("mcmc_acc_lnp.npy")
NW, ND = 8, 3
LO = np.array([0.10, 2.9, 1.5]); HI = np.array([0.14, 3.2, 4.0])

def lnp(p):
    if np.any(p < LO) or np.any(p > HI): return -np.inf
    c, _ = P.chi2_full(p[0], p[1], ('acc', p[2]))
    return -0.5*c

if __name__ == "__main__":
    cible = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    rng = np.random.default_rng(20260823)
    if CH.exists():
        chain = np.load(CH); lnprob = np.load(LN)
        p0 = chain[-1]; fait = chain.shape[0]
        print(f"[mcmc] reprise : {fait} pas")
    else:
        centre = np.array([0.1192, 3.0415, 2.589])
        p0 = centre + rng.normal(size=(NW, ND))*np.array([0.0004, 0.004, 0.02])
        chain = np.empty((0, NW, ND)); lnprob = np.empty((0, NW)); fait = 0
    s = emcee.EnsembleSampler(NW, ND, lnp)
    s.random_state = np.random.RandomState(20260823 + fait).get_state()
    while fait < cible:
        n = min(10, cible - fait)
        p0, lp, _ = s.run_mcmc(p0, n, progress=False, skip_initial_state_check=True)
        chain = np.concatenate([chain, s.get_chain()[-n:]]); lnprob = np.concatenate([lnprob, s.get_log_prob()[-n:]])
        s.reset()
        np.save(CH, chain); np.save(LN, lnprob); fait = chain.shape[0]
        print(f"[mcmc] {fait}/{cible} pas | chi2 min = {-2*lnprob.max():.2f} | "
              f"beta courant (mediane 2e moitie) = {np.median(chain[fait//2:, :, 2]):.3f}", flush=True)
    # verdict
    chi2min = -2*lnprob.max(); apres = chain[fait//2:]
    ok = chi2min <= 1987.0 and apres.shape[0] >= 150
    print(f"\n[mcmc] chi2 min = {chi2min:.2f} (profil 1986,03) ; pas apres rodage = {apres.shape[0]}")
    if not ok:
        print("[mcmc] CHAINE INSUFFISANTE — on continue, rien n'est lu."); sys.exit(0)
    b = apres[:, :, 2].ravel()
    q = np.percentile(b, [16, 50, 84])
    print(f"[mcmc] beta MARGINALISE (Planck complet) = {q[1]:.3f} +{q[2]-q[1]:.3f} / -{q[1]-q[0]:.3f}")
    print(f"       profil (conditionnel) : 2,56 +0,08/-0,02 ; bande publiee [2,42 ; 2,60] -> "
          f"mediane {'DANS' if 2.42 <= q[1] <= 2.60 else 'HORS'} la bande")
    try:
        tau = emcee.autocorr.integrated_time(apres[:, :, 2], quiet=True)
        print(f"       autocorrelation ~ {float(tau[0]):.0f} pas (chaine courte declaree)")
    except Exception: pass
    for i, nom in [(0, "omega_c h2"), (1, "ln 10^10 As")]:
        qq = np.percentile(apres[:, :, i].ravel(), [16, 50, 84])
        print(f"       {nom} = {qq[1]:.4f} +{qq[2]-qq[1]:.4f} / -{qq[1]-qq[0]:.4f}")
