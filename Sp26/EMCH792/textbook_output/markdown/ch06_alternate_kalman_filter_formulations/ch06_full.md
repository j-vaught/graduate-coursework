---
type: chapter
chapter: 6
title: Alternate Kalman filter formulations
---

[Image on page 1]


## CHAPTER 6


Alternate Kalman filter formulations

Our experiences with estimation and control applications engineers, however, indicates that they generally prefer the seemingly simpler Kalman filter algorithms for computer implementation and they dismiss reported instances of numerical failure. -Gerald Bierman and Catherine Thornton [Bie77a]

In this chapter, we will look at some alternate ways of writing the Kalman filter equations. There are a number of mathematically equivalent ways of writing the Kalman filter equations. This can be confusing. You might read two different papers or books that present the Kalman filter equations, and the equations might look completely different. You may not know if one of the equations has a typographical error, or if they are mathematically equivalent. So you try to prove the equivalence 
## of the two sets of equations only to arrive at a mathematical dead end, because it
 is not always easy to prove the equivalence of two sets of equations. This chapter derives some Kalman filter formulations that are different than (but mathematically 
## equivalent to) the equations we derived in Chapter 5. This chapter also illustrates
 their advantages and disadvantages. The first alternate formulation that we discuss is called the sequential Kalman filter, derived in Section 6.1. Sequential Kalman filtering allows for the implemen- tation of the Kalman filter without matrix inversion. This can be a great benefit, especially in an embedded system that does not have matrix libraries, but it only

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **149**

---


[Image on page 2]


**150**

makes sense if certain conditions are satisfied. The second formulation that we **discuss is called information filtering, derived in Section 6.2. Information filter-** **ing propagates the inverse of the covariance matrix (i.e., P-l) instead of P ,  and is** computationally cheaper than Kalman filtering under certain conditions. The third **formulation that we discuss is called square root filtering, derived in Section 6.3.** Square root filtering effectively increases the precision of the Kalman filter, which can help prevent divergence and instability. However, this is at the cost of increased computational effort. The final formulation that we discuss is called U-D filtering, **derived in Section 6.4. This is another way to implement square root filtering,** which helps to prevent numerical difficulties in the implementation of the Kalman filter.

**6.1 SEQUENTIAL KALMAN FILTERING**

In this section, we derive the sequential Kalman filter. This is a way of implement- ing the Kalman filter without matrix inversion. This can be a great advantage, especially in an embedded system that may not have matrix routines. However, the use of sequential Kalman filtering only makes sense if certain conditions are satisfied, which we will discuss in this section. **Recall the Kalman filter measurement update formulas from Equation (5.16):**


## The computation of Kk requires the inversion of an T x T matrix, where T is the
 **number of measurements. This is depicted in Figure 6.1.**

I j r measurements

i 
## r r x r matrix inversion
 !

**k-1** **k** time

**Figure 6.1**

**T x T matrix inversion, where T is the number of measurements.** The measurement-update equation of the standard Kalman filter requires an


## Suppose that instead of measuring Yk at time k, we obtain T separate measure-
 
# ments at time k. That is, we first measure Y k ( l ) ,  then Yk(2), . . ., and finally Yk (.).
 **We will use the shorthand notation Yik for the ith element of the measurement** **vector yk. Assume for now that RI, (the covariance of measurement Y k )  is diagonal;**

---


[Image on page 3]


**151**

**that is, R k  is given as** **R l k** ' * * 0


# R k =  [ 0
 *.. ] (6.2)

* * * **R , k**

**We will also use the notation that H i k  is the ith row of H k ,  and v i k  is the ith** **element of V k .  Then we obtain**

**So instead of processing the measurements at time k as a vector, we will imple-** ment the Kalman filter measurement-update equation one measurement at a time. **We use the notation that K i k  is the Kalman gain that is used to process the ith** **measurement at time k, i& is the optimal estimate after the ith measurement has** **been processed at time k ,  and P$ is the estimation-error covariance after the ith** **measurement at time k has been processed. We can see from these definitions that**

**That is, 3$k is the estimate after zero measurements have been processed, so it is** **equal to the a priori estimate. Similarly, P& is the estimation-error covariance after** zero measurements have been processed, so it is equal to the a priori estimation- **error covariance. The gain K i k  and covariance PA are obtained from the normal** Kalman filter measurement-update equations, with the understanding that they 
## apply to the scalar measurement y i k .  For i = 1,. - . , r we have


## After all r measurements are processed, we set 2; = i?&, and P z  = PA, and
 **we have our a posteriori estimate and error covariance at time k. The sequential** Kalman filter does not require any matrix inversions because all of the expressions **in Equation (6.5) are scalar operations. This process is depicted in Figure 6.2. The** sequential Kalman filter can be summarized as follows.

**The sequential Kalman filter**

1. The system and measurement equations are given as


## x k  = F k - i X k - i +
 **G k - i U k - i f** **W k - 1**


## Y k  = H k X k + V k


**w k** **( O , Q k )**

**v k** **( 0 , R k )** (6.6)

**where W k  and Vk are uncorrelated white noise sequences. The measurement** **covariance R k  is a diagonal matrix given as**


## R k  = diag(Rlk, * * * , R r k )
 (6.7)

---


[Image on page 4]


**152**

1 measurement 1 x 1 matrix inversion

**k-1** - **k** time

**Figure 6.2** The measurement update equation of the sequential Kalman filter requires

**P scalar divisions (where T is the number of measurements) because the measurements at** each time step are processed sequentially. This is in contrast to the standard Kalman filter processing that is depicted in Figure 6.1.

**2. The filter is initialized as**

**3. At each time step k, the time-update equations are given as**

This is the same as the standard Kalman filter.


## 4. At each time step k, the measurement-update equations are given as follows.


**(a) Initialize the a posteriori estimate and covariance as**

(6.~10)

**These are the a posteriori estimate and covariance at time k after zero** *measurements have been processed; that is, they are equal to the a priori* estimate and covariance. 
# , T (where T is the number of measurements), perform the
 following: 
## (b) For i = 1,.


---


[Image on page 5]


153


## (c) Assign the a posteriori estimate and covariance as


## '+ k
 
## = ':k
 **P;** 
## = P+
 **rk** (6.12)

**The development above assumes that the measurement-noise covariance Rk is** 
## diagonal. What if Rk is not diagonal? Suppose that Rk = R is not diagonal, but
 **it is a constant matrix. We perform a Jordan form decomposition of R by finding** a matrix S such that 
## R = SRS-l
 (6.13)


## R is a diagonal matrix containing the eigenvalues of R, and S is an orthogonal
 
# matrix (i.e., S-l = p)
 **containing the eigenvectors of R. This decomposition** **is always possible if R is symmetric positive definite, as discussed in most linear** **systems books [Bay99, Che99, KaiOO]. Now define a new measurement fik as**

(6.14)

**where f i k  and 'uk are defined by the above equation. The covariance of '6k can be** **obtained as**

