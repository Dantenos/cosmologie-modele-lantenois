#!/usr/bin/env python3
"""LE #190 EST-IL VRAI ? — TEST DE MA PROPRE AFFIRMATION PAR LES DONNEES DES AUTRES.
CRITERES PRE-ENREGISTRES (geles AVANT execution ET AVANT d'avoir les valeurs publiees,
24/08/2026). L'ordre importe : les criteres ci-dessous ne dependent d'aucun nombre, ils ont
donc ete geles pendant que la verification bibliographique tournait encore. Je ne pouvais pas
les accorder aux chiffres.

L'AFFIRMATION MISE EN JEU. Le #190 a conclu, et c'est le seul acquis qu'il revendique :
   "Dans la famille rho_m ~ a^(eps-3), eps n'est PAS identifiable par des priors comprimes."
Preuve interne : sur des donnees IDENTIQUES et un modele IDENTIQUE, quatre choix de
comptabilite (le omega_m donne a r_s, celui de R, celui de z_*, la convention de rayonnement)
deplacent eps de +0,0060 a -0,0100 -- une amplitude de 0,016 -- alors que chaque incertitude
citee vaut ~0,002. Cette preuve est interne, donc suspecte : elle ne teste que mon pipeline.

CE QUE CETTE ETUDE FAIT. Elle confronte mon affirmation aux mesures que d'AUTRES ont faites
EN VRAISEMBLANCE COMPLETE (code de Boltzmann modifie, spectres de puissance, aucun prior
comprime). Si ces mesures-la se groupent pres de zero avec une dispersion bien inferieure a
celle des mesures par priors comprimes, mon affirmation est CONFIRMEE PAR DES DONNEES QUI NE
SONT PAS LES MIENNES. Si elles se dispersent autant, elle est REFUTEE et le #190 etait
sur-enonce. Les deux issues sont ecrites ci-dessous avant de regarder.

LES CONVERSIONS, DECLAREES (chaque famille publiee parametre autre chose que notre eps) :
  (a) nu de Lambda(H)CDM       : eps = 3 nu x f,   f = rho_dm/rho_m au notre optimum LCDM.
      Le facteur f est necessaire parce que leur nu porte sur la matiere NOIRE seule.
  (b) w_dm de la matiere noire generalisee : rho_dm ~ a^(-3(1+w)), donc eps = -3 w x f.
  (c) partage Om^early / Om^geo : eps = [ln(Om^early/Om^geo)/ln(a_*)] / K_GEO.
      K_GEO n'est PAS 1. Sonde 6 (hors corpus, declaree) : dans notre famille, le Om que lit
      un ajusteur LCDM pur sur les distances tardives n'est pas l'etiquette -- il derive, et
      la conversion naive sous-estime |eps| d'un facteur CONSTANT sur toute la plage
      [-0,010 ; +0,010]. K_GEO = 0,832 est ce facteur, mesure et non suppose. Il est fige
      ici ; le critere 4 verifie qu'il est bien constant, sinon la conversion (c) tombe.

--- VALIDATIONS (si l'une echoue, la conversion concernee est RETIREE, pas rafistolee) ---
  A. f doit tomber dans [0,80 ; 0,88] (meme borne qu'au controle d'equite gele 714d6f430930).
  B. K_GEO doit etre constant a mieux que 2 % sur [-0,010 ; +0,010], recalcule ici et non
     recopie. S'il varie plus, la conversion (c) est retiree de l'etude et on le dit.
  C. Aucune valeur publiee ne peut entrer sans son incertitude. Une valeur sans barre
     d'erreur est REJETEE, quel que soit son interet.

--- CRITERES (exhaustifs, exclusifs) ---
  1. COHERENCE INTERNE DE LA FAMILLE "VRAISEMBLANCE COMPLETE". chi2 de compatibilite autour
     de leur moyenne ponderee, avec n-1 degres de liberte.
     GROUPE COHERENT si chi2/ddl <= 2,0 ; GROUPE DISPERSE sinon.
  2. DISPERSIONS COMPAREES. On rapporte l'etendue (max - min) de chaque famille :
     E_complete et E_comprimee. La famille comprimee contient les quatre nombres du #188 et
     du #190 -- donnees et modele identiques, seule la comptabilite change -- plus la valeur
     publiee de Yang, Dai & Wang (priors comprimes).
  3. VERDICT SUR L'AFFIRMATION DU #190 :
     CONFIRMEE PAR L'EXTERIEUR si le critere 1 rend GROUPE COHERENT ET E_comprimee >= 3 x
        E_complete ;
     REFUTEE si E_complete >= E_comprimee ;
     INDECIS dans tous les autres cas -- et alors le #190 garde son acquis comme enonce
        INTERNE seulement, ce qui est un recul et doit etre ecrit comme tel.
  4. CONTROLE DE LA CONVERSION (c). K_GEO recalcule sur cinq valeurs de eps ; on rapporte sa
     variation relative. > 2 % -> conversion (c) retiree (validation B).
  5. QUE DIT NOTRE PIPELINE DE LEURS VALEURS ? Pour chaque eps publie converti, on rapporte
     le Delta chi2 que NOS donnees lui assignent, dans les deux configurations que le #190 a
     declarees saines (profil parabolique verifie : 1_table_etiq et 2_table_coh).
     Si un eps publie est rejete a plus de 9 unites (3 sigma) par nos donnees dans LES DEUX,
     il est signale comme EN TENSION AVEC NOS DONNEES -- fait rapporte, jamais exploite comme
     refutation (regle 9 : nos deux configurations se contredisent deja entre elles).
  6. MOYENNE PONDEREE DE LA FAMILLE COMPLETE, avec son incertitude, et sa traduction en
     densites (Om a la recombinaison / Om aujourd'hui). C'est le nombre que le corpus n'a
     pas et qu'il ne peut pas produire lui-meme.

REGLE 6 APPLIQUEE. Cette etude cherche a confirmer une affirmation A MOI. Les substitutions
vont donc contre elle : quand une incertitude publiee est asymetrique on retient la borne qui
ELARGIT la famille complete (donc qui rend la confirmation plus difficile) ; le seuil du
critere 3 est un facteur 3 et non 2 ; et la branche REFUTEE est testee avant la branche
CONFIRMEE dans le code.
REGLE 5. Ce que j'accorde d'avance a quiconque conteste : les modeles publies ne sont pas le
notre (vide dynamique chez les uns, perturbations modifiees chez les autres), leurs donnees
different des notres et entre elles, et la conversion (c) traverse un formalisme entierement
different du notre. Cette etude ne mesure donc PAS eps. Elle mesure une DISPERSION, et c'est
tout ce qu'elle a le droit de conclure.
Regle 3 : elle REDUIT l'incertitude sur la portee du #190 ; elle ne ferme pas T10.
Usage : python3 scripts/confrontation_epsilon.py   (depuis donnees/pantheon_plus)
"""
import sys
import pathlib
import numpy as np
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilution_arbitre as D
import test_wE_v3 as T

