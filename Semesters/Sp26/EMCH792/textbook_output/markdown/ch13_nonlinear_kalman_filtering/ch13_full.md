---
type: chapter
chapter: 13
title: Nonlinear Kalman filtering
---
# Chapter 13 Nonlinear Kalman Filtering

It appears that no particular approximate [nonlinear] filter is consistently better than any other, though ... any nonlinear filter is better than a strictly linear one. 

-Lawrence Schwartz and Edwin Stear [Sch68] 
All of our discussion to this point has considered linear filters for linear systems. 

Unfortunately, linear systems do not exist. All systems are ultimately nonlinear. 

Even the simple I = *V/R* relationship of Ohm's Law is only an approximation over a limited range. If the voltage across a resistor exceeds a certain threshold, then the linear approximation breaks down. Figure 13.1 shows a typical relationship between the current through a resistor and the voltage across the resistor. At small input voltages the relationship is approximately linear, but if the power dissipated by the resistor exceeds some threshold then the relationship becomes highly nonlinear. 

Even a device as simple as a resistor is only approximately linear, and even then only in a limited range of operation. 

So we see that linear systems do not really exist. However, many systems are close enough to linear that linear estimation approaches give satisfactory results. But "close enough" can only be carried so far. Eventually, we run across a system that does not behave linearly even over a small range of operation, and our linear approaches for estimation no longer give good results. In this case, we need to explore nonlinear estimators. 

![1_image_0.png](1_image_0.png)

Figure **13.1** 
for a limited range of operation, but becomes highly nonlinear beyond that range. 

Typical current/voltage relationship for a resistor. The relationship is linear 
Nonlinear filtering can be a difficult and complex subject. It is certainly not as mature, cohesive, or well understood as linear filtering. There is still a lot of room for advances and improvement in nonlinear estimation techniques. However, some nonlinear estimation methods have become (or are becoming) widespread. These techniques include nonlinear extensions of the Kalman filter, unscented filtering, and particle filtering. 

In this chapter, we will discuss some nonlinear extensions of the Kalman filter. 

The Kalman filter that we discussed earlier in this book directly applies only to linear systems. However, a nonlinear system can be linearized as discussed in Section **1.3,** and then linear estimation techniques (such as the Kalman or H, filter) can be applied. This chapter discusses those types of approaches to nonlinear Kalman filtering. 

In Section **13.1,** we will discuss the linearized Kalman filter. This will involve finding a linear system whose states represent the deviations from a nominal trajectory of a nonlinear system. We can then use the Kalman filter to estimate the deviations from the nominal trajectory, and hence obtain an estimate of the states of the nonlinear system. In Section **13.2,** we will extend the linearized Kalman filter to directly estimate the states of a nonlinear system. This filter, called the extended Kalman filter (EKF), is undoubtedly the most widely used nonlinear state estimation technique that has been applied in the past few decades. In Section **13.3,** we will discuss "higher-order" approaches to nonlinear Kalman filtering. These approaches involve more than a direct linearization of the nonlinear system, hence the expression "higher order." Such methods include second-order Kalman filtering, iterated Kalman filtering, sum-based Kalman filtering, and grid-based Kalman filtering. These filters provide ways to reduce the linearization errors that are inherent in the EKF. They typically provide estimation performance that is better than the EKF, but they do so at the price of higher complexity and computational expense. 

Section **13.4** covers parameter estimation using Kalman filtering. Sometimes, an engineer wants to estimate the parameters of a system but does not care about estimating the states. This becomes a system identification problem. The system equations are generally nonlinear functions of the system parameters. System parameters are usually considered to be constant, or slowly timevarying, and a nonlinear Kalman filter (or any other nonlinear state estimator) can be adapted to estimate system parameters. 

## 13.1 The Linearized Kalman Filter

In this section, we will show how to linearize a nonlinear system, and then use Kalman filtering theory to estimate the deviations of the state from a nominal state value. This will then give us an estimate of the state of the nonlinear system. We will derive the linearized Kalman filter from the continuowtime viewpoint, but the analogous derivation for discretetime or hybrid systems are straightforward. 

Consider the following general nonlinear system model: 

$$\begin{array}{lcl}\dot{x}&=&f(x,u,w,t)\\ y&=&h(x,v,t)\\ w&\sim&(0,Q)\\ v&\sim&(0,R)\end{array}\tag{13.1}$$

The system equation f(.) and the measurement equation *h(.)* are nonlinear functions. We will use Taylor series to expand these equations around a nominal control UO, nominal state *20,* nominal output yo, and nominal noise values wo and vo. These nominal values (all of which are functions of time) are based on a *priori* guesses of what the system trajectory might **look** like. For example, if the system equations represent the dynamics of an airplane, then the nominal control, state, and output might be the planned flight trajectory. The *actual* flight trajectory will differ from this nominal trajectory due to mismodeling, disturbances, and other unforeseen effects. But the actual trajectory should be close to the nominal trajectory, in which case the Taylor series linearization should be approximately correct. The Taylor series linearization of Equation **(13.1)** gives 

$$\dot{x}\approx f(x_{0},u_{0},w_{0},t)+\left.\frac{\partial f}{\partial x}\right|_{0}\left(x-x_{0}\right)+\left.\frac{\partial f}{\partial u}\right|_{0}\left(u-u_{0}\right)+$$ $$\left.\frac{\partial f}{\partial w}\right|_{0}\left(w-w_{0}\right)$$ $$=f(x_{0},u_{0},w_{0},t)+A\Delta x+B\Delta u+L\Delta w$$ $$y\approx h(x_{0},v_{0},t)+\left.\frac{\partial h}{\partial x}\right|_{0}\left(x-x_{0}\right)+\left.\frac{\partial h}{\partial v}\right|_{0}\left(v-v_{0}\right)$$ $$=h(x_{0},v_{0},t)+C\Delta x+M\Delta v\tag{13.2}$$  $\dot{x}$\(\
The definitions of the partial derivative matrices A, *B, C,* L, and M are apparent from the above equations. The 0 subscript on the partial derivatives means that they are evaluated at the nominal control, state, output, and noise values. The definitions of the deviations Ax, Au, Aw, **and** Av are also apparent from the above equations. 

Let us assume that the nominal noise values **wo(t)** and *vo(t)* are both equal to 0 for all time. [If they are not equal to 0 then we should be able to write them as the sum of a known deterministic part and a zero-mean part, redefine the noise quantities, and rewrite Equation **(13.1)** so that the nominal noise values are equal to 0. See Problem **13.11.** Since **wo(t)** and *vo(t)* are both equal to 0, we see that Aw(t) = **w(t)** and **Av(t)** = v(t). Further assume that the control *u(t)* is perfectly known. In general, this is a reasonable assumption. After all, the control input *u(t)* 
is determined by our control system, so there should not be any uncertainty in its value. This means that uo(t) = *u(t)* and **Au(t)** = 0. However, in reality there may be uncertainties in the outputs of our control system because they are connected to actuators that have biases and noise. If this is the case then we can express the control as uo(t) + *Au(t),* where *uO(t)* is known and **Au(t)** is a zero-mean random variable, rewrite the system equations with a perfectly known control signal, and include **Au(t)** as part of the process noise (see Problem **13.2).** Now we define the nominal system trajectory as 

$$\begin{array}{rcl}\dot{x}_{0}&=&f(x_{0},u_{0},w_{0},t)\\ y_{0}&=&h(x_{0},v_{0},t)\end{array}\tag{13.3}$$

We define the deviation of the true state derivative from the nominal state derivative, and the deviation of the true measurement from the nominal measurement, as follows: 

$$\begin{array}{lcl}\Delta\dot{x}&=&\dot{x}-\dot{x_{0}}\\ \Delta y&=&y-y_{0}\end{array}\tag{13.4}$$

With these definitions Equation **(13.2)** becomes 

AX = AAx+Lw 
$A\Delta x+Lw$  $A\Delta x+\tilde{w}$  $(0,\tilde{Q}),\quad\tilde{Q}=LQL^{T}$  $C\Delta x+Mv$  $C\Delta x+\tilde{v}$  $(0,\tilde{R}),\quad\tilde{R}=MRM^{T}$ (13.5)
$$\begin{array}{r l}{\Delta{\dot{x}}}&{{}=}\\ {\quad}&{{}=}\\ {\quad}&{{\bar{w}}\quad\sim}\\ {\Delta y}&{{}=}\\ {\quad}&{{}=}\\ {\quad}&{{\bar{v}}\quad\sim}\end{array}$$
Ay = **CAx+Mv** 
The above equation is a linear system with state Ax and measurement **Ay,** so we can use a Kalman filter to estimate **Ax.** The inputs to the filter consist of **Ay,** which is the difference between the actual measurement y and the nominal measurement yo. The Ax that is output from the Kalman filter is an estimate of the difference between the actual state x and the nominal state 20. The Kalman filter equations for the linearized Kalman filter are 

$$\begin{array}{r l}{\Delta{\hat{x}}(0)}&{{}=}\\ {P(0)}&{{}=}\\ {\Delta{\dot{\hat{x}}}}&{{}=}\\ {K}&{{}=}\\ {\dot{P}}&{{}=}\\ {\hat{x}}&{{}=}\end{array}$$
$$(13.6)$$
K = *pCTR-'* 
$$\begin{array}{l}{{0}}\\ {{E\left[(\Delta x(0)-\Delta\hat{x}(0))(\Delta x(0)-\Delta\hat{x}(0))^{T}\right]}}\\ {{A\Delta\hat{x}+K(\Delta y-C\Delta\hat{x})}}\\ {{P C^{T}\tilde{R}^{-1}}}\\ {{A P+P A^{T}+\tilde{Q}-P C^{T}\tilde{R}^{-1}C P}}\\ {{x_{0}+\Delta\hat{x}}}\end{array}$$
$$\begin{array}{r l}{:}&{{}f(x,u,w,t)}\\ {:}&{{}h(x,v,t)}\\ {,}&{{}(0,Q)}\\ {,}&{{}(0,R)}\end{array}$$

For the Kalman filter, P is equal to the covariance of the estimation error. In the linearized Kalman filter this is no longer true because of errors that creep into the linearization of Equation (13.2). However, if the linearization errors are small then P should be approximately equal to the covariance of the estimation error. The linearized Kalman filter can be summarized as follows. 

## The Continuous-Time Linearized Kalrnan Filter

$$\begin{array}{r l}{{\dot{x}}}&{{}=}\\ {y}&{{}=}\end{array}$$

1. The system equations are given as 

$$(13.7)$$
$$\begin{array}{r l}{w}&{{}\sim}\\ {v}&{{}\sim}\end{array}$$
$$\begin{array}{r l}{x_{0}}&{{}=}\\ {y_{0}}&{{}=}\end{array}$$

The nominal trajectory is known ahead of time: 

$f(x_{0},u_{0},0,t)$  $h(x_{0},0,t)$ (13.8)
$$\frac{\partial f}{\partial x}\Big|_{0}$$
2. Compute the following partial derivative matrices evaluated at the nominal trajectory values: 

(13.9) 
3. Compute the following matrices: 

 = $$\frac{1}{2}$$  = $$\frac{1}{2}$$  = $$\frac{1}{2}$$  = $$\frac{1}{2}$$. 
$$\mathbf{A}$$
$${\boldsymbol{L}}$$
$$\begin{array}{c}{{C}}\\ {{}}\end{array}$$
$$\begin{array}{r c l}{{\bar{Q}}}&{{=}}&{{L Q L^{T}}}\\ {{\bar{R}}}&{{=}}&{{M R M^{T}}}\end{array}$$
$$\Delta y=y-y_{0}$$

$$(13.10)$$
$$(13.11)$$
$$(13.12)$$
4. Define Ay as the difference between the actual measurement y and the nom-
AY=Y-Yo (13.11) 
inal measurement yo: 
5. Execute the following Kalman filter equations: 

$$\begin{array}{r c l}{{\Delta\hat{x}(0)}}&{{=}}&{{0}}\\ {{P(0)}}&{{=}}&{{E\left[(\Delta x(0)-\Delta\hat{x}(0))(\Delta x(0)-\Delta\hat{x}(0))^{T}\right]}}\\ {{\Delta\hat{x}}}&{{=}}&{{A\Delta\hat{x}+K(\Delta y-C\Delta\hat{x})}}\\ {{K}}&{{=}}&{{P C^{T}\tilde{R}^{-1}}}\\ {{\hat{P}}}&{{=}}&{{A P+P A^{T}+\tilde{Q}-P C^{T}\tilde{R}^{-1}C P}}\end{array}$$

6. Estimate the state as follows: 

$${\hat{x}}=x_{0}+\Delta{\hat{x}}$$
h = 20 + Ah **(13.13)** 
The hybrid linearized Kalman filter and the discrete-time linearized Kalman filter are not presented here, but if the development above is understood then their derivations should be straightforward. 

## 13.2 **The Extended Kalman Filter**

The previous section obtained a linearized Kalman filter for estimating the states of a nonlinear system. The derivation was based on linearizing the nonlinear system around a nominal state trajectory. The question that arises is, How do we know the nominal state trajectory? In some cases it may not be straightforward to find the nominal trajectory. However, since the Kalman filter estimates the state of the system, we can use the Kalman filter estimate as the nominal state trajectory. 

This is sort of a bootstrap method. We linearize the nonlinear system around the Kalman filter estimate, and the Kalman filter estimate is based on the linearized system. This is the idea of the extended Kalman filter (EKF), which was originally proposed by Stanley Schmidt so that the Kalman filter could be applied to nonlinear spacecraft navigation problems [Be167]. 

In Section **13.2.1,** we will present the EKF for continuous-time systems with continuous-time measurements. In Section **13.2.2,** we will present the hybrid EKF, which is the EKF for continuous-time systems with discrete-time measurements. In Section **13.2.3,** we will present the EKF for discretetime systems with discretetime measurements. 

## The Continuous-Time Extended Kalman Filter 13.2.1

Combine the & expression in Equation **(13.3)** with the A4 expression in Equation **(13.6)** to obtain 

$$\begin{array}{r c l}{{y_{0}}}&{{=}}&{{h(x_{0},v_{0},t)}}\\ {{}}&{{=}}&{{h(\hat{x},v_{0},t)}}\end{array}$$

ko + Ah = **f(~,** UO, *WO,* t) + **AAh** + K[y - YO - *C(2* - **ZO)]** 

$$(13.14)$$
$$[y-y_{0}-C({\hat{x}}-x_{0})]$$

Now choose zo(t) = *h(t)* so that *Ah(t)* = 0 and *AP(t)* = 0. In other words, our linearization trajectory *zo(t)* is equal to our linearized Kalman filter estimate 2(t). Then the nominal measurement expression in Equation **(13.3)** becomes 

$$(13.15)$$
$$(13.16)$$

and Equation **(13.14)** becomes 4 = **f(h, U, WO,** t) + K [Y - *h(h,~o, t)]* **(13.16)** 
This is equivalent to the linearized Kalman filter except that we have chosen zo = 2, and we have rearranged the equations to obtain h directly. The Kalman gain K 
is the same as that presented in Equation **(13.6).** But this formulation inputs the measurement y directly, and outputs the state estimate h directly. This is often referred to as the extended Kalman-Bucy filter because Richard Bucy collaborated with Rudolph Kalman in the first publication of the continuoustime Kalman filter [Kal61]. The continuowtime EKF can be summarized as follows. 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f(x,u,w,t)}}\\ {{y}}&{{=}}&{{h(x,v,t)}}\\ {{w}}&{{\sim}}&{{(0,Q)}}\\ {{v}}&{{\sim}}&{{(0,R)}}\end{array}$$

