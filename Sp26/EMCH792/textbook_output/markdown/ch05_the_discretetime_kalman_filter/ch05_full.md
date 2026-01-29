---
type: chapter
chapter: 5
title: The discretetime Kalman filter
---

[Image on page 1]


## CHAPTER 5


The discrete-time Kalman filter

The Kalman filter in its various forms is clearly established as a fundamental tool for analyzing and solving a broad class of estimation problems. -Leonard McGee and Stanley Schmidt [McG85]

This chapter forms the heart of this book. The earlier chapters were written only to provide the foundation for this chapter, and the later chapters are written only to expand and generalize the results given in this chapter. **As we will see in this chapter, the Kalman filter operates by propagating the** mean and covariance of the state through time. Our approach to deriving the Kalman filter will involve the following steps.

1. We start with a mathematical description of a dynamic system whose states we want to estimate.

**2. We implement equations that describe how the mean of the state and the** covariance of the state propagate with time. These equations, derived in **Chapter 4, themselves form a dynamic system.**

**3. We take the dynamic system that describes the propagation of the state mean** and covariance, and implement the equations on a computer. These equations form the basis for the derivation of the Kalman filter because:

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **123**

---

**124**

(a) The mean of the state is the Kalman filter estimate of the state.

(b) The covariance of the state is the covariance of the Kalman filter state estimate.

**4. Every time that we get a measurement, we update the mean and covariance** **of the state. This is similar to what we did in Chapter 3 where we used** measurements to recursively update our estimate of a constant.

**In Section 5.1, we derive the equations of the discretetime Kalman filter. This** includes several different-looking, but mathematically equivalent forms. Various books and papers that deal with Kalman filters present the filter equations in ways that appear very different from one another. It is not always obvious, but these different formulations are actually mathematically equivalent, and we will **see this in Section 5.1. (Sections 9.1, 10.5.1, and 11.1 also derive alternate but** **equivalent formulations of the Kalman filter equations.) In Section 5.2, we will** examine some of the theoretical properties of the Kalman filter. One remarkable aspect of the Kalman filter is that it is optimal in several different senses, as we **will see in Section 5.2. In Section 5.3, we will see how the Kalman filter equations** 
## can be written with a single time update equation. Section 5.4 presents a way to
 obtain a closed-form equation for the timevarying Kalman filter for a scalar time- invariant system, and a way to quickly compute the steady-state Kalman filter. **Section 5.5 looks at some situations in which the Kalman filter is unstable or gives** state estimates that are not close to the true state. We will also look at some ways that instability and divergence can be corrected in the Kalman filter.

**5.1 DERIVATION OF THE DISCRETE-TIME KALMAN FILTER**

Suppose we have a linear discretetime system given as follows:


# x k  = Fk-1Xk-1 + G k - i U k - 1  + W k - 1


## Yk = H k Z k  + u k
 **(5.1)**

**The noise processes { W k }  and { O k }  are white, zero-mean, uncorrelated, and have** **known covariance matrices Q k  and R k ,  respectively:**


## where bk-j is the Kronecker delta function; that is, & - j  = 1 if k = j, and 6k-J = 0
 
## if k # j. Our goal is to estimate the state 2 k  based on our knowledge of the system
 **dynamics and the availability of the noisy measurements { Y k } .  The amount of** information that is available to us for our state estimate varies depending on the particular problem that we are trying to solve. If we have all of the measurements **up to and including time k available for use in our estimate of Xk, then we can form** 
## an a posteriori estimate, which we denote as 2:.
 The "+" superscript denotes that

---


[Image on page 3]


**125**

*the estimate is a posteriori. One way to form the a posteriori state estimate is to* **compute the expected value of x k  conditioned on all of the measurements up to** **and including time k:**


## 2; = E [ X k / y l ,  y 2 , .  . ., Yk] = a posteriori estimate
 (5.3)

**If we have all of the measurements before (but not including) time k available for** **use in our estimate of X k ,  then we can form an a praori estimate, which we denote** 
## as 2;. The "-" superscript denotes that the estimate is a priori. One way to form
 **the a priori state estimate is to compute the expected value of 51, conditioned on** **all of the measurements before (but not including) time k:**


## 2; = E [ X k l y l ,  y 2 , .  ., Y k - l ]  = a priori estimate
 (5.4)

**It is important to note that 2; and 2; are both estimates of the same quantity; they** 
## are both estimates of X k .  However, 2 i  is our estimate of Xk before the measurement


**Yk is taken into account, and 2: is our estimate of 21, after the measurement y k** 
## is taken into account. We naturally expect 2; to be a better estimate than 2 i ,
 **because we use more information to compute 2;:**


## 2 i  =
 **2' k** = **estimate of Xk after we process the measurement at time k** (5.5)

**If we have measurements after time k available for use in our estimate of X k ,  then** *we can form a smoothed estimate. One way to form the smoothed state estimate is* **to compute the expected value of x k  conditioned on all of the measurements that** are available:

**estimate of Xk before we process the measurement at time k**


## ?klk+N = E [ x k l Y l i Y 2 , ' . . , Y k , " ' , Y k + N ]  = smoothed estimate
 (5.6)

**where N is some positive integer whose value depends on the specific problem that** **is being solved. If we want to find the best prediction of x k  more than one time** *step ahead of the available measurements, then we can form a predicted estimate.* One way to form the predicted state estimate is to compute the expected value of

**Xk conditioned on all of the measurements that are available:**


## 2 k l k - M  = E [ x k j y 1 ,  y 2 ,  - . ., y k - ~ ]  = predicted estimate
 (5.7)

*where M is some positive integer whose value depends on the specific problem that* *is being solved. The relationship between the a posteriori, a priori, smoothed, and* predicted state estimates is depicted in Figure 5.1. **In the notation that follows, we use 2; to denote our initial estimate of xo before** 
## any measurements are available. The first measurement is taken at time k = 1.
 **Since we do not have any measurements available to estimate 20, it is reasonable** **to form 2; as the expected value of the initial state 2 0 :**


## 2; = E ( X 0 )
 (5.8)

