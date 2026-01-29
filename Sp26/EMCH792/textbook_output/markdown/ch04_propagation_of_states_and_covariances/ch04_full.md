---
type: chapter
chapter: 4
title: Propagation of states and covariances
---

[Image on page 1]


## CHAPTER 4


Propagation of states and covariances

In this chapter, we will begin with our mathematical description of a dynamic system, and then derive the equations that govern the propagation of the state mean and covariance. The material presented in this chapter is fundamental to the **state estimation algorithm (the Kalman filter) that we will derive in Chapter 5.** **Section 4.1 covers discrete-time systems. Section 4.2 covers sampled-data sys-** tems, which are the most common types of systems found in the real world. In this type of system, the system dynamics are described by continuous-time differ- ential equations, but the control and measurement signals are discrete time (e.g. , control based on a digital computer and measurements obtained at discrete times). **Section 4.3 covers continuous-time systems.**

**4.1 DISCRETE-TIME SYSTEMS**

Suppose we have the following linear discrete-time system:

**where U k  is a known input and W k  is Gaussian zero-mean white noise with covariance** **Q k .  How does the mean of the state x k  change with time? If we take the expected** **value of both sides of Equation (4.1) we obtain**


## z k  = E ( x k )
 
# = F k - 1 z k - 1  + G k - 1 U k - I


**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 @ZOOS John Wiley 8z Sons, Inc.**

**(4.2)**

**107**

---

**108**

*We therefore obtain the covariance of xk as the expected value of the above expres-* *sion. Since (zk-1 - f k - 1 )  is uncorrelated with Wk-1, we obtain*


## Pk = E [ ( X k  -fk)(***)T]


(4.4) *T* *= Fk-lPk-lFk-i+* *Qk-1*

This is called a discretetime Lyapunov equation, or a Stein equation [Ste52]. We will see in the next chapter that Equations (4.2) and (4.4) are fundamental in the derivation of the Kalman filter. It is interesting to consider the conditions under which the discretetime Lya- 
## punov equation has a steady-state solution. That is, suppose that Fk = F is a
 *constant, and Qk = Q is a constant. Then we have the following theorem, whose* proof can be found in [KaiOO, Appendix D].


# Theorem 21 Consider the equation P = FPFT + Q where F and Q are real
 **matrices. Denote by Xi(F) the eigenvalues of the F matrix.**


## 1. A unique solution P exists if and only if Xi(F)Xj(F) # 1 for all i, j .  This
 *unique solution is symmetric.*

**2. Note that the above condition includes the case of stable F, because if F is sta-** 
## ble then all of its eigenvalues are less than one in magnitude, so Xi(F)Xj(F) #
 **1 for all i, j .  Therefore, we see that if F is stable then the discrete-time Lya-** *punov equation has a solution P that is unique and symmetric. In this case,* *the solution can be written as*

m *P = C F % Q ( F ~ ) ~* (4.5)

**a=O**

**3. If F is stable and Q is positive (semi)definite, then the unique solution P is** *symmetric and positive (semi)definite.*

*4. If F is stable, Q is positive semidefinite, and (F, Q112) is controllable, then P* *is unique, symmetric, and positive definite. Note that Q112, the square root* **of Q, is defined here as any matrix such that Q1/2(Q1/2)T** *= Q.*

Now let us look at the solution of the linear system of Equation (4.1):

How does the covariance of xk change with time? We can use Equations (4.1) and (4.2) to obtain

(4.6)

---


[Image on page 3]


**109**

The matrix F k , a  is the state transition matrix of the system and is defined as

**F k - l F k - z * * * F a  k > i**

F k , a  = *I* **k = i** (4.7) L **k < i**

**Notice from Equation (4.6) that Xk is a linear combination of 20, {wi},** and {ua}. If the input sequence {ua} is known, then it is a constant and can be considered to **be a sequence of Gaussian random variables with zero covariance. If xo and {.ti}** are unknown but are Gaussian random variables, then Xk in Equation (4.6) is a linear combination of Gaussian random variables. Therefore, Xk is itself a Gaussian random variable (see Example 2.4). But we computed the mean and covariance of

