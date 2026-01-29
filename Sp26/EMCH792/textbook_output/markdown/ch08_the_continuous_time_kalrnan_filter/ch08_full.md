---
type: chapter
chapter: 8
title: The continuous-time Kalrnan filter
---

# CHAPTER 8


The continuous-time Kalman filter

Our philosophy here will be to model phenomena with differential equations and then to form estimates of the physical quantities which also satisfy differential equations. --Richard Bucy [Buc68, Chapter 11

James Follin, A. G. Carlton, James Hanson, and Richard Bucy developed the continuous-time Kalman filter in unpublished work for the Johns Hopkins A p plied Physics Lab in the late 1950s. Rudolph Kalman independently developed the discretetime Kalman filter in 1960. In April 1960 Kalman and Bucy became aware of each other's work and collaborated on the publication of the continuous-time **Kalman filter in [Ka161]. This filter is sometimes referred to as the Kalman-Bucy** **filter. Further historical notes are given in Appendix A.** The vast majority of Kalman filter applications are implemented in digital com- puters, so it may seem superfluous to discuss Kalman filtering for continuous-time measurements. However, there are still opportunities to implement Kalman filters in continuous time (i.e., in analog circuits) [Hug88]. Furthermore, the derivation of the continuous-time filter is instructive from a pedagogical point of view. Fi- nally, steady-state continuous-time estimators can be analyzed using conventional frequency-domain concepts, which provides an advantage over discretetime estimc+ tors [Ba187, Ste941. In light of these factors, this chapter presents the continuous- time Kalman filter.

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **229**

---


[Image on page 2]


**230**

Our derivation of the continuous-time filter starts with the previously developed **discrete-time filter from Chapter 5, and then takes the limit as the time step de-** **creases to zero. Section 8.1 shows the relationship between continuous-time white** noise and discrete-time white noise, which is the foundation for the derivation of the continuous-time Kalman filter. Section 8.2 derives the Kalman filter for the case of **continuous-time system dynamics and continuous-time measurements. Section 8.3** shows some creative methods to solve the continuous-time Riccati equation, which is a key component of the continuous-time Kalman filter. Section 8.4 discusses the continuous-time Kalman filter for the cases of correlated process and measurement noise, and for colored measurement noise. Section 8.5 discusses the steady-state **continuous-time Kalman filter, its relationship to the Wiener filter of Section 3.4,** and its relationship to linear quadratic optimal control.


## 8.1 DISCRETE-TIME AND CONTINUOUS-TIME WHITE NOISE


In this section, we will show the relationship between discrete-time white noise and continuous-time white noise. We need to understand this relationship because in **the next section we will derive the continuous-time Kalman filter as the limiting case** of the discretetime Kalman filter as the sample time decreases to zero. First we will discuss the relationship between discrete-time and continuous-time process noise, and then we will discuss the relationship between discrete-time and continuous-time measurement noise.

**8.1.1** **Process noise**

Consider the following discrete-time system with an identity state transition matrix *and a sample time of T:*

**where {Wk} is a discrete-time white noise process. Let us see what effect the white** noise has on the covariance of the state. We can solve this discrete-time system for **the state as follows:**


# x k  = WO + W 1  + - .. + W k - 1
 (8.2)

**The covariance of the state is therefore given as**


# E [ x k x r ]  = E[(Wo + W1 + * + Wk-i)(WO + W 1  + * * * + W ~ - I ) ~ ]
 
# = E[wow3 + E [ W l W T ]  + *
 
# a * + EIWk-lW;-l]
 
## = kQ
 **(8.3)**

*The value of the continuous-time parameter t is equal to the number of discrete-time* 
## steps k times the sample time T. That is, t = kT. We therefore see that


## E [ Z ( t ) X T ( t ) ]  = E [ z k X : ]
 
## = kQ


---


[Image on page 3]


**231**

*The covariance of the state increases linearly with time for a given sample time T.* Now consider the continuoustime system with an identity state transition matrix:

*i ( t )  = w(t)* (8.5)

where w(t) is continuous-time white noise. We propose (in hindsight) the following definition for continuous-time white noise:

(8.6) **E[W(t)WWT(T)]** 
## = -6(t
 *Q* *- T )* *T* *where Q and T are the same as they are in the discretetime system of Equa-* *tion (8.1). 6 ( t  - T )  is the continuous-time impulse response; it is a function with a* *value of 0;) at t = T ,  a value of 0 everywhere else, and an area of 1. Let us compute* *the covariance of z(t) in Equation (8.5):*

*E[z(t)zT(t)] = E* *w(a) da* wT(@) *dp* *[JO’* *Jo’* I

Substituting Equation (8.6) into the above equation gives


# E[z(t)z’(t)] = J’ J’ &6(a - p) dadp


*= J0’4dp*

*0 o T*

*Qt* - - *- T* where we have used the sifting property of the continuous-time impulse function 
## (see Problem 4.10). Recalling that t = kT, we can write the above equation as


*E[z(t)zT(t)]* *= kQ* (8.9)

Comparing this with Equation (8.4), we see that the covariance of the state of **the continuous-time system increases with time in exactly the same way as the** covariance of 6he state of the discretetime system. In other words, discretetime *white noise with covariance Q in a system with a sample period of T ,  is equivalent to* *continuous-time white noise with covariance Qc6(t), where Qc = Q/T. Zero-mean* **continuous-time white noise is denoted as**

**4 t )** *N (0,Qc)* (8.10)

which is equivalent to saying that

*E[W(t)WT(T)] = Qc6(t - T )* (8.11)