## The Continuous-Time Extended Kalman Filter

$$(13.17)$$
$$\begin{array}{l}{{\left.{\frac{\partial f}{\partial x}}\right|_{\hat{x}}}}\\ {{\left.{\frac{\partial f}{\partial w}}\right|_{\hat{x}}}}\\ {{\left.{\frac{\partial h}{\partial x}}\right|_{\hat{x}}}}\\ {{\left.{\frac{\partial h}{\partial v}}\right|_{\hat{x}}}}\end{array}$$

2. Compute the following partial derivative matrices evaluated at the current state estimate: 

$$(13.18)$$

3. Compute the following matrices: 

$A\quad=\quad\cdot$  $L\quad=\quad\cdot$  $C\quad=\quad\cdot$  $M\quad=\quad\cdot$  . 
$$\begin{array}{r c l}{{\tilde{Q}}}&{{=}}&{{L Q L^{T}}}\\ {{\tilde{R}}}&{{=}}&{{M R M^{T}}}\end{array}$$
$$(13.19)$$
$$(13.20)$$
$$(13.21)$$
4. Execute the following Kalman filter equations: 

$$\begin{array}{r c l}{{}}&{{}}\\ {{\hat{x}(0)}}&{{=}}&{{E[x(0)]}}\\ {{P(0)}}&{{=}}&{{E\left[(x(0)-\hat{x}(0))(x(0)-\hat{x}(0))^{T}\right]}}\\ {{}}&{{}}\\ {{\hat{x}}}&{{=}}&{{f(\hat{x},u,w_{0},t)+K\left[y-h(\hat{x},v_{0},t)\right]}}\\ {{K}}&{{=}}&{{P C^{T}\tilde{R}^{-1}}}\\ {{\hat{P}}}&{{=}}&{{A P+P A^{T}+\tilde{Q}-P C^{T}\tilde{R}^{-1}C P}}\end{array}$$
where the nominal noise values are given as wo = 0 and vo = 0. 
i, = -2, + - sin 8 + - 
ib = *-ib* - - cos 8 + - 
ample 1.4 and are repeated here:  $$\dot{i}_{a}=\frac{-R}{L}i_{a}+\frac{\omega\lambda}{L}\sin\theta+\frac{u_{a}+q_{1}}{L}$$ $$\dot{i}_{b}=\frac{-R}{L}i_{b}-\frac{\omega\lambda}{L}\cos\theta+\frac{u_{b}+q_{2}}{L}$$ $$\dot{\omega}=\frac{-3\lambda}{2J}i_{a}\sin\theta+\frac{3\lambda}{2J}i_{b}\cos\theta-\frac{F\omega}{J}+q_{3}$$ $$\dot{\theta}=\omega$$
In this example, we will use the continuous-time EKF to estimate the state 
of a two-phase permanent magnet synchronous motor. The system equations 
are given in Example **1.4** and are repeated here: 
where i, and ib are the currents in the two windings, 6' and w are the angular position and velocity of the rotor, R and L are the winding resistance and inductance, X is the flux constant, and F is the coefficient of viscous friction. 

The control inputs ua and Ub consist of the applied voltages across the two windings, and J is the moment of inertia of the motor shaft and load. The state is defined as 

$T=\left[\begin{array}{cccc}i_{a}&i_{b}&\omega&\theta\end{array}\right]^{T}$ (13.22)
The qi terms are process noise due to uncertainty in the control inputs **(41** 
and 42) and the load torque *(43).* The partial derivative A matrix is obtained as 

$$A=\frac{\partial f}{\partial x}\tag{13.23}$$ $$=\left[\begin{array}{ccc}-R/L&0&\lambda s/L&x_{3}\lambda c/L\\ 0&-R/L&-\lambda c/L&x_{3}\lambda s/L\\ -3\lambda s/2/J&3\lambda c/2/J&-F/J&-3\lambda(x_{1}c+x_{2}s)/2/J\\ 0&0&1&0\end{array}\right]$$

where we have used the notation s = sinxq and c = cosx4. Suppose that we can measure the winding currents with sense resistors so our measurement equations are 

$$(13.24)$$
$$\begin{array}{r c l}{{y(1)}}&{{=}}&{{i_{a}+v(1)}}\\ {{y(2)}}&{{=}}&{{i_{b}+v(2)}}\end{array}$$
$$\begin{array}{r c l}{{u_{a}(t)}}&{{=}}&{{\sin(2\pi t)}}\\ {{u_{b}(t)}}&{{=}}&{{\cos(2\pi t)}}\end{array}$$

where v(1) and 42) are independent zero-mean white noise processes with standard deviations equal to 0.1 amps. The nominal control inputs are set to 

$$(13.25)$$

The actual control inputs are equal to the nominal values plus 41 and 42 (electrical noise terms), which are independent zero-mean white noise processes with standard deviations equal to 0.01'amps. The noise due to load torque disturbances **(43)** has a standard deviation of 0.5 rad/sec2. Measurements are obtained continuously. Even though our measurements consist only of the winding currents and the system is nonlinear, we can use a continuous-time EKF (implemented in analog circuitry or very fast digital logic) to estimate the rotor position and velocity. The simulation results are shown in Figure 13.2. The four states are estimated quite well. In particular, the rotor position estimate is so good that the true and estimated rotor position traces are not distinguishable in Figure 13.2. 

The P matrix quantifies the uncertainty in the state estimates. If the nonlinearities in the system and measurement are not too severe, then the P matrix should give us an idea of how accurate our estimates are. In this example, the standard deviations of the state estimation errors were obtained from the simulation and then compared with the diagonal elements of the steady-state P matrix that came out of the Kalman filter. Table 13.1 shows a comparison of the estimation errors that were determined by simulation and 

![8_image_0.png](8_image_0.png)

Figure **13.2** 
permanent magnet synchronous motor of Example 13.1. 

Continuous extended Kalman filter simulation results for the two-phase Table 13.1 Example **13.1** results showing one standard deviation state estimation errors determined from simulation results and determined from the P matrix of the EKF. These results are for the two-phase permanent magnet motor simulation. This table shows that the P matrix gives a good indication of the magnitude of the EKF 
state estimation errors. 

|                   | Simulation   | P Matrix     |
|-------------------|--------------|--------------|
| Winding A Current | 0.054 amps   | 0.094 Amps   |
| Winding B Current | 0.052 amps   | 0.094 Amps   |
| SPd               | 0.26 rad/sec | 0.44 rad/sec |
| Position          | 0.013 rad    | 0.025 rad    |

the theoretical estimation errors based on the P matrix. We see that the P matrix gives a good indication of the magnitude of the estimation errors. 

vvv 

## 13.2.2 The Hybrid Extended Kalman Filter

Many real engineering systems are governed by continuous-time dynamics whereas the measurements are obtained at discrete instants of time. In this section, we will derive the hybrid EKF, which considers systems with continuoustime dynamics and discretetime measurements. This is the most common situation encountered in practice. 