**We use the term P k  to denote the covariance of the estimation error. P; denotes** **the covariance of the estimation error of 2;, and PL denotes the covariance of the** estimation error of 2:

(5.9)

---

**126**

smoothed estimate **a posteriori estimate I;;** **a priori estimate I;;** **prediction I;9,5**

1 2 3 4 5 6 7 8 9 time

**Figure 5.1** *Time line showing the relationship between the a posteriori, a priori,* smoothed, and predicted state estimates. In this figure, we suppose that we have received 
## measurements at times up to and including k = 5. An estimate of the state at k < 5 is called
 
## a smoothed estimate. An estimate of the state at lc = 5 is called the a posteriori estimate.
 
## An estimate of the state at k = 6 is called the a priori estimate. An estimate of the state
 
## at k > 6 is called the prediction.


These relationships are depicted in Figure 5.2. The figure shows that after we 
## process the measurement at time (k-1), we have an estimate Of X k - 1  (denoted ?:-_,)
 **and the covariance of that estimate (denoted P$-l). When time k arrives, before we** **process the measurement at time k we compute an estimate of x k  (denoted 2;) and** **the covariance of that estimate (denoted Pi). Then we process the measurement** 
## at time k to refine our estimate of X k .  The resulting estimate of X k  is denoted ?i.;cf,
 **and its covariance is denoted Pk+.**

I **k-1** , I **k** time


## Figure 5.2
 error covariance. *Timeline showing a pnori and a posteriori state estimates and estimation-*

We begin the estimation process with at, our best estimate of the initial state


## X O .  Given ?$, how should we compute a,?
 
## We want to set 2; = E(z1). But note
 **that 3;':** 
## = E(xo), and recall from Equation (4.2) how the mean of x propagates
 
## with time: z k  = F k - l Z k - l +
 **Gk-1uk-1. We therefore obtain**

**This is a specific equation that shows how to obtain 2; from 2;. However, the** reasoning can be extended to obtain the following more general equation:

**(5.11)** 
## x k  = Fk-13t-1 -k Gk-iuk-i


# This is called the time update equation for ?. From time (k - 1)f to time k-, the
 state estimate propagates the same way that the mean of the state propagates. This makes sense intuitively. We do not have any additional measurements available to

.-

---


[Image on page 5]


**127**


# help us update our state estimate between time (k - 1)+ and time k-, so we should
 just update the state estimate based on our knowledge of the system dynamics. **Next we need to compute the time update equation for P ,  the covariance of the** **state estimation error. We begin with Po', which is the covariance of our initial** 
## estimate of zo. If we know the initial state perfectly, then P$ = 0. If we have
 
## absolutely no idea of the value of 20, then P$ = 001. In general, P$ represents
 **the uncertainty in our initial estimate of 20:**

**Pof** *= E[(zrJ - zo)(zo - zo)T]* 
# = E"zo - *i.os)(zo - 20
 *-+ ) T I* **(5.12)**

**Given Po', how can we compute P;?** **Recall from Equation (4.4) how the co-** 
## variance of the state of a linear discrete-time system propagates with time: Pk =
 **Fk_1&1F;-,** 
# + Qk-1. we therefore obtain


# PT = FoP$F,T + Qo
 **(5.13)**

**This is a specific equation that shows how to obtain P; from Pof. However, the** reasoning can be extended to obtain the following more general equation:


# p i  = Fk-ip?-,FkT_1 + Q k - 1
 **(5.14)**

**This is called the timeupdate equation for P.** **We have derived the time-update equations for 2 and P .  Now we need to derive** **the measurement-update equations for 2 and P. Given 2;, how should we compute** **2:? The quantity 53; is an estimate of X k ,  and the quantity 53; is also an estimate** **of Z k .  The only difference between 2; and 2: is that 2; takes the measurement**

**Yk into account. Recall from the recursive least squares development in Section 3.3** 
## that the availability of the measurement Yk changes the estimate of a constant z as
 follows:

**Kk** 
# = Pk-iHT(HkPk-lHT + &)-'
 
## = PkH:Ril


## 5k = ?k-1 f Kk(Yk - H k i k - 1 )
 **Pk** 
# = (1 - KkHk)Pk-i(I - KkHk)T + KkRkK;
 
# = (PF:l + HTRL1Hk)-l
 
# = (1 - KkHk)Pk-l
 **(5.15)**

**where i&-1 and Pk-1 are the estimate and its covariance before the measurement**

**Y k  is processed, and 2k and Pk are the estimate and its covariance after the mea-** **surement Y k  is processed. In this chapter, 2; and P; are the estimate and its** **covariance before the measurement Yk is processed, and 2; and P z  are the esti-** **mate and its covariance after the measurement yk is processed. These relationships** **are shown in Table 5.1.l** We can now generalize from the formulas for the estimation of a constant in **Section 3.3, to the measurement update equations required in this section. In**

**'we need to use minus and plus superscripts on &k and Pk in order to distinguish between** **quantities before Yk is taken into account, and quantities after Y k  is taken into account. In** **Chapter 3, we did not need superscripts because x was a constant.**

---


[Image on page 6]


**128**


## Table 5.1
 **Fklationships between estimates and covariances in Sections 3.3 and 5.1**

**Section 3.3** Least squares estimation

~~ Section 5.1 Kalman filtering

*2k-1 = estimate before Y k  is processed* *Pk-1 = covariance before Y k  is processed* *hk = estimate after Yk is processed* *Pk = covariance after Yk is processed*

**I** * **I**


## 2 i  = a praori estimate
 *P- - a priori covariance* 2f *a posteriori estimate* *Pk+ = a posteriori covariance*


## Equation (5.15), we replace 2k-1 with 2 i ,  we replace Pk-1 with P;, we replace 2k
 **with 2:, and we replace Pk with Pk+. This results in**

*Kk* *= P;Hr(HkP;Hr + &)-'* *= P ~ + H ~ R L '*

