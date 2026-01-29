---
type: chapter
chapter: 11
title: The H∞ filter
---
# Chapter 11 The H, Filter

[Kalman filtering] assumes that the message generating process has a known dynamics and that the exogenous inputs have known statistical properties. Unfortunately, these assumptions limit the utility of minimum variance estimators in situations where the message model and/or the noise descriptions are unknown. 

-Uri Shaked and Yahali Theodor [Sha92] 
As we have seen in earlier chapters, the Kalman filter is an effective tool for estimating the states of a system. The early success in the 1960s of the Kalman filter in aerospace applications led to attempts to apply it to more common industrial applications in the 1970s. However, these attempts quickly made it clear that a serious mismatch existed between the underlying assumptions of Kalman filters and industrial state estimation problems. Accurate system models are not as readily available for industrial problems. The government spent millions of dollars on the space program in the 1960s (hence the accurate system models), but industry rarely has millions of dollars to spend on engineering problems (hence the inaccurate system models). In addition, engineers rarely understand the statistical nature of the noise processes that impinge on industrial processes. After a decade or so of reappraising the nature and role of Kalman filters, engineers realized they needed a new filter that could handle modeling errors and noise uncertainty. State estimators that can tolerate such uncertainty are called robust. Although robust estimators based on Kalman filter theory can be designed **(as** seen in Section 10.4), 
these approaches are somewhat ad-hoc in that they attempt to modify an already existing approach. The H, filter was specifically designed for robustness. 

In Section 11.1 we derive a different form of the Kalman filter and discuss the limitations of the Kalman filter. Section 11.2 discusses constrained optimization using Lagrange multipliers, which we will need later for our derivation of the H, 
filter. In Section 11.3 we use a game theory approach to derive the discretetime H, filter, which minimizes the worst-case estimation error. This is in contrast to the Kalman filter's minimization of the expected value of the variance of the estimation error. Furthermore, the H, filter does not make any assumptions about the statistics of the process and measurement noise (although this information can be used in the H, filter if it is available). Section 11.4 presents the continuous-time H, filter, and Section 11.5 discusses an alternative method for deriving the H, filter using a transfer function approach. 

## 11.1 **Introduction**

In this section we will first derive an alternate form for the Kalman filter. We do this to facilitate comparisons that we will make later in this chapter between the Kalman and H, filters. After we derive an alternate Kalman filter form, we will briefly discuss the limitations of the Kalman filter. 

## 11.1.1 An Alternate Form For The Kalman Filter

Recall that the Kalman filter estimates the state of a linear dynamic system defined by the equations 

$$\begin{array}{rcl}\mathcal{I}_{k+1}&=&F_{k}x_{k}+w_{k}\\ y_{k}&=&H_{k}x+v_{k}\end{array}\tag{11.1}$$

where *{wk}* and *{Vk}* are stochastic processes with covariances Qk and **Rk,** respectively. As derived in Section 5.1, the Kalman filter equations are given as follows: 

$$\hat{x}_{k+1}^{-}=F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})$$ $$K_{k}=P_{k}^{-}H_{k}^{T}(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}$$ $$P_{k}^{-}=F_{k-1}P_{k-1}^{+}F_{k-1}^{T}+Q_{k-1}$$ $$P_{k}^{+}=(I-K_{k}H_{k})P_{k}^{-}\tag{11.2}$$
$$(H_{k}P_{k}^{-}H_{k}^{T}+R_{k})^{-1}=R_{k}^{-1}-R_{k}^{-1}H_{k}({\cal I}_{k}^{-}+H_{k}^{T}R_{k}^{-1}H_{k})^{-1}H_{k}^{T}R_{k}^{-1}\tag{11.3}$$ $$=R_{k}^{-1}-R_{k}^{-1}H_{k}(I+P_{k}^{-}H_{k}^{T}R_{k}^{-1}H_{k})^{-1}P_{k}^{-}H_{k}^{T}R_{k}^{-1}$$

Using the matrix inversion lemma from Section 1.1.2 we see that where Zk is the information matrix (i.e., the inverse of the covariance matrix *Pk).* The Kalman gain can therefore be written as follows: 

$$\begin{array}{r l}{K_{k}}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\\ {}&{{}=}\end{array}$$
P H (HkP H H + Rk) -1 B2 H2 B2, - L2 H2 B2, H2(1 + B2 H2 B2, H2 B2, [1 - P = H + B = H = (1 + B = H = B = H = ] P = H ; B = ] [(1 + B + H B B 2 Hx) - B - H + B - H + B - H - B - H - B - H - B - (I + P H R R H R ) - 1 P H R R 1 (11.4)
Substituting this into the expression for Px+1 in Equation (11.2) we get

$$P_{k+1}^{-}$$
= FkP F F + Qk Fk (I - Kk Hk) Px F + Qk FxPx Fx - FxKkHkPx Fx + Qk == Fr P2 E2 - E2 (1 + B2 H2 B2, H2) - } P2 H2 B2, HrB2 F2 + Of Fr P = Fk(In + HE B2 Hk) -1 H2 B2 Hk P2 + Qk (11.5) ==
Apply the matrix inversion lemma again to the inverse on the right side of the above equation to obtain

$$P_{k+1}^{-}$$
= FkPx Ff - Fx [P, - Px H2 (Rk + HkPx H2 )-1HkP2 ] H2 Rx + HkPx Fx + Qk FkPE [I - H] RE HkPi + == H2 (Rk + HkPz H2 )-1 HkP Hk Rz Hk Pk] Fx + Qk Fk Px TxFf + Qk (11.6)  11
where Tk is defined by the above equation. Apply the matrix inversion lemma to the inverse that is in Tk to obtain

Tk = 1 - H; Rx HxPx + HE [RT - RE HK(TE + HE RT-Hk)- +H2 RT ] HkPT H2 RT HkPk I - H2 R2 HkPx + (H2 RE HkPx )2 - ll HE RE Hk (TE + H& RE Hk)-1 (Hx RE HkPr )2 I - H2 R2 HkPx + (Hk Rx 1 HkPx )2 -  ll HE B2 Hx P2 (1 + H2 R2, HxB2 )- ) (H2 B2 )2 I - HE RT HkP + + (Hk Rx HkPr )2 -  II (HT RE Hr B2 )3(I + HE BE 1 HkP2 )-1 [(1 + H2 R2 Hk P2 ) - H2 B2 Hk P2 (1 + H2 B2 ) + ll (H) Bx +HkP2 )2(1 + H2 R2 H2 P2 ) - (H2 B2 HkP2 )3] × (I + H R R - H R P ) - 3 = (I + H R R ] HkP )-1 (11.7)
Substituting this expression for Tk into Equation (11.6) gives

$$P_{k+1}^{-}=F_{k}P_{k}^{-}\,(I+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}^{-})^{-1}F_{k}^{T}+Q_{k}$$
$$(11.8)$$

From Equation (11.4) the Kalman gain can be written as 

$$K_{k}=(I+P_{k}^{-}H_{k}^{T}R_{k}^{-1}H_{k})^{-1}P_{k}^{-}H_{k}^{T}R_{k}^{-1}$$

We can premultiply outside the parentheses by PL , and postmultiply each term inside the parenthesis by *Pi,* to obtain 

$$K_{k}=P_{k}^{-}\,(P_{k}^{-}+P_{k}^{-}H_{k}^{T}R_{k}^{-1}H_{k}P_{k}^{-})^{-1}P_{k}^{-}H_{k}^{T}R_{k}^{-1}$$

We can postmultiply outside the parentheses by the inverse of *Pi,* and premultiply each term inside the parentheses by the inverse of P;, to obtain 

$$K_{k}=P_{k}^{-}\,(I+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}^{-})^{-1}H_{k}^{T}R_{k}^{-1}$$
$$\begin{array}{r c l}{{\hat{x}_{k+1}^{-}}}&{{=}}&{{F_{k}\hat{x}_{k}^{-}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k}^{-})}}\\ {{}}&{{}}&{{}}\\ {{K_{k}}}&{{=}}&{{P_{k}^{-}(I+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}^{-})^{-1}H_{k}^{T}R_{k}^{-1}}}\\ {{P_{k+1}^{-}}}&{{=}}&{{F_{k}P_{k}^{-}(I+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}^{-})^{-1}F_{k}^{T}+Q_{k}}}\end{array}$$

Combining this expression for Kk with Equations (11.2) and (11.8) we can summarize the Kalman filter as follows: 

$$(11.9)$$
$$(11.10)$$
$$(11.11)$$
$$(11.12)$$

## 11.1.2 Kalman Filter Limitations

The Kalman filter works well, but only under certain conditions. 

First, we need to know the mean and correlation of the noise Wk and vk at each time instant. 

Second, we need to know the covariances Qk and Rk of the noise processes. The Kalman filter uses Qk *and* Rk as design parameters, so if we do not know QI, and RI, then it may be difficult to successfully use a Kalman filter. 

Third, the attractiveness of the Kalman filter lies in the fact that it is the one estimator that results in the smallest possible standard deviation of the estimation error. That is, the Kalman filter is the minimum variance estimator if the noise is Gaussian, and it is the linear minimum variance estimator if the noise is not Gaussian. If we desire to minimize a different cost function (such as the worst-case estimation error) then the Kalman filter may not accomplish our objectives. 

0 Finally, we need to know the system model matrices Fk and *Hk.* 
So what do we do if one of the Kalman filter assumptions is not satisfied? What should we do if we do not have any information about the noise statistics? What should we do if we want to minimize the worst-case estimation error rather than the covariance of the estimation error? 

Perhaps we could just use the Kalman filter anyway, even though its assumptions are not satisfied, and hope for the best. That is a common solution to our Kalman filter quandary and it works reasonably well in many cases. However, there is yet another option that we will explore in this chapter: the H, filter, also called the minimax filter. The H, filter does not make any assumptions about the noise, and it minimizes the worst-case estimation error (hence the term minimax). 

## 1 1.2 Co N St R A I N Ed 0 Pti M **I 2 At1** 0 N

In this section we show how constrained optimization can be performed through the use of Lagrange multipliers. This background is required for the solution of the H, filtering problem that is presented in Section 11.3. In Section 11.2.1 we will investigate static problems (i.e., problems in which the independent variables are constant). In Section 11.2.2 we will take a brief segue to look at problems with inequality constraints. In Section 11.2.3 we will extend our constrained optimization method to dynamic problems (i.e., problems in which the independent variables change with time). 

## 11.2.1 Static Constrained Optimization

Suppose we want to minimize some scalar function J(x, w) with respect to x and w. x is an n-dimensional vector, and w is an rn-dimensional vector. w is the independent variable and x is the dependent variable; that is, x is somehow determined by w. Suppose our vector-valued constraint is given as f(x, w) = 0. Further mume that the dimension of f(x, w) is the same as the dimension of x. This problem can be written as 

$$\operatorname*{min}_{x,w}J(x,w){\mathrm{~such~that~}}f(x,w)=0$$
$$(11.13)$$

Suppose that the constrained minimum of J(x, w) occurs at x = x* and w = w*. 

We call this the stationary point of J(x, w). Now suppose that we choose values of x and w such that x is close to x*, w is close to w*, and f(x, w) = 0. Expanding J(x, w) and f(x, w) in a Taylor series around x* and w* gives 

$$J(x,w)=J(x^{\star},w^{\star})+\left.\frac{\partial J}{\partial x}\right|_{x^{\star},w^{\star}}\Delta x+\left.\frac{\partial J}{\partial w}\right|_{x^{\star},w^{\star}}\Delta w$$ $$f(x,w)=f(x^{\star},w^{\star})+\left.\frac{\partial f}{\partial x}\right|_{x^{\star},w^{\star}}\Delta x+\left.\frac{\partial f}{\partial w}\right|_{x^{\star},w^{\star}}\Delta w\tag{11.14}$$

where higher-order terms have been neglected (with the assumption that x is close to x*, and w is close to w*), Ax = x - x*, and Aw = w - w*. These equations can be written as 

$$\Delta J(x,w)=J(x,w)-J(x^{\star},w^{\star})\tag{11.15}$$ $$=\left.\frac{\partial J}{\partial x}\right|_{x^{\star},w^{\star}}\Delta x+\left.\frac{\partial J}{\partial w}\right|_{x^{\star},w^{\star}}\Delta w$$ $$\Delta f(x,w)=f(x,w)-f(x^{\star},w^{\star})$$ $$=\left.\frac{\partial f}{\partial x}\right|_{x^{\star},w^{\star}}\Delta x+\left.\frac{\partial f}{\partial w}\right|_{x^{\star},w^{\star}}\Delta w$$

Now note that for values of x and w that are close to x* and w*, we have A J(x, w) = 
0. This is because the partial derivatives on the right side of the AJ(x, w) equation are zero at the stationary point of J(x, w). We also see that Af(x, w) = 0 at the stationary point of J(x, w). This is because f(x*, w*) = 0 at the constrained stationary point of J(x, w), and we chose x and w such that f(x, w) = 0 also. The above equations can therefore be written as 

