---
type: chapter
chapter: 14
title: The unscented Kalman filter
---
# Chapter 14 The Unscented Kalman Filter

We use the intuition that it is easier to approximate a probability distribution than it is to approximate an arbitrary nonlinear function or transformation. 

-Simon Julier, Jeffrey Uhlmann, **and** Hugh Durrant-Whyte [JulOO] 
As discussed earlier, the extended Kalman filter (EKF) is the most widely ap plied state estimation algorithm for nonlinear systems. However, the EKF can be difficult to tune and often gives unreliable estimates if the system nonlinearities are severe. This is because the EKF relies on linearization to propagate the mean and covariance of the state. This chapter discusses the unscented Kalman filter (UKF), an extension of the Kalman filter that reduces the linearization errors of the EKF. The use of the UKF can provide significant improvement over the EKF. 

First, we will take a diversion from filtering in Section **14.1** to investigate how means and covariances propagate in nonlinear equations. In Section **14.2,** we will present the unscented transformation, which is a way to approximate how the mean and covariance of a random variable change when the random variable undergoes a nonlinear transformation. In Section **14.3,** we will use the previous results to derive the UKF and show that it has less linearization error than the EKF. In Section **14.4,** we will present some modifications of the standard UKF which can be used to obtain more accurate or faster filtering results. 

## 14.1 Means And Covariances Of Nonlinear Transformations

In this section, we will show how linearization approximations can result in errors in the transformation of means and covariances when a random variable is operated on by a nonlinear function. This section does not really have anything to do directly with state estimation, Kalman filtering, or the UKF. However, this section provides some background that will allow us to develop the UKF later in this chapter. This section will also give us a more complete background to understand the type of problems that can arise in the EKF (which relies on linearization). 

Consider the nonlinear transformation 

$$\begin{array}{l}{r\cos\theta}\\ {r\sin\theta}\end{array}$$
$$y_{1}=$$ $$y_{2}=$$
$$(14.1)$$
y1 = rcose 
y2 = rsin8 (14.1) 
This is a standard polar-to-rectangular coordinate transformation. For instance, we might have a sensor that measures range r and angle 8, and we want to convert the measured data to rectangular coordinates y1 and **y2.** The coordinate transformation can be written more generally as 

$$(14.2)$$
$$y=h(x)$$

$$(14.3)$$
Y = h(x) (14.2) 
where y is the two-element output of *h(z),* and the two-element vector 5 is defined as 

$$x={\left[\begin{array}{l}{r}\\ {\theta}\end{array}\right]}$$

Suppose that 51 (which is the range r) is a random variable with a mean of 1 and a standard deviation of *uT.* Suppose that 52 (which is the angle 8) is a random variable with a mean of 7r/2 and a standard deviation of **go.** In other words, the means of the components of 5 are given as F = 1 and s = **~/2.** In addition, we will assume that r and 8 are independent, and that their probability density functions are symmetric around their means (for example, Gaussian or uniform). 

## 14.1.1 The Mean Of A Nonlinear Transformation

An initial consideration of the above problem, along with Equation (14.1), would lead us to believe that y1 has a mean of 0, and y2 has a mean of 1. In addition, a linearization approach would lead us to the same conclusion. If we perform a firstorder linearization of Equation (14.2) and take the expected value of both sides, we obtain 

$$\begin{array}{r c l}{{\bar{h}}}&{{=}}&{{E[h(x)]}}\\ {{}}&{{\approx}}&{{E\left[h(\bar{x})+\left.\frac{\partial h}{\partial x}\right|_{\bar{x}}(x-\bar{x})\right]}}\\ {{}}&{{=}}&{{h(\bar{x})+\left.\frac{\partial h}{\partial x}\right|_{\bar{x}}E(x-\bar{x})}}\\ {{}}&{{=}}&{{h(\bar{x})}}\\ {{}}&{{=}}&{{\left[\begin{array}{l}{{0}}\\ {{1}}\end{array}\right]}}\end{array}$$
$$(14.4)$$

Our intuition, along with a first-order linearization analysis, both lead us to the same conclusion. However, let us pursue this problem with more rigor to check our previous analysis. We can write T and 6' as 

$$\begin{array}{r c l}{{r}}&{{=}}&{{\bar{r}+\tilde{r}}}\\ {{\theta}}&{{=}}&{{\bar{\theta}+\tilde{\theta}}}\end{array}$$
$$(14.5)$$

where ? and e' are simply the deviations of T and 6 from their means. A rigorous analysis of the mean of y1 can be performed as follows: 

$$\tilde{y}_{1}=E(r\cos\theta)$$ $$=E\left[(\tilde{r}+\tilde{r})\cos(\tilde{\theta}+\tilde{\theta})\right]$$ $$=E\left[(\tilde{r}+\tilde{r})(\cos\tilde{\theta}\cos\tilde{\theta}-\sin\tilde{\theta}\sin\tilde{\theta})\right]\tag{1}$$

Carrying out the multiplication, remembering that ? and e' are independent with symmetric pdfs, and taking the expected value, results in 

$$(14.6)$$
$$\begin{array}{r l}{={}}&{{}{\bar{r}}\cos{\bar{\theta}}}\\ {={}}&{{}0}\end{array}$$
$${\bar{y}}_{1}$$
$$(14.7)$$
$$(14.8)$$

Our intuition and our first-order approximation of 81 have been confirmed by rigorous analysis. Let us repeat the process for y2: 

$$\bar{y}_{2}=E(r\sin\theta)\tag{1}$$ $$=E\left[(\bar{r}+\bar{r})\sin(\bar{\theta}+\bar{\theta})\right]$$ $$=E\left[(\bar{r}+\bar{r})(\sin\bar{\theta}\cos\bar{\theta}+\cos\bar{\theta}\sin\bar{\theta})\right]$$

Carrying out the multiplication, remembering that 7 and 8 are independent with symmetric pdfs, and taking the expected value, results in 

$$\begin{array}{l}{{\bar{\tau}\sin\bar{\theta}E(\cos\tilde{\theta})}}\\ {{E(\cos\tilde{\theta})}}\end{array}$$
$$\begin{array}{r l}{{\bar{y}}_{2}}&{{}=1}\\ {\ }&{{}=1}\end{array}$$

We cannot go any further unless we assume some distribution for e, so let us assume that e' is uniformly distributed between *&Om.* In that case, we can compute 

$$(14.9)$$
$$\begin{array}{rcl}\tilde{y}_{2}&=&E(\cos\tilde{\theta})\\ &=&\frac{\sin\theta_{m}}{\theta_{m}}\end{array}\tag{14.10}$$

