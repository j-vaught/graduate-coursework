---
type: chapter
chapter: 8
title: The continuous-time Kalrnan filter
---
# Chapter 8 The Continuous-Time Kalman Filter

Our philosophy here will be to model phenomena with differential equations and then to form estimates of the physical quantities which also satisfy differential equations. 

--Richard Bucy [Buc68, Chapter 11 James Follin, A. G. Carlton, James Hanson, and Richard Bucy developed the continuous-time Kalman filter in unpublished work for the Johns Hopkins Ap plied Physics Lab in the late 1950s. Rudolph Kalman independently developed the discretetime Kalman filter in 1960. In April 1960 Kalman and Bucy became aware of each other's work and collaborated on the publication of the continuous-time Kalman filter in [Ka161]. This filter is sometimes referred to as the Kalman-Bucy filter. Further historical notes are given in Appendix A. 

The vast majority of Kalman filter applications are implemented in digital computers, so it may seem superfluous to discuss Kalman filtering for continuous-time measurements. However, there are still opportunities to implement Kalman filters in continuous time (i.e., in analog circuits) [Hug88]. Furthermore, the derivation of the continuous-time filter is instructive from a pedagogical point of view. Finally, steady-state continuous-time estimators can be analyzed using conventional frequency-domain concepts, which provides an advantage over discretetime estimc+ tors [Ba187, Ste941. In light of these factors, this chapter presents the continuoustime Kalman filter. 

Our derivation of the continuous-time filter starts with the previously developed discrete-time filter from Chapter 5, and then takes the limit as the time step decreases to zero. Section **8.1** shows the relationship between continuous-time white noise and discrete-time white noise, which is the foundation for the derivation of the continuous-time Kalman filter. Section 8.2 derives the Kalman filter for the case of continuous-time system dynamics and continuous-time measurements. Section **8.3** shows some creative methods to solve the continuous-time Riccati equation, which is a key component of the continuous-time Kalman filter. Section 8.4 discusses the continuous-time Kalman filter for the cases of correlated process and measurement noise, and for colored measurement noise. Section 8.5 discusses the steady-state continuous-time Kalman filter, its relationship to the Wiener filter of Section **3.4,** 
and its relationship to linear quadratic optimal control. 

## 8.1 **Discrete-Time And Continuous-Time White Noise**

In this section, we will show the relationship between discrete-time white noise and continuous-time white noise. We need to understand this relationship because in the next section we will derive the continuous-time Kalman filter as the limiting case of the discretetime Kalman filter as the sample time decreases to zero. First we will discuss the relationship between discrete-time and continuous-time process noise, and then we will discuss the relationship between discrete-time and continuous-time measurement noise. 

## 8.1.1 **Process Noise**

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{x_{k-1}+w_{k-1}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q)}}\\ {{x_{0}}}&{{=}}&{{0}}\end{array}$$

Consider the following discrete-time system with an identity state transition matrix and a sample time of T: where *{Wk}* is a discrete-time white noise process. Let us see what effect the white noise has on the covariance of the state. We can solve this discrete-time system for the state as follows: 
xk = WO + W1 + - .. + *Wk-1* (8.2) 
The covariance of the state is therefore given as 

$$x_{k}=w_{0}+w_{1}+\cdots+w_{k-1}$$
$$E[x_{k}x_{k}^{T}]=E[(w_{0}+w_{1}+\cdots+w_{k-1})(w_{0}+w_{1}+\cdots+w_{k-1})^{T}]$$ $$=E[w_{0}w_{0}^{T}]+E[w_{1}w_{1}^{T}]+\cdots+E[w_{k-1}w_{k-1}^{T}]$$ $$=kQ$$

The value of the continuous-time parameter t is equal to the number of discrete-time steps k times the sample time T. That is, t = *kT.* We therefore see that 

$$({\mathfrak{s}},\mathbf{1})$$

$$(8.2)$$
$$(8.3)$$
$$\begin{array}{r c l}{{E[x(t)x^{T}(t)]}}&{{=}}&{{E[x_{k}x_{k}^{T}]}}\\ {{}}&{{=}}&{{k Q}}\end{array}$$

$$(8.4)$$
$${\dot{x}}(t)=w(t)$$
$$(8.5)$$

The covariance of the state increases linearly with time for a given sample time T. 

Now consider the continuoustime system with an identity state transition matrix: 
i(t) = w(t) (8.5) 
where w(t) is continuous-time white noise. We propose (in hindsight) the following definition for continuous-time white noise: 

$$E[w(t)w^{T}(\tau)]=\frac{Q}{T}\delta(t-\tau)\tag{8.6}$$

where Q and T are the same as they are in the discretetime system of Equation (8.1). *6(t* - T) is the continuous-time impulse response; it is a function with a value of *0;)* at t = T, a value of 0 everywhere else, and an area of 1. Let us compute the covariance of *z(t)* in Equation (8.5): 

$$E[x(t)x^{T}(t)]=E\left[\int_{0}^{t}w(\alpha)\,d\alpha\int_{0}^{t}w^{T}(\beta)\,d\beta\right]\tag{8.7}$$ $$=\int_{0}^{t}\int_{0}^{t}E\left[w(\alpha)w^{T}(\beta)\right]\,d\alpha\,d\beta$$

Substituting Equation (8.6) into the above equation gives 

$$\begin{array}{r c l}{{E[x(t)x^{T}(t)]}}&{{=}}&{{\int_{0}^{t}\int_{0}^{t}\frac{Q}{T}\delta(\alpha-\beta)\,d\alpha\,d\beta}}\\ {{}}&{{=}}&{{\int_{0}^{t}\frac{Q}{T}\,d\beta}}\\ {{}}&{{=}}&{{\frac{Q t}{T}}}\end{array}$$
$$(8.8)$$
$$(8.9)$$
where we have used the sifting property of the continuous-time impulse function 
(see Problem 4.10). Recalling that t = *kT,* we can write the above equation as 
$$E[x(t)x^{T}(t)]=k Q$$

Comparing this with Equation (8.4), we see that the covariance of the state of the continuous-time system increases with time in exactly the same way as the covariance of 6he state of the discretetime system. In other words, discretetime white noise with covariance Q in a system with a sample period of T, is equivalent to continuous-time white noise with covariance *Qc6(t),* where Qc = *Q/T.* Zero-mean continuous-time white noise is denoted as 

$$(8.10)$$
$$w(t)\sim(0,Q_{\mathrm{c}})$$

4t) N *(0,Qc)* (8.10) 
which is equivalent to saying that 

$E[w(t)w^{T}(\tau)]=Q_{c}\delta(t-\tau)$ (8.11)
Continuous-time white noise is counterintuitive because w *(t)* is infinitely correlated with *W(T)* at t = T, but it has zero correlation with itself when t \# T. Nevertheless, it can be approximately descriptive of real processes. Also, continuous-time white noise is mathematically well defined and is a useful device that we will use in this chapter. Additional discussion about the relationship between discretetime and continuous-time white noise can be found in [Kai81, Smi781. 

## 8J.2 **Measurement Noise**

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{x_{k-1}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{v_{k}}}&{{\sim}}&{{(0,R)}}\end{array}$$

Now let us think about measurement noise. Suppose we have a discretetime measurement of a constant x every T seconds. The measurement times are tk = kT 
(k = 1,2,**.): 

$$(8.12)$$

From the Kalman filter equations in Section 5.1 we find that the a *posteriori* estimation-error covariance is given by 

$P_{k+1}^{+}=\frac{P_{k}^{+}R}{P_{k}^{+}+R}$ (8.13)
From this it can be shown that 

$$\begin{array}{r c l}{{P_{k}^{+}}}&{{=}}&{{\frac{P_{0}R}{k P_{0}+R}}}\\ {{\operatorname*{lim}_{P_{0}\to\infty}P_{k}^{+}}}&{{=}}&{{\frac{R}{k}}}\\ {{}}&{{=}}&{{\frac{R T}{t_{k}}}}\end{array}\tag{8}$$
$$(8.14)$$

The error covariance at time tk is independent of the sample time T if 

$$(8.15)$$
$$(8.16)$$

where Rc is some constant. This implies that 

$$={\frac{R_{\mathrm{e}}}{T}}$$
$${\boldsymbol{R}}$$
$$\operatorname*{lim}_{T\to0}R=R_{c}\delta(t)$$
$$\begin{array}{r c l}{{v_{k}}}&{{\sim}}&{{(0,R)}}\\ {{v(t)}}&{{\sim}}&{{(0,R_{\mathrm{c}})}}\end{array}$$
lim R = *R,6(t)* (8.16) *T-0* 
where *6(t)* is the continuous-time impulse function. This establishes the equivalence between white measurement noise in discrete time and continuous time. The effects of white measurement noise in discrete time and continuous time are the same if 

$$(8.17)$$
$$(8.18)$$

Equation (8.15) specifies the relationship between R and *Rc,* and the second equation above is a shorthand way of saying 

$$E[v(t)v(\tau)]=R_{c}\delta(t-\tau)$$
E[w(~)w(T)] = *Rc6(t* - T) (8.18) 

## Discretized Simulation Of Noisy Continuous-Time Systems 8.1.3

The results of the above sections can be combined with the results of Section 1.4 to obtain a discretized simulation of a noisy continuous-time system for the purpose of implementing a discrete-time state estimator. Suppose that we have a system given as

$${\dot{x}}$$
$$y\,$$
$$\begin{array}{l}{w}\\ {v}\end{array}$$
$$\begin{array}{l l}{{=}}&{{A x+B u+w}}\\ {{=}}&{{C x+v}}\\ {{\sim}}&{{(0,Q_{\rm e})}}\\ {{\sim}}&{{(0,R_{\rm e})}}\end{array}\tag{8.19}$$

Both w(t) and v(t) are continuous-time noise, and u(t) is a known input. This system is approximately equivalent to the following discrete-time system:

$$x_{k}$$
$$\begin{array}{c}{{y_{k}}}\\ {{w_{k}}}\\ {{v_{k}}}\end{array}$$
$$\begin{array}{r l}{{=}}&{{e^{A\Delta t}x_{k-1}+e^{A\Delta t}\int_{0}^{\Delta t}e^{-A\tau}\,d\tau\,B u_{k-1}+w_{k}}}\\ {{=}}&{{e^{A\Delta t}x_{k-1}+e^{A\Delta t}\left[I-e^{-A\Delta t}\right]A^{-1}B u_{k-1}+w_{k}}}\\ {{=}}&{{C x_{k}+v_{k}}}\\ {{\sim}}&{{(0,Q_{c}\Delta t)}}\\ {{\sim}}&{{(0,R_{c}/\Delta t)}}\end{array}$$
$$(8.20)$$

where At is the discretization step size. The second expression for xk above is valid if A-1 exists. If we use these discretized equations to simulate a continuous-time system, then we can simulate a continuous-time state estimator using the resulting measurements with one of the integration methods discussed in Section 1.5. The remainder of this chapter discusses continuous-time state estimation.

## Derivation Of The Continuous-Time Kalman Filter 8.2

We will now use the results of the previous section to derive the continuous-time Kalman filter. Suppose that we have a continuous-time system given as

$$\begin{array}{r l}{{\dot{x}}}&{{}=}\\ {y}&{{}=}\end{array}$$
$$\begin{array}{r l}{w}&{{}\sim}\\ {v}&{{}\sim}\end{array}$$
$Ax+Bu+w$  $Cx+v$  $(0,Q_{e})$  $(0,R_{e})$
$$(8.21)$$

When we write w ~ (0, Qc) we mean exactly what is written in Equation (8.11).

When we write v ~ (0, Rc) we mean exactly what is written in Equation (8.18). Now suppose that we discretize this system with a sample time of T (see Section 1.4).

We obtain

$$\begin{array}{l l l}{{x_{k}}}&{{=}}&{{F x_{k-1}+G u_{k-1}+\Lambda w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H x_{k}+v_{k}}}\end{array}$$
$$(8.22)$$