$$\left.{\frac{\partial J}{\partial x}}\right|_{x^{\bullet},w^{\bullet}}$$ $$\left.{\frac{\partial f}{\partial x}}\right|_{x^{\bullet},w^{\bullet}}$$
$\begin{array}{c|cccc}\partial J&\Delta w&=&0\\ \hline\partial w&_{x^{*},w^{*}}&\\ \partial f&\Delta w&=&0\\ \hline\partial w&_{x^{*},w^{*}}&\\ \end{array}$
$$\Delta x+$$  $$\Delta x+$$
$$\left.{\frac{\partial f}{\partial x}}\right|_{x^{\star},w^{\star}}\right)^{-1}\left.{\frac{\partial f}{\partial w}}\right|_{z^{\star},w^{\star}}\Delta w$$
$$\Delta x=-\left(\right)$$

These equations are true for arbitrary x and w that are close to x* and w* and that satisfy the constraint *f(x, w)* = 0. Equation (11.16) can be solved for Ax as 

$$(11.17)$$
$$(11.18)$$
This can be substituted into Equation (11.16) to obtain 
$\left.\frac{\partial J}{\partial w}\right|_{x^{\star},w^{\star}}-\left.\frac{\partial J}{\partial x}\right|_{x^{\star},w^{\star}}\left(\left.\frac{\partial f}{\partial x}\right|_{x^{\star},w^{\star}}\right)^{-1}\left.\frac{\partial f}{\partial w}\right|_{x^{\star},w^{\star}}=0$  combined with the constraint $f(x,w)=0$, gives us $(m+m)$ a 
This equation, combined with the constraint *f(s,* w) = 0, gives us *(m+n)* equations that can be solved for the vectors w and x to find the constrained stationary point of J(x, *w).* 
Now consider the augmented cost function 

$$J_{a}=J+\lambda^{T}f$$
Ja = *J+ATf* (1 1.19) 
where A is an n-element unknown constant vector called a Lagrange multiplier. 

Note that 

$$\begin{array}{r c l}{{\frac{\partial J_{a}}{\partial x}}}&{{=}}&{{\frac{\partial J}{\partial x}+\lambda^{T}\frac{\partial f}{\partial x}}}\\ {{\frac{\partial J_{a}}{\partial w}}}&{{=}}&{{\frac{\partial J}{\partial w}+\lambda^{T}\frac{\partial f}{\partial w}}}\\ {{\frac{\partial J_{a}}{\partial\lambda}}}&{{=}}&{{f}}\end{array}$$
$$(11.19)$$

$$(11.20)$$

If we set all three of these equations equal to zero then we have 

$$\lambda^{T}=\frac{-\partial J}{\partial x}\left(\frac{\partial f}{\partial x}\right)^{-1}$$ $$\frac{\partial J}{\partial w}-\frac{\partial J}{\partial x}\left(\frac{\partial f}{\partial x}\right)^{-1}\frac{\partial f}{\partial w}=0$$ $$f=0\tag{11.21}$$

The first equation gives us the value of the Lagrange multiplier, the second equation is identical to Equation (11.18), and the third equation forces the constraint to be satisfied. We therefore see that we can solve the original constrained problem by creating an augmented cost function *Ja,* taking the partial derivatives with respect to *x, w,* and A, setting them equal to zero, and solving for *x, w,* and A. The partial derivative equations give us (271 + m) equations to solve for the n-element vector x, the m-element vector w, and the n-element vector A. We have increased the dimension of the original problem by introducing a Lagrange multiplier, but we have transformed the constrained optimization problem into an unconstrained optimization problem, which can simplify the problem considerably. 

## Example 11.1

Suppose we need to find the minimum of J(x, u) = x2/2 + xu + u2 + u with respect to z and u such that *f(z,* u) = x - 3 = 0. This simple example can be solved by simply realizing that x = 3 in order to satisfy the constraint. Substituting z = 3 into J(x, u) gives J(x, u) = 9/2 + 4u + u2. Setting the derivative with respect to u equal to zero and solving for u gives u = -2. 

We can also solve this problem using the Lagrange multiplier method. We create an augmented cost function as 

$$J_{a}=J+\lambda^{T}f\tag{11.22}$$ $$=x^{2}/2+xu+u^{2}+u+\lambda(x-3)$$

The Lagrange multiplier X has the same dimension as z (scalar in this example). The three necessary conditions for a constrained stationary point of J 
are obtained by setting the partial derivations of Equation (11.20) equal to 0. 

$$\begin{array}{r c l}{{\frac{\partial J_{a}}{\partial x}}}&{{=}}&{{x+u+\lambda=0}}\\ {{\frac{\partial J_{a}}{\partial u}}}&{{=}}&{{x+2u+1=0}}\\ {{\frac{\partial J_{a}}{\partial\lambda}}}&{{=}}&{{x-3=0}}\end{array}$$

$$(11.23)$$
dX - - x+2u+l=O 
-- (11.23) 
Solving these three equations for x, u, and X gives x = 3, u = -2, and X = 
-1. In this example the Lagrange multiplier method seems to require more effort than simply solving the problem directly. However, in more complicated constrained optimization problems the Lagrange multiplier method is essential for finding a solution. 

vvv 

## 11.2.2 Inequality Constraints

Suppose that we want to minimize a scalar function that is subject to an inequality constraint: 
min J(x) such that f(x) 5 0 (11.24) 
This can be reduced to two minimization problems, neither of which contain inequality constraints. The first minimization problem is unconstrained, and the second minimization problem has an equality constraint: 

$$(11.24)$$

