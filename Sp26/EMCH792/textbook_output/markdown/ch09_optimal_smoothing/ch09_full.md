---
type: chapter
chapter: 9
title: Optimal smoothing
---

[Image on page 1]


# CHAPTER 9


Optimal smoothing

*In a post mortem (after the fact) analysis, it is possible to wait for more observations* to accumulate. In that case, the estimate can be improved by smoothing. -Andrew **Jazwinski jJaz70, p. 1431**

*In previous chapters, we discussed how to obtain the optimal a priori and a* **posteriori state estimates. The a priori state estimate at time k, 2;, is the state** **estimate at time k based on all the measurements up to (but not including) time** **k. The a posteriori state estimate at time k, 2:, is the state estimate at time k** **based on all the measurements up to and including time k:**

There are often situations in which we want to obtain other types of state estimates. 
## We will define 2 k , j  as the estimate of X k  given all measurements up to and including
 *time j .  With this notation, we see that*

Now suppose, for example, that we have recorded measurements up to time index **54 and we want to obtain an estimate of the state at time index 33. Our theory in**

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **263**

---


[Image on page 2]


**264**


## the previous chapters tells us how to obtain 2T3 or 2i'3f3, but those estimates only
 **use the measurements up to and including times 32 and 33, respectively. If we have** 
## more measurements (e.g., measurements up to time 54) it stands to reason that we
 **should be able to get an even better estimate of 233. This chapter discusses some** ways of obtaining better estimates. In another scenario, it may be that we are interested in obtaining an estimate of the state at a fixed time j. As measurements keep rolling in, we want to keep **updating our estimate 2j. In other words, we want to obtain 2j,j+l, 2j,j+z,** **a.** This could be the case, for example, if a satellite takes a picture at time j. In order to more accurately process the photograph at time j we need an estimate of the satellite state (position and velocity) at time j. As the satellite continues to orbit, *we may obtain additional range measurements of the satellite, so we can continue to* **update the estimate of zj and thus improve the quality of the processed photograph.** This situation is called fixed-point smoothing because the time point for which we want to obtain a state estimate (time j in this example) is fixed, but the number of measurements that are available to improve that estimate continually changes. **Fixed-point smoothing is depicted in Figure 9.1 and is discussed in Section 9.2.**

1 1 1 1  1

**Figure 9.1** 
## Fixed-point smoothing. We desire an estimate of 2 4 .  Up until k = 4, the
 
## standard Kalman filter operates. At k = 4, we have 2; = 24,4, which is the estimate of 2 4
 **based on measurements up to and including 93. As time progresses, we continue to refine** 
## our estimate of 2 4  based on an increasing number of measurements. At time k = N ,  we have
 **2 4 , ~ ,** 
## which is the estimate of 2 4  based on measurements up to and including time N - 1.


Another type of smoothing is fixed-lag smoothing. In this situation, we want 
# to obtain an estimate of the state at time (k - N )  given measurements up to and
 **including time k, where the time index Ic continually changes as we obtain new** **measurements, but the lag N is a constant. In other words, at each time point we** **have N future measurements available for our state estimate. We therefore want** 
# to obtain ?k-N,k for k = N , N  + l,..., where N is a fixed positive integer. This
 could be the case, for example, if a satellite is continually taking photographs that **are to be displayed or transmitted N time steps after the photograph is taken. In** **this case, since the photograph is processed N time steps after it is taken, we have** **N additional measurements after each photograph that are available to update the** estimate of the satellite state and hence improve the quality of the photograph. **Fixed-lag smoothing is depicted in Figure 9.2 and is discussed in Section 9.3.** The final type of smoothing is fixed-interval smoothing. In this situation, we 
## have a fixed interval of measurements (yl, y2, . - 3, YM) that are available, and we
 want to obtain the optimal state estimates at all the times in that interval. For each state estimate we want to use all of the measurements in the time interval. That is, **we want to obtain 2 0 , ~ ,** **2 1 , ~ ,** . . 
## a ,  ~ M , M .  This is the case when we have recorded


---


[Image on page 3]


**265**

1 1 1 1

**Figure 9.2** Fixed-lag smoothing. We desire an estimate of the state at each time step **based on measurements two time steps ahead. After processing y2, we form the estimate**

**&,2, which is the estimate of 20 based on measurements up to and including yz. Similarly,**

**?1,3 is the estimate of z1 based on measurements up to and including y3.**

some data that are available for post-processing. For example, if a manufacturing process has run over the weekend and we have recorded all of the data, and now we want to plot a time history of the best estimate of the process state, we can use all of the recorded data to estimate the states at each of the time points. Fixed-interval smoothing is depicted in Figure 9.3 and is discussed in Section 9.4.

1

**Figure 9.3** **Fixed-interval smoothing. We desire an estimate of the state at each time step** **based on all of the measurements in some interval. After processing all of the measurements** kom y1 to y ~ , **we form the estimate &o,M, which is the estimate of 20 based on all the** **measurements. Similarly, 5 1 , ~** is the estimate of x1 based on all the measurements.

Our derivation of these optimal smoothers will be based on a form for the Kalman filter different than we have seen in previous chapters. Therefore, before we can discuss the optimal smoothers, we will first present an alternate Kalman filter form in Section 9.1.


## 9.1 AN ALTERNATE FORM FOR T H E  KALMAN FILTER


.In order to put ourselves in position to derive optimal smoothers, we first need to de- rive yet another form for the. Kalman filter. This is the form presented in [And79]. The equations describing the system and the Kalman filter were derived in Sec- **tion 5.1 as follows:**

---


[Image on page 4]


**266**

*Now if we define L k  as*

---


[Image on page 5]


**267**

Combining Equations (9.4), (9.5), and (9.9) gives the alternate form for the one-step 
## a priori Kalman filter, which can be summarized as follows:


**Lk** 
# = F k P F H r ( H k P F H z  + &)-'
 
# pF+1 = FkpF(Fk - LkHk)T + Qk
 **2;+1** 
# = Fk?; -k L k ( Y k  - Hk?;)
 (9.10)


## where Lk is the redefined Kalman gain. This form of the filter obtains only a priori
 **state estimates and covariances. Note that the Kalman gain, L k ,  for this form of** **the filter is not the same as the Kalman gain, K k ,  for the form of the filter that we** derived in Section 5.1. However, the two forms result in identical state estimates and estimation-error covariances.

