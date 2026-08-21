---
type: chapter
chapter: 10
title: Additional topics in Kalman filtering
---
# Chapter 10 Additional Topics In Kalman Filtering

The use of wrong a *priori* statistics in the design of a **Kalman** filter can lead to large estimation errors or even to a divergence of errors. 

--Raman Mehra [Meh72] 
The previous chapters covered the essentials of Kalman filtering and should provide a firm foundation for further studies. This chapter discusses some additional important topics related to Kalman filtering. Section 10.1 talks about how to verify that a Kalman filter is operating reliably. When we run computer-based simulations of a Kalman filter, we can tell if the filter is working because we are in control of the simulation model and so we can compare the true state with the estimated state. 

However, in the real world we do not know what the true state is - after all, that is why we need a Kalman filter. In those situations, it is more difficult to verify that the Kalman filter's estimates are reliable. 

Section 10.2 discusses multiplemodel estimation, which is a way of estimating system states when we are not sure of which model is governing the dynamics of the system. This can be useful when the system model changes due to events of which the engineer may not be aware. Section 10.3 discusses reduced-order filtering. Many system models are of high order, which means that the corresponding Kalman filter will also be of high order. The high order of the filter may prevent the real-time implementation of the Kalman filter due to computational constraints. In these cases a smaller, suboptimal filter (called a reduced-order filter) can be designed to give acceptable estimation performance at a lower computational cost. Section 10.4 discusses robust Kalman filtering, which is a way of making the filter less sensitive to variations in the assumed system model. Section 10.5 discusses the topic of delayed measurements. Sometimes the measurements do not arrive at the filter in chronological order because of processing delays. In these cases, we can modify the filter to optimally incorporate measurements that arrive at the filter in the wrong sequence. 

## 10.1 Verifying Kalman Filter Performance

We can verify Kalman filter performance, or adjust the gain of the Kalman filter, using our knowledge of the statistics of the innovations. The innovations is defined as (yk - *Hk?,),* and in this section we will show that it is a zero-mean white stochastic process with a covariance of *(HkpF* H: + &). 

Recall our original system model, along with the one-step a *priori* update equation for the state estimate: 

$$x_{k}=F_{k-1}x_{k-1}+w_{k-1}$$ $$y_{k}=H_{k}x_{k}+v_{k}$$ $$\hat{x}_{k+1}^{-}=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})\tag{10.1}$$

The innovations is defined as the quantity in parentheses in the update equation. 

The innovations can be thought of as the part of the measurement that contains new information and that is therefore used to update the state estimate (apart from our knowledge of the state transition matrix). If the innovations was zero then the state estimate would simply be updated according to the state transition matrix. A nonzero innovations allows the measurement to affect the state estimate. The innovations Tk can be written as where *€k,* the a *priori* estimation error, is defined by the above equation. The covariance of the innovations is given as 

$$\begin{array}{rcl}\tau_{k}&=&y_{k}-H_{k}\hat{x}_{k}^{-}\\ &=&(H_{k}x_{k}+v_{k})-H_{k}\hat{x}_{k}^{-}\\ &=&H_{k}(x_{k}-\hat{x}_{k}^{-})+v_{k}\\ &=&H_{k}\epsilon_{k}+v_{k}\end{array}\tag{10}$$
$$E[r_{k}r_{i}^{T}]=E\left[(H_{k}e_{k}+v_{k})(H_{i}\epsilon_{i}+v_{i})^{T}\right]$$
$$E[r_{k}r_{i}^{T}]=H_{k}E(\epsilon_{k}\epsilon_{i}^{T})H_{i}^{T}+H_{k}E(\epsilon_{k}v_{i}^{T})$$

Let us see what the covariance is when k \# i. We can assume without loss of generality that k > i. We then obtain 

$$(10.2)$$
$$(10.3)$$
$$(10.4)$$

Note that two of the cross terms reduced to zero because of the whiteness of *Wk,* 
and the fact that the estimation error €a is independent of **'uk** for k > i. In order to evaluate this Covariance, we need to evaluate *E(EkET)* and *E(EkwT).* First we will evaluate *E(EkET).* In order to evaluate this term, notice that the a *priori* state estimate can be written as follows: 

$$\hat{x}_{k+1}^{-}=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})\tag{10.5}$$ $$=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(H_{k}x_{k}+v_{k}-H_{k}\hat{x}_{k}^{-})$$ $$=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}H_{k}(x_{k}-\hat{x}_{k}^{-})+F_{k}K_{k}v_{k}$$
$$(10.6)$$

The a *priori* estimation error can be written as 

