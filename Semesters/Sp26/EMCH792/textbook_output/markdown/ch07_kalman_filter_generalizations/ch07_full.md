---
type: chapter
chapter: 7
title: Kalman filter generalizations
---
# Chapter 7 Ka I Man Filter Generalizations

Many practical systems exist in which the correlation times of the random measurement errors are not short compared to times of interest in the system; for brevity such errors are called "colored" noise. 

-Arthur Bryson and Donald Johansen [Bry65] 
In the last two chapters, we derived the discretetime Kalman filter and presented some alternate but mathematically equivalent formulations. In this chapter we will discuss some generalizations of the Kalman filter that will make it more flexible and effective for a broader class of problems. For example, in our derivation of the Kalman filter in Chapter 5 we assumed that the process noise and measurement noise were uncorrelated. In Section **7.1,** we will show how correlated process and measurement noise changes the Kalman filter equations. Our derivation in Chap ter 5 also assumed that the process noise and measurement noise were white. We modify the Kalman filter to deal with colored process noise and measurement noise in Section 7.2. 

Many Kalman filter implementations are coded in embedded systems (rather than desktop computers) where memory and computational effort is still a primary consideration. For this reason, we can replace the timevarying Kalman filter of Chapter 5 with a steady-state Kalman filter that often performs nearly rn well. This means that we do not have to compute the estimation-error covariance or Kalman gain in real time. This is discussed in Section **7.3,** which includes a presentation of a-P and *a-P-7* filtering. 

When the dynamics of the system are not perfectly known, then the Kalman filter may not provide acceptable state estimates. This can be addressed by giving more weight to recent measurements when updating the state estimate, and discounting measurements that arrived a long time ago. This is called the fading-memory filter and is discussed in Section **7.4.** Finally, there may be other information about the states other than the system model. For example, there may be state constraints that we know must be satisfied. Section **7.5** discusses several ways to incorporate state equality constraints and state inequality constraints into the formulation of the Kalman filter. 

## 7.1 Correlated Process And Measurement Noise

Our derivation of the Kalman filter in Chapter 5 assumed that the process noise and measurement noise were uncorrelated. In this section, we will show how correlated process and measurement noise changes the Kalman filter equations. Suppose that we have a system given by 

$$\begin{array}{r l}{={}}&{{}F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}\\ {={}}&{{}H_{k}x_{k}+v_{k}}\\ {\sim{}}&{{}(0,Q_{k})}\\ {\sim{}}&{{}(0,R_{k})}\\ {={}}&{{}Q_{k}\delta_{k-j}}\\ {={}}&{{}R_{k}\delta_{k-j}}\\ {={}}&{{}M_{k}\delta_{k-j+1}}\end{array}$$
$$\pi_{k}$$
$$y_{k}$$

$$(7.1)$$
E[WkWT] = *Qk8k-j* 
E[WkWjT] = Rk6k-J 
E[Wk'$] = *Mkdk-J+l* **(7.1)** 
We see that the process noise in the system equation is correlated with the measurement noise, with the cross covariance given by *Mk6k-j+l.* Our derivation in Chapter 5 assumed that Mk was zero, but in this section we will relax that assumption. For example, suppose that our system is an airplane and winds are buffeting the plane. We are using an anemometer to measure wind speed as an input to our Kalman filter. So the random gusts of wind affect both the process (i.e., the airplane dynamics) and the measurement (i.e., the sensed wind speed). We see that there is a correlation between the process noise and the measurement noise. From the above equation, we see that the process noise at time k is correlated with the measurement noise at time (k + 1); that is, Wk is correlated with *?&+I.* This is because Wk affects the state at time (k + I), just as *?&+I* affects the measurement at time (k + 1). 

In order to find the Kalman filter equations for the correlated noise system, we will define the estimation errors as 

$$\begin{array}{ccccc}\epsilon_{k}&=&\mathcal{I}_{k}-\hat{\mathcal{I}}_{k}^{-}\\ \epsilon_{k}^{+}&=&\mathcal{I}_{k}-\hat{\mathcal{I}}_{k}^{+}\end{array}\tag{7.2}$$

As in our original Kalman filter derivation of Chapter 5, we still assume that our update equations for the state estimate are given as follows: 

$$\hat{x}_{k}^{-}=F_{k-1}\hat{x}_{k-1}^{+}+G_{k-1}u_{k-1}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$$
$$(7.3)$$

The gain matrix Kk will not be the same as we derived in Chapter 5, but the form of the measurement update equation is still the same. Equation (7.2) can be expanded using the above equations as

$$\begin{array}{r l}{\epsilon_{k}^{-}}&{{}=}\\ {}&{{}=}\end{array}$$
$$\begin{array}{r l}{{}}&{{}=}\\ {\epsilon_{k}^{+}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
$x_{k}-\hat{x}_{k}^{-}$  $(F_{k-1}\hat{x}_{k-1}+G_{k-1}u_{k-1}+w_{k-1})-(F_{k-1}\hat{x}_{k-1}^{+}+G_{k-1}u_{k-1})$  $F_{k-1}\epsilon_{k-1}^{+}+w_{k-1}$  $x_{k}-\left[\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})\right]$  $\epsilon_{k}^{-}-K_{k}(H_{k}x_{k}+v_{k}-H_{k}\hat{x}_{k}^{-})$  $\epsilon_{k}^{-}-K_{k}(H_{k}\epsilon_{k}^{-}+v_{k})$
$$(7.4)$$

The a priori and a posteriori estimation-error covariances can be written as

$$P_{k}^{-}$$
$$P_{k}^{+}$$
Eler (ex )41 Fk-1Pk-1Fk-1 +Qk-1 E[e] (et )2 ] E {[e] - Kk(Hkex + Uk)][ez - Kk(Hkek + vk)]2 } Px - KxHkPx - KkElvk(ex)7] - Px H2 Kk + KKHKPK HK + KRE[vk(Ex)"]HEKT - E (Ex Ux )KE + KRHkE (Ex UE)KE + KkE(Uk VK)KE

$$(7.5)$$

In order to simplify this expression for Pr, we need to find an expression for E(ex v). This can be computed as

$$E(\epsilon_{k}^{-}v_{k}^{T})$$
$$=E[(x_{k}-\hat{x}_{k}^{-})v_{k}^{T}]\tag{7.6}$$ $$=E(x_{k}v_{k}^{T}-\hat{x}_{k}^{-}v_{k}^{T})$$ $$=E[(F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1})v_{k}^{T}]-E[\hat{x}_{k}^{-}v_{k}^{T}]$$ $$=0+0+M_{k}-0$$
 ) $\equiv$ ? 
In the above equation, the first term is 0 because xk-1 is independent of vk, and vk is zero-mean. The second term is 0 because uk-1 is independent of vk. last term is 0 because the a priori state estimate at time k is independent of vk.

Substituting this expression for E(e) into Equation (7.5) gives

$$P_{k}^{+}\quad=\quad$$
$P_{k}^{-}-K_{k}H_{k}P_{k}^{-}-K_{k}M_{k}^{T}-P_{k}^{-}H_{k}^{T}K_{k}^{T}+K_{k}H_{k}P_{k}^{-}H_{k}^{T}K_{k}^{T}+K_{k}M_{k}^{T}H_{k}^{T}K_{k}^{T}-M_{k}K_{k}^{T}+K_{k}H_{k}M_{k}K_{k}^{T}+K_{k}R_{k}K_{k}^{T}$  $(I-K_{k}H_{k})P_{k}^{-}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}+K_{k}(H_{k}M_{k}+M_{k}^{T}H_{k}^{T})K_{k}^{T}-M_{k}K_{k}^{T}-K_{k}M_{k}^{T}$
$$(7.7)$$

Now we need to find the gain matrix Kk that minimizes Tr(Pt).

Recall from Equation (1.66) that

$${\frac{\partial\mathrm{Tr}(A B A^{T})}{\partial A}}=2A B{\mathrm{~if~}}B{\mathrm{~is~symmetric}}$$
$$(7.8)$$
$$\mathbf{\tau}=$$

We can use this fact to derive 

$$\frac{\partial{\rm Tr}(P_{k}^{+})}{\partial K_{k}}=-2(I-K_{k}H_{k})P_{k}^{-}H_{k}^{T}+2K_{k}R_{k}+\tag{7.9}$$ $$2K_{k}(H_{k}M_{k}+M_{k}^{T}H_{k}^{T})-M_{k}-M_{k}$$ $$=2\left[K_{k}(H_{k}P_{k}^{-}H_{k}^{T}+H_{k}M_{k}+M_{k}^{T}H_{k}^{T}+R_{k})-\right.$$ $$P_{k}^{-}H_{k}^{T}-M_{k}\left]\right.$$

In order to make this partial derivative zero, we need to set the gain Kk as follows: 

$$K_{k}=(P_{k}^{-}H_{k}^{T}+M_{k})(H_{k}P_{k}^{-}H_{k}^{T}+H_{k}M_{k}+M_{k}^{T}H_{k}^{T}+R_{k})^{-1}\tag{7.10}$$

This gives the optimal Kalman gain matrix for the system with correlated process and measurement noise. The estimation-error covariance is then obtained from Equation **(7.7)** as 

$$P_{k}^{+}$$
Pz = (1 - KkHk)Pi(I - KkHk)T +  Kk(HkMk + MrHT + Rk)K;- MkK? - KkMF  PL - KkHkPL - PLHrKr +  Kk(HkpFHr + HkMk + M$$ -I- Rk)Kr -  MkKT - KkMF  PL - Kk(HkpL + Mr) - (PLH;+ Mk)KT +  (PLH; + Mk)(HkpLHr + HkMk + MFH; + &)-l(HkPL + M?)  = p; - Kk(HkPL + Mr) - (PLH,' + Mk)Kr + (PiHr + Mk)Kr  = PL - Kk(HkPF +MF) (7.11)  =  = 
This gives the measurement-update equation for the estimation-error covariance for the Kalman filter with correlated process and measurement noise. The measurementupdate equation for the state estimate is the same as for the standard Kalman filter and is given in Equation **(7.3).** The timeupdate equations for the state estimate and the estimation-error covariance are also the same as before. The Kalman filter for the system with correlated process and measurement noise can be summarized as follows. 

## The General Discretetime Kalman Filter

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\\ {{E[w_{k}w_{j}^{T}]}}&{{=}}&{{Q_{k}\delta_{k-j}}}\\ {{E[v_{k}v_{j}^{T}]}}&{{=}}&{{R_{k}\delta_{k-j}}}\\ {{E[w_{k}v_{j}^{T}]}}&{{=}}&{{M_{k}\delta_{k-j+1}}}\end{array}$$

1. The system and measurement equations are given as 

$$(7.12)$$

$$(7.13)$$

2. The Kalman filter is initialized as 

$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E(x_{0})}}\\ {{P_{0}^{+}}}&{{=}}&{{E[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}]}}\end{array}$$

The second form for Pz and the second form for Kk can be derived by following a procedure similar to that shown in Section *3.3.1.* Note that this is a generalization of the Kalman filter that was presented in Equation *(5.19).* If Mk = 0, then the above equations reduce to Equation *(5.19).* 

Consider the following scalar system: 

$$x_{k}=0.8x_{k-1}+w_{k-1}$$ $$y_{k}=x_{k}+v_{k}$$ $$E[w_{k}w_{j}^{T}]=1\delta_{k-j}$$ $$E[v_{k}v_{j}^{T}]=0.1\delta_{k-j}$$ $$E[w_{k}v_{j}^{T}]=M\delta_{k-j+1}\tag{7.15}$$

We can use the method discussed in Section **2.7** to simulate correlated noise. The Kalman filter equations given above can then be run to obtain an estimate of the state. Table *7.1* shows (for several values of M) the variance of the estimation error for the standard Kalman filter (when M = 0 is assumed) and for the correlated noise Kalman filter (when the correct value of M is used). 

When M = 0, the estimation-error variances are the same for the two filters, as expected. However, when M \# 0, the filter that uses the correct value of M performs noticeably better than the filter that incorrectly assumes that M =O. 

vvv 

Table **7.1** 
when there is a cross covariance M between the process noise and the measurement noise. The standard filter assumes that M = 0, and the correlated filter uses the correct value of M 
Experimental estimation-error variance (50 time steps) for Example 7.1 

|               | Standard Filter   | Correlated Filter   |
|---------------|-------------------|---------------------|
| Correlation M | (M = 0 assumed)   | (correct M used)    |
| 0             | 0.076             |                     |
| 0.25          | 0.030             |                     |
| -0.25         | 0.117             | 0.076  0.019  0.052 |

## 7.2 Colored Process And Measurement Noise

Our derivation of the Kalman filter in Chapter 5 assumed that the process noise and measurement noise were both white. In this section, we will show how to deal with colored process noise, and we will present two methods for dealing with colored measurement noise. 

## 7.2.1 Colored Process Noise

If the process noise is colored, then it is straightforward to modify the system equations and obtain an equivalent but higher-order system with white process noise [Buc68]. Then the standard Kalman filter equations can be applied. For example, suppose that we have an LTI system given as 

$$(7.16)$$
$$x_{k}=F x_{k-1}+w_{k-1}$$
$$(7.17)$$
$$w_{k}=\psi w_{k-1}+\zeta_{k-1}$$

$$(7.18)$$
Xk = *FXk-1+ Wk-1* (7.16) 
where the covariance of wk is equal to *Qk.* Further suppose that the process noise is the output of a dynamic system: 
wk = "Wk-1 f *Ck-1* (7.17) 
where **Ck-1** is zero-mean white noise that is uncorrelated with *Wk-1.* In this case, we can see that the covariance between Wk and *Wk-1* is equal to 

