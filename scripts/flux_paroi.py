"""DOUTE #2 EXECUTE — la condition de flux a travers la paroi. CRITERES PRE-ENREGISTRES :
(1) Cote interieur (fluide parfait comobile) : T_ab u^a n^b = 0 EXACTEMENT (u.n=0) — donc
    la violation est le flux exterieur lui-meme : [T u n] = (dM_out/dtau) vdot / (4 pi R^2).
(2) Parametre de controle eps_c = [Tun]/(sigma H) = (dM/dt) vdot / (R s H) [G=1].
    Si eps_c << 1 sur le domaine utile : forme fermee = approximation CONTROLEE, kappa(sigma)
    tient a O(eps_c). Si eps_c = O(1) : je retrograde dv/dt=1/(1-x-s) en ordre dominant, ecrit.
(3) FERMETURE EXACTE testee dans la foulee : promouvoir sigma(t) avec
    d(sigma)/dtau = [Tun] (la paroi absorbe le flux), integrer s(t), recalculer kappa,
    et donner la CORRECTION sur kappa. Verdict rendu par les nombres, pas par preference."""
import numpy as np
np.seterr(all='ignore')
OM,B,ZEQ=0.3113,2.418,3387.
Or=OM/(1+ZEQ);Ode=1-OM-Or;a=np.logspace(-7,0,200000)
E2=OM/a**3+Or/a**4+Ode
for _ in range(12):
    E=np.sqrt(E2);ig=1/(a*E)
    t=np.concatenate([[0],np.cumsum(0.5*(ig[1:]+ig[:-1])*np.diff(a))]);t/=t[-1]
    E2=OM/a**3+Or/a**4+Ode*np.clip(t,1e-300,None)**B/a**3
E=np.sqrt(E2);T=t*0.9501;H=E
print(f"{'x0':>5} {'s0':>5} {'eps_c(z=1)':>11} {'eps_c(0)':>9} {'kappa_fixe':>11} {'kappa_flux':>11} {'d_kappa':>8}")
for x0 in [0.10,0.30]:
    for s0 in [0.10,0.30]:
        chi=x0; R=a*chi; x=H*R
        # --- cas s fixe (s ∝ a, sigma const) ---
        s=s0*a
        m=(a>=1e-3)&(x+s<0.995)
        Tm,Rm,xm,sm,Hm=T[m],R[m],x[m],s[m],H[m]
        Mout=(xm**2+sm*(2-sm))*Rm/2
        dM=np.gradient(Mout,Tm); vd=1/(1-xm-sm)
        eps=dM*vd/(Rm*sm*Hm)
        i1=np.argmin(np.abs(1/a[m]-1-1.0))
        dv=vd; v=np.concatenate([[1e-12],np.cumsum(0.5*(dv[1:]+dv[:-1])*np.diff(Tm))])
        g=(Tm/v)*dv; k_fix=np.gradient(np.log(g),np.log(Tm))[-1]
        # --- fermeture exacte : sigma(t) nourrie par le flux ---
        sf=np.zeros_like(Tm); sf[0]=sm[0]
        for i in range(1,len(Tm)):
            dt=Tm[i]-Tm[i-1]
            Mo=(xm[i-1]**2+sf[i-1]*(2-sf[i-1]))*Rm[i-1]/2
            Mo2=(xm[i]**2+sf[i-1]*(2-sf[i-1]))*Rm[i]/2
            dMo=(Mo2-Mo)/dt
            vdi=1/max(1-xm[i-1]-sf[i-1],1e-9)
            dsig=dMo*vdi/(4*np.pi*Rm[i-1]**2)          # dsigma/dtau = [Tun]
            sf[i]=sf[i-1]+dt*(4*np.pi*(dsig*Rm[i-1])+sf[i-1]*xm[i-1]*Hm[i-1]/xm[i-1]*Hm[i-1]*0)  # ds=4pi(dsig R + sig Rdot)
            sf[i]=sf[i-1]+dt*(4*np.pi*dsig*Rm[i-1]+sf[i-1]*Hm[i-1])
        ok=xm+sf<0.995
        vd2=1/np.clip(1-xm-sf,1e-9,None)
        v2=np.concatenate([[1e-12],np.cumsum(0.5*(vd2[1:]+vd2[:-1])*np.diff(Tm))])
        g2=(Tm/v2)*vd2; k_fl=np.gradient(np.log(np.clip(g2,1e-30,None)),np.log(Tm))[-1] if ok[-1] else float('nan')
        print(f"{x0:>5.2f} {s0:>5.2f} {eps[i1]:>11.3f} {eps[-1]:>9.3f} {k_fix:>11.4f} {k_fl:>11.4f} {k_fl-k_fix:>+8.4f}")
print()
print("Lecture : eps_c est le rapport (flux accrete)/(energie de paroi x H). s'il est <~0,3,")
print("la paroi comobile a tension quasi-constante est une approximation controlee ; la colonne")
print("d_kappa donne la correction EXACTE de la fermeture ou la paroi absorbe tout le flux —")
print("c'est la borne superieure de l'effet (le cas reel partage le flux avec l'interieur).")