Suppose we have a continuous-time system with discretetime measurements as follows: 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f(x,u,w,t)}}\\ {{y_{k}}}&{{=}}&{{h_{k}(x_{k},v_{k})}}\\ {{w(t)}}&{{\sim}}&{{(0,Q)}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$(13.26)\,$$... 
$$(13.27)$$

The process noise *w(t)* is continuous-time white noise with covariance Q, and the measurement noise Vk is discretetime white noise with covariance *Rk.* Between measurements we propagate the state estimate according to the known nonlinear dynamics, and we propagate the covariance as derived in the continuous-time EKF of Section 13.2.1 using Equation (13.20). Recall that the P expression from Equai tion (13.20) is given as 

$$\dot{P}=A P+P A^{T}+L Q L^{T}-P C^{T}(M R M^{T})^{-1}C P$$
$$\begin{array}{r c l}{{\dot{\hat{x}}}}&{{=}}&{{f(\hat{x},u,w_{0},t)}}\\ {{\dot{P}}}&{{=}}&{{A P+P A^{T}+L Q L^{T}}}\end{array}$$

In the hybrid EKF, we should not include the R term in the P equation because we are integrating P between measurement times, during which we do not have any measurements. Another way of looking at it is that in between measurement times we have measurements with infinite covariance (R = *oo),* so the last term on the right side of the P equation goes to zero. This gives us the following for the timeupdate equations of the hybrid EKF: 

$$(13.28)$$
$$(13.29)$$
$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+M_{k}R_{k}M_{k}^{T})^{-1}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k}|y_{k}-h_{k}(\hat{x}_{k}^{-},v_{0},t_{k})|}}\\ {{P_{k}^{+}}}&{{=}}&{{(I-K_{k}H_{k})P_{k}^{-}(I-K_{k}H_{k})^{T}+K_{k}M_{k}R_{k}M_{k}^{T}K_{k}^{T}}}\end{array}$$

where A and L are given in Equation (13.18). The above equations propagate 2 from to *2;,* and P from PzVl to *P;.* Note that wo is the nominal process noise in the above equation; that is, *wo(t)* = 0. 

At each measurement t'ime, we update the state estimate and the covariance as derived in the discretetime Kalman filter (Chapter *5):* 
where **210** is the nominal measurement noise; that is, vo = 0. Hk is the partial derivative of *hk(Xk,Vk)* with respect to **Xk,** and Mk is the partial derivative of hk(Zk, Vk) with respect to *Vk. Hk* and Mk are evaluated at *2;.* 
Note that Pk *and* Kk cannot be computed offline because they depend on Hk and Mk, which depend on *2;,* which in turn depends on the noisy measurements. There fore, a steady-state solution does not (in general) exist to the extended Kalman filter. However, some efforts at obtaining steady-state approximations to the extended Kalman filter have been reported in [Saf78]. 

The hybrid EKF can be summarized as follows. 

## The Hybrid Extended Kalman **Filter**

1. The system equations with continuous-time dynamics and discretetime measurements are given as follows: 

$$(13.30)$$
$$(13.31)$$
$$(13.32)$$

2. Initialize the filter as follows: 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f(x,u,w,t)}}\\ {{y_{k}}}&{{=}}&{{h_{k}(x_{k},v_{k})}}\\ {{w(t)}}&{{\sim}}&{{(0,Q)}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E[x_{0}]}}\\ {{P_{0}^{+}}}&{{=}}&{{E\left[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}\right]}}\end{array}$$

3. For k = **1,2,**. .., perform the following. 

(a) Integrate the state estimate and its covariance from time ( k - 1)+ to time k- as follows: 

$$\begin{array}{r c l}{{\dot{\hat{x}}}}&{{=}}&{{f(\hat{x},u,0,t)}}\\ {{\dot{P}}}&{{=}}&{{A P+P A^{T}+L Q L^{T}}}\end{array}$$

where F and L are given in Equation **(13.18).** We begin this integration process with 2 = *2t-l* and P =*P:--,.* At the end of this integration we have 2 =2; and P =*PF.* 
(b) At time k, incorporate the measurement Y k into the state estimate and estimation covariance as follows: 

$$K_{k}=P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+M_{k}R_{k}M_{k}^{T})^{-1}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K_{k}(y_{k}-h_{k}(\hat{x}_{k}^{-},0,t_{k}))\tag{13.33}$$ $$P_{k}^{+}=(I-K_{k}H_{k})P_{k}^{-}(I-K_{k}H_{k})^{T}+K_{k}M_{k}R_{k}M_{k}^{T}K_{k}^{T}$$

Hk and Mk are the partial derivativesof hk(Zk, Ok) with respect to Z k and Vk, and are both evaluated at 2i. Note that .otherequivalent expressions can be used for Kk and Pz, as is apparent from Equation (5.19). 

$$\begin{array}{r c l}{{\dot{x}_{1}}}&{{=}}&{{x_{2}+w_{1}}}\\ {{\dot{x}_{2}}}&{{=}}&{{\rho_{0}\exp(-x_{1}/k)x_{2}^{2}/2x_{3}-g+w_{2}}}\\ {{\dot{x}_{3}}}&{{=}}&{{w_{3}}}\\ {{y}}&{{=}}&{{x_{1}+v}}\end{array}$$
$$\begin{array}{r c l}{y}&{=}&{x_{1}+v}\end{array}$$

In this example, we will use the continuous-time EKF and the hybrid EKF to estimate the altitude 21, velocity 22,and constant ballistic coefficient **1/23** of a body as it falls toward earth. A rangemeasuring device measures the altitude of the falling body. This example (or a variant thereof) is given in several places, for example IAth68, Ste94, JulOO]. The equations for this system are 

$$(13.34)$$
$$A=\frac{\partial f}{\partial x}\tag{13}$$ $$=\left[\begin{array}{ccc}0&1&0\\ A_{21}&A_{22}&A_{23}\\ 0&0&0\end{array}\right]$$ $$A_{21}=-\rho_{0}\exp(-x_{1}/k)x_{2}^{2}/2kx_{3}$$ $$A_{22}=\rho_{0}\exp(-x_{1}/k)x_{2}/x_{3}$$ $$A_{23}=-\rho_{0}\exp(-x_{1}/k)x_{2}^{2}/2x_{3}^{2}$$ $$C=H=\frac{\partial h}{\partial x}$$ $$=\left[\begin{array}{ccc}1&0&0\end{array}\right]$$

As usual, w, is the noise that affects the ith process equation, and v is the measurement noise. po is the air density at sea level, k is a constant that defines the relationship between air density and altitude, and g is the acceleration due to gravity. The partial derivative matrices for this system are given as follows: 

$$(13.35)$$

We will use the continuous-time system equations to simulate the system. **For** 
the hybrid system we suppose that we obtain range measurements every 0.5 seconds. The constants that we will use are given as 

 $0.0034\text{lb-sec}^2\text{/ft}^4\\ 32.2\text{ft/sec}^2\\ 22000\text{ft}\\ 100\text{ft}^2\\ 0\quad\text{(}i=1,2,3\text{)}$                 (13.36)
$\begin{array}{c}=\\ \\ \vdash\ =\\ \\ \ =\\ =\\ =\end{array}$  . 
$\rho_{0}$  9. 
$$\begin{array}{c}{{k}}\\ {{E[v^{2}(t)]}}\\ {{E[w_{i}^{2}(t)]}}\end{array}$$
g = 32.2 ft/sec2 
k = 22OOOft 
E[v2(t)] = 100 ft2 
The initial conditions of the system and the estimator are given as 