We expected to get 1 for our answer in confirmation of Equation **(14.4),** but instead we got some number that is less than 1. [Note that (sinOm)/Om < 1 for all 8, > 0, and lirq,,-,~(sinO,)/8, = **1.1** The analysis reveals a problem with our initial intuition and the first-order linearization that we performed earlier. The mean of yz will indeed be less than 1. This can be seen by looking at a plot of 300 randomly generated T and 6' values, where 7 is uniformly distributed between **+0.01,** and e' is uniformly distributed between **f0.35** radians. The small variance of F and the large 

![3_image_0.png](3_image_0.png)

![3_image_1.png](3_image_1.png)

Figure **14.** 
uniformly distributed between fO.O1 and 6 uniformly distributed between f0.35 radians. 

Linearized and nonlinear mean of 300 randomly generate, points with F 
variance of 8 result in an arc-shaped distribution of points as seen in Figure 14.1. 

This arc-shaped distribution results in g2 < 1. 

This is not a Kalman filtering example. But since the EKF uses first-order linearization to update the mean of the state, this example shows the kind of error that can creep into the EKF when it is applied to a nonlinear system. 

For a more general analysis of the mean of a nonlinear transformation, recall from Equation (1.89) that y = *h(z)* can be expanded in a Taylor series around 2 as follows: 

$$y=h(x)\tag{14.11}$$ $$=h(\bar{x})+D_{\bar{x}}h+\frac{1}{2!}D_{\bar{x}}^{2}h+\frac{1}{3!}D_{\bar{x}}^{3}h+\cdots$$  The proof is worth of a few examples.  
where 9 = x - 2. The mean of y can therefore be expanded as 

$$\tilde{y}=E\left[h(\tilde{x})+D_{\tilde{z}}h+\frac{1}{2!}D_{\tilde{z}}^{2}h+\frac{1}{3!}D_{\tilde{z}}^{3}h+\cdots\right]\tag{14.12}$$ $$=h(\tilde{x})+E\left[D_{\tilde{z}}h+\frac{1}{2!}D_{\tilde{z}}^{2}h+\frac{1}{3!}D_{\tilde{z}}^{3}h+\cdots\right]$$
$$(14.13)$$

By using Dzh from Equation (1.88) we can see that 

$$\begin{array}{r c l}{{E[D_{\tilde{x}}h]}}&{{=}}&{{E\left[\sum_{i=1}^{n}\tilde{x}_{i}\frac{\partial}{\partial x_{i}}h(x)\Big|_{x=\tilde{x}}\right]}}\\ {{}}&{{=}}&{{\sum_{i=1}^{n}E(\tilde{x}_{i})\frac{\partial}{\partial x_{i}}h(x)\Big|_{x=\tilde{x}}}}\\ {{}}&{{=}}&{{0}}\end{array}$$
=o (1 4.13) 
because *E(Za)* = 0. Likewise, we can see that 

$$\begin{array}{r c l}{{E[D_{\pm}^{3}h]}}&{{=}}&{{E\left[\left(\sum_{i=1}^{n}\tilde{x}_{i}\frac{\partial}{\partial x_{i}}\right)^{3}h(x)\Big|_{x=\tilde{x}}\right]}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{0}}\end{array}$$
$$(14.14)$$
$$(14.15)$$

This is because the sum in the above equation consists only of third-order moments 
[E(Z;), E(Z?Z2), etc.]. These expected values will always be zero as shown at the end of Section 2.2. Similarly all of the odd terms in Equation **(14.12)** will be zero, which leads to the simplification 

$${\bar{y}}=h({\bar{x}})+{\frac{1}{2!}}E[D_{\bar{z}}^{2}h]+{\frac{1}{4!}}E[D_{\bar{z}}^{4}h]+\cdots$$

This shows why the mean calculation in Equation **(14.4)** was incorrect; that calculation was only correct up to the first order. If we approximate g for our polar-tc-rectangular transformation using terms up to the second order from Equation **(14.15),** we obtain 

1  2! g M h(3) + -E[D3]  = [ ;]+y:[ 1 -11 0  (14.16) 
$${\bar{y}}\quad\land\quad$$
We therefore obtain 

$$\begin{array}{r c l}{{\bar{y}_{1}}}&{{\approx}}&{{0}}\\ {{}}&{{}}&{{}}\\ {{\bar{y}_{2}}}&{{\approx}}&{{1-\frac{\sigma_{\theta}^{2}}{2}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{1-\frac{E(\tilde{\theta}^{2})}{2}}}\end{array}$$
$$\text{(14)}$$. 
$$(14.17)$$
$$(14.18)$$

Note that we found the exact value of g2 in Equation **(14.9)** to be equal to E(cos 8). The approximate expression found in Equation **(14.17)** is the first two nonzero terms of the Taylor series expansion of E(cos 8). 

## 14.1.2 **The Covariance Of A Nonlinear Transformation**

Now we turn our attention to the covariance of a random variable that undergoes a nonlinear transformation. The covariance of y is given as 

$$P_{y}=E\left[(y-{\bar{y}})(y-{\bar{y}})^{T}\right]$$

p, = E [(Y - B)(Y - *g)']* (14.18) 
We can use Equations **(14.11)** and **(14.15)** to write (y - g) as 

$$y-\bar{y}=\left[h(\bar{x})+D_{\bar{x}}h+\frac{1}{2!}D_{\bar{x}}^{2}h+\cdots\right]-$$ $$\left[h(\bar{x})+\frac{1}{2!}E(D_{\bar{x}}^{2}h)+\frac{1}{4!}E(D_{\bar{x}}^{4}h)+\cdots\right]$$ $$=\left[D_{\bar{x}}h+\frac{1}{2!}D_{\bar{x}}^{2}h+\cdots\right]-\left[\frac{1}{2!}E(D_{\bar{x}}^{2}h)+\frac{1}{4!}E(D_{\bar{x}}^{4}h)+\cdots\right]\tag{14.19}$$

We substitute this expression into Equation **(14.18)** and use the same type of reasoning as in the previous section to see that all of the odd-powered terms in the expected value evaluate to zero (assuming that Z is zero-mean with a symmetric pdf). This results in 

$$P_{y}=E\left[D_{\underline{z}}h(D_{\underline{z}}h)^{T}\right]+\tag{14.20}$$ $$E\left[\frac{D_{\underline{z}}h(D_{\underline{z}}^{2}h)^{T}}{3!}+\frac{D_{\underline{z}}^{2}h(D_{\underline{z}}^{2}h)^{T}}{2!2!}+\frac{D_{\underline{z}}^{3}h(D_{\underline{z}}h)^{T}}{3!}\right]+$$ $$E\left(\frac{D_{\underline{z}}^{2}h}{2!}\right)E\left(\frac{D_{\underline{z}}^{2}h}{2!}\right)^{T}+\cdots$$

The first term on the right side of the above equation can be written as 

$$E\left[D_{\tilde{\bf z}}h(D_{\tilde{\bf z}}h)^{T}\right]=E\left[\left(\sum_{i=1}^{n}\tilde{x}_{i}\left.\frac{\partial h}{\partial x_{i}}\right|_{x=\tilde{x}}\right)\left(\cdots\right)^{T}\right]\tag{14.21}$$ $$=E\left[\sum_{i,j}\tilde{x}_{i}\left.\frac{\partial h}{\partial x_{i}}\right|_{x=\tilde{x}}\left.\frac{\partial h^{T}}{\partial x_{j}}\right|_{x=\tilde{x}}\tilde{x}_{j}\right]$$ $$=\sum_{i,j}H_{i}E(\tilde{x}_{i}\tilde{x}_{j})H_{j}^{T}$$ $$=\sum_{i,j}H_{i}P_{ij}H_{j}^{T}$$

where the partial derivative vector HZ and the expected value P,j are defined by the above equation. Recall from Equation **(1.16)** that an equation in this form can be written as 

$$E[D_{\underline{z}}h(D_{\underline{z}}h)^{T}]=\left.\frac{\partial h}{\partial x}\right|_{x=\underline{z}}P\left.\frac{\partial h^{T}}{\partial x}\right|_{x=\underline{z}}\tag{14.22}$$ $$=HPH^{T}$$

where the partial derivative matrix H and the covariance matrix P are defined by the above equation. H, in Equation **(14.21)** is the ith column of H, and *P,j* in Equ& 
tion **(14.21)** is the element in the ith row and jth column of P = *E(ZZT).* We can use this in Equation **(14.20)** to write the covariance of a nonlinear transformation y = *h(x)* as follows: 

$$P_{y}=HPH^{T}+E\left[\frac{D_{\bar{\pi}}h(D_{\bar{\pi}}^{3}h)^{T}}{3!}+\frac{D_{\bar{\pi}}^{2}h(D_{\bar{\pi}}^{2}h)^{T}}{2!2!}+\frac{D_{\bar{\pi}}^{3}h(D_{\bar{\pi}}h)^{T}}{3!}\right]+$$ $$E\left(\frac{D_{\bar{\pi}}^{2}h}{2!}\right)E\left(\frac{D_{\bar{\pi}}^{2}h}{2!}\right)^{T}+\cdots\tag{14.23}$$

This is the complete Taylor series expansion for the covariance of a nonlinear transformation. 

In the EKF, we use only the first term of this expansion to approximate the covariance of the estimation error. For example, if the measurement y = *h(x)* + TJ 
then we see from Equation **(10.98)** that the covariance of y is approximated as Pa, = *HPxHT* + R, where H is the partial derivative of h with respect to x, and R is the covariance of ?I. Likewise, if the state propagates as *xk+l* = f(xk) + Wk then we see from Equation **(10.100)** that the covariance of x is approximately updated as Pi = *FPz-_,FT* +&, where F is the partial derivative of *f(x)* with respect to x, and Q is the covariance of *Wk.* However, these covariance approximations can result in significant errors if the underlying functions h(x) and *f(x)* are highly nonlinear. 

For example, consider the nonlinear transformation introduced at the beginning of this section. A linear covariance approximation would indicate that P, M 
HPxHT, where H and Px are given as 

$P_{x}$ are given as  $$H=\left.\frac{\partial h}{\partial x}\right|_{x=\bar{x}}\tag{1}$$ $$=\left[\begin{array}{cc}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{array}\right]_{x=\bar{x}}$$ $$=\left[\begin{array}{cc}0&-1\\ 1&0\end{array}\right]$$ $$P_{x}=E\left(\left[\begin{array}{cc}r-\bar{r}\\ \theta-\bar{\theta}\end{array}\right]\left[\begin{array}{cc}\cdots\end{array}\right]^{T}\right)$$ $$=\left[\begin{array}{cc}\sigma_{r}^{2}&0\\ 0&\sigma_{\theta}^{2}\end{array}\right]$$
$$(14.24)$$
This gives P, as follows. 
$$P_{y}\approx HP_{x}H^{T}$$ $$=\left[\begin{array}{cc}0&-1\\ 1&0\end{array}\right]\left[\begin{array}{cc}\sigma_{r}^{2}&0\\ 0&\sigma_{\theta}^{2}\end{array}\right]\left[\begin{array}{cc}0&1\\ -1&0\end{array}\right]$$ $$=\left[\begin{array}{cc}\sigma_{\theta}^{2}&0\\ 0&\sigma_{r}^{2}\end{array}\right]$$
$$(14.25)$$
$$(14.26)$$
This is an approximation of P,. However, a more rigorous analysis of P, can be conducted using Equations **(14.1), (14.7),** and **(14.10):** 

$$P_{y}=E\left[(y-\bar{y})(y-\bar{y})^{T}\right]$$ $$=E\left[\left(\begin{array}{c}r\cos\theta\\ r\sin\theta-(\sin\theta_{m})/\theta_{m}\end{array}\right)\left(\begin{array}{c}\cdots\end{array}\right)^{T}\right]$$ $$=E\left[\begin{array}{cc}r^{2}\cos^{2}\theta&r^{2}\cos\theta\sin\theta-r\cos\theta(\sin\theta_{m})/\theta_{m}\\ r^{2}\cos\theta\sin\theta-r\cos\theta(\sin\theta_{m})/\theta_{m}&(r\sin\theta-(\sin\theta_{m})/\theta_{m})^{2}\end{array}\right]$$
1 
We again use our assumption that P and 8 are independent, T is uniformly distributed with a mean of 1 and a standard deviation of ur, and 8 = 7~/2 + 8, with 8 uniformly distributed between 44,. We can therefore compute 

$$\begin{array}{r c l}{{}}&{{\cdots}}\\ {{}}&{{E(r^{2})}}\\ {{}}&{{=}}\\ {{}}&{{E(\cos^{2}\tilde{\theta})}}\end{array}=\begin{array}{r c l}{{1+\sigma_{r}^{2}}}\\ {{}}&{{}}\\ {{}}&{{\frac{1-E(\cos2\tilde{\theta})}{2}}}\end{array}$$ $$\begin{array}{r c l}{{E(\cos2\tilde{\theta})}}&{{=}}&{{\frac{\sin2\theta_{m}}{2\theta_{m}}}}\\ {{}}&{{E(\sin\theta)}}&{{=}}\\ {{}}&{{}}\\ {{}}&{{=}}&{{\frac{\sin\theta_{m}}{\theta_{m}}}}\end{array}$$
$$(14.27)$$
$$P_{y}=\left[\begin{array}{cc}\frac{1}{2}(1+\sigma_{r}^{2})(1-\sin2\theta_{m}/2\theta_{m})&0\\ 0&\frac{1}{2}(1+\sigma_{r}^{2})(1+\sin2\theta_{m}/2\theta_{m})-\sin^{2}\theta_{m}/\theta_{m}^{2}\end{array}\right]\tag{14.28}$$  This matrix defines a two-dimensional ellipse, where $P_{y}(1,1)$ specifies the square 
of the y1 axis length, and Pv(2, 2) specifies the square of the y2 axis length. Figure 14.2 shows the linearized covariance defined by Equation (14.25), and the exact covariance defined by Equation (14.28). The linearized covariance is centered at the linearized mean, and the exact covariance is centered around at the exact mean. 

It can be seen that the linearized covariance is not a vew good approximation to the exact 

![7_image_0.png](7_image_0.png)

We can use these expressions in Equation (14.26) to compute 
Figure **14.2** Linearized and nonlinear mean and covariance of 300 randomly generated points with F uniformly distributed between fO.O1 and 6 uniformly distributed between h0.35 radians. 
This is not a Kalman filtering example. But since the EKF uses first-order linearization to update the covariance of the state, this example shows the kind of error that can creep into the EKF when it is applied to a nonlinear system. 

## 14.2 U N S C E N T E D Trans Fo R M At I 0 N S

The problem with nonlinear systems is that it is difficult to transform a probability density function through a general nonlinear function. In the previous section, we were able to obtain exact nonlinear transformations of the mean and covariance, but only for a simple two-dimensional transformation. The extended Kalman filter works on the principle that a linearized transformation of means and covariances is approximately equal to the true nonlinear transformation, but we saw in the previous section that the approximation could be unsatisfactory. 

An unscented transformation is based on two fundamental principles. First, it is easy to perform a nonlinear transformation on a single point (rather than an entire pdf). Second, it is not too hard to find a set of individual points in state space whose sample pdf approximates the true pdf of a state vector. 

Taking these two ideas together, suppose that we know the mean Z and covariance P of a vector x. We then find a set of deterministic vectors called sigma points whose ensemble mean and covariance are equal to Z and P. We next apply our known nonlinear function y = *h(x)* to each deterministic vector to obtain transformed vectors. The ensemble mean and covariance of the transformed vectors will give a good estimate of the true mean and covariance of y. This is the key to the unscented transformation. 

As an example, suppose that x is an n x 1 vector that is transformed by a nonlinear function y = *h(x).* Choose 2n sigma points *di)* as follows: 

$$x^{(i)}=\tilde{x}+\tilde{x}^{(i)}\ \ \ \ i=1,\cdots,2n$$ $$\tilde{x}^{(i)}=\left(\sqrt{nP}\right)_{i}^{T}\ \ \ \ i=1,\cdots,n$$ $$\tilde{x}^{(n+i)}=-\left(\sqrt{nP}\right)_{i}^{T}\ \ \ \ i=1,\cdots,n\tag{14.29}$$
$$(14.30)$$

where a is the matrix square root of nP such that = *nP,* and 
(a)i is the ith row of **@.l** In the next couple of subsections, we will see how the ensemble mean of the above sigma points can be used to approximate the mean and covariance of a nonlinearly transformed vector. 

## 14.2.1 Mean Approxi Mat **Ion**

Suppose that we have a vector x with a known mean Z and covariance P, a nonlinear function y = *h(z),* and we want to approximate the mean of y. We propose transforming each individual sigma point of Equation *(14.29)* using the nonlinear function *h(.),* and then taking the weighted sum of the transformed sigma points to approximate the mean of y. The transformed sigma points are computed as follows: 

$$y^{(i)}=h\left(x^{(i)}\right)\quad\ i=1,\cdots,2n$$

'MATLAB'S Cholesky factorization routine CHOL can be used to **find** a matrix square root. *See* Section 6.3.1, but note the slight difference between the matrix square root definition used in that section and here. 

The true mean of y is denoted as y. The approximated mean of y is denoted as Ju and is computed as follows:

$${\bar{y}}_{u}=\sum_{i=1}^{2n}W^{(i)}y^{(i)}$$
$$(14.31)$$

The weighting coefficients W(4) are defined as follows:

$$W^{(i)}=\frac{1}{2n}\;\;\;\;\;i=1,\cdots,2n$$
$$(14.32)$$

Equation (14.31) can therefore be written as

$${\bar{y}}_{u}={\frac{1}{2n}}\sum_{i=1}^{2n}y^{(i)}$$
$$(14.33)$$

Now let's compute the value of yn to see how well it matches the true mean of y.

To do this we first use Equation (1.89) to expand each y(4) in Equation (14.33) in a Taylor series around z. This results in

$$\bar{y}_{u}\quad=\quad$$  $$\quad=\quad$$
$$\frac{1}{2n}\sum_{i=1}^{2n}\left(h(\bar{x})+D_{\bar{z}^{(i)}}h+\frac{1}{2!}D_{\bar{z}^{(i)}}^{2}h+\cdots\right)$$ $$h(\bar{x})+\frac{1}{2n}\sum_{i=1}^{2n}\left(D_{\bar{z}^{(i)}}h+\frac{1}{2!}D_{\bar{z}^{(i)}}^{2}h+\cdots\right)\tag{14.34}$$

Now notice that for any integer k ≥ 0 we have

$$\sum_{j=1}^{2n}D_{\frac{2}{2}(i)}^{2k+1}h=\sum_{j=1}^{2n}\left[\left(\sum_{i=1}^{n}\tilde{x}_{i}^{(j)}\frac{\partial}{\partial x_{i}}\right)^{2k+1}h(x)\right|_{x=x}\right]\tag{14.35}$$ $$=\sum_{j=1}^{2n}\left[\sum_{i=1}^{n}\left(\tilde{x}_{i}^{(j)}\right)^{2k+1}\frac{\partial^{2k+1}}{\partial x_{i}^{2k+1}}h(x)\right|_{x=x}\right]$$ $$=\sum_{i=1}^{n}\left[\sum_{j=1}^{2n}\left(\tilde{x}_{i}^{(j)}\right)^{2k+1}\frac{\partial^{2k+1}}{\partial x_{i}^{2k+1}}h(x)\right|_{x=x}\right]$$ $$=0$$

because from Equation (14.29) z(0) = - 3(n+j) (j = 1, ···, n). Therefore, all of the odd terms in Equation (14.34) evaluate to zero and we have

$$\begin{array}{r l}{{\bar{y}}_{\mathrm{u}}}&{{}=}\\ {\ }&{}\\ {\ }&{}\\ {\ }&{}\end{array}$$
$$h({\bar{x}})+$$  $$h({\bar{x}})+$$  $$\frac{1}{2n}\sum_{i=1}^{2n}$$  ... 
$$+\frac{1}{2n}\sum_{i=1}^{2n}\left(\frac{1}{2!}D_{\hat{\pi}^{(i)}}^{2}h+\frac{1}{4!}D_{\hat{\pi}^{(i)}}^{4}h+\cdots\right)$$ $$+\frac{1}{2n}\sum_{i=1}^{2n}\frac{1}{2!}D_{\hat{\pi}^{(i)}}^{2}h+$$ $$\sum_{1}^{3}\left(\frac{1}{4!}D_{\hat{\pi}^{(i)}}^{4}h+\frac{1}{6!}D_{\hat{\pi}^{(i)}}^{6}h+\cdots\right)\tag{14.36}$$

Now look at the second term on the right side of the above equation:

2n d l (k) h(x)  ax, 2n 21 2n n Q2 l E (k) = (k) h(x) =  axidx; 4n == k=1 z,j=1  2n n  છેડ l (k) z (k h(x) I Ox;Ox; 4n = ゲ k=1  છેડ  1 x) =(k) (14.37) h(x) 2n dx; dx; == = 1
~(k+n)
where we have again used the fact from Equation (14.29) that x(k) (
(k = 1, ... , n). Substitute for x (k) and x(k) from Equation (14.29) in the above equation to obtain

a2h(x)  1 ( k )  OxiOx, 2n
$$\frac{1}{2n}\sum_{i,j=1}^{n}\sum_{k=1}^{n}\left(\sqrt{nP}\right)_{k_{1}}\left(\sqrt{nP}\right)_{k_{j}}\left.\frac{\partial^{2}h(x)}{\partial x_{i}\partial x_{j}}\right|_{x=x}$$ $$\frac{1}{2n}\sum_{i,j=1}^{n}nP_{ij}\left.\frac{\partial^{2}h(x)}{\partial x_{i}\partial x_{j}}\right|_{x=x}$$ $$\frac{1}{2}\sum_{i,j=1}^{n}P_{ij}\left.\frac{\partial^{2}h(x)}{\partial x_{i}\partial x_{j}}\right|_{x=x}\tag{14.38}$$
Equation (14.36) can therefore be written as

$$\bar{y}_{u}=h(\bar{x})+\frac{1}{2}\sum_{i,j=1}^{n}P_{1j}\left.\frac{\partial^{2}h}{\partial x_{i}\partial x_{j}}\right|_{x=\bar{x}}+$$ $$\frac{1}{2n}\sum_{i=1}^{2n}\left(\frac{1}{4!}D_{\bar{x}^{(i)}}^{4}h+\frac{1}{6!}D_{\bar{x}^{(i)}}^{6}h+\cdots\right)$$
$$(14.39)$$

Now recall that the true mean of y is given by Equation (14.15) as

$$\bar{y}=h(\bar{x})+\frac{1}{2!}E\left[D_{\bar{z}}^{2}h\right]+\frac{1}{4!}E\left[D_{\bar{z}}^{4}h\right]+\cdots\tag{14.40}$$
$$\begin{array}{r l}{{\frac{1}{2!}}E\left[D_{\tilde{z}}^{2}h\right]}&{{}=}\\ {\,}&{{}}\end{array}$$

Look at the second term on the right side of the above equation. It can be written as follows:

$$\begin{array}{c}{{{\frac{1}{2!}}E\left[\left(\sum_{i=1}^{n}\tilde{x}_{i}{\frac{\partial}{\partial x_{i}}}\right)^{2}h(x)\Big|_{x=\tilde{x}}\right]}}\\ {{{\frac{1}{2!}}E\left[\sum_{i,j=1}^{n}\tilde{x}_{i}\tilde{x}_{j}\left.{\frac{\partial^{2}h}{\partial x_{i}\partial x_{j}}}\right|_{x=\tilde{x}}\right]}}\end{array}$$
$$=\frac{1}{2!}\sum_{i,j=1}^{n}E(\tilde{x}_{i}\tilde{x}_{j})\left.\frac{\partial^{2}h}{\partial x_{i}\partial x_{j}}\right|_{x=\tilde{x}}\tag{14.41}$$ $$=\frac{1}{2!}\sum_{i,j=1}^{n}P_{ij}\left.\frac{\partial^{2}h}{\partial x_{i}\partial x_{j}}\right|_{x=\tilde{x}}$$

We therefore see that gj can be written from Equation **(14.40)** as 

$$\bar{y}=h(\bar{x})+\frac{1}{2}\sum_{i,j=1}^{n}P_{ij}\left.\frac{\partial^{2}h}{\partial x_{i}\partial x_{j}}\right|_{z=\bar{z}}+\tag{14.42}$$ $$\frac{1}{4!}E\left[D_{\bar{z}}^{4}h\right]+\frac{1}{6!}E\left[D_{\bar{z}}^{6}h\right]+\cdots$$

Comparing this with Equation **(14.39)** we see that B, (the approximated mean of y) matches the true mean of y correctly up to the third order, whereas linearization only matches the true mean of y up to the first order (see Section **14.1.1).** If we compute B, using Equations **(14.29), (14.30),** and **(14.33),** then the value of **fj,** will match the true mean of y up to the third order. The biggest difficulty with this algorithm is the matrix square root that is required in Equation **(14.29).** But the unscented transformation has the computational advantage that the linearization matrix H does not need to be computed. Of course, the greatest advantage of the unscented transformation (relative to linearization) is the increased accuracy of the mean transformation. 

## 14.2.2 Covariance Approximation

Now suppose that we want to approximate the covariance of the nonlinearly transformed vector x. That is, we have an n-element vector x with known mean 5 and covariance P, and we have a known nonlinear function y = *h(x).* We want to estimate the covariance of y. We will denote the estimate as P,, and we propose using the following equation: 

$$P_{u}=\sum_{i=1}^{2n}W^{(i)}(y^{(i)}-y_{u})(y^{(i)}-y_{u})^{T}\tag{14.43}$$ $$=\frac{1}{2n}\sum_{i=1}^{2n}(y^{(i)}-y_{u})(y^{(i)}-y_{u})^{T}$$

where the y(i) vectors are the transformed sigma points that Equation **(14.30),** and the weighting coefficients are the same as those given in Equation **(14.32).** Expanding this approximation using Equations **(1.89)** and **(14.36)** gives the following: 
were computed in 

$$P_{u}=\frac{1}{2n}\sum_{i=1}^{2n}\left[h(x^{(i)})-y_{u}\right]\left[h(x^{(i)})-y_{u}\right]^{T}\tag{14.44}$$
$$\frac{1}{2n}\sum_{i=1}^{2n}\left[h(\vec{x})+D_{\vec{x}^{(i)}}h+\frac{1}{2}D_{\vec{x}^{(i)}}^{2}h+\frac{1}{3!}D_{\vec{x}^{(i)}}^{3}h+\cdots\right.$$ $$\left.-h(\vec{x})-\frac{1}{2n}\sum_{j=1}^{2n}\left(\frac{1}{2}D_{\vec{x}^{(j)}}^{2}h+\frac{1}{4!}D_{\vec{x}^{(j)}}^{4}h+\cdots\right)\right]\left[\cdots\right]^{T}\tag{14.45}$$
$$\mathbf{\Sigma}=$$

Multiplying this equation out gives

$$P_{u}\quad=$$
2n T l (Dg(s) h) (. Dz(i) h (D}(i) h) T + + 2 2n T l l l (D2(s) h) ( . . . ) T Do (s) h Dz(i) h 2n 2 j  0 0 H  1 Dis (s) h D2(4) h Dig (s) h + 4n2 4n J T (14.46)
Some of the terms in the above equation are zero as noted above because £(4)
- 2(+n) for i = 1, ... , n. So the covariance approximation can be written as

$$P_{u}={\frac{1}{2n}}\sum_{i=1}^{2n}\left(D_{{\bar{x}}^{(i)}}h\right)\left(\cdots\right)^{T}+\mathrm{HOT}$$
$$(14.47)$$

where HOT means higher-order terms (i.e., terms to the fourth power and higher).

Expanding this equation for Pu while neglecting the higher order terms gives

$$P_{u}=\frac{1}{2n}\sum_{i=1}^{2n}\sum_{j,k=1}^{n}\left(\tilde{x}_{j}^{(i)}\frac{\partial h(\tilde{x})}{\partial x_{j}}\right)\left(\tilde{x}_{k}^{(i)}\frac{\partial h(\tilde{x})}{\partial x_{k}}\right)^{T}\tag{14.48}$$

-x (+n) for i = 1, ··· , n. Therefore, the Now recall that x'() = - x(++n) and x)
covariance approximation becomes

$$\begin{array}{r c l}{{P_{u}}}&{{=}}&{{\frac{1}{n}\sum_{i=1}^{n}\sum_{j,k=1}^{n}\left(\tilde{x}_{j}^{(i)}\frac{\partial h(\tilde{x})}{\partial x_{j}}\right)\left(\tilde{x}_{k}^{(i)}\frac{\partial h(\tilde{x})}{\partial x_{k}}\right)^{T}}}\\ {{}}&{{=}}&{{\sum_{j,k=1}^{n}P_{j k}\frac{\partial h(\tilde{x})}{\partial x_{j}}\left(\frac{\partial h(\tilde{x})}{\partial x_{k}}\right)^{T}}}\\ {{}}&{{=}}&{{H P H^{T}}}\end{array}$$
$$(14.49)$$

where the last equality comes from Equation (14.22). Comparing this equation for Pa with the true covariance of y from Equation (14.23), we see that Equation (14.43)
approximates the true covariance of y up to the third order (i.e., only terms to the fourth and higher powers are incorrect). This is the same approximation order as the linearization method, as seen on page 439. However, we would intuitively expect the magnitude of the error of the unscented approximation in Equation (14.43) to be smaller than the linear approximation HPHT, because the unscented approximation at least contains correctly signed terms to the fourth power and higher, whereas the linear approximation does not contain any terms other than HPHT. 

The unscented transformation can be summarized as follows. 

## The Unscented Transformation

1. We begin with an n-element vector z with known mean 2 and covariance P. 

Given a known nonlinear transformation y = *h(z),* we want to estimate the mean and covariance of y, denoted as g, and P,. 

2. Form 2n sigma point vectors *di)* as follows: 

$$x^{(i)}=\bar{x}+\bar{x}^{(i)}\quad\quad i=1,\cdots,2n$$ $$\bar{x}^{(i)}=\left(\sqrt{nP}\right)_{i}^{T}\quad\quad i=1,\cdots,n$$ $$\bar{x}^{(n+i)}=-\left(\sqrt{nP}\right)_{i}^{T}\quad\quad i=1,\cdots,n\tag{14.50}$$
$$(14.51)$$

where a is the matrix square root of nP such that (a)Ta 
= nP, 
and (a), 
is the ith row of a. 

3. Transform the sigma points as follows: 

$$y^{(i)}=h(x^{(i)})\;\;\;\;\;i=1,\cdots,2n$$

4. Approximate the mean and covariance of y as follows: 

$$\begin{array}{r c l}{{\tilde{y}_{u}}}&{{=}}&{{\frac{1}{2n}\sum_{i=1}^{2n}y^{(i)}}}\\ {{}}&{{}}&{{}}\\ {{P_{u}}}&{{=}}&{{\frac{1}{2n}\sum_{i=1}^{2n}\left(y^{(i)}-y_{u}\right)\left(y^{(i)}-y_{u}\right)^{T}}}\end{array}$$
$$(14.52)$$

## Example 14.1

$$\begin{array}{r c l}{{x^{(1)}}}&{{=}}&{{\bar{x}+\left({\sqrt{n P}}\right)_{1}^{T}}}\\ {{}}&{{=}}&{{\left[\begin{array}{c}{{1+\sigma_{r}{\sqrt{2}}}\\ {{\pi/2}}\end{array}\right]}}\end{array}$$

To illustrate the unscented transformation, consider the nonlinear transformation shown in Equation (14.1). Since there are two independent variables 
(T and *O),* we have n = 2. The covariance of P is given as P = diag(o:, *o,").* 
Equation (14.32) shows that *W(i)* = 1/4 for i = 1,2,3,4. Equation (14.29) 
shows that the sigma points are determined as 

$$x^{(2)}=\bar{x}+\left(\sqrt{nP}\right)_{2}^{T}$$ $$=\left[\begin{array}{c}1\\ \pi/2+\sigma_{\theta}\sqrt{2}\end{array}\right]$$ $$x^{(3)}=\bar{x}-\left(\sqrt{nP}\right)_{1}^{T}$$ $$=\left[\begin{array}{c}1-\sigma_{r}\sqrt{2}\\ \pi/2\end{array}\right]$$ $$x^{(4)}=\bar{x}-\left(\sqrt{nP}\right)_{2}^{T}$$ $$=\left[\begin{array}{c}1\\ \pi/2-\sigma_{\theta}\sqrt{2}\end{array}\right]$$  but we found in our picture (4) and (4).  
$$(14.53)$$

Computing the nonlinearly transformed sigma points y(4) = h(x(3) gives

$$\begin{array}{r l}{y^{(1)}}&{{}=}\\ {}&{}\\ {y^{(2)}}&{{}=}\\ {}&{}\\ {y^{(3)}}&{{}=}\\ {}&{}\\ {y^{(4)}}&{{}=}\\ {}&{}\end{array}$$
cosx(1) sin x H x(2) cos x (2) (2) 2) sin x x (3) x (3) cos x 3) sin x 3) I (4) cos x 4) sin x
$\begin{array}{c}\cdot\\ 1+\sigma_{r}\sqrt{2}\end{array}$  $\begin{array}{c}\cdot\\ \cos(\pi/2+\sigma_{\theta}\sqrt{2})\\ \sin(\pi/2+\sigma_{\theta}\sqrt{2})\end{array}$  $\begin{array}{c}\cdot\\ 0\\ 1-\sigma_{r}\sqrt{2}\end{array}$  $\begin{array}{c}\cdot\\ \cos(\pi/2-\sigma_{\theta}\sqrt{2})\\ \sin(\pi/2-\sigma_{\theta}\sqrt{2})\end{array}$  (14.54)
Now we can compute the unscented approximation of the mean and covariance of y = h(x) as

$$\bar{y}_{u}=\sum_{i=1}^{4}W^{(i)}y^{(i)}$$ $$P_{u}=\sum_{i=1}^{4}W^{(i)}\left(y^{(i)}-y_{u}\right)\left(y^{(i)}-y_{u}\right)^{T}\tag{14.55}$$

The results of these transformations are shown in Figure 14.3. This shows the improved accuracy of mean and covariance estimation when unscented transformations are used instead of linear approximations.

The true mean and the approximate unscented mean are so close that they are plotted on top of each other. The true mean and the approximate unscented mean are both equal to (0,0.9797) to four significant digits.

vvv

## 14.3 Unscented Kalman Filtering

The unscented transformation developed in the previous section can be generalized to give the unscented Kalman filter. After all, the Kalman filter algorithm attempts

![15_image_0.png](15_image_0.png)

Figure **14.3** A comparison of the exact, linearized, and unscented mean and covariance of 300 randomly generated points with f uniformly distributed between **fO.O1** and 6 uniformly distributed between **f0.35** radians. 

Results of Example 14.1. 
to propagate the mean and covariance of a system using a time-update and a measurement update. If the system is linear, then the mean and covariance can be exactly updated with the Kalman filter (Chapter **5).** If the system is nonlinear, then the mean and covariance can be approximately updated with the extended Kalman filter (Section **13.2).** However, the EKF is based on linearization, and the previous section showed that unscented transformations are more accurate than linearization for propagating means and covariances. Therefore, we simply replace the EKF equations with unscented transformations to obtain the UKF algorithm. 

The UKF algorithm can be summarized as follows. 

## The Unscented Kalman Filter

1. We have an n-state discretetime nonlinear system given by 

$$(14.56)$$

2. The UKF is initialized as follows. 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{f(x_{k},u_{k},t_{k})+w_{k}}}\\ {{y_{k}}}&{{=}}&{{h(x_{k},t_{k})+v_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q_{k})}}\\ {{v_{k}}}&{{\sim}}&{{(0,R_{k})}}\end{array}$$
$$\hat{x}_{0}^{+}=E(x_{0})$$ $$P_{0}^{+}=E\left[(x_{0}-\hat{x}_{0}^{+})(x_{0}-\hat{x}_{0}^{+})^{T}\right]\tag{14.57}$$