$$\begin{array}{r l}{={}}&{{}E(\psi w_{k-1}w_{k-1}^{T}+\zeta_{k-1}w_{k-1}^{T})}\\ {={}}&{{}\psi Q_{k-1}+0}\end{array}$$
$$E(w_{k}w_{k-1}^{T})$$
$$\begin{array}{r c l}{{\left[\begin{array}{c}{{x_{k}}}\\ {{w_{k}}}\end{array}\right]}}&{{=}}&{{\left[\begin{array}{c c}{{F}}&{{I}}\\ {{0}}&{{\psi}}\end{array}\right]\left[\begin{array}{c}{{x_{k-1}}}\\ {{w_{k-1}}}\end{array}\right]+\left[\begin{array}{c}{{0}}\\ {{\zeta_{k-1}}}\end{array}\right]}}\\ {{\begin{array}{r c l}{{x_{k}^{\prime}}}&{{=}}&{{F^{\prime}x_{k-1}^{\prime}+w_{k-1}^{\prime}}}\end{array}}\end{array}$$
$$(7.19)$$

The 0 arises because *Wk-1* is independent from *&.-I,* and *Ck-1* is zero-mean. We see that Wk is colored process noise (because it is correlated with itself at other time steps). We can combine Equations (7.16) and (7.17) to obtain This is an augmented system with a new state *x',* a new system matrix *F',* and a new process noise vector w' whose covariance is given as follows: 

$$(7.20)$$
$$\begin{array}{r c l}{{E(w_{k}^{\prime}w_{k}^{T})}}&{{=}}&{{\left[\begin{array}{l l}{{0}}&{{0}}\\ {{0}}&{{E(\zeta_{k}\zeta_{k}^{T})}}\end{array}\right]}}\\ {{}}&{{=}}&{{Q_{k}^{\prime}}}\end{array}$$

Now the standard Kalman filter can be run on this augmented system that has white process noise, as long as we know *E(<k<;).* Computational effort increases because the state vector dimension has doubled, but conceptually this is a straightforward approach to dealing with colored process noise. 

## 7.2.2

## Colored Measurement Noise: State Augmentation

Now suppose that we have colored measurement noise. Our system and measure ment equations are given as The measurement noise is itself the output of a linear system. The covariance of the measurement noise is given as 

$$\begin{array}{r c l}{{E[v_{k}v_{k-1}^{T}]}}&{{=}}&{{E[(\psi_{k-1}v_{k-1}+\zeta_{k-1})v_{k-1}^{T}]}}\\ {{}}&{{=}}&{{\psi_{k-1}E[v_{k-1}v_{k-1}^{T}]}}\end{array}$$

There are a couple of ways to solve the colored measurement-noise problem. It was solved by Richard Bucy for continuous-time problems in [Buc68]. Here we will solve the discretetime problem by augmenting the state. This was originally proposed in [Bry65] in the context of continuous-time systems. We augment the original system model as follows: 

$$\left[\begin{array}{c}x_{k}\\ v_{k}\end{array}\right]=\left[\begin{array}{cc}F_{k-1}&0\\ 0&\psi_{k-1}\end{array}\right]\left[\begin{array}{c}x_{k-1}\\ v_{k-1}\end{array}\right]+\left[\begin{array}{c}w_{k-1}\\ \zeta_{k-1}\end{array}\right]$$ $$y_{k}=\left[\begin{array}{cc}H_{k}&I\end{array}\right]\left[\begin{array}{c}x_{k}\\ v_{k}\end{array}\right]+0\tag{7.23}$$
$$\begin{array}{r c l}{{x_{k}^{\prime}}}&{{=}}&{{F_{k-1}^{\prime}x_{k-1}^{\prime}+w_{k-1}^{\prime}}}\\ {{y_{k}}}&{{=}}&{{H_{k}^{\prime}x_{k}^{\prime}+v_{k}^{\prime}}}\end{array}$$
$$(7.21)$$
$$(7.22)$$

This can be written as 

$$(7.24)$$

This system is equivalent to the original system but **has** a modified state *x',* state transition matrix *F',* process noise *w',* measurement matrix HI, and measurement noise *w'.* The covariance of the process noise and the covariance of the measurement noise are computed as 

$$E[w^{\prime}_{k}w^{T}_{k}]=E\left[\left(\begin{array}{c}w_{k}\\ \zeta_{k}\end{array}\right)\left(\begin{array}{cc}w^{T}_{k}&\zeta^{T}_{k}\end{array}\right)\right]\tag{7.25}$$ $$=\left[\begin{array}{cc}Q_{k}&0\\ 0&Q_{\zeta k}\end{array}\right]$$ $$E[v^{\prime}_{k}v^{T}_{k}]=0$$

We see that there is no measurement noise, which is equivalent to saying that the measurement noise is white with a mean of zero and a covariance of zero. Theoretically, it is fine to have zero measurement noise in the Kalman filter. In fact, Kalman's original paper [Ka160] was written without any restrictions on the singularity of the measurement-noise covariance. But practically speaking, a singular measurement-noise covariance often results in numerical problems [May79, p. 2491, [Ste94, p. 3651. For that reason we will present another approach to dealing with colored measurement noise in the next section. 

## 7.2.3

$$\begin{array}{l}{{F_{k-1}x_{k-1}+w_{k-1}}}\\ {{H_{k}x_{k}+v_{k}}}\\ {{\psi_{k-1}v_{k-1}+\zeta_{k-1}}}\\ {{(0,Q_{k})}}\\ {{(0,Q_{\zeta k})}}\\ {{Q_{k}\delta_{k-j}}}\\ {{Q_{\zeta k}\delta_{k-j}}}\\ {{0}}\end{array}$$
$$\begin{array}{r l}{x_{k}}&{{}=}\\ {y_{k}}&{{}=}\\ {v_{k}}&{{}=}\\ {w_{k}}&{{}\sim}\\ {\zeta_{k}}&{{}\sim}\\ {E[w_{k}w_{j}^{T}]}&{{}=}\\ {E[\zeta_{k}\zeta_{j}^{T}]}&{{}=}\\ {E[w_{k}\zeta_{j}^{T}]}&{{}=}\end{array}$$

## Colored Measurement Noise: Measurement Differencing

In this section we present a method for dealing with colored measurement noise that does not rely on augmenting the state vector. This approach is due to [Bry68]. 

As in the previous section, our system is given as 

$$(7.26)$$

Now we define an auxiliary signal y; as follows: 

$$y_{k-1}^{\prime}=y_{k}-\psi_{k-1}y_{k-1}$$
$$(7.27)$$

Substitute for Yk and **Yk-1** in the above definition of *yk-l* to obtain 

$$(H_{k}x_{k}+v_{k})-\psi_{k-1}(H_{k-1}x_{k-1}+v_{k-1})$$ $$H_{k}(F_{k-1}x_{k-1}+w_{k-1})+v_{k}-\psi_{k-1}(H_{k-1}x_{k-1}+v_{k-1})$$ $$(H_{k}F_{k-1}-\psi_{k-1}H_{k-1})x_{k-1}+H_{k}w_{k-1}+v_{k}-\psi_{k-1}v_{k-1}$$ $$(H_{k}F_{k-1}-\psi_{k-1}H_{k-1})x_{k-1}+(H_{k}w_{k-1}+\zeta_{k-1})$$ $$H^{\prime}_{k-1}x_{k-1}+v^{\prime}_{k-1}\tag{7.28}$$
$$y_{k-1}^{\prime}$$
 $\qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad\\ \qquad=\qquad$
and *WL-~* are defined by the above equation. We see that we have a new measurement equation for the measurement **yi-l** that has a measurement matrix 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+w_{k-1}}}\\ {{y_{k}^{\prime}}}&{{=}}&{{H_{k}^{\prime}x_{k}+v_{k}^{\prime}}}\end{array}$$

HA-l and measurement noise v;-l. Our new but equivalent system can therefore be written as 

$$(7.29)$$
$$(7.30)$$

$$(7.31)$$
$$\begin{array}{r c l}{{E[v_{k}^{\prime}v_{k}^{\prime\;T}]}}&{{=}}&{{E[(H_{k+1}w_{k}+\zeta_{k})(w_{k}^{T}H_{k+1}^{T}+\zeta_{k}^{T})]}}\\ {{}}&{{=}}&{{H_{k+1}Q_{k}H_{k+1}^{T}+Q_{\xi k}}}\\ {{E[w_{k}v_{k}^{\prime\;T}]}}&{{=}}&{{E[w_{k}(w_{k}^{T}H_{k+1}^{T}+\zeta_{k}^{T})]}}\\ {{}}&{{=}}&{{Q_{k}H_{k+1}^{T}}}\end{array}$$

The covariance of the new measurement noise *w',* and the cross covariance between the process noise w and the new measurement noise v', can be obtained as where we have used the fact that Wk and ck are independent and zero-mean. 

Now we will dehe the a *priori* and *a posteriori* state estimates for the system of Equation **(7.29)** slightly differently than we have up to this point. The state estimate 2; at time k is defined as the expected value of the state Zk conditioned on measurements up to and including time k. 

$\hat{\bf z}_{k}=E[x_{k}|y_{1},\cdots,y_{k}]$
$$(7.32)$$
The state estimate at time 2; at time k is defined as the expected value of the state Xk conditioned on measurements up to and including time (k + **1).** We assume that it is given by a standard linear predictor/corrector combination: 

$$\hat{x}_{k}^{+}=E[x_{k}|y_{1},\cdots,y_{k+1}]\tag{1}$$ $$=\hat{x}_{k}^{-}+K_{k}(y_{k}^{\prime}-H_{k}^{\prime}\hat{x}_{k}^{-})$$

Note that these definitions of 2; and 2: are slightly different than the definitions used elsewhere in this book. Usually, 2; is based on measurements up to and including time k - 1, and 2; is based on measurements up to and including time k. 

In this section, these two estimates are both based on one additional measurement. 

As in our previous derivations, we choose the gain Kk to minimize the trace of the covariance of the estimation error. In equation form this is written as 

$K_{k}=$ argmin ${\rm Tr}\ E\left[(x_{k}-\hat{x}_{k}^{+})(x_{k}-\hat{x}_{k}^{+})^{T}\right]$ (7.33)
We will not work through the details here, but in [Bry68] it is shown that this minimization leads to the following estimator equations. 

## The Discrete-Time Kalman Filter With Colored Measurement Noise

1. Our system and measurement equations are given by Equation **(7.26).** 
2. y;C and Hi are defined by Equations **(7.27)** and **(7.28).** 

3. At each time step, execute the following equations to update the state estimate: 

A similar approach to the continuous-time filter with colored measurement noise is given in [Ste68]. 

Consider the following linear system with colored measurement noise: 

$$x_{k}=\left[\begin{array}{cc}0.70&-0.15\\ 0.03&0.79\end{array}\right]x_{k-1}+\left[\begin{array}{c}0.15\\ 0.21\end{array}\right]w_{k-1}$$ $$y_{k}=\left[\begin{array}{cc}1&0\\ 0&1\end{array}\right]x_{k}+v_{k}$$ $$v_{k}=\psi v_{k-1}+\zeta_{k-1}$$ $$E[w_{k}w_{j}^{T}]=1\delta_{k-j}$$ $$E[\zeta_{k}\zeta_{j}^{T}]=\left[\begin{array}{cc}0.05&0\\ 0&0.05\end{array}\right]\delta_{k-j}$$ $$E[w_{k}\zeta_{j}^{T}]=0$$ (7)
$$(7.35)$$

The scalar $ indicates the correlation of the measurement noise. If $ = 0 then the measurement noise is white. As $, increases, the color of the measurement noise increases (i.e., it contains more low-frequency components and less high-frequency components). In this example, we simulate the Kalman filter for this system in three different ways. First, we simulate the standard Kalman filter while simply ignoring the colored nature of the measurement noise. Second, we augment the state vector as described in Section **7.2.2,** 
which will take the colored nature of the measurement noise into account, and then simulate the Kalman filter. Third, we implement the measurementdifferencing approach that is described in this section, which again takes the colored nature of the measurement noise into account, and then simulate the filter. Table **7.2** shows the experimental values of the trace of the covariance of the estimation error for the three filters. We can see that if $ = 0 then the three filters perform essentially identically. (There is some difference in performance between the filters because the performance measures in Table **7.2** 
are experimentally determined statistical values.) However, as $ increases 
(i.e., the color of the measurement noise increases) we see that the filters that take this into account provide increasingly better performance compared to the standard Kalman filter. This example shows the improvement in performance that is possible with the colored measurement-noise filters described in this section. 

Table **7.2** 
error (500 time steps) for Example **7.2. As** the color content of the measurement noise increases (i.e., as *11,* increases) the colored measurement-noise filters provide increasingly better performance than the standard Kalman filter Experimental values of the trace of the covariance of the estimation 

|          | Standard   | Augmented   | Measurement   |
|----------|------------|-------------|---------------|
| Color $J | Filter     | Filter      | Differencing  |
| 0.0      | 0.245      | 0.245       | 0.247         |
| 0.2      | 0.260      | 0.258       | 0.259         |
| 0.5      | 0.308      | 0.294       | 0.295         |
| 0.9      | 0.631      | 0.407       | 0.406         |

## Vvv 7.3 Steady-State Filtering

Many Kalman filter implementations are coded in embedded systems (rather than desktop computers) in which memory and computational effort is still a primary consideration. If the underlying system is time-invariant, and the process- and measurement-noise covariances are time-invariant, then we can replace the timevarying Kalman filter of Chapter 5 with a steady-state Kalman filter. The steadystate filter often performs nearly as well as the time-varying filter. Using a steadystate filter has the advantage that we do not have to compute the estimation-error covariance or Kalman gain in real time. Note that a steady-state Kalman filter is still a dynamic system. The term "steady-state" Kalman filtering means that the Kalman filter is time-invariant; it is the Kalman gain that is in steady state. 

As an example, recall the scalar system discussed in Example 5.2: 

$$(7.36)$$

We saw from Example 5.2 that the Kalman gain converged to a steady-state value after a few time steps: 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,1)}}\\ {{v_{k}}}&{{\sim}}&{{(0,1)}}\end{array}$$
$$\operatorname*{lim}_{k\rightarrow\infty}K_{k}\quad=\quad K_{\infty}$$
k+m - 1+d3 
* [10] M. C. Gonzalez-Garcia, M. C. Gonzalez-Garcia, M.  
So instead of performing the measurement-update equation for *Pk,* the time-update equation for **Pk,** and the Kalman gain computation for Kk at each time step, we can simply use the constant Kw as our Kalman gain at each time step. For a system with many states, this can save a lot of computational effort, especially considering the fact that this will allow us to avoid real-time matrix inversions. 

The steady-state Kalman filter for this example is simply given as 

$$\hat{x}_{k}^{-}=F\hat{x}_{k-1}^{+}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{+}+K_{\infty}(y_{k}-H\hat{x}_{k}^{-})$$ $$=F\hat{x}_{k-1}^{+}+K_{\infty}(y_{k}-HF\hat{x}_{k-1}^{+})$$ $$=(I-K_{\infty}H)F\hat{x}_{k-1}^{+}+K_{\infty}y_{k}\tag{7.38}$$

The steady-state Kalman filter is not optimal because we are not using the optimal Kalman gain at each time step (although it approaches optimality in the limit as k + *00).* We are instead using the steady-state Kalman gain. However, for many problems of practical interest, the performance of the steady-state filter is nearly indistinguishable from that of the time-varying filter. For any particular problem, the difference between the time-varying and steady-state filters needs to be assessed by simulation or experimental results. 

One way to determine the steady-state Kalman gain is by numerical simulation. 

We can simply write a computer program to propagate the Kalman gain as a function of time, and then observe the value toward which the gain is converging. 

Another way to determine the steady-state Kalman gain is to manipulate the Kalman filter equations from Equation **(7.14).** Recall the covariance time-update equation for a time-invariant system: 
= *FPzFT* + Q **(7.39)** 

$$P_{k+1}^{-}=F P_{k}^{+}F^{T}+Q$$
$$(7.39)$$

Now substitute the expression for Pz from Equation **(7.14)** into this equation to obtain P;+l = FP;FT - FKkHPFFT - *FKkMTFT* + Q **(7.40)** 
Now substitute the expression for Kk from Equation **(7.14)** into this equation to obtain 

$$\begin{array}{r l}{P_{k+1}^{-}}&{{}=1}\end{array}$$
$$\mathbf{\tau}=$$
P;+~ = FP;F~- 
$$FP_{k}^{-}F^{T}-$$ $$F(P_{k}^{-}H^{T}+M)(HP_{k}^{-}H^{T}+HM+M^{T}H^{T}+R)^{-1}HP_{k}^{-}F^{T}-$$ $$F(P_{k}^{-}H^{T}+M)(HP_{k}^{-}H^{T}+HM+M^{T}H^{T}+R)^{-1}M^{T}F^{T}+Q$$ $$FP_{k}^{-}F^{T}-F(P_{k}^{-}H^{T}+M)(HP_{k}^{-}H^{T}+HM+M^{T}H^{T}+R)^{-1}\times$$ $$(HP_{k}^{-}+M^{T})F^{T}+Q\tag{7.41}$$