The matrices in this discrete-time system are computed as follows:

$$F=\exp(AT)$$ $$\approx(I+AT)\ \mbox{for small}\ T$$ $$G=(\exp(AT)-I)A^{-1}B$$ $$\approx BT\ \mbox{for small}\ T$$ $$\Lambda=(\exp(AT)-I)A^{-1}$$ $$\approx IT\ \mbox{for small}\ T$$ $$H=C$$ $$w_{k}\sim(0,Q),\ \ \ Q=Q_{e}T$$ $$v_{k}\sim N(0,R),\ \ \ R=R_{e}/T\tag{8.23}$$  The discrete-time Kalman filter again for this system was derived in Section 5.1 as  $$K_{k}=P_{k}^{-}H^{T}(HP_{k}^{-}H^{T}+R)^{-1}\tag{8.24}$$  From this second-order
$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{P_{k}^{-}C^{T}(C P_{k}^{-}C^{T}+R_{c}/T)^{-1}}}\\ {{}}&{{}}&{{}}\\ {{\frac{K_{k}}{T}}}&{{=}}&{{P_{k}^{-}C^{T}(C P_{k}^{-}C^{T}T+R_{c})^{-1}}}\\ {{}}&{{}}&{{}}\\ {{\operatorname*{lim}_{T\to0}\frac{K_{k}}{T}}}&{{=}}&{{P_{k}^{-}C^{T}R_{c}^{-1}}}\end{array}$$

From this we can derive 

$$(8.23)$$
$$(8.25)$$

The estimation-error covariances were derived in Section 5.1 as 

$$(8.26)$$
$$(8.27)$$
$$(8.28)$$

For small values of T, this can be written as 

$$\begin{array}{r c l}{{P_{k}^{+}}}&{{=}}&{{(I-K_{k}H)P_{k}^{-}}}\\ {{P_{k+1}^{-}}}&{{=}}&{{F P_{k}^{+}F^{T}+Q}}\end{array}$$
$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{P_{k+1}^{-}}}&{{=}}&{{(I+A T)P_{k}^{+}(I+A T)^{T}+Q_{c}T}}\\ {{}}&{{=}}&{{P_{k}^{+}+(A P_{k}^{+}+P_{k}^{+}A^{T}+Q_{c})T+A P_{k}^{+}A^{T}T^{2}}}\end{array}$$  for $P_{k}^{+}$ gives
Substituting for Pk+ gives 

$$\begin{array}{l}{{(I-K_{k}C)P_{k}^{-}+A P_{k}^{+}A^{T}T^{2}+}}\\ {{[A(I-K_{k}C)P_{k}^{-}+(I-K_{k}C)P_{k}^{-}A^{T}+Q_{c}]T}}\end{array}$$  with sides and then dividing by $T$ gives 
$$P_{k+1}^{-}\quad=$$
$$\frac{P_{k+1}^{-}-P_{k}^{-}}{T}=\frac{-K_{k}CP_{k}^{-}}{T}+AP_{k}^{+}A^{T}T+\tag{8.29}$$ $$(AP_{k}^{-}+AK_{k}CP_{k}^{-}+P_{k}^{-}A^{T}-K_{k}CP_{k}^{-}A^{T}+Q_{c})$$  the limit as $T\to0$ and using Equation (8.25) gives
Subtracting PL from both sides and then dividing by T gives Taking the limit as T + 0 and using Equation **(8.25)** gives 

$$\dot{P}=\lim_{T\to0}\frac{P_{k+1}^{-}-P_{k}^{-}}{T}\tag{8.30}$$ $$=-PC^{T}R_{c}^{-1}CP+AP+PA^{T}+Q_{c}$$
$$(\mathbf{8.31})$$

This equation for P is called a differential Riccati equation and can be used to compute the estimation-error covariance for the continuous-time Kalman filter. This requires n2 integrations because P is an n x n matrix. But P is symmetric, so in practice we only need to integrate *n(n* + **1)/2** equations in order to solve for P. 

In Section **5.1** we derived the Kalman filter equations for 2 as 

$$\begin{array}{r c l}{{\hat{x}_{k}^{-}}}&{{=}}&{{F\hat{x}_{k-1}^{+}+G u_{k-1}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k}(y_{k}-H\hat{x}_{k}^{-})}}\end{array}$$

If we assume that T is small we can use Equation **(8.23)** to write the measurement update equation as 

$$\begin{array}{r c l}{{\hat{x}_{k}^{+}}}&{{=}}&{{F\hat{x}_{k-1}^{+}+G u_{k-1}+K_{k}(y_{k}-H F\hat{x}_{k-1}^{+}-H G u_{k-1})}}\\ {{}}&{{\approx}}&{{(I+A T)\hat{x}_{k-1}^{+}+B T u_{k-1}+}}\\ {{}}&{{}}&{{K_{k}(y_{k}-C(I+A T)\hat{x}_{k-1}^{+}-C B T u_{k-1})}}\end{array}$$

Now substitute for Kk from Equation **(8.25)** to obtain 

$$\begin{array}{r c l}{{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k-1}^{+}+A T\hat{x}_{k-1}^{+}+B T u_{k-1}+}}\\ {{}}&{{}}&{{P C^{T}R_{c}^{-1}T(y_{k}-C\hat{x}_{k-1}^{+}-C A T\hat{x}_{k-1}^{+}-C B T u_{k-1})}}\end{array}$$

Subtracting zkf-l from both sides, dividing by T, and taking the limit as T + 0, gives 

$$\operatorname*{lim}_{T\to0}{\frac{\hat{x}_{k}^{+}-\hat{x}_{k-1}^{+}}{T}}$$ $$A\hat{x}+B u+P C^{T}R_{c}^{-1}(y-C\hat{x})$$
$\dot{\hat{x}}\;\;=\;\;0$  = . 
T 2 = lim 
$$(8.32)$$
$$(8.33)$$
$$(8.34)$$

This can be written as 

$$\begin{array}{r l}{={}}&{{}A{\hat{x}}+B u+K(y-C{\hat{x}})}\\ {={}}&{{}P C^{T}R_{c}^{-1}}\end{array}$$
$${\dot{\hat{x}}}$$ $$K$$
$$(8.35)$$

This gives the differential equation that can be used to integrate the state estimate in the continuous-time Kalman filter. 

## The Continuous-Time Kalman Filter

The continuous-time Kalman filter can be summarized as follows. 

1. The continuous-time system dynamics and measurement equations are given as 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+B u+w}}\\ {{y}}&{{=}}&{{C x+v}}\\ {{w}}&{{\sim}}&{{(0,Q_{c})}}\\ {{v}}&{{\sim}}&{{(0,R_{c})}}\end{array}$$

$$(8.36)$$

Note that w(t) and *w(t)* are continuous-time white noise processes. 

2. The continuous-time Kalman filter equations are given as 

$$\hat{x}(0)=E[x(0)]$$ $$P(0)=E[(x(0)-\hat{x}(0))(x(0)-\hat{x}(0))^{T}]$$ $$K=PCT^{T}R_{c}^{-1}$$ $$\hat{x}=A\hat{x}+Bu+K(y-C\hat{x})$$ $$\hat{P}=-PC^{T}R_{c}^{-1}CP+AP+PA^{T}+Q_{c}\tag{8.37}$$

Other methods of deriving the continuous-time Kalman filter also exist. For example, George Johnson presented a derivation that is based on finding the gain that minimizes the derivative of the estimation covariance [Joh69]. 

In this example we will use the continuous-time Kalman filter to estimate a constant given continuous-time noisy measurements: 

$$(8.38)$$
$$(8.39)$$

We see that A = 0, Q = 0, and C = 1. Equation (8.37) gives the differential equation for the covariance as 

$${\dot{x}}\quad=$$
$$\begin{array}{l}{{0}}\\ {{x+v}}\\ {{(0,R)}}\end{array}$$
$$\begin{array}{r l}{y}&{{}=}\\ {v}&{{}\sim}\end{array}$$
$$\begin{array}{r c l}{{\dot{P}}}&{{=}}&{{-P C^{T}R^{-1}C P+A P+P A^{T}+Q}}\\ {{}}&{{=}}&{{-P^{2}/R}}\end{array}$$

with the initial condition P(0) = *PO.* From this we can derive 

$$\begin{array}{r c l}{{\frac{d P}{P^{2}}}}&{{=}}&{{\frac{-d\tau}{R}}}\\ {{\int_{P(0)}^{P(t)}\frac{1}{P^{2}}\,d P}}&{{=}}&{{-\int_{0}^{t}\frac{1}{R}\,d\tau}}\\ {{-(P^{-1}-P_{0}^{-1})}}&{{=}}&{{-t/R}}\\ {{P^{-1}}}&{{=}}&{{P_{0}^{-1}+t/R}}\\ {{P}}&{{=}}&{{(P_{0}^{-1}+t/R)^{-1}}}\\ {{}}&{{=}}&{{\frac{P_{0}}{1+P_{0}t/R}}}\\ {{\operatorname*{lim}_{t\rightarrow\infty}P}}&{{=}}&{{0}}\end{array}$$

$$\begin{array}{r c l}{{K}}&{{=}}&{{P C^{T}R^{-1}}}\\ {{}}&{{}}&{{=}}&{{\frac{P_{0}/R}{1+P_{0}t/R}}}\\ {{\operatorname*{lim}_{t\rightarrow\infty}K}}&{{=}}&{{0}}\end{array}$$

Equation (8.37) gives the Kalman gain as 

$$(8.40)$$
$$(8.41)$$
$${\dot{\hat{x}}}=A{\hat{x}}+B u+K(y-C{\hat{x}})$$
$$(8.42)$$
$$(8.43)$$
Equation **(8.37)** gives the state-update equation as 
d = A$ + B~ + ~(y - *c?)* **(8.42)** 
from which we can derive 
$$\begin{array}{r c l}{{\dot{\hat{x}}}}&{{=}}&{{K(y-\hat{x})}}\\ {{\operatorname*{lim}_{t\to\infty}\dot{\hat{x}}}}&{{=}}&{{0}}\end{array}$$

This shows that as time goes to infinity, 2 reaches a steady-state value. This is intuitive because as we obtain an infinite number of measurements of a constant, our estimate of that constant becomes perfect and additional measurements cannot improve our estimate. Furthermore, the Kalman gain goes to zero as time goes to infinity, which again says that we ignore additional measurements (since our estimate becomes perfect). Finally, the covariance P goes to zero as time goes to infinity, which says that the uncertainty in our estimate goes to zero, meaning that our estimate is perfect. Compare this example with the equivalent discrete-time system discussed in Example **7.10.** 
vvv 

In this example we are able to obtain measurements of the velocity of an object that is moving in one dimension. The object is subject to random accelerations. We want to estimate the velocity x from noisy velocity measurements. The system and measurement equations are given as 

$${\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{w}}\end{array}}$$
$$\begin{array}{r c l}{{-}}&{{}}&{{-}}\\ {{y}}&{{=}}&{{x+v}}\\ {{w}}&{{\sim}}&{{(0,Q)}}\\ {{v}}&{{\sim}}&{{(0,R)}}\end{array}$$
We see that A = 0 and C = 1. From the covariance update of Equation **(8.37)** 
we obtain 
with the initial condition P(0) = *Po.* From this we can derive 
$$\begin{array}{r c l}{{\dot{P}}}&{{=}}&{{-P C^{T}R^{-1}C P+A P+P A^{T}+Q}}\\ {{}}&{{=}}&{{-P^{2}/R+Q}}\end{array}$$
$$(8.44)$$
$$(8.45)$$
$$\int_{P(0)}^{P(t)}\frac{dP}{Q-P^{2}/R}=\int_{0}^{t}d\tau$$ $$\frac{1}{2\sqrt{Q}}\ln\left(\frac{\sqrt{Q}+P/\sqrt{R}}{\sqrt{Q}-P/\sqrt{R}}\right)\Biggr{|}_{P(0)}^{P(t)}=t$$
$$(8.46)$$
$$(8.47)$$
It this for $P$ gives $$\begin{array}{r c l}{{P}}&{{=}}&{{\sqrt{Q R}\left[\frac{P_{0}-\sqrt{Q R}+(\sqrt{Q R}+P_{0})\exp(2t\sqrt{Q})}{\sqrt{Q R}-P_{0}+(\sqrt{Q R}+P_{0})\exp(2t\sqrt{Q})}\right]}}\\ {{}}&{{}}&{{\operatorname*{lim}_{t\to\infty}P}}&{{=}}&{{\sqrt{Q R}}}\end{array}$$

