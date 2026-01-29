---
type: chapter
chapter: 2
title: Probability theory
---
# Chapter 2 Probability Theory

The most we can know is in terms of probabilities. 

--Richard Feynman [Fey63, p. 6-11] 
While writing my book *[Stochastic Processes,* first published in 19531 I had an argument with Feller. He asserted that everyone said "random variable" and I asserted that everyone said "chance variable." We obviously had to use the same name in our books, so we decided the issue by a stochastic procedure. That is, we tossed for it and he won. 

-Joseph Doob [Sne97, p. 3071 Probabilities do not exist. 

-Bruno de Finetti [deF74] 
In our &tempt to filter a signal, we will be trying to extract meaningful information from a noisy signal. In order to accomplish this, we need to know something about what noise is, some of its characteristics, and how it works. This chapter reviews probability theory. We begin by discussing the basic concept of probability in Section 2.1, and then move on to random variables (RVs) in Section **2.2.** The chapter then continues with the following topics: 
0 An RV is a general case of the normal scalars that we are familiar with, and so just as we can apply a functional mapping to a number, we can also apply Optimal State Estimation, First Edition. By **Dan** J. Simon ISBN **0471708585** 02006 John Wiley & Sons, Inc. 

49 a 

Just as we can have vectors of numbers, we can also have vectors of RVs, and so we discuss groups of random variables and random vectors in Section 2.4. 

a a functional mapping to an RV. We discuss functions (transformations) of random variables in Section 2.3. 

a Just as we can have scalar functions of time, we can also have RVs that are functions of time, and so we discuss RVs that change with time (stochastic processes) in Section 2.5. Stochastic processes can be divided into two categories: white noise and colored noise, and we discuss these concepts in Section 2.6. 
We conclude in Section 2.7 with a high-level discussion of how to write a computer simulation of a noise process. 

This chapter is only a brief introduction and review of probability and stochastic processes, and more detail can be found in many other books on the subject, such as [Pap02, PeeOl]. 

## 2.1 **Probability**

How shall we define the concept of probability? Suppose we run an experiment a certain number of times. Sometimes event A occurs and sometimes it does not. For instance, our experiment may be rolling a six-sided die. Event A may be defined as the number 4 showing up on the top surface of the die after we roll the die. Common sense tells us that the probability of event A occuring is 1/6. Likewise, we would expect that if we run our experiment many times, then we would see the number 1 appearing about 1/6 of the time. This intuitive explanation forms the basis for our formal description of the concept of probability. We define the probability of event A as 

$$(2.1)$$

$$P(A)={\frac{\mathrm{Number~of~times~}A{\mathrm{~occurs}}}{\mathrm{Total~number~of~outcomes}}}$$

This commonsense understanding of probability is called the relative frequency definition. A more formal and mathematically rigorous definition of probability can be obtained using set theory [Bi195, Nel871, which was pioneered by Andrey Kolomogorov in the 1930s. But for our purposes, the relative frequency definition is adequate. 

In general, we know that there are n-choose-k different ways of selecting Ic objects from a total of n objects (assuming that the order of the objects does not matter), 
where n-choose-k is denoted and defined as 

$$\left(\begin{array}{c}n\\ k\end{array}\right)=\frac{n!}{(n-k)!k!}\tag{2.2}$$

For instance, suppose we have a penny (P), nickel (N), dime (D), and quarter (Q). 

How many distinct subsets of three coins can we pick from that set? We can pick PND, PNQ, PDQ, or NDQ, for a total of four possible subsets. This is equal to 4choose-3. 

What is the probability of being dealt four of a kind' in poker? The total number of possible poker hands can be computed as the total number of subsets of size five that can be picked from a deck of 52 cards. The total number of possible hands is 52-choose5 = **2,598,960.** Out of all those hands, there are 48 possible hands containing four aces, 48 possible hands containing four kings, and so on. So there are a total of 13 x 48 hands containing four of a kind. Therefore the probability of being dealt four of a kind is 

$$\frac{(13)(48)}{2,598,960}$$ $$1/4165$$ $$0.024\%$$
$$\begin{array}{r l}{P(A)}&{{}=}\\ {}&{{}=}\\ {}&{{}\approx}\end{array}$$
$$(2.3)$$

$$={\frac{P(A,B)}{P(B)}}$$
$$P(A|B)=$$
$$(2.4)$$

vvv The conditional probability of event A given event B can be defined if the probability of B is nonzero. The conditional probability of A given B is defined as P(A1B) is the conditional probability of A given B, that is, the probability that A occurs given the fact that B occurred. *P(A,B)* is the joint probability of A and B, that is, the probability that events A and B both occur. The probability of a single event [for instance, P(A) or *P(B)]* is called an a *priori* probability because it applies to the probability of an event apart from any previously known information. A conditional probability [for instance, *P(AIB)]* is called an a *posteriori* probability because it applies to a probability given the fact that some information about a possibly related event is already known. 

For example, suppose that A is the appearance of a 4 on a die, and B is the appearance of an even number on a die. *P(A)* = **1/6.** But if we know that the die has an even number on it, then *P(A)* = **1/3** (since the even number could be either a 2, 4, or **6).** This example is intuitive, but we can also obtain the answer using Equation (2.4). *P(A,* B) is the probability that both A occurs (we roll a 4) and B 
occurs (we roll an even number), so *P(A,* B) = **1/6.** So Equation **(2.4)** gives 

$$\begin{array}{r l}{={}}&{{}{\frac{1/6}{1/2}}}\\ {={}}&{{}1/3}\end{array}$$
$$P(A|B)$$

The a *priori* probability of A is **1/6.** But the a *posteriori* probability of A given B 
is **1/3.** 

$$(2.5)$$

Cnsider the eight shapes in Figure **2.1.** We have three circles and five squares, so P(circ1e) = **3/8.** Only one of the shapes is a gray circle, so P(gray, circle) 

'Once I was dealt four sevens while playing poker with some friends (unfortunately, I was not playing for money at the time). I don't expect to see it again in my lifetime. 
= 1/8. Of the three circles, only one is gray, so P(gray I circle) = 1/3. This last probability can be computed using Equation (2.4) as 

$$\frac{P(\mathrm{gray},\mathrm{circle})}{P(\mathrm{circle})}$$ $$\frac{1/8}{3/8}$$ $$1/3$$
$$\begin{array}{r l}{P(\mathrm{gray}|\mathrm{circle})}&{{}=}\\ {}&{}&{}\\ {}&{}&{=}\\ {}&{}&{}\\ {}&{}&{}\\ {}&{}&{}\end{array}$$

![3_image_0.png](3_image_0.png)

$$(2.6)$$
P( circle) P(graylcirc1e) = 
Figure **2.1** Some shapes for illustrating probability and Bayes' Rule. 
vvv Note that we can use Equation (2.4) to write P(BIA) = *P(A,B)/P(A).* We can solve both this equation and Equation (2.4) for *P(A,B)* and equate the two expressions for *P(A,* B) to obtain Bayes' Rule. 

P(AIB)P(B) = *P(BIA)P(A)* (2.7) 
Bayes' Rule is often written by rearranging the above equation to obtain As an example, consider Figure 2.1. The probability of picking a gray shape given the fact that the shape is a circle can be computed from Bayes' Rule as 

$$P(A|B)P(B)=P(B|A)P(A)$$
$$(2.7)$$
$$P(A|B)={\frac{P(B|A)P(A)}{P(B)}}$$
$$(2.8)$$

$$\frac{P(\mathrm{circle}|\mathrm{gray})P(\mathrm{gray})}{P(\mathrm{circle})}$$ $$\frac{(1/5)(5/8)}{3/8}$$ $$1/3$$
$$\begin{array}{r l}{P(\mathrm{gray}|\mathrm{circle})}&{{}=}\\ {}&{}&{}\\ {}&{}&{=}\\ {}&{}&{}\\ {}&{}&{}=\end{array}$$
P(circ1e) P(graylcirc1e) = 
We say that two events are independent if the occurrence of one event has no effect on the probability of the occurrence of the other event. For example, if A is the appearance of a 4 after rolling a die, and B is the appearance of a 3 after rolling another die, then A and B are independent. Mathematically, independence of A 
and B can be expressed several different ways. For example, we can write 

$$(2.9)$$

$$\begin{array}{r l}{={}}&{{}P(A)P(B)}\\ {={}}&{{}P(A)}\\ {={}}&{{}P(B)}\end{array}$$
$$\begin{array}{r c l}{{P(A,B)}}&{{;}}\\ {{}}&{{}}\\ {{P(A|B)}}&{{;}}\\ {{}}&{{}}\\ {{P(B|A)}}&{{;}}\end{array}$$
$$(2.10)$$
P(A,B) = P(A)P(B) 
P(AIB) = P(A) 
P(B1A) = *P(B)* (2.10) 
if A and B are independent. As an example, recall from Equation (2.5) that if A is the appearance of a 4 on a die, and B is the appearance of an even number on a die, then *P(A)* = 1/6 and *P(A1B)* = 1/3. Since P(A1B) \# P(A) we *see* that A 
and B are dependent events. 

## 2.2 Random Variables

We define a random variable (RV) as a functional mapping from a set of experimental outcomes (the domain) to a set of real numbers (the range). *For* example, the roll of a die can be viewed as a RV if we map the appearance of one dot on the die to the output one, the appearance of two dots on the die to the output two, and so on. 

Of course, *after* we throw the die, the value of the die is no longer a random variable - it becomes certain. The outcome of a particular experiment is not an RV. If we define X as an RV that represents the roll of a die, then the probability that X will be a four is equal to 1/6. If we then roll a four, the four is a realization of the RV X. If we then roll the die again and get a three, the three is another realization of the RV X. However, the RV X exists independently of any of its realizations. This distinction between an RV and its realizations is important for understanding the concept of probability. Realizations of an RV are not equal to the RV itself. When we say that the probability of X = 4 is equal to 1/6, that means that there is a 1 out of 6 chance that each realization of X will be equal to 4. However, the RV X will always be random and will never be equal to a specific value. 

An RV can be either continuous or discrete. The throw of a die is a discrete random variable because its realizations belong to a discrete set of values. The high temperature tomorrow is a continuous random variable because its realizations belong to a continuous set of values. 

The most fundamental property of an RV X is its probability distribution function **(PDF)** *Fx(x),* defined as 

$F_{X}(x)=P(X\leq x)$ (2.11)
$$F_{X}(x)\in[0,1]$$ $$F_{X}(-\infty)=0$$ $$F_{X}(\infty)=1$$ $$F_{X}(a)\leq F_{X}(b)\quad\mbox{if}a\leq b$$ $$P(a<X\leq b)=F_{X}(b)-F_{X}(a)\tag{2.12}$$
In the above equation, *Fx(x)* is the *PDF* of the RV X, and z is a nonrandom independent variable or constant. Some properties of the *PDF* that can be obtained from its definition are 

$$f_{X}(x)={\frac{d F_{X}(x)}{d x}}$$

The probability density function (pdf) *fx(x)* is defined as the derivative of the PDF. 

$$(2.13)$$

Some properties of the pdf that can be obtained from this definition are 

$$\begin{array}{r c l}{F_{X}(x)}&{=}&{\int_{-\infty}^{x}f_{X}(z)\,d z}\\ {}&{}&{}&{f_{X}(x)}&{\geq}&{0}\\ {\int_{-\infty}^{\infty}f_{X}(x)\,d x}&{=}&{1}\\ {}&{}&{}&{}\\ {P(a<x\leq b)}&{=}&{\int_{a}^{b}f_{X}(x)\,d x}\end{array}$$
$$\begin{array}{l}{{1-F x(x)}}\\ {{P(X>x)}}\end{array}$$
$$\begin{array}{r l}{Q(x)}&{{}=}\\ {}&{{}=}\end{array}$$
$$(2.14)$$

The Q-function of an RV is defined as one minus the PDF. This is equal to the probability that the RV is greater than the argument of the function: 

$$(2.15)$$

Just as we spoke about conditional probabilities in Equation (2.4), we can also speak about the conditional PDF and the conditional pdf. The conditional distribution and density of the RV X given the fact that event A occurred are defined as 

$$\begin{array}{r l}{F_{X}(x|A)}&{{}=}\\ {}&{{}=}\\ {}&{{}}\\ {f_{X}(x|A)}&{{}=}\end{array}$$
$$\begin{array}{c}{{P(X\leq x|A)}}\\ {{\underline{{{P(X\leq x,A)}}}}}\\ {{\overline{{{P(A)}}}}}\\ {{\underline{{{d F_{X}(x|A)}}}}}\\ {{\overline{{{d x}}}}}\end{array}$$
Fx(2lA) = **P(X5zlA)** 
$$(2.16)$$
$$\begin{array}{r c l}{{f_{X_{1}|X_{2}}(x_{1}|x_{2})}}&{{=}}&{{P[(X_{1}\leq x_{1})|(X_{2}=x_{2})]}}\\ {{}}&{{=}}&{{\frac{f_{X_{1},X_{2}}(x_{1},x_{2})}{f_{X_{2}}(x_{2})}}}\end{array}$$

Bayes' Rule, discussed in Section 2.1, can be generalized to conditional densities. 

Suppose we have random variables XI and **X2.** The conditional pdf of the RV X1 given the fact that RV X2 is equal to the realization 22 is defined as 

$$(2.17)$$
$$\begin{array}{r l}{f[x_{1}|(x_{2},x_{3},x_{4})]f[(x_{2},x_{3})|x_{4}]}&{{}=1}\\ {}&{{}}\\ {=}&{{}}\\ {}&{{}}\\ {=}&{{}}\end{array}$$

Although this is not entirely intuitive, it can be derived without too much difficulty [PapOS, PeeOl]. Now consider the following product of two conditional pdf's: 

$$\begin{array}{l}{{\frac{f(x_{1},x_{2},x_{3},x_{4})}{f(x_{2},x_{3},x_{4})}\frac{f(x_{2},x_{3},x_{4})}{f(x_{4})}}}\\ {{\frac{f(x_{1},x_{2},x_{3},x_{4})}{f(x_{4})}}}\\ {{f[(x_{1},x_{2},x_{3})|x_{4}]}}\end{array}\tag{2.18}$$

Note that in the above equation we have dropped the subscripts on the *f(.)* functions for ease of notation. This is commonly done if the random variable associated with the pdf is clear from the context. This is called the Chapman-Kolmogorov equation [Pap02]. It can be extended to any number of RVs and is fundamental to the Bayesian approach to state estimation (Chapter 15). 

The expected value of an RV X is defined as its average value over a large number of experiments. This can also be called the expectation, the mean, or the average of the RV. Suppose we run the experiment N times and observe a total of m different outcomes. We observe that outcome A1 occurs n1 times, A2 occurs n2 times, . . ., 
and *A,,,* occurs n, times. Then the expected value of X is computed as 

$$E(X)={\frac{1}{N}}\sum_{i=1}^{m}A_{i}n_{i}$$
$$(2.19)$$

E(X) is also often written as *E(x), X,* or 2. 

At this point, we will begin to use lowercase x instead of uppercase X when the meaning is clear. We have been using uppercase X to refer to an RV, and lowercase x to refer to a realization of the RV, which is a constant or independent variable. 

However, it should be clear that, for example, *E(x)* is the expected value of the RV 
X, and so we will interchange x and X in order to simplify notation. 

As an example of the expected value of an RV, suppose that we roll a die an infinite number of times. We would expect to see each possible number (one through six) 1/6 of the time each. We can compute the expected value of the roll of the die as 

$$\begin{array}{r l}{E(X)}&{{}={\mathrm{~}}\operatorname*{lim}_{N\to\infty}{\frac{1}{N}}\left[(1)(N/6)+\cdots+(6)(N/6)\right]}\\ {}&{{}=\mathrm{~}3.5}\end{array}$$

Note that the expected value of an RV is not necessarily what we would expect to see when we run a particular experiment. For example, even though the above expected value of X is 3.5, we will never see a 3.5 when we roll a die. 

We can also talk about a function of an RV, just as we can talk about a function of any scalar. (We will discuss this in more detail in Section 2.3.) If a function, say *g(X),* acts upon an RV, then the output of the function is also an RV. For example, if X is the roll of a die, then *P(X* = 4) = 1/6. If g(X) = *X2,* then P[g(X) = 161 = 1/6. We can compute the expected value of any function *g(X)* as 

$$(2.20)$$
$$E[g(X)]=\int_{-\infty}^{\infty}g(x)f_{X}(x)\,d x$$
$$\begin{array}{r c l}{{\sigma_{X}^{2}}}&{{=}}&{{E[(X-{\bar{x}})^{2}]}}\\ {{}}&{{=}}&{{\int_{-\infty}^{\infty}(x-{\bar{x}})^{2}f_{X}(x)\,d x}}\end{array}$$
$$(2.21)$$

where *fx(x)* is the pdf of X. If *g(X)* = X, then we can compute the expected 
value of X as 
$E(X)=\int_{-\infty}^{\infty}xf_{X}(x)\,dx$ (2.22)
The variance of an RV is a measure of how much we expect the RV to vary from 
its mean. The variance is a measure of how much variability there is in an RV. In the extreme case, if the RV X always is equal to one value (for example, the die 
is loaded and we always get a 4 when we roll the die), then the variance of X is 
equal to 0. On the other extreme, if X can take on any value between *ztco* with equal probability, then the variance of X is equal to 00. The variance of an RV is 
formally defined as 
$$(2.23)$$
The standard deviation of an RV is 0, which is the square root of the variance. 

Sometimes we denote the standard deviation as ox if we need to be explicit about the RV whose standard deviation we are discussing. Note that the variance can be written as 

$$\begin{array}{r c l}{{\sigma^{2}}}&{{=}}&{{E[X^{2}-2X\bar{x}+\bar{x}^{2}]}}\\ {{}}&{{=}}&{{E(X^{2})-2\bar{x}^{2}+\bar{x}^{2}}}\\ {{}}&{{=}}&{{E(X^{2})-\bar{x}^{2}}}\end{array}$$
$$(2.24)$$
We use the notation 
$$X\sim({\bar{x}},\sigma^{2})$$
$$(2.25)$$
$$(2.26)$$
$$(2.27)$$
$$(2.28)$$

to indicate that X is an RV with a mean of 5 and a variance of **g2.** 
Skew is defined as The skew of an RV is a measure of the asymmetry of the pdf around its mean. 

$${\mathrm{skew}}=E[(X-{\bar{x}})^{3}]$$
skew = E[(X - *Z)3] (2.26)* 
The skewness, also called the coefficient of skewness, is the skew normalized by the cube of the standard deviation: 

$${\mathrm{skewness}}={\mathrm{skew}}/\sigma^{3}$$

skewness = skew/g3 *(2.27)* 
In general, the ith moment of a random variable X is the expected value of the ith power of X. The ith central moment of a random variable X is the expected value of the ith power of X minus its mean: 

$$\begin{array}{r c l}{{i\mathrm{th~moment~of~}X}}&{{=}}&{{E(X^{\natural})}}\\ {{i\mathrm{th~central~moment~of~}X}}&{{=}}&{{E[(X-{\bar{x}})^{\natural}]}}\end{array}$$

For example, the first moment of a random variable is equal to its mean. The first central moment of a random variable is always equal to 0. The second central moment of a random variable is equal to its variance. 

An RV is called uniform if its pdf is a constant value between two limits. This indicates that the RV **has** an equally likely probability of obtaining any value between its limits, but a zero probability of obtaining a value outside of its limits: 

$$f_{X}(x)={\left\{\begin{array}{l l}{{\frac{1}{b-a}}}&{x\in[a,b]}\\ {0}&{{\mathrm{otherwise}}}\end{array}\right.}$$
$$(2.29)$$

Figure **2.2** shows the pdf of an RV that is uniformly distributed between fl. Note that the area of this curve is one **(as** is the area of all pdf's). 

In this example we will find the mean and variance of an RV that is uniformly distributed between 1 and 3. The pdf of the RV is given as 

$$f_{X}(x)={\left\{\begin{array}{l l}{1/2}&{x\in[1,3]}\\ {0}&{{\mathrm{otherwise}}}\end{array}\right.}$$
$$(2.30)$$

![8_image_0.png](8_image_0.png)

Figure **2.2** Probability density function of an RV uniformly distributed between fl. 
The mean is computed as follows: 6 

a follows: $\qquad\quad\kappa$  $\begin{array}{rcl}\bar{x}&=&\int_{-\infty}^{\infty}x f_X(x)\,dx\\ &=&\int_1^3\dfrac{1}{2}x\,dx\\ &=&2\end{array}$

$$(2.31)$$
The variance is computed as follows: 

$$\sigma_{X}^{2}=\int_{-\infty}^{\infty}{\frac{1}{2}}(x-{\bar{x}})^{2}f(x)\,d x$$ $$=\int_{1}^{3}{\frac{1}{2}}(x-2)^{2}\,d x$$ $$={\frac{1}{3}}$$
$$(2.32)$$

vvv An RV is called Gaussian or normal if its pdf is given by 

$$f_{X}(x)={\frac{1}{\sigma{\sqrt{2\pi}}}}\exp\left[{\frac{-(x-{\bar{x}})^{2}}{2\sigma^{2}}}\right]$$
$$X\sim N({\bar{x}},\sigma^{2})$$
fX(2) = - 
$$(2.33)$$
$$(2.34)$$

This is called the Laplace distribution in France, but it had many other discoverers, including Robert Adrain. Note that Z and 0 in the above pdf are the mean and standard deviation of the Gaussian RV. We use the notation x N *N(5,02)* **(2.34)** 
to indicate that X is a Gaussian RV with a mean of Z and a variance of **02.** 
Figure **2.3** shows the pdf of a Gaussian RV with a mean of zero and a variance 

$$F_{X}(x)={\frac{1}{\sigma{\sqrt{2\pi}}}}\int_{-\infty}^{x}\exp[-(z-{\bar{x}})^{2}/2\sigma^{2}]\,d z$$

of one. If the mean changes, the pdf will shift to the left or right. If the variance increases, the pdf will spread out. If the variance decreases, the pdf will be squeezed in. The PDF of a Gaussian RV is given by 

$$(2.35)$$
$$F_{X0}(x)={\frac{1}{\sqrt{2\pi}}}\int_{-\infty}^{x}\exp(-z^{2}/2)\,d z$$

This integral does not have a closed-form solution, and so it must be evaluated numerically. However, its evaluation can be simplified by considering the normalized Gaussian PDF of an RV with zero mean and unity variance: 

$$(2.36)$$

It can be shown that any Gaussian PDF can be expressed in terms of this normalized PDF as 

$$(2.37)$$

In addition, a Gaussian PDF can be approximated as the following closed-form expression [Bor79]: 

$$F_{X}(x)=F_{X^{0}}\left({\frac{x-{\bar{x}}}{\sigma}}\right)$$
$$1-\left[{\frac{1}{(1-a)x+a{\sqrt{x^{2}+b}}}}\right]{\frac{\exp(-x^{2}/2)}{{\sqrt{2\pi}}}}\quad\ x\geq0$$ $$0.339$$ $$5.510$$
$$\begin{array}{r l}{F_{X}(x)}&{{}\approx}\\ {\ }&{{}}\\ {a}&{{}=}\\ {b}&{{}=}\end{array}$$
a = 0.339 
b = **5.510** 
$$(2.38)$$

![9_image_0.png](9_image_0.png)

Figure 2.3 variance of one. 

Probability density function of a Gaussian RV with a mean of zero and a 
Suppose we have a random variable X with a mean of zero and a symmetric pdf [i.e., fx(x) = fx(-x)]. This is the case, for example, for the pdf's shown in 

$$m_{\mathrm{t}}$$

Figures 2.2 and 2.3. In this case, the ith moment of X can be written as If i is odd then xz = -(-z)~. Combined with the fact that fx(x) = *fx(-z),* we see that 

$$\int_{-\infty}^{0}x^{i}f_{X}(x)\,dx=\int_{0}^{\infty}(-x)^{i}f_{X}(-x)\,dx\tag{2.40}$$ $$=-\int_{0}^{\infty}x^{i}f_{X}(x)\,dx$$

So for odd i, the ith moment in Equation (2.39) is zero. We see that all of the odd moments of a zero-mean random variable with a symmetric pdf are equal to 0. 

## 2.3 Transformations Of Random Variables

In this section, we will look at what happens to the pdf of an RV when we pass the RV through some function. Suppose that we have two RVs, X and Y, related to one another by the monotonic2 functions *g(.)* and h(.): 

$$\begin{array}{l c l}{{Y}}&{{=}}&{{g(X)}}\\ {{X}}&{{=}}&{{g^{-1}(Y)=h(Y)}}\end{array}\qquad\qquad(2.41)$$

If we know the pdf of X *[fx(x)],* then we can compute the pdf of Y *[fy(y)]* as follows: 

$$P(X\in[x,x+dx])=P(Y\in[y,y+dy])\quad\ (dx>0)$$ $$\int_{x}^{x+dx}f_{X}(z)dz=\left\{\begin{array}{ll}\int_{y+dy}^{y+dy}f_{Y}(z)dz&\mbox{if$dy>0$}\\ -\int_{y}^{y+dy}f_{Y}(z)dz&\mbox{if$dy<0$}\end{array}\right.$$ $$f_{X}(x)dx=f_{Y}(y)|dy|$$ $$f_{Y}(y)=\left|\frac{dx}{dy}\right|f_{X}[h(y)]\tag{2.42}$$ $$=|h^{\prime}(y)|f_{X}[h(y)]$$

where we have used the assumption of small dx and dy in the above calculation. 

'A monotonic function is a function whose slope is either always nonnegativeor always nonpositive. 

If the slope is always nonnegative, then the function is monotonically nondecreasing. If the slope is always positive, then the function is monotonically increasing. If the slope is always nonpositive, then the function is monotonically nonincreasing. If the slope is always negative, then the function is monotonically decreasing. 
In this example, we will find the pdf of a linear function of a Gaussian **RV.** 
Suppose that X N N(3, *u;)* and Y = *g(X)* = aX + b, where a # 0 and b are 
any real constants. Then 
x = *h(Y)* 
$h(Y)$  $(Y-b)/a$  $1/a$  $|h'(y)|f_{X}[h(y)]$  $\left|\dfrac{1}{a}\right|\dfrac{1}{\sigma_{X}\sqrt{2\pi}}\exp\left\{\dfrac{-[(y-b)/a-\bar{x}]^{2}}{2\sigma_{X}^{2}}\right\}$  $\dfrac{1}{a\sigma_{X}\sqrt{2\pi}}\exp\left\{\dfrac{-[y-(a\bar{x}+b)]^{2}}{2a^{2}\sigma_{X}^{2}}\right\}$               (2.43)  $\tau$ is Gaussian with a mean and variance given by 
fY(Y) = Ih'(Y)IfX[h(Y)l 
$$\begin{array}{r c l}{X}&{=}&{h}\\ {}&{=}&{(}\\ {h^{\prime}(y)}&{=}&{1}\\ {f_{Y}(y)}&{=}&{|}\\ {}&{=}&{|}\\ {}&{=}&{\frac{1}{6}}\end{array}$$
$$\begin{array}{r c l}{{\bar{y}}}&{{=}}&{{a\bar{x}+b}}\\ {{\sigma_{Y}^{2}}}&{{=}}&{{a^{2}\sigma_{X}^{2}}}\end{array}$$
In other words, the RV Y is Gaussian with a mean and variance given by 

$$(2.44)$$

This important example shows that a linear transformation of a Gaussian RV 
results in a new Gaussian **RV.** 
vvv 

Suppose that we pass a Gaussian RV X N *N(0,u;)* through the nonlinear 
function Y = g(X) = X3: 
$$X=h(Y)\tag{2.45}$$ $$=Y^{1/3}$$ $$h^{\prime}(y)=\frac{y^{-2/3}}{3}$$ $$f_{Y}(y)=|h^{\prime}(y)|f_{X}[h(y)]$$ $$=\frac{y^{-2/3}}{3}\frac{1}{\sigma_{x}\sqrt{2\pi}}\exp[-x^{2}/(2\sigma_{x}^{2})]$$ $$=\frac{y^{-2/3}}{3}\frac{1}{\sigma_{x}\sqrt{2\pi}}\exp[-y^{2/3}/(2\sigma_{x}^{2})]$$
$$(2.46)$$
We see that the nonlinear transformation Y = X3 converts a Gaussian RV 
to a non-Gaussian **RV.** It can be seen that f~(y) approaches 00 as y + 0. 

Nevertheless, the area under the fy(y) curve is equal to 1 since it is a pdf. 

vvv In the more general case of RVs related by the function Y = g(X), where g(.) is a nonmonotonic function, the pdf of Y (evaluated at y) can be computed from the pdf of X as 

$$f_{Y}(y)=\sum_{i}f_{X}(x_{i})/|g^{\prime}(x_{i})|$$

where the 2% values are the solutions of the equation y = **g(z).** 

## 2.4 Multiple Random Variables

$$\begin{array}{r c l}{F_{X}(x)}&{=}&{P(X\leq x)}\\ {F_{Y}(y)}&{=}&{P(Y\leq y)}\end{array}$$

We have already defined the probability distribution function of an RV. For example, if X and Y are RVs, then their distribution functions are defined as 

$$(2.47)$$
$$(2.48)$$

Now we define the probability that both X I z and Y I y as the joint probability distribution function of X and Y: 

$$F_{X Y}(x,y)=P(X\leq x,Y\leq y)$$

FXY(X, y) = P(X 5 *2, y* 5 9) **(2.48)** 
If the meaning is clear from the context, we often use the shorthand notation F(z, y) to represent the distribution function *Fxy(x,* y). Some properties of the joint distribution function are 

F(z,d E [OJI 
$$\begin{array}{r l}{F(x,y)}&{{}\in}\\ {F(x,-\infty)=F(-\infty,y)}&{{}=}\\ {F(\infty,\infty)}&{{}=}\\ {F(a,c)}&{{}\leq}\\ {P(a<x\leq b,c<y\leq d)}&{{}=}\\ {F(x,\infty)}&{{}=}\\ {F(\infty,y)}&{{}=}\end{array}$$
P(u < 2 I b, c < y I d) = F(b, d) + **F(u,** C) - F(u, d) - F(b, C) 
F(z,oo) = *F(x)* 
F(W,Y) = F(Y) **(2.49)** 
$[0,1]$  $0$  $1$  $F(b,d)$ if $a\leq b$ and $c\leq d$  $F(b,d)+F(a,c)-F(a,d)-F(b,c)$  $F(x)$  $F(y)$  $\bullet$\(\bullet
Note from the last two properties that the distribution function of one RV can be 
obtained from the joint distribution function. When the distribution function for a 
single RV is obtained this way it is called the marginal distribution function. 
The joint probability density function is defined as the following derivative of 
the joint PDF:  $$f_{XY}(x,y)=\frac{\partial^{2}F_{XY}(x,y)}{\partial x\partial y}\tag{2.50}$$  As before, we often use the shorthand notation $f(x,y)$ to represent the density 
$$(2.49)$$
$$(2.51)$$
function fxy(z, y). Some properties of the joint pdf that can be obtained from this definition are 

re  $$\begin{array}{rcl}F(x,y)&=&\int_{-\infty}^x\int_{-\infty}^y f(z_1,z_1)\,dz_1\,dz_2\\ f(x,y)&\ge&0\\ \int_{-\infty}^\infty\int_{-\infty}^\infty f(x,y)\,dx\,dy&=&1\\\\ P(a<x\leq b,c<y\leq d)&=&\int_c^d\int_a^b f(x,y)\,dx\,dy\\ f(x)&=&\int_{-\infty}^\infty f(x,y)\,dy\\ f(y)&=&\int_{-\infty}^\infty f(x,y)\,dx\end{array}$$
Note from the last two properties that the density function of one RV can be obtained from the joint density function. When the density function for a single RV is obtained this way it is called the marginal density function. Computing the expected value of a function *g(.,* .) of two RVs is similar to computing the expected value of a function of a single RV: 

$$(2.52)$$
$$(2.54)$$
$$E[g(x,y)]=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}g(x,y)f(x,y)\,d x\,d y$$

## 2.4.1 Statistical Independence

Recall from Section **2.1** that two events are independent if the occurrence of one event has no effect on the probability of the occurrence of the other event. We extend this to say that RVs X *and* Y are independent if they satisfy the following relation: 

$$(2.53)$$
$$P(X\leq x,Y\leq y)=P(X\leq x)P(Y\leq y)\qquad{\mathrm{for~all~}}x,\,y$$

From our definition of joint distribution and density functions, we see that this implies 

$$\begin{array}{r c l}{{F_{X Y}(x,y)}}&{{=}}&{{F_{X}(x)F_{Y}(y)}}\\ {{f_{X Y}(x,y)}}&{{=}}&{{f_{X}(x)f_{Y}(y)}}\end{array}$$

The central limit theorem says that the sum of independent RVs tends toward a Gaussian RV, regardless of the pdf of the individual RVs that contribute to the sum. This is why so many RVs in nature seem to have a Gaussian distribution. 

Many RVs in nature are actually the sum of many individual and independent RVs. For example, the high temperature on any given day in any given location tends to follow a Gaussian distribution. This is because the high temperature is affected by clouds, precipitation, wind, air pressure, humidity, and other factors. Each of these factors is in turn determined by other random factors. The combination of many independent random variables determines the high temperature, which has a Gaussian pdf. 

We define the covariance of two scalar RVs X *and* Y as 

$$\begin{array}{r c l}{{C_{X Y}}}&{{=}}&{{E[(X-\bar{X})(Y-\bar{Y}]}}\\ {{}}&{{=}}&{{E(X Y)-\bar{X}\bar{Y}}}\end{array}$$
$$\rho={\frac{C_{X Y}}{\sigma_{x}\sigma_{y}}}$$

We define the correlation coefficient of two scalar RVs X *and* Y as 

$$(2.55)$$
$$(2.56)$$

$$(2.57)$$

The correlation coefficient is a normalized measurement of the independence between two RVs X and Y. If X and Y are independent, then p = 0 (although the converse is not necessarily true). If Y is a linear function of X then p = fl (see Problem **2.9).** 
We define the correlation of two scalar RVs X *and* Y as 

$$R_{X Y}=E(X Y)$$
Rxy = *E(XY)* **(2.57)** 
Two RVs are said to be uncorrelated if Rxy = E(X)E(Y). 

$$(2.58)$$

From the definition of independence, we see that if two **RVs** are independent then they are also uncorrelated. Independence implies uncorrelatedness, but uncorrelatedness does not necessarily imply independence. However, in the special case in which two **RVs** are both Gaussian and uncorrelated, then it follows that they are also independent. 

Two **RVs** are said to be orthogonal if *Rxy* = 0. If two RVs are uncorrelated, then they are orthogonal only if at least one of them is zero-mean. If two **RVs** are orthogonal, then they may or may not be uncorrelated. 

Two rolls of the dice are represented by the **RVs** X *and* Y. The two **RVs** are independent because one roll of the die does not have any effect on a second roll of the die. Each roll of the die has an equally likely probability **(1/6)** of being a 1, **2, 3, 4, 5,** or 6. Therefore, 

$E(X)=E(Y)=\frac{1+2+3+4+5+6}{6}$  $=$ 3.5
There are 36 possible combinations of the two rolls of the die. We could get the combination **(l,l), (1,2),** and so on. Each of these 36 combinations have an equally likely probability (1 **/36).** Therefore, the correlation between X and Y is 

$$\begin{array}{r c l}{{R_{X Y}=E(X Y)}}&{{=}}&{{\frac{1}{36}\sum_{i=1}^{6}\sum_{j=1}^{6}i j}}\\ {{}}&{{=}}&{{12.25}}\\ {{}}&{{=}}&{{E(X)E(Y)}}\end{array}$$

Since E(XY) = *E(X)E(Y),* we see that X *and* Y are uncorrelated. However, Rxy \# 0, *so X* and Y are not orthogonal. 

vvv 

## H **Example2.7**

A slot machine is rigged so you get 1 or -1 with equal probability the first spin X, and the opposite number the second spin Y. We have equal probabilities of obtaining *(X, Y)* outcomes of (1, -1) and **(-1,l).** The two RVs are dependent because the realization of Y depends on the realization of X. We also see that 

$$(2.59)$$
 $\begin{array}{rcl}\mbox{-}&\\ E(X)&=&0\\ E(Y)&=&0\\ E(XY)&=&\dfrac{(1)(-1)+(-1)(1)}{2}\\ &=&-1\end{array}$  $'\mbox{are correlated because}E(XY)\neq E(X)E(Y).$
$$(2.60)$$

We see that X and Y are correlated because E(XY) \# *E(X)E(Y).* We also see that X and Y are not orthogonal because *E(XY)* \# 0. 

vvv 

A slot machine is rigged so you get **-1,** 0, or +1 with equal probability the first spin X. On the second spin Y you get 1 if X = 0, and 0 if X \# 0. The two RVs are dependent because the realization of Y depends on the realization of X. We also *see* that 

$$\begin{array}{r l}{=}&{{}{\frac{-1+0+1}{3}}}\\ {=}&{{}0}\\ {=}&{{}{\frac{0+1+0}{3}}}\\ {=}&{{}1/3}\\ {=}&{{}{\frac{(-1)(0)+(0)(1)+(1)(0)}{3}}}\\ {=}&{{}0}\end{array}$$
$${E}{\left({X}\right)}$$  $${E}{\left({Y}\right)}$$  $${E}{\left({X}{Y}\right)}$$  ... 
3 *E(Y)* = 
$$(2.61)$$
=o **(2.61)** 
We see that X *and* Y are uncorrelated because E(XY) = *E(X)E(Y).* We also *see* that X and Y are orthogonal because *E(XY)* = 0. This example illustrates the fact that uncorrelatedness does not necessarily imply independence. 

vvv 

Suppose that x and y are independent RVs, and the RV z is computed as z = *g(x)* + h(y). In this example, we will calculate the mean of z: 

$$\begin{array}{l}{{E[g(x)+h(y)]}}\\ {{\int\int[g(x)+h(y)]f(x,y)\,d x\,d y}}\\ {{\int\int\,g(x)f(x)f(y)\,d x\,d y+\int\int h(y)f(x)f(y)\,d x\,d y}}\\ {{\int\,g(x)f(x)\,d x\,\int\,f(y)\,d y+\int\,h(y)f(y)\,d y\,\int\,f(x)\,d x}}\\ {{E[g(x)](1)+E[h(y)](1)}}\\ {{E[g(x)]+E[h(y)]}}\end{array}$$

E(z) = E[g(4 +h(Y)l 
$$(2.62)$$
$$(2.63)$$

As a special case of this example, we see that the mean of the sum of two independent RVs is equal to the sum of their means. That is, 

$$E(x+y)=E(x)+E(y)\quad{\mathrm{~if~}}x{\mathrm{~and~}}y{\mathrm{~are~independent}}$$

## Vvv Example 2.10

Suppose we roll a die twice. What is the expected value of the sum of the two outcomes? We use X *and* Y to refer to the two rolls of the die, and we use 

$$(2.64)$$

2 to refer to the sum of the two outcomes. Therefore, 2 = X + Y. Since X 
and Y are independent, we have 

$$\begin{array}{r c l}{{E(Z)}}&{{=}}&{{E(X)+E(Y)}}\\ {{}}&{{=}}&{{3.5+3.5}}\\ {{}}&{{=}}&{{7}}\end{array}$$

## Vvq Example 2.11

Consider the circuit of Figure **2.4.** The input voltage V is uniformly distributed on [-1,1]. Voltage V has units of volts, and the two currents have units of amps. 

$$\begin{array}{r c l}{{I_{1}}}&{{=}}&{{\left\{\begin{array}{l l}{{0}}\\ {{V}}\end{array}\right.}}\\ {{}}&{{}}&{{I_{2}}}\end{array}=}&{{\left\{\begin{array}{l l}{{V}}\\ {{0}}\end{array}\right.}}\end{array}$$
$$\begin{array}{l}{{\mathrm{if~}V>0}}\\ {{\mathrm{if~}V\leq0}}\end{array}$$
$$\begin{array}{r}{(2.65)}\end{array}$$
I1 = { V ifVIO 
0 ifV<O I2 = { **(2.65)** 
$$\begin{array}{l}{{\mathrm{if~}V\geq0}}\\ {{\mathrm{if~}V<0}}\end{array}$$

We see that I1 is uniformly distributed on [-1,0] and I2 is uniformly distributed on **[0,1].** The RVs V, 11, and I2 have expected values 

$$\begin{array}{r l}{E(V)}&{{}=}\\ {E(I_{1})}&{{}=}\\ {E(I_{2})}&{{}=}\end{array}$$
$$\begin{array}{l}{{0}}\\ {{-1/2}}\\ {{1/2}}\end{array}$$
$$(2.66)\,$$. 
E(I1) = **-1/2** 
E(12) = **1/2 (2.66)** 
The RVs I1 and I2 are not independent because they are related to each other; if I2 \# 0 then 11 = 0, and if I1 \# 0 then I2 = 0. Since either 11 or I2 is equal to 0 at every time instant, *I14* = 0 and *E(IlI2)* = 0. Therefore 11 and 12 are orthogonal. Since *E(Il)E(I2)* = **-1/4,** we see that E(I1I2) \# *E(Il)E(I2),* 
and I1 and I2 are correlated. 

Figure **2.4** Circuit for Example 2.11. 

![16_image_0.png](16_image_0.png)

## Vvv 2.4.2 Multivariate Statistics

The discussion in the previous subsection can be generalized for RVs that are vectors. In this case, the quantities defined earlier become vectors and matrices. Given an n-element RV X and an rn-element RV Y (assuming that both X and Y are column vectors), their correlation is defined as 

$$\begin{array}{r c l}{{R_{X Y}}}&{{=}}&{{E(X Y^{T})}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{\left[\begin{array}{c c c}{{E(X_{1}Y_{1})}}&{{\cdots}}\\ {{}}&{{}}\\ {{\vdots}}\\ {{E(X_{n}Y_{1})}}&{{\cdots}}\end{array}\right]}}\end{array}$$
$$\left.\begin{array}{c}{{E(X_{1}Y_{m})}}\\ {{\vdots}}\\ {{E(X_{n}Y_{m})}}\end{array}\right]$$
- (2.67) 
Their covariance is defined as 

$$\begin{array}{l l l}{{C_{X Y}}}&{{=}}&{{E[(X-\bar{X})(Y-\bar{Y})^{T}]}}\\ {{}}&{{=}}&{{E(X Y^{T})-\bar{X}\bar{Y}^{T}}}\end{array}$$
$$(2.67)$$
$$(2.68)$$

The autocorrelation of the n-element RV X is defined as 

$$\begin{array}{r c l}{{R_{X}}}&{{=}}&{{E[X X^{T}]}}\\ {{}}&{{=}}&{{\left[\begin{array}{c c c}{{}}&{{E[X_{1}^{2}]}}&{{\cdots}}&{{E[X_{1}X_{n}]}}\\ {{}}&{{}}&{{}}&{{\vdots}}\\ {{}}&{{}}&{{E[X_{n}X_{1}]}}&{{\cdots}}&{{E[X_{n}^{2}]}}\end{array}\right]}}\end{array}$$
$$(2.69)$$
$$\begin{array}{r c l}{{z^{T}R_{X}z}}&{{=}}&{{z^{T}E[X X^{T}]z}}\\ {{}}&{{=}}&{{E[z^{T}X X^{T}z]}}\\ {{}}&{{=}}&{{E[(z^{T}X)^{2}]}}\\ {{}}&{{\geq}}&{{0}}\end{array}$$

Note that E(X,X,) = **E(X,X,)** so Rx = *R$.* An autocorrelation matrix is always symmetric. Also note that for any n-element column vector z we have 

$$(2.70)$$

So an autocorrelation matrix is always positive semidefinite. 

The autocovariance of the n-element RV X is defined as 

$$C_{X}=E[(X-\bar{X})(X-\bar{X})^{T}]\tag{2.71}$$ $$=\left[\begin{array}{cccc}E[(X_{1}-\bar{X}_{1})^{2}]&\ldots&E[(X_{1}-\bar{X}_{1})(X_{n}-\bar{X}_{n})]\\ \vdots&\vdots&\vdots\\ E[(X_{n}-\bar{X}_{n})(X_{1}-\bar{X}_{1})]&\ldots&E[(X_{n}-\bar{X}_{n})^{2}]\end{array}\right]$$ $$=\left[\begin{array}{cccc}\sigma_{1}^{2}&\ldots&\sigma_{1n}\\ \vdots&&\vdots\\ \sigma_{n1}&\ldots&\sigma_{n}^{2}\end{array}\right]$$
$$(2.72)$$

Note that u,j = **uj,** *so Cx* = **CT.** An autocovariance matrix is always symmetric. 

Also note that for any n-element column vector z we have 

$$\stackrel{\cdot}{z^{T}C x z}$$
$$=z^{T}E[(X-\bar{X})(X-\bar{X})^{T}]z\tag{2.72}$$ $$=E[z^{T}(X-\bar{X})(X-\bar{X})^{T}z]$$ $$=E[(z^{T}(X-\bar{X}))^{2}]$$ $$\geq0$$

So an autocovariance matrix is always positive semidefinite. 

An n-element RV X is Gaussian (n~rmal)~ if 

$${\rm pdf}(X)=\frac{1}{(2\pi)^{n/2}|C_{X}|^{1/2}}\exp\left[\frac{-1}{2}(X-\bar{X})^{T}C_{\bar{X}}^{-1}(X-\bar{X})\right]\tag{2.73}$$

Now consider a Gaussian RV X that undergoes a linear transformation: 

$$Y=g(X)\tag{2.74}$$ $$=AX+b$$

where A is a constant n x n matrix, and b is a constant n-element vector. If A is invertible, then 

$$\begin{array}{l l l l}{{X}}&{{=}}&{{h(Y)}}\\ {{}}&{{=}}&{{A^{-1}Y-A^{-1}b}}\end{array}\qquad\qquad\qquad(2.75)$$

From Equation **(2.42)** we obtain 

v N N(AZ+b,ACxAT) (2.76) 
This shows that normality is preserved in linear transformations of random vectors (just as it is preserved in linear transformations of random scalars, as seen in Example **2.4).** 
3Fkancis Edgeworth (1845-1926), an Irish economist and mathematician, first provided a general description and study of the multivariate Gaussian probability distribution in 1892 [Sor80]. 

## 2.5 Stochastic Processes

A stochastic process, also called a random process, is a very simple generalization of the concept of an RV. A stochastic process *X(t)* is an RV X that changes with time.4 A stochastic process can be one of four types. 

0 If the RV at each time is continuous and time is continuous, then X(t) is a continuous random process. For example, the temperature at each moment of the day is a continuous random process because both temperature and time are continuous. 

0 If the RV at each time is discrete and time is continuous, then *X(t)* is a discrete random process. For example, the number of people in a given building at each moment of the day is a discrete random process because the number of people is a discrete variable and time is continuous. 

0 If the RV at each time is continuous and time is discrete, then *X(t)* is a continuous random sequence. For example, the high temperature each day is a continuous random sequence because temperature is continuous but time is discrete (day one, day two, etc.). 
0 If the RV at each time is discrete and time is discrete, then *X(t)* is a discrete random sequence. For example, the highest number of people in a given building each day is a discrete random sequence because the number of people is a discrete variable and time is also discrete. 

Since a stochastic process is an RV that changes with time, it has a distribution and density function that are functions of time. The PDF of *X(t)* is 

$$F_{X}(x,t)=P(X(t)\leq x)$$
$$f_{X}(x,t)={\frac{d F_{X}(x,t)}{d x}}$$
Fx(x,t) = *P(X(t) 5 x)* (2.77) 
If *X(t)* is a random vector, then the inequality above is an element-by-element inequality. For example, if *X(t)* has n elements, then 

$$(2.77)$$
$$(2.78)$$
$$F_{X}(x,t)=P\left[X_{1}(t)\leq x_{1}{\mathrm{~and~}}\cdots X_{n}(t)\leq x_{n}(t)\right]$$

The pdf of *X(t)* is 

$$(2.79)$$

If *X(t)* is a random vector, then the derivative above is taken once with respect to each element of 2. For example, if *X(t)* has n elements, then 

$$(2.80)$$

The mean and covariance of *X(t)* are also functions of time: 

$$f_{X}(x,t)={\frac{d^{n}F_{X}(x,t)}{d x_{1}\cdots d x_{n}}}$$
$$\begin{array}{r c l}{{\bar{x}(t)}}&{{=}}&{{\int_{-\infty}^{\infty}x f(x,t)\,d x}}\end{array}$$

4Actually, the independent variable does not have to be time; for example, it could be spatial location or something else. But typically the independent variable is time, and in this book it will always be time. 

$$C_{X}(t)=E\left\{\left[X(t)-\bar{x}(t)\right]\left[X(t)-\bar{x}(t)\right]^{T}\right\}\tag{2.81}$$ $$=\int_{-\infty}^{\infty}\left[x-\bar{x}(t)\right]\left[x-\bar{x}(t)\right]^{T}f(x,t)\,dx$$

Note that **X(t)** at two different times **(tl** and **t2)** comprise two different random variables [X(tl) and **X(t2)l.** Therefore, we can talk about the joint distribution and joint density functions of **X(t1)** and **X(t2).** These are called the second-order distribution function and the second-order density function: 

$$F(x_{1},x_{2},t_{1},t_{2})=P(X(t_{1})\leq x_{1},X(t_{2})\leq x_{2})$$ $$f(x_{1},x_{2},t_{1},t_{2})=\frac{\partial^{2}F(x_{1},x_{2},t_{1},t_{2})}{\partial x_{1}\partial x_{2}}\tag{2.82}$$

As discussed earlier, if **X(t)** is an n-element random vector, then the inequality that defines *F(Q,* **z2, tl, t2)** actually consists of 2n inequalities, and the derivative that defines **f(sl,z2, tl, t2)** actually consists of 2n derivatives. 

The correlation between the two RVs **X(t1)** and **X(t2)** is called the autocorrelation of the stochastic process X(t): 

$$R_{X}(t_{1},t_{2})=E\left[X(t_{1})X^{T}(t_{2})\right]$$
$$C_{X}(t_{1},t_{2})=E\left\{\left[X(t_{1})-{\tilde{X}}(t_{1})\right]\left[X(t_{2})-{\tilde{X}}(t_{2})\right]^{T}\right\}$$

The autocovariance of a stochastic process is defined as 

$$(2.83)$$
$$(2.84)$$

For some stochastic processes, the pdf does not change with time. For example, if we flip a coin ten times then we can view that process as a stochastic process with the statistics of the process being the same at each of the ten time instances. 

In this case, the stochastic process is called strict-sense stationary (SSS), or just stationary for short. In this case, the mean of the stochastic process is constant with respect to time, and the autocorrelation is a function of the time difference t2 - tl (not a function of the absolute times): 

$$E[X(t)]=\bar{x}$$ $$E[X(t_{1})X^{T}(t_{2})]=R_{X}(t_{2}-t_{1})\tag{2.85}$$
$$(2.87)$$

For some stochastic processes, these two conditions are true even though the pdf does change with time. Stochastic processes for which these two conditions are true are called widesense stationary (WSS). A stationary process is widesense stationary, but a widesense stationary process may or may not be stationary. From the definition of autocorrelation, it can be shown that for a widesense stationary process the following properties hold: 

$$R_{X}(0)=E[X(t)X^{T}(t)]$$ $$R_{X}(-\tau)=R_{X}(\tau)\tag{2.86}$$
$$|R_{X}(\tau)|\leq R_{X}(0)$$

For scalar stochastic processes, it can be shown that 

1. The high temperature each day can be considered a stochastic process. However, this process is not stationary. The high temperature on a day in July might be an RV with a mean of 100 degrees Fahrenheit, but the high temperature on a day in December might have a mean of 30 degrees. This is a stochastic process whose statistics change with time, so the process is not stationary. 

2. Electrical noise in a voltmeter might have a mean of zero and a variance of one millivolt. If we come back the next day and measure the noise again, the mean and variance may be the same as before. If the statistics of the noise are the same every day, then the electrical noise is a stationary process. Note that in reality the noise statistics will eventually change. For example, after a few decades the instrument will begin degrading and the electrical noise mean and variance will change. In this sense, there is no such thing as a stationary random process. Eventually, the universe will freeze and all signals will change. But for practical purposes, if the statistics of a random process do not change over the time interval of interest, then we consider the process to be stationary. 

3. Tomorrow's closing price of the Dow Jones Industrial Average might be an RV with a certain mean and variance. However, 100 years ago the closing price had a mean that was much lower. The closing price of the stock market is an RV whose mean generally increases with time. Therefore, the stock market price is a nonstationary stochastic process. 

vvv Suppose we have a stochastic process *X(t).* Further suppose that the process has a realization *z(t).* The time average of *X(t)* is denoted as *A[X(t)],* and the time autocorrelation of *X(t)* is denoted as *R[X(t)].* These quantities are defined for continuous-time random processes as 

$$\begin{array}{r c l}{{A[X(t)]}}&{{=}}&{{\operatorname*{lim}_{T\to\infty}{\frac{1}{2T}}\int_{-T}^{T}x(t)\,d t}}\\ {{R[X(t),\tau]}}&{{=}}&{{A[X(t)X^{T}(t+\tau)]}}\end{array}$$
A[X(t)] = lim I] 
The definitions for discretetime random processes are straightforward extensions of the continuoustime definitions. 

An ergodic process is a stationary random process for which 

$$(2.88)$$
$$A[X(t)]=E(X)$$ $$R[X(t),\tau]=R_{X}(\tau)\tag{2.89}$$

In the real world, we are often limited to only a few realizations of a stochastic process. For example, if we measure the fluctuation of a voltmeter reading, we are actually only measuring only one realization of a stochastic process. We can compute the time average, time autocorrelation, and other time-based statistics of the realization. If the random process is ergodic, then we can use those time averages to estimate the statistics of the stochastic process. 

1. Suppose each unit of an electrical instrument is manufactured with a small random bias. Is the noise of the instrumentation ergodic? If we measure the noise of one instrument then we measure its bias, which is equal to its mean. However, if we measure the noise of another instrument it might have a different mean because it has a different bias. In other words, we cannot obtain the mean of the stochastic process by simply investigating one instrument (i.e., one realization of the stochastic process). Therefore, the stochastic process is not ergodic. 

2. Suppose each unit of an electrical instrument is manufactured identically, each with zero-mean stationary Gaussian noise. Is the noise ergodic? In this case we could measure the mean of the process by measuring the noise of many separate instruments at one instant of time, or by measuring the noise of one instrument over an extended period of time. Either experiment would correctly inform us that the mean of the stochastic process is zero. We could find the statistics of the stochastic process using all the instruments at a single time, or using a single instrument at many different times. Therefore, the stochastic process is ergodic. 

vvv The definitions of correlation and covariance can be extended to two stochastic processes X(t) and *Y(t).* The cross correlation of *X(t)* and *Y(t)* is defined as 

$$R_{X Y}(t_{1},t_{2})=E[X(t_{1})Y^{T}(t_{2})]$$
$$(2.90)$$

$$(2.91)$$
RXY(t1, t2) = *E[X(tl)YT(t2)1* (2.90) 
Two random processes *X(t)* and Y(t) are said to be uncorrelated if Rxy(t1, t2) = 
E[X(t1)]E[YT(t2)] for all tl and tz. The cross covariance of *X(t)* and *Y(t)* is defined as 

$$C_{X Y}(t_{1},t_{2})=E\left\{[X(t_{1})-\tilde{X}(t_{1})][Y(t_{2})-\tilde{Y}(t_{2})]^{T}\right\}$$

## 2.6 White Noise And Colored Noise

If the RV *X(t1)* is independent from the RV *X(tz)* for all tl \# tz then *X(t)* is called white noise. Otherwise, *X(t)* is called colored noise. 

The whiteness or color content of a stochastic process can be characterized by its power spectrum. The power spectrum *Sx(w)* of a widesense stationary stochastic process *X(t)* is defined as the Fourier transform of the autocorrelation. The autocorrelation is the inverse Fourier transform of the power spectrum. 

$$\begin{array}{r c l}{{S_{X}(\omega)}}&{{=}}&{{\int_{-\infty}^{\infty}R_{X}(\tau)e^{-j\omega\tau}\,d\tau}}\\ {{R_{X}(\tau)}}&{{=}}&{{\frac{1}{2\pi}\int_{-\infty}^{\infty}S_{X}(\omega)e^{j\omega\tau}\,d\omega}}\end{array}$$  I'm lost by Wien = Wien's law, but I am not sure how it's. 
$$(2.92)$$

These equations are called the Wiener-Khintchine relations after Norbert Wiener and Aleksandr Khinchin. Note that some authors put the term 1/2n on the right side of the *Sx(w)* definition, in which case the 1127~ term on the right side of the RX(T) definition disappears. The power spectrum is sometimes referred to as the power density spectrum, the power spectral density, or the power density. The power of a wide-sense stationary stochastic process is defined as 

$$(2.93)$$

The cross power spectrum of two wide-sense stationary stochastic processes *X(t)* 
and Y(t) is the Fourier transform of the cross correlation: 

$$P_{X}={\frac{1}{2\pi}}\int_{-\infty}^{\infty}S_{X}(\omega)\,d\omega$$
$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{S_{X Y}(\omega)}}&{{=}}&{{\int_{-\infty}^{\infty}R_{X Y}(\tau)e^{-j\omega\tau}\,d\tau}}\\ {{}}&{{}}&{{}}\\ {{R_{X Y}(\tau)}}&{{=}}&{{\frac{1}{2\pi}\int_{-\infty}^{\infty}S_{X Y}(\omega)e^{j\omega\tau}\,d\omega}}\end{array}$$  which is a similar procedure. 
$$(2.94)$$

Similar definitions hold for discrete-time random processes. The power spectrum of a discretetime random process is defined as 

$$\begin{array}{r c l}{{S_{X}(\omega)}}&{{=}}&{{\sum_{k=-\infty}^{\infty}R_{X}(k)e^{-j\omega k}\qquad\omega\in[-\pi,\pi]}}\\ {{}}&{{}}&{{}}\\ {{R_{X}(k)}}&{{=}}&{{\frac{1}{2\pi}\int_{-\infty}^{\infty}S_{X}(\omega)e^{j k\omega}\,d\omega}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\end{array}$$
$$(2.95)$$
$$(2.96)$$
$$(2.97)$$
$$(2.98)$$

A discretetime stochastic process X(t) is called white noise if 

$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{R_{X}(k)}}&{{=}}&{{\left\{\begin{array}{l l}{{\sigma^{2}}}&{{\mathrm{if~}k=0}}\\ {{0}}&{{\mathrm{if~}k\neq0}}\end{array}\right.}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{\sigma^{2}\delta_{k}}}\end{array}$$

where 6k is the Kronecker delta function, defined as 
The definition of discrete-time white noise shows that it does not have any correlation with itself except at the present time. If X(k) is a discretetime white noise 
process, then the RV *X(n)* is uncorrelated with X(m) unless n = m. This shows 
$\delta_{k}=\left\{\begin{array}{ll}1&\mbox{if$k=0$}\\ 0&\mbox{if$k\neq 0$}\end{array}\right.$
that the power of a discrete-time white noise process is equal at all frequencies: 
Sx(w) = Rx(0) for all w E *[-n, n]* **(2.98)** 
For a continuous-time random process, white noise is defined similarly. White noise 
has equal power at all frequencies (like white light): 
SX(W) = Rx(0) for all w **(2.99)** 
Substituting this expression for Sx(w) into Equation **(2.92),** we see that for continuoustime white noise 
$$S_{X}(\omega)=R_{X}(0)\quad{\mathrm{~for~all~}}\omega\in\left[-\pi,\pi\right]$$

$$(2.99)$$
$$S_{X}(\omega)=R_{X}(0)\quad\mathrm{~for~all~}\omega$$
$$(2.100)$$
$$R_{X}(\tau)=R_{X}(0)\delta(\tau)$$

Rx(7) = Rx(0)6(7) (2.100) 
where *6(r)* is the continuous-time impulse function. That is, 6(~) is a function that is zero everywhere except at r = 0; it has a width of 0, a height of *CCJ,* and an area of 1. Continuous-time white noise is not something that occurs in the real world because it has infinite power, as seen by comparing Equations **(2.93)** and **(2.99).** Nevertheless, many continuous-time processes approximate white noise and are useful in mathematical analyses of signals and systems. 

Suppose that a zero-mean stationary stochastic process has the autocorrelation function 

$R_{X}(\tau)=\sigma^{2}e^{-\beta|\tau|}$ (2.101)
where ,B is a positive real number. The power spectrum is computed from Equation *(2.92)* as 

$$S_{X}(\omega)=\int_{-\infty}^{\infty}\sigma^{2}e^{-\beta|\tau|}e^{-j\omega\tau}\,d\tau\tag{2.102}$$ $$=\int_{-\infty}^{0}\sigma^{2}e^{(\beta-j\omega)\tau}\,d\tau+\int_{0}^{\infty}\sigma^{2}e^{-(\beta+j\omega)\tau}\,d\tau$$ $$=\frac{\sigma^{2}}{\beta-j\omega}+\frac{\sigma^{2}}{\beta+j\omega}$$ $$=\frac{2\sigma^{2}\beta}{\omega^{2}+\beta^{2}}$$
 The stochastic process is computed as  $$\begin{array}{rcl}E[X^2(t)]&=&\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{2\sigma^2\beta}{\omega^2+\beta^2}\,d\omega\\ &=&\frac{\sigma^2\beta}{\pi}\left[\frac{1}{\beta}\tan^{-1}\frac{\omega}{\beta}\right]_{-\infty}^{\infty}\\ &=&\sigma^2\\ &=&R_X(0)\end{array}$$
27r J *-oilw2+p2* - 
The variance of the stochastic process is computed as 

$$(2.103)$$
$$(2.104)$$

vvv 

## 2.7 Simulating Correlated Noise

In optimal filtering research and experiments, we often have to simulate correlated white noise. That is, we need to create random vectors whose elements are correlated with each other according to some predefined covariance matrix. In this section, we will present one way of accomplishing this. 

Suppose we want to generate an n-element random vector w that has zero mean and covariance Q: 

$$Q={\left[\begin{array}{l l l}{\sigma_{1}^{2}}&{\cdots}&{\sigma_{1n}}\\ {\vdots}&{}&{\vdots}\\ {\sigma_{1n}}&{\cdots}&{\sigma_{n}^{2}}\end{array}\right]}$$
$$(2.105)$$

Since Q is a covariance matrix, we know that all of its eigenvalues are real and nonnegative. We can therefore denote its eigenvalues as *p::* 

$$\lambda(Q)=\mu_{k}^{2}\;\;\;\;\;(k=1,\ldots,n)$$

Suppose the eigenvectors of Q are found to be dl, ., *dn.* Augment the d, vectors together to obtain an n x n matrix D. Since Q is symmetric, we can always choose the eigenvectors such that D is orthogonal, that is, D-l = *DT.* We therefore obtain the Jordan form decomposition of Q as 

$$Q=D{\hat{Q}}D^{T}$$
$$(2.106)$$

$$(2.107)$$

Q = *DQDT* (2.106) 
where Q is the diagonal matrix of the eigenvalues of Q. That is, 

$${\hat{Q}}=\operatorname{diag}(\mu_{1}^{2},\cdots,\mu_{n}^{2})$$
$$(2.108)$$
Q = diag(p.:, a * 7 *P:)* (2.107) 
Now we define the random vector v as v = *D-lw, so* that w = *Dv.* Therefore, 
$$\begin{array}{r c l}{{E(v v^{T})}}&{{=}}&{{E(D^{T}w w^{T}D)}}\\ {{}}&{{=}}&{{D^{T}Q D}}\\ {{}}&{{=}}&{{\hat{Q}}}\\ {{}}&{{=}}&{{\mathrm{diag}(\mu_{1}^{2},\cdots,\mu_{n}^{2})}}\end{array}$$

This shows how we can generate an n-element random vector w with a covariance matrix of Q. The algorithm is given as follows. 

## Correlated Noise Simulation

1. Find the eigenvalues of Q, and denote them as *p:,* - - ., p, 2 2. Find the eigenvectors of Q, and denote them as dl, - ., *d,,* such that 

$D=\left[\begin{array}{cccc}d_{1}&\cdots&d_{n}\end{array}\right]$  $D^{-1}=D^{T}$ (2.109)
3. For i = 1,. -, n compute the random variable vi = *pir2,* where each rZ is an independent random number with a variance of 1 (unity variance). 

4. Set w = *Dv.* 

## 2.8 Summary

In this chapter, we have reviewed the basic concepts of probability, random variables, and stochastic processes. The probability of some event occurring is simply and intuitively defined as the number of times the event occurs divided by the number of chances the event has to occur. A random variable (RV) is a variable whose value is not certain, but is governed by the laws of probability. For example, your score on the test for this chapter is not deterministic, but is a random variable. Your *actual* score, after you take the test, will be a specific, deterministic number. But *before* you take the test, you do not know what you will get on the test. You may suppose that you will probably get between 80% and 90% if you have a decent understanding of the material, but your actual score will be determined by random events such as your health, how well you sleep the night before, what topics the instructor decides to cover on the test versus what topics you study, what the traffic was like on the way to school, the mood of the instructor when she grades the test, and so on. A stochastic process is a random variable that changes with time, such as your performance on all of the quizzes and homework assignments for this course. The expected value of your test grades may be constant throughout the duration of the course if you are a consistent person, or it may increase if you tend to study harder as the course progresses, or it may decrease if you tend to study less as the course progresses. Probability, random variables, stochastic processes, and related topics form a huge area of study that we have only touched on in this chapter. Additional information on these topics can be found in many textbooks, including [Pap02, PeeOl]. A study of these topics will allow a student to delve into many practical engineering subjects, including control and estimation theory, signal processing, and communications theory. 

## Problems Written Exercises

2.1 RV? 

What is the 0th moment of an RV? What is the 0th central moment of an Suppose a deck of 52 cards is randomly divided into four piles of 13 cards 2.2 each. Find the probability that each pile contains exactly one ace [GreOl]. 

2.3 Determine the value of a in the function 

$$f_{X}(x)={\left\{\begin{array}{l l}{a x(1-x)}&{x\in[0,1]}\\ {0}&{{\mathrm{~otherwise~}}}\end{array}\right.}$$
$$f_{X}(x)={\frac{a}{e^{x}+e^{-x}}}$$

so that fx *(x)* is a valid probability density function [Lie67]. 

2.4 Determine the value of a in the function so that fx *(x)* is a valid probability density function. What is the probability that 1x1 5 l? 

$$f_{X}(x)={\left\{\begin{array}{l l}{a e^{-a x}}&{x>0}\\ {0}&{x\leq0}\end{array}\right.}$$

2.5 The probability density function of an exponentially distributed random variable is defined as follows. where *a 2* 0. 

a) Find the probability distribution function of an exponentially distributed random variable. 

b) Find the mean of an exponentially distributed random variable. 

c) Find the second moment of an exponentially distributed random variable. 

d) Find the variance of an exponentially distributed random variable. 

e) What is the probability that an exponentially distributed random variable takes on a value within one standard deviation of its mean? 

2.6 first, second, and third moments. 

Derive an expression for the skew of a random variable as a function of its 2.7 Consider the following probability density function: 

$$f_{X}(x)={\frac{a b}{b^{2}+x^{2}}},\ \ \ \ b>0$$

b2 + x2 ' *fx(2)* = - 
a) Determine the value of a in the so that **fx(2)** is a valid probability density function. (The correct value of a makes *fx(2)* a Cauchy pdf.) 
b) Find the mean of a Cauchy random variable. 

2.8 Consider two zero-mean uncorrelated random variables W *and* V with standard deviations gw and *uv,* respectively. What is the standard deviation of the random variable X = W + V? 

2.9 Consider two scalar RVs X and Y. 

a) Prove that if X and Y are independent, then their correlation coefficient p = 0. 

b) Find an example of two RVs that are not independent but that have a correlation coefficient of zero. 

c) Prove that if Y is a linear function of X then p = fl. 

2.10 Consider the following function [Lie67]. 

$$f_{X Y}(x,y)={\left\{\begin{array}{l l}{a e^{-2x}e^{-3y}}&{x>0,y>0}\\ {0}&{{\mathrm{~otherwise~}}}\end{array}\right.}$$

a) Find the value of a so that *fxy(2,* y) is a valid joint probability density function. 

b) Calculate and g. 

c) Calculate **E(X2),** E(Y2), and *E(XY).* 
d) Calculate the autocorrelation matrix of the random vector [ X 
e) Calculate the variance **09,** the variance *ci,* and the covariance *Cxy.* 
f) Calculate the autocovariance matrix of the random vector [ X 
g) Calculate the correlation coefficient between X and Y. 

T 
Y ] . 

Y ] . 

T 
2.11 k are positive constants. 

A stochastic process has the autocorrelation Rx(T) = *Ae-klT1,* where A and a) What is the power spectrum of the stochastic process? 

b) What is the total power of the stochastic process? 

c) What value of k results in half of the total power residing in frequencies less than 1 Hz? 

2.12 Suppose X is a random variable, and *Y (t)* = X cost is a stochastic process. 

a) Find the expected value of *Y(t).* 
b) Find *A[Y(t)],* the time average of *Y(t).* 
c) Under what condition is y(t) = *A[Y(t)]?* 
2.13 Figure **2.5.** 
a) Plot the pdf of *(ZlX)* as a function of X for 2 = **0.5.** 
Consider the equation 2 = X + V. The pdf's of X *and* B are given in b) Given Z = 0.5, what is conditional expectation of X? What is the most probable value of X? What is the median value of X? 

![28_image_0.png](28_image_0.png)

Figure **2.5** pdf's for Problem **2.13** [Sch73]. 
2.14 The temperature at noon in London is a stochastic process. Is it ergodic? 

## Computer Exercises

2.15 Generate N = 50 independent random numbers, each uniformly distributed between 0 and 1. Plot a histogram of the random numbers using 10 bins. What is the sample mean and standard deviation of the numbers that you generated? 

What would you expect to see for the mean and standard deviation (i.e., what are the theoretical mean and standard deviation)? Repeat for N = 500 and N = 5,000 random numbers. What changes in the histogram do you see as N increases? 2.16 Generate 10,000 samples of (z1+ **22)/2,** where each 2% is a random number uniformly distributed on [-1/2, +1/2]. Plot the 50-bin histogram. Repeat for 
(XI+ xz + 23 + **24)/4.** Describe the difference between the two histograms. 