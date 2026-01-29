---
type: chapter
chapter: 3
title: Least squares estimation
---

[Image on page 1]


# CHAPTER 3


Least squares estimation

**The most probable value of the unknown quantities will be that in which the sum of** the squares of the differences between the actually observed and the computed values **multiplied by numbers that measure the degree of precision is a minimum.** **-Karl Friedrich Gauss [GauOli]**

In this chapter, we will discuss least squares estimation, which is the basic idea of Karl Gauss's quote above.' The material in this chapter relies on the theory of the previous two chapters, and will enable us to derive optimal state estimators later in this book. **Section 3.1 discusses the estimation of a constant vector on the basis of several** **linear but noisy measurements of that vector. Section 3.2 extends the results of** **Section 3.1 to the case in which some measurements are more noisy than others;** **that is, we have less confidence in some measurements than in others. Sections 3.1** **and 3.2 use matrices and vectors whose dimensions grow larger as more measure-** ments are obtained. This makes the problem cumbersome if many measurements **are available. This leads us to Section 3.3, which presents a recursive way of e s** timating a constant on the basis of noisy measurements. Recursive estimation in this chapter is a method of estimating a constant without increasing the computa-

**lGauss published his book in 1809, although he claimed to have worked out his theory as early** as 1795 (when he was 18 years old).

*Optimal State Estimation, First Edition. By Dan J. Simon* **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **79**

---


[Image on page 2]


**80**

tional effort of the algorithm, regardless of how many measurements are available. **Finally, Section 3.4 presents the Wiener filter, which is a method of estimating** a time-varying signal that is corrupted by noise, on the basis of noisy measure- ments. Until 1960, Wiener filtering was the state of the art in signal estimation. The paradigm of signal estimation was shattered with the publication of Rudolph Kalman’s work and related papers in the early 1960s, but it is still worthwhile un- derstanding Wiener filtering because of its historical place in the history of signal estimation. Furthermore, Wiener filtering is still very useful in signal processing and communication theory.


## 3.1 ESTIMATION OF A CONSTANT


In this section, we will determine how to estimate a constant on the basis of several noisy measurements of that constant. For example, suppose we have a resistor but we do not know its resistance. We take several measurements of its resistance using a multimeter, but the measurements are noisy because we have a cheap multimeter. We want to estimate the resistance on the basis of our noisy measurements. In this case, we want to estimate a constant scalar but, in general, we may want to estimate a constant vector. *To put the problem in mathematical terms, suppose x is a constant but unknown* *n-element vector, and y is a Ic-element noisy measurement vector. How can we find* *the “best” estimate h of x? Let us assume that each element of the measurement* *vector y is a linear combination of the elements of x ,  with the addition of some* measurement noise:

*y i  = Hiizi + * * * + H i n ~ n  + 211*

**This set of equations can be put into matrix form as**

*~ = H x + w* **(3.2)**

Now define ey as the difference between the noisy measurements and the vector *H2:* *ey = y - H h* **(3.3)** 
## q, is called the measurement residual. As Karl Gauss wrote [GauOl], the most
 **probable value of the vector x is the vector 2 that minimizes the sum of squares** *between the obsemed values y and the vector Hh. So we will try to compute the h* **that minimizes the cost function J, where J is given as**

*J is often referred to in control and estimation books and papers as a cost func-* tion, objective function, or return function. We can substitute for ey in the above *equation to rewrite J as*

*J* *= ( y -  H 2 ) T ( y -  H2)* *= y T y  - hTHTy - yTH3 + hTHTHh* **(3.5)**

---

**81**

**In order to minimize J with respect to 2, we compute its partial derivative and set** it equal to zero: *- -yTH - yTH + 2?'HTH* *d J* *a? _ -*

= o

Solving this equation for ? results in

*HTy = HTH?* *? = (HTH)-'HTy* *= H L y* **(3.7)** 
## where H L ,  the left pseudo inverse of H ,  exists if k 2 n and H is full rank. This
 **means that the number of measurements k is greater than the number of variables** *n that we are trying to estimate, and the measurements are linearly independent.* In order to prove that we have found a minimum rather than some other type of *stationary point2 of J ,  we need to prove that the second derivative of J is positive* **semidefinite (see Problem 3.1).**

**EXAMPLE3.1**

Let us go back to our original problem of trying to estimate the resistance z of **an unmarked resistor on the basis of k noisy measurements from a multimeter.** **In this case, 2 is a scalar so our k noisy measurements are given as**

**These k equations can be combined into a single matrix equation as**

**Equation (3.7) shows that the optimal estimate of the resistance x is given as**

*? = ( H ~ H ) - ~ H ~ Y*

In this simple example, we see that least squares estimation agrees with our intuition to simply compute the average of the measurements. vvv

**2A stationary point of a function is any point at which its derivative is equal to zero. A stationary** **point of a scalar function could be a maximum, a minimum, or an inflection point. A stationary** point of a vector function could be a maximum, a minimum, or a saddle point.

---


[Image on page 4]


**82**

**3.2** 
## WEIGHTED LEAST SQUARES ESTIMATION