*h i  = &i+Kk(Yk-Hk?i)* 
# Pk+ = (1 - KkHk)P;(I - KkHk)T + KkRkKr
 *= [(P;)-' + HTR,'Hk]-'* *= (I-KkHk)P;* *(5.16)*

*These are the measurement-update equations for hk and Pk. The matrix Kk in the* above equations is called the Kalman filter gain.

**The discrete-time Kalman filter**

Here we summarize the discrete-time Kalman filter by combining the above equ* tions into a single algorithm.

1. The dynamic system is given by the following equations:

**(5.17)**

**2. The Kalman filter is initialized as follows:**

**2;** *= E(X0)* *P$* *= E[(xo - i?i'o+)(~o - X O  -+ ) T ]* *(5.18)*

**3. The Kalman filter is given by the following equations, which are computed** 
## for each time step k = 1,2,. . .:


$$
PL = Fk-ipk+-lFz-l 4- Qk-1
$$
 *Kk* *= P;Hr(HkP;Hr + &)-'*

---

**129**

**The first expression for PL above is called the Joseph stabilized version of the** covariance measurement update equation. It was formulated by Peter Joseph in **the 1960s and can be shown to be more stable and robust than the third expression** **for Pk+ [Buc68, Cra04] (see Problem 5.2). The first expression for Pk+ guarantees** **that Pk+ will always be symmetric positive definite, as long as Pr is symmetric** **positive definite. The third expression for P t  is computationally simpler than the** first expression, but its form does not guarantee symmetry or positive definiteness **for P l .  The second form for Pk+ is rarely implemented as written above but will** be useful in our derivation of the information filter in Section 6.2. **If the second expression for Kk is used, then the second expression for Pk+ must** **be used. This is because the second expression for Kk depends on P;, so we need** **to use an expression for Pk+ that does not depend on Kk.** 
## Note that if x k  is a constant, then Fk = I ,  Qk = 0 ,  and U k  = 0. In this case, the
 **Kalman filter of Equation (5.19) reduces to the recursive least squares algorithm** for the estimation of a constant vector as given in Equation (3.47). Finally we mention one more important practical aspect of the Kalman filter. We **see from Equation (5.19) that the calculation of P;, Kk, and Pk+ does not depend** **on the measurements y k ,  but depends only on the system parameters Fk, Hk, Qk,** **and Rk. That means that the Kalman gain Kk can be calculated offline before the** system operates and saved in memory. Then when it comes time to operate the **system in real time, only the 2k equations need to be implemented in real time. The** **computational effort of calculating Kk can be saved during real-time operation by** precomputing it. If the Kalman filter is implemented in an embedded system with strict computational requirements, this can make the difference between whether or not the system can be implemented in real time. Furthermore, the performance of the filter can be investigated and evaluated before the filter is actually run. This is **because Pk indicates the estimation accuracy of the filter, and it can be computed** **offline since it does not depend on the measurements. In contrast, as we will see in** Chapter 13, the filter gain and covariance for nonlinear systems cannot (in general) be computed offline because they depend on the measurements.

**5.2** 
## KALMAN FILTER PROPERTIES


In this section, we summarize some of the interesting and important properties of **the Kalman filter. Suppose we are given the linear system of Equation (5.17) and** **we want to find a causal filter that results in a state estimate 2k. The error between** **the true state and the estimated state is denoted as 4k:**

---

**130**

Since the state is partly determined by the stochastic process {wk}, **xk is a random** variable. Since the state estimate is determined by the measurement sequence {yk}, **which in turn is partly determined by the stochastic process {wk}, ?k is a random** **variable. Therefore, 5k is also a random variable.** Suppose we want to find the estimator that minimizes (at each time step) a **weighted two-norm of the expected value of the estimation error z k :**

**(5.21)**

**where 5’1,** **is a positive definite user-defined weighting matrix. If sk is diagonal with** 
## elements S k ( l ) ,  . . a ,  Sk(n), then the weighted sum isequal to Sk(l)E[i$(l)]
 **+** **.** **.** **a** **+** 
## sk (n)E [z.%
 *(n)] -*


## 0 If {wk} and {wk} are Gaussian, zero-mean, uncorrelated, and white, then the
 Kalman filter is the solution to the above problem.


## 0 If {wk} and {vk} are zero-mean, uncorrelated, and white, then the Kalman
 filter is the best linear solution to the above problem. That is, the Kalman filter is the best filter that is a linear combination of the measurements. There may be a nonlinear filter that gives a better solution, but the Kalman filter is the best linear filter. It is often asserted in books and papers that the Kalman filter is not optimal unless the noise is Gaussian. However, as our derivation in this chapter has shown, that is simply untrue. Such statements arise from erroneous interpretations of Kalman filter derivations. Even if the noise is *not Gaussian, the Kalman filter is still the optimal linear filter.*


## 0 If {wk} and {vk} are correlated or colored, then the Kalman filter can be
 modified to solve the above problem. This will be shown in Chapter 7.


## 0 For nonlinear systems, various formulations of nonlinear Kalman filters ap-
 proximate the solution to the above problem. This will be discussed further **in Chapters 13-15.**

**Recall the measurement update equation from Equation (5.19):**

*The quantity (yk - Hk?;) is called the innovations. This is the part of the measure-* ment that contains new information about the state. In Section 10.1, we will prove *that the innovations is zero-mean and white with covariance (HkPLHT + R k ) .  In* **fact, the Kalman filter can actually be derived as a filter that whitens the measure-** ment and hence extracts the maximum possible amount of information from the measurement. This was first proposed in [Kai68]. When a Kalman filter is used for state estimation, the innovations can be measured and its mean and covariance can be approximated using statistical methods. If the mean and covariance of the **innovations are not as expected, that means something is wrong with the filter.** Perhaps the assumed system model is incorrect, or the assumed noise statistics are incorrect. This can be used in real time to verify Kalman filter performance and parameters, and even to adjust Kalman filter parameters in order to improve performance. An application of this idea will be explored in Section 10.2.

---

**131**

**5.3** 
## ONE-STEP KALMAN FILTER EQUATIONS


*In this section, we will see how the a priori and a posteriori Kalman filter equations* can be combined into a single equation. This may simplify computer implementa- *tion of the equations. We start with the a priori state estimate expression from* **Equation (5.19), with the time index increased by one:**

**Now take the a posteriori expression for 2; from Equation (5.19), and substitute** it into the above equation to obtain

*This shows that the a priori state estimate can be computed directly from its value* *at the previous time step, without computing the a posteriori state estimate in b e* **tween. A similar procedure can be followed in order to obtain a onestep expression** *for the a priori covariance. We start with the a priori covariance expression from* **Equation (5.19), with the time index increased by one:**

**Now take the expression for Pkf from Equation (5.19), and substitute it into the** above equation to obtain

**This equation, called a discrete Riccati equation, shows how PL+l can be computed** **on the basis of P; without an intermediate calculation of P;.** Similar manipulations can be performed to obtain one-step expressions for the *a posteriori state estimate and covariance. This results in*

**One could imagine many different ways of combining the two expressions for Kk** **and the three expressions for P z  in Equation (5.19). This would result in a num-** *ber of different expressions for onestep updates for the a priori and a posteriori* covariance.

---

**132**

**EXAMPLE5.1**


## Suppose we have a noise-free Newtonian system2 with position T ,  velocity w,
 *and constant acceleration a. The system can be described as* [i] = [ O O l ] [ j 0 1 0

0 0 0 *k = AZ* (5.28)

The discretized version of this system (with a sample time of T) can be written **as**


## X k f l  = FZk
 (5.29)

**where F is given as**


## F = exp(AT)


1 T T2/2 0 1 T 0 0 1

The Kalman filter for this system is

(5.30)

**(5.31)**

We see that the covariance of the estimation error increases between time 
# (k - 1)+ [that is, time (k - 1) after the measurement at that time is processed],
 **and time k- (i.e., time k before the measurement at that time is processed).** 
# Since we do not obtain any measurements between time (k - 1)+ and time
 **k-, it makes sense that our estimation uncertainty increases. Now suppose** that we measure position with a variance of u2:


## Y k  = Hkxk+vk
 
## = [ 1 0 0 ] 2 1 , + v k


**wk** **(0,Rk)** **Rk** 
## = U2
 (5.32)

The Kalman gain can be obtained from Equation (5.19) as


# Kk = PLHz(HkPFHr + Rk)-l
 (5.33)


## If we write out the 3 x 3 matrix P; in terms of its individual elements, and
 **substitute for Hk and Rk in the above equation, we obtain**

2The system described in this example is called Newtonian because it has its roots in the mathe- matical work of Isaac Newton. That is, velocity is the derivative of position, and acceleration is the derivative of velocity.

---


[Image on page 11]


**133**

(5.34)


## The a posteriori covariance can be obtained from Equation (5.19) as


# P; = PL - Kk HkPi
 (5.35)

*If we write out the 3 x 3 matrix P i  in terms of its individual elements, and* **substitute for Hk and Kk in the above equation, we obtain**

1

**(p<ll)2** **p<llp621** **p<llp631**

**p<12p<11** **(p<12)2** **pc12p<31** (5*36)

**p<13p<11** **'** **<** **1** **3** **'** **<** **1** **2** **(p<13)2**

1 
## = p;-


## P < l l +  a2


**We will use this expression to show that from time k- to time k+ the trace** of the estimation-error covariance decreases. To see this first note that the **trace of P; is given as**


## Tr(Pi) = P<ll+
 
# p<22 + p<33
 (5.37)

**From Equation (5.36) we see that the trace of Pz is given as**


# WP,+) = q 1 1 +  q 2 2  + q 3 3


(5.38)

When we get a new measurement, we expect our state estimate to improve. That is, we expect the covariance to decrease, and the above equation shows *that it does indeed decrease. That is, the trace of Pz is less than the trace*

This system was simulated with five time units between discretization steps *(T = 5), and a position-measurement standard deviation of 30 units. Fig-* **ure 5.3 shows the variance of the position estimate (Pcll and P,';,,) for the** first five time steps of the Kalman filter. It can be seen that the variance (uncertainty) increases from one time step to the next, but then decreases at **each time step as the measurement is processed.** **Figure 5.4 shows the variance of the position estimate (PCl1** **and P,';,,)** for the first 60 time steps of the Kalman filter. This shows that the variance increases between time steps, and then decreases at each time step. But it

*of P;.*

---


[Image on page 12]


**134**

**"0** I **2** **3** **4** **5** **time step**

**Figure 5.3** error variances for Example 5.1. 
## The first five time steps of the a priori and a posteriori position-estimation-


**8 3000**


# i 2000


**5** **'5 2500** **L**

**0**

**1500** 
# 4- I
 
## s 1000
 **4-**

**500**

**0** **10** **20** **30** **40** **50** **60** **0** **I** **0** **10** **20** **30** **40** **50** **60** **0'**

**time step**


## Figure 5.4
 **error variances for Example 5.1.** 
## The first 60 time steps of the a priori and a posteriori position-estimation-


can also be seen from this figure that the variance converges to a steady-state value. 
## Figure 5.5 shows the position-measurement error (with a standard devia-
 **tion of 30) and the error of the a posteriori position estimate. The estimation** **error starts out with a standard deviation close to 30, but by the end of the** simulation the standard deviation is about 11. vvv

---

135

-estimation error

**80**

**60 -**


## _. i
 > **7.** . < - .. - .. _ -  - , _. - .. - _- - .. . **-40-**


# -60 1


I **0** **10** **20** **30** 40 50 60 time step


# -80 '


**Figure 5.5** The position-measurement error and position estimation error for Example 5.1.

**5.4** 
## ALTERNATE PROPAGATION OF COVARIANCE


In this section, we derive an alternate equation for the propagation of the estimation- *error covariance P. This alternate equation, based on [GreOl], can be used to find* a closed-form equation for a scalar Kalman filter.3 It can also be used to find a fast solution to the steady-state estimation-error covariance.

**5.4.1 Multiple state systems**

**Recall from Equation (5.19) the update equations for the estimation-error covari-** ance:

*p;* *= Fk-ipz-_lFr-l + Q k - i* **(5.39)** 
# Pk+ = Pc - PcH:(HkPLH: + Rk)-lHkPL


**If the n x n matrix P; can be factored as**

*PL = AkBkl* **(5.40)**

**where Ak and Bk are n x n matrices to be determined, then P;+l satisfies**


## pL+l = Ak+lBii1
 **(5.41)**

**where A and B are propagated as follows:**

3The equations given in [GreOl] have some typographical errors that have been corrected in this section.

---

**136**

**This can be seen by noting from Equation (5.42) that** 
## Biil = [FF T HkRk
 **T -1 HkAk+FFTBk]-l**

