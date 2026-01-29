---
type: chapter
chapter: 15
title: The particle filter
---
# Chapter 15 The Particle Filter

In view of all that we have said in the foregoing sections, the many obstacles we appear to have surmounted, what casts the pall over our victory celebration? It is the curse of dimensionality, a malediction that has plagued the scientist from earliest days. 

--Richard Bellman [Be1611 We want now to point out that modern computing machines are extremely well suited to perform the procedures described. 

-Nicholas Metropolis and S. **Ulam** [Met491 Particle filters had their beginnings in the 1940s with the work of Metropolis, and Norbert Wiener suggested something much like particle filtering as early as 1940 [Wie56]. But only since the 1980s has computational power been adequate for their implementation. Even now it is the computational burden of the particle filter that is its primary obstacle to more widespread use. The particle filter is a statistical, brute-force approach to estimation that often works well for problems that are difficult for the conventional Kalman filter (i.e., systems that are highly nonlinear). Particle filtering goes by many other names, including sequential importance sampling [DouOl, Chapter 111, bootstrap filtering [Gor93], the condensation algorithm [Isa96, Mac991 , interacting particle approximations [Mor98], Monte Carlo filtering [Kit96], sequential Monte Carlo (SMC) filtering [And04, CriOZ] , and sur-

viva1 of the fittest [Kan95]. A short discussion on the origins of particle filtering can be found in [IbaOl]. Reference books on the particle filter include [DouOl, Ris041. 
Particle filters had their origin in Nicolas Metropolis's work in 1949 [Met49], 
in which he proposed studying systems by investigating the properties of sets of 
particles rather than the properties of individual particles. He used the analogy of 
the card game of solitaire. What is the probability of success in a game of solitaire? 
The probability may be impossible to compute analytically (because of all of the possible permutations of play). But if a person plays several hundred games and succeeds in a certain proportion of those games, then the probability of success can be approximated on that basis: 
 Let $\alpha$ be a set of $\alpha$-function. 
Pr(Success) M (15.1) 
$$\quad(15.1)$$. 
This simple idea hearkens back to the definition of probability in Section 2.1. Given the recent invention of the electronic computer at the time, Metropolis's work was certainly ahead of its time. Now that fast, parallel computers are available, his work is beginning to see its fruition in the methods described in this chapter. 

As discussed in Chapter 13, the extended Kalman filter (EKF) is the most widely applied state estimation algorithm for nonlinear systems. However, the EKF can be difficult to tune and often gives unreliable estimates if the system nonlinearities are severe. This is because the EKF relies on linearization to propagate the mean and covariance of the state. Chapter 14 discussed the unscented Kalman filter and showed how it reduces linearization errors. We saw that the UKF can provide significant improvements in estimation accuracy over the EKF. However, the UKF 
is still only an approximate nonlinear estimator. The EKF estimates the mean of a nonlinear system with first-order accuracy, and the UKF improves on this by providing an estimate with higher-order accuracy. However, this simply defers the inevitable divergence that will occur when the system or measurement nonlinearities become too severe. 

This chapter presents the particle filter, which is a completely nonlinear state estimator. Of course, there is no **free** lunch [Ho02]. The price that must be paid for the high performance of the particle filter is an increased level of computational effort. There may be problems for which the improved performance of the particle filter is worth the increased computational effort. There may be other applications for which the improved performance is not worth the extra computational effort. These trade-offs are problem dependent and must be investigated on an individual basis. 

The particle filter is a probability-based estimator. Therefore, in Section 15.1, we will discuss the Bayesian approach to state estimation, which will provide a foundation for the derivation of the particle filter. In Section 15.2, we will derive the particle filter. In Section 15.3, we will explore some implementation issues and methods for improving the performance of the particle filter. 

## 15.1 Bayesian State Estimation

In this section, we will briefly discuss the Bayesian approach to state estimation. 

This is based on Bayes' Rule, which is discussed in Chapter 2. This section is based on the presentation given in [Gor93], which is similar to many other books and papers on the subject of Bayesian estimation [DouOl, Ris041. 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{f_{k}(x_{k},w_{k})}}\\ {{}}&{{y_{k}}}&{{=}}&{{h_{k}(x_{k},v_{k})}}\end{array}$$

Suppose we have a nonlinear system described by the equations 

$$\quad(15.2)$$. 
$$(15.4)$$

where k is the time index, Xk is the state, Wk is the process noise, yk is the measurement, and Wk is the measurement noise. The functions fk(.) and *hk(.)* are time-varying nonlinear system and measurement equations. The noise sequences 
{Wk} and **{Wk}** are assumed to be independent and white with known pdf's. The goal of a Bayesian estimator is to approximate the conditional pdf of Xk based on measurements y1, y2, - , *Yk.* This conditional pdf is denoted as p(XklYk) = pdf of Xk conditioned on measurements y1, y2, . *a, yk* **(15.3)** 
The first measurement is obtained at k = 1, so the initial condition of the estimator is the pdf of *20,* which can be written as 

  **  **ants $\Psi_{1},\Psi_{2},\cdots,\Psi_{k}$** (15.3)
$$p(x_{0})=p(x_{0}|Y_{0})$$
since YO is defined as the set of no measurements. Once we compute *p(2kIYk)* then we can estimate Xk in whatever way we think is most appropriate, depending on the problem. The conditional pdf *p(xkIYk)* may be multimodal, in which case we may not want to use the mean of Xk as our estimate. For example, suppose that the conditional pdf is computed as shown in Figure **15.1.** In this case, the mean of x is 0, but there is zero probability that x is equal to 0, so we may not want to use 0 as our estimate of x. Instead we might want to use fuzzy logic and say that 2 = f2, each with a level of membership equal to 0.5 [Lew97]. 

![2_image_0.png](2_image_0.png)

![2_image_1.png](2_image_1.png)

Figure **15.1** 
number should be used as an estimate of z? 

An example of a multimodal probability density function. What single 
Our goal is to find a recursive way to compute the conditional pdf *p(ZkIYk).* 
Before we find this conditional pdf, we will find the conditional pdfp(xkIYk-1). This 

$$p(x_{k}|Y_{k-1})=\int p[(x_{k},x_{k-1})|Y_{k-1}]\,dx_{k-1}\tag{15.5}$$ $$=\int p[x_{k}|(x_{k-1},Y_{k-1})]p(x_{k-1}|Y_{k-1})\,dx_{k-1}$$

is the pdf of Xk given all measurements *prior to* time k. We can use Equations *(2.17)* and *(2.51)* to write this pdf as But notice from our system description in Equation (15.2) *that* 2k is entirely de termined by 2k-1 and *Wk-1;* therefore p[Zk1(2k-1, Yk-l)] = *p(Zk12k-1)* and we *see* that 

$$p(x_{k}|Y_{k-1})=\int p(x_{k}|x_{k-1})p(x_{k-1}|Y_{k-1})\,dx_{k-1}\tag{15.6}$$

The second pdf on the right side of the above equation is not available yet, but it is available at the initial time [see Equation *(15.4)].* Later in this section we will see how to compute it recursively. The first pdf on the right side of the above equation is available. The pdf *p(Zk12k-1)* is simply the pdf of the state at time k given a specific state at time *(Ic* - 1). We know this pdf because we know the system equation *fk(*)* and we know the pdf of the noise Wk (we Section *2.3).* For example, suppose that the system equation is given as *Xk+l* = Xk + Wk and suppose that 2k-1 = 1 and *Wk-1* is uniformly distributed on *[-1,1].* Then the pdf *p(Zk12k-1)* is uniformly distributed on *[0,2].* 
Now consider the a *posteriori* conditional pdf of *Xk.* We can again use Equations (2.17) and *(2.51)* to write this pdf as 

$$\frac{p(Y_{k}|x_{k})}{p(Y_{k})}p(x_{k})$$ $$\frac{p[(y_{k},Y_{k-1})|x_{k}]}{p(y_{k},Y_{k-1})}\underbrace{\frac{p(x_{k}|Y_{k-1})p(Y_{k-1})}{p(Y_{k-1}|x_{k})}}_{p(x_{k})}$$ $$\frac{p(x_{k},y_{k},Y_{k-1})}{p(x_{k})p(y_{k},Y_{k-1})}\frac{p(x_{k},Y_{k-1})p(Y_{k-1})}{p(Y_{k-1})p(Y_{k-1}|x_{k})}\tag{15.7}$$
$$\begin{array}{r l}{p(x_{k}|Y_{k})}&{{}=}\\ {}&{{}}\\ {}&{{}=}\\ {}&{{}}\end{array}$$
$$p(x_{k}|Y_{k})=\frac{p(x_{k},y_{k},Y_{k-1})p(x_{k},Y_{k-1})p(Y_{k-1})}{p(x_{k})p(y_{k},Y_{k-1})p(Y_{k-1})p(Y_{k-1}|x_{k})}\frac{p(x_{k},y_{k})}{p(x_{k},y_{k})}\tag{15.8}$$

We can multiply both the numerator and denominator of this equation by *p(zk,* **yk)** 
to obtain Now we use the ratios of various joint pdfs to marginal pdfs in the above equation to obtain conditional pdfs. This gives 

$$p(x_{k}|Y_{k})=\frac{p[Y_{k-1}|(x_{k},y_{k})]p(y_{k}|x_{k})p(x_{k}|Y_{k-1})}{p(y_{k}|Y_{k-1})p(Y_{k-1}|x_{k})}\tag{15.9}$$

Note that Yk is a function of Zk, so p[Yk-ll(zk, yk)] = *p(&-lIzk).* These two terms cancel in the above equation and we obtain 

$$p(x_{k}|Y_{k})=\frac{p(y_{k}|x_{k})p(x_{k}|Y_{k-1})}{p(y_{k}|Y_{k-1})}\tag{15.10}$$

All of the pdf's on the right side of the above equation are available. The pdf P(Ykl2k) is available from our knowledge of the measurement equation *hk(')* and our knowledge of the pdf of the measurement noise *wk.* The pdf *p(ZklYk-1)* is available from Equation (15.6). Finally, the pdf *p(ykIYk-1)* is obtained (in the same way that Equation (15.5) wm obtained) as follows: 

$$p(y_{k}|Y_{k-1})=\int p[(y_{k},x_{k})|Y_{k-1}]\,dx_{k}\tag{15.11}$$ $$=\int p[y_{k}|(x_{k},Y_{k-1})]p(x_{k}|Y_{k-1})\,dx_{k}$$

But & iS Completely determined by Xk and Wk, SO p[Ykl(Zk, Yk-l)] = *p(Ykl2k)* and 

$$(15.12)$$
$$p(y_{k}|Y_{k-1})=\int p(y_{k}|x_{k})p(x_{k}|Y_{k-1})\,d x_{k}$$

Both of the pdf's on the right side of the above equation are available as discussed above. *p(ykIZk)* is available from our knowledge of the measurement equation *h(.)* 
and the pdf of Wk, and *p(ZkIYk-1)* is available from Equation (15.6). 

Summarizing the development of this section, the recursive equations of the Bayesian state estimation filter can be summarized as follows. 

## The Recursive Bayesian State Estimator

The system and measurement equations are given as follows: 

$\begin{array}{cccc}\mathcal{I}k+1&=&f_{k}(x_{k},w_{k})\\ \mathcal{I}k&=&h_{k}(x_{k},w_{k})\end{array}$
$$(15.13)$$

$$p(x_{0}|Y_{0})=p(x_{0})$$
where *{Wk}* and *{Wk}* are independent white noise processes with known pdf's. 

Assuming that the pdf of the initial state *p(z0)* is known, initialize the estimator as follows: 
P(zoIY0) = *P(Z0)* (15.14) 
For k = 1'2, . . ., perform the following. 

(a) The a *priori* pdf is obtained from Equation (15.6). 

$$p(x_{k}|Y_{k-1})=\int p(x_{k}|x_{k-1})p(x_{k-1}|Y_{k-1})\,d x_{k-1}$$

(b) The a *posteriori* pdf is obtained from Equations (15.10) and (15.12). 

$$(15.14)$$
$$(15.15)$$
$$p(x_{k}|Y_{k})=\frac{p(y_{k}|x_{k})p(x_{k}|Y_{k-1})}{\int p(y_{k}|x_{k})p(x_{k}|Y_{k-1})\,dx_{k}}\tag{15.16}$$

Analytical solutions to these equations are available only for a few special cases. 

In particular, if *f(.)* and *h(.)* are linear, and zo, *{Wk},* and {Wk} are additive, independent, and Gaussian, then the solution is the Kalman filter discussed in Chapter 5. This way of obtaining the Kalman filter is more complicated than the least squares approach that we used in Chapter 5. The Bayesian derivation of the Kalman filter can be found in many references, including [Rho71], [Spa88, Chapter 61, [Ho64, Wes851, [Kit96a, Chapter 61. When the Kalman filter is derived this way, then no conclusions can be drawn about the optimality of the filter when the noise is not Gaussian. In fact, other optimal (nonKalman) filters have been derived for other noise distributions [Ser81]. Nevertheless, the Bayesian derivation proves that when the noise is Gaussian, the Kalman filter is the optimal filter. However, the least squares derivation that we used in Chapter 5 shows that the Kalman filter is the optimal *linear* filter, regardless of the pdf of the noise. 

## 15.2 Particle Filtering

In this section, we derive the basic idea of the particle filter. The particle filter was invented to numerically implement the Bayesian estimator of the previous section. The main idea is intuitive and straightforward. At the beginning of the estimation problem, we randomly generate a given number N state vectors based on the initial pdf *p(z0)* (which is assumed to be known). These state vectors are called particles and are denoted as z& (i = 1,. - a, *N).* At each time step k = 1,2,. - ., we propagate the particles to the next time step using the process equation *f(.):* 

$$x_{k,i}^{-}=f_{k-1}(x_{k-1,i}^{+},w_{k-1}^{\dagger})\ \ \ \ (i=1,\cdots,N)$$

where each w;-~ noise vector is randomly generated on the basis of the known pdf of wk-1. After we receive the measurement at time k, we compute the conditional relative likelihood of each particle z&. That is, we evaluate the pdf **p(ykI~i,~).** As discussed in Section 15.1, this can be done if we know the nonlinear measurement equation and the pdf of the measurement noise. For example, if an rn-dimensional measurement equation is given as Yk = h(zk) +wk **and** Wk - *N(0, R)* then a relative likelihood qi that the measurement is equal to a specific measurement y* , given the premise that zk is equal to the particle z$~, can be computed as follows [compare with Equation (2.73)]. 

$$\begin{array}{l l l}{{q_{i}}}&{{=}}&{{P[(y_{k}=y^{*})|(x_{k}=x_{k,i}^{-})]}}\\ {{}}&{{=}}&{{P[v_{k}=y^{*}-h(x_{k,i}^{-})]}}\\ {{}}&{{\sim}}&{{\frac{1}{(2\pi)^{m/2}|R|^{1/2}}\exp\left(\frac{-[y^{*}-h(x_{k,i}^{-})]^{T}R^{-1}[y^{*}-h(x_{k,i}^{-})]}{2}\right).}}\end{array}$$

The - symbol in the above equation means that the probability is not really given by the expression on the right side, but the probability is directly proportional to the right side. So if this equation is used for all the particles zi,% (i = 1, . . 1, *N),* 
then the *relative* likelihoods that the state is equal to each particle will be correct. Now we normalize the relative likelihoods obtained in Equation (15.18) as follows. 

$$(15.17)$$
$$\left|\begin{array}{l}{{(15.18)}}\end{array}\right.$$
$$(15.19)$$

$$q_{i}={\frac{q_{i}}{\sum_{j=1}^{N}q_{j}}}$$

This ensures that the sum of all the likelihoods is equal to one. **Next** we resample the particles from the computed likelihoods. That is, we compute a brand new set of particles that are randomly generated on the basis of the relative likelihoods qi. 

This can be done several different ways. One straightforward (but not necessarily efficient) way is the following [Ris04]. For i = 1, - , N, perform the following two steps. 

1. Generate a random number r that is uniformly distributed on [0,1]. 

2. Accumulate the likelihoods qi into a sum, one at a time, until the accumulated sum is greater than T. That is, xk21 qm < T but EL=, *qm 2* r. The new particle *x:,~* is then set equal to the old particle xi,j. 

This resampling idea is formally justified in [Smi92], where it is shown that the ensemble pdf of the new particles x:,% tends to the pdf p(xklyk) as the number of samples N approaches *00.* The resampling step can be summarized as follows: 

$x_{k,i}^{+}=x_{k,j}^{-}$ with probability $q_{j}\quad(i,j=1,\cdots,N)$ (15.20)
This is illustrated in Figure 15.2. 

![6_image_0.png](6_image_0.png)

Figure **15.2** Illustration of resampling in the particle filter. For example, if a random number T = 0.3 is generated (from a distribution that is uniform on [0, l]), the smallest value of j for which *c',=,* qm 2 T is j = 3. Therefore the resampled particle is set equal to 
";,a. 
The computational effort of the particle filter is often a bottleneck to its implementation. With this in mind, more efficient resampling methods can be implemented, such as order statistics [Car99, Rip871, stratified sampling and residual sampling [Liu98], and systematic resampling [Kit96]. Other ways of resampling have also been proposed [Mu191]. For example, the a *priori* samples xi,j (j = 1, +, N) 
could be accepted as a *posteriori* samples with a probability that is proportional to qj. However, in this case additional logic must be incorporated to maintain a constant sample size N. 

Now we have a set of particles x:,% that are distributed according to the pdf p(xk(yk). We can compute any desired statistical measure of this pdf. For example, 

$$E(x_{k}|y_{k})\approx{\frac{1}{N}}\sum_{v=1}^{N}x_{k,v}^{+}$$

if we want to compute the expected value *E(ZklYk)* then we can approximate it as the algebraic mean of the particles: 

$$\left(15.21\right)$$... 
The particle filter can be summarized as follows. 

## The Particle Filter

1. The system and measurement equations are given as follows: 

$$\begin{array}{rcl}\mathcal{I}_{k+1}&=&f_{k}(x_{k},w_{k})\\ \mathcal{I}_{k}&=&h_{k}(x_{k},v_{k})\end{array}\tag{15.22}$$

where (wk) and {vk} are independent white noise processes with known pdf's. 

2. Assuming that the pdf of the initial state *p(z0)* is known, randomly generate N initial particles on the basis of the pdf *p(z0).* These particles are denoted z$,% (i = 1, - . . , *N).* The parameter N is chosen by the user as a tradeoff between computational effort and estimation accuracy. 

3. For k = **1,2,.** . ., do the following. 

(a) Perform the time propagation step to obtain a *priori* particles z;,? using the known process equation and the known pdf of the process noise: 

$$(15.23)$$
$$x_{k,1}^{-}=f_{k-1}(x_{k-1,i}^{+},w_{k-1}^{i})\;\;\;\;\;(i=1,\cdots,N)$$

where each w:-~ noise vector is randomly generated on the basis of the known pdf Of *Wk- 1.* 

Qi qi = - 
$$q_{i}={\frac{q_{i}}{\sum_{j=1}^{N}q_{j}}}$$
Now the sum of all the likelihoods is equal to one. 

(b) Compute the relative likelihood qi of each particle z& conditioned on the measurement **yk.** This is done by evaluating the pdf *p(yk12&)* on the basis of the nonlinear measurement equation and the pdf of the measurement noise. 

(c) Scale the relative likelihoods obtained in the previous step as follows: 

$$(15.24)$$

(d) Generate a set of *a posteriori* particles z;,% on the basis of the relative likelihoods qi. This is called the resampling step (for example, see Figure **15.2).** 
(e) Now that we have a set of particles **xtz** that are distributed according to the pdf *p(zklyk),* we can compute any desired statistical measure of this pdf. We typically are most interested in computing the mean and the covariance. 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\frac{1}{2}x_{k-1}+\frac{25x_{k-1}}{1+x_{k-1}^{2}}+8\cos[1.2(k-1)]+w_{k}}}\\ {{y_{k}}}&{{=}}&{{\frac{1}{20}x_{k}^{2}+v_{k}}}\end{array}$$

Suppose that we have a scalar system given by the following equations: 

$$(15.25)$$

where {Wk} and {Wk} are zero-mean Gaussian white noise sequences, both with variances equal to 1. This system has become a benchmark in the nonlinear estimation literature [Kit87, Gor931. The high degree of nonlinearity in both the process and measurement equations makes this a difficult state estimation problem for a Kalman filter. We take the ipitial state as xo = 0.1, the initial state estimate as 20 = *20,* and the initial estimation covariance for the Kalman filter as P$ = 2. We can simulate the EKF and the particle filter to estimate the state x. We used a simulation length of 50 time steps, and 100 particles in the particle filter. Figure 15.3 shows the EKF and particle filter estimates of the state. Not only is the EKF estimate poor, but the EKF thinks (on the basis of the computed covariance) that the estimate is much better than it really is. The true state is usually farther away from the estimated state than the 95% confidence measure of the EKF (as determined from the covariance P). On the other hand, Figure 15.3 shows that the particle filter does a nice job of estimating the state for this example. The RMS estimation errors for the Kalman and particle filters were 16.3 and **2.6,** respectively. 

Note that it might be possible to modify the Kalman filter to obtain better performance. For example, some of the procedures discussed in Section 5.5 to prevent divergence could improve the Kalman filter performance in this example. Sometimes, changing the coordinate system of the state space equation or measurement equation can improve performance [Aid83]. Nevertheless, this example shows the type of improvement that can be obtained with the use of particle filtering. 

vvv 

## 15.3 I M P L E M E Ntatl 0 N I Ss **U Es**

In this section, we discuss a few implementation issues that often arise in the application of particle filters. The methods discussed in this section can significantly improve the performance of the particle filter, and in fact can make the difference between success and failure. 

## 15.3.1 Sample Impoverishment

Sample impoverishment occurs when the region of state space in which the pdf p(Yk1Xk) has significant values does not overlap with the pdfp(xklYk-1). This means that if all of our a *priori* particles are distributed according to P(XklYk-l), and we then use the computed pdf p(YklXk) to resample the particles, only a few particles will be resampled to become a posteriori particles. This is because only a few of the 

![9_image_0.png](9_image_0.png)

Figure **15.3** 
performance for a highly nonlinear scalar system. 

Example 15.1 results. Extended **Kalman** filter and particle filter estimation 
a priori particles will be in a region of state space where the computed pdf *p(yklzk)* 
has a significant value. This means that the resampling process will select only a few distinct *a priori* particles to become a *posteriori* particles. Eventually, all of the particles will collapse to the same va1ue.l This problem will be exacerbated if the measurements are not consistent with the process model (modeling errors). This can be overcome by a bruteforce method of simply increasing the number of particles N, but this can quickly lead to unreasonable computational demands, and often simply delays the inevitable sample impoverishment. Other more intelligent ways of dealing with this problem can be used [Aru02, Gor93J. In the following subsections we discuss several remedies for sample impoverishment, including roughening, prior editing, regularized particle filtering, Markov chain Monte Carlo resampling, and auxiliary particle filtering. 

15.3.1.1 *Roughening* Roughening can be used to prevent sample impoverishment, as shown in [DouOl, Chapter **141,** [Gor93]. In this method, random noise is added to each particle after the resampling process. This is similar to adding artificial process noise to the Kalman filter (see Section **5.5).** In the roughening approach, the *a posteriori* particles (i.e., the outputs of the resampling step) are modified as follows: 

$$x^{+}_{k,i}(m)=x^{+}_{k,i}(m)+\Delta x(m)\ \ \ \ (m=1,\cdots,n)$$ $$\Delta x(m)\sim(0,KM(m)N^{-1/n})\tag{15.26}$$

Az(m) is a zero-mean random variable (usually Gaussian). K is a scalar tuning parameter, N is the number of particles, n is the dimension of the state space, and M is a vector containing the maximum difference between the particle elements lThis is called the black hole of particle filtering, 

$$M(m)=\max_{i,j}|x^{+}_{k,i}(m)-x^{+}_{k,j}(m)|\ \ \ \ (m=1,\cdots,n)\tag{15.27}$$

before roughening. The mth element of the M vector is given as where Ic is the time step, and i and j are particle numbers. K is a tuning parameter that specifies the amount of jitter that is added to *each* particle. In **[Gor93]** the value K = 0.2 is used. 

In this example, we consider the same problem as discussed in Example 14.2. That is, we will try to estimate the altitude, velocity, and ballistic coefficient of a body as it falls toward earth. We use the extended Kalman filter, the unscented Kalman filter, and the particle filter to estimate the system state. A straightforward implementation of the particle filter does not work very well in this example. In order to get good results we had to use the roughening procedure of Equation (15.26) with a tuning parameter K = 0.2. We also had to constrain each particle's third element (ballistic coefficient) to a nonnegative value so that the integration of the timeupdate equations in the particle filter did not diverge. We used 1000 particles. Figure 15.4 shows typical EKF, UKF, and particle filter estimation error magnitudes for this system. It is seen that the particle filter provides performance on par with the UKF, but at the price of much higher computational effort. The UKF 
is essentially an "intelligent" particle filter with only seven particles (twice the number of states plus one), whereas the particle filter can be viewed as a "brute-force" filter with 1000 particles. Perhaps some additional modifications could be made to the particle filter to obtain better performance, but the same could be said for the UKF. 

![10_image_0.png](10_image_0.png)

Figure **15.4** estimation-error magnitudes. 

Example **15.2** results. Kalman filter, unscented filter, **and** particle filter 
15.3.1.2 Prior editing If roughening does not prevent sample impoverishment, then prior editing can be tried. This involves rejection of an a *priori* sample if it is in a region of state space with small *qi.* If an a *priori* sample is in a region of small probability, then it can be roughened as many times as necessary, using a procedure like Equation **(15.26),** until it is in a region of significant probability qi. In **[Gor93]** 
prior editing is implemented as follows: if the magnitude of [yk - *h(~;,~)]* is more than six standard deviations of the measurement noise, then it is highly unlikely to be selected as an *a posteriori* particle. In this case, is roughened and then passed through the system equation again to obtain a new *xi,i.* This is repeated as many times as necessary until zi,% is in a region of nonnegligible probability. 

15.3.1.3 Regularized particle filtering Another way of preventing sample impoverishment is through the use of the regularized particle filter (RPF) [DouOl, Chapter 121, [Ris04]. This performs resampling from a continuous approximation of the pdf p(ykIzF,J rather than from the discrete pdf samples used thus far. Recall in our resampling step in Equation **(15.18)** that we used the probability 

$$q_{i}=P[(y_{k}=y^{*})|(x_{k}=x_{k,i}^{-})]$$

to determine the likelihood of selecting an a *priori* particle to be an *a posteriori* particle. Instead, we can use the pdf *p(xklyk)* to perform resampling. That is, the probability of selecting the particle *x;,+* to be an a *posteriori* particle is proportional to the pdf *p(zklyk)* evaluated at Xk = *xi,,.* In the RPF, this pdf is approximated as 

$$\hat{p}(x_{k}|y_{k})=\sum_{i=1}^{N}w_{k,i}K_{h}(x_{k}-x_{k,i})\tag{15.29}$$
$$(15.28)$$

where Wk,z are the weights that are used in the approximation. Later on, we will see that these weights should be set equal to the qi probabilities that were computed in Equation (15.18). Kh **(a)** is given as 

$K_{h}(x)=h^{-n}K(x/h)$ (15.30)
where h is the positive scalar kernel bandwidth, and n is the dimension of the state vector. *K(.)* is a kernel density that is a symmetric pdf that satisfies 

$$\begin{array}{r c l}{{\int x K(x)\,d x}}&{{=}}&{{0}}\\ {{}}&{{}}&{{}}\\ {{\int||x||_{2}^{2}K(x)\,d x}}&{{<}}&{{\infty}}\end{array}$$
$$(15.31)$$
$$(15.32)$$
$$(15.33)$$

The kernel *K(.)* and the bandwidth h are chosen to minimize a measure of the error between the assumed true density *p(xklyk)* and the approximate density Ij(sk)yk): 

$$\{K(x),h\}=\operatorname{argmin}\int\left[{\hat{p}}(x|y_{k})-p(x|y_{k})\right]^{2}\,d x$$

In the classic case of equal weights *(wk,$* = **1/N** for i = 1,. , N) the optimal kernel is given as 

$$K(x)={\left\{\begin{array}{l l}{{\frac{n+2}{2v_{n}}}(1-||x||_{2}^{2})}&{{\mathrm{if~}}||x||_{2}<1}\\ {0}&{{\mathrm{otherwise}}}\end{array}\right.}$$

where u, is the volume of the n-dimensional unit hypersphere. *K(x)* is called the Epanechnikov kernel [DouOl, Chapter 121. 

An n-dimensional unit hypersphere is a volume in n dimensions in which all points are one unit from the origin [Cox73]. In one dimension, the unit hypersphere is a line with a length of two and a "volume" of two. In two dimensions, the unit hypersphere is a circle with a radius of one and volume **7r.** In three dimensions, the unit hypersphere is a ball with a radius of one and volume 47r/3. In n dimensions, the unit hypersphere has a volume v, = 27rv,-z/n. 

If *p(zlyk)* is Gaussian with an identity covariance matrix then the optimal bandwidth is given as 

$$h^{*}=\left[8v_{n}^{-1}(n+4)(2\sqrt{\pi})^{n}\right]^{1/(n+4)}N^{-1/(n+4)}\tag{15.34}$$
$$(15.35)$$

In order to handle the case of multimodal pdf's,2 we should use h = h*/2 [DouOl, Chapter 12],[Si186]. These choices for the kernel and the bandwidth are optimal only for the case of equal weights and a Gaussian pdf, but they still are often used in other situations to obtain good particle filtering results. Instead of selecting a *priori* particles to become *a posteriori* particles using the probabilities of Equation (15.28), 
we instead select *a posteriori* particles based on the pdf approximation given in Equation (15.29). This allows more diversity as we perform the update from the a priori particles to *a posteriori* particles. In general, we should set the *Wk,Z* weights in Equation (15.29) equal to the qi probabilities shown in Equation (15.28). 

Since this procedure assumes that the true density *p(xklyk)* has a unity covariance matrix, we numerically compute the covariance of the *xi2* at each time step. 

Suppose that this covariance is computed as S (an n x n matrix). Then we compute the matrix square root of S, denoted as A, such that *AAT* = S (e.g., we can **use** 
Cholesky decomposition for this computation). Then we compute the kernel as 

$$K_{h}(x)=(\operatorname*{det}A)^{-1}h^{-n}K(A^{-1}x/h)$$

The RPF resampling algorithm can be summarized as follows. 

## Regularized Particle Filter Resampling

This resampling strategy replaces Step (3d) in the particle filter algorithm on page 468. We have an n-state system, the N *a priori* particles and the N corresponding (normalized) *a priori* probabilities *qi.* Generate the *a posteriori* particles *x:,~* as follows. 

1. Compute the ensemble mean p and covariance S of the a *priori* particles as follows. 

$$\mu=\frac{1}{N}\sum_{{\bf i}=1}^{N}x_{k,{\bf i}}^{-}$$ $$S=\frac{1}{N-1}\sum_{{\bf i}=1}^{N}(x_{k,{\bf i}}^{-}-\mu)(x_{k,{\bf i}}^{-}-\mu)^{T}\tag{15.36}$$

Some authors use an N in the denominator of the S equation, but (N - 1) 
gives an unbiased estimate *(see* Problem 3.6). 

2A multimodal pdf is one with more than one local maxima. See, for example, Figure 15.1. 

2. Perform a square root factorization of S (e.g., a Cholesky factorization) to compute the n x n matrix A such that *AAT* = S. 

3. Compute the volume of the n-dimensional unit sphere as wn = 2rwn-2/n. 

The starting values for this recursion are 01 = 2, *2r2* = **71,** and w3 = **4n/3.** 
4. Compute the optimal kernel bandwidth h as follows: 

$$h=\frac{1}{2}\left[8v_{n}^{-1}(n+4)(2\sqrt{\pi})^{n}\right]^{1/(n+4)}N^{-1/(n+4)}$$
$$(15.37)$$

The bandwidth h can be considered a tuning parameter for the particle filter. 

5. Approximate the pdf *p(zklgk)* as follows: 
where the kernel *Kh(z)* is given as 

$${\hat{p}}(x_{k}|y_{k})=\sum_{i=1}^{N}q_{i}K_{h}(x_{k}-x_{k,i})$$
$$(15.38)$$
$$K_{h}(x)=(\operatorname*{det}A)^{-1}h^{-n}K(A^{-1}x/h)$$
$$(15.39)$$

$$(15.40)$$
Kh(z) = (det *A)-lh-"K(A-'z/h)* **(15.39)** 
and the Epanechnikov kernel *K(z)* is given as 
$$K(x)=\left\{\begin{array}{c c}{{\frac{n+2}{2v_{n}}(1-||x||_{2}^{2})}}&{{\mathrm{if~}||x||_{2}<1}}\\ {{0}}&{{\mathrm{otherwise}}}\end{array}\right.$$

Note that other kernels can also be used in the pdf approximation (see Problem **15.14).** Equation **(15.38)** must be implemented digitally, so the user must choose a certain number of digital values at which to evaluate Equation **(15.38).** As with the number of particles N, the number of digital values is a trade-off between computational resources and estimation accuracy. 

6. Now that we haveIj(zk1yk) from the previous step, we generate the *a posteriori* particles by probabilistically selecting points from the pdf approximation 
$(xk lyk )* 

Consider the same system &s in Example **15.1,** except use a process-noise covariance of **0.001** and only three particles (N = **3).** In this case, the particles in the standard particle filter can quickly degenerate into a single point, but the use of an RPF can prevent this degeneration, increase diversity among the particles, and provide a better state estimate. Twenty Monte Carlo runs of this system result in average RMS errors of **4.6** for the standard particle filter and **3.0** for the RPF. Figure **15.5** shows the improvement that is possible with the use of an RPF. 

Figure **15.6** shows the difference between the resampling step of the standard particle filter and the RPF. The standard particle filter has an *a priori* pdf approximation that consists of the sum of impulse functions. Therefore, the *a posteriori* particles are all set equal to one of the *a priori* particles. 

However, the RPF has a pdf approximation that is a continuous function of the state estimate. Therefore, the *a posteriori* particles can be equal to any value on the horizontal axis. Of course, when we implement the RPF we have to discretize the horizontal axis in order to choose the a *posteriori* particles, but we can use as fine a discretization as our computational allow. 

resources will 

![14_image_0.png](14_image_0.png)

Figure **15.5** of Example **15.3.** This shows the improvement that is possible with the use of an RPF. 

Particle filter estimation performance for the highly nonlinear scalar system 

![14_image_1.png](14_image_1.png)

Figure **15.6** This shows the discrete pdf approximation of the standard particle filter 
(with three particles), and the continuous pdf approximation of the RPF. **This** plot is a snapshot of the pdf approximations at one time instant. 
15.3.1.4 Markov chain Monte Carlo resampling Another approach for preventing sample impoverishment is the Markov chain Monte Carlo (MCMC) move step [GilOl, Ris041. This approach moves the a *priori* particle z& to a new randomly generated state 5& if a uniformly distributed random number is less than an acceptance probability. The acceptance probability is computed as the probability that the a priori sample is consistent with the measurement, relative to the probability that the resampled state is consistent with the measurement. The Metropolis-Hastings acceptance probability [Rob991 is given as 

$$\alpha=\min\left[1,\frac{p(y_{k}|\tilde{x}_{k,i})}{p(y_{k}|x_{k,i}^{-})}\frac{p(\tilde{x}_{k,i}^{-}|x_{k-1,i}^{+})}{p(x_{k,i}^{-}|x_{k-1,i}^{+})}\right]\tag{15.41}$$

The first fraction in the above equation is the ratio of the measurement probability conditioned on the new particle to the measurement probability conditioned on the old particle. The second fraction is the ratio of the probability of the new particle to the probability of the old particle, both conditioned on the particle at the previous time. The acceptance probability is the product of these two fractions, which increases as the probability of the new particle increases. The old *a priori* particle z& is therefore changed to a new particle 5i,+ if the old particle has a low probability of being selected with the resampling step. This helps to maintain diversity in the particles that come out of the resampling step. 

15.3.1.5 Auxiliary particle filtering Another approach to evening out the probability of the a *priori* particles (and thus increasing diversity in the a *posteriori* particles) is called the auxiliary particle filter [Pit99, Ris041. This approach was de veloped by augmenting each a *priori* particle by one element (an auxiliary variable). This increases the dimension of the problem and thus adds a degree of freedom to the choice of the resampling weights in Equation (15.19), which allows the resampling weights to be more evenly distributed. Recall from Section 15.2 that the resampling step of the standard particle filter is performed by selecting particles based on their probabilities. These probabilities are given by 

$$q_{i}=P[(y_{k}=y^{\star})|(x_{k}=x_{k,i}^{-})]$$
$$\frac{P[(y_{k}=y^{\star})|(x_{k}=x_{k,1}^{-})]}{P[(y_{k}=y^{\star})|\mu_{k,i}]}$$
$$q_{i}=\dot{\bar{\imath}}$$

where y* is the actual measurement at time *Ic.* The problem with this is that outliers in the batch of a *priori* particles are ignored due to their low probabilities, and the particles can therefore collapse into a single point. Auxiliary particle filtering addresses this issue by changing the resampling probability to the following: 

$$(15.42)$$
$$(15.43)$$

where *pk,%* is some statistical characterization of Xk based on *xli.* For example, we could use **pk,z** = E(Z~~Z;,~), or *pk,z* = pdf(zklzi,,). So compared to the standard particle filter, the resampling probability of the auxiliary particle filter is smaller by a factor of P[(yk = y*)Ipk,i]. If the actual measurement is highly likely given *pk,%,* 
then the actual measurement is highly likely given z&. The auxiliary particle filter will then tend to decrease qi relative to the standard particle filter. Likewise, the auxiliary particle filter will tend to increase qi for highly unlikely particles. This tends to promote diversity in the population of particles. 

Another easy way to smooth out the qi probabilities is to use something like the following formula. 

$$\tilde{q}_{i}=\frac{(\alpha-1)q_{i}+\bar{q}}{\alpha}$$
$$(15.44)$$

where Q is the sample mean of all of the qi probabilities. The parameter Q E 
[1,00] controls how much regularization occurs. If Q + 00 then the regularized probabilities @i are equal to the standard probabilities *qi.* If Q = 1 then all of the regularized probabilities & are equal. 

If the dynamics of the statespace system are linear, then there should not be any reason to use auxiliary particle filtering. The existence of outliers in the particles results from nonlinearities. This implies that the use of auxiliary particle filtering is more appropriate when the system nonlinearities are severe. In fact, if the nonlinearities are mild or nonexistent, then the use of auxiliary particle filtering could corrupt the probabilities qi in an inappropriate way and degrade performance relative to the standard particle filter. 

## Example **15.4**

Consider the same system as in Examples 14.2 and 15.2. That is, we will try to estimate the altitude **21,** velocity *22,* and constant ballistic coefficient 23 of a body as it falls toward eahh. The equations for this system are given in Example 14.2. We use fourth-order Rung-Kutta integration with a step size of 0.5 sec to simulate the system for 30 seconds. We estimate the system states with the standard particle filter and the auxiliary particle filter. As mentioned in Example 15.2, a straightfonvard implementation of the particle filter does not work very well in this example. In Example 15.2, we used the roughening procedure of Equation (15.26). In this example, we use the auxiliary particle filter of Equation (15.44) with 200 particles. In the standard particle filter, the particles quickly collapse to a single point in state space. 

In the auxiliary particle filter with a = 1.1 (obtained by manual tuning) 
the diversity of the particles is preserved. Averaged over 10 simulations, the use of the auxiliary particle filter improves altitude estimation by 73%, and improves velocity estimation by 55%. However, the auxiliary particle filter makes the estimate of the ballistic coefficient worse. This may be because the ballistic coefficient is not involved in any nonlinear dynamics in either the system equation or the measurement equation. 

vvv 

## 15.3.2 Particle Filtering Combined With Other Filters

One approach that has been proposed for improving particle filtering is to combine it with another filter such as the EKF or the UKF [WanOl, Ris041. In this approach, each particle is updated at the measurement time using the EKF or the UKF, and then resampling is performed using the measurement. This is like running a bank of N Kalman filters (one for each particle) and then adding a resampling step after each measurement. After **zk2** is obtained as shown in Equation (15.17), it can be refined using the EKF or UKF measurement-update equations. For example, if we want to combine the particle filter with the EKF, then after the measurement is obtained at time *k, xi,%* is updated to *x;,%* according to the EKF equations shown in Section **13.2:** 

$$P^{-}_{k,i}=F_{k-1,i}P^{+}_{k-1,i}F^{T}_{k-1,i}+Q_{k-1}$$ $$K_{k,i}=P^{-}_{k,i}H^{T}_{k,i}(H_{k,i}P^{-}_{k,i}H^{T}_{k,i}+R_{k})^{-1}$$ $$x^{+}_{k,i}=x^{-}_{k,i}+K_{k,i}\left[y_{k}-h(x^{-}_{k,i})\right]$$ $$P^{+}_{k,i}=(I-K_{k,i}H_{k,i})P^{-}_{k,i}\tag{15.45}$$

Kk,% is the Kalman gain for the ith particle, and P& is the *a priori* estimation-error covariance for the ith particle. The partial derivative matrices F and H are defined 

$$F_{k-1,4}=\left.\frac{\partial f}{\partial x}\right|_{x=x_{k-1,4}^{+}},$$ $$H_{k,4}=\left.\frac{\partial h}{\partial x}\right|_{x=x_{n,4}^{-}}\tag{15.46}$$  Next, resampling is performed as discussed in Section 15.2 to modify the $x_{k,4}^{+}$ part 
$$(15.47)$$

cles (and their associated covariances *PLJ.* This is another way to prevent sample impoverishment because the a priori particles *xi,%* are updated on the basis of the measurement at time k before they are resampled. The measurement updates of the particles could be performed with any type of filter - an EKF, a UKF, an H, 
filter, another particle filter, and so on. The extended Kalman particle filter can be summarized as follows. 

## The Extended Kalman Particle Filter

1. The system and measurement equations are given as follows: 

 Then $\begin{array}{rcl}x_{k+1}&=&f_k(x_k,\,w_k)\\ y_k&=&h_k(x_k,\,v_k)\end{array}$                      ()  dependent white noise processes with known . 
where {Wk} and *{Wk}* are independent white noise processes with known pdf's. 

2. Assuming that the pdf of the initial state *p(x0)* is known, randomly generate N initial particles on the basis of the pdf *p(x0).* These particles are denoted x& and their covariances are denoted P& = *Po+* (i = **1,.** -, *N).* The parameter N is chosen by the user as a trade-off between computational effort and estimation accuracy. 

3. For k = **1,2,** - ' ., do the following. 

(a) Perform the time propagation step to obtain a *priori* particles *xi,%* and covariances P& using the known process equation and the known pdf of the process noise: - + 

$$\begin{array}{rcl}\bar{x}_{k,1}&=&f_{k-1}(x_{k-1,1}^{+},w_{k-1}^{1})\\ P_{k,1}^{-}&=&F_{k-1,1}P_{k-1,1}^{+}F_{k-1,1}^{T}+Q_{k-1}\\ F_{k-1,1}&=&\left.\frac{\partial f}{\partial x}\right|_{x=x_{k-1,1}^{+}}\end{array}\tag{15.48}$$

where each *WL-~* noise vector is randomly generated on the basis of the 
(b) Update the a *priori* particles and covariances to obtain a *posteriori* parknown pdf Of *Wk-1.* 
ticles and covariances: 

$$\begin{array}{r c l}{{H_{k,\mathrm{t}}}}&{{=}}&{{\left.\frac{\partial h}{\partial x}\right|_{x=x_{k,\mathrm{t}}^{-}}}}\\ {{K_{k,\mathrm{t}}}}&{{=}}&{{P_{k,\mathrm{t}}^{-}H_{k,\mathrm{t}}^{T}(H_{k,\mathrm{t}}P_{k,\mathrm{t}}^{-}H_{k,\mathrm{t}}^{T}+R_{k})^{-1}}}\\ {{x_{k,\mathrm{t}}^{+}}}&{{=}}&{{x_{k,\mathrm{t}}^{-}+K_{k,\mathrm{t}}\left[y_{k}-h(x_{k,\mathrm{t}}^{-})\right]}}\\ {{P_{k,\mathrm{t}}^{+}}}&{{=}}&{{(I-K_{k,\mathrm{t}}H_{k,\mathrm{t}})P_{k,\mathrm{t}}^{-}}}\end{array}$$

(c) Compute the relative likelihood qi of each particle *x:,~* conditioned on the measurement *Yk.* This is done by evaluating the pdf *p(yklZt,t)* on the basis of the nonlinear measurement equation and the pdf of the measurement noise. 

(d) Scale the relative likelihoods obtained in the previous step as follows: 

$$(15.49)$$
$q_{i}=\frac{q_{i}}{\sum_{j=1}^{N}q_{j}}$ (15.50)
Now the sum of all the likelihoods is equal to one. 

(e) Refine the set of a *posteriori* particles and covariances **Pzt** on the basis of the relative likelihoods *qi.* This is the resampling step. 

(f) Now we have a set of a *posteriori* particles *x:,~* and covariances *Pla.* We can compute any desired statistical measure of this set of particles. We typically are most interested in computing the mean and the covariance. 

Consider the same system as in Example **15.4.** That is, we will try to estimate the altitude **21,** velocity *22,* and constant ballistic coefficient 23 of a body as it falls toward earth. The equations for this system are given in Example **14.2.** We use fourth-order Runge-Kutta integration with a step size of **0.5** sec to simulate the system for 30 s. We use the standard particle filter and the EKF particle filter to estimate the states. The EKF particle filter updates the a *priori* particles at each time based on the measurement, and then the resampling step is performed as usual. In this example, we use **200** particles for the estimator. As mentioned in Example **15.4,** in the standard particle filter the particles quickly collapse to a single trajectory. In Example **15.2,** 
we used roughening to improve the particle filter. In Example **15.3,** we used the regularized particle filter to improve performance. In Example **15.4,** we used the auxiliary particle filter to improve performance. Here we use an EKF particle filter to improve performance. Averaged over 10 simulations, the use of the EKF particle filter improves altitude estimation accuracy by an astounding **99.6%,** almost three orders of magnitude. The velocity estimation is only marginally improved, and the ballistic coefficient estimation is marginally degraded. 

## 15.4 Summary

In this chapter, we laid the foundation of Bayesian state estimation, and from there we developed the particle filter. In a linear system with Gaussian noise, the Kalman filter is optimal. In a system that is nonlinear, the Kalman filter can be used for state estimation, but the particle filter may give better results at the price of additional computational effort. In a system that has non-Gaussian noise, the Kalman filter is the optimal linear filter, but again the particle filter may perform better. The unscented Kalman filter provides a balance between the low computational effort of the Kalman filter and the high performance of the particle filter. This is depicted in Figure 15.7. 

![19_image_0.png](19_image_0.png)

computational effort computational effort 
(a) The **above** figure depicts the increasing computational effort and increasing accuracy that is obtained by going from an EKF to a UKF to a particle filter. This applies to **systems** that are nonlinear or non-Gaussian. 

![19_image_1.png](19_image_1.png)

(b) The above figure depicts the fact that the Kalman filter is optimal for linear Gaussian systems. Going from a Kalman filter to a UKF to a particle filter **will** increase computational effort but **will** not improve estimation accuracy. 

Figure *15.7* State estimation trade-offs. 
particle I I 
The particle filter has some similarities with the UKF (see Chapter 14) in that it transforms a set of points via known nonlinear equations and combines the results to estimate the mean and covariance of the state. However, in the particle filter the points are chosen randomly, whereas in the UKF the points are chosen on the basis of a specific algorithm. Because of this, the number of points used in a particle filter generally needs to be much greater than the number of points in a UKF. Another difference between the two filters is that the estimation error in a UKF does not converge to zero in any sense, but the estimation error in a particle filter does converge to zero as the number of particles (and hence the computational effort) approaches infinity. 

Particle filters have found application in a wide variety of areas, including tracking problems [Ris04], demodulation of communication signals [DouOl, Chapter 41, estimation of ecological parameters and populations [DouOl, Chapter 51, image processing [DouOl, Chapter 161, neural network training [DouOl, Chapter 171, fault de tection [deF02], speech recognition [VerOZ] , and pattern recognition [DouOl, Chapter 261. Particle filtering is a growing area of research with many unexplored avenues and applications. Some of the more important areas of open research include the avoidance of sample impoverishment, methods for determining how many particles are required for a given problem, convergence results [Cri02], application to control and parameter estimation [Mor03, AndO41, connections with genetic algorithms [DouOl, Chapter 201, real-time implementation issues [Kwo04], and hardware implementations of parallel particle filters (e.g., in field programmable gate arrays). 

## Problems Written Exercises

15.1 Consider the scalar system 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k},\quad}}&{{w_{k}\sim U(-1,1)}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k},\quad}}&{{v_{k}\sim U(-1,1)}}\end{array}$$

where xo N U(-1, 1). Suppose that the first measurement y1 = 1. 

a) **Use** the recursive Bayesian state estimator to find pdf(z1 [YO) and pdf(z1 lY1). 

b) What is the Kalman filter estimate *2:?* How is 2: related to pdf(z1 IY,)? 

15.2 Suppose the pdf of an RV x is given as 

$$\operatorname{pdf}(x)={\left\{\begin{array}{l l}{1-x/2}&{\quad x\in[0,2]}\\ {0}&{\quad{\mathrm{~otherwise~}}}\end{array}\right.}$$

The value of z can be estimated several ways. 

a) The maximum-likelihood estimate is written as f = argmqpdf(z). Find the maximum-likelihood estimate of x. 

b) The min-max estimate of z is that value off that minimizes the magnitude of the maximum estimation error. Find the min-max estimate of z. 

c) The minimum mean square estimate of z is that value of 2 that minimizes E[(x - 2)2]. Find the minimum mean square estimate of x. 

d) The expected value estimate of x is given as 2 = *E(z).* Find *E(z).* 
15.3 pdf that is given as Suppose you have a measurement yk = zz + vk, where Vk has a triangular 

$$\mathrm{pdf}(v_{k})={\left\{\begin{array}{l l}{1/2+v_{k}/4}&{v_{k}\in[-2,0]}\\ {1/2-v_{k}/4}&{v_{k}\in[0,2]}\\ {0}&{{\mathrm{otherwise}}}\end{array}\right.}$$

Suppose that five a *priori* particles xi,% are given as -2, -1, 0, 1, and 2, and that the measurement is obtained as Yk = 1. What are the normalized likelihoods qi of each a *priori* particle 15.4 Suppose you have a measurement Yk = Vk/Zk, where Wk N N(9,l). Suppose that five a *priori* particles **zi,z** are given as 0.8, 0.9, 1.0, 1.1, and 1.2, and that the measurement is obtained as yk = 10. What are the relative likelihoods qi of each a priori particle *x;,~?* 
15.5 Suppose that five a *priori* particles are found to have probabilities 0.1, 0.1, 0.1, 0.2, and 0.5. The particles are resampled with the basic strategy depicted in Equation (15.20). 

a) What is the probability that the first particle will be chosen as an a posteriori particle at least once? 

b) What is the probability that the fifth particle will be chosen as an a posteriori particle at least once? 

c) What is the probability that the five *a posteriori* particles will be equal to the five a *priori* particles (disregarding order)? 

15.6 Suppose you have the five particles xCk+,% = { **1, 2, 3, -2,** 6 }. What would you propose to use for the estimate of **Xk?** What would you estimate as the variance of &? 

15.7 Suppose that you have five particles **-1, -1,** 0, 1, and 1. You want to use the roughening procedure of Section **15.3.1.1** to add a uniform random variable with a variance of *KMN-lIn* to each particle. What range of K will give a probability of at least 1/8 that at least one of the roughened particles is less than **-2?** 

$$\operatorname{pdf}(v_{k})={\left\{\begin{array}{l l}{1/2+v_{k}/4}&{v_{k}\in[-2,0]}\\ {1/2-v_{k}/4}&{v_{k}\in[0,2]}\\ {0}&{{\mathrm{otherwise}}}\end{array}\right.}$$

15.8 Suppose you have the system equation **Xk+1** = Xk and the measurement equation Yk = 2: + **Wk,** where **2rk** has a triangular pdf that is given as Suppose that five a *posteriori* particles ZC~+-~,~ are given as **-2, -1,** 0, 1, and 2, and that the measurement is obtained as Yk = 1. You want to use prior editing to ensure that the -2 particle has at least a **10%** chance (after one roughening step) 
of being selected as an a *posteriori* particle at the next time step. What value of K should you use in your roughening step? 

15.9 Suppose you have two particles -1 and **+1,** both with a *priori* probabilities 1/2. Use the kernel bandwidth h = 1 with the regularized particle filter to find the pdf approximations $(xk = -21yk), $(xk = **-llyk),** *$(zk* = Olyk), @(xk = **llyk),** 
and $(zk = **21yk).** For what values of 2k is the pdf approximation **$(xklyk)** equal to zero? 

15.10 Suppose you have N resampling probabilities qi with sample mean /A and sample variance S. What is the sample mean and variance of the auxiliary probabilities given by Equation **(15.44)?** 

## Computer Exercises

15.11 Plot the volume of the n-dimensional unit hypersphere as a function of n for n E **[1,20].** 
15.12 Consider two particles 21 = 1 and 22 = 2, with equal probabilities. Generate the approximate pdf using the Epanechnikov kernel with bandwidth h = *h*.* 
Generate two separate plots (on the same figure) of the two individual terms in the summation of Equation **(15.29),** and also generate a plot (on the same figure) 
of their sum. Repeat for three particles 21 = 1, 22 = 2, **and** 23 = 3 with equal probabilities. 

Repeat Problem **15.12** with h = *h*/2* and with h = *2h*.* This shows that 15.13 the bandwidth selection can have a strong effect on the pdf approximation. 

Kernels other than the Epanechnikov kernel can also be used for pdf approximation [Sim98, DevOl] . 

one dimension as follows. 

15.14 

Expachennikov: $K(x)=\left\{\begin{array}{ll}\mbox{\rm{\small$\frac{1}{2}$}}&\mbox{\rm{\small$\frac{1}{2}$}}\\ \mbox{\rm{\small$\frac{1}{2}$}}&\mbox{\rm{\small$\frac{1}{2}$}}\end{array}\right.$
Biweight: 
Some of the more popular kernels can be described in 
 $\begin{array}{ccc}&&\text{(}\\ &&\text{(}\\ \text{Gaussian:}\:K(x)&=&(2)\\ &&\\ \text{Uniform:}\:K(x)&=&\bigg\{\bigg\}\end{array}$  $\text{Triangular:}\:K(x)\;\;=\;\;\bigg\{\bigg\}$  . 
$\begin{array}{cc}\frac{3}{4}(1-x^2)&|x|<1\\ 0&\text{otherwise}\end{array}$  $\pi)^{-1/2}\exp(-x^2/2)$  $\begin{array}{cc}\frac{1}{2}&|x|<1\\ 0&\text{otherwise}\end{array}$  2. 
$\begin{array}{ll}0&\text{What was}\\ 1-x^2&|x|<1\\ 0&\text{otherwise}\end{array}$  $\frac{15}{16}(1-x^2)^2\quad|x|<0\\ 0\qquad\qquad\text{otherwise}$  . 
K(z) = **(2~)-'/~** exp( **--x2/2)** 
Bandwidth selection is another matter, but for this problem you can simply use the optimal Epanechnikov bandwidth for all of the kernels. 

a) Repeat Problem **15.12** using Gaussian kernels. 

b) Repeat Problem **15.12** using uniform kernels. 

c) Repeat Problem **15.12** using triangular kernels. 

d) Repeat Problem **15.12** using biweight kernels. 

15.15 In this problem, we will explore the performance of the EKF and the particle filter for the system described in Example **15.1.** 
Run 100 simulations of the EKF and the particle filter with N = **10,** 
N = 100, and N = 1000. What is the average RMS state-estimation error for each case? 

Run 100 simulations of the EKF and the particle filter with N = 100 using Q = **0.1,** Q = 1, and Q = 10. What is the average RMS state-estimation error for each case? 