3. The following time update equations are used to propagate the state estimate and covariance from one measurement time to the next. 

(a) To propagate from time step (k - 1) to k, first choose sigma points zfi, as specified in Equation **(14.29),** with appropriate changes since the current best guess for the mean and covariance of Zk are *2$-,* and 
+ *pk-* 1: 

$$\begin{array}{r c l}{{\hat{x}_{k-1}^{(i)}}}&{{=}}&{{\hat{x}_{k-1}^{+}+\tilde{x}^{(i)}\quad i=1,\cdots,2n}}\\ {{}}&{{}}&{{}}\\ {{\tilde{x}^{(i)}}}&{{=}}&{{\left(\sqrt{n P_{k-1}^{+}}\right)_{i}^{T}\quad i=1,\cdots,n}}\\ {{}}&{{}}&{{}}\\ {{\tilde{x}^{(n+i)}}}&{{=}}&{{-\left(\sqrt{n P_{k-1}^{+}}\right)_{i}^{T}\quad i=1,\cdots,n}}\end{array}$$
$$(14.58)$$

(b) Use the known nonlinear system equation *f(.)* to transform the sigma points into **2t)** vectors as shown in Equation **(14.30),** with appropriate changes since our nonlinear transformation is f(.) rather than *h(.):* 

$${\hat{x}}_{k}^{(i)}=f({\hat{x}}_{k-1}^{(i)},u_{k},t_{k})$$
$${\hat{x}}_{k}^{-}={\frac{1}{2n}}\sum_{i=1}^{2n}{\hat{x}}_{k}^{(i)}$$
$$(14.59)$$

