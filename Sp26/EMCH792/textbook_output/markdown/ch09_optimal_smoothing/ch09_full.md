---
type: chapter
chapter: 9
title: Optimal smoothing
---
# Chapter 9 Optimal Smoothing

In a *post mortem* (after the fact) analysis, it is possible to wait for more observations to accumulate. In that case, the estimate can be improved by smoothing. 

-Andrew Jazwinski **jJaz70, p. 1431** 
In previous chapters, we discussed how to obtain the optimal a *priori* and a posteriori state estimates. The a *priori* state estimate at time k, *2;,* is the state estimate at time k based on all the measurements up to (but not including) time k. The a *posteriori* state estimate at time k, *2:,* is the state estimate at time k based on all the measurements up to and including time k: 

$$\begin{array}{l l l}{{\hat{x}_{k}^{-}}}&{{=}}&{{E(x_{k}|y_{1},\cdots,y_{k-1})}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{E(x_{k}|y_{1},\cdots,y_{k})}}\end{array}$$
$$(9.1)$$

There are often situations in which we want to obtain other types of state estimates. We will define *2k,j* as the estimate of Xk given all measurements up to and including time j. With this notation, we see that 

$$\hat{\hat{x}}_{k,k-1}=\hat{\hat{x}}_{k}^{-}$$ $$\hat{\hat{x}}_{k,k}=\hat{\hat{x}}_{k}^{+}\tag{1}$$
$$(9.2)$$

Now suppose, for example, that we have recorded measurements up to time index 54 and we want to obtain an estimate of the state at time index **33.** Our theory in Optimal State Estimation, *First Edition.* By Dan J. Simon ISBN 0471708585 02006 John Wiley & **Sons,** Inc. 

## 263

the previous chapters tells us how to obtain *2T3* or **2i'3f3,** but those estimates only use the measurements up to and including times 32 and **33,** respectively. If we have more measurements (e.g., measurements up to time **54)** it stands to reason that we should be able to get an even better estimate of **233.** This chapter discusses some ways of obtaining better estimates. 

In another scenario, it may be that we are interested in obtaining an estimate of the state at a fixed time j. As measurements keep rolling in, we want to keep updating our estimate *2j.* In other words, we want to obtain *2j,j+l, 2j,j+z,* a. 

This could be the case, for example, if a satellite takes a picture at time j. In order to more accurately process the photograph at time j we need an estimate of the satellite state (position and velocity) at time j. As the satellite continues to orbit, we may obtain additional range measurements of the satellite, so we can continue to update the estimate of zj and thus improve the quality of the processed photograph. 

This situation is called fixed-point smoothing because the time point for which we want to obtain a state estimate (time j in this example) is fixed, but the number of measurements that are available to improve that estimate continually changes. Fixed-point smoothing is depicted in Figure 9.1 and is discussed in Section **9.2.** 

![1_image_0.png](1_image_0.png)

Figure **9.1** Fixed-point smoothing. We desire an estimate of **24.** Up until k = 4, the standard Kalman filter operates. At k = 4, we have 2; = **24,4,** which is the estimate of 24 based on measurements up to and including **93.** As time progresses, we continue to refine our estimate of 24 based on an increasing number of measurements. At time k = N, we have 24,~, which is the estimate of 24 based on measurements up to and including time N - 1. 
Another type of smoothing is fixed-lag smoothing. In this situation, we want to obtain an estimate of the state at time (k - N) given measurements up to and including time k, where the time index Ic continually changes as we obtain new measurements, but the lag N is a constant. In other words, at each time point we have N future measurements available for our state estimate. We therefore want to obtain *?k-N,k* for k = *N,N* + l,..., where N is a fixed positive integer. This could be the case, for example, if a satellite is continually taking photographs that are to be displayed or transmitted N time steps after the photograph is taken. In this case, since the photograph is processed N time steps after it is taken, we have N additional measurements after each photograph that are available to update the estimate of the satellite state and hence improve the quality of the photograph. Fixed-lag smoothing is depicted in Figure **9.2** and is discussed in Section **9.3.** 
The final type of smoothing is fixed-interval smoothing. In this situation, we have a **fixed** interval of measurements **(yl,** y2, . - 3, YM) that are available, and we want to obtain the optimal state estimates at all the times in that interval. For each state estimate we want to use all of the measurements in the time interval. That is, we want to obtain *20,~,* **21,~,** . . a, *~M,M.* This is the case when we have recorded 

![2_image_0.png](2_image_0.png)

Figure 9.2 Fixed-lag smoothing. We desire an estimate of the state at each time step based on measurements two time steps ahead. After processing **y2,** we form the estimate &,2, which is the estimate of 20 based on measurements up to and including yz. Similarly, 
?1,3 is the estimate of z1 based on measurements up to and including **y3.** 
some data that are available for post-processing. For example, if a manufacturing process has run over the weekend and we have recorded all of the data, and now we want to plot a time history of the best estimate of the process state, we can use all of the recorded data to estimate the states at each of the time points. Fixed-interval smoothing is depicted in Figure 9.3 and is discussed in Section 9.4. 

![2_image_1.png](2_image_1.png)

Figure 9.3 Fixed-interval smoothing. We desire an estimate of the state at each time step based on all of the measurements in some interval. After processing **all** of the measurements kom y1 to y~, we form the estimate *&o,M,* which is the estimate of 20 based on **all** the measurements. Similarly, **51,~** is the estimate of x1 based on all the measurements. 
Our derivation of these optimal smoothers will be based on a form for the Kalman filter different than we have seen in previous chapters. Therefore, before we can discuss the optimal smoothers, we will first present an alternate Kalman filter form in Section 9.1. 

## 9.1 **An Alternate Form For The Kalman Filter**

.In order to put ourselves in position to derive optimal smoothers, we first need to derive yet another form for the. Kalman filter. This is the form presented in [And79]. 

The equations describing the system and the Kalman filter were derived in Section 5.1 as follows: 

$\scriptsize\frac{2}{4}$  3. 
I k

$\begin{array}{ccc}\blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\\ \blacksquare&=&\blacksquare\end{array}$  . 
$F_{k-1}x_{k-1}+w_{k-1}$  $H_{k}x_{k}+v_{k}$  $F_{k}P_{k}^{+}F_{k}^{T}+Q_{k}$  $P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}$  $(I-K_{k}H_{k})P_{k}^{-}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}$  $F_{k-1}\hat{x}_{k-1}^{+}$  $\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$
$$(9.3)$$
Now if we define Lk as

$$L_{k}$$
$$\begin{array}{r l}{={}}&{{}F_{k}K_{k}}\\ {={}}&{{}F_{k}P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}}\end{array}$$
$$(9.4)$$

and substitute the expression for x into the expression for 2x+1, then we obtain

$$\hat{x}_{k+1}^{-}=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$$ $$=F_{k}\hat{x}_{k}^{-}+L_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$$
$$(9.5)$$

Expanding the expression for P+ gives

$$P_{k}^{+}=P_{k}^{-}-K_{k}H_{k}P_{k}^{-}-P_{k}^{-}H_{k}^{T}K_{k}^{T}+K_{k}H_{k}P_{k}^{-}H_{k}^{T}K_{k}^{T}+K_{k}R_{k}K_{k}^{T}$$  **Note:** _for $K_{k}$_
$$(9.6)$$

Substituting for Kk gives

$$P_{k}^{+}\quad=$$
= P2 - P2 H2 (HkPE H2 + Rk) -1 HkP2 - P H (Hk P H H + Rk) - 1 Hk P + P H2 (HxP H2 + Bk)-1 H2P2 H2 (HkP H2 + Bk)-1HkP2 + P2 H2 (HkB= H2 + Rk)_1 Bk(HzB= H2 + Bk)_1 H2F2

$${}^{+}$$ $$(9.7)$$

Performing some factoring and collection of like terms on this equation gives

 Pk it
it B + PE H& [-(H&B= Hx + Bx)-1 - (H&P= H& + Bk)-++ (Hr Pi Hi + Bk) -1 Hr B H (Hk P H H + Bx) -1 + (HkPz H2 + Rk)-1 Rk(HkPx Hk + Bk)-1] HkPz = B2 + BE HE {-(HrBE H2 + Bk)-1 - (H&B H& + Bx)-1+ (HkPx Hg + Rk)-1(HkPx Hx + Rk)(HkPx Hx + Rk)-1] HkP2 = Px - Px H (HkP H Hk + Rk)-1 Hk Pr
$$\overline{{{\mathfrak{s}}}}$$
Substituting this expression for Pr into the expression for Px+1 gives

$$\begin{array}{r c l}{{P_{k+1}^{-}}}&{{=}}&{{F_{k}P_{k}^{+}F_{k}^{T}+Q_{k}}}\\ {{}}&{{=}}&{{F_{k}[P_{k}^{-}-P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}H_{k}P_{k}^{-}]F_{k}^{T}+Q_{k}}}\\ {{}}&{{=}}&{{F_{k}P_{k}^{-}(F_{k}-L_{k}H_{k})^{T}+Q_{k}}}\end{array}$$
$$(9.9)$$
$$\begin{array}{c}{{y_{k}}}\\ {{P_{k+1}^{-}}}\\ {{K_{k}}}\\ {{P_{k}^{+}}}\\ {{\hat{x}_{k}^{-}}}\\ {{\hat{x}_{k}^{+}}}\end{array}$$

Combining Equations (9.4), (9.5), and (9.9) gives the alternate form for the one-step a *priori* Kalman filter, which can be summarized as follows: 

$$L_{k}=F_{k}P_{k}^{-}H_{k}^{T}\left(H_{k}P_{k}^{-}H_{k}^{T}+R_{k}\right)^{-1}$$ $$P_{k+1}^{-}=F_{k}P_{k}^{-}\left(F_{k}-L_{k}H_{k}\right)^{T}+Q_{k}$$ $$\hat{x}_{k+1}^{-}=F_{k}\hat{x}_{k}^{-}+L_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})\tag{9.10}$$

where Lk is the redefined Kalman gain. This form of the filter obtains only a *priori* state estimates and covariances. Note that the Kalman gain, **Lk,** for this form of the filter is not the same as the Kalman gain, *Kk,* for the form of the filter that we derived in Section 5.1. However, the two forms result in identical state estimates and estimation-error covariances. 

## 9.2 Fixed-Point Smoothing

The objective in fixed-point smoothing is to obtain a *priori* state estimates of x3 at times j + 1, j + 2, e. a, *k, k* + 1, .... We will use the notation *?j,k* to refer to the estimate of x3 that is obtained by using all of the measurements up to and including time (k - 1). That is, *?j,k* can be thought of as the a *priori* estimate of x3 at time k: 

