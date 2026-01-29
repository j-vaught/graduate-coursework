---
type: chapter
chapter: 3
title: Least squares estimation
---
# Chapter 3 Least Squares Estimation

The most probable value of the unknown quantities will be that in which the sum of the squares of the differences between the actually observed and the computed values multiplied by numbers that measure the degree of precision is a minimum. 

-Karl Friedrich Gauss [GauOli] 
In this chapter, we will discuss least squares estimation, which is the basic idea of Karl Gauss's quote above.' The material in this chapter relies on the theory of the previous two chapters, and will enable us to derive optimal state estimators later in this book. 

Section **3.1** discusses the estimation of a constant vector on the basis of several linear but noisy measurements of that vector. Section **3.2** extends the results of Section **3.1** to the case in which some measurements are more noisy than others; that is, we have less confidence in some measurements than in others. Sections **3.1** 
and **3.2** use matrices and vectors whose dimensions grow larger as more measurements are obtained. This makes the problem cumbersome if many measurements are available. This leads us to Section **3.3,** which presents a recursive way of es timating a constant on the basis of noisy measurements. Recursive estimation in this chapter is a method of estimating a constant without increasing the computa-

lGauss published his book in 1809, although he claimed to have worked out his theory as early as 1795 (when he was 18 years old). 
tional effort of the algorithm, regardless of how many measurements are available. 

Finally, Section **3.4** presents the Wiener filter, which is a method of estimating a time-varying signal that is corrupted by noise, on the basis of noisy measurements. Until 1960, Wiener filtering was the state of the art in signal estimation. The paradigm of signal estimation was shattered with the publication of Rudolph Kalman's work and related papers in the early 1960s, but it is still worthwhile understanding Wiener filtering because of its historical place in the history of signal estimation. Furthermore, Wiener filtering is still very useful in signal processing and communication theory. 

## 3.1 Estimation Of A Constant

In this section, we will determine how to estimate a constant on the basis of several noisy measurements of that constant. For example, suppose we have a resistor but we do not know its resistance. We take several measurements of its resistance using a multimeter, but the measurements are noisy because we have a cheap multimeter. 

We want to estimate the resistance on the basis of our noisy measurements. In this case, we want to estimate a constant scalar but, in general, we may want to estimate a constant vector. 

To put the problem in mathematical terms, suppose x is a constant but unknown n-element vector, and y is a Ic-element noisy measurement vector. How can we find the "best" estimate h of x? Let us assume that each element of the measurement vector y is a linear combination of the elements of x, with the addition of some measurement noise: 

$y_{1}=H_{11}x_{1}+\cdots+H_{1n}x_{n}+v_{1}$  $\vdots$  $y_{k}=H_{k1}x_{1}+\cdots+H_{kn}x_{n}+v_{k}$
$$({\mathfrak{3}}.1)$$
$$(3.2)$$
$$y=\,.$$
$$y=H x+v$$
$\left(3.3\right)^{2}$
$$\epsilon_{y}=y-H{\hat{x}}$$
This set of equations can be put into matrix form as 
~=Hx+w **(3.2)** 
Now define ey as the difference between the noisy measurements and the vector H2: 
ey = y - Hh **(3.3)** 
q, is called the measurement residual. As Karl Gauss wrote [GauOl], the most probable value of the vector x is the vector 2 that minimizes the sum of squares between the obsemed values y and the vector Hh. So we will try to compute the h that minimizes the cost function J, where J is given as J is often referred to in control and estimation books and papers as a cost function, objective function, or return function. We can substitute for ey in the above equation to rewrite J as 

$$\begin{array}{r c l}{{J}}&{{=}}&{{\epsilon_{y1}^{2}+\cdots+\epsilon_{y k}^{2}}}\\ {{}}&{{=}}&{{\epsilon_{y}^{T}\epsilon_{y}}}\end{array}$$
$$(3.4)$$
$$\begin{array}{r c l}{{J}}&{{=}}&{{(y-H\hat{x})^{T}(y-H\hat{x})}}\\ {{}}&{{=}}&{{y^{T}y-\hat{x}^{T}H^{T}y-y^{T}H\hat{x}+\hat{x}^{T}H^{T}H\hat{x}}}\end{array}$$
$$(3.5)$$
$$(3.6)$$
In order to minimize J with respect to 2, we compute its partial derivative and set 
it equal to zero: - *-yTH* - yTH + *2?'HTH dJ* 
$$\begin{array}{r c l}{{\frac{\partial J}{\partial{\hat{x}}}}}&{{=}}&{{-y^{T}H-y^{T}H+2{\hat{x}}^{T}H^{T}H}}\\ {{}}&{{=}}&{{0}}\end{array}$$

Solving this equation for ? results in 

$$H^{T}y=H^{T}H\hat{x}$$ $$\hat{x}=(H^{T}H)^{-1}H^{T}y$$ $$=H^{L}y\tag{3.7}$$

where *HL,* the left pseudo inverse of H, exists if k 2 n and H is full rank. This means that the number of measurements k is greater than the number of variables n that we are trying to estimate, and the measurements are linearly independent. In order to prove that we have found a minimum rather than some other type of stationary point2 of J, we need to prove that the second derivative of J is positive semidefinite (see Problem **3.1).** 

$$\begin{array}{r c l}{y_{1}}&{=}&{x+v_{1}}\end{array}$$

Let us go back to our original problem of trying to estimate the resistance z of an unmarked resistor on the basis of k noisy measurements from a multimeter. 

In this case, 2 is a scalar so our k noisy measurements are given as 

$\mathbf{a}$
$$(3.8)$$
$$\begin{array}{r c l}{y_{k}}&{=}&{x+v_{k}}\end{array}$$
$$\left[\begin{array}{c}y_{1}\\ \vdots\\ y_{k}\end{array}\right]=\left[\begin{array}{c}1\\ \vdots\\ 1\end{array}\right]\,x+\left[\begin{array}{c}v_{1}\\ \vdots\\ v_{k}\end{array}\right]\tag{3.9}$$
These k equations can be combined into a single matrix equation as Equation **(3.7)** shows that the optimal estimate of the resistance x is given as 

$$\begin{array}{r l}{={}}&{{}(H^{T}H)^{-1}H^{T}y}\\ {={}}&{{}\left(\left[\begin{array}{l l l}{1}&{\cdots}&{1}\end{array}\right]\left[\begin{array}{l}{1}\\ {\vdots}\\ {1}\end{array}\right]\right)^{-1}\left[\begin{array}{l l l}{1}&{\cdots}&{1}\end{array}\right]\left[\begin{array}{l}{y_{1}}\\ {\vdots}\\ {y_{k}}\end{array}\right]}\\ {={}}&{{}{\frac{1}{k}}(y_{1}+\cdots+y_{k})}\end{array}$$
$$(3.10)$$

In this simple example, we see that least squares estimation agrees with our intuition to simply compute the average of the measurements. 

vvv 2A stationary point of a function is any point at which its derivative is equal to zero. A stationary point of a scalar function could be a maximum, a minimum, or an inflection point. A stationary point of a vector function could be a maximum, a minimum, or a saddle point. 

## 3.2 Weighted Least Squares Estimation

In the previous section, we assumed that we had an equal amount of confidence in all of our measurements. Now suppose we have more confidence in some measurements than others. In this case, we need to generalize the results of the previous section to obtain weighted least squares estimation. For example, suppose we have several measurements of the resistance of an unmarked resistor. Some of the measurements were taken with an expensive multimeter with low noise, but other measurements were taken with a cheap multimeter by a tired student late at night. We have more confidence in the first set of measurements, so we should somehow place more emphasis on those measurements than on the others. However, even though the second set of measurements is less reliable, it seems that we could get at least *some* information from them. This section shows that we can indeed get some information from less reliable measurements. We should never throw away measurements, no matter how unreliable they may be. 

To put the problem in mathematical terms, suppose x is a constant but unknown n-element vector, and y is a k-element noisy measurement vector. We assume that each element of y is a linear combination of the elements of x, with the addition of some measurement noise, and the variance of the measurement noise may be different for each element of y: 

$$\left[\begin{array}{c}y_{1}\\ \vdots\\ y_{k}\end{array}\right]=\left[\begin{array}{ccc}H_{11}&\cdots&H_{1n}\\ \vdots&\ddots&\vdots\\ H_{k1}&\cdots&H_{kn}\end{array}\right]\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right]+\left[\begin{array}{c}v_{1}\\ \vdots\\ v_{k}\end{array}\right]$$ $$E(v_{i}^{2})=\sigma_{i}^{2}\quad\left(i=1,\ldots,k\right)\tag{3.11}$$

