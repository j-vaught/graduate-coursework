---
type: chapter
chapter: 11
title: The H∞ filter
---

[Image on page 1]


# CHAPTER 11


The H, filter

[Kalman filtering] assumes that the message generating process has a known dynamics and that the exogenous inputs have known statistical properties. Unfortunately, these assumptions limit the utility of minimum variance estimators in situations where the message model and/or the noise descriptions are unknown. -Uri Shaked and Yahali Theodor [Sha92]

As we have seen in earlier chapters, the Kalman filter is an effective tool for estimating the states of a system. The early success in the 1960s of the Kalman filter in aerospace applications led to attempts to apply it to more common industrial applications in the 1970s. However, these attempts quickly made it clear that a serious mismatch existed between the underlying assumptions of Kalman filters and **industrial state estimation problems. Accurate system models are not as readily** available for industrial problems. The government spent millions of dollars on the space program in the 1960s (hence the accurate system models), but industry rarely has millions of dollars to spend on engineering problems (hence the inaccurate system models). In addition, engineers rarely understand the statistical nature of the noise processes that impinge on industrial processes. After a decade or *so of reappraising the nature and role of Kalman filters, engineers realized they* needed a new filter that could handle modeling errors and noise uncertainty. State estimators that can tolerate such uncertainty are called robust. Although robust

**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 @ZOOS John Wiley & Sons, Inc.** **333**

---


[Image on page 2]


**334**

**estimators based on Kalman filter theory can be designed (as seen in Section 10.4),** these approaches are somewhat ad-hoc in that they attempt to modify an already existing approach. The H, filter was specifically designed for robustness. In Section 11.1 we derive a different form of the Kalman filter and discuss the limitations of the Kalman filter. Section 11.2 discusses constrained optimization using Lagrange multipliers, which we will need later for our derivation of the H, filter. In Section 11.3 we use a game theory approach to derive the discretetime H, filter, which minimizes the worst-case estimation error. This is in contrast to the Kalman filter's minimization of the expected value of the variance of the estimation error. Furthermore, the H, filter does not make any assumptions about the statistics of the process and measurement noise (although this information can be used in the H, filter if it is available). Section 11.4 presents the continuous-time H, filter, and Section 11.5 discusses an alternative method for deriving the H, filter using a transfer function approach.


## 11.1 INTRODUCTION


In this section we will first derive an alternate form for the Kalman filter. We do this to facilitate comparisons that we will make later in this chapter between the Kalman and H, filters. After we derive an alternate Kalman filter form, we will briefly discuss the limitations of the Kalman filter.

**11.1.1**

Recall that the Kalman filter estimates the state of a linear dynamic system defined by the equations

**An alternate form for the Kalman filter**

(11.1)

**where {wk} and { V k }  are stochastic processes with covariances Qk and Rk, respec-** **tively. As derived in Section 5.1, the Kalman filter equations are given as follows:**

(11.2)

Using the matrix inversion lemma from Section 1.1.2 we see that

**where Zk is the information matrix (i.e., the inverse of the covariance matrix Pk).** The Kalman gain can therefore be written as follows:

---

**335**

---


[Image on page 4]


**336**

From Equation (11.4) the Kalman gain can be written as


# Kk = (I + PLHTRk1Hk)-'PiH:Rk1
 (11.9)


## We can premultiply outside the parentheses by PL , and postmultiply each term
 **inside the parenthesis by Pi, to obtain**


## Kk = PL(PL f P~HTR~,'HI,PL)-'P,-HTR,~ (11.10)


**We can postmultiply outside the parentheses by the inverse of Pi,** and premultiply **each term inside the parentheses by the inverse of P;, to obtain**


# Kk = Pi(I + HTRk'HkPF)-lHTR-l
 **k** **k** (11.11)

**Combining this expression for Kk with Equations (11.2) and (11.8) we can summa-** rize the Kalman filter as follows:

(1 1.12)

**11.1.2** **Kalman filter limitations**

The Kalman filter works well, but only under certain conditions.

**First, we need to know the mean and correlation of the noise Wk and v k  at** each time instant.

**Second, we need to know the covariances Qk and Rk of the noise processes.** **The Kalman filter uses Qk and Rk as design parameters, so if we do not know** **QI,** **and RI,** then it may be difficult to successfully use a Kalman filter.

Third, the attractiveness of the Kalman filter lies in the fact that it is the one estimator that results in the smallest possible standard deviation of the esti- mation error. That is, the Kalman filter is the minimum variance estimator if the noise is Gaussian, and it is the linear minimum variance estimator if the noise is not Gaussian. If we desire to minimize a different cost function (such as the worst-case estimation error) then the Kalman filter may not accomplish our objectives.


## 0 Finally, we need to know the system model matrices Fk and Hk.


So what do we do if one of the Kalman filter assumptions is not satisfied? What should we do if we do not have any information about the noise statistics? What should we do if we want to minimize the worst-case estimation error rather than the covariance of the estimation error? Perhaps we could just use the Kalman filter anyway, even though its assumptions are not satisfied, and hope for the best. That is a common solution to our Kalman filter quandary and it works reasonably well in many cases. However, there is yet another option that we will explore in this chapter: the H, filter, also called the minimax filter. The H, filter does not make any assumptions about the noise, and it minimizes the worst-case estimation error (hence the term minimax).

---

**337**


## 1 1.2 CO N ST R A I N ED 0
 
## PTI M I 2 AT1 0 N


In this section we show how constrained optimization can be performed through the use of Lagrange multipliers. This background is required for the solution of the H, filtering problem that is presented in Section 11.3. In Section 11.2.1 we will investigate static problems (i.e., problems in which the independent variables are constant). In Section 11.2.2 we will take a brief segue to look at problems with inequality constraints. In Section 11.2.3 we will extend our constrained optimization method to dynamic problems (i.e., problems in which the independent variables change with time).

**11.2.1 Static constrained optimization**

Suppose we want to minimize some scalar function J(x, w) with respect to x and w. x is an n-dimensional vector, and w is an rn-dimensional vector. w is the indepen- dent variable and x is the dependent variable; that is, x is somehow determined by 
## w. Suppose our vector-valued constraint is given as f(x, w) = 0. Further m u m e
 **that the dimension of f(x, w) is the same as the dimension of x. This problem can** be written as min J(x, w) such that f(x, w) = 0 (11.13)

Suppose that the constrained minimum of J(x, w) occurs at x = x* and w = w*. We call this the stationary point of J(x, w). Now suppose that we choose values of x and w such that x is close to x*, w is close to w*, and f(x, w) = 0. Expanding J(x, w) and f(x, w) in a Taylor series around x* and w* gives

**x,w**

J(x, w) = J(x*,w*) + El A x + E ~  AW 
## ax x*,w*
 **x*,w***

f(X,W) = f ( X * , W * ) +  af/ A x + E l Aw (1 1.14) 
## ax I *  ,w*
 **X*,W***

where higher-order terms have been neglected (with the assumption that x is close to x*, and w is close to w*), Ax = x - x*, and Aw = w - w*. These equations can **be written as**

