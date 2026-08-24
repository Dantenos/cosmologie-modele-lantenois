#!/usr/bin/env python3
"""LA CONFLUENCE SUR PLANCK COMPLET — le croisement, mesure par une forme LIBRE.
CRITERES PRE-ENREGISTRES (geles AVANT toute execution, 24/08/2026). Suite directe de #161,
qui a mesure la pente s(a) = d ln rho_de/d ln a sur la vraisemblance LEGERE et a refuse d'y
voir une victoire : z0 (forme libre) et z_x (famille rigide) y sortaient des MEMES donnees.
Ici l'information de forme est INDEPENDANTE : Planck haut-l contraint la geometrie et l'ISW,
pas la forme des SNe a bas z. C'est le test a contenu.

LE MODELE. Lecture EXTERNE seule (matiere intacte — la these du corpus ; la lecture interne
demanderait de modifier la dilution de la matiere DANS CAMB, hors de portee ici, et c'est
declare comme une limite de cette etude, pas comme un choix favorable). La pente libre
  s(a) = -(eps0 + eps1 ln a)   equivaut EXACTEMENT a   w(a) = -1 + (eps0 + eps1 ln a)/3,
soit une simple table w(a) confiee a CAMB en PPF — aucune approximation supplementaire.
eps0 = eps1 = 0 redonne w = -1 exactement.

BRANCHEMENT DECLARE : planck_theta.make_pars est ETENDU EN MEMOIRE (nouvelle branche
'pente') depuis ce script ; AUCUN fichier gele n'est modifie, le docstring de planck_theta
n'est pas touche, et les branches 'lcdm'/'cpl'/'acc' sont deleguees a l'original.
GARDE PRIMORDIALE (identique a #161) : tout point donnant Omega_de(a) > 0,02 pour a < 1e-2
est rejete. BORNES DECLAREES : eps0 dans [-1 ; 2], eps1 dans [-0,5 ; 3].
DEPART (regle 6) : eps1 = 0 — le depart ne suppose PAS le running espere.

--- VALIDATION (si elle echoue, RIEN n'est publie) ---
  chi2('pente', eps0 = 0, eps1 = 0) doit reproduire le LCDM de Planck complet,
  1998,63 (ancre du jackknife #160), a +/- 0,5. C'est un controle de branchement PPF.

--- CE QUE LA FAMILLE RIGIDE PREDIT, ECRIT AVANT LE TEST ---
  Les determinations de beta sur Planck complet donnent, par croisement_fantome.py (gele,
  Om = 0,314) : z_x(2,56) = 0,2617 ; z_x(2,589) = 0,2319 ; z_x(2,603) = 0,2182.
  BANDE RIGIDE PREDITE : z_x dans [0,218 ; 0,262].
  La vraisemblance legere, forme libre (#161), avait mesure z0 = 0,240 [0,090 ; 0,340].

--- CRITERES (exhaustifs, exclusifs) ---
  1. LE RUNNING. d = chi2(eps1 = 0) - chi2_min, a 1 ddl (eps1 = 0 est exactement wCDM) :
     PLANCK DEMANDE LE RUNNING   si d >= 4,0 (2 sigma) ;
     PLANCK NE LE DEMANDE PAS    si d <  1,0 (1 sigma) ;
     INTERMEDIAIRE               sinon. Ecrit tel quel dans les trois cas.
     La significativite rapportee est CELLE-CI (rapport de vraisemblance), jamais la
     courbure locale — piege deja paye deux fois (bosse ; #161).
  2. LA LOCALISATION. Profil sur eps1 (grille DECLAREE : 0,0 ; 0,2 ; 0,4 ; 0,6 ; 0,8 ; 1,0 ;
     1,4 ; 2,0), (omch2, ln10As, eps0) reoptimises a chaque point ; z0(eps1) = exp(eps0/eps1)
     - 1 ; intervalle a 1 sigma = les z0 des points ou dchi2 <= 1.
     Si le running n'est pas demande (critere 1 negatif) : NON LOCALISE, et les criteres 3
     et 4 ne sont pas evalues — on s'arrete et on l'ecrit.
  3. CONVERGENCE RIGIDE : la bande [0,218 ; 0,262] coupe-t-elle l'intervalle a 1 sigma de z0 ?
     OUI -> CONVERGENCE RIGIDE (la forme libre retrouve, sur des donnees dont l'information
     de forme est independante, le croisement que la famille a UN parametre predit) ;
     disjointe a 2 sigma -> TENSION RIGIDE ; sinon INTERMEDIAIRE.
  4. CONVERGENCE INDEPENDANTE : l'intervalle a 1 sigma de z0 coupe-t-il celui de la
     vraisemblance legere, [0,090 ; 0,340] (#161) ? OUI -> CONVERGENCE INDEPENDANTE ;
     disjoint -> DIVERGENCE ENTRE JEUX, ecrite telle quelle et versee a T9.
  Regle 9 : criteres 3 et 4 en desaccord = rien n'est exploite.
  Regle 3 : cette etude REDUIT l'espace des formes ; elle n'en ferme aucune.

Usage : python3 ../../scripts/confluence_planck.py <budget_evals>   (depuis
donnees/pantheon_plus ; reprenable, etat sur disque dans state_confluence.json).
"""
import sys, os, json, pathlib
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import camb
import planck_theta as P