We assume that the noise for each measurement is zero-mean and independent. The measurement covariance matrix is 

$$\begin{array}{r c l}{{R}}&{{=}}&{{E(v v^{T})}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l l}{{\sigma_{1}^{2}}}&{{\cdots}}&{{0}}\\ {{\vdots}}&{{}}&{{\vdots}}\\ {{0}}&{{\cdots}}&{{\sigma_{k}^{2}}}\end{array}\right]}}\end{array}$$
$$(3.12)$$

Now we will minimize the following quantity with respect to 2. 

$$J=\epsilon_{y1}^{2}/\sigma_{1}^{2}+\cdots+\epsilon_{y k}^{2}/\sigma_{k}^{2}$$
$$(3.13)$$

Note that instead of minimizing the sum of squares of the ey elements as we did in Equation **(3.4),** we will minimize the *weighted* sum of squares. If y1 is a relatively noisy measurement, for example, then we do not care as much about minimizing the difference between y1 and the first element of H2 because we do not have much confidence in y1 in the first place. The cost function J can be written as 

$$J=\epsilon_{y}^{T}R^{-1}\epsilon_{y}\tag{3.14}$$ $$=(y-H\hat{x})^{T}R^{-1}(y-H\hat{x})$$ $$=y^{T}R^{-1}y-\hat{x}^{T}H^{T}R^{-1}y-y^{T}R^{-1}H\hat{x}+\hat{x}^{T}H^{T}R^{-1}H\hat{x}$$
Now we take the partial derivative of J with respect to 2 and set it equal to zero 
to compute the best estimate 2: 
$$\frac{\partial J}{\partial\hat{x}}=-y^{T}R^{-1}H+\hat{x}^{T}H^{T}R^{-1}H\tag{3.15}$$ $$=0$$ $$H^{T}R^{-1}y=H^{T}R^{-1}H\hat{x}$$ $$\hat{x}=(H^{T}R^{-1}H)^{-1}H^{T}R^{-1}y$$

Note that this method requires that the measurement noise matrix R be nonsingular. In other words, each of the measurements yi must be corrupted by at least some noise for this method to work. 

We return to our original problem of trying to estimate the resistance x of an unmarked resistor on the basis of k noisy measurements from a multimeter. In this case, 2 is a scalar so our k noisy measurements are given as 

$$\begin{array}{r c l}{{y_{i}}}&{{=}}&{{x+v_{i}}}\\ {{E(v_{i}^{2})}}&{{=}}&{{\sigma_{i}^{2}\ \ \ \ (i=1,\ldots,k)}}\end{array}$$
$${\begin{array}{l}{y_{1}}\\ {\vdots}\\ {y_{k}}\end{array}}\end{array}}\right]=\left[\begin{array}{l}{1}\\ {\vdots}\\ {1}\end{array}\right]\,{\boldsymbol{x}}+\left[\begin{array}{l}{v_{1}}\\ {\vdots}\\ {v_{k}}\end{array}\right]$$

The k measurement equation can be combined into a single matrix equation as 

$$(3.16)$$
$$(3.17)$$

and the measurement noise covariance is given as 

$$R=\mathrm{diag}(\sigma_{1}^{2},\ldots,\sigma_{k}^{2})$$

Equation (3.15) shows that the optimal estimate of the resistance 2 is given 

$$(3.18)$$
-l r 1  ...  01  uT  0 ... u;  .. ..  [ 1 ". 1 ]  = (c l/u?)-l (Yl/.f + . '. + Yk/.E) (3.19) 
We see that the optimal estimate L is a weighted sum of the measurements, where each measurement is weighted by the inverse of its uncertainty. In other words, we put more emphasis on certain measurements, in agreement with our intuition. Note that if all of the 0% constants are equal, this estimate reduces to the simpler form given in Equation **(3.10).** 
vvv 

## 3.3 Recursive Least Squares Estimation

Equation **(3.15)** gives us a way to compute the optimal estimate of a constant, but there is a problem. Note that the H matrix in **(3.15)** is a k x n matrix. If we obtain measurements sequentially and want to update our estimate of z with each new measurement, we need to augment the H matrix and completely recompute the estimate 2. If the number of measurements becomes large, then the computational effort could become prohibitive. For example, suppose we obtain a measurement of a satellite's altitude once per second. After one hour has passed, the number of measurements is **3600** and growing. The computational effort of least squares estimation can rapidly outgrow our resources. 

In this section, we show how to *recursively* compute the weighted least squares estimate of a constant. That is, suppose we have d after (k - 1) measurements, and we obtain a new measurement **Yk.** How can we update our estimate without completely reworking Equation **(3.15)?** 
A linear recursive estimator can be written in the form 

$$y_{k}=H_{k}x+v_{k}$$ $$\hat{x}_{k}=\hat{x}_{k-1}+K_{k}(y_{k}-H_{k}\hat{x}_{k-1})\tag{3.20}$$

That is, we compute dk on the basis of the previous estimate *dk-1* and the new measurement *yk. Kk* is a matrix to be determined called the estimator gain matrix. The quantity *(yk-Hkdk-1)* is called the correction term. Note that if the correction term is zero, or if the gain matrix is zero, then the estimate does not change from time step (k - 1) to k. 

Before we compute the optimal gain matrix *Kk,* let us think about the mean of the estimation error of the linear recursive estimator. The estimation error mean can be computed as 

$$\begin{array}{r l}{E(\epsilon_{z,k})}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
E(%,k) = E(z - *dk)* 
$$=E(x-\hat{x}_{k})\tag{3.21}$$ $$=E[x-\hat{x}_{k-1}-K_{k}(y_{k}-H_{k}\hat{x}_{k-1})]$$ $$=E[\epsilon_{x,k-1}-K_{k}(H_{k}x+v_{k}-H_{k}\hat{x}_{k-1})]$$ $$=E[\epsilon_{x,k-1}-K_{k}H_{k}(x-\hat{x}_{k-1})-K_{k}v_{k}]$$ $$=(I-K_{k}H_{k})E(\epsilon_{x,k-1})-K_{k}E(v_{k})$$

So if *E(?Jk)* = 0 and *E(E2,k-I)* = 0, then *E(E2,k)* = 0. In other words, if the measurement noise vk is zero-mean for all k, and the initial estimate of z is set equal to the expected value of z [i.e., 2i.0 = *E(x)],* then the expected value of ?k will be equal to 5k for all k. Because of this, the estimator of Equation **(3.20)** is called an unbiased estimator. Note that this property holds regardless of the value of the gain matrix **Kk.** This is a desirable property of an estimator because it says that, on *average,* the estimate d will be equal to the true value x. 

Next we turn our attention to the determination of the optimal value of *Kk.* 
Since the estimator is unbiased regardless of what value of Kk we use, we must 

$$E[(x_{1}-\hat{x}_{1})^{2})]+\cdots+E[(x_{n}-\hat{x}_{n})^{2})]$$ $$E\left(\epsilon_{x1,k}^{2}+\cdots+\epsilon_{xn,k}^{2}\right)$$ $$E\left(\epsilon_{x,k}^{T}\epsilon_{x,k}\right)$$ $$E\left[\mbox{Tr}(\epsilon_{x,k}\epsilon_{x,k}^{T})\right]$$ $$\mbox{Tr}P_{k}\tag{3.22}$$
$$\begin{array}{r l}{J_{k}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$

choose some other optimality criterion in order to determine *Kk.* The optimality criterion that we choose to minimize is the sum of the variances of the estimation errors at time k: 
where *Pk,* the estimation-error covariance, is defined by the above equation. We can use a process similar to that followed in Equation **(3.21)** to obtain a recursive formula for the calculation of Pk: 

$$P_{k}=E(\varepsilon_{x,k}\varepsilon_{x,k}^{T})\tag{3.23}$$ $$=E\left\{(I-K_{k}H_{k})\varepsilon_{x,k-1}-K_{k}v_{k}|[\cdots]^{T}\right\}$$ $$=(I-K_{k}H_{k})E(\varepsilon_{x,k-1}\varepsilon_{x,k-1}^{T})(I-K_{k}H_{k})^{T}-$$ $$K_{k}E(v_{k}\varepsilon_{x,k-1}^{T})(I-K_{k}H_{k})^{T}-(I-K_{k}H_{k})E(\varepsilon_{x,k-1}v_{k}^{T})K_{k}^{T}+$$ $$K_{k}E(v_{k}v_{k}^{T})K_{k}^{T}$$

Now note that *Ez,k-l* [the estimation error at time (k - l)] is independent of Vk 
(the measurement noise at time *k).* Therefore, 

$$E(v_{k}\epsilon^{T}_{x,k-1})=E(v_{k})E(\epsilon_{x,k-1})\tag{3.24}$$ $$=0$$
$$(3.25)$$
$$P_{k}=(I-K_{k}H_{k})P_{k-1}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}$$