(c) Combine the *2:)* vectors to obtain the a *priori* state estimate at time k. 

This is based on Equation **(14.33):** 

$$(14.60)$$
$$(14.61)$$
$$P_{k}^{-}=\frac{1}{2n}\sum_{i=1}^{2n}\left(\hat{x}_{k}^{(i)}-\hat{x}_{k}^{-}\right)\left(\hat{x}_{k}^{(i)}-\hat{x}_{k}^{-}\right)^{T}+Q_{k-1}$$

(d) Estimate the a *priori* error covariance as shown in Equation **(14.43).** 
However, we should add **Qk-1** to the end of the equation to take the process noise into account: 
4. Now that the time update equations are done, we implement the measurementupdate equations. 

(a) Choose sigma points *xt)* as specified in Equation **(14.29),** with appropriate changes since the current best guess for the mean and covariance of Xk are 2; and *P;:* 

$$\hat{\vec{x}}_{k}^{(i)}=\hat{\vec{x}}_{k}^{-}+\tilde{\vec{x}}^{(i)}\qquad i=1,\cdots,2n$$ $$\tilde{\vec{x}}^{(i)}=\left(\sqrt{nP_{k}^{-}}\right)_{i}^{T}\qquad i=1,\cdots,n$$ $$\tilde{\vec{x}}^{(n+i)}=-\left(\sqrt{nP_{k}^{-}}\right)_{i}^{T}\qquad i=1,\cdots,n\tag{14.62}$$  be omitted if desired. That is just a left-hand of $\vec{x}^{(i)}$
This step can be omitted if desired. That is, instead of generating new sigma points we can reuse the sigma points that were obtained from the time update. This will save computational effort if we are willing to sacrifice performance. 