If P; converges to a steady-state value, then Pi = *P;+l* for large k. We will denote this steady-state value as *Pm,* which means that we can write 

$$\begin{array}{r c l}{{P_{\infty}}}&{{=}}&{{F P_{\infty}F^{T}-}}\\ {{}}&{{}}&{{F(P_{\infty}H^{T}+M)(H P_{\infty}H^{T}+H M+M^{T}H^{T}+R)^{-1}\times}}\\ {{}}&{{}}&{{(H P_{\infty}+M^{T})F^{T}+Q}}\end{array}$$
$$(7.42)$$

This is called an algebraic Riccati equation (ARE), or more specifically a discrete ARE (DARE).l Once we have *Pw,* we can substitute it for P; in the Kalman gain IIn **MATLAB's** Control System Toolbox, we **can** solve this equation by invoking the command DARE(FT, HT, 8, HM + MTHT + R, FM). 

$$(7.43)$$

formula of Equation (7.14) to obtain the steady-state Kalman gain: 

$$K_{\infty}=(P_{\infty}H^{T}+M)(H P_{\infty}H^{T}+H M+M^{T}H^{T}+R)^{-1}$$

There are systems for which the Riccati equation (and hence the Kalman gain) does not converge to a steady-state value. Furthermore, it may converge to different steady-state values depending on the initial condition *PO.* Finally, even when it does converge to a steady-state value, it may result in an unstable Kalman filter. These issues comprise a rich field of study that has been reported widely in many books and papers [McG74, And79, Kai81, Goo84, Chu871. We will summarize the most important Riccati equation convergence results below, but first we need to define what it means for a system to be controllable on the unit circle. Definition 11 The matrix pair (F,G) is controllable on the unit circle if *there* exists some matrix K such that (F - GK) does not have any eigenvalues with magnitude 1. 

We illustrate this definition with some simple examples. 

## H **Example7.3**

Consider the scalar system xk+1 = xk (7.44) 
In this example, F = 1 and G = 0. The system dynamics are independent of any control signal, and the system has an eigenvalue with a magnitude of 1. 

The system is not controllable on the unit circle because its eigenvalue has a magnitude of 1 regardless of the feedback control input. 

vvv 

Consider the scalar system 

$\left(7.44\right)^2$
xk+1 = *2xk* (7.45) 
In this example, F = 2 and G = 0. As in the previous example, the system dynamics are independent of any control signal. However, the system eigenvalue has a magnitude of 2. The system is controllable on the unit circle because there exists a feedback control gain K such that (F - *GK)* does not have any eigenvalues with a magnitude of 1. In fact, regardless of the feedback control gain, the system eigenvalues will never have a magnitude of 1. 

vvv 

$$x_{k+1}={\left[\begin{array}{l l}{F_{1}}&{0}\\ {0}&{1}\end{array}\right]}\,x_{k}+{\left[\begin{array}{l}{1}\\ {1}\end{array}\right]}\,u_{k}$$

Consider the system 

$$(7.46)$$

$$x_{k+1}={\left[\begin{array}{l l}{F_{1}}&{0}\\ {-K_{1}}&{1-K_{2}}\end{array}\right]}\,x_{k}$$

When the feedback control uk = *-Kxk* is implemented, where K = [ K1 the closed-loop system becomes K2 3, 

$$(7.47)$$

The closed-loop system has eigenvalues at F1 and (1 - *K2).* We see that if FI = fl then there is no feedback control gain K that results in all closedloop eigenvalues having a nonunity magnitude, and the system is therefore not controllable on the unit circle. However, if FI \# fl, then we can find a feedback control gain K that does result in all closed-loop eigenvalues having a nonunity magnitude, and the system is therefore controllable on the unit circle. 

vvv Next we summarize the most important Riccati equation convergence results from [Bit85, Pou86, KaiOO], where proofs are given. Recall that the DARE is given as 

$$\begin{array}{r c l}{{P_{\infty}}}&{{=}}&{{F P_{\infty}F^{T}-}}\\ {{}}&{{}}&{{F(P_{\infty}H^{T}+M)(H P_{\infty}H^{T}+H M+M^{T}H^{T}+R)^{-1}\times}}\\ {{}}&{{}}&{{(H P_{\infty}+M^{T})F^{T}+Q}}\end{array}$$

We assume that Q 2 0 and R > 0. We define G as any matrix such that *GGT* = 
Q - *MR-lMT.* The corresponding steady-state Kalman gain K, is given as 

$$K_{\infty}=(P_{\infty}H^{T}+M)(H P_{\infty}H^{T}+H M+M^{T}H^{T}+R)^{-1}$$
$$\hat{x}_{k}^{+}=(I-K_{\infty}H)F\hat{x}_{k-1}^{+}+K_{\infty}y_{k}$$

The steady-state Kalman filter is given as 

$$(7.48)$$
$$(7.49)$$
$$(7.50)$$

We say that the DARE solution P, is stabilizing if it results in a stable steady-state filter. That is, P, is defined as a stabilizing DARE solution if all of the eigenvalues of (I - *K,H)F* are less than one in magnitude. 

Theorem 23 The DARE has a unique positive semidefinite solution P, if and only if both of the following conditions hold. 

1. (F, H) is detectable. 

2. (F - *MR-lH, G) is stabilizable.* 
Furthermore, the corresponding steady-state Kalman filter is stable. That **is,** *the* eigenvalues of (I - *K,H)F have magnitude less than 1.* 
Theorem 23 does not preclude the existence of DARE solutions that are negative definite or indefinite. If such solutions exist, then they would result in an unstable Kalman filter. If we weaken the stabilizability condition in Theorem **23,** we obtain the following. 

Theorem 24 *The DARE has at least one positive semidefinite solution P, if and* only if both of the following conditions hold. 

1. *(F, H) is detectable.* 
2. (F - MR-IH, G) is controllable on the unit circle. 

Furthermore, exactly one of the positive semidefinite DARE solutions results in a stable steady-state Kalman filter. 

Since controllability on the unit circle is a subset of stabilizability, we see that Theorem 24 is a subset of Theorem **23.** Theorem 24 states conditions for the existence of exactly one stabilizing positive semidefinite DARE solution. However, there may be additional DARE solutions (positive semidefinite or otherwise) that result in unstable Kalman filters. If a timevarying Kalman filter is run in this situation, then the Kalman filter equations may converge to either a stable or an unstable filter, depending on the initial condition *P$.* If we strengthen the controllability condition of Theorem **24,** we obtain the following. 

Theorem 25 The DARE has at least one positive definite solution P, if and only if both of *the following conditions hold.* 
1. (F, H) is detectable. 

2. (F - MR-IH, G) is controllable on and inside the unit circle. 

Furthermore, exactly one of the positive definite DARE solutions results in a stable steady-state Kalman filter. 

If we drop the controllability condition in the above *two* theorems, we obtain the following. 

Theorem 26 *The DARE has at least one positive semidefinite solution P, if* 
(F, H) is detectable. Furthermore, at least one such solution results in a marginally stable steady-state Kalman filter. 

Note that the resulting filter is only marginally stable, so it may have eigenvalues on the unit circle. Also note that this theorem poses a sufficient (not necessary) condition. That is, there may be a stable steady-state Kalman filter even if the conditions of the above theorem do not hold. Furthermore, even if the conditions of the theorem do hold, there may be DARE solutions that result in unstable Kalman filters. 

Consider again the scalar system of Equation **(7.36).** We see that F = 1, H = 1, Q = 1, R = 1, and M = 0. Note that *(F, H)* is observable, and (F,G) is controllable for all G such that *GGT* = Q (recall that M = 0 for this example). We therefore know from Theorem 23 that the DARE has a unique positive semidefinite solution. We know from Theorem 25 that the DARE solution is not only positive semidefinite, but it is also positive definite. We also know from these *two* theorems that the corresponding steady-state Kalman filter is stable. The DARE for this system is given by 

$$\begin{array}{r l}{={}}&{{}F P F^{T}-F P H^{T}(H P H^{T}+R)^{-1}H P F^{T}+Q}\\ {={}}&{{}P-P(P+1)^{-1}P+1}\end{array}$$
$\left(7.51\right)$ . 
This can be solved to obtain 
$$P={\frac{1\pm{\sqrt{5}}}{2}}$$
p=- *2 (7.52)* 
So the DARE has two solutions, one of which is negative and one of which is positive. If we use the negative DARE solution in the steady-state Kalman filter we obtain 

K = PHT(HPHT + R)-l  - 1-4  3-4  --  2' k = (1 - KH)F2;-_, + Kyk 
$$K$$
$${\hat{x}}_{k}^{+}$$
$$\begin{array}{r c l}{{K}}&{{=}}&{{\frac{1+{\sqrt{5}}}{3+{\sqrt{5}}}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\frac{2}{3+{\sqrt{5}}}{\hat{x}}_{k-1}^{+}+K y_{k}}}\\ {{}}&{{}}&{{\approx}}&{{0.38{\hat{x}}_{k-1}^{+}+K y_{k}}}\end{array}$$
$$(7.52)$$
$$(7.53)$$
We see that the resulting Kalman filter is unstable. However, if we use the positive DARE solution in the steady-state Kalman filter we obtain 

$$(7.54)$$

We see that the resulting Kalman filter is stable. 

vvv 

Consider a scalar system with F = 1, H = 1, Q = *0, R* = 1, and M = 0. Note 
(F, H) is detectable. However, it is not true that *(F,* G) is controllable on the unit circle for all G such that *GGT* = Q. We therefore know from Theorem 24 that the DARE does not have a positive semidefinite solution that results in a stable Kalman filter. However, we know from Theorem 26 that the DARE has a positive semidefinite solution that results in a marginally stable Kalman filter. The DARE for this system is given by 

$$\begin{array}{r l}{{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\\ {{}}&{{}}\end{array}$$
$\square$
This has two solutions for P, both of which are 0 (i.e., positive semidefinite). 
If we use this solution in the steady-state Kalman filter we obtain 
$$(7.55)$$
$$(7.56)$$
$$\begin{array}{r c l}{{K}}&{{=}}&{{0}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k-1}^{+}}}\end{array}$$

We see that the resulting Kalman filter is marginally stable (the eigenvalue is vvv 1). 

## W Example **7.8**

Consider a scalar system with F = 2, H = 1, Q = 0, R = 1, and M = 0. Note 
(F, H) is detectable. Also *(F,* G) is controllable on and inside the unit circle for all G such that *GGT* = Q. We therefore know from Theorem 24 that the DARE has exactly one positive semidefinite solution that results in a stable Kalman filter. 

However, we know from Theorem 26 that the DARE has exactly one positive semidefinite solution that results in a marginally stable Kalman filter is stable. We also know from Theorem 25 that this DARE solution is positive definite. The DARE for this system is given by 

$$\begin{array}{r c l}{{P}}&{{=}}&{{F P F^{T}-F P H^{T}(H P H^{T}+R)^{-1}H P F^{T}+Q}}\\ {{}}&{{=}}&{{4P-4P(P+1)^{-1}P}}\end{array}$$

This has two solutions for P, one of which is 0 (i.e., positive semidefinite), and one of which is 3 (i.e., positive definite). If we use P = 0 in the steady-state Kalman filter we obtain 

$$\begin{array}{r l}{K}&{{}=}\\ {{\hat{x}}_{k}^{+}}&{{}=}\end{array}$$
$$\begin{array}{l}{{0}}\\ {{2\hat{x}_{k-1}^{+}}}\end{array}$$
K=O 
$$\begin{array}{l}{{\hat{\mathbf{i}}}}\\ {{\hat{\mathbf{l}}}}\\ {{\hat{\mathbf{l}}}}\\ {{\hat{\mathbf{l}}}}\\ {{\hat{\mathbf{l}}}}\end{array}$$
$$\begin{array}{r l}{K}&{{}=}\\ {\ }&{}\\ {{\hat{x}}_{k}^{+}}&{{}=}\end{array}$$
li.+ = 2f+ 
k k-1 **(7.58)** 
We see that the resulting Kalman filter is unstable (the eigenvalue is **2).** If we use P = 3 in the steady-state Kalman filter we obtain 

$$(7.57)$$
$$(7.58)$$

$$(7.59)$$

We see that the resulting Kalman filter is stable (the eigenvalue is **1/2).** In this example, we have multiple positive semidefinite solutions to the DARE, but only one results in a stable Kalman filter. 

vvv 

## 7.3.1 A-P **Filtering**

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{T}}\\ {{0}}&{{1}}\end{array}\right]x_{k-1}+\left[\begin{array}{c c}{{T^{2}/2}}\\ {{T}}\end{array}\right]w_{k-1}^{\prime}}}\\ {{y_{k}}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{0}}\end{array}\right]x_{k}+v_{k}}}\end{array}$$

In this section, we derive the *a-P* filter [BarOl], also sometimes referred to as the f-g filter or the g-h filter **[Bro98].** The a-P filter is a steady-state Kalman filter that is applied to a two-state Newtonian system with a position measurement. This is the type of estimation problem that commonly arises in tracking problems, and so it is well known and has been widely studied since before the invention of the Kalman filter. 

Suppose we have a Newtonian dynamic system with only two states (position and velocity) and a noisy acceleration input, and we measure position plus noise. The system and measurement equations are then given as 

$$\begin{array}{l}{(0,\sigma_{w}^{2})}\\ {(0,R)}\end{array}$$
$$\begin{array}{r l}{w_{k}^{\prime}}&{{}\sim}\\ {v_{k}}&{{}\sim}\end{array}$$

(7.60) 
where T is the sample time, and wi and Vk are uncorrelated white noise processes. 

The process equation can be written as 

$$\left[\begin{array}{cc}1&T\\ 0&1\end{array}\right]x_{k-1}+w_{k-1}$$ $$(0,Q)$$ $$\left[\begin{array}{cc}T^{2}/2\\ T\end{array}\right]E[w^{\prime}_{k}w^{T}_{k}]\left[\begin{array}{cc}T^{2}/2&T\end{array}\right]$$ $$\left[\begin{array}{cc}T^{4}/4&T^{3}/2\\ T^{3}/2&T^{2}\end{array}\right]\sigma^{2}_{w}\tag{7.61}$$
$$\begin{array}{r l}{x_{k}}&{{}=}\\ {\ }&{}\\ {w_{k}}&{{}\sim}\\ {\ }&{}\\ {Q}&{{}=}\\ {\ }&{}\\ {\ }&{}\\ {\ }&{}\end{array}$$

A steady-state Kalman filter can be designed for this system from Equation **(5.19),** which is repeated here using steady-state notation: 

$$P^{-}=FP^{+}F^{T}+Q$$ $$K=P^{-}H^{T}(HP^{-}H^{T}+R)^{-1}$$ $$\hat{x}_{k}^{-}=F\hat{x}_{k-1}^{+}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K(y_{k}-H_{k}\hat{x}_{k}^{-})$$ $$P^{+}=(I-KH)P^{-}\tag{7.62}$$

For this two-state, onemeasurement problem, we see that K *is a* 2 x 1 matrix, and P- and P+ are 2 x 2 matrices. We will denote their steady-state values as 