1. minJ(z) 
2. min J(z) such that *f(z)* = 0 In other words, the optimal value of z is either not on the constraint boundary 
[i.e., f(x) < 01, or it is on the constraint boundary [i.e., f(x) = 01. If it is not on the constraint boundary then f(x) < 0 and the optimal value of x is obtained by solving the problem without the constraint. If it is on the constraint boundary then *f(z)* = 0 at the constrained minimum, and the optimal value of x is obtained by solving the problem with the equality constraint f(x) = 0. 

The procedure for solving Equation **(11.24)** involves solving the unconstrained problem first. Then we check to see if the unconstrained minimum satisfies the constraint. If the unconstrained minimum satisfies the constraint, then the unconstrained minimum solves the inequality-constrained minimization problem and we are done. However, if the unconstrained minimum does not satisfy the constraint, then the minimization problem with the inequality constraint is equivalent to the minimization problem with the equality constraint. So we solve the problem with the equality constraint *f(z)* = 0 to obtain the final solution. This is illustrated for the scalar case in Figure 11.1. 

![7_image_0.png](7_image_0.png)

![7_image_1.png](7_image_1.png)

-2 -1.5 -1 -0.5 0 0.5 1 1.5 2 
Figure 11.1 This illustrates the constrained minimization of **z2.** If the constraint is z - 1 5 0, then the constrained minimum is equal to the unconstrained minimum and occurs at z = 0. If the constraint is x + 1 5 0, then the constrained minimum can be solved by enforcing the equality constraint x + 1 = 0 and occurs at 2 = -1. 
When we extend this idea to more than one dimension, we obtain the following procedure, which is called the active-set method for optimization with inequality constraints [Fle81, Gi1811. 

1. The problem is to minimize J(z) such that *f(z)* 5 0, where *f(z)* is an melement constraint function and the inequality is taken one element at a time. 

2. First solve the unconstrained minimization problem. If the unconstrained solution satisfies the constraint *f(z)* 5 0 then the problem is solved. If not, continue to the next step. 

3. For all possible combinations of constraints, solve the problem using those constraints as equality constraints. If the solution satisfies the remaining (unused) constraints, then the solution is feasible. Note that this step requires the solution of **(2.'** - 1) constrained optimization problems. 

4. Out of all the feasible solutions that were obtained in the previous step, the one with the smallest J(z) is the solution to the constrained minimization problem. 

Note that there are also other methods for solving optimization problems with inequality constraints, including primal-dual interior-point methods [Wri97]. 

## 11.2.3 Dynamic Constrained Optimization

In this section we extend the Lagrange multiplier method of constrained optimization to the optimization of dynamic systems. Suppose that we have a dynamic system given as 

$$x_{k+1}=F_{k}x_{k}+w_{k}\ \ \ \ (k=0,\cdots,N-1)$$

where Xk is an n-dimensional state vector. We want to minimize the scalar function 

$$(11.25)$$
$$J=\psi(x_{0})+\sum_{k=0}^{N-1}{\mathcal{L}}_{k}$$
$$(11.26)$$

where *$(xo)* is a known function of 20, *and* ek is a known function of Xk and *Wk.* This is a constrained dynamic optimization problem similar to the type that arises in optimal control [Lew86a, Ste941. It is slightly different than typical optimal control problems because *$(Xk)* in the above equation is evaluated at the initial time *(Ic* = 0) instead of the final time (k = *N),* but the methods of optimal control can be used with only slight modifications to solve our problem. The constraints are given in Equation (11.25). From the previous section we know that we can solve this problem by introducing a Lagrange multiplier A, creating an augmented cost function *Ja,* and then setting the partial derivatives of J, with respect to Xk, Wk, and X equal to zero. Since we have N constraints in Equation (11.25) (each of dimension *n),* we have to introduce N Lagrange multipliers *XI,* . a, AN (each of dimension n). The augmented cost function is therefore written as 

$$J_{a}=\psi(x_{0})+\sum_{k=0}^{N-1}\left[{\cal L}_{k}+\lambda_{k+1}^{T}(F_{k}x_{k}+w_{k}-x_{k+1})\right]\tag{11.27}$$

This can be written as 

$$J_{a}=\psi(x_{0})+\sum_{k=0}^{N-1}\left[\mathcal{L}_{k}+\lambda_{k+1}^{T}(F_{k}x_{k}+w_{k})\right]-\sum_{k=0}^{N-1}\lambda_{k+1}^{T}x_{k+1}\tag{11.28}$$ $$=\psi(x_{0})+\sum_{k=0}^{N-1}\left[\mathcal{L}_{k}+\lambda_{k+1}^{T}(F_{k}x_{k}+w_{k})\right]-\sum_{k=0}^{N}\lambda_{k}^{T}x_{k}+\lambda_{0}^{T}x_{0}$$
$${\mathcal{H}}_{k}={\mathcal{L}}_{k}+\lambda_{k+1}^{T}(F_{k}x_{k}+w_{k})$$

where A0 is now an additional term in the Lagrange multiplier sequence. It is not in the original augmented cost function, but we will see in Section 11.3 that its value will be determined when we solve the constrained optimization problem. Now we define the Hamiltonian *'Flk* as 

$$(11.29)$$

With this notation we can write the augmented cost function as follows. 

$$\begin{array}{r l}{J_{a}}&{{}=}\\ {}&{{}}\\ {}&{{}}\\ {}&{{}}\end{array}$$
$$\psi(x_{0})+\sum_{k=0}^{N-1}{\cal H}_{k}-\sum_{k=0}^{N}\lambda_{k}^{T}x_{k}+\lambda_{0}^{T}x_{0}$$ $$\psi(x_{0})+\sum_{k=0}^{N-1}{\cal H}_{k}-\sum_{k=0}^{N-1}\lambda_{k}^{T}x_{k}-\lambda_{N}^{T}x_{N}+\lambda_{0}^{T}x_{0}$$ $$\psi(x_{0})+\sum_{k=0}^{N-1}\left({\cal H}_{k}-\lambda_{k}^{T}x_{k}\right)-\lambda_{N}^{T}x_{N}+\lambda_{0}^{T}x_{0}\tag{11.30}$$

The conditions that are required for a constrained stationary point are

$$\begin{array}{r l}{{\frac{\partial J_{a}}{\partial x_{k}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial w_{k}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial\lambda_{k}}}}&{{}=}\end{array}$$
$\begin{array}{ll}\mbox{\rm(}k=0,\cdots,N\mbox{\rm)}\\ \mbox{\rm(}k=0,\cdots,N-1\mbox{\rm)}\\ \mbox{\rm(}k=0,\cdots,N\mbox{\rm)}\end{array}$ (11.31)
These conditions can also be written as

$$\begin{array}{r l}{{\frac{\partial J_{a}}{\partial x_{0}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial x_{N}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial x_{k}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial w_{k}}}}&{{}=}\\ {{\frac{\partial J_{a}}{\partial\lambda_{k}}}}&{{}=}\end{array}$$
$$=0$$ $$=0$$ $$=0\quad(k=1,\cdots,N-1)$$ $$=0\quad(k=0,\cdots,N-1)$$ $$=0\quad(k=0,\cdots,N)\tag{11.32}$$

The fifth condition ensures that the constraint xk+1 = Fxx + wk is satisfied. Based on the expression for Ja in Equation (11.30), the first four conditions above can be written as

$$\lambda_{0}^{T}+$$
$$\begin{array}{lcl}\partial\psi_{0}&=&0\\ \partial x_{0}&=&0\\ -\lambda_{N}^{T}&=&0\\ \lambda_{k}^{T}&=&\frac{\partial{\cal H}_{k}}{\partial x_{k}}\ \ \ \ (k=1,\cdots,N-1)\\ \partial{\cal H}_{k}&=&0\ \ \ \ (k=0,\cdots,N-1)\\ \partial w_{k}&=&0\ \ \ \ (k=0,\cdots,N-1)\end{array}\tag{11.33}$$

This gives us the necessary conditions for a constrained stationary point of our dynamic optimization problem. These are the results that we will use to solve the Hoo estimation problem in the next section.

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F_{k}x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\end{array}$$

## 11.3 **A Game Theory Approach To H, Filtering**

The H, solution that we present in this section was originally developed by Ravi Banavar [Ban921 and is further discussed in [She95, She971. Suppose we have the standard linear discrete-time system 

$$(11.34)$$
$$(11.35)$$

where Wk and Wk are noise terms. These noise terms may be random with possibly unknown statistics, or they may be deterministic. They may have a nonzero mean. 

Our goal is to estimate a linear combination of the state. That is, we want to estimate **Zk,** which is given by zk = *Lkxk* (11.35) 

$$z_{k}=L_{k}x_{k}$$

where Lk is a user-defined matrix (assumed to be full rank). If we want to directly estimate Xk (as in the Kalman filter) then we set Lk = 1. But in general we may only be interested in certain linear combinations of the state. Our estimate of Zk is denoted &, and our estimate of the state at time 0 is denoted *20.* We want to estimate Zk based on measurements up to and including time (N - 1). In the game theory approach to H, filtering we define the following cost function: 

$$J_{1}=\frac{\sum_{k=0}^{N-1}||z_{k}-\hat{z}_{k}||_{S_{k}}^{2}}{||x_{0}-\hat{x}_{0}||_{P_{0}^{-1}}^{2}+\sum_{k=0}^{N-1}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||v_{k}||_{R_{k}^{-1}}^{2}\right)}\tag{11.36}$$

Our goal as engineers is to find an estimate & that minimizes *J1.* Nature's goal as our adversary is to find disturbances Wk and *Wk,* and the initial state **20,** to maximize J1. Nature's ultimate goal is to maximize the estimation error (Zk - *&).* The way that nature maximizes *(Zk* - &) is by a clever choice of *Wk, Vk,* and *20.* Nature could maximize *(Zk* - &) by simply using infinite magnitudes for *Wk, ?Jk,* 
and *20,* but this would not make the game fair. That is why we define J1 with 
(20 - *20), Wk,* and ?& in the denominator. If nature uses large magnitudes for *'wk,* 
Vk, and xo then *(zk* - &) will be large, but J1 may not be large because of the denominator. The form of J1 prevents nature from using brute force to maximize 
(Zk - *&).* Instead, nature must try to be clever in its choice of *Wk, Vk,* and xo as it tries to maximize (Zk - *&).* Likewise, we as engineers must be clever in finding an estimation strategy to minimize (Zk - *.&).* 
This discussion highlights a fundamental difference in the philosophy of the Kalman filter and the H, filter. In Kalman filtering, nature is assumed to be indifferent. The pdf of the noise is given. We **(as** filter designers) know the pdf of the noise and can use that knowledge to obtain a statistically optimal state estimate. But nature cannot change the pdf to degrade our state estimate. In H, filtering, nature is assumed to be perverse and actively **seeks** to degrade our state estimate as much as possible. Intuition and experience seem to indicate that neither of these extreme viewpoints of nature is entirely correct, but reality probably lies somewhere in the middle. 

lNevertheless, it is advisable to remember the pnnczple of perversity of ananamate objects [BarOl, p. 961 - for instance, when dropping a piece of buttered toast on the floor, the probability is significantly more than 50% that the toast will land buttered-side down. 
Po, Qk, Rk, *and* sk in Equation **(11.36)** are symmetric positive definite matrices chosen by the engineer based on the specific problem. For example, if the user is particularly interested in obtaining an accurate estimate of the third element of *Zk,* then *&(3,3)* should be chosen to be large relative to the other elements of &. If the user knows u *priori* that the second element of the wk disturbance is small, then *Qk(2,2)* should be chosen to be small relative to the other elements of *Qk.* 
In this way, we see that Pi, Qk, *and* Rk are analogous to those same quantities in the Kalman filter, if those quantities are known. That is, suppose that we know that the initial estimation error, the process noise, and the measurement noise are zero-mean. Further suppose that we know their covariances. Then we should use those quantities for Po, *Qk,* and Rk in the H, estimation problem. In the Kalman filter, there is no analogy to the Sk matrix given in Equation **(11.36).** The Kalman filter minimizes the &-weighted sum of estimation-error variances for all positive definite & matrices (see Section *5.2).* But in the H, filter, we will see that the choice of sk affects the filter gain. 

The direct minimization of J1 is not tractable, so instead we choose a performance bound and **seek** an estimation strategy that satisfies the threshold. That is, we will try to find an estimate *,i?k* that results in 

$J_{1}<\frac{1}{\theta}$ (11.37)
where 6' is our user-specified performance bound. Rearranging this equation results in 

$$J=\frac{-1}{\theta}||x_{0}-\hat{x}_{0}||_{F_{0}^{-1}}^{2}+\sum_{k=0}^{N-1}\left[||z_{k}-\hat{z}_{k}||_{S_{k}}^{2}-\frac{1}{\theta}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||v_{k}||_{R_{k}^{-1}}^{2}\right)\right]\tag{11.38}$$ $$<1$$

where J is defined by the above equation. The minimax problem becomes 

$J^{*}=\min\max J$  $\hat{\pi}_{k}$$w_{k},w_{k},\pi_{0}$  $\hat{\pi}_{k}$$w_{k},w_{k},\pi_{0}$ 
$$(11.39)$$
Since Zk = *LkXk,* we naturally choose ik = *Lk2k* and try to find the 2k that minimizes J. This gives us the problem 

$J^{*}=$ min max $J$  $\frac{\partial}{\partial x_{k}}$$w_{k},w_{k},x_{0}$
$$||v_{k}||_{R_{k}^{-1}}^{2}=||y_{k}-H_{k}x_{k}||_{R_{k}^{-1}}^{2}$$
$$(11.40)$$
Since $z_{k}=L_{k}x_{k}$ and $\hat{z}_{k}=L_{k}\hat{x}_{k}$, we see that  $$||z_{k}-\hat{z}_{k}||_{\widehat{S}_{k}}^{2}=(z_{k}-\hat{z}_{k})^{T}S_{k}(z_{k}-\hat{z}_{k})$$ $$=(x_{k}-\hat{x}_{k})^{T}L_{k}^{T}S_{k}L_{k}(x_{k}-\hat{x}_{k})$$ $$=||x_{k}-\hat{x}_{k}||_{\widehat{S}_{k}}^{2}$$
Nature is choosing 20, *wk,* and Vk to maximize J. But 20, *Wk,* and Vk completely 
determine *Yk,* so we can replace the Vk in the minimax problem with *Yk.* We 
therefore have 
$$(11.42)$$
therefore have  $$J^{*}=\min_{\hat{x}_{k}}\max_{w_{k},y_{k},z_{0}}J$$  Since $y_{k}=H_{k}x_{k}+v_{k}$, we see that $v_{k}=y_{k}-H_{k}x_{k}$ and 
$$(11.41)$$
$$(11.43)$$
$$\bar{S}_{k}=L_{k}^{T}S_{k}L_{k}$$
$$(11.44)$$
where sk is defined as We substitute these results in Equation (11.38) to obtain sk = *LrSkLk* ( 11.44) 

$$J=\frac{-1}{\theta}||x_{0}-\hat{x}_{0}||_{F_{0}^{-1}}^{2}+\sum_{k=0}^{N-1}\left[||x_{k}-\hat{x}_{k}||_{S_{k}}^{2}-\frac{1}{\theta}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||y_{k}-H_{k}x_{k}||_{R_{u}^{-1}}^{2}\right)\right]\tag{11.45}$$ $$=\psi(x_{0})+\sum_{k=0}^{N-1}{\cal L}_{k}$$

where **$(Q)** and Lk are defined by the above equation. To solve the minimax problem, we will first find a stationary point of J with respect to xo and *Wk,* and then we will find a stationary point of J with respect to $k and *yk.* 

## 11.3.1 Stationarity With Respect To 20 **And** Wk

The problem in this section is to maximize J = *$(xo)* + cfii Lk (subject to the constraint 2k+1 = Fkxk + *Wk)* with respect to 20 and **Wk.** This is the dynamic constrained optimization problem that we solved in Section 11.2.3. The Hamiltonian for this problem is defined as 

$$(11.46)$$
$${\mathcal{H}}_{k}={\mathcal{L}}_{k}+{\frac{2\lambda_{k+1}^{T}}{\theta}}(F_{k}x_{k}+w_{k})$$

where *2Xk+l/e* is the time-varying Lagrange multiplier that must be computed 
(Ic = **O,-.** , N - 1). Note that we have defined the Lagrange multiplier as **2&+1/0** 
instead of *xk+l.* This does not change the solution to the problem, it simply scales the Lagrange multiplier (in hindsight) by a constant to make the ensuing math more straightforward. From Equation (11.33) we know that the constrained stationary point of J (with respect to xo and *wk)* is solved by the following four equations: 

$$\frac{2\lambda_{0}^{T}}{\theta}+\frac{\partial\psi_{0}}{\partial x_{0}}=0$$ $$\frac{2\lambda_{N}^{T}}{\theta}=0$$ $$\frac{\partial\mathcal{H}_{k}}{\partial\omega_{k}}=0$$ $$\frac{2\lambda_{k}^{T}}{\theta}=\frac{\partial\mathcal{H}_{k}}{\partial x_{k}}\tag{11.47}$$

From the first expression in the above equation we obtain 

$$\begin{array}{r c l}{{\frac{2\lambda_{0}}{\theta}-\frac{2}{\theta}P_{0}^{-1}(x_{0}-\hat{x}_{0})}}&{{=}}&{{0}}\\ {{}}&{{}}&{{P_{0}\lambda_{0}-x_{0}+\hat{x}_{0}}}&{{=}}&{{0}}\\ {{}}&{{}}&{{x_{0}}}&{{=}}&{{\hat{x}_{0}+P_{0}\lambda_{0}}}\end{array}$$
$$(11.48)$$

From the second expression in Equation (11.47) we obtain 

$$\lambda_{N}=0$$
$$(11.49)$$

From the third expression in Equation **(11.47)** we obtain 

 In 240000 (21.17) we obtain  $\begin{matrix}-\dfrac{2}{\theta}Q_k^{-1}w_k+\dfrac{2}{\theta}\lambda_{k+1}&=&0\\ w_k&=&Q_k\lambda_{k+1}\end{matrix}$  into the process dynamics equation to obtain ... 
This can be substituted into the process dynamics equation to obtain 
xk+1 = FkXk -k *Qkxk+i* **(11.51)** 
From the fourth expression in Equation **(11.47)** we obtain 

$$\begin{array}{r c l}{{{\frac{2\lambda_{k}}{\theta}}}}&{{=}}&{{2\bar{S}_{k}(x_{k}-\hat{x}_{k})+{\frac{2}{\theta}}H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}x_{k})+{\frac{2}{\theta}}F_{k}^{T}\lambda_{k+1}}}\\ {{\lambda_{k}}}&{{=}}&{{F_{k}^{T}\lambda_{k+1}+\theta\bar{S}_{k}(x_{k}-\hat{x}_{k})+H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}x_{k})}}\end{array}$$
At this point we have to make an assumption in order to proceed any further. From 
Equation **(11.48)** we know that xo = 20 + *PoXo, so* we will assume that 
$$(11.52)$$
$$(11.50)$$
$\epsilon\to G$
$$(11.51)^{\frac{1}{2}}$$
$$x_{k}=\mu_{k}+P_{k}\lambda_{k}$$
$$(11.53)$$
$$(11.54)$$

xk = pk + *Pkxk* ( **11.53)** 
for all k, where pk and Pk are some functions to be determined, with PO given, and the initial condition po = **20.** That is, we assume that Xk is an affine function of *xk.* This assumption may or may not turn out to be valid. We will proceed as if the assumption were true, and if our results turn out to be correct then we will know that our assumption was indeed valid. Substituting Equation **(11.53)** into Equation **(11.51)** gives 

$$\mu_{k+1}+P_{k+1}\lambda_{k+1}=F_{k}\mu_{k}+F_{k}P_{k}\lambda_{k}+Q_{k}\lambda_{k+1}$$  Substituting Equation (11.53) into Equation (11.52) gives
$$\lambda_{k}=F_{k}^{T}\lambda_{k+1}+\theta\tilde{S}_{k}(\mu_{k}+P_{k}\lambda_{k}-\hat{x}_{k})+H_{k}^{T}R_{k}^{-1}\left[y_{k}-H_{k}(\mu_{k}+P_{k}\lambda_{k})\right].$$
2) gives  $ [y_k-H_k(\mu_k+P_k\lambda_k)]$ . 
Rearranging this equation gives 
The equation gives  $\begin{array}{c}\lambda_k-\theta\tilde{S}_k P_k\lambda_k+H_k^T R_k^{-1}H_k P_k\lambda_k=\\ F_k^T\lambda_{k+1}+\theta\tilde{S}_k(\mu_k-\hat{x}_k)+H_k^T R_k^{-1}(y_k-H_k\mu_k)\end{array}$  I used for λ = 0. 
This can be solved for xk as 
$$\begin{array}{r c l}{{\lambda_{k}}}&{{=}}&{{\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}\times}}\\ {{}}&{{}}&{{\left[F_{k}^{T}\lambda_{k+1}+\theta\bar{S}_{k}\left(\mu_{k}-\hat{x}_{k}\right)+H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}\mu_{k})\right]}}\end{array}$$
Substituting this expression for xk into Equation **(11.54)** gives 
$$(11.55)$$
$$(11.56)$$
$$(11.57)$$
$$\mu_{k+1}+P_{k+1}\lambda_{k+1}=F_{k}\mu_{k}+F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}\times$$ $$\left[F_{k}^{T}\lambda_{k+1}+\theta\bar{S}_{k}(\mu_{k}-\hat{x}_{k})+H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}\mu_{k})\right]+Q_{k}\lambda_{k+1}\tag{11.58}$$
This equation can be rearranged as follows: 
$$\mu_{k+1}-F_{k}\mu_{k}-F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}\times$$ $$\left[\theta\bar{S}_{k}(\mu_{k}-\hat{x}_{k})+H_{k}^{T}R_{k}^{-1}(\mu_{k}-H_{k}\mu_{k})\right]=$$ $$\left[-P_{k+1}+F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}F_{k}^{T}+Q_{k}\right]\lambda_{k+1}\tag{11.59}$$