$$\begin{array}{r c l}{{x_{0}}}&{{=}}&{{\left[\begin{array}{c c}{{100,000}}\\ {{\hat{x}_{0}^{+}}}&{{=}}\end{array}\right.}}\\ {{}}&{{}}&{{\left[\begin{array}{c c}{{100,010}}\\ {{}}\end{array}\right.}}\\ {{}}&{{}}&{{\left[\begin{array}{c c}{{500}}\\ {{}}\end{array}\right.}}\\ {{}}&{{}}&{{=}}\end{array}\right.}}\\ {{}}&{{}}&{{}}&{{\left[\begin{array}{c c}{{0}}&{{20}}\\ {{}}\end{array}\right.}}\\ {{}}&{{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}&{{0}}\end{array}$$
$\begin{array}{cccc}00&-6,000&1/2,000&\end{array}$  $\begin{array}{cccc}10&-6,100&1/2,500&\end{array}$  $\begin{array}{cccc}0&0&\end{array}$  $\begin{array}{cccc}20,000&0&\end{array}$  $\begin{array}{cccc}0&1/250,000&\end{array}$
Po+ = 0 20,000 0 
We use rectangular integration with a step size of 0.4 msec to simulate the system, the continuoustime **EKF,** and the hybrid EKF (with a measurement time of 0.5 sec). Figure 13.3 shows estimation-error magnitudes averaged over 100 simulations for the altitude, velocity, and ballistic coefficient reciprocal of the falling body. We see that the continuoustime EKF appears to perform better in general than the hybrid EKF. This is to be expected since more measurements are incorporated in the continuoustime **EKF.** The RMS estimation errors averaged over 100 simulations was 2.8 feet for the continuous time **EKF** and 5.1 feet for the hybrid **EKF** for altitude estimation, 1.2 feet/s for the continuous-time **EKF** and 2.0 feet/s for the hybrid **EKF** for velocity estimation, and 213 for the continuoustime **EKF** and 246 for the hybrid EKF 
for the reciprocal of ballistic coefficient estimation. Of course, a continuoustime **EKF** (in analog hardware) would be more difficult to implement, tune, and modify than a hybrid **EKF** (in digital hardware). 

![12_image_0.png](12_image_0.png)

Figure **13.3** Example **13.2** altitude, velocity, and ballistic coefficient reciprocal estimation-error magnitudes of a falling body averaged over 100 simulations. The continuoustime EKF generally performs better than the hybrid EKF. 
vvv 

## 13.2.3 **The Discrete-Time Extended Kalman Filter**

In this section, we will derive the discrete-time **EKF,** which considers discretetime dynamics and discretetime measurements. This situation is often encountered in practice. Even if the underljring system dynamics are continuous time, the **EKF** 
usually needs to be implemented in a digital computer. This means that there might not be enough computational power to integrate the system dynamics as required in a continuous-time **EKF** or a hybrid EKF. So the dynamics are often discretized (see Section **1.4)** and then a discrete-time **EKF** can be used. 

Suppose we have the system model 

$$x_{k}=f_{k-1}(x_{k-1},u_{k-1},w_{k-1})$$ $$y_{k}=h_{k}(x_{k},v_{k})$$ $$w_{k}\sim(0,Q_{k})$$ $$v_{k}\sim(0,R_{k})\tag{13.38}$$

We perform a Taylor series expansion of the state equation around *zk-1* = 
and *Wk-1* = 0 to obtain the following: 

$$\tau_{k}$$
$$=f_{k-1}(\hat{x}_{k-1}^{+},u_{k-1},0)+\left.\frac{\partial f_{k-1}}{\partial x}\right|_{\hat{x}_{k-1}^{+}}(x_{k-1}-\hat{x}_{k-1}^{+})+\left.\frac{\partial f_{k-1}}{\partial w}\right|_{\hat{x}_{k-1}^{+}}$$ $$=f_{k-1}(\hat{x}_{k-1}^{+},u_{k-1},0)+F_{k-1}(x_{k-1}-\hat{x}_{k-1}^{+})+L_{k-1}w_{k-1}$$ $$=F_{k-1}x_{k-1}+\left[f_{k-1}(\hat{x}_{k-1}^{+},u_{k-1},0)-F_{k-1}\hat{x}_{k-1}^{+}\right]+L_{k-1}w_{k-1}$$ $$=F_{k-1}x_{k-1}+\tilde{u}_{k-1}+\tilde{w}_{k-1}$$
$$w_{k-1}$$
$$(13.39)$$

Fk-1 and Lk-1 are defined by the above equation. The known signal uk and the noise signal wk are defined as follows:

$$\begin{array}{r c l}{{\hat{u}_{k}}}&{{=}}&{{f_{k}(\hat{x}_{k}^{+},u_{k},0)-F_{k}\hat{x}_{k}^{+}}}\\ {{\hat{w}_{k}}}&{{\sim}}&{{(0,L_{k}Q_{k}L_{k}^{T})}}\end{array}$$
$$(13.40)$$

We linearize the measurement equation around xk = xx and vk = 0 to obtain

$$\begin{array}{l l l}{{y_{k}}}&{{=}}&{{h_{k}(\hat{x}_{k}^{-},0)+\left.{\frac{\partial h_{k}}{\partial x}}\right|_{\hat{x}_{k}^{-}}(x_{k}-\hat{x}_{k}^{-})+\left.{\frac{\partial h_{k}}{\partial v}}\right|_{\hat{x}_{k}^{-}}v_{k}}}\\ {{}}&{{=}}&{{h_{k}(\hat{x}_{k}^{-},0)+H_{k}(x_{k}-\hat{x}_{k}^{-})+M_{k}v_{k}}}\\ {{}}&{{=}}&{{H_{k}x_{k}+\left[h_{k}(\hat{x}_{k}^{-},0)-H_{k}\hat{x}_{k}^{-}\right]+M_{k}v_{k}}}\\ {{}}&{{=}}&{{H_{k}x_{k}+z_{k}+\bar{v}_{k}}}\end{array}$$
$$(13.41)$$

Hk and Mk are defined by the above equation. The known signal zk and the noise signal Ük are defined as

$$\begin{array}{r c l}{{z_{k}}}&{{=}}&{{h_{k}(\hat{x}_{k}^{-},0)-H_{k}\hat{x}_{k}^{-}}}\\ {{\bar{v}_{k}}}&{{\sim}}&{{(0,M_{k}R_{k}M_{k}^{T})}}\end{array}$$
$$(13.42)$$

We have a linear state-space system in Equation (13.39) and a linear measurement in Equation (13.41). That means we can use the standard Kalman filter equations to estimate the state. This results in the following equations for the discrete-time extended Kalman filter.

Fk-1Pk-1 + Lk-1Qk-1Qk-1Lk-1 Pk Kk P H (HKP H + MKRk Mk )-1 xx fk-1(xx-1; Uk- hk ( 2 , 0) - Hkâk Zk x âx + Kk (yk - Hkâk - 2 + Kk [yk - hk (xx , 0)] Pt (I - KkHk)Pr (13.43)
The discrete-time EKF can be summarized as follows.

$$\begin{array}{l}{{f_{k-1}(x_{k-1},u_{k-1},w_{k-1})}}\\ {{h_{k}(x_{k},v_{k})}}\\ {{(0,Q_{k})}}\\ {{(0,R_{k})}}\end{array}$$

## The Discrete-Time Extended Kalman Filter

$$\begin{array}{r l}{x_{k}}&{{}=}\\ {y_{k}}&{{}=}\\ {w_{k}}&{{}\sim}\\ {v_{k}}&{{}\sim}\end{array}$$

1. The system and measurement equations are given as follows: 

$$(13.44)$$
$$\begin{array}{r l}{{\hat{x}}_{0}^{+}}&{{}=}\\ {P_{0}^{+}}&{{}=}\end{array}$$

2. Initialize the filter as follows: 

$E(x_{0})$  $E[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}]$ (13.45)
3. For k = **1,2,** e, perform the following. 

(a) Compute the following partial derivative matrices: 

$$\begin{array}{ccccc}F_{k-1}&=&\frac{\partial f_{k-1}}{\partial x}\left|{}_{\hat{x}_{k-1}^{+}}\right.\\ L_{k-1}&=&\frac{\partial f_{k-1}}{\partial w}\left|{}_{\hat{x}_{k-1}^{+}}\right.\\ \end{array}\tag{13.46}$$
$$(13.47)$$
$$\begin{array}{r c l}{{P_{k}^{-}}}&{{=}}&{{F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+L_{k-1}Q_{k-1}L_{k-1}^{T}}}\\ {{\hat{x}_{k}^{-}}}&{{=}}&{{f_{k-1}(\hat{x}_{k-1}^{+},u_{k-1},0)}}\end{array}$$

Perform the time update of the state estimate and estimation-error covariance as follows: 

$$\begin{array}{r c l}{{H_{k}}}&{{=}}&{{\left.\frac{\partial h_{k}}{\partial x}\right|_{\hat{x}_{k}^{-}}}}\\ {{M_{k}}}&{{=}}&{{\left.\frac{\partial h_{k}}{\partial v}\right|_{\hat{x}_{k}^{-}}}}\end{array}$$

Compute the following partial derivative matrices: 

$$(13.48)$$
$$(13.49)$$
$$\begin{array}{l c l}{{\hat{K}_{k}}}&{{=}}&{{P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+M_{k}R_{k}M_{k}^{T})^{-1}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k}[y_{k}-h_{k}(\hat{x}_{k}^{-},0)]}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{(I-K_{k}H_{k})P_{k}^{-}}}\end{array}$$

Perform the measurement update of the state estimate and estimationerror covariance as follows: 
Note that other equivalent expressions can be used for Kk and *Pk+,* as is apparent from Equation (5.19). 

## 13.3 **High E R-0 Rd Er Approach Es**

More refined linearization techniques can be used to reduce the linearization error in the EKF for highly nonlinear systems. In this section, we will derive and illustrate two such approaches: the iterated EKF, and the second-order EKF. We will also briefly discuss other approaches, including Gaussian sum filters and grid filters. 

## 13.3.1

$$(13.50)$$

## The Iterated Extended Kalman Filter

In this section, we will discuss the iterated EKF. We will confine our discussion here to discretetime filtering, although the concepts can easily be extended to continuous or hybrid filters. 

When we derived the discretetime EKF in Section **13.2.3,** we approximated h(Zk, Vk) by expanding it in a Taylor series around *2;,* as shown in Equation **(13.41):** 

$$\begin{array}{r c l}{{h(x_{k},v_{k})}}&{{=}}&{{h(\hat{x}_{k}^{-},0)+\left.\frac{\partial h}{\partial x}\right|_{\hat{x}_{k}^{-}}(x_{k}-\hat{x}_{k}^{-})+\left.\frac{\partial h}{\partial v}\right|_{\hat{x}_{k}^{-}}v_{k}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{h(\hat{x}_{k}^{-},0)+H_{k}(x_{k}-\hat{x}_{k}^{-})+M_{k}v_{k}}}\end{array}$$

Based on this linearization, we then wrote the measurement-update equations as 
shown in Equation **(13.43):** 
$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{K_{k}}}&{{=}}&{{P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+M_{k}R_{k}M_{k}^{T})^{-1}}}\\ {{}}&{{}}&{{}}\\ {{P_{k}^{+}}}&{{=}}&{{(I-K_{k}H_{k})P_{k}^{-}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k}[y_{k}-h_{k}(\hat{x}_{k}^{-},0)]}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\end{array}$$
$$(13.51)$$

$$(13.52)$$
The reason that we expanded *h(Zk)* around 2; was because that was our best estimate of Xk before the measurement at time k is taken into account. But after we 
implement the discrete EKF equations to obtain the a *posteriori* estimate @, we 
have a better estimate of *Xk.* So we can reduce the linearization error by reformulating the Taylor series expansion of *h(Zk)* around our new estimate. If we then use that new Taylor series expansion of *h(Xk)* and recalculate the measurement-update 
equations, we should get a better a posteriori estimate of **2:.** But then we can 
repeat the previous step; since we have an even better estimate of *xk,* we can again reformulate the expansion of *h(Xk)* around this even better estimate to get an even 
better estimate. This process can be repeated as many times as desired, although 
for most problems the majority of the possible improvement is obtained by only relinearizing one time. 
We use the notation **2i';z,+** to refer to the *a posteriori* estimate of xk after i rehearizations have been performed. So *2k,O* is the a *posteriori* estimate that results 
from the application of the standard EKF. Likewise, we use P& to refer to the 
approximate estimation-error covariance of *2i.k+,i, Kk,+* to refer to the Kalman gain 
that is used during the ith relinearization step, and *Hk,+* to refer to the partial 
derivative matrix evaluated at the Xk = *2i.k+,i.* 
With this notation, we can describe an algorithm for the iterated EKF as follows. 
First, at each time step k we initialize the iterated EKF estimate to the standard EKF estimate: 
PC0 = Pk+ ( 13.52) 
$$\begin{array}{r c l}{{\hat{x}_{k,0}^{+}}}&{{=}}&{{\hat{x}_{k}^{+}}}\\ {{P_{k,0}^{+}}}&{{=}}&{{P_{k}^{+}}}\end{array}$$
$$(13.53)$$
Second, for i = 0, 1, . . . , N, evaluate the following equations: 

$$\begin{array}{r c l}{{H_{k,1}}}&{{=}}&{{\left.\frac{\partial h}{\partial x}\right|_{\hat{x}_{k,1}^{+}}}}\\ {{}}&{{}}&{{K_{k,1}}}&{{=}}&{{P_{k}^{-}H_{k,i}^{T}(H_{k,1}P_{k}^{-}H_{k,1}^{T}+M_{k}R_{k}M_{k}^{T})^{-1}}}\\ {{}}&{{}}&{{P_{k,1+1}^{+}}}&{{=}}&{{(I-K_{k,i}H_{k,i})P_{k}^{-}}}\\ {{\hat{x}_{k,i+1}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k,i}[y_{k}-h_{k}(\hat{x}_{k}^{-})]}}\\ {{}}&{{}}&{{}}&{{}}\end{array}$$

This is done for as many steps as desired to improve the linearization. If N = 0 then the iterated EKF reduces to the standard EKF. 

We still have to make one more modification to the above equations to obtain the iterated Kalman filter. Recall that in the derivation of the EKF, the P measurement update equation was originally derived from the following first-order Taylor series expansion of the measurement equation: 

$${\boldsymbol{y}}_{k}$$
Yk = *h(xk)* 
$$\begin{array}{r l}{={}}&{{}h(x_{k})}\\ {\approx{}}&{{}h({\hat{x}}_{k}^{-})+H|_{{\hat{x}}_{k}^{-}}\left(x_{k}-{\hat{x}}_{k}^{-}\right)}\end{array}$$

To derive the measurement-update equation for 2 we evaluated the right side at the a *priori* estimate 2i and subtracted from yk to get our correction term (the residual) : 

$$\begin{array}{r c l}{{r_{k}}}&{{=}}&{{y_{k}-h(\hat{x}_{k}^{-})-H|_{\hat{x}_{k}^{-}}(\hat{x}_{k}^{-}-\hat{x}_{k}^{-})}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{y_{k}-h(\hat{x}_{k}^{-})}}\end{array}$$
With the iterated EKF we instead want to expand the measurement equation 
around **ii,a** as follows: 
$$y_{k}\approx h(\hat{x}_{k,\imath}^{+})+H|_{\hat{x}_{k,\imath}^{+}}\left(x_{k}-\hat{x}_{k,\imath}^{+}\right)\tag{1}$$
$$(13.54)$$

To derive the iterated EKF measurement-update equation for 2, we evaluate the right side of the above equation at the a *priori* estimate 2i and subtract from Yk to get our correction term: 

$$r_{k}=y_{k}-h({\hat{x}}_{k,i}^{+})-H_{k,i}({\hat{x}}_{k}^{-}-{\hat{x}}_{k,i}^{+})$$
$$(13.55)$$
$$(13.56)$$
$$(13.57)$$

This gives the iterated EKF update equation for 2 as 

$$\hat{x}^{+}_{k,i+1}=\hat{x}^{-}_{k}+K_{k,i}[y_{k}-h(\hat{x}^{+}_{k,i})-H_{k,i}(\hat{x}^{-}_{k}-\hat{x}^{+}_{k,i})]\tag{13.58}$$
The iterated EKF can then be summarized as follows. 

## The Iterated Extended Kalman Filter

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{f_{k-1}(x_{k-1},u_{k-1},w_{k-1})}}\\ {{y_{k}}}&{{=}}&{{h_{k}(x_{k},v_{k})}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$

1. The nonlinear system and measurement equations are given as follows: 

$$(13.59)$$

2. Initialize the filter as follows. 

$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E(x_{0})}}\\ {{P_{0}^{+}}}&{{=}}&{{E\left[(x_{0}-\hat{x}_{0})(x_{0}-\hat{x}_{0})^{T}\right]}}\end{array}$$
$$(13.60)$$
$$(13.61)$$

