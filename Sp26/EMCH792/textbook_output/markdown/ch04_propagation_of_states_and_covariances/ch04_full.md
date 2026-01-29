---
type: chapter
chapter: 4
title: Propagation of states and covariances
---
# Propagation Of States And Covariances

In this chapter, we will begin with our mathematical description of a dynamic system, and then derive the equations that govern the propagation of the state mean and covariance. The material presented in this chapter is fundamental to the state estimation algorithm (the Kalman filter) that we will derive in Chapter 5. 

Section **4.1** covers discrete-time systems. Section **4.2** covers sampled-data systems, which are the most common types of systems found in the real world. In this type of system, the system dynamics are described by continuous-time differential equations, but the control and measurement signals are discrete time (e.g. , 
control based on a digital computer and measurements obtained at discrete times). Section **4.3** covers continuous-time systems. 

## 4.1 Discrete-Time Systems

Suppose we have the following linear discrete-time system: 
where Uk is a known input and Wk is Gaussian zero-mean white noise with covariance Qk. How does the mean of the state xk change with time? If we take the expected value of both sides of Equation **(4.1)** we obtain 

$$\begin{array}{r c l}{{\bar{x}_{k}}}&{{=}}&{{E(x_{k})}}\\ {{}}&{{=}}&{{F_{k-1}\bar{x}_{k-1}+G_{k-1}u_{k-1}}}\end{array}$$
$$(4.1)$$

$$w_{k-1}$$
$$(4.2)$$

Optimal State Estimation, First Edition. By Dan J. Simon ISBN 0471708585 **@ZOOS** John Wiley 8z **Sons, Inc.** 

$$107$$
$$(x_{k}-{\bar{x}}_{k})(\cdot\cdot\cdot)^{T}$$

How does the covariance of xk change with time? We can use Equations (4.1)
and (4.2) to obtain We therefore obtain the covariance of xk as the expected value of the above expression. Since (zk-1 - *fk-1)* is uncorrelated with *Wk-1,* we obtain 

$$\begin{array}{r c l}{{P_{k}}}&{{=}}&{{E\left[(x_{k}-{\bar{x}}_{k})(\cdot\cdot\cdot)^{T}\right]}}\\ {{}}&{{=}}&{{F_{k-1}P_{k-1}F_{k-1}^{T}+Q_{k-1}}}\end{array}$$
$$(4.4)$$

This is called a discretetime Lyapunov equation, or a Stein equation [Ste52]. We will see in the next chapter that Equations (4.2) and (4.4) are fundamental in the derivation of the Kalman filter. 

It is interesting to consider the conditions under which the discretetime Lyapunov equation has a steady-state solution. That is, suppose that Fk = F is a constant, and Qk = Q is a constant. Then we have the following theorem, whose proof can be found in [KaiOO, Appendix D]. 

Theorem 21 Consider the equation P = FPFT + Q where F and Q are real matrices. Denote by Xi(F) the eigenvalues of the F matrix. 

1. A unique solution P exists if and only if Xi(F)Xj(F) \# 1 **for** *all i, j. This* unique solution is symmetric. 

2. Note that the above condition includes the case of stable F, because if F is stable then all of *its eigenvalues are less than one in magnitude, so Xi(F)Xj(F)* # 1 **for** all i, j. Therefore, we see that if F is stable then the discrete-time Lyapunov equation has a solution P that is unique and symmetric. In this case, 
the solution can be written as 
$$P=\sum_{i=0}^{\infty}F^{i}Q(F^{T})^{i}$$
P = *C F%Q(F~)~* (4.5) 
3. If F is stable and Q is positive (semi)definite, then the unique solution P is symmetric and positive (semi)definite. 

4. If *F is stable, Q is positive semidefinite, and (F, Q112) is controllable, then P* 
is unique, symmetric, and positive definite. Note that Q112, the square root of *Q, is defined here as any matrix such that Q1/2(Q1/2)T* = Q. 

$$x_{k}=F_{k,0}x_{0}+\sum_{i=0}^{k-1}\left(F_{k,i+1}w_{i}+F_{k,i+1}G_{i}u_{i}\right)$$

Now let us look at the solution of the linear system of Equation (4.1): 

$$(4.5)$$
$$(4.6)$$