*= [FiT(HZRi1HkAkBi1 + I)&]-'* - *k [* *k* *k H d k B i l + I ] - l F T* **(5.43)**

**(5.44)**

*- B - ~ H T R ~ ~*

**From Equation (5.42) we see that** 
$$
Ak+lB& = [(Fk 4- Q k F i  T
$$
 *T* *Hk RilHk)Ak f QkFLTBk]BFil*

*Substituting the expression for B;jl into this equation gives*

**(5.45)**


$$
Ak+iBii1 = [(Fk 4- QkFiTHFRilHk)PF + QkFFT] X
$$
 *[HFRilHkP; + I]-lF:*

*[FkpF + QkFFT(H;RilHkPF + I ) ]  X* *[HFRi'HkPF + I]-lF:* =

*= FkP<[H:RilHkP[ + I]-lF,T + QkFF T* *T* *Fk* **(5.46)**

Applying the matrix inversion lemma to the term in brackets gives


$$
Ak+1Bii1 = FkpF[I - Hk ( HkPFH? 4- Rk)-lHkpF]F: + Qk
$$
 *= Fk[Pi - PcH;(HkPFHF f Rk)-lHkPF]FT + Qk* *= FkPZFFfQk* *= PF+l* **(5.47)**

*So we see that Ak+lBijl = PF+l.* **Equation (5.42) can be used to obtain a quick solution to the steady-state covari-** ance for multidimensional systems (although not a closed-form solution). Suppose **that F ,  Q, H ,  and R are constant matrices. From Equation (5.42) we obtain** *[ Ak+i ] = [ (F+QF-THTR-lH)* *QF-T* *Bk+1* *F - ~ H ~ R - ~ H  F-T ] [ ti ]* **(5.48)**


## where we used the fact that A1 = P; and B1 = I satisfies the original factoring
 
## of Equation (5.40). Now we can successively square Q a total of p times to obtain
 
## \k2, Q4, Q8, and so on, until \k2' converges to a steady-state value:
 
# [ tz ] w \ k z p  [
 ] **for large p** **(5.49)**

---


[Image on page 15]


**137**

*The steady-state covariance is P; = A,BZ1.* We can also find the steady-state *Kalman gain by simply iterating the filter equations from Equation (5.19), but the* method in this section could be a much quicker way to find the steady-state gain. 
# Once we find P; as shown above, we compute K, = P;HT(HP&HT + R)-l
 **as the steady-state Kalman filter gain. More discussion of steady-state Kalman** **filtering is given in Section 7.3.**

**5.4.2** **Scalar systems**

*Equation (5.42) can be used to obtain a closed-form solution for the scalar Kalman* *filter for time-invariant systems. Suppose that F ,  Q, H ,  and R are constant scalars.* *Then from Equation (5.42) we obtain*

*= .[;:I* *(5.50)*


## where \Ir is defined by the above equation. Now find the eigendata of 8. Suppose
 
## that the eigenvalues of 8 are X 1  and XZ, and the eigenvectors of 8 are combined to
 *create the 2 x 2 matrix M .  Then*

*(5.51)*

and we obtain

*(5.52)*

*where we used the fact that A1 = P c  and B1 = 1 satisfies the original factoring* *of Equation (5.40).* following.

*P;* =

Xz =

*n* *=*

**7-1** =

**7-2** =

*P1 =*

*Pz* =

Working through the math to obtain XI, *X2, and M gives the*

*2FR* *d H 2 Q  + R(F + 1)2.\/H2Q + R(F - 1)2* *H ~ Q + R ( F ~ - I ) + ~* *H ~ Q* *+ R ( F ~* 
# - I) -
 *H ~ Q* 
# + R ( F ~  + 1) + O
 *H Q  + R ( F ~  + 1) -*

---


[Image on page 16]


**138**

**(5.53)**

This is a closed-form equation for the timevarying Kalman filter for a scalar time- *invariant system. This can easily be used to obtain the steady-state value of P i .* 
## Note that p 2  < 111. As k increases, p; gets smaller and smaller relative to pt.
 Therefore

**(5.54)**

This gives the steady-state covariance for a scalar system.


## EXAMPLE 5.2


In this example, we will show how a scalar covariance can be propagated. Consider the following scalar system:

**(5.55)**

This is a very simple system but one that arises in many applications. For *example, it may represent some slowly varying parameter Xk that we measure* *directly. The process noise term W k  accounts for the variations in X k ,  and the* *measurement noise term Vk accounts for measurement errors. In this system,* 
## we have F = H = Q = R = 1. Substituting these values in Equation (5.53)
 gives

*7 1  = l + &*

*7 2  = 1 - &*


## p 1  = 3 + &


## p 2  = 3 - 4 5


**Taking the limit as k t** *00 gives the steady-state value of P i :*

**(5.56)**

*- 1+G* - - *2* **M 1.62** **(5.57)**

---

**139**

**1.4**

**1.2**

1 -

**0.8**

**Now we can use Equation (5.19) to find the steady-state value of Kk:**

**Kk** 
# = pLHr(HkPLHr + &)-'
 - *pi-* - 
# P; + 1


~

-

-

**x** **0.62** (5.58)

*Figure 5.6 shows the a priori estimation covariance and the Kalman gain as* a function of time, and illustrates their convergence to steady-state values. *From the equation for the a posteriori estimation covariance, we know that* 
## P$ = (I- KkHk)Pi. For this example we therefore see that the steady-state
 value of ~ k + is given as

1 + & **3 + 6** - - - (5.59)

**0** **2** **4** **6** **8** 10 time

**Figure 5.6** The covariance and gain converge to steady-state values. **Estimation covariance and Kalman gain as a function of time for Example 5.2.**

vvv

**5.5** **DIVERGENCE ISSUES**

The theory presented in this chapter makes the Kalman filter an attractive choice for state estimation. But when a Kalman filter is implemented on a real system it

---


[Image on page 18]


**140**

may not work, even though the theory is correct. Two of the primary causes for the failure of Kalman filtering are finite precision arithmetic and modeling errors [Fit7l]. The theory presented in this chapter assumes that the Kalman filter arithmetic is infinite precision. In digital microprocessors the arithmetic is finite precision - only a certain number of bits are used to represent the numbers in the Kalman filter equations. This may cause divergence or even instability in the implementation of the Kalman filter. The theory presented also assumes that the system model is precisely known. It *is assumed that the F ,  Q, H, and R matrices are exactly known, and it is assumed* that the noise sequences {wlc} and {Q} are pure white, zero-mean, and completely **uncorrelated. If any of these assumptions are violated, as they always are in real** implementations, then the Kalman filter assumptions are violated and the theory may not work. In order to improve filter performance in the face of these realities, the designer can use several strategies:

1. Increase arithmetic precision

**2. Use some form of square root filtering**


# 3. Symmetrize P at each time step: P = ( P  + PT)/2


**4. Initialize P appropriately to avoid large changes in P**


## 5. Use a fading-memory filter


**6. Use fictitious process noise (especially for estimating “constants”)**

These strategies are often problem dependent and need to be explored via simula- tion or experimentation in order to obtain good results. Some of these strategies may be more attractive than others, depending on the specific problem. Item 1 above, increasing arithmetic precision, simply forces the digital imple- mentation of the filter to more closely match the analog theory. In a PC-based implementation, it may require only a trivial effort to increase the arithmetic pre- cision - change all the variables to double precision. This trivial change may make the difference between divergence and convergence. However, in a microcontroller implementation it may not be feasible to increase the arithmetic precision. **Item 2 above, square root filtering, is a way of reformulating the filter equations.** Even though the physical precision of the implementation does not change, square root filtering effectively increases arithmetic precision. This will be discussed further **in Sections 6.3, 6.4, and 8.3. But square root filtering requires more computational** effort, which may or may not be a major consideration for a given application. Square root filtering also adds a lot of complication to the filter equations, which invites software bugs. **Items 3 and 4 above involve forcing P to be symmetric and initializing P ap-** propriately. These are easy solutions, but they usually do not result in major im- provements to the convergence properties of the filter. However, these steps should always be implemented since they are straightforward and easy, and since they may *prevent numerical problems. Note from Equation (5.19) that the Pr expression is* *already symmetric, and so there is no point to forcing symmetry for Pr. However,* *depending on which equation is used, Pz may or may not be symmetric. The*

---


[Image on page 19]


**141**

*expressions for Pk+ in Equation (5.19) are mathematically equivalent, but they are* not numerically equivalent. One of them has a built-in symmetry, but the others **do not. If an equation for P c  is used that does not have a built-in symmetry, then** it is very easy and may pay large dividends to force symmetry. This has been done **several different ways in the literature. One way is as described in Item 3 above;** *that is, after P is calculated, set P = ( P  + PT)/2. Other ways involve forcing the* terms below the diagonal to be equal to the terms above the diagonal, or forcing **the eigenvalues of P to be positive.** Item 5 above is a simple way of forcing the filter to “forget” measurements in the distant past and place more emphasis on recent measurements. This causes the filter to be more responsive to measurements. It theoretically results in the loss of optimality of the Kalman filter, but it may restore convergence and stability. It is better to have a theoretically suboptimal filter that works rather than a theoretically optimal filter that does not work due to modeling errors. The greater responsiveness of the fading-memory filter to recent measurements makes the filter less sensitive to modeling errors, and hence more robust. This approach will be discussed further **in Section 7.4.** Item 6 above, the use of fictitious process noise, is also easy to implement. In fact, it can be implemented in a way that is mathematically equivalent to the fading-memory filter of Item 5. Adding fictitious process noise is a way of telling the filter that you have less confidence in your system model. This causes the filter to place more emphasis on the measurements, and less emphasis on the process model (which may be incorrect) [Jaz69].

**EXAMPLE5.3**

Let us illustrate the use of fictitious process noise with an example. Suppose we are trying to estimate a state that we think is a constant, but in reality is a ramp. In other words, we have a modeling error. Our assumed (but incorrect) model, upon which we base the Kalman filter, is given as follows:

(5.60)

**The assumed process noise is zero, which means that we are modeling X k  as** a constant. From Equation (5.19) we derive the Kalman filter equations for this system as


# pr = Fk-ipt-lFr-l + Q k - i
 
## = p;-1


*pi-* 
# P; + 1


**Kk** 
# = PFHF(HkPrHF + &.)-I


= -


## ki = Fk-lXk-1
 -+ - 
# - 5;-1


---


[Image on page 20]


**142**

**2;** 
# = 2, f Kk(yk - Hk2;)
 
# = 2, + Kk(yk - 2 i )
 **Pkf** 
# = (1 - KkHk)Pi(I - KkHk)* + KkRkKz
 
# = (1 - Kk)2pi + K i
 (5.61)

Suppose that the true system, although unknown to the Kalman filter de- **signer, is given as the following two-state model:**

**(5.62)**

The first state is a ramp, which we assumed incorrectly in our system model 
## to be a constant. Figure 5.7 shows the true state x 1 , k  and the estimated state


**&,k, It can be seen that the estimate is diverging from the true state, and** the estimation error is'growing without bound.


## Figure 5.7 Kalman filter divergence due to mismodeling.


However, if we add fictitious process noise to the Kalman filter, then the filter will place more emphasis on the measurements, which will improve the **filter performance. Figure 5.8 shows the true state and the estimated state** **when various values of Q are used in the Kalman filter. As the fictitious** process noise gets larger, the estimation error becomes smaller. Of course, this is at the price of poorer performance in case the assumed system model is actually correct. The designer needs to add an appropriate amount of fictitious process noise to balance performance under nominal conditions with performance under mismodel conditions. *Figure 5.9 shows the time history of the Kalman gain Kk for this example* **for various values of Q. As expected, the gain Kk converges to a larger** steady-state value when Q is larger, making the filter more responsive to

---


[Image on page 21]


**143**

**Figure 5.8 Kalman filter improvement due to fictitious process noise.**


## measurements [see the 2: expression in Equation (5.61)]. This compensates
 **for modeling errors. As shown later in Section 7.4, the fading-memory filter** accomplishes the same thing in a different way. Also note from Figure 5.9 that the steady-state Kalman gain is approximately 0.62 when Q = 1. This matches the results of Example 5.2.

**Figure 5.9 Kalman gain for various values of process noise.**

This example illustrates the general principle that model noise is good, but only to a certain extent. If a system model has too much noise then it is difficult to estimate its state. But if a system model has too little noise then


[Image on page 21]


[Image on page 21]


---

**144**

our state estimator might be overly susceptible to modeling  error^.^ When **designing a model for a Kalman filter, we need to balance our confidence in** our model (low noise resulting in close model tracking; i.e., low bandwidth) with a healthy self-doubt (high noise resulting in filter responsiveness; i.e., high bandwidth). vvv Examination of the filter equations shows why adding fictitious process noise compensates for modeling errors. Recall the Kalman filter equations from Equa- tion (5.19), some of which we repeat here:


# p i  = Fk-ip$-lFkT_1 + Q k - i
 **Kk** 
# = PiHT(HkPFHT + Rk)-'
 ?+ **k** 
# = ?i + Kk(yk - H k f i )
 (5.63)

**If Qk is small then the covariance may not increase very much between time samples.** 
## In Example 5.3 we had Fk = 1, so PF = Pz-l when Qk = 0. But the covariance
 **will decrease from PF down to Pk+ every time a measurement is obtained due to** **the measurement-update equation for the covariance. Eventually PF will converge** to zero. This can be seen by looking at Equation (5.26), which shows the one-step 
## equation for PF :


# Pi+1 = FkPFFr - FkKkHkPFFr 4- Qk
 (5.64)


## If Qk = 0 then this equation has a steady solution of zero. A zero value for Pi
 
## will result in Kk = 0, as seen from Equation (5.63). A zero value for Kk means
 that the measurement-update equation (5.63) for 5 will not take any account of 
## the measurement - that is, the measurement y k  will be completely ignored in the
 
## computation of ?+. This is because the measurement noise covariance Rk (assuming
 
## it is greater than zero) will be infinitely times larger than the process noise Qk = 0.
 The filter will become sluggish in the sense that it will not respond to measurements. **On the other hand, if Qk is larger, then the covariance will always increase** 
## between time samples - that is, P i  will always be larger than P:--.
 **When P;** **converges, it will converge to a larger value. This will make Kk converge to a larger** **value. A larger Kk means that the measurement update for 32. in Equation (5.63)** will include a larger emphasis on the measurement - that is, the filter will pay more attention to the measurements.

**5.6** 
## SUMMARY


In this chapter, we have presented the essence of the discrete-time Kalman filter. Over the past few decades, this estimation algorithm has found applications in virtually every area of engineering. We have seen that the Kalman filter equations can be written in several different ways, each of which may appear quite different than the others, although they are all mathematically equivalent. We have seen that

**4Noise, like most things in life, is beneficial in moderate amounts. We also see this in human** psychological responses to noise. Too much noise will drive humans insane, but too little noise might also result in a loss of sanity. Noise is especially beneficial for controls engineers, who would **not only lose their sanity but would also lose their research funding if not for noise [BarOl, p. 1791.**

---

**145**

the Kalman filter is optimal even when the noise is not Gaussian. The Kalman filter *is the optimal estimator when the noise is Gaussian, and it is the optimal linear* estimator when the noise is not Gaussian. We have seen that the Kalman filter may not perform well if the underlying assumptions do not hold, and we briefly mentioned some ways to compensate for violated assumptions. The later chapters of this book will expand and generalize the results presented in this chapter.

**PROBLEMS**

**Written exercises**

**5.1** **A radioactive mass has a half-life of 7 seconds. At each time step the num-** ber of emitted particles x is half of what it was one time step ago, but there is **some error wk (zero-mean with variance Q) in the number of emitted particles due** to background radiation. At each time step, the number of emitted particles is counted. The instrument used to count the number of emitted particles has a ran- **dom error at time k of vk, which is zero-mean with a variance of R. Assume that**

**W k  and V k  are uncorrelated.** a) Write the linear system equations for this system. **b) Suppose we want to use a Kalman filter to find the optimal estimate of** the number of emitted particles at each time step. Write the one-step a *posteriori Kalman filter equations for this system.* **c) -Find the steady-state a posteriori estimation-error variance for the Kalman** filter. 
## d) What is the steady-state Kalman gain when Q = R? What is the steady-
 *state Kalman gain when Q = 2R? Give an intuitive explanation for why* the steady-state gain changes the way it does when the ratio of Q to R changes.

**5.2** This problem illustrates the robustness that is achieved by the use of the Joseph form of the covariance measurement update equation. Suppose you have a discretetime Kalman filter for a scalar system. **a) Find aP,+/aKk for the third form of the covariance measurement update** in Equation (5.19). **b) Find aP,+/aKk for the Joseph form (the first form) of the covariance mea-** surement update in Equation (5.19). After you get your answer, substitute **for Kk from the Kalman gain expression.**


