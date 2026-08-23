"""CHANTIER 3 — eps(nu) : la hauteur de pic peut-elle sauver la lecture pic sans horloge ?
CRITERES PRE-ENREGISTRES : (1) le profil conditionnel exact est decompose en ses deux formes
(terme psi ~ xi, terme courbure ~ -lap xi) SANS formule d'ajustement ; la conclusion n'est
retenue que si elle depend uniquement du SIGNE (x - gamma nu) > 0, etabli par BBKS pour tout
pic de hauteur finie. (2) Aucune carte nu->beta chiffree n'est emise sans gamma(M) calcule
depuis un vrai P(k) — refus explicite sinon. (3) Approximation locale en loi de puissance
declaree : n_eff(M*) = -2.03 (E6, gele 5a8d4094)."""
import numpy as np
n = -2.0255                    # n_eff(M*), M* = 6.25e12 Msun (E6)
a, b = (n+3)/3, (n+5)/3        # exposants exacts des deux formes en delta(M) ~ M^-eps
print("Profil moyen conditionne (gaussien, EXACT) : delta(r) = C1(nu,x)*psi + C2(nu,x)*(-R*^2 lap psi)/3")
print("  avec C2 proportionnel a (x - gamma nu)/(1-gamma^2) ; BBKS : x_bar > gamma nu pour tout nu fini,")
print("  et l'ecart croit quand nu decroit. Donc le poids w de la seconde forme est >= 0, croissant a bas nu.")
print(f"  Formes en masse : psi-> M^-{a:.3f} (eps_pic = {a:.3f}) ; courbure -> M^-{b:.3f} (eps = {b:.3f})")
print()
print("  beta(w) = 2 / (3 [a(1-w)+bw])  — MONOTONE DECROISSANTE en w :")
print(f"  {'w':>6s} {'eps_eff':>8s} {'beta':>7s}")
for w in [0.0,0.1,0.25,0.5,1.0]:
    e=a*(1-w)+b*w; print(f"  {w:>6.2f} {e:>8.3f} {2/(3*e):>7.2f}")
print()
print("VERDICT (independant de la formule x_bar, par le seul signe) :")
print(f"  beta_pic(nu) <= beta_pic(nu->inf) = {2/(3*a):.2f}  pour TOUT nu.")
print(f"  Mesure : beta = 2,42-2,60.  La liberte en nu est un SENS UNIQUE : elle eloigne du mesure.")
print("  -> la lecture pic ne peut atteindre 2,42 a M* pour AUCUNE hauteur de pic sans horloge.")
print("  -> chantier 3 se referme SUR le chantier 1 : sous la lecture pic, kappa > 0 est requis,")
print("     et kappa est desormais kappa(x0, sigma) — calculable, plus libre (papier A, revision).")
print()
print("REFUS (critere 2) : pas de carte nu->beta chiffree sans gamma(M) issu d'un P(k) complet ;")
print("  la formule d'ajustement BBKS pour x_bar n'est PAS utilisee. Transposition complete = E-suite,")
print("  ingredients nommes : P(k) EH ou CAMB -> sigma_0,1,2 -> gamma, R*, x_bar(nu) exacts.")