$$(4.7)$$

The matrix Fk,a is the state transition matrix of the system and is defined as 

$$\begin{array}{l l}{F_{k-1}F_{k-2}\cdot\cdot\cdot F_{i}}&{k>i}\\ {I}&{k=i}\\ {0}&{k<i}\end{array}$$

Fk,a = L I *k=i* (4.7) 
Notice from Equation (4.6) that Xk is a linear combination of **20,** *{wi},* and {ua}. 

If the input sequence {ua} is known, then it is a constant and can be considered to be a sequence of Gaussian random variables with zero covariance. If xo and *{.ti}* 
are unknown but are Gaussian random variables, then Xk in Equation (4.6) is a linear combination of Gaussian random variables. Therefore, Xk is itself a Gaussian random variable (see Example 2.4). But we computed the mean and covariance of Xk in Equations (4.2) and (4.4). Therefore 

$\bar{x}_{k}\sim N(\bar{x}_{k},P_{k})$ (4.8)
This completely characterizes Xk in a statistical sense since a Gaussian random variable is completely characterized by its mean and covariance. 

## Example4.1

A linear system describing the population of a predator z(1) and that of its prey x(2) can be written as 

$$x_{k+1}(1)=x_{k}(1)-0.8x_{k}(1)+0.4x_{k}(2)+w_{k}(1)$$ $$x_{k+1}(2)=x_{k}(2)-0.4x_{k}(1)+u_{k}+w_{k}(2)\tag{4.9}$$

In the first equation, we see that the predator population causes itself to decrease because of overcrowding, but the prey population causes the predator population to, increase. In the second equation, we see that the prey population decreases due to the predator population and increases due to an external food supply Uk. The populations are also subject to random disturbances (with respective variances 1 and 2) due to environmental factors. This system can be written in state-space form as 

$$x_{k+1}=\left[\begin{array}{cc}0.2&0.4\\ -0.4&1\end{array}\right]x_{k}+\left[\begin{array}{c}0\\ 1\end{array}\right]u_{k}+w_{k}$$ $$w_{k}\sim(0,Q)\quad Q={\rm diag}(1,2)\tag{4.10}$$

Equations (4.2) and (4.4) describe how the mean and covariance of the populations change with time. Figure 4.1 depicts the two means and the two diagonal elements of the covariance matrix for the first few time steps when 'ZLk = 1 and the initial conditions are set as 30 = [ 10 and PO = diag(40,40). 

It is seen that the mean and covariance eventually reach steady-state values given by 

T 
20 ] 

$$\begin{array}{r c l}{{\bar{x}}}&{{=}}&{{(I-F)^{-1}G u}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l}{{2.5}}&{{5}}\end{array}\right]^{T}}}\\ {{P^{\cdot}}}&{{\approx}}&{{\left[\begin{array}{l l}{{2.88}}&{{3.08}}\\ {{3.08}}&{{7.96}}\end{array}\right]}}\end{array}$$
$$(4.11)$$

The steady-state value of P can also be found directly (i.e., without simulation) using control system software.' Note that since F for this example is stable and Q is positive definite, Theorem 21 guarantees that P has a unique positive definite steady-state solution. 

![3_image_0.png](3_image_0.png)

![3_image_1.png](3_image_1.png)

$$\tilde{w}_{k}\sim(0,\tilde{Q}_{k})$$
$$(4.12)$$
$$(4.13)$$

Figure **4.1** State means **and** variances for Example 4.1. 
vvv In Equation (4.1), we showed the process noise directly entering the system dynamics. This is the convention that we use in this book. However, many times process noise is **first** multiplied by some matrix before it enters the system dynamics. That is, 

$$x_{k}=F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+L_{k-1}\tilde{u}_{k-1},$$
xk = Fk-1xk-l-k Gk-1Uk-l+ Lk-1Gk-1, Gk (0, *Qk)* (4.12) 
How can we put this into the conventional form of Equation (4.1)? Notice that the rightmost term of Equation (4.12) has a covariance given by 

$$\begin{array}{r c l}{{E\left[(L_{k-1}\tilde{w}_{k-1})(L_{k-1}\tilde{w}_{k-1})^{T}\right]}}&{{=}}&{{L_{k-1}E(\tilde{w}_{k-1}\tilde{w}_{k-1}^{T})L_{k-1}^{T}}}\\ {{}}&{{=}}&{{L_{k-1}\hat{Q}_{k-1}L_{k-1}^{T}}}\end{array}$$