**9.2** 
## FIXED-POINT SMOOTHING


## The objective in fixed-point smoothing is to obtain a priori state estimates of x3
 
# at times j + 1, j + 2, e
 **.** 
# a ,  k, k + 1, .... We will use the notation ?j,k to refer to
 the estimate of x3 that is obtained by using all of the measurements up to and 
# including time (k - 1). That is, ? j , k  can be thought of as the a priori estimate of
 **x3 at time k:**

With this definition we see that

**2 j , k = E ( x j I Y l , . . . , Y k - l )** **k > j** (9.11)

(9.12)

**In other words, 2j,j is just the normal a priori state estimate at time j that we** **derived in Section 5.1. We also see that**

(9.13)


## In other words, 23,j+1 is just the normal a posteriori state estimate at time j that
 we derived in Section 5.1. The question addressed by fixed-point smoothing is as follows: When we get the next measurement at time (j + l), how can we incorporate that information to obtain an improved estimate (along with its covariance) for the state at time j? Furthermore, when we get additional measurements at times **( j  +2), ( j  +3), etc., how can we incorporate that information to obtain an improved** *estimate (along with its covariance) for the state at time j ?* **In order to derive the fixed-point smoother, we will define a new state variable 2'.** 
## This new state variable will be initialized as xi = zj, and will have the dynamics
 
# X L + ~  = xL ( k  = j ,  j + 1,. . .). With this definition, we see that x i  = x3 for all k > j .
 *So if we can use the standard Kalman filter to find the a priori estimate of xi then* **we will, by definition, have a smoothed estimate of x3 given measurements up to** 
# and including time (k - 1). In other words, the a priori estimate of xi will be equal
 **to ?i.,,k. This idea is depicted in Figure 9.4.** **Our original system is given as**

(9.14)

---


[Image on page 6]


**268**


## Figure 9.4
 **This illustrates the idea that is used to obtain the fked-point smoother. A** 
## fictitious state variable x' is initialized as x: = x3 and from that point on has an identity
 **state transition matrix. The a priari estimate of xk is then equal to 23,k.**

**Augmenting the dynamics of our newly defined state x' to the original system** results in the following:

(9.15)

**If we use a standard Kalman filter to obtain an a priori estimate of the augmented** **state, the covariance of the estimation error can be written as**

**The covariance P k  above is the normal a pri0q-i covariance of the estimate of X k .** We have dropped the minus superscript for ease of notation, and we will also feel free to drop the minus superscript on all other quantities in this section with the **understanding that all estimates and covariances are a priori. The c k  and I l k** 
# matrices are defined by the above equation. Note that at time k = j ,  & and I I k
 **are given as**


## C j  = E [ ( ~ j
 
# - * j , j ) ( X j  -
 
# = E [ ( X j  - q ( X ,  - q T ]


## nj
 
# = E [ ( x j  - 2 j , j ) ( x j  - f j , j I T ]
 
## = P j


**A -** *T* 
# = E [(x~ - 57)(xj - X~ ) ]
 
## = P j
 (9.17)

The Kalman filter summarized in Equation (9.10) can be written for the augmented **system as follows:**

**where L k  is the normal Kalman filter gain given in Equation (9.10), and X k  is the** additional part of the Kalman gain, which will be determined later in this section. Writing Equation (9.18) as two separate equations gives

**%+l** 
# = F k - 1 2 ;  + L k  (yk - H k 5 ; )


**2:** 
# 2,k+1 = 2 i k  + X k  ( Y k  - H k 2 ; )
 (9.19)

---

**269**

**The Kalman gain can be written from Equation (9.10) as follows:**