This equation is satisfied if both sides are zero. Setting the left side of the above equation equal to zero gives 

$$\begin{array}{l}{{F_{k}\mu_{k}+F_{k}P_{k}\left[I-\theta\tilde{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}\times}}\\ {{\left[\theta\tilde{S}_{k}(\mu_{k}-\hat{x}_{k})+H_{k}^{T}R_{k}^{-1}(y_{k}-H_{k}\mu_{k})\right]}}\end{array}$$
$$\mu_{k+1}\quad=\quad$$

with *the* initial condition 

$$\mu_{0}={\hat{x}}_{0}$$
$$(11.60)$$
$$(11.61)$$

Setting the right side of Equation (11.59) equal to zero gives 

$$\begin{array}{r c l}{{P_{k+1}}}&{{=}}&{{F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}F_{k}^{T}+Q_{k}}}\\ {{}}&{{=}}&{{F_{k}\bar{P}_{k}F_{k}^{T}+Q_{k}}}\end{array}$$
$$(11.62)$$

where & is defined by the above equation. That is, 

$$\tilde{P}_{k}=P_{k}\left[I-\theta\tilde{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}\tag{11.63}$$ $$=\left[P_{k}^{-1}-\theta\tilde{S}_{k}+H_{k}^{T}R_{k}^{-1}H_{k}\right]^{-1}$$

From the above equation we see that if *Pk, sk,* and Rk are symmetric, then Pk will be symmetric. We see from Equation (11.62) that if Qk is also symmetric, then Pk+1 will be symmetric. So if PO, Qk, Rk, *and* sk are symmetric for all k, then z'r, and Pk will be symmetric for all k. The values of 20 and Wk that provide a stationary point of J can be summarized as follows: 

20 = 20 +POX0  wk = QkAk+l  Ak = [I - 8SkPk f IffR;lHkPk]-l X  [F,TAk+l + eSk(Pk - fk) -k HTR-' k k (Yk -HkPk)]  Pk+i = FkPk [I - 8SkPk + HrRF'HkPk] Fz + Qk  pk+l = Fkpk f FkPk [I - 8SkPk f HrRklHkPk]-l X  [eSk(Pk - 2k) -k HrRil(Yk - HkPk)] (11.64) 
$$x_{0}$$
$$\mathbf{u}_{k}$$

AN = 0 
Po = fo 
The fact that we were able to find a stationary point of J shows that we were correct in our assumption that Xk was an affine function of &. In the following section, given these values of 20 and *Wk,* we will find the values of 2k *and* Yk that provide a stationary point of J. 

## Stationarity With Respect To 5 **And Y** 11.3.2

The problem in this section is to find a stationary point (with respect to 2k and N-1 Yk) Of J = $(Zk)lk=o -k *xk=O ck* (subject to the Constraint zk+l = FkXk f wk). 

This problem is solved given the fact that ZO and Wk have already been set to their maximizing values as described in Section 11.3.1. From Equation (11.53), and the initial condition of pk in Equation (11.61), we see that 

$$(11.65)$$
$$(11.66)$$
$$(11.67)$$

We therefore obtain 

$$\begin{array}{r c l}{{\lambda_{k}}}&{{=}}&{{P_{k}^{-1}(x_{k}-\mu_{k})}}\\ {{\lambda_{0}}}&{{=}}&{{P_{0}^{-1}(x_{0}-{\hat{x}}_{0})}}\end{array}$$
$$\begin{array}{r c l}{{\left|\left|\lambda_{0}\right|\right|_{P_{0}}^{2}}}&{{=}}&{{\lambda_{0}^{T}P_{0}\lambda_{0}}}\\ {{}}&{{=}}&{{(x_{0}-\hat{x}_{0})^{T}P_{0}^{-T}P_{0}P_{0}^{-1}(x_{0}-\hat{x}_{0})}}\\ {{}}&{{=}}&{{(x_{0}-\hat{x}_{0})^{T}P_{0}^{-1}(x_{0}-\hat{x}_{0})}}\\ {{}}&{{=}}&{{\left|\left|x_{0}-\hat{x}_{0}\right|\right|_{P_{0}^{-1}}^{2}}}\end{array}$$
$$J=\frac{-1}{\theta}||\lambda_{0}||_{P_{0}}^{2}+\sum_{k=0}^{N-1}\left[||x_{k}-\hat{x}_{k}||_{\hat{S}_{k}}^{2}-\frac{1}{\theta}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||y_{k}-H_{k}x_{k}||_{R_{k}^{-1}}^{2}\right)\right]$$

Therefore, Equation (1 1.45) becomes Substituting for 2k from Equation (11.53) in this expression gives 

$$J=\frac{-1}{\theta}||\lambda_{0}||_{P_{0}}^{2}+\tag{11.68}$$ $$\sum_{k=0}^{N-1}\left[||\mu_{k}+P_{k}\lambda_{k}-\hat{x}_{k}||_{S_{k}}^{2}-\frac{1}{\theta}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||y_{k}-H_{k}(\mu_{k}+P_{k}\lambda_{k})||_{R_{k}^{-1}}^{2}\right)\right]$$

Consider the term *w~&~lwk* in the above equation. Substituting for Wk from Equation (11.50) in this term gives 

$$\begin{array}{r c l}{{w_{k}^{T}Q_{k}^{-1}w_{k}}}&{{=}}&{{\lambda_{k+1}^{T}Q_{k}^{T}Q_{k}^{-1}Q_{k}\lambda_{k+1}}}\\ {{}}&{{=}}&{{\lambda_{k+1}^{T}Q_{k}\lambda_{k+1}}}\end{array}$$
$$(11.69)$$
$$(11.70)$$
$$k+1||_{Q_{k}}^{2}$$

where we have used the fact that Qk is symmetric. Equation (11.68) can therefore be written as 

$$J=\frac{-1}{\theta}||\lambda_{0}||_{P_{0}}^{2}+$$ $$\sum_{k=0}^{N-1}\left[||\mu_{k}+P_{k}\lambda_{k}-\hat{x}_{k}||_{S_{k}}^{2}-\frac{1}{\theta}||y_{k}-H_{k}(\mu_{k}+P_{k}\lambda_{k})||_{R_{k}^{-1}}^{2}\right]-\frac{1}{\theta}\sum_{k=0}^{N-1}||\lambda_{k}$$
$\sum_{k=0}^{N}\lambda_{k}^{T}P_{k}\lambda_{k}-\sum_{k=0}^{N-1}\lambda_{k}^{T}P_{k}\lambda_{k}=0$ (11.71)
Now we take a slight digression to notice that The reason that this equation is correct is because from Equation (11.49) we know that AN = 0. Therefore, the last term in the first summation above is equal to zero and the two summations are equal. The above equation can be written as

$$0=\lambda_{0}^{T}P_{0}\lambda_{0}+\sum_{k=1}^{N}\lambda_{k}^{T}P_{k}\lambda_{k}-\sum_{k=0}^{N-1}\lambda_{k}^{T}P_{k}\lambda_{k}\tag{11.72}$$ $$=\lambda_{0}^{T}P_{0}\lambda_{0}+\sum_{k=0}^{N-1}\lambda_{k+1}^{T}P_{k+1}\lambda_{k+1}-\sum_{k=0}^{N-1}\lambda_{k}^{T}P_{k}\lambda_{k}$$ $$=\frac{-1}{\theta}\left|\left|\lambda_{0}\right|\right|_{P_{0}}^{2}-\frac{1}{\theta}\sum_{k=0}^{N-1}(\lambda_{k+1}^{T}P_{k+1}\lambda_{k+1}-\lambda_{k}^{T}P_{k}\lambda_{k})$$
$$\begin{array}{r l}{J}&{{}=}\\ {\ }&{{}}\end{array}$$

We can subtract this zero term to the cost function of Equation (11.70) to obtain

Uk + Pk > - 2k | St ||x+1||} + + (x+1 Px+1 )++1 - > Px Px > - }| 3k - Hx(uk + Pk >k)|| Rx (Uk - âk) 5k (Uk - âk) + 2(Uk - âk) " Sk Px > + x Px Sk Pk >k + 2 2 + ( P + 1 - Q x ) k + 1 - 2 2 Pk - H ( 1 ) " R - ( 3 k - H (  2 (3k - HkHk) TR2 HkPk - 2 X Px Hk Rx 1 Hk Pk Xk (11.73)
Now we consider the term λξ+1(Px+1 - Qx)λκ+1 in the above expression. Substi-
tuting for Px+1 from Equation (11.62) in this term gives

$$\begin{array}{l l l}{{\lambda_{k+1}^{T}(P_{k+1}-Q_{k})\lambda_{k+1}}}&{{=}}&{{\lambda_{k+1}^{T}(Q_{k}+F_{k}\tilde{P}_{k}F_{k}^{T}-Q_{k})\lambda_{k+1}}}\\ {{}}&{{=}}&{{\lambda_{k+1}^{T}F_{k}\tilde{P}_{k}F_{k}^{T}\lambda_{k+1}}}\end{array}$$
$$(11.74)$$

But from Equation (11.55) we see that

$F_{k}^{T}\lambda_{k+1}=\lambda_{k}-\theta\bar{S}_{k}(\mu_{k}+P_{k}\lambda_{k}-\hat{x}_{k})-H_{k}^{T}R_{k}^{-1}[y_{k}-H_{k}(\mu_{k}+P_{k}\lambda_{k})]$
(11.75)
Substituting this expression for F x +1 into Equation (11.74) gives

X +1 (Pk +1 - Qk ) x +1 { Àk - 0Šk (Uk + Px Xc - 2k) - Hk Rx 1 (yk - Hk(Uk + Px Ak)] } " Px { }k - 0 Sk (uk + Px >x - 2k) - H Rx - Hk (uk + Px >x ) } { X (I - 0PK Sk + Px H R R - Hk) - 0(uk - âk) T Sk - (yk - HkHk)" Rx Hk } Pk { Xk (I - 0Px Sk + PkH2 Rx 1 Hk)- 0(µk - âk)™ Šk - (yk - HkHk)™ Rz 1 Hk }" (11.76) Now note from Equation (11.63) that (I-0Px Sk+PxHx Rx +Hk) = Pk P2 1. Making
this substitution in the above equation gives the following.

(1 1.77) 
Notice that the above expression is a scalar. That means that each term on the right side is a scalar, which means that each term is equal to its transpose. For example, consider the second term on the right side. Since it is a scalar, we see that e(pk - 2k)TSkPkXk = ex:Pksk(pk - *2k).* (we have used the fact that Pk and Sk are symmetric, and 8 is a scalar.) Equation **(11.77)** can therefore be written as 

(1 1.78) 
$$\begin{array}{r c l}{{\tilde{P}_{k}^{-1}}}&{{=}}&{{\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]P_{k}^{-1}}}\\ {{}}&{{=}}&{{P_{k}^{-1}\left[P_{k}^{-1}-\theta\bar{S}_{k}+H_{k}^{T}R_{k}^{-1}H_{k}\right]P_{k}^{-1}}}\\ {{}}&{{=}}&{{P_{k}^{-1}\left[I-P_{k}\theta\bar{S}_{k}+P_{k}H_{k}^{T}R_{k}^{-1}H_{k}\right]}}\end{array}$$
Now note from Equation **(11.63)** that 

$$(11.79)$$
$$\begin{array}{r l}{{\lambda_{k}^{T}P_{k}\tilde{P}_{k}^{-1}P_{k}\lambda_{k}=\lambda_{k}^{T}\left[I-\theta P_{k}\bar{S}_{k}+P_{k}H_{k}^{T}R_{k}^{-1}H_{k}\right]P_{k}\lambda_{k}}}\\ {{=}}&{{\lambda_{k}^{T}P_{k}\lambda_{k}-\theta\lambda_{k}^{T}P_{k}\bar{S}_{k}P_{k}\lambda_{k}+\lambda_{k}^{T}P_{k}H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\lambda_{k}}}\end{array}$$