## c) Use the above results to explain why the Joseph form of the covariance
 measurement-update equation is stable and robust.


## 5.3 Prove that E[21(5t)T] = 0. Hint: Since 2'
 *= E[zo] is a constant and*

prove that E[2f(2f)T] = 0. From this point, use induction to complete the proof.

**5.4** **Suppose that you have a fish tank with xp piranhas and xg guppies [Bay99].** Once per week, you put guppy food into the tank (which the piranhas do not eat). Each week the piranhas eat some of the guppies. The birth rate of the piranhas is proportional to the guppy population, and the death rate of the piranhas is


# 2+ -
 
# - 20 -2; is zero-mean, we know that E[2;(5$)8] = 0. Given this information,


---

**146**


# proportional to their own population (due to overcrowding). Therefore xp(k + 1) =
 
# xp(k) + k l z g ( k )  - k2zp(k) + wp(k),
 **where kl and k2 are proportionality constants** **and wp(k)** is white noise with a variance of one that accounts for mismodeling. The *birth rate of the guppies is proportional to the food supply u, and the death rate* 
# of the guppies is proportional to the piranha population. Therefore, xg(k + 1 )  =
 
# zg ( k )  + u( k) - k3zp (k) + w g
 
# (k) , where ks is a proportionality constant and wg
 **(k) is** white noise with a variance of one that accounts for mismodeling. The step size for this model is one week. Every week, you count the piranhas and guppies. You can count the piranhas accurately because they are so large, but your guppy count has 