**P k  xT** [::I *= [Fi-l* *; I [ , ,  $][?Ix*

(9.20)

Writing this equation as two separate equations gives

*L k  = F k P k H T ( H k P k H r  + R k ) - '* *= & H z ( H k P k H r  + R k ) - '* (9.21)

The Kalman filter estimation-error covarianceupdate equation can be written from **Equation (9.10) as follows:**

*F k  0* *p k  xz* *[ x k + l* *"+'* *n k + l* "+' ] = [ 0 *I ]  [ C k* *rIk ]*

*Qk* 0

(9.22)

Writing this equation as three separate equations gives

*p k + l* *= F k p k ( F k  - L k H k l T  + Qk*

*n k + l* *= n k - c k H r x r* *G+l = - F k P k H T X %  -k F k c z*

*c k + l  -* *- x k ( F k  - L k H k ) T* (9.23)

It is not immediately apparent from the above expressions that Cftl is really the *transpose of c k + l ,  but the equality can be established by substituting for P k  and* **Lk*** Equations (9.19) - (9.23) completely define the fixed-point smoother. The fixed- 
## point smoother, which is used for obtaining ei.,,k = E ( z j I y l , . . . , p k - l )  for k L j ,
 can be summarized as follows.


## The fixed-point smoother


**1. Run the standard Kalman filter up until time j, at which point we have 2;** *and P37. In the algorithm below, we omit the minus superscript on Pi.,: for* *ease of notation.*

**2. Initialize the filter as follows:**

c . *3 = P j*


## rIj = P.
 *3*

*e 3 , j  = ej-* (9.24)

---

**270**


# 3. For k = j ,  j + 1, - a, perform the following:


**As we recall from Equation (9.16), Pk is the a priori covariance of the standard** **Kalman filter estimate, I I k  is the covariance of the smoothed estimate of xJ at time** **k ,  and Ck is the cross covariance between the two.**


## 9.2.1


Now we will look at the improvement in the estimate of xJ due to smoothing. The 
## estimate 2; is the standard a priori Kalman filter estimate of x3, and the estimate


**?J,k+l is the smoothed estimate after measurements up to and including time k** 
# have been processed. In other words, i$,k uses ( k  + 1 - j) more measurements to
 **obtain the estimate of xJ than 2; uses. How much more accurate can we expect** 
# our estimate to be with the use of these additional (k + 1 - j) measurements?
 The estimation accuracy can be measured by the covariance. The improvement in estimation accuracy due to smoothing is equal to the standard estimation covariance **PJ minus the smoothed estimation covariance n k + l .  We can use Equations (9.24)** **and (9.25) to write this improvement as**

**Estimation improvement due to smoothing**

**k** **(9.26)**

**%=j**

Now assume for purposes of additional analysis that the system is timeinvariant and the covariance of the standard filter has reached steady state at time j. Then we have 
## lim P i  = P
 **(9.27)** **k - r w** **From Equation (9.25) we see that**


## where C is initialized as Cj = P .  Combining this expression for &+I
 with its initial value, we see that

**(9.29)**

---


[Image on page 9]


**271**

where $’ is defined by the above equation. Now substitute this expression, and the **expression for X from Equation (9.25), into Equation (9.26) to obtain**

The quantity on the right side of this equation is positive definite, which shows that the smoothed estimate of z j  is always better than the standard Kalman fil- 
## ter estimate. In other words, (Pj - & + I )
 
## > 0, which implies that &+I
 
## < Pj.
 Furthermore, the quantity on the right side is a sum of positive definite matrices, **which shows that the larger the value of k (i.e., the more measurements that we use** to obtain our smoothed estimate), the greater the improvement in the estimation 
# accuracy. Also note from the above that the quantity (HPHT + R) inside the
 **summation is inverted. This shows that as R increases, the quantity on the right** **side decreases. In the limit we see from Equation (9.30) that**


# lim (Pj -
 = 0 **R+w** **(9.31)**

This illustrates the general principle that the larger the measurement noise, the smaller the improvement in estimation accuracy that we can obtain by smoothing. This is intuitive because large measurement noise means that additional measure- ments will not provide much improvement to our estimation accuracy.

**EXAMPLE9.1**

In this example, we will see the improvement due to smoothing that can be obtained for a vehicle navigation problem. This is a second-order Newtonian system where ~ ( 1 ) **is position and 4 2 )  is velocity. The input is comprised of** **a commanded acceleration u plus acceleration noise 6. The measurement y is** **a noisy measurement of position. After discretizing with a step size of T ,  the** system equations can be written as

**1 T** **T2/2** = [ 0 **T**

**Note that the process noise W k  is given as**

**(9.33)**

**Now suppose the acceleration noise 6 k  has a standard deviation of a. We** **obtain the process noise covariance as follows:**

---


[Image on page 10]


**272**

The percent improvement due to smoothing can be defined as

100 Tr(Pj - I I k + l ) Percent Improvement = TdPj)

(9.34)

(9.35)

**where j is the point which is being smoothed, and k is the number of mea-** surements that are processed by the smoother. We can run the fixed-point smoother given by Equation (9.25) in order to smooth the position and veloc- ity estimate at any desired time. Suppose we use the smoother equations to 
## smooth the estimate at the second time step (k = 1). If we use measurements
 **at times up to and including 10 seconds to estimate 21, then our estimate is** **denoted as 41,101.** In this case, Table 9.1 shows the percent improvement due 
## to smoothing after 10 seconds when the time step T = 0.1 and the acceler-
 
## ation noise standard deviation a = 0.2. As expected from the results of the
 previous subsection, we see that the improvement due to smoothing is more dramatic for small measurement noise.

**Table 9.1** seconds for Example 9.1. The improvement due to smoothing is more noticeable when the measurement noise is small.

Improvement due to smoothing the state at the first time step after 10

Measurement noise Percent standard deviation Improvement

0.1 99.7 1 96.6 10 59.3 100 13.7 1000 **0.2**

Figure 9.5 shows the trace of IIk, which is the covariance of the estimation error of the state at the first time step. As time progresses, our estimate of the state at the first time step improves. After 10 seconds of additional measurements, the estimate of the state at the first time step has improved by 96.6% relative to the standard Kalman filter estimate. Figure 9.6 shows the smoothed estimation error of the position and velocity of the first time step. We see that processing more measurements decreases the estimation-error covariance. In general, the smoothed estimation errors shown in Figure 9.6 will con- verge to nonzero values. The estimation errors are zero-mean, but not for

---


[Image on page 11]


**273**

**Figure 9.5** This shows the trace of the estimation-error covariance of the smoothed estimate of the state at the first time step for Example 9.1. As time progresses and we process more measurements, the covariance decreases, eventually reaching steady state.

**Figure 9.6** This shows typical estimation errors of the smoothed estimate of the state at the first time step for Example 9.1. As time progresses and we process more measurements, the estimation error decreases, and its standard deviation eventually reaches steady state.

any particular simulation. The estimation errors are zero-mean when aver- aged over many simulations. The system discussed here was simulated 1000 
# times and the variance of the estimation errors (q - 21,101)
 were computed numerically to be equal to 0.054 and 0.012 for the two states. The diagonal **elements of lT101 were equal to 0.057 and 0.012.** vvv

---


[Image on page 12]


**274**

**9.2.2** **Smoothing constant states**

Now we will think about the improvement (due to smoothing) in the estimation 
## accuracy of constant states. If the system states are constant then Fk = I and
 
## Q = 0. Equation (9.25) shows that


Comparing these expressions for **and & + I ,** **and realizing from Equation (9.24)** 
# that the initial value of C, = P,, we see that & = Pk for k 2 j .  This means that
 **the expression for Lk from Equation (9.25) can be written as**

**Lk** 
# = FkPkHT(HkpkHT + Rk)-'
 
# = ckHT(HkpkH? + &)-'
 
## = x k
 **(9.37)**

**Substituting these results into the expression for l&+1** **from Equation (9.25) we see** that

**(9.38)**


## Realizing that the initial value of II, = Pj, and comparing this expression for &+I
 
# with Equation (9.36) for Pk+l, we see that & = Pk for k 2 j. Recall that Pk is
 **the covariance of the estimate of x k  from the standard Kalman flter, and & is** **the covariance of the estimate of x, given measurements up to and including time**

This result shows that constant states are not smoothable. Additional measure- ments are still helpful for refining an estimate of a constant state. However, there is no point to using smoothing for estimation of a constant state. If we want to 
## estimate a constant state at time j using measurements up to time k > j, then we
 **may as well simply run the standard Kalman filter up to time k. Implementing the** smoothing equations will not gain any improvement in estimation accuracy.


# (k - 1).


**9.3** 
## FIXED-LAG SMOOTHING


# In fixed-lag smoothing we want to obtain an estimate of the state at time (k - N )
 **given measurements up to and including time k, where the time index k continually** **changes as we obtain new measurements, but the lag N is a constant. In other** *words, at each time point we have N future measurements available for our state* 
# estimate. We therefore want to obtain Sk-N,k for k = N ,  N + 1,. . ., where N is a
 **fixed positive integer. This could be the case, for example, if a satellite is continually** **taking photographs that are to be displayed or transmitted N time steps after the** **photograph is taken. In this case, since the photograph is processed N time steps** **after it is taken, we have N additional measurements after each photograph that**

---

**275**

are available to update the estimate of the satellite state and hence improve the quality of the photograph. In this section we use the notation

**2 k - N , k** 
## = E ( x k - N I Y 1 ,  * * ’ , Y k )


**n k - N** 
# = E [ ( x k - N  - ?k-N,k)(Xk-N - %k-N,k) T ]
 **(9.39)**

Note that the notation has changed slightly from the previous section. In the **previous section we used the notation &,m to refer to the estimate of Xk given** 
# measurements up to and including time (m - 1). In this section (and in the remain-
 **der of this chapter) we use 2 k , m  to refer to the estimate of Xk given measurements** *up to and including time m.* **Let us define X k , m  as the state X k - n  propagated with an identity transition** **matrix and zero process noise to time k. With this definition we see that**

**xk+1,1** = **x k**

**xk+1,2** - **Xk-1** -

**x k , l** - -

**xk+1,3** = **Xk-2**

**x k , 2** - -

etc.

We can therefore define the augmented system

...

(9.40)

The Kalman filter estimates of the components of this augmented state vector are **given as**


## E ( Z k + l I Y l  ’ ’ * Y k )  = *L+l
 
## = *k+l,k


## E ( Z k + l , l l Y l  + * ’ Y k )  = E ( x k l Y 1
 *** * Y k )** - 
# - 2$


## = *k,k


## E(xk+1,21Y1 * * ‘ Y k )  = E ( x k - l l y l  * * ‘ Y k )
 
## = *k-l,k


## E ( X k + l , N + l I Y l  ‘ * * Y k )  = ?k-N,k
 **(9.42)**

We see that if we can use a Kalman filter to estimate the states of the augmented **system (using measurements up to and including time k), then the estimate of the**

---

**276**

**last element of the augmented state vector, Zk+l,N+1, will be equal to the estimate** **of Xk-N given measurements up to and including time k. This is the estimate that** **we are looking for in fixed-lag smoothing. This idea is illustrated in Figure 9.7.**

**'k**


## ' k + m , m  = ' k - L
 ' **_-___-__-_-_I_** - **'0** **1** **' k - m** **' k - m + l**


## Figure 9.7
 **This illustrates the idea that is used to obtain the fixed-lag smoother. A** 
## fictitious state variable Xk,m is initialized a s  Xk,m = Xk-m and from that point on has
 **an identity state transition matrix. The a posteriori estimate of Xk+m,m is then equal to**

**z k - n , k .**

From Equation (9.10) we can write the Kalman filter for the augmented system 
## of Equation (9.41) as follows:


5; [ Fi 1 = [ a [ ***k-:,k-l 1 t**

***k-N,k** 
## ... I
 0 **?k-(N+l),k-1**

**where the Lk,z matrices are components of the smoother gain that will be deter-** **mined in this section. Note that Lk.0 is the standard Kalman gain. The smoother** **gain L k  is defined as**

**From Equation (9.10) we see that the L k  gain matrix is given by**

(9.44) #"I. 
## \ - l  0


**where the Pl'J covariance matrices are defined as**


# pi'' = E [ ( Z k - j  - ? k - J , k - l ) ( z k - z  - 2k-z,k-l)']


(9.45)

(9.46)

---

**277**

*The Lk expression above can be simplified to*

From Equation (9.10) we see that the covariance-update equation for the Kalman filter for our augmented system can be written as

*Substituting for Lk from Equation (9.47) and multiplying out gives*

(9.49)

*This gives us the update equations for the P matrices. The equations for the first* *column of the P matrix are as follows:*

*pjf1 = Fkp;” [FZ - Hr(HkPk’* *0 0  Hk T + Rk)-lHkP;’oFr] + Q k*

=

*= Pi’O(Fk - Lk,oHk)T* *FkPi7O(Fk - Lk,oHk)T + Qk*

(9.50)

---


[Image on page 16]


**278**

*The equations for the diagonal elements of the P matrix are as follows:*

*pi,%* *k+l* *= ' k  a-1,%-1 - ' k  O,%-~HTLT* *k* *k,a FT* *k* (9.51)

These equations give us the formulas that we can use for fixed-lag smoothing. This 
## gives us the estimate E(Zk-NIY1, - - , y k )  for a fixed N as k continually increments.
 **The fixed-lag smoother is summarized as follows.**


## The fixed-lag smoother


*1. Run the standard Kalman filter of Equation (9.10) to obtain 5;+l, L k ,  and* *PL .*

**2. Initialize the fixed-lag smoother as follows:**

(9.52)


## 3. For i = 1,
 + **a** **,** 
# N + 1, perform the following:


Note that the first time through this loop is the measurement update of the standard Kalman filter. At the end of this loop we have the smoothed **estimates of each state with delays between 0 and N ,  given measurements up** **to and including time k. These estimates are denoted &,k,** **. . a ,** *& l N , k .  we*


# also have the estimation-error covariances, denoted Pi$l, .
 **a ,  Pk+l** *N+1,N+1*

**The percent improvement due to smoothing can be computed as**

(9.54)

---


[Image on page 17]


**279**

**EXAMPLE9.2**

Consider the same two state system as described in Example 9.1. Suppose we are trying to estimate the state of the system with a fixed time lag. The *discretization time step T = 0.1 and the standard deviation of the acceleration* noise is 10. Figure 9.8 shows the percent improvement in state estimation that is available with fixed-lag smoothing. The figure shows percent improvement **as a function of lag size, and for two different values of measurement noise. The** values on the plot are based on the theoretical estimation-error covariance. **As expected, the improvement in estimation accuracy is more dramatic as the** measurement noise decreases. This was discussed at the end of Section 9.2. 
# QO


8o t

2ot 10; . I **5** 10 **15** **20** **25** **30** **Number of lag intervals**

**Figure 9.8** This shows the percent improvement of the trace of the estimation-error covariance of the smoothed estimate of the state (relative to the standard Kalman filter) for **Example 9.2. As the number of lag intervals increases, the estimation error of the smoother** **decreases and the percent improvement increases. Also, as the measurement noise decreases,** the improvement due to smoothing is more dramatic.

vvv

**9.4** 
## FIXED-INTERVAL SMOOTHING


Suppose we have measurements for a fixed time interval. In fixed-interval smooth- **ing we seek an estimate of the state at some of the interior points of the time** interval. During the smoothing process we do not obtain any new measurements. Section 9.4.1 discusses the forward-backward approach to smoothing, which is per- haps the most straightforward smoothing algorithm. Section 9.4.2 discusses the RTS smoother, which is conceptually more difficult but is computationally cheaper than forward-backward smoothing.

---

**280**


## 9.4.1 Forward-backward smoothing


## Suppose we want to estimate the state xm based on measurements from k = 1 to
 
## k = N ,  where N > m. The forward-backward approach to smoothing obtains two
 *estimates of xm. The first estimate, P f ,  is based on the standard Kalman filter that* 
## operates from k = 1 to k = m. The second estimate, hb, is based on a Kalman filter
 
## that runs backward in time from k = N back to k = m. The forward-backward
 approach to smoothing combines the two estimates to form an optimal smoothed estimate. This approach was first suggested in [Fra69]. *Suppose that we combine a forward estimate P f  of the state and a backward* *estimate i?b of the state to get a smoothed estimate of x as follows:*

*where K f  and Kb are constant matrix coefficients to be determined. Note that*

*? f  and P b  are both unbiased since they are both outputs from Kalman filters.* *Therefore, if h is to be unbiased, we require K f  + Kb = I (see Problem 9.9). This* gives 
# P = K f h f  + ( I  - K f ) &
 (9.56)

**The covariance of the estimate can then be found as**

(9.57)


$$
where ef = x - x f ,  eb = x - q,, and we have used the fact that E(efer) = 0. The
$$
 *estimates P f  and i?b are both unbiased, and ef and eb are independent (since they* *depend on separate sets of measurements). We can minimize the trace of P with* **respect to K f  using results from Equation (1.66) and Problem 1.4:**

*- -  - 2E {Kf(efeF + ebe;f) - ebe;f}* *aKf* (9.58)

*where Pf = E(efeT) is the covariance of the forward estimate, and Pb = E(eb.5:)* is the covariance of the backward estimate. Setting this equal to zero to find the *optimal value of K f  gives*

(9.59)

*The inverse of (Pf + Pb) always exists since both covariance matrices are positive* definite. We can substitute this result into Equation (9.57) to find the covariance **of the fixed-interval smoother as follows:**

(9.60)

---


[Image on page 19]


**281**


# Using the identity ( A  + B)-l = B-'(AB-'+ I)-l (see Problem 9.2), we can write
 **the above equation as**

*P = ( P f P i l  + I)-'(Pf + Pb)(P;'Pf +I)-' f* *Pb - (PfP;' + I)-lPb - (PfPc' f I)-'Pb* *(9.61)*


## Multiplyingout the first term, and again using the identity (A+B)-l = B-'(AB-l t
 *I)-l on the last two terms, results in*

*(Pr'+PT')-'+(pb -1p f p-1* *b* *+ p-1* 
# b ) -1 ] ( P i l P f  +I)-' +


*(9.62)*

*(9.63)*

*(9.64)*

These results form the basis for the fixed-interval smoothing problem. The system **model is given as**

*xk* *= Fk-ixk-i + Wk-1*

*W k* *(0,Qk)* *uk* *(0,Rk)* *(9.65)*

*Suppose we want a smoothed estimate at time index m. First we run the forward* *Kalman filter normally, using measurements up to and including time m.*

*Yk = Hkxk+vk*

**1. Initialize the forward filter as follows:**


## 2. For k = 1, - , m, perform the following:


*(9.66)*

*(9.67)*

---


[Image on page 20]


**282**

At this point we have a forward estimate for xm, along with its covariance. These *quantities are obtained using measurements up to and including time m.* The backward filter needs to run backward in time, starting at the final time **index N .  Since the forward and backward estimates must be independent, none** of the information that was used in the forward filter is allowed to be used in the *backward filter. Therefore, PrN must be infinite:*


## PCN = 0O
 (9.68)

*We are using the minus superscript on PiN to indicate the backward covariance at* **time N before the measurement at time N is processed. (Recall that the filtering** **is performed backward in time.) So PbN will be updated to obtain Pb+N after the** **measurement at time N is processed. Then it will be extrapolated backward in** **time to obtain PGN-l, and so on.** **Now the question arises how to initialize the backward state estimate ?& at the** 
## final time k = N .  We can solve this problem by introducing the new variable


## s k  = Pil?bk
 (9.69)

A minus or plus superscript can be added on all the quantities in the above equation **to indicate values before or after the measurement at time k is taken into account.** 
## Since PcN = 00 it follows that
 s; = 0 (9.70)

**The infinite boundary condition on P i  means that we cannot run the standard** Kalman filter backward in time because we have to begin with an infinite covariance. **Instead we run the information filter from Section 6.2 backward in time. This can** be done by writing the system of Equation (9.65) as

**z k - 1** 
# = FFJlzk + FiIiWk-1
 
# = FF21Xk + Wb,k-1


(9.71)

**Note that FL1 should always exist if it comes from a real system, because Fk comes** **from a matrix exponential that is always invertible (see Sections 1.2 and 1.4). The** **backward information filter can be written as follows.**

*1. Initialize the filter with zrN = 0.*


## 2. For k = N ,  N - 1, -
 
## a ,  perform the following:


(9.72)

---


[Image on page 21]


**283**


## The first form for Z;k-l above requires the inversion of Zbfk. Consider the first
 
## time step for the backward filter (i.e., at k = N). The information matrix Z;
 is initialized to zero, and then the first time through the above loop we set Z$ = 
# Zk + HFRL'Hk. If there are fewer measurements than states, H F R i l H k  will
 
## always be singular and, therefore, Zbfk will be singular at k = N .  Therefore, the
 **first form given above for Zck-l will not be computable. In practice we can get** *around this by initializing ZbN to a small nonzero matrix instead of zero.* **The third form for ZCk-1 above has its own problems. It does not require the** 
## inversion of Z&, but it does require the inversion of Qk-1.
 So the third form of **Zb;k-l is not computable unless Q k - 1  is nonsingular. Again, in practice we can** **get around this by making a small modification to Q k - 1  so that it is numerically** nonsingular. 
## Since we need to update Sk = Zbk?bk instead of ?bk (because of initialization
 **issues) as defined in Equation (9.69), we rewrite the update equations for the state** **estimate as follows:**


# ?& = ?Lk + K b k ( Y k  - Hk?&)
 *skf = Z+f+* **bk bk** 
# = Zb+k2& + Z&Kbk (Yk - Hkgrk)
 **(9.73)**


# Now note from Equation (6.33) that we can write Zbfk = Zk + HTRklHk, and


## K b k  = P&HrR;? Substituting these expressions into the above equation for skf
 gives

**We combine this with Equation (9.72) to write the backward information filter as** follows.

1. Initialize the filter as follows:

**(9.75)**


# 2. For k = N, N - 1, * . , m + 1, perform the following:


**3. Perform one final time update to obtain the backward estimate of xm:**

---

**284**

(9.77)

**Now we have the backward estimate f;, and its covariance PLm. These** 
# quantities are obtained from measurements m + 1, m + 2,
 
## a ,  N .


**After we obtain the backward quantities as outlined above, we combine them with** the forward quantities from Equation (9.67) to obtain the final state estimate and covariance:


## Kf = P&pTm+P&)-l
 
# f m  = K f q m  + (I - Kf)f,,


(9.78)

*We can obtain an alternative equation for P, by manipulating the above equations.* 
## If we substitute for Kf in the above expression for Pm then we obtain


# - p- p+ + p -  )-1-+
 - bm( f m *bm* *"fm + [('r', + pb-k> - p&] (pTm + p;m)-'f;m* - 
# - p-
 **bm( p+** **f m  +p-** *bm )-l-+* "fm+pf+m(pf+m+p&)-lfbm (9.79)

Using the matrix inversion lemma on the rightmost inverse in the above equation and performing some other manipulations gives


# where we have relied on the identity (A + B)-l = B-l(AB-l + I)-1 (see Prob-
 
## lem 9.2). The coefficients of f:m and 2;'
 in the above equation both have a common factor which can be written as follows:

---

285


# = P;m - P;mT;m (I + P;mT;m) - 1 PTm
 
# P;m - Pfm(Tf+mP;m
 
# + I)-l
 =


# = [P;m(T;mP& +I) - Pf,] (ZTmP& + I)-l


# = P,-,(zf+mP& + I)-1
 = +

**Therefore, using Equation (9.78), we can write Equation (9.80) as**


## hm = PmZj!mi?i.fm
 *+ ~ m ~ r ~ h r ~*


# = pm (.,.ni?~~
 + ~r~i?;~)

Figure 9.9 illustrates how the forward-backward smoother works.

**k 3** **k=m** **k=N**

(9.81)

(9.82)

**Figure 9.9** This figure illustrates the concept of the forward-backward smoother. The *forward filter is run to obtain a posteriori estimates and covariances up to time m. Then* *the backward filter is run to obtain a priori estimates and covariances back to time m (i.e.,* *a priori from a reversed time perspective). Then the forward and backward estimates and* 
## covariances at time m are combined to obtain the find estimate 2m and covariance Pm.


**EXAMPLE9.3**

In this, example we consider the same problem given in Example 9.1. Suppose 
## that we want to estimate the position and velocity of the vehicle at t = 5
 seconds. We have measurements every 0.1 seconds for a total of 10 seconds. The standard deviation of the measurement noise is 10, and the standard deviation of the acceleration noise is 10. Figure 9.10 shows the trace of the 
## covariance of the estimation of the forward filter as it runs from t = 0 to t = 5,
 
## the backward filter as it runs from t = 10 back to t = 5, and the smoothed
 
## estimate at t = 5. The forward and backward filters both converge to the
 same steady-state value, even though the forward filter was initialized to a covariance of 20 for both the position and velocity estimation errors, and the backward filter was initialized to an infinite covariance. The smoothed filter **has a covariance of about 7.6, which shows the dramatic improvement that** can be obtained in estimation accuracy when smoothing is used. vvv

---


[Image on page 24]


**286**

**70** 
# ! 60-
 
## .- 2


**I**

**I**

**1** **I**

- **I**

**I** **I**

**Figure 9.10** **This shows the trace of the estimation-error covariance for Example 9.3.** 
## The forward filter runs from t = 0 to t = 5, the backward filter runs from t = 10 to t = 5,
 
## and the trace of the covariance of the smoothed estimate is shown at t = 5.


.4- **8 20-**

**10**

**I-**

**0-**

**9.4.2** **RTS smoothing**

Several other forms of the fixed-interval smoother have been obtained. One of the most common is the smoother that was presented by Rauch, Tung, and Striebel, usually called the RTS smoother [Rau65]. The RTS smoother is more computai tionally efficient than the smoother presented in the previous section because we do not need to directly compute the backward estimate or covariance in order to get the smoothed estimate and covariance. In order to obtain the RTS smoother, **we will first look at the smoothed covariance given in Equation (9.78) and obtain** *an equivalent expression that does not use Pbm. Then we will look at the smoothed* **estimate given in Equation (9.78), which uses the gain K f ,  which depends on Pbm,** 
## and obtain an equivalent expression that does not use Pbm or &,m.


**forward--backward filter** *J* **0** -

*9.4.2.1 RTS covariance update First consider the smoothed covariance given in* **Equation (9.78). This can be written as**

*= PTm - P;m(P;m + PFm)-1PTm* **(9.83)**

where the second expression comes from an application of the matrix inversion **lemma to the first expression (see Problem 9.3). From Equation (9.72) we see that**

**(9.84)**

*Substituting this into the expression (PTm + PL)-l gives the following:*

---


[Image on page 25]


**287**

We can combine these two equations to obtain

Substituting this into Equation (9.78) gives

(9.85)

(9.86)

(9.87)

(9.8%)

Substituting this into Equation (9.85) gives

*= F T z -* *m f,m+l (pim+l- ',+I)* *zim+lFm* (9.89)

where the last equality comes from an application of the matrix inversion lemma. Substituting this expression into Equation (9.83) gives

*Pm = pFm - Km(Pim+1 - Pm+l)K;* (9.90)

**where the smoother gain Km is given as**

*Km = ~ f + ~ ~ z ~ f ; ~ + l* (9.91)

**The covariance update equation for Pm is not a function of the backward covariance.** *The smoother covariance Pm can be solved by using only the forward covariance* *Pfm, which reduces the computational effort (compared to the algorithm presented* in Section 9.4.1).

---


[Image on page 26]


**288**


## 9.4.2.2 RTS state estimate update Next we consider the smoothed estimate 2,
 given in Equation (9.78). We will find an equivalent expression that does not use *Pam or ?bm. In order to do this we Will fist need to establish a few lemmas.*

**Lemma 1**

*Proof: From Equation (9.67) we see that*

*FF?lQk-lFF-;* *= F - I P - F - T* *k-1* *f k  k-1 - P f , k - l* + (9.92)

*p h  = Fk-lPLk-lFkT-1+* *Qk-1* (9.93)


# Qk - 1 = ph - F k  - 1 p z k  - 1 Fz- 1


*Rearranging this equation gives*

(9.94)

*Premultiplying both sides by FFI1 and postmultiplying both sides by FF-;* *gives the* *desired result.* *QED*

**Lemma 2 The a posteriori covariance P& of the backward filter satisfies the equa-** *tion* *p& = ( P h  f p & ) T ; k p k* (9.95)

*Proof: From Equation (9.78) we obtain*


# I = (I&
 *+ z ; k ) p k* 
# p& = (I + p & z y , ) p k


*= p k  + p & z y k p k* *= P G z Y k p k  + p* *b* *+* *l* *c* *z* *f* *l* *e* *P* *k* *= (p& + p&)zy,pk* (9.96)

*QED*

**Lemma 3 The covariances of the forward and backward filters satisfy the equation**

*p& + p& = F k - l ( P & - i +* *p c k - 1 ) F k - l* *T* (9.97)

*Proof: From Equation (9.67) and (9.72) we see that*

*Adding these two equations and rearranging gives*

(9.98)

(9.99)

(9.100)

---


[Image on page 27]


**289**

*Proof: Fkom Equations (9.69) and (9.82) we have*

*2 k  = P k z T k 2 i k  + P k z h 2 i k* *= Pkz;’k?;k* *+ P k S i*

*&om Equation (9.76) we see that*

(9.101)

*Substitute this expression for s i  and the expression for 2 i k  from Equation (9.67),* *into Equation (9.101) to obtain*

*?k = P k z T k 2 y k  + P k z T k K f k ( Y k  - Hk?yk) f Pkskf - P k H F R k ’ Y k* (9.103)

*Now substitute Pf+kHrRb’ for K f k  [from Equation (9.67’1 in the above equation* *to obtain*


## Lemma 5


*Proof: Recall from Equations (6.26) and (9.72) that*

*Combining these two equations gives*

(9.105)

(9.106)

(9.107)

*where we have used Equation (9.78) in the above derivation. Substitute this expres-* *sion for Pbfk into Equation (9.97) to obtain*

(9.108)

---


[Image on page 28]


**290**

*Invert both sides to obtain*

*Now apply the matrix inversion lemma to the term (Zk -Z;,)-'* *in the above equa-* *tion. This results in*

(9.110)

With the above lemmas we now have the tools that we need to obtain an alternate *expression for the smoothed estimate. Starting with the expression for sk-'* in 
## Equation (9.76), and substituting the expression for Tck-1 from Equation (9.72)
 gives

(9.111)

Rearranging this equation gives

(9.112)

*Multiplying out this equation, and premultiplying both sides by F;21Pa+k, gives*

(9.113)

---


[Image on page 29]


291

**Substituting for F;ylQk- IFF-: from Equation (9.92) gives**

(9.1 14)

*Substituting in this expression for Pb+k from Equation (9.95) gives*

(9.115)

*Substituting for (PG + PA) from Equation (9.97) on both sides of this expression* gives

(9.116) 
# Premultiplying both sides by (Pftk-l + p<k-l)-lFF?l
 gives

(9.117)


# Substituting Equation (9.105) for (Pftk-l + P<k-l)-l
 gives

(9.118)

Now from Equation (9.105) we see that

(9.119)

So we can add the two sides of this equation to the two sides of Equation (9.118) to get

(9.120)

**Now use Equation (9.100) to substitute for PkS$ in the above equation and obtain**

(9.121)

Rearrange this equation to obtain

(9.122)

---

**292**


## From Equation (9.106) we see that ZTk -TFk = HzRk'Hk. Also note that part of
 **the coefficient of 27k on the left side of the above equation can be expressed as**

(9.123)


## From Equation (9.67) we see that FF?12& = 2 i k - 1 ,  Therefore Equation (9.122)
 can be written as

(9.124)

**Now substitute for pk from Equation (9.90) and use Equation (9.91) in the above** equation to obtain

(9.125)

**Premultiplyhg both sides by Plk-1 gives**

(9.126)

Now use Equation (9.91) to notice that the coefficient of  SF-^ on the left side of the above equation can be written as

(9.127)

**Using Equation (9.90) to substitute for &pk+lKz allows us to write the above** expression as

(9.128)

**Since this is the coefficient of s ; - ~  in Equation (9.126), we can write that equation**

(9.129)

**as**

Now from Equations (9.78) and (9.82) we see that

(9.130)

From this we see that

(9.131)

---

**293**


# Rewriting the above equation with the time subscripts (k - 1) and then substituting
 **for the left side of Equation (9.129) gives**

*2 k - 1  - x f , k - 1* -+ *= K k - l ( 2 k  - 2 7 k )* **(9.132)**

from which we can write

*2 k  = 2 F k  + K k ( i k + l  - ? i k + l )* **(9.133)**

*This gives the smoothed estimate 2 k  without needing to explicitly calculate the* backward estimate. The RTS smoother is implemented by first running the stan- **dard Kalman filter of Equation (9.67) forward in time to the final time, and then** **implementing Equations (9.90), (9.91), and (9.133) backward in time. The RTS** smoother can be summarized as follows.

**The RTS smoother**

**1. The system model is given as follows:**

**2. Initialize the forward filter as follows:**


## 3. For k = l,...,
 *N (where N is the final time), execute the standard forward* Kalman filter:

**4. Initialize the RTS smoother as follows:**

**(9.136)**

**(9.137)**

---


[Image on page 32]


**294**


# 5. For k = N - 1, - . -, 1,0, execute the following RTS smoother equations:


## 9.5
 
## SUMMARY


In this chapter we derived the optimal smoothing filters. These filters, sometimes called retrodiction filters [BarOl] , include the following variants.


## 2 J , k  = E ( s j l y l , * . . , y k - l )  ( k  L j )  is the output of the fixed-point smoother.
 *In this filter we find the estimate of the state at the fixed time j when mea-* *surements continue to arrive at the filter at times greater than j .  The time* 
## index j is fixed while k continues to increase as we obtain more measurements.


## ?k-N,k = E ( ~ k - N I Y l , " * , Y k )  for a fixed N is the Output of the fixed-lag
 **smoother. In this filter we find the estimate of the state at each time k while** 
# using measurements up to and including time (k + N ) .  The time index k
 **varies while N remains fixed.**


## 0 i k , N  = E ( z k l y 1 ,  * .  ., y
 **~** **)** **for a fixed N is the output of the fixed-interval** **smoother. In this filter we find the estimate of the state at each time k while** **using measurements up to and including time N .  The time index k varies** **while the total number of measurements N is fixed. The two formulas we** derived for this type of smoothing included the forward-backward smoother and the RTS smoother.

Just as steady-state filters can be used for standard filtering, we can also derive steady-state smoothers to save computational effort [Ge174]. An early survey of smoothing algorithms is given in [Med73].

**PROBLEMS**

**Written exercises**

9.1 Prove or disprove the following conjecture: The trace of the inverse of a matrix is equal to the inverse of the trace of the matrix.

**9.2** 
# Show that ( A  + B ) - l =  B-l(AB-l+ I ) - 1 .


**9.3 Derive Equation (9.83).**

**9.4** 
## Consider a scalar system with F = 1, H = 1, and R = 2Q.
 *a) What is the steady-state value of the a priori estimation-error covariance* **PF?**

---


[Image on page 33]


**295**

b) Suppose that after the Kalman filter has reached steady state, the fixed- point smoother begins to operate. Find a closed-form solution to the **covariance of the smoothed estimate l& as a function of the time index k.** What is the limiting value of


## 9.5 Repeat Problem 9.4 for the case R = l2Q. What is the percent improvement
 in the estimation-error covariance due to smoothing? Explain why the percent improvement due to smoothing for this case differs in the way that it does from the **results of Problem 9.4.**

**9.6** Suppose that the fixed-lag smoother for this system is in steady state so that P;+l = P;,


## L k + l , %  = L k , z ,  Pi$1 = Pila, and Pt$l = Pk’ , for i = l , . . . ,
 **N + 1 .  Find closed-form** *expressions for P;,* **L k , z ,  P;”, and Pi” as functions of i. What is the limit as**


# i --+ m of L k , z ,  pis2, and pi!’?


**9.7 Suppose you have a fixed-lag smoother as shown in Equation (9.43) that** is in steady state. How do the eigenvalues of the fixed-lag smoother relate to the eigenvalues of the standard Kalman filter? What do you conclude about the stability of the fixed-lag smoother?


# 9.8 Solve Equation (9.10) for ( y k  - HIE!?;) [assuming that p ( L k )  = T ,  where T
 is the number of measurements in the system]. Substitute the resulting expression 