LCDM_REF = 1998.63
BANDE_RIGIDE = (0.218, 0.262)
IC_LEGER = (0.090, 0.340)
GRILLE_E1 = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 2.0]
BORNES = dict(e0=(-1.0, 2.0), e1=(-0.5, 3.0))
STATE = "state_confluence.json"
A_TAB = np.logspace(-6, 0, 300)

_orig_make_pars = P.make_pars


def make_pars_pente(H0, omch2, ln10As, de):
    if de[0] != 'pente':
        return _orig_make_pars(H0, omch2, ln10As, de)
    e0, e1 = de[1], de[2]
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=P.OMB_H2, omch2=omch2, tau=P.TAU)
    pars.InitPower.set_params(As=np.exp(ln10As) * 1e-10, ns=P.NS)
    w = -1.0 + (e0 + e1 * np.log(A_TAB)) / 3.0
    pars.set_dark_energy_w_a(A_TAB, np.clip(w, -20, 0.9), dark_energy_model='ppf')
    return pars


P.make_pars = make_pars_pente


def admissible(e0, e1):
    if not (BORNES['e0'][0] <= e0 <= BORNES['e0'][1]):
        return False
    if not (BORNES['e1'][0] <= e1 <= BORNES['e1'][1]):
        return False
    la = np.log(1e-2)
    lg = -(e0 * la + e1 * la**2 / 2)          # ln(rho_de(a)/rho_de0)
    # Omega_de(a) ~ Ode e^lg / (Om a^-3) < 0,02  avec (Om, Ode) = (0,31 ; 0,69)
    return lg < np.log(0.02 * 0.31 / 0.69) + 3 * abs(la)


def chi2_pente(x):
    """x = [omch2, ln10As, eps0, eps1]"""
    if not admissible(x[2], x[3]):
        return 1e10
    c, _ = P.chi2_full(x[0], x[1], ('pente', x[2], x[3]))
    return c


def charge():
    if os.path.exists(STATE):
        return json.load(open(STATE, encoding="utf-8"))
    return dict(phase=0, valid=None, x=[0.1195, 3.041, 0.02, 0.0],
                steps=[0.0008, 0.008, 0.05, 0.20], best=None, nev=0,
                profil={}, prof_x={}, done=False)


def sauve(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)


def motif(x, steps, best, libres, budget, st):
    """recherche de motif sur les indices `libres` ; renvoie (x, steps, best, evals)."""
    x = np.array(x, float)
    steps = np.array(steps, float)
    nev = 0
    TOL = [0.00005, 0.0005, 0.003, 0.0125]     # = pas initiaux / 16, en absolu
    while nev < budget:
        improved = False
        for i in libres:
            for s in (+1, -1):
                if nev >= budget:
                    break
                xt = x.copy()
                xt[i] += s * steps[i]
                c = chi2_pente(xt)
                nev += 1
                st['nev'] += 1
                if c < best - 1e-3:
                    x, best, improved = xt, c, True
                    break
            if improved:
                break
        if not improved:
            steps = steps / 2.0
            if all(steps[i] < TOL[i] for i in libres):
                return x, steps, best, nev, True
        st['x'] = list(x)
        st['steps'] = list(steps)
        st['best'] = best
        sauve(st)
    return x, steps, best, nev, False


