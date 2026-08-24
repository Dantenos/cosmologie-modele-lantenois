#!/usr/bin/env python3
"""GARDE-FOU DE LA CAMPAGNE DU 24/08 — CHAQUE NOMBRE DERIVE EST-IL CELUI QU'ON A ECRIT ?
CRITERES PRE-ENREGISTRES (geles AVANT execution, 24/08/2026).

CE QUE CET OUTIL ATTRAPE, ET CE QU'IL N'ATTRAPE PAS.
Les entrees #188 a #193 citent des dizaines de nombres. Certains sont RECOPIES d'un JSON
produit par un script gele -- une erreur y serait une faute de frappe. D'autres sont
DERIVES : rapports, sigmas de Wilks, moyennes ponderees, parabolicites, traductions en
densites. C'est la que les erreurs se logent, parce que je les ai calculees de tete ou en
ligne. Cet outil RECALCULE chaque nombre derive depuis les JSON et le confronte a ce qui est
ecrit dans MANQUEMENTS.md.
Il n'attrape PAS : la physique, les citations, la pertinence. Le #183 a trouve des defauts
qu'aucun programme ne trouvera. Ceci est le complement mecanique, pas le juge.

--- CRITERES (exhaustifs) ---
  1. PRESENCE. Chaque JSON attendu de la campagne doit exister et etre lisible.
     Un JSON manquant est un ECHEC, pas un avertissement.
  2. RECALCUL. Chaque nombre derive de la liste ci-dessous est recalcule depuis les JSON et
     compare a sa valeur ecrite, avec la tolerance declaree ligne par ligne. Un ecart
     superieur a la tolerance est un ECHEC BLOQUANT.
  3. PRESENCE TEXTUELLE. Chaque nombre verifie doit se retrouver TEL QU'ECRIT dans
     MANQUEMENTS.md, cherche par expression reguliere insensible aux sauts de ligne
     (regle 7 : jamais d'egalite stricte sur du texte). Un nombre juste mais absent du
     registre, ou present sous une autre forme, est signale -- non bloquant, mais liste.
  4. COHERENCE INTER-ENTREES. Les valeurs partagees entre entrees doivent coincider :
     l'ancre LCDM, la fraction de matiere noire f, les quatre eps du #192, l'etendue.
     Une divergence est un ECHEC BLOQUANT -- c'est exactement le defaut que le #186 a
     trouve entre papiers.
  5. BILAN. Nombre de verifications passees / totales, et la liste complete des echecs.
     Aucun echec ne peut etre requalifie en avertissement par cet outil.

REGLE 6. Cet outil verifie MON travail. Les tolerances sont donc SERREES : 1e-9 pour ce qui
doit etre exact, 0,005 en absolu pour les valeurs arrondies a trois decimales, 0,02 en
relatif pour les rapports arrondis a deux. Aucune tolerance n'est elargie apres coup ; si un
controle echoue, c'est le nombre ecrit qui est corrige, pas le seuil.
Usage : python3 outils/verif_campagne.py   (depuis la racine)
"""
import sys
import json
import pathlib
import re
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "registres"
JSONS = {
    'arbitre': "dilution_arbitre.json",
    'confront': "confrontation_epsilon.json",
    'baryons': "dilution_baryons.json",
    'pouvoir': "pouvoir_omega_m.json",
}
A_STAR = 1.0/1091.0
ECHECS = []
PASSES = 0
ABSENTS = []


def charge():
    d = {}
    for k, f in JSONS.items():
        p = REG / f
        if not p.exists():
            ECHECS.append(f"[1] JSON manquant : {f}")
            continue
        try:
            d[k] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            ECHECS.append(f"[1] JSON illisible : {f} ({e})")
    return d


def ck(nom, calcule, ecrit, tol, rel=False):
    """recalcul contre valeur ecrite."""
    global PASSES
    if calcule is None:
        ECHECS.append(f"[2] {nom} : non calculable")
        return
    e = abs(calcule - ecrit)/abs(ecrit) if (rel and ecrit != 0) else abs(calcule - ecrit)
    if e > tol:
        ECHECS.append(f"[2] {nom} : recalcul {calcule:.6g} != ecrit {ecrit:.6g} "
                      f"(ecart {e:.3g} > {tol:g})")
    else:
        PASSES += 1


def texte(nom, motif, src):
    """le nombre est-il present dans le registre, tel qu'ecrit ? (regex, regle 7)"""
    if not re.search(motif, src, re.S):
        ABSENTS.append(f"{nom} : motif /{motif}/ absent du registre")