# for (Yk - H k ! ? i )  in the fixed-lag smoother equation for !?k+l-$,k to show that the
 smoothed state estimate can be driven by the state estimates without any input from the measurements [And79].

**9.9 Suppose that bj and & ,** 
# are unbiased estimates of x, and !? = Kjbj + K&.
 
# Show that if b is an unbiased estimate of x, then we must have Kj + Kb = I.


9.10 
## Consider a scalar system with F = 1, H = 1, and R = 2Q. Use the forward-
 **backward smoother of Section 9.4.1 to find the steady-state value of the covariance** of the smoothed state estimate.


## 9.11 Consider a scalar system with F = 1, H = 1, and R = 2Q. Use the RTS
 **smoother of Section 9.4.2 to find the steady-state value of the covariance of the** smoothed state estimate.


## 9.12 Consider a scalar system with F = 1, H = 1, and R = 2Q. Suppose that
 **the forward filter has reached steady state. Use the RTS smoother of Section 9.4.2** 
# to find the covariance of the smoothed state estimate for k = N ,  N - 1, N - 2, N - 3,
 
# and N - 4. At what point does the covariance of the smoothed state estimate get
 **within 1% of its steady-state value?**


## 9.13 Repeat Problem 9.12 for R = 12Q. How do you intuitively explain the
 **quicker convergence of Pk to steady state?**