since both expected values are zero. Therefore, Equation **(3.23)** becomes 

$$\frac{\partial J_{k}}{\partial K_{k}}=2(I-K_{k}H_{k})P_{k-1}(-H_{k}^{T})+2K_{k}R_{k}\tag{3.26}$$

where Rk is the covariance of **Vk.** This is the recursive formula for the covariance of the least squares estimation error. This is consistent with intuition in the sense that as the measurement noise increases (i.e.l Rk increases) the uncertainty in our estimate also increases (Le., Pk increases). Note that Pk should be positive definite since it is a covariance matrix, and the form of Equation **(3.25)** guarantees that Pk will be positive definite, assuming that Pk-1 *and* Rk are positive definite. 

Now we need to find the value of Kk that makes the cost function in Equation **(3.22)** as small as possible. The mean of the estimation error is zero for any value of **Kk,** so if we choose Kk to make the cost function (i.e.l the trace of *Pk)* 
small then the estimation error will not only be zero-meanl but it will also be consistently close to zero. In order to find the best value of *Kk,* first we need to recall from Equation **(1.66)** that *sn(tfA'l* = **2AB** if B is symmetric. With this in mind we can use Equations **(3.22), (3.25),** and the chain rule to obtain In order to find the value of Kk that minimizes *Jk,* we set the above derivative equal to zero and then solve for Kk as follows: 

$$K_{k}R_{k}=(I-K_{k}H_{k})P_{k-1}H_{k}^{T}$$ $$K_{k}(R_{k}+H_{k}P_{k-1}H_{k}^{T})=P_{k-1}H_{k}^{T}$$ $$K_{k}=P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}\tag{3.27}$$

Equations **(3.20), (3.25),** and **(3.27)** form the recursive least squares estimator. The recursive least squares estimator can be summarized as follows. 

## Recursive Least Squares Estimation

1. Initialize the estimator as follows: 

$$\begin{array}{r c l}{{\hat{x}_{0}}}&{{=}}&{{E(x)}}\\ {{P_{0}}}&{{=}}&{{E[(x-\hat{x}_{0})(x-\hat{x}_{0})^{T}]}}\end{array}$$
$$(3.28)$$
$$(3.29)$$
$$y_{k}=H_{k}x+v_{k}$$

If no knowledge about z is available before measurements are taken, then Po = mI. If perfect knowledge about z is available before measurements are taken, then PO = 0. 

2. For k = **1,2,.** . a, perform the following. 

(a) Obtain the measurement **Yk,** assuming that Yk is given by the equation 

$$P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$ $$\hat{x}_{k-1}+K_{k}(y_{k}-H_{k}\hat{x}_{k-1})$$ $$(I-K_{k}H_{k})P_{k-1}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}\tag{3.30}$$
$$\begin{array}{r l}{K_{k}}&{{}=}\\ {{\hat{x}}_{k}}&{{}=}\\ {P_{k}}&{{}=}\end{array}$$

where Vk is a zero-mean random vector with covariance **Rk.** Further assume that the measurement noise at each time step k is independent, that is, E(V&) = *Rkdk-%.* This implies that the measurement noise is white. 

(b) Update the estimate of x and the estimation-error covariance P as follows: 

## 3.3.1 Alternate Estimator Forms

Sometimes it is useful to write the equations for Pk and Kk in alternate forms. 

Although these alternate forms are mathematically identical, they can be beneficial from a computational point of view. They can also lead to new results, which we will discover in later chapters. 

First we will find an alternate form for the expression for the estimation-error covariance. Substituting for Kk from Equation **(3.27)** into Equation **(3.25)** we obtain 

$$P_{k}=\left[I-P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}\right]P_{k-1}[\cdots]^{T}+K_{k}R_{k}K_{k}^{T}\tag{3.31}$$
$$(3.33)$$
$$(3.34)$$
$$(3.35)$$
$$(3.36)$$
$$P_{k}=P_{k-1}-P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}-P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}+\tag{3.32}$$ $$P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}+P_{k-1}H_{k}^{T}S_{k}^{-1}R_{k}S_{k}^{-1}H_{k}P_{k-1}$$
$$=P_{k-1}-2P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}+P_{k-1}H_{k}^{T}S_{k}^{-1}S_{k}S_{k}^{-1}H_{k}P_{k-1}$$ $$=P_{k-1}-2P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}+P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}$$ $$=P_{k-1}-P_{k-1}H_{k}^{T}S_{k}^{-1}H_{k}P_{k-1}$$
$$\begin{array}{r c l}{{P_{k}}}&{{=}}&{{P_{k-1}-K_{k}H_{k}P_{k-1}}}\\ {{}}&{{=}}&{{(I-K_{k}H_{k})P_{k-1}}}\end{array}$$
$$P_{k}=P_{k-1}-P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}H_{k}P_{k-1}$$

This is a simpler equation for Pk [compared with Equation *(3.25)]* but numerical computing problems (i.e., scaling issues) may cause this expression for Pk to not be positive definite, even when Pk-1 and Rk are positive definite. 

We can also use the matrix inversion lemma from Section 1.1.2 to rewrite the measurement update equation for 9. Starting with Equation *(3.33)* we obtain 

$$P_{k}^{-1}=[P_{k-1}-P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}H_{k}P_{k-1}]^{-1}$$

Applying the matrix inversion lemma to this equation gives Inverting both sides of this equation gives 

$$(3.37)$$

$$(3.38)$$
$$(3.39)$$
$$(3.40)$$

This equation for Pk is more complicated in that it requires three matrix inversions, but it may be computationally advantageous in some situations, as will be discussed in Section *6.2.* 
We can use Equation *(3.38)* to derive an equivalent equation for the estimator gain *Kk.* Starting with Equation *(3.27)* we have 

$$P_{k}=\left[P_{k-1}^{-1}+H_{k}^{T}R_{k}^{-1}H_{k}\right]^{-1}$$
$$K_{k}=P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$

Premultiplying the right side by *PkPF',* which is equal to the identity matrix, gives 

$$K_{k}=P_{k}P_{k}^{-1}P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$
$$K_{k}=P_{k}(P_{k-1}^{-1}+H_{k}^{T}R_{k}^{-1}H_{k})P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$

Substituting for *PL1* from Equation **(3.38)** gives 