3. For k = 1,2, . . ., do the following. 

Perform the following timeupdate equations: 

$$\begin{array}{r c l}{{P_{k}^{-}}}&{{=}}&{{F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+L_{k-1}Q_{k-1}L_{k-1}^{T}}}\\ {{\hat{x}_{k}^{-}}}&{{=}}&{{f_{k-1}(\hat{x}_{k-1}^{+},u_{k-1},0)}}\end{array}$$
$$\begin{array}{r c l}{{F_{k-1}}}&{{=}}&{{\left.\frac{\partial f_{k-1}}{\partial x}\right|_{\hat{\pi}_{k-1}^{+}}}}\\ {{}}&{{}}&{{}}\\ {{L_{k-1}}}&{{=}}&{{\left.\frac{\partial f_{k-1}}{\partial w}\right|_{\hat{\pi}_{k-1}^{+}}}}\end{array}$$

where the partial derivative matrices *Fk-1* and *Lk-1* are defined as follows: 

$$(13.62)$$

Up to this point the iterated EKF is the same as the standard discre& time EKF. 

Perform the measurement update by initializing the iterated EKF estimate to the standard EKF estimate: 

$$(13.63)$$

For i = 0,1,. . , N, evaluate the following equations (where N is the desired number of measurement-update iterations) : 

$$\begin{array}{l c l}{{\hat{x}_{k,0}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}}}\\ {{P_{k,0}^{+}}}&{{=}}&{{P_{k}^{-}}}\end{array}$$
Hk,a = ax &t>% 
The final *a posteriori* state estimate and estimation-error covariance are given as follows: 

$$\begin{array}{l c l}{{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k,N+1}^{+}}}\\ {{P_{k}^{+}}}&{{=}}&{{P_{k,N+1}^{+}}}\end{array}\qquad\qquad(13.65)$$

An illustration of the iterated EKF will be presented in Example 13.3. 

## 13.3.2 The Second-Order Extended Kalman Filter

The second-order EKF is similar to the iterated **EKF** in that it attempts to reduce the linearization error of the **EKF.** In the iterated EKF of the previous section, we refined the point at which we performed a first-order Taylor series expansion of the measurement equation *h(.).* In the second-order EKF we instead perform a *seconh* order Taylor series expansion of f (.) and *h(.).* The second-order **EKF** presented in this section is based on [Ath68, Ge1741. 

In this section, we will consider the hybrid system with continuous-time system dynamics and discretetime measurements: 

$$\dot{x}=f(x,u,w,t)$$ $$y_{k}=h(x_{k},t_{k})+v_{k}$$ $$w(t)\sim(0,Q)$$ $$v_{k}\sim(0,R_{k})\tag{13.66}$$

In the standard EKF, we expanded *f (5,* u, w, t) using a first-order Taylor series. In this section, we will consider only the expansion around a nominal x, ignoring the expansion around nominal u and w values. This is done so that we can present the main ideas of the second-order EKF without getting too bogged down in notation. 

The development in this section can be easily extended to second-order expansions around u and w once the main idea is understood. 

The first-order expansion of f (z, u, w, t) around z = 2 is given as 

$$f(x,u,w,t)=f({\hat{x}},u_{0},w_{0},t)+\left.{\frac{\partial f}{\partial x}}\right|_{{\hat{x}}}(x-{\hat{x}})$$
$$(13.67)$$
$$(13.68)$$
$${\mathfrak{J}}{\mathfrak{0}},t)$$

In the standard **EKF,** we evaluated this expression at 2 = 2 to obtain our timeupdate equation for 2 as i = f **(2,** ug, *wo,* t) **(13.68)** 
In the second-order **EKF** we expand f (5, u, w, t) with an additional term in the Taylor series: 

$$f(x,u,w,t)=f(\hat{x},u_{0},w_{0},t)+\frac{\partial f}{\partial x}\bigg{|}_{\hat{x}}\left(x-\hat{x}\right)+\frac{1}{2}\sum_{i=1}^{n}\phi_{i}(x-\hat{x})^{T}\left.\frac{\partial^{2}f_{i}}{\partial x^{2}}\right|_{\hat{x}}\left(x-\hat{x}\right)\tag{13.69}$$

where n is the dimension of the state vector, fi is the ith element of f(z, u, w, *t),* 
and the 4i vector is defined as an n x 1 vector with all zeros except for a one in the ith element. The quadratic term in the summation can be written as 

$$(x-{\hat{x}})^{T}\left.{\frac{\partial^{2}f_{\mathrm{t}}}{\partial x^{2}}}\right|_{{\hat{x}}}(x-{\hat{x}})=\mathrm{Tr}\left[\left.{\frac{\partial^{2}f_{\mathrm{t}}}{\partial x^{2}}}\right|_{{\hat{x}}}(x-{\hat{x}})(x-{\hat{x}})^{T}\right]$$
- 
$$(13.70)$$
$$(x-{\hat{x}})^{T}\left.{\frac{\partial^{2}f_{t}}{\partial x^{2}}}\right|_{{\hat{x}}}(x-{\hat{x}})\approx\mathrm{Tr}\left[\left.{\frac{\partial^{2}f_{t}}{\partial x^{2}}}\right|_{{\hat{x}}}P\right]$$

Since we do not know the value of (z -2)(z *-2)T* in the above equation, we replace it with its expected value, which is the covariance of the Kalman filter, to obtain 

$$(13.71)$$
$${\dot{\hat{x}}}=f({\hat{x}},u_{0},w_{0},t)+{\frac{1}{2}}\sum_{i=1}^{n}\phi_{i}\mathrm{Tr}\left[\left.{\frac{\partial^{2}f_{i}}{\partial x^{2}}}\right|_{{\hat{x}}}P\right]$$

We then evaluate Equation **(13.69)** at z = 2 and substitute the above expression in the summation to obtain the timeupdate equation for 2 as 

$$(13.72)$$
$$(13.73)$$

The timeupdate equation for P remains the same as in the standard hybrid EKF 
as shown in Equation **(13.28):** 

$${\dot{P}}=F P+P F^{T}+L Q L^{T}$$
P=FP+PF~+LQL~ **(13.73)** 
Now we will derive the measurement-update equations. Suppose that the measurementupdate equation for the state estimate is given as 

$$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K_{k}\left[y_{k}-h(\hat{x}_{k}^{-},t_{k})\right]-\pi_{k}$$

where Kk is the Kalman gain to be determined, and Tk is a correction term to be determined. We will choose *Irk* so that the estimate 2: is unbiased, and we will then choose Kk to minimize the trace of the covariance of the estimate. 

If we define the estimation errors as 

$$(13.74)$$
$$(13.75)$$
$$(13.76)$$

we can see from Equations (13.66) and **(13.74)** that 

$$\begin{array}{r c l}{{e_{k}^{-}}}&{{=}}&{{x_{k}-\hat{x}_{k}^{-}}}\\ {{e_{k}^{+}}}&{{=}}&{{x_{k}-\hat{x}_{k}^{+}}}\end{array}$$
$$e_{k}^{+}=e_{k}^{-}-K_{k}\left[h(x_{k},t_{k})-h(\hat{x}_{k}^{-},t_{k})\right]-K_{k}v_{k}+\pi_{k}$$
el = ei - Kk [h(zk,tk) - h(?i,tk)] - *KkVk* -k rk **(13.76)** 
Now we perform a second-order Taylor series expansion of *h(zk,tk)* around the nominal point 2; to obtain 

(13.77) 
where Hk is defined by the above equation, m is the dimension of the measurement vector, and h, is the ith element of *h(zk, tk).* This gives the a *posteriori* estimation error as 

$$e_{k}^{+}=e_{k}^{-}-K_{k}H_{k}e_{k}^{-}-\frac{1}{2}K_{k}\sum_{i=1}^{m}\phi_{i}(e_{k}^{-})^{T}D_{k,i}e_{k}^{-}-K_{k}v_{k}+\pi_{k}$$
$$D_{k,i}=\left.{\frac{\partial^{2}h_{i}}{\partial x^{2}}}\right|_{\hat{x}_{k}^{-}}$$

where *Dk,%* is defined as 

$$(13.78)$$
$$(13.79)$$. 
$$(13.81)$$

Taking the expected value of both sides of Equation **(13.78),** assuming that *E(e;)* = 
0, and making the same approximation as in Equation **(13.71),** we can see that in order to have *E(et)* = 0 we must set 

$$\pi_{k}=\frac{1}{2}K_{k}\sum_{i=1}^{m}\phi_{i}\mathrm{Tr}\left[D_{k,i}P_{k}^{-}\right]$$
$$P_{k}^{+}=E\left[e_{k}^{+}(e_{k}^{+})^{T}\right]$$
$$(13.80)$$
Defining P$ as 
p$ = [ek + *(ek* +T ] **(13.81)** 
and using the above equations, it can be shown after some involved algebraic calculations [Ath68] that 

$$P_{k}^{+}=(I-K_{k}H_{k})P_{k}^{-}(I-K_{k}H_{k})^{T}+K_{k}(R_{k}+\Lambda_{k})K_{k}^{T}$$
$$\Lambda_{k}=\frac{1}{4}E\left\{\left[\sum_{i=1}^{m}\phi_{i}\mathrm{Tr}[D_{k,i}(e_{k}^{-}(e_{k}^{-})^{T}-P_{k}^{-})]\right]\left[\cdots\right]^{T}\right\}$$

where the matrix Ak is defined as Now we define a cost function Jk that we want to minimize as a weighted sum of estimation errors: 

$$(13.82)$$
$$(13.83)$$
$$(13.84)$$
$$(13.85)$$

where Sk is any positive definition weighting matrix. The Kk that minimizes this cost function can be found as 

$$\begin{array}{r c l}{{J_{k}}}&{{=}}&{{E[(e_{k}^{+})^{T}S_{k}e_{k}^{+}]}}\\ {{}}&{{=}}&{{\mathrm{Tr}[S_{k}P_{k}^{+}]}}\end{array}$$
$$K_{k}=P_{k}^{-}H_{k}^{T}\left(H_{k}P_{k}^{-}H_{k}^{T}+R_{k}+\Lambda_{k}\right)^{-1}$$

This gives the Pz matrix from Equation **(13.82)** as 

$$P_{k}^{+}=P_{k}^{-}-P_{k}^{-}H_{k}^{T}\left(H_{k}P_{k}^{-}H_{k}^{T}+R_{k}+\Lambda_{k}\right)^{-1}H_{k}P_{k}^{-}$$

Now we need to figure out how to evaluate the A, ,matrix in Equation **(13.83).** Note that Ak can be written as the double summation 

$$(13.86)$$
$$\Lambda_{k}=\frac{1}{4}E\left\{\sum_{i,j=1}^{m}\phi_{i}\phi_{j}^{T}\mathrm{Tr}\left[D_{k,i}(e_{k}^{-}(e_{k}^{-})^{T}-P_{k}^{-})\right]\mathrm{Tr}\left[D_{k,j}(e_{k}^{-}(e_{k}^{-})^{T}-P_{k}^{-})\right]\right\}\tag{13.87}$$  The product $\phi_{i}\phi_{j}^{T}$ is an $m\times m$ matrix whose elements are all zero except for the 
$$\Lambda_{k}(i,j)=\frac{1}{4}E\left\{\mbox{Tr}\left[D_{k,i}(e_{k}^{-}(e_{k}^{-})^{T}-P_{k}^{-})\right]\mbox{Tr}\left[D_{k,j}(e_{k}^{-}(e_{k}^{-})^{T}-P_{k}^{-})\right]\right\}\tag{13.88}$$

element in the zth row and jth column. Therefore, the element in the ith row and jth column of Ak can be written as This expression can be evaluated with the following lemma [Ath68]. 

Lemma 6 Suppose we have the n-element random vector x N **N(0,** P). Then 

$$\begin{array}{rcl}E\left[x\,Tr(Axx^{T})\right]&=&0\\ E\left[\,Tr(Axx^{T}Bxx^{T})\right]&=&E\left[\,Tr(Axx^{T})\,Tr(Bxx^{T})\right]\\ &=&2\,Tr(APBP)+\,Tr(AP)\,Tr(BP)\end{array}$$

where A and B are arbitrarg n x *n matrices.* 
Using this lemma with Equation (13.88) we can see that 

$$(13.89)$$
$$(13.90)$$

This equation, along with Equations (13.74), (13.80), (13.82), and (13.85), specify the measurement-update equations **for** the second-order EKF. The second-order EKF can be summarized as follows. 

$$\Lambda_{k}(i,j)=\frac{1}{2}\mathrm{Tr}(D_{k,i}P_{k}^{-}D_{k,j}P_{k}^{-})$$

## The Second-Order Hybrid Extended Kalrnan Filter

1. The system equations are given as follows: 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f(x,u,w,t)}}\\ {{y_{k}}}&{{=}}&{{h(x_{k},t_{k})+v_{k}}}\\ {{w(t)}}&{{\sim}}&{{(0,Q)}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E(x_{0})}}\\ {{P_{0}^{+}}}&{{=}}&{{E\left[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}\right]}}\end{array}$$
$$(13.91)$$

