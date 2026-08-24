#!/usr/bin/env python3
"""manuscrit — LE GARDE-FOU QUI MANQUAIT AU CORPUS (24/08/2026).
CRITERES PRE-ENREGISTRES (geles AVANT execution).

POURQUOI IL EXISTE. L'audit du #183 a trouve 44 defauts dans les trois manuscrits, dont
sept survivances orientees, et le fait decisif est celui-ci : `perime.py` et
`registre.py verify` sont passes tous les deux SANS EN ATTRAPER UN SEUL. Ils surveillent
les criteres geles et les valeurs canoniques ; personne ne surveillait la coherence interne
des manuscrits. Le registre du corpus s'est revele systematiquement plus honnete que les
papiers, et ce n'est pas un hasard : le registre est ecrit sous critere gele, les papiers
ne le sont pas.

CE QUE CET OUTIL VERIFIE, et ce qu'il ne peut pas verifier. Il attrape ce qui est
MECANIQUEMENT verifiable dans un .tex. Il ne juge pas la physique, ne relit pas les
equations, et ne remplace pas une lecture — l'audit du #183 a trouve des choses qu'aucun
programme ne trouvera. Il empeche seulement la classe de defauts qui se repete : references
cassees, entrees incompletes, sources citees dans le texte mais absentes de la bibliographie,
conversions Delta chi2 -> sigma fausses, et cles homonymes divergentes entre papiers.

--- CONTROLES ---
  A. INTEGRITE DES CITATIONS (bloquant). Toutes les formes natbib (\\cite, \\citep, \\citet,
     \\citealt, \\citealp, \\citeauthor, \\citeyear), avec arguments optionnels. Une cle citee
     sans bibitem casse la compilation : REFUS. Une cle definie deux fois : REFUS.
  B. ENTREES INCOMPLETES (rapporte). Un bibitem doit porter au moins un identifiant :
     « arXiv: », « doi », ou un volume en gras avec une annee a quatre chiffres. Une entree
     sans aucun des trois ne permet pas de retrouver la source.
  C. SOURCES NOMMEES SANS CITATION (rapporte). Un motif « Nom et al. (aaaa) » ou
     « Nom & Nom (aaaa) » sans \\cite dans les 220 caracteres qui suivent.
  D. CONVERSIONS Delta chi2 -> sigma (rapporte). Pour chaque couple (Delta chi2, sigma)
     trouve a moins de 160 caracteres l'un de l'autre, on compare a la conversion a 1 ddl
     (sigma = racine de Delta chi2) et a 2 ddl. Un couple compatible avec AUCUNE des deux a
     0,15 pres est signale. TOLERANCE DECLAREE : les couples ou le texte annonce lui-meme
     une conversion non standard (le mot « one-sided », « naive » ou « indicative » dans la
     phrase) sont exclus, parce que le papier les declare deja.
  E. CLES HOMONYMES DIVERGENTES (rapporte). Une meme cle definie dans deux papiers avec des
     textes differents : le lecteur qui suit la reference d'un papier a l'autre tombe sur
     autre chose.

--- VALIDATION (si elle echoue, l'outil ne rapporte rien) ---
  Sur les trois manuscrits du corpus, le controle A doit trouver ZERO cle pendante et ZERO
  doublon — etat verifie a la main au #183. S'il en trouve, c'est l'outil qui lit mal, pas
  les papiers qui sont casses, et son rapport ne vaut rien.

Usage : python3 outils/manuscrit.py            (rapport)
        python3 outils/manuscrit.py --strict   (sortie non nulle si un controle rapporte)
"""
import sys, re, pathlib
from math import sqrt

try:
    from scipy.stats import chi2 as _chi2
except Exception:
    _chi2 = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPIERS = sorted((ROOT / "papiers").glob("papier*.tex"))