$$K_{k}=P_{k}(H_{k}^{T}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k-1}H_{k}^{T})(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$

Note the *Pk-1Hr* factor that is on the right of the first term in parentheses. We can multiply this factor inside the first term in parentheses to obtain 

$$K_{k}=P_{k}H_{k}^{T}(I+R_{k}^{-1}H_{k}P_{k-1}H_{k}^{T})(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$

Now bring Hr out to the left side of the parentheses to obtain 

$$\begin{array}{l l l}{{K_{k}}}&{{=}}&{{P_{k}H_{k}^{T}R_{k}^{-1}(R_{k}+H_{k}P_{k-1}H_{k}^{T})(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}}}\\ {{}}&{{=}}&{{P_{k}H_{k}^{T}R_{k}^{-1}}}\end{array}$$

Now premultiply the first parenthetical expression by *Rkl,* and multiply on the inside of the parenthetical expression by *Rk,* to obtain 

## General Recursive Least Squares Estimation

The recursive least squares algorithm can be summarized with the following equations. The measurement equations are given as 

$$(3.41)$$
$$(3.42)$$
$$(3.43)$$
$$(3.44)$$
$$(3.45)$$

The initial estimate of the constant vector 2, along with the uncertainty in that estimate, is given as 

$$\begin{array}{r c l}{{y_{k}}}&{{=}}&{{H_{k}x+v_{k}}}\\ {{}}&{{}}&{{x}}&{{=}}&{{\mathrm{constant}}}\\ {{E(v_{k})}}&{{=}}&{{0}}\\ {{E(v_{k}v_{i}^{T})}}&{{=}}&{{R_{k}\delta_{k-i}}}\end{array}$$
$$\begin{array}{r c l}{{\hat{x}_{0}}}&{{=}}&{{E(x)}}\\ {{P_{0}}}&{{=}}&{{E[(x-\hat{x}_{0})(x-\hat{x}_{0})^{T}]}}\end{array}$$

$$(3.46)$$
$$K_{k}$$
$${\hat{x}}_{k}$$
$$\stackrel{\cdots}{P_{k}}$$

The recursive least squares algorithm is given as follows. 

Fork= 1,2,..., 

$$(3.47)$$

Once again we revisit the problem of trying to estimate the resistance x of an unmarked resistor on the basis of noisy measurements from a multimeter. However, we do not want to wait until we have all the measurements in order to have an estimate. We want to recursively modify our estimate of x each time we obtain a new measurement. At sample time k our measurement is 

$$\begin{array}{rcl}\mathcal{Y}_{k}&=&H_{k}x+v_{k}\\ H_{k}&=&1\\ R_{k}&=&E(v_{k}^{2})\end{array}\tag{3.48}$$

For this scalar problem, the measurement matrix Hk is a scalar, and the measurement noise covariance Rk is also a scalar. We will suppose that each measurement has the same covariance so the measurement covariance Rk is not a function of k, and can be written as R. Initially, before we have any measurements, we have some idea about the value of the resistance x, and this forms our initial estimate. We also have some uncertainty about our initial estimate, and this forms our initial covariance: 

$$\begin{array}{r l}{={}}&{{}E(x)}\\ {={}}&{{}E[(x-{\hat{x}}_{0})(x-{\hat{x}}_{0})^{T}]}\\ {={}}&{{}E[(x-{\hat{x}}_{0})^{2}]}\end{array}$$
$${\hat{x}}_{0}$$

If we have absolutely no idea about the resistance value, then P(0) = *00.* If we are 100% certain about the resistance value before taking any measurements, then *P(0)* = 0 (but then, of course, there would not be any need to take measurements). Equation **(3.47)** tells us how to obtain the estimator gain, the estimate of x, and the estimation covariance, after the first measurement 
(k = 1): 

$$K_{k}=P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$ $$K_{1}=P_{0}(P_{0}+R)^{-1}$$ $$\hat{x}_{k}=\hat{x}_{k-1}+K_{k}(y_{k}-H_{k}\hat{x}_{k-1})$$ $$\hat{x}_{1}=\hat{x}_{0}+\frac{P_{0}}{P_{0}+R}(y_{1}-\hat{x}_{0})$$ $$P_{k}=(I-K_{k}H_{k})P_{k-1}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}$$ $$P_{1}=\frac{P_{0}R}{P_{0}+R}\tag{1}$$  these calculations to find these quantities after the second one 
$$(3.49)$$
$$(3.50)$$

Repeating these calculations to find these quantities after the second measurement (k = 2) gives 

$$K_{2}=\frac{P_{1}}{P_{1}+R}=\frac{P_{0}}{2P_{0}+R}$$ $$P_{2}=\frac{P_{1}R}{P_{1}+R}=\frac{P_{0}R}{2P_{0}+R}$$ $$\hat{x}_{2}=\hat{x}_{1}+\frac{P_{1}}{P_{1}+R}(y_{2}-\hat{x}_{1})$$ $$=\frac{P_{0}+R}{2P_{0}+R}\hat{x}_{1}+\frac{P_{0}}{2P_{0}+R}y_{2}\tag{3.51}$$

By induction, we can find general expressions for Pk-1, Kk, and xk as follows:

$$P_{k-1}=\frac{P_{0}R}{(k-1)P_{0}+R}$$ $$K_{k}=\frac{P_{0}}{kP_{0}+R}$$ $$\hat{x}_{k}=\hat{x}_{k-1}+K_{k}(y_{k}-\hat{x}_{k-1})$$ $$=(1-K_{k})\hat{x}_{k-1}+K_{k}y_{k}$$ $$=\frac{(k-1)P_{0}+R}{kP_{0}+R}\hat{x}_{k-1}+\frac{P_{0}}{kP_{0}+R}y_{k}\tag{3.52}$$

Note that if x is known perfectly a priori (i.e., before any measurements are obtained) then Po = 0, and the above equations show that Kk = 0 and xk = fo. That is, the optimal estimate of x is independent of any measurements that are obtained. On the other hand, if x is completely unknown a priori, then Po -> 00, and the above equations show that

$$\begin{array}{r l}{{\hat{x}}_{k}}&{{}=}\\ {}&{}&{}\\ {}&{}&{}\\ {}&{}&{}\end{array}$$
$$\frac{(k-1)P_{0}}{kP_{0}}\hat{x}_{k-1}+\frac{P_{0}}{kP_{0}}\,y_{k}$$ $$\frac{(k-1)}{k}\hat{x}_{k-1}+\frac{1}{k}y_{k}$$ $$\frac{1}{k}[(k-1)\hat{x}_{k-1}+y_{k}]\tag{3.53}$$

In other words, the optimal estimate of x is equal to the running average of the measurements yk, which can be written as

Ük
$$\begin{array}{l l}{{}}&{{\frac{1}{k}\sum_{j=1}^{k}y_{j}}}\\ {{}}&{{}}\\ {{}}&{{\frac{1}{k}\left(\sum_{j=1}^{k-1}y_{j}+y_{k}\right)}}\\ {{}}&{{}}\\ {{}}&{{\frac{1}{k}\left[(k-1)\left(\frac{1}{k-1}\sum_{j=1}^{k-1}y_{j}\right)+y_{k}\right]}}\\ {{}}&{{}}\\ {{}}&{{\frac{1}{k}\left[(k-1)\tilde{y}_{k-1}+y_{k}\right]}}\end{array}$$
$$(3.54)$$

## Aaa Example 3.4

In this example, we illustrate the computational advantages of the first form of the covariance update in Equation (3.47) compared with the third form. Suppose we have a scalar parameter x and a perfect measurement of it. That is, H1 = 1 and R1 = 0. Further suppose that our initial estimation covariance Po = 6, and our computer provides precision of three digits to the right of the decimal point for each quantity that it computes. The estimator gain K1 is

$$(3.55)$$

computed as 

$$\begin{array}{r c l}{{K_{1}}}&{{=}}&{{P_{0}(P_{0}+R_{1})^{-1}}}\\ {{}}&{{=}}&{{(6)\left(\frac{1}{6}\right)}}\\ {{}}&{{=}}&{{(6)(0.167)}}\\ {{}}&{{=}}&{{1.002}}\end{array}$$

If we use the third form of the covariance update in Equation **(3.47)** we obtain 

$$\begin{array}{r c l}{{P_{1}}}&{{=}}&{{(1-K_{1})P_{0}}}\\ {{}}&{{=}}&{{(-0.002)(6)}}\\ {{}}&{{=}}&{{-0.012}}\end{array}$$

$$(3.56)$$

$$(3.57)$$
= -0.012 **(3.56)** 
The covariance after the first measurement is negative, which is physically impossible. However, if we use the first form of the covariance update in Equation **(3.47)** we obtain 

$$\begin{array}{r l}{={}}&{{}(1-K_{1})P_{0}(1-K_{1})+K_{1}R_{1}K_{1}}\\ {={}}&{{}(1-K_{1})^{2}P_{0}+K_{1}^{2}R_{1}}\\ {={}}&{{}0}\end{array}$$
$$P_{1}$$
=o **(3.57)** 
The reason we get zero is because (1 - *KI)~* = 0.000004, but our computer retains only three digits to the right of the decimal point. Zero is the theoretically correct value of **PI.** The form of the above expression for PI guarantees that it will never be negative, regardless of any numerical errors in PO, *R1,* 
and *K1.* 
vvv 

Suppose that a tank contains a concentration 21 of chemical 1, and a concentration 22 of chemical 2. You have some instrumentation that can detect the combined concentration (21 + *22)* of the two chemicals, but your instrumentation cannot distinguish between the two chemicals. Chemical 2 is removed from the tank through a leaching process so that its concentration decreases by 1% from one measurement time to the next. The measurement equation is therefore given as 

$$\begin{array}{r l}{={}}&{{}x_{1}+0.99^{k-1}x_{2}+v_{k}}\\ {={}}&{{}{\left[\begin{array}{l l}{1}&{0.99^{k-1}}\end{array}\right]x+v_{k}}\end{array}}\end{array}$$
$$y_{k}$$
$$(3.58)$$

where Vk is the measurement noise, which is a zero-mean random variable with a variance of R = **0.01.** Suppose that 21 = 10 and 52 = 5. Further suppose that your initial estimates are $1 = 8 and $2 = 7, with an initial estimation-error variance Po that is equal to the identity matrix. A recursive least squares algorithm can be implemented as shown in Equation **(3.47)** to estimate the two concentrations. Figure **3.1** shows the estimate of 21 and 22 as measurements are obtained, along with the variance of the estimation errors. 

It can be seen that after a couple dozen measurements the estimates become quite close to their true values of 10 and 5. The variances of the estimation errors asymptotically approach zero, which means that we have increasingly more confidence in our estimates as we obtain more measurements. 

![13_image_0.png](13_image_0.png)

3 **.5~** 0 
Figure **3.1** Parameter estimates and estimation variances for Example **3.5.** 
vvv 

## 3.3.2 Curve Fitting

In this section, we will apply recursive least squares theory to the curve fitting problem. In the recursive curve fitting problem, we measure data one sample at a time *(yl,* y2, ...) and want to find the best fit of a curve to the data. The curve that we want to fit to the data could be constrained to be linear, or quadratic, or sinusoid, or some other shape, depending on the underlying problem. 

## Example38

Suppose that we want to fit a straight line to a set of data points. The linear data fitting problem can be written as 

$$y_{k}=x_{1}+x_{2}t_{k}+v_{k}$$ $$E(v_{k}^{2})=R_{k}\tag{3.59}$$
$$(3.60)$$
$$H_{k}={\left[\begin{array}{l l}{1}&{t_{k}}\end{array}\right]}$$

tk is the independent variable (perhaps time), Yk is the noisy data, and we want to find the linear relationship between yk and *tk.* In other words, we want to estimate the constants 21 and *22.* The measurement matrix can be written as Hk=[ 1 tk ] (3.60) 

$$(3.61)$$
$$y_{k}=H_{k}x+v_{k}$$

so that Equation **(3.59)** can be written as Our recursive estimator is initialized as 

$$\hat{x}_{0}=E(x)$$ $$\left[\begin{array}{c}\hat{x}_{1,0}\\ \hat{x}_{2,0}\end{array}\right]=\left[\begin{array}{c}E(x_{1})\\ E(x_{2})\end{array}\right]$$ $$P_{0}=E[(x-\hat{x}_{0})(x-\hat{x}_{0})^{T}]$$ $$=\left[\begin{array}{cc}E[x_{1}-\hat{x}_{1,0}{}^{2}]&E[(x_{1}-\hat{x}_{1,0})(x_{2}-\hat{x}_{2,0})]\\ E[(x_{1}-\hat{x}_{1,0})(x_{2}-\hat{x}_{2,0})]&E[x_{2}-\hat{x}_{2,0}{}^{2}]\end{array}\right]\tag{3.6}$$  The recursive estimate of the two-element vector $x$ is then obtained from 
Equation **(3.47)** as follows: 
For k = *l,2,...,* 
$$\big|\ \ (3.62)$$
$$K_{k}=P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$ $$\hat{x}_{k}=\hat{x}_{k-1}+K_{k}(y_{k}-H_{k}\hat{x}_{k-1})$$ $$P_{k}=(I-K_{k}H_{k})P_{k-1}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}\tag{3.63}$$