$$\begin{array}{r c l}{{\epsilon_{k+1}}}&{{=}}&{{x_{k+1}-\hat{x}_{k+1}^{-}}}\\ {{}}&{{=}}&{{F_{k}(x_{k}-\hat{x}_{k}^{-})-F_{k}K_{k}H_{k}(x_{k}-\hat{x}_{k}^{-})+w_{k}-F_{k}K_{k}v_{k}}}\\ {{}}&{{=}}&{{F_{k}(I-K_{k}H_{k})\epsilon_{k}+(w_{k}-F_{k}K_{k}v_{k})}}\\ {{}}&{{=}}&{{\hat{\phi}_{k}\epsilon_{k}+v_{k}^{\prime}}}\end{array}$$
$$\tilde{\phi}_{k,\mathrm{t}}=\left\{\begin{array}{c c}{{\tilde{\phi}_{k-1}\tilde{\phi}_{k-2}\cdots\tilde{\phi}_{i}}}&{{k>i}}\\ {{I}}&{{k=i}}\end{array}\right.$$

where & and w(, are defined by the above equation. This is a linear discretetime system for Ek with the state transition matrix 

$$(10.7)$$

Ek can be solved from the initial condition as follows: 

$$\epsilon_{k}=\tilde{\phi}_{k,i}\epsilon_{i}+\sum_{j=i}^{k-1}\tilde{\phi}_{k,j+1}v_{j}^{\prime}$$
$$(10.8)$$

The covariance of *EkET* can be written as 

$$E(\epsilon_{k}\epsilon_{1}^{T})=E\left[\left(\tilde{\phi}_{k,i}\epsilon_{i}+\sum_{j=i}^{k-1}\tilde{\phi}_{k,j+1}v_{j}^{\prime}\right)\epsilon_{1}^{T}\right]\tag{10.9}$$

We see that all of the W~ET terms in the above expression are zero-mean. This is because all of the wi noise terms occur at time i or later and so do not affect *~i.* 
[Note from Equation (10.6) that ~i is affected only by the noise terms at time (i - 1) 
or earlier.] Therefore, 

$$E(v_{j}^{\prime}\epsilon_{i}^{T})=0\;\;\;\;\;(j\geq i)$$

We therefore see that Equation (10.9) can be written as 

$$(10.10)$$
$$E(\epsilon_{k}\epsilon_{i}^{T})=\tilde{\phi}_{k,i}E(\epsilon_{i}\epsilon_{i}^{T})\tag{10.11}$$ $$=\tilde{\phi}_{k,i}P_{i}^{-}$$

Now that we have computed *E(Ek€r),* we need to solve for *E(EkVT)* in order to arrive at our goal, which is the evaluation of Equation (10.4). *E(ekvT)* can be written as 

$$E(\epsilon_{k}v_{i}^{T})=E\left[\left(\tilde{\phi}_{k,i}\epsilon_{1}+\sum_{j=i}^{k-1}\tilde{\phi}_{k,j+1}v_{j}^{\prime}\right)v_{i}^{T}\right]\tag{10.12}$$

The *E~VT* term in the above expression is zero-mean, and the V~VT terms are zeromean for j > i. The above covariance can therefore be written as 

$$\begin{array}{r c l}{{E(\epsilon_{k}v_{i}^{T})}}&{{=}}&{{E\left(\tilde{\phi}_{k,i+1}v_{i}^{\prime}v_{i}^{T}\right)}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{E\left(\tilde{\phi}_{k,i+1}(w_{i}-F_{i}K_{i}v_{i})v_{i}^{T}\right)}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{-\tilde{\phi}_{k,i+1}F_{i}K_{i}R_{i}}}\end{array}$$
$$\begin{array}{r l}{{}}&{{=}}&{{H_{k}E(\epsilon_{k}\epsilon_{i}^{T})H_{i}^{T}+H_{k}E(\epsilon_{k}v_{i}^{T})}}\\ {{}}&{{=}}&{{H_{k}\tilde{\phi}_{k,i}P_{i}^{-}H_{i}^{T}-H_{k}\tilde{\phi}_{k,i+1}F_{i}K_{i}R_{i}}}\\ {{}}&{{=}}&{{H_{k}\tilde{\phi}_{k,i+1}(\tilde{\phi}_{i}P_{i}^{-}H_{i}^{T}-F_{i}K_{i}R_{i})}}\end{array}$$
$$E(r_{k}r_{i}^{T})$$
$$\begin{array}{r c l}{{E(r_{k}r_{i}^{T})}}&{{=}}&{{H_{k}\tilde{\phi}_{k,i+1}(F_{i}P_{i}^{-}H_{i}^{T}-F_{i}K_{i}H_{i}P_{i}^{-}H_{i}^{T}-F_{i}K_{i}R_{i})}}\\ {{}}&{{=}}&{{H_{k}\tilde{\phi}_{k,i+1}[F_{i}P_{i}^{-}H_{i}^{T}-F_{i}K_{i}(H_{i}P_{i}^{-}H_{i}^{T}+R_{i})]}}\end{array}$$

Substituting this equation, along with Equation (lO.ll), into Equation (10.4) gives 

$$(10.13)$$
$$(10.14)$$
$$(10.15)$$
$$(10.16)$$
$$\begin{array}{r c l}{{E(r_{k}r_{i}^{T})}}&{{=}}&{{H_{k}\tilde{\phi}_{k,i+1}(F_{i}P_{i}^{-}H_{i}^{T}-F_{i}P_{i}^{-}H_{i}^{T})}}\\ {{}}&{{=}}&{{0\qquad\mathrm{for~}k>i}}\end{array}$$
$$E(r_{k}r_{k}^{T})=E[(y_{k}-H_{k}\hat{x}_{k}^{-})(y_{k}-H_{k}\hat{x}_{k}^{-})^{T}]\tag{10.17}$$ $$=E\left\{[H_{k}(x_{k}-\hat{x}_{k}^{-})+v_{k}][H_{k}(x_{k}-\hat{x}_{k}^{-})+v_{k}]^{T}\right\}$$ $$=H_{k}E(e_{k}e_{k}^{T})H_{k}^{T}+E(v_{k}v_{k}^{T})$$ $$=H_{k}P_{k}^{-}H_{k}^{T}+R_{k}$$

So we see that the innovations Tk is white noise. Our next task is to determine its covariance. In order to do this we write the covariance as We therefore see that the innovations is a white noise process with zero mean and a covariance of (HkPiHF + *Rk).* While the Kalman filter is operating, we can process the innovations, compute its mean and covariance, and verify that it is white with the expected mean and covariance. If it is colored, nonzero-mean, or has the wrong covariance, then there is something wrong with the filter. The most likely reason for such a discrepancy is a modeling error. In particular, an incorrect value of *F, H, Q,* or R could cause the innovations to statistically deviate from its theoretically expected behavior. Statistical methods can then be used to tune F, H, Q, and R in order to force the innovations to be white zero-mean noise with a covariance of (HkPLHk + *Rk)* [Meh7O, Meh721. This concept is illustrated in Figure 10.1. A scalar example is presented in Problem 10.1. 

Alternatively, if the engineer is uncertain of the correct values of F, H, Q, and R, 
then a bank of Kalman filters can be run in parallel, each Kalman filter with a value of *F, H,* Q, and R that the engineer thinks may be likely. Then the innovations can be inspected in each filter, and the one that matches theory is assumed to have 

Figure **10.1** This figure illustrates how the performance of a Kalman filter can be used 

![4_image_0.png](4_image_0.png)

to tune the values of F, H, Q, and R in order to obtain residual statistics that agree with theory. Alternatively, the Khan gain K could be tuned directly. 
the correct F, H, Q, and R, so the state estimate that comes out of that filter is probably the most correct. *See* [Kobo31 for an application of this idea. 

The analysis of this section can also be conducted for the continuoustime Kalman filter. The continuous-time innovations, y(t) - *H(t)?(t),* is a zero-mean white stochastic process with a covariance *R(t)* (see Problem 10.2). 

## 10.2 M U Lt I P L E- M 0 **D E L Est1 M At1** 0 N

Suppose our system model is not known, or the system model changes depending on unknown factors. We can use multiple Kalman filters (one for each possible system model) and combine the state estimates to obtain a refmed state estimate. Remember Bayes' rule from Section 2.1: 

$$(10.18)$$
$$\Pr(x|y)={\frac{\Pr(y|x)\Pr(x)}{\Pr(y)}}$$
$$\begin{array}{r c l}{\operatorname*{Pr}(y)}&{=}&{\operatorname*{Pr}(y|x_{1})\operatorname*{Pr}(x_{1})+\cdots+\operatorname*{Pr}(y|x_{N})\operatorname*{Pr}(x_{N})}\\ {\operatorname*{Pr}(x|y)}&{=}&{{\frac{\operatorname*{pdf}(y|x)\operatorname*{Pr}(x)}{\sum_{i=1}^{N}\operatorname*{pdf}(y|x_{i})\operatorname*{Pr}(x_{i})}}}\end{array}$$

Suppose that a random variable x can take one of N mutually exclusive values 21, . . . , *XN.* Then we can use Bayes' rule to write 

$$(10.19)$$

where we have used the fact that the probability of an event occurring is directly proportional to the value of its pdf. Now suppose that we have the timeinvariant system 

$$\begin{array}{rcl}\mathcal{I}_{k}&=&Fx_{k-1}+Gu_{k-1}+w_{k-1}\\ \mathcal{I}_{k}&=&Hx_{k}+v_{k}\\ w_{k}&\sim&N(0,Q)\\ \mathcal{I}_{k}&\sim&N(0,R)\end{array}\tag{1}$$
$$\Pr(p_{j}|y_{k})={\frac{\operatorname{pdf}(y_{k}|p_{j})\Pr(p_{j})}{\sum_{i=1}^{N}\operatorname{pdf}(y_{k}|p_{i})\Pr(p_{i})}}$$
$$(10.20)$$

The parameter set p is defined a 
~~ se that p can take one of N possible values pl, , *p~.* The question that'we want to answer in this section is as follows: Given the measurements Yk, what is the probability that p = *pj?* From Equation (10.19) this probability can be written as 

$$(10.21)$$

Now think about the probability that measurement Yk is observed given the fact that p = *pj.* If p = pj then the state will take on some value Xk that is determined by the parameter set *pj.* We therefore see that However, if our state estimate is accurate, then we know that Xk M ?;. Therefore, the above equation can be written as 

$$\begin{array}{r c l}{\operatorname*{Pr}(y_{k}|p_{j})}&{=}&{\operatorname*{Pr}(y_{k}|x_{k})}\\ {\operatorname*{pdf}(y_{k}|p_{j})}&{=}&{\operatorname*{pdf}(y_{k}|x_{k})}\end{array}$$
$$(10.22)$$
$$\mathrm{pdf}(y_{k}|p_{j})\approx\mathrm{pdf}(y_{k}|{\hat{x}}_{k}^{-})$$

The right side of the equation is the pdf of the measurement Yk given the fact that the state is *2;.* But since yk M H?; + 'uk, this pdf is approximately equal to the pdf of (Yk - H2;). We therefore have 

$$\begin{array}{r l}{\operatorname{pdf}(y_{k}|p_{j})}&{{}\approx\quad\operatorname{pdf}(y_{k}-H_{k}{\hat{x}}_{k}^{-})}\\ {\quad}&{{}=\quad\operatorname{pdf}(r_{k})}\end{array}$$
$$\mathrm{pdf}(y_{k}|p_{j})\approx{\frac{\exp(-r_{k}^{T}S_{k}^{-1}r_{k}/2)}{(2\pi)^{q/2}|S_{k}|^{1/2}}}$$

where Tk is the residual defined in Section **10.1.** From Section **10.1** we see that if Wk, Wk, and 20 are Gaussian, then the residual Tk is a linear combination of Gaussian random variables. Recall from Section **2.4.2** that a linear combination of Gaussian random variables is itself Gaussian. In Section **10.1** we found the mean and variance of Tk. The pdf of Tk, which is approximated by the pdf of Yk given pj, can therefore be aDDroximated as 

$$(10.23)$$
$$(10.24)$$
$$(10.25)$$

where Tk = Yk -Hk?;, sk = HkPiH:+Rk, and q is the number of measurements. 

Now from Bayes' rule we can write the following equation for the probability that p = p3 given the fact that the measurement Yk-1 is observed. 

$$\Pr(p_{j}|y_{k-1})=\frac{\Pr(y_{k-1}|p_{j})\Pr(p_{j})}{\Pr(y_{k-1})}\tag{10.26}$$
$$(10.27)$$

If we are presently at time k, then the measurement at time (k - 1) is a given. The value of the measurement at time (k - 1) is a certain event with a probability equal to one. Therefore, Pr(yk-llpj) = PT(Yk-1) = 1 and the above equation becomes 

$$\operatorname*{Pr}(p_{j}|y_{k-1})=\operatorname*{Pr}(p_{j})$$
Pr(pj I Yk - 1) = Pr(pj ) **(10.27)** 
Now in Equation **(10.21)** we can substitute this equation for Pr(pj), and we substitute Equation **(10.25)** for pdf(yk1pj). This gives a timerecursive equation for evaluating the probability that p = pj given the fact that the measurement was equal to Yk. The multiplemodel estimator can be summarized as follows. 

## The Multiple-Model Estimator

1. For j = **l,...,N,** initialize the probabilities of each parameter set before any measurements are obtained. These probabilities are denoted as Pr(pj **190)** 
(j=l,...,N) . 

2. At each time step k we perform the following steps. 

(a) Run N Kalman filters, one for each parameter set pj (j = 1,. , *N).* 
The a *priori* state estimate and covariance of the jth filter are denoted as 2& and Pk>. 

(b) After the measurement at time k is received, for each parameter set approximate the pdf of Yk given p, as follows: 

$$(10.28)$$
$$(10.29)$$
$$\mathrm{pdf}(y_{k}|p_{j})\approx{\frac{\exp(-r_{k}^{T}S_{k}^{-1}r_{k}/2)}{(2\pi)^{q/2}|S_{k}|^{1/2}}}$$

where rk = yk - Hk2ij, sk = HPGHT + Rk, and q is the number of measurements. 

$$\Pr(p_{j}|y_{k})={\frac{\operatorname{pdf}(y_{k}|p_{j})\Pr(p_{j}|y_{k-1})}{\sum_{i=1}^{N}\operatorname{pdf}(y_{k}|p_{i})\Pr(p_{i}|y_{k-1})}}$$

(c) Estimate the probability that p = pj as follows. 

(d) Now that each parameter set pj has an associated probability, we can weight each *2ij* and Pg accordingly to obtain 

N  j=1  N  (10.30)  j=1 
(e) We can estimate the true parameter set in one of several ways, depending on our application. For example, we can use the parameter set with the highest conditional probability as our parameter estimate, or we can estimate the parameter set as a weighted average of the parameter sets: 

$$\hat{p}=\left\{\begin{array}{ll}\mbox{argmax}_{p_{j}}\Pr(p_{j}|y_{k})&\mbox{max-probability method}\\ \sum_{j=1}^{N}\Pr(p_{j}|y_{k})p_{j}&\mbox{weighted-average method}\end{array}\right.\tag{10.31}$$

As time progresses, some of the Pr(pjlyk) terms will approach zero. Those pj possibilities can then be eliminated and the number N can be reduced. 

In Equation **(10.31),** the function argmax,f(z) returns the value of z at which the maximum-of *f(z)* occurs. For example, max( 1 - **z)2** = 0 because the maximum of (1 - **z)2** is 0, but argmax,(l - z)' = 1 because (1 - attains its maximum value when z = 1. A similar definition holds for the function argmin. 

In this example, we consider a second-order system identification problem [Ste94]. Suppose that we have a continuous-time system with discrete-time measurements described as follows: 

1  =[O -w; -26wn I.+[  4-I 
$$(10.32)$$
The damping ratio 6 = 0.1, and the process and measurement noise covariance Qc and R are respectively equal to **1000** and *101.* The natural frequency 
wn = 2, but this is not known to the engineer. The engineer knows that w; 
is either 4, 4.4, or **4.8** with the following a *priori* probabilities: 
$$\begin{array}{r c l}{{}}&{{}}&{{\mathrm{-}}}\\ {{}}&{{}}&{{\mathrm{Pr}(\omega_{n}^{2}=4)}}\\ {{}}&{{}}&{{\mathrm{Pr}(\omega_{n}^{2}=4.4)}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{\mathrm{Pr}(\omega_{n}^{2}=4.8)}}\\ {{}}&{{}}&{{}}\end{array}=\begin{array}{r c l}{{}}&{{}}&{{\mathrm{-}}}\\ {{}}&{{}}&{{\mathrm{-}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\end{array}$$
The state equation can be written as 
$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+w}}\\ {{w}}&{{\sim}}&{{N(0,B Q_{c}B^{T})}}\end{array}$$
$$(10.33)$$
$$(10.35)$$
$$(10.36)$$
$$(10.34)$$
We can discretize the system using the technique given in Section **1.4.** If the measurements are obtained every 0.1 seconds, then we discretize the state equation with a sample time of T = 0.1 to obtain 

 $\begin{array}{rcl}\texttt{time of a unit of a system}\\ x_k&=&F x_{k-1}+\Lambda w_{k-1}^{\prime}\\ y_k&=&\left[\begin{array}{cc}1&0\\ 0&1\end{array}\right]x_k+v_k\\ F&=&\exp(A T)\\ \Lambda&=&(F-I)F^{-1}\end{array}$  so that the covariance $Q^{\prime}$ of the diagonal is $Q^{\prime}$. 
$$Q^{\prime}\approx B Q_{c}B^{T}T$$
$$(10.37)$$
A = *(F-I)F-I* **(10.35)** 
From Section **8.1** we know that the covariance Q' of the discretetime noise wi is given as This means that the discretetime process dynamics can be written as Q' = *BQ,BTT* **(10.36)** 

xk = FXk-1 f wk-1 
wk N(O,Q) 
$$\begin{array}{l}{{F x_{k-1}+w_{k-1}}}\\ {{N(0,Q)}}\\ {{(F-I)F^{-1}(B Q B^{T}T)F^{-T}(F^{T}-I)}}\end{array}.$$
$$\begin{array}{r l}{x_{k}}&{{}=}\\ {w_{k}}&{{}\sim}\\ {Q}&{{}=}\end{array}$$
The multiplemodel estimator described in this section **was** run on this example. Three Kalman filters running in parallel each generate an estimate of the 
state. As the filters run, the probability of each parameter is updated by the multiplemodel Kalman filter. Figure 10.2 shows the parameter probabilities for a typical simulation run. It is seen that even though the correct parameter 
has the lowest initial probability, the multiplemodel filter estimate converges 
to the correct parameter after a few seconds. 
vvv o.;; 0.8 

![8_image_0.png](8_image_0.png)

Figure **10.2** Parameter probabilities for the multiple-model Kalman filter for Example 10.1. The true parameter value is 4, and the filter converges to the correct parameter after a few seconds. 

## 10.3 Reduced-Order Kalman Filtering

If a user wants to estimate only a subset of the state vector, then a reduced-order filter can be designed. This can be the case, for example, in a real-time application where computational effort is a main consideration. Even in off-line applications, some types of problems (e.g., weather forecasting) can involves tens of thousands of states, which naturally motivates reduced-order filtering as a means to reduce computational effort [Pha98, BalOl]. 

Various approaches to reduced-order filtering have been proposed over the years. 

For example, if the dynamic model of the underlying system can be reduced to a lower-order model that approximates the full-order model, then the reduced-order model can form the basis of a normally designed Kalman filter [Ke199]. This is the approach taken in [Gli94, Sot991 for motor state estimation, in [Sim69, Ara941 for navigation system alignment, in [Bur93, Pat981 for image processing, and in [Cha96] 
for audio processing. If some of the states are not observable then the Kalman filter Riccati equation reduces to a lower-order equation [Yon80]. Reduced-order filtering can be implemented by approximating the covariance with a lower-rank SVD-like decomposition [Pha98, BalOl]. If some of the measurements are noise free, or if there are known equality constraints between some of the states, then the Kalman filter is a filter with an order that is lower than the underlying system [Bry65, Hae981 as discussed in Section 7.5.1 of this book. Optimal reduced-order filters are obtained from first principles in [Ber85, Nag871. A more heuristic approach to reducedorder filtering is to decouple portions of the matrix multiplications in the Kalman filter equations [Chu87]. In this section we will present two different approaches to reduced-order filtering. 

## 10.3.1 Anderson'S Approach To Reduced-Order Filtering

Anderson and Moore [And791 suggest a framework for reduced-order filtering that is fully developed in [SimOGa] and in this section. This approach is based on the idea that we do not always need to estimate all of the states of a system. Sometimes, with a system that has n states, we are interested only in estimating m linear combinations of the states, where m < n. In this case, it stands to reason that we could devise a filter with an order less than n that estimates the m linear combinations that we are interested in. Suppose our state space system is given as 

$$\begin{array}{rcl}\bar{x}_{k+1}&=&\bar{F}\bar{x}_{k}+\bar{G}w_{k}\\ y_{k}&=&\bar{H}\bar{x}_{k}+v_{k}\end{array}\tag{10.38}$$

We desire to estimate the following m linear combinations of the state: TTZ, *q2,* 
. a ., *TKZ,* where each *T,'* is a row vector. Define the n x n matrix T as 

$$(10.39)$$
$$(10.40)$$

$$(10.41)$$

where S is arbitrary as long as it makes T a nonsingular n x n matrix. Now perform the state transformation 

$$T=\left[\begin{array}{c}{{T_{1}^{T}}}\\ {{\vdots}}\\ {{T_{m}^{T}}}\\ {{S}}\end{array}\right]$$
$$x=T{\bar{x}}$$
x = *T?t* **(10.40)** 
This means that Z = *T-lx.* From these relationships we can obtain a state space description of the system in terms of the new state as follows: 

$$\begin{array}{r l}{={}}&{{}{\bar{F}}T^{-1}x_{k}+{\bar{G}}w_{k}}\\ {={}}&{{}{T}{\bar{F}}T^{-1}x_{k}+T{\bar{G}}w_{k}}\\ {={}}&{{}{F}x_{k}+G w_{k}}\\ {={}}&{{}{\bar{H}}T^{-1}x_{k}+v_{k}}\\ {={}}&{{}{H}x_{k}+v_{k}}\end{array}$$
$$T^{-1}x_{k+1}$$ $$x_{k+1}$$
$$y_{k}$$

where F, G, and H are defined by the above equations. Remember that our goal is to estimate the first m elements of x, which we will denote as 5. We therefore partition x as follows: 

$x=\left[\begin{array}{c}\tilde{x}\\ \tilde{\tilde{x}}\end{array}\right]$  $\therefore\quad\tilde{x}_{k+1}\quad\text{and}\quad\omega_{k}\text{as follows:}$ . 
$$(10.42)$$
$$(10.43)$$
$$(10.44)$$
We can then write equations for *zk+1, &+I,* and yk as follows: 

$$\begin{array}{r c l}{{\tilde{x}_{k+1}}}&{{=}}&{{F_{11}\tilde{x}_{k}+F_{12}\tilde{\tilde{x}}_{k}+G_{1}w_{k}}}\\ {{\tilde{\tilde{x}}_{k+1}}}&{{=}}&{{F_{21}\tilde{x}_{k}+F_{22}\tilde{\tilde{x}}_{k}+G_{2}w_{k}}}\\ {{y_{k}}}&{{=}}&{{H_{1}\tilde{x}_{k}+H_{2}\tilde{\tilde{x}}_{k}+v_{k}}}\end{array}$$
$$\hat{\tilde{x}}_{k+1}^{+}=F_{11}\hat{\tilde{x}}_{k}^{+}+K_{k}(y_{k+1}-H_{1}F_{11}\hat{\tilde{x}}_{k}^{+})$$

where the *Fij, Gi,* and H, matrices are appropriately dimensioned partitions of F, G, and H. Now we propose the following form for the one-step a *posteriori* estimator of 5: ii+1 = F11ii + Kk(yk+l - *H1Flli:)* (10.44) 

This predictor/corrector form for the estimate of 2 is very similar to the predictor/corrector form of the standard Kalman filter. The estimation **error** is given as 
follows:  $$e_{k+1}=\tilde{x}_{k+1}-\hat{\tilde{x}}_{k+1}^{+}\tag{10.45}$$ $$=F_{11}(\tilde{x}_{k}-\hat{\tilde{x}}_{k}^{+})+F_{12}\tilde{\tilde{x}}_{k}+G_{1}w_{k}-K_{k}(y_{k+1}-H_{1}F_{11}\hat{\tilde{x}}_{k}^{+})$$ $$=(I-K_{k}F_{11})F_{11}e_{k}+[F_{12}-K_{k}(H_{1}F_{12}-H_{2}F_{22})]\tilde{\tilde{x}}_{k}-$$ $$K_{k}H_{2}F_{21}\tilde{x}_{k}-K_{k}v_{k+1}+[G_{1}-K_{k}(H_{1}G_{1}+H_{2}G_{2})]w_{k}$$  Now we will introduce the following notation for various covariance matrices:  $$P_{k}=E(e_{k}e_{k}^{T})$$
 Solution for various covariance matrices  $\begin{array}{l}E({e}_{k}{e}_{k}^{T})\\ E(\tilde{x}_{k}\tilde{x}_{k}^{T})\\ E(\tilde{\tilde{x}}_{k}\tilde{\tilde{x}}_{k}^{T})\\ E(\tilde{x}_{k}\tilde{\tilde{x}}_{k}^{T})\\ E(\hat{\tilde{x}}_{k}\tilde{\tilde{x}}_{k}^{T})\\ E(\hat{\tilde{x}}_{k}\tilde{\tilde{x}}_{k}^{T})\\ E(\hat{\tilde{x}}_{k}\tilde{\tilde{x}}_{k}^{T})\\ \end{array}$  i.e., we have introduced the variables. 
$$\begin{array}{r l}{P_{k}}&{{}=}\\ {\tilde{P}_{k}}&{{}=}\\ {\tilde{\tilde{P}}_{k}}&{{}=}\\ {\Sigma_{k}}&{{}=}\\ {\tilde{\Pi}_{k}}&{{}=}\\ {\tilde{\tilde{\tilde{\Pi}}}_{k}}&{{}=}\\ {\tilde{\tilde{\Pi}}_{k}}&{{}=}\end{array}$$
& = *E(Zk2:)* 
Fk = *E(ik$T)* 
Ck = *E(Zk5;)* 
fik = E(kkzr) 
$$(10.46)$$
$$(10.47)$$
$$(10.48)$$
fik = *E(kk5T)* (10.46) 
$$Y_{k}=[F_{12}-K_{k}(H_{1}F_{12}+H_{2}F_{22})]^{T}$$
With this notation and the equations given earlier in this section, we can obtain 
the following expressions for these covariances: 
$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{\mathrm{argmin~Tr}P_{k+1}}}\\ {{\frac{\partial\mathrm{Tr}P_{k+1}}{\partial K_{k}}}}&{{=}}&{{0}}\end{array}$$
Now we can find the optimal reduced-order gain Kk at each time step as follows: 

$$(10.49)$$
$$(10.51)$$

In order to compute the partial derivative we have to remember from Section **1.1.3** 
that 

$$\begin{array}{r c l}{{\frac{\partial\mbox{Tr}(A B A^{T})}{\partial A}}}&{{=}}&{{A B+A B^{T}}}\\ {{\frac{\partial\mbox{Tr}(A B)}{\partial A}}}&{{=}}&{{B^{T}}}\\ {{\frac{\partial\mbox{Tr}(B A^{T})}{\partial A}}}&{{=}}&{{B}}\end{array}\tag{10.50}$$
Armed with these tools we can compute the partial derivative of Equation 10.49 
and set it equal to zero to obtain 

$$K_{k}=A_{k}^{-1}B_{k}$$
Kk = **AL1Bk (10.51)** 
where Ak **and** Bk are given as follows: 

(HlF12 + HZF22)Fk(HlF12 f H2F22)T -k  [(HlFlP + HZF22)zTF$HT] + [' * '1' + H2F21FkF21H2 -k TT  Rk+l+ (H1G1 + HzGz)Qk(HzGi + HzGz)~  Bk = F11pk + F12z; - FlzfiT) F&HT + (  (Fllzk - Fllfik + FlZFk) (HlF12 + H2F22)T -k  TT (Fiih - Fill% + Fizz:) FZIHZ + GiQk(HiG1 4- HzGz)~ (10.52) 
Equation **(10.51)** ends up being a long and complicated expression for the reducedorder gain. In fact, this reduced-order filter is probably more computationally expensive than the full-order filter (depending on the values of m and n). However, if the gain of the reduced-order filter converges to steady state, then it can be computed off-line to obtain savings in real-time computational cost and memory usage. However, note that the reduced-order filter may not be stable, even if the full-order Kalman filter is stable. 

Suppose we are given the following system: 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\left[\begin{array}{l l}{{0.9}}&{{0.1}}\\ {{0.2}}&{{0.7}}\end{array}\right]x_{k}+\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]w_{k}}}\end{array}$$
$$(10.53)$$
$$\begin{array}{r c l}{{y_{k}}}&{{=}}&{{\left[\begin{array}{l l}{{0}}&{{1}}\end{array}\right]x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,0.1)}}\\ {{v_{k}}}&{{\sim}}&{{(0,1)}}\end{array}$$

We want to find a reduced-order estimator of the first element of x. In this example the reduced-order gain of Equation (10.51) converges to a steadystate value after about 80 time steps. The estimation-error variance of the reduced-order filter converges to a value that is about 10% higher than the estimation-error variance of the full-order filter for the first state, as shown in Figure 10.3. The estimation error for the reduced-order filter and the fullorder filter is shown in Figure 10.3 for a typical simulation. In this example, the standard deviation of the estimation error was 0.46 for the full-order filter and 0.50 for the reduced-order filter. The steady-state full-order estimator is given as follows: 

$$\hat{x}_{k+1}^{-}=\left[\begin{array}{cc}0.9&0.1\\ 0.2&0.7\end{array}\right]\hat{x}_{k}^{+}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K\left(y_{k}-\left[\begin{array}{cc}0&1\end{array}\right]\hat{x}_{k}^{-}\right)$$ $$K=\left[\begin{array}{cc}0.1983\\ 0.1168\end{array}\right]\tag{10.54}$$
$$\hat{\tilde{x}}_{k+1}^{+}=0.9\hat{\tilde{x}}_{k}^{+}+K_{r}\left[y_{k+1}-(0)(0.9)\hat{\tilde{x}}_{k}^{+}\right]$$ $$=0.9\hat{\tilde{x}}_{k}^{+}+K_{r}y_{k+1}$$ $$K_{r}=0.1420$$

The steady-state reduced-order estimator is given as follows: 

$$(10.55)$$

vvv 

## 10.3.2 The Reduced-Order Schmidt-Kalman Filter

Stanley Schmidt's approach to reduced-order filtering can be used if the states are decoupled from each other in the dynamic equation [Sch66, Bro96, GreOl]. This happens, for instance, if colored measurement noise is accounted for by augmenting the state vector (see Section 7.2.2). In fact, satellite navigation with colored measurement noise was the original motivation for this approach. 

Suppose we have a system in the form 

$$\left[\begin{array}{c}\tilde{\tilde{x}}_{k+1}\\ \tilde{\tilde{x}}_{k+1}\end{array}\right]=\left[\begin{array}{cc}F_{1}&0\\ 0&F_{2}\end{array}\right]\left[\begin{array}{c}\tilde{\tilde{x}}_{k}\\ \tilde{\tilde{x}}_{k}\end{array}\right]+\left[\begin{array}{c}\tilde{w}_{k}\\ \tilde{w}_{k}\end{array}\right]$$ $$\tilde{w}_{k}\sim(0,Q_{1})$$ $$\tilde{w}_{k}\sim(0,Q_{2})$$ $$y_{k}=\left[\begin{array}{cc}H_{1}&H_{2}\end{array}\right]\left[\begin{array}{c}\tilde{\tilde{x}}_{k}\\ \tilde{\tilde{x}}_{k}\end{array}\right]+v_{k}$$ $$v_{k}\sim(0,R)\tag{10.56}$$

We want to estimate **i?k** but we do not care about estimating *ik.* Suppose we use a Kalman filter to estimate the entire state vector. The estimation-error covariance 

![13_image_0.png](13_image_0.png)

Figure **10.3** Results for Example 10.2. The top figure shows the analytical estimationerror variances for the first state for the full-order filter and the reduced-order filter. As expected, the reduced-order filter has a higher estimation-error variance, but the small degradation in performance may be worth the computational savings, depending on the application. The bottom figure shows typical error magnitudes for the estimate of the first state for the full-order filter and the reduced-order filter. The reduced-order filter has slightly larger estimation errors. 
can be partitioned as follows: 

$$P=\left[\begin{array}{l l}{{\tilde{P}}}&{{\Sigma}}\\ {{\Sigma^{T}}}&{{\tilde{\tilde{P}}}}\end{array}\right]$$
$$(10.57)$$

We are omitting the time subscripts for ease of notation. The Kalman gain is usually written as K = P-HT(HP-HT + *R)-l.* With our new notation it can be written as follows: 

$$K=\left[\begin{array}{c}\tilde{K}\\ \tilde{K}\end{array}\right]\tag{10.58}$$ $$=\left[\begin{array}{cc}\tilde{P}^{-}&\Sigma^{-}\\ (\Sigma^{-})^{T}&\tilde{P}^{-}\end{array}\right]\times$$ $$\left[\begin{array}{c}H_{1}^{T}\\ H_{2}^{T}\end{array}\right]\left[\left(\begin{array}{cc}H_{1}&H_{2}\end{array}\right)\left(\begin{array}{cc}\tilde{P}^{-}&\Sigma^{-}\\ (\Sigma^{-})^{T}&\tilde{P}^{-}\end{array}\right)\left(\begin{array}{c}H_{1}^{T}\\ H_{2}^{T}\end{array}\right)+R\right]^{-1}$$  By multiplying out this equation we can write the formula for $\tilde{K}$ as follows.  
$$\tilde{K}=(\tilde{P}^{-}H_{1}^{T}+\Sigma^{-}H_{2}^{T})\alpha^{-1}$$
K = (P-HT + *C-H:)Q-~* (10.59) 
$$\alpha=H_{1}\tilde{P}^{-}H_{1}^{T}+H_{1}\Sigma^{-}H_{2}^{T}+H_{2}(\Sigma^{-})^{T}H_{1}^{T}+H_{2}\tilde{P}^{-}H_{2}^{T}+R$$

where Q is defined as 

$$(10.59)$$
$$(10.60)$$

The measurement-update equation for 53 is normally written as 53; = 3i + K(yk - 
H53L). With our new notation it is written as 

$$\left[\begin{array}{c}\hat{\tilde{x}}_{k}^{+}\\ \hat{\tilde{x}}_{k}^{+}\\ \hat{\tilde{x}}_{k}^{+}\end{array}\right]=\left[\begin{array}{c}\tilde{K}\\ \tilde{K}\end{array}\right]\left(y_{k}-H_{1}\hat{\tilde{x}}_{k}^{-}-H_{2}\hat{\tilde{x}}_{k}^{-}\right)\tag{10.61}$$
$$(10.62)$$

A-
Since we are not going to estimate $ with the reduced-order filter, we set ik = 0 in the above equation to obtain the following measurement-update equation for -+ : 

$${\hat{\tilde{x}}}_{k}^{+}={\hat{\tilde{x}}}_{k}^{-}+{\tilde{K}}\left(y_{k}-H_{1}{\hat{\tilde{x}}}_{k}^{-}\right)$$

The measurement-update equation for P is usually written as P+ = (I-KH)P-(I-
KH)T + *KRKT.* With our new notation it is written as 

[( 0' ;) - (i)  ( HI H2 )IT+ ( f )R( KT kT ) (10.63)  I 
At this point, we assume that I? = 0. This can be justified if the measurement noise associated with the 5 states is large, or if H2 is small, or if the elements of are small. The elements are then referred to as consider states, nuisance states, or nuisance variables, because they are only partially used in the reduced-order state estimator, and because we are not interested in estimating them. Based on Equation (10.63), the update equation for p+ can then be written as 

$$\tilde{P}^{+}=(I-\tilde{K}H_{1})\tilde{P}^{-}(I-\tilde{K}H_{1})^{T}-\tilde{K}H_{2}(\Sigma^{-})^{T}(I-\tilde{K}H_{1})^{T}-$$ $$(I-\tilde{K}H_{1})\Sigma^{-}H_{2}^{T}\tilde{K}^{T}+\tilde{K}H_{2}\tilde{P}^{-}H_{2}^{T}\tilde{K}^{T}+\tilde{K}R\tilde{K}^{T}\tag{10.64}$$
$$(10.65)$$
$$(10.66)$$

Multiplying out the above equation and then using the definition of cr from Equation (10.60) results in 

$$\tilde{P}^{+}=\tilde{P}^{-}-\tilde{K}H_{1}\tilde{P}^{-}-\tilde{P}^{-}H_{1}^{T}\tilde{K}^{T}+\tilde{K}\alpha\tilde{K}^{T}-\tilde{K}H_{2}(\Sigma^{-})^{T}-\Sigma^{-}H_{2}^{T}\tilde{K}^{T}\tag{10.65}$$ $$=\tilde{P}^{-}-\tilde{K}H_{1}\tilde{P}^{-}-\tilde{P}^{-}H_{1}^{T}\tilde{K}^{T}+(\tilde{P}^{-}H_{1}^{T}+\Sigma^{-}H_{2}^{T})\tilde{K}^{T}-\tilde{K}H_{2}(\Sigma^{-})^{T}-$$ $$\Sigma^{-}H_{2}^{T}\tilde{K}^{T}$$ $$=(I-\tilde{K}H_{1})\tilde{P}^{-}-\tilde{K}H_{2}(\Sigma^{-})^{T}$$

This gives the measurement-update equation for **p+.** We can go through similar 
manipulations with Equation (10.63) to obtain 
$$\begin{array}{l l l}{{\Sigma^{+}}}&{{=}}&{{(I-\tilde{K}H_{1})\Sigma^{-}-\tilde{K}H_{2}\tilde{\tilde{P}}^{-}}}\\ {{\tilde{\tilde{P}}^{+}}}&{{=}}&{{\tilde{\tilde{P}}^{-}}}\end{array}$$
-- ;+ 
Putting it all together results in the reduced-order Schmidt-Kalman filter. We can summarize the reduced-order filter as follows. 

## The Reduced-Order Schmidt-Kalman Filter

$$\tilde{K}_{k}\;\;=\;\;(\tilde{P}_{k}^{-}H_{1}^{T}+\Sigma_{k}^{-}H_{2}^{T})\alpha_{k}^{-1}$$

1. The system and measurement equations are given in Equation (10.56). 

(10.67) 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{1}}\end{array}\right]x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q)}}&{{Q=\mathrm{diag}(1,0)}}\\ {{v_{k}}}&{{\sim}}&{{(0,R)}}&{{R=1}}\end{array}$$

Consider the following system: 

$$(10.68)$$

Figure 10.4 shows a typical example of the estimation error of the first element of the state vector for the full-order filter and the reduced-order filter. It is seen that the performances of the two estimators are virtually identical. In other words, we can save a lot of computational effort with only a marginal degradation of estimation performance by using the reduced-order filter. 

vvv 

## 10.4 Robust Kalman Filtering

The Kalman filter works well, but it assumes that the system model and noise statistics are known. If any of these assumptions are violated then the filter estimates can degrade. This was noted early in the history of Kalman filtering [S0065, Hef66, Nis661. 

Daniel Pena and Irwin Guttman give an overview of several methods of robustifying the Kalman filter [Spa88, Chapter 91. For example, although the Kalman filter 

![16_image_0.png](16_image_0.png)

Figure **10.4** Results for Example 10.3. Typical error magnitudes for the estimate of the first state for the full-order filter and the reduced-order filter. The reduced-order filter has only slightly larger estimation errors. 
is the optimal linear filter, it is not the optimal filter in general for non-Gaussian noise. Noise in nature is often approximately Gaussian but with heavier tails, and the Kalman filter can be modified to accommodate these types of density functions [Mas75, Mas77, Tsa831. Sometimes, measurements do not contain any useful information but consist entirely of noise (probabilistically), and the Kalman filter can be modified to deal with this possibility also [Nah69, Sin73, Ath77, Bar781. 

The problem of Kalman filtering with uncertainties in the system matrix *Fk,* the measurement matrix *Hk,* and the noise covariances Qk and *Rk,* has been considered by several authors [Xie94, Zha95, Hsi96, The96, XieO41. This can be called adaptive filtering or robust filtering. Comparisons of adaptive filtering methods for navigation are presented in [Hid03]. Continuous-time adaptive filtering is discussed in [Bar05, MarOB]. Methods for identifying the noise covariances Q *and* R are presented in [Meh7O, Meh72, Als74, Mye761. Additional material on robust Kalman filtering can be found in [Che93]. 

In this section we present a conceptually straightfornard way of making the Kalman filter more robust to uncertainties in Q and R [Kos04]. Suppose we have the linear time-invariant system 

$$(10.69)$$
$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{H x_{k}+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q)}}\\ {{v_{k}}}&{{\sim}}&{{(0,R)}}\end{array}$$

Now suppose that a general steady-state gain K (not necessarily the Kalman gain) 
is used in a predictor/corrector type of state estimator. The state estimate update equations are then given as follows: 

$$\hat{x}_{k+1}^{+}=F\hat{x}_{k}^{+}$$ $$\hat{x}_{k+1}^{+}=\hat{x}_{k+1}^{-}+K(y_{k+1}-H\hat{x}_{k+1}^{-})$$ $$=F\hat{x}_{k}^{+}+K(Hx_{k+1}+v_{k+1}-HF\hat{x}_{k}^{+})$$ $$=KHx_{k+1}+(I-KH)F\hat{x}_{k}^{+}+Kv_{k+1}$$ $$=(KHFx_{k}+KHw_{k})+(I-KH)F\hat{x}_{k}^{+}+Kv_{k+1}\tag{1}$$
$$(10.70)$$
$${}^{k+1}]$$  $$(10.71)$$

The error in the a *posteriori* state estimate can be written as 

$$=x_{k+1}-\hat{x}_{k+1}^{+}$$ $$=(Fx_{k}+w_{k})-[(KHFx_{k}+KHw_{k})+(I-KH)F\hat{x}_{k}^{+}+Kv_{k+1}]$$ $$=(I-KH)Fx_{k}+(I-KH)w_{k}-(I-KH)F\hat{x}_{k}^{+}-Kv_{k+1}$$ $$=(I-KH)Fe_{k}+(I-KH)w_{k}-Kv_{k+1}\tag{10}$$
$$e_{k+1}$$

So the covariance of the estimation error can be written as 

$$P_{k+1}=E(e_{k+1}e_{k+1}^{T})$$ $$=(I-KH)FP_{k}F^{T}(I-KH)^{T}+(I-KH)Q(I-KH)^{T}+KRK^{T}$$
$$\vdash$$ $$(10.72)$$

The steady-state covariance P satisfies the following Riccati equation: 

$$P=(I-K H)F P F^{T}(I-K H)^{T}+(I-K H)Q(I-K H)^{T}+K R K^{T}$$

Note that we derived this without making any assumption on the optimality of the filter gain K. That is, this equation holds regardless of what filter gain K we use. 

Now we can consider what happens when there is no measurement noise, and what happens when there is no process noise. Define PI as the steady-state estimationerror covariance when R = 0, and P2 as the steady-state estimation-error covariance when Q = 0. The above equation for P shows that 

$$(10.73)$$
$$\begin{array}{r c l}{{P_{1}}}&{{=}}&{{(I-K H)F P_{1}F^{T}(I-K H)^{T}+(I-K H)Q(I-K H)^{T}}}\\ {{P_{2}}}&{{=}}&{{(I-K H)F P_{2}F^{T}(I-K H)^{T}+K R K^{T}}}\end{array}$$

Adding these two covariances together results in 

$$P_{1}+P_{2}=(I-KH)FP_{1}F^{T}(I-KH)^{T}+(I-KH)Q(I-KH)^{T}+\tag{10.75}$$ $$(I-KH)FP_{2}F^{T}(I-KH)^{T}+KRK^{T}$$ $$=(I-KH)F(P_{1}+P_{2})F^{T}(I-KH)^{T}+$$ $$(I-KH)Q(I-KH)^{T}+KRK^{T}$$

Comparing this equation with Equation (10.73) shows that P and the sum *(PI +P2)* 
both satisfy the same Riccati equation. This shows that 

$$(10.74)$$
$$P=P_{1}+P_{2}$$
$$(10.76)$$
P = PI + Pz (10.76) 
This shows an interesting linearity property of a general predictor/corrector type of state estimator. The estimation covariance is equal to the sum of the covariance 

$$(10.77)$$

due to process noise only and the covariance due to measurement noise only. Recall from Chapter 5 that the Kalman filter was designed to minimize the trace of P. So the Kalman filter minimizes the trace of (PI + *P2).* 
Now suppose that the true process noise and measurement noise covariancea are different from those assumed by the Kalman filter. The filter is designed under the assumption that the noise covariances are Q *and* R, but the true noise covariancea are Q and R: 

$$\begin{array}{r c l}{{\tilde{Q}}}&{{=}}&{{(1+\alpha)Q}}\\ {{\tilde{R}}}&{{=}}&{{(1+\beta)R}}\end{array}$$

where LY and P are unknown scalars. These differences between the assumed and true covariances will result in a change in the estimation-error covariance of the filter. The true estimation-error covariance will be equal to the assumed covariance P plus some difference *AP.* This can be written as 

$$\tilde{P}=(I-KH)F\tilde{P}F^{T}(I-KH)^{T}+(I-KH)\tilde{Q}(I-KH)^{T}+K\tilde{R}K^{T}$$ $$P+\Delta P=(I-KH)F(P+\Delta P)F^{T}(I-KH)^{T}+$$ $$(1+\alpha)(I-KH)Q(I-KH)^{T}+(1+\beta)KRK^{T}\tag{10.78}$$
Comparing this equation with Equation (10.73) shows that 
$$\Delta P=(I-KH)F\Delta PF^{T}(I-KH)^{T}+\alpha(I-KH)Q(I-KH)^{T}+\beta KRK^{T}\tag{10.79}$$
Now we repeat this same line of reasoning for the computation of the true estimationerror covariance when the process noise is zero (A = PI + *API)* and the true 
estimation-error covariance when the measurement noise is zero (4 = P2 + *AP2).* 
Equation (10.74) shows that 
$$\tilde{P}_{1}=(I-KH)F\tilde{P}_{1}F^{T}(I-KH)^{T}+(I-KH)\tilde{Q}(I-KH)^{T}$$ $$P_{1}+\Delta P_{1}=(I-KH)F(P_{1}+\Delta P_{1})F^{T}(I-KH)^{T}+$$ $$(1+\alpha)(I-KH)Q(I-KH)^{T}$$ $$\tilde{P}_{2}=(I-KH)F\tilde{P}_{2}F^{T}(I-KH)^{T}+K\tilde{R}K^{T}\tag{10}$$ $$P_{2}+\Delta P_{2}=(I-KH)F(P_{2}+\Delta P_{2})F^{T}(I-KH)^{T}+(1+\beta)KRK^{T}$$

Comparing these equations with Equation (10.74) shows that 

$$\begin{array}{r c l}{{\Delta P_{1}}}&{{=}}&{{(I-K H)F\Delta P_{1}F^{T}(I-K H)^{T}+\alpha(I-K H)Q(I-K H)^{T}}}\\ {{\Delta P_{2}}}&{{=}}&{{(I-K H)F\Delta P_{2}F^{T}(I-K H)^{T}+\beta K R K^{T}}}\end{array},$$

Adding these two equations and comparing with Equation (10.79 shows that 

$$\Delta P=\Delta P_{1}+\Delta P_{2}$$
$$P_{1}+\Delta P_{2}$$
AP = *AP1+ AP2* (10.82) 
Comparing Equations (10.74) and (10.81) shows that 

$$\begin{array}{l c l}{{\Delta P_{1}}}&{{=}}&{{\alpha P_{1}}}\\ {{\Delta P_{2}}}&{{=}}&{{\beta P_{2}}}\end{array}$$
$$\begin{array}{c}{{(10.80)}}\\ {{\dot{K}^{T}}}\end{array}$$
$${\boldsymbol{T}}$$ $$\quad(10.81)$$
$$(10.82)$$
$$(10.83)$$
$$(10.84)$$

Combining Equations (10.82) and (10.83) shows that 

$$\Delta P=\alpha P_{1}+\beta P_{2}$$
AP = *PP2* (10.84) 
Now suppose that Q and P are independent zero-mean random variables with variances n: and *a;,* respectively. The previous equation shows that 

$$E[{\rm Tr}(\Delta P)]=E(\alpha){\rm Tr}(P_{1})+E(\beta){\rm Tr}(P_{2})\tag{10.85}$$ $$=0$$ $$E\left\{[{\rm Tr}(\Delta P)]^{2}\right\}=E\left\{[\alpha{\rm Tr}(X_{1})+\beta{\rm Tr}(X_{2})]^{2}\right\}$$ $$=\sigma_{1}^{2}{\rm Tr}^{2}(P_{1})+\sigma_{2}^{2}{\rm Tr}^{2}(P_{2})$$

This gives the variance of the change in the estimation-error covariance due to changes in the process and measurement-noise covariances. A robust filter should try to minimize this variance. In other words, a robust filter should have an estimation-error covariance that is insensitive to changes in the process and measurementnoise covariances. So the performance index of a robust filter can be written as follows: 

$$J=\rho{\rm Tr}(P)+(1-\rho)E\left\{[{\rm Tr}(\Delta P)]^{2}\right\}\tag{10.86}$$ $$=\rho[{\rm Tr}(P_{1})+{\rm Tr}(P_{2})]+(1-\rho)\left[\sigma_{1}^{2}{\rm Tr}^{2}(P_{1})+\sigma_{2}^{2}{\rm Tr}^{2}(P_{2})\right]$$

where p is the relative importance given to filter performance under nominal conditions (i.e., when Q and R are as expected), and (1 - p) is the relative importance given to robustness. In other words, (1 - p) is the relative weight given to minimizing the variation of the estimation-error covariance due to changes in Q and R. If p = 1 then we have the standard Kalman filter. If p = 0 then we will minimize changes in the estimation-error covariance, but the nominal estimation-error covariance may be poor. So p should be chosen to balance nominal performance and robustness. Unfortunately, the performance index J cannot be minimized analytically, so numerical methods must be used. PI *and* P2 are functions of the gain K and can be computed using a DARE function in control system software. The partial derivative of J with respect to K must be computed numerically, and then the value of K can be changed using a gradient-descent method to decrease J. 

Suppose we have a discretized second-order Newtonian system that is driven by an acceleration input. z( 1) represents position, **42)** represents velocity, Uk represents the known acceleration input, and Wk represents the noisy acceleration input. This is the same as the system described in Example 9.1. The system is described as follows: 

$$x_{k+1}=\left[\begin{array}{cc}1&T\\ 0&1\end{array}\right]x_{k}+\left[\begin{array}{c}T^{2}/2\\ T\end{array}\right]u_{k}+w_{k}$$ $$y_{k}=\left[\begin{array}{cc}1&0\end{array}\right]x_{k}+v_{k}$$ $$w_{k}\sim(0,Q)$$ $$v_{k}\sim(0,R)$$ $$Q=q^{2}\left[\begin{array}{cc}T^{4}/4&T^{3}/2\\ T^{3}/2&T/2\end{array}\right]\tag{10.87}$$

The sample time T = 0.1. The variance q2 of the acceleration noise is equal to *0.22,* and the variance R of the measurement noise is equal to lo2. Now suppose that Q and R have relative uncertainties of one (one standard deviation). That is, *CT~* = **~2"** = l. Suppose we find the robust filter gain using equal weighting for both nominal and robust performance (i.e., p = **0.5).** Table **10.1** shows the average performance of the robust filter and the standard Kalman filter when Q and R change by factors of -0.8 and 3, respectively. 

One question that remains is, How does the robust filter perform under nominal conditions? That is, since the Kalman filter is optimal, the robust filter will not perform as well as the Kalman filter when Q and R are equal to their nominal values. However, Table **10.2** shows that the performance degradation is marginal. In fact, the robust filter performs identically to the optimal filter (to two decimal places) under nominal conditions. During the gradientdescent optimization of Equation **(10.86),** the nominal part of the cost function increases from 2.02 to **2.04,** the robust part of the cost function decreases from 2.54 to **2.38,** and the total cost function decreases from 2.28 to 2.21. 

Table 10.1 noise covariances are not nominal (p = 0.5, 61 = 02 = 1, a = -0.8, p = 3) 
RMS estimation errors for Example 10.4 over 100 seconds when the 

| Position        | Velocity   |      |
|-----------------|------------|------|
| Standard Filter | 4.62       | 0.38 |
| Robust Filter   | 4.47       | 0.32 |

| Position         | Velocity   |      |
|------------------|------------|------|
| .Standard Filter | 1.38       | 0.19 |
| Robust Filter    | 1.38       | 0.19 |

Table 10.2 noise covariances are nominal (p = 0.5, 01 = 02 = 1, a = 0, ,B = 0) 
RMS estimation errors for Example **10.4** over 100 seconds when the vvv The robust filtering approach presented here opens several possible research topics. For example, under what conditions is the robust filter stable? Is the gain of the robust filter equal to the gain of a standard Kalman filter for some other related system? What is the true estimation-error covariance of the robust filter? 

## 10.5 Delayed Measurements And Synchronization Errors

In decentralized filtering systems, observations are often collected at various physical locations, and then transmitted in bulk to a central processing computer. In this type of setup, the measurements may not arrive at the processing computer synchronously. That is, the computer may receive measurements out of sequence. 

This is typically the case in target-tracking systems. Various approaches have been taken to deal with this problem [Ale91, Bar95, Kas96, Lar98, MalOl]. The case of delayed measurements with uncertainty in the measurement sampling time is discussed in [Tho94a, Tho94bl. The approach to filtering delayed measurements that is presented here is based on [BarOa]. 

First we will present yet another form of the Kalman filter that will provide the basis for the delayed-measurement filter. Then we will derive the optimal way to incorporate delayed measurements into the Kalman filter estimate and covariance. In this section, we will have to change our notation slightly in order to carry out the derivation of the delayed measurement Kalman filter. We will use the following notation to represent a discretetime system: 

$$x(k)=F(k-1)x(k-1)+w(k-1)$$ $$y(k)=H(k)x(k)+v(k)\tag{10.88}$$

where *w(k)* and *v(k)* are independent zero-mean white noise process with covariances Q(k) and *R(k),* respectively. 

## 10.5.1 A Statistical Derivation Of The Kalman Filter

Suppose that we have an a *priori* estimate *2-(k)* at time k, and we want to find an optimal way to update the state estimate based on the measurement at time k. We want our update equation to be linear (for reasons of mathematical tractability) so we decide to update the state estimate at time k with the equation 

$${\hat{x}}^{+}(k)=K(k)y(k)+b(k)$$
$$(10.89)$$

&+(k) = K(k)y(k) + *b(k)* (10.89) 
where **K(k)** and *b(k)* are a matrix and vector to be determined. Our first state estimation criterion is unbiasedness. We can see by taking the mean of Equation (10.89) 
that - 
$$\overline{{{\hat{x}^{+}}}}(k)=K(k)\bar{y}(k)+b(k)$$
This gives us the constraint that 
$$(10.90)$$
$$(10.91)$$
$$b(k)=\bar{x}(k)-K(k)\bar{y}(k)$$
b(k) = 2(k) - *K(k)@)* (10.91) 
This will ensure that *2+(k)* is unbiased regardless of the value of the gain matrix K(k). Next we find the gain matrix *K(k)* that minimizes the trace of the estimation error. First recall that 

$$\begin{array}{r l}{={}}&{{}E[(z-{\bar{z}})(z-{\bar{z}})^{T}]}\\ {={}}&{{}E(z z^{T})-{\bar{z}}{\bar{z}}^{T}}\end{array}$$
$$P_{z}$$
$$(10.92)$$
$$(10.93)$$

for any general random vector z. Now set z = z(k) - *&+(k).* With this definition of z we see that E = 0. The quantity we want to minimize is given by the trace of the following matrix: 

$$\begin{array}{r c l}{{P^{+}(k)}}&{{=}}&{{E[(x(k)-\hat{x}^{+}(k))(x(k)-\hat{x}^{+}(k))^{T}]}}\\ {{}}&{{=}}&{{P_{z}+\bar{z}\bar{z}^{T}}}\end{array}$$

P, can be computed as follows: 

$$P_{z}=E\left\{[x(k)-\hat{x}^{+}(k)-E(x(k)-\hat{x}^{+}(k))][\cdots]^{T}\right\}\tag{10.94}$$ $$=E\left\{[x(k)-(K(k)y(k)+b(k))-\bar{x}(k)-(K(k)\bar{y}(k)+b(k))][\cdots]^{T}\right\}$$ $$=E\left\{[(x(k)-\bar{x}(k))-K(k)(y(k)-\bar{y}(k))][\cdots]^{T}\right\}$$ $$=P^{-}(k)-K(k)P_{yx}-P_{xy}K^{T}(k)+K(k)P_{y}K^{T}(k)$$
We are using the symbol *P,,* to denote the cross covariance between Yk and **Zk,** *P,,* 
to denote the cross covariance between Xk and Yk, and P, to denote the covariance 
of *Yk.* Recall that Pxv = *Pz.* We have omitted the subscript k on *P,,, P,,,* and P, 
for notational convenience. We combine the above equation with (10.93) to obtain 
$$={\rm Tr}\left(P^{-}(k)-K(k)P_{yx}-P_{xy}K(k)^{T}+K(k)P_{y}K(k)^{T}\right)+{\rm Tr}(\bar{z}\bar{z}^{T})$$ $$={\rm Tr}\left(P^{-}(k)-K(k)P_{yx}-P_{xy}K(k)^{T}+K(k)P_{y}K(k)^{T}\right)+$$ $$||\bar{x}(k)-K(k)\bar{y}(k)-b(k)||^{2}$$ $$={\rm Tr}\left[(K(k)-P_{xy}P_{y}^{-1})P_{y}(K(k)-P_{xy}P_{y}^{-1})^{T}\right]+$$ $${\rm Tr}\left(P^{-}(k)-P_{xy}P_{y}^{-1}P_{xy}^{T}\right)+||\bar{x}(k)-K(k)\bar{y}(k)-b(k)||^{2}\tag{10.95}$$  and the fact that ${\cal F}(\Lambda)={\cal F}(\Lambda)$ for a non-trivial linear system 
$$\begin{array}{r l}{{\mathrm{Tr~}}P^{+}(k)}&{{}=1}\\ {}&{{}=1}\end{array}$$

where we have used the fact that Tr(AB) = *Tr(BA)* for compatibly dimensioned matrices [see Equation (1.26)]. We want to choose *K(k)* and **b(k)** in order to minimize the above expression. The second term is independent of **K(k)** and *b(k),* 
and the first and third terms are always nonnegative. The first and third terms can be minimized to zero when 

$$K(k)=P_{xy}P_{y}^{-1}$$ $$b(k)=\bar{x}(k)-K(k)\bar{y}(k)\tag{10.96}$$

Note that this is the same value for *b(k)* that we obtained in Equation (10.91) when we enforced unbiasedness in the state estimate. With these values of *K(k)* and *b(k),* we see that the first and third terms in (10.95) are equal to zero, so the estimationerror covariance *P+(k)* can be seen to be equal to the second term. Substituting these values into Equation (10.89) we obtain 

$$\hat{x}^{+}(k)=K(k)y(k)+\hat{x}(k)-K(k)\bar{y}(k)$$ $$=K(k)y(k)+\hat{x}^{-}(k)-K(k)H(k)\hat{x}^{-}(k)$$ $$=\hat{x}^{-}(k)+K(k)(y(k)-H(k)\hat{x}^{-}(k))$$ $$P^{+}(k)=P^{-}(k)-P_{xy}P_{y}^{-1}P_{xy}^{T}$$ $$=P^{-}(k)-K(k)P_{y}K^{T}(k)$$  In the last section we find the matrix $P$ and $P$.  
Straightforward calculations (see Problem 10.8) show that P,, *and* P, can be computed as 

$$\begin{array}{r c l}{{P_{x y}}}&{{=}}&{{P^{-}(k)H(k)^{T}}}\\ {{P_{y}}}&{{=}}&{{H(k)P^{-}(k)H(k)^{T}+R(k)}}\end{array}$$
$$\begin{array}{r c l}{{x(k)}}&{{=}}&{{F(k-1)x(k-1)+w(k-1)}}\\ {{y(k)}}&{{=}}&{{H(k)x(k)+v(k)}}\end{array}$$
Now consider our linear discrete-time system: 
$$(10.97)$$
$$(10.98)$$
$$(10.99)$$

The noise processes *w(k)* and v(k) are white, zero-mean, and uncorrelated, with covariances *Q(k)* and *R(k),* respectively. We saw in Chapter 4 how the mean and covariance of the state propagates between measurement times. Those equations, along with the measurement-update equations derived above, provide the following Kalman filter equations: 

$$=F(k-1)\hat{x}^{+}(k-1)$$ $$=F(k-1)P^{+}(k-1)F^{T}(k-1)+Q(k)$$ $$=P^{-}(k)H^{T}(k)$$ $$=H(k)P^{-}(k)H^{T}(k)+R(k)$$ $$=P_{xy}P^{-1}$$ $$=\hat{x}^{-}(k)+K(k)(y(k)-H(k)\hat{x}^{-}(k))$$ $$=P^{-}(k)-K(k)P_{y}K^{T}(k)$$ $$=P^{-}(k)-P_{xy}P_{y}^{-1}P_{xy}^{T}\tag{1}$$  $\hat{x}$ is the $\hat{x}$-function.  
$$\begin{array}{r c l}{{\hat{x}^{-}(k)}}&{{:}}\\ {{P^{-}(k)}}&{{:}}\\ {{P_{x y}}}&{{:}}\\ {{P_{y}}}&{{:}}\\ {{K(k)}}&{{:}}\\ {{\hat{x}^{+}(k)}}&{{:}}\\ {{P^{+}(k)}}&{{:}}\\ {{}}&{{}}\\ {{}}&{{}}\end{array}$$
K(k) = *PsvP;l* 
These equations appear much different than the Kalman filter equations derived 
earlier in this book, but actually they are mathematically identical for linear systems. 

## 10.5.2 Kalman Filtering With Delayed Measurements

Now we need to complicate the notation a little bit more in order to derive the Kalman filter with delayed measurements. We will write our system equations as 

$$(10.100)$$
$$\begin{array}{r l}{x(k)}&{{}=}\\ {y(k)}&{{}=}\end{array}$$
Y(k) = H(k)z(k) + *v(k)* (10.101) 
$$\begin{array}{l}{{F(k,k-1)x(k-1)+w(k,k-1)}}\\ {{H(k)x(k)+v(k)}}\end{array}$$

F(k, k - 1) is the matrix that quantifies the state transition from time (k - 1) to time k. Similarly, *w(k,* k - 1) is the effect of the process noise on the state from time (k - 1) to time k. We can then generalize the statespace equation to the following: 

$$(10.101)$$
$\alpha(k)=F(k,k_{0})\alpha(k_{0})+\alpha(k,k_{0})$
$$(10.102)$$
$$(10.103)$$
$$(10.104)$$
z(k) = **F(k,** *ko)z(ko)* + w(k, *ko)* (10.102) 
where ko is any time index less than k. The above equation can be solved for z(k0) 
as z(k0) = F(ko, k)[z(k) - *w(k,* k0)l (10.103) 
where F(k0, k) = F-l(k, *ko).* Note that F(k, *ko)* should always be invertible if it comes from a real system, because F(k, *ko)* comes from a matrix exponential that is always invertible (see Sections 1.2 and 1.4). The noise w(k, *ko)* is the cumulative effect of all of the process noise on the state from time ko to time k. Its covariance is defined as Q *(k, ko)* : 
w(k, *ko)* N 10, *Q(k,* k0)l (10.104) 
At time k we have the standard a *posteriori* Kalman filter estimate, which is the expected value of the state *z(k)* conditioned on all of the measurements up to and including time k. We also have the a *posteriori* covariance of the estimate: 

$$w(k,k_{0})\sim[0,Q(k,k_{0})]$$
$$\begin{array}{r l}{{\hat{x}}(k)}&{{}=1}\\ {}&{{}=1}\end{array}$$
$E[x(k)|y(1),\cdots,y(k)]$  $E[x(k)|Y(k)]$  $E\left\{[x(k)-\hat{x}(k)][x(k)-\hat{x}(k)]^{T}|Y(k)\right\}$
$$(10.105)$$
$$\begin{array}{r l}{P(k)}&{{}=}\end{array}$$

where Y (k) is defined by the above equation; that is, Y(k) is all of the measurements up to and including time k that have been processed by the Kalman filter. (There may be some measurements before time k that have not yet been processed by the filter. These measurements are not part of Y(k).) 
Now suppose an out-of-sequence measurement arrives. That is, we obtain a measurement from time ko < k that we want to incorporate into the estimate and covariance at time k. The problem is how to modify the state estimate and covariance on the basis of this new measurement. The modified state estimate and covariance are given as follows: 

$$\hat{\hat{x}}(k|k_{0})=E[x(k)|Y(k),y(k_{0})]$$ $$P(k|k_{0})=E\left\{[x(k)-\hat{x}(k,k_{0})][x(k)-\hat{x}(k,k_{0})]^{T}|Y(k),y(k_{0})\right\}\tag{10.106}$$

The approach here is to use the new measurement at time ko to obtain an updated state estimate and covariance at time ko, and then use those quantities to update the estimate and covariance at time k. We can use Equation (10.103) to obtain 

$$E[x(k_{0})|Y(k)]$$

E[z(ko)lY(k)l = Wo, *k)E[z(k)* - w(k, kO)lY(k)l 
$$\begin{array}{r l}{={}}&{{}F(k_{0},k)E[x(k)-w(k,k_{0})|Y(k)]}\\ {={}}&{{}F(k_{0},k)[{\hat{x}}^{-}(k)-{\hat{w}}(k,k_{0})]}\end{array}$$
where *G(k,ko)* is defined by the above equation; it is the expected value of the cumulative effect of the process noise from time ko to time k, conditioned on all of the measurements up to and including time k [but not including measurement 
y(ko)]. Now define the vector 
$$(10.107)$$
$$(10.108)$$
$$(10.109)$$
$$z(k)={\left[\begin{array}{l}{x(k)}\\ {w(k,k_{0})}\end{array}\right]}$$
In general, we define the covariance of vector a conditioned on vector c, and the cross covariance of vectors a and b conditioned on vector c, as follows: 

$$\begin{array}{r c l}{{\mathrm{Cov}(a|c)}}&{{=}}&{{E[(a-\bar{a})(a-\bar{a})^{T}|c]}}\\ {{\mathrm{Cov}(a,b|c)}}&{{=}}&{{E[(a-\bar{a})(b-\bar{b})^{T}|c]}}\end{array}$$
We can then generalize Equation (10.100) to obtain 
$$\hat{z}(k)=\hat{z}^{-}(k)+$$ $$\mathrm{Cov}[z(k),y(k)|Y(k-1)]\mathrm{Cov}^{-1}[y(k)|Y(k-1)]\left(y(k)-H(k)\hat{x}^{-}(k)\right)$$ $$\mathrm{Cov}[z(k)|Y(k)]=\mathrm{Cov}[z(k)|Y(k-1)]-\tag{10.110}$$ $$\mathrm{Cov}[z(k),y(k)|Y(k-1)]\mathrm{Cov}^{-1}[y(k)|Y(k-1)]\mathrm{Cov}[y(k),z(k)|Y(k-1)]$$
$${\rm Cov}[z(k),y(k)|Y(k-1)]=\left[\begin{array}{c}{\rm Cov}[x(k),y(k)|Y(k-1)]\\ {\rm Cov}[w(k,k_{0}),y(k)|Y(k-1)]\end{array}\right]\tag{10.111}$$

The first covariance on the right side of the above i(k) equation can be written as Now consider the first covariance in the above equation. This can be written as 

$$\begin{array}{r l}{\operatorname{Cov}[x(k),y(k)|Y(k-1)]}&{{}=}\\ {}&{{}=}\end{array}$$
$=\;\frac{1}{2}$  . 
Cov[z(k), y(k)lY(k - 111 = cov *{z(k)(H(k)z(k)* + V(k)lTIY(k - 1)) 
$$\begin{array}{l}\mbox{Cov}\left\{x(k)(H(k)x(k)+v(k)]^{T}|Y(k-1)\right\}\\ \mbox{Cov}\left\{x(k)[H(k)x(k)]^{T}|Y(k-1)\right\}\\ \mbox{Cov}\left\{x(k)\right\}H^{T}(k)\\ P^{-}(k)H^{T}(k)\end{array}\tag{10.112}$$
$${\rm Cov}[w(k,k_{0}),y(k)|Y(k-1)]=E\left\{w(k,k_{0})[y(k)-\hat{y}^{-}(k)]^{T}|Y(k-1)\right\}\tag{10.113}$$ $$=E\left\{w(k,k_{0})[H(k)(F(k,k_{0})x(k_{0})+w(k,k_{0}))+v(k)-\hat{y}^{-}(k)]^{T}|Y(k-1)\right\}$$ $$=E\left\{w(k,k_{0})w^{T}(k,k_{0})H^{T}(k)\right\}$$ $$=Q(k,k_{0})H^{T}(k)$$

where the covariance of *z(k)* and *w(k)* is zero since they are independent. Now consider the second covariance on the right side of Equation (10.111). This can be written as where the cross covariances of w(k, *ko)* with z(ko), *w(k),* and *$(k)* are zero since they are independent. We are using the notation *c-(k)* to denote the expected value of y(k) based on measurements up to (but not including) time k. Now consider the conditional covariance of y(k) in Equation (10.110). This was derived in Equation (10.17) in Section 10.1 as 

$$\mathrm{Cov}[y(k)|Y(k-1)]=H(k)P^{-}(k)H^{T}(k)+R(k)$$
Cov[y(k)IY(k - l)] = H(k)P-(k)HT(k) + *R(k)* (1 0.114) 
We will write this expression more compactly as 

$$(10.114)$$
$$\operatorname{Cov}[r(k)]=S(k)$$
$$(10.115)$$
$$(10.117)$$
Cov[r(k)] = *S(k)* (10.115) 
$$\hat{z}(k)=\cdot\left[\begin{array}{c}\hat{x}(k)\\ \hat{w}(k,k_{0})\end{array}\right]\tag{10.116}$$ $$=\left[\begin{array}{c}\hat{x}^{-}(k)\\ \hat{w}^{-}(k,k_{0})\end{array}\right]+\left[\begin{array}{c}P^{-}(k)H^{T}(k)\\ Q(k,k_{0})H^{T}(k)\end{array}\right]S^{-1}(k)r(k)$$  that
where the residual *r(k)* = y(k) - *H(k)C(k)* and its covariance *S(k)* are defined by the two above equations. Substituting Equations (10.112) and (10.113) into Equation (lO.lll), and then substituting into Equation (lO.llO), gives 

$$\begin{array}{r c l}{{\hat{w}(k,k_{0})}}&{{=}}&{{\hat{w}^{-}(k,k_{0})+Q(k,k_{0})H^{T}(k)S^{-1}(k)r(k)}}\\ {{}}&{{=}}&{{Q(k,k_{0})H^{T}(k)S^{-1}(k)r(k)}}\end{array}$$

This shows that because E[G(k,ko)lY(k - l)] = 0 [since *w(k,ko)* is independent of the measurements]. Substituting this expression into Equation (10.107) gives 

$$E[x(k_{0})|Y(k)]=F(k_{0},k)\left[\hat{x}(k)-Q(k,k_{0})H^{T}(k)S^{-1}(k)r(k)\right]$$
$$(10.118)$$

This is called the retrodiction of the state estimate from time k back to time *ko.* 
Whereas a prediction equation is used to predict the state at some future time, a retrodiction equation is used to predict the state at some past time. In this case, the state estimate at time k [i.e., f(k)] is retrodicted back to time ko to obtain the state estimate at time *ko,* which is denoted above as E[z(ko)lY(k)]. Note that E[z(k,-,)lY(k)] is computed on the basis of all the measurements up to and including time k, but does not consider the measurement at time *ko.* 
Now we can write Equation (10.110) as follows: 

x(k) Cov[z(k)|Y(k)] |Y (k) Cov = w(k, ko) x(k) Cov |Y (k - 1) w(k, ko) x(k) Cov Cov-1[y(k)|Y(k - 1)] x , y(k)|Y(k - 1) w(k, ko) x(k) Cov |Y(k - 1) y(k), w(k, ko) Cov[x(k)|Y(k - 1)] Cov[x(k), w(k, ko)|Y(k - 1)] Cov[w(k, ko), x(k)|Y(k - 1)] Cov[w(k, ko)|Y(k - 1)] Cov[x(k), y(k)|Y(k - 1)] Cov-1[y(k)|Y(k - 1)] x Cov[w(k, ko), y(k)|Y(k - 1)] H Cov[x(k), y(k)|Y(k - 1)] (10.119) Cov[w(k, ko), y(k)|Y (k - 1)]
From Equation (10.102) we can write

$${\rm Cov}[x(k),w(k,k_{0})|Y(k-1)]=E[x(k)w^{T}(k,k_{0})|Y(k-1)]\tag{10.120}$$ $$=E\left\{[F(k,k_{0})x(k_{0})+w(k,k_{0})]w^{T}(k,k_{0})|Y(k-1)\right\}$$ $$=E\left\{w(k,k_{0})w^{T}(k,k_{0})|Y(k-1)\right\}$$ $$=Q(k,k_{0})$$

where we have used the independence of x(ko) and w(k, ko).

Now substitute this equation along with Equations (10.112), (10.113), and (10.114) into Equation (10.119) to obtain

$${\rm Cov}\left\{\left[\begin{array}{c}x(k)\\ w(k,k_{0})\end{array}\right]|Y(k)\right\}=\left[\begin{array}{cc}P^{-}(k)&Q(k,k_{0})\\ Q(k,k_{0})&Q(k,k_{0})\end{array}\right]-$$ $$\left[\begin{array}{c}P^{-}(k)H^{T}(k)\\ Q(k,k_{0})H^{T}(k)\end{array}\right]S^{-1}(k)\left[\begin{array}{c}P^{-}(k)H^{T}(k)\\ Q(k,k_{0})H^{T}(k)\end{array}\right]^{T}\tag{10.121}$$

From this equation we can write the conditional covariance of w(k, ko), and cross covariance of x(k) and w(k, ko), as follows:

$$P_{w}(k,k_{0})$$  $$P_{x w}(k,k_{0})$$
$$={\rm Cov}[w(k,k_{0})|Y(k)]\tag{10.122}$$ $$=Q(k,k_{0})-Q(k,k_{0})H^{T}(k)S^{-1}(k)H(k)Q(k,k_{0})$$ $$={\rm Cov}[x(k),w(k,k_{0})|Y(k)]$$ $$=Q(k,k_{0})-P^{-}(k)H^{T}(k)S^{-1}(k)H(k)Q(k,k_{0})$$

Using this in Equation (10.103) gives the conditional covariance of the state retrodiction as follows:

$$={\rm Cov}[x(k_{0})|Y(k)]\tag{10.123}$$ $$=F(k_{0},k){\rm Cov}[x(k)-w(k,k_{0})|Y(k)]F^{T}(k_{0},k)$$ $$=F(k_{0},k)\big{\{}{\rm Cov}[x(k)|Y(k)]-{\rm Cov}[x(k),w(k,k_{0})|Y(k)]-$$ $${\rm Cov}^{T}[x(k),w(k,k_{0})|Y(k)]+{\rm Cov}[w(k,k_{0})|Y(k)]\big{\}}F^{T}(k_{0},k)$$ $$=F(k_{0},k)\left\{P^{+}(k)-P_{xw}(k,k_{0})-P_{xw}^{T}(k,k_{0})+\right.$$ $$\left.P_{w}(k,k_{0})\right\}F^{T}(k_{0},k)\right.$$

Using the above along with Equation (10.101) we obtain the conditional covariance OfY(k0) as 

$$={\rm Cov}[y(k_{0})|Y(k)]\tag{10.124}$$ $$=E\left\{[H(k_{0})x(k_{0})+v(k_{0})][H(k_{0})x(k_{0})+v(k_{0})]^{T}|Y(k)\right\}$$ $$=H(k_{0})P(k_{0},k)H^{T}(k_{0})+R(k_{0})$$
$$S(k_{0})$$

We can use Equations (10.101) and (10.103) to obtain the conditional covariance between **z(k)** and y(k.0) as 

$$P_{xy}(k,k_{0})={\rm Cov}[x(k),y(k_{0})|Y(k)]\tag{10.125}$$ $$={\rm Cov}\left\{x(k),H(k_{0})F(k_{0},k)[x(k)-w(k,k_{0})]+v(k_{0})|Y(k)\right\}$$ $$=[P^{+}(k)-P_{xw}(k,k_{0})]F^{T}(k_{0},k)H^{T}(k_{0})$$

We can substitute this into the top partition of the *i(k)* expression in Equation (10.110) to obtain the estimate of *z(k)* which is updated on the basis of the measurement y(k0): 

$$\hat{\hat{x}}(k,k_{0})=\hat{x}(k)+P_{xy}(k,k_{0})S^{-1}(k_{0})[y(k_{0})-H(k_{0})\hat{x}(k_{0},k)]\tag{10.126}$$

where **f(k0,** k) is the retrodiction of the state estimate given in Equation (10.118). From the top partition of the Cov[z(k)IY(k)] expression in Equation (10.110) we obtain 

$${\rm Cov}[x(k)|Y(k),y(k_{0})]=P(k,k_{0})\tag{10.127}$$ $$=P(k)-P_{xy}(k,k_{0})S^{-1}(k_{0})P_{xy}^{T}(k,k_{0})$$

These equations show how the state estimate and its covariance can be updated on the basis of an out-of-sequence measurement. The delayed-measurement Kalman filter can be summarized as follows. 

## The Delayed-Measurement Kalman Filter

1. The Kalman filter is run normally on the basis of measurements that arrive sequentially. If we are presently at time k in the Kalman filter, then we have *ij-(k)* and *P-(k),* the a *priori* state estimate and covariance that are based on measurements up to and including time (k - 1). We also have **f(k)** 
and *P(k),* the a *posteriori* state estimate and covariance that are based on measurements up to and including time k. 

2. If we receive a measurement **y(ko),** where ko < k, then we can update the 
(a) Retrodict the state estimate from k back to ko as shown in Equastate estimate and its covariance to 2(k, *ko)* and P(k, *ko)* as follows. 

tion (10.118): 

$$S(k)=H(k)P^{-}(k)H^{T}(k)+R(k)$$ $$\hat{x}(k_{0},k)=F(k_{0},k)\left[\hat{x}(k)-Q(k,k_{0})H^{T}(k)S^{-1}(k)r(k)\right]\tag{10.128}$$

(b) Compute the covariance of the retrodicted state using Equations (10.122) 
and (10.123): 

$$P_{w}(k,k_{0})=Q(k,k_{0})-Q(k,k_{0})H^{T}(k)S^{-1}(k)H(k)Q(k,k_{0})$$ $$P_{xw}(k,k_{0})=Q(k,k_{0})-P^{-}(k)H^{T}(k)S^{-1}(k)H(k)Q(k,k_{0})$$ $$P(k_{0},k)=F(k_{0},k)\left\{P(k)-P_{xw}(k,k_{0})-P_{xw}^{T}(k,k_{0})+\right.$$ $$\left.P_{w}(k,k_{0})\right\}F^{T}(k_{0},k)\tag{10.129}$$

(c) Compute the covariance of the retrodicted measurement at time ko using Equation (10.124): 

$$\mathrm{T}(k_{0})+R(k_{0})$$
$$(10.130)$$
$$(10.131)$$

S(k0) = H(ko)P(ko, WT(ko) + *R(ko)* (10.130) 
(d) Compute the covariance of the state at time k and the retrodicted measurement at time ko using Equation (10.125): 

$$=\hat{x}(k)+P_{xy}(k,k_{0})S^{-1}(k_{0})[y(k_{0})-H(k_{0})\hat{x}(k_{0},k)]$$ $$=P(k)-P_{xy}(k,k_{0})S^{-1}(k_{0})P_{xy}^{T}(k,k_{0})\tag{10.132}$$

Pz,(k, ko) = [P(k) - *Pzw(k,* kO)l~T(ko, *k)HT(ko>* (10.131) 
(e) Use the delayed measurement **y(k0)** to update the state estimate and its covariance: 
It is possible to make some simplifying approximations to this delayed measurement filter in order to decrease computational cost with only a slight degradation in performance [Bar021 . 

## 10.6 Summary

In this chapter we discussed some important topics related to Kalman filtering that extend beyond standard results. We have seen how to verify if a Kalman filter is operating reliably. This gives us a quantifiable confidence in the accuracy of our filter estimates. We also discussed multiplemodel estimation, which is a way of estimating system states when we are not sure of which model is governing the dynamics of the system. This can be useful when the system model changes in unpredictable ways. We discussed reduced-order filtering, which can be used to estimate a subset of the system states while saving computational effort. We derived a robust Kalman filter, which makes the filter less sensitive to variations in the assumed system model. Robust filtering naturally leads into the topic of H, filtering, which we will discuss in Chapter 11. Finally, we derived a way to update the state estimate when a measurement arrives at the filter in the wrong chronological order because of processing delays. 

There are several other important extensions to Kalman filtering that we have not had time to discuss in this chapter. One is the variable structure filter, which is a combination of the Kalman filter with variable structure control. This guarantees stability under certain conditions and often provides performance better than the Kalman filter, especially when applied to nonlinear systems [Hab03]. Another recent proposal is the proportional integral Kalman filter, which adds an integral term to the measurement state update and thereby improves stability and reduces steady-state tracking errors [Bas99]. Another interesting topic is the use of a perturbation estimator to estimate the process noise . This allows model uncertainties to be lumped with process noise so that the processnoise estimate increases the robustness of the filter [KwoOS]. 

## Problems Written Exercises

10.1 In this problem we consider the scalar system zk+l = zkfwk Yk = xk *+vk* where wk and Vk are white and uncorrelated with respective variances Q and R, which are unknown. A suboptimal steady-state value of K is used in the state estimator since Q and R are unknown. 

a) Use the expression for Pi along with the first expression for Pz in Equation (5.19) to find the steady-state value of Pi as a function of the suboptimal value of K and the true values of Q and R. [Note that the first expression for P$ in Equation (5.19) does not depend on the value for Kk being optimal.] 
b) Now suppose that *E(rg)* and *E(Tk+lTk)* are found numerically as the filter runs. Find the true value of R and the steady-state value of Pi as a function of *~(r:)* and *E(Tkf1Tk).* 
c) **Use** your results from parts (a) and (b) to find the true value of Q. 

10.2 Show that the innovations r = y - C2 of the continuous-time Kalman filter is white with covariance R. 

10.3 Consider the system described in Problem 5.1. Find the steady-state variance of the Kalman filter innovations when Q = R and when Q = *2R.* 
10.4 Consider the system of Problem **10.3** with Q = R = 1. Suppose the Kalman filter for the system has reached steady state. At time k the innovations Tk = 
'& - 2;. 

a) Find an approximate value for pdf(yk **lp)** (where p is the model used in the Kalman filter) if Tk = 0, if Tk = 1, and if Tk = 2. 

b) Suppose that the use of model pl gives Tk = 0, model p2 gives Tk = 1, and model p3 gives rk = 2. Further suppose that *Pr(pllyk-1)* = **1/4,** Pr(pzlyk-1) = **1/4,** and *Pr(p31Yk-l)* = **1/2.** Find *Pr(pj1yk)* forj = **1,2,3.** 
10.5 Consider the system described in Example **4.1** where the measurement consists of the predator population. Suppose that we want to estimate x(1) + **42),** the sum of the predator and prey populations. Create an equivalent system with transformed states such that our goal is to estimate the first element of the transformed state vector. 

10.6 Consider the system 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\left[\begin{array}{l l}{{0}}&{{1}}\\ {{0}}&{{0}}\end{array}\right]x_{k}+\left[\begin{array}{l}{{0}}\\ {{1}}\end{array}\right]w_{k}}}\\ {{y_{k}}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{0}}\end{array}\right]x_{k}+v_{k}}}\end{array}$$

where wk and Vk are uncorrelated zero-mean white noise processes with Variances q and R, respectively. 

a) Use Anderson's approach to reduced-order filtering to estimate the first element of the state vector. Find steady-state values for p, P, **C, fi,** fi, and P. Find the steady-state gain K of the reduced-order filter. 

b) Use the full-order filter to estimate the entire state vector. Find steadystate values for P and K. 

c) Comment on the comparison between your answer for P in part (a) and 
- - 
Consider the reduced-order filter of Example **10.3** with the initial condition Part (b). 

10.7 z+ 
P, =l. 

a) Find analytical expressions for the steady-state values of *I?,* a, p+, **C+,** 
P', *p-,* **C-,** and 3b) What does the reduced-order filter indicate for the steady-state a *posteriori* estimation-error variance of the first state? Find an analytical expression for the true steady-state a *posteriori* estimation-error variance of the first state when the reduced-order filter is used. Your answer should be a function of **~(2).** Solve for the true steady-state a *posteriori* estimationerror variance of the first state when **42)** = 0, when **42)** = 1, and when x(2) = 2. 

c) What is the steady-state a *posteriori* estimation-error variance of the first state when the full-order filter is used? 

10.8 Verify that the two expressions in Equation (10.98) are respectively equal to the cross-covariance of x and y, and the covariance of y. 

10.9 Suppose you have the linear system xk+l = **Fxk** + *wk,* where wk N (0, *Qk)* is zero-mean white noise. Define w(k + 2, *Ic)* as the cumulative effect of all of the process noise on the state from time k to time (k + **2).** What are the mean and covariance of w(k + 2, *k)?* 
10.10 Suppose that a Kalman filter is running with 

$$F\;\;=\;\;\left[\begin{array}{l l}{{1}}&{{1}}\\ {{0}}&{{1}}\end{array}\right]$$
$$\begin{array}{r c l}{{H}}&{{=}}&{{\left[\begin{array}{c c}{{1}}&{{0}}\end{array}\right]}}\\ {{}}&{{}}&{{}}\\ {{Q}}&{{=}}&{{\left[\begin{array}{c c}{{0}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]}}\\ {{}}&{{}}&{{}}\\ {{R}}&{{=}}&{{1}}\\ {{P^{+}(k)}}&{{=}}&{{\left[\begin{array}{c c}{{1/2}}&{{0}}\\ {{0}}&{{1}}\end{array}\right]}}\end{array}$$

An out-of-sequence measurement from time (k - 1) is received at the filter. 

a) What was the value of *P-(k)?* 
b) Use the delayed-measurement filter to find the quantities *Pw(k, k* - l), 
P,,(k, k - l), P(k - 1, *k), P,,(k, k* - l), and *P(k,* k - 1). 

c) Realizing that the measurement at time (k - 1) was not received at time 
(k - l), derive the value of P- (k - 1). Now suppose that the measurement was received in the correct sequence at time (k - 1). Use the standard Kalman filter equations to compute *P+(k* - l), *P-(k),* and *P+(k).* How does your computed value of *P+(k)* compare with the value of *P(k,* k - 1) 
that you computed in part (b) of this problem? 