K_GEO = 0.832
ZG = T.zg
ZFIT = np.linspace(0.01, 2.5, 200)


# ============================================================ VALEURS PUBLIEES
# Chaque entree : (etiquette, type, valeur, sigma_plus, sigma_moins, source, famille)
# type : 'nu' (Lambda(H)CDM), 'wdm' (matiere noire generalisee), 'geo' (partage Om), 'eps'
# famille : 'complete' (Boltzmann modifie + spectres) | 'comprimee' (priors de distance)
# Recopiees sans retouche. Toute valeur sans barre d'erreur est rejetee (validation C).
PUB = []


def ajoute(nom, typ, v, sp, sm, src, fam):
    PUB.append(dict(nom=nom, typ=typ, v=v, sp=abs(sp), sm=abs(sm), src=src, fam=fam))


# --- FAMILLE "VRAISEMBLANCE COMPLETE" : Boltzmann modifie + vraisemblance CMB complete.
# REGLE D'ADMISSION APPLIQUEE ET DECLAREE (elle n'etait PAS dans mes criteres geles, donc
# elle est post-hoc et doit etre visible) : n'entre ici qu'une mesure (i) verifiee A LA
# SOURCE dans cette session, (ii) a barres d'erreur BILATERALES, (iii) sur un exposant
# CONSTANT, (iv) sur un fond de type Lambda. Chaque exclusion est nommee plus bas.
#
# Tsiapi & Basilakos, MNRAS 485 (2019) 2505 = arXiv:1810.12902. CAMB modifie + Planck 2015
# TT,TE,EE+lowP. Lambda(H)CDM2 : Q = 3 nu H rho_dm, rho_dm = rho_dm,0 a^(-3(1-nu)).
ajoute("Tsiapi 2019 L(H)CDM2 Planck seul", 'nu', +0.59e-3, +1.00e-3, -1.00e-3,
       "arXiv:1810.12902 tab.1", 'complete')