## Vvv Example3.7

Suppose that we know a *priori* that the underlying data is a quadratic function of time. In this case, we have a quadratic data fitting problem. For example, suppose we are measuring the altitude of a free-falling object. We know from our understanding of physics that altitude r is a function of the acceleration due to gravity, the initial altitude and velocity of the object TO and TJO, and time t, as given by the equation r = ro + vot + *(a/2)t2. So* if we measure T 
at various time instants and fit a quadratic to the resulting r versus t curve, then we have an estimate of the parameters *7-0,* **210,** and *a/2.* In general, the quadratic data fitting problem can be written as 

$$y_{k}=x_{1}+x_{2}t_{k}+x_{3}t_{k}^{2}+v_{k}$$ $$E(v_{k}^{2})=R_{k}\tag{3.64}$$
$$(3.65)$$
$$(3.66)$$
$$(3.67)$$

tk is the independent variable, Yk is the noisy measurement, and we want to find the quadratic relationship between Yk and *tk.* In other words, we want to estimate the constants *XI, 22,* and 23. The measurement matrix can be written as 

so that Equation **(3.64)** can be written as 
$$H_{k}={\left[\begin{array}{l l l}{1}&{t_{k}}&{t_{k}^{2}}\end{array}\right]}$$ be written as 
Yk = *HkX* + Vk **(3.66)** 
Our recursive estimator is initialized as 

$$y_{k}=H_{k}x+v_{k}$$
$$\begin{array}{r c l}{{\hat{x}_{0}}}&{{=}}&{{E(x)}}\\ {{P_{0}}}&{{=}}&{{E[(x-\hat{x}_{0})(x-\hat{x}_{0})^{T}]}}\end{array}$$

where Po is a 3 x 3 matrix. The recursive estimate of the three-element vector z is then obtained from Equation (3.47) as follows: 
For k = 1,2,. . ., 

$$K_{k}=P_{k-1}H_{k}^{T}(H_{k}P_{k-1}H_{k}^{T}+R_{k})^{-1}$$ $$\hat{x}_{k}=\hat{x}_{k-1}+K_{k}(y_{k}-H_{k}\hat{x}_{k-1})$$ $$P_{k}=(I-K_{k}H_{k})P_{k-1}(I-K_{k}H_{k})^{T}+K_{k}R_{k}K_{k}^{T}\tag{3.68}$$

vvv 

## 3.4 W I En E R F I Lt E R **I N** G

In this section, we will give a brief review of Wiener filtering. The rest of this book does not assume any knowledge on the reader's part of Wiener filtering. However, Wiener filtering is important from a historical perspective, and it still has a lot of applications in signal processing and communication theory. But since it is not used much for state estimation anymore, the reader can safely skip this section if desired. 

Wiener filtering addresses the problem of designing a linear, timeinvariant filter to extract a signal from noise, approaching the problem from the frequency domain perspective. Norbert Wiener invented his filter as part of the World War I1 effort for the United States. He published his work on the problem in 1942, but it was not available to the public until 1949 [Wie64]. His book was known as the "yellow peril" because of its mathematical difficulty and its yellow cover [Deu65, page 1761. Andrey Kolmogorov actually solved a more general problem earlier (1941), and Mark Krein also worked on the same problem (1945). Kolmogorov's and Krein's work was independent of Wiener's work, and Wiener acknowledges that Kolmogorov's work predated his own work [Wie56]. However, Kolmogorov's and Krein's work did not become well known in the Western world until later, since it was published in Russian [Ko141]. A nontechnical account of Wiener's work is given in his autobiography [Wie56]. 

To set up the presentation of the Wiener filter, we first need to ask the following question: How does the power spectrum of a stochastic process *z(t)* change when it goes through an LTI system with impulse response *g(t)?* The output y(t) of the system is given by the convolution of the impulse response with the input: 
Y(t) = *dt)* * 4t) (3.69) 
Since the system is time-invariant, a time shift in the input results in an equal time shift in the output: 
y(t + a) = **g(t)** * *z(t* + a) (3.70) 
Multiplying the above two equations and writing out the convolutions as integrals gives 

$$y(t)y(t+\alpha)=\int g(\tau)x(t-\tau)\,d\tau\int g(\gamma)x(t+\alpha-\gamma)\,d\gamma$$
$$y(t)=g(t)*x(t)$$
$$y(t+\alpha)=g(t)*x(t+\alpha)$$
$$E[y(t)y(t+\alpha)]=\int\int g(\tau)g(\gamma)E[x(t-\tau)x(t+\alpha-\gamma)]\,d\tau\,d\gamma$$

Taking the expected value of both sides of the above equation gives the autocorre lation of y(t) as a function of the autocorrelation of *z(t):* 

$$(3.69)$$

$$(3.70)$$
$$(3.71)$$
$$(3.72)$$
$$R_{y}(\alpha)=\int\int g(\tau)g(\gamma)R_{x}(\alpha+\tau-\gamma)\,d\tau\,d\gamma$$

which we will write in shorthand notation as 

$$(3.73)$$
$$(3.75)$$

Now we take the Fourier transform of the above equation to obtain 

$$\int R_{y}(\alpha)e^{-j\omega\alpha}\,d\alpha=\int\int g(\tau)g(\gamma)R_{x}(\alpha+\tau-\gamma)e^{-j\omega\alpha}\,d\tau\,d\gamma\,d\alpha\tag{3.74}$$  Now we define a new variable of integration $\beta=\alpha+\tau-\gamma$ and replace $\alpha$ in the 
above equation to obtain 
$$\begin{array}{r c l}{{S_{y}(\omega)}}&{{=}}&{{\int\int\int g(\tau)g(\gamma)R_{x}(\beta)e^{-j\omega\beta}e^{-j\omega\gamma}e^{j\omega\tau}\,d\tau\,d\gamma\,d\beta}}\\ {{}}&{{=}}&{{G(-\omega)G(\omega)S_{x}(\omega)}}\end{array}$$

