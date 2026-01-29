---
type: chapter
chapter: 6
title: Alternate Kalman filter formulations
---
# Chapter 6 Alternate Kalman Filter Formulations

Our experiences with estimation and control applications engineers, however, indicates that they generally prefer the seemingly simpler Kalman filter algorithms for computer implementation and they dismiss reported instances of numerical failure. 

-Gerald Bierman and Catherine Thornton [Bie77a] 
In this chapter, we will look at some alternate ways of writing the Kalman filter equations. There are a number of mathematically equivalent ways of writing the Kalman filter equations. This can be confusing. You might read two different papers or books that present the Kalman filter equations, and the equations might look completely different. You may not know if one of the equations has a typographical error, or if they are mathematically equivalent. So you try to prove the equivalence of the two sets of equations **only** to arrive at a mathematical dead end, because it is not always easy to prove the equivalence of two sets of equations. This chapter derives some Kalman filter formulations that are different than (but mathematically equivalent to) the equations we derived in Chapter 5. This chapter also illustrates their advantages and disadvantages. 

The first alternate formulation that we discuss is called the sequential Kalman filter, derived in Section 6.1. Sequential Kalman filtering allows for the implementation of the Kalman filter without matrix inversion. This can be a great benefit, especially in an embedded system that does not have matrix libraries, but it only makes sense if certain conditions are satisfied. The second formulation that we discuss is called information filtering, derived in Section *6.2.* Information filtering propagates the inverse of the covariance matrix (i.e., *P-l)* instead of P, and is computationally cheaper than Kalman filtering under certain conditions. The third formulation that we discuss is called square root filtering, derived in Section *6.3.* 
Square root filtering effectively increases the precision of the Kalman filter, which can help prevent divergence and instability. However, this is at the cost of increased computational effort. The final formulation that we discuss is called U-D filtering, derived in Section *6.4.* This is another way to implement square root filtering, which helps to prevent numerical difficulties in the implementation of the Kalman filter. 

## 6.1 Sequential Kalman Filtering

$$y_{k}=H_{k}x_{k}+v_{k}$$ $$K_{k}=P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$$ $$P_{k}^{+}=(I-K_{k}H_{k})P_{k}^{-}\tag{6.1}$$

In this section, we derive the sequential Kalman filter. This is a way of implementing the Kalman filter without matrix inversion. This can be a great advantage, especially in an embedded system that may not have matrix routines. However, the use of sequential Kalman filtering only makes sense if certain conditions are satisfied, which we will discuss in this section. 

Recall the Kalman filter measurement update formulas from Equation *(5.16):* 
The computation of Kk requires the inversion of an T x T matrix, where T is the number of measurements. This is depicted in Figure *6.1.* 

![1_image_0.png](1_image_0.png)

Figure **6.1** T x T matrix inversion, where T is the number of measurements. 

The measurement-update equation of the standard Kalman filter requires an 
Suppose that instead of measuring Yk at time k, we obtain T separate measurements at time k. That is, we first measure *Yk(l),* then *Yk(2),* . . ., and finally Yk (.). 

We will use the shorthand notation **Yik** for the ith element of the measurement vector *yk.* Assume for now that *RI,* (the covariance of measurement *Yk)* is diagonal; 

$$({\mathfrak{h}}.2)$$
that is, Rk is given as 
$R_{k}=\left[\begin{array}{cccc}R_{1k}&\cdots&0\\ \vdots&\ddots&\vdots\\ 0&\cdots&R_{rk}\end{array}\right]$  $R_{k}=\left[\begin{array}{cccc}R_{1k}&\cdots&0\\ \vdots&\ddots&\vdots\\ 0&\cdots&R_{rk}\end{array}\right]$  $R_{k}=\left[\begin{array}{cccc}R_{1k}&\cdots&0\\ \vdots&\ddots&\vdots\\ 0&\cdots&R_{rk}\end{array}\right]$  \(R_{k}=\left[\begin{array}{cccc}R_{1k}&\cdots&0\\ \vdots&\ddots&\vdots\\ 0&\cdots&R_{rk}\end{array}\right]
$$\begin{array}{r c l}{{y_{i k}}}&{{=}}&{{H_{i k}x_{k}+v_{i k}}}\\ {{v_{i k}}}&{{\sim}}&{{(0,R_{i k})}}\end{array}$$
$$({\mathfrak{h}}.{\mathfrak{3}})$$

We will also use the notation that **Hik** is the ith row of *Hk,* and **vik** is the ith element of *Vk.* Then we obtain So instead of processing the measurements at time k as a vector, we will implement the Kalman filter measurement-update equation one measurement at a time. 

We use the notation that **Kik** is the Kalman gain that is used to process the ith measurement at time *k, i&* is the optimal estimate after the ith measurement has been processed at time k, and P$ is the estimation-error covariance after the ith measurement at time k has been processed. We can see from these definitions that 

$$\begin{array}{lcl}\hat{x}_{0k}^{+}&=&\hat{x}_{k}^{-}\\ P_{0k}^{+}&=&P_{k}^{-}\end{array}\tag{6.4}$$

That is, *3$k* is the estimate after zero measurements have been processed, so it is equal to the a priori estimate. Similarly, P& is the estimation-error covariance after zero measurements have been processed, so it is equal to the a priori estimationerror covariance. The gain **Kik** and covariance PA are obtained from the normal Kalman filter measurement-update equations, with the understanding that they apply to the scalar measurement *yik.* For i = 1,. - . , r we have 

$$K_{ik}=P^{+}_{t-1,k}H^{T}_{ik}(H_{ik}P^{+}_{t-1,k}H^{T}_{ik}+R_{ik})^{-1}$$ $$\hat{x}^{+}_{ik}=\hat{x}^{+}_{t-1,k}+K_{ik}(y_{ik}-H_{ik}\hat{x}^{+}_{i-1,k})$$ $$P^{+}_{ik}=(I-K_{ik}H_{ik})P^{+}_{i-1,k}\tag{6.5}$$

After all r measurements are processed, we set 2; = *i?&,* and Pz = *PA,* and we have our a posteriori estimate and error covariance at time k. The sequential Kalman filter does not require any matrix inversions because all of the expressions in Equation (6.5) are scalar operations. This process is depicted in Figure **6.2.** The sequential Kalman filter can be summarized as follows. 

## The Sequential Kalman Filter

1. The system and measurement equations are given as 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$

where Wk and Vk are uncorrelated white noise sequences. The measurement covariance Rk is a diagonal matrix given as 

$$({\mathfrak{h}}.{\mathfrak{h}})$$
$$R_{k}=\mathrm{diag}(R_{1k},\cdots,R_{\tau k})$$
$$({\mathfrak{h}},7)$$
Rk = diag(Rlk, * * * , *Rrk)* (6.7) 
1 measurement 

![3_image_0.png](3_image_0.png)

(6.8)  $$\begin{array}{l}\mbox{\rm(6.8)}\end{array}$$

![3_image_1.png](3_image_1.png)

![3_image_3.png](3_image_3.png)

k time k-1 

![3_image_2.png](3_image_2.png)

Figure **6.2** The measurement update equation of the sequential Kalman filter requires P scalar divisions (where T is the number of measurements) because the measurements at each time step are processed sequentially. This is in contrast to the standard Kalman filter processing that is depicted in Figure 6.1. 

$$\begin{array}{r c l}{{\hat{x}_{0}^{+}}}&{{=}}&{{E(x_{0})}}\\ {{P_{0}^{+}}}&{{=}}&{{E[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}]}}\end{array}$$

2. The filter is initialized as 3. At each time step k, the time-update equations are given as 

$$P_{k}^{-}=F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}$$ $$\hat{\bf z}_{k}^{-}=F_{k-1}\hat{\bf z}_{k-1}^{+}+G_{k-1}u_{k-1}\tag{6.9}$$

This is the same as the standard Kalman filter. 

4. At each time step k, the measurement-update equations are given as follows. 

(a) Initialize the a *posteriori* estimate and covariance as 

$$\begin{array}{lcl}\hat{x}_{0k}^{+}&=&\hat{x}_{k}^{-}\\ P_{0k}^{+}&=&P_{k}^{-}\end{array}\tag{6.10}$$

$$\begin{array}{r l}{K_{i k}}&{{}=}\\ {}&{}&{}\\ {}&{}&{}\\ {\hat{x}_{i k}^{+}}&{{}=}\\ {P_{i k}^{+}}&{{}=}\end{array}$$

These are the a *posteriori* estimate and covariance at time k after zero measurements have been processed; that is, they are equal to the a *priori* estimate and covariance. 

, T (where T is the number of measurements), perform the following: 
(b) For i = 1,. 

$$(6.11)$$
$$({\mathfrak{h}}.12)$$
$$\begin{array}{r l}{={}}&{{}\left[(P_{i-1,k}^{+})^{-1}+H_{i k}^{T}H_{i k}/R_{i k}\right]^{-1}}\\ {={}}&{{}(I-K_{i k}H_{i k})P_{i-1,k}^{+}}\end{array}$$

(c) Assign the a *posteriori* estimate and covariance as 

$$\begin{array}{r c l}{{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{r k}^{+}}}\\ {{P_{k}^{+}}}&{{=}}&{{P_{r k}^{+}}}\end{array}$$

The development above assumes that the measurement-noise covariance Rk is diagonal. What if Rk is not diagonal? Suppose that Rk = R is not diagonal, but it is a constant matrix. We perform a Jordan form decomposition of R by finding a matrix S such that 

$$R=S{\hat{R}}S^{-1}$$

R is a diagonal matrix containing the eigenvalues of R, and S is an orthogonal matrix (i.e., S-l = p) containing the eigenvectors of R. This decomposition is always possible if R is symmetric positive definite, as discussed in most linear systems books [Bay99, Che99, KaiOO]. Now define a new measurement **fik** as 

$$(6.13)$$
$$\hat{y}_{k}=S^{-1}y_{k}\tag{6.14}$$ $$=S^{-1}(H_{k}x_{k}+v_{k})$$ $$=\hat{H}_{k}x_{k}+\hat{v}_{k}$$
$$\begin{array}{l}=\ E(S^{-1}v_{k}v_{k}^{T}S^{-T})\\ =\ E(S^{-1}v_{k}v_{k}^{T}S)\\ =\ S^{-1}E(v_{k}v_{k}^{T})S\\ =\ S^{-1}RS\\ =\ \hat{R}\end{array}\tag{6.15}$$
$$E({\tilde{v}}_{k}{\tilde{v}}_{k}^{T})$$

where **fik** and *'uk* are defined by the above equation. The covariance of *'6k* can be obtained as So we have introduced a normalized measurement **fik** that **has** a diagonal noise covariance. Now we can implement the sequential Kalman filter equations, except that we use the measurement *fik* instead of *Yk,* the measurement matrix *fik* instead of *Hk,* and the measurement noise covariance R. 

Note that this procedure would not make sense if R were timevarying, because in that case we would have to perform a Jordan form decomposition at each step of the Kalman filter. That would be a lot of computational effort in order to avoid a matrix inversion. However, if R is constant and it is known before the implementation of the Kalman filter, then we can perform the Jordan form decomposition offline and use the sequential Kalman filter to our advantage. 

In summary, it only makes sense to use the sequential Kalman filter if one of the following two conditions holds: 
1. The measurement noise covariance Rk is diagonal 2. The measurement noise covariance R is a constant. 