**So we have introduced a normalized measurement fik that has a diagonal noise** covariance. Now we can implement the sequential Kalman filter equations, except **that we use the measurement fik instead of Y k ,  the measurement matrix f i k  instead** **of Hk, and the measurement noise covariance R.** **Note that this procedure would not make sense if R were timevarying, because in** that case we would have to perform a Jordan form decomposition at each step of the Kalman filter. That would be a lot of computational effort in order to avoid a matrix **inversion. However, if R is constant and it is known before the implementation of** the Kalman filter, then we can perform the Jordan form decomposition offline and use the sequential Kalman filter to our advantage. In summary, it only makes sense to use the sequential Kalman filter if one of the following two conditions holds:

**1. The measurement noise covariance Rk is diagonal**

**2. The measurement noise covariance R is a constant.**

---

**154**

Finally, note that the term sequential filtering is sometimes used synonymously with the Kalman filter. That is, sequential is often used as a synonym for recur- sive [Buc68, Chapter 131, [Bro96]. This can cause some confusion in terminology. **However, sequential filtering is usually used in the literature as we use it in this sec-** tion; that is, sequential filtering is a filtering method that processes measurements **one at a time (rather than processing the measurements as a whole vector). Some** times, the standard Kalman filter is called the batch Kalman filter to distinguish it from the sequential Kalman filter.

**EXAMPLE6.1**

**The change X k  from one week to the next of an American football team’s** ranking is related to the team’s performance against that week’s opponent. **The expected relationships between various normalized game measures y&** and the team’s ranking change at the kth week are given as


# Y l k  = X k  + V l k  = point differential


# yzk = -xk + w2k = turnover differential


## Y3k =
 
# - X k  + V3k = yardage differential


## where W l k  N (0,2), W2k N (0, l), and V3k N (0,50). Before the first game of the
 season is played, it is expected that the team ranking will increase by one due *to certain players having returned from injuries. The variance of this a priori* **estimate is 4. Uncertainty in ownership conditions is expected to decrease** **the team’s ranking by 5% each week, with a variance of 2. The system can** therefore be modeled as

1 **5** **1** **50** (6.16)


## xk+l = 0 . 9 5 ~ k + w k


**yk** 
## = [ 1 1/5 1/50 ] T X k + W k


**wk** **( O , Q )** **Q = 2**

**Wk** *N* *(0, R) R = diag(2,1,50)* **2;** = 1 
## Po+ = 4
 (6.17)

*Suppose that the team plays its first game and wins by six points, gains* **three more turnovers than its opponent, and is outgained by 100 yards. That** is, y1 = [ 6 3 -100 3’. ranking as follows: The standard Kalman filter adjusts the team’s


# FP$FT + Q
 **5.61** **0.952;** **0.95**


## [ 0.6961 0.2785 0.0006 ]
 
# P p P ( H P T H T  + R)-1


# 2T + Kl(y1- H?i.,)


---


[Image on page 7]


**155**

= 5.1922 *P.f* *= (I-K1H)P,-* = 1.3923 (6.18)

*The K1 calculation requires the inversion of a 3 x 3 matrix. On the other* hand, the sequential Kalman filter could be used to update the estimated team ranking as follows:

*Pc = FP2FT+Q*

**2;** = 0.952: = 5.61

= 0.95


## 2i'ofi = 2;
 *Pofi* *= P-* *1*

The first measurement is processed as follows:

*Kii = P&HT(HiP&HT + Rii)-l* = 0.7372

*$1* = *+ Kll(Y11 - Hl2i'o+l)*

*p;:* *= (I-K11HdP&* = 4.6728

= 1.4744

**The second measurement is processed as follows:**

(6.19)

(6.20)

(6.21)

The third measurement is processed as follows:

*K31 = P,',H,T(H3PZ+lHT + R33)-'* = 0.0006 *2&* 
# zz 2$l f K31(Y33 - H32i1)
 = 5.1922 *PA = ( I  - K31H3)PL* = 1.3923 (6.22)

The sequential Kalman filter requires three loops through the measurement update equations, but no matrix inversions are required. vvv

---


[Image on page 8]


156

**6.2** 
## I N FO R MAT I 0
 
## N F I LT E R I N G


In this section, we discuss information filtering. This is an implementation of the **Kalman filter that propagates the inverse of P rather than propagating P ;  that is,** information filtering propagates the information matrix of the system. Recall that


# P = E[(z - ?)(z -?)TI
 **(6.23)**

**That is, P represents the uncertainty in the state estimate. If P is “large” then** **we have a lot of uncertainty in our state estimate. In the limit as P t 0 we** **have perfect knowledge of x ,  and as P t** *00 we have zero knowledge of x. The* information matrix is defined as 
## Z = p-1
 **(6.24)**

That is, Z represents the certainty in the state estimate. If Z is “large” then we 
## have a lot of confidence in our state estimate. In the limit as Z + 0 we have zero
 
## knowledge of x ,  and as Z t
 
## 00 we have perfect knowledge of x .
 **Recall from Equation (5.19) that the measurement update equation for P can** be written as **(6.25)** 
# (P;)-1 = (P;)-’ + HrRk’Hk


Substituting the definition of Z into this equation gives


## 1: =
 
# + HrRk’Hk
 **(6.26)**

This gives the measurement-update equation for the information matrix. Recall **from Equation (5.19) the time-update equation for P :**


## p; = Fk-iPk+lFF-1+ Q k - i
 **(6.27)**

This implies that 
# 1; = [Fk-i(ZL-l)-lFr-l + Qk-11-l
 **(6.28)**

**Now we can use the matrix inversion lemma from Section 1.1.2, which we restate** here: 
# ( A  + BD-lC)-l= A-’ - A-lB(D + CA-lB)-lCA-l
 **(6.29)**


## If we make the identifications A = Qk-1, B = 9 - 1 ,  C = FkT_l, and D = Zk+-l,
 **then we can apply the matrix inversion lemma to Equation (6.28) to obtain** 
# 1; = Q L 2 1 -  Qi?iFk-l(Zk-i
 
# + + Fk-1Qk21Fk-l)-1Fr-iQ~~l
 **T** **(6.30)**

This gives the timeupdate equation for the information matrix. The information filter can be summarized as follows.

**The information filter**

**1. The dynamic system is given by the following equations:**


# x k  = Fk-126-1 + Gk-1Uk-l f W k - ]


## Yk = HkXk+vk
 **wk** **(0,Qk)**

---


[Image on page 9]


**157**

**(6.31)**

**2. The Kalman filter is initialized as follows:**

**3. The information filter is given by the following equations, which are computed** 
## for each time step k = 1,2,
 **a:**


## The standard Kalman filter equations require the inversion of an T x T matrix, where
 *r is the number of measurements. The information filter equations require at least* 
## a couple of n x n matrix inversions, where n is the number of states. Therefore,
 
## if T >> n (i.e., we have significantly more measurements than states) it may be
 computationally more efficient to use the information filter. It could be argued that since the Kalman gain is given as

**(6.34)**


## we have to perform and T x T matrix inversion on Rk anyway, whether we use the
 **standard Kalman filter or the information filter. But if Rk is constant, then we** could invert it as part of the initialization process, so the Kalman gain equation 
## may not require this T x T matrix inversion after all. The same thinking also applies
 **to the inversion of Q k - 1 .** 
## If the initial uncertainty is infinite, we cannot numerically set Po+ = 00, but we
 **can numerically set 1 ,** = 0. This makes the information filter more mathematically precise for the zero initial certainty case. However, if the initial uncertainty is zero 
## (i.e., we have perfect knowledge of zo), we can numerically set P: = 0, but we
 
## cannot numerically set 1; = 00. This makes the standard Kalman filter more
 mathematically precise for the zero initial uncertainty case

**EXAMPLE6.2**

The information filter can be used to solve the American football team ranking **problem of Example 6.1. The information filter equations are given as**


# 1,- = Q-1 - Q-~F(z$ + F T Q - ~ F ) - ~ F T Q - ~
 
## = 0.1783


---

158

z,- 
# + H ~ R - ~ H
 0.7183

**@ ) - I** **HTR-1**

**F2i.,f** [ 0.6961 0.2785 0.0006 ]

0.95 
# 2; + Kl(yl - H2;)
 5.1922 (6.35)

**The information filter requires the inversion of Q and R, but in many appli-** cations these matrices are constant and can therefore be inverted offline. The only other matrix inversions are in the **and Kk equations. These inversions** are scalar in this example because there is only one state in this example. vvv


## 6.3
 **SQUARE ROOT FILTERING**

The early days of Kalman filtering in the 1960s saw a lot of promise and successful applications in the aerospace industry and in NASA’s space program, but sometimes problems arose in implementation. Many of the problems that were encountered **were due to numerical difficulties. The Riccati equation solution Pk should theoret-** ically always be -a symmetric positive semidefinite matrix, but numerical problems **in computer implementations sometimes led to Pk matrices that became indefinite** or nonsymmetric. This was often because of the short word lengths in the com- puters of the 1960s [Sch81]. Numerical problems may arise in cases in which some **elements of the state-vector 2 are estimated to much greater precision than other** **elements of 2. This could be because of discrepancies in the units of the state-vector** elements. For example, one state might be in units of miles and can be estimated to within 0.01 miles, whereas a second state might be in units of cm/s and can be estimated to within 10 cm/s. The covariance for the first state would be on the order of whereas the covariance for the second state would be on the order of lo2. This led to a lot of research during the 1960s that was related to numerical implementations. Square root filtering is a way to mathematically increase the precision of the Kalman filter when hardware precision is not available. Perhaps the first square root algorithm was developed by James Potter for NASA’s Apollo space pro- gram [Bat64]. Although Potter’s algorithm was limited to zero process noise and **scalar measurements, its success led to a lot of additional square root research** in the following years. Potter’s algorithm was extended to handle process noise **in [And68, Dye691, and was generalized in two different ways to handle vector mea-** surements in [Be167, And681. Paul Kaminski gives a good review of square root filtering developments during the first decade of the Kalman filter [Kam7l]. Now that computers have become so much more capable, we do not have to worry **about numerical problems as often. Nevertheless, numerical issues still arise in** finite-word-length implementations of algorithms, especially in embedded systems. In this section, we will discuss the square root filter, which was developed in order to

---

**159**

effectively increase the numerical precision of the Kalman filter and hence mitigate numerical difficulties in implementations. However, this improved performance is at the cost of greater computational effort. First, we will review the concept of the condition number of a matrix, then we will derive the square root version of the time update equation, and finally we will derive the square root version of the measurement update equations. Section 8.3.3 contains a discussion of square root filtering for the continuous-time Kalman filter.


## 6.3.1 Condition number


*Recall the definition of the singular values of a matrix. An n x n matrix P has n* **singular values o, given as**

*02(P) = X(PTP)* *= X(PPT)* (6.36)

*The matrix PTP is symmetric, and the eigenvalues of a symmetric matrix are* always real and nonnegative, so the singular values of a matrix are always real and nonnegative. The matrix P is nonsingular (invertible) if and only if all of its **singular values are positive. The condition number of a matrix is defined as**

**omax (P)**

omin (P) *.(P)* =

(6.37)

Note that some authors use alternate definitions for condition number; for example, **some authors define the condition number of a matrix as the square of the above** *definiti0n.l As .(P)* *--t 00, the matrix P is said to be poorly conditioned or* *ill conditioned, and P approaches a singular matrix. In the implementation of* a Kalman filter, the error covariance matrix P should always be positive definite 
$$
because P = E[(z - i)(z -
$$
 We use the standard notation

*P>O* (6.38)

*to indicate that P is positive definite. This is equivalent to saying that P is invert-* ible, which is equivalent to saying that all of the eigenvalues of P are greater than zero. But suppose in our Kalman filter that some elements of z are estimated to much greater precision than other elements of z. For example, suppose that

(6.39)

**This means that our estimate of X I  has a standard deviation of lo3 and our estimate** of x2 has a standard deviation of This could be due to drastically different **units in z1 and z2, or it could be simply that z1 is much more observable that**

2 2 .  The singular values of a diagonal matrix are the magnitudes of the diagonal elements, which are lo6 and lo-'. In other words,

*.(P) = 10l2* (6.40)

lIn MATLAB the COND function can be used to find the condition number of a matrix.

---


[Image on page 12]


**160**

This is a pretty large condition number, which means that the P matrix might look like a singular matrix to a digital computer. For example, if we have a fixed- point computer with 10 decimal digits of precision and the lo6 term is represented correctly in the computer, then the term will be represented as a zero in the *computer. Mathematically, P is nonsingular, but computationally P is singular.* *The square root filter is based on the idea of finding an S matrix such that* *P = S p .  The S matrix is then called a square root of P. Note that the definition* 
# of the square root of P is not that P = 9,
 but that P = S p .  Also note that this definition of the matrix square root is not standard. Some books and papers 
# defined the matrix square root as P = 9, others define it as P = P S ,  and others
 
## define it as P = SST. This latter definition is the one that we will use in this book.
 If P is symmetric positive definite then it always has a square root [Go189, MooOO]. The square root of a matrix may not be unique; that is, there may be more than *one solution for S in the equation P = S p .  (This is analogous to the scalar square* root, which is usually not unique. For example, the number 1 has two square roots; f l  and -1.) Also note that S p  will always be symmetric positive semidefinite no *matter what the value of the S matrix. Whereas numerical difficulties might cause* P to become nonsymmetric or indefinite in the Kalman filter equations, numerical difficulties can never cause S p  to become nonsymmetric or indefinite. Matrix square root algorithms were first given by the French military officer An- dre Cholesky (1875-1918) and the Polish astronomer Tadeusz Banachiewicz (1882- 1954) [Fad59]. An interesting biography of Cholesky is given in the appendix of [Mai84]. *The following algorithm computes an S matrix such that P = S p  for an n x n* *matrix P.* 
## The Cholesky Matrix Square Root Algorithm {
 
## For i = l , . - - , n


*For j = l , - . . , n*

*Sji=O* j < i


# sji = & (PJZ
 
# - cklt S j k s i k )
 *j* **i**

{

**1** } } *This is called Cholesky factorization and results in a matrix S such that P =* 
## SST. The matrix S is referred to as the Cholesky triangle because it is a lower
 triangular matrix. However, the algorithm only works if P is symmetric positive definite. If P is not symmetric positive definite, then it may or may not have a square root.2 In the following example we illustrate the application of Cholesky factorization.

**2The MATLAB function CHOL outputs the transpose of the Cholesky triangle that is computed** above.

---

**161**

**1 EXAMPLE63**

**This example is taken from [Kam71]. Suppose we have a P matrix given as**


## The Cholesky factorization algorithm tells us that, for i = 1,


# Sll = 6


# S 2 l  = -
 **( P 2 l )**

= 1 1

**s 1 1** **=** **2**

**=** **3**


## For i = 2, the algorithm tells us that


I **1**

**=** **2**


## s 1 2  = 0


## = -2


## For i = 3, the algorithm tells us that


I **2**


# s 3 3  = 11 P 3 3  - C S &
 **j=1**

**(6.41)**

**(6.42)**

**(6.43)**

**(6.44)**

So we obtain

**S** **=** **2** **2** **Q** **(6.45)** [: **:2** :I


## and it can be verified that P = S p .
 vvv 
## After defining S as the square root of P in the Kalman filter, we will propagate S
 **instead of P .  This requires more computational effort but it doubles the precision**

---


[Image on page 14]


**162**

**of the filter and helps prevent numerical problems. The singular values B of P are** given as


## 2 ( P )  = X(PTP)
 = X(SSTSST) (6.46)

*The singular values of S are given as*


## 2 ( S )  = X(SST)
 (6.47)


## Recall that for a general matrix A we have X(A2) = X2(A). Therefore, we see from
 the above equations that


## 02(P) = [B2(S)I2


**.(P)** 
## = 2 ( S )
 (6.48)

That is, the condition number of P is the square of the condition number of S. For **example, consider the P matrix given earlier in this section:**

0 **10-6** O l 
# p = 1 Io6


L **1** *.(P)* 
## = 10l2


The square root of this matrix and its condition number are

o 10-3 " 1 
# s = [ lo3


*.(S)* 
## = lo6


(6.49)

(6.50)

**The condition number of P is 10l2, but the condition number of the square root** **of P is only lo6. Square root filtering uses this idea to provide twice the precision** *of the standard Kalman filter. Instead of propagating P, we propagate the square* *root of P.*


## 6.3.2
 **The square root timeupdate equation**

**Suppose we have an n-state discrete LTI system given as**


## x k  = Fk-lXk-l+ Gk-iUk-i+ W k - 1
 
## E(WkWT) = Qk
 (6.51)


## The a priori error covariance matrix of the Kalman filter is P;, and its square root
 *is S;. The a posteriori error covariance matrix is Pz, and its square root is S;.* **Suppose that we can find an orthogonal 2n x 2n matrix T such that**

(6.52)

---


[Image on page 15]


**163**

*Since T is orthogonal we see that*

= [: ;]

*where TI and T2 are both n x n matrices. We see from the above that*

(6.53)

(6.54)

Now note that we can use Equation (6.52) to write

We can use this equation, along with Equation (6.54), to write

*If St-, is the square root of Pkfl, this implies that*

*which is exactly the timeupdate equation for Pk that is required in the Kalman* *filter, as shown in Equation (5.19). So if we can find an orthogonal 2n x 2n matrix* *T such that*

(6.58)

*then the n x n matrix in the upper half of the matrix on the right side is equal* *to ( S i ) T .  This assumes that (Sz-l)T is available from a square root measure-* ment update equation, which we will discuss in the following two subsections. The square root time update equation above is mathematically equivalent to the origi- *nal Kalman filter time update equation for P, but the update equation is used to* *update S instead of P.* **As we noted above, the square root of Pi is not unique, so different algorithms** **for solving Equation (6.58) will result in different T and (S;)T matrices. We can use** *various methods from numerical linear algebra to find the orthogonal 2n x 2n matrix* *T and the resulting square root matrix S i  (e.g., Householder, Gram-Schmidt,* modified Gram-Schmidt, or Givens transformations) [Hor85, Gol89, Str90, MooOO]. A couple of these algorithms are discussed in Section 6.3.5.

---

**164**

**EXAMPLE6.4**


# Suppose that at time (k - 1) our Kalman filter has a system matrix, process
 *noise covariance, and a posteriori estimation covariance square root equal to*

**(6.59)**


## It can be verified that the square root of Qk-l (so that Qk/_”1Qr!; = Qk-l)
 is given by


# Q:/_2, = [
 ] **(6.60)**

**Equation (6.58) can be solved as**

**As mentioned earlier, algorithms for performing this computation will be dis-** **cussed in Section 6.3.5. The upper-right square matrix on the right side of** 
## the above equation is equal to (Si)=, so this shows that the square root of
 
## the a priori estimation covariance at time k is given as


**(6.62)**

**From this it can be inferred that the a priori estimation covariance at time k** **is given as**

*PL = S,-(S,-)T*


$$
= [:,:I
$$
 **(6.63)**

Indeed, a straightforward implementation of the timeupdate equation for the estimation-error covariance gives


$$
= [:: :I
$$
 **(6.64)**

which confirms our square root results. However, the square root time update has essentially twice the precision of the standard time-update equation. vvv

---

**165**

**6.3.3**

The square root measurement-update equation discussed here is based on James Potter's algorithm, which was developed for NASA's Apollo space program [Bat64, Kam7lI and modified by Angus Andrews to handle vector measurements [And68]. Recall from Equation (5.19) that the measurement update equation for the estima- **tion covariance is given as**


## Pk+ = ( I  - KkHk)PF
 (6.65)

We can process the measurements one at a time using the sequential Kalman filter 
## of Section 6.1. That is, first we initialize Pofk = PL. Then, for i = l , . . . , ~
 (where


## T is the number of measurements), we compute


**Potter's square root measurement-update equation**


## p& = ( I  - KikHik)PLl,k
 (6.66)

**where Hik is the ith row of Hk and Rik is the variance of the ith measurement.** **(We are assuming here, as in Section 6.1, that Rk is diagonal.) suppose we have** 
## the square root of Pz+-l,k so that P:,,, = s:l,ks:;,k.
 **Then Kik can be written** **a5**

(6.67)

**and P$ can be written as**

where $ and a are defined as

(6.69)

It can be shown (see Problem 6.9) that


# I - a$+T = ( I  - ay$$T)2
 (6.70)

where y is given as **1** (6.71)

Either the plus or minus sign can be used in the computation of y. Comparing Equations (6.68) and (6.70) shows that


# s.ik + -
 - s+ 
# i - l , k ( I  - ay$4T)
 (6.72)

This results in a square root measurement-update algorithm that can be summa- rized as follows.

---


[Image on page 18]


**166**

**Potter's square root measurement-update algorithm**

*1. After the a priori covariance square root S i  and the a priori state estimate* 
## 2 i  have been computed, initialize


## 2& = 2;


**s:k** *= s i* (6.73)


# 2. For i = 1, . . , r (where r is the number of measurements), perform the fol-
 lowing.

**Define H i k  as the ith row of H k ,  y i k  as the ith element of Y k ,  and R i k** **as the variance of the ith measurement (assuming that R k  is diagonal).** Perform the following to fmd the square root of the covariance after the ith measurement has been processed:


## 4i = s,'-?;,kHz'k
 1 
# @4i + R i k
 *a, =*

**1** l k d a i 
## Ti =
 *s;* *= s+* 
# i- 1,k (I -
 **$i dT)**

Compute the Kalman gain for the ith measurement

(6.74)

as

(6.75)

Compute the state estimate update due to the ith measurement as

**x i k** -+ - 
# - x , - l , k
 -+ 
# + K i k ( Y i k  - Hikf:-l,k)
 (6.76)

**3. Set the a posteriori covariance square root and the a posteriori state estimate** as *sk+ = s+* **r k** **2;** 
## = ':k
 (6.77)

Although square root filtering improves the numerical characteristics of the Kalman filter, it also increases computational requirements. Efforts to make square root filtering more efficient are reported in [Car73, Tho77, Tap801.

**EXAMPLE6.5**

This example is based on [Kam71]. Suppose that we have an LTI system with


# pi- = [; ;]


**H** = [ l  0 1

= [: :] (6.78)

---

**167**

*If we had an infiniteprecision computer, the exact Kalman gain and a poste-* **riori covariance at time k would be given by**

*Kk* *= P p T ( H P p T  4- R)-l*

(6.79)

**L**


# The a priori covariance and Kalman gain at the next time step (k + 1) would
 be given by

*Pr+l = FPk+FT+Q*

- - [+I (6.80)

Now consider implementation in a finite precision digital computer. Suppose *that the measurement covariance R << 1. The covariance R is such a tiny* *number that because of rounding in the computer, 1 + R = 1, but 1 + a>* 1. **The rounded values of the Kalman gain and. a posteriori covariance at time k** would be given by

(6.81)

*Note that Pkf has become singular because of the numerical limitations of the* *computer. The rounded values of the a priori covariance and Kalman gain at* 
# the next time step (k + 1) would be given by


*PF+l = F P I F T + Q*


$$
= [;I
$$
 (6.82)

The numerical limitations of the computer have resulted in a zero Kalman **gain, whereas the infiniteprecision Kalman gain as given in Equation (6.80)** is about [ 1/2 0 1'.

---


[Image on page 20]


**168**

Now suppose we implement the measurement-update equation using Pot- ter’s algorithm. We start out with

1 0 S L = [ o  11 (6.83)

We only have to iterate through Equation (6.74) one time since we only have one measurement. The rounded values of the parameters given in Equa- tion (6.74) are

*a* *=*

*(SF)THT*

1 
# dTd + R
 1 l + R 1 **1**

1 1+m

1+dX 
# s,- (1 - [+ ;]
 (6.84)

*Note that SzScT is nonsingular. The rounded values of the square root of* *the a priori covariance, the parameters of Equation (6.74), and the Kalman* 
# gain at the next time step (k + 1) would be given by


**%+l** = **d** **=**

*a* *=*

**L** **J** 1 
# dTd + R
 1 + R + 2 & *R2 + 2R i- 2 R a* 1 + 2 & 2R + 2R@ 
## as,, 14
 **R** +2fl [ 1+R;2Jfi ] *2R(1 +a)* [*I (6.85)

---

**169**

Note that the rounded Kalman gain is almost identical to the exact Kalman gain given by Equation (6.80). This shows the benefit that can be gained by using the square root filter. vvv

**6.3.4** **Square root measurement update via triangularization**

The previous section derived a measurement update based on Potter's algorithm that could be performed on the square root of the Kalman filter estimation covari- ance. This section derives an alternative method for performing the measurement update. Suppose that we want to design a Kalman filter for a system with n states *and r measurements. Suppose that we can find an orthogonal matrix (n+r) x (n+r)* *matrix rif such that*

*S; and S,'* *are the square roots of the a priori and a posteriori covariances, and* **kk is defined as** 
# Kk = Kk(Rk + HkPFHT)T/2
 (6.87)


## where Kk is the normal Kalman gain matrix. Note that Sk+ in Equation (6.86) is not
 known until after an orthogonal is found that forces the left side of Equation (6.86) *into the specified form. That is, we need to find a 5? so that the upper-left r x r block* 
# of the left side of Equation (6.86) is equal to (Rk + HkPLH?)T/2, the upper-right
 *r x n block is equal to k;,* *and the lower-left n x r block is equal to 0. After such* a is found, whatever the lower right n x n block turns out to be is, by definition, *equal to (S,')',* **which is the transpose of the square root of P z .  Now write the** 
# (n + r )  x (n + r )  matrix F as


(6.88)


## where 5?11 is an r x r matrix, 5?12 is an r x n matrix, T21 is an n x r matrix, and
 
## p22 is an n x n matrix. Since 5? is orthogonal we can write


= [; ;]

**Now we expand Equation (6.86) as**

(6.89)

(6.90)

---


[Image on page 22]


**170**

We will equate the four matrix partitions of this equation to write four separate equalities. We will then take each equality and premultiply each side by its trans- pose to obtain four new equalities. The first two equalities obtained this way are


# (Rk + HkP;Hr)1/2(. -
 =


## 1/2pT p R T / ~  + iyks- PT p
 
## TI2 +
 **Rk** **11 11 k** **k** **12 l l R k** **R ~ / ~ F T F** **T** **T** **T** **T** **11 12(si) Hk +Hksi5%F12(si)** **Hk** 
# 1'2pTp RT12 + R:/2?!?22(Si) T
 **T** 
# Hk +


# Hksip&p21RT/2 + H k s ~ p & ~ 2 2 ( s i )
 **T** **T** **Hk** 
## = Rk
 **21 21** **k**

(6.91)

Adding these two equations and using Equations (6.87) and (6.89) to simplify the result gives 
# Rk 4- HkPFHr = Rk + H k s i  ( s i ) T H T
 (6.92) This shows that the proposed measurement update of Equation (6.86) is consistent 
## with S i  being the square root of P;.
 The second two equalities that can be written from Equation (6.90) are

**r?kl?r** 
## = siFg!f12(Si)T


*S,'(S,')'* 
## = S,-F&T22(Si)T
 (6.93)

Adding these two equations and using Equation (6.89) to simplify the result gives 
# S,'(s,')' f Kk(Rk + HkP;Hr)Kr = si(&)T
 (6.94)


# Substituting the standard Kalman gain equation Kk = P;HT(Rk + HkP;Hr)-l
 into this equation gives ~k+(skf)~ 
# + P;H,TK,T
 = 
## s,'(s,')~ = P-
 
## k - P - H ~ K ~
 **k** **k** **k** (6.95)

Since the left side of the above equation is symmetric and the first term on the right side is symmetric, the last term on the right side must also be symmetric, which means that we can transpose it in the above equation to obtain

*S,'(s,')'* 
# = P i  - KkHkp;
 (6.96)

The right side of this equation is the Kalman filter measurement-update equation **for P ,  which means that the left side of the equation must be P z ,  which means that** *S,'* 
# must be the square root of Pz. So if we can find an orthogonal (n + r )  x (n + r )
 
## matrix p such that


*then the lower-right n x n matrix on the left side of the equation is equal to the* **transpose of the square root of Pk+, and this equation is mathematically equiv-** **alent to the original Kalman filter measurement-update equation for Pk. This** measurement-update method results in numerical precision that is effectively twice **as much as the standard Kalman filter, which helps to avoid numerical problems.** However, the computation of? adds a lot of computational effort to the Kalman filter. In addition, the form of the transformation given in Equation (6.97) makes it of questionable practicality (see Problem 6.10).

---

171

**6.3.5**

Several numerical algorithms are available for performing the orthogonal transfor- *mations that are required to solve for the T and S;* matrices in Equation (6.58). Some algorithms that can be used are the Householder method, the Givens method, the Gram-Schmidt method, and the modified Gram-Schmidt method. In this section we will present (without derivation) the Householder algorithm and the modified Gram-Schmidt algorithm. Derivations and presentations of the other al- **gorithms can be found in many texts on numerical linear algebra, such as [Hor85,** **Go189, MooOO]. A comparison of Gram-Schmidt, modified Gram-Schmidt, and** Householder transformations can be found in [Jor68], where it is stated that the modified Gram-Schmidt procedure is best (from a numerical point of view), with the Householder method offering competitive performance.


## Algorithms for ort hogona I transformations


## 6.3.5.1 The Householder algorithm The algorithm presented here was developed
 by Alston Householder [Hou64, Chapter 51, applied to least squares estimation by Gene Golub [Go165], and summarized for Kalman filtering by Paul Kamin- ski [Kam7l].


## 1. Suppose that we have a 2n x n matrix A(1), and we want to find an n x n


(6.98)

*where T is an orthogonal 2n x 2n matrix, and 0 is the n x n matrix consisting* of all zeros. Note that this problem statement is in the same form as Equa- **tion (6.58). Also note that we do not necessarily need to find T ;  our goal is** *to find W .*


## 2. For k = 1, . . . , n perform the following:


**(a) Compute the scalar Uk as**

(6.99)

**where A!:) is the element in the ith row and kth column of A(k). The** sgn(.) function is defined to be equal to $1 if its argument is greater than or equal to zero, and -1 if its argument is less than zero.

**(b) Compute the scalar ,& as**


## (c) For i = 1, * ,2n perform the following:


(6.100)

(6.101)

---


[Image on page 24]


**172**

This gives a 2n-element column vector ~ ( ~ 1 . 
## (d) For i = 1, . , n perform the following:


i < k 
## y y  =
 1 i = k (6.102) 
## { O  &U(k)TAl(k) i > k


**where A(k) is the ith column of A(k). This gives an n-element column** vector &I. *(e) Compute the 2n x n matrix* as


# A(k+fl) = A(k) - u(k)y(k)T
 (6.103)

**3. After the above steps have been executed, A("+1) has the form**

(6.104)


## where W is the n x n matrix that we are trying to solve for. Note that if


## b k  = 0 at any stage of the algorithm, that means A(1) is rank deficient and
 the algorithm will fail. Also note that the above algorithm does not compute *the T matrix. However, we can find the T matrix as*


## 6.3.5.2 The modified Gram-Schmidt algorithm The modified Gram-Schmidt al-
 gorithm for orthonormalization that is presented here is discussed in most linear **systems books [Kai80, Bay99, Che991. It was first given in [Bjo67] and was sum-** marized for Kalman filtering in [Kam7l].


## Suppose that we have a 2n x n matrix A(1), and we want to find an n x n
 **matrix W such that** 
# TA(l) = [ y ]
 (6.106)

*where T is an orthogonal 2n x 2n matrix, and 0 is the n x n matrix con-* sisting of all zeros. Note that this problem statement is in the same form as Equation (6.58).

For k = 1, 
## a . a ,  n perform the following.


**(a) Compute the scalar b k  as**

**where A!k) is the ith column of A(')).** **(b) Compute the kth row of W as**

(6.107)

(6.108)

---

**173**

**(c) Compute the kth row of T as**


# (d) If (k < n), compute the last (n - k) columns of
 as

(6.109)

(6.110)

**Note that the first k columns of** rithm. are not computed in this algo-


## As with the Householder algorithm, if Uk = 0 at any stage of the algorithm, that
 means A(1) is rank deficient and the algorithm fails. After this algorithm completes, 
## we have the first n rows of T ,  and T is an n x 2n matrix. If we want to know the
 **last n rows of T ,  we can compute them using a regular Gram-Schmidt algorithm** **as follows [Hor85, Go189, MooOO].**


## 1. Fill out the T matrix that was begun above by appending a 2n x 2n identity
 **matrix to the bottom of it. This ensures that the rows of T span the entire** 2n-dimensional vector space:


# T =  [ TI
 (6.111)


## Note that this T is a 3n x 2n matrix.


2. Now we perform a standard Gram-Schmidt orthonormalization procedure on 
## the last 2n rows of T (with respect to the already obtained first n rows of T ) .
 
# For k = n + 1,. ., 3n, compute the kth row of T as


**k - 1**

**2=1**

(6.112)

**If Tk is zero then that means that it is a linear combination of the previous** **rows of T .  In that case, the division in the above equation will be a divide** **by zero, so instead Tk should be discarded. This discard will actually occur** 
## exactly n times so that this procedure will compute n additional rows of T
 
## and we will end up with an orthogonal 2n x 2n matrix T .


The Gram-Schmidt algorithms are named after the Danish mathematician Jor- gen Gram (1850-1916) and the German mathematician Erhard Schmidt (1876- 1959). Schmidt received his doctorate in 1905 under David Hilbert’s supervision, and in 1929 he was on the doctoral committee of Eberhard Hopf (see Section 3.4.4). However, the Gram-Schmidt algorithm was actually invented by Pierre Laplace (1749-1827).

---


[Image on page 26]


174

**6.4** 
## U-D FILTERING


**U-D filtering was introduced in [Bie76, Bie77al as another way to increase the** numerical precision of the Kalman filter. It is sometimes considered as a type of square root filtering, and sometimes it is considered distinct from square root filtering (depending on the author). It increases the computational cost of the filter but not so severely as the square root filter of the previous section. **The idea of U-D filtering is to factor the n x n matrix P as UDUT, where U is** 
## an n x n upper triangular matrix with ones along the diagonal, and D is an n x n
 **diagonal matrix. This can always be accomplished for a symmetric positive definite** 
## matrix P [Go189, Chapter 41, so it can always be implemented on a Kalman filter.
 **A U-D factorization routine can be implemented without too much difficulty. For** example, suppose that we want to compute the U-D factorization of a 3 x 3 matrix. We can then write

**P l l** **P l 2** **P13** **1 u12** 0 0 0 
# [ P12
 **P22** **P 2 3 ]** = [ 
# p:] [ d f
 **$2** 
# [ ii i3 :]
 **P13** **P23** **P33**


# d22 + d 3 3 4 3
 **d33U23** (6.113) **1** =[ **d33u13** **d33U23** **d33**


# d l l  + d22'42 + d33uq3
 
# d22u12 + d33U13u23
 **d33U13**


# d22u12 + d33u13u23


**We need to solve for the u a j  and d i i  elements. We can begin at the lower-right** 
## element of the matrix equality to see that d33 = p33. Next we can look at the other
 elements in the third column to see that


## u13 = p 1 3 / d 3 3


**2123** 
## = p 2 3 / d 3 3


Now look at the (2,2) and (1,2) elements of the equality to see that


# d22 = P22 - d 3 3 4 3


## u12 =
 
# (P12 - d33u13u23)/d22


Finally look at the (1,l) element of the equality to see that

(6.114)

(6.115)


# dii = pi1 - d22& - d33&
 **(6.11 6)**

This gives us the U-D factorization for a 3 x 3 symmetric matrix, and provides the outline for a general U-D factorization algorithm.

**6.4.1**

Recall from Equation (5.19) the measurement update equation for the covariance of the Kalman filter:


# P f  = P- - P-H*(HP-HT + R)-lHP-
 (6.11 7)

We have omitted the time subscripts for ease of notation. Now suppose that we **process the measurements sequentially as discussed in Section 6.1. This gives the** equation 
# P, = Pa-1 - Pt-1H,T(HaPa-1H,T + ~ a ) - ' ~ a & - l
 (6.118)


## U-D filtering: The measurement-update equation


---

**175**

**where H, is the ith row of H ,  R, is the ith diagonal entry of R, and Pz is the esti-** mation covariance after i measurements have been processed. Now define the scalar 
# ai z H,P,-lH? + R,. Suppose that P,-1 = U,-lDi-lUzl, and P, = U,DiU,'.
 With these factorizations we can write the measurement update of Equation (6.118) as 1

ffi *U, Di U,'* *= U,- 1 Di- 1 U z  - -* 
## U,- 1 Dg- 1 U z  1 HT Hi U,- 1 Di- 1 U z


1 1 1 *= U,-l Di-1 - -(Di-lU~,H,T)(Di-1U2T_1HT* uL1(6.119)

The term in brackets in the above equation is symmetric positive definite so it has **a U-D factorization that can be written as** [ ffi

(6.120) 1

**1** - - - *UDUT = Di-1- -* *(Di- 1 U,T_ H,T) (Di- 1 U,T_ H,T)T* [ ffi

Combining this with Equation (6.119) gives

*U,DiU,'* *= U,-lUDUTU.,* *= (U,- 10)b (V,- 1 O)T* (6.121)

**Note that U,-10 is upper triangular with diagonal elements equal to 1, and b is** 
## diagonal. Therefore the above equation means that U, = Ua-lu, and Di = D:
 
$$
u, = u,-J
$$
 *Di = D* (6.122)

**This gives us a way of performing the measurement update of P in terms of its U-D** factors. The algorithm can be summarized as follows.


## The U-D measurement update


## We start with the a priori estimation covariance P- at time k. Define Po =
 *P- .*

For i = 1,. . **e** **,** 
## T (where T is the number of measurements), perform the fol-
 lowing:

*(a) Define H, as the ith row of H ,  R, as the ith diagonal entry of R, and*

*(b) Perform a U-D factorization of Pi-1 to obtain U,-l and Di-1, and then*

**(c) Find the U-D factorization of the matrix on the right side of Equa-**

*(d) Compute U, and Di from Equation (6.122).*

*= H,Pi-iH,T + R,.*

form the matrix on the right side of Equation (6.120).


## tion (6.120) and call the factors U and 0.


## The a posteriori estimation covariance is given as P+ = U,D,U,'.


Since the U-D measurement-update equation relies on sequential filtering, the con- ditions discussed at the end of Section 6.1 apply to U-D filtering. That is, it proba- bly does not make sense to implement U-D filtering unless one of the following two conditions is true.

---


[Image on page 28]


176

**1. The measurement noise covariance Rk is diagonal**

**2. The measurement noise covariance R is a constant.**


## 6.4.2


Recall from Equation (5.19) the time-update equation for the covariance of the Kalman filter: *P- = FP'F'* *+ Q* (6.123)

We have omitted the time subscripts for ease of notation. If the Kalman filter is being used to estimate the state of an n-state system, then the P matrices will be 
## n x n matrices. Suppose that P+ is factored as U+D+U+'
 (from the measurement *update equation discussed previously). We need to find the U-D factors of P- such* *that P- = U-D-U-'* *= FP+FT + Q. Note that U-'* in this notation is not the **transpose of the inverse of U ;** *it is rather the transpose of U-. The time update of* **Equation (6.123) can be written as**


## U-D filtering: The timeupdate equation


*P-* *= FP+F'+Q*


$$
= WDW'
$$
 (6.124)

*where W and D are defined by the above equation. Note that W is an n x 2n* 
## matrix, and fi is a 2n x 2n matrix. From the above equation we see that the U-D
 *factors of P- need to satisfy*

*U-D-U-'* *= WDWT* (6.125)

*The transpose of W can be written as* 
$$
w'=[ wy
$$
 
## . * *  w,T]
 (6.126)

**That is, wi (a 2n-element row vector) is the ith row of W .  Now we find n vectors** vi such that


## VkDVT = 0
 **k # j** (6.127)

The vi vectors (2n-element row vectors) can be found with the following Gram- Schmidt orthogonalization procedure [Hor85, Go189, MooOO]:


## vn = W n


**If we define u(k, j )  as**

(6.129)

---

**177**

then from Equation (6.128) we see that Wk can be expressed as

or equivalently n

(6.130)

(6.131) j = k + l These n equations can be written as


$$
w = u-v
$$
 (6.132)

*The n x 2n matrix W ,  the n x n matrix U-, and the n x 2n matrix V are defined by* *the above equation. Note that U -  is a unit upper triangular matrix. The matrix* **product WDWT can then be written as**

*WbWT = (u-v)Ij(u-v)T* *= u-(vIjvT)u-T* *= U-D-U-T* (6.133)

**where the D- matrix is defined by the above equation. From Equation (6.127),** **we see that the vi vectors are orthogonal with respect to the b inner product. We** therefore know that

*D-* *= VbVT = diag(d1, - -, dn)* dk = VkDV: (6.134)

**That is, D- is a diagonal matrix. From Equations (6.124), (6.125), and (6.133)** **we see that U- and D- satisfy the conditions of being the U-D factors of P-.** This gives us a way to perform the Kalman filter time-update equation in U-D factorization form. The algorithm can be summarized as follows.


## The U-D time update


*1. Begin with P+ = U+D+UST (from the measurement update equation).*

2. Define the following matrices.


## W = [ F U +  I ]
 *D+* 0 D = [ o Q I (6.135)

*3. Use the rows of W along with the Gram-Schmidt orthogonalization procedure* *to generate vi vectors that are orthogonal with respect to the D inner product.* The algorithm for generating the vi vectors is given in Equation (6.128).

---

**178**

**4. Form the V matrix using the wi vectors as rows; see Equation (6.132).**


## 5. Use D inner products to form the unit upper triangular matrix U-;
 see Equa- tions (6.129) and (6.132).


## 6. Define D- as D- = V b v .


**The U-D filter results in twice as much precision as the standard Kalman filter,** just like the square root filter, but it requires less computation than the square root filter. If some of the states are missing from the measurement vector, a more efficient U-D algorithm can be derived [Bar83].

**6.5** 
## SUMMARY


In this chapter, we discussed the sequential Kalman filter, which is mathematically identical to the Kalman filter, but which avoids matrix inversion. This is an attrac- tive formulation for embedded systems in which computational time and memory are at a premium. However, sequential filtering can only be used if the noise co- variance is diagonal, or if the noise covariance is constant. Information filtering is also equivalent to the Kalman filter, but it propagates the inverse of the covariance. This can be computationally beneficial in cases in which the number of measure ments is much larger than the number of states. Square root filtering and U-D filtering effectively increase the precision of the Kalman filter. Although these ap- proaches require additional computational effort, they can help prevent divergence and instability. Gerald Bierman’s book provides an excellent and comprehensive overview of square root and U-D filtering [Bie77b]. We see that we have a number of different choices when implementing a Kalman filter.


## 0 Covariance filtering or information filtering


## 0 Standard filtering, square root filtering, or U-D filtering


## 0 Batch filtering or sequential filtering


Any of these choices can be made independently of the other choices. For instance, we can choose to combine information filtering with square root filtering [Kam7l] **in much the same way as we combined covariance filtering with square root filtering** in this chapter. The choices in the list above gives us a total of 12 different Kalman filter formulations (two choices in the first item, three choices in the second item, and two choices in the third item). There are also other choices that are not listed **above, especially other types of square root filtering. A numerical comparison** of various Kalman filter formulations (including the standard filter, the square root covariance filter, the square root information filter, and the Chandrasekhar algorithm) is given in [Ver86]. Numerical and computational comparisons of various Kalman filtering approaches are given in [Bie73, Bie77al. Continuous-time square root filtering is discussed in [Mor78] and in Section 8.3.3 of this book.

---


[Image on page 31]


**179**

PROBLEMS

**Written exercises**

**6.1 In this chapter, we discussed alternatives to the standard Kalman filter for-** mulation. Some of these alternatives include the sequential Kalman filter, the information filter, and the square root filter. What is the advantage of the sequential Kalman filter over the batch Kalman filter? What is the advantage of the batch Kalman filter over the sequential Kalman filter? What is the advantage of the information filter over the standard Kalman filter? What is the advantage of the standard Kalman filter over the information filter? What is the advantage of the square root filter over the standard Kalman filter? What is an advantage of the standard Kalman filter over the square root Kalman filter?

**6.2** surement noise covariance matrices Suppose that you have a system with the following measurement and mea-


$$
= [: :I
$$


You want to use a sequential Kalman filter to estimate the state of the system. Derive the normalized measurement, measurement matrix, and measurement noise covariance matrix that could be used in a sequential Kalman filter.

**6.3 Consider the two alternative forms for the information matrix time-update** **equation. What advantages does Equation (6.28) have? What advantages does** Equation (6.30) have?

**6.4** **A radioactive mass has a half-life of 7 seconds. At each time step k the** **number of emitted particles 2 is half of what it was one time step ago, but there** **is some error wk (zero-mean with variance Q k )  in the number of emitted particles** due to background radiation. At each time step the number of emitted particles is counted with two separate and independent instruments. The instruments used to count the number of emitted particles both have a random error at each time step that is zero-mean with a unity variance. The initial uncertainty in the number of radioactive particles is a random variable with zero mean and unity variance. The discrete-time equations that model this system have a one-dimensional state and a two-dimensional measurement. Use the information filter to 
## compute the a priori and a posteriori information matrix at k = 1 and
 
## k = 2. Assume that QO = 1 and Q1 = 5/4.
 Another way to solve this problem is to realize that the two measurements can be averaged to form a single measurement with a smaller variance than the two independent measurements. What is the variance of the averaged measurement at each time step? Use the standard Kalman filter equations

---


[Image on page 32]


180


## to compute the a priori and a posteriori covariance matrix at k = 1 and
 
## k = 2, and verify that it is the inverse of the information matrix that you
 computed in 'part (a).

Prove that the singular values of a diagonal matrix are the magnitudes of the

Prove that S p  is symmetric positive semidefinite for any S matrix.

Find an upper triangular matrix S (using only paper and pencil) such that

**6.5** diagonal elements.

**6.6**

**6.7**

Is your solution unique?

**6.8 Find an upper triangular matrix S (using only paper and pencil) such that**


## S F = [  5 2
 **2 2 -2 -;I**

**-2** -1

How many solutions exist to this problem?

**6.9 Verify Equation (6.70). Hint: Equate the two sides of the equation, take the** trace, and solve for y. Make sure to explain why taking the trace is valid.

**6.10** 
## ~ Suppose that an orthogonal matrix p is desired to satisfy Equation (6.97),
 where Cholesky factorization is used to compute the matrix square roots on the left 
## side of the equation. This equation can then be written as U = PA, where U is an
 upper triangular matrix. Show that such a transformation cannot be found unless **the two-norm of the first column of A happens to be equal to IUlll. [Note that this** does not necessarily prevent the possibility of the transformation of Equation (6.97), **because U could be nontriangular if nontriangular square root matrices are used to** **form the U matrix.]**

**6.11 Use the Householder method (using only paper and pencil) to find an or-**


# thogonal T such that T A  = [ :
 
# ] where W is a 2 x 2 matrix and


**6.12** solve Problem 6.11.

**6.13**

Use the modified Gram-Schmidt method (using only paper and pencil) to

Compute the U-D factorization (using only paper and pencil) for the matrix

---


[Image on page 33]


**181**

**Computer exercises**


## 6.14 Consider the RLC circuit of Example 1.8 with R = 100 and L = C = 1.
 Suppose the applied voltage is continuous-time, zero-mean white noise with a stan- **dard deviation of 3. The initial capacitor voltage and inductor current are both** zero. Discretize the system with a time step of 0.1. The discretetime measure ments consist of the capacitor voltage and the inductor current, both measurements containing zero-mean unity variance noise. Implement a sequential Kalman filter for the system. Simulate the system for 2 seconds. Let the initial state estimate be equal to the initial state, and the initial estimation covariance be equal to 0.11. *Hint: Set the discretetime process noise covariance Q = QcAt, where Qc is the co-* *variance of the continuoustime process noise, and At is the discretization step size.* Q will be nondiagonal, which means you need to use the algorithm in Section 2.7 to simulate the process noise. **a) Generate a plot showing the a priori variance of the capacitor voltage** *estimation error, and the two a posteriori variances of the capacitor voltage* estimation error. **b) Generate a plot showing a typical trace of the true, a posteriori estimated,** and measured capacitor voltage. What is the standard deviation of the capacitor voltage measurement error? What is the standard deviation of the capacitor voltage estimation error?

The pitch motion of an aircraft flying at constant speed can be approxi- **6.15** mately described by the following equations [Ste94] :

-0.5680 17.9800 0.1750 *0.1750 ] u +  [ 17.9800 ]* 
# 1.0000 -1.2370 ] 2 +  [ -0.0010
 -0.0010 -1.2370 x = [


## Y ( t k )  = z ( t k )  -k uk


**where 51 is the pitch rate, 5 2  is the angle of attack, u consists of the elevator and** flap angles, and w is disturbance due to wind. Suppose that the variance of the wind **disturbance is 0.001, and the measurement variances are 0.3. Discretize the system** with a step size of 0.01 and simulate the system and a square root Kalman filter for 100 time steps. Use an initial state of zero, an initial state estimate of zero, an initial estimation-error covariance of 0.011, and a control input of zero. Hint: Set *the discretetime process noise covariance Q = QcAt, where Qc is the covariance of* *the continuous-time process noise, and At is the discretization step size. Q will be* nondiagonal, which means you need to use the algorithm in Section 2.7 to simulate the process noise. **a) Generate a plot showing the a posteriori variance of the estimation errors** of the two states. *b) Generate a plot showing a typical trace of the true, a posteriori estimated,* and measured pitch rate. What is the standard deviation of the pitch rate measurement error? What is the standard deviation of the pitch rate estimation error?


## c) Generate a plot showing a typical trace of the true, a posteriori estimated,
 and measured angle of attack. What is the standard deviation of the angle of attack measurement error? What is the standard deviation of the angle of attack estimation error?