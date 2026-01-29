---
type: chapter
chapter: 13
title: Nonlinear Kalman filtering
---

# CHAPTER 13


Nonlinear Kalman filtering

It appears that no particular approximate [nonlinear] filter is consistently better than any other, though ... any nonlinear filter is better than a strictly linear one. -Lawrence Schwartz and Edwin Stear [Sch68]

All of our discussion to this point has considered linear filters for linear systems. Unfortunately, linear systems do not exist. All systems are ultimately nonlinear. *Even the simple I = V / R  relationship of Ohm’s Law is only an approximation over* a limited range. If the voltage across a resistor exceeds a certain threshold, then the linear approximation breaks down. Figure 13.1 shows a typical relationship between the current through a resistor and the voltage across the resistor. At small input voltages the relationship is approximately linear, but if the power dissipated by the resistor exceeds some threshold then the relationship becomes highly nonlinear. **Even a device as simple as a resistor is only approximately linear, and even then** only in a limited range of operation. So we see that linear systems do not really exist. However, many systems are close enough to linear that linear estimation approaches give satisfactory results. But “close enough” can only be carried so far. Eventually, we run across a system that does not behave linearly even over a small range of operation, and our linear approaches for estimation no longer give good results. In this case, we need to explore nonlinear estimators.

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **395**

---


[Image on page 2]


**396**

**Figure 13.1** for a limited range of operation, but becomes highly nonlinear beyond that range. Typical current/voltage relationship for a resistor. The relationship is linear

Nonlinear filtering can be a difficult and complex subject. It is certainly not as mature, cohesive, or well understood as linear filtering. There is still a lot of room for advances and improvement in nonlinear estimation techniques. However, some nonlinear estimation methods have become (or are becoming) widespread. These techniques include nonlinear extensions of the Kalman filter, unscented filtering, and particle filtering. In this chapter, we will discuss some nonlinear extensions of the Kalman filter. The Kalman filter that we discussed earlier in this book directly applies only to linear systems. However, a nonlinear system can be linearized as discussed in **Section 1.3, and then linear estimation techniques (such as the Kalman or H,** filter) can be applied. This chapter discusses those types of approaches to nonlinear Kalman filtering. **In Section 13.1, we will discuss the linearized Kalman filter. This will involve** finding a linear system whose states represent the deviations from a nominal tra- jectory of a nonlinear system. We can then use the Kalman filter to estimate the deviations from the nominal trajectory, and hence obtain an estimate of the states **of the nonlinear system. In Section 13.2, we will extend the linearized Kalman** filter to directly estimate the states of a nonlinear system. This filter, called the extended Kalman filter (EKF), is undoubtedly the most widely used nonlinear state **estimation technique that has been applied in the past few decades. In Section 13.3,** we will discuss “higher-order” approaches to nonlinear Kalman filtering. These ap- proaches involve more than a direct linearization of the nonlinear system, hence the expression “higher order.” Such methods include second-order Kalman filter- ing, iterated Kalman filtering, sum-based Kalman filtering, and grid-based Kalman filtering. These filters provide ways to reduce the linearization errors that are in- herent in the EKF. They typically provide estimation performance that is better than the EKF, but they do so at the price of higher complexity and computational expense.

---


[Image on page 3]


**397**

**Section 13.4 covers parameter estimation using Kalman filtering. Sometimes, an** engineer wants to estimate the parameters of a system but does not care about estimating the states. This becomes a system identification problem. The sys- tem equations are generally nonlinear functions of the system parameters. System parameters are usually considered to be constant, or slowly timevarying, and a nonlinear Kalman filter (or any other nonlinear state estimator) can be adapted to estimate system parameters.


## 13.1 THE LINEARIZED KALMAN FILTER


In this section, we will show how to linearize a nonlinear system, and then use Kalman filtering theory to estimate the deviations of the state from a nominal state value. This will then give us an estimate of the state of the nonlinear system. We will derive the linearized Kalman filter from the continuowtime viewpoint, but the analogous derivation for discretetime or hybrid systems are straightforward. Consider the following general nonlinear system model:

**(13.1)**

*The system equation f(.) and the measurement equation h(.) are nonlinear func-* tions. We will use Taylor series to expand these equations around a nominal control


## UO, nominal state 20, nominal output yo, and nominal noise values wo and vo. These
 *nominal values (all of which are functions of time) are based on a priori guesses of* **what the system trajectory might look like. For example, if the system equations** represent the dynamics of an airplane, then the nominal control, state, and output *might be the planned flight trajectory. The actual flight trajectory will differ from* this nominal trajectory due to mismodeling, disturbances, and other unforeseen ef- fects. But the actual trajectory should be close to the nominal trajectory, in which case the Taylor series linearization should be approximately correct. The Taylor **series linearization of Equation (13.1) gives**


# h(zo, VO, t) + CAX + MAv
 **(13.2)**

**The definitions of the partial derivative matrices A, B, C,** **L, and M are apparent** from the above equations. The 0 subscript on the partial derivatives means that they are evaluated at the nominal control, state, output, and noise values. The **definitions of the deviations Ax, Au, Aw, and Av are also apparent from the** above equations.

---


[Image on page 4]


**398**