In the previous section, we assumed that we had an equal amount of confidence in all of our measurements. Now suppose we have more confidence in some measurements than others. In this case, we need to generalize the results of the previous section to obtain weighted least squares estimation. For example, suppose we have several measurements of the resistance of an unmarked resistor. Some of the measurements were taken with an expensive multimeter with low noise, but other measurements were taken with a cheap multimeter by a tired student late at night. We have more confidence in the first set of measurements, so we should somehow place more emphasis on those measurements than on the others. However, even though the *second set of measurements is less reliable, it seems that we could get at least some* information from them. This section shows that we can indeed get some information from less reliable measurements. We should never throw away measurements, no matter how unreliable they may be. To put the problem in mathematical terms, suppose x is a constant but unknown **n-element vector, and y is a k-element noisy measurement vector. We assume that** **each element of y is a linear combination of the elements of x, with the addition** of some measurement noise, and the variance of the measurement noise may be **different for each element of y:**

*E($) =* **CT,"** 
## (i = 1,. . . , k)
 **(3.11)**

We assume that the noise for each measurement is zero-mean and independent. The measurement covariance matrix is

*R = E ( v w ~ )*

0 CTf ... - - [ 0 ... u;] **(3.12)**

**Now we will minimize the following quantity with respect to 2.**


## J = Eyl/Cl
 **2** **2** + 
# 9 * * + eEk/g;
 **(3.13)**

**Note that instead of minimizing the sum of squares of the ey elements as we did in** **Equation (3.4), we will minimize the weighted sum of squares. If y1 is a relatively** noisy measurement, for example, then we do not care as much about minimizing **the difference between y1 and the first element of H2 because we do not have much** **confidence in y1 in the first place. The cost function J can be written as**

*J* 
## = ETR-'E~
 
# = (9 - H2)TR-1(y - H 2 )
 
# = y T ~ - l y  - P H ~ R - ~ Y
 
# - Y ~ R - ~ H P
 
# + P H ~ R - ~ H ~
 **(3.14)**

---

**83**

**Now we take the partial derivative of J with respect to 2 and set it equal to zero** **to compute the best estimate 2:** - - y T ~ - l ~ + 3 i . T ~ T ~ - 1 ~ *d J* *at _ -*

= o

H T R - ~ ~  = H T R - ~ H ~ ~ 
## 2 = ( H T R - ~ H ) - ~ H T R - ~ ~
 **(3.15)**

*Note that this method requires that the measurement noise matrix R be nonsin-* gular. In other words, each of the measurements yi must be corrupted by at least *some noise for this method to work.*

**EXAMPLE3.2**

We return to our original problem of trying to estimate the resistance x of an **unmarked resistor on the basis of k noisy measurements from a multimeter.** **In this case, 2 is a scalar so our k noisy measurements are given as**


# yi = x + vi
 *E($) = .P* 
## ( i = l ,  .... k)
 **(3.16)**

**The k measurement equation can be combined into a single matrix equation** as

**(3.17)**

and the measurement noise covariance is given as


## R = diag(a!, .... c:)


**Equation (3.15) shows that the optimal estimate of the resistance 2 is given**

**(3.18)**