Xk in Equations (4.2) and (4.4). Therefore

xk N(zk, pk) (4.8)

This completely characterizes Xk in a statistical sense since a Gaussian random variable is completely characterized by its mean and covariance.

**EXAMPLE4.1**

**A linear system describing the population of a predator z(1) and that of its** prey x(2) can be written as

T k + l ( l ) = X k ( 1 )  - 0.8~k(1) + 0.4~k(2) + U ) k ( l )

Xk+1(2) = xk(2) - 0.4~k(1) + uk + wk(2) (4.9)

In the first equation, we see that the predator population causes itself to de- crease because of overcrowding, but the prey population causes the predator population to, increase. In the second equation, we see that the prey pop- ulation decreases due to the predator population and increases due to an external food supply Uk. The populations are also subject to random distur- bances (with respective variances 1 and 2) due to environmental factors. This system can be written in state-space form as

wk *N* *( O , Q )* Q =diag(l,2) (4.10)

Equations (4.2) and (4.4) describe how the mean and covariance of the popula- tions change with time. Figure 4.1 depicts the two means and the two diagonal elements of the covariance matrix for the first few time steps when 'ZLk = 1 
## and the initial conditions are set as 30 = [ 10
 *and PO = diag(40,40).* It is seen that the mean and covariance eventually reach steady-state values given by

**T** 20 ]

z = ( I - F ) - ~ G ~


## = [ 2.5 5 1'


(4.11)

---


[Image on page 4]


**110**

The steady-state value of P can also be found directly (i.e., without simula- *tion) using control system software.' Note that since F for this example is* stable and Q is positive definite, Theorem 21 guarantees that P has a unique positive definite steady-state solution.

**vO** **2** **4** **6** **0** 10 **12** **14**

**time step**

**Figure 4.1 State means and variances for Example 4.1.**

vvv In Equation (4.1), we showed the process noise directly entering the system dynamics. This is the convention that we use in this book. However, many times **process noise is first multiplied by some matrix before it enters the system dynamics.** That is,


## xk = F k - 1 x k - l - k  G k - 1 U k - l +
 **Lk-1Gk-1,** **Gk** **(0, Q k )** (4.12)

How can we put this into the conventional form of Equation (4.1)? Notice that the rightmost term of Equation (4.12) has a covariance given by


## E [(Lk-lGk-l)(Lk-lGk-l)T] = Lk-IE(Gk-lG;-'_1)L;-l
 
## = L k - l Q k - I L k - 1
 **-** **T** (4.13)

Therefore, Equation (4.12) is equivalent to the equation


# z k  = Fk-1zk-l -t Gk-iW-1 + Wk-1,
 **W k** 
## (0, LkQkL;)
 (4.14)

This idea is illustrated in Sections 7.3.1 and 7.3.2. The same type of transformation can be made with noisy measurement equations. That is, the measurement equation


# y k  = H k X k  + L k c k ,
 **fik** **(0, R k )** (4.15)

is equivalent to the measurement equation


# Yk = H k z k  + v k ,
 **v k** 
## (0, LkRkL;)
 (4.16)

**lFor example, we can use the MATLAB Control System Toolbox function DLYAP(F, Q).**

---


[Image on page 5]


## 111


**4.2** **SAMPLED-DATA SYSTEMS**

Now we move on to sampled-data systems, which are the most frequently encoun- **tered systems in practice. A sampled-data system is a system whose dynamics are** described by a continuous-time differential equation, but the input only changes at discrete time instants, because (for example) the input is generated by a digital computer. In addition, we are interested in estimating the state only at discrete time instants. We are interested in obtaining the mean and covariance of the state **only at discrete time instants. The continuous-time dynamics are described as**


# X = AX + Bu+ w
 **(4.17)**

