#!/usr/bin/env python3
"""LA DECOUVERTE TENTEE — beta_1 SUR LE PLANCK COMPLET : la tension interne est-elle le
running predit par l'heredite ? CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

LE FIL. #151 : beta marginalise = 2,42 +/- 0,07 (fond leger) contre 2,60 +/- 0,05 (Planck
complet) — 2,1 sigma, le levier profond tire beta vers le HAUT, donc lu comme un running :
dbeta/dlnt < 0, beta plus grand dans le passe. Or l'EDO d'heredite (heredite_edo.py, ancre
rejouee le 23/08) PREDIT beta_1 = -0,42 (lecture K=2 ; -0,68 en rms). Signe identique,
ordre de grandeur compatible (Dbeta ~ 0,18 sur ~0,4 en ln t). Le beta_1 mesure du corpus
(+0,06 +/- 0,31) n'a ete ajuste QUE sur la vraisemblance legere, au bras trop court.
Personne n'a jamais ajuste (beta_0, beta_1) sur le Planck complet. C'est fait ici.

MODELE. M ∝ exp(int beta(t) dlnt) avec beta(t) = beta_0 + beta_1 ln(t/t_0), donc
rho_de a^3 ∝ exp(beta_0 ln t + (beta_1/2) ln^2 t), w = -beta(t)/(3Ht) — la generalisation
minimale, un parametre de plus, meme iteration auto-coherente que planck_theta.w_of_a_acc.
emcee (graine 20260824), 8 marcheurs, (omega_c, ln As, beta_0, beta_1), priors plats
[0,10;0,14]x[2,9;3,2]x[1,5;4,0]x[-1,5;+1,5]. DEPART A beta_1 = 0 (regle 6 : on ne part pas
sur la valeur esperee). omega_b, ns, tau fixes comme le profil (declare). Chaine reprenable
(mcmc_acc1_chain.npy, tranches de 10 pas).

CRITERES (exhaustifs, exclusifs — le piege est declare d'avance).
  - VALIDATION : chi2 min visite <= 1986,5 (le sous-espace beta_1 = 0 contient 1986,03) ET
    >= 150 pas par marcheur apres rodage (moitie jetee). Sinon CHAINE INSUFFISANTE, rien lu.
  - NON CONCLUANT si |beta_1| < 2 sigma (quantiles 16/84) — MEME s'il est negatif : le signe
    attendu par l'heredite est -0,42, donc un negatif mou est traite comme du bruit (regle 6,
    defavorable a la these). La tension #151 reste alors ouverte, arbitrage DR3.
  - COMPATIBLE HEREDITE si beta_1 < 0 a >= 2 sigma ET mediane dans [-0,9 ; -0,1] (les deux
    lectures de l'EDO : -0,42 et -0,68, avec marge). Ecrit tel quel + verse au role : beta_1
    est DEJA dans le verdict scelle de DR3 (refutee si beta_1 exclut +0,06 +/- 0,31 a 3 sigma).
  - CONTRE-HEREDITE si beta_1 > 0 a >= 2 sigma : la tension #151 n'est pas un running
    d'heredite ; ecrit tel quel.
  - Dans tous les cas : beta_0 marginalise rapporte, correlation beta_0-beta_1 rapportee,
    chaine courte declaree si l'autocorrelation depasse pas/25.
Usage : python3 scripts/mcmc_planck_beta1.py <n_pas_cible>   (depuis donnees/pantheon_plus)
"""
import sys, pathlib
import numpy as np
import emcee

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import planck_theta as P

def w_of_a_run(a_tab, Om, b):
    b0, b1 = (b if isinstance(b, (tuple, list, np.ndarray)) else (b, 0.0))
    Or = 4.15e-5/0.68**2; Ode = 1-Om-Or
    a = np.logspace(-7, 0, 30000)
    E2 = (Om+Ode)/a**3 + Or/a**4
    for _ in range(4):
        E = np.sqrt(E2); integ = 1/(a*E)
        t = np.concatenate([[0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(a))]); t = t/t[-1]
        lnt = np.log(np.clip(t, 1e-30, None))
        E2 = (Om + Ode*np.exp(np.clip(b0*lnt + 0.5*b1*lnt**2, -690, 690)))/a**3 + Or/a**4
    beta_t = b0 + b1*np.log(np.clip(t, 1e-30, None))
    w = -(beta_t/3.0)/np.clip(np.sqrt(E2)*t, 1e-10, None)
    return np.interp(a_tab, a, np.clip(w, -20, 0.9))

P.w_of_a_acc = w_of_a_run   # make_pars('acc', (b0, b1)) passe desormais par le running