Therefore, Equation (4.12) is equivalent to the equation zk = Fk-1zk-l -t Gk-iW-1 + Wk-1, Wk (0, *LkQkL;)* (4.14) 
This idea is illustrated in Sections 7.3.1 and 7.3.2. The same type of transformation can be made with noisy measurement equations. That is, the measurement equation 

$$w_{k}\sim(0,L_{k}Q_{k}L_{k}^{T})$$
$$(4.14)$$
$$(4.15)$$
$$y_{k}=H_{k}x_{k}+L_{k}\tilde{v}_{k},\ \ \ \ \tilde{v}_{k}\sim(0,\tilde{R}_{k})$$

$$(4.16)$$
yk = HkXk + *Lkck, fik* (0, *Rk)* (4.15) 
is equivalent to the measurement equation 

$$y_{k}=H_{k}x_{k}+v_{k},~~~~v_{k}\sim(0,L_{k}\tilde{R}_{k}L_{k}^{T})$$
Yk = Hkzk + vk, vk (0, *LkRkL;)* (4.16) 
lFor example, we can **use** the **MATLAB** Control System Toolbox function DLYAP(F, Q). 

## 4.2 Sampled-Data Systems

Now we move on to sampled-data systems, which are the most frequently encountered systems in practice. A sampled-data system is a system whose dynamics are described by a continuous-time differential equation, but the input only changes at discrete time instants, because (for example) the input is generated by a digital computer. In addition, we are interested in estimating the state only at discrete time instants. We are interested in obtaining the mean and covariance of the state only at discrete time instants. The continuous-time dynamics are described as 

$${\dot{x}}=A x+B u+w$$
X = AX + *Bu+ w* **(4.17)** 
From Chapter 1 we know that the solution of *z(t)* at some arbitrary time, say *tk,* 
is given as 

$$x(t_{k})=e^{A(t_{k}-t_{k-1})}x(t_{k-1})+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}[B(\tau)u(\tau)+w(\tau)]\,d\tau$$
$$\begin{array}{r c l}{{\Delta t}}&{{=}}&{{t_{k}-t_{k-1}}}\\ {{x_{k}}}&{{=}}&{{x(t_{k})}}\\ {{u_{k}}}&{{=}}&{{u(t_{k})}}\end{array}$$

Now assume that u(t) = *?Lk* for t E *[tk,tk+l];* that is, the control *u(t)* is piecewise constante2 If we make the definitions .\ 

$$(4.17)$$
$$(4.18)$$
$$(4.19)$$
$$(4.20)$$
$$x_{k}=e^{A\Delta t}x_{k-1}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}B(\tau)\,d\tau\,u_{k-1}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}w(\tau)\,d\tau$$

then Equation **(4.18)** becomes 

$$(4.21)$$
$$(4.22)$$
$$\begin{array}{r c l}{{F_{k}}}&{{=}}&{{e^{A\Delta t}}}\\ {{G_{k}}}&{{=}}&{{\int_{t_{k}}^{t_{k+1}}e^{A(t_{k+1}-\tau)}B(\tau)\,d\tau}}\end{array}$$
$$x_{k}=F_{k-1}x_{k-1}+G_{k-1}u_{k-1}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}w(\tau)\,d\tau$$

then Equation **(4.20)** becomes eA(tk-') is the state transition matrix of the system from time T to time *tk.* Now take the mean of the above equation, remembering that *w(t)* is zero-mean, to obtain 

$$\bar{\bar{x}}_{k}=E(x_{k})\tag{4.23}$$ $$=F_{k-1}\bar{x}_{k-1}+G_{k-1}u_{k-1}$$

2This assumes that a first-order hold is used for the control inputs. Other types of holds can be used in sampled data systems, but in this book we assume that first-order holds are used. 

$$P_{k}$$

We can use the previous equations to obtain the covariance of the state as 

Now, if we assume that w(t) is continuous-time white noise with a covariance of Qc(t), we see that 
$$E\left[w(\tau)w^{T}(\alpha)\right]=Q_{c}(\tau)\delta(\tau-\alpha)$$
This means that we can use the sifting property of the impulse function (see Problem 4.10) to write Equation (4.24) as 
$$\begin{array}{r c l}{{P_{k}}}&{{=}}&{{F_{k-1}P_{k-1}F_{k-1}^{T}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}Q_{c}(\tau)e^{A^{T}(t_{k}-\tau)}\,d\tau}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{F_{k-1}P_{k-1}F_{k-1}^{T}+Q_{k-1}}}\end{array}$$
where *Qk-1* is defined by the above equation; that is, 