$$\begin{array}{r c l}{{\hat{x}_{j,j}}}&{{=}}&{{E(x_{j}|y_{1},\cdots,y_{j-1})}}\\ {{}}&{{=}}&{{\hat{x}_{j}^{-}}}\end{array}$$
With this definition we see that 
$\hat{x}_{j,k}=E(x_{j}|y_{1},\cdots,y_{k-1})$$k\geq j$
$$(9.11)$$
$$(9.12)$$
$$\begin{array}{r c l}{{\hat{x}_{j,j+1}}}&{{=}}&{{E(x_{j}|y_{1},\cdots,y_{j})}}\\ {{}}&{{=}}&{{\hat{x}_{j}^{+}}}\end{array}$$

In other words, **2j,j** is just the normal a *priori* state estimate at time j that we derived in Section **5.1.** We also see that 

$$(9.13)$$
$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\end{array}$$

In other words, *23,j+1* is just the normal a *posteriori* state estimate at time j that we derived in Section 5.1. The question addressed by fixed-point smoothing is as follows: When we get the next measurement at time (j + l), how can we incorporate that information to obtain an improved estimate (along with its covariance) for the state at time j? Furthermore, when we get additional measurements at times 
(j *+2),* (j **+3),** etc., how can we incorporate that information to obtain an improved estimate (along with its covariance) for the state at time j? 

In order to derive the fixed-point smoother, we will define a new state variable *2'.* 
This new state variable will be initialized as xi = zj, and will have the dynamics XL+~ = **xL (k** = *j, j* + 1,. . .). With this definition, we see that xi = x3 for all k > j. 

So if we can use the standard Kalman filter to find the a *priori* estimate of xi then we will, by definition, have a smoothed estimate of x3 given measurements up to and including time (k - 1). In other words, the a *priori* estimate of xi will be equal to *?i.,,k.* This idea is depicted in Figure 9.4. 

Our original system is given as 

$$(9.14)$$
$$\begin{array}{r l}{+{\mathrm{~................~}}+{\mathrm{~\underline{{~\phantom{~\downarrow~}~}}~}}+{\mathrm{~................~}}=}\\ {x_{1}{\mathrm{~................~}}\quad x_{j}}&{x_{j+1}{\mathrm{~................~}}}\\ {\qquad\qquad x_{j}^{\prime}=x_{j}}&{x_{j+1}^{\prime}=x_{j}{\mathrm{~................~}}\quad x_{j}^{\prime}}\end{array}$$

![5_image_0.png](5_image_0.png)

Figure **9.4** This illustrates the idea that is used to obtain the fked-point smoother. A 
fictitious state variable x' is initialized as x: = x3 and from that point on has an identity state transition matrix. The a *priari* estimate of xk is then equal to *23,k.* 
Augmenting the dynamics of our newly defined state x' to the original system results in the following: 

$$\left[\begin{array}{c}x_{k}\\ x^{\prime}_{k}\end{array}\right]=\left[\begin{array}{cc}F_{k-1}&0\\ 0&I\end{array}\right]\left[\begin{array}{c}x_{k-1}\\ x^{\prime}_{k-1}\end{array}\right]+\left[\begin{array}{c}I\\ 0\end{array}\right]w_{k-1}$$ $$y_{k}=\left[\begin{array}{cc}H_{k}&0\end{array}\right]\left[\begin{array}{c}x_{k}\\ x^{\prime}_{k}\end{array}\right]+v_{k}\tag{9.15}$$
$$E\left[\left(\begin{array}{c}x_{k}-\hat{x}_{k}^{-}\\ x_{j}-\hat{x}_{j,k}\end{array}\right)\left(\begin{array}{cc}(x_{k}-\hat{x}_{k}^{-})^{T}&(x_{j}-\hat{x}_{j,k})^{T}\end{array}\right)\right]=\left[\begin{array}{cc}P_{k}&\Sigma_{k}^{T}\\ \Sigma_{k}&\Pi_{k}\end{array}\right]\tag{9.16}$$

If we use a standard Kalman filter to obtain an a *priori* estimate of the augmented state, the covariance of the estimation error can be written as The covariance Pk above is the normal a *pri0q-i* covariance of the estimate of *Xk.* We have dropped the minus superscript for ease of notation, and we will also feel free to drop the minus superscript on all other quantities in this section with the understanding that all estimates and covariances are a priori. The ck and *Ilk* matrices are defined by the above equation. Note that at time k = j, & and *IIk* are given as 

$$\begin{array}{r c l}{{\Sigma_{j}}}&{{=}}&{{E\left[(x_{j}-\hat{x}_{j,j})(x_{j}-\hat{x}_{j}^{-})^{T}\right]}}\\ {{}}&{{=}}&{{E\left[(x_{j}-\hat{x}_{j}^{-})(x_{j}-\hat{x}_{j}^{-})^{T}\right]}}\\ {{}}&{{=}}&{{P_{j}}}\\ {{\Pi_{j}}}&{{=}}&{{E\left[(x_{j}-\hat{x}_{j,j})(x_{j}-\hat{x}_{j,j})^{T}\right]}}\\ {{}}&{{=}}&{{E\left[(x_{j}-\hat{x}_{j}^{-})(x_{j}-\hat{x}_{j}^{-})^{T}\right]}}\\ {{}}&{{=}}&{{P_{j}}}\end{array}$$
$$(9.17)$$
$$|{\mathrm{~}}(9.18)$$
= Pj (9.17) 

The Kalman filter summarized in Equation (9.10) can be written for the augmented system as follows: 
where Lk is the normal Kalman filter gain given in Equation (9.10), and Xk is the additional part of the Kalman gain, which will be determined later in this section. 

Writing Equation (9.18) as two separate equations gives 

$$\hat{x}_{k+1}=F_{k-1}\hat{x}_{k}^{-}+L_{k}\left(y_{k}-H_{k}\hat{x}_{k}^{-}\right)$$ $$\hat{x}_{j,k+1}^{-}=\hat{x}_{j,k}^{-}+\lambda_{k}\left(y_{k}-H_{k}\hat{x}_{k}^{-}\right)\tag{9.19}$$

The Kalman gain can be written from Equation (9.10) as follows: 

Pk xT  [::I = [Fi-l ;I[,, $][?Ix  Writing this equation as two separate equations gives 
 In Equation (9.10) as follows:  $\left.\begin{array}{l}\Sigma_{k}^{T}\\ \Pi_{k}\end{array}\right]\left[\begin{array}{l}H_{k}^{T}\\ 0\end{array}\right]\times$  $\left.\begin{array}{l}\Sigma_{k}^{T}\\ \Pi_{k}\end{array}\right]\left[\begin{array}{l}H_{k}^{T}\\ 0\end{array}\right]+R_{k}\right)^{-1}$                      (9.20)  $\left.\begin{array}{l}\Sigma_{k}^{T}\\ \Pi_{k}\end{array}\right]\left[\begin{array}{l}H_{k}^{T}\\ 0\end{array}\right]\left(H_{k}P_{k}H_{k}^{T}+R_{k}\right)^{-1}$  equations gives  $s_{1}=-\sigma_{1}=\sigma_{1}+1$. 
$$(9.21)$$
$$\begin{array}{r c l}{{{\cal L}_{k}}}&{{=}}&{{F_{k}P_{k}H_{k}^{T}(H_{k}P_{k}H_{k}^{T}+R_{k})^{-1}}}\\ {{\lambda_{k}}}&{{=}}&{{\Sigma_{k}H_{k}^{T}(H_{k}P_{k}H_{k}^{T}+R_{k})^{-1}}}\end{array}$$
The Kalman filter estimation-error covarianceupdate equation can be written from Equation (9.10) as follows: 

