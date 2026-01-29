---
type: chapter
chapter: 12
title: Additional topics in H∞ filtering
---
# Chapter 12 Additional Topics In H, Filtering

Since [H, filters] make no assumption about the disturbances, they have to accommodate for all conceivable disturbances, and are thus over-conservative. 

-Babak Hassibi and Thomas Kailath [Has951 In this chapter we will briefly introduce some advanced topics in H, filtering. 

H, filtering was not introduced until the 1980s and is therefore considerably less mature than Kalman filtering. As such, there is more room for additional work and development in H, filtering than Kalman filtering. This chapter introduces some of the current directions of research in the area of H, filtering. 

Section 12.1 looks at the mixed Kalman/H, estimation problem. We present a filter that satisfies an H, performance bound while at the same time minimizing a Kalman performance bound. Section 12.2 looks at the robust mixed Kalman/H, estimation problem. This is the same as mixed Kalman/H, filtering but with the added complication of uncertainties in the system matrices. Section 12.3 discusses the solution of the constrained H, filter, where equality (or inequality) constraints are enforced on the state estimate. 

## 12.1 Mixed Kalman/H, Filtering

In this section we look at the problem of finding a filter that combines the best features of Kalman filtering with the best features of H, filtering. This problem can be attacked a couple of different ways. Recall from Section **5.2** the cost function that is minimized by the steady-state Kalman filter: 

$$J_{2}=\operatorname*{lim}_{N\rightarrow\infty}\sum_{k=0}^{N}E\left(||x_{k}-{\hat{x}}_{k}||_{2}\right)\tag{1}$$
$$(12.1)$$
$$(12.2)$$

Recall from Section **11.3** the cost function that is minimized by the steady-state H, state estimator if sk and Lk are identity matrices: 

$$J_{\infty}=\operatorname*{lim}_{N\to\infty}\operatorname*{max}_{x_{0},w_{k},v_{k}}{\frac{\sum_{k=0}^{N}||x_{k}-{\hat{x}}_{k}||^{2}}{||x(0)-{\hat{x}}(0)||_{P_{0}^{-1}}^{2}+\sum_{k=0}^{N}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||v_{k}||_{R_{k}^{-1}}^{2}\right)}}\quad.$$

Loosely speaking, the Kalman filter minimizes the RMS estimation error, and the H, filter minimizes the worst-case estimation error. 

In [Had911 these two performance objectives are combined to form the following problem: Given the n-state observable LTI system 

$$(12.3)$$
$$(12.4)$$

where **{Wk}** and *{Vk}* are uncorrelated zero-mean, white noise processes with covariances Q and R respectively, find an estimator of the form 

$T_{k}+1=F_{k}+w_{k}$  $y_{k}=H_{k}+v_{k}$
$${\hat{x}}_{k+1}={\hat{F}}x_{k}+K y_{k}$$
*k+l = PXk + *Kyk* **(12.4)** 
that satisfies the following criteria: 
1. F is a stable matrix (so the estimator is stable). 

2. The H, cost function is bounded by a user-specified parameter: 

$$J_{\infty}<{\frac{1}{\theta}}$$
$$\left(\mathbf{12.5}\right)$$. 
3. Among all estimators satisfying the above criteria, the filter minimizes the Kalman filter cost function *J2.* 
The solution to this problem provides the best RMS estimation error among all estimators that bound the worst-case estimation error. The filter that solves this problem is given as follows. 

## The Mixed Kalman/H, Filter

1. Find the n x n positive semidefinite matrix P that satisfies the following Riccati equation: 

$$P=FPF^{T}+Q+FP(I/\theta^{2}-P)^{-1}PF^{T}-P_{a}V^{-1}P_{a}^{T}\tag{12.6}$$

where Pa and V are defined as 

$$\begin{array}{r c l}{{P_{a}}}&{{=}}&{{F P H^{T}+F P(I/\theta^{2}-P)^{-1}P H^{T}}}\\ {{V}}&{{=}}&{{R+H P H^{T}+H P(I/\theta^{2}-P)^{-1}P H^{T}}}\end{array}\qquad\qquad0$$
$$(12.7)$$

2. Derive the F and K matrices in Equation (12.4) as 

K = P,V-'  F = F-KH 
$$(12.8)$$
$$(12.9)$$
3. The estimator of Equation (12.4) satisfies the mixed Kalman/H, estimation problem if and only if k is stable. In this case, the state estimation error satisfies the bound 

$$\operatorname*{lim}_{k\to\infty}E\left(||x_{k}-{\hat{x}}_{k}||^{2}\right)\leq\operatorname{Tr}(P)$$

Note that if 0 = 0, then the problem statement reduces to the Kalman filter problem statement. In this case we can see that Equation (12.6) reduces to the discrete-time algebraic Riccati equation that is associated with the Kalman filter 
(see Problem 12.2 and Section **7.3).** The continuous-time version of this theory is given in [Ber89]. 

## Example 12.1

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\end{array}$$

In this example, we take another look at the scalar system that is described in Example 11.2: 

$$(12.10)$$
$$(12.11)$$

where *{Wk}* and *{Vk}* are uncorrelated zero-mean, white noise processes with covariances Q and R, respectively. Equation (12.6), the Riccati equation for the mixed Kalman/H, filter, reduces to the following scalar equation: 

$$\theta^{2}(1-R\theta^{2})P^{3}+(Q\theta^{2}+1)(R\theta^{2}-1)P^{2}+Q(1-2R\theta^{2})+Q R=0$$

Suppose that (for some value of *Q, R,* and 8) this equation has a solution P 2 0, and 11 - KI < 1, where the filter gain K from Equation (12.8) is given as 

$$(12.12)$$
 $ K=\frac{P}{P+R-PR{{\theta}^{2}}}$  2.2) is bounded from above by $ 1/{{\theta}_{2}}$ and the ... 