Solving this for P gives 

The Kalman gain is obtained from Equation **(8.37)** as 
K = PCTR-'  = P/R  lim K = 

$$(8.48)$$
t+w **(8.48)** 
The state estimate update expression is obtained from Equation **(8.37)** as 
* [10] M. C. Gonzalez-Garcia, M. C. Gonzalez-Garcia, M.  
$$\dot{\hat{x}}$$
$$(8.49)$$
From these expressions we see that if process noise increases (i.e., Q increases) 
then K increases. This is intuitively agreeable, because from the 4 equation we see that K defines the rate at which we change 3 based on the measurements. If Q is large then we have less confidence in our system model, and relatively more confidence in our measurements, so we change f more aggressively to be consistent with our measurements. 

Similarly, we see that if we have large measurement noise (i.e., R is large) 
then K decreases. This is again intuitively agreeable. Large measurement noise means that we have less confidence in our measurements, so we change f less aggressively to be consistent with our measurements. 

Finally, we see that P increases as both Q and R increase. An increase in the noise in either the system model or the measurements will degrade our confidence in our state estimate. 

vvv 

## 8.3 **Alternate Solutions To The Rlccatl Equation**

The differential Riccati equation of Equation **(8.37)** can be computationally expensive to integrate, especially for systems with small time constants. Also, direct integration of the Riccati equation may result in a P matrix that loses its positive definiteness due to numerical problems. In this section we will look at some alternate solutions to the differential Riccati equation. This first two methods, called the transition matrix approach and the Chandrasekhar algorithm, are both intended to reduce computational effort. The third method, called square root filtering, is intended to reduce numerical difficulties. 

## 8.3.1 The Transition Matrix Approach

Assume that P = *AY-l,* where A and Y are n x n matrices to be determined. In 
the following we will determine what equalities must be satisfied by A and Y in 
order for this factorization to be valid. If the factorization is valid then 
  **A so we want a the determination to find that**  $$\dot{P}=\dot{\Lambda}Y^{-1}+\Lambda\frac{d}{dt}(Y^{-1})$$ $$=\dot{\Lambda}Y^{-1}-\Lambda Y^{-1}\dot{Y}Y^{-1}\tag{1}$$
$$(8.50)$$
$$\dot{P}Y=\dot{\Lambda}-\Lambda Y^{-1}\dot{Y}$$
$$(8.51)$$
where we have used Equation (1.51) for the time derivative of *Y-l.* We postmultiply both sides of the above equation by Y to obtain 
py = A - *Ay-ly* (8.51) 
$$(8.52)$$
$$(8.53)$$
$$(8.54)$$
$$(8.55)$$
Recall from Equation (8.37) that the differential equation for P is given by 

$${\dot{P}}=A P+P A^{T}-P C^{T}R^{-1}C P+Q$$
P = AP + PAT - *PCTR-lCP* + Q (8.52) 
Substitute AY-l *for* P in this equation to obtain 

$$\dot{P}=A\Lambda Y^{-1}+\Lambda Y^{-1}A^{T}-\Lambda Y^{-1}C^{T}R^{-1}C\Lambda Y^{-1}+Q$$

Post-multiply both sides of this equation by Y to obtain 

$$\dot{P}Y=A\Lambda+\Lambda Y^{-1}A^{T}Y-\Lambda Y^{-1}C^{T}R^{-1}C\Lambda+Q Y$$
PY = Ah + AY-lATY - *AY-lCTR-lCA* + QY (8.54) 
Now we can equate the right sides of Equations (8.51) and (8.54) to obtain 

$$\begin{array}{r c l}{{\dot{\Lambda}-\Lambda Y^{-1}\dot{Y}}}&{{=}}&{{A\Lambda+\Lambda Y^{-1}A^{T}Y-\Lambda Y^{-1}C^{T}R^{-1}C\Lambda+Q Y}}\\ {{}}&{{}}&{{\dot{\Lambda}}}&{{=}}&{{A\Lambda+Q Y+\Lambda Y^{-1}(\dot{Y}+A^{T}Y-C^{T}R^{-1}C\Lambda)}}\end{array}$$

This equation came from our original factorization of P, and if this equation reduces to 0 = 0 then we know that the original factorization was valid. So if Y = CTR-ICA - *ATY,* and A = AA + *QY,* then our assumed factorization will be valid. These differential equations for Y and A can be combined as 

$$\left[\begin{array}{c}\dot{\Lambda}\\ \dot{Y}\end{array}\right]=\left[\begin{array}{cc}A&Q\\ C^{T}R^{-1}C&-A^{T}\end{array}\right]\left[\begin{array}{c}\Lambda\\ Y\end{array}\right]\tag{8.56}$$ $$=J\left[\begin{array}{c}\Lambda\\ Y\end{array}\right]$$

where J is defined by the above equation. The initial conditions on A and Y can be chosen to be consistent with the initial condition on P as follows: 

$$\begin{array}{r c l}{\Lambda(0)}&{=}&{P(0)}\\ {Y(0)}&{=}&{I}\end{array}$$

Now suppose that A, Q, C, and R are constant (that is, we have an LTI system with constant process and measurement noise covariances). In this case J is constant and Equation (8.56) can be solved as 

$${\left[\begin{array}{l}{\Lambda(t+T)}\\ {Y(t+T)}\end{array}\right]}=\exp(J T)\left[\begin{array}{l}{\Lambda(t)}\\ {Y(t)}\end{array}\right]$$
This can be written as 
$$8.56)$$
$$(8.57)$$
$$(8.58)$$
$$(8.59)$$
$$(8.60)$$
$$\left[\begin{array}{l}{{\Lambda(t+T)}}\\ {{Y(t+T)}}\end{array}\right]=\left[\begin{array}{l l}{{\phi_{11}(T)}}&{{\phi_{12}(T)}}\\ {{\phi_{21}(T)}}&{{\phi_{22}(T)}}\end{array}\right]\left[\begin{array}{l}{{\Lambda(t)}}\\ {{Y(t)}}\end{array}\right]$$
$$\left[\begin{array}{c c}{{\phi_{11}(T)}}&{{\phi_{12}(T)}}\\ {{\phi_{21}(T)}}&{{\phi_{22}(T)}}\end{array}\right]\left[\begin{array}{c c}{{P(t)Y(t)}}\\ {{Y(t)}}\end{array}\right]$$  at equations:
$\left[\begin{array}{c}\Lambda(t+T)\\ Y(t+T)\end{array}\right]=$  It's true, e.g. 
where the *q5iJ* matrices are defined as the four n x n submatrices in exp(JT). From our original factorization assumption we have A = *PY, so* this equation can be 

$$\begin{array}{l}{{\phi_{11}(T)P(t)Y(t)+\phi_{12}(T)Y(t)}}\\ {{\phi_{21}(T)P(t)Y(t)+\phi_{22}(T)Y(t)}}\end{array}$$
$$\begin{array}{r l}{\Lambda(t+T)}&{{}=}\\ {Y(t+T)}&{{}=}\end{array}$$

This can be written as two separate equations: 

$$(8.61)$$

Since h(t + T) = P(t + T)Y(t + *T),* we can write the first equation as 

$$Y(t+T),\,\cdot$$
$$P(t+T)Y(t+T)=\phi_{11}(T)P(t)Y(t)+\phi_{12}(T)Y(t)$$
$$(8.62)$$

Substituting for *Y(t* + T) from Equation *(8.61)* in the above equation gives 

$$P(t+T)\left[\phi_{21}(T)P(t)Y(t)+\phi_{22}(T)Y(t)\right]=\phi_{11}(T)P(t)Y(t)+\phi_{12}(T)Y(t)\tag{8.63}$$ $$P(t+T)\left[\phi_{21}(T)P(t)+\phi_{22}(T)\right]=\phi_{11}(T)P(t)+\phi_{12}(T)$$

This equation is finally solved for *P(t* + T) as 

$$T)]\left[\phi_{21}(T)P(t)+\phi_{22}(T)\right]^{-1}$$
$$P(t+T)=\left[\phi_{11}(T)P(t)+\phi_{12}(T)\right]\left[\phi_{21}(T)P(t)+\phi_{22}(T)\right]^{-1}$$

This may be a faster way to solve for P instead of integrating the Riccati equation. 

Note that we do not have to worry about the integration step size with this method. 

This method can be used to propagate from P(t) to *P(t* + T) in a single equation, for any values t and T. 

## M Example^.^

Suppose that we want to estimate a gyroscope drift rate E (assumed to be constant) given measurements of the gyro angle 8. The system and measurement model can be written as 

$$\begin{array}{r c l}{{\dot{\theta}}}&{{=}}&{{\epsilon}}\\ {{y}}&{{=}}&{{\theta+v}}\\ {{\left[\begin{array}{l}{{\dot{\theta}}}\\ {{\dot{\epsilon}}}\end{array}\right]}}&{{=}}&{{\left[\begin{array}{l l}{{0}}&{{1}}\\ {{0}}&{{0}}\end{array}\right]\left[\begin{array}{l}{{\theta}}\\ {{\epsilon}}\end{array}\right]}}\\ {{y}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{0}}\end{array}\right]\left[\begin{array}{l}{{\theta}}\\ {{\epsilon}}\end{array}\right]+v}}\\ {{v}}&{{\sim}}&{{(0,R)}}\end{array}$$
$$(8.64)$$
$$(8.65)$$
$$(8.67)$$

Direct **use** of the differential Riccati equation from Equation *(8.37)* gives 

$$\begin{array}{l}\dot{P}=AP+PA^{T}-PC^{T}R^{-1}CP+Q\\ \dot{P}_{11}\ \ \dot{P}_{12}\ \ \ \ =\ \ \left[\begin{array}{cc}2P_{12}-P_{11}^{2}/R&P_{22}-P_{11}P_{12}/R\\ P_{22}-P_{11}P_{12}/R&-P_{12}^{2}/R\end{array}\right]\end{array}\tag{8.66}$$

We can solve for P by performing three numerical integrations (recall that P is symmetric). However, it would be difficult to find a closed-form solution for P(t) from these coupled differential equations. A transition matrix approach to this problem would proceed as follows, assuming that *P(0)* is diagonal. We suppose that P is factored as P = *AY-l,* where A and Y *are* 2 x 2 matrices. 

The initial conditions on *A(t)* and *Y(t)* can be chosen as 

$$\begin{array}{r c l}{{\Lambda(0)}}&{{=}}&{{P(0)}}\\ {{}}&{{=}}&{{\left[\begin{array}{c c}{{P_{11}(0)}}&{{0}}\\ {{0}}&{{P_{22}(0)}}\end{array}\right]}}\\ {{Y(0)}}&{{=}}&{{I}}\end{array}$$
Y(0) = I (8.67) 
The differential equation for A(t) and *Y(t)* is given as 

$$\left[\begin{array}{l}{{\dot{\Lambda}}}\\ {{\dot{Y}}}\end{array}\right]=J\left[\begin{array}{l}{{\Lambda}}\\ {{Y}}\end{array}\right]$$
$\bigstar|$. 
$$(8.68)$$