K = [ Ki K2 1'  = [ a PIT I' 
$$(7.63)$$

The parameters of the Kalman gain matrix K define the a *and* P parameters of the *a-P* filter. We can use Equation **(7.62)** to yrite 

$$(7.64)$$

The P+ expression in Equation **(7.62)** can be written as 

$$(7.65)$$

The P- expression in Equation **(7.62)** can be rewritten in terms of P+ as follows: 

p+ = F-l(P--Q)F-T 
* [16] M. C.  
$$(7.67)$$
$$(7.68)$$
Carrying out the multiplication gives the elements of P+ as 

P.&, = PG i- a;T3/2 - PGT 
$$\begin{array}{r c l}{{\rho_{12}^{+}}}&{{=}}&{{P_{12}^{-}+\sigma_{w}^{2}T^{3}/2-P_{22}^{-}T}}\\ {{\rho_{11}^{+}}}&{{=}}&{{P_{11}^{-}+\sigma_{w}^{2}T^{4}/4-P_{12}^{-}T-P_{12}^{+}T}}\\ {{\rho_{22}^{+}}}&{{=}}&{{P_{22}^{-}-\sigma_{w}^{2}T^{2}}}\end{array}$$
Equating the P$ elements in Equations **(7.65)** and **(7.67)** and performing a little algebra gives 

$$\begin{array}{r c l}{{K_{1}P_{11}^{-}}}&{{=}}&{{2T P_{12}^{-}-T^{2}P_{22}^{-}+T^{4}\sigma_{w}^{2}/4}}\\ {{K_{1}P_{12}^{-}}}&{{=}}&{{T P_{22}^{-}-T^{3}\sigma_{w}^{2}/2}}\\ {{K_{2}P_{12}^{-}}}&{{=}}&{{T^{2}\sigma_{w}^{2}}}\end{array}$$

These three equations, along with the expressions for K1 and K2 in the last line of Equation **(7.64),** can be solved for the five unknowns *KI, K2, PG, P;,* and *PG.* 
After some algebra, this gives 

$$K_{1}=-\frac{1}{8}\left(\lambda^{2}+8\lambda-(\lambda+4)\sqrt{\lambda^{2}+8\lambda}\right)$$ $$K_{2}=\frac{1}{4T}\left(\lambda^{2}+4\lambda-\lambda\sqrt{\lambda^{2}+8\lambda}\right)$$ $$P_{11}^{-}=\frac{K_{1}\sigma_{w}^{2}}{1-K_{1}}$$ $$P_{12}^{-}=\frac{K_{2}\sigma_{w}^{2}}{1-K_{1}}$$ $$P_{22}^{-}=\left(\frac{K_{1}}{T}+\frac{K_{2}}{2}\right)P_{12}^{-}\tag{1}$$
 $ \lambda=\frac{\sigma_w^2T^2}{R}$  - matter uncertainty to the mass. 
$$(7.69)$$
$$(7.70)$$

where X is called the target maneuvering index or target tracking index [Ka184] and is defined as *aLT2* A=- R **(7.70)** 
Note that X gives the ratio of the motion uncertainty to the measurement uncertainty. From these expressions and Equation **(7.65)** it can be shown that the elements of the steady-state a *posteriori* estimation-error covariance are given as 

$$\begin{array}{lcl}P_{11}^{+}&=&K_{1}R\\ P_{12}^{+}&=&K_{2}R\\ P_{22}^{+}&=&\left(\frac{K_{1}}{T}-\frac{K_{2}}{2}\right)P_{12}^{-}\end{array}\tag{7.71}$$

## 7.3.2 A-P-7 **Filtering**

In this section, we present (without derivation) the *a-P-y* filter [BarOl], also sometimes referred to as the *f-g-h* filter or the *g-h-k* filter [Bro98]. The *a-P-7* filter is a steady-state Kalman filter that is applied to a threestate Newtonian system with a position measurement. This is very similar to the *a-P* filter presented in the previous section, except that the dynamic system model is one order higher in the a-P-7 filter. 

Consider the threestate system given in Example 5.1. The states consist of position, velocity, and acceleration, the input consists of noisy acceleration, and the measurement consists of position plus noise. The system and measurement equations are given as 

$$x_{k}=\left[\begin{array}{ccc}1&T&T^{2}/2\\ 0&1&T\\ 0&0&1\end{array}\right]x_{k-1}+\left[\begin{array}{c}T^{2}/2\\ T\\ 1\end{array}\right]w^{\prime}_{k-1}$$ $$y_{k}=\left[\begin{array}{ccc}1&0&0\end{array}\right]x_{k}+v_{k}$$ $$w^{\prime}_{k}\sim\left(0,\sigma^{2}_{w}\right)$$ $$v_{k}\sim\left(0,R\right)\tag{7.72}$$
$$\begin{array}{l}x_{k}\end{array}$$ = $$\begin{array}{l}w_{k}\end{array}$$ = $$\begin{array}{l}Q\end{array}$$ . 
where T is the sample time, and wi and Vk are uncorrelated white noise processes. The process equation can be written as 

$$\begin{array}{l}\mbox{\bf r}=\left[\begin{array}{ccc}1&T&T^{2}/2\\ 0&1&T\\ 0&0&1\end{array}\right]x_{k-1}+w_{k-1}\\ \mbox{\bf r}\sim(0,Q)\\ \mbox{\bf0}=\left[\begin{array}{c}T^{2}/2\\ T\\ 1\end{array}\right]E[w^{\prime}_{k}w^{T}_{k}]\left[\begin{array}{cc}T^{2}/2&T&1\end{array}\right]\\ \mbox{\bf0}=\left[\begin{array}{cc}T^{4}/4&T^{3}/2&T^{2}/2\\ T^{3}/2&T^{2}&T\\ T^{2}/2&T&1\end{array}\right]\sigma^{2}_{w}\end{array}\tag{7.73}$$

A steady-state Kalman filter can be designed for this system from Equation (5.19), 
in a similar way that the a-P filter was designed in the previous section. The steady-state values of the Kalman gain and a *posteriori* estimation-error covariance are denoted as 

$$K=\left[\begin{array}{cccc}K_{1}&K_{2}&K_{3}\end{array}\right]^{T}\tag{7.74}$$ $$=\left[\begin{array}{cccc}\alpha&\beta/T&\gamma/2T^{2}\end{array}\right]^{T}$$ $$P^{+}=\left[\begin{array}{cccc}P_{11}^{+}&P_{12}^{+}&P_{13}^{+}\\ P_{12}^{+}&P_{22}^{+}&P_{23}^{+}\\ P_{13}^{+}&P_{23}^{+}&P_{33}^{+}\end{array}\right]$$

The parameters of the Kalman gain matrix K define the a, P, and y parameters of the *a-P-7* filter. The solution can be computed as follows [Gra93]: 

$$(7.75)$$
$$\begin{array}{r c l}{{\alpha}}&{{=}}&{{1-s^{2}}}\\ {{\beta}}&{{=}}&{{2(1-s)^{2}}}\\ {{\gamma}}&{{=}}&{{2\lambda s}}\end{array}$$
$\begin{array}{ccc}b&=&\dfrac{\lambda}{2}-3\\ \[-3mm]c&=&\dfrac{\lambda}{2}+3\\ \[-3mm]p&=&c-\dfrac{b^2}{3}\\ \[-3mm]q&=&\dfrac{2b^3}{27}-\dfrac{bc}{3}-1\\ \[-3mm]z&=&\left[\dfrac{-q+\sqrt{q^2+4p^3/27}}{2}\right]^{1/3}\\ \[-3mm]s&=&z-\dfrac{p}{3z}-\dfrac{b}{3}\\ \[-3mm]\end{array}$  $\begin{array}{ccc}s&=&z-\dfrac{p}{3z}-\dfrac{b}{3}\\ \[-3mm]z&=&z-\dfrac{p}{3z}-\dfrac{b}{3}\\ \[-3mm]\end{array}$  Now, the answer is: . 
where X is the target maneuvering index defined in Equation (7.70), and s is an auxiliary variable. The variable s is defined via auxiliary variables b, c, p, q, and z as follows. 

$$\quad(7.76)$$. 
The steady-state a *posteriori* error covariance can be computed as 

 $P^+_{11}\;\;=\;\;$  $P^+_{12}\;\;=\;\;$  $P^+_{13}\;\;=\;\;$  $P^+_{22}\;\;=\;\;$  $P^+_{23}\;\;=\;\;$  $P^+_{33}\;\;=\;\;$  . 
PA = a!R 
PA = PR/T 
PA = yR/2T2 
$\alpha R$  $\beta R/T$  $\gamma R/2T^{2}$  $\alpha\beta+\gamma(\beta-2\alpha-4)$  $8T^{2}(1-\alpha)$  $\beta(2\beta-\gamma)R$  $4T^{3}(1-\alpha)$  $\gamma(2\beta-\gamma)R$  $4T^{4}(1-\alpha)$  (7.77)
The general idea of the a-P and *a!-P-7* filters date back to the 1940s [Mec49, Sk157, Ben621, before the advent of Kalman filtering, although, of course, the optimal cu-P-7 values were not known at that time. Further discussion of these filters and related issues can be found in [Bro98, BarOl]. A steady-state Kalman filter that is applied to a one-state Newtonian system with a position measurement is called an a filter [Sio96]. 

## 7.3.3 A Hamiltonian Approach To Steady-State Filtering

In this section, we present an alternative method for obtaining the steady-state Kalman filter. We will assume in this section that the correlation M between the process noise and measurement noise is zero so that we can simplify notation. The a priori Riccati equation of Equation (7.41) can then be written as

$$P_{k+1}=F P_{k}F^{T}-F P_{k}H^{T}(H P_{k}H^{T}+R)^{-1}H P_{k}F^{T}+Q$$
$$(7.78)$$

where we have dropped the minus superscript for ease of notation. We can use the matrix inversion lemma of Equation (1.39) to write

$$(H P_{k}H^{T}+R)^{-1}=R^{-1}-R^{-1}H(H^{T}R^{-1}H+P_{k}^{-1})^{-1}H^{T}R^{-1}$$
$$(7.79)$$

Substituting this into Equation (7.78) gives

$$P_{k+1}=FP_{k}F^{T}-FP_{k}H^{T}R^{-1}HP_{k}F^{T}+\tag{7.80}$$ $$FP_{k}H^{T}R^{-1}H(H^{T}R^{-1}H+P_{k}^{-1})^{-1}H^{T}R^{-1}HP_{k}F^{T}+Q$$

Factoring out F and FT from the beginning and end of the first three terms on the right side gives

Pk+1 = F {Pk - PkHTR-1HPk+
PkHTR-1H(HTR-1H + P23)-1HTR-1HPx} FT + Q
= F {Px - PxHT R-1H [Px - (HT R-1H + P2-1)-1HT R-1HPk] } FT + Q
F { Pk - PxHT R-1H(HT R-1H + P-1)-1 x
ll
[(HT R-1H + P=1)Pk - HT R-1HPk] } FT +Q
F {Pk - PrHT R-1H(HTR-1H + P21)-1} FT +Q
 n
=    FPx [(HT R-1H + P2-) - HT R-1H] (HT R-1 H + P2-1)-1FT + Q
F(HTR-1H + Pr-1)-1FT + Q
=
FPx(HTR-1HPx + I)-1FT + QF-TFF
=
[FPx + QF-T(HTR-1HPx + I)] (HTR-1HPx + I)-1FT
=
[(F +QF-T HT R-1H)Px + QF-7] (HT R-1H Px + I)-1 FT
(7.81)
ll
Now suppose that Pk can be factored as
$$P_{k}=S_{k}Z_{k}^{-1}\,$$
$$(7.82)$$
where Sk and Zk both have the same dimensions as Px. Making this substitution in Equation (7.81) gives

$$P_{k+1}=\left[(F+QF^{-T}H^{T}R^{-1}H)S_{k}+QF^{-T}Z_{k}\right]Z_{k}^{-1}(H^{T}R^{-1}HS_{k}Z_{k}^{-1}+I)^{-1}F^{T}\tag{7.83}$$ $$=\left[(F+QF^{-T}H^{T}R^{-1}H)S_{k}+QF^{-T}Z_{k}\right](H^{T}R^{-1}HS_{k}+Z_{k})^{-1}F^{T}$$ $$=\left[(F+QF^{-T}H^{T}R^{-1}H)S_{k}+QF^{-T}Z_{k}\right](F^{-T}H^{T}R^{-1}HS_{k}+F^{-T}Z_{k})^{-1}$$ $$=S_{k+1}Z_{k+1}^{-1}$$

This shows that

$$S_{k+1}=(F+QF^{-T}H^{T}R^{-1}H)S_{k}+QF^{-T}Z_{k}$$ $$Z_{k+1}=F^{-T}H^{T}R^{-1}HS_{k}+F^{-T}Z_{k}\tag{7.84}$$

These equations for and **Zk+1** can be written as the following single equation: 

$$\left[\begin{array}{c}Z_{k+1}\\ S_{k+1}\end{array}\right]=\left[\begin{array}{cc}F^{-T}&F^{-T}H^{T}R^{-1}H\\ QF^{-T}&F+QF^{-T}H^{T}R^{-1}H\end{array}\right]\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]\tag{7.85}$$ $$={\cal H}\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]$$

If the covariance matrix P is an n x n matrix, then 1-I will be a 2n x 2n matrix. The matrix 'H on the right side of the above equation is called a Hamiltonian matrix 
and has some interesting properties. It is a symplectic matrix; that is, it satisfies the equation 
$$J^{-1}{\cal H}^{T}J={\cal H}^{-1}\qquad\mbox{where}J=\left[\begin{array}{cc}0&I\\ -I&0\end{array}\right]\tag{7.86}$$
Symplectic matrices have the following properties (see Problem **7.7).** 
0 None of the eigenvalues of a symplectic matrix are equal to 0. 

0 If A is an eigenvalue of a symplectic matrix, then so is 1/X. 

0 The determinant of a symplectic matrix is equal to fl. 
If a symplectic matrix does not have any eigenvalues with magnitude equal to one, then half of its eigenvalues will be outside the unit circle, and the other half will be inside the unit circle. Let us define A as the diagonal matrix that contains all of the eigenvalues of h! that are outside the unit circle (assuming that none of the eigenvalues are on the unit circle). Then the Jordan form of 'FI can be written as 

$$\begin{array}{rcl}{\cal H}&=&\Psi\left[\begin{array}{cc}\Lambda^{-1}&0\\ 0&\Lambda\end{array}\right]\Psi^{-1}\\ &=&\Psi D\Psi^{-1}\end{array}\tag{7.87}$$

where the D matrix is the diagonal matrix of eigenvalues, and is defined by the above equation. The 9 matrix can be partitioned into four n x n blocks as 

$$\Psi={\left[\begin{array}{l l}{\Psi_{11}}&{\Psi_{12}}\\ {\Psi_{21}}&{\Psi_{22}}\end{array}\right]}$$

Note that the 2n x n matrix [ i:: ] contains the eigenvectors of 1-I that correspond to the stable eigenvalues of *1-I* (i.e., the eigenvalues that are inside the unit circle). 

The 2n x n matrix [ :i: ] contain the eigenvectors of 'H that correspond to the unstable eigenvalues of 'H (i.e., the eigenvalues that are outside the unit circle). 