Then J, from Equation (12.2) is bounded from above by l/O, and the variance of the state estimation error is bounded from above by P. The top half of Figure 12.1 shows the Kalman filter performance bound P and the estimator gain K as a function of 8 when Q = R = 1. Note that at 8 = 0 the mixed Kalman/H, filter reduces to a standard Kalman filter. In this case the performance bound P M 1.62 and the estimator gain K M 0.62, as discussed in Example 11.2. However, if 8 = 0 then we do not have any guarantee on the worst-case performance index *J,.* 
From the top half of Figure 12.1, we see that as 8 increases, the performance bound P increases, which means that our Kalman performance index gets worse. However, at the same time, the worst-case performance index J, 
decreases as 0 increases. From the bottom half of Figure 12.1, we see that as f3 increases, K increases, which is consistent with better H, performance and worse Kalman performance (see Example 11.2). When 0 reaches about 0.91, numerical difficulties prevent a solution to the mixed filter problem. 

The bottom half of Figure 12.1 shows that at f3 = 0.5 the estimator gain K M 0.76. Recall from Example 11.2 that the H, filter had an estimator gain K = 1 for the same value of 6. This shows that the mixed Kalman/H, 
filter has a smaller estimator gain (for the same 0) than the pure H, filter. 

In other words, the mixed filter uses a lower gain in order to obtain better Kalman performance, whereas the pure H, filter uses a higher gain because it does not take Kalman performance into account. 

![3_image_0.png](3_image_0.png)

Figure **12.1** Results for Example 12.1 of the estimation-error variance bound and estimator gain as a function of B for the mixed Kalman/H, filter. As B increases, the worst-case performance bound l/B decreases, the error-variance bound increases, and the estimator gain increases greater than the Kalman gain (0 = 0). This shows a trade-off between worst-case performance and RMS performance. 
vvv Although the approach presented above is a theoretically elegant method of obtaining a mixed Kalman/H, filter, the solution of the Riccati equation can be challenging for problems with a large number of states. Other more straightforward approaches can be used to combine the Kalman and H, filters. For example, if the steady-state Kalman filter gain for a given problem is denoted as Kz and the steady-state H, filter gain is denoted as K,, then a hybrid filter gain can be constructed as K = dK2 + (1 *-d)Km* **(12.13)** 
where d E [0,1]. This hybrid filter gain is a convex combination of the Kalman and H, filter gains, which would be expected to provide a balance between RMS and worst-case performance [Sim96]. However, this approach is not as attractive theoretically since stability must be determined numerically, and no a *priori* bounds on 

$$(12.14)$$

the Kalman or H, performance measures can be given. Analytical determination of stability and performance bounds for this type of filter is an open research issue. 

## 12.2 Robust Kalman/H, Filtering

The material in this section is based on [Hun03]. In most practical problems, an exact model of the system may not be available. The performance of the system in the presence of model uncertainties becomes an important issue. For example, suppose we have a system given as 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{(F_{k}+\Delta F_{k})x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{(H_{k}+\Delta H_{k})x_{k}+v_{k}}}\end{array}$$

where *{wk}* and *{Wk}* are uncorrelated zero-mean white noise processes with covariances Qk and *Rk,* respectively. Matrices **AFk** and *AH,* represent uncertainties in the system and measurement matrices. These uncertainties are assumed to be of the form 

$$(12.15)$$
$${\left[\begin{array}{l}{\Delta F_{k}}\\ {\Delta H_{k}}\end{array}\right]}={\left[\begin{array}{l}{M_{1k}}\\ {M_{2k}}\end{array}\right]}\,\Gamma_{k}N_{k}$$

where *Mlk, M2k,* and Nk are known matrices, and rk is an unknown matrix satisfying the bound r;rk 5 I **(12.16)** 
[Recall that we use the general notation A *5 B* to denote that (A - B) is a negative semidefinite matrix.] Assume that Fk is nonsingular. This assumption is not too restrictive; Fk should always be nonsingular for a real system because it comes from the matrix exponential of the system matrix of a continuous-time system, and the matrix exponential is always nonsingular (see Sections 1.2 and **1.4).** The problem is to design a state estimator of the form 

$$\Gamma_{k}^{T}\Gamma_{k}\leq I$$

$${\hat{x}}_{k+1}={\hat{F}}_{k}{\hat{x}}_{k}+K_{k}y_{k}$$

?k+l = kk?k -k *Kkyk* **(12.17)** 
with the following characteristics: 
1. The estimator is stable (i.e., the eigenvalues of Fk are less than one in magnitude). 

2. The estimation error zk satisfies the following worst-case bound: 

$$(12.16)$$
$$(12.17)$$

$$\max_{w_{k},v_{k}}\frac{||\tilde{x}_{k}||_{2}}{||w_{k}||_{2}+||v_{k}||_{2}+||\tilde{x}_{0}||_{S_{1}^{-1}}+||x_{0}||_{S_{2}^{-1}}}<\frac{1}{\theta}\tag{12.18}$$
$$(12.19)$$
$$E\left({\tilde{x}}_{k}{\tilde{x}}_{k}^{T}\right)<P_{k}$$

3. The estimation error 2k satisfies the following RMS bound: 
The solution to the problem can be found by the following procedure [HunOS]. 

## The Robust Mixed Kalman/H, Filter