where the matrix J is computed as 

$$J=\left[\begin{array}{ccc}A&Q\\ C^{T}R^{-1}C&-A^{T}\end{array}\right]\tag{8.69}$$ $$=\left[\begin{array}{cccc}0&1&0&0\\ 0&0&0&0\\ 1/R&0&0&0\\ 0&0&-1&0\end{array}\right]$$

The transition matrix for the differential equation for A and Y is computed as 

$$\exp(Jt)=\left[\begin{array}{cccc}1&t&0&0\\ 0&1&0&0\\ t/R&t^{2}/2R&1&0\\ -t^{2}/2R&-t^{3}/6R&-t&1\end{array}\right]\tag{1}$$ $$=\left[\begin{array}{cc}\phi_{11}(t)&\phi_{12}(t)\\ \phi_{21}(t)&\phi_{22}(t)\end{array}\right]$$
$$(8.70)$$
$$\mathbf{\Sigma}_{1}^{(8.71)}$$
$$(8.72)$$

where the *+ij(t)* terms are 2 x 2 matrix partitions. The Riccati equation solution is obtained from Equation *(8.64)* as 

$$\begin{array}{r l}{P(t)=[\phi_{11}(t)P(0)+\phi_{12}(t)][\phi_{21}(t)P(0)+\phi_{22}(t)]^{-1}}&{{}}\\ {={}}&{{}{\left[\begin{array}{l l}{P_{11}(0)}&{t P_{22}(0)}\\ {0}&{P_{22}(0)}\end{array}\right]{\frac{1}{\Delta}}{\left[\begin{array}{l l}{12R^{2}-2t^{3}P_{22}(0)}&{-6R t^{2}P_{22}(0)}\\ {12R^{2}t+6t^{2}P_{11}(0)}&{12R^{2}+12t P_{11}(0)}\end{array}\right]}}\end{array}$$

where A is given as 

$$\Delta=12R^{2}+P_{11}(0)P_{22}(0)t^{4}+12P_{11}(0)t R+4P_{22}(0)t^{3}R$$

Carrying out the multiplication and some algebra gives the Riccati equation solution as 

$$=\left[\begin{array}{cc}P_{11}(t)&P_{12}(t)\\ P_{12}(t)&P_{22}(t)\end{array}\right]\tag{8.73}$$ $$=\frac{1}{\Delta}4R\left[P_{11}(0)P_{22}(0)t^{3}+3P_{11}(0)R+3t^{2}P_{22}(0)R\right]$$ $$=\frac{1}{\Delta}6RP_{22}(0)t\left[P_{11}(0)t+2R\right]$$ $$=\frac{1}{\Delta}12RP_{22}(0)\left[P_{11}(0)t+R\right]$$
$${P}{\left({t}\right)}$$ $${P}_{{{11}}}{\left({t}\right)}$$ $${P}_{{{12}}}{\left({t}\right)}$$ $${P}_{{{22}}}{\left({t}\right)}$$

With the transition matrix approach we have obtained a closed-form solution for *P(t),* something that was not possible with a direct approach to the Riccati equation. In the special case that our initial uncertainty is infinite, we can further simplify *P(t)* as 

$$\lim_{P(0)\to\infty}\Delta=P_{11}(0)P_{22}(0)t^{4}$$ $$\lim_{P(0)\to\infty}P(t)=\left[\begin{array}{cc}4R/t&6R/t^{2}\\ 6R/t^{2}&12R/t^{3}\end{array}\right]$$ $$\lim_{t\to\infty}\left[\lim_{P(0)\to\infty}P(t)\right]=\left[\begin{array}{cc}0&0\\ 0&0\end{array}\right]\tag{8}$$
$$(8.74)$$

That is, our uncertainty goes to zero as time goes to infinity. This occurs because the process noise is zero (i.e., we are estimating a constant). Since K = *PCTR-l,* we see that the Kalman gain also goes to zero as time goes to infinity. This simply means that eventually we get so many measurements that our knowledge is complete. Additional measurements cannot give us any new information, so we ignore additional measurements. 

vvv 

## 8.3.2 The Chandrasekhar Algorithm

Recall the differential Riccati equation for the continuous-time Kalman filter from Equation (8.37): 
$${\dot{P}}=A P+P A^{T}-P C^{T}R^{-1}C P+Q$$
If P were not symmetric then the numerical computation of P would require n2 integrations. However, since P = PT the computation of P requires only n(n+1)/2 
integrations. This can still be computationally taxing, especially for problems with small time constants. The Chandrasekhar algorithm gives computational savings 
in some circumstances. The algorithm is based on the work of the Nobel prize 
winning astrophysicist Subramanan Chandrasekhar, who used similar algorithms to 
solve computationally difficult astrophysics problems in the 1940s [Cha47, Cha481. Chandrasekhar's algorithms were applied to Kalman filtering in [Kai73, KaiOO]. 
The Chandrasekhar algorithm applies only when A, C, R, *and* Q are constant. 

8.3.2.1 The Chandrasekhar algorithm derivation Consider the continuoustime differential equation for the state estimate, assuming that the original system is timeinvariant and the Kalman gain K is a constant: 

$$(8.75)$$
$$(8.76)$$
$$(8.77)$$

The measurement y is the output of the system, but it is the input to the filter. 

Consider the zero-input Kalman filter (i.e., y = 0). 

$$\begin{array}{r l}{={}}&{{}A{\hat{x}}+K(y-C{\hat{x}})}\\ {={}}&{{}(A-K C){\hat{x}}+K y}\end{array}$$
$$\dot{\hat{\mathbf{z}}}$$
$${\dot{\hat{x}}}=(A-K C){\hat{x}}$$
$$\begin{array}{r c l}{{\hat{x}(t)}}&{{=}}&{{\exp[(A-K C)t]\hat{x}(0)}}\\ {{}}&{{=}}&{{\phi(t)\hat{x}(0)}}\end{array}$$
$ = (A - *KC)?* (8.77) 
This equation has the solution 

$$(8.78)$$
$$\begin{array}{r c l}{{\dot{\phi}}}&{{=}}&{{(A-K C)\phi}}\\ {{\phi(0)}}&{{=}}&{{I}}\end{array}$$

where *4J(t)* is the state transition matrix of the filter and is defined by the above equation. From the definition of **4J(t)** as a state transition matrix we **know** that 

$$(8.79)$$
$$(8.80)$$
$$(8.81)$$

We can differentiate both sides of Equation (8.75) to obtain 

$$\begin{array}{r l}{={}}&{{}A{\dot{P}}+{\dot{P}}A^{T}-{\dot{P}}C^{T}R^{-1}C P-P C^{T}R^{-1}C{\dot{P}}}\\ {={}}&{{}A{\dot{P}}+{\dot{P}}A^{T}-{\dot{P}}C^{T}K^{T}-K C{\dot{P}}}\\ {={}}&{{}(A-K C){\dot{P}}+{\dot{P}}(A-K C)^{T}}\end{array}$$
$\overset{\text{ra}}{\mathcal{P}}$. 
Now note that for a general timevarying matrix Y(t), if Y = AY + *YAT,* where A is a constant matrix, then *Y(t)* = exp(At)Y(0)exp(ATt) (see Problem 8.2). 

Therefore, we can solve the above equation for P as 

$${\dot{P}}=\phi{\dot{P}}(0)\phi^{T}$$
$$({\bf8.82})$$
P = **4JP(0)4JT** (8.81) 
where P(0) is obtained from Equation (8.75) as 

$${\dot{P}}(0)=A P(0)+P(0)A^{T}-P(0)C^{T}R^{-1}C P(0)+Q$$

The symmetric matrix *P(0)* can be factored as follows (see Section 8.3.2.2): 

$$\dot{P}(0)=M_{1}M_{1}^{T}-M_{2}M_{2}^{T}\qquad\qquad,$$
$$\begin{array}{r l}{{\dot{P}}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
P(0) = MiM,T - *M2M:* (8.83) 
P(0) is an n x n matrix. The rank of P(0) is *a 5* n. Since *p(0)* is symmetric, all of its eigenvalues are real. The number of positive eigenvalues of *P(0)* is P, and the number of negative eigenvalues is (a - *P).* Matrix MI is an n x ,6 matrix, and Mz is an n x (a - p) matrix. From the previous three equations we can write P = **4JP(0)4JT** 

$\phi\dot{P}(0)\phi^{T}$  $\phi(M_{1}M_{1}^{T}-M_{2}M_{2}^{T})\phi^{T}$  $\phi M_{1}M_{1}^{T}\phi^{T}-\phi M_{2}M_{2}^{T}\phi^{T}$ (8.84)
Now define the matrices Y1 *and* YZ as 

$$(8.83)$$

$$(8.85)$$
$$(8.86)$$

Then the P equation can be written as 

$$\begin{array}{r c l}{{Y_{1}}}&{{=}}&{{\phi M_{1}}}\\ {{Y_{2}}}&{{=}}&{{\phi M_{2}}}\end{array}$$
$$\dot{P}=Y_{1}Y_{1}^{T}-Y_{2}Y_{2}^{T}$$
$$\begin{array}{r c l}{{Y_{1}(0)}}&{{=}}&{{\phi(0)M_{1}=M_{1}}}\\ {{\dot{Y}_{1}}}&{{=}}&{{\dot{\phi}M_{1}}}\\ {{}}&{{=}}&{{(A-K C)\phi M_{1}}}\\ {{}}&{{=}}&{{(A-K C)Y_{1}}}\end{array}$$
P = KY? - *YZY?* (8.86) 
Also, from the definition of Y1 we can see that 

$$(8.87)$$

Similarly, we see that 

$$(8.88)$$
$$(8.89)$$

Recall from Equation **(8.37)** that K = *PCTRV1.* Therefore, a differential equation and initial condition for K can be written as 

$$\begin{array}{r c l}{{Y_{2}(0)}}&{{=}}&{{\phi(0)M_{2}=M_{2}}}\\ {{\dot{Y}_{2}}}&{{=}}&{{(A-K C)Y_{2}}}\end{array}$$
K = PCTR-l  = (YlY,' - &Y?)CTR-l  K(0) = P(0)CTR-' (8.89) 
To compute K from its differential equation we need to integrate three equations. 

1. We need to integrate Y1 from Equation (8.87), where Y1 is an n x p matrix. 

2. We need to integrate Y2 from Equation (8.88), where Y2 is an n x (a - p) 
matrix. 

3. We need to integrate K from Equation (8.89), where K is an n x r matrix (T 
is the number of measurements of the system). 

So we need to perform a total of *n(a* + T) integrations. The direct computation of P from the differential Riccati equation requires *n(n* + **1)/2** integrations. So if 
%(a + T) < (n + 1) then the Chandrasekhar algorithm reduces the computational effort of solving the differential Riccati equation. 

## The Chandrasekhar Algorithm

The Chandrasekhar algorithm can be summarized as follows. 

1. Compute *P(o).* 
2. Use the method of Section **8.3.2.2** to find MI and M2 matrices that satisfy 

P(0) = MlM,T - *M2MF.* 
3. Initialize Yl(0) = MI, Yz(0) = *M2,* and K(0) = *P(0)CTR-l.* 
4. Integrate K, *Y1,* and Y2 as follows: 

$$\begin{array}{r c l}{{\dot{K}}}&{{=}}&{{(Y_{1}Y_{1}^{T}-Y_{2}Y_{2}^{T})C^{T}R^{-1}}}\\ {{\dot{Y}_{1}}}&{{=}}&{{(A-K C)Y_{1}}}\\ {{\dot{Y}_{2}}}&{{=}}&{{(A-K C)Y_{2}}}\end{array}$$
$$(8.90)$$

8.3.2.2 Chandrasekhar factorization The derivation of the Chandrasekhar algorithm requires the factorization of *P(0)* as shown in Equation **(8.83):** 

$$\dot{P}(0)=M_{1}M_{1}^{T}-M_{2}M_{2}^{T}$$
$$(8.91)$$

P(0) = M1M,T - *M2MF* (8.91) 
e(0) is an n x n matrix with rank a 5 n. The number of positive eigenvalues of P(0) is p, and the number of negative eigenvalues is (a *-p).* Matrix MI is an n x p matrix, and M2 is an n x (a - p) matrix. In this section, we will show one way to perform that factorization. 

Since *P(0)* is symmetric, all of its eigenvalues are real. We can therefore write the Jordan form of *P(0)* as 

$$\dot{P}(0)=SDS^{T}\tag{8.92}$$ $$=\left[\begin{array}{ccc}S_{11}&S_{12}&S_{13}\\ S_{21}&S_{22}&S_{23}\\ S_{31}&S_{32}&S_{33}\end{array}\right]\left[\begin{array}{ccc}D_{1}&0&0\\ 0&-D_{2}&0\\ 0&0&0\end{array}\right]\left[\begin{array}{ccc}S_{11}^{T}&S_{21}^{T}&S_{31}^{T}\\ S_{12}^{T}&S_{22}^{T}&S_{32}^{T}\\ S_{13}^{T}&S_{23}^{T}&S_{33}^{T}\end{array}\right]$$

S is an orthogonal matrix whose columns comprise the eigenvectors of *P(0).* The p x p matrix D1 is a diagonal matrix whose entries are the positive eigenvalues of P(0). The (a - p) x (a - p) matrix D2 is a diagonal matrix whose entries are the magnitudes of the negative eigenvalues of *P(0).* Multiplying out the above equation results in P(0) = N1+ N2 (8.93) 
where N1 and N2 are given as 

$${\dot{P}}(0)=N_{1}+N_{2}$$
S11Dlgi S11D1gi 41D1g1  NI = [ S21D1S?1 S2iDiS& S21D1S3T1  s31Dlgl S31Dls& S31Dlg1  1  (8.94) 
 $\large N_1\ \ =\ \ $$  $$\large N_2\ \ =\ \ $$  $$\large=\ \ $$  $$\large=\ \ $$  . 
$$(8.93)$$

Note that Nl is the product of an n x p matrix, the p x p matrix D1, and a /3 x n matrix. N1 can therefore be written as 

$$N_{1}=M_{1}M_{1}^{T}$$
$$M_{1}=\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right]$$
$$\left.\begin{array}{l}{{S_{11}}}\\ {{S_{21}}}\\ {{S_{31}}}\end{array}\right]\sqrt{D_{1}}$$

where MI is the n x p matrix 

$$(8.95)$$
$$(8.96)$$

A similar development can be followed to see that M2 is the n x (a - p) matrix 

$$M_{2}=\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right]$$
$\begin{array}{c}\mbox{\rm S}_{12}\\ \mbox{\rm S}_{22}\\ \mbox{\rm S}_{32}\end{array}$\(\begin{array}{c}\mbox{\rm\ \

## 8.3.3 The Square Root Filter

The early days of Kalman filtering in the 1960s saw a lot of successful applications. But there were also some problems in implementation, many due to numerical difficulties. The differential Riccati equation solution *P(t)* should theoretically always be a symmetric positive semidefinite matrix (since it is a covariance matrix). 

But numerical problems in computer implementations sometimes led to P matrices that became indefinite or nonsymmetric. This **was** often because of the short word lengths in the computers of the 1960s [Sch81].' This led to a lot of research during that decade related to numerical implementations. 

Now that computers have become so much more capable, we don't have to worry about numerical problems as often. Nevertheless, numerical issues still arise in finite word-length implementations of algorithms, especially in embedded systems.2 The square root filter was developed in order to effectively increase the numerical precision of the Kalman filter and hence mitigate numerical difficulties in implementations. 

The square root filter is based on the idea of finding an S matrix such that P = Sp. The S matrix is then called a square root of P. Note that the definition of the square root of P is not that P = 9, but rather P = Sfl. Also note that this definition of the matrix square root is not standard. Some books and papers define the matrix square root as P = 9, others define it as P = flS, and others define it as P = SP. The latter definition is the one that we will use in this book. 

Finally, note that the square root of a matrix may not be unique; that is, there may be more than one solution for S in the equation P = Sfl. (This is analogous to the existence of multiple square roots for scalars. For example, the number 4 has two square roots: +2 and **-2.)** Sections 6.3 and **6.4** contain a discussion of square root filtering for the discrete-time Kalman filter. 

After defining S as the square root of P, we will integrate S instead of P in our Kalman filter solution. This requires more computational effort but it doubles the precision of the filter and helps prevent numerical problems. From the differential Riccati equation of Equation **(8.37),** and the definition of S, we obtain 

$$\dot{P}=AP+PA^{T}-PC^{T}R^{-1}CP+Q$$ $$\dot{S}S^{T}+S\dot{S}^{T}=ASS^{T}+SS^{T}A^{T}-SS^{T}C^{T}R^{-1}CSS^{T}+Q\tag{8.98}$$

Now premultiply both sides by S-' and postmultiply by S-T to obtain 

$$S^{-1}\hat{P}S^{-T}=S^{-1}\hat{S}+\hat{S}^{T}S^{-T}\tag{8.99}$$ $$=S^{-1}AS+S^{T}A^{T}S^{-T}-S^{T}C^{T}R^{-1}CS+S^{-1}QS^{-T}$$

Since P is symmetric positive definite, we can always find an upper triangular S 
such that P = Sp [Go189, MooOO]. For example, consider the following matrices: 

lThe United States' Apollo space program of the 1960s resulted in the first man on the moon in 1969. The Apollo spacecraft guidance computer had a word length of 16 bits [Bat82], which corresponds to **4.8** decimal digits of precision. 2Most microcontrollers in the first decade of the 21st century have 16 bit words, and 8 bit microcontrollers still comprise a large share of the market. 
$$\left.\begin{array}{c}{{2}}\\ {{1}}\\ {{2}}\\ {{1}}\end{array}\right]$$
$$(8.100)$$

$P\;\;=\;\;\left[\begin{array}{c}5\\ 2\end{array}\right]$  $S\;\;=\;\;\left[\begin{array}{c}1\\ 0\end{array}\right]$  . 
[; :] (8.100) 
P is symmetric positive definite, S is upper triangular, and P = Sp. It can be shown that if S is upper triangular, then S and S-l are also upper triangular (see Problem 8.4). Also, the product of upper triangular matrices is another upper triangular matrix (see Problem 8.5). Therefore, the product **S-lS** is upper triangular. Similarly, since fl and FT are lower triangular, the product PFT is lower triangular. That is, s-'S = Mu STs-T = ML (8.101) 
where Mu and ML denote upper triangular and lower triangular matrices. From this we can obtain S = *SMu* (8.102) 

Now we can use Equations (8.99) and (8.101) to find  $$S^{-1}\dot{P}S^{-T}=S^{-1}\dot{S}+\dot{S}^{T}S^{-T}$$ $$=M_{U}+M_{L}$$
$$\begin{array}{r l}{S^{-1}{\dot{S}}}&{{}=}\\ {{\dot{S}}^{T}S^{-T}}&{{}=}\end{array}$$
$$\begin{array}{l}{{M_{U}}}\\ {{M_{L}}}\end{array}$$
$$(8.101)$$
$${\dot{S}}=S M_{U}$$
$$(8.102)$$

$$(8.103)$$

= *Mu+ML* (8.103) 
So we see that Mu is the upper triangular portion of *S-'PS-T.* This gives us the square root algorithm as follows. 

## The Continuous-Time Square Root Kalman Filter

1. The initialization step consists of computing the upper triangular S(0) such that S(O)fl(O) = *P(0).* 
2. At each time step compute P from the differential Riccati equation, and then compute MU as the upper triangular portion of *S-lPST.* 
3. **Use** S = *SMu* to integrate S to the next time step. 4. Use the equation K = PCTR-l = *SSTCTR-'* to compute the Kalman gain. 

This is more computationally expensive than a straightforward integration of the differential Riccati equation, but it is also more numerically stable. The numerical benefits of square root filtering are discussed in more detail in-Section **6.3.** 

## 8.4 Generalizations Of The Continuous-Time Filter

In this section, we will discuss some generalizations of the continuous-time Kalman filter, just as we did in Chapter 7 for the discrete-time Kalman filter. The continuoustime filter was derived under the assumptions that the process and measurement noise was uncorrelated, and that the process and measurement noise was white. We will consider the case in which the process and measurement noise are correlated in Section 8.4.1, and the case in which the measurement noise is colored in Section 8.4.2. 

## 8.4.1 Consider The Continuoustime System Correlated Process And Measurement Noise

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+w}}\\ {{w}}&{{\sim}}&{{(0,Q)}}\\ {{y}}&{{=}}&{{C x+v}}\\ {{v}}&{{\sim}}&{{(0,R)}}\\ {{E[w(t)v^{T}(\tau)]}}&{{=}}&{{M\delta(t-\tau)}}\end{array}$$
$$(8.104)$$
$$(8.105)$$
$$(8.106)$$

Since y - Cx - v = 0 we can write the system dynamics as 

$$\begin{array}{r l}{={}}&{{}A x+w+M R^{-1}(y-C x-v)}\\ {={}}&{{}(A-M R^{-1}C)x+M R^{-1}y+(w-M R^{-1}v)}\\ {={}}&{{}\tilde{A}x+\tilde{u}+\tilde{w}}\end{array}$$

where A, *ii,* and 6 are defined by the above equation. Note that ii is a known input to the X equation, and 6 is a new process noise term. The cross covariance between the new process noise 8 and the measurement noise u can be found as 

$$\begin{array}{r c l}{{E(\hat{w}v^{T})}}&{{=}}&{{E[(w-M R^{-1}v)v^{T}]}}\\ {{}}&{{=}}&{{E(w v^{T})-M R^{-1}E(v v^{T})}}\\ {{}}&{{=}}&{{M-M}}\\ {{}}&{{=}}&{{0}}\end{array}$$

So 8 and w are uncorrelated. The covariance of the new process noise 6 can be found as 

$$\begin{array}{r l}{{\tilde{Q}}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
Q = *E(66T)* 
= 
= 
$$\begin{array}{l}{{E(\tilde{w}\tilde{w}^{T})}}\\ {{E[(w-M R^{-1}v)(w-M R^{-1}v)^{T}]}}\\ {{Q-M R^{-1}M^{T}-M R^{-1}M^{T}+M R^{-1}M^{T}}}\\ {{Q-M R^{-1}M^{T}}}\end{array}$$
The differential Riccati equation **for** Kalman filter for the system given in Equation (8.105) is given by 
$$\begin{array}{l l l}{{\dot{P}}}&{{=}}&{{\bar{A}P+P\bar{A}^{T}-P C^{T}R^{-1}C P+\bar{Q}}}\\ {{}}&{{=}}&{{(A-M R^{-1}C)P+P(A-M R^{-1}C)^{T}-P C^{T}R^{-1}C P+}}\\ {{}}&{{}}&{{Q-M R^{-1}M^{T}}}\end{array}$$
If we define k as 
$$\begin{array}{r c l}{{\tilde{K}}}&{{=}}&{{K+M R^{-1}}}\\ {{}}&{{=}}&{{P C^{T}R^{-1}+M R^{-1}}}\\ {{}}&{{=}}&{{(P C^{T}+M)R^{-1}}}\end{array}$$
$$(8.107)$$
$$(8.108)$$
$$(8.109)$$

then the differential Riccati equation becomes 

$$\dot{P}=A P+P A^{T}+Q-\tilde{K}R\tilde{K}^{T}$$
$$(8.110)$$
$$(8.111)$$

The differential equation for the state estimate can be written as 

$$\begin{array}{r c l}{{\dot{\hat{x}}}}&{{=}}&{{\tilde{A}\hat{x}+\tilde{u}+K(y-C\hat{x})}}\\ {{}}&{{=}}&{{(A-M R^{-1}C)\hat{x}+M R^{-1}y+K(y-C\hat{x})}}\\ {{}}&{{=}}&{{A\hat{x}-M R^{-1}C\hat{x}+M R^{-1}y+(\tilde{K}-M R^{-1})(y-C\hat{x})}}\\ {{}}&{{=}}&{{A\hat{x}+\tilde{K}(y-C\hat{x})}}\end{array}$$

We see that the introduction of correlation between the process and measurement noise has the effect of simply modifying the Kalman gain. The stateupdate equation and the differential Riccati equation retain the same form as for the standard Kalman filter. The Kalman filter for correlated process and measurement noise can be summarized as follows. 

## The Continuous-Time Kalman Filter With Correlated Noise

1. The system dynamics and measurement equation are given as 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+w}}\\ {{}}&{{}}&{{w}}&{{\sim}}&{{(0,Q)}}\\ {{}}&{{}}&{{y}}&{{=}}&{{C x+v}}\\ {{}}&{{}}&{{v}}&{{\sim}}&{{(0,R)}}\\ {{E[w(t)v^{T}(\tau)]}}&{{=}}&{{M\delta(t-\tau)}}\end{array}$$