In other words, the power spectrum of the output y(t) is a function of the Fourier transform of the impulse response of the system, *G(w),* and the power spectrum of the input *z(t).* 
Now we can state our problem as follows: Design a stable LTI filter to extract a signal from noise. The quantities of interest in this problem are given as 

$${\mathrm{noise~free~signal}}$$ additive noise
$$\begin{array}{r l}{x(t)}&{{}=}\\ {v(t)}&{{}=}\end{array}$$
z(t) = noise free signal 
w(t) = additive noise 
$v(t)=$ additive noise  $g(t)=$ filter impulse response (to be designed)  $\hat{x}(t)=$ output of filter [estimate of $x(t)$]  $e(t)=$ estimation error  $=$$x(t)-\hat{x}(t)$

![16_image_0.png](16_image_0.png)

$$(3.76)$$

Figure **3.2** Wiener filter representation. 

![16_image_1.png](16_image_1.png)

These quantities are represented in Figure **3.2,** from which we see that 

$$\begin{array}{r l}{{\hat{x}}(t)}&{{}=}\\ {{\hat{X}}(\omega)}&{{}=}\\ {E(\omega)}&{{}=}\\ {\quad}&{{}=}\\ {\quad}&{{}=}\\ {\quad}&{{}=}\end{array}$$
$$(3.77)$$
?(t> = *dt)* * Mt) + *4t)l* 
$$(3.78)$$
E(w) = X(w) -X(w) 
X(w) = G(w)[X(w) + *V(w)]* 
$$\begin{array}{l}{{g(t)*[x(t)+v(t)]}}\\ {{G(\omega)[X(\omega)+V(\omega)]}}\\ {{X(\omega)-\hat{X}(\omega)}}\\ {{X(\omega)-G(\omega)[X(\omega)+V(\omega)]}}\\ {{[1-G(\omega)]X(\omega)-G(\omega)V(\omega)}}\end{array}$$

We see that the error signal *e(t)* is the superposition of the system *[l -G(w)]* acting on the signal *z(t),* and the system *G(w)* acting on the signal w(t). Therefore, from Equation **(3.75),** we obtain 

$$S_{e}(\omega)=[1-G(\omega)][1-G(-\omega)]S_{x}(\omega)-G(\omega)G(-\omega)S_{v}(\omega)$$

The variance of the estimation error is obtained from Equation (2.92) as 

$$E[e^{2}(t)]=\frac{1}{2\pi}\int S_{e}(\omega)\,d\omega\tag{3.79}$$
$$(3.80)$$

To find the optimal filter *G(w)* we need to minimize *E[e2(t)],* which means that we need to know Sz(w) and *Sv(w),* the statistical properties of the signal *z(t)* and the noise w (t ) . 

## 3.4.1 Parametric Filter Optimization

In order to simplify the problem of the determination of the optimal filter *G(w),* we can assume that the optimal filter is a first-order, low-pass filter (stable and 
causal3) with a bandwidth 1/T to be determined by parametric optimization. 
$$\frac{1}{1+T j\omega}$$
1 + *Tjw G(w)* = - (3.80) 
This may not be a valid assumption, but it reduces the problem to a parametric 
optimization problem. In order to simplify the problem further, suppose that *Sz(w)* and *S,(w)* are in the following forms. 
$$G(\omega)={\overline{{1}}}$$
2u2p *Sz(W)* = - 
$$\frac{2\sigma^{2}\beta}{\omega^{2}+\beta^{2}}$$ $$A$$
Sv(w) = A (3.81) 
In other words, the noise w(t) is white. From Equation (3.78) we obtain 

$$\begin{array}{r l}{S_{x}(\omega)}&{{}=}\\ {S_{v}(\omega)}&{{}=}\end{array}$$
$$\begin{array}{r c l}{{S_{e}(\omega)}}&{{=}}&{{\left(\frac{T j\omega}{1+T j\omega}\right)\left(\frac{-T j\omega}{1-T j\omega}\right)\left(\frac{2\sigma^{2}\beta}{\omega^{2}+\beta^{2}}\right)-}}\\ {{}}&{{}}&{{\left(\frac{1}{1+T j\omega}\right)\left(\frac{1}{1-T j\omega}\right)A}}\end{array}$$
$$T_{\mathrm{opt}}={\frac{\sqrt{A}}{\sigma{\sqrt{2\beta}}-\beta{\sqrt{A}}}}$$

Now we can substitute *Se(w)* in Equation (3.79) and differentiate with respect to T to find 

$$(3.81)$$
$$(3.82)$$
$$(3.83)$$

If A = 0 = p = 1 then the optimal time constant of the filter is computed as 

$$\begin{array}{r c l}{{T}}&{{=}}&{{\frac{1}{\sqrt{2}-1}}}\\ {{}}&{{}}&{{\approx}}&{{2.4}}\end{array}$$

and the optimal filter is given as 
$$G(\omega)\quad=\quad\frac{1}{1+j\omega T}$$
1 + *jwT G(w)* = - 
$$(3.84)$$
3A causal system is one whose output depends only on present and .future inputs. Real-world systems are always causal, but a filter that is used for postprocessing may be noncausal. 

$$\begin{array}{r l}{={}}&{{}{\frac{1/T}{1/T+j\omega}}}\\ {g(t)}&{{}={}}&{{}{\frac{1}{T}}e^{-t/T}\quad t\geq0}\end{array}$$
$$(3.85)$$

Converting this filter to the time domain results in 

$${\dot{\hat{x}}}={\frac{1}{T}}(-{\hat{x}}+y)$$

$$(3.86)$$

vvv 

## 3.4.2 General Filter Optimization

Now we take a more general approach to find the optimal filter. The expected value of the estimation error can be computed as 

$$e(t)=x(t)-\hat{x}(t)$$ $$e^{2}(t)=x^{2}(t)-2x(t)\hat{x}(t)+\hat{x}^{2}(t)$$ $$=x^{2}(t)-2x(t)\int g(u)[x(t-u)+v(t-u)]\,du+$$ $$\int\int g(u)g(\gamma)[x(t-u)+v(t-u)]\times$$ $$[x(t-v)+v(t-v)]\,du\,d\gamma$$ $$E[e^{2}(t)]=E[x^{2}(t)]-2\int g(u)R_{x}(u)\,du+$$ $$\int\int g(u)g(\gamma)[R_{x}(u-v)+R_{v}(u-v)]\,du\,d\gamma\tag{3.87}$$

Now we can use a calculus of variations approach [FomOO, Wei74] to find the filter g(t) that minimizes *E[e2(t)].* Replace *g(t)* in the above equation with g(t) + *Eq(t),* 
where E is some small number, and *q(t)* is an arbitrary perturbation in *g(t).* The calculus of variations says that we can minimize *E(e2(t))* by setting 

$$(3.88)$$
$$\left.{\frac{\partial E(e^{2}(t))}{\partial\epsilon}}\right|_{\epsilon=0}=0$$
$$R_{\varepsilon}(0)=R_{x}(0)-2\int[g(u)+\epsilon\eta(u)]R_{x}(u)\,du+\tag{3.89}$$ $$\int\int[g(u)+\epsilon\eta(u)][g(\gamma)+\epsilon\eta(\gamma)][R_{x}(u-\gamma)+R_{v}(u-\gamma)]\,du\,d\gamma$$

and thus solve for the optimal *g(t).* From Equation (3.87) we can write Taking the partial derivative with respect to E gives 

aRe(0) OE aRe(0) ರಿє =0 -2 -2
$$-2\int\eta(u)R_{x}(u)\,du+$$ $$\int\int[\eta(u)g(\gamma)+\eta(\gamma)g(u)+2\epsilon\eta(u)\eta(\gamma)]\times$$ $$[R_{x}(u-v)+R_{v}(u-\gamma)]\,du\,d\gamma$$ $$-2\int\eta(\tau)R_{x}(\tau)\,d\tau+$$ $$\int\int\eta(\tau)g(\gamma)[R_{x}(\tau-\gamma)+R_{v}(\tau-\gamma)]\,d\tau\,d\gamma+$$ $$\int\int\eta(\tau)g(u)[R_{x}(u-\tau)+R_{w}(u-\tau)]\,d\tau\,du\tag{3.90}$$
Now recall from Equation (2.87) that Rx (7 - u) = Rx (u - 7) [i.e., R2(r) is even] if x(t) is stationary. In this case, the above equation can be written as