Equation **(7.85)** can be written as 

$$(7.88)$$
$$\left[\begin{array}{c}Z_{k+1}\\ S_{k+1}\end{array}\right]=\Psi D\Psi^{-1}\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]$$ $$\Psi^{-1}\left[\begin{array}{c}Z_{k+1}\\ S_{k+1}\end{array}\right]=D\Psi^{-1}\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]\tag{7.89}$$

Now define the n x n matrices *Y1k* and *Y2k1* and the 2n x n matrix *Yk,* as follows: 

$$\left[\begin{array}{c}Y_{1k}\\ Y_{2k}\end{array}\right]=\Psi^{-1}\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]\tag{7.90}$$ $$=\left[\begin{array}{cc}(\Psi^{-1})_{11}&(\Psi^{-1})_{12}\\ (\Psi^{-1})_{21}&(\Psi^{-1})_{22}\end{array}\right]\left[\begin{array}{c}Z_{k}\\ S_{k}\end{array}\right]$$ $$=Y_{k}$$
$$\begin{array}{r c l}{{Y_{k+1}}}&{{=}}&{{D Y_{k}}}\\ {{Y_{1,k+1}}}\\ {{Y_{2,k+1}}}\end{array}\right]\quad=\quad\left[\begin{array}{c c}{{\Lambda^{-1}}}&{{0}}\\ {{0}}&{{\Lambda}}\end{array}\right]\left[\begin{array}{c}{{Y_{1k}}}\\ {{Y_{2k}}}\end{array}\right]$$

Note in the above equation that **(V1)ll** is *not* the inverse of the upper left n x n partition of \k; the matrix *(W1)ll* is rather the upper left n x n partition of *T1.* 
(Similar statements hold for the other partitions.) With these definitions we can write Equation (7.89) as 

$$(7.91)$$

From this equation we see that 

$$(7.92)$$

Similarly we see that 

$$(7.93)$$

Now note that Equation (7.90) can be written as 

$$Y_{1k}=\Lambda^{-k}Y_{1,0}$$
$$\begin{array}{r c l}{{Y_{2,k+1}}}&{{=}}&{{\Lambda Y_{2k}}}\\ {{}}&{{Y_{2k}}}&{{=}}&{{\Lambda^{k}Y_{2,0}}}\end{array}$$
$$\left[\begin{array}{c}{{Z_{k}}}\\ {{S_{k}}}\end{array}\right]=\left[\begin{array}{c c}{{\Psi_{11}}}&{{\Psi_{21}}}\\ {{\Psi_{21}}}&{{\Psi_{3}}}\end{array}\right]$$ $$=\left[\begin{array}{c c}{{\Psi_{11}}}&{{\Psi_{3}}}\\ {{\Psi_{21}}}&{{\Psi_{4}}}\end{array}\right]$$

[ 21 = [ 2 21 [ *z:]* 
$$\begin{array}{l}{{\Psi_{12}}}\\ {{\Psi_{22}}}\end{array}\left[\begin{array}{l}{{Y_{1k}}}\\ {{Y_{2k}}}\end{array}\right]$$
= [ E: E: ] [ *AkY2,0* ] 
$$(7.94)$$
$$(7.95)$$
$$(7.96)$$
As k increases, the *A-k* matrix approaches **zero** (because it is a diagonal matrix whose elements are all less than one in magnitude). Therefore, for large k we obtain 

$$\begin{array}{r c l}{{\left[\begin{array}{c}{{Z_{k}}}\\ {{S_{k}}}\end{array}\right]}}&{{=}}&{{\left[\begin{array}{c c}{{\Psi_{11}}}&{{\Psi_{12}}}\\ {{\Psi_{21}}}&{{\Psi_{22}}}\end{array}\right]\left[\begin{array}{c}{{0}}\\ {{\Lambda^{k}Y_{2,0}}}\end{array}\right]}}\\ {{Z_{k}}}&{{=}}&{{\Psi_{12}Y_{2k}}}\\ {{S_{k}}}&{{=}}&{{\Psi_{22}Y_{2k}}}\end{array}$$

Solving for sk for large values of k gives 

$$S_{k}=\Psi_{22}\Psi_{12}^{-1}Z_{k}$$
sk = *q22QT;zk* (7.96) 
But we also **know** from Equation **(7.82)** that 

$$(7.97)$$
$$S_{k}=P_{k}Z_{k}$$
$$(7.98)$$
$$\operatorname*{lim}_{k\rightarrow\infty}P_{k}=\Psi_{22}\Psi_{12}^{-1}$$
sk = *PkZk* (7.97) 
Combining the two previous equations shows that This gives us a way to determine the steady-state solution of the Riccati equation solution. However, this analysis assumed that A was a diagonal matrix with all elements outside the unit circle. In other words, if the Hamiltonian matrix has any eigenvalues with magnitude equal to one, then this analysis falls apart. This gives the following algorithm for computing the steady-state, discretetime Riccati equation solution. 

## The Hamiltonian Approach To Steady-State Kalrnan Filtering

Form the Hamiltonian matrix 

$${\cal H}=\left[\begin{array}{cc}F^{-T}&F^{-T}H^{T}R^{-1}H\\ QF^{-T}&F+QF^{-T}H^{T}R^{-1}H\end{array}\right]\tag{7.99}$$

For an n-state Kalman filtering problem, the Hamiltonian matrix will be a 2n x 2n matrix. 

Compute the eigenvalues of 'H. If any of them are on the unit circle, then we cannot go any further with this procedure; the Riccati equation does not have a steady-state solution. Collect the n eigenvectors that correspond to the n eigenvalues that are outside the unit circle. Put these n eigenvectors in a matrix partitioned as 

$$\begin{array}{l}{{\Psi_{12}}}\\ {{\Psi_{22}}}\end{array}\Biggr]$$
$$(7.100)$$

$$(7.101)$$

The first column of this matrix is the first eigenvector, the second column is the second eigenvector, etc. Q12 and **Qzz** are both n x n matrices. 

Compute the steady-state Riccati equation solution as PZ = Q22Q;; **(7.101)** 
Note that Ql2 must be invertible for this method to work. 

The Hamiltonian approach to steady-state filtering is due to [Vau70], which also derives time-varying DARE solutions using Hamiltonian matrices. 

## Example **7.9**

Consider the scalar system of Equation **(7.36):** 

$$P_{\infty}^{-}=\Psi_{22}\Psi_{12}^{-1}$$
$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{N(0,1)}}\\ {{v_{k}}}&{{\sim}}&{{N(0,1)}}\end{array}$$
$$(7.102)$$

wk **N(O,1) (7.102)** 
We see that F = H = Q = R = 1. Substituting these values into the expression for the Hamiltonian matrix gives 

$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{\mathcal{H}}}&{{=}}&{{\left[\begin{array}{l l}{{F^{-T}}}&{{F^{-T}H^{T}R^{-1}H}}\\ {{Q F^{-T}}}&{{F+Q F^{-T}H^{T}R^{-1}H}}\end{array}\right]}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{1}}\\ {{1}}&{{2}}\end{array}\right]}}\end{array}$$
$$(7.103)$$

The eigenvalues of 3-t are 0.38 and 2.62. None of the eigenvalues has a magnitude of one so we are able to continue with the procedure. The eigenvector of 'FI that corresponds to the eigenvalue outside the unit circle is 
[ 0.5257 0.8507 1'. We form the corresponding eigenvector matrix as 

$${\left[\begin{array}{l}{\Psi_{12}}\\ {\Psi_{22}}\end{array}\right]}={\left[\begin{array}{l}{0.5257}\\ {0.8507}\end{array}\right]}$$

Note that **912** is invertible so we are able to continue with the problem. The steady-state Riccati equation solution is 

$$(7.104)$$
$$\begin{array}{r c l}{{P}}&{{=}}&{{\Psi_{22}\Psi_{12}^{-1}}}\\ {{}}&{{}}&{{=}}&{{\frac{0.8507}{0.5257}}}\\ {{}}&{{}}&{{=}}&{{1.62}}\end{array}$$
$$(7.105)$$
$$(7.106)$$
= 1.62 (7.105) 
The steady-state Kalman gain is therefore computed from Equation (7.14) as 

$K=PH^{T}(HPH^{T}+R)^{-1}$  $=$$(1.62)(1)$  $(1)(1.62)(1)+1$  $=$$0.62$
which is in agreement with Equation (7.37). 

vvv 

## 7.4 Kalman Filtering With Fading Memory

In Section 5.5, we discussed the problem of filter divergence due to mismodeling. That is, if our system model does not match reality, then the Kalman filter estimate may diverge from the true state. Example 5.3 showed how the addition of fictitious process noise can compensate for mismodeling. In this section, we show how to accomplish the same thing with the fading-memory filter. Recall our linear discretetime system model: 

$$\begin{array}{rcl}x_{k}&=&F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}\\ y_{k}&=&H_{k}x_{k}+v_{k}\\ w_{k}&\sim&(0,Q_{k})\\ v_{k}&\sim&(0,R_{k})\\ E[w_{k}w_{j}^{T}]&=&Q_{k}\delta_{k-j}\\ E[v_{k}v_{j}^{T}]&=&R_{k}\delta_{k-j}\\ E[w_{k}v_{j}^{T}]&=&0\end{array}$$
$$(7.107)$$
$$(7.108)$$
The Kalman filter finds the sequence of estimates *{2;,* - - a, *2;)* that minimizes 
E(JN), where JN is given as 
$$J_{N}=\sum_{k=1}^{N}\left[(y_{k}-H_{k}\hat{x}_{k}^{-})^{T}R_{k}^{-1}(y_{k}-H_{k}\hat{x}_{k}^{-})+\hat{w}_{k}^{T}Q_{k}^{-1}\hat{w}_{k}\right]$$

Note that 2 determines 6 through the system equation, and vice versa. This expression for JN shows how we could give greater emphasis to more recent data. Instead of finding the filter that minimizes *E(JN),* we can find the filter that minimizes E(~N), where JN is given as 

$$\tilde{J}_{N}=\sum_{k=1}^{N}\left[(y_{k}-H_{k}\hat{x}_{k}^{-})^{T}\alpha^{2k}R_{k}^{-1}(y_{k}-H_{k}\hat{x}_{k}^{-})+\hat{w}_{k}^{T}\alpha^{2k+2}Q_{k}^{-1}\hat{w}_{k}\right]\tag{7.109}$$

where a 2 1. The 0 term in the first part of the cost function means that we are more interested in minimizing the weighted covariance of the residual at recent times (large values of k) than at times in the distant past (small values of *k).* This will force the filter to converge to state estimates that discount old measurements and give greater emphasis to more recent measurements. The cr term in the second part of the cost function is added for mathematical tractability, as we will see in the subsequent development. The second part of the cost function is constant as far as our minimization problem is concerned. 

The solution to the minimization of *E(.?N)* is equivalent to the minimization of E(JN) (which is the Kalman filter), except that Rk is replaced with *ff-2kRk* and Qk is replaced with *ff-2k-2Qk.* The modified Kalman gain can therefore be written a5 

$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+\alpha^{-2k}R_{k})^{-1}}}\\ {{}}&{{=}}&{{\alpha^{2k}P_{k}^{-}H_{k}^{T}(H_{k}\alpha^{2k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}}}\end{array}$$
The time update for the estimation-error covariance can be written as 
$$(7.110)$$
$$\begin{array}{r c l}{{P_{k}^{-}}}&{{=}}&{{F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+\alpha^{-2k+2}Q_{k-1}/\alpha^{2}}}\\ {{\alpha^{2k}P_{k}^{-}}}&{{=}}&{{F_{k-1}\alpha^{2k}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}}}\\ {{}}&{{=}}&{{\alpha^{2}F_{k-1}\alpha^{2(k-1)}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}}}\end{array}$$

The measurement update for the estimation-error covariance can be written as 

$$(7.111)$$
the for the estimation-error covariance can be written  $\begin{array}{rcl}P_k^+&=&P_k^--K_k H_k P_k^-\\ \alpha^{2k}P_k^+&=&\alpha^{2k}P_k^--K_k H_k\alpha^{2k}P_k^-\end{array}$  $\tilde{P}_k^-$ as 
$$(7.112)$$
$$(7.113)$$
Now we define pz and *f';* as 
$$\begin{array}{r c l}{{\tilde{P}_{k}^{+}}}&{{=}}&{{\alpha^{2k}P_{k}^{+}}}\\ {{\tilde{P}_{k}^{-}}}&{{=}}&{{\alpha^{2k}P_{k}^{-}}}\end{array}$$

We can then write Equations (7.110), (7.111), and (7.112) as 

$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{\tilde{P}_{k}^{-}H_{k}^{T}(H_{k}\tilde{P}_{k}^{-}H_{k}^{T}+R_{k})^{-1}}}\\ {{\tilde{P}_{k}^{-}}}&{{=}}&{{\alpha^{2}F_{k-1}\tilde{P}_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}}}\\ {{\tilde{P}_{k}^{+}}}&{{=}}&{{\tilde{P}_{k}^{-}-K_{k}H_{k}\tilde{P}_{k}^{-}}}\end{array}$$
These are the new Kalman gain equation and covariance-update equations. The 
state-update equations remain as before: 
$$(7.114)$$
$$\begin{array}{r c l}{{\hat{x}_{k}^{-}}}&{{=}}&{{F_{k-1}\hat{x}_{k-1}^{+}+G_{k-1}u_{k-1}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})}}\end{array}$$
$$(7.115)$$

We see that the fading-memory filter is identical to the standard Kalman filter, with the exception that the time-update equation for the computation of the a *priori* estimation-error covariance has an o2 factor in its first term. This serves to increase the uncertainty in the state estimate, which results in the filter giving more credence to the measurement. This is equivalent to increasing the process noise, which also results in the filter giving relatively more credence to the measurement. This strategy, along with other solutions to the filter divergence problem, was suggested early in the history of the Kalman filter [Sch67, Sor7laI. The fading-memory filter can be summarized as follows. 

## The Fading-Memory Filter

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{E(w_{k}w_{j}^{T})}}&{{=}}&{{Q_{k}\delta_{k-j}}}\\ {{E(v_{k}v_{j}^{T})}}&{{=}}&{{R_{k}\delta_{k-j}}}\\ {{E(w_{k}v_{j}^{T})}}&{{=}}&{{0}}\end{array}$$

1. The dynamic system is given by the following equations: 
2. The Kalman filter is initialized as follows: 

$$(7.116)$$
$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E(x_{0})}}\\ {{\hat{P}_{0}^{+}}}&{{=}}&{{E[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}]}}\end{array}$$
$$(7.117)$$

3. Choose Q 2 1 based on how much you want the filter to forget past measurements. If Q = 1 then the fading-memory filter is equivalent to the standard Kalman filter. In most applications, Q is only slightly greater than 1 (for example, Q x 1.01). 

puted for each time step k = 1,2, **e a e:** 
4. The fading-memory filter is given by the following equations, which are com-

pi = Q2Fk-ipz-lF~-1 -k Qk-1  Kk = PiHr(HkpFHr + Rk)-'  = PZH~R~~  2i = Fk-l*l-l -k Gk-iUk-1  2' k = 2i f Kk(Yk - Hk?;)  pz = (I - KkHk)&(I - KkHk)T + KkRkKT 
Note that p is not equal to the covariance of the estimation error. However, the fading-memory filter is more robust to modeling errors than the standard Kalman filter. 