2. The estimator is initialized as follows: 

$$(13.92)$$

3. The timeupdate equations are given as 

 The equations are given as  $\begin{array}{rcl}\dot{\vec{x}}&=&f(\dot{x},u,0,t)+\dfrac{1}{2}\sum\limits_{i=1}^n\phi_i\text{Tr}\left[\left.\dfrac{\partial^2f_i}{\partial x^2}\right|_{\dot{x}}P\right]\\ \dot{P}&=&FP+PF^T+LQL^T\\ &&\left[\begin{array}{c}0\\ \vdots\\ 0\\ 1\\ 0\end{array}\right]\gets i\text{th element}\\ F&=&\left.\dfrac{\partial f}{\partial x}\right|_{\dot{x}}\\ L&=&\left.\dfrac{\partial f}{\partial w}\right|_{\dot{x}}\end{array}$. 
$$(13.93)$$
$\frac{1}{2}$ 2. 

4. The measurement update equations are given as Note that setting the second partial derivative matrices in this algorithm to zero matrices results in the standard hybrid EKF. 

In this example, we compare the performance of the EKF, the second-order EKF, and the iterated EKF for the falling body problem described in Example 13.2. A similar comparison was shown in [Wis69], where it was concluded that the iterated EKF had better RMS error performance, but the secondorder filter had smaller bias. The system equations are the same as those shown in Example 13.2: 

$$\dot{x}_{1}=x_{2}+w_{1}$$ $$\dot{x}_{2}=\rho_{0}\exp(-x_{1}/k)x_{2}^{2}x_{3}/2-g+w_{2}$$ $$\dot{x}_{3}=w_{3}\tag{13.95}$$

In this example, we change the measurement system so that it does not measure the altitude of the falling body, but instead measures the range to the measuring device. The measuring device is Iocated at an altitude a and at a horizontal distance M from the body's vertical line of fall. The measurement equation is therefore given by 

$$=\sqrt{M^{2}+(x_{1}(t_{k})-a)^{2}}+v_{k}\tag{13.96}$$ $$=h(x_{k})+v_{k}$$

This makes the problem more nonlinear and hence more difficult to estimate 
(i.e., in Example 13.2 we had a nonlinear system but a linear measurement, whereas in this example we have nonlinearities in both the system and the measurement equations). The partial derivative F matrix for the EKFs are given in Example 13.2. The other partial derivative matrices used in the second-order EKF are given as follows: 

L=  -  dh  ax  [ (Xl - a)(M2 + (XI - a)2)-1/2  af  dW  H=  -  0 0 ]  -  [s 8 H] -  d2hl  h-yl - (21 - a)2h-2) 0 0  0 i' 0  00  ( 13.97)  x$x3/2k2 -~2~3/k -~,2/2k  -~$/2k 22 x2 0 1  -xzz3/k 23  Table 13.2 shows the performances of the EKFs (averaged over 20 simulation 
runs). It is seen that second-order EKF provides significant improvement over the first-order EKF for altitude and velocity estimation, but for some reason it actually provides worse performance for ballistic coefficient estimation. Also note that the iterated EKF provides only slight improvement over the firstorder EKF, and (as expected) the iterated EKF performs better when more iterations are executed for the linearization refinement. 

Table 13.2 different EKF approaches for tracking a falling body. 

Example **13.3** results. A comparison of the estimation errors of 

|                      |          | ~            | ~~~                   |
|----------------------|----------|--------------|-----------------------|
| Filter               | Altitude | Velocity     | Ballistic Coefficient |
| First-order EKF      | 758 feet | 518 feet/sec | 0.091 feet3/lb/sec2   |
| Second-order EKF     | 356      | 483          | 0.129                 |
| Iterated EKF (N = 2) | 755      | 517          | 0.091                 |
| Iterated EKF (N = 3) | 745      | 516          | 0.091                 |
| Iterated EKF (N = 4) | 738      | 509          | 0.091                 |
| Iterated EKF (N = 5) | 733      | 506          | 0.091                 |
| Iterated EKF (N = 6) | 723      | 506          | 0.091                 |

We conclude from this that the second-order filter has better estimation performance. However, the implementation is much more difficult and requires the computation of second-order derivatives. In this example, the second-order derivatives could be taken analytically because we have explicit analytical system and measurement equations. In many applications secondorder derivatives will not be available analytically, and approximations will inevitably be subject to error. 

These results are different than reported in [Wis69], where it was shown that the iterated EKF performed better than the second-order EKF. The different conclusions between this book and [Wis69] show that comparisons between different algorithms are often subjective. Perhaps the discrepancies are due to differences in implementations of the filtering algorithms, differences in implementations of the system dynamics or random noise generation, differences in the way that the estimation errors were measured, or even differences in the computing platforms that were used. 