**From Chapter 1 we know that the solution of z(t) at some arbitrary time, say t k ,** **is given as**

**J t k - i**


## Now assume that u(t) = ?Lk for t E [ t k , t k + l ] ;  that is, the control u(t) is piecewise
 constante2 If we make the definitions

. \

**(4.19)**

**then Equation (4.18) becomes**

**(4.21)**

**then Equation (4.20) becomes**

**eA(tk-') is the state transition matrix of the system from time T to time t k .  Now** **take the mean of the above equation, remembering that w(t) is zero-mean, to obtain**


## z k  = E ( x k )
 
## = Fk-1Zk-l -k G k - i U k - 1
 **(4.23)**

2This assumes that a first-order hold is used for the control inputs. Other types of holds can be **used in sampled data systems, but in this book we assume that first-order holds are used.**

---

**112**

**We can use the previous equations to obtain the covariance of the state as**

Now, if we assume that w(t) is continuous-time white noise with a covariance of **Qc(t), we see that** 
# E [w(r)w'(a)] = Q c ( 7 ) 6 ( ~  - a)
 (4.25)

This means that we can use the sifting property of the impulse function (see Prob- lem 4.10) to write Equation (4.24) as


## P k  = F k - i p k - i F r - 1  -k
 **eA(tk-7) QC(** **T)eAT ( t k - T )  d r** **L1** 
## = F k - l p k - l F k - 1
 **T -k Qk-1** (4.26)

**where Qk-1 is defined by the above equation; that is,**

**T** *t k* **eA(tk -7) Qc(T)eA ( t k - 7 )  dr** (4.27) 
# *lc-l = Lk-l


# In general, it is difficult to calculate Q k - 1 ,  but for small values of ( t k  - t k - 1 )  we
 obtain

(4.28)

**EXAMPLE4.2**

Suppose we have a first-order, continuoustime dynamic system given by the equation

(4.29)

First-order equations can be used to describe many simple physical processes. For example, this equation describes the behavior of the current through a *series RL circuit that is driven by a random voltage w(t), where f = -R/L.* Suppose we are interested in obtaining the mean and covariance of the state 
## z(t) every At time units; that is, t k  - t k - 1  = At. For this simple scalar


---

**113**

(4.30)

For small values of At, we can expand the above equation in a Taylor series around At = 0 to obtain

% [1+ 2fAt - 11 2f (4.31)

**This matches Equation (4.28), which says that for small At we have Qk-1 M** qcAt. The sampled mean of the state is computed from Equation (4.23) **[noting that the control input in Equation (4.29) is zero] as**

We see that if f > 0 (i.e., the system is unstable) then the mean Zk will 
## increase without bound (unless 30 = 0). However, iff < 0 (i.e., the system is
 **stable) then the mean Zk will decay to zero regardless of the value of 50. The** **sampled covariance of the state is computed from Equation (4.26) as**

**T** p k  = F k - l P k - l F k - 1 -k Qk-1


# M (1 + 2fAt)Pk-1 +qcAt


p k  - 9 - 1  = (2fpk-1 -k qc)At (4.33)

From the above equation, we can see that P k  reaches steady state (Le., P k  -

p k - 1  = 0) when P k - 1  = -qc/2f, assuming that f < 0. On the other hand, *if f 2 0 then P k  - 9 - 1  will always be greater than 0, which means that* limk,, *P k  = 00.* vvv

---


[Image on page 8]


**114**


## 4.3
 
## CONTINUOUS-TIME SYSTEMS


In this section, we will look at how the mean and covariance of the state of a continuous-time linear system propagate. Consider the continuous-time system


# X = AX + Bu + w


**where u(t) is a known control input and w(t) is zero-mean white noise with a** covariance of

**By taking the mean of Equation (4.34), we can obtain the following equation for** the derivative of the mean of the state:

**(4.34)**

**E[W(t)WT(T)]** 
## = Qcd(t - 7 )
 **(4.35)**


# P = A1 + Bu
 **(4.36)**

This equation shows how the mean of the state propagates with time. The linear equation that describes the propagation of the mean looks very much like the orig- **inal state equation, Equation (4.34). We can also obtain Equation (4.36) by using** the equation that describes the mean of a sampled-data system and taking the limit 
# as At = tk - tk-1 goes to zero. Taking the mean of Equation (4.'18) gives


The state transition matrix can be written as

**AAt** *F* *=* *e* **(AAt)2** **2!**

**For small values of At, this can be approximated as**


## = I + A A t + - + - . -


**F w I + A A t**

**With this substitution Equation (4.37) becomes**

**Subtracting z k - 1  from both sides and dividing by At gives**

**Taking some limits as At goes to zero gives the following:**

**1** - 
# P k  - 1 k - 1
 lim - **At-0** **At** 
## lim eA(tk-T) = I for T E [tk-l,tk]
 **At-0**

**Making these substitutions in (4.41) gives**


# i = A5 + Bu


**(4.37)**

**(4.38)**

**(4.39)**

**(4.40)**

**(4.41)**

**(4.42)**

**(4.43)**

---

**115**

**which is the same equation as the one we derived earlier in Equation (4.36) by a more** direct method. Although the limiting argument that we used here was not necessary **because we already had the mean equation in Equation (4.36), this method shows us** how we can use limiting arguments (in general) to obtain continuous-time formulas. Next we will use a limiting argument to derive the covariance of the state of a continuous-time system. Recall the equation for the covariance of a sampled data **system from Equation (4.26):**

**(4.44)**

**For small At we again approximate Fk-1 as shown in Equation (4.39) and substitute** into the above equation to obtain

*Pk* 
# M (I + AAt)Pk-,(I + AAt)T + Qk-1
 *= Pk-l+ APk-lAt + Pk-lATAt + APk-1AT(At)2 + Qk-1* **(4.45)**

*Subtracting Pk-1 from both sides and dividing by At gives*

**Recall from Equation (4.28) that for small At**

**Qk-1 M Qc(tk)At** **(4.47)**

This can be written as - 
## M Qc(tk)
 **(4.48)** *Q k - i* *At* **Therefore, taking the limit of Equation (4.46) as At goes to zero gives**


# P = AP + PA^ + Q ~
 **(4.49)**

This continuous-time Lyapunov equation, also sometimes called a Sylvester equa- tion, gives us the equation for how the covariance of the state of a continuous-time system propagates with time. It is interesting to consider the conditions under which the continuous-time Lya- *punov equation has a steady-state solution. That is, suppose that A(t) = A is* *a constant, and Qc(t) = Qc is a constant. Then we have the following theorem,* whose proof can be found in [KaiOO, Appendix D].


# Theorem 22 Consider the equation AP + PAT + Qc = 0 where A and Qc are real
 *matrices. Denote by &(A) the eigenvalues of the A matrix.*

*1. A unique solution P exists if and only if &(A) + Xj(A) # 0 for all i, j .  This* *unique solution is symmetric.*

*2. Note that the above condition includes the case of stable A, because if A is* *stable then all of its eigenvalues have realparts less than 0, so Xi(A)+Xj(A) #* *0 for all i, j .  Therefore, we see that if A is stable then the continuous-time* *Lyapunov equation has a solution P that is unique and symmetric. In this* *case, the solution can be written as*


# P = lw
 *eATrQceAr d7* **(4.50)**

---

**116**

**3. If A is stable and Qc is positive (semi)definite, then the unique solution P is**


## 4. If A is stable, Qc is positive semidefinite, and [A, (Q,?'))'] is controllable,


**then P is unique, symmetric, and positive definite. Note that Q;12, the square** 
## root of Qc, is defined here as any matrix such that Qi'2(Q;/2)T = Qc.


*symmetric and positive (semi)definite.*

**EXAMPLE4.3**

Suppose we have the first-order, continuoustime dynamic system given by **Equation (4.29):**


## i = f z + w
 *E"W(t)'W(t +.)I* = **Q C b ( . r )** **(4.51)**

*where w(t) is zero-mean noise. The equation for the continuous-time propa-* **gation of the mean of the state is obtained from Equation (4.36):**

& =  f Z **(4.52)**

*Solving this equation for Z(t) gives*

*Z(t) = exp(ft)Z(O)* **(4.53)**

We see that the mean will increase without bound iff > 0 (i.e., if the system is unstable), but the mean will asymptotically tend to zero if f < 0 (i.e., if the system is stable). The equation for the continuous-time propagation of **the covariance of the state is obtained from Equation (4.49):**

*P=2fP+qc* **(4.54)**

*Solving this equation for P(t) gives*

**(4.55)**

We see that the covariance will increase without bound if f > 0 (i.e., if the **system is unstable), but the covariance will asymptotically tend to -qc/2 f if** 
## f < 0 (i.e., if the system is stable). Compare these results with Example 4.2.
 **The steady-state value of P can also be computed using Equation (4.50).** **If we substitute f for A and qc for Qc in Equation (4.50), we obtain**

*00* *P =* *e2frqcdr*

*00* **(4.56)**


## The integral converges for f < 0 (i.e., if the system is stable), in which case


vvv


## P = -qc/2f.


---

**117**

**4.4** 
## SUMMARY


In this chapter, we have derived equations for the propagation of the mean and covariance of the state of linear systems. For discretetime systems, the mean and covariance are described by difference equations. Sampled-data systems are sys- tems with continuous-time dynamics but control inputs that are constant between sample times. If the dynamics of a sampled-data system does not change between sample times, then the mean and covariance are described by difference equations, although the factors of the difference equations are more complicated than they are for discretetime systems. For continuous-time systems, the mean and covari- ance are described by differential equations. These results will form part of the **foundation for our Kalman filter derivation in Chapter 5.** The covariance equations that we studied in this chapter are named after Alek- sandr Lyapunov, James Sylvester, and Philip Stein. Lyapunov was a Russian math- ematician who lived from 1857 to 1918. He made important contributions in the areas of differential equations, system stability, and probability. Sylvester was an English mathematician and lawyer who lived from 1814 to 1897. He worked for a time in the United States as a professor at the University of Virginia and Johns *Hopkins University. While at Johns Hopkins, he founded the American Journal of* *Mathematics, which was the first mathematical journal in the United States.*

**PROBLEMS**

**Written exercises**

**4.1 Prove that**

**4.2** 
# Suppose that a dynamic scalar system is given as X k + l  = f x k  + W k ,  where


## W k  is zero-mean white noise with variance q. Show that if the variance of X k  is u2
 
# for all k, then it must be true that f2 = (u2 - q)/u2.


**4.3** Consider the system

**where W k  is white noise.** a) Find all possible steady-state values of the mean of zk. **b) Find all possible steady-state values of the covariance of X k .**