**Let us assume that the nominal noise values wo(t) and vo(t) are both equal to** 0 for all time. [If they are not equal to 0 then we should be able to write them as the sum of a known deterministic part and a zero-mean part, redefine the noise **quantities, and rewrite Equation (13.1) so that the nominal noise values are equal** **to 0. See Problem 13.11. Since wo(t) and vo(t) are both equal to 0, we see that** 
## Aw(t) = w(t) and Av(t) = v(t). Further assume that the control u(t) is perfectly
 *known. In general, this is a reasonable assumption. After all, the control input u(t)* is determined by our control system, so there should not be any uncertainty in its 
## value. This means that uo(t) = u(t) and Au(t) = 0. However, in reality there may
 be uncertainties in the outputs of our control system because they are connected to actuators that have biases and noise. If this is the case then we can express the 
# control as uo(t) + Au(t), where uO(t) is known and Au(t) is a zero-mean random
 variable, rewrite the system equations with a perfectly known control signal, and **include Au(t) as part of the process noise (see Problem 13.2). Now we define the** **nominal system trajectory as**

**(13.3)**

We define the deviation of the true state derivative from the nominal state deriva- **tive, and the deviation of the true measurement from the nominal measurement, as** follows:

**AX** 
## = i - f o


**AY** 
## = Y-yo
 **(13.4)**

**With these definitions Equation (13.2) becomes**

**AX** 
## = AAx+Lw
 
## = AAX+G
 *6 N* *(O,Q),* *Q=LQLT* 
## Ay = CAx+Mv
 
## = CAX+G


*6* **(o,R), R = M R M ~** **(13.5)**

**The above equation is a linear system with state Ax and measurement Ay, so we** **can use a Kalman filter to estimate Ax. The inputs to the filter consist of Ay, which** **is the difference between the actual measurement y and the nominal measurement** **yo. The Ax that is output from the Kalman filter is an estimate of the difference** **between the actual state x and the nominal state 20. The Kalman filter equations** for the linearized Kalman filter are


## A2(0) = 0
 
# P(O) = E [(Ax(O) - Aa(O))(Az(O) - A2(o))T]


## A i  = AA2+K(Ay-CA2)
 
## K = pCTR-'
 
# P = A P  + PAT + Q - PCTR-'CP
 
## 2 = XO +A&
 **(13.6)**

---

**399**

For the Kalman filter, P is equal to the covariance of the estimation error. In the linearized Kalman filter this is no longer true because of errors that creep into the linearization of Equation (13.2). However, if the linearization errors are small then P should be approximately equal to the covariance of the estimation error. The linearized Kalman filter can be summarized as follows.

**The continuous-time linearized Kalrnan filter**

**1. The system equations are given as**

The nominal trajectory is known ahead of time:

(13.7)

(13.8)

2. Compute the following partial derivative matrices evaluated at the nominal trajectory values:

3. Compute the following matrices:

*Q = L Q L ~* 
## R = M R M ~


(13.9)

(13.10)

**4. Define Ay as the difference between the actual measurement y and the nom-**

AY=Y-Yo (13.11) inal measurement yo:

**5. Execute the following Kalman filter equations:**

Ali(0) = 0 *P(O) = E [(Ax(O) - A~~(O))(AX(O)* 
# - Ai(0))T]


## A& = AAli+K(Ay-CA2)
 
## K = PCTR-l
 
# P = A P  + PAT + Q - PCTR-'CP
 (1 3.12)

---

400

**6. Estimate the state as follows:**


# h = 20 + Ah
 **(13.13)**

The hybrid linearized Kalman filter and the discrete-time linearized Kalman filter are not presented here, but if the development above is understood then their derivations should be straightforward.


## 13.2 THE EXTENDED KALMAN FILTER


The previous section obtained a linearized Kalman filter for estimating the states of a nonlinear system. The derivation was based on linearizing the nonlinear system around a nominal state trajectory. The question that arises is, How do we know the nominal state trajectory? In some cases it may not be straightforward to find the nominal trajectory. However, since the Kalman filter estimates the state of **the system, we can use the Kalman filter estimate as the nominal state trajectory.** This is sort of a bootstrap method. We linearize the nonlinear system around the Kalman filter estimate, and the Kalman filter estimate is based on the linearized system. This is the idea of the extended Kalman filter (EKF), which was originally proposed by Stanley Schmidt so that the Kalman filter could be applied to nonlinear spacecraft navigation problems [Be167]. **In Section 13.2.1, we will present the EKF for continuous-time systems with** **continuous-time measurements. In Section 13.2.2, we will present the hybrid EKF,** which is the EKF for continuous-time systems with discrete-time measurements. In **Section 13.2.3, we will present the EKF for discretetime systems with discretetime** measurements.

**13.2.1**


## Combine the & expression in Equation (13.3) with the A4 expression in Equa-
 **tion (13.6) to obtain**

**(13.14)**


## Now choose zo(t) = h(t) so that Ah(t) = 0 and AP(t) = 0. In other words, our
 *linearization trajectory zo(t) is equal to our linearized Kalman filter estimate 2(t).* **Then the nominal measurement expression in Equation (13.3) becomes**

**The continuous-time extended Kalman filter**


# ko + Ah = f ( ~ ,
 **UO, WO,** 
# t) + AAh + K[y - YO - C(2 - ZO)]


**(13.15)**

**and Equation (13.14) becomes** 
## 4 = f(h,
 **U, WO,** *t) + K [Y - h ( h , ~ o ,* *t)]* **(13.16)**


## This is equivalent to the linearized Kalman filter except that we have chosen zo = 2,
 *and we have rearranged the equations to obtain h directly. The Kalman gain K* **is the same as that presented in Equation (13.6). But this formulation inputs the** *measurement y directly, and outputs the state estimate h directly. This is often* **referred to as the extended Kalman-Bucy filter because Richard Bucy collaborated** with Rudolph Kalman in the first publication of the continuoustime Kalman fil- **ter [Kal61]. The continuowtime EKF can be summarized as follows.**

---

**401**


## The continuous-time extended Kalman filter


**(1 3.17)**

**2. Compute the following partial derivative matrices evaluated at the current** state estimate:

**3. Compute the following matrices:**

*Q = L Q L ~* 
$$
ii = M R M ~
$$


**(13.18)**


## ( 13.19)


**4. Execute the following Kalman filter equations:**


$$
f(0) = E[x(O)]
$$
 
$$
P(0) = E [(x(O) - h(O))(x(O) - h(0))T]
$$
 
# i = f(h,
 **U ,  ~ 0 ,** 
# t )  + K [Y - h(h, WO, t)]
 *K = PCTR-I* 
# P = AP + PAT + - PCTR-’CP
 **(13.20)**


## where the nominal noise values are given as wo = 0 and vo = 0.


**EXAMPLE 13.1**

In this example, we will use the continuous-time EKF to estimate the state of a two-phase permanent magnet synchronous motor. The system equations **are given in Example 1.4 and are repeated here:**

*-R* *W X* 
# u a  + 91
 *L* *L* *L*


# U b  + 92
 *-R* **WX** *L* *L* *L* **-3x** **3x** *Fw* **2 J** **2 J** **J**

-2, + - sin 8 + - **i,** =


## ib =
 **-ib** - - cos 8 + -


$$
i j =
$$
 **-i,** 
# sin 8 + - i b
 cos 8 - - 
# + q3


*e* *=* *w* **(13.21)**

---


[Image on page 8]


**402**


## where i, and i b  are the currents in the two windings, 6' and w are the angular
 **position and velocity of the rotor, R and L are the winding resistance and** *inductance, X is the flux constant, and F is the coefficient of viscous friction.* *The control inputs ua and Ub consist of the applied voltages across the two* *windings, and J is the moment of inertia of the motor shaft and load. The* **state is defined as** 
## x =  [ ia
 *i b  w e I'* (13.22)

**The qi terms are process noise due to uncertainty in the control inputs (41** **and 42) and the load torque (43). The partial derivative A matrix is obtained** as

( 13.23) 1

0 *X S I L* **X&/L** **-R/L** **- X C / L** **X 3 X S I L** = [ - ; : / *J* 3Xc/2/J *-F/ J* -3X(xlc + x2s)/2/ J 0 1 0

*where we have used the notation s = sinxq and c = cosx4. Suppose that* we can measure the winding currents with sense resistors so our measurement equations are

(13.24)

where v(1) and 4 2 )  are independent zero-mean white noise processes with standard deviations equal to 0.1 amps. The nominal control inputs are set to

( 13.25)


## The actual control inputs are equal to the nominal values plus 41 and 42 (elec-
 trical noise terms), which are independent zero-mean white noise processes with standard deviations equal to 0.01'amps. The noise due to load torque **disturbances (43) has a standard deviation of 0.5 rad/sec2. Measurements are** obtained continuously. Even though our measurements consist only of the winding currents and the system is nonlinear, we can use a continuous-time EKF (implemented in analog circuitry or very fast digital logic) to estimate the rotor position and velocity. The simulation results are shown in Fig- ure 13.2. The four states are estimated quite well. In particular, the rotor position estimate is so good that the true and estimated rotor position traces are not distinguishable in Figure 13.2. The P matrix quantifies the uncertainty in the state estimates. If the nonlinearities in the system and measurement are not too severe, then the P matrix should give us an idea of how accurate our estimates are. In this example, the standard deviations of the state estimation errors were obtained from the simulation and then compared with the diagonal elements of the *steady-state P matrix that came out of the Kalman filter. Table 13.1 shows a* comparison of the estimation errors that were determined by simulation and

---


[Image on page 9]


**403**

**-True**

**v)** **-loo** **0.5** **1** **1.5** **0** **0.5** **1** **1.5** **Time (Seconds)** **Time (Seconds)**

**Figure 13.2** permanent magnet synchronous motor of Example 13.1. Continuous extended Kalman filter simulation results for the two-phase

**Table 13.1** **Example 13.1 results showing one standard deviation state estimation** errors determined from simulation results and determined from the P matrix of the EKF. These results are for the two-phase permanent magnet motor simulation. This *table shows that the P matrix gives a good indication of the magnitude of the EKF* state estimation errors.

Simulation P Matrix