$$0=-2\int\eta(\tau)R_{x}(\tau)\,d\tau+\tag{3.91}$$ $$2\int\int\eta(\tau)g(u)[R_{x}(u-\tau)+R_{v}(u-\tau)]\,d\tau\,du$$

This gives the necessary condition for the optimality of the filter g(t) as follows:

$$\int\eta(\tau)\left[-R_{x}(\tau)+\int g(u)[R_{x}(u-\tau)+R_{v}(u-\tau)]\,du\right]d\tau=0\tag{3.92}$$

We need to solve this for g(t) to find the optimal filter.

## 3.4.3 Noncausal Filter Optimization

If we do not have any restrictions on causality of our filter, then g(t) can be nonzero for t < 0, which means that our perturbation n(t) can also be nonzero for t < 0. This means that the quantity inside the square brackets in Equation (3.92) must be zero. This results in

$$R_{x}(\tau)=\int g(u)[R_{x}(u-\tau)+R_{v}(u-\tau)]\,du\tag{3.93}$$ $$=g(\tau)*[R_{x}(\tau)+R_{v}(\tau)]$$ $$S_{x}(\omega)=G(\omega)[S_{x}(\omega)+S_{v}(\omega)]$$ $$G(\omega)=\frac{S_{x}(\omega)}{S_{x}(\omega)+S_{v}(\omega)}$$

The transfer function of the optimal filter is the ratio of the power spectrum of the signal x(t) to the sum of the power spectrums of x(t) and the noise v(t).

$$(3.94)$$

Consider the system discussed in Example *3.8* with A = ,8 = u = 1. The signal and noise power spectra are given as 

$$\begin{array}{l l l}{{S_{x}(\omega)}}&{{=}}&{{\frac{2}{\omega^{2}+1}}}\\ {{S_{v}(\omega)}}&{{=}}&{{1}}\end{array}$$

From this we obtain the optimal noncausal filter from Equation *(3.93)* as 

2 G(w) = - 
$$G(\omega)=\frac{2}{\omega^{2}+3}\tag{1}$$ $$=\frac{1}{\sqrt{3}}\left(\frac{2\sqrt{3}}{\omega^{2}+3}\right)$$ $$g(t)=\frac{1}{\sqrt{3}}e^{-\sqrt{3}|t|}$$ $$\approx0.58e^{-0.58|t|},\ \ \ \ t\in[-\infty,\infty]$$
-- *(3.96)* 
causal filter anticausal filter 
$$(3.95)$$
In order to find a time domain representation of the filter, we perform a partial fraction expansion of G(w) to find the causal part and the anticausa14 part of the filter5: From this we see that 

= R,(w) + X&) (3.97) 
Xc(w) and *Xa(y)* (defined by the above equation) are the causal and anticausal part of *X(w),* respectively. In the time domain, this can be written as 

$$(3.96)$$
$$(3.97)$$
$$\hat{x}(t)=\hat{x}_{c}(t)+\hat{x}_{a}(t)$$ $$\hat{x}_{c}=-\sqrt{3}\hat{x}_{c}+y/\sqrt{3}$$ $$\hat{x}_{a}=\sqrt{3}\hat{x}_{a}-y/\sqrt{3}\tag{3.98}$$

The i, equation runs forward in time and is therefore causal and stable. The fa equation runs backward in time and is therefore anticausal and stable. (If it ran forward in time, it would be unstable.) 
vvv 

4An anticausal system is one **whose** output depends only on present and future inputs. 

5The MATLAB function RESIDUE performs partial fraction expansions. 

## 3.4.4 Causal Filter Optimization

If we require a causal filter for signal estimation, then *g(t)* = 0 for t < 0, and the perturbation *q(t)* must be equal to 0 for t < 0. In this case, Equation (3.92) gives 

$$R_{x}(\tau)-\int g(u)[R_{x}(u-\tau)+R_{v}(u-\tau)]\,du=0,\quad\ t\geq0\tag{3.99}$$

The initial application of this equation was in the field of astrophysics in 1894 [Sob631 Explicit solutions were thought to be impossible, but Norbert Wiener and Eberhard Hopf became instantly famous when they solved this equation in 1931. Their solution was so impressive that the equation became known as the Wiener-Hopf equation. 

To solve Equation (3.99), postulate some function *a(t)* that is arbitrary for t < 0, but is equal to 0 for t 2 0. Then we obtain 

$$\begin{array}{r c l}{{R_{x}(\tau)-\int g(u)[R_{x}(u-\tau)+R_{v}(u-\tau)]\,d u}}&{{=}}&{{a(\tau)}}\\ {{}}&{{}}&{{}}\\ {{S_{x}(\omega)-G(\omega)[S_{x}(\omega)+S_{v}(\omega)]}}&{{=}}&{{A(\omega)}}\end{array}$$

For ease of notation, make the following definition: 

$$S_{x v}(\omega)=S_{x}(\omega)+S_{v}(\omega)$$
$$S_{x}(\omega)-G(\omega)S_{x v}^{+}(\omega)S_{x v}^{-}(\omega)=A(\omega)$$
S,,(w) = Sz(w) + *%(w)* (3.101) 
Then Equation (3.100) becomes 
- G(w)S,+,(4S,-,(w> = *A(w)* (3.102) 
where *S&(w)* is the part of *Szv(w)* that has all its poles and zeros in the LHP (and hence corresponds to a causal time function), and *S&(w)* is the part of *SZ,(w)* that has all its poles and zeros in the RHP (and hence corresponds to an anticausal time function). Equation (3.102) can be written as 

$$(3.100)$$
$$(3.101)$$
$$(3.102)$$

$$(3.103)$$

The term on the left side corresponds to a causal time function [assuming that g(t) is stable]. The last term on the right side corresponds to an anticausal time function. Therefore, 

$$G(\omega)S_{x v}^{+}(\omega)=\frac{S_{x}(\omega)}{S_{x v}^{-}(\omega)}-\frac{A(\omega)}{S_{x v}^{-}(\omega)}$$

s;v (w ) *G(w)S,f,(w)* = causal part of - 
$$G(\omega)S^{+}_{xv}(\omega)=\mbox{causal part of}\frac{S_{x}(\omega)}{S^{-}_{xv}(\omega)}\tag{3.104}$$ $$G(\omega)=\frac{1}{S^{+}_{xv}(\omega)}\left[\mbox{causal part of}\frac{S_{x}(\omega)}{S^{-}_{xv}(\omega)}\right]$$

## ~(W) = [ Causal Part Of - (3.104) 
This Gives The Tf Of The Optimal Causal Filter. Example 3.10

Consider the system discussed in Section 3.4.1 with A = ,8 = u = 1. This was also discussed in Example 3.9. For this example we have 

$$\begin{array}{r c l}{{S_{x}(\omega)}}&{{=}}&{{\frac{2}{\omega^{2}+1}}}\end{array}$$

$$\begin{array}{r c l}{{S_{v}(\omega)}}&{{=}}&{{1}}\\ {{S_{x v}(\omega)}}&{{=}}&{{\frac{\omega^{2}+3}{\omega^{2}+1}}}\end{array}$$
$$(3.105)$$

Splitting this up into its causal and anticausal factors gives 

$$S_{vv}(\omega)=\underbrace{\left(\frac{j\omega+\sqrt{3}}{j\omega+1}\right)\left(\frac{-j\omega+\sqrt{3}}{-j\omega+1}\right)}_{S_{vv}^{*}(\omega)}$$ $$\frac{S_{x}(\omega)}{S_{vv}^{-}(\omega)}=\frac{2(-j\omega+1)}{(\omega^{2}+1)(-j\omega+\sqrt{3})}$$ $$=\frac{2}{(-j\omega+\sqrt{3})(j\omega+1)}$$ $$=\frac{\sqrt{3}-1}{j\omega+1}\quad+\quad\frac{\sqrt{3}-1}{-j\omega+\sqrt{3}}\tag{3.106}$$ $$\text{causal part}\quad\text{anticausal part}$$

Equation *(3.104)* gives 

$$G(\omega)=\left(\frac{j\omega+1}{j\omega+\sqrt{3}}\right)\left(\frac{\sqrt{3}-1}{j\omega+1}\right)\tag{3.107}$$ $$=\frac{\sqrt{3}-1}{j\omega+\sqrt{3}}$$ $$g(t)=(\sqrt{3}-1)e^{-\sqrt{3}t},\ \ \ \ t\geq0$$

This gives the TF and impulse response of the optimal filter when causality is required. 

vvv 

## 3.4.5 Comparison

Comparing the three examples of optimal filter design presented in this section (Examples 3.8, 3.9, and *3.10),* it can be shown that the mean square errors of the filter are as fdlows *[Bro96]:* 
0 Parameter optimization method: E[e2(t)] = *0.914* 0 Causal Wiener filter: E[e2(t)] = *0.732* 0 Noncausal Wiener filter: E[e2(t)] = *0.577* As expected, the estimation error decreases when we have fewer constraints on the filter. However, the removal of constraints makes the filter design problem more difficult. The Wiener filter is not very amenable to state estimation because of difficulty in extension to MIMO problems with state variable descriptions, and difficulty in application to signals with time-varying statistical properties. 

## 3.5 Summary

In this chapter we discussed least squares estimation in a couple of different contexts. First we derived a method for estimating a constant vector on the basis of several noisy measurements of that vector. In fact, the measurements do not have to be direct measurements of the constant vector, but they can be measurements of some linear combination of the elements of the constant vector. In addition, the noise associated with each measurement does not have to be the same. The least squares estimation technique that we derived assumed that we the measurement noise is zero-mean and white (uncorrelated with itself from one time step to the next), and that we know the variance of the measurement noise. We then extended our least squares estimator to a recursive formulation, wherein the computational effort remains the same at each time step regardless of the total number of measurements that we have processed. Least squares estimation of a constant vector forms a large part of the foundation for the Kalman filter, which we will derive later in this book. 

In Section **3.4,** we took a brief segue into Wiener filtering, which is a method of estimating a time-varying signal that is corrupted by noise. The Wiener filter is based on frequency domain analyses, whereas the Kalman filter that we derive later is based on time domain analyses. Nevertheless, both filters are optimal under their own assumptions. Some problems are solvable by both the Wiener and Kalman filter methods, in which case both methods give the same result. 

## Problems Written Exercises

3.1 In Equation **(3.6)** we computed the partial derivative of our cost function with respect to our estimate and set the result equal to 0 to solve for the optimal estimate. 

However, the solution minimizes the cost function only if the second derivative of the cost function with respect to the estimate is positive semidefinite. Find the second derivative of the cost function and show that it is positive semidefinite. 3.2 Prove that the matrix Pk that is computed from Equation **(3.25)** will always be positive definite if 9-1 and Rk are positive definite. 

3.3 Consider the recursive least squares estimator of Equations **(3.28)-(3.30).** If zero information about the initial state is available, then Po = *001.* Suppose that you have a system like this with Hk = 1. What will be the values of K1 and *PI?* 
3.4 Consider a battery with a completely unknown voltage *(PO* = m). Two independent measurements of the voltage are taken to estimate the voltage, the first with a variance of 1, and the second with a variance of 4. 

a) Write the weighted least squares voltage estimate in terms of the two measurements y1 and **y2.** 
b) If weighted least squares is used to estimate the voltage, what is the variance of voltage estimate after the first measurement? What is the variance of the voltage estimate after the second measurement? 

c) If the voltage is estimated as (y1 + y2)/2, an unweighted average of the measurements, what is the variance of the voltage estimate? 