10.11 Under what conditions will P, in Equation (10.100) be invertible for all k? 

## Computer Exercises

10.12 Consider the equations 

$$\begin{array}{r l}{={}}&{{}700}\\ {={}}&{{}233}\end{array}$$
$$300x+400y$$ $$100x+133y$$
300~+400y = 700 
lOO~+133y = 233 
a) What is the solution of these equations? 

b) What is the solution of these equations if each constant in the second equation increases by l? 

c) What is the condition number of the original set of equations? 

10.13 ,Repeat Problem 10.12 for the equations 

$$\begin{array}{r l}{300x+400y}&{{}=}\\ {100x+200y}&{{}=}\end{array}$$
$$700$$ $$200$$
300~+400y = 700 
1oox+2ooy = 200 
Comment on the difference between this set of equations and the set given in Problem 10.12. 

10.14 Tire tread is measured every r **weeks.** After r weeks, 20% of the tread has worn off, so we can model the dynamics of the tread height as Xk+1 = fXk + *Wk,* where f = 0.8, and Wk is zero-mean white noise with a variance of 0.01. We measure the tread height every T weeks with zero-mean white measurement noise that has a variance of 0.01. The initial tread height is known to be exactly 1 cm. Write a program to simulate the system and a Kalman filter to estimate the tread height. 