**a) Discretize the system to find the single step state transition matrix F k ,** **the discretetime input matrix G k ,  and the multiplestep state transition** **matrix F k , % .**

**4.4** Consider the system of Example 1.2.

---


[Image on page 12]


**118**


## b) Suppose the covariance of the initial state is Po = diag( 1, 0), and zero-mean
 
## discrete-time white noise with a covariance of Q = diag(1,O) is input to
 **the discrete-time system. Find a closed-form solution for Pk.**

**4.5** **Two chemical mixtures are poured into a tank. One has concentration c1 and** 
## is poured at rate F1, and the other has concentration cz and is poured at rate F2.
 
## The tank has volume V, and its outflow is at concentration c and rate F .  This is
 typical of many process control systems [Kwa72]. The linearized equation for this **system can be written as**

1 l l


# x = [  - 2 L  - & I . + [ -
 0 -

vo vo


## where Fo, VO, and Q are the linearization points of F, V, and c. The state x
 consists of deviations from the steady-state values of V and c, and the noise input **w consists of the deviations from the steady-state values of F1 and Fz. Suppose** 
# that FO = 2V0, c1 - Q = Vo, and cz - Q = 2Vo. Suppose the noise input w has an
 identity covariance matrix. **a) Use Equation (4.27) to calculate Qk-1.** **b) Use Equation (4.28) to approximate Qk-1.** 