We therefore see that 

$$(11.80)$$

Substituting this into Equation **(11.78)** gives 

(11.81)  Substituting this equation for xr+l(Pk+l- Qk)&+l into Equation (11.73) gives the  following. 

$$\begin{array}{r l}{J}&{{}=}\\ {}&{{}}\end{array}$$

$$\begin{array}{r c l}{{\hat{x}_{k}}}&{{=}}&{{\mu_{k}}}\\ {{y_{k}}}&{{=}}&{{H_{k}\mu_{k}}}\end{array}$$
These equations are clearly satisfied for the following values of 2k and yk: 

$$(11.84)$$

These are the extremizing values of ?k and *yk.* However, we still are not sure if these extremizing values give a local minimum or maximum of J. Recall that the second derivative of J tells us what kind of stationary point we have. If the second derivative is positive definite, then our stationary point is a minimum. If the second derivative is negative definite, then our stationary point is a maximum. If the second derivative has both positive and negative eigenvalues, then our stationary point is a saddle point. The second derivative of J with respect to hk can be computed as 

$$(11.85)$$
$$\frac{\partial^{2}J}{\partial\hat{x}_{k}^{2}}=2(\bar{S}_{k}+\theta\bar{S}_{k}\tilde{P}_{k}\bar{S}_{k})$$

_-_ 
Our ?k will therefore be a minimizing value of J if (sk + *eskpksk)* is positive definite. The value of sk chosen for use in Equation *(11.36)* should always be positive definite, which means that Sk defined in Equation *(11.44)* will be positive definite. This means that our ?k will be a minimizing value of J if & is positive definite. 

in Equation *(11.63),* the condition required for ?k to minimize J is that (P;' - esk + *H?R;lHk)-l* be positive definite. This is So, from the definition of equivalent to requiring that *(PF'* - esk + *H?RilHk)* be positive definite. The individual terms in this expression are always positive definite [note in particular from Equation **(11.62)** that Pk will be positive definite if 4 is positive definite]. 

So the condition for ?k to minimize J is that *esk* be "small enough" so that 
(PF' - esk + *HFRk'Hk)* is positive definite. Requiring that be small can be accomplished three different ways. 

1. *esk* will be small if 0 is small. This means that the performance requirement specified in Equation **(11.37)** is not too stringent. As long as our performance requirement is not too stringent then the problem will have a solution. If, however, the performance requirement is too stringent (i.e., 6 is large) then the problem will not have a solution. 

2. *63,* will be small if Lk is small. This statement is based on the relationship between Sk *and* Lk as shown in Equation **(11.44).** From Equation **(11.36)** we see that the numerator of the cost function is given as (Zk-&)TLTSkLk(Zk- 
&). So if Lk is small we see that the numerator of the cost function will be small, which means that it will be easier to minimize the cost function. If, however, Lk is too large, then the problem will not have a solution. 

3. *esk* will be small if sk is small. This statement is based on the relationship between sk *and* Sk as shown in Equation **(11.44).** From Equation **(11.36)** we see that the numerator of the cost function is given as (Z1,-?k)TL;SkLk(3&- 
&). so if sk is small we see that the numerator of the cost function will be small, which means that it will be easier to minimize the cost function. If, however, sk is too large, then the problem will not have a solution. 

Note from Equation **(11.62)** that the positive definiteness of pk implies the positive definiteness of *%+I.* Therefore, if Po is positive definite (per our original problem statement), and pk is positive definite for all k, then Pk will also be positive definite for all k. 

It is also academically interesting (though of questionable utility) to note the conditions under which the Yk that we found in Equation **(11.84)** will be a maximizing value of J. (Recall that Yk is chosen by nature, our adversary, to maximize the cost function.) The second derivative of J with respect to yk can be computed as 

$$(11.86)$$
$$\begin{array}{r c l}{{\frac{\partial^{2}J}{\partial y_{k}^{2}}}}&{{=}}&{{\frac{2}{\theta}(R_{k}^{-1}H_{k}\tilde{P}_{k}H_{k}^{T}R_{k}^{-1}-R_{k}^{-1})}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{\frac{2}{\theta}R_{k}^{-1}(H_{k}\tilde{P}_{k}H_{k}^{T}-R_{k})R_{k}^{-1}}}\end{array}$$

Rk and *Rk',* specified by the tion **(11.36),** should always be user as part of the problem statement in Equapositive definite. So the second derivative above will be negative definite (which means that Yk will be a maximizing value of J) if 
(Rk - *HkpkH?)* is positive definite. This requirement can be satisfied in two ways. 

1. (Rk - *HkpkHF)* will be positive definite if Rk is large enough. A large value of Rk means that the denominator of the cost function of Equation **(11.36)** 
will be small, which means that the cost function will be large. A large cost function value is easier to maximize and will therefore tend to have a maximizing value for **Yk.** Also note that the designer typically chooses Rk to be proportional to the magnitude of the measurement noise. If the user knows that the measurement noise is large, then Rk will be large, which again will result in a problem with a maximizing value for **yk.** In other words, nature will be better able to maximize the cost function if the measurement noise is large. 

2. (& - *Hk&HT)* will be positive definite if Hk is small enough. If Hk becomes smaller, that means that the measurement noise becomes larger relative to the size of the measurements, as seen in Equation **(11.34).** In other words, a small value of Hk means a smaller signal-to-noise ratio for the measurements. A small signal-to-noise ratio gives nature a better opportunity to find a maximizing value of *Yk.* 
Of course, we are not really interested in finding a maximizing value of **Yk.** Our goal was to find the minimizing value of *Xk.* The H, filter algorithm can be summarized as follows. 

## The Discretetime H, Filter

1. The system equations are given as 

$$(11.87)$$
$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F_{k}x_{k}+w_{k}}}\\ {{}}&{{y_{k}}}&{{=}}&{{H_{k}x_{k}+v_{k}}}\\ {{}}&{{z_{k}}}&{{=}}&{{L_{k}x_{k}}}\end{array}$$

where Wk and Vk are noise terms, and our goal is to estimate 9. 

$$J_{1}=\frac{\sum_{k=0}^{N-1}||z_{k}-\hat{z}_{k}||_{S_{k}}^{2}}{||x_{0}-\hat{x}_{0}||_{P_{0}^{-1}}^{2}+\sum_{k=0}^{N-1}\left(||w_{k}||_{Q_{k}^{-1}}^{2}+||v_{k}||_{R_{k}^{-1}}^{2}\right)}\tag{11.88}$$

2. The cost function is given as where *PO, &k, Rk,* and sk are symmetric, positive definite matrices chosen by the engineer based on the specific problem. 

3. The cost function can be made to be less than *l/e* (a user-specified bound) 
with the following estimation strategy, which is derived from Equations **(11.44),** 
(11.60), (11.62), and **(11.84):** 

$$\hat{S}_{k}=L_{k}^{T}S_{k}L_{k}$$ $$K_{k}=P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}H_{k}^{T}R_{k}^{-1}$$ $$\hat{x}_{k+1}=F_{k}\hat{x}_{k}+F_{k}K_{k}(y_{k}-H_{k}\hat{x}_{k})$$ $$P_{k+1}=F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}F_{k}^{T}+Q_{k}\tag{11.89}$$

4. The following condition must hold at each time step k in order for the above estimator to be a solution to the problem: 

$$P_{k}^{-1}-\theta\bar{S}_{k}+H_{k}^{T}R_{k}^{-1}H_{k}>0$$
$$(11.90)$$
PF1 - OSk + *HZRklHk* > 0 (1 1.90) 

## A Comparison Of The Kalman And H, Filters 11.3.3

Comparing the Kalman filter in Equation (11.12) and the H, filter in Equation (11.89) reveals some fascinating connections. For instance, in the H, filter, Qk, Rk, and Po are design parameters chosen by the user based on a *priori* knowledge of the magnitude of the process disturbance *'wk,* the measurement disturbance wk, and the initial estimation error *(20* - **$0).** In the Kalman filter, *wk, Vk,* and 
(20 - *20)* are zero-mean, and *Qk, Rk,* and PO are their respective covariances. 

Now suppose we use Lk = sk = I in the H, filter. That is, we are interested in estimating the entire state, and we want to weight all of the estimation errors equally in the cost function. If we use 6 = 0 then the H, filter reduces to the Kalman filter (assuming Qk, Rk, *and* Po are chosen as above). This provides an interesting interpretation of the Kalman filter; that is, the Kalman filter is the minimax filter in the case that the performance bound in Equation (11.36) is set equal to *00.* We see that although the Kalman filter minimizes the variance of the estimation error (as discussed in Section 5.2), it does not provide any guarantee as far as limiting the worst-case estimation error. That is, it does not guarantee any bound for the cost function of Equation (11.36). 

The Kalman and H, filter equations have an interesting difference. If we want to estimate a linear combination of states using the Kalman filter, the estimator is the same regardless of the linear combination that we want to estimate. That is, if we want to estimate *Lkxk* using the Kalman filter, the answer is the same regardless of the Lk matrix that we choose. However, in the H, approach, the resulting filter depends strongly on Lk and the particular linear combination of states that we want to estimate. 

Note that the H, filter of Equation (11.89) is identical to the Kalman filter except for subtraction of the term *eSkPk* in the Kk and *Pk+1* equations. Recall from Section 5.5 that the Kalman filter can be made more robust to unmodeled noise and unmodeled dynamics by artificially increasing Qk in the Kalman filter equations. This results in a larger covariance **Pk,** which in turn results in a larger gain *Kk.* From Equation (11.89) we can see that subtracting *eskkpk* on the right side of the *pk+1* equation tends to make **Pk+l** larger (since the subtraction is inside a matrix inverse operation). Similarly, subtracting *eskkpk* on the right side of the Kk equation tends to make Kk larger. Increasing Qk in the Kalman filter is conceptually the same as increasing Pk and **Kk.** Therefore, the H, filter equations make intuitive sense when compared with the Kalman filter equations. The H, filter is a worst-case filter in the sense that it assumes that *'wk, Vk,* and 20 will be chosen by nature to maximize the cost function. The H, filter is therefore robust by design. Comparing the H, filter with the Kalman filter, we can see that the H, filter is simply a robust version of the Kalman filter. When we robustified the Kalman filter in Section 5.5 to add tolerance to unmodeled noise and dynamics, we did not derive an optimal way to increase *Qk.* However, H, filter theory shows us the optimal way to robustify the Kalman filter. 

## 11.3.4 Steady-State H, Filtering

If the underlying system and the design parameters are time-invariant, then it may be possible to obtain a steady-state solution to the H, filtering problem. Suppose 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{H x_{k}+v_{k}}}\\ {{z_{k}}}&{{=}}&{{L x_{k}}}\end{array}$$

that our system is given as 

$$(11.91)$$

where Wk *and* Vk are noise terms. Our goal is to estimate Zk such that 

$$\lim_{N\rightarrow\infty}\frac{\sum_{k=0}^{N-1}||z_{k}-\hat{z}_{k}||_{S}^{2}}{\sum_{k=0}^{N-1}\left(||w_{k}||_{Q^{-1}}^{2}+||v_{k}||_{R^{-1}}^{2}\right)}<\frac{1}{\theta}\tag{11.92}$$
$$(11.94)$$
$$(11.95)$$

where Q, R, and S are symmetric positive definite matrices chosen by the engineer based on the specific problem. The steady-state filter of Equation (11.89) becomes 

$$\begin{array}{r l}{{\bar{S}}}&{{}=}\\ {K}&{{}=}\\ {{\hat{x}}_{k+1}}&{{}=}\\ {P}&{{}=}\end{array}$$
S = L~SL 
$L^{T}SL$  $P\left[I-\theta\bar{S}P+H^{T}R^{-1}HP\right]^{-1}H^{T}R^{-1}$  $F\hat{x}_{k}+FK_{k}(y_{k}-H\hat{x}_{k})$  $FP\left[I-\theta\bar{S}P+H^{T}R^{-1}HP\right]^{-1}F^{T}+Q$ (11.93)
$$P^{-1}-\theta\bar{S}+H^{T}R^{-1}H>0$$

The following condition must hold in order for the above estimator to be a solution to the problem: 
p-l- eS + *H~R-~H* > o (11.94) 
If 0, *L, R,* or S is too large, or if H is too small, then the H, estimator will not have a solution. Note that the expression for P in Equation (11.93) can be written as 

$$P=F\left[P^{-1}-\theta\bar{S}+H^{T}R^{-1}H\right]^{-1}F^{T}+Q$$

Applying the matrix inversion lemma to the inverse in the above expression gives 

$$P=F\left\{P-P\left[(H^{T}R^{-1}H-\theta\bar{S})^{-1}+P\right]^{-1}P\right\}F^{T}+Q\tag{11.96}$$ $$=FPF^{T}-FP\left[(H^{T}R^{-1}H-\theta\bar{S})^{-1}+P\right]^{-1}PF^{T}+Q$$