1. Choose some scalar sequence *(Yk* > 0, and a small scalar e > 0. 

2. Define the following matrices: 

$$\begin{array}{r c l}{{R_{11k}}}&{{=}}&{{Q_{k}+\alpha_{k}M_{1k}M_{1k}^{T}}}\\ {{R_{12k}}}&{{=}}&{{\alpha_{k}M_{1k}M_{2k}^{T}}}\\ {{R_{22k}}}&{{=}}&{{R_{k}+\alpha_{k}M_{2k}M_{2k}^{T}}}\end{array}$$
$$\begin{array}{r c l}{{P_{0}}}&{{=}}&{{S_{1}}}\\ {{\tilde{P}_{0}}}&{{=}}&{{S_{2}}}\end{array}$$
$$(12.20)$$
$$F_{1k}T_{k}F_{1k}^{T}+R_{11k}+R_{11k}R_{2k}R_{11k}^{T}-$$ $$\left[F_{1k}T_{k}H_{1k}^{T}+R_{11k}R_{2k}R_{12k}+R_{12k}\right]R_{k}^{-1}\left[\cdots\right]^{T}+\epsilon I$$ $$F_{k}\tilde{P}_{k}F_{k}^{T}+F_{k}\tilde{P}_{k}N_{k}^{T}(\alpha_{k}I-N_{k}\tilde{P}_{k}N_{k}^{T})^{-1}N_{k}\tilde{P}_{k}F_{k}^{T}+$$ $$R_{11k}+\epsilon I\tag{2}$$

3. Initialize Pk and ijk as follows: 

$$(12.21)$$
$$\mathbf{\partial}^{-}$$
$$(12.23)$$

5. If the Riccati equation solutions satisfy 

$$\begin{array}{l l l}{{\frac{1}{\theta^{2}}I}}&{{>}}&{{P_{k}}}\\ {{\alpha_{k}I}}&{{>}}&{{N_{k}\tilde{P}_{k}N_{k}^{T}}}\end{array}$$
$$(12.24)$$
$$(12.25)$$
$$\begin{array}{r c l}{{K_{k}}}&{{=}}&{{\left[F_{1k}T_{k}H_{1k}^{T}+R_{11k}R_{2k}R_{12k}+R_{12k}\right]\tilde{R}_{k}^{-1}}}\\ {{\tilde{R}_{k}}}&{{=}}&{{H_{1k}T_{k}H_{1k}^{T}+R_{12k}^{T}R_{2k}R_{12k}+R_{22k}}}\\ {{\tilde{F}_{k}}}&{{=}}&{{F_{1k}-K_{k}H_{1k}}}\end{array}$$

then the estimator of Equation **(12.17)** solves the problem with The parameter e is generally chosen as a very small positive number. In the example in [Hun031 the value is e = The parameter Qk **has** to be chosen large enough so that the conditions of Equation **(12.24)** are satisfied. However, as *(Yk* increases, Pk also increases, which results in a looser bound on the RMS estimation error. 

A steady-state robust filter can be obtained by letting *Pk+l* = Pk and &+I = *ijk* in Equation *(12.22)* and removing all the time subscripts (assuming that the system is time-invariant). But the resulting coupled steady-state Riccati equations will be more difficult to solve than the discretetime Riccati equations in Equation *(12.22),* which can be solved by a simple (albeit tedious) iterative process. Similar problems have been solved in [MahO4b, Xie04, Yo0041. 

## Example 12.2

Suppose we have an angular positioning system such as a motor. The moment of inertia of the motor and its load is J and the coefficient of viscous friction is B. The torque that is applied to the motor is **CZL+** w, where u is the applied voltage, c is a motor constant that relates applied voltage to generated torque, and w is unmodeled torque that can be considered as noise. The differential equation for this system is given as 

$$J{\ddot{\phi}}+B{\dot{\phi}}=c u+w$$
$$(12.26)$$

where 4 is the motor shaft angle. We choose the states as *x(1)* = q5 and x(2) = 4. The dynamic system model can then be written as 

$$\dot{x}=Ax+B_{u}u+B_{w}w\tag{12.27}$$ $$=\left[\begin{array}{cc}0&1\\ 0&-B/J\end{array}\right]x+\left[\begin{array}{c}0\\ c/J\end{array}\right]u+\left[\begin{array}{c}0\\ 1/J\end{array}\right]w$$

In order to discretize the system with a sample time T, we use the method of Section **1.4** to obtain The discretetime system matrices are given as 

$$(12.28)$$
$$x_{k+1}=F x_{k}+G_{u}u_{k}+G_{w}w_{k}$$

$$\begin{array}{r c l}{{F}}&{{=}}&{{\exp(A T)}}\\ {{G_{u}}}&{{=}}&{{\int_{0}^{T}\exp(A t)\,d t\,B_{u}}}\\ {{}}&{{=}}&{{\frac{c}{B}\left[\begin{array}{c}{{T-1/\alpha+e^{-\alpha T}/\alpha}}\\ {{1-e^{-\alpha T}}}\end{array}\right]}}\\ {{G_{w}}}&{{=}}&{{\frac{1}{B}\left[\begin{array}{c}{{T-1/\alpha+e^{-\alpha T}/\alpha}}\\ {{1-e^{-\alpha T}}}\end{array}\right]}}\\ {{\alpha}}&{{=}}&{{\frac{B}{J}}}\end{array}$$
$$(12.29)$$

If our measurement is angular position q5 corrupted by noise, then our measurement equation can be written as 

$$y_{k}={\left[\begin{array}{l l}{1}&{0}\end{array}\right]}\,x_{k}+v_{k}$$
$$(12.30)$$
Yk= [ 1 0 *]xkfvk (12.30)* 
Suppose the system has a torque disturbance Wk with a standard deviation of 2, and a measurement noise Vk with a standard deviation of *0.2* degrees. We can run the Kalman filter and the robust mixed Kalman/H, filter for this problem. Figure **12.2** shows the position and velocity estimation errors of the Kalman and robust mixed Kalman/H, filters. The robust filter performs better at the beginning of the simulation, although the Kalman filter performs better in steady state. (It is not easy to see the advantage of Kalman filter during steady state in Figure **12.2** because of the scale, but over the last half of the plot the Kalman filter estimation errors have standard deviations of 0.33 deg and **1.65** deg/s, whereas the robust filter has standard deviations of 0.36 deg and **4.83** deg/s.) 
Now suppose that the moment of inertia of the motor changes by a factor of 100. That is, the filter assumes that J is **100** times greater than it really is. 

In this, case Figure **12.3** shows the position and velocity estimation errors of the Kalman and robust filters. It is apparent that in this case the robust filter performs better not only at the beginning of the simulation, but in steady state also. After the filters reach "steady state" (which we have defined somewhat arbitrarily as the time at which the position estimation error magnitude falls below 1 degree) the Kalman filter RMS estimation errors are **0.36** degrees for position and **1.33** degrees/s for velocity, whereas the robust filter RMS estimation errors are **0.28** degrees for position and **1.29** degrees/s for velocity. The square roots of the diagonal elements of the Pk Riccati equation solution of Equation **(12.22)** reach steady-state values of **0.51** degrees and **1.52** degrees/s, which shows that the estimation-error variance is indeed bounded by the Riccati equation solution 4. 

![7_image_0.png](7_image_0.png)

Figure **12.2** Position and velocity estimation errors for Example **12.2** for the Kalman filter and the robust filter, assuming that the system model is perfectly known. The robust filter performs better at the beginning of the simulation, but the Kalman filter performs better in steady state. The steady-state Kalman filter estimation errors have standard deviations of 0.33 deg and 1.65 deg/s, whereas the robust filter has standard deviations of 0.36 deg and 4.83 deg/s. 

![8_image_0.png](8_image_0.png)

Figure **12.3** Position and velocity estimation errors for Example **12.2** for the **Kalman** 
filter and the robust filter, assuming that the system model is not well known. The robust filter performs better both at the beginning of the simulation and in steady state. The steady-state Kalman filter estimation errors have standard deviations of **0.36** deg and **1.33** degls, whereas the robust filter has standard deviations of 0.28 deg and 1.29 deg/s. 

## 12.3 Constrained H, Filtering

As in Section **7.5,** suppose that we know (on the basis of physical considerations) 
that the states satisfy some equality constraint DkXk = *dk,* or some inequality constraint Dkxk 5 *dk,* where Dk is a known matrix and dk is a known vector. 

This section discusses how those constraints can be incorporated into the H, filter equations. As discussed in Section **7.5,** state equality constraints can always be handled by reducing the system-model parameterization [Wen92], or by treating state equality constraints as perfect measurements [Por88, Hay981. However, these approaches cannot be extended to inequality constraints. The approach summ& rized in this section is to incorporate the state constraints into the derivation of the H, filter [SimOGc]. 

Consider the discrete LTI system given by 

$$\begin{array}{rcl}\mathcal{I}_{k+1}&=&Fx_{k}+w_{k}+\delta_{k}\\ \mathcal{I}_{k}&=&Hx_{k}+v_{k}\end{array}\tag{12.31}$$

where Yk is the measurement, *{Wk}* and *{Vk}* are uncorrelated white noise sequences with respective covariances Q and I, and *(6k)* is a noise sequence generated by an adversary (i.e., nature). Note that we are assuming that the measurement noise has a unity covariance matrix. In a real system, if the measurement noise covariance is not equal to the identity matrix, then we will have to normalize the measurement equation as shown in Example **12.3** below. In general, F, H, and Q can be timevarying matrices, but we will omit the time subscript on these matrices for ease of notation. In addition to the state equation, we know (on the basis of physical considerations or other a *priori* information) that the states satisfy the following constraint: 

$$D_{k}x_{k}=d_{k}$$

DkXk = dk (12.32) 
We assume that the Dk matrix is full rank and normalized so that *DkDT* = I. 

In general, Dk is an s x n matrix, where s is the number of constraints, n is the number of states, and s < n. If s = n then Equation (12.32) completely defines *Xk,* which makes the estimation problem trivial (i.e., 2k = *Dk'dk).* For s < n, which is the case in this section, there are fewer constraints than states, which makes the estimation problem nontrivial. Assuming that Dk is full rank is the same as the assumption made in the constrained Kalman filtering problem of Section 7.5. For notational convenience we define the matrix vk as fi = *DrDk* (12.33) 
We assume that both the noisy system and the noise-free system satisfy the state constraint. The problem is to find an estimate 2k+l Of *Xk+l* given the measurements 
{yl, **y2,.** . . , *gk}.* The estimate should satisfy the state constraint. We will assume that the estimate is given by the following standard predictor/corrector form: 

$$V_{k}=D_{k}^{T}D_{k}$$
$$(12.33)$$

$$\begin{array}{r c l}{{\hat{x}_{0}}}&{{=}}&{{0}}\\ {{\hat{x}_{k+1}}}&{{=}}&{{F\hat{x}_{k}+K_{k}(y_{k}-H\hat{x}_{k})}}\end{array}$$
$$(12.34)$$
$$\delta_{k}=L_{k}[G_{k}(x_{k}-{\hat{x}}_{k})+n_{k}]$$
$$(12.35)$$

The noise bk in (12.31) is introduced by an adversary that has the goal of maximizing the estimation error. We will assume that our adversary's input to the system is given as follows: 
bk = Lk [Gk(xk - 2k) + *nk]* (1 2.35) 
where Lk is a gain to be determined, Gk is a given matrix, and *{nk}* is a noise sequence with variance equal to the identity matrix. We assume that *{nk}* is uncorrelated with *{Wk}, {Vk},* and **20.** This form of the adversary's input is not intuitive because it is based on the state estimation error, but this form is taken because the solution of the resulting problem results in a state estimator that bounds the infinity-norm of the transfer function from the random noise terms to the state estimation error [Yae92]. 

Gk in Equation (12.35) is chosen by the designer as a tuning parameter or weighting matrix that can be adjusted on the basis of our a *priori* knowledge about the adversary's noise input. Suppose, for example, that we know ahead of time that the first component of the adversary's noise input to the system is twice the magnitude of the second component, the third component is zero, and so on; then that information can be reflected in the designer's choice of **Gk.** We do not need to make any assumptions about the form of Gk (e.g., it does not need to be positive definite or square). From Equation (12.35) we see that as Gk approaches the zero matrix, the adversary's input becomes a purely random process without any deterministic component. This causes the resulting filter to approach the Kalman filter; that is, we obtain better RMS error performance but poorer worst-case error performance. As Gk becomes large, the filter places more emphasis on minimizing the estimation error due to the deterministic component of the adversary's input. That is, the filter assumes less about the adversary's input, and we obtain better worst-case error performance but worse RMS error performance. The estimation error is defined as 

$$(12.36)$$
$$e_{k}=x_{k}-{\hat{x}}_{k}$$
ek = xk - Pk ( 12.36) 
It can be shown from the preceding equations that the dynamic system describing the estimation error is given as 

$$e_{0}=x_{0}$$ $$e_{k+1}=(F-K_{k}H+L_{k}G_{k})e_{k}+w_{k}+L_{k}n_{k}-K_{k}v_{k}\tag{12.37}$$  $\alpha$ _and_ $\alpha$ _are that $D$ _is_ $\alpha$ _but it can also be shown [Stern 06]._
Since *DkZk* = Dkkk = *dk,* we see that *Dkek* = 0. But it can also be shown [SimOGc] 
that *Dk+lFek* = 0. Therefore, we can subtract the zero term *DT+lDk+lFek* = 
Vk+lFek from Equation (12.37) to obtain 

$$e_{0}=x_{0}$$ $$e_{k+1}=[(I-V_{k+1})F-K_{k}H+L_{k}G_{k}]e_{k}+w_{k}+L_{k}n_{k}-K_{k}v_{k}\tag{12.38}$$  However, this is an inappropriate term for a minimax problem because the adver
sary can arbitrarily increase ek by arbitrarily increasing *Lk.* To prevent this, we 
decompose ek as 
where *e1,k* and **e2,k** evolve as follows: 
$$e_{k}=e_{1,k}+e_{2,k}$$
$$(12.39)$$
$$e_{1,0}=x_{0}$$ $$e_{1,k}=[(I-V_{k+1})F-K_{k}H+L_{k}Gk]e_{1,k}+w_{k}-K_{k}v_{k}$$ $$e_{2,0}=0$$ $$e_{2,k}=[(I-V_{k+1})F-K_{k}H+L_{k}G_{k}]e_{2,k}+L_{k}n_{k}$$  We define the objective function for the filtering problem as 
$$J(K,L)=\mbox{trace}\sum_{k=0}^{N}W_{k}E\left(e_{1,k}e_{1,k}^{T}-e_{2,k}e_{2,k}^{T}\right)\tag{12.41}$$  **notice definite** **multi** **multi** **The differential** **same** **is** **for**
where wk is any positive definite weighting matrix. The differential game is for the filter designer to find a gain sequence **{Kk}** that minimizes J, and for the adversary to find a gain sequence *{Lk}* that maximizes J. As such, J is considered a function of *{Kk}* and *{Lk},* which we denote in shorthand notation as K *and* L. 

This objective function is not intuitive, but is used here because the solution of the problem results in a state estimator that bounds the infinity-norm of the transfer function from the random noise terms to the state estimation error [Yae92]. That is, suppose we can find an estimator gain K* that minimizes J( *K, L)* when the matrix Gk in (12.35) is equal to 01 for some positive scalar 0. Then the infinity-norm of the weighted transfer function from the noise terms Wk and Vk to the estimation error ek is bounded by 110. That is, 

$$(12.40)$$
$$(12.42)$$

where sup stands for *suprernum.l* The filtering solution is obtained by finding optimal gain sequences {Kl} and *{L;}* that satisfy the following saddle point: 

$\sup\limits_{\begin{subarray}{c}\sum_{k=0}^{N}e_{k}^{T}e_{k}\\ w_{k},v_{k}\end{subarray}}\frac{\sum_{k=0}^{N}\left(w_{k}^{T}Q^{-1}w_{k}+v_{k}^{T}v_{k}\right)}{\sum_{k=0}^{N}\left(w_{k}^{T}Q^{-1}w_{k}+v_{k}^{T}v_{k}\right)}<\frac{1}{\theta}$  _commere 1_. The filtering solution is obtained by 
$$J(K^{*},L)\leq J(K^{*},L^{*})\leq J(K,L^{*}){\mathrm{~for~all~}}K,L$$
(12.43) 

'The supremum of a function is its least upper bound. This is similar to the maximum of a function, but a maximum is a value that is actually attained by a function, whereas a supremum may or may not be attained. For example, the supremum of (1 - **e-")** is 1, but (1 - **e-=)** never actually reaches the value 1. Similar distinctions hold for the operators minimum and infimum 
(usually abbreviated *2nd.* 
This problem is solved subject to the constraint that *Dk5k* = dk in [SimOGc], whose result is presented here. We define Pk *and* & as the nonsingular solutions to the following set of equations: 

$$\begin{array}{r c l}{{P_{0}}}&{{=}}&{{E(x_{0}x_{0}^{T})}}\\ {{\Sigma_{k}}}&{{=}}&{{(P_{k}H^{T}H-P_{k}G_{k}^{T}G_{k}+I)^{-1}P_{k}}}\\ {{P_{k+1}}}&{{=}}&{{(I-V_{k+1})F\Sigma_{k}F^{T}(I-V_{k+1})+Q}}\end{array}$$
$$\begin{array}{l c l}{{K_{k}^{*}}}&{{=}}&{{(I-V_{k+1})F\Sigma_{k}H^{T}}}\\ {{L_{k}^{*}}}&{{=}}&{{(I-V_{k+1})F\Sigma_{k}G_{k}^{T}}}\end{array}$$

Nonsingular solutions to these equations are not always guaranteed to exist, in which case a solution to the H, filtering problem may not exist. However, if nonsingular solutions do exist, then the following gain matrices for our estimator and adversary satisfy the constrained H, filtering problem: 

$$(12.44)$$
$$(12.45)$$
$$(12.46)$$

These matrices solve the constrained H, filtering problem only if *(I-GkPkG;)* 2 0. 

Note that as Gk becomes larger, we will be less likely to satisfy this condition. Fkom Equation (12.35) we see that a larger Gk gives the adversary more latitude in choosing a disturbance. This makes it less likely that the designer can minimize the cost function. 

The mean square estimation error that results from using the optimal gain K; 
cannot be specified because it depends on the adversary's input *6k.* However, we can state an upper bound for the mean square estimation error [SimOGc] as follows: 

$$E\left[(x_{k}-{\hat{x}}_{k})(x_{k}-{\hat{x}}_{k})^{T}\right]\leq P_{k}$$

This provides additional motivation for using the game theory approach presented in this section. The estimator not only bounds the worst-case estimation error, but also bounds the mean square estimation error. 

Now consider the special case that there are no state constraints. Then in Equ& 
tion (12.32) we can set the Dk matrix equal to a zero row vector and the dk vector equal to the zero scalar. In this case *vk+1* = 0 and we obtain from Equations (12.44) 
and (12.45) the following estimator and adversary strategies: 

$$\begin{array}{r c l}{{}}&{{}}&{{P_{0}}}&{{=}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{P_{k}(I-H^{T}H\Sigma_{k})}}&{{=}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\end{array}$$
Po = E(ZOZ;) 
Pk(I- HTH&) = (I - PkGrGk)& 
pk+1 = *FCkFT+Q* 
KE = *FCkCT* 
$E(x_{0}x_{0}^{T})$  $(I-P_{k}G_{k}^{T}G_{k})\Sigma_{k}$  $F\Sigma_{k}F^{T}+Q$  $F\Sigma_{k}C^{T}$  $F\Sigma_{k}G_{k}^{T}$
This is identical to the unconstrained H, estimator [Yae92]. The unconstrained H, estimator for continuous-time systems is given in [YaeO4]. 

In the case of state inequality constraints (i-e., constraints of the form DkXk 5 dk), a standard activeset method [Fle81, Gi1811 can be used to solve the H, filtering problem. An activeset method uses the fact that it is only those constraints that are active at the solution of the problem that affect the optimality conditions; the inactive constraints can be ignored. Therefore, an inequality-constrained problem is equivalent to an equality-constrained problem. An activeset method determines which constraints are active at the solution of the problem and then solves the problem using the active constraints as equality constraints. Inequality constraints will significantly increase the computational effort required for a problem solution because the active constraints need to be determined, but conceptually this poses no difficulty. 

## The Constrained H, Filter

The constrained H, filter can be summarized as follows. 

1. We have a linear system given as 

$$\begin{array}{l}{{F_{k}x_{k}+w_{k}}}\\ {{H_{k}x_{k}+v_{k}}}\\ {{d_{k}}}\end{array}$$
$$\begin{array}{r l}{x_{k+1}}&{{}=}\\ {y_{k}}&{{}=}\\ {D_{k}x_{k}}&{{}=}\end{array}$$
xk+l = *Fkxk+wk* 
$$\begin{array}{r l}{{\hat{x}}_{0}}&{{}=}\\ {P_{0}}&{{}=}\end{array}$$
Yk = Hkxk+vk 
DkXk = dk (12.48) 
where Wk is the process noise, Vk is the measurement noise, and the last equation above specifies equality constraints on the state. We assume that the constraints are normalized so *DkDT* = I. The covariance of Wk is equal to Qk, *but* Wk might have a zero mean or it might have a nonzero mean (i.e., it might contain a deterministic component). The covariance of vk is the identity matrix. 

2. Initialize the filter as follows: 

$$(12.48)$$
$$\begin{array}{l}{{0}}\\ {{E(x_{0}x_{0}^{T})}}\end{array}$$
$$(12.49)$$

3. At each time step k = O,l,. ., do the following. 

$D_{k}^{T}D_{k}$  $(P_{k}H_{k}^{T}H_{k}-P_{k}G_{k}^{T}G_{k}+I)^{-1}P_{k}$  $(I-V_{k+1})F_{k}\Sigma_{k}F_{k}^{T}(I-V_{k+1})+Q_{k}$  $(I-V_{k+1})F_{k}\Sigma_{k}H_{k}^{T}$  $F_{k}\hat{x}_{k}+K_{k}(y_{k}-H_{k}\hat{x}_{k})$
(a) Choose the tuning parameter matrix Gk to weight the deterministic, biased component of the process noise. If Gk = 0 then we are assuming that the process noise is zero-mean and we get Kalman filter performance. As Gk increases we are assuming that there is more of a deterministic, biased component to the process noise. This gives us better worst-case error performance but worse RMS error performance. 

(b) Compute the next state estimate as follows: 

$$(12.50)$$
$$\begin{array}{r l}{V_{k}}&{{}=}\\ {\Sigma_{k}}&{{}=}\\ {P_{k+1}}&{{}=}\\ {K_{k}}&{{}=}\\ {\hat{x}_{k+1}}&{{}=}\end{array}$$
$$\mathrm{(c)~Verify~that}$$
If not then the filter is invalid. 
$$(I-G_{k}P_{k}G_{k}^{T})\geq0$$
$$(12.51)$$

## Example 12.3

Consider a land-based vehicle that is equipped to measure its latitude and longitude (e.g., through the use of a GPS receiver). This is the same problem as that considered in Example 7.12. The vehicle dynamics and measurements can be approximated by the following equations: 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\\ {{0}}\end{array}\right]}}\\ {{y_{k}^{\prime}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]}}\end{array}$$
$$\left[\begin{array}{c c c}{{0}}&{{T}}&{{0}}\\ {{1}}&{{0}}&{{T}}\\ {{0}}&{{1}}&{{0}}\\ {{0}}&{{0}}&{{1}}\end{array}\right]x_{k}+\left[\begin{array}{c c}{{0}}\\ {{0}}\\ {{T\sin\alpha}}\\ {{T\cos\alpha}}\end{array}\right]u_{k}+w_{k}+\delta_{k}$$

The first two components of Xk are the latitude and longitude positions, the last two components of Xk are the latitude and longitude velocities, Wk represents zero-mean process noise due to potholes and other disturbances, 6k is additional unknown process noise, and Uk is the commanded acceleration. 

T is the sample period of the system, and a is the heading angle (measured counterclockwise from due east). The measurement yk consists of latitude and longitude, and *TJ(,* is the measurement noise. Suppose the standard deviations of the measurement noises are known to be cq and **172.** Then we must normalize our measurement equation to satisfy the condition that the me& 
surement noise has a unity covariance. We therefore define the normalized measurement Yk as 

$$(12.52)$$
$$(12.53)$$
$$(12.54)$$

In our simulation we set the covariances of the process and measurement noise as follows: 

$$y_{k}={\left[\begin{array}{l l}{\sigma_{1}}&{0}\\ {0}&{\sigma_{2}}\end{array}\right]}^{-1}y_{k}^{\prime}$$
$$\begin{array}{l l l}{{Q}}&{{=}}&{{\mathrm{Diag}(4~\mathrm{m}^{2},4~\mathrm{m}^{2},1~{\left(\mathrm{m}/\mathrm{s}\right)}^{2},1~{\left(\mathrm{m}/\mathrm{s}\right)}^{2})}}\\ {{R}}&{{=}}&{{\mathrm{Diag}(\sigma_{1}^{2},\sigma_{2}^{2})=\mathrm{Diag}(900~\mathrm{m}^{2},900~\mathrm{m}^{2})}}\end{array}$$

We can use an H, filter to estimate the position of the vehicle. There may be times when the vehicle is traveling off-road, or on an unknown road, in which case the problem is unconstrained. At other times it may be known that the vehicle is traveling on a given road, in which case the state estimation problem is constrained. For instance, if it is known that the vehicle is traveling on a straight road with a heading of a then the matrix Dk and the vector dk of Equation (12.32) can be given as follows: 

$$D_{k}=\left[\begin{array}{cccc}1&-\tan\alpha&0&0\\ 0&0&1&-\tan\alpha\end{array}\right]$$ $$d_{k}=\left[\begin{array}{cc}0&0\end{array}\right]^{T}\tag{12.55}$$

We can enforce the condition *DkDr* = I by dividing Dk by dl + tan2 a. In our simulation we set the sample period T to 1 s and the heading angle cy to a constant 60 degrees. The commanded acceleration is toggled between 

ltl0 m/s2, as if the vehicle were accelerating and decelerating in traffic. The initial conditions are set to 

$$(12.56)$$
$$x_{0}={\left[\begin{array}{l l l l}{0}&{0}&{173}&{100}\end{array}\right]}^{T}$$

We found via tuning that a Gk matrix of *@I,* with 0 = 1/40, gave good filter performance. Smaller values of B make. the H, filter perform like a Kalman filter. Larger values of 0 prevent the H, filter from finding a solution as the positive definite conditions in Equations (12.44) and (12.45) are not satisfied. 

This example could be solved by reducing the system-model parameterization [Wen92], or by introducing artificial perfect measurements into the problem [Hay98, Por881. In fact, those methods could be used for any estimation problem with equality constraints. However, those methods cannot be extended to inequality constraints, whereas the method discussed in this section can be extended to inequality constraints, as discussed earlier. 

The unconstrained and constrained H, filters were simulated 100 times each, and the average RMS position and estimation error magnitudes at each time step are plotted in Figure 12.4. It can be seen that the constrained filter results in more accurate estimates. The unconstrained estimator results in position errors that average 35.3 m, whereas the constrained estimator gives position errors that average about 27.1 m. The unconstrained velocity estimation error is 12.9 m/s, whereas the constrained velocity estimation error is 10.9 m/s. 

Table 12.1 shows a comparison of the unconstrained and constrained Kalman and H, filters when the noise statistics are nominal. Table 12.2 shows a comparison of the unconstrained and constrained Kalman and H, filters when the acceleration noise on the system has a bias of 1 m/s2 in both the north and east directions. In both situations, the H, filter estimates position more accurately, but the Kalman filter estimates velocity more accurately. In the off-nominal noise case, the advantage of the H, filter over the Kalman filter for position estimation is more pronounced than when the noise is nominal. 

Table **12.1** Example **12.3** estimation errors (averaged over 100 Monte Carlo simulations) of the unconstrained and constrained Kalman and H, filters with nominal noise statistics. The H, filters perform better for position estimation, and the Kalman filters perform better for velocity estimation. Position errors are in units of meters, and velocity errors are in units of meters/second. 

| Kalman        | H,   |      |      |      |
|---------------|------|------|------|------|
| Pos.          | Vel. | Pos. | Vel. |      |
| Unconstrained | 40.3 | 12.4 | 35.3 | 12.9 |
| Constrained   | 33.2 | 10.4 | 27.1 | 10.9 |

## Vvv

Table 12.2 Example **12.3** estimation errors (averaged over 100 Monte Carlo simulations) of the unconstrained and constrained Kalman and H, filters with off-nominal noise statistics. The H, filters perform better for position estimation, and the Kalman filters perform better for velocity estimation. Position errors are in units of meters, and velocity errors are in units of meters/second. 

| Kalman        | H,   |           |      |      |
|---------------|------|-----------|------|------|
| Pos.          | Vel. | Pos.      | Vel. |      |
| Unconstrained | 60.8 | 19.2 45.9 | 20.6 |      |
| Constrained   | 56.2 | 17.6      | 39.1 | 19.1 |

![15_image_0.png](15_image_0.png)

Figure **12.4** Example **12.3** unconstrained and constrained H, filter estimation-error magnitudes. The plots show the average estimation-error magnitudes of **100** Monte Carlo simulations when the noise statistics are nominal. 

## 12.4 Summary

In this chapter we briefly introduced some advanced topics in the area of H, 
filtering. We discussed an approach for minimizing a combination of the Kalman and H, filter performance indices. This provides a way to balance the excessive optimism of the Kalman filter with the excessive pessimism of the H, filter. We also looked at the robust mixed Kalman/H, estimation problem, where we took system-model uncertainties into account. This is an important problem because 
(in practice) the system model is never perfectly known. Finally we discussed constrained H, filtering, in which equality (or inequality) constraints are enforced on the state estimate. This can improve filter performance in cases in which we know that the state must satisfy certain constraints. 

There is still a lot of room for additional work and development in H, filtering. 

For example, reduced-order H, filtering tries to obtain good minimax estimation performance with a filter whose order is less than that of the underlying system. 

Reduced-order Kalman filtering was discussed in Section 10.3, and reduced-order H, filtering is considered in [Bet94, Gri97, Xu021. The approach taken in [Ko06] 
for constrained Kalman filtering may be applicable to constrained H, filtering and may give better results than the method discussed in this chapter. The use of Krein space approaches for solving various H, filtering problems is promising [Has96a, Has96bl. H, smoothing is discussed in [Grigla, The94b, Has99, Zha05a1, and robust H, smoothing is discussed in [The94a]. An information form for the H, filter 
(analogous to the Kalman information filter discussed in Section 6.2) is presented in jZha05bI. Approaches to dealing with delayed measurements and synchronization errors have been extensively explored for Kalman filters (see Section 10.5), but are notably absent in the H, filter literature. There has been a lot of work on nonlinear Kalman filtering (see Chapters 13-15), but not nearly as much on nonlinear H, filtering. 

## Problems Written Exercises

12.1 Consider the system described in Example 12.1 with Q = R = 1. 

a) Find the steady-state a *priori* estimation-error variance P as a function of the estimator gain K. 

b) Find I /GseI&, the square of the infinity-norm of the transfer function from the noise w and v to the a *priori* state estimation error 2, as a function of the estimator gain K. 

c) Find the estimator gain K that minimizes (P + **I/GseI** I&). 

Verify that if 8 = 0, the Riccati equation associated with the mixed Kalman/H, 
12.2 filter in Equation (12.6) reduces to the Riccati equation associated with the Kalman filter. 

12.3 Suppose that the hybrid filter gain of Equation (12.13) is used for the system of Example 12.1 with 0 = 1/2. For what values of d will the hybrid filter be stable? 

12.4 Suppose that the robust filter of Section 12.2 is used for a system with n states and T measurements. What are the dimensions of *MI, Mz,* **l?,** and N? 

12.5 Suppose that a system matrix is given as 

$$F=\left[\begin{array}{c c}{{0.4\pm0.2}}&{{0.4}}\\ {{-0.4}}&{{1}}\end{array}\right]$$

(Note that this is the system matrix of Example 4.1 in case the effect of overcrowding on the predator population is uncertain.) Give an MI and N matrix that satisfy Equation (12.15) for this uncertainty. 

12.6 Consider an uncertain system with F = -1, H = 1, Q = R = 1, MI = 1/5, Mz = 0, and N = 1. Suppose that E = 0 is used to design a robust mixed Kalman/H, filter. 

a) For what values of a will the steady-state value of in Equation (12.22) 
be real and positive? 

b) For what values of a will the steady-state value of condition of Equation (12.24)? 

satisfy the second 12.7 Consider a constrained H, state estimation problem with 

$$F\;\;=\;\;\left[\begin{array}{c c}{{1}}&{{1/2}}\\ {{1/2}}&{{0}}\end{array}\right]$$
$$G=H$$
$$\left[\begin{array}{l l}{G_{1}}&{0}\end{array}\right]$$
$\equiv$ . 
$$D\quad=$$
$$\left[\begin{array}{l l}{{1}}&{{\mathrm{\boldmath~1~}}}\\ {{1}}&{{\mathrm{\boldmath~1~}}}\end{array}\right],$$
$$\begin{array}{r l}{Q}&{{}=}\end{array}$$
G=H = *[GI 0]* 
D = [l 11 
Find the steady-state constrained Riccati solution for P from Equation (12.50). 

For what values of G1 will the condition of Equation (12.51) be satisfied? 

## Computer **Exercises**

12.8 T = 1, a = 1, and R = 1. 

Consider a two-state Newtonian system as discussed in Example 9.1 with a) What is the steady-state Kalman gain? 

b) What is the maximum 0 for which the H, estimator exists? Answer to the nearest 0.01. What is the H, gain for this value of 0? 

c) What is the H, gain when B = 0.5? Plot the maximum estimator eigenvalue magnitude as a function of d for the hybrid filter of Equation (12.13) 
when 0 = 0.5. 

Implement the timevarying Riccati equations for the robust mixed KaIman/H, 
12.9 filter for F = 1/2, H = Q = R = 1, MI = 1/4, M2 = 0, N = 1, E = 0, 0 = 1/10, and S1 = S2 = 1. 

a) At what time do the conditions of Equation (12.24) fail to ,be satisfied when Q = 2? Repeat for a = 3, 4, 5, and 6. 

b) What is the steady-state theoretical bound on the estimation error when Q = lo? Repeat for a = **20,** 30, and 40. 

Consider a constrained H, state estimation problem with 12.10 

$$F\quad=\quad\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]$$
 $\blacksquare$