[ 1 ". 1 ] ... 0 1

**uT**

0 
## . . .  u;
 . . . .

-l r 1

*= (c* **l/u?)-l (Yl/.f** + . ' .  + Yk/.E) **(3.19)**

**We see that the optimal estimate L is a weighted sum of the measurements,** where each measurement is weighted by the inverse of its uncertainty. In other words, we put more emphasis on certain measurements, in agreement

---


[Image on page 6]


**84**

**with our intuition. Note that if all of the 0% constants are equal, this estimate** **reduces to the simpler form given in Equation (3.10).** vvv


## 3.3
 
## RECURSIVE LEAST SQUARES ESTIMATION


**Equation (3.15) gives us a way to compute the optimal estimate of a constant, but** 
## there is a problem. Note that the H matrix in (3.15) is a k x n matrix. If we obtain
 measurements sequentially and want to update our estimate of z with each new **measurement, we need to augment the H matrix and completely recompute the** **estimate 2. If the number of measurements becomes large, then the computational** effort could become prohibitive. For example, suppose we obtain a measurement of a satellite's altitude once per second. After one hour has passed, the number **of measurements is 3600 and growing. The computational effort of least squares** estimation can rapidly outgrow our resources. **In this section, we show how to r e c u r s i v e l y  compute the weighted least squares** 
# estimate of a constant. That is, suppose we have d after (k - 1) measurements,
 **and we obtain a new measurement Y k .  How can we update our estimate without** **completely reworking Equation (3.15)?** **A linear recursive estimator can be written in the form**

**(3.20)**

**That is, we compute d k  on the basis of the previous estimate d k - 1  and the new** **measurement y k .  Kk is a matrix to be determined called the estimator gain matrix.** **The quantity ( y k - H k d k - 1 )  is called the correction term. Note that if the correction** term is zero, or if the gain matrix is zero, then the estimate does not change from 
# time step (k - 1) to k.
 **Before we compute the optimal gain matrix Kk, let us think about the mean of** the estimation error of the linear recursive estimator. The estimation error mean **can be computed as**


# E(%,k) = E(z - d k )
 
# = E[X - d k - 1  - K k ( Y k  - H k d k - l ) ]
 
# = E[Ez,k-l- K k ( H k Z  -k wk - H k d k - I ) ]
 
# = EIEz,k-l - K k H k ( X  - d k - 1 )  - K k W k ]
 
# = (1 - K k H k ) E ( % , k - l )  - K k E ( V k )
 **(3.21)**


## So if E(?Jk) = 0 and E ( E 2 , k - I )  = 0, then E(E2,k) = 0. In other words, if the
 
## measurement noise vk is zero-mean for all k, and the initial estimate of z is set
 
## equal to the expected value of z [i.e., 2i.0 = E ( x ) ] ,  then the expected value of ?k
 **will be equal to 5 k  for all k .  Because of this, the estimator of Equation (3.20) is** called an unbiased estimator. Note that this property holds regardless of the value **of the gain matrix Kk. This is a desirable property of an estimator because it says** 
## that, on average, the estimate d will be equal to the true value x .
 **Next we turn our attention to the determination of the optimal value of Kk.** **Since the estimator is unbiased regardless of what value of Kk we use, we must**

---


[Image on page 7]


**85**

**choose some other optimality criterion in order to determine Kk. The optimality** criterion that we choose to minimize is the sum of the variances of the estimation **errors at time k:**

**where Pk, the estimation-error covariance, is defined by the above equation. We** **can use a process similar to that followed in Equation (3.21) to obtain a recursive** **formula for the calculation of Pk:**

**pk** 
## = E(Ez,ke:,k)
 
# = E { [ ( I  - K k H k ) E z , k - l  - K k V k ]  [ *  * *IT}
 
## = ( I  - KkHk)E(E.,k-iE:,k-1)(I
 
# - KkHk)T -


# K k E ( V k c : , k - l ) ( I  - KkHk)T - ( I  - KkHk)E(Ez,k-i$)K; f


**KkE(VkVz)K?** **(3.23)**


# Now note that E z , k - l  [the estimation error at time (k - l)] is independent of V k
 **(the measurement noise at time k). Therefore,**

**(3.24)**

**since both expected values are zero. Therefore, Equation (3.23) becomes**

**where Rk is the covariance of V k .  This is the recursive formula for the covariance** of the least squares estimation error. This is consistent with intuition in the sense **that as the measurement noise increases (i.e.l Rk increases) the uncertainty in our** **estimate also increases (Le., Pk increases). Note that Pk should be positive definite** **since it is a covariance matrix, and the form of Equation (3.25) guarantees that Pk** **will be positive definite, assuming that Pk-1 and Rk are positive definite.** **Now we need to find the value of Kk that makes the cost function in Equa-** **tion (3.22) as small as possible. The mean of the estimation error is zero for any** **value of Kk, so if we choose Kk to make the cost function (i.e.l the trace of Pk)** small then the estimation error will not only be zero-meanl but it will also be con- **sistently close to zero. In order to find the best value of Kk, first we need to recall** 
## from Equation (1.66) that sn(tfA'l = 2AB if B is symmetric. With this in mind
 **we can use Equations (3.22), (3.25), and the chain rule to obtain**

---

**86**

**In order to find the value of Kk that minimizes J k ,  we set the above derivative** **equal to zero and then solve for Kk as follows:**


# KkRk = ( I  - KkHk)pk-iH;
 
## Kk(Rk 4- Hkpk-iHT) = Pk-iHr
 **Kk** 
## = Pk-iH;(HkPk-1H;
 
# -k &)-'
 **(3.27)**

**Equations (3.20), (3.25), and (3.27) form the recursive least squares estimator. The** recursive least squares estimator can be summarized as follows.

**Recursive least squares estimation**

**1. Initialize the estimator as follows:**


## $0 = E(z)
 **Po** 
# = E[(x - ?o)(x - 20)7
 **(3.28)**

If no knowledge about z is available before measurements are taken, then 
## Po = mI. If perfect knowledge about z is available before measurements are
 
## taken, then PO = 0.


## 2. For k = 1,2,. .
 
## a, perform the following.


**(a) Obtain the measurement Y k ,  assuming that Y k  is given by the equation**

**where V k  is a zero-mean random vector with covariance Rk. Further** **assume that the measurement noise at each time step k is independent,** 
## that is, E(V&) = Rkdk-%. This implies that the measurement noise is
 white.

**(b) Update the estimate of x and the estimation-error covariance P as fol-** lows:

**3.3.1** **Alternate estimator forms**

**Sometimes it is useful to write the equations for Pk and Kk in alternate forms.** Although these alternate forms are mathematically identical, they can be beneficial from a computational point of view. They can also lead to new results, which we will discover in later chapters. First we will find an alternate form for the expression for the estimation-error **covariance. Substituting for Kk from Equation (3.27) into Equation (3.25) we** obtain **(3.31)** 
# Pk = [I - Pk-lHrsilHk] Pk-i[- *IT -t KkRkK;


---


[Image on page 9]


**87**

(3.34)

This is a simpler equation for Pk [compared with Equation (3.25)] but numerical computing problems (i.e., scaling issues) may cause this expression for Pk to not be positive definite, even when Pk-1 and Rk are positive definite. We can also use the matrix inversion lemma from Section 1.1.2 to rewrite the measurement update equation for 9. Starting with Equation (3.33) we obtain

Applying the matrix inversion lemma to this equation gives

Inverting both sides of this equation gives

(3.38)

This equation for Pk is more complicated in that it requires three matrix inversions, but it may be computationally advantageous in some situations, as will be discussed in Section 6.2. We can use Equation (3.38) to derive an equivalent equation for the estimator gain Kk. Starting with Equation (3.27) we have


$$
Kk = Pk-lH:(HkPk-lH: + Rk)-'
$$
 (3.39)

Premultiplying the right side by PkPF', which is equal to the identity matrix, gives


$$
Kk = PkPFIPk-lHr(HkPk-lH: + Rk)-'
$$
 (3.40)

---

88

**Substituting for PL1 from Equation (3.38) gives**

**Note the Pk-1Hr factor that is on the right of the first term in parentheses. We** can multiply this factor inside the first term in parentheses to obtain

**Now bring Hr out to the left side of the parentheses to obtain**

**Now premultiply the first parenthetical expression by Rkl, and multiply on the** **inside of the parenthetical expression by Rk, to obtain**

**General recursive least squares estimation**

The recursive least squares algorithm can be summarized with the following equa- tions. The measurement equations are given as

**(3.45)**

**The initial estimate of the constant vector 2, along with the uncertainty in that** **estimate, is given as**

**20** *= E(z)* **Po** 
## = E[(x -
 **&I))@** 