This is a discretetime algebraic Riccati equation that can be solved with control system software.2 If control system software is not available, then the algebraic Riccati equation can be solved by numerically iterating the discrete-time Riccati equation of Equation (11.89) until it converges to a steady-state value. The steadystate filter is much easier to implement in a system in which real-time computational effort or code size is a serious consideration. The disadvantage of the steady-state filter is that (theoretically) it does not perform as well as the time-varying filter. 

However, the reduced performance that is seen in the steady-state filter is often a small fraction of the optimal performance, whereas the computational savings can be significant. 

2For example, in **MATLAB's** Control System Toolbox we can use the command DARE(FT,I,Q, (H~R-~H - es)-1. 

## 1 **Example** 11.2

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{z_{k}}}&{{=}}&{{x_{k}}}\end{array}$$

Suppose we are trying to estimate a randomly varying scalar on the basis of noisy measurements. We have the scalar system 

$$(11.97)$$

This system could describe our attempt to estimate a noisy voltage. The voltage is essentially constant, but it is subject to random fluctuations, hence the noise term Wk in the process equation. Our measurement of the voltage is also subject to noise or instrument bias, hence the noise term Vk in the measurement equation. We see in this example that F = H = L = 1. Further suppose that Q = R = S = 1 in the cost function of Equation **(11.88).** Then the discretetime Riccati equation associated with the H, filter equations becomes 

$$P_{k+1}=F_{k}P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}F_{k}^{T}+Q_{k}\tag{11.98}$$ $$=P_{k}\left[1-\theta P_{k}+P_{k}\right]^{-1}+1$$

This can be solved numerically or analytically as a function of time for a given 8 to give **Pk,** and then the H, gain can be obtained as 

$$K_{k}=P_{k}\left[I-\theta\bar{S}_{k}P_{k}+H_{k}^{T}R_{k}^{-1}H_{k}P_{k}\right]^{-1}H_{k}^{T}R_{k}^{-1}\tag{11.99}$$ $$=P_{k}\left[1-\theta P_{k}+P_{k}\right]^{-1}$$

we can set **Pk+l** = Pk in Equation **(11.98)** to obtain the steady-state solution for **Pk.** This gives 

$$P=P\left(1-\theta P+P\right)^{-1}+1$$ $$P)=P+(1-\theta P+P)$$ $$-1=0$$ $$P=\frac{1-\theta\pm\sqrt{(\theta-1)(\theta-5)}}{2(1-\theta)}\tag{11.100}$$
$$\begin{array}{c}{{P}}\\ {{(1-\theta)P^{2}+(\theta-1)P-1}}\\ {{P}}\end{array}$$

As we discussed earlier, i-n order for this value of P to be a solution to the H, estimation problem, P must be positive definite. The first solution for P 
is positive if 6 < 1, and both solutions for P are positive if *0 2* 5. Another condition for the solution of the H, estimation problem is that 

$P^{-1}-\theta\bar{S}+H^{T}R^{-1}H$$>$$0$  $P^{-1}-\theta+1$$>$$0$ (11.101)
If 6 < 1 then the first solution for P satisfies this bound. However, if *8 2* 5, then neither solution for P satisfies this bound. Combining this data shows that the H, estimator problem has a solution for 6 < 1. Every H, estimator problem will have a solution for 6 less than some upper bound because of the nature of the cost function. 

$$(11.102)$$

For a general estimator gain K the estimate can be written as 

$$\begin{array}{r c l}{{\hat{x}_{k+1}}}&{{=}}&{{F\hat{x}_{k}+F K(y_{k}-H_{k}\hat{x}_{k})}}\\ {{}}&{{=}}&{{(1-K)\hat{x}_{k}+K y_{k}}}\end{array}$$
= (1 - K)?k + *Kyk* (11.102) 
If we choose 8 = 1/2, then we obtain P = 2 and K = 1. As seen from the above equation, this results in bk+l = *yk.* In other words, the estimator ignores the previous estimate and simply sets the estimate equal to the previous measurement. As 8 increases toward 1, P increases above 2 and approaches 00, and the estimator gain K increases greater than 1 and also approaches *00.* 
In this case, the estimator will actually place a negative weight on the previous estimate and compensate by placing additional weight on the measurement. 

If 8 increases too much (gets too close to 1) then the estimator gain K will be greater than 2 and the H, estimator will be unstable. It is always a good idea to check the stability of your H, filter. If the filter is unstable then you should probably decrease 8 to obtain a stable filter. As 8 decreases below 1/2, P decreases below 2 and the gain K decreases below 1. In this case, the estimator balances the relative weight placed on the previous estimate and the measurement. 

A Kalman filter to estimate Xk is equivalent to an H, filter with 0 = 0. In this case, we obtain the positive definite solution of the steady-state Riccati equation as P = (1 + G)/2. This gives a steady-state estimator gain K = 
(1 + **&)/(3** + 4) = (4 - 1)/2 M 0.62. The Kalman filter gain is smaller than the H, filter gain for 8 > 0, which means that the Kalman filter relies less on measurements and more on the system model. The Kalman filter gives an optimal estimate if the model and the noise statistics are known, but it may undervalue the measurements if there are errors in the system model or the assumed noise statistics. 

Figure 11.2 shows the true state Xk and the estimate ?k when the steadystate Kalman and H, filters are used to estimate the state. The H, filter was designed with 8 = **1/3,** which gave a filter gain K = (3 + 3fi)/(8 + 28) x 0.82. The disturbances Wk *and* Wk were both normally distributed zero-mean white noise sequences with standard deviations equal to 10. The performance of the two filters is very similar. The RMS estimation error of the Kalman filter is 3.6 and the RMS estimation error of the H, filter is 4.1. As expected, the Kalman filter performs better than the H, filter. However, suppose that the process noise has a mean of 10. Figure 11.3 shows the performance of the filters for this situation. In this case the H, filter performs better. The RMS estimation error of the Kalman filter is 15.6 and the RMS estimation error of the H, filter is 12.0. 

If we choose 8 = 1/10 then we obtain P = 5/3 and K = **2/3. As** 8 gets smaller, the H, estimator gain gets closer and closer to the Kalman filter gain. 

vvv 

## The Transfer Function Bound Of The H, Filter 11.3.5

In this section, we show that the steady-state H, filter derived in the previous section bounds the transfer function from the noise to the estimation error, if Q, 

![25_image_0.png](25_image_0.png)

Figure **11.2** Example 11.2 results. Khan and H, filter peformance when the noise statistics are known. The Kalman gain is **0.62** and the H, gain is 0.82. The Kalman filter performs about 12% better than the H, filter. 

![25_image_1.png](25_image_1.png)

Figure **11.3** Example 11.2 results. Kalman and H, filter peformance when the process noise is biased. The Kalman gain is 0.62 and the H, gain is 0.82. The H, filter performs about 23% better than the Kalman filter. 
R, and S are all identity matrices. Recall that the two-norm of a column vector x 
is defined as 
$$||x||_{2}^{2}=x^{T}x$$
Now suppose we have a timevarying vector **50, XI, 22,** a. The signal two-norm of 
x is defined as 
$$(11.103)$$
$$(11.104)$$
$$||x||_{2}^{2}=\sum_{k=0}^{\infty}||x_{k}||_{2}^{2}$$
That is, the square of the signal two-norm is the sum of all of the squares of the vector two-norms that are taken at each time step.3 Now suppose that we have a system with input u and output 5, and the transfer function is *G(z).* If the input u is comprised entirely of signals at the frequency w and the sample time of the system is T, then we define the phase of u as q5 = *Tw.* In this case the maximum gain from u to x is determined as 

sup - 
$$\sup_{u\neq0}\frac{||x||_{2}}{||u||_{2}}=\sigma_{1}\left[G\left(e^{\jmath\phi}\right)\right]\tag{11.105}$$
where ol(G) is the largest singular value of the matrix G. If u can be comprised of an arbitrary mix of frequencies, then the maximum gain from u to z is determined as follows: 

$$\sup_{\phi}\frac{||x||_{2}}{||u||_{2}}=\sup_{\phi}\sigma_{1}\left[G\left(e^{j\phi}\right)\right]\tag{11.106}$$ $$=||G||_{\infty}$$
$$J=\operatorname*{lim}_{N\rightarrow\infty}{\frac{\sum_{k=0}^{N-1}||z_{k}-{\hat{z}}_{k}||_{S}^{2}}{\sum_{k=0}^{N-1}\left(||w_{k}||_{Q^{-1}}^{2}+||v_{k}||_{R^{-1}}^{2}\right)}}$$

The above equation defines llGli,, which is the infinity-norm of the system that has the transfer function *G(z).~* 
Now consider Equation (1 1.92), the cost function that is bounded by the steadystate H, filter: 

$$(11.107)$$
$$J=\operatorname*{lim}_{N\rightarrow\infty}{\frac{\sum_{k=0}^{N-1}||z_{k}-{\hat{z}}_{k}||_{2}^{2}}{\sum_{k=0}^{N-1}\left(||w_{k}||_{2}^{2}+||v_{k}||_{2}^{2}\right)}}$$

If Q, R, and S are all equal to identity matrices, then 

$$(11.108)$$
$$\begin{array}{r c l}{{||G_{\hat{z}e}||_{\infty}^{2}}}&{{=}}&{{\operatorname*{sup}_{\phi}\frac{|\,|z-\hat{z}||_{2}^{2}}{|w||_{2}^{2}+||v||_{2}^{2}}}}\\ {{}}&{{}}&{{\leq}}&{{\frac{1}{\theta}}}\end{array}$$

Since the H, filter makes this scalar less than l/e for all Wk and vk, we can write 

$$(11.109)$$

where we have defined 2 = *z-2, eT* = [ wT vT ] T, and **Gze** is the system that has e as its input and 2 as its output. We see that the steady-state H, filter bounds the infinity-norm (i.e., the maximum gain) from the combined disturbances w and v to the estimation error 2, if &, R, and S are all identity matrices. Further information about the computation of infinity-norms and related issues can be found in [Bur99]. 

3Note that this definition means that many signals have unboundedsignal two-norms. The signal two-norm can also be defined as the **sum** from k = 0 to a finite limit k = N. 

4Note that the infinity-norm of a matrix has a definition that is different than the infinity-norm of a system. In general, the expression I IGI could refer either to the matrix infinity-normor the system infinity-norm. The meaning needs to be inferred from the context unless it is explicitly st at ed . 

## 1 **Example** 11.3

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{\hat{x}_{k+1}}}&{{=}}&{{(1-K)\hat{x}_{k}+K y_{k}}}\end{array}$$

Consider the system and filter discussed in Example **11.2:** 

$$(11.110)$$

The estimation error can be computed as 

$$(11.111)$$

Taking the z-transform of this equation gives 

$$\begin{array}{r c l}{{\tilde{x}_{k+1}}}&{{=}}&{{x_{k+1}-\hat{x}_{k+1}}}\\ {{}}&{{=}}&{{(1-K)\tilde{x}_{k}+w_{k}-K v_{k}}}\end{array}$$
$$z\tilde{X}(z)=(1-K)\tilde{X}(z)+W(z)-KV(z)$$ $$\tilde{X}(z)=\frac{1}{z-1+K}\left[\begin{array}{cc}1&-K\end{array}\right]\left[\begin{array}{c}W(z)\\ V(z)\end{array}\right]\tag{11.112}$$ $$=G(z)\left[\begin{array}{c}W(z)\\ V(z)\end{array}\right]$$

G(z), the transfer function from Wk and Wk to *gk,* is a 2 x 1 matrix. This matrix has one singular value, which is computed as 

$$\sigma^{2}(G)=\lambda_{\max}\left[G(e^{j\phi})G^{H}(e^{j\phi})\right]\tag{11.113}$$ $$=\frac{1+K^{2}}{(e^{j\phi}-1+K)(e^{-j\phi}-1+K)}$$ $$=\frac{1+K^{2}}{K^{2}+2(K-1)(\cos\phi-1)}$$
$$\begin{array}{r c l}{{\vert\vert G\vert\vert_{\infty}^{2}}}&{{=}}&{{\operatorname*{sup}_{\phi}\sigma^{2}\left[G\left(e^{j\phi}\right)\right]}}\\ {{}}&{{=}}&{{\frac{1+K^{2}}{K^{2}}}}\end{array}$$

The supremum of this expression occurs at + = 0 when K 5 1, so 

$$(11.114)$$

Recall from Example **11.2** that 6 = **1/2** resulted in K = 1. In this case, the above expression indicates that 11G11k = 2 5 l/e = 2. In this case, the infinity-norm bound specified by 0 is exact. Also recall from Example **11.2** 
that 6' = **1/10** resulted in K = **2/3.** In this case, the above expression indicates that 1.lGl IL = 13/4 5 l/e = **10.** In this case, the infinity-norm bound specified by 0 is quite conservative. 

Note that as K increases, the infinity-norm from the noise to the estimation error decreases. However, the estimator also is unstable for K > 1. So even though large K reduces the infinity-norm of the estimator, it gives poor results. In other words, just because the effect of the noise on the estimation error is small does not necessarily prove that the estimator is good. For example, we could set the estimate $k = 00 for all k. In that case, the noise will have zero effect on the estimation error because the estimation error will be infinite regardless of the noise value. However, the estimate will obviously be poor. This example shows the importance of balancing H, performance with other performance criteria. 