a) Run the program for 10 time steps per tire, and for 1000 tires. What is the mean of the 10,000 measurement residuals? 

b) Suppose the Kalman filter designer incorrectly believes that **30%** of the tread wears off every 7 weeks. What is the mean of the 10,000 measure ment residuals in this case? 

c) Suppose the Kalman filter designer incorrectly believes that 10% of the tread wears off every 7 weeks. What is the mean of the 10,000 measurement residuals in this case? 

10.15 Consider the system described in Problem 10.14. Suppose the engineer does not know the true value off but knows the initial probabilities Pr(f = 0.8) = 
Pr(f = 0.85) = Pr(f = 0.9) = **1/3.** Run the multiple-model estimator for 10 time steps on 100 tires to estimate f. The f probabilities at each time step can be taken as the mean of the 100 f probabilities that are obtained from the 100 tire simulations, and similarly for the f estimate at each time step. Plot the f probabilities and the f estimate as a function of time. 

10.16 Consider a scalar system with F = H = 1 and nominal noise variances Q = R = 5. The true but unknown noise variances Q and R are given as 

$$\begin{array}{r c l}{{\tilde{Q}}}&{{=}}&{{(1+\alpha)Q}}\\ {{\tilde{R}}}&{{=}}&{{(1+\beta)R}}\\ {{E(\alpha^{2})}}&{{=}}&{{\sigma_{1}^{2}=1/2}}\\ {{E(\beta^{2})}}&{{=}}&{{\sigma_{2}^{2}=1}}\end{array}$$

where a and P are independent zero-mean random variables. The variance of the a posteriori estimation error is P if a = P = 0. In general, a and P are nonzero and the variance of the estimation error is *P+ AP.* Plot *P, E(AP2),* and *(P+E(AP2))* 
as a function of K for K E **[0.3,0.7].** What are the minimizing values of K for the three plots? 

PART 111 

# The H, Filter

Optzmal State Estamataon, Fzrst *Edztzon.* By Dan J. Simon ISBN **0471708585** 02006 John Wiley li Sons. Inc. 