(b) Use the known nonlinear measurement equation *h(.)* to transform the sigma points into **6:'** vectors (predicted measurements) as shown in Equation **(14.30):** 

$${\hat{y}}_{k}^{(i)}=h({\hat{x}}_{k}^{(i)},t_{k})$$
$${\hat{y}}_{k}={\frac{1}{2n}}\sum_{i=1}^{2n}{\hat{y}}_{k}^{(i)}$$

(c) Combine the of) vectors to obtain the predicted measurement at time k, This is based on Equation **(14.33):** 

$$(14.63)$$
$$(14.64)$$
$$(14.65)$$
$$P_{y}={\frac{1}{2n}}\sum_{i=1}^{2n}\left({\hat{y}}_{k}^{(i)}-{\hat{y}}_{k}\right)\left({\hat{y}}_{k}^{(i)}-{\hat{y}}_{k}\right)^{T}+R_{k}$$

(d) Estimate the covariance of the predicted measurement as shown in Equation **(14.43).** However, we should add Rk to the end of the equation to take the measurement noise into account: 

$$P_{xy}=\frac{1}{2n}\sum_{i=1}^{2n}\left(\hat{x}_{k}^{(i)}-\hat{x}_{k}^{-}\right)\left(\hat{y}_{k}^{(i)}-\hat{y}_{k}\right)^{T}\tag{14.66}$$

