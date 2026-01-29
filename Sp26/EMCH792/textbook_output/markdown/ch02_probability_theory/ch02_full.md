---
type: chapter
chapter: 2
title: Probability theory
---

[Image on page 1]


## CHAPTER 2


Probability theory

*The most we can know is in terms of probabilities.* --Richard Feynman [Fey63, p. 6-11]

*While writing my book [Stochastic Processes, first published in 19531 I had an argument* with Feller. He asserted that everyone said “random variable” and I asserted that **everyone said “chance variable.” We obviously had to use the same name in our books,** so we decided the issue by a stochastic procedure. That is, we tossed for it and he won. -Joseph Doob [Sne97, p. 3071

Probabilities do not exist. -Bruno de Finetti [deF74]

In our &tempt to filter a signal, we will be trying to extract meaningful informa- tion from a noisy signal. In order to accomplish this, we need to know something about what noise is, some of its characteristics, and how it works. This chapter reviews probability theory. We begin by discussing the basic concept of probability **in Section 2.1, and then move on to random variables (RVs) in Section 2.2. The** chapter then continues with the following topics:


## 0 An RV is a general case of the normal scalars that we are familiar with, and
 
## so just as we can apply a functional mapping to a number, we can also apply


**Optimal State Estimation, First Edition. By Dan J. Simon** **ISBN 0471708585 02006 John Wiley & Sons, Inc.** **49**

---


[Image on page 2]


**50**

**a**

**a**

**a**

a functional mapping to an RV. We discuss functions (transformations) of random variables in Section 2.3.

**Just as we can have vectors of numbers, we can also have vectors of RVs, and** **so we discuss groups of random variables and random vectors in Section 2.4.**

**Just as we can have scalar functions of time, we can also have RVs that are** functions of time, and so we discuss RVs that change with time (stochastic processes) in Section 2.5.

Stochastic processes can be divided into two categories: white noise and col- ored noise, and we discuss these concepts in Section 2.6.

We conclude in Section 2.7 with a high-level discussion of how to write a computer simulation of a noise process. This chapter is only a brief introduction and review of probability and stochastic processes, and more detail can be found in many other books on the subject, such **as [Pap02, PeeOl].**


## 2.1 PROBABILITY


How shall we define the concept of probability? Suppose we run an experiment a **certain number of times. Sometimes event A occurs and sometimes it does not. For** **instance, our experiment may be rolling a six-sided die. Event A may be defined** **as the number 4 showing up on the top surface of the die after we roll the die.** **Common sense tells us that the probability of event A occuring is 1/6. Likewise,** we would expect that if we run our experiment many times, then we would see the number 1 appearing about 1/6 of the time. This intuitive explanation forms the basis for our formal description of the concept of probability. We define the **probability of event A as**

(2.1) **Number of times A occurs** Total number of outcomes 
## P(A) =


This commonsense understanding of probability is called the relative frequency **definition. A more formal and mathematically rigorous definition of probability** can be obtained using set theory [Bi195, Nel871, which was pioneered by Andrey Kolomogorov in the 1930s. But for our purposes, the relative frequency definition is adequate. **In general, we know that there are n-choose-k different ways of selecting Ic objects** from a total of n objects (assuming that the order of the objects does not matter), **where n-choose-k is denoted and defined as**

n! ( ) = (n - k)!k!

For instance, suppose we have a penny (P), nickel (N), dime (D), and quarter (Q). How many distinct subsets of three coins can we pick from that set? We can pick PND, PNQ, PDQ, or NDQ, for a total of four possible subsets. This is equal to 4choose-3.

---

**51**

**EXAMPLE2.1**

What is the probability of being dealt four of a kind' in poker? The total number of possible poker hands can be computed as the total number of **subsets of size five that can be picked from a deck of 52 cards. The total** 
## number of possible hands is 52-choose5 = 2,598,960. Out of all those hands,
 **there are 48 possible hands containing four aces, 48 possible hands containing** 
## four kings, and so on. So there are a total of 13 x 48 hands containing four of
 a kind. Therefore the probability of being dealt four of a kind is


## = 1/4165


**M 0.024%**

vvv **The conditional probability of event A given event B can be defined if the prob-** **ability of B is nonzero. The conditional probability of A given B is defined as**

**P(A1B) is the conditional probability of A given B, that is, the probability that A** **occurs given the fact that B occurred. P(A,B) is the joint probability of A and** **B, that is, the probability that events A and B both occur. The probability of a** **single event [for instance, P(A) or P(B)] is called an a priori probability because it** applies to the probability of an event apart from any previously known information. **A conditional probability [for instance, P(AIB)] is called an a posteriori probability** because it applies to a probability given the fact that some information about a possibly related event is already known. **For example, suppose that A is the appearance of a 4 on a die, and B is the** 
## appearance of an even number on a die. P(A) = 1/6. But if we know that the die
 
## has an even number on it, then P(A) = 1/3 (since the even number could be either
 **a 2, 4, or 6). This example is intuitive, but we can also obtain the answer using** **Equation (2.4). P(A, B) is the probability that both A occurs (we roll a 4) and B** 
## occurs (we roll an even number), so P(A, B) = 1/6. So Equation (2.4) gives


## = 1/3
 **(2.5)**

**The a priori probability of A is 1/6. But the a posteriori probability of A given B** **is 1/3.**

**EXAMPLE2.2**

**Cnsider the eight shapes in Figure 2.1. We have three circles and five squares,** 
## so P(circ1e) = 3/8. Only one of the shapes is a gray circle, so P(gray, circle)


**'Once I was dealt four sevens while playing poker with some friends (unfortunately, I was not** **playing for money at the time). I don't expect to see it again in my lifetime.**

---


[Image on page 4]


**52**

= 1/8. Of the three circles, only one is gray, so P(gray I circle) = 1/3. This **last probability can be computed using Equation (2.4) as**

P(gray, circle) *P( circle)* P(graylcirc1e) =

**Figure 2.1 Some shapes for illustrating probability and Bayes’ Rule.**

vvv 
## Note that we can use Equation (2.4) to write P(BIA) = P(A,B)/P(A). We
 **can solve both this equation and Equation (2.4) for P(A,B) and equate the two** **expressions for P(A, B) to obtain Bayes’ Rule.**


## P(AIB)P(B) = P(BIA)P(A)
 (2.7)

Bayes’ Rule is often written by rearranging the above equation to obtain

**As an example, consider Figure 2.1. The probability of picking a gray shape given** **the fact that the shape is a circle can be computed from Bayes’ Rule as**

*P( circle1 gray) P( gray)* P(circ1e) P(graylcirc1e) =

We say that two events are independent if the occurrence of one event has no effect **on the probability of the occurrence of the other event. For example, if A is the** **appearance of a 4 after rolling a die, and B is the appearance of a 3 after rolling** **another die, then A and B are independent. Mathematically, independence of A** *and B can be expressed several different ways. For example, we can write*


## P(A,B) = P(A)P(B)
 
## P(AIB) = P(A)
 
## P(B1A) = P(B)
 (2.10)


[Image on page 4]


---


[Image on page 5]


**53**

**if A and B are independent. As an example, recall from Equation (2.5) that if A** **is the appearance of a 4 on a die, and B is the appearance of an even number on** 
## a die, then P(A) = 1/6 and P(A1B) = 1/3. Since P(A1B) # P(A)
 **we see that A** **and B are dependent events.**

**2.2** **RANDOM VARIABLES**

We define a random variable (RV) as a functional mapping from a set of experi- **mental outcomes (the domain) to a set of real numbers (the range). For example,** the roll of a die can be viewed as a RV if we map the appearance of one dot on the die to the output one, the appearance of two dots on the die to the output two, and so on. *Of course, after we throw the die, the value of the die is no longer a random* variable - it becomes certain. The outcome of a particular experiment is not an RV. If we define X as an RV that represents the roll of a die, then the probability that X will be a four is equal to 1/6. If we then roll a four, the four is a realization of the RV X. If we then roll the die again and get a three, the three is another realization of the RV X. However, the RV X exists independently of any of its realizations. This distinction between an RV and its realizations is important for understanding the concept of probability. Realizations of an RV are not equal to 
## the RV itself. When we say that the probability of X = 4 is equal to 1/6, that
 means that there is a 1 out of 6 chance that each realization of X will be equal to **4. However, the RV X will always be random and will never be equal to a specific** value. An RV can be either continuous or discrete. The throw of a die is a discrete random variable because its realizations belong to a discrete set of values. The high temperature tomorrow is a continuous random variable because its realizations belong to a continuous set of values. The most fundamental property of an RV X is its probability distribution func- **tion (PDF)** *F x ( x ) ,  defined as*

*F x ( x )  = P ( X  5 z)* (2.11)

**In the above equation, F x ( x )  is the PDF of the RV X, and z is a nonrandom** **independent variable or constant. Some properties of the PDF that can be obtained** from its definition are

*The probability density function (pdf) f x ( x )  is defined as the derivative of the* PDF.

(2.13)

---


[Image on page 6]


**54**

Some properties of the pdf that can be obtained from this definition are


## F X b )  = s_a.(.)dz


## J_mfx(z)dz = 1


## P ( a < z I b )  = JIbfX(s)d5


## fX(2) 2 0
 *00*

(2.14)

The Q-function of an RV is defined as one minus the PDF. This is equal to the probability that the RV is greater than the argument of the function:

(2.15)

Just as we spoke about conditional probabilities in Equation (2.4), we can also speak about the conditional PDF and the conditional pdf. The conditional distribution **and density of the RV X given the fact that event A occurred are defined as**


## Fx(2lA) = P(X5zlA)


(2.16)

Bayes’ Rule, discussed in Section 2.1, can be generalized to conditional densities. **Suppose we have random variables XI and X 2 .  The conditional pdf of the RV X 1** **given the fact that RV X 2  is equal to the realization 2 2  is defined as**

(2.17)

Although this is not entirely intuitive, it can be derived without too much diffi- culty [PapOS, PeeOl]. Now consider the following product of two conditional pdf’s:

- 
# - f ( 5 1 , 2 2 , 2 3 , 2 4 )
 
## f (54)
 
## = f [ ( X l ,  52,53)1541
 (2.18)

**Note that in the above equation we have dropped the subscripts on the f(.) func-** tions for ease of notation. This is commonly done if the random variable associated with the pdf is clear from the context. This is called the Chapman-Kolmogorov equation [Pap02]. It can be extended to any number of RVs and is fundamental to the Bayesian approach to state estimation (Chapter 15). **The expected value of an RV X is defined as its average value over a large number** of experiments. This can also be called the expectation, the mean, or the average of

---


[Image on page 7]


**55**

*the RV. Suppose we run the experiment N times and observe a total of m different* 
## outcomes. We observe that outcome A1 occurs n1 times, A2 occurs n2 times, . . .,
 **and A,,, occurs n, times. Then the expected value of X is computed as**

**.** **m** **E(X)** = *I A i n ,* N **2=1** (2.19)

**E(X)** **is also often written as E(x),** **X,** **or 2.** **At this point, we will begin to use lowercase x instead of uppercase X when the** **meaning is clear. We have been using uppercase X to refer to an RV, and lowercase** **x to refer to a realization of the RV, which is a constant or independent variable.** **However, it should be clear that, for example, E(x) is the expected value of the RV** **X,** **and so we will interchange x and X in order to simplify notation.** As an example of the expected value of an RV, suppose that we roll a die an infinite number of times. We would expect to see each possible number (one through six) 1/6 of the time each. We can compute the expected value of the roll of the die **as**

1

**N+-m N** 
## E(X) =
 lim - [(1)(N/6) +...+ (6)(N/6)]

= 3.5 (2.20)

Note that the expected value of an RV is not necessarily what we would expect to see when we run a particular experiment. For example, even though the above **expected value of X is 3.5, we will never see a 3.5 when we roll a die.** We can also talk about a function of an RV, just as we can talk about a function of any scalar. (We will discuss this in more detail in Section 2.3.) If a function, **say g(X),** acts upon an RV, then the output of the function is also an RV. For 
## example, if X is the roll of a die, then P(X = 4) = 1/6. If g(X) = X2,
 then **P[g(X)** 
## = 161 = 1/6. We can compute the expected value of any function g(X)
 as

**J-00** (2.21)


## where fx(x) is the pdf of X. If g(X) = X, then we can compute the expected
 **value of X as**

(2.22) **J --m**

The variance of an RV is a measure of how much we expect the RV to vary from its mean. The variance is a measure of how much variability there is in an RV. In **the extreme case, if the RV X always is equal to one value (for example, the die** 
## is loaded and we always get a 4 when we roll the die), then the variance of X is
 *equal to 0. On the other extreme, if X can take on any value between ztco with* 
## equal probability, then the variance of X is equal to 00. The variance of an RV is
 formally defined as

(2.23)

---


[Image on page 8]


**56**

The standard deviation of an RV is 0, which is the square root of the variance. **Sometimes we denote the standard deviation as ox if we need to be explicit about** the RV whose standard deviation we are discussing. Note that the variance can be written as


## g 2  = E [ X 2 - - 2 X 1 + 2 2 ]


# E ( X 2 )  - 212 + 1 2
 
## = E ( X 2 ) - Z 2
 =

We use the notation 
# x N (z,a2)


**(2.24)**

**(2.25)**


## to indicate that X is an RV with a mean of 5 and a variance of g2.


Skew is defined as The skew of an RV is a measure of the asymmetry of the pdf around its mean.


# skew = E [ ( X  - Z ) 3 ]
 **(2.26)**

The skewness, also called the coefficient of skewness, is the skew normalized by the cube of the standard deviation:

skewness = skew/g3 **(2.27)**

**In general, the ith moment of a random variable X is the expected value of the** **ith power of X .  The ith central moment of a random variable X is the expected** **value of the ith power of X minus its mean:**

**ith moment of X** 
## = E(X')
 **ith central moment of X** 
# = E [ ( X  - Z)']
 **(2.28)**

For example, the first moment of a random variable is equal to its mean. The first central moment of a random variable is always equal to 0. The second central moment of a random variable is equal to its variance. An RV is called uniform if its pdf is a constant value between two limits. This in- **dicates that the RV has an equally likely probability of obtaining any value between** its limits, but a zero probability of obtaining a value outside of its limits:

**x E [a,b]** 0 otherwise **(2.29)**

**Figure 2.2 shows the pdf of an RV that is uniformly distributed between fl. Note** **that the area of this curve is one (as is the area of all pdf's).**

**EXAMPLE 2.3**

In this example we will find the mean and variance of an RV that is uniformly **distributed between 1 and 3. The pdf of the RV is given as**

**112 x E [1,3]** 0 otherwise **(2.30)**

---


[Image on page 9]


**57**


# 0.4 t
 I

**X**

**Figure 2.2** **Probability density function of an RV uniformly distributed between fl.**

**The mean is computed as follows:** **6**

*= [ i x d z*

**=** **2**

The variance is computed as follows:


# = l3
 
# i(z - 2)2 dx


vvv An RV is called Gaussian or normal if its pdf is given by

**1** *-(x - Z)2* *f X ( 2 )  = -* afiexp [ **2a2 I**

**(2.31)**

**(2.32)**

**(2.33)**

This is called the Laplace distribution in France, but it had many other discoverers, **including Robert Adrain. Note that Z and 0 in the above pdf are the mean and** standard deviation of the Gaussian RV. We use the notation x *N N(5,02)* **(2.34)**


## to indicate that X is a Gaussian RV with a mean of Z and a variance of 02.
 **Figure 2.3 shows the pdf of a Gaussian RV with a mean of zero and a variance**

---


[Image on page 10]


**58**

**0.4**

**0.35**

**0.3**


## p 0.25.


**0.2-**


# v -
 '0

**0.15**

of one. If the mean changes, the pdf will shift to the left or right. If the variance increases, the pdf will spread out. If the variance decreases, the pdf will be squeezed in. The PDF of a Gaussian RV is given by

-

-

-

-

(2.35)

This integral does not have a closed-form solution, and so it must be evaluated nu- merically. However, its evaluation can be simplified by considering the normalized Gaussian PDF of an RV with zero mean and unity variance:

(2.36)

It can be shown that any Gaussian PDF can be expressed in terms of this normalized **PDF as**

(2.37)

**In addition, a Gaussian PDF can be approximated as the following closed-form** expression [Bor79]:

*a = 0.339*


## b = 5.510


**0.45**

**0.05** O ' l I

**n** **I**

*I L*

(2.38)

**2** **-** **3** **-** **2** **-** **1** **0** **1** **2** **3** **4** **X**

**Figure 2.3** variance of one. Probability density function of a Gaussian RV with a mean of zero and a

Suppose we have a random variable X with a mean of zero and a symmetric pdf [i.e., fx(x) = fx(-x)]. This is the case, for example, for the pdf's shown in

---


[Image on page 11]


**59**

Figures 2.2 and 2.3. In this case, the ith moment of X can be written as


## If i is odd then xz = -(-z)~. Combined with the fact that fx(x) = fx(-z), we
 see that

(2.40)

So for odd i, the ith moment in Equation (2.39) is zero. We see that all of the odd moments of a zero-mean random variable with a symmetric pdf are equal to 0.


## 2.3
 **TRANSFORMATIONS OF RANDOM VARIABLES**

In this section, we will look at what happens to the pdf of an RV when we pass the *RV through some function. Suppose that we have two RVs, X and Y ,  related to* *one another by the monotonic2 functions g(.) and h(.):*


$$
y = dX)
$$
 
$$
x = g-l(Y) =h(Y)
$$
 (2.41)

If we know the pdf of X [fx(x)], *then we can compute the pdf of Y [fy(y)] as* follows:

**P(X E [x,** 
$$
x + dz]) = P(Y E [Y,
$$
 Y + dy]) (dx > 0)

if dy > 0 if dy < 0

(2.42)

where we have used the assumption of small dx and dy in the above calculation.

**'A monotonic function is a function whose slope is either always nonnegativeor always nonpositive.** If the slope is always nonnegative, then the function is monotonically nondecreasing. If the slope is always positive, then the function is monotonically increasing. If the slope is always nonpositive, then the function is monotonically nonincreasing. If the slope is always negative, then the function is monotonically decreasing.

---


[Image on page 12]


**60**

**EXAMPLE2.4**

**In this example, we will find the pdf of a linear function of a Gaussian RV.** 
# Suppose that X N N (3, u;) and Y = g ( X )  = aX + b, where a # 0 and b are
 any real constants. Then 
$$
x = h(Y)
$$
 *= (Y - b)/a*

*h‘(y) = l / a*

fY(Y) = Ih’(Y)IfX[h(Y)l I = lAl-exp{ 1 *-[(y - b)/a - 212* 
## a u x f i
 2u: I - 1 { -[y - (aZ+b)]2 - a u x a 2 a 2 4


## g = a Z + b


**In other words, the RV Y is Gaussian with a mean and variance given by**

**u:** = a2a:

(2.43)

(2.44)

**This important example shows that a linear transformation of a Gaussian RV** **results in a new Gaussian RV.** vvv

**EXAMPLE2.5**


## Suppose that we pass a Gaussian RV X N N(0,u;) through the nonlinear
 
## function Y = g(X) = X3:
 
$$
x = h(Y)
$$
 - 
# - yv3
 y-2/3

fY(Y) = Ih’(Y)lfX[h(Y)l


$$
h’(Y) = 3
$$


(2.45)


## We see that the nonlinear transformation Y = X 3  converts a Gaussian RV
 
## to a non-Gaussian RV. It can be seen that f ~ ( y )  approaches 00 as y + 0.
 Nevertheless, the area under the fy(y) curve is equal to 1 since it is a pdf. vvv 
## In the more general case of RVs related by the function Y = g(X), where g(.) is
 *a nonmonotonic function, the pdf of Y (evaluated at y) can be computed from the* pdf of X as *~ Y ( Y )  = C fx(za)/Ig’(zt)I* (2.46)

**a**

---


[Image on page 13]


61


## where the 2% values are the solutions of the equation y = g(z).


**2.4** **MULTIPLE RANDOM VARIABLES**

We have already defined the probability distribution function of an RV. For exam- **ple, if X and Y are RVs, then their distribution functions are defined as**

**(2.47)**


# Now we define the probability that both X I z and Y I y as the joint probability
 **distribution function of X and Y:**


## FXY(X, y) = P(X 5 2, y 5 9)
 **(2.48)**

If the meaning is clear from the context, we often use the shorthand notation **F(z, y) to represent the distribution function Fxy(x, y). Some properties of the** joint distribution function are

**F ( z , d  E [ O J I** *F(z,-oo)=F(-oo,y)* = 0 F(m,oo) = 1 *F(a,c) 5 F(b,d)* 
# if a I b and c I d
 
# P(u < 2 I b, c < y I d) = F(b, d )  + F(u, C) - F(u, d )  - F(b, C)
 *F(z,oo) = F ( x )*

F(W,Y) = F(Y) **(2.49)**

Note from the last two properties that the distribution function of one RV can be obtained from the joint distribution function. When the distribution function for a single RV is obtained this way it is called the marginal distribution function. **The joint probability density function is defined as the following derivative of** the joint PDF:

**(2.50)**

**As before, we often use the shorthand notation f(z,y) to represent the density** function f x y ( z ,  y). Some properties of the joint pdf that can be obtained from this definition are

*P(u < x 5 b, c < y 5 d)*

f (Y) **(2.51)**

---


[Image on page 14]


**62**

Note from the last two properties that the density function of one RV can be obtained from the joint density function. When the density function for a single RV is obtained this way it is called the marginal density function. Computing the *expected value of a function g(., .) of two RVs is similar to computing the expected* value of a function of a single RV:

**(2.52)**


## 2.4.1
 **Statistical independence**

**Recall from Section 2.1 that two events are independent if the occurrence of one** event has no effect on the probability of the occurrence of the other event. We **extend this to say that RVs X and Y are independent if they satisfy the following** relation: **(2.53)**

From our definition of joint distribution and density functions, we see that this implies


## P(X 5 2, Y 5 y) = P(X 5 z)P(Y 5 y)
 **for all 2, y**

**F X Y  (2,** 
## Y) = FX(.)FY (Y)


**f X Y  (2,** 
## Y) = f X ( Z ) f Y  (Y)
 **(2.54)**

The central limit theorem says that the sum of independent RVs tends toward a Gaussian RV, regardless of the pdf of the individual RVs that contribute to the sum. This is why so many RVs in nature seem to have a Gaussian distribution. Many RVs in nature are actually the sum of many individual and independent RVs. For example, the high temperature on any given day in any given location tends to follow a Gaussian distribution. This is because the high temperature is affected by clouds, precipitation, wind, air pressure, humidity, and other factors. Each of these factors is in turn determined by other random factors. The combination of many independent random variables determines the high temperature, which has a Gaussian pdf. **We define the covariance of two scalar RVs X and Y as**


## c x y  = E[(X-X)(Y
 **-Y]** 
## = E(XY)-XP
 **(2.55)**

**We define the correlation coefficient of two scalar RVs X and Y as**

**(2.56)**

The correlation coefficient is a normalized measurement of the independence be- 
## tween two RVs X and Y. If X and Y are independent, then p = 0 (although the
 
## converse is not necessarily true). If Y is a linear function of X then p = f l  (see
 **Problem 2.9).** **We define the correlation of two scalar RVs X and Y as**


## Rxy = E(XY)
 **(2.57)**


## Two RVs are said to be uncorrelated if Rxy = E(X)E(Y).


---

**63**

**From the definition of independence, we see that if two RVs are independent** then they are also uncorrelated. Independence implies uncorrelatedness, but un- correlatedness does not necessarily imply independence. However, in the special **case in which two RVs are both Gaussian and uncorrelated, then it follows that** they are also independent. 
## Two RVs are said to be orthogonal if Rxy = 0. If two RVs are uncorrelated,
 **then they are orthogonal only if at least one of them is zero-mean. If two RVs are** orthogonal, then they may or may not be uncorrelated.

**EXAMPLE2.6**

**Two rolls of the dice are represented by the RVs X and Y .  The two RVs are** independent because one roll of the die does not have any effect on a second **roll of the die. Each roll of the die has an equally likely probability (1/6) of** **being a 1, 2, 3, 4, 5, or 6. Therefore,**

**1 + 2 + 3 + 4 + 5 + 6** **6** *E ( X )  = E ( Y )  =*


## = 3.5
 **(2.58)**

**There are 36 possible combinations of the two rolls of the die. We could get** **the combination (l,l), (1,2), and so on. Each of these 36 combinations have** **an equally likely probability (1 /36). Therefore, the correlation between X** *and Y is*

**6** **6** **1** *R x y = E ( X Y )  = zyrij*


$$
z=1 j=l
$$
 
## = 12.25
 *= E ( X ) E ( Y )* **(2.59)**

*Since E ( X Y )  = E ( X ) E ( Y ) ,  we see that X and Y are uncorrelated. However,* *R x y  # 0, so X and Y are not orthogonal.* vvv


## H EXAMPLE2.7


## A slot machine is rigged so you get 1 or -1 with equal probability the first spin
 *X ,  and the opposite number the second spin Y .  We have equal probabilities of* **obtaining ( X ,  Y )  outcomes of (1, -1) and (-1,l). The two RVs are dependent** **because the realization of Y depends on the realization of X .  We also see that**


## E(X) = 0
 *E(Y) = 0*

*= -1* **(2.60)**

*We see that X and Y are correlated because E ( X Y )  # E ( X ) E ( Y ) .  We also* *see that X and Y are not orthogonal because E ( X Y )  # 0.* vvv

---


[Image on page 16]


**64**

**EXAMPLE2.8**


## A slot machine is rigged so you get -1, 0, or +1 with equal probability the
 *first spin X .  On the second spin Y you get 1 if X = 0, and 0 if X # 0. The* *two RVs are dependent because the realization of Y depends on the realization* *of X .  We also see that*

**- 1 + 0 + 1** **3** *E ( X )  =* = o 0 + 1 + 0 **3** *E(Y) =*

= o **(2.61)**

*We see that X and Y are uncorrelated because E(XY) = E ( X ) E ( Y ) .  We* *also see that X and Y are orthogonal because E(XY) = 0. This example* illustrates the fact that uncorrelatedness does not necessarily imply indepen- dence. vvv

**EXAMPLE2.9**

*Suppose that x and y are independent RVs, and the RV z is computed as* 
$$
z = g(x) + h(y). In this example, we will calculate the mean of z:
$$


*E(z) = E[g(4 +h(Y)l*

**(2.62)**

As a special case of this example, we see that the mean of the sum of two independent RVs is equal to the sum of their means. That is,

*E(z + y) = E(z) + E(y)* if x and y are independent **(2.63)**

vvv

**EXAMPLE 2.10**

Suppose we roll a die twice. What is the expected value of the sum of the two *outcomes? We use X and Y to refer to the two rolls of the die, and we use*

---

**65**


# 2 to refer to the sum of the two outcomes. Therefore, 2 = X + Y.
 **Since X** and Y are independent, we have

*E ( 2 )  = E ( X ) + E ( Y )* 
## = 3.5+3.5
 = 7 **(2.64)**

VVQ

**EXAMPLE 2.11**

**Consider the circuit of Figure 2.4. The input voltage V is uniformly dis-** tributed on [-1,1]. Voltage V has units of volts, and the two currents have units of amps.

0 i f V > O **I1** = { V i f V I O

V i f V 2 O 0 i f V < O **I2** = { **(2.65)**

**We see that I1 is uniformly distributed on [-1,0] and I2 is uniformly dis-** **tributed on [0,1]. The RVs V, 11, and I2 have expected values**

E(V) = 0 
## E(I1) = -1/2
 
## E(12) = 1/2
 **(2.66)**

**The RVs I1 and I2 are not independent because they are related to each other;** 
## if I2 # 0 then 11 = 0, and if I1 # 0 then I2 = 0. Since either 11 or I2 is equal
 
## to 0 at every time instant, I14 = 0 and E(IlI2) = 0. Therefore 11 and 12 are
 
## orthogonal. Since E(Il)E(I2) = -1/4, we see that E(I1I2) # E(Il)E(I2),
 **and I1 and I2 are correlated.**

**Figure 2.4** Circuit for Example 2.11.

vvv

**2.4.2** **Multivariate statistics**

The discussion in the previous subsection can be generalized for RVs that are vec- tors. In this case, the quantities defined earlier become vectors and matrices. Given

---


[Image on page 18]


**66**

**an n-element RV X and an rn-element RV Y (assuming that both X and Y are** column vectors), their correlation is defined as

(2.67) - -

Their covariance is defined as


# c x y  = E[(X - X)(Y - F)T]
 
## = E(XYT)-XPT


**The autocorrelation of the n-element RV X is defined as**

(2.68)


## Rx = E[XXT]


(2.69) **E[X?]** ***** ***** **a** 
## EIXIXn]


**EIXnX1]** * * * **E[X3**

**Note that E(X,X,)** 
## = E(X,X,)
 *so Rx = R$. An autocorrelation matrix is always* *symmetric. Also note that for any n-element column vector z we have*

(2.70)

So an autocorrelation matrix is always positive semidefinite. **The autocovariance of the n-element RV X is defined as**


## c x  = E[(X-X)(X-X)T]
 
# E[(X1 - Q 2 ]


(2.71) 1


## * * * E[(X1
 
# - X1)(Xn - Xn)]


# E[(Xn - %I2]
 = [ **E[(Xn** 
## - Xn)(X1-
 **XI)]** *

- - [ * . .  ““1

**Unl** ***** **.** **a** **u;**


## Note that u,j = uj, so Cx = CT. An autocovariance matrix is always symmetric.
 *Also note that for any n-element column vector z we have*


## zTCxz = zTE[(X
 
# - X)(X - X)T]z
 
# E[zT(X - X)(X - X)TZ]
 
## = E[(zT(X
 
# - X))2]
 =

**L O** (2.72)

---

**67**

So an autocovariance matrix is always positive semidefinite. An n-element RV X is Gaussian ( n ~ r m a l ) ~ if

Now consider a Gaussian RV X that undergoes a linear transformation:

**(2.73)**

**(2.74)**


## where A is a constant n x n matrix, and b is a constant n-element vector. If A is
 invertible, then

**(2.75)**

**From Equation (2.42) we obtain**

v 
## N N(AZ+b,ACxAT)
 **(2.76)**

This shows that normality is preserved in linear transformations of random vec- tors (just as it is preserved in linear transformations of random scalars, as seen in **Example 2.4).**

3Fkancis Edgeworth (1845-1926), an Irish economist and mathematician, first provided a general description and study of the multivariate Gaussian probability distribution in 1892 [Sor80].

---


[Image on page 20]


**68**

**2.5** 
## STOCHASTIC PROCESSES


**A stochastic process, also called a random process, is a very simple generalization** **of the concept of an RV. A stochastic process X ( t )  is an RV X that changes with** **time.4 A stochastic process can be one of four types.**


## 0 If the RV at each time is continuous and time is continuous, then X ( t )  is a
 continuous random process. For example, the temperature at each moment of the day is a continuous random process because both temperature and time are continuous.


## 0 If the RV at each time is discrete and time is continuous, then X ( t )  is a discrete
 random process. For example, the number of people in a given building at each moment of the day is a discrete random process because the number of people is a discrete variable and time is continuous.


## 0 If the RV at each time is continuous and time is discrete, then X ( t )  is a
 continuous random sequence. For example, the high temperature each day is a continuous random sequence because temperature is continuous but time is discrete (day one, day two, etc.).


## 0 If the RV at each time is discrete and time is discrete, then X ( t )  is a discrete
 random sequence. For example, the highest number of people in a given building each day is a discrete random sequence because the number of people is a discrete variable and time is also discrete.

Since a stochastic process is an RV that changes with time, it has a distribution *and density function that are functions of time. The PDF of X ( t )  is*

*F x ( x , t )  = P ( X ( t )  5 x )* (2.77)

*If X ( t )  is a random vector, then the inequality above is an element-by-element* *inequality. For example, if X ( t )  has n elements, then*

*The pdf of X ( t )  is*

**(2.78)**

(2.79)

*If X ( t )  is a random vector, then the derivative above is taken once with respect to* 
## each element of 2. For example, if X ( t )  has n elements, then


(2.80)

*The mean and covariance of X ( t )  are also functions of time:*

*00* *z(t) = S _ _ x f ( z , t ) d x*

4Actually, the independent variable does not have to be time; for example, it could be spatial location or something else. But typically the independent variable is time, and in this book it will always be time.

---


[Image on page 21]


**69**

*(2.81)*

**Note that X(t) at two different times (tl and t2) comprise two different random** **variables [X(tl) and X(t2)l. Therefore, we can talk about the joint distribution** **and joint density functions of X(t1) and X(t2). These are called the second-order** distribution function and the second-order density function:

*(2.82)*

**As discussed earlier, if X(t) is an n-element random vector, then the inequality** 
## that defines F(Q, z2, tl, t2) actually consists of 2 n  inequalities, and the derivative
 
## that defines f(sl,z2, tl, t2) actually consists of 2 n  derivatives.
 **The correlation between the two RVs X(t1) and X(t2) is called the autocorrela-** **tion of the stochastic process X(t):**


## RX(tl,t2) = E [X(tl)XT(t2)]
 *(2.83)*

The autocovariance of a stochastic process is defined as

*(2.84)*

For some stochastic processes, the pdf does not change with time. For example, **if we flip a coin ten times then we can view that process as a stochastic process** with the statistics of the process being the same at each of the ten time instances. In this case, the stochastic process is called strict-sense stationary (SSS), or just stationary for short. In this case, the mean of the stochastic process is constant with respect to time, and the autocorrelation is a function of the time difference


## t2 - tl (not a function of the absolute times):


*(2.85)*

For some stochastic processes, these two conditions are true even though the pdf does change with time. Stochastic processes for which these two conditions are **true are called widesense stationary (WSS). A stationary process is widesense** stationary, but a widesense stationary process may or may not be stationary. From the definition of autocorrelation, it can be shown that for a widesense stationary process the following properties hold:


## Rx(O) = EIX(t)XT(t)l
 Rx(-.) 
$$
= Rx(.)
$$
 *(2.86)*

For scalar stochastic processes, it can be shown that

---


[Image on page 22]


**70**

**EXAMPLE 2.12**

1. The high temperature each day can be considered a stochastic process. How- ever, this process is not stationary. The high temperature on a day in July might be an RV with a mean of 100 degrees Fahrenheit, but the high tem- **perature on a day in December might have a mean of 30 degrees. This is** a stochastic process whose statistics change with time, so the process is not stationary.

**2. Electrical noise in a voltmeter might have a mean of zero and a variance of** one millivolt. If we come back the next day and measure the noise again, **the mean and variance may be the same as before. If the statistics of the** noise are the same every day, then the electrical noise is a stationary process. Note that in reality the noise statistics will eventually change. For example, after a few decades the instrument will begin degrading and the electrical noise mean and variance will change. In this sense, there is no such thing as a stationary random process. Eventually, the universe will freeze and all signals will change. But for practical purposes, if the statistics of a random process do not change over the time interval of interest, then we consider the process to be stationary.

**3. Tomorrow’s closing price of the Dow Jones Industrial Average might be an** RV with a certain mean and variance. However, 100 years ago the closing price had a mean that was much lower. The closing price of the stock market is an RV whose mean generally increases with time. Therefore, the stock market price is a nonstationary stochastic process.

vvv *Suppose we have a stochastic process X ( t ) .  Further suppose that the process* *has a realization z(t). The time average of X ( t )  is denoted as A[X(t)], and the* **time autocorrelation of X ( t )  is denoted as R[X(t)]. These quantities are defined** **for continuous-time random processes as**

*rT* *A[X(t)] =* 
# lim I]
 *z(t)dt* **T+m 2T** *-T* 
$$
R[X(t), ‘r] = A[X(t)XT(t 4- T ) ]
$$
 *(2.88)*

The definitions for discretetime random processes are straightforward extensions of the continuoustime definitions. 
## An ergodic process is a stationary random process for which


(2.89)

In the real world, we are often limited to only a few realizations of a stochastic process. For example, if we measure the fluctuation of a voltmeter reading, we are actually only measuring only one realization of a stochastic process. We can compute the time average, time autocorrelation, and other time-based statistics of the realization. If the random process is ergodic, then we can use those time averages to estimate the statistics of the stochastic process.

---

**71**

**EXAMPLE 2.13**

1. Suppose each unit of an electrical instrument is manufactured with a small random bias. Is the noise of the instrumentation ergodic? If we measure the noise of one instrument then we measure its bias, which is equal to its mean. However, if we measure the noise of another instrument it might have a different mean because it has a different bias. In other words, we cannot obtain the mean of the stochastic process by simply investigating one instrument (i.e., one realization of the stochastic process). Therefore, the stochastic process is not ergodic.

2. Suppose each unit of an electrical instrument is manufactured identically, each with zero-mean stationary Gaussian noise. Is the noise ergodic? In this case we could measure the mean of the process by measuring the noise of many separate instruments at one instant of time, or by measuring the noise of one instrument over an extended period of time. Either experiment would correctly inform us that the mean of the stochastic process is zero. We could find the statistics of the stochastic process using all the instruments at a single time, or using a single instrument at many different times. Therefore, the stochastic process is ergodic.

vvv The definitions of correlation and covariance can be extended to two stochastic *processes X ( t )  and Y(t). The cross correlation of X ( t )  and Y(t) is defined as*

*RXY(t1, t 2 )  = E[X(tl)YT(t2)1* (2.90)

*Two random processes X ( t )  and Y(t) are said to be uncorrelated if Rxy(t1, t 2 )  =* *E[X(t1)]E[YT(t2)]* *for all tl and t z .  The cross covariance of X ( t )  and Y(t) is* defined as (2.91) *Cxy(t1, t2) = E { [ X ( t i )  - x(ti>I[Y(t~)* *- F(tz)lT}*

**2.6** 
## WHITE NOISE AND COLORED NOISE


*If the RV X(t1) is independent from the RV X ( t z )  for all tl # t z  then X ( t )  is called* *white noise. Otherwise, X ( t )  is called colored noise.* The whiteness or color content of a stochastic process can be characterized by its *power spectrum. The power spectrum Sx(w) of a widesense stationary stochas-* **tic process X ( t )  is defined as the Fourier transform of the autocorrelation. The** autocorrelation is the inverse Fourier transform of the power spectrum.

*00* *S X ( W )  = [ 0 0* *Rx(r)e-'"'dT*

*Rx(r) = '/* *Sx(w)@""dw* (2.92)

These equations are called the Wiener-Khintchine relations after Norbert Wiener and Aleksandr Khinchin. Note that some authors put the term 1/2n on the right *side of the Sx(w) definition, in which case the 1127~ term on the right side of the*

**W**

2n *-00*

---


[Image on page 24]


**72**

**RX(T) definition disappears. The power spectrum is sometimes referred to as the** power density spectrum, the power spectral density, or the power density. The **power of a wide-sense stationary stochastic process is defined as**

**(2.93)**

*The cross power spectrum of two wide-sense stationary stochastic processes X ( t )* *and Y(t) is the Fourier transform of the cross correlation:*


$$
~ x y ( w )  = S_, Rxy(r)e-jwrdr
$$
 M

**(2.94)**

Similar definitions hold for discrete-time random processes. The power spectrum **of a discretetime random process is defined as**

**l** **W** 
# RXY (7) = 2;; 1, SXU
 (w)e'"'

**w E [-n,7r]**

**(2.95)**

**A discretetime stochastic process X ( t )  is called white noise if**


# Rx(k) = { u2 i f k = O
 0 ifk#O = U26k **(2.96)**

where 6k is the Kronecker delta function, defined as 1 i f k = O 
# 6 k  = { 0 i f k # O
 **(2.97)**

The definition of discrete-time white noise shows that it does not have any corre- lation with itself except at the present time. If X(k) is a discretetime white noise **process, then the RV X ( n )  is uncorrelated with X(m)** *unless n = m. This shows* that the power of a discrete-time white noise process is equal at all frequencies: Sx(w) = Rx(0) **for all w E [-n,** n] **(2.98)**

For a continuous-time random process, white noise is defined similarly. White noise has equal power at all frequencies (like white light):

SX(W) = Rx(0) for all w **(2.99)**

**Substituting this expression for Sx(w) into Equation (2.92), we see that for continuous-** time white noise

*where 6(r) is the continuous-time impulse function. That is, 6 ( ~ )  is a function* *that is zero everywhere except at r = 0; it has a width of 0, a height of CCJ, and* an area of 1. Continuous-time white noise is not something that occurs in the **real world because it has infinite power, as seen by comparing Equations (2.93)** **and (2.99). Nevertheless, many continuous-time processes approximate white noise** and are useful in mathematical analyses of signals and systems.

Rx(7) = Rx(0)6(7) **(2.100)**

---


[Image on page 25]


**73**

**EXAMPLE 2.14**

Suppose that a zero-mean stationary stochastic process has the autocorrela- tion function *R ~ ( T )* 
## = u 2 e -PI71
 **(2.101)**

where ,B is a positive real number. The power spectrum is computed from 
## Equation (2.92) as


oil **02e-PITI e - j W 7  d7**

**J-w** **J o**

**U 2** **IS2** +- **p - j w** **P + j w**


# W2 + p 2


- -

- **2 2 p** - -

The variance of the stochastic process is computed as

**1** oil 
## 2u2p dw
 
# E [ X 2 ( t ) ]  = - J -
 **27r** **-oilw2+p2**

**(2.102)**

**(2.103)**

vvv

**2.7** **SIMULATING CORRELATED NOISE**

In optimal filtering research and experiments, we often have to simulate correlated white noise. That is, we need to create random vectors whose elements are cor- related with each other according to some predefined covariance matrix. In this section, we will present one way of accomplishing this. Suppose we want to generate an n-element random vector w that has zero mean and covariance Q:

Q = [  ! **i 2 ]** **(2.104)**

Since Q is a covariance matrix, we know that all of its eigenvalues are real and 
## nonnegative. We can therefore denote its eigenvalues as p::


*U l n* (y! ...

*U l n* **un**


## X(Q) = p i
 
## (k = 1 , .  . . , n)
 **(2.105)**

*Suppose the eigenvectors of Q are found to be d l ,  ., dn. Augment the d, vectors* together to obtain an n x n matrix D. Since Q is symmetric, we can always choose

---


[Image on page 26]


**74**

*the eigenvectors such that D is orthogonal, that is, D-l = DT. We therefore obtain* **the Jordan form decomposition of Q as**

*Q = DQDT* (2.106)

*where Q is the diagonal matrix of the eigenvalues of Q. That is,*


## Q = diag(p.:, a
 *** 7 P:)** (2.107)


## Now we define the random vector v as v = D-lw, so that w = Dv. Therefore,
 *qVVT)* *= E ( D ~ W U I ~ D )* *= D ~ Q D* = Q 
# = diag(p:, . -, p:)
 (2.108)

This shows how we can generate an n-element random vector w with a covariance *matrix of Q. The algorithm is given as follows.*

**Correlated noise simulation** 
## 1. Find the eigenvalues of Q, and denote them as p:, - - ., p, 2


## 2. Find the eigenvectors of Q, and denote them as d l ,  - ., d,, such that


*D = [ d l* ***** ***** **a** *d, ]* *D-l* *= DT* (2.109)


# 3. For i = 1,. -, n compute the random variable vi = pir2, where each rZ is an
 independent random number with a variance of 1 (unity variance).


## 4. Set w = Dv.


**2.8** 
## SUMMARY


In this chapter, we have reviewed the basic concepts of probability, random vari- ables, and stochastic processes. The probability of some event occurring is simply **and intuitively defined as the number of times the event occurs divided by the num-** **ber of chances the event has to occur. A random variable (RV) is a variable whose** value is not certain, but is governed by the laws of probability. For example, your score on the test for this chapter is not deterministic, but is a random variable. *Your actual score, after you take the test, will be a specific, deterministic number.* **But before you take the test, you do not know what you will get on the test. You** may suppose that you will probably get between 80% and 90% if you have a decent understanding of the material, but your actual score will be determined by random **events such as your health, how well you sleep the night before, what topics the** instructor decides to cover on the test versus what topics you study, what the traf- fic was like on the way to school, the mood of the instructor when she grades the **test, and so on. A stochastic process is a random variable that changes with time,**

---


[Image on page 27]


**75**

such as your performance on all of the quizzes and homework assignments for this course. The expected value of your test grades may be constant throughout the duration of the course if you are a consistent person, or it may increase if you tend to study harder as the course progresses, or it may decrease if you tend to study less as the course progresses. Probability, random variables, stochastic processes, and related topics form a huge area of study that we have only touched on in this chapter. Additional information on these topics can be found in many textbooks, **including [Pap02, PeeOl]. A study of these topics will allow a student to delve into** many practical engineering subjects, including control and estimation theory, signal processing, and communications theory.

**PROBLEMS**

**Written exercises**

**2.1** RV?

**2.2** each. Find the probability that each pile contains exactly one ace [GreOl].

**2.3**

What is the 0th moment of an RV? What is the 0th central moment of an

Suppose a deck of 52 cards is randomly divided into four piles of 13 cards

*Determine the value of a in the function*

*ax(1- x) x E [O, 11* otherwise

**so that fx (x) is a valid probability density function [Lie67].**

**2.4** *Determine the value of a in the function*

**so that fx (x) is a valid probability density function. What is the probability that**

**2.5** The probability density function of an exponentially distributed random vari- able is defined as follows.

*1x1 5 l?*

*where a 2 0.* **a) Find the probability distribution function of an exponentially distributed** random variable. **b) Find the mean of an exponentially distributed random variable.** 
## c) Find the second moment of an exponentially distributed random variable.
 **d) Find the variance of an exponentially distributed random variable.** **e) What is the probability that an exponentially distributed random variable** takes on a value within one standard deviation of its mean?

---


[Image on page 28]


**76**

**2.6** first, second, and third moments.

**2.7**

Derive an expression for the skew of a random variable as a function of its

Consider the following probability density function:

*b > O* *ab* 
# b2 + x2 ’
 
# fx(2) = -


## a) Determine the value of a in the so that fx(2) is a valid probability density
 **function. (The correct value of a makes fx(2) a Cauchy pdf.)** **b) Find the mean of a Cauchy random variable.**

**2.8 Consider two zero-mean uncorrelated random variables W and V with stan-** 
## dard deviations gw and uv, respectively. What is the standard deviation of the
 *random variable X = W + V?*

**2.9 Consider two scalar RVs X and Y .** **a) Prove that if X and Y are independent, then their correlation coefficient** 
## p = 0.
 **b) Find an example of two RVs that are not independent but that have a** correlation coefficient of zero. 
## c )  Prove that if Y is a linear function of X then p = fl.


**2.10 Consider the following function [Lie67].**

**ae-2xe-3Y** x > 0, y > o otherwise


## a) Find the value of a so that fxy(2, y) is a valid joint probability density
 function. **b) Calculate** **and g.** **c )  Calculate E ( X 2 ) ,  E(Y2), and E ( X Y ) .** 
## d) Calculate the autocorrelation matrix of the random vector [ X
 
## e) Calculate the variance 09, the variance ci, and the covariance C x y .


## f) Calculate the autocovariance matrix of the random vector [ X


## g) Calculate the correlation coefficient between X and Y.


**T** *Y ] .*

*Y ] .* **T**

**2.11** **k are positive constants.** 
## A stochastic process has the autocorrelation Rx(T) = Ae-klT1, where A and


**a) What is the power spectrum of the stochastic process?** **b) What is the total power of the stochastic process?** 
## c )  What value of k results in half of the total power residing in frequencies
 less than 1 Hz?

*Suppose X is a random variable, and Y (t) = X cost is a stochastic process.* **2.12** **a) Find the expected value of Y(t).** **b) Find A[Y(t)],** *the time average of Y(t).* 
## c )  Under what condition is y(t) = A[Y(t)]?


**2.13** **Figure 2.5.** 
## a) Plot the pdf of (ZlX) as a function of X for 2 = 0.5.


*Consider the equation 2 = X + V .  The pdf’s of X and B are given in*

---


[Image on page 29]


**77**


## b) Given Z = 0.5, what is conditional expectation of X? What is the most
 **probable value of X? What is the median value of X?**

**-1.5** **-1** **-05** **0** **0.5** 1 **1.5** **X**

0.5

-1.5 -1 **-05** **0** **0.5** **1** **1.5**


## Figure 2.5
 **pdf’s for Problem 2.13 [Sch73].**

**2.14** The temperature at noon in London is a stochastic process. Is it ergodic?

**Computer exercises**

**2.15** *Generate N = 50 independent random numbers, each uniformly distributed* between 0 and 1. Plot a histogram of the random numbers using 10 bins. What is the sample mean and standard deviation of the numbers that you generated? What would you expect to see for the mean and standard deviation (i.e., what are 
## the theoretical mean and standard deviation)? Repeat for N = 500 and N = 5,000
 **random numbers. What changes in the histogram do you see as N increases?**

**2.16** 
## Generate 10,000 samples of (z1+ 22)/2, where each 2% is a random number
 uniformly distributed on [-1/2, +1/2]. Plot the 50-bin histogram. Repeat for


# ( X I +  xz + 23 + 24)/4. Describe the difference between the two histograms.