vvv The second-order filter was initially developed by Bass [Bas661 and Jazwinski [Jaz66]. A Gaussian second-order filter was developed by Athans [Ath68] and Jazwinski [ Jaz701, in which fourth-order terms in Taylor series approximations are retained and approximated by assuming that the underlying probabilities are Gaussian. A small correction in the original derivations of the second-order EKF was reported by Rolf Henriksen [Hen82]. Although the second-order filter often provides improved performance over the extended Kalman filter, nothing definitive can be said about its performance, as evidenced by an example of an unstable second-order filter reported in [Kus67]. Additional comparison and analysis of some nonlinear Kalman filters can be found in [Sch68, Wis69, Wis70, Net781. A simplified version of Henriksen's discretetime second-order filter can be summarized as follows. 

## The Second-Order Discretetime Extended Kalman Filter

$$\begin{array}{r l}{={}}&{{}f(x_{k},u_{k},k)+w_{k}}\\ {={}}&{{}h(x_{k},k)+v_{k}}\\ {\sim{}}&{{}(0,Q_{k})}\\ {\sim{}}&{{}(0,R_{k})}\end{array}$$
$$x_{k+1}$$
$$\begin{array}{c}{{y_{k}}}\\ {{w_{k}}}\\ {{v_{k}}}\end{array}$$

1. The system equations are given as follows: 

$$(13.98)$$

2. The estimator is initialized as follows: 

$$\hat{x}_{0}^{+}=E(x_{0})$$ $$P_{0}^{+}=E\left[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}\right]\tag{13.99}$$

3. The time update equations are given as follows: 

$$\begin{array}{r c l}{{\hat{x}_{k+1}^{-}}}&{{=}}&{{f(\hat{x}_{k}^{+},u_{k},k)+\frac{1}{2}\sum_{i=1}^{n}\phi_{i}\mathrm{Tr}\left[\left.\frac{\partial^{2}f_{i}}{\partial x}\right|_{\hat{x}_{k}^{+}}P_{k}^{+}\right]}}\\ {{P_{k+1}^{-}}}&{{=}}&{{F P_{k}^{+}F^{T}+Q_{k}}}\end{array}$$

![25_image_0.png](25_image_0.png)

$$(13.100)$$

4. The measurement update equations are given as follows: 
A more general version of the above algorithm can be found in [Hen82]. Similar to the hybrid second-order EKF presented earlier in this section, we note that setting the second-order partial derivative matrices in this algorithm to zero matrices results in the standard discretetime EKF. 

## 13.3.3 Other Approaches

We have considered a couple of higher-order approaches to reducing the linearization error of the EKF. We looked at the iterated EKF and the second-order EKF, 
but other approaches are also available. For example, Gaussian sum filters are based on the idea that a non-Gaussian pdf can be approximated by a sum of Gaussian pdfs. This is similar to the idea that any curve can be approximated by a piecewise constant function. Since the true pdf of the process noise and measurement noise can be approximated by a sum of M Gaussian pdfs, we can run M Kalman filters in parallel on M Gaussian filtering problems, each of them optimal filters, and then combine them to obtain an approximately optimal estimate. The number of filters M is a trade-off between approximation accuracy (and hence optimality) and computational effort. This idea was first mentioned in [Aok65] and was explored in [Cam68, Sor7lb, Als74, Kit891. The Gaussian sum filter algorithm presented in [Ah721 can be summarized as follows. 

$$(13.102)$$
$$(13.103)$$

## The Gaussian Sum **Filter**

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{f_{k-1}(x_{k-1},u_{k-1},w_{k-1})}}\\ {{y_{k}}}&{{=}}&{{h_{k}(x_{k},v_{k})}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$

1. The discrete-time n-state system and measurement equations are given as follows: 
2. Initialize the filter by approximating the pdf of the initial state as follows: 

$$\mathrm{pdf}({\hat{x}}_{0}^{+})=\sum_{i=1}^{M}a_{0i}N({\hat{x}}_{0i}^{+},P_{0i}^{+})$$

The *a,-,%* coefficients (which are positive and add up to l), the **2i.,$,** means, and the PL covariances, are chosen by the user to provide a good approximation to the pdf of the initial state. 

3. For k = 1,2,. . ., do the following. 

$$\begin{array}{r c l}{{\hat{x}_{k i}^{-}}}&{{=}}&{{f_{k-1}(\hat{x}_{k-1,i}^{+},u_{k-1,0})}}\\ {{F_{k-1,i}}}&{{=}}&{{\left.\frac{\partial f_{k-1}}{\partial x_{k-1}}\right|_{\hat{x}_{k-1,i}^{+}}}}\\ {{}}&{{}}&{{P_{k i}^{-}}}&{{=}}&{{F_{k-1,i}P_{k-1,i}^{+}F_{k-1,i}^{T}+Q_{k-1,i}}}\\ {{}}&{{}}&{{a_{k i}}}&{{=}}&{{a_{k-1,i}}}\end{array}$$

(a) The a *priori* state estimate is obtained by first executing the following time-update equations for i = 1, . , M: 
The pdf of the a *priori* state estimate is obtained by the following sum: 

$$(13.104)$$
$\mathrm{pdf}(\hat{x}_{k}^{-})=\sum_{i=1}^{M}a_{k_{1}}N(\hat{x}_{k_{1}}^{-},P_{k_{1}}^{-})$ (13.105)
(b) The a *posteriori* state estimate is obtained by first executing the following measurement update equations for i = 1, - . . , M: 

$$H_{k_{1}}=\frac{\partial h_{k}}{\partial x_{k}}\bigg{|}_{\hat{x}_{k}}$$ $$K_{k_{1}}=P_{k_{1}}^{-}H_{ki}^{T}(H_{k_{1}}P_{k_{1}}^{-}H_{k_{1}}^{T}+R_{k})^{-1}$$ $$P_{k_{1}}^{+}=P_{k_{1}}^{-}-K_{k_{1}}H_{k_{1}}P_{k_{1}}^{-}$$ $$\hat{x}_{k_{1}}^{+}=\hat{x}_{k_{1}}^{-}+K_{k_{1}}\left[y_{k}-h_{k}(\hat{x}_{k_{1}}^{-},0)\right]\tag{13.106}$$  coefficients $\alpha$ for the individual estimates are obtained.  
The weighting coefficients *akz* for the individual estimates are obtained as follows: 

$$r_{k1}=y_{k}-h_{k}(\hat{x}_{k1}^{-},0)$$ $$S_{k1}=H_{k1}P_{k1}^{-}H_{k1}^{T}+R_{k}$$ $$\beta_{k1}=\frac{\exp\left[-r_{k1}^{T}S_{k2}^{-1}r_{k1}/2\right]}{(2\pi)^{n/2}|S_{k1}|^{1/2}}$$ $$a_{k1}=\frac{a_{k-1,i}\beta_{k1}}{\sum_{j=1}^{M}a_{k-1,j}\beta_{kj}}\tag{13.107}$$

Note that the weighting coefficient *aka* is computed by using the me& surement yk to obtain the relative confidence *Pkz* of the estimate *2ii.* The pdf of the a *posteriori* state estimate is obtained by the following sum: 

$$\mathrm{pdf}(\hat{x}_{k}^{+})=\sum_{i=1}^{M}a_{ki}N(\hat{x}_{ki}^{+},P_{ki}^{+})\tag{13.108}$$

This approach can also be extended to smoothing [Kit94]. Similar approaches can be taken to expand the pdf using non-Gaussian functions [Aok67, Sor68, Sri70, deF71, Hec71, Hec73, Mcr75, Wi181, Kit87, Kra881. A related filter has been derived for the case where either the process noise or the measurement noise is strictly Gaussian, but the other noise is Gaussian with heavy tails [Mas75, Tsa831. This is motivated by the observation that many instances of noise in nature have pdfs that are approximately Gaussian but with heavier tails [Mas77]. 

Another approach to nonlinear filtering is called grid-based filtering. In gridbased filtering, the value of the pdf of the state is approximated, stored, propagated, and updated at discrete points in state space [Buc69, Buc711; [Spa88, Chapter 61. This is similar to particle filtering (discussed in Chapter 15), except in particle filtering we choose the particles to be distributed in state space according to the pdf of the state. Grid-based filtering does not distribute the particles in this way, and hence has computational requirements that increase exponentially with the dimension of the state. Grid-based filtering is even more computationally expensive than particle filtering, and this has limited its application. Furthermore, particle filtering is a type of "intelligent" grid-based filtering. This seems to portend very little further work in grid-based filtering. 

Richard Bucy suggested yet another approach to nonlinear filtering [Buc65]. Instead of linearizing the system dynamics, compute the theoretically optimal nonlinear filter, and then linearize the nonlinear filter. However, the theoretically optimal nonlinear filter is very difficult to compute except in special cases. 

## 13.4 Parameter Estimation

State estimation theory can be used to not only estimate the states of a system, but also to estimate the unknown parameters of a system. This may have first been suggested in [Kop63]. Suppose that we have a discretetime system model, but the system matrices depend in a nonlinear way on an unknown parameter vector p: 

$$(13.109)$$
$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F_{k}(p)x_{k}+G_{k}(p)u_{k}+L_{k}(p)w_{k}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{p}}&{{=}}&{{\mathrm{unknown~parameter~vector}}}\end{array}$$

In this model, we are assuming that the measurement is independent of p, but this is only for notational convenience. The discussion here can easily be extended to include a dependence of Yk on p. Assume that p is a constant parameter vector. 

We do not really care about estimating the state, but we are interested in estimating p. This is the case, for example, in the aircraft engine health estimation problem [KobOS, Sim05aI. In those papers it was assumed that we want to estimate aircraft engine health (for the purpose of maintenance scheduling), but we do not really care about estimating the states of the engine. 

In order to estimate the parameter p, we first augment the state with the parameter to obtain an augmented state vector *x':* 

$\mathbf{x}_{k}^{\prime}=\left[\begin{array}{c}\mathbf{x}_{k}\\ \mathbf{p}_{k}\end{array}\right]$ (13.110)
If pk is constant then we model pk+l = *pk+Wpk,* where *Wpk* is a small artificial noise term that allows the Kalman filter to change its estimate of *pk.* Our augmented system model can be written as 

$$x^{\prime}_{k+1}=\left[\begin{array}{c}F_{k}(p_{k})x_{k}+G_{k}(p_{k})u_{k}+L_{k}(p_{k})w_{k}\\ p_{k}+w_{pk}\end{array}\right]\tag{13.111}$$ $$=f(x^{\prime}_{k},u_{k},w_{k},w_{pk})$$ $$y_{k}=\left[\begin{array}{cc}H_{k}&0\end{array}\right]\left[\begin{array}{c}x_{k}\\ p_{k}\end{array}\right]+v_{k}$$
$$(13.111)$$
$$(13.112)$$

Note that !(xi, *Uk, Wk, Wpk)* is a nonlinear function of the augmented state *xi.* We can therefore use an extended Kalman filter (or any other nonlinear filter) to estimate *xi.* 

This example is taken from [Ste94]. Suppose we have a second-order system governed by the following equations: 

$$\ddot{x}_{1}+2\zeta\omega_{n}\dot{x}_{1}+\omega_{n}^{2}x_{1}=\omega_{n}^{2}w$$

where w, is the natural frequency of the system, < is the damping ratio, and the input w is zero-mean noise. A statespace model for this system can be written as 

$$\dot{x}_{1}=x_{2}$$ $$\dot{x}_{2}=-\omega_{n}^{2}x_{1}-2\zeta\omega_{n}x_{2}+\omega_{n}^{2}w$$ $$\left[\begin{array}{c}\dot{x}_{1}\\ \dot{x}_{2}\end{array}\right]=\left[\begin{array}{cc}0&1\\ -\omega_{n}^{2}&-2\zeta\omega_{n}\end{array}\right]\left[\begin{array}{c}x_{1}\\ x_{2}\end{array}\right]+\left[\begin{array}{c}0\\ \omega_{n}^{2}\end{array}\right]w\tag{13.113}$$

Suppose that *-2<wn* is known, but 6 and wn are unknown. We want to estimate *-wt.* Suppose that both 21 and 22 are available for measurement. 

We define the known parameter as b; that is, b = *-2Cwn.* We define a new state element equal to the parameter that we want to estimate. That is, 53 = -wf. We then form an augmented system model as follows: 

$$\dot{x}^{\prime}=\left[\begin{array}{c}x_{2}\\ x_{3}x_{1}+b\!x_{2}-x_{3}w\\ w_{p}\end{array}\right]\tag{13.114}$$ $$=f(x^{\prime},w^{\prime})$$ $$w^{\prime}=\left[\begin{array}{c}w\\ w_{p}\end{array}\right]$$ $$y=\left[\begin{array}{ccc}1&0&0\\ 0&1&0\end{array}\right]x^{\prime}+v$$

where wp is an artificial noise term that we add to the system that allows the Kalman filter to modify its estimate of **23.** We can use an extended Kalman filter to estimate the augmented state. First we need to find the partial derivative matrices: 

$$F=\frac{\partial f}{\partial x^{\prime}}\bigg{|}_{\hat{x}^{\prime},w^{\prime}_{0}}$$ $$=\left[\begin{array}{ccc}0&1&0\\ x_{3}&b&x_{1}-w\\ 0&0&0\end{array}\right]_{\hat{x}^{\prime},w^{\prime}_{0}}$$ $$=\left[\begin{array}{ccc}0&1&0\\ \hat{x}_{3}&b&\hat{x}_{1}\\ 0&0&0\end{array}\right]$$ $$L=\frac{\partial f}{\partial w^{\prime}}\bigg{|}_{\hat{x}^{\prime},w^{\prime}_{0}}$$ $$=\left[\begin{array}{ccc}0&0\\ -\hat{x}_{3}&0\\ 0&1\end{array}\right]$$
$$(13.115)$$
$$(13.116)$$

The continuous-time extended Kalman filter can be written as 

$$\begin{array}{r c l}{{\dot{\hat{x}}^{\prime}}}&{{=}}&{{f(\hat{x}^{\prime},0)+K(y-H\hat{x}^{\prime})}}\\ {{K}}&{{=}}&{{P H^{T}R^{-1}}}\\ {{\dot{P}}}&{{=}}&{{F P+P F^{T}+L Q L^{T}-P H^{T}R^{-1}H P}}\end{array}$$

Figure **13.4** illustrates the results of a typical simulation of the extended Kalman filter that is used to estimate -wi for this system. The true system parameters are wn = 2 and 6 = **0.1,** so *-wt* = **-4.** Suppose that we begin by estimating *-w:* as -8 with an initial estimation variance of 20. Figure **13.4** 
shows that the error in our estimate of *-w:* gradually decreases toward zero, and the estimation variance gradually decreases. We set the variance of the artificial noise wp equal to **0.1** in this example. This allows the Kalman filter 

I: 0 1 0 20 40 **60 80** 100 

![30_image_0.png](30_image_0.png)

Figure **13.4** Example **13.4** results. Typical parameter estimation performance and parameter uncertainty for an extended Kalman filter estimating *-uK* for a second-order system. The estimation error of the unknown parameter and its variance gradually decrease toward zero. 
to more readily adjust its estimate of *-wi,* but also may prevent the filter from converging to the true value (see Problem 13.23). 

vvv 

## 13.5 Summary

Optimal state estimators can be derived for general classes of nonlinear systems as shown in [Kus67], but the filters are generally infinite dimensional, which makes them impractical for implementation. Finite-dimensional, optimal, nonlinear state estimators can be derived for more restricted classes of nonlinear systems [Liu80], 
but the restriction on the classes of applicable systems are significant enough to prevent wide applicability. Because of these factors, nonlinear Kalman filtering is the most widespread approach to state estimation for nonlinear systems. 

It is interesting to note that the first applications of Kalman filtering were on nonlinear orbit-estimation problems [Bat62]. Some early investigations in nonlinear Kalman filtering can be found in [Cox64, Fri661. Whereas stability and convergence results are readily available **for** the linear Kalman filter, such results are much more difficult to obtain for nonlinear Kalman filtering. Some convergence results for nonlinear Kalman filtering are found in [Urs80]. If the nonlinearities have known bounds then the Riccati equation can be modified in a simple way to guarantee stability for the continuous-time EKF [Rei98]. Conditions needed to guarantee the boundedness of the discrete-time EKF error covariance can be related to the observability of the underlying nonlinear system [Dez92, Son951. 

## Problems

Written exercises 13.1 Consider the scalar system 

$${\dot{x}}\ \ =\ _{,}-x+w$$
$$\begin{array}{r c l}{y}&{=}&{x+v}\end{array}$$

The process noise has a mean value of 2, and the measurement noise has a mean value of 3. Redefine the noise quantities and the state to obtain an equivalent system of the form 

$$\begin{array}{r c l}{{\dot{x}^{\prime}}}&{{=}}&{{A x^{\prime}+B u+w^{\prime}}}\\ {{y}}&{{=}}&{{C x^{\prime}+v^{\prime}}}\end{array}$$

so that the new noise quantities w' and v' both have mean values of 0. 

13.2 Consider the scalar system X=-x+u+w w is zero-mean process noise with a variance of Q. The control has a mean value of *UO,* an uncertainty of 2 (one standard deviation), and is uncorrelated with w. Rewrite the system equations to obtain an equivalent system with a normalized control that is perfectly known. What is the variance of the new process noise term in the transformed system equation? 

13.3 Suppose that x is a constant scalar, and yk = fi(1 + *Vk)* are noisy measurements, where Vk N *N(0, R).* 
a) An intuitive way to estimate x is to set zk = y:. Compute the mean and variance of the estimation error for this estimate. Your answer should be a function of x and R. Hint: recall that *E(vi)* = 0 and E(vi) = *3R2.* 
b) Perhaps a better estimate for Xk could be obtained by averaging all previous values of y:. That is, 

$${\hat{x}}_{k}={\frac{1}{k}}\sum_{i=1}^{k}y_{i}^{2}$$

Compute the mean and variance of the estimation error for this estimate. 

Your answer should be a function of k, x, *and* R. Note that if you substitute k = 1 into your solution, you should get the same answer as part (a). 

What is the variance as k + *cm?* 
c) Write the extended Kalman filter equations to estimate x. What is the theoretical mean and variance of the EKF estimate as k -+ *cm?* 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}^{2}}}\end{array}$$

13.4 Consider the system where Wk and Wk are uniformly distributed, uncorrelated, zero-mean white noise processes with variances Q and R, respectively. 

a) What is the mean of the a *posteriori* estimation error for the discrete EKF? 

b) Modify the measurement equation by subtracting the known bias of the measurement noise so that the modified measurement noise is zero-mean. 

What is the variance of the modified measurement noise? 

13.5 Consider the nonlinear system Find the nominal values for Xk *and* Yk when 20 = 0 and Uk = 1. 

13.6 + *Wk,* where Wk is zero-mean. The initial state 20 is uniformly distributed between 0 and 1. An EKF is initialized with 3;'; = *E(z0).* What is *E(zl)?* What is **3;';?** This problem illustrates the fact that the state estimate of an EKF is not always equal to the expected value of the state. 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{-x_{k}^{2}+u_{k}+w_{k}}}\\ {{}}&{{y_{k}}}&{{=}}&{{4x_{k}^{2}+v_{k}}}\end{array}$$

Consider the system *2k+1* = 
13.7 Find the terminal velocity of the falling body of Example **13.2** if the terminal velocity occurs at an altitude of 1 mile. 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f(x)+w,\;\;\;\;\;w\sim N(0,Q)}}\\ {{y_{k}}}&{{=}}&{{h(x_{k})+v_{k},\;\;\;\;\;v_{k}\sim N(0,R)}}\end{array}$$