$$Q_{k-1}=\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}Q_{c}(\tau)e^{A^{T}(t_{k}-\tau)}\,d\tau$$

In general, it is difficult to calculate *Qk-1,* but for small values of (tk - *tk-1)* we obtain 

$$(4.25)$$
$$(4.26)$$
$$(4.27)$$
$$e^{A(t_{k}-\tau)}\approx I\ {\rm for}\ \tau\in[t_{k-1},t_{k}]$$ $$Q_{k-1}\approx Q_{c}(t_{k})\Delta t\tag{4.28}$$

## Example4.2

Suppose we have a first-order, continuoustime dynamic system given by the equation 

$$\dot{x}=fx+w$$ $$E[w(t)w(t+\tau)]=qc\delta(\tau)\tag{4.29}$$

First-order equations can be used to describe many simple physical processes. For example, this equation describes the behavior of the current through a series RL circuit that is driven by a random voltage w(t), where f = *-R/L.* 
Suppose we are interested in obtaining the mean and covariance of the state z(t) every At time units; that is, tk - tk-1 = *At.* For this simple scalar 

$$Q_{k-1}=\int_{t_{k-1}}^{t_{k}}\exp[f(t_{k}-\tau)]q_{c}\exp[f(t_{k}-\tau)]\,d\tau\tag{4.30}$$ $$=\exp(2ft_{k})q_{c}\int_{t_{k-1}}^{t_{k}}\exp(-2f\tau)\,d\tau$$ $$=\exp(2ft_{k})q_{c}\left[\frac{\exp(-2ft_{k-1})-\exp(-2ft_{k})}{2f}\right]$$ $$=\frac{q_{c}}{2f}\left[\exp(2f(t_{k}-t_{k-1}))-1\right]$$ $$=\frac{q_{c}}{2f}\left[\exp(2f\Delta t)-1\right]$$
 $\large\begin{array}{rcll}Q_{k-1}&=&\\ &&\\ &=&\\ &&\approx&\\ &&\\ &=&\end{array}$  4. 
For small values of At, we can expand the above equation in a Taylor series around At = 0 to obtain 

$${\frac{q_{c}}{2f}}\left[\exp(2f\Delta t)-1\right]$$ $${\frac{q_{c}}{2f}}\left[\left(1+2f\Delta t+{\frac{(2f\Delta t)^{2}}{2!}}+\cdots\right)-1\right]$$ $${\frac{q_{c}}{2f}}\left[1+2f\Delta t-1\right]$$ $$q_{c}\Delta t$$
$$=F_{k-1}\bar{x}_{k-1}+G_{k-1}u_{k-1}\tag{4.32}$$ $$=\exp\left[f(t_{k}-t_{k-1})\right]\bar{x}_{k-1}+0$$ $$=\exp(f\Delta t)\bar{x}_{k-1}$$ $$=\exp(kf\Delta t)\bar{x}_{0}$$
$$(4.31)$$

This matches Equation (4.28), which says that for small At we have Qk-1 M 
qcAt. The sampled mean of the state is computed from Equation (4.23) [noting that the control input in Equation (4.29) is zero] as We see that if f > 0 (i.e., the system is unstable) then the mean Zk will increase without bound (unless 30 = 0). However, iff < 0 (i.e., the system is stable) then the mean Zk will decay to zero regardless of the value of *50.* The sampled covariance of the state is computed from Equation (4.26) as 

$$P_{k}=F_{k-1}P_{k-1}F_{k-1}^{T}+Q_{k-1}\tag{4.33}$$ $$\approx(1+2f\Delta t)P_{k-1}+q_{c}\Delta t$$ $$P_{k}-P_{k-1}=(2fP_{k-1}+q_{c})\Delta t$$