Winding A Current 0.054 amps 0.094 Amps Winding B Current 0.052 amps 0.094 Amps S P d 0.26 rad/sec 0.44 rad/sec Position 0.013 rad 0.025 rad

*the theoretical estimation errors based on the P matrix. We see that the P* matrix gives a good indication of the magnitude of the estimation errors. vvv

**13.2.2 The hybrid extended Kalman filter**

Many real engineering systems are governed by continuous-time dynamics whereas the measurements are obtained at discrete instants of time. In this section, we will derive the hybrid EKF, which considers systems with continuoustime dynamics and discretetime measurements. This is the most common situation encountered in practice. **Suppose we have a continuous-time system with discretetime measurements as** follows:

---


[Image on page 10]


**404**

( 13.26)

**The process noise w(t) is continuous-time white noise with covariance Q ,  and the** **measurement noise V k  is discretetime white noise with covariance Rk. Between** measurements we propagate the state estimate according to the known nonlinear **dynamics, and we propagate the covariance as derived in the continuous-time EKF** **of Section 13.2.1 using Equation (13.20). Recall that the P expression from Equai** tion (13.20) is given as


# P = AP + PAT + LQLT - PCT(MRMT)-lCP
 ( 13.2 7)

**In the hybrid EKF, we should not include the R term in the P equation because** **we are integrating P between measurement times, during which we do not have** any measurements. Another way of looking at it is that in between measurement 
## times we have measurements with infinite covariance ( R  = oo), so the last term on
 **the right side of the P equation goes to zero. This gives us the following for the** timeupdate equations of the hybrid EKF:

( 13.28)

**where A and L are given in Equation (13.18). The above equations propagate 2** from **to 2;, and P from PzVl to P;. Note that wo is the nominal process** *noise in the above equation; that is, wo(t) = 0.* At each measurement t'ime, we update the state estimate and the covariance as 
## derived in the discretetime Kalman filter (Chapter 5 ) :


## where 210 is the nominal measurement noise; that is, vo = 0. Hk is the partial
 **derivative of hk(Xk,Vk) with respect to X k ,  and Mk is the partial derivative of** **hk(Zk, V k )  with respect to V k .  Hk and Mk are evaluated at 2;.** **Note that Pk and Kk cannot be computed offline because they depend on Hk and** **Mk, which depend on 2;, which in turn depends on the noisy measurements. There** fore, a steady-state solution does not (in general) exist to the extended Kalman filter. However, some efforts at obtaining steady-state approximations to the ex- tended Kalman filter have been reported in [Saf78]. **The hybrid EKF can be summarized as follows.**

---


[Image on page 11]


**The hybrid extended Kalman filter**

**1. The system equations with continuous-time dynamics and discretetime mea-** surements are given as follows:

**(13.30)**

**2. Initialize the filter as follows:**

**2;** *= E[zo]* 
# P,s = E [(zo - 2;)(zo
 - ?;)'I **(13.31)**


## 3. For k = 1,2, . . ., perform the following.


# (a) Integrate the state estimate and its covariance from time (k - 1)+ to
 **time k- as follows:**

**2** **=** 
## P = A P + P A ~ + L Q L ~
 **(13.32)**

**where F and L are given in Equation (13.18). We begin this integration** 
## process with 2 = 2t-l and P = P:--,. At the end of this integration we
 
## have 2 = 2; and P = PF.
 **(b) At time k, incorporate the measurement Y k  into the state estimate and** estimation covariance as follows:


## f (2, u, 0, t )


**Kk** 
## = PFHF(HkPFHF 4- MkRkM?)-l
 **2' k** 
# = 2; -b Kk(yk - hk(?;, 0, tk))
 **(13.33)** 
# Pk+ = (I - KkHk)Pi(I - KkHk)' + KkMkRkMrKT


**Hk and Mk are the partial derivatives of h k ( Z k ,  O k )  with respect to Z k  and**


## V k ,  and are both evaluated at 2 i .  Note that .other equivalent expressions
 **can be used for Kk and P z ,  as is apparent from Equation (5.19).**

**EXAMPLE 13.2**

In this example, we will use the continuous-time EKF and the hybrid EKF **to estimate the altitude 21, velocity 22, and constant ballistic coefficient 1/23** **of a body as it falls toward earth. A rangemeasuring device measures the** altitude of the falling body. This example (or a variant thereof) is given in several places, for example IAth68, Ste94, JulOO]. The equations for this system are

**(13.34)**

**403**

---

**406**

**As usual, w, is the noise that affects the ith process equation, and v is the** 
## measurement noise. po is the air density at sea level, k is a constant that
 defines the relationship between air density and altitude, and g is the acceler- ation due to gravity. The partial derivative matrices for this system are given **as follows:**

(13.35)

**We will use the continuous-time system equations to simulate the system. For** the hybrid system we suppose that we obtain range measurements every 0.5 **seconds. The constants that we will use are given as**

**po** = 0.0034 lb-sec2/ft4


## g = 32.2 ft/sec2
 k = 22OOOft E[v2(t)] = 100 ft2 *E[w:(t)] = 0* 
## (i = 1,2,3)
 (13.36)

**The initial conditions of the system and the estimator are given as**

xo =

5; =