$$(8.112)$$
E[W(t)VT(T)] = *Mb(t* - T) (8.112) 
2. The continuous-time Kalman filter is given as 

$$\begin{array}{r c l}{{\dot{P}}}&{{=}}&{{A P+P A^{T}+Q-K R K^{T}}}\\ {{K}}&{{=}}&{{(P C^{T}+M)R^{-1}}}\\ {{\dot{\hat{x}}}}&{{=}}&{{A\hat{x}+K(y-C\hat{x})}}\end{array}$$

Note that (as expected) this filter reduces to the standard continuous-time filter of Equation **(8.37)** if the process and measurement noise are uncorrelated (i.e., 
M = 0). This filter can therefore be considered as a general formulation of the continuous-time Kalman filter, with the situation M = 0 as a special case. 

## 8.4.2 Colored Measurement Noise

$${\dot{x}}\quad=$$
$$w\quad\sim$$

In this section we will derive the Kalman filter when the measurement noise is not white. Suppose we have the system 

$$(8.113)$$
$$\begin{array}{c}{{A x+w}}\\ {{(0,Q)}}\\ {{C x+v}}\\ {{N v+\phi}}\\ {{(0,\Phi)}}\end{array}$$
$$(8.114)$$
$$\begin{array}{r l}{y}&{{}=}\\ {\dot{w}}&{{}=}\\ {\phi}&{{}\sim}\end{array}$$