CH, LN = pathlib.Path("mcmc_acc1_chain.npy"), pathlib.Path("mcmc_acc1_lnp.npy")
NW, ND = 8, 4
LO = np.array([0.10, 2.9, 1.5, -1.5]); HI = np.array([0.14, 3.2, 4.0, 1.5])

def lnp(p):
    if np.any(p < LO) or np.any(p > HI): return -np.inf
    c, _ = P.chi2_full(p[0], p[1], ('acc', (p[2], p[3])))
    return -0.5*c

if __name__ == "__main__":
    cible = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rng = np.random.default_rng(20260824)
    if CH.exists():
        chain = np.load(CH); lnprob = np.load(LN); p0 = chain[-1]; fait = chain.shape[0]
        print(f"[mcmc-b1] reprise : {fait} pas")
    else:
        centre = np.array([0.1192, 3.0415, 2.60, 0.0])   # depart beta_1 = 0 (regle 6)
        p0 = centre + rng.normal(size=(NW, ND))*np.array([0.0004, 0.004, 0.02, 0.03])
        chain = np.empty((0, NW, ND)); lnprob = np.empty((0, NW)); fait = 0
    s = emcee.EnsembleSampler(NW, ND, lnp)
    s.random_state = np.random.RandomState(20260824 + fait).get_state()
    while fait < cible:
        n = min(10, cible - fait)
        p0, lp, _ = s.run_mcmc(p0, n, progress=False, skip_initial_state_check=True)
        chain = np.concatenate([chain, s.get_chain()[-n:]]); lnprob = np.concatenate([lnprob, s.get_log_prob()[-n:]])
        s.reset(); np.save(CH, chain); np.save(LN, lnprob); fait = chain.shape[0]
        ap = chain[fait//2:]
        print(f"[mcmc-b1] {fait}/{cible} | chi2 min = {-2*lnprob.max():.2f} | "
              f"b0 = {np.median(ap[:,:,2]):.3f}  b1 = {np.median(ap[:,:,3]):+.3f}", flush=True)
    chi2min = -2*lnprob.max(); ap = chain[fait//2:]
    ok = chi2min <= 1986.5 and ap.shape[0] >= 150
    print(f"\n[mcmc-b1] chi2 min = {chi2min:.2f} (sous-espace b1=0 : 1986,03) ; pas apres rodage = {ap.shape[0]}")
    if not ok:
        print("[mcmc-b1] CHAINE INSUFFISANTE — on continue, rien n'est lu."); sys.exit(0)
    b0s, b1s = ap[:, :, 2].ravel(), ap[:, :, 3].ravel()
    q0 = np.percentile(b0s, [16, 50, 84]); q1 = np.percentile(b1s, [16, 50, 84])
    s1 = 0.5*(q1[2]-q1[0]); nsig = abs(q1[1])/s1 if s1 > 0 else 0
    rho = float(np.corrcoef(b0s, b1s)[0, 1])
    print(f"[mcmc-b1] beta_0 = {q0[1]:.3f} +{q0[2]-q0[1]:.3f}/-{q0[1]-q0[0]:.3f}")
    print(f"[mcmc-b1] beta_1 = {q1[1]:+.3f} +{q1[2]-q1[1]:.3f}/-{q1[1]-q1[0]:.3f}   ({nsig:.1f} sigma de 0)")
    print(f"[mcmc-b1] corr(beta_0, beta_1) = {rho:+.2f} ; heredite : -0,42 (K=2) / -0,68 (rms) ; leger : +0,06 +/- 0,31")
    if nsig < 2: v = "NON CONCLUANT (|beta_1| < 2 sigma — meme negatif, regle 6). Tension #151 ouverte, arbitrage DR3."
    elif q1[1] < 0 and -0.9 <= q1[1] <= -0.1: v = "COMPATIBLE HEREDITE : signe et gamme de l'EDO. Ecrit tel quel ; beta_1 est deja dans le sceau DR3."
    elif q1[1] > 0: v = "CONTRE-HEREDITE : running positif. La tension #151 n'est pas l'heredite. Ecrit tel quel."
    else: v = "NEGATIF HORS GAMME [-0,9;-0,1] : ni bruit ni heredite — a comprendre avant d'exploiter."
    print(f"[mcmc-b1] VERDICT (criteres geles) : {v}")
    try:
        tau = emcee.autocorr.integrated_time(ap[:, :, 3], quiet=True)
        print(f"[mcmc-b1] autocorrelation beta_1 ~ {float(tau[0]):.0f} pas (chaine courte declaree si > pas/25)")
    except Exception: pass