13.8 Consider the hybrid scalar system The estimator that is used for the system is Suppose that the state *~(t)* is normally distributed with a mean of zero and a variance of *P,.* 
a) Find an equation relating a, b, and c that must be satisfied in order for & 
to be an unbiased estimate of *2(tk)* [Ge174]. 

b) Find values of a, b, and c so that & is the minimum-variance estimate. 

Assume that h(z) is an odd function of z. 

13.9 Suppose for a scalar system that Pc = 1, R = 1, and H = 3. What is the value of Pkf as given by Equation **(5.19)?** What will be the computed value of Pkf if H = 2 is used instead? What will be the computed value of *Pk+* if H = 1 is used instead? This illustrates how the iterated Kalman filter gets a more accurate estimate of P: by using a more accurate value for *Hk.* 
13.10 Consider a system with the measurement equation Yk = xi f *Wk.* At time k the a *priori* state estimate is **3;';** = 1, the true state is zk = 5, and the measurement is Yk = **25.** The a *priori* estimation-error variance is P; = 1, and the measurement noise variance is Rk = 4. **Use** the iterated EKF algorithm to find *2z,l* and **3;'12.** 
Although the iterated EKF does not always improve the a *posteriori* state estimate, this problem illustrates how it usually does. 

13.11 Prove Lemma 6 for scalar random variables z. 

13.12 Suppose you have the process equation x = x2 + w and the state estimate 2: = 0. What is the differential equation for propagating 2 to the next measurement time using the first-order EKF? What is the differential equation using the second-order EKF? 

13.13 Consider the measurement equation yk = xi + *'uk,* where Vk N (0, *R).* 
Suppose that Pi = 1, and &, = 1 is unbiased. 

a) What is the expected value of 2: if the first-order EKF is used for the measurement update? **Based** on your expression for *E(2:),* how does the bias of the state estimate change with R? **Does** this make intuitive sense? 

b) What is the expected value of 2: if the second-order EKF is used for the measurement update? 

13.14 Consider the system 

$$\begin{array}{r c l}{{z_{k+1}}}&{{=}}&{{a z_{k}+w_{k},\quad}}&{{w_{k}\sim(0,Q)}}\\ {{y_{k}}}&{{=}}&{{z_{k}+v_{k},\quad}}&{{v_{k}\sim(0,R)}}\end{array}$$

with unknown parameter a. Suppose that an EKF is used to estimate the state Zk and the parameter a. Further suppose that the artificial noise term used in the estimation of a is zero, and the EKF converges to the correct value of a with zero variance. Show that the EKF in this situation is equivalent to the standard Kalman filter for the scalar system when a is known. 

## Computer Exercises

13.15 Write a program that implements the moving average filter and the extended Kalman filter for the system described in Problem **13.3.** Use R = 1, x = 1, Po+ = 1, and 20 = 2. Which filter appears to perform better? 

$$\ddot{r}~~=~~r\dot{\theta}^{2}-\frac{G M}{r^{2}}+w,$$

13.16 A planar model for a satellite orbiting around the earth can be modeled as 

$$\ddot{\theta}\ \ =\ \ \frac{-2\dot{\theta}\dot{r}}{r}$$

where T is the distance of the satellite from the center of the earth, 8 is the angular position of the satellite in its orbit, G = **6.6742** x 10-11m3/kg/s2 is the universal gravitational constant, M = 5.98 x **loz4** kg is the mass of the earth, and w N 
(0, **low6)** is random noise due to space debris, atmospheric drag, outgassing, and Write a state-space model for this system with XI = T, xz = +, x3 = 8, and 24 = 8.. 

What must 9 be equal to in order for the orbit to have a constant radius when w = O? 

Linearize the model around the point T = *TO,* I: = 0, 8 = woT, 8 = *wo.* 
What are the eigenvalues of the system matrix for the linearized system when TO = **6.57** x lo6 m? What would you estimate to be the largest integration step size that could be used to simulate the system? (Hint: 
recall that for a second-order transfer function with imaginary poles kja, the time constant is equal to l/a.) 
d) Suppose that measurements of the satellite radius and angular position are obtained every minute, with error standard deviations of 100 meters and 0.1 radians, respectively. Simulate the linearized Kalman filter for three hours. Initialize the system with z(0) = [ TO 0 0 1.1~0 1,2(0) = z(O), and *P(0)* = diag(0,0,0,0). Plot the radius estimation error as a function of time. Why is the performance so poor? How could you modify the linearized Kalman filter to get better performance? 

e) Implement an extended Kalman filter and plot the radius estimation error as a function of time. How does the performance compare with the linearized Kalman filter? 

13.17 Implement the hybrid EKF with a measurement period of 0.1s for the system described in Example 13.1. Assume that the winding current measurement noises have a standard deviation of 0.1 amps. Create a table showing the experimental standard deviation of the motor velocity estimation error as a function of the standard deviation of the control input uncertainties 41 and *42.* **Use** control input standard deviations from 0 to 0.1 volts in steps of 0.01 (i.e., oq = 0, oq = 0.01, 
. . ., gq = 0.1). In order to make a fair comparison, you should either run several simulations for each value of oq and average the results, or else initialize the random seed in your software so that each simulation runs with the same random noise history. 

13.18 Derive the first-order EKF, second-order EKF, and iterated EKF (with one iteration) for the scalar system 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}^{2}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}^{2}+v_{k}}}\end{array}$$

where *'Wk* and Vk are independent zero-mean white noise terms with variances 0.1 and 1, respectively. Simulate the first-order, second-order, and iterated extended Kalman filters for five time steps. Set the initial state to 1, the initial estimationerror variance to 1, and the initial state estimate to 2. Compute the RMS error of the filter estimates. How does the performance of the filters compare? (Note that you need more than one simulation, in general, to obtain a fair comparison of filter performance. ) 
13.19 Use the following procedure [Sor7lb] to approximate a uniform pdf that is defined on fl with M Gaussian pdfs; that is, U(-1, 1) M **CE1** azN(pr, *0:).* 
0 Select the weighting coefficients so that a, = 1/M for all i. 

0 Select the means of the Gaussian pdfs to be equally spaced on the range 
[-1,1] with p,+1 - p, = *2/(M* + 1). 

0 Select the variances *cri* of the Gaussian pdfs to all be the same and to minimize the RMS difference between U(-1, 1) and *xzl* azN(pz, *o,")* over the range 
[-I, 11. 

The above approach reduces the approximation problem to a onedimensional optimization problem, which can be solved in a number of different ways (for example, using the golden search method [Pre92]). Plot the true pdf and the approximate pdf for M = 3, 5, and 10, and compare the RMS errors. 

13.20 Suppose you have a scalar system given as 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}^{2}+v_{k}}}\end{array}$$

where Vk is white Gaussian noise with a variance of 0.01. The pdf of the initial state xo is uniform between -1 and +1. Note from the measurement equation that there is 4 b) 
13.21 no way to distinguish between a positive state and a negative state. 

What will the extended Kalman filter estimate of the system be equal to? 

The pdf of xo can be approximated with two Gaussian pdfs, each with a variance of **0.43,** and with respective means of -1/3 and +1/3. Suppose that xo = -1/2. Plot the true state and the individual state estimates of a two-term Gaussian sum filter for 20 time steps. Plot the Gaussian pdfs at the final time for each estimate of the two-term Gaussian sum filter. 

Consider the problem of tracking a moving vehicle in two dimensions (north is one dimension and east is the other dimension). The vehicle's acceleration in the north and east directions consists of independent white noise. Two tracking stations, located at north-east coordinates *(N1, El)* and *(N2, E2),* respectively, measure the range to the vehicle. The system model can therefore be written as where nk and ek are the vehicle's north and east coordinates at time step k, T 
is the time step of the system, wk is the zero-mean process noise, and vk is the zero-mean measurement noise. Suppose that the time step T = O.ls, the process noise covariance Q = diag(0, 0,4,4), and the measurement noise covariance R = diag(1,l). The tracking stations are located at *(NI, El)* = (20,0), and **(N2,** *E2)* = 
(0,20). The initial state of the vehicle zo = [ 0 0 50 50 ] and is perfectly known. Design an extended Kalman filter to estimate the state of the vehicle. Run the simulation for 60 s. Plot the estimation error for the four states. What is the experimental standard deviation of the estimation error for each of the four states? Based on the steady-state covariance matrix of the filter, what is the theoretical standard deviation of the estimation error for each of the four states? 

T 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\phi x_{k}+w_{k}}}\\ {{}}&{{y_{k}}}&{{=}}&{{x_{k}}}\end{array}$$

13.22 Consider the system where Wk - (O,l), and $ = 0.9 is an unknown constant. Design an extended Kalman filter to estimate $. Simulate the filter for 100 time steps with zo = 1, PO = I, 20 = 0, and $0 = 0. Hand in your source code and a plot showing $ as a function of time. 

13.23 Simulate Example **13.4** with artificial parameter noise variance values 0; = 
0, 1, and 100. How does a change in the artificial parameter noise variance affect the filter's estimate of -wi? 