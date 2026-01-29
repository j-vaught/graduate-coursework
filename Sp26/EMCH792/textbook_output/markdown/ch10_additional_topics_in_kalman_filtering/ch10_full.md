---
type: chapter
chapter: 10
title: Additional topics in Kalman filtering
---

[Image on page 1]


# CHAPTER 10


Additional topics in Kalman filtering


## The use of wrong a priori statistics in the design of a Kalman filter can lead to large
 estimation errors or even to a divergence of errors. --Raman Mehra [Meh72]

The previous chapters covered the essentials of Kalman filtering and should provide a firm foundation for further studies. This chapter discusses some additional important topics related to Kalman filtering. Section 10.1 talks about how to verify that a Kalman filter is operating reliably. When we run computer-based simulations of a Kalman filter, we can tell if the filter is working because we are in control of the *simulation model and so we can compare the true state with the estimated state.* However, in the real world we do not know what the true state is - after all, that is why we need a Kalman filter. In those situations, it is more difficult to verify that the Kalman filter’s estimates are reliable. Section 10.2 discusses multiplemodel estimation, which is a way of estimating system states when we are not sure of which model is governing the dynamics of the system. This can be useful when the system model changes due to events of which the engineer may not be aware. Section 10.3 discusses reduced-order filtering. Many system models are of high order, which means that the corresponding Kalman filter will also be of high order. The high order of the filter may prevent the real-time implementation of the Kalman filter due to computational constraints. In these

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **297**

---

**298**

cases a smaller, suboptimal filter (called a reduced-order filter) can be designed to give acceptable estimation performance at a lower computational cost. Section 10.4 discusses robust Kalman filtering, which is a way of making the filter less sensitive to variations in the assumed system model. Section 10.5 discusses the topic of delayed measurements. Sometimes the measurements do not arrive at the filter in chronological order because of processing delays. In these cases, we can modify the filter to optimally incorporate measurements that arrive at the filter in the wrong sequence.


## 10.1 VERIFYING KALMAN FILTER PERFORMANCE


We can verify Kalman filter performance, or adjust the gain of the Kalman filter, using our knowledge of the statistics of the innovations. The innovations is defined 
# as ( y k  - H k ? , ) ,
 and in this section we will show that it is a zero-mean white 
# stochastic process with a covariance of ( H k p F  H: + &).
 *Recall our original system model, along with the one-step a priori update equa-* tion for the state estimate:


## x k  = F k - 1 X k - l - k  w k - 1


## Yk = H k x k  +'"k
 
# ?;+I = Fk?, + F k K k ( Y k  - Hk?;)
 (10.1)

**The innovations is defined as the quantity in parentheses in the update equation.** The innovations can be thought of as the part of the measurement that contains new information and that is therefore used to update the state estimate (apart from our knowledge of the state transition matrix). If the innovations was zero then the state estimate would simply be updated according to the state transition matrix. **A nonzero innovations allows the measurement to affect the state estimate. The** **innovations Tk can be written as**

**where € k ,  the a priori estimation error, is defined by the above equation. The** **covariance of the innovations is given as**


# E['?'kTT] = E [ ( H k € k  + 'Uk)(Hi'& + W i ) T ]
 **(10.3)**


## Let us see what the covariance is when k # i. We can assume without loss of
 
## generality that k > i. We then obtain


**(10.4)**

**Note that two of the cross terms reduced to zero because of the whiteness of Wk,** 
## and the fact that the estimation error € a  is independent of 'uk for k > i. In order
 **to evaluate this Covariance, we need to evaluate E ( E k E T )  and E ( E k w T ) .  First we**

---


[Image on page 3]


**299**

**will evaluate E ( E k E T ) .  In order to evaluate this term, notice that the a priori state** estimate can be written as follows:

(10.5)

*The a priori estimation error can be written as*

**Ek+1** 
## = x k + l  - ?;+i
 = = = 
# $ k € k  + vk
 (10.6)

**where & and w(, are defined by the above equation. This is a linear discretetime** **system for Ek with the state transition matrix**


# F k ( X k  - 5;) - F k K k H k ( X k  - 3;)
 
# -k w k  - F k K k V k


# F k ( I  - K k H k ) E k  -k ( W k  - F k K k V k )


**Ek can be solved from the initial condition** as follows:

**j =a**

**The covariance of EkET can be written as**

(10.7)

(10.8)

(10.9)

We see that all of the W ~ E T terms in the above expression are zero-mean. This is **because all of the wi noise terms occur at time i or later and so do not affect ~ i .** 
# [Note from Equation (10.6) that ~i is affected only by the noise terms at time (i - 1)
 or earlier.] Therefore,


## E ( V i E T )  = 0
 
## ( j  2 i)
 (10.10)

**We therefore see that Equation (10.9) can be written as**

(10.11)

**Now that we have computed E ( E k € r ) ,  we need to solve for E ( E k V T )  in order to** **arrive at our goal, which is the evaluation of Equation (10.4). E ( e k v T )  can be** **written as**

(10.12)

---

**300**

**The E ~ V T** term in the above expression is zero-mean, and the V ~ V T terms are zero- 
## mean for j > i. The above covariance can therefore be written as


**E(Ek'$)** 
## = E ($k,z+lViVT)


# = E ($k,i+l(Wi - F&ivi)vT)


## = -$k,z+iFtKt&
 (10.13)

Substituting this equation, along with Equation ( l O . l l ) ,  into Equation (10.4) gives

(10.14)

**So we see that the innovations Tk is white noise. Our next task is to determine its** **covariance. In order to do this we write the covariance as**

We therefore see that the innovations is a white noise process with zero mean and 
# a covariance of (HkPiHF + Rk). While the Kalman filter is operating, we can
 process the innovations, compute its mean and covariance, and verify that it is white with the expected mean and covariance. If it is colored, nonzero-mean, or has the wrong covariance, then there is something wrong with the filter. The most likely reason for such a discrepancy is a modeling error. In particular, an incorrect **value of F ,  H ,  Q, or R could cause the innovations to statistically deviate from its** **theoretically expected behavior. Statistical methods can then be used to tune F ,** **H ,  Q, and R in order to force the innovations to be white zero-mean noise with** 
# a covariance of (HkPLHk + Rk) [Meh7O, Meh721. This concept is illustrated in
 **Figure 10.1. A scalar example is presented in Problem 10.1.** **Alternatively, if the engineer is uncertain of the correct values of F, H ,  Q, and R,** then a bank of Kalman filters can be run in parallel, each Kalman filter with a value **of F ,  H ,  Q, and R that the engineer thinks may be likely. Then the innovations** can be inspected in each filter, and the one that matches theory is assumed to have

---


[Image on page 5]


301

**Figure 10.1** This figure illustrates how the performance of a Kalman filter can be used **to tune the values of F ,  H ,  Q,** and R in order to obtain residual statistics that agree with *theory. Alternatively, the K h a n  gain K could be tuned directly.*

**the correct F, H ,  Q, and R, so the state estimate that comes out of that filter is** **probably the most correct. See [Kobo31 for an application of this idea.** The analysis of this section can also be conducted for the continuoustime Kalman *filter. The continuous-time innovations, y(t) - H(t)?(t), is a zero-mean white* *stochastic process with a covariance R(t) (see Problem 10.2).*


## 10.2 M U LT I P L E- M 0
 
## D E L EST1 M AT1 0
 
## N


Suppose our system model is not known, or the system model changes depending on unknown factors. We can use multiple Kalman filters (one for each possible system model) and combine the state estimates to obtain a refmed state estimate. Remember Bayes’ rule from Section 2.1:

(10.18)

*Suppose that a random variable x can take one of N mutually exclusive values* *21, . . . , X N .  Then we can use Bayes’ rule to write*

(10.19)

where we have used the fact that the probability of an event occurring is directly proportional to the value of its pdf. Now suppose that we have the timeinvariant system

xk =

Yk =

wk

vk

**The parameter set p is defined a**

(10.20)

~~ se that p can take **one of N possible values pl,** 
# , p
 **~** **.** The question that’we want to answer in this section is as follows: Given the measurements Yk, what is the probability that 
## p = p j ?  From Equation (10.19) this probability can be written as


(10.21)

---

**302**

Now think about the probability that measurement Yk is observed given the fact 
## that p = p j .  If p = pj then the state will take on some value Xk that is determined
 **by the parameter set p j .  We therefore see that**


## However, if our state estimate is accurate, then we know that Xk M ?;.
 Therefore, the above equation can be written as

pdfbk Ipj) pdfbk 15;) 
## ( 10.23)