[ 100,000 -6,000 1/2,000 3'

[ 100,010 -6,100 1/2,500 1'

[ o 0 1/250,000 (1 3.37) 1

500 0 0 0 20,000 0 *Po+ =*

We use rectangular integration with a step size of 0.4 msec to simulate the **system, the continuoustime EKF, and the hybrid EKF (with a measurement** time of 0.5 sec). Figure 13.3 shows estimation-error magnitudes averaged over 100 simulations for the altitude, velocity, and ballistic coefficient reciprocal of **the falling body. We see that the continuoustime EKF appears to perform** **better in general than the hybrid EKF. This is to be expected since more** **measurements are incorporated in the continuoustime EKF. The RMS esti-** mation errors averaged over 100 simulations was 2.8 feet for the continuous **time EKF and 5.1 feet for the hybrid EKF for altitude estimation, 1.2 feet/s** **for the continuous-time EKF and 2.0 feet/s for the hybrid EKF for velocity** **estimation, and 213 for the continuoustime EKF and 246 for the hybrid EKF**

---

407

for the reciprocal of ballistic coefficient estimation. Of course, a continuous- **time EKF (in analog hardware) would be more difficult to implement, tune,** **and modify than a hybrid EKF (in digital hardware).**

**m**


## a
 
## 3
 .,- .- .,-

**"0** **2** **4** **6** **8** **10** **12** **14** **16**

**. , I , , . ,  Continuous**

**0** **2** **4** **6** **0** 10 **12** **14** **16** **Time**

**-** **0**

**Figure 13.3** **Example 13.2 altitude, velocity, and ballistic coefficient reciprocal** estimation-error magnitudes of a falling body averaged over 100 simulations. The continuous- time EKF generally performs better than the hybrid EKF.

vvv


## 13.2.3 The discrete-time extended Kalman filter


**In this section, we will derive the discrete-time EKF, which considers discretetime** dynamics and discretetime measurements. This situation is often encountered in **practice. Even if the underljring system dynamics are continuous time, the EKF** usually needs to be implemented in a digital computer. This means that there might not be enough computational power to integrate the system dynamics as **required in a continuous-time EKF or a hybrid EKF. So the dynamics are often** **discretized (see Section 1.4) and then a discrete-time EKF can be used.** Suppose we have the system model


## We perform a Taylor series expansion of the state equation around z k - 1  =
 
## and W k - 1  = 0 to obtain the following:


---


[Image on page 14]


**408**

*F k - 1  and L k - 1  are defined by the above equation. The known signal '& and the* *noise signal 'I& are defined as follows:*


## We linearize the measurement equation around Xk = 2; and V k  = 0 to obtain


*H k  and M k  are defined by the above equation. The known signal Zk and the noise* **signal 6 k  are defined as**

**We have a linear statespace system in Equation (13.39) and a linear measurement** **in Equation (13.41). That means we can use the standard Kalman filter equations** to estimate the state. This results in the following equations for the discretetime extended Kalman filter.

**(13.43)**

The discretetime EKF can be summarized as follows.

---

**409**

**The discrete-time extended Kalman filter**

**1. The system and measurement equations are given as follows:**

**2. Initialize the filter as follows:**


## 3. For k = 1,2,
 **e** **,** 
## perform the following.


(a) Compute the following partial derivative matrices:

**(1 3.44)**

**(13.45)**

**(13.46)**

Perform the time update of the state estimate and estimation-error co- variance as follows:

Compute the following partial derivative matrices:

**(13.48)**

Perform the measurement update of the state estimate and estimation- error covariance as follows:

**Note that other equivalent expressions can be used for Kk and Pk+, as** **is apparent from Equation (5.19).**

---


[Image on page 16]


410


## 13.3 HIGH E R-0 R D  ER APPROACH ES


More refined linearization techniques can be used to reduce the linearization error in the EKF for highly nonlinear systems. In this section, we will derive and illustrate two such approaches: the iterated EKF, and the second-order EKF. We will also briefly discuss other approaches, including Gaussian sum filters and grid filters.

**13.3.1**

In this section, we will discuss the iterated EKF. We will confine our discussion here to discretetime filtering, although the concepts can easily be extended to continuous or hybrid filters. **When we derived the discretetime EKF in Section 13.2.3, we approximated** **h ( Z k ,  V k )  by expanding it in a Taylor series around 2;, as shown in Equation (13.41):**

**The iterated extended Kalman filter**

Based on this linearization, we then wrote the measurement-update equations as **shown in Equation (13.43):**

**Kk** 
# = P i H z ( H k P i H z  + MkRkM?)-l
 
## P z  = ( I - K k H k ) P r
 
## 2i.k+ = 2; + K k [ Y k  - h k ( 2 ; , 0 ) ]
 **(13.51)**

**The reason that we expanded h ( Z k )  around 2; was because that was our best es-** **timate of X k  before the measurement at time k is taken into account. But after we** *implement the discrete EKF equations to obtain the a posteriori estimate @, we* **have a better estimate of X k .  So we can reduce the linearization error by reformu-** **lating the Taylor series expansion of h ( Z k )  around our new estimate. If we then use** **that new Taylor series expansion of h ( X k )  and recalculate the measurement-update** **equations, we should get a better a posteriori estimate of 2:. But then we can** **repeat the previous step; since we have an even better estimate of x k ,  we can again** **reformulate the expansion of h ( X k )  around this even better estimate to get an even** *better estimate. This process can be repeated as many times as desired, although* for most problems the majority of the possible improvement is obtained by only relinearizing one time. 
## We use the notation 2i';z,+ to refer to the a posteriori estimate of x k  after i r e h -
 **earizations have been performed. So 2k,O is the a posteriori estimate that results** **from the application of the standard EKF. Likewise, we use P& to refer to the** **approximate estimation-error covariance of 2i.k+,i, Kk,+ to refer to the Kalman gain** **that is used during the ith relinearization step, and Hk,+ to refer to the partial** 
## derivative matrix evaluated at the X k  = 2i.k+,i.
 With this notation, we can describe an algorithm for the iterated EKF as follows. **First, at each time step k we initialize the iterated EKF estimate to the standard** EKF estimate: **q0** 
## = 22


## PC0 = Pk+
 
## ( 13.52)


---


[Image on page 17]


411


## Second, for i = 0, 1, . . . , N ,  evaluate the following equations:


*ah* 
# Hk,a = -


# Kk,a = pFHci(Hk,tpFHc+ + MkRkM?)-l


# a x  IP;,


# p c Z + l  = (1 - Kk,%Hk,%)pL


# 2i,i+1 = 2 i  + K k , i [ Y k  - h k ( ? i ) ]
 **(13.53)**


## This is done for as many steps as desired to improve the linearization. If N = 0
 then the iterated EKF reduces to the standard EKF. We still have to make one more modification to the above equations to obtain the iterated Kalman filter. Recall that in the derivation of the EKF, the P measurement update equation was originally derived from the following first-order Taylor series expansion of the measurement equation:


## Y k  = h(xk)


# % h(2i) + HIS; ( x k  - 2;)
 **(13.54)**

**To derive the measurement-update equation for 2 we evaluated the right side at** 
## the a priori estimate 2 i  and subtracted from yk to get our correction term (the
 residual) :


# T k  = y k  - h(2i) - HI,; ( P i  - 2 i )


# = Yk - h(2;)
 
## ( 13.55)


With the iterated EKF we instead want to expand the measurement equation **around ii,a** as follows:

**Yk** 
# h(?;,%) + HI,+ ( x k  - 2;,,)
 
## ( 13.56)


**To derive the iterated EKF measurement-update equation for 2, we evaluate the** 
## right side of the above equation at the a priori estimate 2 i  and subtract from Y k
 to get our correction term:


# T k  = Y k  - h(hi,,) - Hk,i($L - *k,%)
 +

**k,.**


## ( 13.57)


**This gives the iterated EKF update equation for 2 as**


# *;,,+I = 2 i  + K k , i [ Y k  - h(?;,,) - Hk,i(?i - *$,%)I
 **(1 3.58)**

**The iterated EKF can then be summarized as follows.**

**The iterated extended Kalman filter**

**1. The nonlinear system and measurement equations are given as follows:**

**(13.59)**

---

**412**

**2. Initialize the filter as follows.**

**2;** *= E(X0)* 
## PO+ = E [(ZO - ~ o ) ( x o


## 3. For k = 1,2, . . ., do the following.


(13.60)

Perform the following timeupdate equations:

**T** 
## p i  = Fk-1Pk+-1Fz-1+
 **L k - 1 Q k - 1 L k - 1** 
## 2 i  = .fk-l(2:-1,
 **U k - 1 7 0 )** (13.61)

**where the partial derivative matrices F k - 1  and L k - 1  are defined as fol-** lows:

( 13.62)

**Up to this point the iterated EKF is the same as the standard discre&** time EKF.

Perform the measurement update by initializing the iterated EKF esti- mate to the standard EKF estimate:

(13.63)


## For i = 0,1,. . , N ,  evaluate the following equations (where N is the
 desired number of measurement-update iterations) :


## H k , a  =
 ax &t>%

*The final a posteriori state estimate and estimation-error covariance are* given as follows:

(13.65)

**An illustration of the iterated EKF will be presented in Example 13.3.**

---

**413**

**13.3.2**

**The second-order EKF is similar to the iterated EKF in that it attempts to reduce** **the linearization error of the EKF. In the iterated EKF of the previous section, we** refined the point at which we performed a first-order Taylor series expansion of the **measurement equation h(.). In the second-order EKF we instead perform a seconh** 
## order Taylor series expansion of f (.) and h(.). The second-order EKF presented in
 this section is based on [Ath68, Ge1741. In this section, we will consider the hybrid system with continuous-time system dynamics and discretetime measurements:

**The second-order extended Kalman filter**

**(13.66)**

**In the standard EKF, we expanded f (5,** *u, w, t )  using a first-order Taylor series. In* this section, we will consider only the expansion around a nominal x, ignoring the expansion around nominal u and w values. This is done so that we can present the **main ideas of the second-order EKF without getting too bogged down in notation.** The development in this section can be easily extended to second-order expansions around u and w once the main idea is understood. **The first-order expansion of f (z, u, w,** 
## t )  around z = 2 is given as


## f (2,217 w,
 
# t )  = f (2, uo, 'wo, t) +
 
# (a: - 2)
 **(1 3.67)**


## In the standard EKF, we evaluated this expression at 2 = 2 to obtain our time-
 **update equation for 2 as** 
# i = f (2, u g ,  wo,
 *t)* **(13.68)**


## In the second-order EKF we expand f (5, u, w, t )  with an additional term in the
 Taylor series:

af I*


## where n is the dimension of the state vector, fi is the ith element of f(z,
 *u, w, t),* 