ajoute("Tsiapi 2019 L(H)CDM2 joint", 'nu', -0.08e-3, +0.72e-3, -0.78e-3,
       "arXiv:1810.12902 tab.2", 'complete')
# Lambda(H)CDM1 (Q = nu H (3 rho_m + 4 rho_r)) porte le MEME exposant dominant plus des
# termes sources baryons/rayonnement : conversion approchee. On l'inclut quand meme parce
# que REGLE 6 -- elle ELARGIT la famille et rend ma confirmation PLUS DIFFICILE.
ajoute("Tsiapi 2019 L(H)CDM1 joint [conv. approchee]", 'nu', +1.20e-3, +0.60e-3, -0.50e-3,
       "arXiv:1810.12902 tab.2", 'complete')
# Kumar, Ajith & Verma, arXiv:2504.14419. CAMB modifie + Cobaya, Planck 2018 TT/TE/EE +
# lentillage PR3, DESI DR2. w_dm CONSTANT, c_s^2 fixee a 0 : le cas propre, fond seul.
# C'EST EXACTEMENT L'ARBITRE QUE T10 RECLAMAIT (Planck 2018 complet + DESI DR2).
ajoute("Kumar 2025 PL18+DESI DR2 (w_dm const.)", 'wdm', +0.00077, +0.00038, -0.00038,
       "arXiv:2504.14419 tab.1", 'complete')
# Li et al., arXiv:2510.11363, IDECAMB + Cobaya, NPIPE CamSpec + lentillage PR4, DESI DR2.
# ILCDM2 : Q = beta H rho_c, donc rho_c ~ a^(-3-beta), soit eps_dm = -beta exactement.
ajoute("Li 2025 Planck+DESI DR2+DESY5 (Q=bH rho_c)", 'epsdm', -0.0015, +0.0009, -0.0009,
       "arXiv:2510.11363", 'complete')
# Meme groupe, meme modele, DESI DR1 : predecesseur emboite. Inclus et signale, parce que
# l'exclure serait le choix confortable (sa valeur est la plus proche de zero).
ajoute("Li 2024 CMB+DESI DR1+DESY5 [emboite]", 'epsdm', -0.0003, +0.0011, -0.0011,
       "arXiv:2407.14934", 'complete')
#
# EXCLUSIONS, toutes motivees et toutes ecrites :
#  - Keil, Tutusaus & Blanchard (arXiv:2607.28326) : DEUX raisons. (1) ce n'est PAS la
#    vraisemblance complete -- coupures d'echelle 35 < l < 396, pas de lentillage, low-l en
#    EE seul. (2) surtout : leur Om^early et Om^geo sont DEUX PARAMETRES NORMALISES A
#    AUJOURD'HUI alimentant deux parties du pipeline, PAS deux densites a deux epoques.
#    Leur rapport n'a donc pas de bras de levier, et leur article ne publie aucun z_dec.
#    MA CONVERSION (c) ETAIT FONDEE SUR UN CONTRESENS : voir la note de vice au registre.
#  - Yadav et al. (arXiv:2307.05155) : bornes UNILATERALES sous prior w_dm >= 0 -- cette
#    analyse ne peut pas contraindre eps > 0 -- et marginalisation sur une vitesse du son
#    libre. Echoue la condition (ii) et la condition (iii).
#  - Ilic, Kopp, Skordis & Thomas (arXiv:2004.09572, 1802.09541) : w BINNE en 8 tranches,
#    pas un exposant constant. Echoue (iii). (Leur conclusion, citee : "no evidence for
#    nonzero EoS in any of the eight redshift bins".)
#  - Li et al. (arXiv:2506.09819) : fond PEDE et non Lambda. Echoue (iv).
#  - Kaeonikhom 2023 (eps = +0,0016 +/- 0,0014) et Wang 2018 (eps = -0,00029 +0,00028
#    -0,00025) : connues seulement de SECONDE MAIN via la revue de litterature de
#    arXiv:2505.09879. Echouent (i). L'exclusion de Wang est ANTI-regle 6 : sa barre
#    minuscule dominerait la moyenne, et l'ecarter m'arrange. On le dit ; on ne l'importe
#    pas non verifiee.

