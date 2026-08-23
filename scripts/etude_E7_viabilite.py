"""E7 — L'INDICE DE VIABILITE HORS COSMOLOGIE. CRITERES PRE-ENREGISTRES (geles avant run) :
INCLUSION : un systeme n'est SCORE que si sa dynamique se reduit EXACTEMENT a
  dM/dt = g(t) M avec g decroissant (classe d'isomorphisme de dM/dt = (beta/t)M).
  Alors seul beta_equiv = dlnM/dlnt est exporte.
EXCLUSIONS (= anti-pseudoscience, la valeur de l'etude est aussi ses refus) :
  - x = -w N'EST PAS exporte hors cosmologie : il vient d'un bilan d'energie-pression
    sans analogue defini ailleurs. x n'est calcule QUE pour l'univers.
  - lois d'echelle en TAILLE (villes de Bettencourt, Kleiber) : autre variable, autre
    equation -> ECHO, refusees au scoring.
  - systemes sans operationalisation de fourni/consomme (open-source, la campagne) ->
    REFUSES v1, operationalisation exigee avant tout score (E7.2 eventuelle).
  - exposants publies cites en PLAGES de litterature, jamais en valeurs precises inventees.
VERDICT ATTENDU : une carte a deux panneaux (beta_equiv universel ; x(t) univers seul),
et la table inclus/refuses avec motifs. Rien d'autre n'est affirme."""
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
np.seterr(all='ignore')
OM,B,ZEQ=0.3113,2.42,3387.
Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-4,0,60000)
E2=OM/a**3+Or/a**4+Ode
for _ in range(10):
    E=np.sqrt(E2);ig=1/(a*E)
    t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
    E2=OM/a**3+Or/a**4+Ode*np.clip(t,1e-300,None)**B/a**3
E=np.sqrt(E2);t0=0.951;x=B/(3*E*t*t0)   # x = -w = beta/(3Ht)
z=1/a-1
fig,ax=plt.subplots(1,2,figsize=(11,4.6));plt.subplots_adjust(wspace=.28,bottom=.16)
# Panneau A : axe beta_equiv universel
A=ax[0];A.set_xlim(0,4.6);A.set_ylim(0,1);A.set_yticks([])
A.set_xlabel(r'$\beta_{equiv}=d\ln M/d\ln t$ (classe $\dot M=(\beta/t)M$)')
A.set_title('A — Les systemes qui partagent l\'equation',fontsize=10)
A.axvspan(2.42,2.60,color='#8B2500',alpha=.85);A.text(2.51,.88,'notre\nunivers',ha='center',fontsize=8,color='#8B2500')
A.axvspan(1.0,3.0,color='#7fa3b8',alpha=.25);A.text(2.0,.62,'epidemies sous-exponentielles\n(taux de contact declinant,\nplage litterature 2020)',ha='center',fontsize=8,color='#3e6478')
A.annotate('etoiles AGB : auto-consommation,\nsortie de fenetre observee (qualitatif)',xy=(4.3,.30),ha='right',fontsize=8,color='#555')
A.text(.15,.10,'REFUSES au scoring (motifs en table) :\nvilles/Kleiber - open-source - la campagne',fontsize=7.5,color='#999')
# Panneau B : x(t), univers seul
Bx=ax[1];m=z<9
Bx.plot(np.log10(1+z[m]),x[m],color='#8B2500',lw=2)
Bx.axhline(1,color='k',lw=.8,ls='--');Bx.axhline(0.548,color='#7fa3b8',lw=.8,ls=':')
Bx.set_xlabel(r'$\log_{10}(1+z)$   (le temps va vers la gauche)');Bx.set_ylabel(r'$x=-w=\beta/(3Ht)$')
Bx.set_title('B — x(t), UNIVERS SEUL (non exportable)',fontsize=10)
Bx.text(.72,1.06,'x=1 : croisement fantome (z=0,46)',fontsize=8)
Bx.text(.55,.50,'attracteur x*=0,548',fontsize=8,color='#3e6478')
Bx.set_xlim(1,0);Bx.set_ylim(0,2.4)
Bx.text(.05,2.2,f'aujourd\'hui : x0={x[-1]:.2f}',fontsize=9)
plt.savefig('E7_carte_viabilite.png',dpi=160,bbox_inches='tight')
print(f"x0 (aujourd'hui) = {x[-1]:.3f} ; croisement x=1 a z = {z[np.argmin(np.abs(x-1))]:.2f} ; figure ecrite")