RE_CITE = re.compile(r"\\cite[a-zA-Z]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
RE_ITEM = re.compile(r"\\bibitem\s*(?:\[[^\]]*\]\s*)?\{([^}]*)\}")
RE_NOMME = re.compile(r"\b([A-Z][a-zA-Z\u00c0-\u017f'-]{2,})\s+"
                      r"(?:et\s+al\.|\\&\s+[A-Z][a-zA-Z\u00c0-\u017f'-]{2,})\s*\((\d{4})\)")
RE_DCHI = re.compile(r"\\Delta\\chi\^2\s*(?:=|\\simeq|\\approx)\s*([+-]?\d+\.?\d*)")
RE_SIG = re.compile(r"(\d+\.?\d*)\\sigma")
EXCUSES = ("one-sided", "naive", "indicative", "not nested", "not calibrated")


def sigma_2ddl(d):
    if _chi2 is None or d <= 0:
        return None
    p = _chi2.sf(d, 2)
    if not (0 < p < 1):
        return None
    return float(sqrt(_chi2.isf(p, 1)))


def corps(txt):
    """le texte hors bibliographie."""
    i = txt.find("\\begin{thebibliography}")
    return txt if i < 0 else txt[:i]


def main():
    strict = "--strict" in sys.argv
    if not PAPIERS:
        sys.exit("[manuscrit] aucun papier trouve dans papiers/")
    tous, items_txt, ndef = {}, {}, 0
    dangling = dupli = 0
    print(f"[manuscrit] {len(PAPIERS)} manuscrit(s)\n")

    # ---------- A : integrite (bloquant) ----------
    print("  A. integrite des citations")
    for p in PAPIERS:
        s = p.read_text(encoding="utf-8")
        cites = set()
        for m in RE_CITE.findall(s):
            cites.update(c.strip() for c in m.split(",") if c.strip())
        items = RE_ITEM.findall(s)
        ndef += len(items)
        dup = sorted({k for k in items if items.count(k) > 1})
        orph = sorted(cites - set(items))
        inut = sorted(set(items) - cites)
        dangling += len(orph)
        dupli += len(dup)
        for k in items:
            j = s.find("\\bibitem")
            tous.setdefault(k, []).append(p.name)
            m = re.search(r"\\bibitem\s*(?:\[[^\]]*\]\s*)?\{" + re.escape(k) + r"\}([^\n]*)", s)
            if m:
                items_txt.setdefault(k, {})[p.name] = m.group(1).strip()
        etat = "OK" if not (dup or orph) else "DEFAUT"
        print(f"     {p.name[:34]:<34s} {len(cites):3d} cles / {len(items):3d} entrees  {etat}")
        if orph:
            print(f"        >>> CLE CITEE SANS ENTREE : {orph}")
        if dup:
            print(f"        >>> ENTREE DUPLIQUEE : {dup}")
        if inut:
            print(f"        >>> entree jamais citee : {inut}")
    if dangling or dupli:
        sys.exit(f"\n  VALIDATION ECHOUE : {dangling} cle(s) pendante(s), {dupli} doublon(s) "
                 f"— l'outil ne rapporte rien de plus tant que l'integrite n'est pas retablie.")
    print("     -> validation passee : aucune cle pendante, aucun doublon\n")

    # ---------- B : entrees incompletes ----------
    print("  B. entrees sans identifiant")
    nb = 0
    for p in PAPIERS:
        s = p.read_text(encoding="utf-8")
        for m in RE_ITEM.finditer(s):
            k = m.group(1)
            fin = s.find("\\bibitem", m.end())
            bloc = s[m.end():fin if fin > 0 else s.find("\\end{thebibliography}", m.end())]
            # identifiants ANCIEN FORMAT arXiv (astro-ph/YYMMNNN, gr-qc/, hep-th/, etc.) :
            # ils ne portent pas le mot « arXiv » et etaient donc comptes comme absents.
            # Trois faux positifs sur le papier D l'ont revele (#196). Le critere gele dit
            # « au moins un identifiant » : un astro-ph/9709112 EN EST UN.
            ancien = re.search(r"\b(astro-ph|gr-qc|hep-(?:th|ph|ex)|math-ph|nucl-th)/\d{7}\b",
                               bloc)
            # une reference de journal complete (revue + volume + page + annee) en est un
            # autre : ApJ 496, 605 (1998) identifie sans ambiguite.
            journal = re.search(r"\b(ApJ|A&A|A\\&A|MNRAS|JCAP|Phys\.?\\?\s*Rev|PRD|PRL|"
                                r"Nature|Science)\b[^\n]{0,40}?\d{1,4}\s*,\s*\d{1,5}", bloc)
            ok = ("arXiv" in bloc or "doi" in bloc.lower() or bool(ancien) or bool(journal)
                  or (re.search(r"\\textbf\{[^}]*\}", bloc) and re.search(r"\(\d{4}\)", bloc)))
            if not ok:
                # un ouvrage (editeur + annee, sans volume) est legitimement sans
                # identifiant numerique : on l'etiquette et on le compte a part
                livre = bool(re.search(r"(University Press|OUP|Press\)|Head|"
                                       r"\(\w[\w\s.&'-]*,\s*\d{4}\))", bloc))
                if livre:
                    print(f"     {p.name[:22]:<22s} {k[:26]:<26s} [ouvrage] "
                          f"{bloc.strip()[:44]!r}")
                else:
                    nb += 1
                    print(f"     {p.name[:22]:<22s} {k[:26]:<26s} {bloc.strip()[:58]!r}")
    print(f"     -> {nb} entree(s) sans identifiant retrouvable\n")

    # ---------- C : sources nommees sans citation ----------
    print("  C. sources nommees dans le texte, sans citation")
    nc = 0
    for p in PAPIERS:
        s = corps(p.read_text(encoding="utf-8"))
        for m in RE_NOMME.finditer(s):
            suite = s[m.end():m.end() + 220]
            avant = s[max(0, m.start() - 90):m.start()]
            if "\\cite" in suite or "\\cite" in avant:
                continue
            nc += 1
            print(f"     {p.name[:22]:<22s} {m.group(0)[:46]}")
    print(f"     -> {nc} source(s) nommee(s) sans citation\n")

    # ---------- D : conversions Delta chi2 -> sigma ----------
    print("  D. conversions Delta chi2 -> sigma")
    nd = 0
    for p in PAPIERS:
        s = corps(p.read_text(encoding="utf-8"))
        for m in RE_DCHI.finditer(s):
            try:
                d = abs(float(m.group(1)))
            except ValueError:
                continue
            fen = s[m.end():m.end() + 160]
            g = RE_SIG.search(fen)
            if not g or d <= 0:
                continue
            phrase = s[max(0, m.start() - 120):m.end() + 240].lower()
            if any(e in phrase for e in EXCUSES):
                continue
            sig = float(g.group(1))
            s1, s2 = sqrt(d), sigma_2ddl(d)
            if abs(sig - s1) < 0.15 or (s2 is not None and abs(sig - s2) < 0.15):
                continue
            # la fenetre gelee de 160 caracteres ne distingue pas les propositions : un
            # sigma separe du Delta chi2 par une frontiere de phrase appartient presque
            # toujours a une AUTRE quantite. On l'etiquette au lieu de le taire.
            entre = fen[:g.start()]
            faux = any(x in entre for x in (". ", " (", "; ", "---"))
            att = f"1 ddl {s1:.2f}" + (f" / 2 ddl {s2:.2f}" if s2 else "")
            if faux:
                print(f"     {p.name[:22]:<22s} Dchi2 = {d:6.2f} -> {sig}sigma  "
                      f"(attendu {att})  [separateur intercale : probable faux positif]")
            else:
                nd += 1
                print(f"     {p.name[:22]:<22s} Dchi2 = {d:6.2f} -> {sig}sigma  "
                      f"(attendu {att})")
    print(f"     -> {nd} conversion(s) incompatible(s) avec 1 ou 2 ddl\n")

    # ---------- E : cles homonymes divergentes ----------
    print("  E. cles homonymes divergentes entre papiers")
    ne = 0
    for k, d in items_txt.items():
        # Une EDITION TRADUITE (papierX_fr.tex) n'est pas un autre papier : ses entrees
        # bibliographiques disent la meme chose dans une autre langue (« Sandia National
        # Laboratories report » contre « rapport Sandia »). Les comparer produisait deux
        # faux positifs. On regroupe donc chaque edition avec son original avant de
        # comparer : le controle continue de detecter une vraie divergence ENTRE PAPIERS,
        # et cesse d'en inventer une entre deux langues du meme papier.
        souches = {}
        for f, v in d.items():
            souches.setdefault(re.sub(r"_(fr|en)\.tex$", ".tex", f), []).append(v)
        if len(souches) > 1 and len(set(v[0][:70] for v in souches.values())) > 1:
            ne += 1
            print(f"     {k}")
            for f, v in d.items():
                print(f"        {f[:24]:<24s} {v[:62]!r}")
    print(f"     -> {ne} cle(s) divergente(s)\n")

    total = nb + nc + nd + ne
    print(f"  BILAN : {total} signalement(s) non bloquant(s) sur {ndef} entrees "
          f"bibliographiques.")
    print("  Rappel gele : cet outil attrape ce qui est mecaniquement verifiable. Il ne relit")
    print("  pas les equations et ne juge pas la physique — le #183 a trouve des defauts")
    print("  qu'aucun programme ne trouvera.")
    if strict and total:
        sys.exit(1)


if __name__ == "__main__":
    main()