# --- FAMILLE "PRIORS COMPRIMES"
# Yang, Dai & Wang, arXiv:2505.09879 : rho_dm ~ (1+z)^(3-eps), meme convention que la notre
# mais definie sur la MATIERE NOIRE seule -> type 'epsdm'.
ajoute("Yang 2025 (priors Planck + DESI DR1)", 'epsdm', -0.0073, +0.0029, -0.0033,
       "arXiv:2505.09879", 'comprimee')
# Nos quatre nombres : donnees IDENTIQUES, modele IDENTIQUE, seule la comptabilite change.
ajoute("nous #188 etalonnage-etiquette", 'eps', +0.0060, +0.0030, -0.0020,
       "MANQUEMENTS #188", 'comprimee')
ajoute("nous #188 etalonnage-coherent", 'eps', -0.0030, +0.0010, -0.0020,
       "MANQUEMENTS #188", 'comprimee')
ajoute("nous #190 r_s direct + R etiquette", 'eps', +0.0020, +0.0020, -0.0030,
       "MANQUEMENTS #190", 'comprimee')
ajoute("nous #190 arbitre (R retire)", 'eps', -0.0100, +0.0020, -0.0020,
       "MANQUEMENTS #190", 'comprimee')


# ============================================================ machinerie
def frac_dm():
    """f = rho_dm/rho_m a notre optimum LCDM gele."""
    r0 = D.profil(0.0, D.CFG['1_table_etiq'])
    h, ob, Om = (float(v) for v in r0.x)
    return 1.0 - ob/(Om*h*h), h, ob, Om


def dc_of(Om, eps):
    zz, Ea = D.fond_arb(Om, eps)
    Ez = np.interp(ZG, zz, Ea)
    inv = 1.0/Ez
    return np.concatenate([[0], np.cumsum(0.5*(inv[1:] + inv[:-1])*np.diff(ZG))])


def om_geo(Om, eps):
    """Om que lit un ajusteur LCDM pur sur les distances tardives du modele."""
    d_mod = np.interp(ZFIT, ZG, dc_of(Om, eps))

    def cout(x):
        d_l = np.interp(ZFIT, ZG, dc_of(x, 0.0))
        k = np.sum(d_mod*d_l)/np.sum(d_l*d_l)
        return float(np.sum((d_mod - k*d_l)**2))
    return float(minimize_scalar(cout, bounds=(0.15, 0.55), method='bounded',
                                 options=dict(xatol=1e-7)).x)


def k_geo_mesure(Om=0.30, eps_list=(-0.010, -0.005, -0.002, 0.005, 0.010)):
    """K_GEO recalcule ici (validation B) : rapport entre le eps qu'on lirait sur
    ln(Om^early/Om^geo) et le eps vrai."""
    la = np.log(D.A_STAR)
    ks = []
    for e in eps_list:
        lu = np.log((Om*D.A_STAR**e)/om_geo(Om, e))/la
        ks.append(lu/e)
    ks = np.array(ks)
    return float(ks.mean()), float((ks.max() - ks.min())/ks.mean()), ks


def en_eps(p, f):
    """conversion declaree, avec la regle 6 : on retient la borne qui ELARGIT la famille."""
    if p['typ'] == 'nu':
        return 3.0*p['v']*f, 3.0*p['sp']*f, 3.0*p['sm']*f
    if p['typ'] == 'wdm':
        return -3.0*p['v']*f, 3.0*p['sm']*f, 3.0*p['sp']*f      # le signe echange les bornes
    if p['typ'] == 'epsdm':
        # eps deja dans notre convention mais defini sur la MATIERE NOIRE seule
        return p['v']*f, p['sp']*f, p['sm']*f
    if p['typ'] == 'geo':
        la = np.log(D.A_STAR)
        c = np.log(p['v'])/la/K_GEO
        return c, abs(p['sp']/p['v']/la/K_GEO), abs(p['sm']/p['v']/la/K_GEO)
    return p['v'], p['sp'], p['sm']