$$x_{k}=$$
$$\begin{array}{r l}{y_{k}}&{{}=}\\ {v_{k}}&{{}\subset}\end{array}$$

## 4 **Example** 7.10

In this example, we will show how the fading-memory filter makes the Kalman filter more responsive to measurements when the process noise is zero. Consider the following scalar system: 

(7.119) 

In other words, we are trying to estimate a constant on the basis of noisy measurements of that constant. Applying the fading-memory filter equations given in Equation (7.118) to this problem, we see that 

$$(7.120)$$
$$P_{\infty}^{+}=\alpha^{2}P_{\infty}^{+}-\left(\frac{\alpha^{2}P_{\infty}^{+}}{\alpha^{2}P_{\infty}^{+}+R}\right)\alpha^{2}P_{\infty}^{+}$$

As the filter approaches steady state, *Pk+* approaches a steady-state value that can be obtained from the above equation as 

$$(7.121)$$

This can be solved for P& as 

$$(7.122)$$

The steady-state Kalman gain K, can then be solved EM 

$$P_{\infty}^{+}={\frac{(\alpha^{2}-1)R}{\alpha^{2}}}$$
$$\begin{array}{r c l}{{K_{\infty}}}&{{=}}&{{\frac{\alpha^{2}P_{\infty}^{+}}{\alpha^{2}P_{\infty}^{+}+R}}}\\ {{}}&{{=}}&{{\frac{\alpha^{2}-1}{\alpha^{2}}}}\end{array}$$

$$(7.123)$$

We see that if a = 1 (i.e., if we use the standard Kalman filter) then P& = K, = 0. However, if a > 1 (i.e., if we use the fading-memory Kalman filter) 
then P& and K, will both be greater than zero. The measurement update equation for the state is given as 

$$(7.124)$$
$${\hat{x}}_{k}^{+}={\hat{x}}_{k}^{-}+K_{k}(y_{k}-{\hat{x}}_{k}^{-})$$

For the standard Kalman filter, limk,, Kk = 0, which means that new measurements will be ignored and will not be used to update the state estimate. 

The Kalman filter may have a false confidence in the certainty of its state estimate. However, for the fading-memory filter, Kk > 0 for all k, and the filter will always be responsive to new measurements. A larger value of a will make the filter more responsive to new measurements. In the limit as a + *00,* 
we see from Equation (7.123) that K, = 1. This will result in a measurement update from Equation (7.124) of 

$$(7.125)$$
$$\begin{array}{r c l}{{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}+(1)(y_{k}-\hat{x}_{k}^{-})}}\\ {{}}&{{=}}&{{y_{k}}}\end{array}$$

In other words, the fading-memory filter, when carried to an extreme, ignores the system model and estimates the state solely on the basis of the mea surements. This is the same thing that will happen if the process noise is extremely large. The Kalman filter will ignore the system model because we are telling it that we do not have any confidence in the system model. 

vvv 

## 7.5 Constrained Kalman Filtering

In the application of state estimators, there is often known information that does not fit into the Kalman filter equations in an obvious way. For example, suppose that we know (on the basis of physical considerations) that the states satisfy some equality constraint *Da:* = d, or some inequality constraint *Da:* 5 d, where D is a known matrix and d is a known vector. This section discusses some ways of incorporating those constraints into the Kalman filter equations. 

Some researchers have treated state equality constraints by reducing the system model parameterization [Wen92], and this will be discussed in Section 7.5.1. 