# c) Evaluate your answer to part (a) for small ( t k  - t k - 1 )  to verify that it
 matches your answer to part (b).

Suppose that a certain sampled data system has the following state-transition **4.6** **matrix and approximate Q k - 1  matrix [as calculated by Equation (4.28)]:**

0 **Fk-1** 
# = [ "OT e-zT ]


## where T = t k  - t k - 1  is the discretization step size. Use Equation (4.26) to compute
 *the steady-state covariance of the state as a function of T.*

**4.7** 
## Consider the tank system described in Problem 4.5. Find closed-form solu-
 **tions for the elements of the state covariance as functions of time.**

**4.8** Consider the system

Use Equation (4.5) to find the steady-state covariance of the state vector.

**4.9** The third condition of Theorem 21 gives a sufficient condition for the discrete- time Lyapunov equation to have a unique, symmetric, positive semidefinite solution. Since the condition is sufficient but not necessary, there may be cases that do not meet the criteria of the third condition that still have a unique, symmetric, positive semidefinite solution. Give an example of one such case with a nonzero solution.

---

**119**

**4.10** which can be stated as *Prove the sifting property of the continuous-time impulse function 6(t),*

*00*

**Computer exercises**

**4.11 Write code for the propagation of the mean and variance of the state of** 
## Example 4.2. Use rno = 1, PO = 2, f = -0.5 and qc = 1. Plot the mean and
 