We will assume that w and q5 are uncorrelated white noise processes. We could augment v onto the state vector (as suggested in Section **7.2.2** for discretetime systems), but then the covariance of the measurement noise of the augmented system would be singular, which could potentially cause numerical problems in the Kalman filter implementation. Instead, we will define a new signal as 

$$\hat{y}=\hat{y}-Ny\tag{8.1}$$ $$=\hat{C}x+C\hat{x}+\hat{v}-N(Cx+v)$$ $$=\hat{C}x+C(Ax+w)+(Nv+\phi)-N(Cx+v)$$ $$=(\hat{C}+CA-NC)x+(Cw+\phi)$$ $$=\hat{C}x+\hat{v}$$
$$(8.115)$$

where c and 6 are defined by the above equation. Note that 6 is a white noise process (since w and 4 are uncorrelated and white). So we have defined a new measurement equation that has white noise, but this is at the expense of creating a correlation between the process noise w and the new measurement noise 6. The correlation can be obtained as where the cross correlation matrix M is defined by the above equation. The covariance of the new measurement noise 6 can be obtained as 

$$E[w(t)\hat{v}^{T}(\tau)]=E\left[w(t)(Cw(\tau)+\phi(\tau))^{T}\right]\tag{8.116}$$ $$=QC^{T}\delta(t-\tau)+0$$ $$=M\delta(t-\tau)$$
$$\begin{array}{r c l}{{E(\tilde{v}\tilde{v}^{T})}}&{{=}}&{{E[(C w+\phi)(C w+\phi)^{T}]}}\\ {{\tilde{R}}}&{{=}}&{{C Q C^{T}+\Phi}}\end{array}$$
$$(8.117)$$

So we have defined a new measurement equation with white noise. We have the correlation between the process noise and the new measurement noise in Equation (8.116), and the covariance of the new measurement noise in Equation (8.117). Now we can use the results from Section 8.4.1 which discussed Kalman filtering for systems with correlated process and measurement noise. The Kalman filter can be written from Equation (8.113) as 

$$\dot{P}=AP+PA^{T}+Q-K\tilde{R}K^{T}$$ $$K=(PC^{T}+M)\tilde{R}^{-1}$$ $$\dot{\tilde{x}}=A\hat{x}+K(\hat{y}-\tilde{C}\hat{x})$$ $$=A\hat{x}+K(\hat{y}-Ny-\tilde{C}\hat{x})\tag{8.118}$$

However, the new measurement that we defined in Equation (8.115) could cause some problems. The original measurement y is already a noisy measurement, so the new measurement (which contains y) will be even more noisy. How can we avoid the use of y in the filter? We can attack this problem by looking at the derivative of the product Ky as follows: 

$$\begin{array}{r c l}{{\frac{d(K y)}{d t}}}&{{=}}&{{\dot{K}y+K\dot{y}}}\\ {{}}&{{}}&{{K\dot{y}}}&{{=}}&{{\frac{d(K y)}{d t}-\dot{K}y}}\end{array}\tag{8.119}$$
$$z={\hat{x}}-K y$$

The dynamic equation for the state estimate in Equation (8.118) can then be written as follows: 

$$\begin{array}{r c l}{{\dot{\hat{x}}}}&{{=}}&{{A\hat{x}+\frac{d(K y)}{d t}-\dot{K}y-K(N y+\tilde{C}\hat{x})}}\\ {{}}&{{}}&{{}}\\ {{\dot{\hat{x}}-\frac{d(K y)}{d t}}}&{{=}}&{{(A-K\tilde{C})\hat{x}-(\dot{K}+K N)y}}\end{array}$$
Now define a new signal z as z=f-Ky 
$$(8.120)$$
$$(8.121)$$
$${\mathrm{tion~}}(8.120){\mathrm{:}}$$
$$(8.122)$$
$${\dot{z}}=(A-K{\tilde{C}}){\hat{x}}-({\dot{K}}+K N)y$$

Differentiating z results in the right side of Equation (8.120): 
t = (A - *KC)?* - (k + KN)~ (8.122) 
Here we have an equation for k that we can integrate to solve for z. We can then use our solution for z in Equation (8.121) to solve for 2, So the only signal we have to differentiate in the Kalman filter algorithm is the Kalman gain K, because we need K in the computation of k above. However, this differentiation should be much easier than differentiating y, because we expect the Kalman gain K to be much smoother than the noisy measurement y. The Kalman filter for the case of colored measurement noise can be summarized as follows. 

## The Continuous-Time Kalman Filter With Colored Measurement Noise

1. The system and measurement equations are given as 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+w}}\\ {{w}}&{{\sim}}&{{(0,Q)}}\\ {{y}}&{{=}}&{{C x+v}}\\ {{\dot{v}}}&{{=}}&{{N v+\phi}}\\ {{\phi}}&{{\sim}}&{{(0,\Phi)}}\end{array}$$

$$(8.123)$$

where w and \#J and uncorrelated white noise processes. 

2. Make the following matrix definitions: 

$$\begin{array}{r c l}{{\tilde{C}}}&{{=}}&{{\dot{C}+C A-N C}}\\ {{\tilde{R}}}&{{=}}&{{C Q C^{T}+\Phi}}\\ {{M}}&{{=}}&{{Q C^{T}}}\end{array}$$
$$(8.124)$$

3. Initialize the Kalman filter as 

$$\begin{array}{r c l}{{K(0)}}&{{=}}&{{\{P(0)C^{T}+M\}\bar{R}^{-1}}}\\ {{z(0)}}&{{=}}&{{\hat{x}(0)-K(0)y(0)}}\end{array}$$
$$(8.125)$$

4. Integrate *P, K,* and z using the following equations: 

$$\begin{array}{r c l}{{\dot{P}}}&{{=}}&{{A P+P A^{T}+Q-K\tilde{R}K^{T}}}\\ {{\dot{K}}}&{{=}}&{{\frac{d}{d t}[(P C^{T}+M)\tilde{R}^{-1}]}}\\ {{\dot{z}}}&{{=}}&{{(A-K\tilde{C})\hat{x}-(\dot{K}+K N)y}}\end{array}$$
$$(8.126)$$

Note that the K equation can be simplified to the following if Q, C, and @ 
are constant: k = **pcTR-1** *(8.127)* 
5. Compute the state estimate as 

$$\dot{K}=\dot{P}C^{T}\tilde{R}^{-1}$$

$$(8.127)$$
$$(8.128)$$
$${\hat{x}}=z+K y$$
?=,Z++Ky *(8.128)* 

## Example **8.4**

Suppose that it is known that a continuous-time measurement v(t) has a total power of 1 watt and a power spectrum that is bandlimited to frequencies below 10 Hz. In this example, we will use our knowledge of the frequency content of *v(t)* to obtain a dynamic model for v(t). The power spectrum *Sv(w)* can be plotted as shown in Figure *8.1.* The magnitude of the spectrum, **1/40~,** is obtained by realizing that the total power of the signal (1 watt) is equal to the integral from *-oo* to +oo of *Sv(w),* and *Sv(w)* is an even function of w. 

The spectrum shown in Figure *8.1* can be approximated as 

$$S_{v}(\omega)\approx\frac{1/2}{\omega^{2}+(20\pi)^{2}}\tag{8.129}$$ $$=\left(\frac{1}{j\omega+20\pi}\right)\left(\frac{1}{-j\omega+20\pi}\right)\left(\frac{1}{2}\right)$$ $$=G(\omega)G(-\omega)S_{\phi}(\omega)$$

This shows that *v(t)* is the output of a linear system with a transfer function of *G(w)* and an input of *\#(t),* where *\#(t)* is white noise with a variance of 1/2 
(see Equation *3.75).* This can be written in the sdomain and then translated to the time domain as follows: 

$$\begin{array}{c}{{V(s)}}\\ {{}}\end{array}$$
$$\begin{array}{r l}{={}}&{{}G(s)\Phi(s)}\\ {={}}&{{}{\frac{\Phi(s)}{s+20\pi}}}\\ {={}}&{{}\Phi(s)}\\ {={}}&{{}-20\pi V(s)+\Phi(s)}\\ {={}}&{{}-20\pi v+\phi}\end{array}$$
$$(8.130)$$
sV(s) + *20TV(S)* = @(s) 
where *+(t)* is white noise with variance @ = *1/2.* Additional discussion and examples of this method can be found in [Bur99]. 

vvv 

## 8.5 The Steady-State Continuous-Time Kalman Filter

In some situations, the Kalman filter converges t o a n LTI filter. If this is the case then we can often get good filtering performance by using a constant Kalman gain K in the filter. Then we do not have to worry about integrating the differential Riccati equation to solve for P and we do not have to worry about updating K in 

![24_image_0.png](24_image_0.png)

Figure **8.1** Power spectrum of bandlimited measurement noise for Example 8.4. 
real time. This can provide a large savings in filter complexity and computational effort at the cost of only a small sacrifice of performance. In this section, we discuss the conditions under which the continuous-time filter converges to an LTI filter, and the steady-state filter's relationship to Wiener filtering and optimal control. 

## 8.5.1 The Algebraic Riccati Equation

Recall from Equation (8.37) that the differential Riccati equation is given as 

$${\dot{P}}=-P C^{T}R^{-1}C P+A P+P A^{T}+Q$$
$$(8.131)$$