## - 20)T]


The recursive least squares algorithm is given as follows. 
## Fork= 1,2,...,


**(3.46)**

**(3.47)**

---


[Image on page 11]


**89**

**EXAMPLE3.3**

*Once again we revisit the problem of trying to estimate the resistance x of* an unmarked resistor on the basis of noisy measurements from a multimeter. However, we do not want to wait until we have all the measurements in order *to have an estimate. We want to recursively modify our estimate of x each* **time we obtain a new measurement. At sample time k our measurement is**

**(3.48)**

*For this scalar problem, the measurement matrix Hk is a scalar, and the* *measurement noise covariance Rk is also a scalar. We will suppose that each* *measurement has the same covariance so the measurement covariance Rk is* **not a function of k, and can be written as R. Initially, before we have any** measurements, we have some idea about the value of the resistance x, and this forms our initial estimate. We also have some uncertainty about our initial estimate, and this forms our initial covariance:

*2 0  = E(x)* *Po* 
$$
= E[(x - &)(x - f o ) T ]
$$
 *= E[(X-fo)Z]* **(3.49)**

*If we have absolutely no idea about the resistance value, then P(0) = 00. If we* are 100% certain about the resistance value before taking any measurements, *then P(0) = 0 (but then, of course, there would not be any need to take* **measurements). Equation (3.47) tells us how to obtain the estimator gain,** *the estimate of x, and the estimation covariance, after the first measurement* 
## (k = 1):


*Kk* *= Pk-1Hr(HkPk-lHr + Rk)-'* *K1 = Po(Po+R)-l*

*f k  = ?k-1 + Kk(yk - Hkfk-1)*

**(3.50)**

Repeating these calculations to find these quantities after the second mea- 
## surement ( k  = 2 )  gives


*Kz =*

*Pz* =


## 22 =


- - **(3.51)**

---


[Image on page 12]


**90**

*By induction, we can find general expressions for Pk-1, Kk, and 2 k  as follows:*

**(3.52)**

*Note that if z is known perfectly a priori (i.e., before any measurements are* *obtained) then Po = 0, and the above equations show that Kk = 0 and ?k =* 
## 20. That is, the optimal estimate of z is independent of any measurements
 
## that are obtained. On the other hand, if z is completely unknown a priori,
 *then Po + m, and the above equations show that*

*1* *-[(k - l ) ? k - l  + Y k ]* *k* = **(3.53)**

*In other words, the optimal estimate of x is equal to the running average of* **the measurements Y k ,  which can be written as**

vvv

**EXAMPLE3.4**

**1** **(3.54)**

In this example, we illustrate the computational advantages of the first form **of the covariance update in Equation (3.47) compared with the third form.** Suppose we have a scalar parameter z and a perfect measurement of it. That *is, H1 = 1 and R1 = 0. Further suppose that our initial estimation covariance* *Po = 6, and our computer provides precision of three digits to the right of the* *decimal point for each quantity that it computes. The estimator gain K1 is*

---

**91**

**computed as**


## = (6)(0.167)
 = 1.002 **(3.55)**

**If we use the third form of the covariance update in Equation (3.47) we obtain**

**PI** 
## = (1 -K1)Po
 = (-0.002)(6) = -0.012 **(3.56)**

The covariance after the first measurement is negative, which is physically impossible. However, if we use the first form of the covariance update in **Equation (3.47) we obtain**

**Pl** 
# = (1 - Kl)PO(l - K l )  + KlRlKl
 
# (1 - K1)2Po + K?R1
 = = o **(3.57)**


# The reason we get zero is because (1 - K I ) ~
 = 0.000004, but our computer retains only three digits to the right of the decimal point. Zero is the theoret- **ically correct value of PI. The form of the above expression for PI guarantees** **that it will never be negative, regardless of any numerical errors in PO,** **R1,** *and K1.* vvv

**EXAMPLE3.5**

**Suppose that a tank contains a concentration 2 1  of chemical 1, and a concen-** **tration 22 of chemical 2. You have some instrumentation that can detect the** 
# combined concentration (21 + 22) of the two chemicals, but your instrumen-
 tation cannot distinguish between the two chemicals. Chemical 2 is removed from the tank through a leaching process so that its concentration decreases by 1% from one measurement time to the next. The measurement equation **is therefore given as**

**where V k  is the measurement noise, which is a zero-mean random variable** 
## with a variance of R = 0.01. Suppose that 21 = 10 and 52 = 5. Further
 
## suppose that your initial estimates are $1 = 8 and $2 = 7, with an initial
 **estimation-error variance Po that is equal to the identity matrix. A recursive** **least squares algorithm can be implemented as shown in Equation (3.47) to** **estimate the two concentrations. Figure 3.1 shows the estimate of 2 1  and 22 as**

---

92