From the above equation, we can see that Pk reaches steady state (Le., Pk - 
pk-1 = 0) when Pk-1 = -qc/2f, assuming that f < 0. On the other hand, if f 2 0 then Pk - 9-1 will always be greater than 0, which means that limk,, Pk = *00.* 
vvv 

## 4.3 Continuous-Time Systems

In this section, we will look at how the mean and covariance of the state of a continuous-time linear system propagate. Consider the continuous-time system 

$${\dot{x}}=A x+B u+w$$
$$(4.34)$$
$$(4.35)$$
$$(4.36)$$

where *u(t)* is a known control input and w(t) is zero-mean white noise with a covariance of 

$$\Xi[w(t)w^{T}(\tau$$

E[W(t)WT(T)] = Qcd(t - 7) **(4.35)** 
By taking the mean of Equation **(4.34),** we can obtain the following equation for the derivative of the mean of the state: 

$${\bar{v}}(t-\tau)$$
$${\dot{\bar{x}}}=A{\bar{x}}+B u$$
P = A1 + Bu **(4.36)** 
This equation shows how the mean of the state propagates with time. The linear equation that describes the propagation of the mean looks very much like the original state equation, Equation **(4.34).** We can also obtain Equation **(4.36)** by using the equation that describes the mean of a sampled-data system and taking the limit as At = tk - *tk-1* goes to zero. Taking the mean of Equation **(4.'18)** gives 

$$(4.37)$$

The state transition matrix can be written as 

$$=e^{A\Delta t}$$ $$=I+A\Delta t+\frac{(A\Delta t)^{2}}{2!}+\cdots$$  is an be approximated as 
For small values of *At,* this can be approximated as 
$${\bar{x}}_{k}=e^{A\Delta t}{\bar{x}}_{k-1}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}B(\tau)u(\tau)\,d\tau$$
$\mu$
$$(4.38)$$
$$F\approx I+A\Delta t$$
$$(4.39)$$
$${\bar{x}}_{k}=(I+A\Delta t){\bar{x}}_{k-1}+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}B(\tau)u(\tau)\,d\tau$$

With this substitution Equation **(4.37)** becomes 

$$(4.40)$$

Subtracting *zk-1* from both sides and dividing by At gives 

$$(4.41)$$

Taking some limits as At goes to zero gives the following: 

$${\frac{\tilde{x}_{k}-\tilde{x}_{k-1}}{\Delta t}}=A\tilde{x}_{k-1}+{\frac{1}{\Delta t}}\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}B(\tau)u(\tau)\,d\tau$$
$$\begin{array}{r c l}{{\operatorname*{lim}_{\Delta t\to0}{\frac{\tilde{x}_{k}-\tilde{x}_{k-1}}{\Delta t}}}}&{{=}}&{{\dot{\tilde{x}}}}\\ {{\operatorname*{lim}_{\Delta t\to0}e^{A(t_{k}-\tau)}}}&{{=}}&{{I{\mathrm{~for~}}\tau\in[t_{k-1},t_{k}]}}\end{array}$$
$$(4.42)$$

Making these substitutions in **(4.41)** gives 

$${\dot{\bar{x}}}=A{\bar{x}}+B u$$
$$(4.43)$$

which is the same equation as the one we derived earlier in Equation **(4.36)** by a more direct method. Although the limiting argument that we used here was not necessary because we already had the mean equation in Equation **(4.36),** this method shows us how we can use limiting arguments (in general) to obtain continuous-time formulas. 

Next we will use a limiting argument to derive the covariance of the state of a continuous-time system. Recall the equation for the covariance of a sampled data system from Equation **(4.26):** 

$P_{k}=F_{k-1}P_{k-1}F_{k-1}^{T}+Q_{k-1}$ (4.44)
$$(4.46)$$
$$(4.47)$$
$$(4.48)$$
For small At we again approximate *Fk-1* as shown in Equation **(4.39)** and substitute into the above equation to obtain 

$$P_{k}\approx(I+A\Delta t)P_{k-1}(I+A\Delta t)^{T}+Q_{k-1}\tag{4.45}$$ $$=P_{k-1}+AP_{k-1}\Delta t+P_{k-1}A^{T}\Delta t+AP_{k-1}A^{T}(\Delta t)^{2}+Q_{k-1}$$

