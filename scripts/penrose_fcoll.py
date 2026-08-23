#!/usr/bin/env python3
"""GRAND LIVRE DE PENROSE (papier B, section 3) — f_coll(>M_cut) et R selon la masse de graine.
CRITERES PRE-ENREGISTRES (geles avant execution, 23/08/2026).

Le paragraphe (ii)-(iii) du papier B chiffrait le cout par niveau avec la coupure GSL retiree
par #52 (M_cut = 2,5e14 Msun) : f_coll = 0,039, O(25), R ~ 10^7,6. Ce script recalcule ces
trois quantites dans la machinerie de gradient_v2.py (Press-Schechter, spectre Planck 2018,
volume implicite du papier B : 6,225e12 (Mpc/h)^3, convention.py) pour :
  - la coupure retiree (2,5e14), en VALIDATION ;
  - la route analytique adoptee par B en revision (#52 : M_cut = 3,0e12) ;
  - la route simulation (#80 : 2,0e15 / 5,6e15 / 1,8e16), que B ne chiffre pas.
f_coll(>M) = erfc(delta_c / (sqrt(2) sigma(M))) (fraction de masse Press-Schechter) ;
R = n(>M) x V_B.
CRITERES :
  - VALIDATION : a 2,5e14 la machinerie doit redonner f_coll a +/-20 % de 0,039, 1/f_coll a
    +/-20 % de 25 et log10 R a +/-0,5 de 7,6 ; sinon RIEN n'est exploite (autre pipeline).
  - Les chiffres de la route analytique sont reportes TELS QUELS dans le papier B ; ceux de la
    route simulation sont reportes comme caveat. Si R < 1 sur une route, on l'ecrit : l'arbre
    ne pousse pas, il n'y a pas de grand livre.
Usage : python3 scripts/penrose_fcoll.py
"""
import sys, pathlib
import numpy as np
from scipy.special import erfc
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gradient_v2 as G
np.seterr(all='ignore')

c, Mc, F = G.etat()
h = G.REF['h']; V_B = 6.225e12
def fcoll(M_msun): return erfc(G.DELTA_C / (np.sqrt(2) * c.sig_M(M_msun * h)))
def R(M_msun):     return c.F(M_msun * h) * V_B

if __name__ == "__main__":
    f, r = fcoll(2.5e14), R(2.5e14)
    ok = abs(f/0.039 - 1) < 0.2 and abs((1/f)/25 - 1) < 0.2 and abs(np.log10(r) - 7.6) < 0.5
    print(f"[validation] M=2,5e14 : f_coll={f:.3f} (publie 0,039) 1/f={1/f:.1f} (O(25)) log10 R={np.log10(r):.1f} (7,6) -> "
          + ("OK" if ok else "ECHEC : autre pipeline, rien n'est exploite"))
    if not ok: sys.exit(1)
    print(f"{'M [Msun]':>10s} {'f_coll':>8s} {'1/f_coll':>10s} {'log10 R':>8s}  route")
    for M, lab in [(3.0e12, "#52 route analytique (adoptee par B)"), (2.0e15, "#80 simulation z<3"),
                   (5.6e15, "#80 simulation z<2"), (1.8e16, "#80 simulation z<1")]:
        f, r = fcoll(M), R(M)
        print(f"{M:10.1e} {f:8.3f} {1/f:10.3g} {np.log10(r):8.1f}  {lab}" + ("   <- R < 1 : pas d'arbre" if r < 1 else ""))