measurements are obtained, along with the variance of the estimation errors. It can be seen that after a couple dozen measurements the estimates become 
## quite close to their true values of 10 and 5. The variances of the estimation
 errors asymptotically approach zero, which means that we have increasingly **more confidence in our estimates as we obtain more measurements.**

**ln 8** **.- S O** 
## 3 .
 **5** **0**

**0** 10 **20** **30** **40** **50** **time step**

**Figure 3.1 Parameter estimates and estimation variances for Example 3.5.**

vvv


## 3.3.2
 **Curve fitting**

In this section, we will apply recursive least squares theory to the curve fitting problem. In the recursive curve fitting problem, we measure data one sample at a 
## time (yl, y2, ...) and want to find the best fit of a curve to the data. The curve
 that we want to fit to the data could be constrained to be linear, or quadratic, or sinusoid, or some other shape, depending on the underlying problem.

**EXAMPLE38**

Suppose that we want to fit a straight line to a set of data points. The linear data fitting problem can be written as

**(3.59)**

**tk is the independent variable (perhaps time), Y k  is the noisy data, and we** **want to find the linear relationship between yk and tk. In other words, we** **want to estimate the constants 2 1  and 22. The measurement matrix can be** **written as**


## H k = [  1 tk ]
 **(3.60)**

---

**93**

**so that Equation (3.59) can be written as**

**Our recursive estimator is initialized as**


## f o  = E(x)


f 2 , o **E(x2)** 
# [ f1,o ] = [ E ( X d  ]


*Po* 
# = E[(z - 2O)(X -


## E [ X l  - f1,0)21
 
# E[(z1 - fl,O)(X2 - f2,o)l
 = [ 
# q z l  - fl,O)(X2 - f2,o)l
 
## El22 - 22,0121


The recursive estimate of the two-element vector z is then obtained from **Equation (3.47) as follows:** 
## For k = l,2,...,


**(3.63)**

vvv

**EXAMPLE3.7**

**Suppose that we know a priori that the underlying data is a quadratic function** of time. In this case, we have a quadratic data fitting problem. For example, suppose we are measuring the altitude of a free-falling object. We know from *our understanding of physics that altitude r is a function of the acceleration* *due to gravity, the initial altitude and velocity of the object TO and TJO, and* 
# time t, as given by the equation r = ro + vot + (a/2)t2. So if we measure T
 **at various time instants and fit a quadratic to the resulting r versus t curve,** 
## then we have an estimate of the parameters 7-0, 210, and a/2. In general, the
 **quadratic data fitting problem can be written as**

**(3.64)**

**tk is the independent variable, Y k  is the noisy measurement, and we want to** **find the quadratic relationship between Y k  and tk. In other words, we want** **to estimate the constants XI, 22, and 23. The measurement matrix can be** written as

**so that Equation (3.64) can be written as** 
## Hk= [ 1 t k
 
## ti ]
 **(3.65)**


# Y k  = H k X  + Vk
 **(3.66)**

**Our recursive estimator is initialized as**


## Po = E(x)
 *Po* 
# = E[(x - fo)(x - 20)*1
 **(3.67)**

---

**94**


## where Po is a 3 x 3 matrix. The recursive estimate of the three-element vector
 z is then obtained from Equation (3.47) as follows: 
## For k = 1,2,. . .,


vvv

(3.68)

**3.4** 
## W I EN E R F I LT E R I N G


In this section, we will give a brief review of Wiener filtering. The rest of this book does not assume any knowledge on the reader’s part of Wiener filtering. However, Wiener filtering is important from a historical perspective, and it still has a lot of applications in signal processing and communication theory. But since it is not used much for state estimation anymore, the reader can safely skip this section if desired. Wiener filtering addresses the problem of designing a linear, timeinvariant filter to extract a signal from noise, approaching the problem from the frequency domain perspective. Norbert Wiener invented his filter as part of the World War I1 effort for the United States. He published his work on the problem in 1942, but it was not **available to the public until 1949 [Wie64]. His book was known as the “yellow peril”** because of its mathematical difficulty and its yellow cover [Deu65, page 1761. An- drey Kolmogorov actually solved a more general problem earlier (1941), and Mark Krein also worked on the same problem (1945). Kolmogorov’s and Krein’s work was independent of Wiener’s work, and Wiener acknowledges that Kolmogorov’s work predated his own work [Wie56]. However, Kolmogorov’s and Krein’s work did not become well known in the Western world until later, since it was pub- **lished in Russian [Ko141]. A nontechnical account of Wiener’s work is given in his** autobiography [Wie56]. To set up the presentation of the Wiener filter, we first need to ask the following *question: How does the power spectrum of a stochastic process z(t) change when* **it goes through an LTI system with impulse response g(t)? The output y(t) of the** system is given by the convolution of the impulse response with the input:


# Y(t) = dt) * 4t)
 (3.69)

Since the system is time-invariant, a time shift in the input results in an equal time shift in the output: 
# y(t + a) = g(t) * z(t + a)
 (3.70) Multiplying the above two equations and writing out the convolutions as integrals gives


# Y(t>Y(t + a) =
 
# g(7)4t - 7 )  &-
 
# S ( M t  + Q - 7)
 **d7** (3.71)

Taking the expected value of both sides of the above equation gives the autocorre **lation of y(t) as a function of the autocorrelation of z(t):** s s

(3.72)

---

**95**

**which we will write in shorthand notation as**

**(3.73)**

Now we take the Fourier transform of the above equation to obtain

*RzI(a)e-jw" d a  = / / / g ( ~ ) g ( y ) R , ( a  + r -y)e-jwad7dyda* **(3.74)** / 
$$
Now we define a new variable of integration /? = a + r - y and replace a in the
$$
 above equation to obtain

*= G(-w)G(w)S,(w)* **(3.75)**

In other words, the power spectrum of the output y(t) is a function of the Fourier *transform of the impulse response of the system, G(w), and the power spectrum of* *the input z(t).* Now we can state our problem as follows: Design a stable LTI filter to extract a signal from noise. The quantities of interest in this problem are given as

*z(t) =* noise free signal

w(t) = additive noise

*g(t) =* filter impulse response (to be designed) *?(t) =* *output of filter [estimate of z(t)]*

*e(t) =* estimation error *= z(t) - ?(t)* **(3.76)**

**Figure 3.2 Wiener filter representation.**

**These quantities are represented in Figure 3.2, from which we see that**

*?(t> = dt) * Mt) + 4t)l*