Finally, note that the term sequential filtering is sometimes used synonymously with the Kalman filter. That is, sequential is often used as a synonym for recursive [Buc68, Chapter 131, [Bro96]. This can cause some confusion in terminology. 

However, sequential filtering is usually used in the literature as we use it in this section; that is, sequential filtering is a filtering method that processes measurements one at a time (rather than processing the measurements as a whole vector). Some times, the standard Kalman filter is called the batch Kalman filter to distinguish it from the sequential Kalman filter. 

The change Xk from one week to the next of an American football team's ranking is related to the team's performance against that week's opponent. The expected relationships between various normalized game measures y& and the team's ranking change at the kth week are given as 

$$y_{1k}=x_{k}+v_{1k}=\mbox{point differential}$$ $$y_{2k}=\frac{1}{5}x_{k}+v_{2k}=\mbox{turnover differential}$$ $$y_{3k}=\frac{1}{50}x_{k}+v_{3k}=\mbox{yardage differential}\tag{6.16}$$

where *Wlk* N (0,2), *W2k* N (0, l), and V3k N *(0,50).* Before the first game of the season is played, it is expected that the team ranking will increase by one due to certain players having returned from injuries. The variance of this a *priori* estimate is 4. Uncertainty in ownership conditions is expected to decrease the team's ranking by 5% each week, with a variance of 2. The system can therefore be modeled as 

xk+l = 0.95~k+wk 
 $0.95x_k+w_k\\ \left[\begin{array}{cc}1&1/5&1/50\end{array}\right]^T x_k+v_k\\ (0,Q)\ \ \ \ Q=2\\ (0,R)\ \ \ \ R=\mathrm{diag}(2,1,50)\\ 1\\ 4\end{array}$  . 
wk (O,Q) Q=2 
Po+ = 4 (6.17) 
$$\begin{array}{r l}{x_{k+1}}&{{}=}\\ {y_{k}}&{{}=}\\ {w_{k}}&{{}\sim}\\ {v_{k}}&{{}\sim}\\ {\hat{x}_{0}^{+}}&{{}=}\\ {P_{0}^{+}}&{{}=}\end{array}$$
Suppose that the team plays its first game and wins by *six* points, gains three more turnovers than its opponent, and is outgained by *100* yards. That is, y1 = [ 6 3 -100 3'. 

ranking as follows: 
The standard Kalman filter adjusts the team's 

$$(6.17)$$
FP$FT + Q  5.61  0.952;  0.95  [ 0.6961 0.2785 0.0006 ]  PpP(HPTHT + R)-1  2T + Kl(y1- H?i.,) 
$$=5.1922$$ $$P_{1}^{+}=(I-K_{1}H)P_{1}^{-}\tag{6.18}$$ $$=1.3923$$

The K1 calculation requires the inversion of a 3 x 3 matrix. On the other hand, the sequential Kalman filter could be used to update the estimated team ranking as follows: 

$$\begin{array}{r c l}{{P_{1}^{-}}}&{{=}}&{{F P_{0}^{+}F^{T}+Q}}\\ {{}}&{{=}}&{{5.61}}\\ {{\hat{x}_{1}^{-}}}&{{=}}&{{0.95\hat{x}_{0}^{+}}}\\ {{}}&{{=}}&{{0.95}}\\ {{\hat{x}_{01}^{+}}}&{{=}}&{{\hat{x}_{1}^{-}}}\\ {{P_{01}^{+}}}&{{=}}&{{P_{1}^{-}}}\end{array}$$
$$(6.19)$$

The first measurement is processed as follows: 

$$\begin{array}{l}{{P_{01}^{+}H_{1}^{T}(H_{1}P_{01}^{+}H_{1}^{T}+R_{11})^{-1}}}\\ {{0.7372}}\\ {{\hat{x}_{01}^{+}+K_{11}(y_{11}-H_{1}\hat{x}_{01}^{+})}}\\ {{4.6728}}\\ {{(I-K_{11}H_{1})P_{01}^{+}}}\\ {{1.4744}}\end{array}$$
$$\begin{array}{r l}{K_{11}}&{{}=}\\ {}&{{}=}\end{array}$$
$\begin{array}{cc}\hat{x}_{11}^{+}&=\\ &=\\ &=\end{array}$  4. 
$$\begin{array}{r l}{P_{11}^{+}}&{{}=}\\ {}&{{}=}\end{array}$$
p;: = *(I-K11HdP&* 
$P_{11}^{+}H_{2}^{T}(H_{2}P_{11}^{+}H_{2}^{T}+R_{22})^{-1}$  0.2785  $\hat{x}_{11}^{+}+K_{21}(y_{21}-H_{2}\hat{x}_{11}^{+})$  5.2479  $(I-K_{21}H_{2})P_{11}^{+}$  1.3923
$\begin{array}{ccc}K_{21}&=&\\ &=&\\ \grave{x}_{21}^{+}&=&\\ &=&\\ \vdots&\end{array}$  4. 

$$(6.20)$$

The second measurement is processed as follows: 

$$(6.21)$$

$$(6.22)$$

The third measurement is processed as follows: 

$$\begin{array}{r l}{{}}&{{}}\\ {P_{21}^{+}}&{{}=}\\ {}&{{}}\\ {=}\end{array}$$
$P_{21}^{+}H_3^T(H_3P_{21}^{+}H_3^T+R_{33})^{-1}$  0.0006  $\hat{x}_{21}^{+}+K_{31}(y_{33}-H_3\hat{x}_{21}^{+})$  5.1922  $(I-K_{31}H_3)P_{21}^{+}$  1.3923
$$\begin{array}{r l}{K_{31}}&{{}=}\\ {}&{{}=}\end{array}$$
$$\begin{array}{r l}{{}}&{{}=}\\ {\hat{x}_{31}^{+}}&{{}=}\\ {}&{{}=}\\ {P_{31}^{+}}&{{}=}\\ {}&{{}=}\end{array}$$
PA = (I - *K31H3)PL* 
The sequential Kalman filter requires three loops through the measurement update equations, but no matrix inversions are required. 

vvv 

## 6.2 I N **Fo R Mat I** 0 N **F I Lt E R** I N G

In this section, we discuss information filtering. This is an implementation of the Kalman filter that propagates the inverse of P rather than propagating P; that is, information filtering propagates the information matrix of the system. Recall that 

$$P=E[(x-{\hat{x}})(x-{\hat{x}})^{T}]$$
$$(6.23)$$
$$(6.24)$$
P = *E[(z* - ?)(z -?)TI **(6.23)** 
That is, P represents the uncertainty in the state estimate. If P is "large" then we have a lot of uncertainty in our state estimate. In the limit as P t 0 we have perfect knowledge of x, and as P t 00 we have zero knowledge of x. The information matrix is defined as Z = *p-1* **(6.24)** 
That is, Z represents the certainty in the state estimate. If Z is "large" then we have a lot of confidence in our state estimate. In the limit as Z + 0 we have zero knowledge of x, and as Z t 00 we have perfect knowledge of x. 

Recall from Equation **(5.19)** that the measurement update equation for P can be written as 
(P;)-1 = (P;)-' + *HrRk'Hk* **(6.25)** 
Substituting the definition of Z into this equation gives 

$$(P_{k}^{+})^{-1}=(P_{k}^{-})^{-1}+H_{k}^{T}R_{k}^{-1}H_{k}$$
$$(6,25)$$
$$\mathcal{I}_{k}^{+}=\mathcal{I}_{k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k}$$
$$(6.26)^{\frac{1}{2}}$$
$$(6.27)$$
1: = + *HrRk'Hk* **(6.26)** 
This gives the measurement-update equation for the information matrix. Recall from Equation **(5.19)** the time-update equation for P: 

$$P_{k}^{-}=F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}$$
$$\mathcal{I}_{k}^{-}=[F_{k-1}(\mathcal{I}_{k-1}^{+})^{-1}F_{k-1}^{T}+Q_{k-1}]^{-1}$$
$$(6.28)$$

$$(6.29)$$

This implies that 1; = [Fk-i(ZL-l)-lFr-l + *Qk-11-l* **(6.28)** 
Now we can use the matrix inversion lemma from Section **1.1.2,** which we restate 
here: 
$$(A+B D^{-1}C)^{-1}=A^{-1}-A^{-1}B(D+C A^{-1}B)^{-1}C A^{-1}$$
If we make the identifications A = Qk-1, B = 9-1, C = FkT_l, *and* D = Zk+-l, 
then we can apply the matrix inversion lemma to Equation **(6.28)** to obtain 
$$\mathcal{I}_{k}^{-}=Q_{k-1}^{-1}-Q_{k-1}^{-1}F_{k-1}(\mathcal{I}_{k-1}^{+}+F_{k-1}^{T}Q_{k-1}^{-1}F_{k-1})^{-1}F_{k-1}^{T}Q_{k-1}^{-1}$$
This gives the timeupdate equation for the information matrix. The information filter can be summarized as follows. 

## The Information Filter

1. The dynamic system is given by the following equations: 

$$(6.30)$$
$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\end{array}$$
$$(6.31)$$
$$\begin{array}{r c l}{{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\\ {{E(w_{k}w_{j}^{T})}}&{{=}}&{{Q_{k}\delta_{k-j}}}\\ {{E(v_{k}v_{j}^{T})}}&{{=}}&{{R_{k}\delta_{k-j}}}\\ {{E(w_{k}v_{k}^{T})}}&{{=}}&{{0}}\end{array}$$
$$\hat{x}_{0}^{+}=E(x_{0})$$ $$\hat{x}_{0}^{+}=\left\{E[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}]\right\}^{-1}\tag{6.32}$$

2. The Kalman filter is initialized as follows: 

$$=Q_{k-1}^{-1}-Q_{k-1}^{-1}F_{k-1}({\cal I}_{k-1}^{+}+F_{k-1}^{T}Q_{k-1}^{-1}F_{k-1})^{-1}F_{k-1}^{T}Q_{k-1}^{-1}$$ $$={\cal I}_{k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k}$$ $$=({\cal I}_{k}^{+})^{-1}H_{k}^{T}R_{k}^{-1}$$ $$=F_{k-1}\hat{x}_{k-1}^{+}+G_{k-1}u_{k-1}$$ $$=\hat{x}_{k}^{-}+K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})\tag{6}$$
$$\begin{array}{c}{{\mathcal{I}_{k}^{-}}}\\ {{\mathcal{I}_{k}^{+}}}\\ {{K_{k}}}\\ {{\hat{x}_{k}^{-}}}\\ {{\hat{x}_{k}^{+}}}\end{array}$$

3. The information filter is given by the following equations, which are computed for each time step k = **1,2,** a: 
The standard Kalman filter equations require the inversion of an T x T matrix, where r is the number of measurements. The information filter equations require at least a couple of n x n matrix inversions, where n is the number of states. Therefore, if T >> n (i.e., we have significantly more measurements than states) it may be computationally more efficient to use the information filter. It could be argued that since the Kalman gain is given as 

$$(6.33)$$
$$(6.34)$$
$$K_{k}=P_{k}^{+}H_{k}^{T}R_{k}^{-1}$$

we have to perform and T x T matrix inversion on Rk anyway, whether we use the standard Kalman filter or the information filter. But if Rk is constant, then we could invert it as part of the initialization process, so the Kalman gain equation may not require this T x T matrix inversion after all. The same thinking also applies to the inversion of *Qk-1.* 
If the initial uncertainty is infinite, we cannot numerically set **Po+** = *00,* but we can numerically set 1, = 0. This makes the information filter more mathematically precise for the zero initial certainty case. However, if the initial uncertainty is zero 
(i.e., we have perfect knowledge of zo), we can numerically set P: = 0, but we cannot numerically set 1; = *00.* This makes the standard Kalman filter more mathematically precise for the zero initial uncertainty case 

The information filter can be used to solve the American football team ranking problem of Example **6.1.** The information filter equations are given as 

$$\begin{array}{l l l}{{{\mathcal I}_{1}^{-}}}&{{=}}&{{Q^{-1}-Q^{-1}F({\mathcal I}_{0}^{+}+F^{T}Q^{-1}F)^{-1}F^{T}Q^{-1}}}\\ {{}}&{{=}}&{{0.1783}}\end{array}$$
$$\begin{array}{l l l}{{=}}&{{{\mathcal{I}}_{1}^{-}+H^{T}R^{-1}H}}\\ {{=}}&{{0.7183}}\\ {{=}}&{{({\mathcal{I}}_{1}^{+})^{-1}H^{T}R^{-1}}}\\ {{=}}&{{\left[\begin{array}{l l l}{{0.6961}}&{{0.2785}}&{{0.0006}}\end{array}\right]}}\\ {{=}}&{{F\hat{x}_{0}^{+}}}\\ {{=}}&{{0.95}}\\ {{=}}&{{\hat{x}_{1}^{-}+K_{1}(y_{1}-H\hat{x}_{1}^{-})}}\\ {{=}}&{{5.1922}}\end{array}$$
$$\tau_{1}^{+}$$
 -  $K_1\\ \\ \\ \\ \hat{x}_1^-\\ \\ \\ \hat{x}_1^+\\ \\ \\$
$$(6.35)$$
5.1922 (6.35) 
The information filter requires the inversion of Q and R, but in many applications these matrices are constant and can therefore be inverted offline. The only other matrix inversions are in the and Kk equations. These inversions are scalar in this example because there is only one state in this example. 

vvv 

## 6.3 Square Root Filtering

The early days of Kalman filtering in the 1960s saw a lot of promise and successful applications in the aerospace industry and in NASA's space program, but sometimes problems arose in implementation. Many of the problems that were encountered were due to numerical difficulties. The Riccati equation solution Pk should theoretically always be -a symmetric positive semidefinite matrix, but numerical problems in computer implementations sometimes led to Pk matrices that became indefinite or nonsymmetric. This was often because of the short word lengths in the computers of the 1960s [Sch81]. Numerical problems may arise in cases in which some elements of the state-vector 2 are estimated to much greater precision than other elements of 2. This could be because of discrepancies in the units of the state-vector elements. For example, one state might be in units of miles and can be estimated to within 0.01 miles, whereas a second state might be in units of cm/s and can be estimated to within 10 cm/s. The covariance for the first state would be on the order of whereas the covariance for the second state would be on the order of lo2. This led to a lot of research during the 1960s that was related to numerical implementations. 

Square root filtering is a way to mathematically increase the precision of the Kalman filter when hardware precision is not available. Perhaps the first square root algorithm was developed by James Potter for NASA's Apollo space program [Bat64]. Although Potter's algorithm was limited to zero process noise and scalar measurements, its success **led** to a lot of additional square root research in the following years. Potter's algorithm was extended to handle process noise in [And68, Dye691, and **was** generalized in two different ways to handle vector measurements in [Be167, And681. Paul Kaminski gives a good review of square root filtering developments during the first decade of the Kalman filter [Kam7l]. 

Now that computers have become so much more capable, we do not have to worry about numerical problems as often. Nevertheless, numerical issues still arise in finite-word-length implementations of algorithms, especially in embedded systems. 

In this section, we will discuss the square root filter, which was developed in order to effectively increase the numerical precision of the Kalman filter and hence mitigate numerical difficulties in implementations. However, this improved performance is at the cost of greater computational effort. First, we will review the concept of the condition number of a matrix, then we will derive the square root version of the time update equation, and finally we will derive the square root version of the measurement update equations. Section 8.3.3 contains a discussion of square root filtering for the continuous-time Kalman filter. 

## 6.3.1 Condition Number

Recall the definition of the singular values of a matrix. An n x n matrix P *has* n singular values o, given as 

$$\begin{array}{r l}{\sigma^{2}(P)}&{{}=}\\ {}&{{}=}\end{array}$$
02(P) = X(PTP) 
$$\begin{array}{l}{{\lambda(P^{T}P)}}\\ {{\lambda(P P^{T})}}\end{array}$$

The matrix PTP is symmetric, and the eigenvalues of a symmetric matrix are always real and nonnegative, so the singular values of a matrix are always real and nonnegative. The matrix P is nonsingular (invertible) if and only if all of its singular values are positive. The condition number of a matrix is defined as 

$$\kappa(P)=\frac{\sigma_{\max}(P)}{\sigma_{\min}(P)}\tag{6.37}$$ $$\geq1$$
$$(6.36)$$

Note that some authors use alternate definitions for condition number; for example, some authors define the condition number of a matrix as the square of the above definiti0n.l As *.(P)* --t *00,* the matrix P is said to be poorly conditioned or ill conditioned, and P approaches a singular matrix. In the implementation of a Kalman filter, the error covariance matrix P should always be positive definite because P = E[(z - *i)(z* - We use the standard notation 

$$P>0$$
$$P={\left[\begin{array}{l l}{10^{6}}&{0}\\ {0}&{10^{-6}}\end{array}\right]}$$
P>O (6.38) 
to indicate that P is positive definite. This is equivalent to saying that P is invertible, which is equivalent to saying that all of the eigenvalues of P are greater than zero. But suppose in our Kalman filter that some elements of z are estimated to much greater precision than other elements of z. For example, suppose that 

$$(6.38)$$
$$(6.39)$$
$$(6.40)$$

This means that our estimate of XI has a standard deviation of **lo3** and our estimate of x2 has a standard deviation of This could be due to drastically different units in z1 and z2, or it could be simply that z1 is much more observable that 22. The singular values of a diagonal matrix are the magnitudes of the diagonal elements, which are lo6 and lo-'. In other words, 

$$\kappa(P)=10^{12}$$
.(P) = 10l2 (6.40) 
lIn MATLAB the COND function can be used to find the condition number of a matrix. 

This is a pretty large condition number, which means that the P matrix might look like a singular matrix to a digital computer. For example, if we have a fixedpoint computer with 10 decimal digits of precision and the lo6 term is represented correctly in the computer, then the term will be represented as a zero in the computer. Mathematically, P is nonsingular, but computationally P is singular. 

The square root filter is based on the idea of finding an S matrix such that P = Sp. The S matrix is then called a square root of P. Note that the definition of the square root of P is *not* that P = 9, but that P = Sp. Also note that this definition of the matrix square root is not standard. Some books and papers defined the matrix square root as P = 9, others define it as P = PS, and others define it as P = *SST.* This latter definition is the one that we will use in this book. If P is symmetric positive definite then it always has a square root [Go189, MooOO]. 

The square root of a matrix may not be unique; that is, there may be more than one solution for S in the equation P = Sp. (This is analogous to the scalar square root, which is usually not unique. For example, the number 1 has two square roots; fl and -1.) Also note that Sp will always be symmetric positive semidefinite no matter what the value of the S matrix. Whereas numerical difficulties might cause P to become nonsymmetric or indefinite in the Kalman filter equations, numerical difficulties can never cause Sp to become nonsymmetric or indefinite. 

Matrix square root algorithms were first given by the French military officer Andre Cholesky (1875-1918) and the Polish astronomer Tadeusz Banachiewicz (18821954) [Fad59]. An interesting biography of Cholesky is given in the appendix of [Mai84]. 

The following algorithm computes an S matrix such that P = Sp for an n x n matrix P. 

The Cholesky Matrix **Square** Root Algorithm { 
For i = l,.--,n For j = *l,-..,n* 
{ 

$$\begin{array}{l}{{1\quad j<i}}\\ {{\frac{1}{S_{i i}}\left(P_{j i}-\sum_{k}^{i}\right)}}\end{array}$$
$\star\quad1$ ... 
Sji=O j<i sji = & *(PJZ* - cklt *Sjksik)* j i 1 
} 
} 
This is called Cholesky factorization and results in a matrix S such that P = 
SST. The matrix S is referred to as the Cholesky triangle because it is a lower triangular matrix. However, the algorithm only works if P is symmetric positive definite. If P is not symmetric positive definite, then it may or may not have a square root.2 In the following example we illustrate the application of Cholesky factorization. 

2The **MATLAB** function CHOL outputs the transpose of the Cholesky triangle that is computed above. 

## 1 **Example63**

This example is taken from [Kam71]. Suppose we have a P matrix given as 

$$\left[\begin{array}{ccc}1&2&3\\ 2&8&2\\ 3&2&14\end{array}\right]\tag{6.41}$$

The Cholesky factorization algorithm tells us that, for i = 1, 

$$P=$$
Sll = 6 
$$\begin{array}{r l}{S_{11}}&{{}=}\\ {}&{{}=}\\ {S_{21}}&{{}=}\\ {}&{{}=}\\ {S_{31}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
S2l = - **(P2l)** 
$$\begin{array}{l}{{\sqrt{P_{11}}}}\\ {1}\\ {\frac{1}{S_{11}}\left(P_{21}\right)}\\ {2}\\ {\frac{1}{S_{11}}\left(P_{31}\right)}\\ {3}\end{array}$$
$$(6.42)$$

For i = 2, the algorithm tells us that 

$$=\sqrt{P_{22}-\sum_{j=1}^{1}S_{2j}^{2}}$$ $$=2$$ $$=0$$ $$=\frac{1}{S_{22}}\left(P_{32}-\sum_{k=1}^{1}S_{3k}S_{2k}\right)$$ $$=-2$$
$$S_{22}$$

$$S_{12}$$  $$S_{32}$$
s12 = 0 
$$(6.43)$$

For i = 3, the algorithm tells us that 

$$\begin{array}{l}{{0}}\\ {{0}}\\ {{1}}\end{array}$$
I 2 
$$\begin{array}{r c l}{{S_{33}}}&{{=}}&{{\sqrt{\vphantom{\bigg|}P_{33}-1}}}\\ {{}}&{{=}}&{{1}}\\ {{S_{13}}}&{{=}}&{{0}}\\ {{S_{23}}}&{{=}}&{{0}}\end{array}$$
$$S=\left[\begin{array}{l l}{{1}}&{{0}}\\ {{2}}&{{2}}\\ {{3}}&{{-2}}\end{array}\right]$$
s33 = 11 **P33** - *CS&* 
$$\overline{{\sum_{j=1}^{2}S_{3j}^{2}}}$$
$$(6.44)$$
$$(6.45)$$

So we obtain S=22Q (6.45) [: :2 :I 
and it can be verified that P = Sp. 

vvv After defining S as the square root of P in the Kalman filter, we will propagate S 
instead of P. This requires more computational effort but it doubles the precision of the filter and helps prevent numerical problems. The singular values B of P are given as 

2(P) = X(PTP)  = X(SSTSST) (6.46) 
The singular values of S are given as 

$$(6.46)$$
$$\sigma^{2}(S)=\lambda(S S^{T})$$
2(S) = *X(SST)* (6.47) 
Recall that for a general matrix A we have X(A2) = **X2(A).** Therefore, we see from the above equations that 

$$\begin{array}{r c l}{{\sigma^{2}(P)}}&{{=}}&{{\left[\sigma^{2}(S)\right]^{2}}}\\ {{\frac{\sigma_{\operatorname*{max}}(P)}{\sigma_{\operatorname*{min}}(P)}}}&{{=}}&{{\frac{\sigma_{\operatorname*{max}}^{2}(S)}{\sigma_{\operatorname*{min}}^{2}(S)}}}\\ {{\kappa(P)}}&{{=}}&{{\kappa^{2}(S)}}\end{array}\tag{1}$$

That is, the condition number of P is the square of the condition number of S. For example, consider the P matrix given earlier in this section: 

$$P=\left[\begin{array}{cc}10^{6}&0\\ 0&10^{-6}\end{array}\right]$$ $$\kappa(P)=10^{12}\tag{6.49}$$
$$(6.47)$$
$$(6.48)$$

The square root of this matrix and its condition number are 

$$S=\left[\begin{array}{cc}10^{3}&0\\ 0&10^{-3}\end{array}\right]$$ $$\kappa(S)=10^{6}\tag{6.50}$$

The condition number of P is *10l2,* but the condition number of the square root of P is only *lo6.* Square root filtering uses this idea to provide twice the precision of the standard Kalman filter. Instead of propagating P, we propagate the square root of P. 

## 6.3.2 The Square Root Timeupdate Equation

Suppose we have an n-state discrete LTI system given as 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+w_{k-1}}}\\ {{E(w_{k}w_{k}^{T})}}&{{=}}&{{Q_{k}}}\end{array}$$

The *a priori* error covariance matrix of the Kalman filter is **P;,** and its square root is *S;.* The *a posteriori* error covariance matrix is *Pz,* and its square root is *S;.* 
Suppose that we can find an orthogonal 2n x 2n matrix T such that 

$$(6.51)$$
$$\left[\begin{array}{c}(S_{k}^{-})^{T}\\ 0\end{array}\right]=T\left[\begin{array}{c}(S_{k-1}^{+})^{T}F_{k-1}^{T}\\ Q_{k-1}^{T/2}\end{array}\right]\tag{6.52}$$ $$=\left[\begin{array}{cc}T_{1}&T_{2}\end{array}\right]\left[\begin{array}{c}(S_{k-1}^{+})^{T}F_{k-1}^{T}\\ Q_{k-1}^{T/2}\end{array}\right]$$

Since T is orthogonal we see that 

$\begin{array}{ccc}T^T T&=&\left[\begin{array}{c}7\\ 8\end{array}\right]\\ \[-3mm]&=&\left[\begin{array}{c}9\\ 7\end{array}\right]\\ \[-3mm]&=&\left[\begin{array}{c}4\\ 7\end{array}\right]\\ \[-3mm]&=&\left[\begin{array}{c}7\\ 7\end{array}\right]\end{array}$  . 
$$\begin{array}{l c l}{{T_{1}^{T}T_{2}=T_{2}^{T}T_{1}}}&{{=}}&{{0}}\\ {{T_{1}^{T}T_{1}=T_{2}^{T}T_{2}}}&{{=}}&{{I}}\end{array}$$
[: ;]  (6.53) 
where TI and T2 are both n x n matrices. We *see* from the above that 

$$(6.54)$$
$$(6.55)$$
$$(6.56)$$
$${\left[\begin{array}{l l}{S_{k}^{-}}&{0}\end{array}\right]}\left[\begin{array}{l}{(S_{k}^{-})^{T}}\\ {0}\end{array}\right]=\left[T_{1}(S_{k-1}^{+})^{T}F_{k-1}^{T}+T_{2}Q_{k-1}^{T/2}\right]^{T}\left[\cdots\right]$$

Now note that we can use Equation (6.52) to write 

We can use this equation, along with Equation (6.54), to write 

$$P_{k}^{-}=F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}$$

If St-, is the square root of *Pkfl,* this implies that 

$$T\left[\begin{array}{c}{{(S_{k-1}^{+})^{T}F_{k-1}^{T}}}\\ {{Q_{k-1}^{T/2}}}\end{array}\right]=\left[\begin{array}{c}{{n\times n\mathrm{\scriptsize~matrix}}}\\ {{0}}\end{array}\right]$$

which is exactly the timeupdate equation for Pk that is required in the Kalman filter, as shown in Equation (5.19). So if we can find an orthogonal 2n x 2n matrix T such that 

$$(6.57)$$
$$(6.58)$$

then the *n x n* matrix in the upper half of the matrix on the right side is equal to *(Si)T.* This assumes that *(Sz-l)T* is available from a square root measurement update equation, which we will discuss in the following two subsections. The square root time update equation above is mathematically equivalent to the original Kalman filter time update equation for P, but the update equation is used to update S instead of P. 

As we noted above, the square root of Pi is not unique, so different algorithms for solving Equation (6.58) will result in different T and *(S;)T* matrices. We can use various methods from numerical linear algebra to find the orthogonal *2n x 2n* matrix T and the resulting square root matrix Si (e.g., Householder, Gram-Schmidt, modified Gram-Schmidt, or Givens transformations) [Hor85, Gol89, Str90, MooOO]. 

A couple of these algorithms are discussed in Section 6.3.5. 

Suppose that at time (k - 1) our Kalman filter has a system matrix, process noise covariance, and a posteriori estimation covariance square root equal to

$$\begin{array}{r c l}{{F_{k-1}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right.}}\\ {{}}&{{}}&{{Q_{k-1}}}&{{=}}&{{\left[\begin{array}{l}{{0}}\\ {{0}}\end{array}\right.}}\\ {{}}&{{}}&{{S_{k-1}^{+}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right.}}\end{array}$$
$$\begin{array}{l}{{1\ \ }}\\ {{1\ \ }}\\ {{0\ \ }}\\ {{2\ \ }}\\ {{0\ \ }}\\ {{1\ \ }}\end{array}$$
$$(6.59)$$

It can be verified that the square root of Qk-1 (so that is given by

$$Q_{k-1}^{1/2}=\left[\begin{array}{c c}{{0}}&{{0}}\\ {{-1}}&{{-1}}\end{array}\right]$$

$$(6.60)$$

Equation (6.58) can be solved as

T FF (SF I I /2 0 Q -1 /5 0 0 √20 0 l v5 l l 1 2 2 l l 0 -5 0 -2 .2 1 l 0 -1 0 √10 √10 0 0 15 0 0
$$\left[\begin{array}{l}{{(6.61)}}\\ {{}}\end{array}\right.$$
As mentioned earlier, algorithms for performing this computation will be discussed in Section 6.3.5. The upper-right square matrix on the right side of the above equation is equal to (ST)2, so this shows that the square root of the a priori estimation covariance at time k is given as

$$S_{k}^{-}={\frac{1}{\sqrt{10}}}\left[\begin{array}{l l}{{\sqrt{20}}}&{{0.}}\\ {{\sqrt{5}}}&{{-5}}\end{array}\right]$$
$$(6.62)$$

From this it can be inferred that the a priori estimation covariance at time k is given as

$$\begin{array}{l l l}{{P_{k}^{-}}}&{{=}}&{{S_{k}^{-}\left(S_{k}^{-}\right)^{T}}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l}{{2\cdot}}&{{1}}\\ {{1}}&{{3}}\end{array}\right]}}\end{array}$$
$$(6.63)$$

Indeed, a straightforward implementation of the time-update equation for the estimation-error covariance gives

$$\begin{array}{r c l}{{P_{k}^{-}}}&{{=}}&{{F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l}{{2}}&{{1}}\\ {{1}}&{{3}}\end{array}\right]}}\end{array}$$
$$(6.64)$$

which confirms our square root results. However, the square root time update has essentially twice the precision of the standard time-update equation.

AAA
164

$$(6.65)$$

## 6.3.3 Potter'S Square Root Measurement-Update Equation

The square root measurement-update equation discussed here is based on James Potter's algorithm, which was developed for NASA's Apollo space program [Bat64, Kam7lI and modified by Angus Andrews to handle vector measurements [And68]. Recall from Equation (5.19) that the measurement update equation for the estimation covariance is given as 

$$P_{k}^{+}=(I-K_{k}H_{k})P_{k}^{-}$$

We can process the measurements one at a time using the sequential Kalman filter of Section 6.1. That is, first we initialize Pofk = *PL.* Then, for i = l,...,~ (where T is the number of measurements), we compute 

$$\begin{array}{c}{{K_{i k}=\frac{P_{i-1,k}^{+}H_{i k}^{T}}{H_{i k}P_{i-1,k}^{+}H_{i k}^{T}+R_{i k}}}}\\ {{P_{i k}^{+}=(I-K_{i k}H_{i k})P_{i-1,k}^{+}}}\end{array}$$
$$K_{i k}=\frac{S_{i-1,k}^{+}S_{i-1,k}^{+T}H_{i k}^{T}}{H_{i k}S_{i-1,k}^{+}S_{i-1,k}^{+T}H_{i k}^{T}+R_{i k}}$$

where *Hik* is the ith row of Hk and *Rik* is the variance of the ith measurement. 

(We are assuming here, as in Section 6.1, that Rk is diagonal.) suppose we have the square root of *Pz+-l,k* so that P:,,, = s:l,ks:;,k. Then *Kik* can be written a5 

$$(6.66)$$
$$(6.67)$$
$$(6.68)$$
$$\begin{array}{r c l}{{P_{i k}^{+}}}&{{=}}&{{\left(I-\frac{S_{i-1,k}^{+}S_{i-1,k}^{+T}H_{i k}^{T}H_{i k}}{H_{i k}S_{i-1,k}^{+T}S_{i-1,k}^{+T}H_{i k}^{T}+R_{i k}}\right)S_{i-1,k}^{+}S_{i-1,k}^{+T}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{S_{i-1,k}^{+}(I-a\phi\phi^{T})S_{i-1,k}^{+T}}}\end{array}$$

and P$ can be written as where $ and a are defined as 

$$(6.69)$$
$$(6.70)$$
$$(6.72)$$

It can be shown (see Problem 6.9) that 

$$\begin{array}{r c l}{{\phi}}&{{=}}&{{S_{i-1,k}^{+T}H_{i k}^{T}}}\\ {{a}}&{{=}}&{{\frac{1}{\phi^{T}\phi+R_{i k}}}}\end{array}$$
$$I-a\phi\phi^{T}=(I-a\gamma\phi\phi^{T})^{2}$$
$$\gamma=\frac{1}{1\pm\sqrt{a R_{i k}}}$$
I - a$+T = (I - *ay$$T)2* (6.70) 
where y is given as 1 
$$(6.71)$$

Either the plus or minus sign can be used in the computation of y. Comparing Equations (6.68) and (6.70) shows that 

$$S_{i k}^{+}=S_{i-1,k}^{+}(I-a\gamma\phi\phi^{T})$$

This results in a square root measurement-update algorithm that can be summarized as follows. 

## Potter'S Square Root Measurement-Update Algorithm

1. After the a priori covariance square root Si and the a priori state estimate 2i have been computed, initialize 

$$\begin{array}{l c l}{{\hat{x}_{0k}^{+}}}&{{=}}&{{\hat{x}_{k}^{-}}}\\ {{S_{0k}^{+}}}&{{=}}&{{S_{k}^{-}}}\end{array}$$
(6.73)  $$\newcommand{\vecs}[1]{\overset{\rightharpoonup}{\mathbf{#1}}}$$  $$\newcommand{\vecd}[1]{\overset{-\!-\!\rightharpoonup}{\vphantom{a}\smash{#1}}}$$

2. For i = 1, . . , r (where r is the number of measurements), perform the following. 

Define **Hik** as the ith row of *Hk, yik* as the ith element of *Yk,* and *Rik* as the variance of the ith measurement (assuming that Rk is diagonal). 

Perform the following to fmd the square root of the covariance after the ith measurement has been processed: 

 As seen produced:  $\begin{array}{rcl}\phi_i&=&S^{+T}_{i-1,k}H^T_{ik}\\ a_i&=&\dfrac{1}{\phi_i^T\phi_i+R_{ik}}\\ \gamma_i&=&\dfrac{1}{1\pm\sqrt{a_i R_{ik}}}\\ S^+_{ik}&=&S^+_{i-1,k}(I-a_i\gamma_i\phi_i\phi_i^T)\\ \end{array}$  The first term is the second term. 
$$=a_{i}S_{i k}^{+}\phi_{i}$$
$$(6,74)$$
Compute the Kalman gain for the ith measurement as 

$$(6.75)$$
$$(6.76)$$
$$(6.77)$$
$$\hat{x}_{i k}^{+}=\hat{x}_{i-1,k}^{+}+K_{i k}(y_{i k}-H_{i k}\hat{x}_{i-1,k}^{+})$$

Compute the state estimate update due to the ith measurement as xik -+ - x,-l,k -+ + Kik(Yik - *Hikf:-l,k)* (6.76) 
3. Set the a posteriori covariance square root and the a posteriori state estimate as 

$$\begin{array}{l c l}{{S_{k}^{+}}}&{{=}}&{{S_{r k}^{+}}}\\ {{\hat{x}_{k}^{+}}}&{{=}}&{{\hat{x}_{r k}^{+}}}\end{array}$$

Although square root filtering improves the numerical characteristics of the Kalman filter, it also increases computational requirements. Efforts to make square root filtering more efficient are reported in [Car73, Tho77, Tap801. 

This example is based on [Kam71]. Suppose that we have an LTI system with 

$$\begin{array}{c c}{{1}}&{{0}}\\ {{0}}&{{1}}\\ {{}}&{{}}\\ {{1}}&{{0}}\end{array}\Big{]}$$ $$\begin{array}{c c}{{1}}&{{0}}\\ {{}}&{{}}\\ {{0}}&{{1}}\\ {{}}&{{}}\\ {{0}}&{{0}}\\ {{}}&{{0}}\end{array}\Big{]}$$
$\begin{array}{ccc}&&\\ &\\ P^-_k&=&\left[\begin{array}{c}1\\ 0\end{array}\right]\\ \[-3mm]H&=&\left[\begin{array}{c}1\\ 0\end{array}\right]\\ \[-3mm]F&=&\left[\begin{array}{c}1\\ 0\end{array}\right]\\ \[-3mm]Q&=&\left[\begin{array}{c}0\\ 0\end{array}\right]\end{array}$  . 
pi- = [; ;] 
H = [l 01 
$$(6.78)$$
= [: :] (6.78) 
If we had an infiniteprecision computer, the exact Kalman gain and a posteriori covariance at time k would be given by 

$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{P_{k}^{-}\,H^{T}(H P_{k}^{-}H^{T}+R)^{-1}}}\\ {{}}&{{=}}&{{\left[\begin{array}{c}{{\frac{1}{1+R}}}\\ {{0}}\end{array}\right]}}\\ {{}}&{{P_{k}^{+}}}&{{=}}&{{(I-K_{k}H)P_{k}^{-}}}\\ {{}}&{{=}}&{{\left[\begin{array}{c c}{{\frac{R}{1+R}}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]}}\end{array}$$
$$(6.79)$$
The a *priori* covariance and Kalman gain at the next time step (k + 1) would 
be given by 
$$P_{k+1}^{-}=FP_{k}^{+}F^{T}+Q\tag{6.80}$$ $$=\left[\begin{array}{cc}\frac{R}{1+R}&0\\ 0&1\end{array}\right]$$ $$K_{k+1}=P_{k+1}^{-}H^{T}(HP_{k+1}^{-}H^{T}+R)^{-1}$$ $$=\left[\begin{array}{c}\frac{1}{2+R}\\ 0\end{array}\right]$$

Now consider implementation in a finite precision digital computer. Suppose that the measurement covariance R << 1. The covariance R is such a tiny number that because of rounding in the computer, 1 + R = 1, but 1 + a> 1. 

The rounded values of the Kalman gain and. a *posteriori* covariance at time k would be given by 

$$K_{k}=\left[\begin{array}{c}\frac{1}{1+R}\\ 0\end{array}\right]\tag{6.81}$$ $$=\left[\begin{array}{c}1\\ 0\end{array}\right]$$ $$P_{k}^{+}=(I-K_{k}H)P_{k}^{-}$$ $$=\left[\begin{array}{cc}0&0\\ 0&1\end{array}\right]$$

Note that Pkf has become singular because of the numerical limitations of the computer. The rounded values of the a *priori* covariance and Kalman gain at the next time step (k + 1) would be given by 

$$\begin{array}{l}=\;FP_{k}^{+}F^{T}+Q\\ =\;\left[\begin{array}{cc}0&0\\ 0&1\end{array}\right]\\ =\;P_{k+1}^{-}H^{T}(HP_{k+1}^{-}H^{T}+R)^{-1}\\ =\;\left[\begin{array}{cc}0\\ 0\end{array}\right]\\ \end{array}\tag{6.82}$$
$$P_{k+1}^{-}$$  $$K_{k+1}$$

The numerical limitations of the computer have resulted in a zero Kalman gain, whereas the infiniteprecision Kalman gain as given in Equation (6.80) 
is about [ 1/2 0 1'. 

Now suppose we implement the measurement-update equation using Potter's algorithm. We start out with 

$S_{k}^{-}=\left[\begin{array}{cc}1&0\\ 0&1\end{array}\right]$ (6.83)
We only have to iterate through Equation (6.74) one time since we only have one measurement. The rounded values of the parameters given in Equation (6.74) are 

$\begin{array}{ccc}\phi&=&(S^-_k)^T H^T\\ &=&\left[\begin{array}{c}1\\ 0\end{array}\right]\\ \[-3mm]a&=&\dfrac{1}{\phi^T\phi+R}\\ \[-3mm]&=&\dfrac{1}{1+R}\\ \[-3mm]\gamma&=&\dfrac{1}{1+\sqrt{aR}}\\ \[-3mm]&=&\dfrac{1}{1+\sqrt{R}}\\ \[-3mm]S^+_k&=&S^-_k(I-a\gamma\phi\phi^T)\\ \[-3mm]&=&\left[\begin{array}{cc}\frac{\sqrt{R}}{1+\sqrt{R}}&0\\ 0&1\end{array}\right]\\ \[-3mm]\end{array}$  is also The number of the "non-negative". 
$$(6.84)$$
Note that *SzScT* is nonsingular. The rounded values of the square root of the a *priori* covariance, the parameters of Equation (6.74), and the Kalman gain at the next time step (k + 1) would be given by 

The step $(\kappa+1)$ would be given by  $\begin{array}{rcl}S_{k+1}^-&=&S_k^+\\ \phi&=&(S_{k+1}^-)^T H^T\\ &=&\left[\begin{array}{c}\frac{\sqrt{R}}{1+\sqrt{R}}\\ 0\end{array}\right]\\ a&=&\frac{1}{\phi^T\phi+R}\\ &=&\frac{1+R+2\sqrt{R}}{R^2+2R+2R\sqrt{R}}\\ &=&\frac{1+2\sqrt{R}}{2R+2R\sqrt{R}}\\ K_{k+1}&=&aS_{k+1}^-\phi\\ &=&\frac{1+2\sqrt{R}}{2R(1+\sqrt{R})}\left[\begin{array}{c}\frac{R}{1+R+2\sqrt{R}}\\ 0\end{array}\right]\\ &=&\left[\begin{array}{c}\frac{1}{2(1+\sqrt{R})}\\ 0\end{array}\right]\end{array}$
$$(6.85)$$
[*I (6.85) 
Note that the rounded Kalman gain is almost identical to the exact Kalman gain given by Equation (6.80). This shows the benefit that can be gained by using the square root filter. 

vvv 

## 6.3.4 Square Root Measurement Update Via Triangularization

The previous section derived a measurement update based on Potter's algorithm that could be performed on the square root of the Kalman filter estimation covariance. This section derives an alternative method for performing the measurement update. Suppose that we want to design a Kalman filter for a system with n states and r measurements. Suppose that we can find an orthogonal matrix (n+r) x *(n+r)* matrix rif such that 

$$\begin{array}{ccc}(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})^{T/2}&\tilde{K}_{k}^{T}\\ 0&(S_{k}^{+})^{T}\end{array}\Big{]}=\tilde{T}\left[\begin{array}{cc}R_{k}^{T/2}&0\\ (S_{k}^{-})^{T}H_{k}^{T}&(S_{k}^{-})^{T}\end{array}\right]\tag{6.86}$$

S; and S,' are the square roots of the a *priori* and a *posteriori* covariances, and 
kk is defined as 
$\tilde{K}_{k}=K_{k}(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})^{T/2}$ (6.87)
where Kk is the normal Kalman gain matrix. Note that Sk+ in Equation (6.86) is not 
known until after an orthogonal is found that forces the left side of Equation (6.86) 
into the specified form. That is, we need to find a 5? so that the upper-left r x r block 
of the left side of Equation (6.86) is equal to (Rk + *HkPLH?)T/2,* the upper-right 
r x n block is equal to *k;,* and the lower-left n x r block is equal to 0. After such 
a is found, whatever the lower right n x n block turns out to be is, by definition, 
equal to *(S,')',* which is the transpose of the square root of *Pz.* Now write the 
(n + r) x (n + r) matrix F as 
$$\tilde{T}=\left[\begin{array}{cc}\tilde{T}_{11}&\tilde{T}_{12}\\ \tilde{T}_{21}&\tilde{T}_{22}\end{array}\right]\tag{6.88}$$
where **5?11** is an r x r matrix, *5?12* is an r x n matrix, *T21* is an n x r matrix, and p22 is an n x n matrix. Since 5? is orthogonal we can write 

(6.89)  = [; ;] 
$$\left[\begin{array}{c c}{{(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})^{T/2}}}&{{\tilde{K}_{k}^{T}}}\\ {{0}}&{{(S_{k}^{+})^{T}}}\end{array}\right]=$$ $$\left[\begin{array}{c c}{{\tilde{T}_{11}R_{k}^{T/2}+\tilde{T}_{12}(S_{k}^{-})^{T}H_{k}^{T}}}&{{\tilde{T}_{12}(S_{k}^{-})^{T}}}\\ {{\tilde{T}_{21}R_{k}^{T/2}+\tilde{T}_{22}(S_{k}^{-})^{T}H_{k}^{T}}}&{{\tilde{T}_{22}(S_{k}^{-})^{T}}}\end{array}\right]$$
Now we expand Equation (6.86) as 

$$(6.90)$$

We will equate the four matrix partitions of this equation to write four separate equalities. We will then take each equality and premultiply each side by its transpose to obtain four new equalities. The first two equalities obtained this way are 

(Rk + HkP;Hr)1/2(. - =  1/2pT p RT/~ + iyks- PT p TI2 +  Rk 11 11 k k 12 llRk  R~/~FTF T T TT  11 12(si) Hk +Hksi5%F12(si) Hk  1'2pTp RT12 + R:/2?!?22(Si) TT Hk +  Hksip&p21RT/2 + Hks~p&~22(si) TT Hk = Rk 21 21 k 
Adding these two equations and using Equations (6.87) and (6.89) to simplify the 
with Si being the square root of *P;.* 
The second two equalities that can be written from Equation (6.90) are 
result gives  $$R_{k}+H_{k}P_{k}^{-}H_{k}^{T}=R_{k}+H_{k}S_{k}^{-}\left(S_{k}^{-}\right)^{T}H_{k}^{T}\tag{6.92}$$  This shows that the proposed measurement update of Equation (6.86) is consistent.  
$$(6.91)$$
ities that can be written from Equation (6.90) are  $\begin{array}{rcl}\tilde{K}_k\tilde{K}_k^T&=&S_k^-\tilde{T}_{12}^T\tilde{T}_{12}(S_k^-)^T\\ S_k^+(S_k^+)^T&=&S_k^-\tilde{T}_{22}^T\tilde{T}_{22}(S_k^-)^T\end{array}$  ons and using Equation (6.89) to simplify the rest. 
$$(6.93)$$
$$(6.95)$$
$$(6.96)$$
Adding these two equations and using Equation (6.89) to simplify the result gives 
Adding these two equations and using Equation (6.89) to simplify the result gives  $$S_{k}^{+}(S_{k}^{+})^{T}+K_{k}(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})K_{k}^{T}=S_{k}^{-}(S_{k}^{-})^{T}\tag{6.94}$$  Substituting the standard Kalman gain equation $K_{k}=P_{k}^{-}H_{k}^{T}(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})^{-1}$
into this equation gives Since the left side of the above equation is symmetric and the first term on the right side is symmetric, the last term on the right side must also be symmetric, which means that we can transpose it in the above equation to obtain 
$$\begin{array}{r c l}{{S_{k}^{+}\,(S_{k}^{+})^{T}+P_{k}^{-}H_{k}^{T}K_{k}^{T}}}&{{=}}&{{P_{k}^{-}}}\\ {{}}&{{}}&{{S_{k}^{+}\,(S_{k}^{+})^{T}}}&{{=}}&{{P_{k}^{-}-P_{k}^{-}H_{k}^{T}K_{k}^{T}}}\end{array}$$
$$S_{k}^{+}(S_{k}^{+})^{T}=P_{k}^{-}-K_{k}H_{k}P_{k}^{-}$$
S,'(s,')' = Pi - *KkHkp;* (6.96) 
The right side of this equation is the Kalman filter measurement-update equation for P, which means that the left side of the equation must be *Pz,* which means that S,' must be the square root of *Pz.* So if we can find an orthogonal (n + r) x (n + r) 
matrix p such that 

$$\begin{array}{c c}{{(R_{k}+H_{k}P_{k}^{-}H_{k}^{T})^{T/2}}}&{{\tilde{K}_{k}^{T}}}\\ {{0}}&{{(n\times n\mathrm{~matrix})}}\end{array}\Bigg{]}=\tilde{T}\left[\begin{array}{c c}{{R_{k}^{T/2}}}&{{0}}\\ {{(S_{k}^{-})^{T}H_{k}^{T}}}&{{(S_{k}^{-})^{T}}}\end{array}\right]$$
$$(6.97)$$

then the lower-right n x n matrix on the left side of the equation is equal to the transpose of the square root of **Pk+,** and this equation is mathematically equivalent to the original Kalman filter measurement-update equation for **Pk.** This measurement-update method results in numerical precision that is effectively twice as much as the standard Kalman filter, which helps to avoid numerical problems. 

However, the computation of? adds a lot of computational effort to the Kalman filter. In addition, the form of the transformation given in Equation (6.97) makes it of questionable practicality (see Problem 6.10). 

## Algorithms For Ort Hogona I Transformations 6.3.5

Several numerical algorithms are available for performing the orthogonal transformations that are required to solve for the T and S; matrices in Equation (6.58). 

Some algorithms that can be used are the Householder method, the Givens method, the Gram-Schmidt method, and the modified Gram-Schmidt method. In this section we will present (without derivation) the Householder algorithm and the modified Gram-Schmidt algorithm. Derivations and presentations of the other algorithms can be found in many texts on numerical linear algebra, such as [Hor85, Go189, MooOO]. A comparison of Gram-Schmidt, modified Gram-Schmidt, and Householder transformations can be found in [Jor68], where it is stated that the modified Gram-Schmidt procedure is best (from a numerical point of view), with the Householder method offering competitive performance. 

6.3.5.1 The Householder algorithm The algorithm presented here **was** developed by Alston Householder [Hou64, Chapter 51, applied to least squares estimation by Gene Golub [Go165], and summarized for Kalman filtering by Paul Kaminski [Kam7l]. 

1. Suppose that we have a 2n x n matrix *A(1),* and we want to find an n x n 

$TA^{(1)}=\left[\begin{array}{c}W\\ 0\end{array}\right]$ (6.98)
where T is an orthogonal 2n x 2n matrix, and 0 is the n x n matrix consisting of all zeros. Note that this problem statement is in the same form as Equation (6.58). **Also** note that we do not necessarily need to find T; our goal is to find W. 

2. For k = 1, . . . , n perform the following: 
(a) Compute the scalar Uk as 

$$\sigma_{k}=\text{sgn}\left(A_{kk}^{(k)}\right)\sqrt{\sum_{i=k}^{2n}\left(A_{ik}^{(k)}\right)^{2}}\tag{6.99}$$

where *A!:)* is the element in the ith row and kth column of *A(k).* The sgn(.) function is defined to be equal to $1 if its argument is greater than or equal to zero, and -1 if its argument is less than zero. 

(b) Compute the scalar ,& as 

$$(6.100)$$
$$\beta_{k}=\frac{1}{\sigma_{k}\left(\sigma_{k}+A_{k k}^{(k)}\right)}$$

(c) For i = 1, * *,2n* perform the following: 

$$u_{i}^{(k)}=\left\{\begin{array}{ll}0&i<k\\ \sigma_{k}+A_{kk}^{(k)}&i=k\\ A_{ik}^{(k)}&i>k\end{array}\right.\tag{6.101}$$

This gives a 2n-element column vector ~(~1. 

(d) For i = 1, . , n perform the following: 

$$y_{i}^{(k)}=\left\{\begin{array}{l l}{{0}}&{{i<k}}\\ {{1}}&{{i=k}}\\ {{\beta_{k}u^{(k)T}A_{i}^{(k)}}}&{{i>k}}\end{array}\right.$$
$$(6.102)$$
$$A^{(k+1)}=A^{(k)}-u^{(k)}y^{(k)T}$$
$$A^{(n+1)}={\left[\begin{array}{l}{W}\\ {0}\end{array}\right]}$$

where *A(k)* is the ith column of *A(k).* This gives an n-element column vector &I. 

(e) Compute the 2n x n matrix as A(k+fl) = A(k) - *u(k)y(k)T* (6.103) 
3. After the above steps have been executed, *A("+1)* has the form 

$$(6.103)$$
$$(6.104)$$
$$(6.105)$$
$$\begin{array}{r c l}{{T}}&{{=}}&{{T^{(n)}T^{(n-1)}\cdots T^{(1)}}}\\ {{T^{(k)}}}&{{=}}&{{I-\beta_{k}u^{(k)}u^{(k)T}\quad i=1,\cdots,n}}\end{array}$$

where W is the n x n matrix that we are trying to solve for. Note that if bk = 0 at any stage of the algorithm, that means *A(1)* is rank deficient and the algorithm will fail. Also note that the above algorithm does not compute the T matrix. However, we can find the T matrix as 6.3.5.2 The modified Gram-Schmidt algorithm The modified Gram-Schmidt algorithm for orthonormalization that is presented here is discussed in most linear systems books [Kai80, Bay99, Che991. It **was** first given in [Bjo67] and was summarized for Kalman filtering in [Kam7l]. 

Suppose that we have a 2n x n matrix *A(1),* and we want to find an n x n 
matrix W such that 
$TA^{(1)}=\left[\begin{array}{c}W\\ 0\end{array}\right]$ (6.106)
where T is an orthogonal 2n x 2n matrix, and 0 is the n x n matrix consisting of all zeros. Note that this problem statement is in the same form as Equation (6.58). 

For k = 1, a . a, n perform the following. 

$$\sigma_{k}=\sqrt{A_{k}^{(k)T}A_{k}^{(k)}}$$

(a) Compute the scalar bk as 

$$(6.107)$$

where *A!k)* is the ith column of *A(')).* 
(b) Compute the kth row of W as 

$$W_{kj}=\left\{\begin{array}{ll}0&j=1,\cdots,k-1\\ \sigma_{k}&j=k\\ A_{k}^{(k)T}A_{j}^{(k)}/\sigma_{k}&j=k+1,\cdots,n\end{array}\right.\tag{6.108}$$
$$T_{k}=A_{k}^{(k)T}/\sigma_{k}$$

(c) Compute the kth row of T as 

$$(6.109)$$

(d) If (k < n), compute the last (n - k) columns of as 

$$(6.110)$$
$$A_{j}^{(k+1)}=A_{j}^{(k)}-W_{k j}A_{k}^{(k)}/\sigma_{k}\;\;\;\;\;j=k+1,\cdots,n$$

Note that the first k columns of rithm. 

are not computed in this algo-
As with the Householder algorithm, if Uk = 0 at any stage of the algorithm, that means A(1) is rank deficient and the algorithm fails. After this algorithm completes, we have the first n rows of T, and T is an n x 2n matrix. If we want to know the last n rows of T, we can compute them using a regular Gram-Schmidt algorithm as follows [Hor85, Go189, MooOO]. 

1. Fill out the T matrix that was begun above by appending a 2n x 2n identity matrix to the bottom of it. This ensures that the rows of T span the entire 2n-dimensional vector space: 

$$T={\left[\begin{array}{l}{T}\\ {I}\end{array}\right]}$$

Note that this T is a 3n x 2n matrix. 

2. Now we perform a standard Gram-Schmidt orthonormalization procedure on the last 2n rows of T (with respect to the already obtained first n rows of *T).* 
For k = n + 1,. ., 3n, compute the kth row of T as 

$$T_{k}=T_{k}-\sum_{i=1}^{k-1}(T_{k}T_{i}^{T})T_{i}$$ $$T_{k}=\frac{T_{k}}{||T_{k}||_{2}}\tag{6.1}$$
$$(6.111)$$
$$(6.112)$$

If Tk is zero then that means that it is a linear combination of the previous rows of T. In that case, the division in the above equation will be a divide by zero, so instead Tk should be discarded. This discard will actually occur exactly n times so that this procedure will compute n additional rows of T 
and we will end up with an orthogonal 2n x 2n matrix T. 

The Gram-Schmidt algorithms are named after the Danish mathematician Jorgen Gram (1850-1916) and the German mathematician Erhard Schmidt (18761959). Schmidt received his doctorate in 1905 under David Hilbert's supervision, and in 1929 he was on the doctoral committee of Eberhard Hopf (see Section 3.4.4). However, the Gram-Schmidt algorithm was actually invented by Pierre Laplace 
(1749-1827). 

## 6.4 U-D Filtering

U-D filtering was introduced in [Bie76, Bie77al as another way to increase the numerical precision of the Kalman filter. It is sometimes considered as a type of square root filtering, and sometimes it is considered distinct from square root filtering (depending on the author). It increases the computational cost of the filter but not so severely as the square root filter of the previous section. 

The idea of U-D filtering is to factor the n x n matrix P as *UDUT,* where U is an n x n upper triangular matrix with ones along the diagonal, and D is an n x n diagonal matrix. This can always be accomplished **for** a symmetric positive definite matrix P [Go189, Chapter **41,** so it can always be implemented on a Kalman filter. A U-D factorization routine can be implemented without too much difficulty. For example, suppose that we want to compute the U-D factorization of a 3 x 3 matrix. We can then write 

Pll Pl2 P13 1 u12 0 00  [ P12 P22 P23] = [  P13 P23 P33 p:] [ df $2 [ ii i3 :]  dll + d22'42 + d33uq3 d22u12 + d33U13u23 d33U13  d22u12 + d33u13u23  d22 + d3343 d33U23 (6.113)  =[ d33u13 d33U23 d33 1 
We need to solve for the uaj and *dii* elements. We can begin at the lower-right element of the matrix equality to see that d33 = *p33.* Next we can look at the other elements in the third column to see that 

$$\begin{array}{r c l}{{u_{13}}}&{{=}}&{{p_{13}/d_{33}}}\\ {{u_{23}}}&{{=}}&{{p_{23}/d_{33}}}\end{array}$$
$$(6.114)$$

Now look at the (2,2) and (1,2) elements of the equality to see that 

$$\begin{array}{r c l}{{d_{22}}}&{{=}}&{{p_{22}-d_{33}u_{23}^{2}}}\\ {{u_{12}}}&{{=}}&{{(p_{12}-d_{33}u_{13}u_{23})/d_{22}}}\end{array}$$
Finally look at the (1,l) element of the equality to see that 
$$(6.115)$$
$d_{11}=p_{11}-d_{22}u_{12}^{2}-d_{33}u_{13}^{2}$ (6.116)
This gives us the U-D factorization for a 3 x 3 symmetric matrix, and provides the outline for a general U-D factorization algorithm. 

## 6.4.1 U-D Filtering: The Measurement-Update Equation

Recall from Equation (5.19) the measurement update equation for the covariance of the Kalman filter: 

$P^{+}=P^{-}-P^{-}H^{T}(HP^{-}H^{T}+R)^{-1}HP^{-}$ (6.117)
We have omitted the time subscripts for ease of notation. Now suppose that we process the measurements sequentially as discussed in Section 6.1. This gives the equation 

$$P_{t}=P_{t-1}-P_{t-1}H_{t}^{T}(H_{t}P_{t-1}H_{t}^{T}+R_{t})^{-1}H_{t}P_{t-1}\tag{6.118}$$
$$(6.120)$$

where H, is the ith row of H, R, is the ith diagonal entry of R, *and* Pz is the estimation covariance after i measurements have been processed. Now define the scalar ai z H,P,-lH? + *R,.* Suppose that P,-1 = U,-lDi-lUzl, and P, = *U,DiU,'.* 
With these factorizations we can write the measurement update of Equation (6.118) 
as 

$$U_{i}D_{i}U_{i}^{T}=U_{i-1}D_{i-1}U_{i-1}^{T}-\frac{1}{\alpha_{i}}U_{i-1}D_{i-1}U_{i-1}^{T}H_{i}^{T}H_{i}U_{i-1}D_{i-1}U_{i-1}^{T}\tag{6.119}$$ $$=U_{i-1}\left[D_{i-1}-\frac{1}{\alpha_{i}}(D_{i-1}U_{i-1}^{T}H_{i}^{T})(D_{i-1}U_{i-1}^{T}H_{i}^{T})^{T}\right]U_{i-1}^{T}$$

The term in brackets in the above equation is symmetric positive definite so it has a U-D factorization that can be written as 

(6.120) 1 
$$\bar{U}\bar{D}\bar{U}^{T}=\left[D_{i-1}-\frac{1}{\alpha_{i}}(D_{i-1}U_{i-1}^{T}H_{i}^{T})(D_{i-1}U_{i-1}^{T}H_{i}^{T})^{T}\right]$$  which with Equation (2.110) is 
Combining this with Equation (6.119) gives 
on $(6,119)$ gives. 
$$\begin{array}{r c l}{{U_{i}D_{i}U_{i}^{T}}}&{{=}}&{{U_{i-1}\bar{U}\bar{D}\bar{U}^{T}U_{i-1}^{T}}}\\ {{}}&{{=}}&{{(U_{i-1}\bar{U})\bar{D}(U_{i-1}\bar{U})^{T}}}\end{array}$$
$$(6.121)$$
$$(6.122)$$
Note that *U,-10* is upper triangular with diagonal elements equal to 1, and b is diagonal. Therefore the above equation means that U, = *Ua-lu,* and Di = D: 

$$\begin{array}{r c l}{{U_{i}}}&{{=}}&{{U_{i-1}{\bar{U}}}}\\ {{D_{i}}}&{{=}}&{{{\bar{D}}}}\end{array}$$

This gives us a way of performing the measurement update of P in terms of its U-D 
factors. The algorithm can be summarized as follows. 

## The U-D **Measurement Update**

We start with the a *priori* estimation covariance P- at time k. Define Po = 
P- . 

For i = 1,. . e, T (where T is the number of measurements), perform the following: 
(a) Define H, as the ith row of *H, R,* as the ith diagonal entry of R, and 
= H,Pi-iH,T + *R,.* 
(b) Perform a U-D factorization of *Pi-1* to obtain *U,-l* and *Di-1,* and then form the matrix on the right side of Equation (6.120). 

(c) Find the U-D factorization of the matrix on the right side of Equation (6.120) and call the factors U and 0. 

(d) Compute U, and Di from Equation (6.122). 
The *a posteriori* estimation covariance is given as P+ = *U,D,U,'.* 
Since the U-D measurement-update equation relies on sequential filtering, the conditions discussed at the end of Section 6.1 apply to U-D filtering. That is, it probably does not make sense to implement U-D filtering unless one of the following two conditions is true. 

1. The measurement noise covariance Rk is diagonal 2. The measurement noise covariance R is a constant. 

## 6.4.2 U-D Filtering: The Timeupdate Equation

Recall from Equation (5.19) the time-update equation for the covariance of the Kalman filter: 

$P^{-}=FP^{+}F^{T}+Q$ (6.123)
We have omitted the time subscripts for ease of notation. If the Kalman filter is being used to estimate the state of an n-state system, then the P matrices will be n x n matrices. Suppose that P+ is factored as *U+D+U+'* (from the measurement update equation discussed previously). We need to find the U-D factors of P- such that P- = U-D-U-' = *FP+FT* + Q. Note that U-' in this notation is not the transpose of the inverse of U; it is rather the transpose of *U-.* The time update of Equation (6.123) can be written as 

$$P^{-}=FP^{+}F^{T}+Q\tag{6.124}$$ $$=\left[\begin{array}{cc}FU^{+}&I\end{array}\right]\left[\begin{array}{cc}D^{+}&0\\ 0&Q\end{array}\right]\left[\begin{array}{cc}U^{+T}F^{T}\\ I\end{array}\right]$$ $$=W\hat{D}W^{T}$$

where W and D are defined by the above equation. Note that W is an n x 2n matrix, and fi is a 2n x 2n matrix. From the above equation we see that the U-D factors of P- need to satisfy 

$$U^{-}D^{-}U^{-T}=W\hat{D}W^{T}$$
$$(6.125)$$
$$(6.126)$$
The transpose of W can be written as 
$$W^{T}={\left[\begin{array}{l l l}{w_{1}^{T}}&{\cdots}&{w_{n}^{T}}\end{array}\right]}$$

That is, wi (a 2n-element row vector) is the ith row of W. Now we find n vectors vi such that 

$$v_{k}\hat{D}v_{j}^{T}\quad=\quad0\quad k\neq j$$

The vi vectors (2n-element row vectors) can be found with the following Gram- Schmidt orthogonalization procedure [Hor85, Go189, MooOO]: 

$$\begin{array}{r c l}{{v_{n}}}&{{=}}&{{w_{n}}}\\ {{v_{k}}}&{{=}}&{{w_{k}-\sum_{j=k+1}^{n}\frac{w_{k}\hat{D}v_{j}^{T}}{v_{j}\hat{D}v_{j}^{T}}v_{j}\quad k=n-1,\cdots,1}}\end{array}$$
$$u(k,j)={\frac{w_{k}{\hat{D}}v_{j}^{T}}{v_{j}{\hat{D}}v_{j}^{T}}}\quad\ j,k=1,\cdots,n$$

If we define *u(k, j)* as 

$$(6.127)$$
$$(6.128)$$
$$(6.129)$$
$$w_{k}=v_{k}+\sum_{j=k+1}^{n}u(k,j)v_{j}\;\;\;\;\;k=1,\cdots,n$$

then from Equation (6.128) we see that Wk can be expressed as 

$$(6.130)$$
or equivalently n 
$$(6.131)$$
$$(6.132)$$
$$({\mathfrak{6}}.133)$$
$$w_{k}^{T}=v_{k}^{T}+\sum_{j=k+1}^{n}u(k,j)v_{j}^{T}\quad k=1,\cdots,n$$

These n equations can be written as 

$${\left[\begin{array}{l}{w_{1}}\\ {w_{2}}\\ {\vdots}\\ {w_{n}}\end{array}\right]}\quad=\quad{\left[\begin{array}{l l l l}{1}&{u(1,2)}&{\cdots}&{u(1,n)}\\ {0}&{1}&{\ddots}&{\vdots}\\ {\vdots}&{\ddots}&{\ddots}&{u(n-1,n)}\\ {0}&{\cdots}&{0}&{1}\end{array}\right]}\left[\begin{array}{l}{v_{1}}\\ {v_{2}}\\ {\vdots}\\ {v_{n}}\end{array}\right]}$$

The n x 2n matrix W, the n x n matrix *U-,* and the n x 2n matrix V are defined by the above equation. Note that U- is a unit upper triangular matrix. The matrix product *WDWT* can then be written as 

$$\begin{array}{r c l}{{W\hat{D}W^{T}}}&{{=}}&{{(U^{-}V)\hat{D}(U^{-}V)^{T}}}\\ {{}}&{{=}}&{{U^{-}(V\hat{D}V^{T})U^{-T}}}\\ {{}}&{{=}}&{{U^{-}D^{-}U^{-T}}}\end{array}$$

where the D- matrix is defined by the above equation. From Equation (6.127), 
we see that the vi vectors are orthogonal with respect to the b inner product. We therefore know that 

$$\begin{array}{r c l}{{D^{-}}}&{{=}}&{{V\hat{D}V^{T}=\mathrm{diag}(d_{1},\cdots,d_{n})}}\\ {{d_{k}}}&{{=}}&{{v_{k}\hat{D}v_{k}^{T}}}\end{array}$$
$$(6.134)$$

That is, D- is a diagonal matrix. From Equations (6.124), (6.125), and (6.133) 
we see that U- and D- satisfy the conditions of being the U-D factors of *P-.* This gives us a way to perform the Kalman filter time-update equation in U-D factorization form. The algorithm can be summarized as follows. 

## The U-D Time Update

1. Begin with P+ = *U+D+UST* (from the measurement update equation). 

2. Define the following matrices. 

$$\begin{array}{l c l}{{W}}&{{=}}&{{\left[\begin{array}{c c}{{F U^{+}}}&{{I}}\end{array}\right]}}\\ {{\hat{D}}}&{{=}}&{{\left[\begin{array}{c c}{{D^{+}}}&{{0}}\\ {{0}}&{{Q}}\end{array}\right]}}\end{array}\tag{6.135}$$

3. Use the rows of W along with the Gram-Schmidt orthogonalization procedure to generate vi vectors that are orthogonal with respect to the D inner product. The algorithm for generating the vi vectors is given in Equation (6.128). 

4. Form the V matrix using the wi vectors as rows; see Equation (6.132). 

5. Use D inner products to form the unit upper triangular matrix *U-;* see Equations (6.129) and (6.132). 

6. Define D- as D- = *Vbv.* 
The U-D filter results in twice as much precision as the standard Kalman filter, just like the square root filter, but it requires less computation than the square root filter. If some of the states are missing from the measurement vector, a more efficient U-D algorithm can be derived [Bar83]. 

## 6.5 Summary

In this chapter, we discussed the sequential Kalman filter, which is mathematically identical to the Kalman filter, but which avoids matrix inversion. This is an attractive formulation for embedded systems in which computational time and memory are at a premium. However, sequential filtering can only be used if the noise covariance is diagonal, or if the noise covariance is constant. Information filtering is also equivalent to the Kalman filter, but it propagates the inverse of the covariance. This can be computationally beneficial in cases in which the number of measure ments is much larger than the number of states. Square root filtering and U-D filtering effectively increase the precision of the Kalman filter. Although these approaches require additional computational effort, they can help prevent divergence and instability. Gerald Bierman's book provides an excellent and comprehensive overview of square root and U-D filtering [Bie77b]. 

We see that we have a number of different choices when implementing a Kalman filter. 

0 Covariance filtering or information filtering 0 Standard filtering, square root filtering, or U-D filtering 0 Batch filtering or sequential filtering Any of these choices can be made independently of the other choices. For instance, we can choose to combine information filtering with square root filtering [Kam7l] in much the same way as we combined covariance filtering with square root filtering in this chapter. The choices in the list above gives us a total of 12 different Kalman filter formulations (two choices in the first item, three choices in the second item, and two choices in the third item). There are also other choices that are not listed above, especially other types of square root filtering. A numerical comparison of various Kalman filter formulations (including the standard filter, the square root covariance filter, the square root information filter, and the Chandrasekhar algorithm) is given in [Ver86]. Numerical and computational comparisons of various Kalman filtering approaches are given in [Bie73, Bie77al. Continuous-time square root filtering is discussed in [Mor78] and in Section 8.3.3 of this book. 

## Written Exercises

6.1 In this chapter, we discussed alternatives to the standard Kalman filter formulation. Some of these alternatives include the sequential Kalman filter, the information filter, and the square root filter. 

What is the advantage of the sequential Kalman filter over the batch Kalman filter? What is the advantage of the batch Kalman filter over the sequential Kalman filter? 

What is the advantage of the information filter over the standard Kalman filter? What is the advantage of the standard Kalman filter over the information filter? What is the advantage of the square root filter over the standard Kalman filter? What is an advantage of the standard Kalman filter over the square root Kalman filter? 

6.2 surement noise covariance matrices Suppose that you have a system with the following measurement and mea- 

$\left[\begin{array}{l}1\\ 0\end{array}\right]$
$$\begin{array}{c}{{0}}\\ {{1}}\end{array}$$
$$\begin{array}{r l}{H}&{{}=}\end{array}$$
$${\bar{\left[\begin{array}{l l}{2}&{1}\\ {1}&{2}\end{array}\right]}}$$
$$R_{\mathrm{{}}}=$$
[: :I 
You want to use a sequential Kalman filter to estimate the state of the system. Derive the normalized measurement, measurement matrix, and measurement noise covariance matrix that could be used in a sequential Kalman filter. 

6.3 Consider the two alternative forms for the information matrix time-update equation. What advantages does Equation **(6.28)** have? What advantages does Equation (6.30) have? 

6.4 A radioactive mass has a half-life of 7 seconds. At each time step k the number of emitted particles 2 is half of what it was one time step ago, but there is some error wk (zero-mean with variance *Qk)* in the number of emitted particles due to background radiation. At each time step the number of emitted particles is counted with two separate and independent instruments. The instruments used to count the number of emitted particles both have a random error at each time step that is zero-mean with a unity variance. The initial uncertainty in the number of radioactive particles is a random variable with zero mean and unity variance. 

The discrete-time equations that model this system have a one-dimensional state and a two-dimensional measurement. Use the information filter to compute the a *priori* and *a posteriori* information matrix at k = 1 and k = 2. Assume that QO = 1 and Q1 = **5/4.** 
Another way to solve this problem is to realize that the two measurements can be averaged to form a single measurement with a smaller variance than the two independent measurements. What is the variance of the averaged measurement at each time step? Use the standard Kalman filter equations to compute the a *priori* and a *posteriori* covariance matrix at k = 1 and k = 2, and verify that it is the inverse of the information matrix that you computed in 'part (a). 

6.5 diagonal elements. 

Prove that the singular values of a diagonal matrix are the magnitudes of the 6.6 Prove that Sp is symmetric positive semidefinite for any S matrix. 

6.7 Find an upper triangular matrix S (using only paper and pencil) such that Is your solution unique? 

6.8 Find an upper triangular matrix S (using only paper and pencil) such that 

$$S S^{T}=\left[\begin{array}{l}{{}}\\ {{}}\end{array}\right]$$
$$\left.{\begin{array}{l}{3}\\ {9}\end{array}}\right]$$
$$S S^{T}={\left[\begin{array}{l}{\quad5}\\ {\quad2}\\ {-2}\end{array}\right]}$$
SF=[ 5 **2 2 -2** -;I 
$$\begin{array}{r l}{{2}}&{{-2}}\\ {{2}}&{{-1}}\\ {{-1}}&{{}}1\end{array}$$
-2 -1 
How many solutions exist to this problem? 

6.9 Verify Equation (6.70). Hint: Equate the two sides of the equation, take the trace, and solve for y. Make sure to explain why taking the trace is valid. 

6.10 ~ Suppose that an orthogonal matrix p is desired to satisfy Equation (6.97), 
where Cholesky factorization is used to compute the matrix square roots on the left side of the equation. This equation can then be written as U = *PA,* where U is an upper triangular matrix. Show that such a transformation cannot be found unless the two-norm of the first column of A happens to be equal to *IUlll.* [Note that this does not necessarily prevent the possibility of the transformation of Equation (6.97), 
because U could be nontriangular if nontriangular square root matrices are used to form the U matrix.] 
6.11 Use the Householder method (using only paper and pencil) to find an orthogonal T such that TA = [ : 
] where W is a 2 x 2 matrix and 

$$\left[\begin{array}{l}{1}\\ {2}\\ {0}\\ {2}\end{array}\right]$$
$$\begin{array}{c}{{1}}\\ {{2}}\\ {{1}}\\ {{2}}\end{array}$$
$${\boldsymbol{A}}=$$

Use the modified Gram-Schmidt method (using only paper and pencil) to 6.12 solve Problem 6.11. 

$$\left.\begin{array}{l}{3}\\ {9}\end{array}\right]$$
$$P={\left[\begin{array}{l}{1}\\ {3}\end{array}\right]}$$

Compute the U-D factorization (using only paper and pencil) for the matrix 6.13 

## Computer Exercises

6.14 Consider the RLC circuit of Example 1.8 with R = 100 and L = C = 1. 

Suppose the applied voltage is continuous-time, zero-mean white noise with a standard deviation of 3. The initial capacitor voltage and inductor current are both zero. Discretize the system with a time step of 0.1. The discretetime measure ments consist of the capacitor voltage and the inductor current, both measurements containing zero-mean unity variance noise. Implement a sequential Kalman filter for the system. Simulate the system for 2 seconds. Let the initial state estimate be equal to the initial state, and the initial estimation covariance be equal to 0.11. 

Hint: Set the discretetime process noise covariance Q = *QcAt,* where Qc is the covariance of the continuoustime process noise, and At is the discretization step size. 

Q will be nondiagonal, which means you need to use the algorithm in Section 2.7 to simulate the process noise. 

a) Generate a plot showing the a *priori* variance of the capacitor voltage estimation error, and the two a *posteriori* variances of the capacitor voltage estimation error. 

b) Generate a plot showing a typical trace of the true, a *posteriori* estimated, and measured capacitor voltage. What is the standard deviation of the capacitor voltage measurement error? What is the standard deviation of the capacitor voltage estimation error? 

6.15 The pitch motion of an aircraft flying at constant speed can be approximately described by the following equations [Ste94] : 

$$\dot{x}=\left[\begin{array}{cc}-0.5680&17.9800\\ 1.0000&-1.2370\end{array}\right]x+\left[\begin{array}{cc}0.1750&0.1750\\ -0.0010&-0.0010\end{array}\right]u+\left[\begin{array}{cc}17.9800\\ -1.2370\end{array}\right]w$$ $$v_{k})=x(t_{k})+v_{k}$$
$$y(t_{k})$$

where 51 is the pitch rate, 52 is the angle of attack, u consists of the elevator and flap angles, and w is disturbance due to wind. Suppose that the variance of the wind disturbance is 0.001, and the measurement variances are **0.3.** Discretize the system with a step size of 0.01 and simulate the system and a square root Kalman filter for 100 time steps. Use an initial state of zero, an initial state estimate of zero, an initial estimation-error covariance of 0.011, and a control input of zero. Hint: Set the discretetime process noise covariance Q = *QcAt,* where Qc is the covariance of the continuous-time process noise, and At is the discretization step size. Q will be nondiagonal, which means you need to use the algorithm in Section 2.7 to simulate the process noise. 

a) Generate a plot showing the a *posteriori* variance of the estimation errors of the two states. 

b) Generate a plot showing a typical trace of the true, a *posteriori* estimated, and measured pitch rate. What is the standard deviation of the pitch rate measurement error? What is the standard deviation of the pitch rate estimation error? 

c) Generate a plot showing a typical trace of the true, a *posteriori* estimated, and measured angle of attack. What is the standard deviation of the angle of attack measurement error? What is the standard deviation of the angle of attack estimation error? 