3.5 Consider a battery whose voltage is a random variable with a variance of 1. 

Two independent measurements of the voltage are taken to estimate the voltage, the first with a variance of 1, and the second with a variance of 4. 

a) Write the weighted least squares voltage estimate in terms of the initial estimate 30 and the two measurements y1 and y2. 

b) If weighted least squares is used to estimate the voltage, what is the variance of voltage estimate after the first measurement? What is the variance of the voltage estimate after the second measurement? 

3.6 Suppose that *{z1,xz,* * , z,} is a set of random variables, each with mean 3 and variance *a2.* Further suppose that **E[(x2** - *3)(x,* - Z)] = 0 for i \# j. We estimate 3 and u2 as follows. 

$$\begin{array}{r c l}{{{\hat{\vec{x}}}}}&{{=}}&{{{\frac{1}{n}}\sum_{i=1}^{n}x_{i}}}\\ {{{\hat{\sigma}}^{2}}}&{{=}}&{{{\frac{1}{n}}\sum_{i=1}^{n}(x_{i}-{\hat{\vec{x}}})^{2}}}\end{array}$$

a) Is 5 an unbiased estimate of z? That is, is *E(2)* = Z? 

b) Find *E(xgj)* in terms of 1 and u2 for both i = j and i \# j. 

c) Is b2 an unbiased estimate of *a2?* That is, is E($) = *u2?* If not, how should we change 6' to make it an unbiased estimate of *u2?* 
3.7 Suppose a scalar signal has the values 1, 2, and 3. Consider three different estimates of this timevarying signal. The first estimate is 3, 4, 1. The second estimate is 1, 2, 6. The third estimate is 5, 6, 7. Create a table showing the RMS 
value, average absolute error, and standard deviation of the error of each estimate. Which estimate results in the error with the smallest RMS value? Which estimate results in the error with the smallest infinity-norm? Which estimate gives the error with the smallest standard deviation? Which estimate do you think is best from an intuitive point of view? Which estimate do you think is worst from an intuitive point of view? 

3.8 Suppose a random variable x has the pdf *f(x)* given in Figure **3.3.** 
a) x can be estimated by taking the median of its pdf. That is, P is the 
solution to the equation 
$$f(x)\,d x=\int_{\hat{x}}^{\infty}f(x)\,d x$$
Find the median estimate of x. 
b) x can be estimated by taking the mode of its pdf. That is, 
$$\int_{-\infty}^{\pm}$$
f = arg maxf(x) 
Find the mode estimate of x. 

c) x can be estimated by computing its mean. That is, 

$${\hat{x}}=\int_{-\infty}^{\infty}x f(x)\,d x$$

Find the mean of z. 

d) z can be estimated by computing the minimax value. That is, 2 = minmaxlz - $1 X 
Find the minimax estimate of z. 

![25_image_0.png](25_image_0.png)

Figure **3.3** pdf for Problem **3.8.** 
3.9 Suppose you are responsible for increasing the tracking accuracy of a radar system. You presently have a radar that **has** a measurement variance of 10. For equal cost you could either: (a) optimally combine the present radar system with a new radar system that has a measurement variance of 6; or, (b) optimally combine the present radar system with two new radar systems that both have the same performance as the original system [May79]. Which would you propose to do? 

Why? 

3.10 Consider the differential equation 

$$S_{x}(s)={\frac{1-s^{2}}{s^{4}-5s^{2}+4}}$$

k+3z=u If the input *u(t)* is an impulse, there are two solutions *z(t)* that satisfy the differential equation. One solution is causal and stable, the other solution is anticausal and unstable. Find the two solutions. 

3.11 Suppose a signal *z(t)* with power spectral density is corrupted with additive white noise *v(t)* with a power spectral density *Sv(s)* = 1. 

a) Find the optimal noncausal Wiener filter to extract the signal from the noise corrupted signal. 

b) Find the optimal causal Wiener filter to extract the signal from the noise corrupted signal. 

3.12 A system has the transfer function 
$$G(s)={\frac{1}{s-3}}$$
G(s) = - 
If the input is an impulse, there are two solutions for the output *z(t)* that satisfy the transfer function. One solution is causal and unstable, the other solution is anticausal and stable. Find the two solutions. 

## Computer Exercises

3.13 The production of steel in the United States between 1946 and 1956 was 66.6,84.9,88.6,78.0,96.8, 105.2,93.2, 111.6,88.3,117.0, and 115.2milliontons [Sor80]. 

Find the least squares fit to these data using (a) linear curve fit; (b) quadratic curve fit; (c) cubic curve fit; (d) quartic curve fit. For each case give the following: (1) a plot of the original data along with the least squares curve; **(2)** the RMS error of the least squares curve; (3) the prediction of steel production in 1957. 

3.14 Implement the Wiener filters for the three examples given in Section 3.4 
and verify the results shown in Section 3.4.5. Hint: Example 8.6 shows that if 
j. = -z + w where *w(t)* is white noise with a variance of Qc = 2, then 
$$S_{x}(\omega)=\frac{2}{\omega^{2}+1}$$
L *SZ(W)* = - 
$$\begin{array}{r c l}{{x(t+\Delta t)}}&{{=}}&{{e^{-\Delta t}x(t)+w(t)\sqrt{Q_{e}\Delta t}}}\\ {{}}&{{}}&{{y(t)}}&{{=}}&{{x(t)+v(t)\sqrt{R_{e}/\Delta t}}}\end{array}$$
From Sections 1.4 and 8.1 we see that this system can be simulated as where w *(t)* and v(t) are independent zero-mean, unity variance random variables. 