## and the 4i vector is defined as an n x 1 vector with all zeros except for a one in the
 **ith element. The quadratic term in the summation can be written as**

(r-f)Tg~i.(5-*)=n [Ti - 
# 1 i. (5 - *)(. - *)T 1
 **(1 3.70)**


## Since we do not know the value of (z -2)(z -2)T in the above equation, we replace
 it with its expected value, which is the covariance of the Kalman filter, to obtain

**(13.71)**

---


[Image on page 20]


**414**


## We then evaluate Equation (13.69) at z = 2 and substitute the above expression
 **in the summation to obtain the timeupdate equation for 2 as**

**(13.72)**

**The timeupdate equation for P remains the same as in the standard hybrid EKF** 
## as shown in Equation (13.28):


*P = F P + P F ~ + L Q L ~* **(13.73)**

Now we will derive the measurement-update equations. Suppose that the measurement- update equation for the state estimate is given as

**2 + -** 
# k - z k
 
# A -  + K k  [Yk - h(2i, t k ) ]  - r k
 
## (1 3.74)


**where K k  is the Kalman gain to be determined, and T k  is a correction term to be** **determined. We will choose Irk so that the estimate 2: is unbiased, and we will** **then choose K k  to minimize the trace of the covariance of the estimate.** **If we define the estimation errors as**

**(13.75)**


## we can see from Equations (13.66) and (13.74) that


# e l  = e i  - K k  [ h ( z k , t k )  - h ( ? i , t k ) ]  - K k V k  -k r k
 **(13.76)**

**Now we perform a second-order Taylor series expansion of h ( z k , t k )  around the** **nominal point 2; to obtain**

**(13.77)**


## where H k  is defined by the above equation, m is the dimension of the measurement
 **vector, and h, is the ith element of h ( z k ,  t k ) .  This gives the a posteriori estimation** error as

**m**

**where D k , %  is defined as**

**(13.79)**

---


[Image on page 21]


**415**


## Taking the expected value of both sides of Equation (13.78), assuming that E(e;) =
 **0, and making the same approximation as in Equation (13.71), we can see that in** 
## order to have E ( e t )  = 0 we must set


**m** **(13.80)**

**Defining P$ as** 
## p$ =
 
## [ek + (ek + T  ]
 **(13.81)**

and using the above equations, it can be shown after some involved algebraic cal- culations [Ath68] that


# P$ = (1 - KkHk)pi(I - KkHk)T f Kk(Rk 4- &)K;
 
## ( 13.82)


**where the matrix Ak is defined as**

**Now we define a cost function Jk that we want to minimize as a weighted sum of** estimation errors:

**(13.84)**

**where Sk is any positive definition weighting matrix. The Kk that minimizes this** cost function can be found as


# Kk = PiHT (HkPiH: + Rk + h k ) - '
 **(13.85)**

**This gives the P z  matrix from Equation (13.82) as**


# P z  = P; - PLHT (HkPiHT f Rk f hk)-'HkP;
 **(13.86)**

**Now we need to figure out how to evaluate the A, ,matrix in Equation (13.83). Note** **that Ak can be written as the double summation**

**(i3.87)** The product +i$ *is an m x m matrix whose elements are all zero except for the* element in the zth row and j t h  column. Therefore, the element in the ith row and **jth column of A k  can be written as**

This expression can be evaluated with the following lemma [Ath68].

---


[Image on page 22]


416

- 0 -

0 I t 0

0 - -


## Lemma 6 Suppose we have the n-element random vector x N N(0, P). Then


*E [zT7(AzzT)] = 0* *E [ TT(hxTBxxT)] = E [ T7(AxzT) T7(BxxT)]* *= 2 q A P B P )  + T7(AP)T7(BP)* (13.89)

*where A and B are arbitrarg n x n matrices.*

Using this lemma with Equation (13.88) we can see that

(1 3.90)

This equation, along with Equations (13.74), (13.80), (13.82), and (13.85), specify **the measurement-update equations for the second-order EKF. The second-order** **EKF can be summarized as follows.**

1 
## A k ( i , j )  = p ( D k , z P p k , j P F )


**The second-order hybrid extended Kalrnan filter**

**1. The system equations are given as follows:**

x = *f ( x ,  u, w,* *t)*


# Y k  = h(xk, t k )  + Vk


w(t) *N* *(0, Q )*

**Vk** **(0,Rk)**

**2. The estimator is initialized as follows:**

3. The timeupdate equations are given as


## p = F P + P F ~ + L Q L ~


## di =
 ith element

(13.91)

(13.92)

(13.93)

---


[Image on page 23]


**417**

**4. The measurement update equations are given as**

Note that setting the second partial derivative matrices in this algorithm to zero matrices results in the standard hybrid EKF.

**EXAMPLE 13.3**

In this example, we compare the performance of the EKF, the second-order EKF, and the iterated EKF for the falling body problem described in Exam- **ple 13.2. A similar comparison was shown in [Wis69], where it was concluded** that the iterated EKF had better RMS error performance, but the second- **order filter had smaller bias. The system equations are the same as those** shown in Example 13.2:

In this example, we change the measurement system so that it does not mea- sure the altitude of the falling body, but instead measures the range to the measuring device. The measuring device is Iocated at an altitude a and at a *horizontal distance M from the body's vertical line of fall. The measurement* equation is therefore given by

This makes the problem more nonlinear and hence more difficult to estimate (i.e., in Example 13.2 we had a nonlinear system but a linear measurement, whereas in this example we have nonlinearities in both the system and the measurement equations). The partial derivative F matrix for the EKFs are given in Example 13.2. The other partial derivative matrices used in the **second-order EKF are given as follows:**

---


[Image on page 24]


**418**

*H* *=* - -

**L** **=**

dh - ax [ ( X l  - a)(M2 + (XI - a)2)-1/2 af **dW**

*0 0 ]* -

[ s  8 H]

d2hl -

h - y l  - (21 - a)2h-2) 0 0

*0* *0*

( 13.97)

*0* i’ *0*

x$x3/2k2 - ~ 2 ~ 3 / k  -~,2/2k

- ~ $ / 2 k 2 2 **x 2** 0 1 -xzz3/k 23

Table 13.2 shows the performances of the EKFs (averaged over 20 simulation runs). It is seen that second-order EKF provides significant improvement over the first-order EKF for altitude and velocity estimation, but for some reason it actually provides worse performance for ballistic coefficient estimation. Also note that the iterated EKF provides only slight improvement over the first- **order EKF, and (as expected) the iterated EKF performs better when more** iterations are executed for the linearization refinement.

**Table 13.2** different EKF approaches for tracking a falling body. **Example 13.3 results. A comparison of the estimation errors of**

Filter

~ ~~~ Altitude Velocity Ballistic Coefficient

First-order EKF 758 feet 518 feet/sec 0.091 feet3/lb/sec2 Second-order EKF 356 483 0.129 
## Iterated EKF ( N  = 2)
 755 517 0.091 
## Iterated EKF ( N  = 3)
 745 516 0.091 
## Iterated EKF ( N  = 4)
 738 509 0.091 