## zero-mean noise with a variance of one. Assume that kl = 1 and k2 = kg = 1 / 2 .
 
## a) Generate a linear state-space model for this system.
 **b) Suppose that at the initial time you have a perfect count for x p  and xg. Us-** ing a Kalman filter to estimate the guppy population, what is the variance of your guppy population estimate after one week? What is the variance after two weeks?


## c) What is the ratio of the piranha population to the guppy population when
 they reach steady state? Assume that the process noise is zero for this part of the problem.


# The measured output of a simple moving average process is gk = z k  + z k - 1 ,


## a) Generate a state-space description for this system with the first element
 **of X k  equal to Z k - 1  and second element equal to Z k .** b) Suppose that the initial estimation-error covariance is equal to the identity **matrix. Show that the a posteriori estimation-error covariance is given by**

**5.5** **where {zJ} is zero-mean white noise with a variance of one.**

**1** **1 -1** **p:'&** **1 1**


# c) Find E [IIXk -
 
## In] as a function of k.


## 5.6
 
# In this problem, we use the auxiliary variable Sk = HkPrHT + Rk. Note


Use the product rule for determinants to show that

**5.7** **In Section 4.1, we saw that &,** the covariance of the state of a discrete- 
# time system, is given as Ck+l = Fk&FT + Qk. use this along with the one-step
 **expression for the a priori estimation-error covariance of the Kalman filter to show** **that &-PF 2 0 for all k. Give an intuitive explanation for this expression [And79].**