*E(w) = X ( w )  - X ( w )*

*X ( w )  = G ( w ) [ X ( w )  + V ( w ) ]*

*= X ( W )  - G ( w ) [ X ( w )  + V(W)]* *= [ I  - G ( w ) ] X ( w )  - G(w)V(w)* **(3.77)**

*We see that the error signal e(t) is the superposition of the system [l -G(w)] acting* *on the signal z(t), and the system G ( w )  acting on the signal w(t). Therefore, from* **Equation (3.75), we obtain**

*Se(w) = [ I  - G ( w ) ] [ l -  G(-w)]S,(w) -G(w)G(-w)S,(w)* **(3.78)**

---


[Image on page 18]


**96**

The variance of the estimation error is obtained from Equation (2.92) as

(3.79)

*To find the optimal filter G(w) we need to minimize E[e2(t)],* which means that we *need to know Sz(w) and Sv(w), the statistical properties of the signal z(t) and the* *noise w (t ) .*

**3.4.1 Parametric filter optimization**

*In order to simplify the problem of the determination of the optimal filter G(w),* we can assume that the optimal filter is a first-order, low-pass filter (stable and causal3) with a bandwidth 1/T to be determined by parametric optimization.

1 *1 + T j w* *G(w) = -* (3.80)

This may not be a valid assumption, but it reduces the problem to a parametric *optimization problem. In order to simplify the problem further, suppose that Sz(w)* *and S,(w) are in the following forms.*

**2u2p** *S z ( W )  = -* *W2 + p2* *Sv(w) = A* (3.81)

In other words, the noise w(t) is white. From Equation (3.78) we obtain

**(I+ 1** T j w )  (m) ' A (3.82)

*Now we can substitute Se(w) in Equation (3.79) and differentiate with respect to* *T to find*

(3.83)

**EXAMPLE3.8**


## If A = 0 = p = 1 then the optimal time constant of the filter is computed as


**M 2.4**

**and the optimal filter is given as**

*1* *1 + j w T* *G(w) = -*

(3.84)

**3A causal system is one whose output depends only on present and .future inputs. Real-world** **systems are always causal, but a filter that is used for postprocessing may be noncausal.**

---

*1* *T* *g ( t )  = -e-t/T* *t 2 o*

Converting this filter to the time domain results in

1 *T* 
# d = -(-2 + y)


vvv

**97**

(3.85)

(3.86)

**3.4.2** **General filter optimization**

Now we take a more general approach to find the optimal filter. The expected value of the estimation error can be computed as

*~ [ e ~ ( t ) ]* *= ~ [ s ~ ( t ) ]* - 2 *g(u)R,(u) du -t-* *J*

Now we can use a calculus of variations approach [FomOO, Wei74] to find the filter *g ( t )  that minimizes E[e2(t)].* *Replace g ( t )  in the above equation with g(t) + Eq(t),* 
## where E is some small number, and q(t) is an arbitrary perturbation in g(t). The
 *calculus of variations says that we can minimize E(e2(t)) by setting*

(3.88)

*and thus solve for the optimal g ( t ) .  From Equation (3.87) we can write*

**Taking the partial derivative with respect to E gives**

---

98


# Now recall from Equation (2.87) that R=(T - u) = R,(u - T )  [i.e., R,(T) is even] if
 *z(t) is stationary. In this case, the above equation can be written as*


## o = -2
 *~ ( T ) R , ( T ) ~ T* **t** *J*


## This gives the necessary condition for the optimality of the filter g(t) as follows:


*We need to solve this for g(t) to find the optimal filter.*


## 3.4.3
 **Noncausal filter optimization**

*If we do not have any restrictions on causality of our filter, then g(t) can be nonzero* *for t < 0, which means that our perturbation q(t) can also be nonzero for t < 0.* **This means that the quantity inside the square brackets in Equation (3.92) must** be zero. This results in

**(3.93)**

The transfer function of the optimal filter is the ratio of the power spectrum of the *signal z(t) to the sum of the power spectrums of z(t) and the noise w(t).*

---


[Image on page 21]


**99**

**EXAMPLE3.9**


## Consider the system discussed in Example 3.8 with A = ,8 = u = 1. The
 **signal and noise power spectra are given as**

*S,(w)* *= 1* *(3.94)*

*From this we obtain the optimal noncausal filter from Equation (3.93) as*

*2* *G(w) = -* *W2+3*

**x** *0.58e-0.581ti,* 
## t E [-m, m]
 *(3.95)*

In order to find a time domain representation of the filter, we perform a partial *fraction expansion of G ( w )  to find the causal part and the anticausa14 part of* the filter5:

*(3.96)* -- causal filter anticausal filter

From this we see that

*= R,(w) + X&)* *(3.97)*

*Xc(w) and Xa(y) (defined by the above equation) are the causal and anti-* *causal part of X ( w ) ,  respectively. In the time domain, this can be written* **as**

*(3.98)*

The i, equation runs forward in time and is therefore causal and stable. The **fa equation runs backward in time and is therefore anticausal and stable. (If** it ran forward in time, it would be unstable.) vvv

**4An anticausal system is one whose output depends only on present and future inputs.** 5The MATLAB function RESIDUE performs partial fraction expansions.

---


[Image on page 22]


**100**

**3.4.4** **Causal filter optimization**

*If we require a causal filter for signal estimation, then g(t) = 0 for t < 0, and the* *perturbation q(t) must be equal to 0 for t < 0. In this case, Equation (3.92) gives*


$$
R,(T) - g(u)[R,(u - T )  + R,(u - T ) ]  du = 0,
$$
 *t 2 0* (3.99) s

The initial application of this equation was in the field of astrophysics in 1894 [Sob631 Explicit solutions were thought to be impossible, but Norbert Wiener and Eber- hard Hopf became instantly famous when they solved this equation in 1931. Their solution was so impressive that the equation became known as the Wiener-Hopf equation. *To solve Equation (3.99), postulate some function a(t) that is arbitrary for t < 0,* *but is equal to 0 for t 2 0. Then we obtain*

*R,(T) - /g(u)[R,(u* 
$$
- T) + R,(u - T ) ]  du = a ( ~ )
$$


*S&) - G(w)[&(w) + &J(w)l* *= A(w)* (3.100)

For ease of notation, make the following definition:


$$
S,,(w) = Sz(w) + %(w)
$$
 (3.101)

Then Equation (3.100) becomes *- G(w)S,+,(4S,-,(w> = A ( w )* (3.102)


## where S&(w) is the part of Szv(w)
 that has all its poles and zeros in the LHP (and *hence corresponds to a causal time function), and S&(w) is the part of SZ,(w) that* has all its poles and zeros in the RHP (and hence corresponds to an anticausal time function). Equation (3.102) can be written as

(3.103)

The term on the left side corresponds to a causal time function [assuming that *g(t) is stable]. The last term on the right side corresponds to an anticausal time* function. Therefore,

**SX (w)**


## s;v (w )
 *G(w)S,f,(w) =* causal part of -

*SFV (w)* 1 *~ ( w )  =* [ causal part of - (3.104)

This gives the TF of the optimal causal filter.

**EXAMPLE 3.10**


## Consider the system discussed in Section 3.4.1 with A = ,8 = u = 1. This was
 also discussed in Example 3.9. For this example we have

**n**

---

*S,(W)* = 1

**101**

*(3.105)*

Splitting this up into its causal and anticausal factors gives

*j w + a* *- j w + d 3*

*szv(w)* *= ( j w +  1 ) ( -jw + 1  )*

*Equation (3.104) gives*

*(3.106)*

*(3.107)*

This gives the TF and impulse response of the optimal filter when causality is required. vvv

**3.4.5** **Comparison**

Comparing the three examples of optimal filter design presented in this section *(Examples 3.8, 3.9, and 3.10), it can be shown that the mean square errors of the* *filter are as fdlows [Bro96]:*


## 0 Parameter optimization method: E[e2(t)]
 *= 0.914*


## 0 Causal Wiener filter: E[e2(t)] = 0.732


## 0 Noncausal Wiener filter: E[e2(t)] = 0.577


**As expected, the estimation error decreases when we have fewer constraints on** the filter. However, the removal of constraints makes the filter design problem more difficult. The Wiener filter is not very amenable to state estimation because of difficulty in extension to MIMO problems with state variable descriptions, and difficulty in application to signals with time-varying statistical properties.

---

**102**

**3.5** 
## SUMMARY


In this chapter we discussed least squares estimation in a couple of different con- texts. First we derived a method for estimating a constant vector on the basis of several noisy measurements of that vector. In fact, the measurements do not have to be direct measurements of the constant vector, but they can be measurements of some linear combination of the elements of the constant vector. In addition, the noise associated with each measurement does not have to be the same. The least squares estimation technique that we derived assumed that we the measurement noise is zero-mean and white (uncorrelated with itself from one time step to the next), and that we know the variance of the measurement noise. We then extended our least squares estimator to a recursive formulation, wherein the computational effort remains the same at each time step regardless of the total number of mea- surements that we have processed. Least squares estimation of a constant vector forms a large part of the foundation for the Kalman filter, which we will derive later in this book. **In Section 3.4, we took a brief segue into Wiener filtering, which is a method** of estimating a time-varying signal that is corrupted by noise. The Wiener filter is based on frequency domain analyses, whereas the Kalman filter that we derive later is based on time domain analyses. Nevertheless, both filters are optimal under their own assumptions. Some problems are solvable by both the Wiener and Kalman filter methods, in which case both methods give the same result.

**PROBLEMS**

**Written exercises**

**3.1** **In Equation (3.6) we computed the partial derivative of our cost function with** respect to our estimate and set the result equal to 0 to solve for the optimal estimate. However, the solution minimizes the cost function only if the second derivative of the cost function with respect to the estimate is positive semidefinite. Find the second derivative of the cost function and show that it is positive semidefinite.

**3.2 Prove that the matrix Pk that is computed from Equation (3.25) will always** **be positive definite if 9 - 1  and Rk are positive definite.**

**3.3 Consider the recursive least squares estimator of Equations (3.28)-(3.30). If** 
## zero information about the initial state is available, then Po = 001. Suppose that
 
## you have a system like this with Hk = 1. What will be the values of K1 and PI?


## 3.4 Consider a battery with a completely unknown voltage (PO = m). Two
 independent measurements of the voltage are taken to estimate the voltage, the **first with a variance of 1, and the second with a variance of 4.** 
## a) Write the weighted least squares voltage estimate in terms of the two
 
## measurements y1 and y2.
 **b) If weighted least squares is used to estimate the voltage, what is the vari-** ance of voltage estimate after the first measurement? What is the variance of the voltage estimate after the second measurement?

---

**103**


# c) If the voltage is estimated as (y1 + y2)/2, an unweighted average of the
 measurements, what is the variance of the voltage estimate?

**3.5** Consider a battery whose voltage is a random variable with a variance of 1. Two independent measurements of the voltage are taken to estimate the voltage, **the first with a variance of 1, and the second with a variance of 4.** **a) Write the weighted least squares voltage estimate in terms of the initial** 
## estimate 30 and the two measurements y1 and y2.
 b) If weighted least squares is used to estimate the voltage, what is the vari- ance of voltage estimate after the first measurement? What is the variance of the voltage estimate after the second measurement?

**3.6** 
## Suppose that { z 1 , x z ,  * , z,} is a set of random variables, each with mean
 
# 3 and variance a2. Further suppose that E[(x2 - 3)(x, - Z)] = 0 for i # j .  We
 
## estimate 3 and u2 as follows.


## a) Is 5 an unbiased estimate of z? That is, is E(2) = Z?
 
## b) Find E ( x g j )  in terms of 1 and u2 for both i = j and i # j.
 
## c )  Is b2 an unbiased estimate of a2? That is, is E($) = u2? If not, how
 
## should we change 6' to make it an unbiased estimate of u2?


**3.7 Suppose a scalar signal has the values 1, 2, and 3. Consider three different** **estimates of this timevarying signal. The first estimate is 3, 4, 1. The second** 
## estimate is 1, 2, 6. The third estimate is 5 ,  6, 7. Create a table showing the RMS
 value, average absolute error, and standard deviation of the error of each estimate. Which estimate results in the error with the smallest RMS value? Which estimate results in the error with the smallest infinity-norm? Which estimate gives the error with the smallest standard deviation? Which estimate do you think is best from an intuitive point of view? Which estimate do you think is worst from an intuitive point of view?

**3.8** **Suppose a random variable x has the pdf f(x) given in Figure 3.3.** **a) x can be estimated by taking the median of its pdf. That is, P is the** solution to the equation