Subtracting *Pk-1* from both sides and dividing by At gives 

This can be written as 
- M *Qc(tk)* (4.48) 
$${\frac{Q_{k-1}}{\Delta t}}\approx Q_{c}(t_{k})$$
Therefore, taking the limit of Equation **(4.46)** as At goes to zero gives 
$$\frac{P_{k}-P_{k-1}}{\Delta t}=AP_{k-1}+P_{k-1}A^{T}+AP_{k-1}A^{T}\Delta t+\frac{Q_{k-1}}{\Delta t}$$  Recall from Equation (4.28) that for small $\Delta t$
$$Q_{k-1}\approx Q_{c}(t_{k})\Delta t$$
Qk-1 M *Qc(tk)At* **(4.47)** 
(4.46) as $\Delta t$ goes to zero give:
$${\dot{P}}=A P+P A^{T}+Q_{c}$$
$$(4.49)$$
P = AP + *PA^ +Q~* **(4.49)** 
This continuous-time Lyapunov equation, also sometimes called a Sylvester equation, gives us the equation for how the covariance of the state of a continuous-time system propagates with time. 

It is interesting to consider the conditions under which the continuous-time Lyapunov equation has a steady-state solution. That is, suppose that *A(t)* = A is a constant, and *Qc(t)* = Qc is a constant. Then we have the following theorem, whose proof can be found in [KaiOO, Appendix D]. 

Theorem 22 Consider the equation AP + PAT + Qc = 0 where A *and Qc are real* matrices. Denote by &(A) the eigenvalues of the A matrix. 

1. A unique solution P exists if and only if &(A) + Xj(A) \# 0 for all i, j. This unique solution is symmetric. 

2. Note that the above condition includes the case of stable A, because if A is stable then all of its eigenvalues have realparts less than 0, so Xi(A)+Xj(A) \# 
0 for all i, j. Therefore, we see that if A is stable then the continuous-time Lyapunov equation has a solution P that is unique and symmetric. In this case, the solution can be written as 

$$(4.50)$$
P = lw 
$$P=\int_{0}^{\infty}e^{A^{T}\tau}Q_{c}e^{A\tau}\,d\tau$$

3. If A is stable and Qc is positive (semi)definite, then the unique solution P is symmetric and positive (semi)definite. 

4. If A is stable, Qc is positive semidefinite, and **[A,** (Q,?'))'] is controllable, then P is unique, symmetric, and positive definite. Note that **Q;12,** *the square* root of Qc, is defined here as any matrix such that **Qi'2(Q;/2)T** = *Qc.* 

## Example4.3

Suppose we have the first-order, continuoustime dynamic system given by Equation **(4.29):** 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{f x+w}}\\ {{E[w(t)w(t+\tau)]}}&{{=}}&{{q_{c}\delta(\tau)}}\end{array}$$

where *w(t)* is zero-mean noise. The equation for the continuous-time propagation of the mean of the state is obtained from Equation **(4.36):** 

$$(4.51)$$
$$(4.52)$$
$${\dot{\bar{x}}}=f{\bar{x}}$$

&= fZ **(4.52)** 
Solving this equation for *Z(t)* gives 

$${\bar{x}}(t)=\exp(f t){\bar{x}}(0)$$
Z(t) = exp(ft)Z(O) **(4.53)** 
We see that the mean will increase without bound iff > 0 (i.e., if the system is unstable), but the mean will asymptotically tend to zero if f < 0 (i.e., if the system is stable). The equation for the continuous-time propagation of the covariance of the state is obtained from Equation **(4.49):** 

$${\dot{P}}=2f P+q_{c}$$
$$P(t)=\left(P(0)+{\frac{q_{c}}{2f}}\right)\exp(2f t)-{\frac{q_{c}}{2f}}$$
P=2fP+qc **(4.54)** 
Solving this equation for *P(t)* gives 

$$(4.53)$$
$$(4.54)$$
$$(4.55)$$

We see that the covariance will increase without bound if f > 0 (i.e., if the system is unstable), but the covariance will asymptotically tend to **-qc/2** f if f < 0 (i.e., if the system is stable). Compare these results with Example **4.2.** 
The steady-state value of P can also be computed using Equation **(4.50).** 
If we substitute f for A and qc for Qc in Equation **(4.50),** we obtain 