Fk 0 pk xz [ xk+l "+' nk+l "+' ] = [ 0 I] [ Ck rIk ]  Qk 0  (9.22) 
$$(9.23)$$
Writing this equation as three separate equations gives 

$$\begin{array}{l c l}{{P_{k+1}}}&{{=}}&{{F_{k}P_{k}(F_{k}-L_{k}H_{k})^{T}+Q_{k}}}\\ {{\Pi_{k+1}}}&{{=}}&{{\Pi_{k}-\Sigma_{k}H_{k}^{T}\lambda_{k}^{T}}}\\ {{\Sigma_{k+1}^{T}}}&{{=}}&{{-F_{k}P_{k}H_{k}^{T}\lambda_{k}^{T}+F_{k}\Sigma_{k}^{T}}}\\ {{\Sigma_{k+1}}}&{{=}}&{{\Sigma_{k}(F_{k}-L_{k}H_{k})^{T}}}\end{array}$$

It is not immediately apparent from the above expressions that Cftl is really the transpose of *ck+l,* but the equality can be established by substituting for Pk and Lk* Equations (9.19) - (9.23) completely define the fixed-point smoother. The fixedpoint smoother, which is used for obtaining ei.,,k = *E(zjIyl,...,pk-l)* for k L j, can be summarized as follows. 

## The Fixed-Point **Smoother**

1. Run the standard Kalman filter up until time j, at which point we have 2; and *P37.* In the algorithm below, we omit the minus superscript on *Pi.,:* for ease of notation. 

2. Initialize the filter as follows: 

$$\begin{array}{r c l}{{\Sigma_{j}}}&{{=}}&{{P_{j}}}\\ {{\Pi_{j}}}&{{=}}&{{P_{j}}}\\ {{\hat{x}_{j,j}}}&{{=}}&{{\hat{x}_{j}^{-}}}\end{array}$$
$$(9.24)$$
e3,j = ej- (9.24) 

3. For k = *j, j* + 1, - a, perform the following: 
As we recall from Equation **(9.16),** Pk is the a *priori* covariance of the standard Kalman filter estimate, **IIk** is the covariance of the smoothed estimate of xJ at time k, *and* Ck is the cross covariance between the two. 

## Estimation Improvement Due To Smoothing 9.2.1

Now we will look at the improvement in the estimate of xJ due to smoothing. The estimate 2; is the standard a *priori* Kalman filter estimate of x3, and the estimate ?J,k+l is the smoothed estimate after measurements up to and including time k have been processed. In other words, *i$,k* uses (k + 1 - j) more measurements to obtain the estimate of xJ than 2; uses. How much more accurate can we expect our estimate to be with the use of these additional (k + 1 - j) measurements? 

The estimation accuracy can be measured by the covariance. The improvement in estimation accuracy due to smoothing is equal to the standard estimation covariance PJ minus the smoothed estimation covariance *nk+l.* We can use Equations **(9.24)** and **(9.25)** to write this improvement as 

$$P_{j}-\Pi_{k+1}=\Pi_{j}-\left(\Pi_{j}-\sum_{i=j}^{k}\Sigma_{i}H_{i}^{T}\lambda_{i}^{T}\right)\tag{9.26}$$ $$=\sum_{i=j}^{k}\Sigma_{i}H_{i}^{T}\lambda_{i}^{T}$$
$$\Sigma_{k+1}=\Sigma_{k}(F-L H)^{T}$$

Now assume for purposes of additional analysis that the system is timeinvariant 
and the covariance of the standard filter has reached steady state at time j. Then 
we have 
$$\operatorname*{lim}_{k\to\infty}P_{k}^{-}=P$$
From Equation **(9.25)** we see that 
$$\begin{array}{r c l}{{\Sigma_{k+1}}}&{{=}}&{{P\left[(F-L H)^{T}\right]^{k+1-j}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{P\left({\tilde{F}}^{T}\right)^{k+1-j}}}\end{array}$$
where C is initialized as Cj = P. Combining this expression for *&+I* with its initial value, we see that 

$$(9.27)$$

$$(9.28)$$
$$(9.29)$$
$$P_{j}-\Pi_{k+1}=\sum_{i=j}^{k}\Sigma_{i}H^{T}\lambda^{T}\tag{9.30}$$ $$=P\left[\sum_{i=j}^{k}\left(\tilde{F}^{T}\right)^{i-j}H^{T}(HPH^{T}+R)^{-1}H\tilde{F}^{i-j}\right]P$$

where $' is defined by the above equation. Now substitute this expression, and the expression for X from Equation *(9.25),* into Equation *(9.26)* to obtain The quantity on the right side of this equation is positive definite, which shows that the smoothed estimate of zj is always better than the standard Kalman filter estimate. In other words, (Pj - *&+I)* > 0, which implies that &+I < *Pj.* 
Furthermore, the quantity on the right side is a sum of positive definite matrices, which shows that the larger the value of k (i.e., the more measurements that we use to obtain our smoothed estimate), the greater the improvement in the estimation accuracy. Also note from the above that the quantity *(HPHT* + R) inside the summation is inverted. This shows that as R increases, the quantity on the right side decreases. In the limit we see from Equation *(9.30)* that 

$$\operatorname*{lim}_{R\to\infty}(P_{j}-\Pi_{k+1})=0$$
$$(9.31)$$

This illustrates the general principle that the larger the measurement noise, the smaller the improvement in estimation accuracy that we can obtain by smoothing. This is intuitive because large measurement noise means that additional measurements will not provide much improvement to our estimation accuracy. 

## Example9.1

In this example, we will see the improvement due to smoothing that can be obtained for a vehicle navigation problem. This is a second-order Newtonian system where ~(1) is position and **42)** is velocity. The input is comprised of a commanded acceleration u plus acceleration noise 6. The measurement y is a noisy measurement of position. After discretizing with a step size of T, the system equations can be written as 

$$\left[\begin{array}{cc}1&T\\ 0&1\end{array}\right]x_{k}+\left[\begin{array}{c}T^{2}/2\\ T\end{array}\right](u_{k}+\tilde{u}_{k})$$ $$\left[\begin{array}{cc}1&T\\ 0&1\end{array}\right]x_{k}+\left[\begin{array}{c}T^{2}/2\\ T\end{array}\right]u_{k}+w_{k}$$ $$\left[\begin{array}{cc}1&0\end{array}\right]x_{k}+v_{k}\tag{9}$$
$$\begin{array}{r l}{x_{k+1}}&{{}=}\\ {}&{}\\ {}&{{}=}\\ {y_{k}}&{{}=}\end{array}$$

Note that the process noise Wk is given as 

$$(9.32)$$
$$w_{k}=\left[\begin{array}{c}T^{2}/2\\ T\end{array}\right]\tilde{u}_{k}\tag{9.33}$$

Now suppose the acceleration noise 6k **has** a standard deviation of a. We obtain the process noise covariance as follows: 

$$(9.34)$$

The percent improvement due to smoothing can be defined as 

$$\begin{array}{r c l}{{Q_{k}}}&{{=}}&{{E(w_{k}w_{k}^{T})}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l}{{T^{4}/4}}&{{T^{3}/2}}\\ {{T^{3}/2}}&{{T^{2}}}\end{array}\right]E(\tilde{u}_{k}^{2})}}\\ {{}}&{{=}}&{{a^{2}\left[\begin{array}{l l}{{T^{4}/4}}&{{T^{3}/2}}\\ {{T^{3}/2}}&{{T^{2}}}\end{array}\right]}}\end{array}$$
$$\frac{100\ \mathrm{Tr}(P_{j}-\Pi_{k+1})}{\mathrm{Tr}(P_{j})}\qquad\qquad(9.35)$$
 Percent Improvement $=\dfrac{100\text{T}}{\text{m}}\\$. 
where j is the point which is being smoothed, and k is the number of measurements that are processed by the smoother. We can run the fixed-point smoother given by Equation (9.25) in order to smooth the position and velocity estimate at any desired time. Suppose we use the smoother equations to smooth the estimate at the second time step (k = 1). If we use measurements at times up to and including 10 seconds to estimate **21,** then our estimate is denoted **as 41,101.** In this case, Table 9.1 shows the percent improvement due to smoothing after 10 seconds when the time step T = 0.1 and the acceleration noise standard deviation a = *0.2.* As expected from the results of the previous subsection, we see that the improvement due to smoothing is more dramatic for small measurement noise. 

Table 9.1 seconds for Example 9.1. The improvement due to smoothing is more noticeable when the measurement noise is small. 

Improvement due to smoothing the state at the first time step after 10 

| Measurement noise                                                             | Percent   |
|-------------------------------------------------------------------------------|-----------|
| standard deviation Improvement  0.1 99.7  1 96.6  10 59.3  100 13.7  1000 0.2 |           |

Figure 9.5 shows the trace of IIk, which is the covariance of the estimation error of the state at the first time step. As time progresses, our estimate of the state at the first time step improves. After 10 seconds of additional measurements, the estimate of the state at the first time step has improved by 96.6% relative to the standard Kalman filter estimate. Figure 9.6 shows the smoothed estimation error of the position and velocity of the first time step. We see that processing more measurements decreases the estimation-error covariance. 

In general, the smoothed estimation errors shown in Figure 9.6 will converge to nonzero values. The estimation errors are zero-mean, but not for 

![10_image_0.png](10_image_0.png)

This shows the trace of the estimation-error covariance of the smoothed Figure 9.5 estimate of the state at the first time step for Example 9.1. As time progresses and we process more measurements, the covariance decreases, eventually reaching steady state.

![10_image_1.png](10_image_1.png)

Figure 9.6 This shows typical estimation errors of the smoothed estimate of the state at the first time step for Example 9.1. As time progresses and we process more measurements, the estimation error decreases, and its standard deviation eventually reaches steady state.
any particular simulation. The estimation errors are zero-mean when averaged over many simulations. The system discussed here was simulated 1000 times and the variance of the estimation errors (x1 - x1,101) were computed numerically to be equal to 0.054 and 0.012 for the two states. The diagonal elements of II01 were equal to 0.057 and 0.012.

���

## 9.2.2 Smoothing Constant States

$$P_{k+1}=F_{k}P_{k}(F_{k}-L_{k}H_{k})^{T}+Q_{k}\tag{9.36}$$ $$=P_{k}(I-L_{k}H_{k})^{T}$$ $$\Sigma_{k+1}=\Sigma_{k}(F_{k}-L_{k}H_{k})^{T}$$ $$=\Sigma_{k}(I-L_{k}H_{k})^{T}$$

Now we will think about the improvement (due to smoothing) in the estimation accuracy of constant states. If the system states are constant then Fk = I and Q = 0. Equation **(9.25)** shows that Comparing these expressions for and *&+I,* and realizing from Equation **(9.24)** 
that the initial value of C, = *P,,* we see that & = Pk **for** k *2 j.* This means that the expression for Lk from Equation **(9.25)** can be written as 

$$\begin{array}{r l}{{}}&{{}={}}\\ {{}}&{{}F_{k}P_{k}H_{k}^{T}\left(H_{k}P_{k}H_{k}^{T}+R_{k}\right)^{-1}}\\ {{}}&{{}={}}\\ {{}}&{{}\Sigma_{k}H_{k}^{T}\left(H_{k}P_{k}H_{k}^{T}+R_{k}\right)^{-1}}\\ {{}}&{{}={}}\\ {{}}&{{}\lambda_{k}}\end{array}$$
$$L_{k}$$
$$\begin{array}{r c l}{{\Pi_{k+1}}}&{{=}}&{{\Pi_{k}-\Sigma_{k}H_{k}^{T}\lambda_{k}^{T}}}\\ {{}}&{{=}}&{{\Pi_{k}-P_{k}H_{k}^{T}L_{k}^{T}}}\end{array}$$

Substituting these results into the expression for *l&+1* from Equation **(9.25)** we see that 

$$(9.36)$$
$$(9.37)$$
$$(9.38)$$

Realizing that the initial value of II, = *Pj,* and comparing this expression for *&+I* 
with Equation **(9.36)** for *Pk+l,* we see that & = Pk for k 2 j. Recall that Pk is the covariance of the estimate of xk from the standard Kalman flter, and & is the covariance of the estimate of x, given measurements up to and including time 
(k - 1). 

This result shows that constant states are not smoothable. Additional measurements are still helpful for refining an estimate of a constant state. However, there is no point to using smoothing for estimation of a constant state. If we want to estimate a constant state at time j using measurements up to time k > j, then we may as well simply run the standard Kalman filter up to time k. Implementing the smoothing equations will not gain any improvement in estimation accuracy. 

## 9.3 Fixed-Lag Smoothing

In fixed-lag smoothing we want to obtain an estimate of the state at time (k - N) 
given measurements up to and including time k, where the time index k continually changes as we obtain new measurements, but the lag N is a constant. In other words, at each time point we have N future measurements available for our state estimate. We therefore want to obtain *Sk-N,k* for k = *N, N* + **1,.** . ., where N is a fixed positive integer. This could be the case, for example, if a satellite is continually taking photographs that are to be displayed or transmitted N time steps after the photograph is taken. In this case, since the photograph is processed N time steps after it is taken, we have N additional measurements after each photograph that are available to update the estimate of the satellite state and hence improve the quality of the photograph. In this section we use the notation 

$$\hat{\hat{x}}_{k-N,k}=E(x_{k-N}|y_{1},\cdots,y_{k})$$ $$\Pi_{k-N}=E\left[(x_{k-N}-\hat{x}_{k-N,k})(x_{k-N}-\hat{x}_{k-N,k})^{T}\right]\tag{9.39}$$

Note that the notation has changed slightly from the previous section. In the previous section we used the notation **&,m** to refer to the estimate of Xk given measurements up to and including time (m - 1). In this section (and in the remainder of this chapter) we use *2k,m* to refer to the estimate of Xk given measurements up to and including time m. 

Let us define *Xk,m* as the state *Xk-n* propagated with an identity transition matrix and zero process noise to time k. With this definition we see that 

$\begin{array}{ccc}x_{k+1,1}&=&x\\ x_{k+1,2}&=&3\\ &=&2\\ x_{k+1,3}&=&3\\ &=&2\\ &=&2\\ &\text{etc.}\end{array}$
xk,l - 
$${x}_{{k}}$$ $${x}_{{k}-{1}}$$ $${x}_{{k},{1}}$$ $${x}_{{k}-{2}}$$ $${x}_{{k},{2}}$$
$$(9.40)$$
$$(9.41)$$
We can therefore define the augmented system 