*h* *00* 
# f(x) dx = 1
 **f(x)** *L* Find the median estimate of x. b) x can be estimated by taking the mode of its pdf. That is,


## f = arg maxf(x)


Find the mode estimate of x.


## c )  x can be estimated by computing its mean. That is,


*00*

---

**104**

Find the mean of z. 
## d) z can be estimated by computing the minimax value. That is,


# 2 = minmaxlz - $1
 **X**

Find the minimax estimate of z.

**X**

**Figure 3.3 pdf for Problem 3.8.**

**3.9 Suppose you are responsible for increasing the tracking accuracy of a radar** **system. You presently have a radar that has a measurement variance of 10. For** equal cost you could either: (a) optimally combine the present radar system with a new radar system that has a measurement variance of 6; or, (b) optimally combine **the present radar system with two new radar systems that both have the same** **performance as the original system [May79]. Which would you propose to do?** Why?

**3.10 Consider the differential equation**

*k + 3 z = u*

*If the input u(t) is an impulse, there are two solutions z(t) that satisfy the differ-* ential equation. One solution is causal and stable, the other solution is anticausal and unstable. Find the two solutions.

**3.11 Suppose a signal z(t) with power spectral density**

*is corrupted with additive white noise v(t) with a power spectral density Sv(s) = 1.* **a) Find the optimal noncausal Wiener filter to extract the signal from the** noise corrupted signal. b) Find the optimal causal Wiener filter to extract the signal from the noise corrupted signal.

---

**105**

**3.12 A system has the transfer function**

1 *G(s) = -* s - 3

*If the input is an impulse, there are two solutions for the output z(t) that satisfy* the transfer function. One solution is causal and unstable, the other solution is anticausal and stable. Find the two solutions.

**Computer exercises**

**3.13 The production of steel in the United States between 1946 and 1956 was** 66.6,84.9,88.6,78.0,96.8, 105.2,93.2, 111.6,88.3,117.0, and 115.2milliontons [Sor80]. Find the least squares fit to these data using (a) linear curve fit; (b) quadratic curve fit; (c) cubic curve fit; (d) quartic curve fit. For each case give the following: (1) a **plot of the original data along with the least squares curve; (2) the RMS error of** the least squares curve; (3) the prediction of steel production in 1957.

**3.14 Implement the Wiener filters for the three examples given in Section 3.4** and verify the results shown in Section 3.4.5. Hint: Example 8.6 shows that if 
# j. = -z + w where w(t) is white noise with a variance of Qc = 2, then


**n** **L** *S Z ( W )  = -* w2 + 1

**From Sections 1.4 and 8.1 we see that this system can be simulated as**

*where w (t) and v(t) are independent zero-mean, unity variance random variables.*