The right side of the equation is the pdf of the measurement Yk given the fact that 
# the state is 2;. But since yk M H?; + 'uk, this pdf is approximately equal to the
 pdf of (Yk - H2;). We therefore have

pdf(Yk Ipj) pdf(yk - Hk2;) = pdf(Tk) **(10.24)**

**where Tk is the residual defined in Section 10.1. From Section 10.1 we see that if Wk,**

**Wk, and 20 are Gaussian, then the residual Tk is a linear combination of Gaussian** **random variables. Recall from Section 2.4.2 that a linear combination of Gaussian** **random variables is itself Gaussian. In Section 10.1 we found the mean and variance** of Tk. The pdf of Tk, which is approximated by the pdf of Yk given pj, can therefore **be aDDroximated as**


## ( 10.25)


where Tk = Yk -Hk?;, s k  = HkPiH:+Rk, *and q is the number of measurements.* Now from Bayes' rule we can write the following equation for the probability 
## that p = p3 given the fact that the measurement Yk-1 is observed.


**(10.26)**


# If we are presently at time k, then the measurement at time (k - 1) is a given. The
 
# value of the measurement at time (k - 1) is a certain event with a probability equal
 to one. Therefore, Pr(yk-llpj) = PT(Yk-1) = 1 and the above equation becomes


## Pr(pj I Yk - 1) = Pr(pj )
 **(10.27)**

**Now in Equation (10.21) we can substitute this equation for Pr(pj), and we sub-** **stitute Equation (10.25) for pdf(yk1pj). This gives a timerecursive equation for** 
## evaluating the probability that p = pj given the fact that the measurement was
 **equal to Yk. The multiplemodel estimator can be summarized as follows.**

**The multiple-model estimator**


## 1. For j = l , . . . , N ,  initialize the probabilities of each parameter set before
 **any measurements are obtained. These probabilities are denoted as Pr(pj 190)** ( j = l , . . . , N )  .

---

**303**

**2. At each time step k we perform the following steps.**


# (a) Run N Kalman filters, one for each parameter set pj ( j  = 1,. , N ) .
 *The a priori state estimate and covariance of the j t h  filter are denoted* **as 2& and Pk>.**

**(b) After the measurement at time k is received, for each parameter set** approximate the pdf of Yk given p, as follows:


## ( 10.28)


*where r k  = yk - Hk2ij, s k  = HPGHT + Rk, and q is the number of* measurements.


## (c) Estimate the probability that p = p j  as follows.


**(d) Now that each parameter set pj has an associated probability, we can** 
# weight each 2ij and Pg accordingly to obtain


**N**

**j=1** **N** **(10.30)**

**j=1**

(e) We can estimate the true parameter set in one of several ways, depending on our application. For example, we can use the parameter set with the highest conditional probability as our parameter estimate, or we can **estimate the parameter set as a weighted average of the parameter sets:**

argm%j Pr(pj Iyk) max-probability method *c:=,* Pr@j 1yk)pj weighted-average method **(10.31)**

**As time progresses, some of the Pr(pjlyk) terms will approach zero. Those pj** **possibilities can then be eliminated and the number N can be reduced.** 
## In Equation (10.31), the function argmax,f(z) returns the value of z at which
 the maximum-of f(z) 
# occurs. For example, max( 1 - z)2 = 0 because the maximum
 
# of (1 - z)2 is 0, but argmax,(l - z)' = 1 because (1 -
 attains its maximum value when z = 1. A similar definition holds for the function argmin.

**EXAMPLE 10.1**

In this example, we consider a second-order system identification problem [Ste94]. Suppose that we have a continuous-time system with discrete-time measure- ments described as follows:

---

**304**