**5.8** 
## a) Use the method of Section 5.4 to find a closed-form solution for Pi-, as
 
## suming that Q = 1, R = 5, and Po = 0.
 **b) Use your result from above to find the steady-state value of P;.**

Consider the system of Problem 5.1.

---

**147**

**5.9** Suppose that a Kalman filter is designed for the system

**x k + l** 
## = x k


## Yk = x k  f v k


**v k** *(O,R)*


## a) Suppose that E(xg) = 1. Design a Kalman filter for the system and find
 
## a closed-form expression for P i .  What is the limit of P i  as k -+
 oo? 
# b) Now suppose that the true process equation is actually xk+1 = x k  + W k ,
 
## where W k  N (0, Q). Find a difference equation for the variance of the a
 **priori estimation error if the Kalman filter that you designed in part (a)** is used to estimate the state. What is the limit of the estimation-error **variance as k t oa?**

**5.10 Suppose that a Kalman filter is designed for a discrete LTI system with** *an assumed measurement noise covariance of R, but the actual measurement noise* 
# covariance is ( R  + AR). The output of the Kalman filter will indicate that the a
 
## priori estimation-error covariance is P;, but the actual a priori estimation-error
 
# covariance will be EL. Find a difference equation for Ak = (C, - P;). Will A,
 always be positive definite?