if __name__ == "__main__":
    import json
    print("CONFRONTATION SUR eps — le #190 tient-il hors de mon pipeline ? (criteres geles)\n")

    # ---------- validation A
    f, h0, ob0, Om0 = frac_dm()
    okA = 0.80 <= f <= 0.88
    print("  --- validation A : facteur de conversion matiere noire / matiere ---")
    print(f"     optimum LCDM gele : h = {h0:.5f}  ob = {ob0:.5f}  Om = {Om0:.5f}")
    print(f"     f = rho_dm/rho_m = {f:.4f}   -> {'OK' if okA else 'ECHEC'}")
    if not okA:
        sys.exit("     conversion non fiable : rien n'est publie.")

    # ---------- validation B / critere 4
    kbar, kvar, ks = k_geo_mesure()
    okB = kvar <= 0.02
    print("\n  --- validation B / critere 4 : constance de K_GEO ---")
    print(f"     K_GEO recalcule = {kbar:.4f}  (fige dans le docstring : {K_GEO})")
    print(f"     variation relative sur 5 valeurs de eps : {100*kvar:.3f} %  "
          f"-> {'OK' if okB else 'ECHEC : conversion (c) RETIREE'}")
    print(f"     valeurs : {np.array2string(ks, precision=4)}")

    # ---------- validation C + conversions
    print("\n  --- valeurs publiees converties en eps ---")
    rej = [p['nom'] for p in PUB if p['sp'] == 0 and p['sm'] == 0]
    for n in rej:
        print(f"     REJETEE (sans barre d'erreur, validation C) : {n}")
    utiles = [p for p in PUB if not (p['sp'] == 0 and p['sm'] == 0)]
    if not okB:
        retirees = [p['nom'] for p in utiles if p['typ'] == 'geo']
        utiles = [p for p in utiles if p['typ'] != 'geo']
        for n in retirees:
            print(f"     RETIREE (validation B) : {n}")

    CONV = []
    print(f"     {'mesure':<34s} {'famille':<10s} {'eps':>10s} {'sigma+':>9s} {'sigma-':>9s}")
    for p in utiles:
        e, sp, sm = en_eps(p, f)
        CONV.append(dict(p, eps=e, esp=sp, esm=sm))
        print(f"     {p['nom']:<34s} {p['fam']:<10s} {e:+10.5f} {sp:9.5f} {sm:9.5f}")

    CPL = [c for c in CONV if c['fam'] == 'complete']
    CPR = [c for c in CONV if c['fam'] == 'comprimee']

    # ---------- critere 1
    print("\n  --- critere 1 : coherence interne de la famille VRAISEMBLANCE COMPLETE ---")
    # regle 6 : on prend la borne qui ELARGIT, donc la PLUS GRANDE des deux
    sig = np.array([max(c['esp'], c['esm']) for c in CPL])
    val = np.array([c['eps'] for c in CPL])
    w = 1.0/sig**2
    mu = float(np.sum(w*val)/np.sum(w))
    smu = float(1.0/np.sqrt(np.sum(w)))
    chi2 = float(np.sum(((val - mu)/sig)**2))
    ddl = max(len(val) - 1, 1)
    coherent = chi2/ddl <= 2.0
    print(f"     n = {len(val)}   moyenne ponderee = {mu:+.5f} +/- {smu:.5f}")
    print(f"     chi2 = {chi2:.3f} pour {ddl} ddl  ->  chi2/ddl = {chi2/ddl:.3f}  "
          f"-> {'GROUPE COHERENT' if coherent else 'GROUPE DISPERSE'}")

    # ---------- critere 2
    print("\n  --- critere 2 : dispersions comparees ---")
    E_cpl = float(max(val) - min(val))
    vpr = np.array([c['eps'] for c in CPR])
    E_cpr = float(max(vpr) - min(vpr))
    print(f"     famille COMPLETE  ({len(val)} mesures) : etendue = {E_cpl:.5f}   "
          f"[{min(val):+.5f} ; {max(val):+.5f}]")
    print(f"     famille COMPRIMEE ({len(vpr)} mesures) : etendue = {E_cpr:.5f}   "
          f"[{min(vpr):+.5f} ; {max(vpr):+.5f}]")
    print(f"     rapport E_comprimee / E_complete = {E_cpr/E_cpl:.2f}")

    # ---------- critere 3 (regle 6 : la branche REFUTEE est testee d'abord)
    print("\n  --- critere 3 : VERDICT SUR L'AFFIRMATION DU #190 ---")
    if E_cpl >= E_cpr:
        v3 = ("REFUTEE — la famille en vraisemblance complete se disperse autant ou plus "
              "que celle par priors comprimes ; le #190 etait sur-enonce")
    elif coherent and E_cpr >= 3.0*E_cpl:
        v3 = ("CONFIRMEE PAR L'EXTERIEUR — les mesures en vraisemblance complete se "
              "groupent, celles par priors comprimes se dispersent d'un facteur "
              f"{E_cpr/E_cpl:.1f}")
    else:
        v3 = ("INDECIS — le #190 garde son acquis comme enonce INTERNE seulement. "
              "C'est un recul par rapport a ce qu'il revendiquait")
    print(f"     {v3}")

    # ---------- critere 5
    print("\n  --- critere 5 : que disent NOS donnees de leurs valeurs ? ---")
    print("     (Delta chi2 contre le minimum de chaque configuration saine du #190)")
    base = {k: D.mesure(D.CFG[k]) for k in ('1_table_etiq', '2_table_coh')}
    for k, m in base.items():
        print(f"     rappel {k} : minimum a eps = {m['eps']:+.5f}, chi2 = {m['chi2']:.3f}")
    tension = []
    for c in CPL:
        d = {}
        for k, m in base.items():
            d[k] = float(D.profil(round(c['eps'], 5), D.CFG[k]).fun - m['chi2'])
        t = all(x > 9.0 for x in d.values())
        if t:
            tension.append(c['nom'])
        print(f"     {c['nom']:<34s} eps = {c['eps']:+.5f}   "
              f"Dchi2 etiq = {d['1_table_etiq']:+7.2f}   coh = {d['2_table_coh']:+7.2f}"
              f"   {'EN TENSION AVEC NOS DONNEES' if t else ''}")
    if tension:
        print("     -> fait rapporte, JAMAIS exploite comme refutation (regle 9 : nos deux")
        print("        configurations se contredisent deja entre elles).")

    # ---------- critere 6
    print("\n  --- critere 6 : le nombre que le corpus ne peut pas produire lui-meme ---")
    rap = D.A_STAR**mu
    print(f"     eps (vraisemblance complete, moyenne ponderee) = {mu:+.5f} +/- {smu:.5f}")
    print(f"     zero est a {abs(mu)/smu:.2f} sigma")
    print(f"     Om(recombinaison)/Om(aujourd'hui) = {rap:.5f}, soit la matiere "
          f"d'aujourd'hui {100*(1/rap - 1):+.3f} %")
    print(f"     (discriminant scelle de T9 : 1,70 % ; notre #188 coherent : -2,1 %)")

    sortie = dict(f=f, K_GEO_mesure=kbar, K_GEO_variation=kvar,
                  complete=[{q: c[q] for q in ('nom', 'eps', 'esp', 'esm', 'src')}
                            for c in CPL],
                  comprimee=[{q: c[q] for q in ('nom', 'eps', 'esp', 'esm', 'src')}
                             for c in CPR],
                  moyenne=mu, sigma_moyenne=smu, chi2_coherence=chi2, ddl=ddl,
                  etendue_complete=E_cpl, etendue_comprimee=E_cpr, verdict=v3,
                  tension=tension)
    pathlib.Path(__file__).resolve().parent.parent.joinpath(
        "registres", "confrontation_epsilon.json").write_text(
        json.dumps(sortie, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
        newline="\n")
    print("\n  resultats verses dans registres/confrontation_epsilon.json")