(e) Estimate the cross covariance between 2; and gk based on Equation **(14.43):** 

$$K_{k}=P_{xy}P_{y}^{-1}$$ $$\hat{x}_{k}^{+}=\hat{x}_{k}^{-}+K_{k}(y_{k}-\hat{y}_{k})$$ $$P_{k}^{+}=P_{k}^{-}-K_{k}P_{y}K_{k}^{T}\tag{14.67}$$

(f) The measurement update of the state estimate can be performed using the normal Kalman filter equations as shown in Equation **(10.100):** 
The algorithm above assumes that the process and measurement equations are linear with respect to the noise, as shown in Equation **(14.56).** In general, the process and measurement equations may have noise that enters the process and measurement equations nonlinearly. That is, 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{f(x_{k},u_{k},w_{k},t_{k})}}\\ {{y_{k}}}&{{=}}&{{h(x_{k},v_{k},t_{k})}}\end{array}$$
$$x_{k}^{(a)}={\left[\begin{array}{l}{x_{k}}\\ {w_{k}}\\ {v_{k}}\end{array}\right]}$$

In this case, the UKF algorithm presented above is not rigorous because it treats the noise as additive, as seen in Equations **(14.61)** and **(14.65).** To handle this situation, we can augment the noise onto the state vector as shown in [Ju104, WanOl]: 

$$(14.68)$$
$$(14.69)$$

Then we can use the UKF to estimate the augmented state zt'. The UKF is initialized as 

$$\hat{x}_{0}^{a+}=\left[\begin{array}{c}E(x_{0})\\ 0\\ 0\end{array}\right]$$ $$P_{0}^{a+}=\left[\begin{array}{ccc}E\left[(x_{0}-\hat{x}_{0})(x_{0}-\hat{x}_{0})^{T}\right]&0&0\\ 0&Q_{0}&0\\ 0&0&R_{0}\end{array}\right]\tag{14.70}$$

Then we use the UKF algorithm presented above, except that we are estimating the augmented mean and covariance, so we remove Qk-1 *and* Rk from Equations (14.61) 
and (14.65). 

## Example **14.2**

Suppose we are trying to estimate the altitude *21,* velocity *22,* and constant ballistic coefficient 23 of a body as it falls toward earth. A range measuring device is located at an altitude a and the horizontal range between the measuring device and the body is M. This system is the same as the one in Example 13.3. The equations for this system are 

$$\dot{x}_{1}=x_{2}+w_{1}$$ $$\dot{x}_{2}=\rho_{0}\exp(-x_{1}/k)x_{2}^{2}x_{3}/2-g+w_{2}$$ $$\dot{x}_{3}=w_{3}$$ $$y(t_{k})=\sqrt{M^{2}+(x_{1}(t_{k})-a)^{2}}+v_{k}\tag{14.71}$$

As usual, wi is the noise that affects the ith process equation, and v is the 
measurement noise. po is the air density at sea level, k is a constant that 
defines the relationship between air density and altitude, and g is the acceleration due to gravity. We will use the continuous-time system equations to simulate the system, and suppose that we obtain range measurements every 0.5 seconds. The constants that we will use are given as 
 -  $2\text{lb-sec}^{2}/\text{ft}^{4}$  : $32.2\text{ft}/\text{sec}^{2}$  : $20,000\text{ft}$  : $10,000\text{ft}^{2}$  : $0\ \ \ \ i=1,2,3$  : $100,000\text{ft}$  : $100,000\text{ft}$
$$\begin{array}{r c l}{{\rho_{0}}}&{{=}}&{{}}\\ {{}}&{{g}}&{{=}}\\ {{}}&{{k}}&{{=}}\\ {{}}&{{E[v_{k}^{2}]}}&{{=}}\\ {{}}&{{E[w_{i}^{2}(t)]}}&{{=}}\\ {{}}&{{M}}&{{=}}\\ {{}}&{{}}&{{a}}&{{=}}\end{array}$$
E[v;] = 10,000 **ft2** 
E[wf(t)] = *0 i* = 1,2,3 
M = 100,OOOft 
a = 100,000ft (14.72) 
The initial conditions of the system and the estimator are given as 

$$\begin{array}{r c l}{{x_{0}}}&{{=}}&{{\left[\begin{array}{c c c c}{{300,000}}&{{-20,000}}&{{0.001}}\end{array}\right]^{T}}}\\ {{\hat{x}_{0}^{+}}}&{{=}}&{{x_{0}}}\\ {{{\cal P}_{0}^{+}}}&{{=}}&{{\left[\begin{array}{c c c c}{{1,000,000}}&{{0}}&{{0}}\\ {{0}}&{{4,000,000}}&{{0}}\\ {{0}}&{{0}}&{{10}}\end{array}\right]}}\end{array}$$

$$(14.72)$$
$$(14.73)$$

We use rectangular integration with a step size of 1 msec to simulate the system, the extended Kalman filter, and the unscented Kalman filter for 30 seconds. Figure 14.4 shows the altitude and velocity of the falling body. 

For the first few seconds, the velocity is constant. But then the air density increases and drag slows the falling object. Toward the end of the simulation, the object has reached a constant terminal velocity as the acceleration due to gravity is canceled by drag. 

Figure 14.5 shows typical EKF and UKF estimation-error magnitudes for this system. It is seen that the altitude and velocity estimates both spike around 10 seconds, at which point the altitude of the measuring device and the falling body are about the same, so the measurement gives less information about the body's altitude and velocity. It is seen from the figure that the UKF 
consistently gives estimates that are one or two orders of magnitude better than the EKF. 

![19_image_0.png](19_image_0.png)

Figure **14.4** Altitude and velocity of a falling body for Example **14.2.** 
vvv 

## 14.4 Other Unscented Transformations