## Iterated EKF ( N  = 5)
 733 506 0.091 
## Iterated EKF ( N  = 6)
 723 506 0.091

We conclude from this that the second-order filter has better estimation **performance. However, the implementation is much more difficult and re-** quires the computation of second-order derivatives. In this example, the second-order derivatives could be taken analytically because we have explicit

---


[Image on page 25]


419

analytical system and measurement equations. In many applications second- order derivatives will not be available analytically, and approximations will inevitably be subject to error. These results are different than reported in [Wis69], where it was shown that the iterated EKF performed better than the second-order EKF. The different conclusions between this book and [Wis69] show that comparisons between different algorithms are often subjective. Perhaps the discrepancies are due to differences in implementations of the filtering algorithms, differ- ences in implementations of the system dynamics or random noise generation, differences in the way that the estimation errors were measured, or even dif- ferences in the computing platforms that were used. vvv The second-order filter was initially developed by Bass [Bas661 and Jazwin- ski [Jaz66]. A Gaussian second-order filter was developed by Athans [Ath68] and Jazwinski [ Jaz701, in which fourth-order terms in Taylor series approximations are retained and approximated by assuming that the underlying probabilities are Gaus- sian. A small correction in the original derivations of the second-order EKF was reported by Rolf Henriksen [Hen82]. Although the second-order filter often provides improved performance over the extended Kalman filter, nothing definitive can be said about its performance, as evidenced by an example of an unstable second-order filter reported in [Kus67]. Additional comparison and analysis of some nonlinear Kalman filters can be found in [Sch68, Wis69, Wis70, Net781. A simplified version of Henriksen's discretetime second-order filter can be summarized as follows.

**The second-order discretetime extended Kalman filter**

1. The system equations are given as follows:

**2. The estimator is initialized as follows:**

3. The time update equations are given as follows:

(13.98)

(13.99)


# PF+l = FPcFT + Q k


---


[Image on page 26]


420

(13.100)


## 4. The measurement update equations are given as follows:


A more general version of the above algorithm can be found in [Hen82]. Similar to the hybrid second-order EKF presented earlier in this section, we note that set- ting the second-order partial derivative matrices in this algorithm to zero matrices results in the standard discretetime EKF.


## 13.3.3
 **Other approaches**

We have considered a couple of higher-order approaches to reducing the lineariza- tion error of the EKF. We looked at the iterated EKF and the second-order EKF, but other approaches are also available. For example, Gaussian sum filters are based on the idea that a non-Gaussian pdf can be approximated by a sum of Gaussian pdfs. This is similar to the idea that any curve can be approximated by a piecewise constant function. Since the true pdf of the process noise and measurement noise *can be approximated by a sum of M Gaussian pdfs, we can run M Kalman filters* *in parallel on M Gaussian filtering problems, each of them optimal filters, and then* combine them to obtain an approximately optimal estimate. The number of fil- *ters M is a trade-off between approximation accuracy (and hence optimality) and* computational effort. This idea was first mentioned in [Aok65] and was explored in [Cam68, Sor7lb, Als74, Kit891. The Gaussian sum filter algorithm presented in [Ah721 can be summarized as follows.

---


[Image on page 27]


**421**


## The Gaussian sum filter


**1. The discrete-time n-state system and measurement equations are given as** follows:

**2. Initialize the filter by approximating the pdf of the initial state as follows:**

**The a,-,% coefficients (which are positive and add up to l), the 2i.,$, means, and** **the PL covariances, are chosen by the user to provide a good approximation** to the pdf of the initial state.


## 3. For k = 1,2,. . ., do the following.


*(a) The a priori state estimate is obtained by first executing the following* 
# time-update equations for i = 1, . , M :


*The pdf of the a priori state estimate is obtained by the following sum:*

**M** pdf(fi) = **aktN(*,, p i )** 
## ( 13.105)
 **2=1**

*(b) The a posteriori state estimate is obtained by first executing the following* 
# measurement update equations for i = 1, - . . , M :


# Hk2 = ah./
 **dxk i;,**


## Kk2 = p ~ H ~ ( H k 2 p ~ H ~
 
# + & ) - I
 **p;** 
## = p i  -KkzHkzPi
 
## 2t2 =
 
# f Kkz [Yk - hk(2ii, o)]
 **(13.106)**

**The weighting coefficients akz for the individual estimates are obtained** as follows:

---

422

( 13.107)

**Note that the weighting coefficient aka is computed by using the me&** **surement yk to obtain the relative confidence P k z  of the estimate 2ii.** **The pdf of the a posteriori state estimate is obtained by the following** sum:

**M** pdf(2:) = 
# akzN(g&, PL)
 ( 13.108) **2=1**

This approach can also be extended to smoothing [Kit94]. Similar approaches can be taken to expand the pdf using non-Gaussian functions [Aok67, Sor68, Sri70, deF71, Hec71, Hec73, Mcr75, Wi181, Kit87, Kra881. A related filter has been derived for the case where either the process noise or the measurement noise is strictly Gaussian, but the other noise is Gaussian with heavy tails [Mas75, Tsa831. This is motivated by the observation that many instances of noise in nature have pdfs that are approximately Gaussian but with heavier tails [Mas77]. Another approach to nonlinear filtering is called grid-based filtering. In grid- based filtering, the value of the pdf of the state is approximated, stored, propagated, and updated at discrete points in state space [Buc69, Buc711; [Spa88, Chapter 61. This is similar to particle filtering (discussed in Chapter 15), except in particle filtering we choose the particles to be distributed in state space according to the pdf of the state. Grid-based filtering does not distribute the particles in this way, and hence has computational requirements that increase exponentially with the dimension of the state. Grid-based filtering is even more computationally expensive than particle filtering, and this has limited its application. Furthermore, particle filtering is a type of “intelligent” grid-based filtering. This seems to portend very little further work in grid-based filtering. Richard Bucy suggested yet another approach to nonlinear filtering [Buc65]. In- stead of linearizing the system dynamics, compute the theoretically optimal nonlin- ear filter, and then linearize the nonlinear filter. However, the theoretically optimal nonlinear filter is very difficult to compute except in special cases.


## 13.4
 **PARAMETER ESTIMATION**

State estimation theory can be used to not only estimate the states of a system, but also to estimate the unknown parameters of a system. This may have first been suggested in [Kop63]. Suppose that we have a discretetime system model, but the **system matrices depend in a nonlinear way on an unknown parameter vector p :**

---

**423**


# Z k f l  = F k ( p ) x k  -k G k ( P ) U k  f L k ( P ) w k


## Yk = H k x k + v k
 **p** = unknown parameter vector (13.109)

**In this model, we are assuming that the measurement is independent of p ,  but this** is only for notational convenience. The discussion here can easily be extended to **include a dependence of Yk on p .  Assume that p is a constant parameter vector.** **We do not really care about estimating the state, but we are interested in esti-** **mating p .  This is the case, for example, in the aircraft engine health estimation** problem [KobOS, Sim05aI. In those papers it was assumed that we want to estimate aircraft engine health (for the purpose of maintenance scheduling), but we do not really care about estimating the states of the engine. **In order to estimate the parameter p ,  we first augment the state with the pa-** **rameter to obtain an augmented state vector x':**


# x i  = [ ; ]
 (13.110)


## If p k  is constant then we model pk+l = p k + W p k ,  where Wpk is a small artificial noise
 **term that allows the Kalman filter to change its estimate of p k .  Our augmented** system model can be written as

(13.11 1)

**Note that !(xi, U k ,  W k ,  W p k )  is a nonlinear function of the augmented state xi.** We can therefore use an extended Kalman filter (or any other nonlinear filter) to **estimate x i .**

**EXAMPLE 13.4**

This example is taken from [Ste94]. Suppose we have a second-order system governed by the following equations:

**X I +  2<wnXl+ wnxl** **2** 
## = W ~ W
 (13.112)

where w, is the natural frequency of the system, < is the damping ratio, and **the input w is zero-mean noise. A statespace model for this system can be** written as

(13.1 13) 
# [5:] = [ -w:
 **O** *-2<wn*

---

**424**


## Suppose that -2<wn is known, but 6 and wn are unknown. We want to
 
## estimate -wt. Suppose that both 21 and 2 2  are available for measurement.
 
## We define the known parameter as b; that is, b = -2Cwn. We define a new
 state element equal to the parameter that we want to estimate. That is, 
## 53 = -wf. We then form a n  augmented system model as follows:


**(1 3.114)**

**where w p  is an artificial noise term that we add to the system that allows** **the Kalman filter to modify its estimate of 23. We can use an extended** Kalman filter to estimate the augmented state. First we need to find the partial derivative matrices:

0 1 0

**9’,W;I** **0** **1** **0**

**0** **0** **0** 
# = [ 23 b
 *P I ]*

0 
# = [ -;3 ;]


The continuous-time extended Kalman filter can be written as

**(13.115)**

i’ - 
# - f(2’,
 *0) + K(y - HP’)*

*K = PHTR-‘* 
# P = F P  + PFT + LQLT - PHTR-‘HP
 **(1 3.116)**

**Figure 13.4 illustrates the results of a typical simulation of the extended** Kalman filter that is used to estimate -wi for this system. The true system 
## parameters are wn = 2 and 6 = 0.1, so -wt = -4. Suppose that we begin by
 *estimating -w:* **as -8 with an initial estimation variance of 20. Figure 13.4** *shows that the error in our estimate of -w: gradually decreases toward zero,* and the estimation variance gradually decreases. We set the variance of the **artificial noise w p  equal to 0.1 in this example. This allows the Kalman filter**

---

**425**

**I0** **1 0** **20** **40** **60** **80** 100

**0** **20** **40** **60** **80** **100** **Seconds**

**Figure 13.4** **Example 13.4 results.** Typical parameter estimation performance and *parameter uncertainty for an extended Kalman filter estimating -uK for a second-order* system. The estimation error of the unknown parameter and its variance gradually decrease toward zero.

*to more readily adjust its estimate of -wi, but also may prevent the filter* from converging to the true value (see Problem 13.23). vvv


## 13.5 SUMMARY


Optimal state estimators can be derived for general classes of nonlinear systems as shown in [Kus67], but the filters are generally infinite dimensional, which makes them impractical for implementation. Finite-dimensional, optimal, nonlinear state estimators can be derived for more restricted classes of nonlinear systems [Liu80], but the restriction on the classes of applicable systems are significant enough to prevent wide applicability. Because of these factors, nonlinear Kalman filtering is the most widespread approach to state estimation for nonlinear systems. It is interesting to note that the first applications of Kalman filtering were on nonlinear orbit-estimation problems [Bat62]. Some early investigations in nonlinear Kalman filtering can be found in [Cox64, Fri661. Whereas stability and convergence **results are readily available for the linear Kalman filter, such results are much more** difficult to obtain for nonlinear Kalman filtering. Some convergence results for nonlinear Kalman filtering are found in [Urs80]. If the nonlinearities have known bounds then the Riccati equation can be modified in a simple way to guarantee stability for the continuous-time EKF [Rei98]. Conditions needed to guarantee the boundedness of the discrete-time EKF error covariance can be related to the observability of the underlying nonlinear system [Dez92, Son951.

---


[Image on page 32]


**426**

**PROBLEMS**

**Written exercises**

**13.1 Consider the scalar system**


$$
x = -x+w
$$


*y = x + v*

The process noise has a mean value of 2, and the measurement noise has a mean *value of 3. Redefine the noise quantities and the state to obtain an equivalent* system of the form

*X'* *= AX'+ Bu+w'*


## y = CX'+ 0'


*so that the new noise quantities w' and v' both have mean values of 0.*

**13.2 Consider the scalar system**

*X = - x + u + w*

*w is zero-mean process noise with a variance of Q. The control has a mean value* **of UO, an uncertainty of 2 (one standard deviation), and is uncorrelated with w.** Rewrite the system equations to obtain an equivalent system with a normalized control that is perfectly known. What is the variance of the new process noise term in the transformed system equation?


# 13.3 Suppose that x is a constant scalar, and yk = fi(1 + V k )  are noisy mea-
 
## surements, where Vk N N(0, R).
 *a) An intuitive way to estimate x is to set z k  = y:.* Compute the mean and variance of the estimation error for this estimate. Your answer should be *a function of x and R. Hint: recall that E(vi) = 0 and E(vi) = 3R2.* **b) Perhaps a better estimate for X k  could be obtained by averaging all pre-** vious values of y:. That is,

Compute the mean and variance of the estimation error for this estimate. **Your answer should be a function of k, x, and R. Note that if you substi-** 
## tute k = 1 into your solution, you should get the same answer as part (a).
 
## What is the variance as k + cm?


## c) Write the extended Kalman filter equations to estimate x. What is the
 
## theoretical mean and variance of the EKF estimate as k -+ cm?


**13.4 Consider the system**

---

**427**

**where W k  and Wk are uniformly distributed, uncorrelated, zero-mean white noise** **processes with variances Q and R, respectively.** 
## a) What is the mean of the a posteriori estimation error for the discrete EKF?
 **b) Modify the measurement equation by subtracting the known bias of the** measurement noise so that the modified measurement noise is zero-mean. What is the variance of the modified measurement noise?

**13.5 Consider the nonlinear system**


## Find the nominal values for Xk and Yk when 20 = 0 and Uk = 1.


**13.6** 
# + W k ,  where W k  is zero-mean. The initial
 
## state 20 is uniformly distributed between 0 and 1. An EKF is initialized with


**3;';** 
## = E(z0). What is E(zl)? What is 3;';?
 This problem illustrates the fact that the state estimate of an EKF is not always equal to the expected value of the state.

**13.7 Find the terminal velocity of the falling body of Example 13.2 if the terminal** **velocity occurs at an altitude of 1 mile.**

**13.8 Consider the hybrid scalar system**


## Consider the system 2k+1 =


The estimator that is used for the system is

*Suppose that the state ~ ( t )* is normally distributed with a mean of zero and a *variance of P,.* 
## a) Find an equation relating a, b, and c that must be satisfied in order for &
 **to be an unbiased estimate of 2 ( t k )  [Ge174].** 
## b) Find values of a, b, and c so that & is the minimum-variance estimate.
 *Assume that h(z) is an odd function of z.*


## 13.9 Suppose for a scalar system that Pc = 1, R = 1, and H = 3. What is the
 **value of Pkf as given by Equation (5.19)? What will be the computed value of Pkf** 
## if H = 2 is used instead? What will be the computed value of Pk+ if H = 1 is
 used instead? This illustrates how the iterated Kalman filter gets a more accurate *estimate of P:* **by using a more accurate value for H k .**

13.10 
## Consider a system with the measurement equation Yk = xi f Wk. At time k
 
## the a priori state estimate is 3;'; = 1, the true state is z k  = 5, and the measurement
 
## is Yk = 25. The a priori estimation-error variance is P; = 1, and the measurement
 
# noise variance is R k  = 4. Use the iterated EKF algorithm to find 2z,l and 3;'12.
 
## Although the iterated EKF does not always improve the a posteriori state estimate,
 this problem illustrates how it usually does.


## 13.11 Prove Lemma 6 for scalar random variables z.


---


[Image on page 34]


**428**


# 13.12 Suppose you have the process equation x = x2 + w and the state estimate
 
## 2: = 0. What is the differential equation for propagating 2 to the next measure-
 ment time using the first-order EKF? What is the differential equation using the second-order EKF?


# 13.13 Consider the measurement equation yk = xi + 'uk, where V k  N (0, R).
 
## Suppose that Pi = 1, and &,
 = 1 is unbiased. **a) What is the expected value of 2: if the first-order EKF is used for the** **measurement update? Based on your expression for E(2:), how does the** **bias of the state estimate change with R? Does this make intuitive sense?** **b) What is the expected value of 2: if the second-order EKF is used for the** measurement update?

**13.14 Consider the system**

**zk+l** 
## = azk +wk,
 **wk** *(079)*


## Yk = z k  +vk,
 **wk** *(O,R)*

**with unknown parameter a. Suppose that an EKF is used to estimate the state**

**Zk and the parameter a. Further suppose that the artificial noise term used in the** **estimation of a is zero, and the EKF converges to the correct value of a with zero** variance. Show that the EKF in this situation is equivalent to the standard Kalman **filter for the scalar system when a is known.**

**Computer exercises**

**13.15 Write a program that implements the moving average filter and the ex-** 
## tended Kalman filter for the system described in Problem 13.3. Use R = 1, x = 1,
 
## Po+ = 1, and 20 = 2. Which filter appears to perform better?


**13.16 A planar model for a satellite orbiting around the earth can be modeled** **as**

*-a&* **e** **=** **-** **T**


## where T is the distance of the satellite from the center of the earth, 8 is the angular
 
## position of the satellite in its orbit, G = 6.6742 x 10-11m3/kg/s2 is the universal
 
## gravitational constant, M = 5.98 x loz4 kg is the mass of the earth, and w N
 **(0, low6) is random noise due to space debris, atmospheric drag, outgassing, and**


## Write a state-space model for this system with X I  = T ,  xz = +, x3 = 8,
 
## and 2 4  = 8..
 
## What must 9 be equal to in order for the orbit to have a constant radius
 when w = O? 
## Linearize the model around the point T = T O, I: = 0, 8 = woT, 8 = wo.
 What are the eigenvalues of the system matrix for the linearized system 
## when TO = 6.57 x lo6 m? What would you estimate to be the largest


---

**429**

integration step size that could be used to simulate the system? (Hint: recall that for a second-order transfer function with imaginary poles kja, the time constant is equal to l/a.) **d) Suppose that measurements of the satellite radius and angular position are** obtained every minute, with error standard deviations of 100 meters and 0.1 radians, respectively. Simulate the linearized Kalman filter for three 
## hours. Initialize the system with z(0) = [ TO 0 0 1.1~0
 1, 2(0) = 
## z(O), and P(0) = diag(0,0,0,0). Plot the radius estimation error as a
 function of time. Why is the performance so poor? How could you modify the linearized Kalman filter to get better performance?


## e )  Implement an extended Kalman filter and plot the radius estimation er-
 ror as a function of time. How does the performance compare with the linearized Kalman filter?

**13.17 Implement the hybrid EKF with a measurement period of 0.1s for the** system described in Example 13.1. Assume that the winding current measurement noises have a standard deviation of 0.1 amps. Create a table showing the experi- mental standard deviation of the motor velocity estimation error as a function of **the standard deviation of the control input uncertainties 41 and 42. Use control in-** 
## put standard deviations from 0 to 0.1 volts in steps of 0.01 (i.e., oq = 0, oq = 0.01,
 *. . ., gq = 0.1). In order to make a fair comparison, you should either run several* *simulations for each value of oq and average the results, or else initialize the ran-* dom seed in your software so that each simulation runs with the same random noise history.

**13.18 Derive the first-order EKF, second-order EKF, and iterated EKF (with** one iteration) for the scalar system

**z k + 1** 
## = z i + w k
 
## '& = 5: +'Uk


**where 'Wk and V k  are independent zero-mean white noise terms with variances 0.1** and 1, respectively. Simulate the first-order, second-order, and iterated extended Kalman filters for five time steps. Set the initial state to 1, the initial estimation- 
## error variance to 1, and the initial state estimate to 2. Compute the RMS error of
 the filter estimates. How does the performance of the filters compare? (Note that you need more than one simulation, in general, to obtain a fair comparison of filter performance. )

**13.19 Use the following procedure [Sor7lb] to approximate a uniform pdf that is** 
# defined on f l  with M Gaussian pdfs; that is, U(-1, 1) M CE1 azN(pr,
 **0:).**


## 0 Select the weighting coefficients so that a, = 1/M for all i.


## 0 Select the means of the Gaussian pdfs to be equally spaced on the range
 
# [-1,1] with p,+1 - p, = 2/(M + 1).


## 0 Select the variances cri of the Gaussian pdfs to all be the same and to minimize
 **the RMS difference between U(-1, 1) and xzl azN(pz,** **o,")** over the range [-I, 11. The above approach reduces the approximation problem to a onedimensional opti- mization problem, which can be solved in a number of different ways (for example,

---

**430**

using the golden search method [Pre92]). Plot the true pdf and the approximate 
## pdf for M = 3, 5, and 10, and compare the RMS errors.


**13.20 Suppose you have a scalar system given as**

**Xk+1** 
## = X k


## Yk = ZE +2’k


**where V k  is white Gaussian noise with a variance of 0.01. The pdf of the initial** **state xo is uniform between -1 and +1. Note from the measurement equation that** there is 4 **b)**

**13.21**

no way to distinguish between a positive state and a negative state. What will the extended Kalman filter estimate of the system be equal to? **The pdf of xo can be approximated with two Gaussian pdfs, each with a** **variance of 0.43, and with respective means of -1/3 and +1/3. Suppose** 
## that xo = -1/2. Plot the true state and the individual state estimates of
 a two-term Gaussian sum filter for 20 time steps. Plot the Gaussian pdfs at the final time for each estimate of the two-term Gaussian sum filter.

Consider the problem of tracking a moving vehicle in two dimensions (north is one dimension and east is the other dimension). The vehicle’s acceleration in the north and east directions consists of independent white noise. Two tracking sta- **tions, located at north-east coordinates (N1, El) and (N2, E2), respectively, mea-** sure the range to the vehicle. The system model can therefore be written as

**where nk and ek are the vehicle’s north and east coordinates at time step k, T** **is the time step of the system, wk is the zero-mean process noise, and vk is the** *zero-mean measurement noise. Suppose that the time step T = O.ls, the process* noise covariance Q = diag(0, 0,4,4), and the measurement noise covariance R = 
## diag(1,l). The tracking stations are located at ( N I ,  El) = (20,0), and (N2, E2) =
 
## (0,20). The initial state of the vehicle zo = [ 0 0 50 50 ]
 and is perfectly known. Design an extended Kalman filter to estimate the state of the vehicle. Run the simulation for 60 s. Plot the estimation error for the four states. What is the experimental standard deviation of the estimation error for each of the four states? Based on the steady-state covariance matrix of the filter, what is the theoretical standard deviation of the estimation error for each of the four states?

**13.22 Consider the system**

**T**


# where W k  - ( O , l ) ,  and $ = 0.9 is an unknown constant. Design an extended
 
## Kalman filter to estimate $. Simulate the filter for 100 time steps with zo = 1,


---


[Image on page 37]


**431**


## PO = I ,  20 = 0, and $0 = 0. Hand in your source code and a plot showing $ as a
 function of time.


## 13.23 Simulate Example 13.4 with artificial parameter noise variance values 0; =
 0, 1, and 100. How does a change in the artificial parameter noise variance affect *the filter’s estimate of -wi?*