**9.14 Use the RTS smoother equations to show that constant states are not** 
## smoothable. That is, if F = I and Q = 0, then P k  = PIN for all k.


## as k ---f m?


## Consider a scalar system with F = 1, H = 1, and R = 2Q.


0 2

---


[Image on page 34]


**296**

**Computer exercises**

**9.15 Consider the second-order system**

*where w = 6 rad/s is the natural frequency of the system, and c = 0.16 is the* damping ratio. The input w(t) is continuous-time white noise with a variance of 0.01. Measurements of the first state are taken every 0.5 s:


# Y ( t k )  = [ 1 0 ] z ( t k )  + u(tk)


*where ' ~ ( t k )* is discrete-time white noise with a variance of estimate, and covariance are The initial state,

*f(0) = x(0)*

a) Discretize the system equation. b) Implement the discretetime Kalman filter and the RTS smoother for 10 s (20 time steps). Plot the variance of the estimation error of the first state for the forward filter and for the RTS smoother on a single plot. Do the same for the second state. Why is the second state more smoothable than **the first state?**

**9.16 Repeat Problem 9.15 with the continuous-time process noise w(t) having a** variance of 1. How does this change the smoothability of the states?

**9.17 Design a fixed-interval smoother for the system described in Problem 5.11** to estimate the state at each time on the basis of measurements at all 10 time steps. *a) Plot the a posteriori covariance of the forward state estimate and the* **covariance of the smoothed state estimate as a function of time for both** states. **b) What are the percent improvements in the estimation-error variances due** to smoothing for the two states at the initial time? Why is there so much more improvement for one state than for the other state?


## c )  Simulate the system and smoother a hundred times or so, each simulation
 with a different noise history. On the basis of your simulations, derive a numerical estimate of the smoother estimation-error variances of the two states at the initial time. How do your numerical variances compare with the theoretical variances obtained in part (b)?