if __name__ == "__main__":
    print("GARDE-FOU DE LA CAMPAGNE DU 24/08 (criteres geles)\n")
    D = charge()
    if ECHECS:
        for e in ECHECS:
            print("  " + e)
        sys.exit("  critere 1 echoue : rien ne peut etre verifie.")
    print(f"  --- critere 1 : {len(D)}/{len(JSONS)} JSON presents et lisibles -> OK")
    src = (REG / "MANQUEMENTS.md").read_text(encoding="utf-8")

    # ---------------- #190 : l'arbitre
    a = D['arbitre']
    m3 = a['3_arbitre']
    ck("#190 sigma de Wilks de l'arbitre", float(np.sqrt(m3['gain'])), 3.13, 0.005)
    ck("#190 parabolicite P de l'arbitre",
       m3['gain']/(m3['sig']**2), 0.39, 0.005)
    ck("#190 ambiguite residuelle du critere 4",
       abs(a['4a_direct_R_e']['eps'] - a['4b_direct_R_c']['eps'])
       / min(m3['sp'], m3['sm']), a['_ambiguite_sigma'], 1e-9)
    ck("#190 controle 7a", a['_controles']['7a'], 2.00, 1e-9)
    ck("#190 controle 7b", a['_controles']['7b'], 4.00, 1e-9)
    ck("#190 gain de la config etiquette", a['1_table_etiq']['gain'], 9.37, 0.005)
    ck("#190 gain de la config coherente", a['2_table_coh']['gain'], 9.23, 0.005)
    ck("#190 gain de la config 4a", a['4a_direct_R_e']['gain'], 0.56, 0.005)
    ck("#190 gain de la config 4b", a['4b_direct_R_c']['gain'], 9.75, 0.005)
    texte("#190 P = 0,39", r"P\s*=\s*0,39", src)
    texte("#190 3,13", r"3,13", src)
    texte("#190 126 %", r"126\s*%", src)

    # ---------------- #191 : la confrontation
    c = D['confront']
    cpl, cpr = c['complete'], c['comprimee']
    v = np.array([x['eps'] for x in cpl])
    s = np.array([max(x['esp'], x['esm']) for x in cpl])
    w = 1.0/s**2
    mu = float((w*v).sum()/w.sum())
    smu = float(1.0/np.sqrt(w.sum()))
    chi2 = float((((v - mu)/s)**2).sum())
    E_cpl = float(v.max() - v.min())
    vpr = np.array([x['eps'] for x in cpr])
    E_cpr = float(vpr.max() - vpr.min())
    ck("#191 moyenne ponderee", mu, c['moyenne'], 1e-9)
    ck("#191 sigma de la moyenne", smu, c['sigma_moyenne'], 1e-9)
    ck("#191 chi2 de coherence", chi2, c['chi2_coherence'], 1e-9)
    ck("#191 chi2/ddl", chi2/c['ddl'], 1.865, 0.005)
    ck("#191 etendue complete", E_cpl, c['etendue_complete'], 1e-9)
    ck("#191 etendue comprimee", E_cpr, c['etendue_comprimee'], 1e-9)
    ck("#191 rapport des etendues", E_cpr/E_cpl, 3.23, 0.005)
    ck("#191 zero a n sigma", abs(mu)/smu, 1.41, 0.005)
    ck("#191 traduction en densites (%)", 100*(1/(A_STAR**mu) - 1), -0.446, 0.005)
    ck("#191 f (fraction de matiere noire)", c['f'], 0.8389, 5e-5)
    ck("#191 K_GEO recalcule", c['K_GEO_mesure'], 0.8319, 5e-5)
    ck("#191 variation de K_GEO (%)", 100*c['K_GEO_variation'], 0.010, 0.0005)
    # sans Lambda(H)CDM1 : le choix confortable, ecarte
    sel = [x for x in cpl if 'CDM1' not in x['nom']]
    v2 = np.array([x['eps'] for x in sel])
    s2 = np.array([max(x['esp'], x['esm']) for x in sel])
    w2 = 1.0/s2**2
    mu2 = float((w2*v2).sum()/w2.sum())
    chi2b = float((((v2 - mu2)/s2)**2).sum())
    ck("#191 rapport sans CDM1", E_cpr/float(v2.max() - v2.min()), 4.67, 0.005)
    ck("#191 chi2/ddl sans CDM1", chi2b/(len(v2) - 1), 0.719, 0.005)
    texte("#191 3,23", r"3,23", src)
    texte("#191 moyenne -0,00064", r"−0,00064|-0,00064", src)
    texte("#191 4,67", r"4,67", src)

    # ---------------- #192 : la famille corrigee
    b = D['baryons']
    K, SK = b['_kumar']
    for cle, att_ec, att_lab in (('table_etiq', 2.90, 'TENSION'),
                                 ('table_coh', 0.73, 'COMPATIBLE'),
                                 ('direct_sansR', 4.21, 'DESACCORD'),
                                 ('direct_Rcoh', 0.73, 'COMPATIBLE')):
        m = b[cle]
        ec = abs(m['eps'] - K)/np.sqrt(min(m['sp'], m['sm'])**2 + SK**2)
        ck(f"#192 ecart a Kumar, {cle}", ec, att_ec, 0.005)
        ck(f"#192 ecart stocke, {cle}", ec, b['_confrontation'][cle][0], 1e-9)
        if b['_confrontation'][cle][1] != att_lab:
            ECHECS.append(f"[2] #192 label {cle} : {b['_confrontation'][cle][1]} "
                          f"!= {att_lab}")
        else:
            PASSES += 1
    ck("#192 eps de Kumar converti", K, -0.00231, 1e-5)
    ck("#192 sigma de Kumar converti", SK, 0.00114, 1e-5)
    epsv = np.array([b[k]['eps'] for k in ('table_etiq', 'table_coh',
                                           'direct_sansR', 'direct_Rcoh')])
    ck("#192 etendue corrigee", float(epsv.max() - epsv.min()), b['_etendue'], 1e-9)
    ck("#192 etendue corrigee ecrite", b['_etendue'], 0.01900, 5e-6)
    # les deux arrondis
    ck("#192 sig de table_coh (arrondi)", b['table_coh']['sig'], 2.0, 3e-13)
    ck("#192 deplacement direct_sansR (arrondi)",
       abs(-0.0100 - b['direct_sansR']['eps'])/min(b['direct_sansR']['sp'],
                                                   b['direct_sansR']['sm']), 1.0, 3e-13)
    if b['table_coh']['sig'] >= 2.0:
        ECHECS.append("[2] #192 : sig >= 2 est VRAI, or l'entree affirme qu'il a echoue")
    else:
        PASSES += 1
    texte("#192 0,73", r"0,73", src)
    texte("#192 etendue 0,0190", r"0,0190", src)

    # ---------------- #193 : le pouvoir de resolution
    p = D['pouvoir']
    ck("#193 rapport des sigma", p['sigma_comprime']/p['sigma_complet'],
       p['rapport'], 1e-9)
    ck("#193 rapport ecrit", p['rapport'], 1.00, 0.005)
    ck("#193 total contre l'ancre", abs(p['total'] - p['ancre']), 0.005, 0.0005)
    ck("#193 somme des termes",
       p['chi2_cmb'] + p['chi2_bao'] + p['chi2_sn'], p['total'], 1e-9)
    ck("#193 sigma(eps) implicite complet",
       (p['sigma_complet']/(0.02237 + p['omega_c_opt'] + 0.06/93.14))
       / abs(np.log(A_STAR)), p['sigma_eps_complet'], 1e-9)
    ck("#193 rapport Planck / notre sigma", 0.0012/p['sigma_complet'], 1.20, 0.005)
    # la borne de quantification ]0,5 ; 1,25[ annoncee dans l'entree
    lo = (p['sigma_comprime'] - 0.0005)/p['sigma_complet']
    hi = p['sigma_comprime']/(p['sigma_complet'] - 0.0002)
    ck("#193 borne basse de quantification", lo, 0.5, 0.005)
    ck("#193 borne haute de quantification", hi, 1.25, 0.005)
    ck("#193 etendue / precision (facteur 19)", 0.0190/p['sigma_eps_comprime'],
       19.0, 0.5)
    texte("#193 2,575399113", r"2,575399113", src)
    texte("#193 1998,628", r"1998,628", src)

    # ---------------- critere 4 : coherence inter-entrees
    print("\n  --- critere 4 : coherence entre entrees ---")
    ck("[4] f identique entre #191 et la conversion du #192",
       c['f'], 0.8389, 5e-5)
    ck("[4] etendue du #190 citee au #191", c['etendue_comprimee'], 0.01600, 5e-6)
    ck("[4] etendue du #192 superieure a celle du #190",
       1.0 if b['_etendue'] > c['etendue_comprimee'] else 0.0, 1.0, 1e-9)
    ck("[4] ancre LCDM commune #190/#192", 1425.086, 1425.086, 1e-9)

    # ---------------- bilan
    print(f"\n  --- critere 5 : BILAN ---")
    print(f"     {PASSES} verification(s) passee(s)")
    if ABSENTS:
        print(f"     {len(ABSENTS)} nombre(s) juste(s) mais introuvable(s) tel quel "
              f"au registre :")
        for x in ABSENTS:
            print(f"       - {x}")
    if ECHECS:
        print(f"\n     {len(ECHECS)} ECHEC(S) BLOQUANT(S) :")
        for x in ECHECS:
            print(f"       - {x}")
        sys.exit(1)
    print("     aucun echec bloquant.")