$$\left[\begin{array}{c}x_{k+1}\\ x_{k+1,1}\\ \vdots\\ x_{k+1,N+1}\end{array}\right]=\left[\begin{array}{cccc}F_{k}&0&\cdots&0\\ I&0&\cdots&0\\ \vdots&\ddots&\ddots&\vdots\\ 0&\cdots&I&0\end{array}\right]\left[\begin{array}{c}x_{k}\\ x_{k,1}\\ \vdots\\ x_{k,N+1}\end{array}\right]+\left[\begin{array}{c}I\\ 0\\ \vdots\\ 0\end{array}\right]w_{k}$$ $$y_{k}=\left[\begin{array}{cccc}H_{k}&0&\cdots&0\end{array}\right]\left[\begin{array}{c}x_{k}\\ x_{k,1}\\ \vdots\\ x_{k,N+1}\end{array}\right]+v_{k}\tag{1}$$

The Kalman filter estimates of the components of this augmented state vector are given as 

$$E(x_{k+1}|y_{1}\cdot\cdot\cdot y_{k})$$  $$E(x_{k+1,1}|y_{1}\cdot\cdot\cdot y_{k})$$
$$\begin{array}{l}{{\hat{x}_{k+1}^{-}}}\\ {{\hat{x}_{k+1,k}}}\\ {{E(x_{k}|y_{1}\cdot\cdot\cdot y_{k})}}\\ {{\hat{x}_{k}^{+}}}\\ {{\hat{x}_{k,k}}}\\ {{E(x_{k-1}|y_{1}\cdot\cdot\cdot y_{k})}}\\ {{\hat{x}_{k-1,k}}}\end{array}$$