**Computer exercises**

5.11 **Let p k  denote the wombat population at time k, and f k  denote the size of** **the wombat's food supply at time k. From one time step to the next, half of the** existing wombat population dies, but the number of new wombats is added to the population is equal to twice the food supply. The food supply is constant except for zero-mean random fluctuations with a variance of 10. At each time step the wombat population is counted with an error that has zero mean and a variance of 10. The initial state is


## PO = 650


## fo = 250


The initial state estimate and uncertainty is


## $0 = 600
 **E[($o - P o ) 2 ]** 
## = 500
 
# jcJ = 200


## q . f o  - fo>21 = 200


Design a Kalman filter to estimate the population and food supply. a) Simulate the system and the Kalman filter for 10 time steps. Hand in the following.


## 0 Source code listing.


## 0 A plot showing the true population and the estimated population as a function
 of time.

---


[Image on page 26]


**148**


## 0 A plot showing the true food supply and the estimated food supply as a
 function of time.


## 0 A plot showing the standard deviation of the population and food supply
 estimation error as a function of time.


## 0 A plot showing the elements of the Kalman gain matrix as a function of time.


b) Compare the standard deviation of the estimation error of your simulation *with the steady-state theoretical standard deviation based on Pk+. Why* is there such a discrepancy?


## c) Run the simulation again for 1000 time steps and compare the experi-
 mental estimation error standard deviation with the theoretical standard deviation.


## 5.12 Consider the RLC circuit described in Problem 1.18 with R = 3, L = 1, and
 
## C = 0.5. The input voltage is zero-mean, unity variance white noise. Suppose that
 the capacitor voltage is measured at 10 Hz with zero-mean, unity variance white noise. Design a Kalman filter to estimate the inductor current, with an initial 
## covariance P$ = 0. Generate a plot showing the a priori and a posteriori variances
 of the inductor current estimate for 20 time steps. Based on the plot, what is the **steady-state value of P;? Use the development of Section 5.4.1 to approximate the** 
## steady-state value of P; using 1, 2, 3, and 4 successive squares of the Q matrix.