Others have handled state equality constraints by treating them as perfect measurements [Por88, Hay981, and this will be discussed in Section 7.5.2. A third approach is to incorporate the state constraints into the derivation of the Kalman filter [Chi85, Sim021, and this will presented in Section 7.5.3. A final approach is to incorporate the constraints by discarding that portion of the pdf of the state estimate that violates the constraints [Shi98, SimOGb], and this will be discussed in Section 7.5.4. 

## 7.5.1 Model Reduction

Some researchers have treated state equality constraints by reducing the system model parameterization [Wen92]. This is straightforward but there are some disadvantages with this approach. First, it may be desirable to maintain the form and structure of the state equations due to the physical meaning associated with each state. The reduction of the state equations makes their interpretation less natural and more difficult. Second, equality constraints that are formulated this way cannot be extended to inequality constraints. On the other hand, the model reduction approach is conceptually straightforward and usually can be easily implemented. 

$$(7.126)$$

As an example of the model reduction approach, consider the system 

Zk+l = [j 4 -2 : 2 'Izk+[;;;]  Yk = [2 4 5]zk+Vk (7.126) 
$\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0$ (7.127)  $\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0$ (7.127)  $\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0$ (7.127)  $\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0$ (7.127)  $\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0$ (7.127)  \(\left[\begin{array}{cccc}1&0&1\end{array}\right]x_{k}=0\
$$x_{k+1}(1)$$  $$x_{k+1}(2)$$
Now suppose that we also know, on the basis of our understanding of the physics underlying the problem, that the following constraint is always satisfied between the states: **[l 0 l]Xk=o (7.127)** 
This means that xk(3) = **-xk(1).** If we make this substitution for **zk(3)** in the original state and measurement equations, we obtain 

$$(1)=x_{k}(1)+2x_{k}(2)-3x_{k}(1)\tag{1}$$ $$=-2x_{k}(1)+2x_{k}(2)$$ $$=3x_{k}(1)+2x_{k}(2)-x_{k}(1)$$ $$=2x_{k}(1)+2x_{k}(2)$$ $$y_{k}=2x_{k}(1)+4x_{k}(2)-5x_{k}(1)+v_{k}$$ $$=-3x_{k}(1)+4x_{k}(2)+v_{k}\tag{7.128}$$

These equations can be written in matrix form as 

$\frac{1}{2}$  . 
$$\begin{array}{rcl}\mathcal{I}_{k+1}&=&\left[\begin{array}{cc}-2&2\\ 2&2\end{array}\right]\mathcal{I}_{k}+\left[\begin{array}{c}w_{k1}\\ w_{k2}\end{array}\right]\\ \mathcal{I}_{k}&=&\left[\begin{array}{cc}-3&4\end{array}\right]\mathcal{I}_{k}+\mathcal{I}_{k}\end{array}\tag{7.129}$$
We have reduced the filtering problem with equality constraints to an equivalent but unconstrained filtering problem. An advantage of this approach is that the dimension of the problem has been reduced, and so the computational effort of the problem is less. One disadvantage of this approach is that the physical meaning of the state variables has been lost. Also, this approach can only be used for equality constraints (i.e., constraints of the form Dx = d) and cannot be used for inequality constraints (i.e., constraints of the form Dz I *d).* 

## 7.5.2 Perfect Measurements

Some researchers treat state constraints as perfect measurements (i.e., no measurement noise) [Por88, Hay981. Suppose that our constraints are given as *Dzk* = d, where D is a known s x n matrix (s < *n),* and d is a known vector. We can solve the constrained Kalman filtering problem by augmenting the measurement equation with s perfect measurements of the state: 

$$\begin{array}{rcl}\mathbf{x}_{k+1}&=&F_{k}\mathbf{x}_{k}+\mathbf{w}_{k}\\ \left[\begin{array}{c}\mathbf{y}_{k}\\ d\end{array}\right]&=&\left[\begin{array}{c}H_{k}\\ D\end{array}\right]\mathbf{x}_{k}+\left[\begin{array}{c}\mathbf{v}_{k}\\ 0\end{array}\right]\end{array}\tag{7.130}$$

The state equation is the same as usual, but the measurement equation has been augmented. The fact that the last s elements of the measurement equation are noise free means that the Kalman filter estimate of the state will always be consistent with these s measurements; that is, the Kalman filter estimate will always be consistent with the constraint 02: = d. Note that the new measurement noise covariance will be singular - the last s rows and the last s columns of the measure ment noise covariance will be zero. A singular covariance matrix does not present any theoretical problems [Gee97]. In fact, Kalman's original paper [Ka160] presents an example that uses perfect measurements. However, in practice a singular covariance increases the possibility of numerical problems [May79, p. 2491, [Ste94, p. 3651. In addition, the use of perfect measurements is directly applicable only to equality constraints. It can be extended to inequality constraints by adding small nonzero measurement noise to the "perfect" measurements, but then the constraints will be soft [MahOla] and it will be difficult to control how close the state estimate gets to the constraint boundary. 

## 7.5.3 Projection Approaches

Another approach to constrained filtering is to incorporate the state constraints into the derivation of the Kalman filter [Chi85, Sim021. We can incorporate the constraints into a maximum probability derivation of the filter, or a mean square derivation of the Kalman filter. Also, we can simply project the standard Kalman filter estimate onto the constraint surface. 

7.5.3.1 Maximum probability approach Assuming that **20,** Wk, and Vk are Gaussian, the Kalman filter solves the problem 

$${\hat{x}}_{k}=\operatorname{argmax}_{x_{k}}\operatorname{pdf}(x_{k}|Y_{k})$$

That is, ik is the value of Xk that maximizes pdf(zk1Yk). In the above equation, Yk is the vector of measurements up to and including time k; that is, Yk = 
[ y? . - y: 1'. This interpretation of the Kalman filter looks at Xk as a random variable with a pdf that is conditioned on the measurements up to and including time k. The Kalman filter estimate is that value of Xk that maximizes its conditional pdf. If the noise processes are Gaussian, then 

$$(7.131)$$
$${\rm pdf}(x_{k}|Y_{k})=\frac{\exp[-(x_{k}-\bar{\bar{x}}_{k})^{T}P_{k}^{-1}(x_{k}-\bar{\bar{x}}_{k})/2]}{(2\pi)^{n/2}|P_{k}|^{1/2}}\tag{7.132}$$
$$(7.133)$$

where n is the dimension of the state, Pk is the covariance of the state estimate, and zk is defined as the mean of Xk conditioned on the measurements Yk: 

$${\hat{x}}_{k}=E(x_{k}|Y_{k})$$
zk = E(xl,IYk) (7.133) 
To maximize pdf(xkIYk), we can maximize lnpdf(xr,lYk), which means minimizing 
(zk - zk)'Pi'(xk - zk). Now suppose that we have the additional constraint that Dxk = d. The solution of this constrained minimization problem is the constrained state estimate 2. That is, 

$$\tilde{x}_{k}=\mbox{argmin}_{\tilde{x}_{k}}(\tilde{x}_{k}-\tilde{x}_{k})^{T}P_{k}^{-1}(\tilde{x}_{k}-\tilde{x}_{k})\mbox{such that}D\tilde{x}_{k}=d\tag{7.134}$$

Constrained optimization problems can be solved using the Lagrange multiplier method discussed in Section 11.2 [Ste94, MooOO]. We form the Lagrangian L and 

$$(7.135)$$
$$(7.136)$$

find the necessary conditions for a minimum as follows: 

ary conditions for a minimum as follows:  $$L=(\tilde{x}_{k}-\tilde{x}_{k})^{T}P_{k}^{-1}(\tilde{x}_{k}-\tilde{x}_{k})+2\lambda^{T}(D\tilde{x}_{k}-d)$$ $$\frac{\partial L}{\partial\tilde{x}}=P_{k}^{-1}(\tilde{x}_{k}-\tilde{x}_{k})+D^{T}\lambda=0$$ $$\frac{\partial L}{\partial\lambda}=D\tilde{x}_{k}-d=0$$
where X is the n-element Lagrange multiplier. Solving these equations gives 
$$\begin{array}{r c l c l}{{}}&{{}}&{{}}&{{}}\\ {{\lambda}}&{{=}}&{{(D P_{k}D^{T})^{-1}(D\hat{x}_{k}-d)}}\\ {{}}&{{=}}&{{(D P_{k}D^{T})^{-1}(D\hat{x}_{k}-d)}}\\ {{\hat{x}_{k}}}&{{=}}&{{\hat{x}_{k}-P_{k}D^{T}\lambda}}\\ {{}}&{{=}}&{{\hat{x}_{k}-P_{k}D^{T}(D P_{k}D^{T})^{-1}(D\hat{x}_{k}-d)}}\\ {{}}&{{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}&{{}}\end{array}$$
We see that the constrained state estimate 5 is equal to the unconstrained state estimate 2, minus a correction term. 

7.5.3.2 Least squares approach Another way to solve the constrained Kalman filtering problem is to approach the problem from a least squares point of view. In this approach, we find the constrained state estimate 5 as 5 = argmin5E( **112** - 51 1'1Y) such that D5 = d **(7.137)** 
where we have dropped the time subscripts for ease of notation. This interpretation of the Kalman filter looks at z as a random variable. The quantity (z - 5) (for any constant 5) is also a random variable. The conditional expected value can be written as 

$${\tilde{x}}=\operatorname{argmin}_{\tilde{x}}E(||x-{\tilde{x}}||^{2}|Y){\mathrm{~such~that~}}D{\tilde{x}}=d$$
$$\begin{array}{r l}{E(||x-{\tilde{x}}||^{2}|Y)=\int(x-{\tilde{x}})^{T}(x-{\tilde{x}})\operatorname{pdf}(x|Y)\,d x}\\ {=}&{{}\int x^{T}x\operatorname{pdf}(x|Y)\,d x-2{\tilde{x}}\int x\operatorname{pdf}(x|Y)\,d x+{\tilde{x}}^{T}{\tilde{x}}}\end{array}$$
$$(7.137)$$
$$(7.138)$$
$$(7.139)$$
$$(7.140)$$

We form the Lagrangian for the constrained optimization problem as 

L = E(llz - 511'1Y) + 2XT(D5 - d)  = / zTz pdf(z1Y) dz - 25 z pdf(a:IY) dz + ZT5 +  s  2XT(D2 - d) (7.139) 
$$(7.141)$$
Assuming that 20, *Wk,* and Wk are Gaussian, the standard Kalman filter estimate 2 is given by 

$$\begin{array}{r c l}{{\hat{x}}}&{{=}}&{{E(x|Y)}}\\ {{}}&{{=}}&{{\int x\operatorname{pdf}(x|Y)\,d x}}\end{array}$$

Solving the constrained minimization problem involves setting the partial derivatives of the Lagrangian of Equation **(7.139)** equal to zero. This gives the equations 

dL - = -2f+25+2DTX=0 
$$\begin{array}{r c l}{{\frac{\partial L}{\partial{\tilde{x}}}}}&{{=}}&{{-2{\hat{x}}+2{\tilde{x}}+2D^{T}\lambda=0}}\\ {{\frac{\partial L}{\partial\lambda}}}&{{=}}&{{D{\tilde{x}}-d=0}}\end{array}$$
Solving these equations for X and Z gives 

$$\begin{array}{r c l}{{\lambda}}&{{=}}&{{(D D^{T})^{-1}(D\hat{x}-d)}}\\ {{\hat{x}}}&{{=}}&{{\hat{x}-D^{T}(D D^{T})^{-1}(D\hat{x}-d)}}\end{array}$$
$$(7.142)$$

We see that the constrained state estimate P is equal to the unconstrained state estimate P, minus a correction term. This is similar to the constrained estimate that was obtained by the maximum probability approach in Equation (7.136). 

7.5.3.3 General projection approach A third way to derive the constrained state estimate is to begin with the standard unconstrained estimate P and project it onto the constraint surface Dx = d. This can be written as 

$${\hat{x}}=\operatorname{argmin}_{\tilde{x}}({\tilde{x}}-{\hat{x}})^{T}W({\tilde{x}}-{\hat{x}}){\mathrm{~such~that~}}D{\tilde{x}}=d$$
2 = argminz(Z - *P)TW(Z* - 2) such that DZ = d (7.143) 
where W is any positive definite weighting matrix. [W is chosen to weight various elements of the difference (5 - **3).** This is generally based on the designer's relative confidence in the elements of the unconstrained state estimate.] The solution to the above problem is 

$$(7.143)$$
$$\tilde{x}=\hat{x}-W^{-1}D^{T}(D W^{-1}D^{T})^{-1}(D\hat{x}-d)$$
$$(7.144)$$

This is the most general approach to the problem. Note that the maximum probability estimate of Equation (7.136) is equal to this if we set W = *P-'.* The mean square estimate of Equation (7.142) is equal to this if we set W = I. 

It is shown in [Chi85, Sim021 that the constrained state estimate of Equation (7.144) has several interesting properties. 

1. The constrained estimate is unbiased. That is, *E(Z)* = E(x). 

2. Setting W = *P-l* results in the minimumvariance filter. That is, if W = *P-'* 
then Cov(x - Z) 5 Cov(x - 2) for all 2. 

3. Setting W = I results in a constrained estimate that is always (i.e., at each time step) closer to the true state than the unconstrained estimate. That is, if W = I then I lxk - *Pk]* 12 5 I1q - hk **112** for all k. 

The projection approach to constrained filtering has the advantage that it can be easily extended to inequality constraints. That is, if we have the constraints Dx 5 d, then the constrained estimate can be obtained by modifying Equation (7.143) and solving the problem 

$$\hat{\mathbf{x}}=\mbox{argmin}_{\hat{\mathbf{x}}}(\hat{\mathbf{x}}-\hat{\mathbf{x}})^{T}W(\hat{\mathbf{x}}-\hat{\mathbf{x}})\mbox{such that}D\hat{\mathbf{x}}\leq d\tag{7.145}$$

The problem defined above is known as a quadratic programming problem [Fle81, Gi1811. There are several algorithms for solving quadratic programming problems, most of which fall in the category known as active set methods. An active set method **uses** the fact that it is only those constraints that are active at the solution of the problem that are significant in the optimality conditions. Assume that we have s inequality constraints (i.e., D has s rows), and q of the s inequality constraints are active at the solution of Equation (7.145). Denote by l? and d^ the q rows of D and q elements of d corresponding to the active constraints. If the correct 

$$(7.146)$$

set of active constraints was known a *priori* then the solution of Equation **(7.145)** 
would also be a solution of the equality constrained problem 

$${\tilde{x}}=\operatorname{argmin}_{{\tilde{x}}}({\tilde{x}}-{\hat{x}})^{T}W({\tilde{x}}-{\hat{x}}){\mathrm{~such~that~}}{\hat{D}}{\tilde{x}}={\hat{d}}$$

This shows that the inequality constrained problem of Equation **(7.145)** is equivalent to the equality constrained problem of Equation **(7.146).** Therefore, all of the properties of the equality constrained state estimate enumerated above also apply to the inequality constrained state estimate. Standard quadratic programming routines2 can be used to solve inequality constrained problems that are in the form of Equation (7.145). 

Suppose that we have an unconstrained estimate and covariance given as 

$$\begin{array}{r c l}{{\hat{x}}}&{{=}}&{{\left[\begin{array}{l}{{3}}\\ {{3}}\end{array}\right]}}\\ {{P}}&{{=}}&{{\left[\begin{array}{l l}{{2}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]}}\end{array}$$

[: ;] **(7.147)** 
That is, we are twice as certain of our 22 estimate as we are of our XI estimate. We also know (from our understanding of the underlying system) that the state must satisfy the constraint 

$$(7.147)$$
$$\begin{array}{r l r l}{D x}&{{}=}&{d}\\ {{\left[\begin{array}{l l}{1}&{1}\end{array}\right]}\,x}&{{}=}&{1}\end{array}$$
$$(7.148)$$
$$\hat{\vec{x}}_{LS}=\hat{x}-D^{T}(DD^{T})^{-1}(D\hat{x}-d)\tag{7.149}$$ $$=\left[\begin{array}{c}3\\ 3\end{array}\right]-\left[\begin{array}{c}1\\ 1\end{array}\right]\left(\left[\begin{array}{cc}1&1\end{array}\right]\left[\begin{array}{c}1\\ 1\end{array}\right]\right)^{-1}\left(\left[\begin{array}{cc}1&1\end{array}\right]\left[\begin{array}{c}3\\ 3\end{array}\right]-1\right)$$ $$=\left[\begin{array}{c}1/2\\ 1/2\end{array}\right]$$

Clearly, the unconstrained estimate does not satisfy this constraint. The least squares approach to constrained estimation uses Equation **(7.142)** to compute the constrained estimate as We see that the estimates for x1 and 22 both changed by the same amount 
(from the unconstrained values of 3, to the constrained values of **1/2).** The maximum probability approach to constrained estimation uses Equation **(7.136)** 
to compute the constrained estimate as 

$$\tilde{\tilde{x}}_{MP}=\hat{x}-PD^{T}(DPD^{T})^{-1}(D\hat{x}-d)\tag{7.150}$$ $$=\left[\begin{array}{c}-1/3\\ 4/3\end{array}\right]$$

The estimate for x1 changed by **10/3** (from the unconstrained value of 3, to the constrained value of **-1/3).** The estimate for 22 changed by **5/3.** We see 2For example, the QP function in MATLAB's Optimization Toolbox. 

that the estimate for XI changed twice as much as the estimate for **22,** because the certainty of the unconstrained 22 estimate was twice the certainty of the unconstrained XI estimate. This is illustrated in Figure **7.1.** 

![35_image_0.png](35_image_0.png)

Figure **7.1** In Example 7.11, the unconstrained estimate violates the equality constraint. 

The least squares approach to constrained estimation projects the estimate in the direction perpendicular to the constraint surface. The maximum probability approach projects the estimate in the direction *P-l* relative to the constraint surface. 

## Vvv 7.5.4 A Pdf Truncation Approach

In the projection approach to constrained estimation discussed in the previous section, the state estimates are projected onto the constraint surface. In the pdf truncation approach, we take the probability density function that is computed by the Kalman filter (assuming that it is Gaussian) and truncate it at the constraint edges. The constrained state estimate then becomes equal to the mean of the truncated pdf [Shi98, SimOGb] . This approach is designed for inequality constraints on the state, although it can also be applied to equality constraints. 

Suppose that at time k we have the s scalar state constraints 

$$(7.151)$$
$$i=1,\ldots,s$$
i = **1,.** . . , s **(7.151)** T 
$$a_{k i}\leq\phi_{k i}^{T}x_{k}\leq b_{k i}$$

where akz < *bkz.* This is a two-sided constraint on the linear function of the state 
$zt2k. If we have a one-sided constraint, then we set *akz* = --oo or *bkz* = +m. 

Now suppose at time k that we have a standard Kalman filter estimate Pk with covariance *Pk.* The problem is to truncate the Gaussian pdf *N(&,Pk)* at the s constraints given in Equation **(7.151),** and then find the mean zk and covariance pk of the truncated pdf. These new quantities, zk and &, become the constrained state estimate and its covariance. 

In order to make the problem tractable, we will define &, as the state estimate after the first i constraints of **(7.151)** have been enforced, and *ijkr* as the covariance of *Zka.* We therefore initialize 

$$(7.152)$$
$$(7.153)$$
$$(7.154)$$

Now perform the following transformation: 

$$\begin{array}{r c l}{{i}}&{{=}}&{{0}}\\ {{\tilde{x}_{k i}}}&{{=}}&{{\hat{x}_{k i}}}\\ {{\tilde{P}_{k i}}}&{{=}}&{{P_{k i}}}\end{array}$$
$$z_{k t}=\rho W^{-1/2}T^{T}(x_{k}-\tilde{x}_{k t})$$
$$T W T^{T}={\tilde{P}}_{k_{1}}$$
Zka = pW-'/2TT(2k - *5ka)* **(7.153)** 
p is an orthogonal n x n matrix that will be determined later, and T and W are obtained from the Jordan canonical decomposition of &. This transformation will allow us to solve the pdf truncation problem that we have posed, and find the mean of the pdf as the estimated state after i constraints have been enforced. From the description of T and W we know that TWTT = 4% **(7.154)** 
T is orthogonal and W is diagonal (therefore, its square root is very easy to compute). Next we use Gram-Schmidt orthogonalization [MooOO] to find the orthogonal p matrix that satisfies 

$$\rho W^{1/2}T^{T}\phi_{k_{1}}=\left[\begin{array}{c c c c}{{(\phi_{k_{1}}^{T}\tilde{P}_{k_{1}}\phi_{k_{1}})^{1/2}}}&{{0}}&{{\cdots}}&{{0}}\end{array}\right]^{T}$$
$$\rho=$$

The Gram-Schmidt orthogonalization procedure for computing p is given as follows. 

1. Suppose that p is an n x n matrix with rows pi (i = **1,.** - -, *n):* 

$$(7.155)$$
$$(7.156)$$
$$\left[\begin{array}{l}{{\rho_{1}}}\\ {{\vdots}}\\ {{\vdots}}\\ {{\rho_{n}}}\end{array}\right]$$

The first row of p is computed as 

$$(7.157)$$
$$(7.158)$$

2. For k = 2, - a, n, perform the following. 

(a) Compute the kth row of p as follows: 

$$\rho_{1}=\frac{\phi_{k_{1}}^{T}T W^{1/2}}{(\phi_{k_{1}}^{T}\tilde{P}_{k i}\phi_{k i})^{1/2}}$$
$$\rho_{k}=e_{k}-\sum_{i=1}^{k-1}(e_{k}^{T}\rho_{i})\rho_{i}$$

where ek is the unit vector; that is, ek is an n-element column vector comprised entirely of zeros, except that its kth element is a 1. 

$$e_{k}=\left[\begin{array}{c}0\\ \vdots\\ 0\\ 1\\ 0\\ \vdots\\ 0\end{array}\right]\gets k\mbox{th element}\tag{7.1}$$
$$(7.159)$$

(b) If the pk computed above is zero, then replace it with the following: 

$\rho_{k}=e_{1}-\sum_{i=1}^{k-1}(e_{1}^{T}\rho_{i})\rho_{i}$ (7.160)
(c) Normalize *Pk:* 
$\rho_{k}=\frac{\rho_{k}}{||\rho_{k}||_{2}}$ (7.161)
$$\begin{array}{c}{{\phi_{k_{1}}^{T}x_{k_{1}}}}\\ {{\phi_{k_{1}}^{T}T W^{1/2}\rho^{T}z_{k_{1}}+\phi_{k_{1}}^{T}\tilde{x}_{k_{1}}}}\\ {{\frac{(\phi_{k_{1}}^{T}T W^{1/2}\rho^{T})z_{k_{1}}}{(\phi_{k_{1}}^{T}\tilde{P}_{k_{1}}\phi_{k_{1}})^{1/2}}}}\\ {{\left[\begin{array}{c c c}{{1}}&{{0}}&{{\cdots}}&{{0}}\end{array}\right]z_{k_{1}}}}\end{array}$$
It can be shown from Equations (7.153)-(7.155) that **zkz** has a mean of 0 and covariance matrix of identity. With these definitions we see that the upper bound of Equation (7.151) is transformed as follows: 

$\leq$$b_{ki}$$\leq$$b_{ki}$$\leq$$b_{ki}-\phi_{ki}^{T}\tilde{x}_{ki}$$\leq$$(\phi_{ki}^{T}\tilde{P}_{ki}\phi_{ki})^{1/2}$$\leq$$b_{ki}-\phi_{ki}^{T}\tilde{x}_{ki}$$\leq$$(\phi_{ki}^{T}\tilde{P}_{ki}\phi_{ki})^{1/2}$$\leq$$d_{ki}$$\leq$$(7.162)$
$$\begin{array}{r l}{{\left[\begin{array}{l l l l}{1}&{0}&{\cdots}&{0}\end{array}\right]z_{k_{1}}}}&{{\geq}}&{{{\frac{a_{k_{1}}-\phi_{k_{1}}^{T}{\tilde{x}}_{k_{1}}}{(\phi_{k_{1}}^{T}{\tilde{P}}_{k_{1}}\phi_{k_{1}})^{1/2}}}}}\\ {{}}&{{\geq}}&{{c_{k_{1}}}}\end{array}$$
where *dkz* is defined by the above equation. Similarly we can see that 

$$(7.163)$$

$$(7.164)$$

where *Ckz* is defined by the above equation. We therefore have the normalized scalar constraint 
$c_{k_{1}}\leq[\ 1\ 0\ \cdots\ 0\ ]\ z_{k_{1}}\leq d_{k_{1}}$
Since *Zkz* has a covariance of identity, its elements are statistically independent of each other. Only the first element of *.Zk,* is constrained, so the pdf truncation 
reduces to a one dimensional pdf truncation. The first element of *Zkz* is distributed 
as N(0,l) (before constraint enforcement), but the constraint says that *Zkz* must lie between *ckz* and **dkz.** We therefore remove that part of the Gaussian pdf that is outside of the constraints and compute the area of the remaining portion of the pdf as 
$$\int_{c_{k_{k}}}^{d_{k_{k}}}\frac{1}{\sqrt{2\pi}}\exp(-\zeta^{2}/2)\,d\zeta=\frac{1}{2}\left[\mbox{erf}(d_{i}(k)/\sqrt{2})-\mbox{erf}(c_{k_{i}}/\sqrt{2})\right]\tag{7.165}$$
- exp(-C2/2) dC = [erf(di(k)/fi) - erf(ckz/fi)] (7.165) 
where erf(.) is the error function, defined as 
erf(t) = - *exp(-y2)dy* (7.166) 
$$\mathrm{erf}(t)=\frac{2}{\sqrt{\pi}}\int_{0}^{t}\exp(-\gamma^{2})\,d\gamma\tag{7.166}$$
(Note that the error function is sometimes defined without the **2/fi** factor, which can lead to confusion. However, the above definition is the most commonly used one.) We normalize the truncated pdf so that it has an area of one, and we find that the truncated pdf (i.e., the constrained pdf of the first element of Zkz) is given by 

$$\begin{array}{rcl}\mbox{pdf}(\zeta)&=&\left\{\begin{array}{ll}\alpha\exp(-\zeta^{2}/2)&\zeta\in[c_{k1},d_{ki}]\\ 0&\mbox{otherwise}\end{array}\right.\\ \alpha&=&\frac{\sqrt{2}}{\sqrt{\pi}\left[\mbox{erf}(d_{ki}/\sqrt{2})-\mbox{erf}(c_{ki}/\sqrt{2})\right]}\end{array}\tag{7.167}$$
$$(7.168)$$

We define Zk,z+l as the random variable that has the same pdf as Zkz except that the pdf is truncated and normalized, so that its pdf lies entirely between the limits Cka and dk,: 
pdf(Zk,,+l) = truncated pdf(Zk,,) (7.168) 
We can compute the mean and variance of Zk,z+l as follows: 

$$\mu=E[z_{k,1+1}]$$ $$=\alpha\int_{c_{k}}^{d_{k_{1}}}\zeta\exp(-\zeta^{2}/2)\,d\zeta$$ $$=\alpha\left[\exp(-c_{k1}^{2}/2)-\exp(-d_{k1}^{2}/2)\right]$$ $$\sigma^{2}=E\left[(z_{k,1+1}-\mu)^{2}\right]$$ $$=\alpha\int_{c_{k_{1}}}^{d_{k_{1}}}(\zeta-\mu)^{2}\exp(-\zeta^{2}/2)\,d\zeta$$ $$=\alpha\left[\exp(-c_{k1}^{2}/2)(c_{k_{1}}-2\mu)-\exp(-d_{k1}^{2}/2)(d_{k_{1}}-2\mu)\right]+\mu^{2}+1$$
$$(7.169)$$  1  . 
$$(7.170)$$

The mean and variance of the transformed state estimate, after enforcement of the first constraint, are therefore given as 

$$\begin{array}{r c l}{{\tilde{z}_{k,1+1}}}&{{=}}&{{\left[\begin{array}{l l l l}{{\mu}}&{{0}}&{{\cdots}}&{{0}}\end{array}\right]^{T}}}\\ {{\mathrm{Cov}(\tilde{z}_{k,1+1})}}&{{=}}&{{\mathrm{diag}(\sigma^{2},1,\cdots,1)}}\end{array}$$
$$\begin{array}{l l l}{{\tilde{x}_{k,{\mathrm{t}}+1}}}&{{=}}&{{T W^{1/2}\rho^{T}\tilde{z}_{k,{\mathrm{t}}+1}+\tilde{x}_{k{\mathrm{t}}}}}\\ {{\tilde{P}_{k,{\mathrm{t}}+1}}}&{{=}}&{{T W^{1/2}\rho^{T}\mathrm{Cov}(\tilde{z}_{k,{\mathrm{t}}+1})\rho W^{1/2}T^{T}}}\end{array}$$

We then take the inverse of the transformation of Equation (7.153) to find the mean and variance of the state estimate after enforcement of the first constraint. 

$$\begin{array}{r c l}{{\tilde{x}_{k}}}&{{=}}&{{\tilde{x}_{k s}}}\\ {{\tilde{P}_{k}}}&{{=}}&{{\tilde{P}_{k s}}}\end{array}$$

We then increment i by one and repeat the process of Equations (7.153)-(7.171) to obtain the state estimate after enforcement of the next constraint. Note that fkk0 is the unconstrained state estimate at time k, ?kl is the state estimate at time k after the enforcement of the first constraint, 2k2 is the state estimate at time k after the enforcement of the first two constraints, and so on. After going through this process s times (once for each constraint), we have the final constrained state estimate and covariance at time k: 

$$(7.171)$$
$$(7.172)$$

Figure **7.2** shows an example of a one-dimensional state estimate before and after truncation. Before truncation, the state estimate is outside of the state constraints. 

After truncation, the state estimate is set equal to the mean of the truncated pdf. Figure **7.3** shows another example. In this case, the unconstrained state estimate is inside the state constraints. However, truncation changes the pdf and so the constrained state estimate changes to the mean of the truncated pdf. 

![39_image_0.png](39_image_0.png)

Figure 7.2 estimate, which is at z c -1.38, is the centroid of the truncated pdf. 

The unconstrainedestimate at z = 0 violates the constraints. The constrained 

![39_image_1.png](39_image_1.png)

Figure 7.3 The unconstrained estimate at z = 0 satisfies the constraints. Nevertheless, the truncation approach to constrained estimation shifts the estimate to the centroid of the truncated pdf, which is at z M -0.23. 

$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{x_{k+1}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\\ {{0}}\end{array}\right]}}\\ {{}}&{{}}&{{}}\\ {{y_{k}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]}}\end{array}$$
$$\begin{array}{r l}{0}&{T}\\ {1}&{0}\\ {0}&{1}\\ {0}&{0}\\ {0}&{0}\\ {1}&{0}\end{array}$$

In this example, we consider a vehicle navigation problem. The first two state elements are the north and east positions of a land vehicle, and the last two elements are the north and east velocities. The velocity of the vehicle is in the direction of 8, an angle measured clockwise from due east. A positionmeasuring device provides a noisy measurement of the vehicle's north and east positions. The process and measurement equations for this system can be written as 

$$(7.173)$$
$$(7.174)$$

where T is the discretization step size. We can implement a Kalman filter to estimate the position and velocity of the vehicle based on our noisy position measurements. If we know that the vehicle is on a road with a heading of 8, then we know that 

$$\begin{array}{c}{{0}}\\ {{T}}\\ {{0}}\\ {{1}}\end{array}\left[\begin{array}{c}{{0}}\\ {{0}}\\ {{T\sin\theta}}\\ {{T\cos\theta}}\end{array}\right]u_{k}+w_{k}$$
$$\tan\theta$$
$$\begin{array}{r l}{={}}&{{}x(1)/x(2)}\\ {={}}&{{}x(3)/x(4)}\end{array}$$

$${\begin{array}{l l}{0}&{0}\\ {1}&{-\tan\theta}\end{array}}\end{array}}\right]x_{k}={\left[\begin{array}{l}{0}\\ {0}\end{array}\right]}$$
= **43)/44) (7.174)** 
These constraints can be written as 

$$\begin{array}{c}{{-\tan\theta}}\\ {{0}}\end{array}$$
$$\mathbf{\Sigma}_{0}^{1}=$$
$$(7.175)$$
1 -tan8 0 0 
1 0 0 1 -tan8 
The constrained filter can be implemented using any of the four approaches discussed in this section (model reduction, perfect measurements, projection, or pdf truncation). Figure **7.4** shows the magnitude of the north position estimation error of the unconstrained and constrained filters (projection approach using W = I) for a typical simulation. In this example, significant estimation improvement can be obtained when constraint information is incorporated into the filter, although the improvement will be problem dependent. 

vvv It is clear from this section that there are a variety of ways to enforce equality or inequality constraints on state estimation problems. The "best" way is not clearcut, and probably depends on the application. Other approaches to constrained estimation and some discussion of the mathematical meaning of state constraints can be found in [He194, Rao03, DewO4, Goo05a, Gooosb, Ko061. 

## 7.6 Summary

In this chapter, we discussed a variety of Kalman filter generalizations that make the filter more widely applicable to a broader class of problems. Correlated and colored process and measurement noise were studied early in the history of the 

![41_image_0.png](41_image_0.png)

Figure **7.4** constrained Kalman filters for Example **7.12.** 
North position estimation error magnitude of the unconstrained and 
Kalman filter. We showed in this chapter that filter modifications taking correlation and color into account can improve estimation performance. However, whether or not these approaches are worth the extra complexity and computational effort is problem dependent. One of the most practical extensions of the Kalman filter is the steady-state Kalman filter. The steady-state Kalman filter often performs nearly identically to the more theoretically rigorous timevarying filter. However, the steady-state filter requires only a fraction of the computational cost. The *a-p* and a-B-7 filters are special cases of the steady-state Kalman filter. We also discussed the fading-memory filter, which is a way of making the Kalman filter more robust to modeling errors. The fading-memory filter is a simple modification to the Kalman filter that can noticeably improve filter performance. Further discussion of filter robustness is found in Section 10.4 and Chapter 11. Finally, we discussed several ways to incorporate state constraints in the Kalman filter to improve estimation accuracy when information other than the state model is available. Other Kalman filter generalizations are discussed in later chapters of this book. 

Kalman filters with fewer states than the system (Section 10.3) Kalman filtering when the system model or noise statistics are not known (Section 10.4) 
order (Section 10.5) 
Kalman filtering when the measurements arrive at the filter in the wrong Kalman filters for nonlinear systems (Chapter 13) 
Further generalizations undoubtedly await future development by the efforts of enterprising students and researchers. 

## Written Exercises

7.1 Consider the scalar system 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\frac{1}{2}x_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{}}&{{}}&{{1}}\end{array}$$
$$\begin{array}{r c l}{{\phi_{k}}}&{{}}&{{v_{k}+v_{k}}}\\ {{v_{k}}}&{{=}}&{{\frac{1}{2}v_{k-1}+\zeta_{k-1}}}\end{array}$$

where Wk N (0, Q) and (k N (0, Qc). *Let* Q = Qc = 1. 

a) Design a Kalman filter in which the dynamics of the measurement noise Vk are ignored and it is assumed that Vk is white noise with a variance of *Qc.* 
Based on the incorrect Kalman filter equations, what does the Kalman filter think that the steady-state a *posteriori* estimation covariance is? 

b) Based on the incorrect Kalman filter equations, what is the true steadystate a *posteriori* estimation covariance *E(e%)?* Hint: Find a recursive equation for *E($)* in terms of E(e%-,), **E(w;-J,** *E(v;),* and *E(ek-lVk),* 
then solve for the steady-state value of *E(ei).* 
c) Design a Kalman filter using the state augmentation approach in which the dynamics of the measurement noise are correctly taken into account. What is the steady-state estimation covariance? Hint: You may need to use MATLAB's DARE function to solve the steady-state Riccati equation that is associated with this question. 

7.2 Show that the Kalman filter for an LTI system with a noise-free scalar measurement that satisfies the equation (HQHT)Q = *QHTHQ* has a steady-state a posteriori covariance of zero. 7.3 Consider the scalar system 

$$x_{k}+v_{k}$$
Yk = *x k + v k* 
$$x_{k-1}+w_{k-1}$$
$$\begin{array}{r l}{x_{k}}&{{}=}\\ {y_{k}}&{{}=}\end{array}$$
xk = xk-I-kwk-1 
where wk N (0, Q) and Vk N (0, R) are white noise processes with Q = R = 1. 

Design a Kalman filter in which the correlation between Wk and *wk+l* is ignored. Based on the incorrect Kalman filter equations, what does it appear that the steady-state a *posteriori* estimation covariance is? 

For the Kalman filter designed above, write a recursive equation for the a *posteriori* estimation error ek = Xk - *2;.* use this equation to find the steady-state solution to *E(ei).* Design a Kalman filter in which the correlation between Wk and *Vk+1* is correctly taken into account. Show that the steady-state a *posteriori* estimation covariance is zero. Explain why the estimation covariance goes to zero in spite of the existence of process noise and measurement noise. 

(Hint: Use the correlation between wk and *Vk+1* to write an equivalent two-state system, and then use the results of Problem 7.2.) 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\left[\begin{array}{c c}{{1/2}}&{{0}}\\ {{0}}&{{1/2}}\end{array}\right]x_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{1}}\end{array}\right]x_{k}+v_{k}}}\end{array}$$

7.4 Consider the system where Wk N (0, Q) and Q = I. 

Find one matrix square root of Q. 

Is *(F,H)* observable? Is *(F, H)* detectable? 

Is *(F,* G) controllable for all G such that *GGT* = Q? Is *(F,* G) stabilizable for all G such that *GGT* = Q? 

Use the above results to specify how many positive definite solutions exist to the DARE that is associated with the Kalman filter for this problem. Use the above results to specify whether or not the steady-state Kalman filter for this system is stable. 

7.5 Prove that the matrix 3.1 in Equation **(7.85)** is symplectic. 

7.6 In this problem, we will use the shorthand notation P = PS and M = *P-.* 
Use the following procedure to find a as a function of ,B for the *cu-p* filter [BarOl]. 

Use the time-update equation for M to solve for the three unique elements of P as a function of the three unique elements of M. 

Use the measurement-update equation for P to solve for the three unique elements of P as a function of the three unique elements of M. 

Equate the sets of equations from the two steps above to get expressions for M11K1, M12K1, and *M12K2,* that do not have any *P23* terms. 

Use Equation **(7.64)** to solve for M11 and *M12.* 
Combine the five equations from the two previous steps to get a single equation with K1 and K2 that does not have any *M,j* terms. 

Replace K1 and K2 in the previously obtained equation with a and ,B from Equation **(7.63),** then solve for a as a function of p. 

7.7 lowing Equation **(7.86).** 
Prove the properties of symplectic matrices that are listed immediately fol7.8 riori Kalman filter can be written as 

$$\begin{array}{l}{{(I-K H)F\hat{x}_{k-1}^{+}+K y_{k}}}\\ {{H\hat{x}_{k}^{+}}}\end{array}$$
$$\begin{array}{r l}{{\hat{x}}_{k}^{+}}&{{}=}\\ {{\hat{y}}_{k}}&{{}=}\end{array}$$

Recall that the steady-state, zero-input, one-step formulation of the a poste-
Prove that if *(F,* H) is observable and (I - *HK)* is full rank, then the Kalman filter in the above equation is an observable system. Hint: H(I - KH) = (I - *HK)H.* 
7.9 Suppose you have a two-state Newtonian system of the type described in Section **7.3.1.** The sample time is 1 and the variance of the acceleration noise is 1. 

A requirement is given to estimate the position with an a *posteriori* steady-state variance of 1 or less. What is the largest measurement variance that will meet the requirement? 

7.10 Consider the system described in Problem 7.1. Implement the Kalman filter that assumes white noise and the Kalman filter that assumes colored noise. Numerically calculate the RMS a *posteriori* estimation-error variance and verify that it matches the analytically calculated values from your answer to Problem 7.1. 

7.11 Plot the a and P parameters of the *a-P* filter as a function of A. Use a log scale for X with a range of to **lo3.** What are the limiting values of a and p as X + O? Does this make intuitive sense? What are the limiting values of a and pas X -+ m? 

7.12 Plot the a, p, and y parameters of the *a-P-y* filter as a function of A. Use a log scale for X with a range of to **lo3.** What are the limiting values of a, P, 
and y as X + O? Does this make intuitive sense? What are the limiting values of a, P, and y as X -+ m? 

7.13 A simple model of the ingestion and metabolism of a drug is given as 

$$\begin{array}{r c l}{{\dot{x}_{1}}}&{{=}}&{{-k_{1}x_{1}+u}}\\ {{}}&{{\dot{x}_{2}}}&{{=}}&{{k_{1}x_{1}-k_{2}x_{2}}}\\ {{}}&{{y(t_{k})}}&{{=}}&{{x_{2}(t_{k})+v(t_{k})}}\end{array}$$

where the units of time are days, XI is the mass of the drug in the gastrointestinal tract, 22 is the mass of the drug in the bloodstream, and u is the ingestion rate of the drug. Suppose that kl = k2 = 1. The measurement noise *'U(tk)* is zero-mean and unity variance. The initial state, estimate, and covariance are 

$$\begin{array}{r c l}{{x(0)}}&{{=}}&{{\left[\begin{array}{c}{{0.8}}\\ {{0}}\end{array}\right]}}\\ {{\hat{x}(0)}}&{{=}}&{{x(0)}}\\ {{P(0)}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]}}\end{array}$$

It is known from physical constraints that 21 E [0.8,1]. 

a) Discretize the system with a step size of 1 hour. 

b) Implement the discrete-time Kalman filter, the projection-based constrained Kalman filter with W = I, and the pdf truncation constrained filter. Run simulations of these filters for a three-day period. Plot the magnitude of the 21 estimation error for the three filters. Which filter appears to perform best? Which filter appears to perform worst? 