AJ(x, W) = J(x, W) - J(x*, w')

(11.15)

Now note that for values of x and w that are close to x* and w*, we have A J(x, w) = 0. This is because the partial derivatives on the right side of the AJ(x, w) equation are zero at the stationary point of J(x, w). We also see that Af(x, w) = 0 at the stationary point of J(x, w). This is because f(x*, w*) = 0 at the constrained stationary point of J(x, w), and we chose x and w such that f(x, w) = 0 also. The

---


[Image on page 6]


**338**

**above equations can therefore be written as**

**A X +** 1 
## A w  = 0
 **x',w'**

*a f* (1 1.16)

**These equations are true for arbitrary x and w that are close to x* and w* and** 
## that satisfy the constraint f(x, w )  = 0. Equation (11.16) can be solved for Ax as


(1 1.17)

This can be substituted into Equation (11.16) to obtain - *dJ1* - - *dJ1* ("I 
$$
)-'xi = o
$$
 (1 1.18) 
## dw x*,w*
 
## dx x8,w.
 **dx** 
## dw x*,w*


This equation, combined with the constraint f(s, 
## w )  = 0, gives us (m+n) equations
 **that can be solved for the vectors w and x to find the constrained stationary point** **of J ( x ,  w).** Now consider the augmented cost function

*Ja = J + A T f* (1 1.19)

where A is an n-element unknown constant vector called a Lagrange multiplier. Note that *d J* *d f* *- -+AT-* *Ja* **dX** **dX** **dX** - -

*d J* *T d f* - - + A - *d Ja* **dW** **dW** **dW** - -

If we set all three of these equations equal to zero then we have

(1 1.20)

(11.21)

The first equation gives us the value of the Lagrange multiplier, the second equation is identical to Equation (11.18), and the third equation forces the constraint to be satisfied. We therefore see that we can solve the original constrained problem by *creating an augmented cost function Ja, taking the partial derivatives with respect* 
## to x, w ,  and A, setting them equal to zero, and solving for x, w ,  and A. The
 *partial derivative equations give us (271 + m) equations to solve for the n-element* 
## vector x, the m-element vector w ,  and the n-element vector A. We have increased
 the dimension of the original problem by introducing a Lagrange multiplier, but we have transformed the constrained optimization problem into an unconstrained optimization problem, which can simplify the problem considerably.

---


[Image on page 7]


**339**

**EXAMPLE 11.1**

*Suppose we need to find the minimum of J(x, u) = x2/2 + xu + u2 + u with* respect to z and u such that f(z, u) = x - 3 = 0. This simple example can 
## be solved by simply realizing that x = 3 in order to satisfy the constraint.
 
# Substituting z = 3 into J(x, u) gives J(x, u) = 9/2 + 4u + u2. Setting the
 derivative with respect to u equal to zero and solving for u gives u = -2. We can also solve this problem using the Lagrange multiplier method. We **create an augmented cost function as**

Ja = J + X T f = z2/2 + z u  + u2 + u + X(x - 3) (11.22)


## The Lagrange multiplier X has the same dimension as z (scalar in this exam-
 ple). The three necessary conditions for a constrained stationary point of J are obtained by setting the partial derivations of Equation (11.20) equal to 0.

= z + u + X = O aJa d X  -

- x + 2 u + l = O *a Ja*

d U - -

- x - 3 = 0 aJa *dX* - - (11.23)


## Solving these three equations for x, u, and X gives x = 3, u = -2, and X =
 -1. In this example the Lagrange multiplier method seems to require more effort than simply solving the problem directly. However, in more complicated constrained optimization problems the Lagrange multiplier method is essential for finding a solution. vvv

**11.2.2** **Inequality constraints**

Suppose that we want to minimize a scalar function that is subject to an inequality constraint: *min J(x) such that f(x) 5 0* (11.24)

This can be reduced to two minimization problems, neither of which contain in- equality constraints. The first minimization problem is unconstrained, and the second minimization problem has an equality constraint:

1. minJ(z)


$$
2. min J(z) such that f(z) = 0
$$


In other words, the optimal value of z is either not on the constraint boundary [i.e., f(x) < 01, or it is on the constraint boundary [i.e., f(x) = 01. If it is not on the constraint boundary then f(x) < 0 and the optimal value of x is obtained by solving the problem without the constraint. If it is on the constraint boundary then f(z) = 0 at the constrained minimum, and the optimal value of x is obtained by solving the problem with the equality constraint f(x) = 0.

---

**340**

**The procedure for solving Equation (11.24) involves solving the unconstrained** problem first. Then we check to see if the unconstrained minimum satisfies the constraint. If the unconstrained minimum satisfies the constraint, then the uncon- strained minimum solves the inequality-constrained minimization problem and we are done. However, if the unconstrained minimum does not satisfy the constraint, then the minimization problem with the inequality constraint is equivalent to the minimization problem with the equality constraint. So we solve the problem with 
$$
the equality constraint f(z) = 0 to obtain the final solution. This is illustrated for
$$
 the scalar case in Figure 11.1.

**-0.5 -** **-0.5**

**-2** **-1.5** **-1** **-0.5** **0** **0.5** **1** **1.5** **2**

**X**

**Figure 11.1** **This illustrates the constrained minimization of z2. If the constraint is** *z - 1 5 0, then the constrained minimum is equal to the unconstrained minimum and occurs* 
$$
at z = 0. If the constraint is x + 1 5 0, then the constrained minimum can be solved by
$$
 
# enforcing the equality constraint x + 1 = 0 and occurs at 2 = -1.


When we extend this idea to more than one dimension, we obtain the following procedure, which is called the active-set method for optimization with inequality constraints [Fle81, Gi1811.

*1. The problem is to minimize J ( z )  such that f(z) 5 0, where f(z) is an m-* element constraint function and the inequality is taken one element at a time.

**2. First solve the unconstrained minimization problem. If the unconstrained** *solution satisfies the constraint f(z) 5 0 then the problem is solved. If not,* continue to the next step.

**3. For all possible combinations of constraints, solve the problem using those** constraints as equality constraints. If the solution satisfies the remaining (unused) constraints, then the solution is feasible. Note that this step requires 
# the solution of (2.' - 1) constrained optimization problems.


**4. Out of all the feasible solutions that were obtained in the previous step, the** *one with the smallest J(z) is the solution to the constrained minimization* problem.

---


[Image on page 9]


**341**

Note that there are also other methods for solving optimization problems with inequality constraints, including primal-dual interior-point methods [Wri97].

**11.2.3** **Dynamic constrained optimization**

In this section we extend the Lagrange multiplier method of constrained optimiza- tion to the optimization of dynamic systems. Suppose that we have a dynamic system given as

**z k + 1  = F k X k f W k** **( k = O , * * * , N - 1 )** (1 1.25)

**where Xk is an n-dimensional state vector. We want to minimize the scalar function**

**N - 1** (11.26)

**k=O**

**where $(xo) is a known function of 20, and e k  is a known function of Xk and W k .** This is a constrained dynamic optimization problem similar to the type that arises in optimal control [Lew86a, Ste941. It is slightly different than typical optimal **control problems because $ ( X k )  in the above equation is evaluated at the initial** 
## time ( I c  = 0) instead of the final time (k = N ) ,  but the methods of optimal control
 can be used with only slight modifications to solve our problem. The constraints are given in Equation (11.25). From the previous section we know that we can solve this problem by introducing a Lagrange multiplier A, creating an augmented **cost function Ja, and then setting the partial derivatives of J, with respect to Xk,**


## W k ,  and X equal to zero. Since we have N constraints in Equation (11.25) (each
 
## of dimension n), we have to introduce N Lagrange multipliers X I ,  .
 
## a ,  AN (each of
 dimension n). The augmented cost function is therefore written as

This can be written as

**N - 1** **N - 1**

**k=O** **k=O**

where A0 is now an additional term in the Lagrange multiplier sequence. It is not in the original augmented cost function, but we will see in Section 11.3 that its value will be determined when we solve the constrained optimization problem. Now we **define the Hamiltonian 'Flk as**

(1 1.29)

**With this notation we can write the augmented cost function as follows.**

---

**342**


$$
k =O
$$


The conditions that are required for a constrained stationary point are

**These conditions can also be written as**

(11.30)

**(11.31)**

**(11.32)**


# The fifth condition ensures that the constraint X k f l  = F k x k  + W k  is satisfied. Based
 **on the expression for Ja in Equation (11.30), the first four conditions above can be** written as

This gives us the necessary conditions for a constrained stationary point of our dynamic optimization problem. These are the results that we will use to solve the H, estimation problem in the next section.

---

**343**


## 11.3 A GAME THEORY APPROACH T O  H,
 **FILTERING**

The H, solution that we present in this section was originally developed by Ravi Banavar [Ban921 and is further discussed in [She95, She971. Suppose we have the standard linear discrete-time system

(1 1.34)

**where W k  and Wk are noise terms. These noise terms may be random with possibly** unknown statistics, or they may be deterministic. They may have a nonzero mean. Our goal is to estimate a linear combination of the state. That is, we want to **estimate Z k ,  which is given by**


## z k  = L k x k
 (11.35)

**where L k  is a user-defined matrix (assumed to be full rank). If we want to directly** 
## estimate X k  (as in the Kalman filter) then we set L k  = 1. But in general we may
 **only be interested in certain linear combinations of the state. Our estimate of Zk** **is denoted &, and our estimate of the state at time 0 is denoted 20. We want to** 
## estimate Zk based on measurements up to and including time ( N  - 1). In the game
 theory approach to H, filtering we define the following cost function:

**Our goal as engineers is to find an estimate & that minimizes J 1 .  Nature's goal** **as our adversary is to find disturbances Wk and Wk, and the initial state 20, to** 
# maximize J1. Nature's ultimate goal is to maximize the estimation error ( Z k  - &).
 
## The way that nature maximizes ( Z k  - &) is by a clever choice of W k ,  V k ,  and 20.
 
## Nature could maximize ( Z k  - &) by simply using infinite magnitudes for W k ,  ?Jk,
 **and 20, but this would not make the game fair. That is why we define J 1  with** 
# (20 - 20), W k ,  and ?& in the denominator. If nature uses large magnitudes for ' w k ,


# V k ,  and xo then ( z k  - &) will be large, but J 1  may not be large because of the
 **denominator. The form of J 1  prevents nature from using brute force to maximize**


# (Zk - &). Instead, nature must try to be clever in its choice of W k ,  V k ,  and xo as
 
# it tries to maximize ( Z k  - &). Likewise, we as engineers must be clever in finding
 
# an estimation strategy to minimize (Zk - .&).
 This discussion highlights a fundamental difference in the philosophy of the Kalman filter and the H, filter. In Kalman filtering, nature is assumed to be **indifferent. The pdf of the noise is given. We (as filter designers) know the pdf** of the noise and can use that knowledge to obtain a statistically optimal state es- timate. But nature cannot change the pdf to degrade our state estimate. In H, **filtering, nature is assumed to be perverse and actively seeks to degrade our state** estimate as much as possible. Intuition and experience seem to indicate that nei- ther of these extreme viewpoints of nature is entirely correct, but reality probably lies somewhere in the middle.

lNevertheless, it is advisable to remember the pnnczple of perversity of ananamate objects [BarOl, 
## p. 961 - for instance, when dropping a piece of buttered toast on the floor, the probability is
 significantly more than 50% that the toast will land buttered-side down.

---

**344**

**Po, Q k ,  R k ,  and s k  in Equation (11.36) are symmetric positive definite matrices** chosen by the engineer based on the specific problem. For example, if the user is **particularly interested in obtaining an accurate estimate of the third element of Z k ,** **then & ( 3 , 3 )  should be chosen to be large relative to the other elements of &. If** **the user knows u priori that the second element of the w k  disturbance is small,** **then Q k ( 2 , 2 )  should be chosen to be small relative to the other elements of Q k .** **In this way, we see that Pi,** **Q k ,  and R k  are analogous to those same quantities in** the Kalman filter, if those quantities are known. That is, suppose that we know that the initial estimation error, the process noise, and the measurement noise are zero-mean. Further suppose that we know their covariances. Then we should use **those quantities for Po, Q k ,  and R k  in the H,** estimation problem. In the Kalman **filter, there is no analogy to the S k  matrix given in Equation (11.36). The Kalman** filter minimizes the &-weighted sum of estimation-error variances for all positive **definite & matrices (see Section 5.2). But in the H,** filter, we will see that the **choice of s k  affects the filter gain.** *The direct minimization of J1 is not tractable, so instead we choose a perfor-* **mance bound and seek an estimation strategy that satisfies the threshold. That is,** **we will try to find an estimate ,i?k that results in**

**1** *J1 < -* *e* **(11.37)**

**where 6' is our user-specified performance bound. Rearranging this equation results** in

**<** **1** **(1 1.38)**

*where J is defined by the above equation. The minimax problem becomes*

*J* = min max J* **(11.39)**


## Since Zk = L k X k ,  we naturally choose i k  = L k 2 k  and try to find the 2 k  that
 *minimizes J .  This gives us the problem*

**i k  W k , V k , X O**


## J* = min rnax J
 **2 ,  W k  r v k  9x0** **(11.40)**

**Nature is choosing 20,** **w k ,  and Vk to maximize J .  But 20,** **W k ,  and V k  completely** **determine Y k ,  so we can replace the V k  in the minimax problem with Y k .  We** therefore have *J* = min max J* **(11.41)** *** k** **W k , Y k i Z O** 
# Since Y k  = H k X k  + ?&, We See that V k  = Y k  - H k X k  and


**(1 1.42)**

**(1 1.43)**

---

**345**

**where s k  is defined as**

We substitute these results in Equation (11.38) to obtain


## s k  = L r S k L k
 ( 11.44)

**N - 1** 
# = $(xO) +
 **L k** (1 1.45)

**k=O**


## where $(Q) and L k  are defined by the above equation. To solve the minimax
 **problem, we will first find a stationary point of J with respect to xo and W k ,  and** **then we will find a stationary point of J with respect to $k and y k .**


## 11.3.1 Stationarity with respect to 20 and W k


# The problem in this section is to maximize J = $(xo) + cfii L k  (subject to the
 
# constraint 2k+1 = F k x k  + W k )  with respect to 20 and W k .  This is the dynamic con-
 strained optimization problem that we solved in Section 11.2.3. The Hamiltonian **for this problem is defined as**

(11.46)

**where 2 X k + l / e  is the time-varying Lagrange multiplier that must be computed**


# (Ic = O,-. , N - 1). Note that we have defined the Lagrange multiplier as 2&+1/0
 **instead of x k + l .  This does not change the solution to the problem, it simply scales** the Lagrange multiplier (in hindsight) by a constant to make the ensuing math more straightforward. From Equation (11.33) we know that the constrained stationary **point of J (with respect to xo and w k )  is solved by the following four equations:**

From the first expression in the above equation we obtain

2x0 2 *e* *e* 
# -- -P,-'(zo-do)
 = 0

*Poxo-xo+~o = 0*


## 20 = $i.o+Poxo


From the second expression in Equation (11.47) we obtain


## A N  = 0


(1 1.47)

(11.48)

(11.49)

---

**346**

**From the third expression in Equation (11.47) we obtain**

*W k  = Q k x k + i* **(11.50)**

This can be substituted into the process dynamics equation to obtain

*xk+1 = F k X k  -k Q k x k + i* **(11.51)**

**From the fourth expression in Equation (11.47) we obtain**

*T* *-1* *2* *- 2 s k ( x k  - $ k )  + $ H k  R k  ( y k  - H k X k )  + j F z x k + i*

*= F?Xk+l + e s k ( x k  - ? k )  + H F R i l ( y k  - H k x k )*

*2 x k* - - *e* **(1 1.52)**

At this point we have to make an assumption in order to proceed any further. From 
# Equation (11.48) we know that xo = 20 + PoXo, so we will assume that


*x k  = p k  + P k x k* 
## ( 11.53)


**for all k, where p k  and P k  are some functions to be determined, with PO given,** 
## and the initial condition po = 20. That is, we assume that Xk is an affine function
 *of x k .  This assumption may or may not turn out to be valid. We will proceed as* if the assumption were true, and if our results turn out to be correct then we will **know that our assumption was indeed valid. Substituting Equation (11.53) into** **Equation (11.51) gives**

**(1 1.54)** *pk+1 + P k + l x k + l  = F k P k  + F k p k x k  + Q k x k + l*

**Substituting Equation (11.53) into Equation (11.52) gives**

*x k  = F z x k + l  + e s k ( p k  + P k x k  - & k )  + HrRL1 [Yk - H k ( p k  + p k x k ) ]* **(11.55)**

Rearranging this equation gives

*x k  - O S k P k X k  + H F R k l H k P k . &* =

*F z x k + l  + e g k ( p k  - * k )  + H ; R I , ' ( y k  - H k p k )* **(1 1.56)**

*This can be solved for x k  as*


# Xk = [I - 6 s k P k  + H z R c l H k p k ] - '
 X **T -1** *[ F z x k + l  + e s k ( p k  - z k )  + H k  R k  ( y k  - H k p k ) ]* **(11.57)**

**Substituting this expression for x k  into Equation (11.54) gives**


# p k + i  -k Pk+lXk+l = F k p k  + F k p k  [I - e s k p k  + H r R , l H k P k ] - l
 X

*[F?xk+.l + e S k ( p k  - 2 k )  + H ; R i l ( Y k  - H k p k ) ]  + QkXk+i* **(11.58)**

**This equation can be rearranged as follows:**


# p k + l  - F k p k  - F k P k  [I - e s k P k  + H I R i l H k P k ] - l  X


*[ e s k ( p k  - 2 k )  -k H z R k l ( Y k  - H k p k ) ]  =*


# [-pk+l + F k P k  [I - e s k p k  + H F R i l H k P k ] - l  F z  + Q k ]  &+I
 **(11.59)**

---

**347**

This equation is satisfied if both sides are zero. Setting the left side of the above equation equal to zero gives

*pk+1* *= F k p k  -k F k P k  [I - 8 s k P k  -k H ; R ; l H k P k ] - l* X

*[ e S k ( P k  - 2 k )  f H k* *T R k* 
# -1 ( Y k  - H k P k ) ]
 (1 1.60)

**with the initial condition**


## Po = fo


Setting the right side of Equation (11.59) equal to zero gives

*Pk+1* 
# = F k P k  [I - 8 s k P k  f H f R i l H k P k ] - l  Fr + Q k
 *= F k & F r - k Q k*

*where & is defined by the above equation. That is,*

(11.61)

(11.62)

*= P k  [I - 8 S k P k  -k H r R k l H k P k ] - l*

*= [P;' - 89, f H F R i ' H k 1 - l* (1 1.63)

*From the above equation we see that if P k ,  s k ,  and R k  are symmetric, then P k  will* *be symmetric. We see from Equation (11.62) that if Qk is also symmetric, then*

**Pk+1 will be symmetric. So if PO, Q k ,  R k ,  and s k  are symmetric for all k, then** **z'r, and P k  will be symmetric for all k. The values of 20 and W k  that provide a** **stationary point of J can be summarized as follows:**


## 20 = 2 0  +POX0


*w k  = QkAk+l*

*AN* = 0

*Ak* *= [I - 8 S k P k  f I f f R ; l H k P k ] - l* X

*[F,TAk+l + e S k ( P k  - f k )  -k HTR-'* *k* *k (Yk - H k P k ) ]*

*P k + i* 
# = F k P k  [I - 8 S k P k  + H r R F ' H k P k ]
 *F z  + Q k*


## Po = fo


*p k + l* *= F k p k  f F k P k  [I - 8 S k P k  f H r R k l H k P k ] - l  X*

*[ e S k ( P k  - 2 k )  -k H r R i l ( Y k  - H k P k ) ]* (11.64)

The fact that we were able to find a stationary point of J shows that we were *correct in our assumption that X k  was an affine function of &. In the following* **section, given these values of 20 and W k ,  we will find the values of 2 k  and Y k  that** *provide a stationary point of J .*

**11.3.2**

*The problem in this section is to find a stationary point (with respect to 2 k  and*

**This problem is solved given the fact that ZO and W k  have already been set to their**


## Stationarity with respect to 5 and y


**N-1** *Y k )  Of J = $(Zk)lk=o -k x k = O  c k  (subject to the Constraint z k + l  = F k X k  f w k ) .*

---

**348**

maximizing values as described in Section 11.3.1. From Equation (11.53), and the **initial condition of p k  in Equation (11.61), we see that**

(1 1.65)

We therefore obtain

lxol;o 
## = gpoxo
 = **(20 -20) T Po -T PoPo-l(zo - 2 0 )**

**(20 -20) T Po** **- 1  (20 -20)** = = llzo - 2oIlp;1 **2** (1 1.66)

Therefore, Equation (1 1.45) becomes

**Substituting for 2 k  from Equation (11.53) in this expression gives**

(1 1.68) -1 *J = ~ l l ~ o / l ~ o +*

**Consider the term w ~ & ~ l w k** **in the above equation. Substituting for W k  from** Equation (11.50) in this term gives

**T** **-1** **T** **- 1** 
## W k Q k  Wk = A;+l&kQk
 **QkAk+l** 
## = AT+iQkAk+l
 (11.69)

**where we have used the fact that Q k  is symmetric. Equation (11.68) can therefore** **be written as**

(1 1.70) -1 
## J = -lIxoll;o+
 *e*

Now we take a slight digression to notice that

The reason that this equation is correct is because from Equation (11.49) we know 
## that AN = 0. Therefore, the last term in the first summation above is equal to zero


---


[Image on page 17]


**349**

and the two summations are equal. The above equation can be written as

We can subtract this zero term to the cost function of Equation (11.70) to obtain

*Now we consider the term xc+;1(Pk+l - Qk)&+l* in the above expression. Substi- *tuting for Pk+l from Equation (11.62) in this term gives*

A;+; *(PkAl - Qk)Ak+l* *= x c + i ( Q k  + FkpkFT - Q k ) x k + i* = $+ *1 Fk p k  FF x k  + I* *(1 1.74)*

---

**350**

**(1 1.77)**

Notice that the above expression is a scalar. That means that each term on the right side is a scalar, which means that each term is equal to its transpose. For example, consider the second term on the right side. Since it is a scalar, we see 
# that e ( p k  - 2 k ) T S k P k X k  = e x : P k s k ( p k  - 2 k ) .  (we have used the fact that P k  and


## S k  are symmetric, and 8 is a scalar.) Equation (11.77) can therefore be written as


**(1 1.78)**

**Now note from Equation (11.63) that**

**(1 1.79)**

We therefore see that

(1 1.80)

**Substituting this into Equation (11.78) gives**

**(11.81)**

**Substituting this equation for x r + l ( P k + l -** **Q k ) & + l** **into Equation (11.73) gives the** following.

---


[Image on page 19]


**351**

*These equations are clearly satisfied for the following values of 2 k  and yk:*

*( 1  1.84)*

*These are the extremizing values of ?k and yk. However, we still are not sure if* *these extremizing values give a local minimum or maximum of J .  Recall that the* *second derivative of J tells us what kind of stationary point we have. If the second* derivative is positive definite, then our stationary point is a minimum. If the second derivative is negative definite, then our stationary point is a maximum. If the second derivative has both positive and negative eigenvalues, then our stationary point is *a saddle point. The second derivative of J with respect to h k  can be computed as*

*( 1  1.85)*

_ - _ *Our ?k will therefore be a minimizing value of J if ( s k  + e s k p k s k )  is positive* *definite. The value of s k  chosen for use in Equation (11.36) should always be* *positive definite, which means that S k  defined in Equation (11.44) will be positive* **definite. This means that our ?k will be a minimizing value of J if & is positive** definite. *in Equation (11.63), the condition required for ?k* *to minimize J is that (P;' - e s k  + H?R;lHk)-l* be positive definite. This is

*So, from the definition of*

---

**352**


# equivalent to requiring that (PF' - e s k  + H ? R i l H k )  be positive definite. The
 individual terms in this expression are always positive definite [note in particular **from Equation (11.62) that P k  will be positive definite if 4 is positive definite].** **So the condition for ?k to minimize J is that e s k  be "small enough" so that** 
# (PF' - e s k  + H F R k ' H k )  is positive definite. Requiring that
 be small can be accomplished three different ways.

**1. e s k  will be small if 0 is small. This means that the performance requirement** **specified in Equation (11.37) is not too stringent. As long as our performance** requirement is not too stringent then the problem will have a solution. If, *however, the performance requirement is too stringent (i.e., 6 is large) then* the problem will not have a solution.

**2. 63, will be small if L k  is small. This statement is based on the relationship** **between S k  and L k  as shown in Equation (11.44). From Equation (11.36) we** **see that the numerator of the cost function is given as ( Z k - & ) T L T S k L k ( Z k -** 
## &). So if L k  is small we see that the numerator of the cost function will be
 small, which means that it will be easier to minimize the cost function. If, **however, L k  is too large, then the problem will not have a solution.**

**3. e s k  will be small if s k  is small. This statement is based on the relationship** **between s k  and S k  as shown in Equation (11.44). From Equation (11.36) we** **see that the numerator of the cost function is given as ( Z 1 , - ? k ) T L ; S k L k ( 3 & -** 
## &). so if s k  is small we see that the numerator of the cost function will be
 small, which means that it will be easier to minimize the cost function. If, **however, s k  is too large, then the problem will not have a solution.**

**Note from Equation (11.62) that the positive definiteness of p k  implies the positive** **definiteness of %+I.** **Therefore, if Po is positive definite (per our original problem** **statement), and p k  is positive definite for all k ,  then P k  will also be positive definite** **for all k.** It is also academically interesting (though of questionable utility) to note the **conditions under which the Y k  that we found in Equation (11.84) will be a maxi-** **mizing value of J .  (Recall that Y k  is chosen by nature, our adversary, to maximize** **the cost function.) The second derivative of J with respect to y k  can be computed** as

**R k  and Rk', specified by the** **tion (11.36), should always be**

**(11.86)**

**user as part of the problem statement in Equa-** positive definite. So the second derivative above **will be negative definite (which means that Y k  will be a maximizing value of J )  if**


# ( R k  - H k p k H ? )  is positive definite. This requirement can be satisfied in two ways.


# 1. (Rk - H k p k H F )  will be positive definite if R k  is large enough. A large value
 **of R k  means that the denominator of the cost function of Equation (11.36)** **will be small, which means that the cost function will be large. A large** cost function value is easier to maximize and will therefore tend to have a

---


[Image on page 21]


**353**

**maximizing value for Y k .  Also note that the designer typically chooses R k  to** be proportional to the magnitude of the measurement noise. If the user knows **that the measurement noise is large, then R k  will be large, which again will** **result in a problem with a maximizing value for y k .  In other words, nature** will be better able to maximize the cost function if the measurement noise is large.


## 2. (& - H k & H T )  will be positive definite if H k  is small enough. If H k  becomes
 smaller, that means that the measurement noise becomes larger relative to **the size of the measurements, as seen in Equation (11.34). In other words,** **a small value of H k  means a smaller signal-to-noise ratio for the measure-** **ments. A small signal-to-noise ratio gives nature a better opportunity to find** **a maximizing value of Y k .**

**Of course, we are not really interested in finding a maximizing value of Y k .  Our goal** **was to find the minimizing value of X k .  The H,** filter algorithm can be summarized as follows.


## The discretetime H,
 **filter**

**1. The system equations are given as**

**(11.87)**

**where W k  and Vk are noise terms, and our goal is to estimate 9.**

**2. The cost function is given as**

**where PO, & k ,  R k ,  and s k  are symmetric, positive definite matrices chosen** by the engineer based on the specific problem.

**3. The cost function can be made to be less than l / e  (a user-specified bound)** **with the following estimation strategy, which is derived from Equations (11.44),** **(11.60), (11.62), and (11.84):**


## s k  = L T s k L k


# K k  = P k  [I - e s k p k  + H T R i l H k P k ] - l  HTRkl


# i k f l  = F k 2 k  -k F k K k ( Y k  - H k 2 k )


**P k + l** 
# = F k P k  [I - e s k p k  + H ? R I , l H k P k ] - l  FF + Q k
 **(11.89)**

**4. The following condition must hold at each time step k in order for the above** estimator to be a solution to the problem:


# PF1 - O S k  + H Z R k l H k  > 0
 (1 1.90)

---


[Image on page 22]


**354**

**11.3.3**

Comparing the Kalman filter in Equation (11.12) and the H, filter in Equa- tion (11.89) reveals some fascinating connections. For instance, in the H, filter,


## Q k ,  R k ,  and Po are design parameters chosen by the user based on a priori knowl-
 **edge of the magnitude of the process disturbance ' w k ,  the measurement disturbance**


# w k ,  and the initial estimation error (20 - $0). In the Kalman filter, w k ,  V k ,  and


# (20 - 20) are zero-mean, and Q k ,  R k ,  and PO are their respective covariances.
 
## Now suppose we use L k  = s k  = I in the H,
 filter. That is, we are interested in estimating the entire state, and we want to weight all of the estimation errors 
## equally in the cost function. If we use 6 = 0 then the H,
 filter reduces to the **Kalman filter (assuming Q k ,  R k ,  and Po are chosen as above). This provides an** interesting interpretation of the Kalman filter; that is, the Kalman filter is the minimax filter in the case that the performance bound in Equation (11.36) is set *equal to 00. We see that although the Kalman filter minimizes the variance of the* **estimation error (as discussed in Section 5.2), it does not provide any guarantee as** far as limiting the worst-case estimation error. That is, it does not guarantee any bound for the cost function of Equation (11.36). The Kalman and H, filter equations have an interesting difference. If we want to estimate a linear combination of states using the Kalman filter, the estimator is the same regardless of the linear combination that we want to estimate. That is, if **we want to estimate L k x k  using the Kalman filter, the answer is the same regardless** **of the L k  matrix that we choose. However, in the H,** approach, the resulting filter **depends strongly on L k  and the particular linear combination of states that we** want to estimate. Note that the H, filter of Equation (11.89) is identical to the Kalman filter **except for subtraction of the term e S k P k  in the K k  and P k + 1  equations. Recall** from Section 5.5 that the Kalman filter can be made more robust to unmodeled **noise and unmodeled dynamics by artificially increasing Qk in the Kalman filter** **equations. This results in a larger covariance P k ,  which in turn results in a larger** **gain K k .  From Equation (11.89) we can see that subtracting e s k k p k  on the right** **side of the p k + 1  equation tends to make P k + l  larger (since the subtraction is inside** **a matrix inverse operation). Similarly, subtracting e s k k p k  on the right side of** **the K k  equation tends to make K k  larger. Increasing Q k  in the Kalman filter is** **conceptually the same as increasing P k  and K k .  Therefore, the H, filter equations** make intuitive sense when compared with the Kalman filter equations. The H, **filter is a worst-case filter in the sense that it assumes that ' w k ,  V k ,  and 20 will be** chosen by nature to maximize the cost function. The H, filter is therefore robust by design. Comparing the H, filter with the Kalman filter, we can see that the H, filter is simply a robust version of the Kalman filter. When we robustified the Kalman filter in Section 5.5 to add tolerance to unmodeled noise and dynamics, we **did not derive an optimal way to increase Q k .  However, H,** filter theory shows us the optimal way to robustify the Kalman filter.


## A comparison of the Kalman and H,
 **filters**


## 11.3.4 Steady-state H,
 **filtering**

If the underlying system and the design parameters are time-invariant, then it may be possible to obtain a steady-state solution to the H, filtering problem. Suppose

---


[Image on page 23]


**355**

that our system is given as

*where W k  and Vk are noise terms. Our goal is to estimate Zk such that*

(11.91)

(11.92)

*where Q, R, and S are symmetric positive definite matrices chosen by the engineer* based on the specific problem. The steady-state filter of Equation (11.89) becomes


## S = L ~ S L
 *K = P [I - eSP + HTR-lHP]-' HTR-l*

*P = FP [I - eSP + HTR-lHP]-' FT + Q*

*?k+l* *= Fhk -k FKk(yk - H f k )*

(11.93)

The following condition must hold in order for the above estimator to be a solution to the problem: *p - l -  eS + H ~ R - ~ H* *> o* (11.94)


## If 0, L, R, or S is too large, or if H is too small, then the H,
 estimator will not *have a solution. Note that the expression for P in Equation (11.93) can be written* as 
# P = F [P-' - 0s + HTR-lH]-' FT + Q
 (1 1.95)

Applying the matrix inversion lemma to the inverse in the above expression gives

*P = F { P -  P [(HTR-lH - eS)-' + P]-'P} FT + Q*

*= FPFT - F P  [ ( H T R - ~ H  - es)-l+* *PI-'* *PFT + Q* (11.96)

This is a discretetime algebraic Riccati equation that can be solved with control system software.2 If control system software is not available, then the algebraic Riccati equation can be solved by numerically iterating the discrete-time Riccati equation of Equation (11.89) until it converges to a steady-state value. The steady- state filter is much easier to implement in a system in which real-time computational effort or code size is a serious consideration. The disadvantage of the steady-state **filter is that (theoretically) it does not perform as well as the time-varying filter.** However, the reduced performance that is seen in the steady-state filter is often a small fraction of the optimal performance, whereas the computational savings can be significant.

2For example, **in MATLAB's Control System Toolbox we can use the command** **DARE(FT,I,Q,** **( H ~ R - ~ H** 
## - es)-1.


---


[Image on page 24]


**356**

**1 EXAMPLE 11.2**

Suppose we are trying to estimate a randomly varying scalar on the basis of noisy measurements. We have the scalar system

**(1 1.97)**

This system could describe our attempt to estimate a noisy voltage. The voltage is essentially constant, but it is subject to random fluctuations, hence **the noise term Wk in the process equation. Our measurement of the voltage** **is also subject to noise or instrument bias, hence the noise term Vk in the** 
## measurement equation. We see in this example that F = H = L = 1. Further
 
## suppose that Q = R = S = 1 in the cost function of Equation (11.88). Then
 the discretetime Riccati equation associated with the H, filter equations becomes


# Pk+1 = F k P k  [I - eskpk -k HTRklHkPk]-l F r  + Qk
 
# = Pk [1 - e p k  + Pk1-l + 1
 **(11.98)**

This can be solved numerically or analytically as a function of time for a given 
## 8 to give P k ,  and then the H,
 gain can be obtained as

**Kk** 
# = P k  [I - eSkPk + HTRilHkPk]-l H;Ril
 
# = p k  [1 - e p k  + Pk1-l
 **(1 1.99)**


## we can set P k + l  = Pk in Equation (11.98) to obtain the steady-state solution
 **for Pk. This gives**


## P = p(i-eP+p)-l+i
 
## P(i-eP+P) = p+(i-ep+p)
 
# (1 - e)p2 + (e - i
 **)** **~** - 1 = o


# 1 - e & J(e - i)(e - 5)
 
## 2(1- e)
 *P* *=* **(1 1.100)**

**As we discussed earlier, i-n order for this value of P to be a solution to the** H, **estimation problem, P must be positive definite. The first solution for P** 
## is positive if 6 < 1, and both solutions for P are positive if 0 2 5. Another
 condition for the solution of the H, estimation problem is that


# p-l- eS + H ~ R - ~ H
 > o 
## P - l - e + i  > o
 **(11.101)**


## If 6 < 1 then the first solution for P satisfies this bound. However, if 8 2 5,
 **then neither solution for P satisfies this bound. Combining this data shows** that the H, 
## estimator problem has a solution for 6 < 1. Every H,
 estimator *problem will have a solution for 6 less than some upper bound because of the* nature of the cost function.

---


[Image on page 25]


**357**

**For a general estimator gain K the estimate can be written as**

**?k+l** 
# = F?k + FK(yk - H k ? k )
 
# = (1 - K)?k + Kyk
 (11.102)


## If we choose 8 = 1/2, then we obtain P = 2 and K = 1. As seen from the above
 
## equation, this results in bk+l = y k .  In other words, the estimator ignores
 the previous estimate and simply sets the estimate equal to the previous 
## measurement. As 8 increases toward 1, P increases above 2 and approaches


## 00, and the estimator gain K increases greater than 1 and also approaches 00.
 In this case, the estimator will actually place a negative weight on the previous estimate and compensate by placing additional weight on the measurement. **If 8 increases too much (gets too close to 1) then the estimator gain K will** be greater than 2 and the H, estimator will be unstable. It is always a good idea to check the stability of your H, filter. If the filter is unstable then you **should probably decrease 8 to obtain a stable filter. As 8 decreases below** **1/2, P decreases below 2 and the gain K decreases below 1. In this case, the** estimator balances the relative weight placed on the previous estimate and the measurement. **A Kalman filter to estimate Xk is equivalent to an H,** 
## filter with 0 = 0. In
 this case, we obtain the positive definite solution of the steady-state Riccati 
# equation as P = (1 + G)/2. This gives a steady-state estimator gain K =
 
# (1 + &)/(3 + 4)
 
# = (4 - 1)/2 M 0.62. The Kalman filter gain is smaller
 than the H, filter gain for 8 > 0, which means that the Kalman filter relies less on measurements and more on the system model. The Kalman filter gives an optimal estimate if the model and the noise statistics are known, but it may undervalue the measurements if there are errors in the system model or the assumed noise statistics. **Figure 11.2 shows the true state Xk and the estimate ?k when the steady-** state Kalman and H, filters are used to estimate the state. The H, filter was 
# designed with 8 = 1/3, which gave a filter gain K = (3 + 3fi)/(8 + 2 8 )  x
 **0.82. The disturbances W k  and Wk were both normally distributed zero-mean** white noise sequences with standard deviations equal to 10. The performance of the two filters is very similar. The RMS estimation error of the Kalman filter is 3.6 and the RMS estimation error of the H, **filter is 4.1. As expected,** the Kalman filter performs better than the H, filter. However, suppose that the process noise has a mean of 10. Figure 11.3 shows the performance of the filters for this situation. In this case the H, filter performs better. The RMS estimation error of the Kalman filter is 15.6 and the RMS estimation error of the H, filter is 12.0. 
## If we choose 8 = 1/10 then we obtain P = 5/3 and K = 2/3. As 8 gets
 smaller, the H, estimator gain gets closer and closer to the Kalman filter gain. vvv

**11.3.5**

In this section, we show that the steady-state H, filter derived in the previous section bounds the transfer function from the noise to the estimation error, if Q,


## The transfer function bound of the H,
 **filter**

---

**358**

-4-

-6' I 0 5 10 15 20 time

**Figure 11.2** Example 11.2 results. K h a n  and H, filter peformance when the noise **statistics are known. The Kalman gain is 0.62 and the H,** gain is 0.82. The Kalman filter performs about 12% better than the H, filter.

Kalman estimate

**J 150-** - **9**

0 5 10 15 20 time

**Figure 11.3** Example 11.2 results. Kalman and H, filter peformance when the process noise is biased. The Kalman gain is 0.62 and the H, gain is 0.82. The H, filter performs about 23% better than the Kalman filter.

**R, and S are all identity matrices. Recall that the two-norm of a column vector x** is defined as

**l l x l l 2 - x** **2 -** **T 2** **(1 1.103)**

**Now suppose we have a timevarying vector 50, XI, 2 2 ,** 
## a .  The signal two-norm of
 **x is defined as**

(11.104)

**k=O**

---

**359**

That is, the square of the signal two-norm is the sum of all of the squares of the vector two-norms that are taken at each time step.3 Now suppose that we have a **system with input u and output 5, and the transfer function is G(z). If the input** *u is comprised entirely of signals at the frequency w and the sample time of the* *system is T ,  then we define the phase of u as q5 = Tw. In this case the maximum* **gain from u to x is determined as**

sup - **I 1 5 c l 1 2** 
## = 01 [G (&@)I


## U#O llullz
 (11.105)

where ol(G) is the largest singular value of the matrix G. If u can be comprised of an arbitrary mix of frequencies, then the maximum gain from u to z is determined as follows:

= IlGllco (1 1.106)

The above equation defines llGli,, which is the infinity-norm of the system that *has the transfer function G ( z ) . ~* Now consider Equation (1 1.92), the cost function that is bounded by the steady- state H, filter:

*If Q, R, and S are all equal to identity matrices, then*

(11.107)

(11.108)

Since the H, **filter makes this scalar less than l/e for all Wk and vk, we can write**

(1 1.109)


## where we have defined 2 = z-2, eT = [ wT vT ] T ,  and Gze is the system that has
 **e as its input and 2 as its output. We see that the steady-state H,** filter bounds the infinity-norm (i.e., the maximum gain) from the combined disturbances w and v to 
## the estimation error 2, if &, R, and S are all identity matrices. Further information
 about the computation of infinity-norms and related issues can be found in [Bur99].

3Note that this definition means that many signals have unboundedsignal two-norms. The signal 
$$
two-norm can also be defined as the sum from k = 0 to a finite limit k = N .
$$
 4Note that the infinity-norm of a matrix has a definition that is different than the infinity-norm of a system. In general, the expression I IGI could refer either to the matrix infinity-normor the system infinity-norm. The meaning needs to be inferred from the context unless it is explicitly st at ed .

---


[Image on page 28]


**360**

**1 EXAMPLE 11.3**

**Consider the system and filter discussed in Example 11.2:**

The estimation error can be computed as

Taking the z-transform of this equation gives


# zZ(Z) = (1 - K ) Z ( z )  + W ( Z )  - KV(z)


**(11.1 10)**

**(11.111)**

**(1 1.112)**


## G(z), the transfer function from Wk and Wk to g k ,  is a 2 x 1 matrix. This
 matrix has one singular value, which is computed as


# The supremum of this expression occurs at + = 0 when K 5 1, so


**(11.113)**

**(11.114)**


## Recall from Example 11.2 that 6 = 1/2 resulted in K = 1. In this case,
 
## the above expression indicates that 11G11k = 2 5 l/e = 2. In this case, the
 
## infinity-norm bound specified by 0 is exact. Also recall from Example 11.2
 
## that 6’ = 1/10 resulted in K = 2/3. In this case, the above expression indicates
 
# that 1.lGl IL = 13/4 5 l/e = 10. In this case, the infinity-norm bound specified
 *by 0 is quite conservative.* **Note that as K increases, the infinity-norm from the noise to the estimation** 
## error decreases. However, the estimator also is unstable for K > 1. So
 **even though large K reduces the infinity-norm of the estimator, it gives poor** results. In other words, just because the effect of the noise on the estimation error is small does not necessarily prove that the estimator is good. For 
## example, we could set the estimate $k = 00 for all k. In that case, the noise


---

**361**

will have zero effect on the estimation error because the estimation error will be infinite regardless of the noise value. However, the estimate will obviously be poor. This example shows the importance of balancing H, performance with other performance criteria. vvv


## 11.4 THE CONTINUOUS-TIME H,
 
## FILTER


The methods of the earlier sections can also be used to derive a continuous-time H, **filter, as shown in** continuous-time system [Rhe89, Ban91, Ban921. In this section we consider the


$$
x = Ax+Bu+w
$$


y = c x + v

*z = La:* (1 1.115)

*where L is a user-defined matrix and z is the vector that we want to estimate. Our* 
## estimate of z is denoted 2, and our estimate of the state at time 0 is denoted h(0).
 The vectors w and v are disturbances with unknown statistics; they may not even be zero-mean. In the game theory approach to H, filtering we define the following cost function:

(1 1.116)

*Po, Q, R, and S are positive definite matrices chosen by the engineer based on the* specific problem. Our goal is to find an estimator such that

(1 1.117)

The estimator that solves this problem is given by

*P(0) = Po* 
# P = A P  + PAT + Q - KCP + 6'PLTSLP
 *K* *= PCTRM1* 
## 2 = AP+Bu+K(y-C2)
 
## 2 = L2
 (11 **I 118)**

These equations are identical to the continuous-time Kalman filter equations (see **Section 8.2) except for the 6' term in the P equation. The inclusion of the 6' term** **in the P equation tends to increase P, which tends to increase the gain K, which** tends to make the estimator more responsive to measurements than the Kalman filter. This is a way of robustifymg the filter to uncertainty in the system model. The estimator given above solves the H, estimation problem if and only if P(t) **remains positive definite for all t E [0, TI. As with the discrete-time filter, we can** also obtain a steady-state continuous-time H, 
## filter. To do this we let P = 0 so
 that the differential Riccati equation above reduces to an algebraic Riccati equation.

---


[Image on page 30]


**362**

**EXAMPLE 11.4**

Consider the scalar continuous-time system


$$
x = x+w
$$


$$
y = x + w
$$


*z* *=* *X* (1 1.119)


## We see that A = C = L = 1. Further suppose that Q = R = S = 1 in the
 cost function of Equation (11.116). Then the differential Riccati equation for the H, filter is


# P = A P  + PAT + Q - PCTR-'CP + .4PLTSLP
 = 2 p + i + ( e - i ) p 2 (11.120)

**This can be solved numerically or analytically as a function of time for a given** *0 to give P, and then the H,* gain K = PCTR-' = P can be obtained. We 
## can also set P = 0 in Equation (11.120) to obtain the steady-state solution
 **for P. This gives**

**As mentioned above, the solution to this quadratic equation must be positive** definite in order for it to solve the H, estimation problem. For this scalar equation, positive definite simply means positive. The equation has a positive *solution for 6 < 1, in which case the steady-state solution is given by*

(e - i)p2 + 2~ + 1 = o (11.121)

*-1 - rn* 8 - 1 P = (11.122)

*Suppose we choose 8 = 7/16. In this case, the analytic solution for the time-* **varying P can be obtained from Equation (11.120) as**

4 + 160ce5t/2 -9 + 40ce5t/2 P(t) =

9P(O) + 4 c = 40P(O) - 160

From this analytic expression for P(t) we can see that

lim P(t) = 4 t - + m

(11.123)

(1 1.124)

*Alternatively, we can substitute 6 = 7/16 in Equation (11.122) to obtain* 
## P = 4. Figure 11.4 shows P as a function of time when P(0) = 1. Note that
 in this example, since C = R = 1, the H, *gain K is equal to P.* Figure 11.5 shows the state estimation errors for the time-varying H, filter and the steady-state H, filter. In these simulations, the disturbances w and w were both normally distributed white noise sequences with standard deviations equal to 10. w had a mean of zero, and w had a mean of 10. Both simulations were run with identical disturbance time histories. It can be seen that the performance of the two filters is very similar. There are some differences between the two plots at small values of time before the

---


[Image on page 31]


**363**

**2** **4** **6** **8** **10** **Time**

**Figure 11.4** Example 11.4 H, **Riccati equation solution as a function of time.**

time-varying Riccati solution has converged to steady state (note that the time-varying filter performs better during the initial transient). But after the *Riccati solution gets close to steady state (after about t = 1) the performance* of the two filters is nearly identical. This illustrates the possibility of saving a lot of computational effort by using a steady-state filter while giving up only an incremental amount of performance.


## -25 '
 I a 1 **2** **3** **4** **5** **Time**

**Figure 11.5** the measurement noise is zero-mean. Example 11.4 timevarying and steady-state Hm filter performance when


## If we use the performance bound 0 = 0 in this example then we obtain
 the Kalman filter. The steady-state Riccati equation solution from Equa- tion (11.120) is (l+a) 
## when 0 = 0, so the steady-state Kalman gain K M 2.4,


---

**364**

which is less than the steady-state H, gain K = 4 that we obtained for 
## 0 = 7/16. From Equation (11.118) we see that this will make the Kalman
 filter less responsive to measurements than the H, filter, but the Kalman filter should provide optimal RMS error performance. Indeed, if we run the 
## timevarying Kalman filter (0 = 0) then the two-norm of the estimation error
 turns out to be 26.5. If we run the timevarying H, filter (0 = 7/16) then **the two-norm of the estimation error increases to 30.0.** However, the Kalman filter assumes that the system model is known ex- actly, the process and measurement noises are zero-mean and uncorrelated, and the noise statistics are known exactly. If we change the simulation so the measurement noise has a mean of 10 then the H, filter works better than the Kalman filter. Figure 11.6 shows the estimation error of the two filters in this case. The two-norm of the estimation error is 112.8 for the Kalman filter but only 94.2 for the H, filter.

I **0** **1** **2** **3** **4** **5** **Time**


## -30 '


**Figure 11.6** measurement noise is not zero-mean. Example 11.4 time-varying Kalman and H, filter performance when the

vvv 
## As with the discretetime steady-state filter, if Q, R, and S are all identity
 matrices, the continuous-time steady-state filter bounds the maximum gain from the noise to the estimation error:

(11.125)


# where w is the frequency of the noise, and we have defined 2 = z - 2, eT =
 
## [ wT vT IT, and Gi, is the system that has e as its input and 2 as its output.
 **The continuous-time infinity-norm of the system Gi, is defined as follows:**

---


[Image on page 33]


**365**

(1 1.126)

**where Gie(s) is the transfer function from e to 2.**


## 11.5
 **TRANSFER FUNCTION APPROACHES**

It should be emphasized that other formulations to H, filtering have been proposed. For instance, Isaac Yaesh and Uri Shaked [YaeSl] consider the following time- invariant system:

(11.127)

**where W k  and V k  are uncorrelated process and measurement noise, Y k  is the mea-** **surement, and Zk is the vector to be estimated. Define the estimation error as**

Define an augmented disturbance vector as

(11.129)

The goal is to find a steady-state estimator such that the infinity-norm of the **transfer function from the augmented disturbance vector e to the estimation error**

,Z is less than some user specified bound:

1 IIGzeII2 ; (1 1.130)

**The steady-state a priori filter that solves this problem is given as**


# P = I + F P F ~
 
# - F P H ~ ( I  + H P H ~ ) - ~ H P F ~
 +


# q I / e  + L P L ~ ) - ~ L P
 
# K = F P H ~ ( I  + H P H ~ ) - ~


?k+l 
# = F f k  + K ( y k  - H f k )
 (11.131)

These equations solve the H, estimation problem if and only if P is positive definite. **The steady-state a posteriori filter that solves this problem is given as**


## c-1 = P - ~ - B L T L + H T H
 
## F = F F ( H ~ H F
 *- O L ~ L F* 
# + I ) - ~ F ~
 
# + I
 **K** 
## = ( I + B L ~ L ) - ' c H ~
 
# = F(I + H ~ H P ) - ~ H ~


**?k+l** 
# = F?k + I?r(Yk+l - HF?k)
 (1 1.132)

---

**366**

Again, these equations solve the H, **estimation problem if and only if P is positive** definite. *Interestingly, the P matrix in the a priori filter of Equation (11.131) is related* **to the p matrix in the a posteriori filter of Equation (11.132) by the following** equation: *p-l= p-1- eLTL* (11.133)

In general, the Riccati equations in these filters can be difficult to solve. However, the solution can be obtained by the eigenvector method shown in [YaeSl]. (This is similar to the Hamiltonian approach to steady-state Kalman filtering described in Section 7.3.3.) Define the 2n x 2n matrix ] (11.134)

*Note that F-l should always exist if it comes from a real system, because F comes* from a matrix exponential that is always invertible (see Sections 1.2 and 1.4). Compute the n eigenvectors of 'FI that correspond to the eigenvalues outside the 
# unit circle. Denote those eigenvectors as & (i = 1, . . . , n). Form the 2n x n matrix


*FT + HTHF-l* *OFTLTL - HTHF-l(I - t9LTL)* 'H= [ -F-l **P(I** *- eLTL)*

(11.135)

*where X i  and X2 are n x n matrices. The P matrix used in the a priori H,* filter can be computed as *P = X2X,l* (11.136)

*For the a posteriori fdter, define the 2n x 2n matrix*

1 *ii = [ F-T* *F-T(HTH - BLTL)* *F-T* *F + F-T(HTH - BLTL)* (11.137)


## Compute the n eigenvectors of I? that correspond to the eigenvalues outside the
 
# unit circle. Denote those eigenvectors as & (i = 1, . . . , n). Form the 2n x n matrix


(11.138)

where 
## and x2 are n x n matrices. The f' matrix used in the a posteriori H,
 **filter can be computed as** 
## p = x2x,1
 (11.139)

The eigenvector method for the Riccati equation solutions works because 'H and *7? are symplectic matrices (see Section 7.3.3 and Problem 11.9). This assumes* *that F is nonsingular and that 'H and fi do not have any eigenvalues on the unit* circle. If these assumptions are violated, then the problem becomes more compli- **cated [YaeSl]. A method similar to this for continuoustime systems is developed** in [Naggl]. **It is important to be aware that the P and p solutions given by Equations (11.136)** and (11.139) only give one solution each to Equations (11.131) and (11.132). Equ& tions (11.136) and (11.139) may give solutions to Equations (11.131) and (11.132) that are not positive definite and therefore do not satisfy the H, filtering problem. However, that does not prove that the H, filtering solution does not exist (see Problem 11.13).

---

**367**

**EXAMPLE 11.5**

We will revisit Example 11.2, but assume that the initial state is 0:

(1 1.140)

From Equation (11.131) we can find the a prioristeady-state filter that bounds **the infinity-norm of the transfer function from e to 2 by l/&. (Recall that** ek = [ 'Wk *Vk ] T . )  The algebraic Riccati equation associated with this prob-* lem is given by

P = 1 + P - ~ ( i + P)-+ + p ( i / e  + P)-+

P 2 P 2 1 + P  l/O+P = 1+P--+-

Solving the above for P we obtain

*-e - 1 f* 
# Je2 - 68 + 5
 2(2e - 1) P =

(11.141)

(11.142)

In order for the solution of this equation to solve the H, filtering problem, 
## we must have P > 0. The only solution for which P > 0 is when 0 5 0 < 1/2
 and when we use the negative sign in the above s~lution.~ If we choose 
## 0 = 1/10 then P = 2. The gain of the a priori filter is then computed from
 Equation (11.131) as

*K* = P ( l + P ) - - l = 2/3 (1 1.143)


## Note that the P value t h t  i's obtained for 8 = 1/10 does not match Ex-
 ample 11.2, but K does match. The H, filter equation is computed from **Equation (11.131) as**

?k+l = ?k + K(Yk - ?k) = i k  + (2/3)(yk - 5k) (1 1.144)

vvv


## 11.6
 
## SUMMARY


**In this chapter, we have presented a couple of different approaches to H,** esti- mation, also called minimax estimation. H, filtering minimizes the worst-case


## 5Note that Example 11.2 showed that this problem has a solution for 0 5 8 < 1, which indicates
 **that the game theory approach to H,** filtering may be more general than the transfer function approach.

---

**368**

estimation error and is thus more robust than Kalman filtering, which minimizes the RMS estimation error. H, filtering has sometimes been criticized for being too pessimistic in its assumption about t-he noise processes that impinge on the system and measurement equations. After all, H, estimation assumes that the noise is worst case, thus attributinga degree of perversity to the noise that intuitively seems unrealistic. This has led to mixed Kalman/H, estimation techniques, which we will discuss in Chapter 12. Research in H, estimation began in the 1980s. During that decade, some work was directed toward the design of minimax state estimators for systems corrupted by random noise whose covariances were within known bounds [POOH, Dar84, Ver841. This was a first step toward H, filtering, although it still assumed that the noise was characterized by statistical measurements. The earliest work that could pass for what we now call H, filtering was probably published by Mike Grimble [Gri88]. However, unlike the presentation in this chapter, he used a frequency domain ap- proach. He designed a state estimator such that the frequency response from the noise to the estimation error had a user-defined upper bound. Some early tutorials on H, filtering can be found in [Griglb, Sha921. A poly- nomial systems approach to H, filtering is presented in [GriSO]. Nonlinear H, filtering is discussed in [Rei99], where a stable state estimator with a bounded infinity-norm is derived. System identification using H, methods is discussed in [Sto94, Tse94, Bai95, Did95, Pan961. The effectiveness of the H, filter can be highly sensitive to the weighting func- 
## tions [e.g., &, Po, Qk, and Rk in Equation (11.36), and 8 in the performance
 bound]. This sometimes makes H, filter design more sensitive than Kalman filter design (which is ironic, considering the higher degree of robustness in H, filter- ing). The advantages of H, estimation over Kalman filtering can be summarized **as follows.**

1. H, filtering provides a rigorous method for dealing with systems that have model uncertainty.

2. H, filtering provides a natural way to limit the frequency response of the estimator.

The disadvantages of H, filtering compared to Kalman filtering can be summarized **as follows.**

1. The filter performance is more sensitive to the design parameters.

**2. The theory underlying H,** filtering is more abstract and complicated.

The types of applications where H, filtering may be preferred over Kalman filtering could include the following.

1. Systems in which stability margins must be guaranteed, or worst-case esti- mation performance is a primary consideration (rather than RMS estimation performance) [Sim96] .

2. Systems in which the model changes unpredictably, and identification and gain scheduling are too complex or time-consuming.

3. Systems in which the model is not well known.

---

**369**

Work by Babak Hassibi, Ali Sayed, and Thomas Kailath involves the solution of state estimation problems within the context of Krein spaces (as opposed to the usual Hilbert space approach). This provides a general framework for both Kalman and H, filtering (along with other types of filtering), and is discussed in some of their papers [Has96a, Has96bI and books [Has99, KaiOO].

PROBLEMS

**Written exercises**

**11.1**

**11.2** *measurement noise variances Q and R. Suppose a state estimator of the form*


# Show that ( I  + A)-lA = A(I + A)-1.


## Consider a scalar system with F = H = 1 and with process noise and


**?;+I** 
# = 2; + K(yk - 2;)


*is used to estimate the state, where K is a general estimator gain.* *a) Find the optimal gain K if R = 2Q. Call this gain KO. What is the* *resulting steady-state a priori estimation-error variance?* *b) Suppose that R = 0. What is the optimal steady-state a priori estimation-* *error variance? What is the (suboptimal) steady-state a priori estimation-* *error variance if KO is used in the estimator? Repeat for R = Q and* *R = 5Q.*


## 11.3 Consider a scalar system with F = H = 1 and with process noise and
 *measurement noise variances Q and R = 2Q.* **A Kalman filter is designed to** estimate the state, but (unknown to the engineer) the process noise has a mean of a. *a) What is the steady-state value of the mean of the a priori estimation error?* b) Introduce a new state-vector element that is equal to a. Augment the new state-vector element to the original system so that a Kalman filter can be used to estimate both the original state element and the new state element. *Find an analytical solution to the steady-state a priori estimation-error* covariance for the augmented system.

Suppose that a Kalman filter is designed to estimate the state of a scalar **11.4** system. The assumed system is given as


## where Wk N (0, Q )  and V k  N (0, R) _are uncorrelated zero-mean white noise pro-
 
# cesses. The actual system matrix is F = F + AF.
 *a) Under what conditions is the mean of the steady-state value of the a priori* state estimation error equal to zero? *b) What is the steady-state value of the a priori estimation-error variance P?* **How much larger is P because of the modeling error AF?**

---


[Image on page 38]


**370**


# 11.5 Find the stationary point of (2s + 2122 + 2223) subject to the constraint


# Maximize (142 - x2 + 6y - y2 + 7) subject to the constraints ( x  + y 5 2)


# ( X I  + 22 = 4) [MooOO].


**11.6** 
# and ( x  + 2y 5 3) [Lue84].


**11.7 Consider the system**

**1** **xk** 
## = s x k - 1  -k wk-1


## Y k  = xk +vk


Note that this is the system model for the radiation system described in Prob- **lem 5.1.** **a) Find the steady-state value of Pk for the H,** filter, using a variable 8 and

**b) Find the bound on f3 such that the steady-state H,** filter exists.

**11.8 Suppose that you use a continuous-time H,** filter to estimate a constant on the basis of noisy measurements. The measurement noise is zero-mean and white *with a covariance of R. Find the H,* **estimator gain as a function of PO, R, 8, and** *time. What is the limit of the estimator gain as t + oo? What is the maximum* value of 8 such that the H, estimation problem has a solution? How does the value of 8 influence the estimator gain?

**11.9**

**11.10 Prove that the solution of the a posteriori H,** Riccati equation given in 
## Equation (11.132) with 6' = 0 is equivalent to the solution of the steady-state a
 *priori Kalman filter Riccati equation with R = I and Q = I.*


## 11.11 Prove that C in Equation (11.132) with 8 = 0 is equivalent to the solution
 *of the steady-state a posteriori Kalman filter Riccati equation with R = I and* *Q = I.*

**11.12 Find the a posteriori steady-state H,** 
## filter for Example 11.5 when f3 =
 **1/10, Verify that the a priori and a posteriori Riccati equation solutions satisfy** **Equation (11.133).**

**11.13 Find all possible solutions P to the a priori H,** filtering problem for Ex- 
## ample 11.5 when 8 = 0. Next use Equation (11.139) to find the P solution. Repeat
 
## for f3 = 1/10. [Note that Equation (11.139) gives a negative solution for P and
 therefore cannot be used.]


## L = R =  Q =  S =  1.


## Prove that 3-1 and 7? in Equations (11.134) and (11.137) are symplectic.


**Computer exercises**


## 11.14 Generate the time-varying solution to Pk for Problem 11.7 with PO = 1.
 
## What is the largest value of 6' for which Equation (11.90) will be satisfied for all k
 
## up to and including k = 20? Answer to the nearest 0.01. Repeat for k = 10, k = 5,
 
## and k = 1.


**11.15 Consider the vehicle navigation problem described in Example 7.12. De-** sign a Kalman filter and an H, filter to estimate the states of the system. Use the

---


[Image on page 39]


**371**

following parameters.

*T* *=* *3*


## uk = 1


Q = diag(4,4,1,1) *R = diag(900,900)* heading angle = 0 . 9 ~ **T** z(0) = q o )  = [ 0 0 0 0 ]

Simulate the system and the filters for 300 seconds. In the H, *filter use S = L = I* *and 6' = 0.0005.* **a) Plot the position estimation errors for the Kalman and H,** filters. What are the RMS position estimation errors for the two filters? 
## b) Now suppose that unknown to the filter designer, Uk = 2. Plot the position
 estimation errors for the Kalman and H, filters. What are the RMS position estimation errors for the two filters?


## c) What are the closed loop estimator eigenvalues for the Kalman and H,
 filters? Do their relative magnitudes agree with your intuition? **d) Use MATLAB's DARE function to find the largest 6' for which a steady-** state solution exists to the H, DARE. Answer to the nearest 0.0001. How well does the H, *filter work for this value of 6'? What are the closed-loop* eigenvalues of the H, 
## filter for this value of O?