$$E(x_{k+1,2}|y_{1}\cdot\cdot\cdot y_{k})$$
E(Zk+lIYl ' ' * Yk) = **L+l* 
= **k+l,k* 
E(Zk+l,llYl + * 'Yk) = E(xklY1 * **Yk)* 
- 2$ 
= *k,k 
E(xk+1,21Y1 * * 'Yk) = *E(xk-llyl* * * *'Yk)* 
= *k-l,k 
$E(x_{k+1,N+1}|y_{1}\cdots y_{k})=\hat{\Sigma}_{k-N,k}$
$$(9.42)$$

We see that if we can use a Kalman filter to estimate the states of the augmented system (using measurements up to and including time k), then the estimate of the last element of the augmented state vector, xk+1,N+1, will be equal to the estimate of xx-N given measurements up to and including time k. This is the estimate that we are looking for in fixed-lag smoothing. This idea is illustrated in Figure 9.7.

$\begin{array}{c}\includegraphics[height=142.26375pt]{Fig1}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig2}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig3}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig4}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig5}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig6}\end{array}$  $\begin{array}{c}\includegraphics[height=142.26375pt]{Fig7}\end{array}$  \(\begin{array}{c}\includegraphics[height=142.  
Figure 9.7 This illustrates the idea that is used to obtain the fixed-lag smoother. A
fictitious state variable xk,m is initialized as xk,m = xk-m and from that point on has an identity state transition matrix. The a posteriori estimate of x+m,m is then equal to
£k-m.k.

From Equation (9.10) we can write the Kalman filter for the augmented system of Equation (9.41) as follows:

Fk 0 x + + 1 0 fk Îk, k I 0 Îk-1,k-1 0 + : Îk-N,k 0 I 0 Îk-(N+1),k-1 Lk,0 x Lk, 1 Îk - 1, k - 1 Hk 0 0 (9.43) yk - .. Lk, N+1 x k - ( N + 1 ) , k .
where the Lk, matrices are components of the smoother gain that will be determined in this section. Note that Lk,o is the standard Kalman gain. The smoother gain Lk is defined as

$$L_{k}=\left[\begin{array}{c}{{L_{k,0}}}\\ {{L_{k,1}}}\\ {{\vdots}}\\ {{L_{k,N+1}}}\end{array}\right]$$

$$(9.44)$$

From Equation (9.10) we see that the Lk gain matrix is given by

$$\begin{array}{r c l}{{L_{k}}}&{{=}}&{{\left[\begin{array}{c c c c}{{F_{k}}}&{{0}}&{{\cdots}}&{{0}}\\ {{I}}&{{0}}&{{\cdots}}&{{0}}\\ {{\vdots}}&{{\ddots}}&{{\ddots}}&{{\vdots}}\\ {{0}}&{{\cdots}}&{{I}}&{{0}}\end{array}\right]}}\\ {{}}&{{}}&{{}}&{{}}\\ {{\left(\begin{array}{c c c c}{{}}&{{}}&{{}}&{{}}\\ {{I_{k}}}&{{0}}&{{\cdots}}&{{0}}\end{array}\right]\left[\begin{array}{c c c c}{{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{\vdots}}&{{}}&{{\ddots}}\\ {{P_{k}^{0,N+1}}}&{{}}&{{\cdots}}\end{array}\right]}}\end{array}$$
H f P,0,0 (P0,N+1)T 0 o0,N+1 P + 1,N + 1 0  H (Po, N+1)T 0 + Rk : P;V+1,N+1 0
$$\mathbf{\nabla}\times$$
$$(9.45)$$

where the P2 covariance matrices are defined as

$P_{k}^{i,j}=E\left[(x_{k-j}-\hat{x}_{k-j,k-1})(x_{k-i}-\hat{x}_{k-i,k-1})^{T}\right]$
$$(9.46)$$

The Lk expression above can be simplified to

$$L_{k}=\left[\begin{array}{c}F_{k}P_{k}^{0,0}H_{k}^{T}\\ P_{k}^{0,0}H_{k}^{T}\\ \vdots\\ P_{k}^{0,N}H_{k}^{T}\end{array}\right](H_{k}P_{k}^{0,0}H_{k}^{T}+R_{k})^{-1}\tag{9.47}$$

From Equation (9.10) we see that the covariance-update equation for the Kalman filter for our augmented system can be written as

Fk 0 0 (P&+I P&+1 P,0,0 I 0 0  x , N +1 P0,N+1 P:V+1,N+1 P:N+1,N+1 P.º. k + 1 0 0  k k k +1 FK I 0  H 2 0 Qk 0 0 0 0 0 0 0 LT (9.48) + 0 0 0
Substituting for Lk from Equation (9.47) and multiplying out gives

p0,0 k + 1 0, N +1 k+1
0,17 Fx P0,0 Fk (Po,N+1)T (Po,N+1)T (Po, N+ P0,0 (Po, k × PN+1,N+1 Pk+1 (PN,N+1)T Pr N P0,N FT I 0 0 0 0 H + Rk)-1 Hkx I 0 0 PO: FF D, N P0,0 Qx 0 0 K k 0 0 0 0 0 (9.49) + 0 0 0
This gives us the update equations for the P matrices. The equations for the first column of the P matrix are as follows:

$$P_{k+1}^{0,0}=F_{k}P_{k}^{0,0}\left[F_{k}^{T}-H_{k}^{T}(H_{k}P_{k}^{0,0}H_{k}^{T}+R_{k})^{-1}H_{k}P_{k}^{0,0}F_{k}^{T}\right]+Q_{k}\tag{5}$$ $$=F_{k}P_{k}^{0,0}(F_{k}-L_{k,0}H_{k})^{T}+Q_{k}$$ $$P_{k+1}^{0,1}=P_{k}^{0,0}(F_{k}-L_{k,0}H_{k})^{T}$$ $$\vdots$$ $$P_{k+1}^{0,N+1}=P_{k}^{0,N}(F_{k}-L_{k,0}H_{k})^{T}$$
$$(9.50)$$

The equations for the diagonal elements of the P matrix are as follows: 

pi,% k+l = 'k a-1,%-1 - 'k O,%-~HTLT k k,a FT k (9.51) 
These equations give us the formulas that we can use for fixed-lag smoothing. This gives us the estimate *E(Zk-NIY1,* - - , *yk)* for a **fixed** N as k continually increments. 

The fixed-lag smoother is summarized as follows. 

## The Fixed-Lag Smoother

1. Run the standard Kalman filter of Equation (9.10) to obtain *5;+l, Lk,* and PL . 

$$\begin{array}{r c l}{{\hat{x}_{k+1,k}}}&{{=}}&{{\hat{x}_{k+1}^{-}}}\\ {{}}&{{L_{k,0}}}&{{=}}&{{L_{k}}}\\ {{}}&{{P_{k}^{0,0}}}&{{=}}&{{P_{k}^{-}}}\end{array}$$

2. Initialize the fixed-lag smoother as follows: 

$$(9.52)$$

3. For i = 1, + a, N + 1, perform the following: 
Note that the first time through this loop is the measurement update of the standard Kalman filter. At the end of this loop we have the smoothed estimates of each state with delays between 0 and N, given measurements up to and including time k. These estimates are denoted *&,k,* **..a,** *&lN,k.* we also have the estimation-error covariances, denoted Pi$l, . a, *Pk+l N+1,N+1* The percent improvement due to smoothing can be computed as 

Percent Improvement = $\frac{100\ \mathrm{Tr}(P_{k}^{0,0}-P_{k}^{N+1,N+1})}{\mathrm{Tr}(P_{k}^{0,0})}$ (9.54)

## Example9.2

Consider the same two state system as described in Example 9.1. Suppose we are trying to estimate the state of the system with a fixed time lag. The discretization time step T = 0.1 and the standard deviation of the acceleration noise is 10. Figure 9.8 shows the percent improvement in state estimation that is available with fixed-lag smoothing. The figure shows percent improvement as a function of lag size, and for two different values of measurement noise. The values on the plot are based on the theoretical estimation-error covariance. 

As expected, the improvement in estimation accuracy is more dramatic as the measurement noise **QOm** 
decreases. This was discussed at the end of Section 9.2. 

![16_image_0.png](16_image_0.png)

Figure **9.8** This shows the percent improvement of the trace of the estimation-error covariance of the smoothed estimate of the state (relative to the standard Kalman filter) for Example **9.2. As** the number of lag intervals increases, the estimation error of the smoother decreases and the percent improvement increases. **Also,** as the measurement noise decreases, the improvement due to smoothing is more dramatic. 

## Vvv 9.4 Fixed-Interval Smoothing

Suppose we have measurements for a fixed time interval. In fixed-interval smoothing we **seek** an estimate of the state at some of the interior points of the time interval. During the smoothing process we do not obtain any new measurements. Section 9.4.1 discusses the forward-backward approach to smoothing, which is perhaps the most straightforward smoothing algorithm. Section 9.4.2 discusses the RTS smoother, which is conceptually more difficult but is computationally cheaper than forward-backward smoothing. 

## 9.4.1 Forward-Backward Smoothing

Suppose we want to estimate the state xm based on measurements from k = 1 to k = N, where N > m. The forward-backward approach to smoothing obtains two estimates of *xm.* The first estimate, *Pf,* is based on the standard Kalman filter that operates from k = 1 to k = m. The second estimate, *hb,* is based on a Kalman filter that runs backward in time from k = N back to k = m. The forward-backward approach to smoothing combines the two estimates to form an optimal smoothed estimate. This approach was first suggested in [Fra69]. 

Suppose that we combine a forward estimate Pf of the state and a backward estimate i?b of the state to get a smoothed estimate of x as follows: 

$${\hat{x}}=K_{f}{\hat{x}}_{f}+K_{b}{\hat{x}}_{b}$$

where Kf *and* Kb are constant matrix coefficients to be determined. Note that 

$${\hat{x}}=K_{f}{\hat{x}}_{f}+(I-K_{f}){\hat{x}}_{b}$$

?f *and* Pb are both unbiased since they are both outputs from Kalman filters. 

Therefore, if h is to be unbiased, we require Kf + Kb = I (see Problem 9.9). This gives P = Kfhf + (I - *Kf)&* (9.56) 
The covariance of the estimate can then be found as 

$$(9.55)$$
$$(9.56)$$
$$P=E[(x-\hat{x})(x-\hat{x})^{T}]\tag{9.57}$$ $$=E\left\{[x-K_{f}\hat{x}_{f}-(I-K_{f})\hat{x}_{b}][\cdots]^{T}\right\}$$ $$=E\left\{[K_{f}(e_{f}-e_{b})+e_{b}][\cdots]^{T}\right\}$$ $$=E\left\{K_{f}(e_{f}e_{f}^{T}+e_{b}e_{b}^{T})K_{f}^{T}+e_{b}e_{b}^{T}-K_{f}e_{b}e_{b}^{T}-e_{b}e_{b}^{T}K_{f}^{T}\right\}$$

where ef = x - xf, eb = x - *q,,* and we have used the fact that *E(efer)* = 0. The estimates Pf and i?b are both unbiased, and ef *and* eb are independent (since they depend on separate sets of measurements). We can minimize the trace of P with respect to Kf using results from Equation (1.66) and Problem **1.4:** 

$$=2E\left\{K_{f}(e_{f}e_{f}^{T}+e_{b}e_{b}^{T})-e_{b}e_{b}^{T}\right\}\tag{9.58}$$ $$=2[K_{f}(P_{f}+P_{b})-P_{b}]$$
$$\frac{\partial\mathrm{Tr}(P)}{\partial K_{f}}$$

where Pf = *E(efeT)* is the covariance of the forward estimate, and Pb = *E(eb.5:)* 
is the covariance of the backward estimate. Setting this equal to zero to find the optimal value of Kf gives 

$$(9.59)$$
$$\begin{array}{r c l}{{K_{f}}}&{{=}}&{{P_{b}(P_{f}+P_{b})^{-1}}}\\ {{K_{b}}}&{{=}}&{{P_{f}(P_{f}+P_{b})^{-1}}}\end{array}$$

The inverse of (Pf + *Pb)* always exists since both covariance matrices are positive definite. We can substitute this result into Equation (9.57) to find the covariance of the fixed-interval smoother as follows: 

$$P=P_{b}(P_{f}+P_{b})^{-1}(P_{f}+P_{b})(P_{f}+P_{b})^{-1}P_{b}+$$ $$P_{b}-P_{b}(P_{f}+P_{b})^{-1}P_{b}-P_{b}(P_{f}+P_{b})^{-1}P_{b}\tag{9.60}$$

Using the identity (A + B)-l = **B-'(AB-'+** *I)-l* (see Problem *9.2),* we can write the above equation as 

$$\begin{array}{r c l}{{P}}&{{=}}&{{(P_{f}P_{b}^{-1}+I)^{-1}(P_{f}+P_{b})(P_{b}^{-1}P_{f}+I)^{-1}+}}\\ {{}}&{{}}&{{P_{b}-(P_{f}P_{b}^{-1}+I)^{-1}P_{b}-(P_{f}P_{b}^{-1}+I)^{-1}P_{b}}}\end{array}$$

Multiplyingout the first term, and again using the identity (A+B)-l = *B-'(AB-l* t I)-l on the last two terms, results in 

$$\begin{array}{r c l}{{P}}&{{=}}&{{\left[(P_{b}^{-1}+P_{f}^{-1})^{-1}+(P_{b}^{-1}P_{f}P_{b}^{-1}+P_{b}^{-1})^{-1}\right](P_{b}^{-1}P_{f}+I)^{-1}+}}\\ {{}}&{{}}&{{P_{b}-2(P_{b}^{-1}P_{f}P_{b}^{-1}+P_{b}^{-1})^{-1}}}\end{array}$$
$$(P_{b}^{-1}P_{f}P_{b}^{-1}+P_{b}^{-1})^{-1}=P_{b}-(P_{f}^{-1}+P_{b}^{-1})^{-1}$$
$$(9.61)$$
$$(9.62)$$
$$(9.63)$$
$$(9.64)$$
$$(9.65)$$
$$P=P_{b}(P_{b}^{-1}P_{f}+I)^{-1}+P_{b}-2P_{b}+2(P_{f}^{-1}+P_{b}^{-1})^{-1}\tag{1}$$ $$=(P_{b}^{-1}P_{f}P_{b}^{-1}+P_{b}^{-1})^{-1}-P_{b}+2(P_{f}^{-1}+P_{b}^{-1})^{-1}$$ $$=P_{b}-(P_{f}^{-1}+P_{b}^{-1})^{-1}-P_{b}+2(P_{f}^{-1}+P_{b}^{-1})^{-1}$$ $$=(P_{f}^{-1}+P_{b}^{-1})^{-1}$$

These results form the basis for the fixed-interval smoothing problem. The system model is given as 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$

Suppose we want a smoothed estimate at time index m. First we run the forward Kalman filter normally, using measurements up to and including time m. 

1. Initialize the forward filter as follows: 

$$\hat{\hat{x}}_{f0}^{+}=E(x_{0})$$ $$P_{f0}^{+}=E\left[(x_{0}-\hat{x}_{f0}^{+})(x_{0}-\hat{x}_{f0}^{+})^{T}\right]\tag{9.66}$$

2. For k = 1, - , m, perform the following: 

$$(9.67)$$

At this point we have a forward estimate for xm, along with its covariance. These quantities are obtained using measurements up to and including time m. 

The backward filter needs to run backward in time, starting at the final time index N. Since the forward and backward estimates must be independent, none of the information that was used in the forward filter is allowed to be used in the backward filter. Therefore, *PrN* must be infinite: 

$$(9.68)$$
$$P_{b N}^{-}=\infty$$
PCN = 0O (9.68) 
We are using the minus superscript on *PiN* to indicate the backward covariance at time N before the measurement at time N is processed. (Recall that the filtering is performed backward in time.) So *PbN* will be updated to obtain *Pb+N* after the measurement at time N is processed. Then it will be extrapolated backward in time to obtain *PGN-l,* and so on. 

Now the question arises how to initialize the backward state estimate ?& at the final time k = N. We can solve this problem by introducing the new variable 

$$s_{k}=P_{b k}^{-1}\hat{x}_{b k}$$
$$(9.69)$$
 $s^-_{N}=0$  $B^-_{N}$ means that we cannot $s^-_{N}=0$. 
sk = *Pil?bk* (9.69) 
A minus or plus superscript can be added on all the quantities in the above equation to indicate values before or after the measurement at time k is taken into account. 

Since *PcN* = 00 it follows that s; = 0 (9.70) 
The infinite boundary condition on Pi means that we cannot run the standard Kalman filter backward in time because we have to begin with an infinite covariance. Instead we run the information filter from Section **6.2** backward in time. This can be done by writing the system of Equation (9.65) as 

$$\begin{array}{r c l}{{x_{k-1}}}&{{=}}&{{F_{k-1}^{-1}x_{k}+F_{k-1}^{-1}w_{k-1}}}\\ {{}}&{{=}}&{{F_{k-1}^{-1}x_{k}+w_{b,k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{b k}}}&{{\sim}}&{{(0,F_{k}^{-1}Q_{k}F_{k}^{-T})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$(9.70)$$
$$(9.71)$$

Note that *FL1* should always exist if it comes from a real system, because Fk comes from a matrix exponential that is always invertible (see Sections **1.2** and **1.4).** The backward information filter can be written as follows. 

1. Initialize the filter with *zrN* = 0. 

$$N-1,\cdots,{\mathrm{~per}}$$

2. For k = *N, N* - 1, - a, perform the following: 

$$(9.72)$$

The first form for *Z;k-l* above requires the inversion of Zbfk. Consider the first time step for the backward filter (i.e., at k = *N).* The information matrix Z; is initialized to zero, and then the first time through the above loop we set Z$ = 
Zk + *HFRL'Hk.* If there are fewer measurements than states, *HFRilHk* will always be singular and, therefore, Zbfk will be singular at k = N. Therefore, the first form given above for *Zck-l* will not be computable. In practice we can get around this by initializing ZbN to a small nonzero matrix instead of zero. 

The third form for *ZCk-1* above has its own problems. It does not require the inversion of Z&, but it does require the inversion of *Qk-1.* So the third form of Zb;k-l is not computable unless *Qk-1* is nonsingular. Again, in practice we can get around this by making a small modification to **Qk-1** so that it is numerically nonsingular. 

Since we need to update Sk = *Zbk?bk* instead of *?bk* (because of initialization issues) as defined in Equation **(9.69),** we rewrite the update equations for the state estimate as follows: 

$$\hat{x}^{+}_{bk}=\hat{x}^{-}_{bk}+K_{bk}(y_{k}-H_{k}\hat{x}^{-}_{bk})$$ $$\hat{s}^{+}_{k}={\cal I}^{+}_{bk}\hat{x}^{+}_{bk}\tag{9.73}$$ $$={\cal I}^{+}_{bk}\hat{x}^{-}_{bk}+{\cal I}^{+}_{bk}K_{bk}(y_{k}-H_{k}\hat{x}^{-}_{bk})$$
$$\begin{array}{r c l}{{s_{k}^{+}}}&{{=}}&{{{\mathcal{I}}_{b k}^{-}\hat{x}_{b k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k}\hat{x}_{b k}^{-}+H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}\hat{x}_{b k}^{-})}}\\ {{}}&{{=}}&{{s_{k}^{-}+H_{k}^{T}R_{k}^{-1}y_{k}}}\end{array}$$

Now note from Equation **(6.33)** that we can write Zbfk = Zk + *HTRklHk,* and Kbk = *P&HrR;?* Substituting these expressions into the above equation for skf gives We combine this with Equation **(9.72)** to write the backward information filter as follows. 

$$\begin{array}{r c l}{{s_{N}^{-}}}&{{=}}&{{0}}\\ {{{\mathcal{I}}_{b N}^{-}}}&{{=}}&{{0}}\end{array}$$

1. Initialize the filter as follows: 

$$(9.74)$$
$$\left(\text{9.75}\right)$$. 

2. For k = *N, N* - 1, * . , m + 1, perform the following: 
3. Perform one final time update to obtain the backward estimate of xm: 

$${\cal T}_{bm}=Q_{m}^{-1}-Q_{m}^{-1}F_{m}^{-1}({\cal T}_{b,m+1}^{+}+F_{m}^{-T}Q_{m}^{-1}F_{m}^{-1})^{-1}F_{m}^{-T}Q_{m}^{-1}$$ $$P_{bm}=({\cal T}_{bm})^{-1}$$ $$s_{m}^{-}={\cal T}_{bm}F_{m}^{-1}({\cal T}_{b,m+1}^{+})^{-1}s_{m+1}^{+}$$ $$\hat{\mathbf{x}}_{bm}^{-}=({\cal T}_{bm}^{-})^{-1}s_{m}^{-}\tag{9.77}$$

Now we have the backward estimate f;, and its covariance *PLm.* These quantities are obtained from measurements m + 1, m + 2, a, N. 

After we obtain the backward quantities as outlined above, we combine them with the forward quantities from Equation (9.67) to obtain the final state estimate and covariance: 

$$K_{f}=P_{bm}^{-}(P_{fm}^{+}+P_{bm}^{-})^{-1}$$ $$\hat{x}_{m}=K_{f}\hat{x}_{fm}^{+}+(I-K_{f})\hat{x}_{bm}^{-}$$ $$P_{m}=\left[(P_{fm}^{+})^{-1}+(P_{bm}^{-})^{-1}\right]^{-1}\tag{9.78}$$

We can obtain an alternative equation for P, by manipulating the above equations. 

If we substitute for Kf in the above expression for Pm then we obtain 

$$\hat{x}_{m}=P^{-}_{bm}(P^{+}_{fm}+P^{-}_{bm})^{-1}\hat{x}^{+}_{fm}+\left[I-P^{-}_{bm}(P^{+}_{fm}+P^{-}_{bm})^{-1}\right]\hat{x}^{-}_{bm}\tag{9.79}$$ $$=P^{-}_{bm}(P^{+}_{fm}+P^{-}_{bm})^{-1}\hat{x}^{+}_{fm}+\left[(P^{+}_{fm}+P^{-}_{bm})-P^{-}_{bm}\right](P^{+}_{fm}+P^{-}_{bm})^{-1}\hat{x}^{-}_{bm}$$ $$=P^{-}_{bm}(P^{+}_{fm}+P^{-}_{bm})^{-1}\hat{x}^{+}_{fm}+P^{+}_{fm}(P^{+}_{fm}+P^{-}_{bm})^{-1}\hat{x}^{-}_{bm}$$

Using the matrix inversion lemma on the rightmost inverse in the above equation and performing some other manipulations gives where we have relied on the identity (A + *B)-l* = B-l(AB-l + **I)-1** (see Problem 9.2). The coefficients of *f:m* and **2;'** in the above equation both have a common factor which can be written as follows: 

= P;m - P;mT;m (I + P;mT;m) - 1 PTm  P;m - Pfm(Tf+mP;m + I)-l =  = [P;m(T;mP& +I) - Pf,] (ZTmP& + I)-l  = P,-,(zf+mP& + I)-1  = +  (9.81) 
Therefore, using Equation (9.78), we can write Equation (9.80) as 

$$\begin{array}{r c l}{{\hat{x}_{m}}}&{{=}}&{{P_{m}{\mathcal{I}}_{f m}^{+}\hat{x}_{f m}^{+}+P_{m}{\mathcal{I}}_{b m}^{-}\hat{x}_{b m}^{-}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{P_{m}\left({\mathcal{I}}_{f m}^{+}\hat{x}_{f m}^{+}+{\mathcal{I}}_{b m}^{-}\hat{x}_{b m}^{-}\right)}}\end{array}$$
$$(9.82)$$

Figure 9.9 illustrates how the forward-backward smoother works. 

![22_image_0.png](22_image_0.png)

Figure **9.9** This figure illustrates the concept of the forward-backward smoother. The forward filter is run to obtain a *posteriori* estimates and covariances up to time m. Then the backward filter is run to obtain a *priori* estimates and covariances back to time m (i.e., 
a *priori* from a reversed time perspective). Then the forward and backward estimates and covariances at time m are combined to obtain the find estimate 2m and covariance *Pm.* 

## Example9.3

In this, example we consider the same problem given in Example 9.1. Suppose that we want to estimate the position and velocity of the vehicle at t = 5 seconds. We have measurements every 0.1 seconds for a total of 10 seconds. 

The standard deviation of the measurement noise is 10, and the standard deviation of the acceleration noise is 10. Figure 9.10 shows the trace of the covariance of the estimation of the forward filter as it runs from t = 0 to t = 5, the backward filter as it runs from t = 10 back to t = 5, and the smoothed estimate at t = 5. The forward and backward filters both converge to the same steady-state value, even though the forward filter was initialized to a covariance of 20 for both the position and velocity estimation errors, and the backward filter was initialized to an infinite covariance. The smoothed filter has a covariance of about **7.6,** which shows the dramatic improvement that can be obtained in estimation accuracy when smoothing is used. 

vvv 

![23_image_0.png](23_image_0.png)

Figure 9.10 This shows the trace of the estimation-error covariance for Example **9.3.** 
The forward filter runs from t = 0 to t = 5, the backward filter runs from t = 10 to t = 5, and the trace of the covariance of the smoothed estimate is shown at t = 5. 

## 9.4.2 Rts Smoothing

Several other forms of the fixed-interval smoother have been obtained. One of the most common is the smoother that was presented by Rauch, Tung, and Striebel, usually called the RTS smoother [Rau65]. The RTS smoother is more computai tionally efficient than the smoother presented in the previous section because we do not need to directly compute the backward estimate or covariance in order to get the smoothed estimate and covariance. In order to obtain the RTS smoother, we will first look at the smoothed covariance given in Equation **(9.78)** and obtain an equivalent expression that does not use *Pbm.* Then we will look at the smoothed estimate given in Equation **(9.78),** which uses the gain *Kf,* which depends on *Pbm,* and obtain an equivalent expression that does not use Pbm or *&,m.* 
9.4.2.1 RTS covariance update First consider the smoothed covariance given in Equation **(9.78).** This can be written as 

$$P_{m}=\left[(P_{fm}^{+})^{-1}+(P_{bm}^{-})^{-1}\right]^{-1}\tag{9.83}$$ $$=P_{fm}^{+}-P_{fm}^{+}(P_{fm}^{+}+P_{bm}^{-})^{-1}P_{fm}^{+}$$

where the second expression comes from an application of the matrix inversion lemma to the first expression (see Problem **9.3).** From Equation **(9.72)** we see that 

$$P_{bm}^{-}=F_{m}^{-1}\left[P_{b,m+1}^{+}+Q_{m}\right]F_{m}^{-T}\tag{9.84}$$

Substituting this into the expression (PTm + *PL)-l* gives the following: 

(9.85) 
$$9.85)$$
$$(9.86)$$
$$\begin{array}{l c l}{{{\mathcal I}_{f m}^{+}}}&{{=}}&{{{\mathcal I}_{f m}^{-}+H_{m}^{T}R_{m}^{-1}H_{m}}}\\ {{{\mathcal I}_{b m}^{+}}}&{{=}}&{{{\mathcal I}_{b m}^{-}+H_{m}^{T}R_{m}^{-1}H_{m}}}\end{array}$$
$$\mathcal{I}_{b,m+1}^{+}=\mathcal{I}_{b,m+1}^{-}+\mathcal{I}_{f,m+1}^{+}-\mathcal{I}_{f,m+1}^{-}$$
We can combine these two equations to obtain 

$$(9.87)$$
$$P_{m+1}=\left[{\cal I}_{f,m+1}^{+}+{\cal I}_{b,m+1}^{-}\right]^{-1}\tag{9}$$ $$=\left[{\cal I}_{b,m+1}^{+}+{\cal I}_{f,m+1}^{-}\right]^{-1}$$ $$P_{m+1}^{-1}={\cal I}_{b,m+1}^{+}+{\cal I}_{f,m+1}^{-}$$ $$P_{b,m+1}^{+}=\left[P_{m+1}^{-1}-{\cal I}_{f,m+1}^{-}\right]^{-1}$$

Substituting this into Equation (9.78) gives 

$$(9.88)$$
$$(9.90)$$
$$(9.91)$$

Substituting this into Equation (9.85) gives 

= FTz- m f,m+l (pim+l- ',+I) zim+lFm (9.89) 
where the last equality comes from an application of the matrix inversion lemma. Substituting this expression into Equation (9.83) gives 

$$P_{m}=P_{f m}^{+}-K_{m}(P_{f,m+1}^{-}-P_{m+1})K_{m}^{T}$$
where the smoother gain Km is given as 
$$K_{m}=P_{f m}^{+}F_{m}^{T}{\cal T}_{f,m+1}^{-}$$

The covariance update equation for Pm is not a function of the backward covariance. The smoother covariance Pm can be solved by using only the forward covariance Pfm, which reduces the computational effort (compared to the algorithm presented in Section 9.4.1). 9.4.2.2 RTS state estimate update Next we consider the smoothed estimate 2, given in Equation (9.78). We will find an equivalent expression that does not use Pam or ?bm. In order to do this we Will fist need to establish a few lemmas. 

$$\mathbf{Lemma\ 1}$$
  **Lemma 1**: $$F_{k-1}^{-1}Q_{k-1}F_{k-1}^{-T}=F_{k-1}^{-1}P_{fk}^{-T}F_{k-1}^{-T}-P_{f,k-1}^{+}$$  _Proof: From Equation (9.67) we see that_
$$P_{f k}^{-}=F_{k-1}P_{f,k-1}^{+}F_{k-1}^{T}+Q_{k-1}$$
ph = *Fk-lPLk-lFkT-1+ Qk-1* (9.93) 
$$Q_{k-1}=P_{f k}^{-}-F_{k-1}P_{f,k-1}^{+}F_{k-1}^{T}$$
Rearranging this equation gives 
$$(9.92)$$
$$(9.93)$$
$$(9.94)$$
$$(9.95)$$

Premultiplying both sides by FFI1 and postmultiplying both sides by FF-; gives the desired result. 

QED 

Lemma 2 The a posteriori covariance P& of the backward filter satisfies the equation 
$P_{bk}^{+}=(P_{fk}^{-}+P_{bk}^{+})T_{fk}P_{k}$  _) we obtain_
Proof: From Equation (9.78) we obtain 
I = (I& 
$$\begin{array}{l}{{(\mathcal{I}_{b k}^{+}+\mathcal{I}_{f k}^{-})P_{k}}}\\ {{(I+P_{b k}^{+}\mathcal{I}_{f k}^{-})P_{k}}}\\ {{P_{k}+P_{b k}^{+}\mathcal{I}_{f k}^{-}P_{k}}}\\ {{P_{f k}^{-}\mathcal{I}_{f k}^{-}P_{k}+P_{b k}^{+}\mathcal{I}_{f k}^{-}P_{k}}}\\ {{(P_{f k}^{-}+P_{b k}^{+})\mathcal{I}_{f k}^{-}P_{k}}}\end{array}$$
$$\begin{array}{r l}{I}&{{}=}\\ {P_{b k}^{+}}&{{}=}\end{array}$$
$$\mathbf{\Sigma}=\mathbf{\Sigma}$$
p& = (I + *p&zy,)pk* QED 
Lemma 3 *The covariances of the forward and backward filters satisfy the equation* 

$$P_{f k}^{-}+P_{b k}^{+}=F_{k-1}(P_{f,k-1}^{+}+P_{b,k-1}^{-})F_{k-1}^{T}$$  _Proof: From Equation (9.67) and (9.72) we see that_
$$\begin{array}{l c l}{{P_{f,k-1}^{+}}}&{{=}}&{{F_{k-1}^{-1}P_{f k}^{-}F_{k-1}^{-T}-F_{k-1}Q_{k-1}F_{k-1}^{-T}}}\\ {{P_{b,k-1}^{-}}}&{{=}}&{{F_{k-1}^{-1}P_{b k}^{+}F_{k-1}^{-T}+F_{k-1}^{-1}Q_{k-1}F_{k-1}^{-T}}}\end{array}$$
$$(9.96)$$
$$(9.97)$$
$$(9.98)$$
$$\begin{array}{r c l}{{P_{f,k-1}^{+}+P_{b,k-1}^{-}}}&{{=}}&{{F_{k-1}^{-1}(P_{f k}^{-}+P_{b k}^{+})F_{k-1}^{-T}}}\\ {{}}&{{}}&{{P_{f k}^{-}+P_{b k}^{+}}}&{{=}}&{{F_{k-1}(P_{f,k-1}^{+}+P_{b,k-1}^{-})F_{k-1}^{T}}}\end{array}$$

Adding these two equations and rearranging gives 

$$(9.99)$$
$$\hat{x}_{k}=P_{k}T_{fk}^{+}\hat{x}_{fk}^{-}-P_{k}H_{k}^{T}R_{k}^{-1}H_{k}\hat{x}_{fk}^{-}+P_{k}s_{k}^{+}\tag{9.100}$$

Proof: Fkom Equations (9.69) and (9.82) we have 

$$\begin{array}{r c l}{{\hat{x}_{k}}}&{{=}}&{{P_{k}{\mathcal{I}}_{f k}^{+}\hat{x}_{f k}^{+}+P_{k}{\mathcal{I}}_{b k}^{-}\hat{x}_{b k}^{-}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{P_{k}{\mathcal{I}}_{f k}^{+}\hat{x}_{f k}^{+}+P_{k}s_{k}^{-}}}\end{array}$$
$$s_{k}^{-}=s_{k}^{+}-H_{k}^{T}R_{k}^{-1}y_{k}$$
$$(9.101)$$
$$(9.102)$$

&om Equation (9.76) we see that Substitute this expression for si and the expression for 2ik from Equation (9.67), into Equation (9.101) to obtain 

$$\hat{x}_{k}=P_{k}{\cal I}^{+}_{jk}\hat{x}^{-}_{fk}+P_{k}{\cal I}^{+}_{jk}K_{fk}(y_{k}-H_{k}\hat{x}^{-}_{fk})+P_{k}s^{+}_{k}-P_{k}H^{T}_{k}R^{-1}_{k}y_{k}\tag{9.103}$$

Now substitute Pf+kHrRb' for Kfk [from Equation (9.67'1 in the above equation to obtain 

$$(P_{f,k-1}^{+}+P_{b,k-1}^{-})^{-1}=F_{k-1}^{T}\mathcal{I}_{f k}^{-}(P_{f k}^{-}-P_{k})\mathcal{I}_{f k}^{-}F_{k-1}$$

Lemma 5 

$$(9.105)$$
$$\begin{array}{l c l}{{{\mathcal I}_{f k}^{+}}}&{{=}}&{{{\mathcal I}_{f k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k}}}\\ {{{\mathcal I}_{b k}^{+}}}&{{=}}&{{{\mathcal I}_{b k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k}}}\end{array}$$

Proof: Recall from Equations (6.26) and (9.72) that 

$$(9.106)$$

Combining these two equations gives 

$${\cal I}^{+}_{b\bar{k}}={\cal I}^{-}_{b\bar{k}}+{\cal I}^{+}_{f\bar{k}}-{\cal I}^{-}_{f\bar{k}}\tag{9.107}$$ $$=\left[\left({\cal I}^{-}_{b\bar{k}}+{\cal I}^{+}_{f\bar{k}}\right)^{-1}\right]^{-1}-{\cal I}^{-}_{f\bar{k}}$$ $$=P^{-1}_{\bar{k}}-{\cal I}^{-}_{f\bar{k}}$$ $$P^{+}_{b\bar{k}}=\left({\cal I}_{k}-{\cal I}^{-}_{f\bar{k}}\right)^{-1}$$
$$\begin{array}{r c l}{{F_{k-1}(P_{f,k-1}^{+}+P_{b,k-1}^{-})F_{k-1}^{T}}}&{{=}}&{{P_{f k}^{-}+P_{b k}^{+}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{P_{f k}^{-}+\left({\mathcal{I}}_{k}-{\mathcal{I}}_{f k}^{-}\right)^{-1}}}\end{array}$$

where we have used Equation (9.78) in the above derivation. Substitute this expression for Pbfk into Equation (9.97) to obtain 

$$(9.108)$$

Invert both sides to obtain

2 (Pfk-1 + Po,k )-1F-1 F - 1 1) -1 -1 + Ppk - Fk-1 Pfk + Pjk + Pjk Ijk (Ik - Ijk) Fr (9.109)
Now apply the matrix inversion lemma to the term (Ix - Iz) -1 in the above equation.  This results in

(Pf,k=1 + Pb,k. [2]x + Ijk (-Pjk - Pjk(-Pjk + Pk)-1 Pjk) Ijk | Ijk Fk-1 [Ijk + (-I - (-Pix + Pk)-1 Pjk ) Ijk] IgkFk-1 1 I fr 1 Jk [Ijk - Ijk - (Pjx + Pk) -1] - Ijk Fk -1 Fk-1Ifk (Pjk - Pk)IjkFk-1 (9.110)
QED
With the above lemmas we now have the tools that we need to obtain an alternate expression for the smoothed estimate. Starting with the expression for 8x-1 in Equation (9.76), and substituting the expression for IJ k-1 from Equation (9.72) gives

$$s_{k-1}^{-}$$
Ibk Fk - 1 Pok Sk M Qx21 - Qx21 (Zix + Qx2 ) -1 Qx2 | Fk-1Fx-1P22 I - (It + Q = 1) - Q = 1 ] P  F = 1 Q = 2 ( ( 2 + Q = 2 ) ( Z ] + Q = 1 - Q = 1 - Q = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 3 = 1 ) P = 2 FF-1Qx21 (ISk +Qx21) s F2 = ( + I = Q k - 1 ) - 1 st
$$(9.111)$$

Rearranging this equation gives

$$(I+\mathcal{I}_{b k}^{+}Q_{k-1})F_{k-1}^{-T}s_{k-1}^{-}=s_{k}^{+}$$
$$(9.112)$$

Multiplying out this equation, and premultiplying both sides by FF-1 Pives

$$F_{k-1}^{-1}P_{b k}^{+}F_{k-1}^{-T}s_{k-1}^{-}+F_{k-1}^{-1}Q_{k-1}F_{k-1}^{-T}s_{k-1}^{-}=F_{k-1}^{-1}P_{b k}^{+}s_{k}^{+}$$
$$(9.113)$$

Substituting for **F;ylQk-** *IFF-:* from Equation (9.92) gives 

(9.1 14) 
 $\left[(P^-_{fk}+P^+_{bk})F^{-T}_{k-1}-F_{k-1}P^+_{f,k-1}\right]s^-_{k-1}=(P^-_{fk}+P^+_{bk})\mathcal{I}^-_{fk}P_k s^+_k$  buting for $(P^-_{fk}+P^+_{bk})$ from Equation (0.07) on both sides of this set. 
Substituting in this expression for *Pb+k* from Equation (9.95) gives 

$$(9.115)$$

Substituting for (PG + *PA)* from Equation (9.97) on both sides of this expression gives 

$$\left[F_{k-1}(P^{+}_{f,k-1}+P^{-}_{b,k-1})-F_{k-1}P^{+}_{f,k-1}\right]s^{-}_{k-1}=F_{k-1}(P^{+}_{f,k-1}+P^{-}_{b,k-1})F^{T}_{k-1}T^{-}_{f,k}P_{k}s^{+}_{k}\tag{9.116}$$  Premultiplying both sides by $(P^{+}_{f,k-1}+P^{-}_{b,k-1})^{-1}F^{-1}_{k-1}$ gives
$$\left[I-(P_{f,k-1}^{+}+P_{b,k-1}^{-})^{-1}P_{f,k-1}^{+}\right]s_{k-1}^{-}=F_{k-1}^{T}T_{f k}^{-}P_{k}s_{k}^{+}$$  Substituting Equation (9.105) for $(P_{f,k-1}^{+}+P_{b,k-1}^{-})^{-1}$ gives
$$(9.117)$$
$$s_{k-1}^{-}-F_{k-1}^{T}\mathcal{I}_{f k}^{-}(P_{f k}^{-}-P_{k})\mathcal{I}_{f k}^{-}F_{k-1}P_{f,k-1}^{+}s_{k-1}^{-}=F_{k-1}^{T}\mathcal{I}_{f k}^{-}P_{k}s_{k}^{+}$$  Now from Equation (9.105) we see that 
$$-(P_{f,k-1}^{+}+P_{b,k-1}^{-})^{-1}F_{k-1}^{-1}\hat{x}_{f k}^{-}=F_{k-1}^{T}\mathcal{I}_{f k}^{-}(P_{k}-P_{f k}^{-})\mathcal{I}_{f k}^{-}\hat{x}_{f k}^{-}$$

(9.118) 

$$(9.119)$$

So we can add the two sides of this equation to the two sides of Equation (9.118) 
to get 

(9.120) 
Now use Equation (9.100) to substitute for *PkS$* in the above equation and obtain 

(9.121) 
Rearrange this equation to obtain 

(9.122) 
From Equation (9.106) we see that ZTk -TFk = *HzRk'Hk.* Also note that part of the coefficient of **27k** on the left side of the above equation can be expressed as 

$$(P^{+}_{f,k-1}+P^{-}_{b,k-1})^{-1}F^{-1}_{k-1}={\cal T}^{-}_{b,k-1}(I+P^{+}_{f,k-1}{\cal T}^{-}_{b,k-1})^{-1}F^{-1}_{k-1}\tag{9.123}$$

From Equation (9.67) we see that FF?12& = *2ik-1,* Therefore Equation (9.122) 
can be written as 

(9.124) 
Now substitute for pk from Equation (9.90) and use Equation (9.91) in the above equation to obtain 

(9.125) 
Premultiplyhg both sides by *Plk-1* gives 

(9.126) 
Now use Equation (9.91) to notice that the coefficient of SF-^ on the left side of the above equation can be written as 

(9.127) 
Using Equation (9.90) to substitute for *&pk+lKz* allows us to write the above expression as 

(9.128) 
Since this is the coefficient of *s;-~* in Equation (9.126), we can write that equation 
(9.129) 
as Now from Equations (9.78) and (9.82) we see that 

$\hat{x}_{k}$ = $({\cal T}_{jk}^{+}+{\cal T}_{bb}^{-})^{-1}{\cal T}_{jk}^{+}\hat{x}_{jk}^{+}+P_{k}{\cal T}_{bbk}^{-}\hat{x}_{bbk}^{-}$  = $(I+P_{jk}^{+}{\cal T}_{bbk}^{-})^{-1}\hat{x}_{jk}^{+}+P_{k}s_{k}^{-}$ (9.130)  at
From this we *see* that 

(9.131) 
Rewriting the above equation with the time subscripts (k-1) and then substituting for the left side of Equation (9.129) gives

$${\hat{x}}_{k-1}-{\hat{x}}_{f,k-1}^{+}=K_{k-1}({\hat{x}}_{k}-{\hat{x}}_{f k}^{-})$$
$$(9.132)$$

from which we can write

$\hat{x}_{k}=\hat{x}_{fk}^{+}+K_{k}(\hat{x}_{k+1}-\hat{x}_{f,k+1}^{-})$ (9.133)
This gives the smoothed estimate ik without needing to explicitly calculate the backward estimate. The RTS smoother is implemented by first running the standard Kalman filter of Equation (9.67) forward in time to the final time, and then implementing Equations (9.90), (9.91), and (9.133) backward in time. The RTS
smoother can be summarized as follows.

## The Rts Smoother

1. The system model is given as follows:

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$(9.134)$$

2. Initialize the forward filter as follows:

$$\hat{x}_{f0}=E(x_{0})$$ $$P_{f0}^{+}=E\left[(x_{0}-\hat{x}_{f0})(x_{0}-\hat{x}_{f0})^{T}\right]\tag{9.135}$$

3. For k = 1, ... , N (where N is the final time), execute the standard forward Kalman filter:

Pik Kik P FK Hk (HkPjx H2 + Rk)-1 P H H R R Fk-12 k-1 + Gk-1Uk-1 x Tk ll â Fk + Kfk (yk - Hkâfk) x fk ll Pik (I - K fkHk)P Fk (I - K fkHk)" + K fk Rk K Fk ll - I (PFK)-1 + H2 RT Hk (I - K Jk Hk)Pfk
$$(9.136)$$
4. Initialize the RTS smoother as follows:

$$\begin{array}{r c l}{{\hat{x}_{N}}}&{{=}}&{{\hat{x}_{f N}^{+}}}\\ {{P_{N}}}&{{=}}&{{P_{f N}^{+}}}\end{array}$$

$$(9.137)$$
$$\begin{array}{r c l}{{{\mathcal T}_{f,k+1}^{-}}}&{{=}}&{{\left(P_{f,k+1}^{-}\right)^{-1}}}\\ {{}}&{{}}&{{K_{k}}}&{{=}}&{{P_{f k}^{+}F_{k}^{T}{\mathcal T}_{f,k+1}}}\\ {{}}&{{}}&{{P_{k}}}&{{=}}&{{P_{f k}^{+}-K_{k}(P_{f,k+1}^{-}-P_{k+1})K_{k}^{T}}}\\ {{}}&{{}}&{{\hat{x}_{k}}}&{{=}}&{{\hat{x}_{f k}^{+}+K_{k}(\hat{x}_{k+1}-\hat{x}_{f,k+1}^{-})}}\end{array}$$

5. For k = N - 1, - . -, 1,0, execute the following RTS smoother equations: 

## 9.5 Summary

In this chapter we derived the optimal smoothing filters. These filters, sometimes called retrodiction filters [BarOl] , include the following variants. 

$$(9.138)$$

2J,k = *E(sjlyl,*..,yk-l) (k L* j) is the output of the fixed-point smoother. 

In this filter we find the estimate of the state at the fixed time j when measurements continue to arrive at the filter at times greater than j. The time index j is fixed while k continues to increase as we obtain more measurements. 

?k-N,k = *E(~k-NIYl,"*,Yk)* for a fixed N is the Output of the fixed-lag smoother. In this filter we find the estimate of the state at each time k while using measurements up to and including time (k + *N).* The time index k varies while N remains fixed. 

0 ik,N = *E(zkly1,* *. ., *y~)* for a fixed N is the output of the fixed-interval smoother. In this filter we find the estimate of the state at each time k while using measurements up to and including time N. The time index k varies while the total number of measurements N is fixed. The two formulas we derived for this type of smoothing included the forward-backward smoother and the RTS smoother. 

Just as steady-state filters can be used for standard filtering, we can also derive steady-state smoothers to save computational effort [Ge174]. An early survey of smoothing algorithms is given in [Med73]. 

## Problems Written Exercises

9.1 Prove or disprove the following conjecture: The trace of the inverse of a matrix is equal to the inverse of the trace of the matrix. 

9.2 Show that (A + *B)-l= B-l(AB-l+ I)-1.* 
9.3 Derive Equation (9.83). 

9.4 Consider a scalar system with F = 1, H = 1, and R = 2Q. 

a) What is the steady-state value of the a *priori* estimation-error covariance PF? 

b) Suppose that after the Kalman filter has reached steady state, the fixedpoint smoother begins to operate. Find a closed-form solution to the covariance of the smoothed estimate l& as a function of the time index k. 

What is the limiting value of as k ---f m? 

9.5 Repeat Problem **9.4** for the case R = **l2Q.** What is the percent improvement in the estimation-error covariance due to smoothing? Explain why the percent improvement due to smoothing for this case differs in the way that it does from the results of Problem **9.4.** 
Consider a scalar system with F = 1, H = 1, and R = **2Q.** 
9.6 Suppose that the fixed-lag smoother for this system is in steady state so that P;+l = P;, Lk+l,% = **Lk,z,** *Pi$1* = Pila, and Pt$l = Pk' , for i = **l,..., N+1.** Find closed-form expressions for P;, *Lk,z,* P;", and Pi" as functions of i. What is the limit as 02 i --+ m of *Lk,z,* pis2, and pi!'? 

9.7 Suppose you have a fixed-lag smoother as shown in Equation **(9.43)** that is in steady state. How do the eigenvalues of the fixed-lag smoother relate to the eigenvalues of the standard Kalman filter? What do you conclude about the stability of the fixed-lag smoother? 

9.8 Solve Equation **(9.10)** for (yk - *HIE!?;)* [assuming that *p(Lk)* = T, where T 
is the number of measurements in the system]. Substitute the resulting expression for (Yk - *Hk!?i)* in the fixed-lag smoother equation for *!?k+l-$,k* to show that the smoothed state estimate can be driven by the state estimates without any input from the measurements [And79]. 

9.9 Suppose that bj and &, are unbiased estimates of x, and !? = Kjbj + *K&.* 
Show that if b is an unbiased estimate of x, then we must have Kj + Kb = I. 9.10 Consider a scalar system with F = 1, H = 1, and R = **2Q.** Use the forwardbackward smoother of Section **9.4.1** to find the steady-state value of the covariance of the smoothed state estimate. 

9.11 Consider a scalar system with F = 1, H = 1, and R = **2Q.** Use the RTS 
smoother of Section **9.4.2** to find the steady-state value of the covariance of the smoothed state estimate. 

9.12 Consider a scalar system with F = 1, H = 1, and R = **2Q.** Suppose that the forward filter has reached steady state. Use the RTS smoother of Section **9.4.2** 
to find the covariance of the smoothed state estimate for k = *N, N* - **1, N** - 2, N - 3, and N - 4. At what point does the covariance of the smoothed state estimate get within 1% of its steady-state value? 

9.13 Repeat Problem **9.12** for R = **12Q.** How do you intuitively explain the quicker convergence of Pk to steady state? 

9.14 Use the RTS smoother equations to show that constant states are not smoothable. That is, if F = I and Q = 0, then Pk = *PIN* for all k. 

## Computer Exercises

$$\left[\begin{array}{c}{{\dot{x}_{1}}}\\ {{\dot{x}_{2}}}\end{array}\right]=\left[\begin{array}{c c}{{0}}&{{1}}\\ {{-\omega^{2}}}&{{-2\zeta\omega}}\end{array}\right]\left[\begin{array}{c}{{x_{1}}}\\ {{x_{2}}}\end{array}\right]+\left[\begin{array}{c}{{0}}\\ {{1}}\end{array}\right]w(t)$$

9.15 Consider the second-order system where w = 6 rad/s is the natural frequency of the system, and c = 0.16 is the damping ratio. The input w(t) is continuous-time white noise with a variance of 0.01. Measurements of the first state are taken every 0.5 s: 

$$y(t_{k})={\left[\begin{array}{l l}{1}&{0}\end{array}\right]}\,x(t_{k})+v(t_{k})$$

where *'~(tk)* is discrete-time white noise with a variance of estimate, and covariance are The initial state, 

$$\begin{array}{r c l}{{x(0)}}&{{=}}&{{\left[\begin{array}{c}{{1}}\\ {{1}}\end{array}\right]}}\\ {{\hat{x}(0)}}&{{=}}&{{x(0)}}\\ {{P(0)}}&{{=}}&{{\left[\begin{array}{c c}{{10^{-5}}}&{{0}}\\ {{0}}&{{10^{-2}}}\end{array}\right]}}\end{array}$$

a) Discretize the system equation. 

b) Implement the discretetime Kalman filter and the RTS smoother for 10 s 
(20 time steps). Plot the variance of the estimation error of the first state for the forward filter and for the RTS smoother on a single plot. Do the same for the second state. Why is the second state more smoothable than the **first** state? 

9.16 Repeat Problem 9.15 with the continuous-time process noise *w(t)* having a variance of 1. How does this change the smoothability of the states? 

9.17 Design a fixed-interval smoother for the system described in Problem 5.11 to estimate the state at each time on the basis of measurements at all 10 time steps. 

a) Plot the a *posteriori* covariance of the forward state estimate and the covariance of the smoothed state estimate as a function of time for both states. 

b) What are the percent improvements in the estimation-error variances due to smoothing for the two states at the initial time? Why is there so much more improvement for one state than for the other state? 

c) Simulate the system and smoother a hundred times or so, each simulation with a different noise history. On the basis of your simulations, derive a numerical estimate of the smoother estimation-error variances of the two states at the initial time. How do your numerical variances compare with the theoretical variances obtained in part (b)? 