If A, C, Q, and R are constant (i.e., the system and measurement equations form an LTI system with constant noise covariances) then P may reach a steady-state value and P may eventually reach zero. This implies that 

$$4^{T}+Q=0$$
$$-P C^{T}R^{-1}C P+A P+P A^{T}+Q=0$$
$$(8.132)$$
-PCTR-lCP + AP + PAT + Q = 0 (8.132) 
This is called an algebraic Riccati equation (ARE). To be more specific, it is called a continuous ARE (CARE) .3 The ARE solution may not always exist, and even if it does exist it may not result in a stable Kalman filter. We will summarize the most important Riccati equation convergence results below, but first we need to define what it means for a system to be controllable on the imaginary axis. 

Definition 12 The matrix pair (A, B) is controllable on the imaginary axis if there exists some matrix K such that (A - *BK) does not have any eigenvalues on the* imaginary *axis.* 
31n the MATLAB Control System Toolbox the CARE can be solved by invoking the command P = CARE(AT, **CT, Q,** *8).* The reason that the transposes are required is that MATLAB's CARE 
command is designed to solve the ARE for continuous-time optimal control problems. When we use it to solve for the Kalman filtering problem we need to transpose the A and C matrices, as discussed in Section 8.5.3. 

This is similar to the concept of controllability on the unit circle for discretetime systems (see Section **7.3).** Now we summarize the most important Riccati equation convergence results from [KaiOO], where proofs are given. Recall that the ARE is given as 
-PCTR-'CP + AP + *PAT* + Q = 0 **(8.133)** 
We assume that Q 2 0 and R > 0. We define G as any matrix such that GGT = Q. 

The corresponding steady-state Kalman gain K is given as 

$$-P C^{T}R^{-1}C P+A P+P A^{T}+Q=0$$
$$K=P C^{T}R^{-1}$$
$$(8.134)$$
$$(8.135)$$
K = *PCTR-'* **(8.134)** 
The steady-state Kalman filter is given as 

$${\dot{\hat{x}}}=(A-K C){\hat{x}}+K y$$
h = (A - *KC)2* + Ky **(8.135)** 
We say that the CARE solution P is stabilizing if it results in a stable steady-state filter. That is, P is defined as a stabilizing CARE solution if all of the eigenvalues of (A - *KC)* have negative real parts. 

Theorem 27 The **CARE** has a unique positive semidefinite solution P if and only if both of the following conditions hold. 

1. (A, C) is detectable. 

2. **(A,** *G) is stabilizable.* 
Furthermore, the corresponding steady-state Kalman filter is stable. That is, the eigenvalues of (A - **KC)** *have negative real parts.* 
This theorem is analogous to Theorem 23 for discretetime Kalman filters. The above theorem does not preclude the existence of CARE solutions that are negative definite or indefinite. If such solutions exist, then they would result in an unstable Kalman filter. If we weaken the stabilizability condition in the above theorem, we obtain the following. 

Theorem 28 The **CARE** *has at least one positive semidefinite solution P if and* only if both of *the following conditions hold.* 
1. (A, *C) is detectable.* 
2. (A, G) *is controllable on the imaginary* axis. 

firthewnore, exactly one of the positive semidefinite ARE *solutions results an a* stable steady-state Kalman filter. 

This theorem is analogous to Theorem 24 for discretetime Kalman filters. This theorem states conditions for the existence of exactly one stabilizing positive definite CARE solution. However, there may be additional CARE solutions (positive definite or otherwise) that result in unstable Kalman filters. If a timevarying Kalman filter is run in this situation, then the Kalman filter equations may converge to either a stable or an unstable filter, depending on the initial condition *P(0).* If we strengthen the controllability condition of Theorem **28,** we obtain the following. 

Theorem 29 The CARE has at least one positive definite solution P if and only if both of *the following conditions hold.* 
1. (A, C) is detectable. 

2. (A, G) is controllable in the closed left half plane. 

Furthermore, exactly one of *the positive definite CARE solutions results in a stable* steady-state Kalman filter. 

This theorem is analogous to Theorem 25 for discretetime Kalman filters. If we drop the controllability condition in the above two theorems, we obtain the following. 

Theorem 30 The CARE has at least one positive semidefinite solution P if (A, C) 
is detectable. firthemnore, at least one such solution results in a marginally stable steady-state Kalman filter. 

This theorem is analogous to Theorem 26 for discretetime Kalman filters. Note that the resulting filter is only marginally stable, so it may have eigenvalues on the imaginary axis. Also note that this theorem poses a sufficient (not necessary) 
condition. That is, there may be a stable steady-state Kalman filter even if the conditions of the above theorem do not hold. Furthermore, even if the conditions of the theorem do hold, there may be CARE solutions that result in unstable Kalman filters. 