**1** = [ O *-w;* **-26wn I.+[ 4-I**


## ( 10.3 2)


The damping ratio 6 = 0.1, and the process and measurement noise covari- **ance Qc and R are respectively equal to 1000 and 101. The natural frequency** 
## wn = 2, but this is not known to the engineer. The engineer knows that w;
 **is either 4, 4.4, or 4.8 with the following a priori probabilities:**


## Pr(wi = 4) = 0.1
 
## Pr(wi = 4.4) = 0.6
 
## Pr(wi = 4.8) = 0.3


**The state equation can be written as**


## k = A X + W
 **w** *N ( O , B Q , B ~ )*

**(10.33)**

**(10.34)**

**We can discretize the system using the technique given in Section 1.4. If the** measurements are obtained every 0.1 seconds, then we discretize the state *equation with a sample time of T = 0.1 to obtain*


## X k  = F Z k - 1 + A W 6 - 1


## F = exp(AT)
 
## A = (F-I)F-I
 **(10.35)**

**From Section 8.1 we know that the covariance Q' of the discretetime noise** **wi is given as**

This means that the discretetime process dynamics can be written as *Q' = BQ,BTT* **(10.36)**


## x k  = F X k - 1  f w k - 1


**wk** *N(O,Q)* *Q = ( F  - 1)F-l(BQB*T)FwT(FT - I )* **(10.37)**

**The multiplemodel estimator described in this section was run on this exam-** ple. Three Kalman filters running in parallel each generate an estimate of the **state. As the filters run, the probability of each parameter is updated by the** multiplemodel Kalman filter. Figure 10.2 shows the parameter probabilities for a typical simulation run. It is seen that even though the correct parameter has the lowest initial probability, the multiplemodel filter estimate converges to the correct parameter after a few seconds. vvv

---


[Image on page 9]


**305**

o . ; **0.8**

**0.71**


# - - - Probability that a: = 4.4


**. b ' c . Probability that coi = 4.8**

**0** **10** **20** **30** **40** **50** **60** **Seconds**

**Figure 10.2** Parameter probabilities for the multiple-model Kalman filter for **Example 10.1. The true parameter value is 4, and the filter converges to the correct** parameter after a few seconds.


## 10.3 REDUCED-ORDER KALMAN FILTERING


If a user wants to estimate only a subset of the state vector, then a reduced-order filter can be designed. This can be the case, for example, in a real-time application where computational effort is a main consideration. Even in off-line applications, some types of problems (e.g., weather forecasting) can involves tens of thousands **of states, which naturally motivates reduced-order filtering as a means to reduce** computational effort [Pha98, BalOl]. Various approaches to reduced-order filtering have been proposed over the years. For example, if the dynamic model of the underlying system can be reduced to a lower-order model that approximates the full-order model, then the reduced-order model can form the basis of a normally designed Kalman filter [Ke199]. This is the approach taken in [Gli94, Sot991 for motor state estimation, in [Sim69, Ara941 for navigation system alignment, in [Bur93, Pat981 for image processing, and in [Cha96] for audio processing. If some of the states are not observable then the Kalman filter Riccati equation reduces to a lower-order equation [Yon80]. Reduced-order filtering can be implemented by approximating the covariance with a lower-rank SVD-like decomposition [Pha98, BalOl]. If some of the measurements are noise free, or if there are known equality constraints between some of the states, then the Kalman filter **is a filter with an order that is lower than the underlying system [Bry65, Hae981 as** discussed in Section 7.5.1 of this book. Optimal reduced-order filters are obtained from first principles in [Ber85, Nag871. A more heuristic approach to reduced- order filtering is to decouple portions of the matrix multiplications in the Kalman filter equations [Chu87]. In this section we will present two different approaches to reduced-order filtering.

---

**306**

**10.3.1**

Anderson and Moore [And791 suggest a framework for reduced-order filtering that is fully developed in [SimOGa] and in this section. This approach is based on the idea that we do not always need to estimate all of the states of a system. Sometimes, *with a system that has n states, we are interested only in estimating m linear* *combinations of the states, where m < n. In this case, it stands to reason that* *we could devise a filter with an order less than n that estimates the m linear* combinations that we are interested in. Suppose our state space system is given as

**Anderson's approach to reduced-order filtering**

**(10.38)**

**We desire to estimate the following m linear combinations of the state: TTZ, q 2 ,** . 
# a ., TKZ, where each T,' is a row vector. Define the n x n matrix T as


**(10.39)**


## where S is arbitrary as long as it makes T a nonsingular n x n matrix. Now perform
 the state transformation


## x = T?t
 **(10.40)**


## This means that Z = T-lx. From these relationships we can obtain a state space
 **description of the system in terms of the new state as follows:**

**T - ' X k + l** 
## = FT-lXk f
 **G W k**

**x k + 1** 
## = Tp"T-lxk+T&k
 
## = F X k f G W k


## Yk = H T - l X k f  V k
 
## = H x k + V k
 **(10.41)**

*where F ,  G, and H are defined by the above equations. Remember that our goal* 
## is to estimate the first m elements of x ,  which we will denote as 5. We therefore
 **partition x as follows:**


# x =  [ ;]
 **(10.42)**

**We can then write equations for z k + 1 ,  & + I ,** **and y k  as follows:**


# zk+1 = F11z.k -l-
 
# F12& + Giwk


**h k + l** 
# = F2 iZ k  f F22hk + Gzwk


# Y k  = Hlzk f H 2 2 k  f v k
 **(10.43)**

*where the Fij, Gi, and H, matrices are appropriately dimensioned partitions of* **F ,  G, and H. Now we propose the following form for the one-step a posteriori** *estimator of 5:* 
# ii+1 = F11ii + K k ( y k + l  - H1Flli:)
 **(10.44)**

---


[Image on page 11]


**307**

**This predictor/corrector form for the estimate of 2 is very similar to the predic-** **tor/corrector form of the standard Kalman filter. The estimation error is given as** follows:

c+ 
# ek+l = 2k+l - zk+l


*= Fii(& - k:)* *f F 1 2 i k  + G i W k  - K k ( Y k + i  - HiFiik;)* 
# = (I - KkH1)Fllek + [F12 - Kk(H1F12 - HZF22)]5k -


*KkH2F215.k - Kkvk+l+ [Gl - Kk(HlG1 + H2G2)lwk*

Now we will introduce the following notation for various covariance matrices:

**(10.45)**


## Pk = E(ekeF)
 *& = E(Zk2:)*


## F k  = E(ik$T)


*C k  = E(Zk5;)*

*f i k  = E(kkzr)*

*f i k  = E(kk5T)* (10.46)

With this notation and the equations given earlier in this section, we can obtain the following expressions for these covariances:

---

**308**

**Now we can find the optimal reduced-order gain Kk at each time step as follows:**

**(10.49)**

**In order to compute the partial derivative we have to remember from Section 1.1.3** that

*=* *B* 
## dTr ( BAT)
 **aA** **(10.50)**

Armed with these tools we can compute the partial derivative of Equation 10.49 and set it equal to zero to obtain


## Kk = AL1Bk
 **(10.51)**

**where Ak and Bk are given as follows:**


# (HlF12 + HZF22)Fk(HlF12 f H2F22)T -k


# [(HlFlP + HZF22)zTF$HT] + [' * '1' + H2F21FkF21H2 -k
 **T** **T**


# Rk+l+ (H1G1 + HzGz)Qk(HzGi + H z G z ) ~


**Bk** = 
# F11pk + F12z; - FlzfiT) F&HT +
 (


# (Fllzk - F l l f i k  + FlZFk) (HlF12 + H2F22)T -k


*T* *T* 
# (Fiih - Fill% + Fizz:) FZIHZ + GiQk(HiG1 4- H z G z ) ~  (10.52)


**Equation (10.51) ends up being a long and complicated expression for the reduced-** order gain. In fact, this reduced-order filter is probably more computationally *expensive than the full-order filter (depending on the values of m and n). However,* if the gain of the reduced-order filter converges to steady state, then it can be computed off-line to obtain savings in real-time computational cost and memory usage. However, note that the reduced-order filter may not be stable, even if the full-order Kalman filter is stable.

**EXAMPLE 10.2**

Suppose we are given the following system:

0.9 0.1

**2k+1** 
# = [ 0.2 0.71 2k + [ ] wk


---


[Image on page 13]


**309**

(10.53)

**We want to find a reduced-order estimator of the first element of x. In this** example the reduced-order gain of Equation (10.51) converges to a steady- state value after about 80 time steps. The estimation-error variance of the reduced-order filter converges to a value that is about 10% higher than the **estimation-error variance of the full-order filter for the first state, as shown** in Figure 10.3. The estimation error for the reduced-order filter and the full- order filter is shown in Figure 10.3 for a typical simulation. In this example, the standard deviation of the estimation error was 0.46 for the full-order filter and 0.50 for the reduced-order filter. The steady-state full-order estimator is **given as follows:**

0.9 0.1 **%+l** 0.2 0.7

**jj+** **k** 
## = ? i f K ( y k - [  O
 112;)

0.1983 = [ 0.11681

**The steady-state reduced-order estimator is given as follows:**

(10.54)

(10.55)

vvv


## 10.3.2 The reduced-order Schmidt-Kalman filter


Stanley Schmidt's approach to reduced-order filtering can be used if the states are decoupled from each other in the dynamic equation [Sch66, Bro96, GreOl]. This happens, for instance, if colored measurement noise is accounted for by augment- ing the state vector (see Section 7.2.2). In fact, satellite navigation with colored measurement noise was the original motivation for this approach. Suppose we have a system in the form

**?Jk** *(O,R)* (10.56)

**We want to estimate i?k but we do not care about estimating i k .  Suppose we use a** Kalman filter to estimate the entire state vector. The estimation-error covariance

---


[Image on page 14]


**310**

**'C** **>" 0.6** **E** 
## y 0.4


## g 0.2
 **E**

**c**

**Reduced-order variance** ' a ' ' ' ' c  - **Full-order variance**

- ,. , , . , , , , , , , , . / , , , , , . . / , I . . I I , I I I I , ~ I I I I I I I 1

-

**1.5-**

**/ , I . * , ,  Standard Kalman filter error** - **Reduced-order filter error** '

**0** **10** **20** **30** **40** **50** **Time Step**

**Figure 10.3** Results for Example 10.2. The top figure shows the analytical estimation- **error variances for the first state for the full-order filter and the reduced-order filter. As** expected, the reduced-order filter has a higher estimation-error variance, but the small degradation in performance may be worth the computational savings, depending on the application. The bottom figure shows typical error magnitudes for the estimate of the first state for the full-order filter and the reduced-order filter. The reduced-order filter has slightly larger estimation errors.

**can be partitioned as follows:**

*' = [ c T* **P** **c** 
# F ]
 (10.57)

We are omitting the time subscripts for ease of notation. The Kalman gain is 
# usually written as K = P-HT(HP-HT + R)-l. With our new notation it can be
 **written as follows:**

*K =*

**L** **J**

*[ gi ] [( H I  H2 ) ( (C-)T '-* 
# P ) ( gi ) + R1-l (10.58)


**By multiplying out this equation we can write the formula for I? as follows.**


# K = (P-HT + C-H:)Q-~
 (10.59)


## where Q is defined as


(10.60)

---


[Image on page 15]


311


# The measurement-update equation for 53 is normally written as 53; = 3 i  + K ( y k  -
 **H53L). With our new notation it is written as**

(10.61)

**A -** 
## Since we are not going to estimate $ with the reduced-order filter, we set i k  = 0 in
 the above equation to obtain the following measurement-update equation for -+ :


## The measurement-update equation for P is usually written as P+ = ( I - K H ) P - ( I -
 
# K H ) T  + KRKT. With our new notation it is written as


*[( 0' ;) - ( i )* 
# ( H I  H2 )IT+ ( f ) R (  K T  kT ) (10.63)


**I** 
$$
At this point, we assume that I? = 0. This can be justified if the measurement
$$
 **noise associated with the 5 states is large, or if H2 is small, or if the elements of** are small. The elements are then referred to as consider states, nuisance states, or nuisance variables, because they are only partially used in the reduced-order state estimator, and because we are not interested in estimating them. Based on **Equation (10.63), the update equation for p+ can then be written as**


# P+ = ( I  - R H 1 ) P - ( I  - K H I ) ~
 
# - K H z ( C - ) ~ ( I  - K H I ) ~
 -


# ( I  - K H 1 ) C - H r K T  + K H $ - H r K T  + KRKT
 (10.64)

**Multiplying out the above equation and then using the definition of cr from Equa-** tion (10.60) results in


## p+ = p- - K H I P -  - P - H T K T  +
 
# - KH2(C-)T - C - H r K T
 
# = P- - K H 1 P  - P-HTKT + ( F H T  + C-H,T)KT - KH2(C-)T -
 **C - H r K T** 
# = (I - R H 1 ) P -  - R H z ( C - ) ~
 (10.65)

**This gives the measurement-update equation for p+. We can go through similar** manipulations with Equation (10.63) to obtain -- 
## C+ = ( I - k H l ) C - - k H 2 P
 - - ;+ 
## = p
 (10.66)

Putting it all together results in the reduced-order Schmidt-Kalman filter. We can **summarize the reduced-order filter as follows.**

---

**312**

**The reduced-order Schmidt-Kalman filter**

1. The system and measurement equations are given in Equation (10.56).

(10.67)

**EXAMPLE 10.3**

Consider the following system:

(10.68)

Figure 10.4 shows a typical example of the estimation error of the first element of the state vector for the full-order filter and the reduced-order filter. It is seen that the performances of the two estimators are virtually identical. In other words, we can save a lot of computational effort with only a marginal degradation of estimation performance by using the reduced-order filter. vvv

**10.4** **ROBUST KALMAN FILTERING**

The Kalman filter works well, but it assumes that the system model and noise statistics are known. If any of these assumptions are violated then the filter estimates can degrade. This was noted early in the history of Kalman filter- ing [S0065, Hef66, Nis661. Daniel Pena and Irwin Guttman give an overview of several methods of robusti- fying the Kalman filter [Spa88, Chapter 91. For example, although the Kalman filter

---


[Image on page 17]


**313**

**2.E**

**2**

**L** **9**

**.P**

- 1

**b 1.5**

**2**

**w"**

**C** +

**0.5**

**C**

**Full-Order Filter** **Reduced-Order Filter**

**5** 10 **15** **20** **Time Step**

**Figure 10.4** Results for Example 10.3. Typical error magnitudes for the estimate of the first state for the full-order filter and the reduced-order filter. The reduced-order filter has only slightly larger estimation errors.

is the optimal linear filter, it is not the optimal filter in general for non-Gaussian noise. Noise in nature is often approximately Gaussian but with heavier tails, and the Kalman filter can be modified to accommodate these types of density func- tions [Mas75, Mas77, Tsa831. Sometimes, measurements do not contain any useful information but consist entirely of noise (probabilistically), and the Kalman filter can be modified to deal with this possibility also [Nah69, Sin73, Ath77, Bar781. **The problem of Kalman filtering with uncertainties in the system matrix Fk, the** **measurement matrix Hk, and the noise covariances Qk and Rk, has been consid-** ered by several authors [Xie94, Zha95, Hsi96, The96, XieO41. This can be called adaptive filtering or robust filtering. Comparisons of adaptive filtering methods for navigation are presented in [Hid03]. Continuous-time adaptive filtering is discussed **in [Bar05, MarOB]. Methods for identifying the noise covariances Q and R are pre-** sented in [Meh7O, Meh72, Als74, Mye761. Additional material on robust Kalman filtering can be found in [Che93]. In this section we present a conceptually straightfornard way of making the *Kalman filter more robust to uncertainties in Q and R [Kos04]. Suppose we have* the linear time-invariant system

(10.69)

**Now suppose that a general steady-state gain K (not necessarily the Kalman gain)** is used in a predictor/corrector type of state estimator. The state estimate update **equations are then given as follows:**

---


[Image on page 18]


**314**

**2;+l** 
## = F2;
 
## 2i+l =
 
# + K(!/k+l - Hki+l)
 
# = F2; + K(HZk+l + uk+l - HF2;)
 
# KHzk+l -k (I - KH)Ffi + K2)k+l
 
# (KHFzk + KHwk) + (I - K H ) F k i  + KZ)k+l
 = = (10.70)

**The error in the a posteriori state estimate can be written as**

**ek+l** 
## = z k + 1  -
 
# = (FZk + wk) - [(KHFZk + KHwk) + (I - KH)FP; + K2)k+1]
 
# = (I - KH)FZk + (I - KH)wl, - (I - K H p ;  - KWk+l
 
# = (I - KH)Fek f (I - KH)wk - K2'k+l
 (10.71)

**So the covariance of the estimation error can be written as**

**p k + l** 
## = E(ek+leT+;,)
 
# = ( I  - KH)FPkFT(I - KH)T + (I - KH)Q(I - KH)= +
 *K R K ~* (10.72)

*The steady-state covariance P satisfies the following Riccati equation:*

*P = ( I  - KH)FPFT(I -* 
# + (I - KH)Q(I - KH)T + KRKT
 (10.73)

Note that we derived this without making any assumption on the optimality of the *filter gain K. That is, this equation holds regardless of what filter gain K we use.* Now we can consider what happens when there is no measurement noise, and what **happens when there is no process noise. Define PI as the steady-state estimation-** 
## error covariance when R = 0, and P2 as the steady-state estimation-error covariance
 *when Q = 0. The above equation for P shows that*

*Pi* 
# (I - KH)FPIFT(I - KH)= + (I - KH)Q(I - KH)T
 *p2 = (I - K H ) F P ~ ( I* *- K H ) ~* *+ K R K ~* (10.74) =

Adding these two covariances together results in

*Pi + P2* 
# = ( I  - KH)FPIFT(I - KH)T + (I - KH)Q(I - KH)T +
 *(I - KH)FP2FT(I - KH)T + KRKT*

*( I  - KH)Q(I - KH)T + KRKT* *= ( I  - KH)F(Pl+ PZ)FT(I - KH)T +* (10.75)

*Comparing this equation with Equation (10.73) shows that P and the sum (PI +P2)* both satisfy the same Riccati equation. This shows that

*P = PI + Pz* (10.76)

This shows an interesting linearity property of a general predictor/corrector type of state estimator. The estimation covariance is equal to the sum of the covariance

---


[Image on page 19]


**315**

due to process noise only and the covariance due to measurement noise only. Recall 
## from Chapter 5 that the Kalman filter was designed to minimize the trace of P. So
 *the Kalman filter minimizes the trace of (PI + P2).* Now suppose that the true process noise and measurement noise covariancea are different from those assumed by the Kalman filter. The filter is designed under the *assumption that the noise covariances are Q and R, but the true noise covariancea* **are Q and R:**

*Q = (1+a)Q* *R = (1+P)R* (10.77)


## where LY and P are unknown scalars. These differences between the assumed and
 **true covariances will result in a change in the estimation-error covariance of the fil-** ter. The true estimation-error covariance will be equal to the assumed covariance **P plus some difference AP. This can be written as**


## F =
 *P + AP =* *( I  - KH)FFFT(I - KH)= + ( I  - KH)Q(I - KH)= + KRKT* *( I  - KH)F(P + AP)FT(I - KH)= +* *(1 + a)(I - KH)Q(I -* *+ (1 + P)KRKT* (10.78)

Comparing this equation with Equation (10.73) shows that


# A P = ( I  - KH)FA PFT( I - KH)T + a( I - KH)Q(I - KH)= + PKRKT (10.79)


Now we repeat this same line of reasoning for the computation of the true estimation- 
# error covariance when the process noise is zero (A = PI + API) and the true
 *estimation-error covariance when the measurement noise is zero (4 = P2 + AP2).* Equation (10.74) shows that

=

*Pi + AP1 =* *(I - KH)FPIFT(I - KH)= + (I - KH)Q(I - KH)T* *(I - KH)F(Pi + AP1)FT(I - KH)= +* *(1 + cr)(I- KH)Q(I - KH)T*

*(I - KH)F(Pz + AP2)FT(I - KH)* + (1 + P)KRKT* *l3 = (I - KH)FF2FT(I - KH)T + KkKT* (10.80) *P2 + AP2 =*

Comparing these equations with Equation (10.74) shows that

*AP1* *AP2 = ( I  - KH)FAP2FT(I - KH)T + PKRKT* (10.81) *= (I - KH)FAPIFT(I - KH)= + a(I - KH)Q(I - KH)=*

Adding these two equations and comparing with Equation (10.79 shows that

*A P  = AP1+ AP2* (10.82)

Comparing Equations (10.74) and (10.81) shows that

*AP1 =  CUP^* *AP2 = PP2*

Combining Equations (10.82) and (10.83) shows that

(10.83)

*AP =* *PP2* (10.84)

---


[Image on page 20]


**316**


## Now suppose that Q and P are independent zero-mean random variables with vari-
 *ances n: and a;, respectively. The previous equation shows that*


# E[73(AP)1 = E(Q)Tr(Pl) + E(P)Tr(P2)


# E { [Tr(AP)I2} = E { IQTr(X1) + PTr(X2)I2}
 = o


# = n:Tr2(P1) + 4Tr2(P2)
 (10.85)

This gives the variance of the change in the estimation-error covariance due to **changes in the process and measurement-noise covariances. A robust filter should** try to minimize this variance. In other words, a robust filter should have an estimation-error covariance that is insensitive to changes in the process and measurement- noise covariances. So the performance index of a robust filter can be written as follows:


## where p is the relative importance given to filter performance under nominal con-
 
# ditions (i.e., when Q and R are as expected), and (1 - p) is the relative importance
 
# given to robustness. In other words, ( 1  - p) is the relative weight given to min-
 imizing the variation of the estimation-error covariance due to changes in Q and 
## R. If p = 1 then we have the standard Kalman filter. If p = 0 then we will mini-
 mize changes in the estimation-error covariance, but the nominal estimation-error 
## covariance may be poor. So p should be chosen to balance nominal performance
 *and robustness. Unfortunately, the performance index J cannot be minimized an-* *alytically, so numerical methods must be used. PI and P2 are functions of the gain* *K and can be computed using a DARE function in control system software. The* *partial derivative of J with respect to K must be computed numerically, and then* *the value of K can be changed using a gradient-descent method to decrease J .*

**EXAMPLE 10.4**

Suppose we have a discretized second-order Newtonian system that is driven 
## by an acceleration input. z( 1) represents position, 4 2 )  represents velocity,
 **Uk represents the known acceleration input, and Wk represents the noisy ac-** **celeration input. This is the same as the system described in Example 9.1.** The system is described as follows:

**1 T** **T2/2** 
# xk+l = [ 0
 **1 ] . k + [** **T**

(1 0.87)


## The sample time T = 0.1. The variance q2 of the acceleration noise is equal
 **to 0.22, and the variance R of the measurement noise is equal to lo2. Now**

---

**317**

*suppose that Q and R have relative uncertainties of one (one standard devi-* 
## ation). That is, C T ~  = ~ 2 ”
 
## = l. Suppose we find the robust filter gain using
 
## equal weighting for both nominal and robust performance (i.e., p = 0.5). Ta-
 **ble 10.1 shows the average performance of the robust filter and the standard** **Kalman filter when Q and R change by factors of -0.8 and 3, respectively.** One question that remains is, How does the robust filter perform under nom- inal conditions? That is, since the Kalman filter is optimal, the robust filter **will not perform as well as the Kalman filter when Q and R are equal to their** **nominal values. However, Table 10.2 shows that the performance degrada-** tion is marginal. In fact, the robust filter performs identically to the optimal filter (to two decimal places) under nominal conditions. During the gradient- **descent optimization of Equation (10.86), the nominal part of the cost function** **increases from 2.02 to 2.04, the robust part of the cost function decreases from** **2.54 to 2.38, and the total cost function decreases from 2.28 to 2.21.**

**Table 10.1** 
## noise covariances are not nominal ( p  = 0.5, 6 1  = 02 = 1, a = -0.8, p = 3)
 RMS estimation errors for Example 10.4 over 100 seconds when the

Position Velocity

Standard Filter **4.62** **0.38** Robust Filter **4.47** **0.32**

**Table 10.2** 
## noise covariances are nominal ( p  = 0.5, 01 = 02 = 1, a = 0, ,B = 0)
 **RMS estimation errors for Example 10.4 over 100 seconds when the**

Position Velocity

.Standard Filter **1.38** **0.19** Robust Filter **1.38** **0.19**

vvv The robust filtering approach presented here opens several possible research top- ics. For example, under what conditions is the robust filter stable? Is the gain of the robust filter equal to the gain of a standard Kalman filter for some other related system? What is the true estimation-error covariance of the robust filter?


## 10.5
 
## DELAYED MEASUREMENTS AND SYNCHRONIZATION ERRORS


In decentralized filtering systems, observations are often collected at various phys- ical locations, and then transmitted in bulk to a central processing computer. In this type of setup, the measurements may not arrive at the processing computer synchronously. That is, the computer may receive measurements out of sequence. This is typically the case in target-tracking systems. Various approaches have been

---


[Image on page 22]


**318**

taken to deal with this problem [Ale91, Bar95, Kas96, Lar98, MalOl]. The case of delayed measurements with uncertainty in the measurement sampling time is discussed in [Tho94a, Tho94bl. The approach to filtering delayed measurements that is presented here is based on [BarOa]. First we will present yet another form of the Kalman filter that will provide the basis for the delayed-measurement filter. Then we will derive the optimal way to incorporate delayed measurements into the Kalman filter estimate and covariance. In this section, we will have to change our notation slightly in order to carry out the derivation of the delayed measurement Kalman filter. We will use the following notation to represent a discretetime system:


# s ( k )  = F(k - l)z(k - 1) + w(k - 1)


# Y(k) = H ( k ) z ( k )  + 4 k )
 (10.88)

**where w(k) and v(k) are independent zero-mean white noise process with covari-** **ances Q(k) and R(k), respectively.**


## 10.5.1


**Suppose that we have an a priori estimate 2-(k) at time k, and we want to find an** **optimal way to update the state estimate based on the measurement at time k. We** want our update equation to be linear (for reasons of mathematical tractability) so **we decide to update the state estimate at time k with the equation**

**A statistical derivation of the Kalman filter**


# &+(k) = K ( k ) y ( k )  + b(k)
 (10.89)

**where K(k) and b(k) are a matrix and vector to be determined. Our first state esti-** mation criterion is unbiasedness. We can see by taking the mean of Equation (10.89) that - 
# &+(k) = K(k)fj(k) + b(k)
 (10.90)

This gives us the constraint that


# b(k) = 2 ( k )  - K(k)@)
 (10.91)

**This will ensure that 2+(k) is unbiased regardless of the value of the gain matrix** **K(k). Next we find the gain matrix K(k) that minimizes the trace of the estimation** error. First recall that


# P, = E[(z - e)(z - E)T]
 *= E(zzT) -zzT* (10.92)


# for any general random vector z. Now set z = z ( k )  - &+(k). With this definition
 
## of z we see that E = 0. The quantity we want to minimize is given by the trace of
 the following matrix:


# P+(k) = E[(z(k) - ?+(k)>(S(k) - 2+(k))T]
 
# = P, + EET
 (10.93)

**P, can be computed as follows:**

---


[Image on page 23]


**319**


# P, = E { [x(k) - ?+(k) - E(x(k) - ?+(k))][. . a]'}


# E { [x(k) - (K(k)Y(k)
 
# + W))
 
# - Z ( k )  - (K(k)i@) + b(k))l[. a .I*}
 
# E { [(x(k) - Z ( k ) )  - K(k)(Y(k)
 - y(k))l[* * *IT>

= =

*= P-(k) - K(k)P,, - P,,KT(k) + K(k)P,KT(k)* (10.94)

**We are using the symbol P,, to denote the cross covariance between Yk and Zk, P,,** **to denote the cross covariance between Xk and Yk, and P, to denote the covariance** 
## of Yk. Recall that Pxv = P z .  We have omitted the subscript k on P,,, P,,, and P,
 for notational convenience. We combine the above equation with (10.93) to obtain 
# Tr P+(k) = Tr (P-(k) - K(k)P,, - P,,K(k)T + K(k)P,K(k)T) + Tr(ZF)


*Tr (P-(k) - K(k)P,, - P,,K(k)T + K(k)P,K(k)T) +*


# I F(k) - K(kMk) - b(k) I l2
 
# Tr [(K(k) - P,,P,-l)P,(K(k) - Pz,P,-l)T] +


=

=


# Tr (P-(k) - PxVPL'P,T,) + IlZ(k) - K ( k ) g ( k )  - b(k)1I2
 (10.95)


## where we have used the fact that Tr(AB) = Tr(BA) for compatibly dimensioned
 **matrices [see Equation (1.26)]. We want to choose K(k) and b(k) in order to** **minimize the above expression. The second term is independent of K(k) and b(k),** and the first and third terms are always nonnegative. The first and third terms can be minimized to zero when


## K(k) = PxyP;l


# b(k) = Z(k) - K(k)P(k)
 (10.96)

**Note that this is the same value for b(k) that we obtained in Equation (10.91) when** **we enforced unbiasedness in the state estimate. With these values of K(k) and b(k),** we see that the first and third terms in (10.95) are equal to zero, so the estimation- *error covariance P+(k) can be seen to be equal to the second term. Substituting* these values into Equation (10.89) we obtain


## ?+(k) = K(k)y(k)
 
# + Z ( k )  - K ( k ) y ( k )


*P+(k) = P-(k) - PxyP,-'P&*


## = K(k)y(k)
 
# + ?-(k) - K(k)H(k)?-(k)


# &-(k) + K(k)(y(k)
 
# - H(k)?.-(k))
 =

*= P-(k) - K(k)P,K*(k)* (10.97)

*Straightforward calculations (see Problem 10.8) show that P,, and P, can be com-* puted as

*P,,* 
## = P- (k)H(k)T
 
# P, = H(k)P-(k)H(k)T + R(k)
 (10.98)

Now consider our linear discrete-time system:

(10.99)

---


[Image on page 24]


**320**

**The noise processes w(k) and v(k) are white, zero-mean, and uncorrelated, with** **covariances Q ( k )  and R(k), respectively. We saw in Chapter 4 how the mean and** covariance of the state propagates between measurement times. Those equations, along with the measurement-update equations derived above, provide the following Kalman filter equations:

**q** **c** **)** 
# = F(k - l)5+(k - 1)


# P-(k) = F(k - 1)P+(k - l)FT(k - 1) + Q ( k )
 
## Pzv = P-(k)HT(k)
 
# Pv = H(k)P-(k)HT(k) + R(k)
 
## K(k) = PsvP;l


# 2+(k) = r ( k )  + K ( k ) ( y ( k )  - H ( k ) f - ( k ) )
 
# P+(k) = P-(k) - K(k)P,K*(k)
 
# = P-(k) - PzvP;lP&
 ( 10.100)

These equations appear much different than the Kalman filter equations derived earlier in this book, but actually they are mathematically identical for linear sys- tems.


## 10.5.2


Now we need to complicate the notation a little bit more in order to derive the **Kalman filter with delayed measurements. We will write our system equations as**

**Kalman filtering with delayed measurements**

**z ( k )** 
# Y(k) = H(k)z(k) + v(k)
 (10.101)


# = F(k, k - l)z(k - 1) + w(k, k - 1)


# F(k, k - 1) is the matrix that quantifies the state transition from time (k - 1) to
 
# time k. Similarly, w(k, k - 1) is the effect of the process noise on the state from
 
# time (k - 1) to time k. We can then generalize the statespace equation to the
 following:

**where ko is any time index less than k. The above equation can be solved for z ( k 0 )**


# z(k0) = F(ko, k)[z(k) - w(k, k0)l
 (10.103) 
## where F(k0, k) = F - l ( k ,  ko). Note that F(k, ko) should always be invertible if it
 **comes from a real system, because F(k, ko) comes from a matrix exponential that** 
## is always invertible (see Sections 1.2 and 1.4). The noise w(k, ko) is the cumulative
 **effect of all of the process noise on the state from time ko to time k. Its covariance** 
## is defined as Q (k, ko) :
 *w(k, ko) N 10, Q(k, k0)l* (10.104) **At time k we have the standard a posteriori Kalman filter estimate, which is the** **expected value of the state z ( k )  conditioned on all of the measurements up to and** **including time k. We also have the a posteriori covariance of the estimate:**


# z ( k )  = F(k, ko)z(ko) + w(k, ko)
 (10.102)

**as**


## q k )  = E[z(k)ly(l),
 
## * * * 7 Y(k)l
 = ~ [ W l Y ( ~ ) l 
## P(k) =
 
# { [ z ( k )  - W l [ z ( k )  - w T l y ( k ) )
 (10.105)

---


[Image on page 25]


**321**

**where Y (k) is defined by the above equation; that is, Y(k) is all of the measurements** **up to and including time k that have been processed by the Kalman filter. (There** **may be some measurements before time k that have not yet been processed by the** filter. These measurements are not part of Y(k).) Now suppose an out-of-sequence measurement arrives. That is, we obtain a 
## measurement from time ko < k that we want to incorporate into the estimate
 **and covariance at time k. The problem is how to modify the state estimate and** covariance on the basis of this new measurement. The modified state estimate and **covariance are given as follows:**


## W k O )  = E[z(k)IY(k), Y(ko)l


# P(klko) = E { [ z ( k )  - Z(k, ko)][Z(k) - Z(k, ko)lTIY(k), ~ ( k o ) )
 (10.106)

**The approach here is to use the new measurement at time ko to obtain an updated** **state estimate and covariance at time ko, and then use those quantities to update** **the estimate and covariance at time k. We can use Equation (10.103) to obtain**


# E[z(ko)lY(k)l = W o ,  k)E[z(k) - w(k, kO)lY(k)l
 
## = F(k0, k)[Zi.-(k) - d(k, ko)]
 ( 10.107)

**where G(k,ko) is defined by the above equation; it is the expected value of the** **cumulative effect of the process noise from time ko to time k, conditioned on all** **of the measurements up to and including time k [but not including measurement** y(ko)]. Now define the vector

(10.108)

In general, we define the covariance of vector a conditioned on vector c, and the 
## cross covariance of vectors a and b conditioned on vector c, as follows:


*Cov(a1c) = E[(a - ii)(a - ii)TIC]* *Cov(a, blc) = E[(a - a)(b - E)TIC]* (10.109)

We can then generalize Equation (10.100) to obtain


# f ( k )  = i-@) +


Cov[z(k), Y(k)IY(k - l)lcov-l[Y(~)ly(~ 
# - 111 (dk) - H ( W ( k ) )


W . ( k ) ,  Y(k)IY(k - l)lcov-l[Y(k)ly(k - 1)1COV[Y(k), z(k)IY(k - I)]

Cov[z(k)lY(k)] = Cov[z(k)IY(k - l)] - ( 10.1 lo)

**The first covariance on the right side of the above i(k) equation can be written as**

**Now consider the first covariance in the above equation. This can be written as**


# Cov[z(k), y(k)lY(k - 111 = cov { z ( k ) ( H ( k ) z ( k )  + V(k)lTIY(k - 1))
 = cov {z(k)[H(k)z(k)]TJY(k - 1)) 
## = cov{z(k)} HT(k)
 
## = P-(k)HT(k)
 (10.1 12)

---


[Image on page 26]


**322**

**where the covariance of z ( k )  and w(k) is zero since they are independent. Now** consider the second covariance on the right side of Equation (10.111). This can be written as

**where the cross covariances of w(k, ko) with z ( k o ) ,  w(k), and $(k) are zero since** **they are independent. We are using the notation c - ( k )  to denote the expected** **value of y(k) based on measurements up to (but not including) time k. Now con-** sider the conditional covariance of y(k) in Equation (10.110). This was derived in Equation (10.17) in Section 10.1 as


# Cov[y(k)IY(k - l)] = H(k)P-(k)HT(k) + R(k)
 (1 0.114)

**We will write this expression more compactly as**


## Cov[r(k)] = S(k)
 (10.115)


## where the residual r(k) = y(k) - H ( k ) C ( k )  and its covariance S(k) are defined
 by the two above equations. Substituting Equations (10.112) and (10.113) into Equation ( l O . l l l ) ,  and then substituting into Equation ( l O . l l O ) ,  gives

This shows that


## because E[G(k,ko)lY(k - l)] = 0 [since w(k,ko) is independent of the measure-
 ments]. Substituting this expression into Equation (10.107) gives


# E[z(ko)lY(k)I = F(ko, k) [ f ( k )  - Q(k, ko)HT(k)S-'(k)r(k)]
 (10.11 8)

**This is called the retrodiction of the state estimate from time k back to time ko.** Whereas a prediction equation is used to predict the state at some future time, a retrodiction equation is used to predict the state at some past time. In this case, **the state estimate at time k [i.e., f(k)] is retrodicted back to time ko to obtain** **the state estimate at time ko, which is denoted above as E[z(ko)lY(k)]. Note that** E[z(k,-,)lY(k)] is computed on the basis of all the measurements up to and including **time k, but does not consider the measurement at time ko.** Now we can write Equation (10.110) as follows:

---

**323**

(10.119)

From Equation (10.102) we can write

**where we have used the independence of z(k0) and w(k,ko). Now substitute** this equation along with Equations (10.112), (10.113), and (10.114) into Equa- tion (10.119) to obtain

**From this equation we can write the conditional covariance of w(k, ko), and cross** 
# covariance of z (k) and w (k, ko) , as follows:


Using this in Equation (10.103) gives the conditional covariance of the state retro- diction as follows:

---


[Image on page 28]


**324**


## p(ko, k) = cov[z(koji~(k)i
 
# = F(k0, k)Cov[z(k) - w(k, k0)lY(k)IFT(kO, k)


# F(k0, k){Cov[z(k)lY(k)] - Cov[z(k), w(k, ko)IY(k)l -


# COVT[2(k), w(k, kO>lY(k)l + Cov[w(k, ko)lY(k)l}FT(ko, k)


# F(k0, k) {P+(k) - Pzw(k, ko) - P 2 ( k ,  ko)+


=

=


## P W ( k  ko)) FT(ko, k)
 ( 10.123)

Using the above along with Equation (10.101) we obtain the conditional covariance

**OfY(k0) as**

*S(k0) = cov[Y(ko)IY(k)l* = *{ [H(ko).(ko) + 4ko)l[H(ko)z(ko) + .(ko>lTIY(k)}* 
# = H(ko)P(ko, k)HT(ko) + R(k0)
 (10.124)

We can use Equations (10.101) and (10.103) to obtain the conditional covariance **between z ( k )  and y(k.0) as**


## Pz,(k, ko) = W z ( k ) ,  Y(ko)lY(k)l
 
# = Cov{z(k), H(ko)F(ko, k)[z(k) - w(k, k0)l + 4ko)lY(k>)
 
# = [P+(k) - ~ z w ( k ,
 *ko>lFT(ko, k)HT(ko)* (10.125)

**We can substitute this into the top partition of the i(k) expression in Equa-** **tion (10.110) to obtain the estimate of z ( k )  which is updated on the basis of the** measurement y(k0):


# q k ,  ko) = ri.(k) + Pz,(k,
 *ko)S-l(ko>[Y(ko) - H ( k o ) W o ,  k)l* (10.126)

**where f ( k 0 ,  k) is the retrodiction of the state estimate given in Equation (10.118).** From the top partition of the Cov[z(k)IY(k)] expression in Equation (10.110) we obtain

These equations show how the state estimate and its covariance can be updated on the basis of an out-of-sequence measurement. The delayed-measurement Kalman **filter can be summarized as follows.**

**The delayed-measurement Kalman filter**

1. The Kalman filter is run normally on the basis of measurements that arrive **sequentially. If we are presently at time k in the Kalman filter, then we** **have ij-(k) and P-(k), the a priori state estimate and covariance that are** 
# based on measurements up to and including time (k - 1). We also have f ( k )
 **and P(k), the a posteriori state estimate and covariance that are based on** **measurements up to and including time k.**

---

**325**


## 2. If we receive a measurement y(ko), where ko < k, then we can update the


**(a) Retrodict the state estimate from k back to ko as shown in Equa-**

**state estimate and its covariance to 2(k, ko) and P(k, ko) as follows.**

tion (10.118):


# S(k) = H(k)P-(k)HT(k) + R(k)


## 2(k0, k) = F ( ~ o ,
 
# k) [ f ( k )  - Q(k, ko)HT(k)S-'(k)~(k)]
 (10.128)

(b) Compute the covariance of the retrodicted state using Equations (10.122) and (10.123):


# Pw(k, ko) = Q(k, ko) - Q(k, ~ o ) H ~ ( ~ ) S - ~ ( ~ ) H ( ~ ) Q ( ~ ,
 *ko)*


# P z w ( k ,  ko) = Q(k, ko) - P-(k)HT(k)S-l(k)H(k)Q(k,
 *ko)* 
# P(k0, k) = q k o ,  k) {P(k) - P z w ( k ,  ko) - Pzw(
 **k,ko)+**

**Pw(k, ko)IFT(ko, k)** (1 0.129)

**(c) Compute the covariance of the retrodicted measurement at time ko using** Equation (10.124):

*S(k0) = H(ko)P(ko, W T ( k o )  + R(ko)* (10.130)

**(d) Compute the covariance of the state at time k and the retrodicted mea-** **surement at time ko using Equation (10.125):**


# Pz,(k, ko) = [P(k) - Pzw(k, kO)l~T(ko, k)HT(ko>
 (10.131)

**(e) Use the delayed measurement y(k0) to update the state estimate and its** covariance:

It is possible to make some simplifying approximations to this delayed measurement filter in order to decrease computational cost with only a slight degradation in performance [Bar021 .


## 10.6 SUMMARY


In this chapter we discussed some important topics related to Kalman filtering that extend beyond standard results. We have seen how to verify if a Kalman filter is operating reliably. This gives us a quantifiable confidence in the accuracy of our filter estimates. We also discussed multiplemodel estimation, which is a way of estimating system states when we are not sure of which model is governing the dynamics of the system. This can be useful when the system model changes in unpredictable ways. We discussed reduced-order filtering, which can be used to estimate a subset of the system states while saving computational effort. We derived a robust Kalman filter, which makes the filter less sensitive to variations

---

**326**

in the assumed system model. Robust filtering naturally leads into the topic of H, filtering, which we will discuss in Chapter 11. Finally, we derived a way to update the state estimate when a measurement arrives at the filter in the wrong chronological order because of processing delays. There are several other important extensions to Kalman filtering that we have not had time to discuss in this chapter. One is the variable structure filter, which is a combination of the Kalman filter with variable structure control. This guaran- tees stability under certain conditions and often provides performance better than the Kalman filter, especially when applied to nonlinear systems [Hab03]. Another recent proposal is the proportional integral Kalman filter, which adds an integral term to the measurement state update and thereby improves stability and reduces steady-state tracking errors [Bas99]. Another interesting topic is the use of a per- turbation estimator to estimate the process noise . This allows model uncertainties to be lumped with process noise so that the processnoise estimate increases the robustness of the filter [KwoOS].

**PROBLEMS**


## Written exercises


**10.1 In this problem we consider the scalar system**

**z k + l** 
## = z k f w k


## Yk = x k  + v k


**where w k  and V k  are white and uncorrelated with respective variances Q and R,** **which are unknown. A suboptimal steady-state value of K is used in the state** *estimator since Q and R are unknown.* **a) Use the expression for Pi along with the first expression for Pz in Equa-** **tion (5.19) to find the steady-state value of Pi as a function of the sub-** **optimal value of K and the true values of Q and R. [Note that the first** **expression for P$ in Equation (5.19) does not depend on the value for K k** being optimal.] **b) Now suppose that E(rg) and E ( T k + l T k )  are found numerically as the filter** **runs. Find the true value of R and the steady-state value of Pi as a** 
## function of ~ ( r : )
 **and E ( T k f 1 T k ) .**


## c) Use your results from parts (a) and (b) to find the true value of Q.


# 10.2 Show that the innovations r = y - C2 of the continuous-time Kalman filter
 *is white with covariance R.*

**10.3** Consider the system described in Problem 5.1. Find the steady-state vari- 
## ance of the Kalman filter innovations when Q = R and when Q = 2R.


## 10.4
 
## Consider the system of Problem 10.3 with Q = R = 1. Suppose the Kalman
 
## filter for the system has reached steady state. At time k the innovations T k  =


**a) Find an approximate value for pdf(yk lp) (where p is the model used in the** 
## Kalman filter) if Tk = 0, if Tk = 1, and if Tk = 2.


# ’& - 2;.


---


[Image on page 31]


**327**


## b) Suppose that the use of model pl gives T k  = 0, model p2 gives T k  = 1,
 
## and model p3 gives r k  = 2. Further suppose that Pr(pllyk-1) = 1/4,
 
## Pr(pzlyk-1) = 1/4, and Pr(p31Yk-l) = 1/2. Find Pr(pj1yk) forj = 1,2,3.


**10.5 Consider the system described in Example 4.1 where the measurement con-** 
# sists of the predator population. Suppose that we want to estimate x(1) + 4 2 ) ,  the
 **sum of the predator and prey populations. Create an equivalent system with trans-** formed states such that our goal is to estimate the first element of the transformed state vector.

**10.6 Consider the system**


## Yk = [ 1 0 ] Z k + v k


**where wk and V k  are uncorrelated zero-mean white noise processes with Variances** *q and R, respectively.* **a) Use Anderson's approach to reduced-order filtering to estimate the first** **element of the state vector. Find steady-state values for p, P, C, fi, fi,** *and P. Find the steady-state gain K of the reduced-order filter.* b) Use the full-order filter to estimate the entire state vector. Find steady- *state values for P and K .* **c )  Comment on the comparison between your answer for P in part (a) and**

**Consider the reduced-order filter of Example 10.3 with the initial condition**

**a) Find analytical expressions for the steady-state values of I?, a, p+, C+,**


# P', p-, C-, and 3-
 **b) What does the reduced-order filter indicate for the steady-state a posteriori** estimation-error variance of the first state? Find an analytical expression **for the true steady-state a posteriori estimation-error variance of the first** state when the reduced-order filter is used. Your answer should be a **function of ~ ( 2 ) .  Solve for the true steady-state a posteriori estimation-** 
## error variance of the first state when 4 2 )  = 0, when 4 2 )  = 1, and when


**c )  What is the steady-state a posteriori estimation-error variance of the first** state when the full-order filter is used?

10.8 Verify that the two expressions in Equation (10.98) are respectively equal **to the cross-covariance of x and y ,  and the covariance of y.**

10.9 
# Suppose you have the linear system xk+l = Fxk + wk,
 
## where wk N (0, Q k )
 
# is zero-mean white noise. Define w(k + 2, Ic) as the cumulative effect of all of the
 
# process noise on the state from time k to time (k + 2). What are the mean and
 
# covariance of w ( k  + 2, k)?


**10.10**

- -

Part (b). **10.7** **z +** *P, = l .*


## x(2) = 2.


Suppose that a Kalman filter is running with


$$
= [ k  :I
$$


---


[Image on page 32]


**328**

*H* = [ l  0 1

R = l


# An out-of-sequence measurement from time (k - 1) is received at the filter.
 **a) What was the value of P-(k)?** **b) Use the delayed-measurement filter to find the quantities Pw(k,** 
# k - l),
 
# P,,(k, k - l), P(k - 1, k), P,,(k, k - l), and P(k, k - 1).
 
# c) Realizing that the measurement at time (k - 1) was not received at time
 
# (k - l), derive the value of P- (k - 1). Now suppose that the measurement
 
# was received in the correct sequence at time (k - 1). Use the standard
 
## Kalman filter equations to compute P+(k - l), P-(k), and P+(k). How
 
# does your computed value of P+(k) compare with the value of P(k, k - 1)
 that you computed in part (b) of this problem?

**Under what conditions will P, in Equation (10.100) be invertible for all k?** **10.11**

**Computer exercises**

**10.12 Consider the equations**

300~+400y = 700 lOO~+133y = 233

a) What is the solution of these equations? **b) What is the solution of these equations if each constant in the second** equation increases by l ? **c )  What is the condition number of the original set of equations?**

,Repeat Problem 10.12 for the equations **10.13**

300~+400y = 700 1oox+2ooy = 200

Comment on the difference between this set of equations and the set given in Problem 10.12.

**10.14 Tire tread is measured every r weeks. After r weeks, 20% of the tread has** 
# worn off, so we can model the dynamics of the tread height as Xk+1 = fXk + Wk,
 
## where f = 0.8, and Wk is zero-mean white noise with a variance of 0.01. We measure
 **the tread height every T weeks with zero-mean white measurement noise that has** a variance of 0.01. The initial tread height is known to be exactly 1 cm. Write a program to simulate the system and a Kalman filter to estimate the tread height. Run the program for 10 time steps per tire, and for 1000 tires. What is **a)** the mean of the 10,000 measurement residuals?

---


[Image on page 33]


**329**

**b) Suppose the Kalman filter designer incorrectly believes that 30% of the** **tread wears off every 7 weeks. What is the mean of the 10,000 measure** ment residuals in this case? **c )  Suppose the Kalman filter designer incorrectly believes that 10% of the** **tread wears off every 7 weeks. What is the mean of the 10,000 measure-** ment residuals in this case?

10.15 Consider the system described in Problem 10.14. Suppose the engineer does not know the true value off but knows the initial probabilities Pr(f = 0.8) = 
## Pr(f = 0.85) = Pr(f = 0.9) = 1/3. Run the multiple-model estimator for 10
 time steps on 100 tires to estimate f. The f probabilities at each time step can be taken as the mean of the 100 f probabilities that are obtained from the 100 tire simulations, and similarly for the f estimate at each time step. Plot the f **probabilities and the f estimate as a function of time.**

10.16 *Consider a scalar system with F = H = 1 and nominal noise variances* 
## Q = R = 5. The true but unknown noise variances Q and R are given as


*Q = (l+a)Q* 
## R = (1 +P)R
 
## E(a2) = 0: = 1/2
 
## E(P2) = 0; = 1


*where a and P are independent zero-mean random variables. The variance of the a* 
## posteriori estimation error is P if a = P = 0. In general, a and P are nonzero and
 **the variance of the estimation error is P +  AP. Plot P ,  E(AP2), and (P+E(AP2))** **as a function of K for K E [0.3,0.7]. What are the minimizing values of K for the** three plots?

---


## PART 111


THE H, FILTER


[Image on page 35]


*Optzmal State Estamataon, Fzrst Edztzon. By Dan J. Simon* **ISBN 0471708585** *02006 John Wiley li Sons. Inc.*