**Continuous-time white noise is counterintuitive because w (t) is infinitely correlated** 
## with W ( T )  at t = T, but it has zero correlation with itself when t # T. Nevertheless,
 it can be approximately descriptive of real processes. Also, continuous-time white noise is mathematically well defined and is a useful device that we will use in this chapter. Additional discussion about the relationship between discretetime and continuous-time white noise can be found in [Kai81, Smi781.

---


[Image on page 4]


232


## 8J.2 Measurement noise


**Now let us think about measurement noise. Suppose we have a discretetime mea-** 
## surement of a constant x every T seconds. The measurement times are tk = kT
 *( k  = 1,2,**.):*

(8.12)

*From the Kalman filter equations in Section 5.1 we find that the a posteriori* estimation-error covariance is given by

From this it can be shown that

*PoR* *kPo + R* *Pk+ =*

lim ~ k +  = - *R*

**Po-tw** *k* *RT* = - **tk**

**The error covariance at time tk is independent of the sample time T if**

(8.13)

(8.14)

(8.15)

*where Rc is some constant. This implies that*


## lim R = R,6(t)
 (8.16) **T-0**

**where 6(t) is the continuous-time impulse function. This establishes the equivalence** between white measurement noise in discrete time and continuous time. The effects of white measurement noise in discrete time and continuous time are the same if

(8.17)

*Equation (8.15) specifies the relationship between R and Rc, and the second equa-* tion above is a shorthand way of saying

*E [ w ( ~ ) w ( T ) ]* 
# = Rc6(t - T)
 (8.18)

**8.1.3**

The results of the above sections can be combined with the results of Section 1.4 to obtain a discretized simulation of a noisy continuous-time system for the purpose


## Discretized simulation of noisy continuous-time systems


---

**233**

of implementing a discretetime state estimator. Suppose that we have a system given as

(8.19)

**Both w(t) and v(t) are continuous-time noise, and u(t) is a known input. This** system is approximately equivalent to the following discretetime system:

(8.20)

**where At is the discretization step size. The second expression for X k  above is valid** **if A-l exists. If we use these discretized equations to simulate a continuous-time** system, then we can simulate a continuous-time state estimator using the resulting **measurements with one of the integration methods discussed in Section 1.5. The** remainder of this chapter discusses continuous-time state estimation.


## 8.2
 
## DERIVATION OF THE CONTINUOUS-TIME KALMAN FILTER


We will now use the results of the previous section to derive the continuous-time **Kalman filter. Suppose that we have a continuous-time system given as**

(8.21)


# When we write w - (O,Qc) we mean exactly what is written in Equation (8.11).
 
## When we write w N (0, R,) we mean exactly what is written in Equation (8.18). Now
 *suppose that we discretize this system with a sample time of T (see Section 1.4).* We obtain

(8.22)

**The matrices in this discretetime system are computed as follows:**

---


[Image on page 6]


**234**

*F* *=*

**M** **G** **=**

**w**

**A** **=**

**M** *H* *=*

*wk*

*uk*

*exP(AT)* *(I + AT) for small T* *(exp(AT) - I)A-'B* *BT for small T* *(exp(AT) - I)A-I* *IT for small T* *C*

*(O,Q),* *Q =  QcT* *N(0, R),* *R = RJT* **(8.23)**

**The discretetime Kalman filter gain for this system was derived in Section 5.1 a**

*Kk = PLHT(HPLHT + R)-'* (8.24)

From this we can derive

**The estimation-error covariances were derived in Section 5.1 as**

**(8.25)**

**(8.26)**

*For small values of T ,  this can be written as*

*PL+'* *= (I + AT)Pkf(I + ATjT + QcT* *= P; + (AP; + P , ~ A ~* *+ Q,)T + AP,+A~T~* **(8.27)**

*Substituting for Pk+ gives*


# PF+l = (I - Kkc)Pi f APk+ATT2 +


*[A(I - Kkc)Pi + ( I  - KkC)PLAT i- Qc]T* **(8.28)**

*Subtracting PL from both sides and then dividing by T gives*


## Taking the limit as T + 0 and using Equation (8.25) gives


*= -PCTRLICP + AP +PAT + Qc* **(8.30)**

---

**235**

*This equation for P is called a differential Riccati equation and can be used to com-* pute the estimation-error covariance for the continuous-time Kalman filter. This 
## requires n2 integrations because P is an n x n matrix. But P is symmetric, so in
 
# practice we only need to integrate n(n + 1)/2 equations in order to solve for P.
 **In Section 5.1 we derived the Kalman filter equations for 2 as**

**2;** *= Ff;-_,+G~k-l*

**2;** 
# = 2, + Kk(yk - H2;)
 **(8.31)**

**If we assume that T is small we can use Equation (8.23) to write the measurement** **update equation as**

**2;** *= F i t - l f  G u ~ - I +* *Kk(yk - HFi?t-'_, - HGuk-1)*

*NN ( I  +* *+ BTuk-l+* *Kk(yk - C(I + AT)2t-l - CBTUk-1)* **(8.32)**

**Now substitute for Kk from Equation (8.25) to obtain**

**i+** **k** *= 2:.-1+ ATi;-l + B T u ~ - ~ +* **T -1** 
# PC R, T(yk - C2;-l - CAT?:-_, - CBTuk-1)
 **(8.33)**


## Subtracting zkf-l from both sides, dividing by T ,  and taking the limit as T + 0,
 gives


# i; - q-l
 *T* 
## 2 = lim
 **T+O** 
# = A2 + BU + PCTRL1(y - C2)


**This can be written as** 
# 1 = A P + B u f K ( y - C 2 )
 *K = PCTRF1*

**(8.34)**

**(8.35)**

This gives the differential equation that can be used to integrate the state estimate in the continuous-time Kalman filter.

**The continuous-time Kalman filter**

The continuous-time Kalman filter can be summarized as follows.

1. The continuous-time system dynamics and measurement equations are given **as**


## Si. = Ax+Bu+w


*y* = c x + v **w** *N* *( 0 , Q c )*

**y** *(0,RC)*

*Note that w(t) and w ( t )  are continuous-time white noise processes.*

**(8.36)**

---


[Image on page 8]


**236**

**2. The continuous-time Kalman filter equations are given as**


## 2(0) = E[z(O)]
 
# P(0) = E((s(0) - 2(0))(z(O) - 2(0))T]
 *K = PCTRF1*


# P = -PCTRLICP + AP + PAT + Qc
 (8.37) 
## 2 = A2++~u+K(y-C2)


Other methods of deriving the continuous-time Kalman filter also exist. For exam- ple, George Johnson presented a derivation that is based on finding the gain that minimizes the derivative of the estimation covariance [Joh69].

**EXAMPLE8.1**

In this example we will use the continuous-time Kalman filter to estimate a constant given continuous-time noisy measurements:

(8.38)


## We see that A = 0, Q = 0, and C = 1. Equation (8.37) gives the differential
 equation for the covariance as


# P = -PCTR-lCP + AP + PAT + Q
 *= -P2/R* (8.39)

*with the initial condition P(0) = PO. From this we can derive*

*lim P* *t-ca*

*-dT* *R* = -

*= - j f i d r*

*= Prl + t / R* *= (Prl + t/R)-'*

*1 + Pot/R*

*= -t/R*

- *PO* -

= o (8.40)

**Equation (8.37) gives the Kalman gain as**

(8.41)

---


[Image on page 9]


**237**

**Equation (8.37) gives the state-update equation as** 
# d = A$ + B~ + ~
 ( y 
# - c?)
 **(8.42)**

from which we can derive

**2** **=** 
# K(Y - 2)
 
## lim 2 = 0
 **(8.43)** t+m **This shows that as time goes to infinity, 2 reaches a steady-state value. This** is intuitive because as we obtain an infinite number of measurements of a constant, our estimate of that constant becomes perfect and additional mea- surements cannot improve our estimate. Furthermore, the Kalman gain goes to zero as time goes to infinity, which again says that we ignore additional measurements (since our estimate becomes perfect). Finally, the covariance *P goes to zero as time goes to infinity, which says that the uncertainty in our* estimate goes to zero, meaning that our estimate is perfect. Compare this **example with the equivalent discrete-time system discussed in Example 7.10.** vvv

**EXAMPLE8.2**

In this example we are able to obtain measurements of the velocity of an object that is moving in one dimension. The object is subject to random accelera- tions. We want to estimate the velocity x from noisy velocity measurements. **The system and measurement equations are given as**


$$
j . =  W
$$


y = a:+v *w N* *(0,Q)*

**tJ** *(0,R)* **(8.44)**


## We see that A = 0 and C = 1. From the covariance update of Equation (8.37)
 we obtain 
## P = - P C ~ R - ~ C P
 *+ AP + PA^ + Q* - *- -P2/R+Q* **(8.45)**

*with the initial condition P(0) = Po. From this we can derive*

*Solving this for P gives*

*= (Q-P2/R)dr*

*= 1 dr* **t**

*=* *t* **(8.46)**

---


[Image on page 10]


238

**The Kalman gain is obtained from Equation (8.37) as**

*K = PCTR-'* *= P/R*

*lim K =* **t+w** **(8.48)**

**The state estimate update expression is obtained from Equation (8.37) as**


## f = A h + B t ~ + K ( y - C f i . )
 *= K(y - 5)* (8.49)

From these expressions we see that if process noise increases (i.e., Q increases) **then K increases. This is intuitively agreeable, because from the 4 equation we** **see that K defines the rate at which we change 3 based on the measurements.** If Q is large then we have less confidence in our system model, and relatively **more confidence in our measurements, so we change f more aggressively to** be consistent with our measurements. *Similarly, we see that if we have large measurement noise (i.e., R is large)* *then K decreases. This is again intuitively agreeable. Large measurement* noise means that we have less confidence in our measurements, so we change **f less aggressively to be consistent with our measurements.** **Finally, we see that P increases as both Q and R increase. An increase in** the noise in either the system model or the measurements will degrade our confidence in our state estimate. vvv


## 8.3 ALTERNATE SOLUTIONS T O  THE RlCCATl EQUATION


**The differential Riccati equation of Equation (8.37) can be computationally expen-** sive to integrate, especially for systems with small time constants. Also, direct *integration of the Riccati equation may result in a P matrix that loses its positive* definiteness due to numerical problems. In this section we will look at some alter- nate solutions to the differential Riccati equation. This first two methods, called the transition matrix approach and the Chandrasekhar algorithm, are both intended to reduce computational effort. The third method, called square root filtering, is intended to reduce numerical difficulties.


## 8.3.1
 **The transition matrix approach**


## Assume that P = AY-l, where A and Y are n x n matrices to be determined. In
 **the following we will determine what equalities must be satisfied by A and Y in** order for this factorization to be valid. If the factorization is valid then *d* *dt* *AY-l+ A-(Y-l)*

*= Ay-1- AY-1yy-l* (8.50)

*where we have used Equation (1.51) for the time derivative of Y-l. We post-* *multiply both sides of the above equation by Y to obtain*

(8.51) 
# py = A - Ay-ly


---


[Image on page 11]


**239**

*Recall from Equation (8.37) that the differential equation for P is given by*


# P = AP + PAT - PCTR-lCP + Q
 (8.52)

*Substitute AY-l for P in this equation to obtain*


# P = AAY-l+ AY-lAT - AY-lCTR-'CAY-l + Q
 (8.53)

*Post-multiply both sides of this equation by Y to obtain*

*PY = Ah + AY-lATY - AY-lCTR-lCA + QY* (8.54)

Now we can equate the right sides of Equations (8.51) and (8.54) to obtain


$$
A - AY-~Y = AA + A Y - ~ A ~ Y
$$
 *- A Y - ~ C ~ R - ~ C A* *+ QY* *A = AA + QY + AY-'(Y + ATY - CTR-lCA)* (8.55)

**This equation came from our original factorization of P, and if this equation re-** duces to 0 = 0 then we know that the original factorization was valid. So if 
# Y = CTR-ICA - ATY, and A = AA + QY, then our assumed factorization will be
 **valid. These differential equations for Y and A can be combined as**

*[ i] = [ CTR-lC -AT ] [ $ 1* *A* *Q*

= J [ b ] (8.56)

**where J is defined by the above equation. The initial conditions on A and Y can** *be chosen to be consistent with the initial condition on P as follows:*

*A(0) = P(0)* *Y(0) = I* (8.57)

*Now suppose that A, Q, C, and R are constant (that is, we have an LTI system with* constant process and measurement noise covariances). In this case J is constant and Equation (8.56) can be solved as


# A(t + T )
 *[ Y ( t  + T )  ] = exp(JT) [ ![;{ ]*

This can be written as

(8.58)

(8.59)


## where the q5iJ matrices are defined as the four n x n submatrices in exp(JT). From
 
## our original factorization assumption we have A = PY, so this equation can be


This can be written as two separate equations:

(8.61)

---

**240**


# Since h(t + T )  = P(t + T)Y(t + T), we can write the first equation as


*P(t + T)Y(t + T )  = 411(T)P(t)Y(t) + 412(T)Y(t)* *(8.62)*

*Substituting for Y ( t  + T )  from Equation (8.61) in the above equation gives*

*P(t + T )  [42l(~)P(t)Y(t)* *+ 422(T)Y(t)l = 411(T)P(t)Y(t) + $12(T)Y(t)* 
# P(t + T )  [421(T)P(t) + 422(T)1 = 411(T)P(t) + 412(T)
 *(8.63)*


# This equation is finally solved for P(t + T )  as


*P(t + T )  = [ h ( T ) P ( t )  + 412(T)] [421(T)P(t) + 422(T)]-l* *(8.64)*

*This may be a faster way to solve for P instead of integrating the Riccati equation.* Note that we do not have to worry about the integration step size with this method. *This method can be used to propagate from P(t) to P(t + T )  in a single equation,* *for any values t and T.*


## m  EXAMPLE^.^


**Suppose that we want to estimate a gyroscope drift rate E (assumed to be con-** stant) given measurements of the gyro angle 8. The system and measurement **model can be written as**

**e** **=** **E** 
$$
Y = e + v
$$


v *(0,R)*

**Direct use of the differential Riccati equation from Equation (8.37) gives**


# P = AP + PAT - PCTR-lCP + Q


*(8.65)*

*We can solve for P by performing three numerical integrations (recall that P* is symmetric). However, it would be difficult to find a closed-form solution for **P(t) from these coupled differential equations. A transition matrix approach** **to this problem would proceed as follows, assuming that P(0) is diagonal. We** *suppose that P is factored as P = AY-l, where A and Y are 2 x 2 matrices.* **The initial conditions on A(t) and Y ( t )  can be chosen as**


## A(0) = P(0)


*Y(0) = I* *(8.67)*

---

**241**

*The differential equation for A(t) and Y(t) is given as*

[ $ ] = J [  $ 1

**where the matrix J is computed as**

*(8.68)*

*(8.69)*

**The transition matrix for the differential equation for A and Y is computed** **as**

*r* *1* *t* *0* 0 1 *1* *exp(Jt) = 1 tj)R* *t2/2R* *-t2/2R -t3/6R -t* *1*

*(8.70)*

*where the +ij(t) terms are 2 x 2 matrix partitions. The Riccati equation* *solution is obtained from Equation (8.64) as*

*P(t) = [4ll(t)P(O) + 412(t)1[421(t)P(O)* *+ 4 2 2 ( t ) l - l* *(8.71)* - *12R2 - 2t3Pz2(0)* - *12R2t + 6t2P11(0) 12R2 + 12tP11(0)*

**where A is given as**


# A = 12R2 + P I I ( O ) P ~ ~ ( O ) ~ ~
 *+ 12Pll(O)tR + 4P22(0)t3R* *(8.72)*

Carrying out the multiplication and some algebra gives the Riccati equation **solution as**

*1*

1

1

*P11(t) = a4R [P11(0)P22(O)t3 + 3P11(O)R + 3t2P22(0)R]*

*P12(t) = ~6RPzz(O)t* *[Pii(O)t + 2R]*

*&(t) = ~12R%2(0)* 
# [Pii(O)t + R]
 *(8.73)*

With the transition matrix approach we have obtained a closed-form solution *for P(t), something that was not possible with a direct approach to the Riccati* equation. In the special case that our initial uncertainty is infinite, we can

---


[Image on page 14]


242

**further simplify P(t) as**


## lim A = P11(0)P22(O)t4
 **P(O)+w**

*lim [ lim ~ ( t ) ]* *= [ 0* *0* *]*

**t+w** **P(O)+W** (8.74)

**That is, our uncertainty goes to zero as time goes to infinity. This occurs** because the process noise is zero (i.e., we are estimating a constant). Since 
## K = PCTR-l, we see that the Kalman gain also goes to zero as time goes
 to infinity. This simply means that eventually we get so many measurements that our knowledge is complete. Additional measurements cannot give us any new information, so we ignore additional measurements. vvv


## 8.3.2
 **The Chandrasekhar algorithm**

Recall the differential Riccati equation for the continuous-time Kalman filter from Equation (8.37): 
# P = AP + PAT - PCTR-’CP + Q
 (8.75)

*If P were not symmetric then the numerical computation of P would require n2* *integrations. However, since P = PT the computation of P requires only n(n+1)/2* integrations. This can still be computationally taxing, especially for problems with small time constants. The Chandrasekhar algorithm gives computational savings in some circumstances. The algorithm is based on the work of the Nobel prize winning astrophysicist Subramanan Chandrasekhar, who used similar algorithms to solve computationally difficult astrophysics problems in the 1940s [Cha47, Cha481. Chandrasekhar’s algorithms were applied to Kalman filtering in [Kai73, KaiOO]. *The Chandrasekhar algorithm applies only when A, C, R, and Q are constant.*


## 8.3.2.1 The Chandrasekhar algorithm derivation Consider the continuoustime dif-
 ferential equation for the state estimate, assuming that the original system is time- *invariant and the Kalman gain K is a constant:*

(8.76)

The measurement y is the output of the system, but it is the input to the filter. *Consider the zero-input Kalman filter (i.e., y = 0).*


# $ = ( A  - KC)?
 (8.77)

**This equation has the solution**

(8.78)

---


[Image on page 15]


**243**

*where 4J(t) is the state transition matrix of the filter and is defined by the above* 
## equation. From the definition of 4J(t) as a state transition matrix we know that


(8.79)

We can differentiate both sides of Equation (8.75) to obtain


# P = AP +PAT - PCTR-'CP - PCTR-'CP
 
# = AP + PAT - PCTKT - KCP
 
# = ( A  - KC)P + P(A -  KC)^
 (8.80)


# Now note that for a general timevarying matrix Y(t), if Y = AY + YAT, where
 
## A is a constant matrix, then Y ( t )  = exp(At)Y(0)exp(ATt) (see Problem 8.2).
 **Therefore, we can solve the above equation for P as**


## P = 4JP(0)4JT
 (8.81)

where P(0) is obtained from Equation (8.75) as


# P(0) = AP(0) + P(0)AT - F'(0)CTR-lCP(O) + Q
 (8.82)

*The symmetric matrix P(0) can be factored as follows (see Section 8.3.2.2):*


# P(0) = MiM,T - M2M:
 (8.83)

*P(0) is an n x n matrix. The rank of P(0) is a 5 n. Since p(0) is symmetric, all* *of its eigenvalues are real. The number of positive eigenvalues of P(0) is P, and the* 
## number of negative eigenvalues is (a - P). Matrix MI is an n x ,6 matrix, and Mz
 *is an n x (a - p) matrix. From the previous three equations we can write*


## P = 4JP(0)4JT
 
# = 4J(M&fF - M2M:)p
 
# = 4JM1MF4JT - 4JM2MT4JT
 (8.84)

**Now define the matrices Y1 and YZ as**

(8.85)

**Then the P equation can be written as**


# P = KY? - YZY?
 (8.86)

**Also, from the definition of Y1 we can see that**

(8.87)

---

**244**

Similarly, we see that

(8.88)


## Recall from Equation (8.37) that K = PCTRV1. Therefore, a differential equation
 *and initial condition for K can be written as*


## K = PCTR-l
 *= (YlY,' - &Y?)CTR-l* *K(0) = P(0)CTR-'* (8.89)

*To compute K from its differential equation we need to integrate three equations.*

*1. We need to integrate Y1 from Equation (8.87), where Y1 is an n x p matrix.*


## 2. We need to integrate Y2 from Equation (8.88), where Y2 is an n x (a - p)
 matrix.


## 3. We need to integrate K from Equation (8.89), where K is an n x r matrix (T
 is the number of measurements of the system).


# So we need to perform a total of n(a + T )  integrations. The direct computation
 
# of P from the differential Riccati equation requires n(n + 1)/2 integrations. So if
 *%(a + T )  < (n + 1) then the Chandrasekhar algorithm reduces the computational* effort of solving the differential Riccati equation.

**The Chandrasekhar algorithm**

**The Chandrasekhar algorithm can be summarized as follows.**

**1. Compute P(o).**


## 2. Use the method of Section 8.3.2.2 to find MI and M2 matrices that satisfy


## 3. Initialize Yl(0) = M I ,  Yz(0) = M2, and K(0) = P(0)CTR-l.


## 4. Integrate K ,  Y1,
 **and Y2 as follows:**


# P(0) = MlM,T - M2MF.


$$
I;; = (YiY,' - Y2Y,T)CTR-l
$$


*Y 1  = ( A - K C ) K*


## Y 2  = (A-KC)Yz
 (8.90)


## 8.3.2.2 Chandrasekhar factorization The derivation of the Chandrasekhar algo-
 **rithm requires the factorization of P(0) as shown in Equation (8.83):**


# P(0) = M1M,T - M2MF
 (8.91)


## e(0) is an n x n matrix with rank a 5 n. The number of positive eigenvalues of
 *P(0) is p, and the number of negative eigenvalues is (a -p). Matrix MI is an n x p*

---

**245**

*matrix, and M2 is an n x (a - p) matrix. In this section, we will show one way to* perform that factorization. *Since P(0) is symmetric, all of its eigenvalues are real. We can therefore write* *the Jordan form of P(0) as*


## P(0) = SDST
 s11 s 1 2  s13 0

*S is an orthogonal matrix whose columns comprise the eigenvectors of P(0). The* *p x p matrix D1 is a diagonal matrix whose entries are the positive eigenvalues of* *P(0). The (a - p) x (a - p) matrix D2 is a diagonal matrix whose entries are the* *magnitudes of the negative eigenvalues of P(0). Multiplying out the above equation* results in 
## P(0) = N1+ N2
 (8.93)

where N1 and N2 are given as

1

S11Dlgi S11D1gi 41D1g1 NI = [ S21D1S?1 S2iDiS& S21D1S3T1 s31Dlgl S31Dls& S31Dlg1

(8.94)

*Note that Nl is the product of an n x p matrix, the p x p matrix D1, and a /3 x n* **matrix. N1 can therefore be written as**

Ni = MiMT (8.95)

*where MI is the n x p matrix*

(8.96)


# A similar development can be followed to see that M2 is the n x (a - p) matrix


s 1 2 
# M2 = 1 s 2 2  1
 (8.97)

---

246


## 8.3.3
 
## The square root filter


The early days of Kalman filtering in the 1960s saw a lot of successful applications. But there were also some problems in implementation, many due to numerical *difficulties. The differential Riccati equation solution P(t) should theoretically* always be a symmetric positive semidefinite matrix (since it is a covariance matrix). *But numerical problems in computer implementations sometimes led to P matrices* **that became indefinite or nonsymmetric. This was often because of the short word** lengths in the computers of the 1960s [Sch81].' This led to a lot of research during that decade related to numerical implementations. Now that computers have become so much more capable, we don't have to worry **about numerical problems as often. Nevertheless, numerical issues still arise in fi-** nite word-length implementations of algorithms, especially in embedded systems.2 The square root filter was developed in order to effectively increase the numerical precision of the Kalman filter and hence mitigate numerical difficulties in imple- mentations. *The square root filter is based on the idea of finding an S matrix such that* *P = S p .  The S matrix is then called a square root of P. Note that the definition* 
$$
of the square root of P is not that P = 9,
$$
 
$$
but rather P = Sfl. Also note that
$$
 this definition of the matrix square root is not standard. Some books and papers 
# define the matrix square root as P = 9, others define it as P = flS, and others
 
$$
define it as P = SP.
$$
 The latter definition is the one that we will use in this book. Finally, note that the square root of a matrix may not be unique; that is, there may 
$$
be more than one solution for S in the equation P = Sfl. (This is analogous to
$$
 **the existence of multiple square roots for scalars. For example, the number 4 has** 
## two square roots: +2 and -2.) Sections 6.3 and 6.4 contain a discussion of square
 root filtering for the discrete-time Kalman filter. 
## After defining S as the square root of P, we will integrate S instead of P in our
 Kalman filter solution. This requires more computational effort but it doubles the precision of the filter and helps prevent numerical problems. From the differential **Riccati equation of Equation (8.37), and the definition of S, we obtain**


# P = AP + PAT - PCTR-'CP + Q
 
# SST + S F  = A S P  + SSTAT - SSTCTR-'CSP + Q
 (8.98)

*Now premultiply both sides by S-' and postmultiply by S-T to obtain*

**8-1pS-T** 
## = S-19 + 9Ts-T


*= S ' A S  + S T A T S T  - STCTR-'CS -k S - ' Q S T* (8.99)

*Since P is symmetric positive definite, we can always find an upper triangular S* *such that P = S p  [Go189, MooOO]. For example, consider the following matrices:*

lThe United States' Apollo space program of the 1960s resulted in the first man on the moon in 1969. The Apollo spacecraft guidance computer had a word length of 16 bits [Bat82], which **corresponds to 4.8 decimal digits of precision.** 2Most microcontrollers in the first decade of the 21st century have 16 bit words, and 8 bit micro- controllers still comprise a large share of the market.

---

**247**

= [; :] (8.100)


$$
P is symmetric positive definite, S is upper triangular, and P = Sp.
$$
 It can be 
## shown that if S is upper triangular, then S and S-l are also upper triangular (see
 Problem 8.4). Also, the product of upper triangular matrices is another upper 
## triangular matrix (see Problem 8.5). Therefore, the product S-lS is upper trian-
 *gular. Similarly, since fl and FT are lower triangular, the product PFT is* lower triangular. That is, 
# s-'S = Mu
 *STs-T* *= ML* (8.101)

*where Mu and ML denote upper triangular and lower triangular matrices. From* this we can obtain 
## S = SMu
 (8.102) Now we can use Equations (8.99) and (8.101) to find

*= Mu+ML* (8.103)

*So we see that Mu is the upper triangular portion of S-'PS-T. This gives us the* **square root algorithm as follows.**

**The continuous-time square root Kalman filter**

1. The initialization step consists of computing the upper triangular S(0) such

**2. At each time step compute P from the differential Riccati equation, and then**


## 3. Use S = SMu to integrate S to the next time step.


*4. Use the equation K = PCTR-l = SSTCTR-' to compute the Kalman gain.*

This is more computationally expensive than a straightforward integration of the differential Riccati equation, but it is also more numerically stable. The numerical **benefits of square root filtering are discussed in more detail in-Section 6.3.**

*that S ( O ) f l ( O )  = P(0).*

*compute MU as the upper triangular portion of S - l P S T .*

**8.4** 
## GENERALIZATIONS OF THE CONTINUOUS-TIME FILTER


In this section, we will discuss some generalizations of the continuous-time Kalman **filter, just as we did in Chapter 7 for the discrete-time Kalman filter. The continuous-** time filter was derived under the assumptions that the process and measurement noise was uncorrelated, and that the process and measurement noise was white. We will consider the case in which the process and measurement noise are corre- lated in Section 8.4.1, and the case in which the measurement noise is colored in Section 8.4.2.

---


[Image on page 20]


248


## 8.4.1


Consider the continuoustime system

**Correlated process and measurement noise**

*X* *= AX+W* *w N (0,Q)*

*y = cx+w*

21 *(0,R)* *E [ w ( ~ ) v ~ ( T ) ]* 
# = Md(t - 7)


# Since y - Cx - v = 0 we can write the system dynamics as


(8.104)


## 5 = A X + W + M R - ~ ( ~ - C Z - U )
 = = AZ+ii+G (8.105)


## where A, ii, and 6 are defined by the above equation. Note that ii is a known input
 to the X equation, and 6 is a new process noise term. The cross covariance between 
## the new process noise 8 and the measurement noise u can be found as


*( A  - MR-lC)z + MR-ly + (w - MR-'w)*

*E(6wT) = E[(w - MR-'w)wT]* *= E ( W V ~ )  - M R - ~ E ( W V ~ )* *= M - M* = o (8.106)

**So 8 and w are uncorrelated. The covariance of the new process noise 6 can be** **found as**


## Q = E(66T)
 = = *= Q - M R - ~ M T* (8.107)

**The differential Riccati equation for Kalman filter for the system given in Equa-** tion (8.105) is given by

*E[(w - MR-%)(w - M R - I w ) ~ ]* *Q - MR-lMT - MR-lMT + MR-IMT*


# P = AP + PAT - PCTR-lCP + Q
 *= ( A  - MR-lC)P + P ( A  - MR-lC)T - PCTR-'CP +* *Q - MR-'MT* (8.108)

If we define k **as**


## K = K + M R - ~
 *= PCTR-l + MR-I* *= ( P C ~ + M ) R - ~*

then the differential Riccati equation becomes


# P = AP+  PA^ + Q - K R K ~


(8.109)

(8.1 10)

---

**249**

The differential equation for the state estimate can be written as

i~! *= A2+ii+K(y-C2)* = = = A2+k(y-C2) **(8.111)**

We see that the introduction of correlation between the process and measurement noise has the effect of simply modifying the Kalman gain. The stateupdate equa- **tion and the differential Riccati equation retain the same form as for the standard** Kalman filter. The Kalman filter for correlated process and measurement noise can **be summarized as follows.**


# ( A  - MR-'C)2 + MR-'y + K(y - C2)
 
# A2 - M X ' C 2  + MR-ly + (I? - MR-')(y - C2)


**The continuous-time Kalman filter with correlated noise**

**1. The system dynamics and measurement equation are given as**


## i = AX+W


w *N* *(0,Q)*

*y = c x + v* *(O,R)* 
# E[W(t)VT(T)] = Mb(t - T)
 **(8.112)**

**2. The continuous-time Kalman filter is given as** 
# P = A P + P A ~ + Q - K R K ~
 *K* *= ( P C T + M ) X 1* *d = A2+K(y-C2)* **(8.113)**

Note that (as expected) this filter reduces to the standard continuous-time filter **of Equation (8.37) if the process and measurement noise are uncorrelated (i.e.,** 
## M = 0). This filter can therefore be considered as a general formulation of the
 
## continuous-time Kalman filter, with the situation M = 0 as a special case.


**8.4.2** **Colored measurement noise**

In this section we will derive the Kalman filter when the measurement noise is not white. Suppose we have the system

**(8.114)**

**We will assume that w and q5 are uncorrelated white noise processes. We could** **augment v onto the state vector (as suggested in Section 7.2.2 for discretetime sys-** tems), but then the covariance of the measurement noise of the augmented system

---


[Image on page 22]


**250**

would be singular, which could potentially cause numerical problems in the Kalman **filter implementation. Instead, we will define a new signal as**

*0 = y - N y* *= Cz+Ck++--N(Cz+w)* = = 
# CX +C(Az+ W )  + (Nw + 4) -N(Cz+v)
 
# (C + C A  - NC)z + (CW + 4)
 *= Cx+6* (8.115)

*where c and 6 are defined by the above equation. Note that 6 is a white noise* 
## process (since w and 4 are uncorrelated and white). So we have defined a new
 measurement equation that has white noise, but this is at the expense of creating a correlation between the process noise w and the new measurement noise 6. The correlation can be obtained as

*where the cross correlation matrix M is defined by the above equation. The covari-* ance of the new measurement noise 6 can be obtained as


# E ( G T )  = E[(Cw + $)(cW +
 
## R = CQCT+@
 (8.117)

So we have defined a new measurement equation with white noise. We have the correlation between the process noise and the new measurement noise in Equa- tion (8.116), and the covariance of the new measurement noise in Equation (8.117). Now we can use the results from Section 8.4.1 which discussed Kalman filtering for systems with correlated process and measurement noise. The Kalman filter can be written from Equation (8.113) as


## P = A P + P A ~ + Q - K ~ K ~
 
## K = (PCT+M)Ri-l
 *h = &+K(g-Ci!)* *= A ~ + K ( O - N Y - C ~ ! )* (8.118)

However, the new measurement that we defined in Equation (8.115) could cause *some problems. The original measurement y is already a noisy measurement, so the* *new measurement (which contains y )  will be even more noisy. How can we avoid* *the use of y in the filter? We can attack this problem by looking at the derivative* **of the product Ky as follows:**

*K y* *Ky = --* *dt* (8.119)

---

**251**

The dynamic equation for the state estimate in Equation (8.118) can then be written as follows:

**f-- d(Ky)** * 
# = ( A  - KC)f - (k + KN)y
 dt


## Now define a new signal z as
 z = f - K y

(8.120)

(8.121)

*Differentiating z results in the right side of Equation (8.120):*


# t = ( A  - KC)? - (k
 + K N ) ~ (8.122)

*Here we have an equation for k that we can integrate to solve for z. We can then* 
## use our solution for z in Equation (8.121) to solve for 2, So the only signal we
 *have to differentiate in the Kalman filter algorithm is the Kalman gain K ,  because* **we need K in the computation of k above. However, this differentiation should be** *much easier than differentiating y, because we expect the Kalman gain K to be* much smoother than the noisy measurement y. The Kalman filter for the case of **colored measurement noise can be summarized as follows.**

**The continuous-time Kalman filter with colored measurement noise**

1. The system and measurement equations are given as


$$
X = AX+W
$$
 *w N* *(0,Q)* 
$$
y = C x + w
$$


## 4
 *( O , @ )*


## ir = Nw+#J


where w and #J and uncorrelated white noise processes.

2. Make the following matrix definitions:

*C'* *= C + C A - N C* *R = CQCT+@* *M* *= QCT*

**3. Initialize the Kalman filter as**

*K(0) = [P(0)CT + M1R-l*

~ ( 0 )  = f(0) - K(O)y(O)


## 4. Integrate P, K ,  and z using the following equations:


## P = A P + P A ~ + Q - K R K ~
 d dt *k = -[(PCT+M)R-']*

= ( A - K C ) ~ - ( ( ~ + K N ) Y

(8.123)

(8.124)

(8.125)

(8.126)

---


[Image on page 24]


**252**


## Note that the K equation can be simplified to the following if Q, C, and @
 are constant: 
# k = p c T R - 1
 *(8.127)*


## 5. Compute the state estimate as


**? = , Z + + K y** *(8.128)*


## EXAMPLE 8.4


Suppose that it is known that a continuous-time measurement v(t) has a total power of 1 watt and a power spectrum that is bandlimited to frequencies below *10 Hz. In this example, we will use our knowledge of the frequency content* **of v(t) to obtain a dynamic model for v(t). The power spectrum Sv(w) can** 
## be plotted as shown in Figure 8.1. The magnitude of the spectrum, 1/40~,
 is *obtained by realizing that the total power of the signal (1 watt) is equal to* *the integral from -oo to +oo of Sv(w), and Sv(w) is an even function of w.* 
## The spectrum shown in Figure 8.1 can be approximated as


*= G(w)G(-w)Sb(w)* (8.129)

*This shows that v(t) is the output of a linear system with a transfer function* *of G(w) and an input of #(t),* *where #(t) is white noise with a variance of 1 / 2* *(see Equation 3.75). This can be written in the sdomain and then translated* **to the time domain as follows:**

*V(S) = G(s)@(s)* - @(s) - - *s + 20T* *sV(s) + 20TV(S) = @(s)*

*S V ( S )  = -2OTV(S) + @(s)* *6 = -207rv+#* *(8.130)*

*where +(t) is white noise with variance @ = 1/2. Additional discussion and* examples of this method can be found in [Bur99]. vvv

**8.5** 
## THE STEADY-STATE CONTINUOUS-TIME KALMAN FILTER


In some situations, the Kalman filter converges to an LTI filter. If this is the case then we can often get good filtering performance by using a constant Kalman gain *K in the filter. Then we do not have to worry about integrating the differential* *Riccati equation to solve for P and we do not have to worry about updating K in*

---

**253**

**frequency (radkec)**

**Figure 8.1** Power spectrum of bandlimited measurement noise for Example 8.4.

real time. This can provide a large savings in filter complexity and computational effort at the cost of only a small sacrifice of performance. In this section, we discuss the conditions under which the continuous-time filter converges to an LTI filter, and the steady-state filter’s relationship to Wiener filtering and optimal control.

**8.5.1 The algebraic Riccati equation**

**Recall from Equation (8.37) that the differential Riccati equation is given as**


# P = -PCTR-lCP + AP + PAT + Q
 (8.131)

**If A, C, Q, and R are constant (i.e., the system and measurement equations form** **an LTI system with constant noise covariances) then P may reach a steady-state** **value and P may eventually reach zero. This implies that**

*-PCTR-lCP + AP + PAT + Q = 0* (8.132)

This is called an algebraic Riccati equation (ARE). To be more specific, it is called **a continuous ARE (CARE) .3** The ARE solution may not always exist, and even if it does exist it may not result in a stable Kalman filter. We will summarize the most important Riccati equation convergence results below, but first we need to define what it means for a system to be controllable on the imaginary axis.

**Definition 12 The matrix pair (A, B )  is controllable on the imaginary axis i f  there** *exists some matrix K such that ( A  - B K )  does not have any eigenvalues on the* *imaginary axis.*

31n the MATLAB Control System Toolbox the CARE can be solved by invoking the command 
## P = CARE(AT, CT,
 **Q,** *8). The reason that the transposes are required is that MATLAB’s CARE* **command is designed to solve the ARE for continuous-time optimal control problems. When we** **use it to solve for the Kalman filtering problem we need to transpose the A and C matrices, as** **discussed in Section 8.5.3.**

---


[Image on page 26]


**254**

This is similar to the concept of controllability on the unit circle for discretetime **systems (see Section 7.3). Now we summarize the most important Riccati equation** convergence results from [KaiOO], where proofs are given. Recall that the ARE is **given as** *-PCTR-'CP + AP + PAT + Q = 0* **(8.133)**

*We assume that Q 2 0 and R > 0. We define G as any matrix such that GGT = Q.* *The corresponding steady-state Kalman gain K is given as*

*K = PCTR-'* **(8.134)**

**The steady-state Kalman filter is given as**


# h = ( A  - KC)2 + K y
 **(8.135)**

*We say that the CARE solution P is stabilizing if it results in a stable steady-state* **filter. That is, P is defined as a stabilizing CARE solution if all of the eigenvalues** 
# of ( A  - KC) have negative real parts.


**Theorem 27 The CARE has a unique positive semidefinite solution P if and only** *if both of the following conditions hold.*

*1. (A, C )  is detectable.*

**2. (A, G) is stabilizable.**

*Furthermore, the corresponding steady-state Kalman filter is stable. That is, the* 
# eigenvalues of (A - KC) have negative real parts.


**This theorem is analogous to Theorem 23 for discretetime Kalman filters. The** above theorem does not preclude the existence of CARE solutions that are negative definite or indefinite. If such solutions exist, then they would result in an unstable Kalman filter. If we weaken the stabilizability condition in the above theorem, we obtain the following.

**Theorem 28 The CARE has at least one positive semidefinite solution P if and** *only i f  both of the following conditions hold.*

**1. (A,** *C )  is detectable.*


## 2. (A, G) is controllable on the imaginary axis.


**firthewnore, exactly one of the positive semidefinite ARE solutions results an a** *stable steady-state Kalman filter.*

**This theorem is analogous to Theorem 24 for discretetime Kalman filters. This** theorem states conditions for the existence of exactly one stabilizing positive definite CARE solution. However, there may be additional CARE solutions (positive defi- nite or otherwise) that result in unstable Kalman filters. If a timevarying Kalman filter is run in this situation, then the Kalman filter equations may converge to *either a stable or an unstable filter, depending on the initial condition P(0). If we* **strengthen the controllability condition of Theorem 28, we obtain the following.**

---

**255**

**Theorem 29 The CARE has at least one positive definite solution P i f  and only** **if both of the following conditions hold.**

*1. (A, C )  is detectable.*

*2. (A, G) is controllable in the closed left half plane.*

*Furthermore, exactly one of the positive definite C A R E  solutions results in a stable* *steady-state Kalman filter.*

This theorem is analogous to Theorem 25 for discretetime Kalman filters. If we drop the controllability condition in the above two theorems, we obtain the following.

**Theorem 30 The CARE has at least one positive semidefinite solution P i f  (A, C )** *is detectable. firthemnore, at least one such solution results in a marginally stable* *steady-state Kalman filter.*

This theorem is analogous to Theorem 26 for discretetime Kalman filters. Note that the resulting filter is only marginally stable, so it may have eigenvalues on the imaginary axis. Also note that this theorem poses a sufficient (not necessary) condition. That is, there may be a stable steady-state Kalman filter even if the conditions of the above theorem do not hold. Furthermore, even if the conditions of the theorem do hold, there may be CARE solutions that result in unstable Kalman filters. Additional results related to the stability of the steady-state continuous-time filter can be found many places, including [Aok67, Buc67, Buc68, Kwa721. Many practical Kalman filters are applied to systems that do not meet the conditions of the above theorems, but the filters still work well in practice.

**EXAMPLE8.5**

In this example we consider the following two-state system that is taken 
## from [Buc68, Chapter 51:


(8.136)

In the remainder of this example, we use the symbol G to denote any matrix 
## such that GGT = Q. The differential Riccati equation for the Kalman filter
 is given as 
# P = -PCTR-'CP + AP + PAT + Q
 (8.137)

**This can be written as the following three coupled differential equations.**

---

**256**


# Pll = 2UlPll - p:1/7-1 - P:2 + 411


# P12 = (a1 + a2)p12 - PllP12/7-l - P12P22/7-2 + 412


# P22 = 2 a 2 ~ 2 2  - p&/rl - pi2/7-2 + 422
 (8.138)

We set these derivatives equal to zero to obtain the steady-state Riccati equa- tion solution. 
## If a 1  # a 2  and 412 # 0, then (A, C) is detectable and (A, G) is stabilizable
 **(see Problem 8.8). The results of Theorem 27 therefore apply to this situation.** It can be shown that the unique positive semidefinite ARE solution in this case is


# P22 = 7-2 [a2+ (12 - g2]


**P12**

**41 1** 
$$
71 = -
$$
 **7-1 +a:**

**422**

**7-2** 
## 1 2  = -+a;
 (8.139)

This results in a stable steady-state Kalman filter. 
## If a1 = a 2  < 0 , 4 1 2  # 0, and IQI = 0, then (A, C) is detectable, and (A, G)
 **is stabilizable (see Problem 8.9). The results of Theorem 27 therefore apply** to this situation as well. It can be shown that the unique positive semidefinite **ARE solution in this case is given as**


## Pll = 411/13


## p22 = q22/13


## P12 = q12/13


# 7 3  = -a1 + (4
 
# + 411/7-l+ 422/r2)1/2
 (8.140)

This results in a stable steady-state Kalman filter. 
## If a 1  = a 2  > 0, 412 # 0, and IQI = 0, then (A,C) is detectable and
 **(A, G) is controllable on the imaginary axis, but (A, G) is not stabilizable (see** **Problem 8.10). The results of Theorem 27 do not apply to this situation,** but Theorem 28 does apply to this situation. it can be shown that Equa- tions (8.139) and (8.140) are both positive semidefinite ARE solutions in this case. If we integrate Equation (8.138) we may come up with Equation (8.139) as the steady-state solution, or we may come up with Equation (8.140) as the *steady-state solution, depending on the initial condition P(0). However, only* one of the solutions will result in a stable Kalman filter.4 
## To be more specific, consider the case a 1  = a 2  = 1, 411 = q12 = 422 = 0,
 
## and 7-1 = 7-2 = 1. For these values, we can simulate the differential Riccati


**41f we use MATLAB's CARE function then we will get the stabilizing solution.**

---

**257**

equations of Equation (8.138) to find the steady-state Riccati solution, the steady-state Kalman gain, and the steady-state estimator, as follows:

*P = [ 2 0 ] o r [ o* 0 2 0 0 *O ]* *K = PCTR-'* 2 0 
$$
= [ o  2 ] 0 r [ ;  4
$$
 4 = (A-KC)?+Ky 
# = (-2 + Ky) or (i + Ky)
 (8.141)

*The ARE solution depends on the initial condition P(0). The first ARE* solution results in a positive semidefinite ARE solution that gives a stable Kalman filter. The second ARE solution results in a positive semidefinite ARE solution that gives an unstable Kalman filter. This agrees with Theorem 28. vvv

**8.5.2**

Consider the steady-state continuous-time Kalman filter.

**The Wiener filter is a Kalman filter**


# 1 = AZ + K(Y - cq
 (8.142)

Taking the Laplace transform of both sides of this equation gives


# (d - A + KC)X(s) = K Y ( s )
 
# X ( S )  = (d - A + KC)-lKY(s)
 (8.143)

*The transfer function from y(t) to ?(t) is identical to the transfer function of the* **Wiener filter [Buc68, Chapter 5],Sha82, [Sag7l, Chapter 71. In other words, the** Wiener filter is a special case of the Kalman filter. The equivalence of discrete-time Wiener and Kalman filtering is discussed in [Men87].

**EXAMPLE8.6**

Consider the scalar system given by


$$
x = -x+w
$$


$$
y = x + w
$$
 (8.144)

where w and w are zero-mean, uncorrelated white noise processes with re- *spective variances Q = 2 and R = 1. The steady-state Kalman filter for this* 
## system can be obtained by solving Equation (8.37) with P = 0, from which
 we obtain 
# 1 = -A*+ (A- l)y
 (8.145)

Taking the Laplace transform of this estimator gives


# (s + &)R(s) = (6
 - 1)Y(s) (8.146)

---

**258**

In other words, the Kalman filter is equivalent to passing the measurement *y(t) through the transfer function G(s), which is given as*

**f i - 1**

S + f i *G(s) = -* **(8.147)**

The impulse response of the Kalman filter is obtained by taking the inverse Laplace transform, which gives


# g(t) = (d-
 **1)e-&t,** *t 2 0* **(8.148)**

Now we will obtain the power spectrum of the state by taking the Laplace **transform of Equation (8.144). This gives**

*sX(s) = -X(s) +W(s)* 1 **s + l** *X ( S )  = -W(s)* **(8.149)**

**We see that the state x ( t )  can be obtained by passing the white noise w(t)** 
## (which has a power spectrum Sw(w) = Q = 2) through the transfer function
 
# L(s) = l/(s + 1). From Equation (3.75) we see how to compute the power
 spectrum of the output of a linear system. This gives the power spectrum of *4 t )*

1 
$$
= ( - j w + l )  (A)'
$$
 **2** *w2 + 1* = - **(8.150)**

The causal Wiener filter for a signal with this power spectrum, corrupted by white measurement noise with a unity power spectrum, was obtained in **Example 3.10. The Wiener filter was found to be identical to the steady-** **state Kalman filter of Equation (8.148). This example serves to illustrate the** equivalence of Wiener filtering and steady-state Kalman filtering. vvv

**8.5.3** **Duality**

It is interesting to note the duality between optimal estimation and optimal control. The optimal estimation problem begins with the system and measurement equations

**(8.151)**

*Recall that Q and R are symmetric matrices. The optimal estimation problem tries* **to find the state estimate 2 that minimizes the cost function**

**tf** 
## Je =
 
# E[(x - 2)T(x - 2)] dt
 **(8.152)** **Jo**

---

**259**

The optimal estimator (the Kalman filter) is given as

*Pe(0) = E[(z(o) - ~(o))(z(o) -*


# P e  = APe + PeAT - PeCTR-lCPe + Q
 *Ke = PeCTR-’* *= A2+Ke(p-C2)* (8.153)

The differential Riccati equation for the optimal estimator is integrated forward in *time from its initial condition Pe(0).* The optimal control problem begins with the system


# 5 = AZ + CU
 (8.154)

*where u is the control variable. The finitetime optimal control problem tries to* fmd the control u that minimizes the cost function

**tf** *J, = zT+zltf + 1 (zTQz + uTRu) dt* (8.155)

*4, Q, and R (which are assumed to be symmetric positive definite matrices) provide* user-specified weighting in the performance index. The optimal controller is given as

*P&)* = 
# P, = -ATP, - PcA + PcCR-lCTP, - Q
 *K, = R-lCTPC* 
$$
u = -K,z
$$
 (8.156)

The differential Riccati equation for the optimal control problem is integrated back- *ward in time from the final condition P(tf). Note the relationships between the* optima1 estimation solution of Equation (8.153) and the optimal control solution of Equation (8.156). The differential Riccati equations have the same form, except **they are negatives of each other, and A and C are replaced by their transposes. The** *estimator gain K, and the controller gain Kc have very similar forms. The Q and* *R covariance matrices in the estimation problems have duals in the cost function* weighting matrices of the optimal control problem. The dual relationship between the estimation and control problems was noted in the very first papers on the Kalman filter [Ka160, Ka1611. Since then, it has been used many times to extrapolate results known from one problem to obtain new results for the dual problem.


## 8.6
 
## SUMMARY


In this chapter, we derived the continuous-time Kalman filter by applying a limiting **argument to the discretetime Kalman filter. However, just as there are several** ways to derive the discretetime Kalman filter, there are also several ways to derive the continuous-time Kalman filter. Kalman and BUCY’S original derivation [Ka161] involved the solution of the Wiener-Hopf integral equation. Another derivation is provided in [ Joh691.

---


[Image on page 32]


260

We have seen that the differential and algebraic Riccati equations are key to the solution of the continuous-time Kalman filter. The scalar version of what is **now known as the Riccati equation was initially studied by such mathematical** **luminaries as James Bernoulli and John Bernoulli in the 1600s’ and Jacopo Riccati,** Daniel Bernoulli, Leonard Euler, Jean-leRond d’ Alembert , and Adrien Legendre in the 1700s. The equation waa first called “Riccati’s equation” by d’Alembert in 1763 [Wat22]. Jacopo Riccati originally entered the University of Padua in 1693 to study law, but he found his true calling when his astronomy professor, Stefan0 Angeli, inspired him to study math. Additional technical discussion of Riccati equations can be found in many places, including [Rei72, Lan95, Abo031. An account of Riccati equations with indefinite quadratic terms is given in [Ion99]. Interesting historical background to the Riccati equation can be found in [Wat22, Bit911. The continuous-time Kalman filter applies to systems with continuous-time white noise in the both the process and measurement equations. Continuous-time white noise is nonintuitive because it has an infinite correlation with itself at the present time, but zero correlation with itself when separated by arbitrarily small nonzero times. However, continuous-time white noise is a limiting case of discretetime white noise, which is intuitively acceptable. Therefore, continuous-time white noise **can be accepted as an approximation to reality. This corresponds to many other** approximations to reality that we accept at face value (e.g., our mathematical system model is an approximation to reality, and our infinite-precision arithmetic is an approximation to reality). The continuous-time Kalman filter applies regardless of the statistical nature **of the noise, as long it is zero-mean. That is, the Kalman filter is optimal even** when the noise is not Gaussian. The Kalman filter was extended in this chapter to systems with correlated process and measurement noise, and with colored me& surement noise. The steady-state Kalman filter provides near-optimal estimation performance at a small fraction of the computational effort of the timevarying Kalman filter. The steady-state Kalman filter is identical to the Wiener filter of Section 3.4, and has an interesting dual relationship to linear quadratic optimal control.

**PROBLEMS**

**Written exercises**

**8.1 Suppose you have two discrete-time systems with identity transition matrices** driven with stationary zero-mean white noise. The first system has a sample period *of T, and the second system has a sample period of T l n  for some integer n > 1.* **The noise in the first system has a covariance of Q. What should the covariance** of the noise in the second system be in order for both states to have the same 
## covariance at times kT (k = 0,1,2,. .
 **a)?**


## 8.2
 
# Show that for a general timevarying matrix Y(t), if Y = AY + YAT, where
 A is a constant matrix, then Y(t) = exp(At)Y(0)exp(ATt).

---

**261**

**8.3 Suppose you have a third-order Newtonian system with**

0 1 0

**A** **=** **[::;I**

& = [K]

*c = [ I  0 0 1*

2 0 1

*R* *=* *l*

*with P(0) = I .* **a) What is the rank of p(O)? How much computational savings in integration** effort can be obtained by using the Chandrasekhar algorithm to find the Kalman gain for this system? 
# b) Find MI and M2 such that P(0) = M1Mr - M2MT.


**8.4** **Show that if S is upper triangular, then S and S-l are also upper triangular.**

**8.5** Show that the product of upper triangular matrices is another upper trian- gular matrix.

**8.6 Find the steady-state solution of the differential Riccati equation for a scalar** **system. Show from your solution how the steady-state solution changes with A, C,** *Q, and R, and give intuitive explanations.*

**8.7** Consider the system of Example 8.3 except with process noise that has a co- *variance of diag(0, q). Find an analytical expression for the steady-state estimation-* error covariance.


## 8.8 Show that if a1 # a2 and 412 # 0 in the system of Example 8.5, then (A, C)
 
## is detectable and (A, G) is stabilizable for all matrices G such that GGT = Q.


**8.9** 
## Show that if a1 = a2 < 0, q12 # 0, and IQI = 0 in the system of Example 8.5,
 **then (A,C) is detectable and ( A , G )  is stabilizable for all matrices G such that** *GGT = Q.*

**8.10** 
## Show that if a1 = a2 > 0, q12 # 0, and IQI = 0 in the system of Example 8.5,
 
## then (A, C) is detectable and (A, G) is controllable on the imaginary axis, but (A, G)
 *is not stabilizable for all matrices G such that GGT = Q.*

**Computer exercises**

8.11 
## Consider the discrete-time system Xk+1 = Xk +wk with the initial condition
 
## 50 = 0. The sample time is T and the variance of the zero-mean process noise Wk is
 
## equal to 2T. Simulate the system a few thousand times for 10 s with: (a) T = 0.5
 
## s; (b) T = 0.4 s; (c) T = 0.2 s. Use the value of Xk at t = 10 s to obtain a statistical
 estimate of ~ ( 1 0 ) 
## = E[x2(10)].
 **a) What is your estimate of P(10) for the three sample times given?** **b) What is the analytically derived value for P(lO)?**

---


[Image on page 34]


**262**

**8.12 Consider the continuous-time scalar system**


$$
x = -x+w
$$


y = z + v


## where w(t) and v(t) are continuous-time white noise with variances Q, = 2 and
 
## R, = 1 respectively. Design a continuous-time Kalman filter to estimate x.
 **a) What is the theoretical steady-state variance of the estimation error?** **b) Simulate the system for 1000 s with discretization step sizes of 0.4, 0.2,** 
## and 0.1 s. What are the resulting experimental estimation-error variances?


## 8.13 Simulate the system of Problem 8.7 for 10 seconds with q = 2 and R =
 **3. Plot the elements of the estimation-error covariance matrix as a function of** time. Compare the experimental RMS estimation errors when using a timcvarying Kalman gain and a constant Kalman gain.

**8.14** **Repeat Problem 8.13 using the correlated noise filter when the process noise** that affects the second state is equal to the measurement noise. How much do the estimation-error variances decrease due to the correlation between the two noise terms?


## 8.15 Consider the system of Example 8.5 with R = I.
 
## Integrate the Riccati equation with a1 = 1, a2 = 2, 411 = 412 = q22 = 1,
 *and P(0) = I .  Plot the Riccati equation solution as a function of time and* **verify that its steady-state value matches the results of Equation (8.139)** and MATLAB’s CARE function. 
## Integrate the Riccati equation with a1 = a2 = -1, qll = 1, q12 = 2,
 
## 422 = 4, and P(0) = I. Plot the Riccati equation solution as a func-
 tion of time and verify that its steady-state value matches the results of **Equation (8.140) and MATLAB’s CARE function.** 
## Integrate the Riccati equation with a1 = a2 = 1, 411 = 1,412 = 2,422 = 4,
 *and P(0) = I. Plot the Riccati equation solution as a function of time and* **verify that its steady-state value matches the results of Equation (8.139)** and MATLAB’s CARE function. 
## Integrate the Riccati equation with a1 = a2 = 1, qll = 1,412 = 2, q22 = 4,
 
## and P(0) = 0. [Note that this is the same as part (c) except for P(O).]
 **Plot the Riccati equation solution as a function of time and verify that** **its steady-state value matches the results of Equation (8.140). Does it** match the results of MATLAB’s CARE function? Does it result in a stable steady-state Kalman filter?