$\mathbf{l}$
[: :] 
H = [l 01 
$\begin{array}{c}\overleftarrow{\left[\begin{array}{c}1\\ 5\end{array}\right]}\end{array}$
$$H\quad=\quad$$
$$\mathbf{0}$$
$$G\;\;=\;\;\stackrel{\cdot}{[}\;G_{1}$$
$=\;\frac{1}{2}$
$\left[\begin{array}{l}\frac{1}{2}\end{array}\right]$
$$\mathbf{D}$$
D = [l 11 
G = *[GI* 01 
$$\mathbf{0}$$
$\mathbf{l}$. 
$$Q\;\;=\;\;\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]$$
$$\begin{array}{c}{{0}}\\ {{1}}\end{array}$$

Implement the Ck and Pk expressions from Equation (12.50). 

a) What is the largest value of GI for which Pk reaches a positive definite steady-state solution that satisfies the condition given in Equation (12.51)? 

Answer to the nearest 0.01. What is the resulting steady-state value of P? 

b) Set GI equal to 1% of the maximum G1 that you found in part (a). What is the new steady-state value of P? Give an intuitive explanation for why P gets smaller when G1 gets smaller. 

PART IV 

# Nonlinear Filters

Optzmal State Estamataon, Fzrst *Edztzon.* By Dan J. Simon ISBN **0471708585** 02006 John Wiley li Sons. Inc. 