vvv 

## 11.4 The Continuous-Time H, Filter

The methods of the earlier sections can also be used to derive a continuous-time H, filter, as shown in continuous-time system 
[Rhe89, Ban91, Ban921. In this section we consider the 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+B u+w}}\\ {{y}}&{{=}}&{{C x+v}}\\ {{z}}&{{=}}&{{L x}}\end{array}\tag{1}$$

where L is a user-defined matrix and z is the vector that we want to estimate. Our estimate of z is denoted 2, and our estimate of the state at time 0 is denoted *h(0).* The vectors w and v are disturbances with unknown statistics; they may not even be zero-mean. In the game theory approach to H, filtering we define the following cost function: 

$$(11.115)$$
$$(11.116)$$
$$J_{1}={\frac{\int_{0}^{T}||z-{\hat{z}}||_{S}^{2}\,d t}{|\,|x(0)-{\hat{x}}(0)||_{P_{0}^{-1}}^{2}+\int_{0}^{T}\left(|\,|w||_{Q^{-1}}^{2}+|\,|v||_{R^{-1}}^{2}\right)\,d t}}$$

Po, Q, R, and S are positive definite matrices chosen by the engineer based on the specific problem. Our goal is to find an estimator such that 

$$(11.117)$$

The estimator that solves this problem is given by 

$$J_{1}<{\frac{1}{\theta}}$$
$$P(0)=$$
$$\begin{array}{r l}{{\langle\ ,}}\\ {{\dot{P}}}&{{}=}\\ {K}&{{}=}\\ {{\dot{x}}}&{{}=}\\ {{\hat{z}}}&{{}=}\end{array}$$
P(0) = Po 
$P_{0}$  $AP+PA^{T}+Q-KCP+\thetaPL^{T}SLP$  $PC^{T}R^{-1}$  $A\hat{x}+Bu+K(y-C\hat{x})$  $L\hat{x}$ (11.118)
These equations are identical to the continuous-time Kalman filter equations (see Section 8.2) except for the 6' term in the P equation. The inclusion of the 6' term in the P equation tends to increase P, which tends to increase the gain K, which tends to make the estimator more responsive to measurements than the Kalman filter. This is a way of robustifymg the filter to uncertainty in the system model. 

The estimator given above solves the H, estimation problem if and only if P(t) 
remains positive definite for all t E [0, *TI.* As with the discrete-time filter, we can also obtain a steady-state continuous-time H, filter. To do this we let P = 0 so that the differential Riccati equation above reduces to an algebraic Riccati equation. 

## Example 11.4

Consider the scalar continuous-time system 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{x+w}}\end{array}$$

$$(11.119)$$
$$(11.120)$$
z= X (1 1.119) 
$$\begin{array}{r c l}{y}&{=}&{x+v}\\ {z}&{=}&{x}\end{array}$$

We see that A = C = L = 1. Further suppose that Q = R = S = 1 in the cost function of Equation (11.116). Then the differential Riccati equation for the H, filter is 

$$\begin{array}{r c l}{{\dot{P}}}&{{=}}&{{A P+P A^{T}+Q-P C^{T}R^{-1}C P+\theta P L^{T}S L P}}\\ {{}}&{{=}}&{{2P+1+(\theta-1)P^{2}}}\end{array}$$

This can be solved numerically or analytically as a function of time for a given 0 to give P, and then the H, gain K = PCTR-' = P can be obtained. We can also set P = 0 in Equation (11.120) to obtain the steady-state solution for P. This gives 

$$(\theta-1)P^{2}+2P+1=0$$

As mentioned above, the solution to this quadratic equation must be positive definite in order for it to solve the H, estimation problem. For this scalar equation, positive definite simply means positive. The equation has a positive solution for 6 < 1, in which case the steady-state solution is given by 

$$P={\frac{-1-{\sqrt{2-\theta}}}{\theta-1}}$$

Suppose we choose 8 = 7/16. In this case, the analytic solution for the timevarying P can be obtained from Equation (11.120) as 

$$\begin{array}{r c l}{{P(t)}}&{{=}}&{{\frac{4+160c e^{5t/2}}{-9+40c e^{5t/2}}}}\\ {{}}&{{c}}&{{=}}&{{\frac{9P(0)+4}{40P(0)-160}}}\end{array}$$
$$(11.121)$$
$$(11.122)$$

$$(11.123)$$

From this analytic expression for P(t) we can see that 

$$(11.124)^{\frac{1}{2}}$$
$$\operatorname*{lim}_{t\to\infty}P(t)=4$$

Alternatively, we can substitute 6 = 7/16 in Equation (11.122) to obtain P = 4. Figure 11.4 shows P as a function of time when P(0) = 1. Note that in this example, since C = R = 1, the H, gain K is equal to P. 

Figure 11.5 shows the state estimation errors for the time-varying H, 
filter and the steady-state H, filter. In these simulations, the disturbances w and w were both normally distributed white noise sequences with standard deviations equal to 10. w had a mean of zero, and w had a mean of 10. 

Both simulations were run with identical disturbance time histories. It can be seen that the performance of the two filters is very similar. There are some differences between the two plots at small values of time before the 

![30_image_0.png](30_image_0.png)

Figure 11.4 Example 11.4 H, Riccati equation solution as a function of time. 
time-varying Riccati solution has converged to steady state (note that the time-varying filter performs better during the initial transient). But after the Riccati solution gets close to steady state (after about t = 1) the performance of the two filters is nearly identical. This illustrates the possibility of saving a lot of computational effort by using a steady-state filter while giving up only an incremental amount of performance. 

![30_image_1.png](30_image_1.png)

Figure 11.5 the measurement noise is zero-mean. 

Example 11.4 timevarying and steady-state Hm filter performance when 
If we use the performance bound 0 = 0 in this example then we obtain the Kalman filter. The steady-state Riccati equation solution from Equation (11.120) is (l+a) 
when 0 = 0, so the steady-state Kalman gain *K M* 2.4, which is less than the steady-state H, gain K = 4 that we obtained for 0 = 7/16. From Equation (11.118) we see that this will make the Kalman filter less responsive to measurements than the H, filter, but the Kalman filter should provide optimal RMS error performance. Indeed, if we run the timevarying Kalman filter (0 = 0) then the two-norm of the estimation error turns out to be 26.5. If we run the timevarying H, filter (0 = 7/16) then the two-norm of the estimation error increases to **30.0.** 
However, the Kalman filter assumes that the system model is known exactly, the process and measurement noises are zero-mean and uncorrelated, and the noise statistics are known exactly. If we change the simulation so the measurement noise has a mean of 10 then the H, filter works better than the Kalman filter. Figure 11.6 shows the estimation error of the two filters in this case. The two-norm of the estimation error is 112.8 for the Kalman filter but only 94.2 for the H, filter. 

![31_image_0.png](31_image_0.png)

Figure 11.6 measurement noise is not zero-mean. 

Example 11.4 time-varying Kalman and H, filter performance when the 
vvv As with the discretetime steady-state filter, if Q, R, and S are all identity matrices, the continuous-time steady-state filter bounds the maximum gain from the noise to the estimation error: 

$$||G_{\tilde{z}e}||_{\infty}^{2}=\sup_{\omega}\frac{||z-\hat{z}||_{2}^{2}}{||w||_{2}^{2}+||v||_{2}^{2}}\tag{11.125}$$ $$\leq\frac{1}{\theta}$$

where w is the frequency of the noise, and we have defined 2 = z - 2, eT = 
[ *wT vT IT,* and *Gi,* is the system that has e as its input and 2 as its output. 

The continuous-time infinity-norm of the system *Gi,* is defined as follows: 

$$\begin{array}{r c l}{{||G_{\bar{z}e}||_{\infty}}}&{{=}}&{{\operatorname*{sup}_{\omega}{\frac{||\bar{z}||_{2}}{||e||_{2}}}}}\\ {{}}&{{=}}&{{\operatorname*{sup}_{\omega}\sigma_{1}\left[G_{\bar{z}e}\left(j\omega\right)\right]}}\end{array}$$

$$(11.126)$$

where *Gie(s)* is the transfer function from e to 2. 

## 11.5 Transfer Function Approaches

$T_{k+1}=F_{2k}+w_{k}$  $T_{0}=0$  $W_{k}=H_{2k}+w_{k}$  $Z_{k}=L_{2k}$
It should be emphasized that other formulations to H, filtering have been proposed. 

For instance, Isaac Yaesh and Uri Shaked [YaeSl] consider the following timeinvariant system: 

$$(11.127)$$
$$(11.128)$$

where Wk and Vk are uncorrelated process and measurement noise, Yk is the measurement, and Zk is the vector to be estimated. Define the estimation error as 

$$\tilde{z}_{k}=z_{k}-\hat{z}_{k}$$

Define an augmented disturbance vector as 

$$(11.129)$$

$$(11.130)$$
$$(11.131)$$

The goal is to find a steady-state estimator such that the infinity-norm of the transfer function from the augmented disturbance vector e to the estimation error ,Z is less than some user specified bound: 
1 IIGzeII2 ; (1 1.130) 
The steady-state *a priori* filter that solves this problem is given as 

$$e_{k}={\left[\begin{array}{l}{w_{k}}\\ {v_{k}}\end{array}\right]}$$
$$||G_{\bar{z}e}||_{\infty}^{2}<{\frac{1}{\theta}}$$
$$\begin{array}{r c l}{{P}}&{{=}}&{{I+F P F^{T}-F P H^{T}(I+H P H^{T})^{-1}H P F^{T}+}}\\ {{}}&{{}}&{{P L(I/\theta+L P L^{T})^{-1}L P}}\\ {{K}}&{{=}}&{{F P H^{T}(I+H P H^{T})^{-1}}}\\ {{\hat{x}_{k+1}}}&{{=}}&{{F\hat{x}_{k}+K(y_{k}-H\hat{x}_{k})}}\end{array}$$
These equations solve the H, estimation problem if and only if P is positive definite. 
The steady-state *a posteriori* filter that solves this problem is given as 
$$\Sigma^{-1}=\tilde{P}^{-1}-\theta L^{T}L+H^{T}H$$ $$\tilde{P}=F\tilde{P}(H^{T}H\tilde{P}-\theta L^{T}L\tilde{P}+I)^{-1}F^{T}+I$$ $$\tilde{K}=(I+\theta L^{T}L)^{-1}\Sigma H^{T}$$ $$=\tilde{P}(I+H^{T}H\tilde{P})^{-1}H^{T}$$ $$\hat{x}_{k+1}=F\hat{x}_{k}+\tilde{K}(y_{k+1}-HF\hat{x}_{k})\tag{11.132}$$

Again, these equations solve the H, estimation problem if and only if P is positive definite. 

Interestingly, the P matrix in the a *priori* filter of Equation (11.131) is related to the p matrix in the a *posteriori* filter of Equation (11.132) by the following equation: *p-l= p-1- eLTL* (11.133) 
In general, the Riccati equations in these filters can be difficult to solve. However, the solution can be obtained by the eigenvector method shown in [YaeSl]. (This is similar to the Hamiltonian approach to steady-state Kalman filtering described in Section 7.3.3.) Define the 2n x 2n matrix 

$$P^{-1}=\tilde{P}^{-1}-\theta L^{T}L$$
$${\mathcal{H}}={\left[\begin{array}{l l}{F^{T}+H^{T}H F^{-1}}&{\theta F^{T}L^{T}L-H^{T}H F^{-1}(I-\theta L^{T}L)}\\ {-F^{-1}}&{F^{-1}(I-\theta L^{T}L)}\end{array}\right]}$$
$$(11.133)$$
$$(11.134)$$
] (11.134) 
Note that F-l should always exist if it comes from a real system, because F comes from a matrix exponential that is always invertible (see Sections 1.2 and 1.4). Compute the n eigenvectors of 'FI that correspond to the eigenvalues outside the unit circle. Denote those eigenvectors as & (i = 1, . . . , n). Form the 2n x n matrix 

$$(11.135)$$
$$(11.136)$$

where Xi and X2 are n x n matrices. The P matrix used in the a *priori* H, filter can be computed as P = *X2X,l* (11.136) 
For the a *posteriori* fdter, define the 2n x 2n matrix 

$\left[\begin{array}{cccc}\xi_{1}&\cdots&\xi_{n}\end{array}\right]=\left[\begin{array}{c}X_{1}\\ X_{2}\end{array}\right]$
$$P=X_{2}X_{1}^{-1}$$
$$\begin{array}{l l}{{}}&{{=}}\\ {{}}&{{\times2n\mathrm{~matrix}}}\end{array}$$
$${\tilde{\mathcal{H}}}={\left[\begin{array}{l l}{F^{-T}}&{F^{-T}(H^{T}H-\theta L^{T}L)}\\ {F^{-T}}&{F+F^{-T}(H^{T}H-\theta L^{T}L)}\end{array}\right]}$$
$${\left[\begin{array}{l l l}{{\tilde{\xi}_{1}}}&{\cdots}&{{\tilde{\xi}_{n}}}\end{array}\right]}={\left[\begin{array}{l}{{\tilde{X}_{1}}}\\ {{\tilde{X}_{2}}}\end{array}\right]}$$
$$\tilde{P}=\tilde{X}_{2}\tilde{X}_{1}^{-1}$$
Compute the n eigenvectors of I? that correspond to the eigenvalues outside the unit circle. Denote those eigenvectors as & (i = 1, . . . , n). Form the 2n x n matrix 