The unscented transformation discussed in the previous section is not the only one that exists. In this section, we discuss several other possible transformations. These other transformations can be used if we have some information about the statistics of the noise, or if we are interested in computational savings. 

## 14.4.1 General Unscented Transformations

We have seen that an accurate mean and covariance approximation for a nonlinear transformation y = *h(z)* can be obtained by choosing 2n sigma points (where n is the dimension of z) as given in Equation (14.29), and approximating the mean and 

- Kalman filter 

![20_image_0.png](20_image_0.png)

Figure **14.5** 
altitude, velocity, and ballistic coefficient of a falling body for Example **14.2.** 
Kalman filter and unscented filter estimation-error magnitudes of the 
covariance as given in Equations (14.33) and **(14.43).** However, it can be shown that the same order of mean and covariance estimation accuracy can be obtained by choosing **(2n** + 1) sigma points di) as follows: 

n w(0) = - 
$$W^{(0)}=\frac{\kappa}{n+\kappa}$$ $$W^{(i)}=\frac{1}{2(n+\kappa)}\quad\ i=1,\cdots,2n\tag{14.75}$$
$$x^{(0)}=\tilde{x}$$ $$x^{(i)}=\tilde{x}+\tilde{x}^{(i)}\ \ \ \ i=1,\cdots,2n$$ $$\tilde{x}^{(i)}=\left(\sqrt{(n+\kappa)P}\right)_{i}^{T}\ \ \ \ \ i=1,\cdots,n$$ $$\tilde{x}^{(n+i)}=-\left(\sqrt{(n+\kappa)P}\right)_{i}^{T}\ \ \ \ \ i=1,\cdots,n\tag{14.74}$$  which is a $\alpha$-function.  
The **(271** + 1) weighting coefficients are given as The unscented mean and covariance approximations are computed as 

$$\begin{array}{l}h\left(x^{(i)}\right)\\ \sum_{i=0}^{2n}W^{(i)}y^{(i)}\\ \sum_{i=0}^{2n}W^{(i)}\left(y^{(i)}-y_{u}\right)\left(y^{(i)}-y_{u}\right)^{T}\end{array}\tag{14.76}$$
$$\begin{array}{r l}{y^{(i)}}&{{}=}\\ {}&{}&{{}}\\ {{}}&{{}}&{{}}\\ {{\bar{y}}_{u}}&{{}=}\\ {}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{P}_{u}}&{{}=}\end{array}$$