$$\begin{array}{r c l}{{P}}&{{=}}&{{\int_{0}^{\infty}e^{2f\tau}q_{c}\,d\tau}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{\left.\frac{q_{c}}{2f}e^{2f\tau}\right|_{0}^{\infty}}}\end{array}$$
$$\begin{array}{l}\left(4.56\right)\end{array}$$ . 
The integral converges for f < 0 (i.e., if the system is stable), in which case vvv P = -qc/2f. 

## 4.4 Summary

In this chapter, we have derived equations for the propagation of the mean and covariance of the state of linear systems. For discretetime systems, the mean and covariance are described by difference equations. Sampled-data systems are systems with continuous-time dynamics but control inputs that are constant between sample times. If the dynamics of a sampled-data system does not change between sample times, then the mean and covariance are described by difference equations, although the factors of the difference equations are more complicated than they are for discretetime systems. For continuous-time systems, the mean and covariance are described by differential equations. These results will form part of the foundation for our Kalman filter derivation in Chapter 5. 

The covariance equations that we studied in this chapter are named after Aleksandr Lyapunov, James Sylvester, and Philip Stein. Lyapunov was a Russian mathematician who lived from 1857 to 1918. He made important contributions in the areas of differential equations, system stability, and probability. Sylvester was an English mathematician and lawyer who lived from 1814 to 1897. He worked for a time in the United States as a professor at the University of Virginia and Johns Hopkins University. While at Johns Hopkins, he founded the American Journal of Mathematics, which was the first mathematical journal in the United States. 

## Problems Written Exercises

$${\frac{d}{d t}}\left(E[x]\right)=E\left[{\frac{d x}{d t}}\right]$$

4.1 Prove that 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{1}}\\ {{0}}&{{1/2}}\end{array}\right]x_{k-1}+\left[\begin{array}{l}{{0}}\\ {{1}}\end{array}\right]w_{k-1}}}\\ {{w_{k}}}&{{\sim}}&{{(0,1)}}\end{array}$$

4.2 Suppose that a dynamic scalar system is given as Xk+l = fxk + *Wk,* where Wk is zero-mean white noise with variance q. Show that if the variance of Xk is u2 for all k, then it must be true that f2 = (u2 - *q)/u2.* 
4.3 Consider the system where Wk is white noise. 

a) Find all possible steady-state values of the mean of zk. 

b) Find all possible steady-state values of the covariance of *Xk.* 
4.4 Consider the system of Example 1.2. 

a) Discretize the system to find the single step state transition matrix *Fk,* 
the discretetime input matrix **Gk,** and the multiplestep state transition matrix *Fk,%.* 
b) Suppose the covariance of the initial state is Po = diag( 1, 0), and zero-mean discrete-time white noise with a covariance of Q = diag(1,O) is input to the discrete-time system. Find a closed-form solution for *Pk.* 
4.5 Two chemical mixtures are poured into a tank. One has concentration c1 and is poured at rate *F1,* and the other has concentration cz and is poured at rate *F2.* The tank has volume V, and its outflow is at concentration c and rate F. This is typical of many process control systems [Kwa72]. The linearized equation for this system can be written as 
- 

$${\left[\begin{array}{l l}{-{\frac{F_{0}}{2V_{0}}}}&{0}\\ {0}&{-{\frac{F_{0}}{V_{0}}}}\end{array}\right]}\,x+{\left[\begin{array}{l l}{1}&{1}\\ {{\frac{c_{1}-c_{0}}{V_{0}}}}&{{\frac{c_{2}-c_{0}}{V_{0}}}}\end{array}\right]}\,w$$
$${\dot{x}}=$$

where *Fo,* VO, and Q are the linearization points of F, V, and c. The state x consists of deviations from the steady-state values of V and c, and the noise input w consists of the deviations from the steady-state values of F1 and *Fz.* Suppose that FO = 2V0, c1 - Q = Vo, and cz - Q = 2Vo. Suppose the noise input w has an identity covariance matrix. 

a) Use Equation (4.27) to calculate *Qk-1.* 
b) Use Equation (4.28) to approximate *Qk-1.* 
c) Evaluate your answer to part (a) for small (tk - *tk-1)* to verify that it matches your answer to part (b). 