Additional results related to the stability of the steady-state continuous-time filter can be found many places, including [Aok67, Buc67, Buc68, Kwa721. Many practical Kalman filters are applied to systems that do not meet the conditions of the above theorems, but the filters still work well in practice. 

In this example we consider the following two-state system that is taken from [Buc68, Chapter **51:** 

$$(8.136)$$
$$(8.137)$$

$${\dot{P}}=-P C^{T}R^{-1}C P+A P+P A^{T}+Q$$

In the remainder of this example, we use the symbol G to denote any matrix such that *GGT* = Q. The differential Riccati equation **for** the Kalman filter is given as P = *-PCTR-'CP* + AP + PAT + Q (8.137) 
This can be written as the following three coupled differential equations. 

$$\dot{p}_{11}=2a_{1}p_{11}-p_{11}^{2}/r_{1}-p_{12}^{2}+q_{1}1\tag{8.138}$$ $$\dot{p}_{12}=(a_{1}+a_{2})p_{12}-p_{11}p_{12}/r_{1}-p_{12}p_{22}/r_{2}+q_{12}$$ $$\dot{p}_{22}=2a_{2}p_{22}-p_{12}^{2}/r_{1}-p_{22}^{2}/r_{2}+q_{22}$$

We set these derivatives equal to zero to obtain the steady-state Riccati equation solution. 

If a1 \# a2 and **412** \# 0, then **(A,** C) is detectable and *(A,* G) is stabilizable 
(see Problem 8.8). The results of Theorem 27 therefore apply to this situation. 

It can be shown that the unique positive semidefinite ARE solution in this case is 

P22 = 7-2 [a2+ (12 - g2]  41 1  71 =  -  7-1 +a:  P12  7-2  12 = -+a; (8.139)  422 
$$(8.139)$$
This results in a stable steady-state Kalman filter. 

If a1 = a2 < **0,412** \# 0, and IQI = 0, then *(A,* C) is detectable, and **(A,** G) 
is stabilizable (see Problem 8.9). The results of Theorem 27 therefore apply to this situation as well. It can be shown that the unique positive semidefinite ARE solution in this case is given as 

$$p_{11}=q_{11}/\gamma_{3}$$ $$p_{22}=q_{22}/\gamma_{3}$$ $$p_{12}=q_{12}/\gamma_{3}$$ $$\gamma_{3}=-a_{1}+\left(a_{1}^{2}+q_{11}/r_{1}+q_{22}/r_{2}\right)^{1/2}\tag{8.140}$$

This results in a stable steady-state Kalman filter. 

If a1 = a2 > **0, 412** \# 0, and IQI = 0, then *(A,C)* is detectable and 
(A, G) is controllable on the imaginary axis, but *(A,* G) is not stabilizable (see Problem 8.10). The results of Theorem 27 do not apply to this situation, but Theorem 28 does apply to this situation. it can be shown that Equations (8.139) and (8.140) are both positive semidefinite ARE solutions in this case. If we integrate Equation (8.138) we may come up with Equation (8.139) 
as the steady-state solution, or we may come up with Equation (8.140) as the steady-state solution, depending on the initial condition *P(0).* However, only one of the solutions will result in a stable Kalman filter.4 To be more specific, consider the case a1 = a2 = 1, 411 = q12 = **422** = 0, and 7-1 = **7-2** = 1. For these values, we can simulate the differential Riccati 41f we use **MATLAB's** CARE function then we will get the stabilizing solution. 

equations of Equation (8.138) to find the steady-state Riccati solution, the steady-state Kalman gain, and the steady-state estimator, as follows: 

$$P=\left[\begin{array}{cc}2&0\\ 0&2\end{array}\right]\mbox{or}\left[\begin{array}{cc}0&0\\ 0&0\end{array}\right]$$ $$K=PC^{T}R^{-1}$$ $$=\left[\begin{array}{cc}2&0\\ 0&2\end{array}\right]\mbox{or}\left[\begin{array}{cc}0&0\\ 0&0\end{array}\right]$$ $$\dot{\hat{x}}=(A-KC)\hat{x}+Ky$$ $$=(-\hat{x}+Ky)\mbox{or}(\hat{x}+Ky)\tag{8.141}$$

The ARE solution depends on the initial condition *P(0).* The first ARE 
solution results in a positive semidefinite ARE solution that gives a stable Kalman filter. The second ARE solution results in a positive semidefinite ARE solution that gives an unstable Kalman filter. This agrees with Theorem 28. 

vvv 

## 8.5.2

Consider the steady-state continuous-time Kalman filter. 

## The Wiener Filter Is A Kalman Filter

$${\dot{\hat{x}}}=A x+K(y-C{\hat{x}})$$
$$(8.142)$$
1 = AZ + K(Y - cq (8.142) 
Taking the Laplace transform of both sides of this equation gives 
$$(sI-A+KC)\hat{X}(s)=KY(s)$$ $$\hat{X}(s)=(sI-A+KC)^{-1}KY(s)\tag{8.143}$$

The transfer function from y(t) to *?(t)* is identical to the transfer function of the Wiener filter [Buc68, Chapter 5],Sha82, [Sag7l, Chapter **71.** In other words, the Wiener filter is a special case of the Kalman filter. The equivalence of discrete-time Wiener and Kalman filtering is discussed in [Men87]. 

Consider the scalar system given by 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{-x+w}}\\ {{y}}&{{=}}&{{x+v}}\end{array}$$

$$(8.144)$$
$$(8.145)$$
y = *x+w* (8.144) 
where w and w are zero-mean, uncorrelated white noise processes with respective variances Q = 2 and R = 1. The steady-state Kalman filter for this system can be obtained by solving Equation (8.37) with P = 0, from which we obtain 1 = *-A*+ (A-* l)y (8.145) 
Taking the Laplace transform of this estimator gives 

$${\dot{\hat{x}}}=-{\sqrt{3}}{\hat{x}}+({\sqrt{3}}-1)y$$
$$(s+{\sqrt{3}}){\hat{X}}(s)=({\sqrt{3}}-1)Y(s)$$
$$(8.146)$$
(s + **&)R(s)** = (6 - 1)Y(s) (8.146) 
In other words, the Kalman filter is equivalent to passing the measurement y(t) through the transfer function *G(s),* which is given as 

$$G(s)={\frac{\sqrt{3}-1}{s+\sqrt{3}}}$$
$$(8.147)$$
$$(8.148)$$

G(s) = - **(8.147)** 
The impulse response of the Kalman filter is obtained by taking the inverse Laplace transform, which gives 

$$g(t)=({\sqrt{3}}-1)e^{-{\sqrt{3}}t},\ \ \ \ t\geq0$$

Now we will obtain the power spectrum of the state by taking the Laplace transform of Equation **(8.144).** This gives 

$$\begin{array}{r c l}{{s X(s)}}&{{=}}&{{-X(s)+W(s)}}\\ {{}}&{{X(s)}}&{{=}}&{{\frac{1}{s+1}W(s)}}\end{array}$$

We see that the state *x(t)* can be obtained by passing the white noise w(t) 
(which has a power spectrum *Sw(w)* = Q = 2) through the transfer function L(s) = l/(s + 1). From Equation **(3.75)** we see how to compute the power spectrum of the output of a linear system. This gives the power spectrum of 4t) 

$$(8.149)$$
$$S_{x}(\omega)=L(-\omega)L(\omega)S_{w}(\omega)\tag{8.150}$$ $$=\left(\frac{1}{-j\omega+1}\right)\left(\frac{1}{j\omega+1}\right)2$$ $$=\frac{2}{\omega^{2}+1}$$

The causal Wiener filter for a signal with this power spectrum, corrupted by white measurement noise with a unity power spectrum, was obtained in Example **3.10.** The Wiener filter was found to be identical to the steadystate Kalman filter of Equation **(8.148).** This example serves to illustrate the equivalence of Wiener filtering and steady-state Kalman filtering. 

vvv 

## 8.5.3 Duality

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+w}}\\ {{w}}&{{\sim}}&{{N(0,Q)}}\\ {{}}&{{}}&{{x}}\end{array}$$

It is interesting to note the duality between optimal estimation and optimal control. 

The optimal estimation problem begins with the system and measurement equations 

$$(8.151)$$
$$\begin{array}{r c l}{{y}}&{{=}}&{{C x+v}}\\ {{v}}&{{\sim}}&{{N(0,R)}}\end{array}$$

Recall that Q and R are symmetric matrices. The optimal estimation problem tries to find the state estimate 2 that minimizes the cost function 

$$J_{e}=\int_{0}^{t_{f}}E[(x-\hat{x})^{T}(x-\hat{x})]\,dt\tag{8.152}$$
$$(8.153)$$
$$(8.154)$$

The optimal estimator (the Kalman filter) is given as 

$$E[(x(0)-\hat{x}(0))(x(0)-\hat{x}(0))^{T}]$$ $$AP_{e}+P_{e}A^{T}-P_{e}C^{T}R^{-1}CP_{e}+Q$$ $$P_{e}C^{T}R^{-1}$$ $$A\hat{x}+K_{e}(y-C\hat{x})\tag{1}$$
$$\begin{array}{r l}{P_{e}(0)}&{{}=}\\ {\dot{P}_{e}}&{{}=}\\ {K_{e}}&{{}=}\\ {\dot{\hat{x}}}&{{}=}\end{array}$$
Ke = PeCTR-' 
The differential Riccati equation for the optimal estimator is integrated forward in time from its initial condition *Pe(0).* 
The optimal control problem begins with the system 

$${\dot{x}}=A x+C u$$

$$(8.156)$$
5 = AZ + CU (8.154) 
where u is the control variable. The finitetime optimal control problem tries to fmd the control u that minimizes the cost function 

$$J_{c}=\left.x^{T}\phi x\right|_{t_{f}}+\int_{0}^{t_{f}}(x^{T}Qx+u^{T}Ru)\,dt\tag{8.155}$$

4, Q, and R (which are assumed to be symmetric positive definite matrices) provide user-specified weighting in the performance index. The optimal controller is given as 

$$P_{\rm c}(t_{f})=\phi(t_{f})$$ $$\dot{P}_{\rm c}=-A^{T}P_{\rm c}-P_{\rm c}A+P_{\rm c}CR^{-1}C^{T}P_{\rm c}-Q$$ $$K_{\rm c}=R^{-1}C^{T}P_{\rm c}$$ $$u=-K_{\rm c}x\tag{8.1}$$

The differential Riccati equation for the optimal control problem is integrated backward in time from the final condition *P(tf).* Note the relationships between the optima1 estimation solution of Equation (8.153) and the optimal control solution of Equation (8.156). The differential Riccati equations have the same form, except they are negatives of each other, and A and C are replaced by their transposes. The estimator gain K, and the controller gain Kc have very similar forms. The Q and R covariance matrices in the estimation problems have duals in the cost function weighting matrices of the optimal control problem. 

The dual relationship between the estimation and control problems was noted in the very first papers on the Kalman filter [Ka160, Ka1611. Since then, it has been used many times to extrapolate results known from one problem to obtain new results for the dual problem. 

## 8.6 Summary

In this chapter, we derived the continuous-time Kalman filter by applying a limiting argument to the discretetime Kalman filter. However, just as there are several ways to derive the discretetime Kalman filter, there are also several ways to derive the continuous-time Kalman filter. Kalman and BUCY'S original derivation [Ka161] involved the solution of the Wiener-Hopf integral equation. Another derivation is provided in [ Joh691. 

We have seen that the differential and algebraic Riccati equations are key to the solution of the continuous-time Kalman filter. The scalar version of what is now known as the Riccati equation was initially studied by such mathematical luminaries as James Bernoulli and John Bernoulli in the 1600s' and Jacopo Riccati, Daniel Bernoulli, Leonard Euler, Jean-leRond d' Alembert , and Adrien Legendre in the 1700s. The equation waa first called "Riccati's equation" by d'Alembert in 1763 [Wat22]. Jacopo Riccati originally entered the University of Padua in 1693 to study law, but he found his true calling when his astronomy professor, Stefan0 Angeli, inspired him to study math. Additional technical discussion of Riccati equations can be found in many places, including [Rei72, Lan95, Abo031. 

An account of Riccati equations with indefinite quadratic terms is given in [Ion99]. Interesting historical background to the Riccati equation can be found in [Wat22, Bit911. 

The continuous-time Kalman filter applies to systems with continuous-time white noise in the both the process and measurement equations. Continuous-time white noise is nonintuitive because it has an infinite correlation with itself at the present time, but zero correlation with itself when separated by arbitrarily small nonzero times. However, continuous-time white noise is a limiting case of discretetime white noise, which is intuitively acceptable. Therefore, continuous-time white noise can be accepted as an approximation to reality. This corresponds to many other approximations to reality that we accept at face value (e.g., our mathematical system model is an approximation to reality, and our infinite-precision arithmetic is an approximation to reality). 

The continuous-time Kalman filter applies regardless of the statistical nature of the noise, as long it is zero-mean. That is, the Kalman filter is optimal even when the noise is not Gaussian. The Kalman filter was extended in this chapter to systems with correlated process and measurement noise, and with colored me& surement noise. The steady-state Kalman filter provides near-optimal estimation performance at a small fraction of the computational effort of the timevarying Kalman filter. The steady-state Kalman filter is identical to the Wiener filter of Section 3.4, and has an interesting dual relationship to linear quadratic optimal control. 

## Problems Written Exercises

8.1 Suppose you have two discrete-time systems with identity transition matrices driven with stationary zero-mean white noise. The first system has a sample period of T, and the second system has a sample period of *Tln* for some integer n > 1. 

The noise in the first system has a covariance of Q. What should the covariance of the noise in the second system be in order for both states to have the same covariance at times kT (k = 0,1,2,. . a)? 

8.2 Show that for a general timevarying matrix Y(t), if Y = AY + YAT, where A is a constant matrix, then Y(t) = exp(At)Y(0)exp(ATt). 

8.3 Suppose you have a third-order Newtonian system with 

$$\mathbf{U}$$
$\square$
$\uparrow$
$$\mathbf{0}$$
$\mathrm{Q}$. 
$$\mathbf{0}$$
$\square$
$\square$
$$1\quad0$$
$$\mathbf{0}^{-1}$$
$\downarrow$ . 
$$\mathbf{\Sigma}_{0}^{1}$$
010 
$=\;\frac{1}{2}$
A= [::;I 
$$C\quad=\quad$$
c = [I 0 01 
201 
$$\begin{array}{l l}{{2}}&{{0}}\\ {{0}}&{{1}}\\ {{1}}&{{0}}\end{array}$$
$$Q\ \ =$$

&= [K] 
$$\mathbf{1}$$
$${\boldsymbol{\vec{\imath}}}\quad=\quad$$
$\downarrow$ . 
R=l 
with *P(0)* = I. 

a) What is the rank of *p(O)?* How much computational savings in integration effort can be obtained by using the Chandrasekhar algorithm to find the Kalman gain for this system? 

b) Find MI and M2 such that P(0) = M1Mr - *M2MT.* 
8.4 Show that if S is upper triangular, then S and *S-l* are also upper triangular. 

8.5 Show that the product of upper triangular matrices is another upper triangular matrix. 

8.6 Find the steady-state solution of the differential Riccati equation for a scalar system. Show from your solution how the steady-state solution changes with A, C, Q, and R, and give intuitive explanations. 

8.7 Consider the system of Example 8.3 except with process noise that has a covariance of diag(0, *q).* Find an analytical expression for the steady-state estimationerror covariance. 

8.8 Show that if a1 \# a2 and *412* \# 0 in the system of Example 8.5, then *(A,* C) 
is detectable and **(A,** G) is stabilizable for all matrices G such that *GGT* = Q. 8.9 Show that if a1 = a2 < 0, *q12* \# 0, and IQI = 0 in the system of Example 8.5, then *(A,C)* is detectable and *(A,G)* is stabilizable for all matrices G such that GGT = Q. 

8.10 Show that if a1 = a2 > 0, **q12** \# 0, and IQI = 0 in the system of Example 8.5, then *(A,* C) is detectable and **(A,** G) is controllable on the imaginary axis, but *(A,* G) 
is not stabilizable for all matrices G such that *GGT* = Q. 

## Computer Exercises

8.11 Consider the discrete-time system Xk+1 = *Xk +wk* with the initial condition 50 = 0. The sample time is T and the variance of the zero-mean process noise Wk is equal to *2T.* Simulate the system a few thousand times for 10 s with: (a) T = 0.5 s; (b) T = 0.4 s; (c) T = 0.2 s. **Use** the value of Xk at t = 10 s to obtain a statistical estimate of ~(10) =*E[x2(10)].* 
a) What is your estimate of P(10) for the three sample times given? 

b) What is the analytically derived value for P(lO)? 

8.12 Consider the continuous-time scalar system x = *-x+w* y = z+v where w(t) and *v(t)* are continuous-time white noise with variances Q, = 2 and R, = 1 respectively. Design a continuous-time Kalman filter to estimate x. 

a) What is the theoretical steady-state variance of the estimation error? 

b) Simulate the system for 1000 s with discretization step sizes of **0.4,** 0.2, and **0.1** s. What are the resulting experimental estimation-error variances? 

8.13 Simulate the system of Problem 8.7 **for** 10 seconds with q = 2 and R = 
3. Plot the elements of the estimation-error covariance matrix as a function of time. Compare the experimental RMS estimation errors when using a timcvarying Kalman gain and a constant Kalman gain. 

8.14 Repeat Problem **8.13** using the correlated noise filter when the process noise that affects the second state is equal to the measurement noise. How much do the estimation-error variances decrease due to the correlation between the two noise terms? 

8.15 Consider the system of Example **8.5** with R = I. 

Integrate the Riccati equation with a1 = 1, a2 = 2, 411 = 412 = *q22* = 1, and *P(0)* = I. Plot the Riccati equation solution as a function of time and verify that its steady-state value matches the results of Equation **(8.139)** 
and MATLAB's CARE function. 

Integrate the Riccati equation with a1 = a2 = **-1, qll** = 1, **q12** = 2, 422 = 4, and *P(0)* = I. Plot the Riccati equation solution as a function of time and verify that its steady-state value matches the results of Equation **(8.140)** and MATLAB's CARE function. 

Integrate the Riccati equation with a1 = a2 = 1, 411 = 1,412 = **2,422** = 4, and *P(0)* = I. Plot the Riccati equation solution as a function of time and verify that its steady-state value matches the results of Equation **(8.139)** 
and MATLAB's CARE function. 

Integrate the Riccati equation with a1 = a2 = 1, qll = 1,412 = **2, q22** = 4, and *P(0)* = 0. [Note that this is the same as part (c) except for *P(O).]* 
Plot the Riccati equation solution as a function of time and verify that its steady-state value matches the results of Equation **(8.140).** Does it match the results of MATLAB's CARE function? Does it result in a stable steady-state Kalman filter? 