It can be seen that if n = 0 then these definitions reduce to the quantities given in Section **14.2.** Any n value can be used [as long **as (n** + n) \# 01 and will give a mean and covariance estimation accuracy with the same order of accuracy as derived in Section 14.2. However, IE can be used to reduce the higher-order errors of the mean and covariance approximation. For example, if z is Gaussian then IC = 3 - n will minimize some of the errors in the fourth-order terms in the mean and covariance approximation [ Ju100, Ju1041. 

## 14.4.2 The Simplex Unscented Transformation

If computational effort is a primary consideration, then a minimum number of sigma points can be chosen to give the order of estimation accuracy derived in the previous section. It can be shown [JulO2a, Ju1041 that if z has n elements then the minimum number of sigma points that gives the order of estimation accuracy of the previous section is equal to (n + 1). These sigma points are called simplex sigma points. The following algorithm results in (n + 2) sigma points, but the number can be reduced to (n + 1) by choosing one of the weights to be zero. The simplex sigm&point algorithm can be summarized as follows. 

## The Simplex Sigma-Point Algorithm

1. Choose the weight *W(O)* E [0, 1). The choice of *W(O)* affects only the fourth and higher order moments of the set of sigma points [JulOO, Jul02al. 

2. Choose the rest of the weights as follows: 

$$W^{(i)}=\left\{\begin{array}{ll}2^{-n}(1-W^{(0)})&i=1,2\\ 2^{i-2}W^{(1)}&i=3,\cdots,n+1\end{array}\right.\tag{14.77}$$
$$\begin{array}{r c l}{{\sigma_{0}^{(1)}}}&{{=}}&{{0}}\\ {{\sigma_{1}^{(1)}}}&{{=}}&{{\frac{-1}{\sqrt{2W^{(1)}}}}}\\ {{\sigma_{2}^{(1)}}}&{{=}}&{{\frac{1}{\sqrt{2W^{(1)}}}}}\end{array}$$

3. Initialize the following one-element vectors: 

$$(14.78)\,$$. 
4. Recursively expand the o vectors by performing the following steps for j = 
2,. , n: 

$$\sigma_{i}^{(j)}=\left\{\begin{array}{cc}\left[\begin{array}{cc}\sigma_{0}^{(j-1)}\\ 0\end{array}\right]&i=0\\ \\ \left[\begin{array}{cc}\sigma_{i}^{(j-1)}\\ \frac{1}{\sqrt{2W(j+1)}}\end{array}\right]&i=1,\cdots,j\\ \\ \left[\begin{array}{cc}0_{j-1}\\ \frac{1}{\sqrt{2W(j+1)}}\end{array}\right]&i=j+1\end{array}\right.\tag{14.79}$$   column vector containing $i$ zeros
where Oj is the column vector containing j zeros. 

5. After the above recursion is complete we have the n-element vectors ~7:~) (i = 
0,. , n + 1). We modify the unscented transformation of Equation (14.29) 
and obtain the sigma points for the unscented transformation as follows: 

$$x^{(i)}=\bar{x}+\sqrt{P}\sigma_{i}^{(n)}\quad\ (i=0,\cdots,n+1)\tag{14.80}$$

We actually have (n + 2) sigma points instead of the (n + 1) sigma points as we claimed, but if we choose *W(O)* = 0 then the *do)* sigma point can be ignored in the ensuing unscented transformation. The unscented Kalman filter algorithm in Section 14.3 is then modified in the obvious way based on this minimal set of sigma points. 

The problem with the simplex UKF is that the ratio of *W(n)* to W(l) is equal to 2n-2 , where n is the dimension of the state vector x. As the dimension of the state increases, this ratio increases and can quickly cause numerical problems. The only reason for using the simplex UKF is the computational savings, and computational savings is an issue only for problems of high dimension (in general). This makes the simplex UKF of limited utility and leads to the spherical unscented transformation in the following section. 

## 14.4.3 The Spherical Unscented Transformation

The unscented transformation discussed in Section 14.2 is numerically stable. However, it requires 2n sigma points and may be too computationally expensive for some applications. The simplex unscented transformation discussed in Section 14.4.2 is the cheapest computational unscented transformation but loses numerical stability for problems with a moderately large number of dimensions. The spherical unscented transformation was developed with the goal of rearranging the sigma points of the simplex algorithm in order to obtain better numerical stability [Ju103, Ju1041. The spherical sigma points are chosen with the following algorithm. 

## The Spherical Sigma-Point Algorithm

1. Choose the weight *W(O)* E [0,1). The choice of *W(O)* affects only the fourthand higher-order moments of the set of sigma points [JulOO, Jul02al. 

2. Choose the rest of the weights as follows: 

$$W^{(i)}=\frac{1-W^{(0)}}{n+1}\quad i=1,\cdots,n+1\tag{14.81}$$
$$\begin{array}{r c l}{{\sigma_{0}^{(1)}}}&{{=}}&{{0}}\\ {{\sigma_{1}^{(1)}}}&{{=}}&{{\frac{-1}{\sqrt{2W^{(1)}}}}}\\ {{\sigma_{2}^{(1)}}}&{{=}}&{{\frac{1}{\sqrt{2W^{(1)}}}}}\end{array}$$

Note that (in contrast to the simplex unscented transformation) all of the weights are identical except for *W(O).* 
3. Initialize the following oneelement vectors: 

$$(14.82)$$

4. Recursively expand the Q vectors by performing the following steps for j = 

$2,\cdots,n$:  $$\sigma_{i}^{(j)}=\left\{\begin{array}{cc}\left[\begin{array}{c}\sigma_{0}^{(j-1)}\\ 0\end{array}\right]&i=0\\ \\ \left[\begin{array}{c}\sigma_{i-1}^{(j-1)}\\ \sqrt{j(j+1)W^{(1)}}\end{array}\right]&i=1,\cdots,j\\ \\ \left[\begin{array}{c}0_{j-1}\\ \sqrt{j(j+1)W^{(1)}}\end{array}\right]&i=j+1\end{array}\right.\tag{14.83}$$  where $0_{j}$ is the column vector containing $j$ zeros.  
5. After the above recursion is complete, we have the n-element vectors **Q!"'** 
(i = 0, . . , n + 1). As with the simplex sigma points, we actually have (n + 2) 
sigma points above, but if we choose *W(O)* = 0 then the do) sigma point can be ignored in the ensuing unscented transformation. We modify the unscented transformation of Equation **(14.29)** and obtain the sigma points for the unscented transformation as follows: 

$$(14.84)$$
$$x^{(i)}=\bar{x}+\sqrt{P}\sigma_{i}^{(n)}\;\;\;\;\;(i=0,\cdots,n+1)$$
$${\frac{n}{\sqrt{n(n+1)W^{(1)}}}}\left/{\frac{1}{\sqrt{n(n+1)W^{(1)}}}}=n\right.$$

The unscented Kalman filter algorithm in Section **14.3** is then modified in the obvious way based on this set of sigma points. 

The ratio of the largest element of **Q:")** to the smallest element is 

$$(14.85)$$

so numerical problems should not be an issue for the spherical unscented transformation. 

## Example 14.3

Here we consider the falling-body system described in Example 14.2. The initial conditions of the system and the estimator are given as 

$$\begin{array}{r c l}{{x_{0}}}&{{=}}&{{\left[\begin{array}{c c c}{{300,000}}&{{-20,000}}&{{1/1000}}\end{array}\right]^{T}}}\\ {{\hat{x}_{0}^{+}}}&{{=}}&{{\left[\begin{array}{c c c}{{303,000}}&{{-20,200}}&{{1/1010}}\end{array}\right]^{T}}}\\ {{P_{0}^{+}}}&{{=}}&{{\left[\begin{array}{c c c}{{30,000}}&{{0}}&{{0}}\\ {{0}}&{{2,000}}&{{0}}\\ {{0}}&{{0}}&{{1/10,000}}\end{array}\right]}}\end{array}$$
$$(14.86)$$

We ran 100 Monte Carlo simulations, each with a 60 s simulation time. The average RMS estimation errors of the EKF, standard UKF (six sigma points), 
simplex UKF (four sigma points since we chose *W(O)* = 0), and spherical UKF 
(four sigma points since we chose *W(O)* = 0) are given in Table **14.1.** The simplex UKF performs best for altitude estimation, with the standard UKF 
not far behind. The standard UKF performs best for velocity estimation, and the spherical UKF performs best for ballistic coefficient estimation. The EKF is generally the worst performing of the four state estimators. 

Table 14.1 standard unscented Kalman filter with 2n sigma points, and the spherical unscented Kalman filter with (n + 1) sigma points. The standard UKF generally performs best. 

The spherical UKF performance and computational effort lie between those of the EKF and the standard UKF. 

Example **14.3** estimation errors for the extended Kalman filter, the 

| Altitude      | Velocity   | Ballistic Coefficient Reciprocal   |      |
|---------------|------------|------------------------------------|------|
| EKF           | 615        | 173                                | 11.6 |
| UKF           | 460        | 112                                | 7.5  |
| Simplex UKF   | 449        | 266                                | 80.8 |
| Spherical UKF | 578        | 142                                | 0.4  |

## Vvv 14.5 Summary

The unscented filter can give greatly improved estimation performance (compared with the extended Kalman filter) for nonlinear systems. In addition, the EKF requires the computation of Jacobians (partial derivative matrices), and the UKF does not use Jacobians. For systems with analytic process and measurement equ& tions (such as Example 14.2), it is easy to compute Jacobians. But some systems are not given in analytical form and it is numerically difficult to compute Jacobians. 

The UKF was first published in 1995 [Ju195] and since then has been expounded upon in many publications.2 Although the UKF is a relatively recent development, it is rapidly finding applications in such areas as aircraft engine health estimation [Dew03], aircraft model estimation [CamOl], neural network training [WanOl], financial forecasting [WanOl], and motor state estimation [Aki03]. In addition, just as in the Kalman filter, the UKF can be implemented in a square root form to effectively increase numerical precision [VanOl, WanOl]. Note that a filter based on polynomial approximations of nonlinear functions is presented in [NorOO], and it seems that the UKF is a special case of this filter. 

There is a lot of room for development in the area of unscented filtering. A glance through this book's table of contents shows many specialized topics that have been applied to Kalman and H, filtering, revealing a rich source of research topics for unscented filtering. These include UKF stability properties, constrained unscented filtering, unscented smoothing, reduced-order unscented filtering, robust unscented filtering, unscented filtering with delayed measurements, hybrid unscented/H, filtering, and others. 

21t is interestingto note that the first journal publicationof the **UKF** waa submitted for publication in 1994, but did not appear in print until 2000 [JulOO]. Alternative technologies that are highly different than existing approaches tend to meet with resistance, but persistence (if accompanied by technical rigor) can break down barriers. 

## Problems Written Exercises

14.1 Suppose the RV 2 is uniformly distributed on [-1,1], and y = **z2.** What is g? What is the first-order approximation to g? What is the second-order approximation to **fj?** 
14.2 Suppose the RV z is uniformly distributed on [-1,1], and y = e". What is g? What is the first-order approximation to g? What is the second-order approximation to g? What is the third-order approximation to g? What is the fourth-order approximation to g? 

14.3 Suppose the RV z is uniformly distributed on [-1,1], and y = e". What is the variance of y? What is the first-order approximation to the variance of y? What is the fourth-order approximation to the variance of y? 

14.4 Suppose the RV z is uniformly distributed on [-1,1], and y = *ex.* What is g? What is the unscented approximation to g? 

$\begin{array}{ccc}\text{-}1&3\\ 3&9\end{array}$  . 
$$P=\left|\begin{array}{l}{{}}\\ {{}}\end{array}\right|$$
14.5 Consider the matrix Find an upper triangular matrix S (using only paper and pencil) such that PS = P. Find a lower triangular matrix S such that **flS** = P. (Note the difference between your solution to this problem and the solution to Problem 6.7.) 
14.6 Suppose the RV z is uniformly distributed on [-1,1], and y = e". What is the variance of y? What is unscented approximation to the variance of y? 

14.7 Show that for a system with an identity transition matrix, the UKF algorithm gives 2; = 
14.8 Show that for a system with Yk = **zk,** the UKF gain Kk is positive definite. 14.9 Suppose the RV z is uniformly distributed on [-1,l], and y = e". What is g? Use the generalized unscented transformation to approximate Q with K. = 0, K. = 1, and K. = 2. 

14.10 Suppose the RV z is uniformly distributed on [-1,1], and y = e". What is the variance of y? Use the generalized unscented transformation to approximate the variance of y with K. = 0, K = 1, and K. = 2. 

14.11 Consider the simplex sigma-point algorithm. Prove that *C, W(i)oy)* = 0 
(i.e., the weighted sample mean of the 0:) vectors is zero). 14.12 Prove that the sum of the weights in the simplex sigma-point algorithm is equal to 1. 

14.13 Consider the simplex sigm&point algorithm. Prove that the C, W(i)z(i) = 
5 (i.e., the weighted sample mean of the sigma points is equal to 5). (Hint: Use the results of Problems 14.11 and 14.12.) 

## Computer Exercises

14.14 Design an unscented Kalman filter for the system described in Problem 13.21. Simulate the system and the filter for 60 s. Plot the estimation error for the four states. What is the experimental standard deviation of the estimation error for each of the four states? Based on the steady-state covariance matrix of the filter, what is the theoretical standard deviation of the estimation error for each of the four states? How does this compare with the extended Kalman filter results of Problem 13.21? 

14.15 An inverted pendulum on a cart can be modeled as follows [Bay99, Che991. 

$$\begin{array}{r c l}{{\ddot{\theta}}}&{{=}}&{{\frac{m g l\sin\theta(M+m)-m l\cos\theta(u+m l\dot{\theta}^{2}\sin\theta-B\dot{d})}{(J+m^{2})(M+m)-m^{2}l^{2}\cos^{2}\theta}}}\\ {{}}&{{}}&{{}}\\ {{\ddot{d}}}&{{=}}&{{\frac{u-m l\ddot{\theta}\cos\theta+m l\dot{\theta}^{2}\sin\theta-B\dot{d}}{M+m}}}\end{array}$$

The quantities in the system model are as follows: 
e(o) = 
d(0) = 
m= 
M= 
9= 
B= 
1= 
T= 
u= 
J= 
- 
initial angle (0.1 rad) 
initial cart displacement (0 rad) pendulum mass (0.2 kg) 
cart mass (1 kg) 
acceleration due to gravity (9.81 m/s2) coefficient of friction between cart and ground [0.1 N/(m/s)] 
pendulum length (1 m) 
pendulum mass radius (0.02 m) external force applied to cart pendulum moment of inertia mr2/2 where we have assumed that the pendulum mass is concentrated in a cylinder at the end of the pendulum. Define the state of the system as z = [ *d d* 8 e ] , 
The horizontal displacement d is measured every 5 ms with a standard deviation of 0.1 m. The continuous-time process noise is Qc = diag(0,0.0004,0,0.04). The system can be linearized (so that an EKF can be used to estimate the state) by assuming that 0 is small, so cos t9 m 1, sin 8 M 0, and e2 = 0. Suppose that the feedback control signal is given as u = 408 and the initial state is perfectly known. 

Write an EKF and a UKF to estimate the state, where the control is assumed by the filters to be 0 = 408. Plot the true states and estimated states for a 2 second simulation. Which filter appears to perform better? 

T 