## variance of x for 5 seconds. Repeat for PO = 0. Based on the plots, what does
 the steady-state value of the variance appear to be? What is the analytically determined steady-state value of the variance?


## 4.12 Consider the RLC circuit of Example 1.8 with R = L = C = 1. Suppose
 the applied voltage is continuous-time zero-mean white noise with a variance of 1. The initial capacitor voltage is a random variable with a mean of 1 and a variance of 1. The initial inductor current is a random variable (independent of the **initial capacitor voltage) with a mean of 2 and a variance of 2. Write a program** to propagate the mean and covariance of the state for five seconds. Plot the two elements of the mean of the state, and the three unique elements of the covariance. Based on the plots, what does the steady-state value of the covariance appear to be? What is the analytically determined steady-state value of the covariance? (Hint: The MATLAB function LYAP can be used to solve for the continuous-time algebraic Lyapunov equation.)


## 4.13 Consider the RLC circuit of Problem 1.18 with R = 3, L = 1, and C =
 0.5. Suppose the applied voltage is continuous-time zero-mean white noise with a variance of 1. We can find the steady-state covariance of the state a couple of different ways.

**0 Use Equation (4.49).**


## 0 Discretize the system and use Equation (4.4) along with the MATLAB func-
 *tion DLYAP. In this case, the discrete-time white noise covariance Q is related* *to the continuous-time white noise covariance Q, by the equation Q = TQ,,* *where T is the discretization step size (see Section 8.1.1).*

a) Analytically compute the continuous-time, -steady-state covariance of the state. **b) Analytically compute the discretized steady-state covariance of the state** *in the limit as T 4 00.*


## c) One way of measuring the distance between two matrices is by using the
 MATLAB function NORM to take the F’robenius norm of the difference between the matrices. Generate a plot showing the F’robenius norm of the difference between the continuous-time, steady-state covariance of the *state, and the discretized steady-state covariance of the state for T between* 0.01 and 1.

---


# PART II


THE KALMAN FILTER


[Image on page 15]


*Optzmal State Estamataon, Fzrst Edztzon. By Dan J. Simon* **ISBN 0471708585** *02006 John Wiley li Sons. Inc.*