$$(11.137)$$
$$(11.138)$$
$$(11.139)$$

where and x2 are n x n matrices. The f' matrix used in the a *posteriori* H, 
filter can be computed as p = *x2x,1* (11.139) 
The eigenvector method for the Riccati equation solutions works because 'H and 7? are symplectic matrices (see Section 7.3.3 and Problem 11.9). This assumes that F is nonsingular and that 'H and fi do not have any eigenvalues on the unit circle. If these assumptions are violated, then the problem becomes more complicated [YaeSl]. A method similar to this for continuoustime systems is developed in [Naggl]. 

It is important to be aware that the P and p solutions given by Equations (11.136) 
and (11.139) only give one solution each to Equations (11.131) and (11.132). Equ& 
tions (11.136) and (11.139) may give solutions to Equations (11.131) and (11.132) that are not positive definite and therefore do not satisfy the H, filtering problem. 

However, that does not prove that the H, filtering solution does not exist (see Problem 11.13). 

## Example 11.5

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{x_{k}+w_{k}}}\\ {{}}&{{}}&{{x_{0}}}&{{=}}&{{0}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\\ {{z_{k}}}&{{=}}&{{x_{k}}}\end{array}$$

We will revisit Example 11.2, but assume that the initial state is 0: 

$$\text{(1)}$$. 

$$(11.140)$$

From Equation (11.131) we can find the a prioristeady-state filter that bounds the infinity-norm of the transfer function from e to 2 by l/&. (Recall that ek = [ 'Wk Vk ] *T.)* The algebraic Riccati equation associated with this problem is given by 

$$\begin{array}{r c l}{{P}}&{{=}}&{{1+P-P(1+P)^{-1}P+P(1/\theta+P)^{-1}P}}\\ {{}}&{{=}}&{{1+P-\frac{P^{2}}{1+P}+\frac{P^{2}}{1/\theta+P}}}\end{array}$$
$$(11.141)$$

Solving the above for P we obtain 

$$P={\frac{-\theta-1\pm{\sqrt{\theta^{2}-6\theta+5}}}{2(2\theta-1)}}$$
$$(11.142)$$
$$(11.143)$$
$$(11.144)$$

In order for the solution of this equation to solve the H, filtering problem, we must have P > 0. The only solution for which P > 0 is when 0 5 0 < 1/2 and when we use the negative sign in the above s~lution.~ If we choose 0 = 1/10 then P = 2. The gain of the a *priori* filter is then computed from Equation (11.131) as 

$$\begin{array}{r c l}{{K}}&{{=}}&{{P(1+P)^{-1}}}\\ {{}}&{{=}}&{{2/3}}\end{array}$$

Note that the P value tht i's obtained for 8 = 1/10 does not match Example 11.2, but K does match. The H, filter equation is computed from Equation (11.131) as 

$$\begin{array}{r c l}{{\hat{x}_{k+1}}}&{{=}}&{{\hat{x}_{k}+K(y_{k}-\hat{x}_{k})}}\\ {{}}&{{=}}&{{\hat{x}_{k}+(2/3)(y_{k}-\hat{x}_{k})}}\end{array}$$

vvv 

## 11.6 Summary

In this chapter, we have presented a couple of different approaches to H, estimation, also called minimax estimation. H, filtering minimizes the worst-case 5Note that Example 11.2 showed that this problem has a solution for 0 5 8 < 1, which indicates that the game theory approach to H, filtering may be more general than the transfer function approach. 

estimation error and is thus more robust than Kalman filtering, which minimizes the RMS estimation error. H, filtering has sometimes been criticized for being too pessimistic in its assumption about t-he noise processes that impinge on the system and measurement equations. After all, H, estimation assumes that the noise is worst case, thus attributinga degree of perversity to the noise that intuitively seems unrealistic. This has led to mixed Kalman/H, estimation techniques, which we will discuss in Chapter 12. 

Research in H, estimation began in the 1980s. During that decade, some work was directed toward the design of minimax state estimators for systems corrupted by random noise whose covariances were within known bounds [POOH, Dar84, Ver841. 

This was a first step toward H, filtering, although it still assumed that the noise was characterized by statistical measurements. The earliest work that could pass for what we now call H, filtering was probably published by Mike Grimble [Gri88]. However, unlike the presentation in this chapter, he used a frequency domain approach. He designed a state estimator such that the frequency response from the noise to the estimation error had a user-defined upper bound. 

Some early tutorials on H, filtering can be found in [Griglb, Sha921. A polynomial systems approach to H, filtering is presented in [GriSO]. Nonlinear H, filtering is discussed in [Rei99], where a stable state estimator with a bounded infinity-norm is derived. System identification using H, methods is discussed in [Sto94, Tse94, Bai95, Did95, Pan961. 

The effectiveness of the H, filter can be highly sensitive to the weighting functions [e.g., &, Po, Qk, *and* Rk in Equation (11.36), and 8 in the performance bound]. This sometimes makes H, filter design more sensitive than Kalman filter design (which is ironic, considering the higher degree of robustness in H, filtering). The advantages of H, estimation over Kalman filtering can be summarized as follows. 

1. H, filtering provides a rigorous method for dealing with systems that have model uncertainty. 

2. H, filtering provides a natural way to limit the frequency response of the estimator. 

The disadvantages of H, filtering compared to Kalman filtering can be summarized as follows. 

1. The filter performance is more sensitive to the design parameters. 

2. The theory underlying H, filtering is more abstract and complicated. 

The types of applications where H, filtering may be preferred over Kalman filtering could include the following. 

1. Systems in which stability margins must be guaranteed, or worst-case estimation performance is a primary consideration (rather than RMS estimation performance) [Sim96] . 

2. Systems in which the model changes unpredictably, and identification and gain scheduling are too complex or time-consuming. 

3. Systems in which the model is not well known. 

Work by Babak Hassibi, Ali Sayed, and Thomas Kailath involves the solution of state estimation problems within the context of Krein spaces (as opposed to the usual Hilbert space approach). This provides a general framework for both Kalman and H, filtering (along with other types of filtering), and is discussed in some of their papers [Has96a, Has96bI and books [Has99, KaiOO]. 

## Problems Written Exercises

Show that (I + A)-lA = A(I + *A)-1.* 
11.1 Consider a scalar system with F = H = 1 and with process noise and 11.2 measurement noise variances Q and R. Suppose a state estimator of the form 

$$\hat{x}_{k+1}^{-}=\hat{x}_{k}^{-}+K(y_{k}-\hat{x}_{k}^{-})$$

is used to estimate the state, where K is a general estimator gain. 

a) Find the optimal gain K if R = 2Q. Call this gain *KO.* What is the resulting steady-state a *priori* estimation-error variance? 

b) Suppose that R = 0. What is the optimal steady-state a *priori* estimationerror variance? What is the (suboptimal) steady-state a *priori* estimationerror variance if KO is used in the estimator? Repeat for R = Q and R = 5Q. 

11.3 Consider a scalar system with F = H = 1 and with process noise and measurement noise variances Q and R = 2Q. A Kalman filter is designed to estimate the state, but (unknown to the engineer) the process noise has a mean of a. 

a) What is the steady-state value of the mean of the a *priori* estimation error? 

b) Introduce a new state-vector element that is equal to a. Augment the new state-vector element to the original system so that a Kalman filter can be used to estimate both the original state element and the new state element. Find an analytical solution to the steady-state *a priori* estimation-error covariance for the augmented system. 

$$\begin{array}{r c l}{x_{k+1}}&{=}&{F x_{k}+w_{k}}\\ {y_{k}}&{=}&{H x_{k}+v_{k}}\end{array}$$

11.4 Suppose that a Kalman filter is designed to estimate the state of a scalar system. The assumed system is given as where Wk N (0, Q) and Vk N (0, R) _are uncorrelated zero-mean white noise processes. The actual system matrix is F = F + *AF.* 
a) Under what conditions is the mean of the steady-state value of the a *priori* state estimation error equal to zero? 

b) What is the steady-state value of the a *priori* estimation-error variance P? 

How much larger is P because of the modeling error AF? 

11.5 Find the stationary point of (2s + 2122 + *2223)* subject to the constraint Maximize **(142** - x2 + 6y - y2 + 7) subject to the constraints (x + y 5 2) 
(XI + 22 = 4) [MooOO]. 

11.6 and (x + 2y 5 3) [Lue84]. 

11.7 Consider the system 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\frac{1}{2}x_{k-1}+i w_{k-1}}}\\ {{y_{k}}}&{{=}}&{{x_{k}+v_{k}}}\end{array}$$

Note that this is the system model for the radiation system described in Problem **5.1.** 
a) Find the steady-state value of Pk for the H, filter, using a variable 8 and L = *R= Q=* S= 1. 

b) Find the bound on f3 such that the steady-state H, filter exists. 

11.8 Suppose that you use a continuous-time H, filter to estimate a constant on the basis of noisy measurements. The measurement noise is zero-mean and white with a covariance of R. Find the H, estimator gain as a function of *PO,* R, 8, and time. What is the limit of the estimator gain as t + *oo?* What is the maximum value of 8 such that the H, estimation problem has a solution? How does the value of 8 influence the estimator gain? 

11.9 Prove that 3-1 and 7? in Equations **(11.134)** and **(11.137)** are symplectic. 

11.10 Prove that the solution of the a *posteriori* H, Riccati equation given in Equation **(11.132)** with 6' = 0 is equivalent to the solution of the steady-state a priori Kalman filter Riccati equation with R = I and Q = I. 

11.11 Prove that C in Equation **(11.132)** with 8 = 0 is equivalent to the solution of the steady-state a *posteriori* Kalman filter Riccati equation with R = I and Q = I. 

11.12 Find the a *posteriori* steady-state H, filter for Example **11.5** when f3 = 
1/10, Verify that the a priori and *a posteriori* Riccati equation solutions satisfy Equation **(11.133).** 
11.13 Find all possible solutions P to the a *priori* H, filtering problem for Example **11.5** when 8 = 0. Next use Equation **(11.139)** to find the P solution. Repeat for f3 = 1/10. [Note that Equation **(11.139)** gives a negative solution for P and therefore cannot be used.] 

## Computer Exercises

11.14 Generate the time-varying solution to Pk for Problem 11.7 with PO = 1. 

What is the largest value of 6' for which Equation **(11.90)** will be satisfied for all k up to and including k = 20? Answer to the nearest **0.01.** Repeat for k = **10, k** = 5, and k = 1. 

11.15 Consider the vehicle navigation problem described in Example **7.12.** Design a Kalman filter and an H, filter to estimate the states of the system. Use the 

$$0\ \big]^{T}$$

following parameters. 

$=\;\;\;3$ . 
$$\boldsymbol{\mathcal{T}}$$
$${\mathfrak{u}}_{k}$$
$$\mathbf{0}$$
T=3 
$$\begin{array}{r l}{{\hat{\mathbf{\sigma}}}^{0}}&{{}}\\ {=}&{1}\\ {0}&{{}=\mathrm{\boldmath~\diag(4,4,1,1)~}}\\ {\hat{\mathbf{\sigma}}}&{{}=\mathrm{\boldmath~\diag(900,900)~}}\\ {\hat{\mathbf{\sigma}}}&{{}=\mathrm{\boldmath~\nabla~}0.9\pi}\\ {=}&{\hat{\mathbf{\sigma}}(0)={\left[\begin{array}{l l}{0}&{0}\end{array}\right]}}\end{array}$$
 $$\begin{array}{l}\omega_{R}\end{array}$$ $$\begin{array}{l}Q\end{array}$$ $$\begin{array}{l}R\end{array}$$ $$\begin{array}{l}\mbox{heading angle}\end{array}$$ $$\begin{array}{l}\omega_{R}\end{array}$$ = $$\begin{array}{l}\omega_{R}\end{array}$$
$$x(0)$$
heading angle = 0.9~ 
T z(0) = qo) = [ 0 0 0 0 ] 
Simulate the system and the filters for 300 seconds. In the H, filter use S = L = I 
and 6' = 0.0005. 

a) Plot the position estimation errors for the Kalman and H, filters. What are the RMS position estimation errors for the two filters? 

b) Now suppose that unknown to the filter designer, Uk = 2. Plot the position estimation errors for the Kalman and H, filters. What are the RMS position estimation errors for the two filters? 

c) What are the closed loop estimator eigenvalues for the Kalman and H, 
filters? Do their relative magnitudes agree with your intuition? 

d) Use MATLAB's DARE function to find the largest 6' for which a steadystate solution exists to the H, DARE. Answer to the nearest 0.0001. How well does the H, filter work for this value of *6'?* What are the closed-loop eigenvalues of the H, filter for this value of O? 