def verdicts(st):
    prof = {float(k): v for k, v in st['profil'].items()}
    px = {float(k): v for k, v in st['prof_x'].items()}
    cmin = min(min(prof.values()), st.get('best_global', st['best']))
    c0 = prof.get(0.0)
    print("\n  --- profil sur eps1 (Planck complet) ---")
    zs = {}
    for e1 in sorted(prof):
        d = prof[e1] - cmin
        e0 = px[e1][2]
        z0 = (np.exp(e0 / e1) - 1) if abs(e1) > 1e-9 else float('nan')
        zs[e1] = z0
        print(f"    eps1 = {e1:4.2f}  chi2 = {prof[e1]:9.2f}  dchi2 = {d:6.2f}  "
              f"eps0 = {e0:+.4f}  z0 = {z0:.3f}" if np.isfinite(z0) else
              f"    eps1 = {e1:4.2f}  chi2 = {prof[e1]:9.2f}  dchi2 = {d:6.2f}  "
              f"eps0 = {e0:+.4f}  z0 = -- (pente constante)")
    d_run = (c0 - cmin) if c0 is not None else float('nan')
    if d_run >= 4.0:
        v1 = f"PLANCK DEMANDE LE RUNNING (dchi2 = {d_run:.2f} a 1 ddl -> {np.sqrt(max(d_run,0)):.2f} sigma)"
    elif d_run < 1.0:
        v1 = f"PLANCK NE DEMANDE PAS LE RUNNING (dchi2 = {d_run:.2f} -> {np.sqrt(max(d_run,0)):.2f} sigma)"
    else:
        v1 = f"INTERMEDIAIRE (dchi2 = {d_run:.2f} -> {np.sqrt(max(d_run,0)):.2f} sigma)"
    print(f"\n  VERDICT 1 (le running) : {v1}")
    if d_run < 4.0:
        print("  VERDICT 2 : NON LOCALISE — criteres 3 et 4 non evalues (critere gele).")
        return
    dans = [zs[e] for e in sorted(prof) if prof[e] - cmin <= 1.0 and np.isfinite(zs[e])]
    if not dans:
        print("  VERDICT 2 : NON LOCALISE — aucun point du profil a dchi2 <= 1 avec z0 defini.")
        return
    lo, hi = min(dans), max(dans)
    print(f"  VERDICT 2 (localisation) : z0 dans [{lo:.3f} ; {hi:.3f}] a 1 sigma")
    inter = not (hi < BANDE_RIGIDE[0] or lo > BANDE_RIGIDE[1])
    print(f"  VERDICT 3 (rigide) : bande predite {BANDE_RIGIDE} -> "
          + ("CONVERGENCE RIGIDE" if inter else "TENSION RIGIDE"))
    inter2 = not (hi < IC_LEGER[0] or lo > IC_LEGER[1])
    print(f"  VERDICT 4 (independance) : intervalle leger {IC_LEGER} -> "
          + ("CONVERGENCE INDEPENDANTE" if inter2 else "DIVERGENCE ENTRE JEUX — versee a T9"))
    if inter != inter2:
        print("  REGLE 9 : criteres 3 et 4 en desaccord -> RIEN N'EST EXPLOITE.")


if __name__ == "__main__":
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    st = charge()

    if st['valid'] is None:
        c = chi2_pente([0.1200, 3.044, 0.0, 0.0])
        st['valid'] = c
        st['nev'] += 1
        sauve(st)
        print(f"[validation] pente(0,0) = {c:.2f} vs LCDM {LCDM_REF} -> "
              f"{'OK' if abs(c - LCDM_REF) < 0.5 else 'ECHEC'}", flush=True)
    if abs(st['valid'] - LCDM_REF) >= 0.5:
        sys.exit(f"  VALIDATION ECHOUE ({st['valid']:.2f}) — rien n'est publie.")

    if st['best'] is None:
        st['best'] = chi2_pente(st['x'])
        st['nev'] += 1
        sauve(st)

    if st['phase'] == 0:
        x, steps, best, nev, fini = motif(st['x'], st['steps'], st['best'], [0, 1, 2, 3], budget, st)
        print(f"[phase1] chi2 = {best:.2f}  x = {np.round(x, 4)}  evals = {st['nev']}  "
              f"fini = {fini}", flush=True)
        if fini:
            st['phase'] = 1
            st['x0_prof'] = list(x)
            st['best_global'] = float(best)
        sauve(st)
        sys.exit(0)

    for e1 in GRILLE_E1:
        k = str(e1)
        if k in st['profil']:
            continue
        x0 = list(st.get('x0_prof', st['x']))
        x0[3] = e1
        c0 = chi2_pente(x0)
        st['nev'] += 1
        x, steps, best, nev, fini = motif(x0, [0.0008, 0.008, 0.05, 0.0], c0,
                                          [0, 1, 2], budget, st)
        st['profil'][k] = best
        st['prof_x'][k] = list(np.round(x, 6))
        sauve(st)
        print(f"[profil] eps1 = {e1}  chi2 = {best:.2f}  eps0 = {x[2]:+.4f}  "
              f"evals = {st['nev']}  fini = {fini}", flush=True)
        if not fini:
            sys.exit(0)
        break
    else:
        st['done'] = True
        sauve(st)
        verdicts(st)