4.6 Suppose that a certain sampled data system has the following state-transition matrix and approximate *Qk-1* matrix [as calculated by Equation (4.28)]: 

$$\begin{array}{r c l}{{F_{k-1}}}&{{=}}&{{\left[\begin{array}{c c}{{e^{-T}}}&{{0}}\\ {{0}}&{{e^{-2T}}}\end{array}\right]}}\\ {{Q_{k-1}}}&{{=}}&{{\left[\begin{array}{c c}{{2T}}&{{3T}}\\ {{3T}}&{{5T}}\end{array}\right]}}\end{array}$$

where T = *tk -tk-1* is the discretization step size. Use Equation (4.26) to compute the steady-state covariance of the state as a function of T. 

4.7 Consider the tank system described in Problem **4.5.** Find closed-form solutions for the elements of the state covariance as functions of time. 

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{\left[\begin{array}{l l}{{1/2}}&{{0}}\\ {{0}}&{{1/2}}\end{array}\right]x_{k}+w_{k}}}\\ {{w_{k}}}&{{\sim}}&{{(0,Q)}}\\ {{Q}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{1}}\\ {{0}}&{{1}}\end{array}\right]}}\end{array}$$

4.8 Consider the system Use Equation (4.5) to find the steady-state covariance of the state vector. 

4.9 The third condition of Theorem 21 gives a sufficient condition for the discretetime Lyapunov equation to have a unique, symmetric, positive semidefinite solution. Since the condition is sufficient but not necessary, there may be cases that do not meet the criteria of the third condition that still have a unique, symmetric, positive semidefinite solution. Give an example of one such case with a nonzero solution. 

4.10 which can be stated as Prove the sifting property of the continuous-time impulse function *6(t),* 

$$\int_{-\infty}^{\infty}f(t)\delta(t-\alpha)\,d t=f(\alpha)$$

## Computer Exercises

4.11 Write code for the propagation of the mean and variance of the state of Example **4.2.** Use *rno* = 1, PO = 2, f = **-0.5** and qc = 1. Plot the mean and variance of x for 5 seconds. Repeat for PO = 0. Based on the plots, what does the steady-state value of the variance appear to be? What is the analytically determined steady-state value of the variance? 

4.12 Consider the RLC circuit of Example 1.8 with R = L = C = 1. Suppose the applied voltage is continuous-time zero-mean white noise with a variance of 1. The initial capacitor voltage is a random variable with a mean of 1 and a variance of 1. The initial inductor current is a random variable (independent of the initial capacitor voltage) with a mean of 2 and a variance of 2. Write a program to propagate the mean and covariance of the state for five seconds. Plot the two elements of the mean of the state, and the three unique elements of the covariance. Based on the plots, what does the steady-state value of the covariance appear to be? What is the analytically determined steady-state value of the covariance? 

(Hint: The MATLAB function LYAP can be used to solve for the continuous-time algebraic Lyapunov equation.) 
4.13 Consider the RLC circuit of Problem 1.18 with R = 3, L = 1, and C = 
0.5. Suppose the applied voltage is continuous-time zero-mean white noise with a variance of 1. We can find the steady-state covariance of the state a couple of different ways. 

0 Use Equation **(4.49).** 0 Discretize the system and use Equation **(4.4)** along with the MATLAB function DLYAP. In this case, the discrete-time white noise covariance Q is related to the continuous-time white noise covariance Q, by the equation Q = *TQ,,* 
where T is the discretization step size (see Section 8.1.1). 

a) Analytically compute the continuous-time, -steady-state covariance of the state. 

b) Analytically compute the discretized steady-state covariance of the state in the limit as T 4 *00.* 
c) One way of measuring the distance between two matrices is by using the MATLAB function NORM to take the F'robenius norm of the difference between the matrices. Generate a plot showing the F'robenius norm of the difference between the continuous-time, steady-state covariance of the state, and the discretized steady-state covariance of the state for T between 0.01 and 1. 

PART II 

# The Kalman Filter

Optzmal State Estamataon, Fzrst *Edztzon.* By Dan J. Simon ISBN **0471708585** 02006 John Wiley li Sons. Inc. 