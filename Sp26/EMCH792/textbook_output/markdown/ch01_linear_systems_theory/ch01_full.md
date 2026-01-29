---
type: chapter
chapter: 1
title: Linear systems theory
---
# Chapter 1 Linear Systems Theory

Finally, we make some remarks on why *linear* systems are so important. The answer is simple: because we can solve them! 

--Richard Feynman [Fey63, p. **25-41** 
This chapter reviews some essentials of linear systems theory. This material is typically covered in a linear systems course, which is a first-semester graduate level course in electrical engineering. The theory of optimal state estimation heavily relies on matrix theory, including matrix calculus, so matrix theory is reviewed in Section 1.1. Optimal state estimation can be applied to both linear and nonlinear systems, although state estimation is much more straightforward for linear systems. Linear systems are briefly reviewed in Section **1.2** and nonlinear systems are discussed in Section **1.3.** State-space systems can be represented in the continuoustime domain or the discrete-time domain. Physical systems are typically described in continuous time, but control and state estimation algorithms are typically implemented on digital computers. Section **1.4** discusses some standard methods for obtaining a discrete-time representation of a continuous-time system. Section 1.5 discusses how to simulate continuous-time systems on a digital computer. Sections 1.6 and **1.7** discuss the standard concepts of stability, controllability, and observability of linear systems. These concepts are necessary to understand some of the optimal state estimation material later in the book. Students with a strong background in linear systems theory can skip the material in this chapter. However, it would still help to at least review this chapter to solidify the foundational concepts of state estimation before moving on to the later chapters of this book. 

## 1.1 Matrix Algebra And Matrix Calculus

$$\left[\begin{array}{l l l}{1}&{3}&{\pi}\end{array}\right]$$
$$(1.1)$$

In this section, we review matrices, matrix algebra, and matrix calculus. This is necessary in order to understand the rest of the book because optimal state estimation algorithms are usually formulated with matrices. 

A scalar is a single quantity. For example, the number 2 is a scalar. The number 1 + 3j is a scalar (we use j in this book to denote the square root of -1). The number T is a scalar. 

A vector consists of scalars that are arranged in a row or column. For example, the vector P 3 TI (1.1) 
is a %element vector. This vector is a called a 1 x 3 vector because it has 1 row and 3 columns. This vector is also called a row vector because it is arranged as a single row. The vector 

$$\left[\begin{array}{l}{-2}\\ {\pi^{2}}\\ {j}\\ {0}\end{array}\right]$$

$$(1.2)$$

is a 4-element vector. This vector is a called a 4 x 1 vector because it has 4 rows and 1 column. This vector is also called a column vector because it is arranged as a single column. Note that a scalar can be viewed as a 1-element vector; a scalar is a degenerate vector. (This is just like a plane can be viewed as a 3-dimensional shape; a plane is a degenerate 3-dimensional shape.) 
A matrix consists of scalars that are arranged in a rectangle. For example, the matrix 

$$\left[\begin{array}{l l}{{-2}}&{{3}}\\ {{0}}&{{\pi^{2}}}\\ {{j}}&{{0}}\end{array}\right]$$
$$(1.3)$$
$$A={\left[\begin{array}{l l}{1}&{2}\\ {2}&{4}\end{array}\right]}$$
$$(1.4)$$

is a 3 x 2 matrix because it has 3 rows and 2 columns. The number of rows and columns in a matrix can be collectively referred to as the dimension of the matrix. 

For example, the dimension of the matrix in the preceding equation is 3 x 2. Note that a vector can be viewed as a degenerate matrix. For example, Equation (1.1) is a 1 x 3 matrix. A scalar can also be viewed as a degenerate matrix. For example, the scalar 6 is a 1 x 1 matrix. 

The rank of a matrix is defined as the number of linearly independent rows. This is also equal to the number of linearly independent columns. The rank of a matrix A is often indicated with the notation *p(A).* The rank of a matrix is always less than or equal to the number of rows, and it is also less than or equal to the number of columns. For example, the matrix 

$$(1.5)$$
$$(1.6)$$
$$(1.7)$$

has a rank of one because it has only one linearly independent row; the two rows are multiples of each other. It also has only one linearly independent column; the two columns are multiples of each other. On the other hand, the matrix 

$$A={\left[\begin{array}{l l}{1}&{3}\\ {2}&{4}\end{array}\right]}$$

has a rank of two because it has two linearly independent rows. That is, there are no nonzero scalars c1 and cz such that 

$$c_{1}\left[\begin{array}{l l}{{1}}&{{3}}\end{array}\right]+c_{2}\left[\begin{array}{l l}{{2}}&{{4}}\end{array}\right]=\left[\begin{array}{l l}{{0}}&{{0}}\end{array}\right]$$
$$c_{1}\left[\begin{array}{l}{{1}}\\ {{2}}\end{array}\right]+c_{2}\left[\begin{array}{l}{{3}}\\ {{4}}\end{array}\right]=\left[\begin{array}{l}{{0}}\\ {{0}}\end{array}\right]$$

so the two rows are linearly independent. It also has two linearly independent columns. That is, there are no nonzero scalars c1 and c2 such that so the two columns are linearly independent. A matrix whose elements are comprised entirely of zeros has a rank of zero. An n x m matrix whose rank is equal to min(n,m) is called full rank. The nullity of an n x m matrix A is equal to 
[m - P(41. 

The transpose of a matrix (or vector) can be taken by changing all the rows to columns, and all the columns to rows. The transpose of a matrix is indicated with a T superscript, as in AT.l For example, if A is the r x n matrix 

$$A={\left[\begin{array}{l l l}{A_{11}}&{\cdots}&{A_{1n}}\\ {\vdots}&{}&{\vdots}\\ {A_{r1}}&{\cdots}&{A_{r n}}\end{array}\right]}$$
$$(1.8)$$
$$A^{T}={\left[\begin{array}{l l l}{A_{11}}&{\cdots}&{A_{r1}}\\ {\vdots}&{}&{\vdots}\\ {A_{1n}}&{\cdots}&{A_{r n}}\end{array}\right]}$$

then AT is the n x r matrix Note that we use the notation A,, to indicate the scalar in the ith row and jth column of the matrix A. A symmetric matrix is one for which A = AT. 

The hermitian transpose of a matrix (or vector) is the complex conjugate of the transpose, and is indicated with an H superscript, as in AH. For example, if 

$$A={\left[\begin{array}{l l l}{1}&{2j}&{3-j}\\ {4j}&{5+j}&{1-3j}\end{array}\right]}$$
$$A={\left[\begin{array}{l l}{1}&{-4j}\\ {-2j}&{5-j}\\ {3+j}&{}\\ {1+3j}&{}\\ {-\mathbf{x}}&{}\end{array}\right]}$$

then 

$$(1.9)$$
$$(1.10)$$
$$(1.11)$$

A hermitian matrix is one for which A = AH. 

lMany papers or **books** indicate transpose with a prime, as in **A',** or with a lower case t, as in At. 

## 1.1.1 Matrix Algebra

Matrix addition and subtraction is simply defined as element-by-element addition and subtraction. For example, 

$$(1.12)$$
$${\left[\begin{array}{l l l}{1}&{2}&{3}\\ {3}&{2}&{1}\end{array}\right]}+{\left[\begin{array}{l l l}{0}&{4}&{1}\\ {1}&{-1}&{-2}\end{array}\right]}={\left[\begin{array}{l l l}{1}&{6}&{4}\\ {4}&{1}&{-1}\end{array}\right]}$$

The sum (A + B) and the difference (A - B) is defined only if the dimension of A 
is equal to the dimension of B. 

Suppose that A is an n x T matrix and B is an T x p matrix. Then the product of A *and* B is written as C = *AB.* Each element in the matrix product C is computed as 

$$C_{i j}=\sum_{k=1}^{r}A_{i k}B_{k j}\qquad\qquad i=1,\ldots,n\qquad\qquad j=1,\ldots,p$$

The matrix product AB is defined only if the number of columns in A is equal to the number of rows in B. It is important to note that matrix multiplication does not commute. In general, AB \# *BA.* 
Suppose we have an *n x* 1 vector x. We can compute the 1 x 1 product *xTx,* and the n x n product *xxT* as follows: 

$$x^{T}x=\left[\begin{array}{cccc}x_{1}&\cdots&x_{n}\end{array}\right]\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right]\tag{1.14}$$ $$=x_{1}^{2}+\cdots+x_{n}^{2}$$ $$xx^{T}=\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right]\left[\begin{array}{cccc}x_{1}&\cdots&x_{n}\end{array}\right]$$ $$=\left[\begin{array}{cccc}x_{1}^{2}&\cdots&x_{1}x_{n}\\ \vdots&\ddots&\vdots\\ x_{n}x_{1}&\cdots&x_{n}^{2}\end{array}\right]$$
$$(1.13)$$

Suppose that we have a p x n matrix H and an *n x n* matrix P. Then HT is a n x p matrix, and we can compute the p x p matrix product *HPHT.* 

(1.15) 
This matrix of sums can be written as the following sum of matrices: 

$$HPH^{T}=\left[\begin{array}{cccc}H_{11}P_{11}H_{11}&\cdots&H_{11}P_{11}H_{p1}\\ \vdots&\ddots&\vdots\\ H_{p1}P_{11}H_{11}&\cdots&H_{p1}P_{11}H_{p1}\end{array}\right]+\cdots+$$ $$\left[\begin{array}{cccc}H_{1n}P_{nn}H_{1n}&\cdots&H_{1n}P_{nn}H_{pn}\\ \vdots&\ddots&\vdots\\ H_{pn}P_{nn}H_{1n}&\cdots&H_{pn}P_{nn}H_{pn}\end{array}\right]$$ $$=H_{1}P_{11}H_{1}^{T}+\cdots+H_{n}P_{nn}H_{n}^{T}$$ $$=\sum_{j,k}H_{j}P_{jk}H_{k}^{T}\tag{1.16}$$

where we have used the notation that Hk is the kth column of H. 

Matrix division is not defined; we cannot divide a matrix by another matrix 
(unless, of course, the denominator matrix is a scalar). 

An identity matrix I is defined as a square matrix with ones on the diagonal and zeros everywhere else. For example, the 3 x 3 identity matrix is equal to 

$$I=\left[\begin{array}{ccc}1&0&0\\ 0&1&0\\ 0&0&1\end{array}\right]\tag{1.17}$$

The identity matrix has the property that AI = A for any matrix A, and IA = A 
(as long the dimensions of the identity matrices are compatible with those of **A).** 
The 1 x 1 identity matrix is equal to the scalar 1. 

The determinant of a matrix is defined inductively for square matrices. The determinant of a scalar (i.e., a 1 x 1 matrix) is equal to the scalar. Now consider an n x n matrix A. Use the notation **A(iJ)** to denote the matrix that is formed by deleting the ith row and jth column of A. The determinant of A is defined as 

$$|A|=\sum_{j=1}^{n}(-1)^{i+j}A_{i j}|A^{(i,j)}|$$

for any value of i E **[I,** *n].* This is called the Laplace expansion of A along its ith row. We see that the determinant of the n x n matrix A is defined in terms of the determinants of (n - 1) x (n - 1) matrices. Similarly, the determinants of 
(n - 1) x (n - 1) matrices are defined in terms of the determinants of (n - 2) x (n - 2) 
matrices. This continues until the determinants of 2 x 2 matrices are defined in terms of the determinants of 1 x 1 matrices, which are scalars. The determinant of A can also be defined as 

$$(1.18)$$
$$|A|=\sum_{i=1}^{n}(-1)^{i+j}A_{ij}|A^{(i,j)}|\tag{1.19}$$

for any value of j E [l, n]. This is called the Laplace expansion of A along its jth column. Interestingly, Equation (1.18) (for any value of i) and Equation **(1.19)** (for any value of j) both give identical results. From the definition of the determinant 

$$\begin{array}{r l}{\operatorname*{det}[A_{11}]}&{{}=}\\ {\operatorname*{det}{\left[\begin{array}{l l}{A_{11}}&{A_{12}}\\ {A_{21}}&{A_{22}}\end{array}\right]}}&{{}=}\\ {\operatorname*{det}{\left[\begin{array}{l l l}{A_{11}}&{A_{12}}&{A_{13}}\\ {A_{21}}&{A_{22}}&{A_{23}}\\ {A_{31}}&{A_{32}}&{A_{33}}\end{array}\right]}}&{{}=}\end{array}$$

we see that 

$$(1.20)$$

Some interesting properties of determinants are 

$$\begin{array}{l}{{A_{11}}}\\ {{A_{11}A_{22}-A_{12}A_{21}}}\\ {{\ }}\\ {{A_{11}(A_{22}A_{33}-A_{23}A_{32})-}}\\ {{\ }}\\ {{A_{12}(A_{21}A_{33}-A_{23}A_{31})+}}\\ {{A_{13}(A_{21}A_{32}-A_{22}A_{31})}}\end{array}\qquad\mathrm{(1)}$$
$$|A B|=|A||B|$$
$$(1.21)$$

$$(1.23)$$

assuming that A **and** B are square and have the same dimensions. Also, 

$$|A|=\prod_{i=1}^{n}\lambda_{i}$$
$$(1.22)$$

where A, (the eigenvalues of A) are defined below. 

The inverse of a matrix A is defined as the matrix **A-l** such that **AA-l** = 
A-lA = I. A matrix cannot have an inverse unless it is square. Some square matrices do not have an inverse. A square matrix that does not have an inverse is called singular or invertible. In the scalar case, the only number that does not have an inverse is the number 0. But in the matrix case, there are many matrices that are singular. A matrix that does have an inverse is called nonsingular or invertible. 

For example, notice that 

$${\left[\begin{array}{l l}{1}&{0}\\ {2}&{3}\end{array}\right]}\left[\begin{array}{l l}{1}&{0}\\ {-2/3}&{1/3}\end{array}\right]={\left[\begin{array}{l l}{1}&{0}\\ {0}&{1}\end{array}\right]}$$

Therefore, the two matrices on the left side of the equation are inverses of each other. The nonsingularity of an n x n matrix A can be stated in many equivalent ways, some of which are the following **[Hor85]:** 
0 A is nonsingular. 

0 A-l exists. 
0 The rank of A is equal to n. 

0 The rows of A are linearly independent. 

0 The columns of A are linearly independent. 

IAl \# 0. 

0 Az = b has a unique solution z for all b. 

0 0 is not an eigenvalue of A. 
The trace of a square matrix is defined as the sum of its diagonal elements: 

$$\operatorname{Tr}(A)=\sum_{i}A_{i i}$$
$$(1.24)$$
$$(1.25)$$

The trace of a matrix is defined only if the matrix is square. The trace of a 1 x 1 matrix is equal to the trace of a scalar, which is equal to the value of the scalar. 

One interesting property of the trace of a square matrix is 

$$\operatorname{Tr}(A)=\sum_{i}\lambda_{i}$$

That is, the trace of a square matrix is equal to the sum of its eigenvalues. 

Some interesting and useful characteristics of matrix products are the following: 

$$(AB)^{T}=B^{T}A^{T}$$ $$(AB)^{-1}=B^{-1}A^{-1}$$ $${\rm Tr}(AB)={\rm Tr}(BA)\tag{1.26}$$

This assumes that the inverses exist for the inverse equation, and that the matrix dimensions are compatible so that matrix multiplication is defined. The transpose of a matrix product is equal to the product of the transposes in the opposite order. The inverse of a matrix product is equal to the product of the inverses in the opposite order. The trace of a matrix product is independent of the order in which the matrices are multiplied. 

The two-norm of a column vector of real numbers, also called the Euclidean norm, is defined as follows: 

$$\begin{array}{r c l}{{||x||_{2}}}&{{=}}&{{\sqrt{x^{T}x}}}\\ {{}}&{{=}}&{{\sqrt{x_{1}^{2}+\cdots+x_{n}^{2}}}}\end{array}$$
$$x x^{T}={\left[\begin{array}{l l l}{x_{1}^{2}}&{\cdots}&{x_{1}x_{n}}\\ {\vdots}&{\ddots}&{\vdots}\\ {x_{n}x_{1}}&{\cdots}&{x_{n}^{2}}\end{array}\right]}$$
$$(1.27)$$

From (1.14) we see that 

$$(1.28)$$
$$\begin{array}{r c l}{\operatorname{Tr}(x x^{T})}&{{}=}&{x_{1}^{2}+\cdots+x_{n}^{2}}\\ {}&{{}=}&{\vert\vert x\vert\vert_{2}^{2}}\end{array}$$

Taking the trace of this matrix is 

$$(1.29)$$
$$(1.30)$$
$$A x=\lambda x$$

An n x n matrix A has n eigenvalues and n eigenvectors. The scalar X is an eigenvalue of A, and the n x 1 vector x is an eigenvector of A, if the following equation holds: 
AX = AX (1.30) 
The eigenvalues and eigenvectors of a matrix are collectively referred to as the eigendata of the matrix.2 An n x n matrix has exactly n eigenvalues, although 

2Eigendata have also been referred to by many other terms over the years, including characteristic roots, latent roots and vectors, and proper numbers and vectors [Fad59]. 
some may be repeated. This is like saying that an nth order polynomial equation has exactly n roots, although some may be repeated. From the above definitions of eigenvalues and eigenvectors we can see that 

$$\begin{array}{r c l}{{A x}}&{{=}}&{{\lambda x}}\\ {{A^{2}x}}&{{=}}&{{A\lambda}}\\ {{}}&{{=}}&{{\lambda(\lambda)}}\\ {{}}&{{=}}&{{\lambda(\lambda)}}\\ {{}}&{{=}}&{{\lambda^{2}x}}\end{array}$$
$$\lambda x$$ $$A\lambda x$$
$$\begin{array}{l}{{x=x}}\\ {{\lambda(A x)}}\\ {{\lambda(\lambda x)}}\\ {{\lambda^{2}x}}\end{array}$$
$$(1.31)$$
= *X(Ax)* 
= X(Xz) 
= X2x (1.31) 
So if A has eigendata (X,z), then A2 has eigendata (X2,z). It can be shown that A-l exists if and only if none of the eigenvalues of A are equal to 0. If A is symmetric then all of its eigenvalues are real numbers. 

A symmetric n x n matrix A can be characterized as either positive definite, positive semidefinite, negative definite, negative semidefinite, or indefinite. Matrix A is: 

0 Positive definite if *xTAx* > 0 for all nonzero n x 1 vectors z. This is equivalent to saying that all of the eigenvalues of A are positive real numbers. If A is positive definite, then **A-'** is also positive definite. 

0 Positive semidefinite if *zTAz* 2 0 for all n x 1 vectors z. This is equivalent to saying that all of the eigenvalues of A are nonnegative real numbers. Positive semidefinite matrices are sometimes called nonnegative definite. 

0 Negative definite if *zTAz* < 0 for all nonzero n x 1 vectors z. This is equivalent to saying that all of the eigenvalues of A are negative real numbers. If A is negative definite, then **A-'** is also negative definite. 

0 Negative semidefinite if *zTAz* 5 0 for all n x 1 vectors 2. This is equivalent to saying that all of the eigenvalues of A are nonpositive real numbers. Negative semidefinite matrices are sometimes called nonpositive definite. 

0 *Indefinite* if it does not fit into any of the above four categories. This is equivalent to saying that some of its eigenvalues are positive and some are negative. 
Some books generalize the idea of positive definiteness and negative definiteness to include nonsymmetric matrices. 

The weighted two-norm of an n x 1 vector x is defined as 

$$||x||_{Q}^{2}={\sqrt{x^{T}Q x}}$$
$$(1.32)$$
11.11; = mz **(1.32)** 
where Q is required to be an n x n positive definite matrix. The above norm is also called the Q-weighted two-norm of 2. A quantity of the form *xTQz* is called a quadratic in analogy to a quadratic term in a scalar equation. 

The singular values g of a matrix A are defined as 

$$\begin{array}{r c l}{{\sigma^{2}(A)}}&{{=}}&{{\lambda(A^{T}A)}}\\ {{}}&{{=}}&{{\lambda(A A^{T})}}\end{array}$$
$$(1.33)$$
= *X(AA~)* (1.33) 
If A is an n x m matrix, then it has min(n,m) singular values. AAT will have n eigenvalues, and *ATA* will have m eigenvalues. If n > m then AAT will have the same eigenvalues as *ATA* plus an additional (n - m) zeros. These additional zeros are not considered to be singular values of A, because A always has min(n, m) 
singular values. This knowledge can help reduce effort during the computation of singular values. For example, if A is a 13 x 3 matrix, then it is much easier to compute the eigenvalues of the 3 x 3 matrix *ATA* rather than the 13 x 13 matrix AAT. Either computation will result in the same three singular values. 

## 1.1.2 The Matrix Inversion Lemma

Suppose we have the partitioned matrix [ : E ] where A and D are invertible square matrices, and the B and C matrices may or may not be square. We define E and F matrices as follows: 
In this section, we will derive the matrix inversion lemma, which is a tool that we will use many times in this book. It is also a tool that is frequently useful in other areas of control, estimation theory, and signal processing. 

$$\begin{array}{r c l}{{E}}&{{=}}&{{D-C A^{-1}B}}\\ {{F}}&{{=}}&{{A-B D^{-1}C}}\end{array}$$
$$(1.34)$$
Assume that E is invertible. Then we can show that  =[: ;]  (1.35) 
$$1.35)$$

Now assume that F is invertible. Then we can show that 

the data $F$ is invertible. Then we can show that  $$\left[\begin{array}{cc}A&B\\ C&D\end{array}\right]\left[\begin{array}{cc}F^{-1}&-A^{-1}BE^{-1}\\ -D^{-1}CF^{-1}&E^{-1}\end{array}\right]$$ $$=\left[\begin{array}{cc}AF^{-1}-BD^{-1}CF^{-1}&-BE^{-1}+BE^{-1}\\ CF^{-1}-CF^{-1}&-CA^{-1}BE^{-1}+DE^{-1}\end{array}\right]$$ $$=\left[\begin{array}{cc}(A-BD^{-1}C)F^{-1}&0\\ 0&(D-CA^{-1}B)E^{-1}\end{array}\right]$$ $$=\left[\begin{array}{cc}I&0\\ 0&I\end{array}\right]$$
[ : E ] [ *-D-lCF-l* 

$$(1.36)$$
$$(1.37)$$
Equations **(1.35)** and **(1.36)** are two expressions for the inverse of [ : 1. Since these two expressions are inverses of the same matrix, they must be equal. We therefore conclude that the upper-left partitions of the matrices are equal, which gives 

$$F^{-1}=A^{-1}+A^{-1}B E^{-1}C A^{-1}$$

Now we can use the definition of F to obtain 

$$(A-BD^{-1}C)^{-1}=A^{-1}+A^{-1}B(D-CA^{-1}B)^{-1}CA^{-1}\tag{1.38}$$

This is called the matrix inversion lemma. It is also referred to by other terms, such as the Sherman-Morrison formula, Woodbury's identity, and the modified matrices formula. One of its earliest presentations ww in **1944** by William Duncan [Dun44], and similar identities were developed by Alston Householder [Hou53]. An account of its origins and variations (e.g., singular A) is given in [Hen81]. The matrix inversion lemma is often stated in slightly different but equivalent ways. For example, 

$$(A+B D^{-1}C)^{-1}=A^{-1}-A^{-1}B(D+C A^{-1}B)^{-1}C A^{-1}$$
$$(1.39)$$

The matrix inversion lemma can sometimes be used to reduce the computational effort of matrix inversion. For instance, suppose that A is n x n, B is n xp, C is p x n, D is *p x p,* and p < n. Suppose further that we already know *A-l,* and we want to add some quantity to A and then compute the new inverse. A straightforward computation of the new inverse would be an n x n inversion. But if the new matrix to invert can be written in the form of the left side of Equation **(1.39),** then we can use the right side of Equation **(1.39)** to compute the new inverse, and the right side of Equation **(1.39)** requires a *p x p* inversion instead of an n x n inversion (since we already know the inverse of the old A matrix). 

## Ex Amp Lei.^

At your investment firm, you notice that in January the New **York** Stock Exchange index decreased by 2%, the American Stock Exchange index increased by **1%,** and the NASDAQ stock exchange index increased by 2%. As a result, investors increased their deposits by **1%.** The next month, the stock exchange indices changed by -4%, 3%, and **2%,** respectively, and investor deposits increased by 2%. The following month, the stock exchange indices changed by -5%, **1%,** and 5%, respectively, and investor deposits increased by 2%. You suspect that investment changes y can be modeled as y = g1q + ~2x2 + *~3x3,* 
where the 2% variables are the stock exchange index changes, and the gi are unknown constants. In order to determine the gi constants you need to invert the matrix 
-2 1 2 

$$A={\left[\begin{array}{l}{-2}\\ {-4}\\ {-5}\end{array}\right]}$$
-5 1 5 
$$\begin{array}{r r}{1}&{2}\\ {3}&{2}\\ {1}&{5}\end{array}\tag{1.40}$$

The result is 

$$\begin{array}{c}{{\frac{1}{6}\left[\begin{array}{c c c}{{13}}&{{-3}}&{{-4}}\\ {{10}}&{{0}}&{{-4}}\\ {{11}}&{{-3}}&{{-2}}\end{array}\right]}}\\ {{A^{-1}\left[\begin{array}{c}{{1}}\\ {{2}}\\ {{2}}\end{array}\right]}}\\ {{\frac{1}{6}\left[\begin{array}{c}{{-1}}\\ {{2}}\\ {{1}}\end{array}\right]}}\end{array}$$

$$(1.41)$$
A-' = 1 [ 10 0 **-41** 
$$\begin{array}{r l}{A^{-1}}&{{}=}\\ {}&{}\\ {g}&{{}=}\\ {}&{}\\ {}&{}\\ {}&{}\\ {}&{}\\ {}&{}\end{array}$$
-11 (1.41) 
This allows you to use stock exchange index changes to predict investment changes in the following month, which allows you to better schedule personnel and computer resources. However, soon afterward you find out that the NASDAQ change in the third month was actually 6% rather than **5%.** This means that in order to find the gi constants you need to invert the matrix 

-2 1 2 
$$A^{\prime}={\left[\begin{array}{l}{-2}\\ {-4}\\ {-5}\end{array}\right]}$$
-5 1 6 
$$\begin{array}{l l}{{1}}&{{2}}\\ {{3}}&{{2}}\\ {{1}}&{{6}}\end{array}\Biggr]\qquad\qquad\qquad\qquad(1.42)$$
You are tired of inverting matrices and so you wonder if you can somehow use the inverse of A (which you have already calculated) to find the inverse of *A'.* 
Remembering the matrix inversion lemma, you realize that A' = *A+BD-lC,* 
where 

$$\begin{array}{r c l}{{B}}&{{=}}&{{\left[\begin{array}{l l l}{{0}}&{{0}}&{{1}}\end{array}\right]^{T}}}\\ {{C}}&{{=}}&{{\left[\begin{array}{l l l}{{0}}&{{0}}&{{1}}\end{array}\right]}}\\ {{D}}&{{=}}&{{1}}\end{array}$$

D=1 **(1.43)** 
You therefore use the matrix inversion lemma to compute 

$\begin{array}{lcl}\mbox{\rm{\bfseries}}&\mbox{\rm{\bfseries}}\\ \mbox{\rm{\bf(}}A^{\prime}\mbox{\rm{\bf)}}^{-1}&=&(A+BD^{-1}C)^{-1}\\ &=&A^{-1}-A^{-1}B(D+CA^{-1}B)^{-1}CA^{-1}\end{array}$  . 
The (D + *CA-lB)* term that needs to be inverted in the above equation is a scalar, so its inversion is simple. This gives 

$\qquad\quad\;\;\;$ -  $\left[\begin{array}{ccc}4.00&1.00&-1.00\\ 3.50&-0.50&-1.00\\ 2.75&-0.75&-0.50\end{array}\right]$  $(A')^{-1}\left[\begin{array}{l}1\\ 2\\ 2\end{array}\right]$  $\left[\begin{array}{l}0\\ 0.5\\ 0.25\end{array}\right]$  . 
(A')-' = **3.50** *-0.50* -1.00 
$$(1.43)$$
$$(1.44)$$
$$(1.45)$$
$$\begin{array}{r c l}{{g}}&{{=}}&{{(1)}}\end{array}$$
g = *(A')-'* [ i] 
$$\mathbf{\mu}=\mathbf{\mu}\left|\mathbf{\mu}_{\mathrm{\scriptsize{\boldmath~\mu~}}}\right|$$
- [ i.5 ] (1.45) 
In this example, the use of the matrix inversion lemma is not really necessary because A' (the new matrix to invert) is only 3 x 3. However, with larger matrices, such as 1000 x 1000 matrices, the computational savings that is realized by using the matrix inversion lemma could be significant. 

vvv Now suppose that *A, B,* C, and D are matrices, with A and D being square. 

Then it can be seen that 

$\left[\begin{array}{cc}I&0\\ -CA^{-1}&I\end{array}\right]\left[\begin{array}{cc}A&B\\ C&D\end{array}\right]\left[\begin{array}{cc}I&-A^{-1}B\\ 0&I\end{array}\right]=\left[\begin{array}{cc}A&0\\ 0&D-CA^{-1}B\end{array}\right]$
$${\begin{array}{l l}{A}&{B}\\ {C}&{D}\end{array}}\Big|=|A||D-C A^{-1}B|$$
$$(1.46)$$
$$(1.47)$$
Similarly, it can be shown that 

$A$$B$$C$$D$$\left|\right.=\left|D||A-BD^{-1}C\right|$ (1.48)
These formulas are called product rules for determinants. They were first given by the Russian-born mathematician Issai Schur in a German paper [Schl7] that was reprinted in English in [Sch86]. 

## 1.1.3 **Matrix Calculus**

In our first calculus course, we learned the mathematics of derivatives and integrals and how to apply those concepts to scalars. We can also apply the mathematics of calculus to vectors and matrices. Some aspects of matrix calculus are identical to scalar calculus, but some scalar calculus concepts need to be extended in order to derive formulas for matrix calculus. 

As intuition would lead us to believe, the time derivative of a matrix is simply equal to the matrix of the time derivatives of the individual matrix elements. Also, the integral of a matrix is equal to the matrix of the integrals of the individual matrix elements. In other words, assuming that A is an m x n matrix, we have 

$$\dot{A}(t)=\left[\begin{array}{ccc}\dot{A}_{11}(t)&\cdots&\dot{A}_{1n}(t)\\ \vdots&\ddots&\vdots\\ \dot{A}_{n1}(t)&\cdots&\dot{A}_{nn}(t)\end{array}\right]$$ $$\int A(t)\,dt=\left[\begin{array}{ccc}\int A_{11}(t)\,dt&\cdots&\int A_{1n}(t)\,dt\\ \vdots&\ddots&\vdots\\ \int A_{n1}(t)\,dt&\cdots&\int A_{nn}(t)\,dt\end{array}\right]\tag{1.49}$$
$$(1.50)$$
$$(1.51)$$

Next we will compute the time derivative of the inverse of a matrix. Suppose that matrix **A(t),** which we will denote as A, has elements that are functions of time. 

We know that **AA-l** = I; that is, **AA-l** 6s a constant matrix and therefore has a time derivative of zero. But the time derivative of **AA-l** can be computed as 

$${\frac{d}{d t}}(A A^{-1})=\dot{A}A^{-1}+A{\frac{d}{d t}}(A^{-1})$$

Since this is zero, we can solve for **d(A-')/dt** as 

$${\frac{d}{d t}}(A^{-1})=-A^{-1}\dot{A}A^{-1}$$
Note that for the special case of a scalar A, this reduces to the familiar equation 
$$\begin{array}{r c l}{{\frac{d}{d t}(1/A)}}&{{=}}&{{\frac{\partial(1/A)}{\partial A}\frac{d A}{d t}}}\\ {{}}&{{=}}&{{-\dot{A}/A^{2}}}\end{array}$$
$$(1.52)$$
$$(1.53)$$
-- 
Now suppose that x is an n x 1 vector and f **(x)** is a scalar function of the elements 

$${\frac{\partial f}{\partial x}}={\left[\begin{array}{l l l}{\partial f/\partial x_{1}}&{\cdots}&{\partial f/\partial x_{n}}\end{array}\right]}$$
of 2. Then - = [ **af/axl** . . . af/axn ] 
Even though x is a column vector, *df/dx* is a row vector. The converse is also true - if x is a row vector, then *df/dx* is a column vector. Note that some authors define this the other way around. That is, they say that if x is a column vector then d f */dz* is also a column vector. There is no accepted convention for the definition of the partial derivative of a scalar with respect to a vector. It does not really matter which definition we use as long as we are consistent. In this book, we will use the convention described by Equation **(1.53).** 
Now suppose that A is an m x n matrix and *f(A)* is a scalar. Then the partial derivative of a scalar with respect to a matrix can be computed as follows: 

$$\frac{\partial f}{\partial A}=\left[\begin{array}{cccc}\partial f/\partial A_{11}&\cdots&\partial f/\partial A_{1n}\\ \vdots&\ddots&\vdots\\ \partial f/\partial A_{m1}&\cdots&\partial f/\partial A_{mn}\end{array}\right]\tag{1.54}$$

With these definitions we can compute the partial derivative of the dot product of two vectors. Suppose x and y are n-element column vectors. Then 

$$x^{T}y=x_{1}y_{1}+\cdots+x_{n}y_{n}$$ $$\frac{\partial(x^{T}y)}{\partial x}=\left[\begin{array}{cccc}\partial(x^{T}y)/\partial x_{1}&\cdots&\partial(x^{T}y)/\partial x_{n}\end{array}\right]\tag{1.55}$$ $$=\left[\begin{array}{cccc}y_{1}&\cdots&y_{n}\end{array}\right]$$ $$=y^{T}$$
$${\frac{\partial(x^{T}y)}{\partial y}}=x^{T}$$

Likewise, we can obtain 

$$(1.56)$$

Now we will compute the partial derivative of a quadratic with respect to a vector. First write the quadratic as follows: 

the quadratic as follows.  $$x^{T}Ax=\left[\begin{array}{ccc}x_{1}&\cdots&x_{n}\end{array}\right]\left[\begin{array}{ccc}A_{11}&\cdots&A_{1n}\\ \vdots&\ddots&\vdots\\ A_{n1}&\cdots&A_{nn}\end{array}\right]\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right]$$ $$=\left[\begin{array}{ccc}\sum_{1}x_{1}A_{i1}&\cdots&\sum_{1}x_{i}A_{in}\end{array}\right]\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right]$$ $$=\sum_{i,j}x_{i}x_{j}A_{ij}\tag{1.57}$$

Now take the partial derivative of the quadratic as follows: 
If A is symmetric, as it often is in quadratic expressions, then A = AT and the above expression simplifies to 

$$\partial(x^{T}Ax)=2x^{T}A\qquad\qquad\mbox{if$A=A^{T}$}\tag{1.59}$$
$$\left[\begin{array}{c c c}{{\partial g_{1}/\partial x_{1}}}&{{\cdots}}&{{\partial g_{1}/\partial x_{n}}}\\ {{\vdots}}&{{}}&{{\vdots}}\\ {{\partial g_{m}/\partial x_{1}}}&{{\cdots}}&{{\partial g_{m}\partial x_{n}}}\end{array}\right]$$
$${\frac{\partial g}{\partial x}}=$$

Next we define the partial derivative of a vector with respect to another vector. 

Next we define the partial derivative of a vector with a  Suppose $g(x)=\left[\begin{array}{c}g_{1}(x)\\ \vdots\\ g_{m}(x)\end{array}\right]$ and $x=\left[\begin{array}{c}x_{1}\\ \vdots\\ x_{n}\end{array}\right].$ Then
$$(1.60)$$
If either g(x) or x is transposed, then the partial derivative is also transposed. 

$$\begin{array}{lcl}\partial g^{T}&=&\left(\frac{\partial g}{\partial x}\right)^{T}\\ \partial g&=&\left(\frac{\partial g}{\partial x}\right)^{T}\\ \partial g^{T}&=&\frac{\partial g}{\partial x}\end{array}\tag{1.61}$$

With these definitions, the following important equalities can be derived. Suppose A is an m x n matrix and x is an n x 1 vector. Then 

$$\begin{array}{l}\partial(Ax)\\ \partial x\\ \partial(x^{T}A)\\ \partial x\end{array}=\begin{array}{l}A\\ \partial(x^{T}A)\\ \partial x\end{array}=\begin{array}{l}A\\ \partial(x^{T}A)\\ \partial x\end{array}\tag{1.62}$$
$$\mathrm{Tr}(A B A^{T})=\sum_{i,j,k}A_{i k}B_{k j}A_{i j}$$

Now we suppose that A is an m x n matrix, B is an n x n matrix, and we want to compute the partial derivative of *Tr(ABAT)* with respect to A. First compute ABA~ as follows: 

$$(1.64)$$
partial derivative with respect to $\Lambda$ can be computed as  $$\frac{\partial\text{Tr}(ABA^{T})}{\partial A}=\left[\begin{array}{cccc}\partial\text{Tr}(ABA^{T})/\partial A_{11}&\cdots&\partial\text{Tr}(ABA^{T})/\partial A_{1n}\\ \vdots&&\vdots\\ \partial\text{Tr}(ABA^{T})/\partial A_{m1}&\cdots&\partial\text{Tr}(ABA^{T})/\partial A_{mn}\end{array}\right]$$ $$=\left[\begin{array}{cccc}\sum_{j}A_{1j}B_{1j}+\sum_{k}A_{1k}B_{k1}&\cdots&\sum_{j}A_{1j}B_{nj}+\sum_{k}A_{1k}B_{kn}\\ \vdots&&\vdots\\ \sum_{j}A_{mj}B
$$(1.65)$$

If B is symmetric, as it often is in partial derivatives of the form above, then this can be simplified to 

$$\partial{\rm Tr}(ABA^{T})=2AB\qquad{\rm if}\ B=B^{T}\tag{1.66}$$

A number of additional interesting results related to matrix calculus can be found in jSke98, Appendix B]. 

## 1.1.4 **The History Of Matrices**

This section is a brief diversion to present some of the history of matrix theory. 

Much of the information in this section is taken from [OCo96]. 

The use of matrices can be found as far back as the fourth century BC. We see in ancient clay tablets that the Babylonians studied problems that led to simultaneous linear equations. For example, a tablet dating from about 300 BC contains the following problem: "There are two fields whose total area is 1800 units. One produces grain at the rate of 2/3 of a bushel per unit while the other produces grain at the rate of 1/2 a bushel per unit. If the total yield is 1100 bushels, what is the size of each field?" 
Later, the Chinese came even closer to the use of matrices. In [She991 (originally published between 200 BC and 100 AD) we see the following problem: "There are three types of corn, of which three bundles of the first, two of the second, and one of the third make 39 measures. Two of the first, three of the second, and one of the third make 34 measures. And one of the first, two of the second and three of the third make 26 measures. How many measures of corn are contained in one bundle of each type?" At that point, the ancient Chinese essentially use Gaussian elimination (which was not well known until the 19th century) to solve the problem. 

In spite of this very early beginning, it was not until the end of the 17th century that serious investigation of matrix algebra began. In 1683, the Japanese mathematician Takakazu Seki Kowa wrote a book called "Method of Solving the Dissimulated Problems." This book gives general methods for calculating determinants and presents examples for matrices as large as 5 x 5. Coincidentally, in the same year (1683) Gottfried Leibniz in Europe also first used determinants to solve systems of linear equations. Leibniz also discovered that a determinant could be expanded using any of the matrix columns. 

In the middle of the 1700s, Colin Maclaurin and Gabriel Cramer published some major contributions to matrix theory. After that point, work on matrices became rather regular, with significant contributions by Etienne Bezout, Alexandre Vandermonde, Pierre Laplace, Joseph Lagrange, and Carl Gauss. The term "determinant" was first used in the modern sense by Augustin Cauchy in 1812 (although the word was used earlier by Gauss in a different sense). Cauchy also discovered matrix eigenvalues and diagonalization, and introduced the idea of similar matrices. He was the first to prove that every real symmetric matrix is diagonalizable. 

James Sylvester (in 1850) was the first to use the term "matrix." Sylvester moved to England in 1851 to became a lawyer and met Arthur Cayley, a fellow lawyer who was also interested in mathematics. Cayley saw the importance of the idea of matrices and in 1853 he invented matrix inversion. Cayley also proved that 2 x 2 and 3 x 3 matrices satisfy their own characteristic equations. The fact that a matrix satisfies its own characteristic equation is now called the Cayley-Hamilton theorem (see Problem 1.5). The theorem has William Hamilton's name associated with it because he proved the theorem for 4 x 4 matrices during the course of his work on quaternions. 

Camille Jordan invented the Jordan canonical form of a matrix in 1870. Georg Frobenius proved in 1878 that all matrices satisfy their own characteristic equation 
(the Cayley Hamilton theorem). He also introduced the definition of the rank of a matrix. The nullity of a square matrix was defined by Sylvester in 1884. Karl Weierstrass's and Leopold Kronecker's publications in 1903 were instrumental in establishing matrix theory as an important branch of mathematics. Leon Mirsky's book in 1955 [MirSO] helped solidify matrix theory as a fundamentally important topic in university mathematics. 

## 1.2 Linear Systems

Many processes in our world can be described by statespace systems. These include processes in engineering, economics, physics, chemistry, biology, and many other areas. If we can derive a mathematical model for a process, then we can use the tools of mathematics to control the process and obtain information about the process. 

This is why statespace systems are so important to engineers. If we know the state of a system at the present time, and we know all of the present and future inputs, then we can deduce the values of all future outputs of the system. 

Statespace models can be generally divided into linear models and nonlinear models. Although most real processes are nonlinear, the mathematical tools that are available for estimation and control are much more accessible and well understood for linear systems. That is why nonlinear systems are often approximated as linear systems. That way we can use the tools that have been developed for linear systems to derive estimation or control algorithms. 

$$(1.67)$$

A continuous-time, deterministic linear system can be described by the equations 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+B u}}\\ {{y}}&{{=}}&{{C x}}\end{array}$$
y = cx (1.67) 
where x is the state vector, u is the control vector, and y is the output vector. 

Matrices *A, B,* and C are appropriately dimensioned matrices. The A matrix is often called the system matrix, B is often called the input matrix, and C is often called the output matrix. In general, A, B, and C can be time-varying matrices and the system will still be linear. If A, B, and C are constant then the solution to Equation (1.67) is given by 

$$\begin{array}{r c l}{{x(t)}}&{{=}}&{{e^{A(t-t_{0})}x(t_{0})+\int_{t_{0}}^{t}e^{A(t-\tau)}B u(\tau)\,d\tau}}\\ {{y(t)}}&{{=}}&{{C x(t)}}\end{array}$$
$$(1.68)$$
$$(1.69)$$
$$(1.70)$$

where to is the initial time of the system and is often taken to be 0. This is easy to verify when all of the quantities in Equation (1.67) are scalar, but it happens to be true in the vector case also. Note that in the zero input case, *x(t)* is given as 

$$x(t)=e^{A(t-t_{0})}x(t_{0}),\quad\mathrm{~zero~input~case}$$
x(t) = *eA(t-to) x(to),* zero input case (1.69) 
For this reason, *eAt* is called the state-transition matrix of the ~ystem.~ It is the matrix that describes how the state changes from its initial condition in the absence of external inputs. We can evaluate the above equation at t = to to see that 

$$e^{A0}=I$$
eAO = I (1.70) 
in analogy with the scalar exponential of zero. 

As stated above, even if x is an n-element vector, then Equation (1.68) still describes the solution of Equation (1.67). However, a fundamental question arises in this case: How can we take the exponential of the matrix A in Equation (1.68)? What does it mean to raise the scalar e to the power of a matrix? There are many different ways to compute this quantity [Mo103]. Three of the most useful are the following: 

$$e^{At}=\sum_{j=0}^{\infty}\frac{(At)^{j}}{j!}\tag{1.71}$$ $$={\cal L}^{-1}[(sI-A)^{-1}]$$ $$=Qe^{At}Q^{-1}.$$
The first expression above is the definition of *eAt,* and is analogous to the definition 
of the exponential of a scalar. This definition shows that A must be square in 
order for eAt to exist. From Equation (1.67), we see that a system matrix is always 
square. The definition of eAt can also be used to derive the following properties. 

$$(1.72)$$
$$\begin{array}{r c l}{{\frac{d}{d t}e^{A t}}}&{{=}}&{{A e^{A t}}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{e^{A t}A}}\end{array}$$

3The MATLAB function EXPM computes the matrix exponential. Note that the MATLAB 
function EXP computes the element-by-element exponential of a matrix, which is generally not the same as the matrix exponential. 

In general, matrices do not commute under multiplication but, interestingly, a matrix always commutes with its exponential. 

The first expression in Equation (1.71) is not usually practical for computational purposes since it is an infinite sum (although the latter terms in the sum often decrease rapidly in magnitude, and may even become zero). The second expression in Equation **(1.71)** uses the inverse Laplace transform to compute *eAt.* In the third expression of Equation (1.71), Q is a matrix whose columns comprise the eigenvectors of A, and A is the Jordan form4 of A. Note that Q and A are well defined for any square matrix A, so the matrix exponential eAt exists for all square matrices A and all finite t. The matrix A is often diagonal, in which case **eat** is easy to compute: 

$$(1.73)$$

This can be computed from the definition of *eAt* in Equation (1.71). Even if the Jordan form matrix A is not diagonal, *eAt* is easy to compute [Bay99, Che99, Kai801. 

We can also note from the third expression in Equation (1.71) that 

$$\left[e^{At}\right]^{-1}=e^{-At}\tag{1.74}$$ $$=Qe^{-At}Q^{-1}$$

(Recall that A and -A have the same eigenvectors, and their eigenvalues are negatives of each other. *See* Problem 1.10.) We see from this that eAt is always invertible. This is analogous to the scalar situation in which the exponential of a scalar is always nonzero. 

Another interesting fact about the matrix exponential is that all of the individual elements of the matrix exponential eA are nonnegative if and only if all of the individual elements of A are nonnegative [Be160, Be1801. 

As an example of a linear system, suppose that we are controlling the angular acceleration of a motor (for example, with some applied voltage across the motor windings). The derivative of the position is the velocity. A simplified motor model can then be written as 41n fact, Equation **(1.71)** can be **used** to define the Jordan form of a matrix. That is, if *eAt* can be written as shown in Equation **(1.71),** where Q is a matrix whose columns comprise the eigenvectors of A, then A is the Jordan form of A. More discussion about Jordan **forms** and their computation can be found in most linear systems books [Kai80, Bay99, Che991. 

$$(1.75)$$
$$\begin{array}{r c l}{{\dot{\theta}}}&{{=}}&{{\omega}}\\ {{\dot{\omega}}}&{{=}}&{{u+w_{1}}}\end{array}$$
w = u+w1 **(1.75)** 
The scalar w1 is the acceleration noise and could consist of such factors as uncertainty in the applied acceleration, motor shaft eccentricity, and load disturbances. If our measurement consists of the angular position of the motor then a state space description of this system can be written as 

$$\begin{array}{l}\dot{\theta}\\ \dot{\omega}\end{array}\right]=\left[\begin{array}{cc}0&1\\ 0&0\end{array}\right]\left[\begin{array}{c}\theta\\ \omega\end{array}\right]+\left[\begin{array}{c}0\\ 1\end{array}\right]u+\left[\begin{array}{c}0\\ w_{1}\end{array}\right]$$ $$y=\left[\begin{array}{cc}1&0\end{array}\right]x+v\tag{1.76}$$

The scalar w consists of measurement noise. Comparing with Equation **(1.67),** 
we see that the state vector z is a 2 x 1 vector containing the scalars 13 and w. 

vvv 

In this example, we will use the three expressions in Equation **(1.71)** to compute the state-transition matrix of the system described in Example **1.2.** From the first expression in Equation **(1.71)** we obtain 

$$e^{At}=\sum_{j=0}^{\infty}\frac{(At)^{2}}{j!}\tag{1.77}$$ $$=(At)^{0}+(At)^{1}+\frac{(At)^{2}}{2!}+\frac{(At)^{3}}{3!}+\cdots$$ $$=I+At$$

where the last equality comes from the fact that Ak = 0 when k > 1 for the A matrix given in Example 1.2. We therefore obtain 

$\begin{array}{ccc}e^{At}&=&\left[\begin{array}{c}1\\ 0\end{array}\right]\\ &=&\left[\begin{array}{c}1\\ 0\end{array}\right]\end{array}$  . 
10 
= [o **1]+[:** ;] 
= [: E] 
From the second expression in Equation **(1.71)** we obtain 
$$(1.78)$$
$$e^{At}={\mathcal{L}}^{-1}[(sI-A)^{-1}]$$ $$={\mathcal{L}}^{-1}\left(\left[\begin{array}{cc}s&-1\\ 0&s\end{array}\right]^{-1}\right)$$ $$={\mathcal{L}}^{-1}\left[\begin{array}{cc}1/s&1/s^{2}\\ 0&1/s\end{array}\right]$$ $$=\left[\begin{array}{cc}1&t\\ 0&1\end{array}\right]$$
$$(1.79)$$
In order to use the third expression in Equation (1.71) we first need to obtain the eigendata (i.e., the eigenvalues and eigenvectors) of the A matrix. These are found as 

$$(1.80)$$

This shows that 

$$\begin{array}{r c l}{{\lambda(A)}}&{{=}}&{{\{0,0\}}}\\ {{v(A)}}&{{=}}&{{\left\{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right],\left[\begin{array}{l}{{0}}\\ {{1}}\end{array}\right]\right\}}}\end{array}$$
$$\begin{array}{r l}{{\hat{A}}}&{{}=}\\ {\ }&{}\\ {Q}&{{}=}\end{array}$$
$$\left[\begin{array}{l l}{0}&{1}\\ {0}&{0}\end{array}\right]$$ $$\left[\begin{array}{l l}{1}&{0}\\ {0}&{1}\end{array}\right]$$
$$(1.81)$$

Note that in this simple example A is already in Jordan form, so A = A and Q = I. The third expression in Equation (1.71) therefore gives 

$$Qe^{\hat{A}t}Q^{-1}$$ $$\left[\begin{array}{cc}1&0\\ 0&1\end{array}\right]\left[\begin{array}{cc}1&t\\ 0&1\end{array}\right]\left[\begin{array}{cc}1&0\\ 0&1\end{array}\right]^{-1}$$ $$\left[\begin{array}{cc}1&t\\ 0&1\end{array}\right]\tag{1.82}$$
$$\begin{array}{r l}{e^{A t}}&{{}=}\\ {}&{{}}\\ {}&{{}=}\\ {}&{{}}\\ {}&{{}=}\end{array}$$

vvv 

## 1.3 **Nonlinear Systems**

The discussion of linear systems in the preceding section is a bit optimistic, because in reality linear systems do not exist. Real systems always have some nonlinearities. Even a simple resistor is ultimately nonlinear if we apply a large enough voltage across it. However, we often model a resistor with the simple linear equation V = IR because this equation accurately describes the operation of the resistor over a wide operating range. So even though linear systems do not exist in the real world, linear systems theory is still a valuable tool for dealing with nonlinear systems. 

The general form of a continuous-time nonlinear system can be written as 

$$\begin{array}{lcl}\dot{t}&=&f(x,u,w)\\ y&=&h(x,v)\end{array}\tag{1.83}$$

where *f(.)* and h(.) are arbitrary vector-valued functions. We use w to indicate process noise, and w to indicate measurement noise. If *f(.)* and *h(.)* are explicit functions of t then the system is time-varying. Otherwise, the system is timeinvariant. If f (2, u, w) = As + Bu + w, and **h(s, v)** = *Ha:* + w, then the system is linear [compare with Equation (1.67)]. Otherwise, the system is nonlinear. 

In order to apply tools from linear systems theory to nonlinear systems, we need to linearize the nonlinear system. In other words, we need to find a linear system that is approximately equal to the nonlinear system. To see how this is done, let us start with a nonlinear vector function f(.) of a scalar x. We expand f(x) in a Taylor series around some nominal operating point (also called a linearization point) x = x, defining x = x - x:

$$f(x)=f(\bar{x})+\left.{\frac{\partial f}{\partial x}}\right|_{\bar{x}}\tilde{x}+{\frac{1}{2!}}\left.{\frac{\partial^{2}f}{\partial x^{2}}}\right|_{\bar{x}}\tilde{x}^{2}+{\frac{1}{3!}}\left.{\frac{\partial^{3}f}{\partial x^{3}}}\right|_{\bar{x}}\tilde{x}^{3}+\cdots$$
$$(1.84)$$

Now suppose that x is a 2×1 vector. This implies that f(x) is a nonlinear function of two independent variables x1 and x2. The Taylor series expansion of f(x) becomes

$$\begin{array}{r l}{f(x)}&{{}=}\\ {\end{array}$$
af af x1 + f(x) + x2 + dx1 dx2 t 82 f l  82  દર્ x 2 + 2 x1x2 + 2!  მx? dx1x2 z 88 f 83 f  ガ¤2 + 3 ಟ್ಟ  £3 + 3 x1x2 dx1x2 3!  විx3 ax 2x2  t 3
(1.85)  $\left)+\cdot\cdot\cdot\right.$  . 
This can be written more compactly as

$$f(x)\quad=\quad$$
$$f(\tilde{x})+\left.\left(\tilde{x}_{1}\frac{\partial}{\partial x_{1}}+\tilde{x}_{2}\frac{\partial}{\partial x_{2}}\right)f\right|_{\tilde{x}}+\left.\frac{1}{2!}\left(\tilde{x}_{1}\frac{\partial}{\partial x_{1}}+\tilde{x}_{2}\frac{\partial}{\partial x_{2}}\right)^{2}f\right|_{\tilde{x}}$$  $$\frac{1}{3!}\left(\tilde{x}_{1}\frac{\partial}{\partial x_{1}}+\tilde{x}_{2}\frac{\partial}{\partial x_{2}}\right)^{3}f\right|_{\tilde{x}}+\cdots$$
$$\left|{\begin{array}{l}{+}\\ {x}\end{array}}\right.$$  $$(1.86)$$

Extending this to the general case in which x is an n x 1 vector, we see that any continuous vector-valued function f (x) can be expanded in a Taylor series as

$$f(x)=f(\bar{x})+\left(\bar{x}_{1}\frac{\partial}{\partial x_{1}}+\cdots+\bar{x}_{2}\frac{\partial}{\partial x_{n}}\right)f\bigg{|}_{\bar{x}}+$$ $$\frac{1}{2!}\left(\bar{x}_{1}\frac{\partial}{\partial x_{1}}+\cdots+\bar{x}_{n}\frac{\partial}{\partial x_{n}}\right)^{2}f\bigg{|}_{\bar{x}}+$$ $$\frac{1}{3!}\left(\bar{x}_{1}\frac{\partial}{\partial x_{1}}+\cdots+\bar{x}_{n}\frac{\partial}{\partial x_{n}}\right)^{3}f\bigg{|}_{\bar{x}}+\cdots\tag{1.87}$$

Now we define the operation Dif as

$$D_{\tilde{\bf z}}^{k}f=\left.\left(\sum_{i=1}^{n}\tilde{x}_{i}\frac{\partial}{\partial x_{i}}\right)^{k}f(x)\right|_{\bf z}$$
$$(1.88)$$

Using this definition we write the Taylor series expansion of f(x) as

$$f(x)=f(\bar{x})+D_{\bar{x}}f+{\frac{1}{2!}}D_{\bar{z}}^{2}f+{\frac{1}{3!}}D_{\bar{x}}^{3}f+\cdots$$
$$(1.89)$$

If the nonlinear function f(x) is "sufficiently smooth," then high-order derivatives of f(x) should be "somewhat small." Also, if f(x) is expanded around a point such that x is "close" to 2, then 4 will be "small" and the higher powers of 4 in Equ& 
tion (1.89) will be "small." Finally, the higher-order derivatives in the Taylor series expansion of Equation (1.89) are divided by increasingly large factorials, which further diminishes the magnitude of the higher-order terms in Equation (1.89). This justifies the approximation 

$$f(x)$$
$$\approx f(\bar{x})+D_{\bar{x}}f\tag{1.90}$$ $$\approx f(\bar{x})+\left.\frac{\partial f}{\partial x}\right|_{\bar{x}}\bar{x}$$ $$\approx f(\bar{x})+A\bar{x}$$
$$(1.91)$$

where A is the matrix defined by the above equation. 

Returning to our nonlinear system equations in Equation (1.83), we can expand the nonlinear system equation *f(x,* u, w) around the nominal operating point 
(2,0, a). We then obtain a linear system approximation as follows. 

$$\dot{x}=f(x,u,w)\tag{1}$$ $$\approx f(\bar{x},\bar{u},\bar{w})+\left.\frac{\partial f}{\partial x}\right|_{0}(x-\bar{x})+\left.\frac{\partial f}{\partial u}\right|_{0}(u-\bar{u})+\left.\frac{\partial f}{\partial w}\right|_{0}(w-\bar{w})$$ $$=\dot{\bar{x}}+A\bar{x}+B\bar{u}+L\bar{w}$$

where the 0 subscript means that the function is evaluated at the nominal point 
(2, *ii,* a), and A, B, and L are defined by the above equations. Subtracting h from both sides of Equation (1.91) gives 

$${\dot{\bar{x}}}=A{\tilde{x}}+B{\tilde{u}}+L{\tilde{w}}$$
$$(1.92)$$

i = AZ + ~ii + LG (1.92) 
Since w is noise, we will set *tij* = 0 so that tC = w and we obtain 

$$(1.93)$$

i = AZ + ~ii + LW (1.93) 
We *see* that we have a linear equation for i in terms of 2, *12,* and w. We have a linear equation for the deviations of the state and control from their nominal values. As long as the deviations remain small, the linearization will be accurate and the linear equation will accurately describe deviations of x from its nominal value 2. 

In a similar manner we can expand the nonlinear measurement equation given by Equation (1.83) around a nominal operating point x = 2 and v = V = 0. This results in the linearized measurement equation 

$$\begin{array}{r c l}{{\tilde{y}}}&{{=}}&{{\left.\frac{\partial h}{\partial x}\right|_{0}\tilde{x}+\left.\frac{\partial h}{\partial v}\right|_{0}\tilde{v}}}\\ {{}}&{{=}}&{{C\tilde{x}+D v}}\end{array}$$
$$\begin{array}{r c l}{{\tilde{x}}}&{{=}}&{{x-\tilde{x}}}\\ {{\tilde{u}}}&{{=}}&{{u-\tilde{u}}}\\ {{\tilde{y}}}&{{=}}&{{y-\bar{y}}}\end{array}$$

where C and D are defined by the above equation. Equations (1.93) and (1.94) 
comprise a linear system that describes the deviations of the state and output from their nominal values. Recall that the tilde quantities in Equations (1.93) and (1.94) are defined as 

$$(1.94)$$
$$(1.95)$$
$$(1.96)$$

Consider the following model for a two-phase permanent magnet synchronous motor: 

$$\begin{array}{r c l}{{i_{a}}}&{{=}}&{{\frac{-R}{L}i_{a}+\frac{\omega\lambda}{L}\sin\theta+\frac{u_{a}}{L}}}\\ {{i_{b}}}&{{=}}&{{\frac{-R}{L}i_{b}-\frac{\omega\lambda}{L}\cos\theta+\frac{u_{b}}{L}}}\\ {{\omega}}&{{=}}&{{\frac{-3\lambda}{2J}i_{a}\sin\theta+\frac{3\lambda}{2J}i_{b}\cos\theta-\frac{F\omega}{J}-\frac{T_{l}}{J}}}\\ {{\dot{\theta}}}&{{=}}&{{\omega}}\end{array}$$

where i, and zb are the currents through the two windings, R *and* L are the resistance and inductance of the windings, 8 and w are the angular position and velocity of the rotor, A is the flux constant of the motor, Ua *and* Ub are the voltages applied across the two windings, J is the moment of inertia of the rotor and its load, F is the viscous friction of the rotor, and Z is the load torque. The time variable does not explicitly appear on the right side of the above equation, so this is a time-invariant system. However, the system is highly nonlinear and we therefore cannot directly use any linear systems tools for control or estimation. However, if we linearize the system around a nominal (possibly time-varying) operating point then we can use linear system tools for control and estimation. We start by defining a state vector as x = [ i, *zb w 8* 3'. With this definition we write 

(1.97) 

We linearize the system equation by taking the partial derivative of *f (x,* u) 
with respect to x and u to obtain 

$$\frac{\partial f}{\partial x}$$ $$\left[\begin{array}{cccc}-R/L&0&\lambda s_{4}/L&x_{3}\lambda c_{4}/L\\ 0&-R/L&-\lambda c_{4}/L&x_{3}\lambda s_{4}/L\\ -3\lambda s_{4}/2/J&3\lambda c_{4}/2/J&-F/J&-3\lambda(x_{1}c_{4}+x_{2}s_{4})/2/J\\ 0&0&1&0\end{array}\right]$$ $$\frac{\partial f}{\partial u}$$ $$\left[\begin{array}{cc}1/L&0\\ 0&1/L\\ 0&0\\ 0&0\end{array}\right]\tag{1.98}$$

where s4 = sin 2 4 and c4 =cos 24. The linear system 

$${\dot{\tilde{x}}}=A{\tilde{x}}+B{\tilde{u}}$$
$$(1.99)$$

i=~z++ii (1.99) 
approximately describesthe deviation of 2 from its nominal value 5. The nonlinear system was simulated with the nominal control values *fia(t)*= sin2.rrt and *fib(t)* = cos2.rrt. This resulted in a nominal state trajectory *Z(t).* The linear and nonlinearsystems were then simulated with nonnominal control values. Figure 1.1showsthe results of the linear and nonlinear simulations when the control magnitude deviation from nominal is a small positive number. It can be seen that the simulations result in similar state-space trajectories, although they do not match exactly. If the deviation is zero, then the linear and nonlinear simulations will match exactly. As the deviation from nominal increases, the difference between the linear and nonlinear simulations will increase. 

![23_image_0.png](23_image_0.png)

Figure **1.1** Example 1.4 comparison of nonlinear and linearized motor simulations. 
vvv 

## 1.4 Disc R **Et I 2 At I** 0 N

Most systems in the real world are described with continuous-time dynamics of the type shown in Equations (1.67) or **(1.83).** However, state estimation and control algorithms are almost always implemented in digital electronics. This often requires a transformation of continuous-time dynamics to discrete-time dynamics. This section discusses how a continuous-time linear system can be transformed into a discretetime linear system. 

Recall from Equation (1.68) that the solution of a continuous-time linear system is given by 

$$x(t)=e^{A(t-t_{0})}x(t_{0})+\int_{t_{0}}^{t}e^{A(t-\tau)}Bu(\tau)\,d\tau\tag{1.100}$$

Let t = tk (some discrete time point) and let the initial time to = *tk-1* (the previous discrete time point). Assume that **A(T),** B(T), and *U(T)* are approximately constant in the interval of integration. We then obtain 

$$x(t_{k})=e^{A(t_{k}-t_{k-1})}x(t_{k-1})+\int_{t_{k-1}}^{t_{k}}e^{A(t_{k}-\tau)}\,d\tau\,Bu(t_{k-1})\tag{1.101}$$
$$(1.102)$$

Now define At = tk - *tk-1,* define Q = T - *tk-1,* and substitute for T in the above equation to obtain 

$$\begin{array}{r c l}{{x(t_{k})}}&{{=}}&{{e^{A\Delta t}x(t_{k-1})+\int_{0}^{\Delta t}e^{A(\Delta t-\alpha)}\,d\alpha\,B u(t_{k-1})}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{=}}&{{e^{A\Delta t}x(t_{k-1})+e^{A\Delta t}\int_{0}^{\Delta t}e^{-A\alpha}\,d\alpha\,B u(t_{k-1})}}\\ {{}}&{{}}&{{}}\\ {{x_{k}}}&{{=}}&{{F_{k-1}x_{k-1}+G_{k-1}u_{k-1}}}\end{array}$$

where *Xk, Fk, Gk,* and Uk are defined by the above equation. This is a linear discretetime approximation to the continuous-time dynamics given in Equation (1.67). Note that this discretetime system defines Xk only at the discrete time points *{tk};* it does not say anything about what happens to the continuous-time signal *z(t)* in between the discrete time points. 

The difficulty with the above discretetime system is the computation of the integral of the matrix exponential, which is necessary in order to compute the G matrix. This computation can be simplified if A is invertible: 

$$\int_{0}^{\Delta t}e^{-A\tau}d\tau=\int_{0}^{\Delta t}\sum_{j=0}^{\infty}\frac{(-A\tau)^{j}}{j!}\,d\tau\tag{1.103}$$ $$=\int_{0}^{\Delta t}\left[I-A\tau+A^{2}\tau^{2}/2!-\cdots\right]\,d\tau$$ $$=\left[I\tau-A\tau^{2}/2!+A^{2}\tau^{3}/3!-\cdots\right]_{0}^{\Delta t}$$ $$=\left[I\Delta t-A(\Delta t)^{2}/2!+A^{2}(\Delta t)^{3}/3!-\cdots\right]$$ $$=\left[A\Delta t-(A\Delta t)^{2}/2!+(A\Delta t)^{3}/3!-\cdots\right]A^{-1}$$ $$=\left[I-e^{-A\Delta t}\right]A^{-1}$$  version from continuous time system matrices $A$ and $B$ to discrete time 
The conversion from continuous-time system matrices A and B to discretetime 
system matrices F and G can be summarized as follows: 
$$F=e^{A\Delta t}$$ $$G=F\int_{0}^{\Delta t}e^{-A\tau}\,d\tau\,B$$ $$=F\left[I-e^{-A\Delta t}\right]A^{-1}B\tag{1.104}$$
where At is the discretization step size. 

## 1.5 Simulation

In this section, we discuss how to simulate continuous-time systems (either linear or nonlinear) on a digital computer. We consider the following form of the general system equation from Equation (1.83): 

$${\dot{x}}=f(x,u,t)$$
$$x(t_{f})=x(t_{0})+\int_{t_{0}}^{t_{f}}f[x(t),u(t),t]\,d t$$
i = *f(z,* u, t) (1.105) 
where *u(t)* is a known control input. In order to simulate this system on a computer, we need to program a computer to solve for z(tp) at some user-specified value of tf. In other words, we want to compute 

$$x(t_{f})=x(0)+\int_{0}^{t_{f}}f[x(t),u(t),t]\,d t$$

Often, the initial time is taken as to = 0, in which case we have the slightly simpler looking equation 

$$(1.105)$$
$$(1.106)$$
$$(1.107)$$

We see that in order to find the solution *z(tf)* to the differential equation i = 
f(z,u,t), we need to compute an integral. The problem of finding the solution z(tf) is therefore commonly referred to as an integration problem. 

Now suppose that we divide the time interval [0, *tf]* into L equally spaced intervals so that tk = kT for k = 0,. . . , L, and the time interval T = *tf/L.* From this we note that tf = *tL.* With this division of the time interval, we can write the solution of Equation (1.107) as 

$$x(t_{f})=x(t_{L})\tag{1.108}$$ $$=x(0)+\sum_{k=0}^{L}\int_{t_{k}}^{t_{k+1}}f[x(t),u(t),t]\,dt$$
$$x(t_{n})=x(0)+\sum_{k=0}^{n}\int_{t_{k}}^{t_{k+1}}f[x(t),u(t),t]\,dt$$ $$x(t_{n+1})=x(0)+\sum_{k=0}^{n+1}\int_{t_{k}}^{t_{k+1}}f[x(t),u(t),t]\,dt\tag{1.109}$$

More generally, for some n E [0, L - 11, we can write *z(tn)* and *z(t,+l)* as 

$$x(t_{n+1})=x(t_{n})+\int_{t_{n}}^{t_{n+1}}f[x(t),u(t),t]\,dt\tag{1.110}$$

which means that If we can find a way to approximate the integral on the right side of the above equation, we can repeatedly propagate our *z(t)* approximation from time t, to time *tn+l,* thus obtaining an approximation for *z(t)* at any desired time t. The algorithm could **look** something like the following. 

$${}^{T}\,f[x(t),u(t),t]\,d t$$

Differential equation solution 
Assume that z(0) is given 
fort=O:T:tf-T 
Find an approximation I(t) x **s,""** *f[z(t), u(t),* t] dt 
* [10] M. C. Gonzalez-Garcia, M. C. Gonzalez-Garcia, M.  

## End 
In The Following Sections, We Present Three Different Ways To Approximate This Integral. The Approximations, In Order Of Increasing Computational Effort And Increasing Accuracy, Are Rectangular Integration, Trapezoidal Integration, And Fourth-Order Runge-Kutta Integration. 1.5.1 Rectangular Integration

If the time interval *(tn+l -tn)* is small, then *f[z(t), u(t), t]* is approximately constant in this interval. Equation (1.110) can therefore be approximated as 

$$x(t_{n+1})\approx x(t_{n})+\int_{t_{n}}^{t_{n+1}}f[x(t_{n}),u(t_{n}),t_{n}]\,dt\tag{1.111}$$ $$\approx x(t_{n})+f[x(t_{n}),u(t_{n}),t_{n}]T$$
$$(1.112)$$

Equation (1.109) can therefore be approximated as 

$$x(t_{n})\approx x(0)+\sum_{k=0}^{n}\int_{t_{k}}^{t_{k+1}}f[x(t_{k}),u(t_{k}),t_{k}]\,dt$$ $$=x(0)+\sum_{k=0}^{n}f[x(t_{k}),u(t_{k}),t_{k}]T$$

This is called Euler integration, or rectangular integration, and is illustrated in Figure 1.2. As long as T is sufficiently small, this gives a good approximation for This gives the following algorithm for integrating continuous-time dynamics using rectangular integration. The time loop in the algorithm is executed for 4tn). 

t = 0, T, 2T, . . . , tf - T. 
Rectangular integration 
Assume that $x(0)$ is given for t = 0 : $T:t_{f}-T$  Compute $f[x(t),u(t),t]\\ x(t+T)=x(t)+f[x(t),u(t),t]T$  and ... 

## End 1.5.2 Trapezoidal Integration

An inspection of Figure 1.2 suggests an idea for improving the approximation for z(t). Instead of approximating each area as a rectangle, what if we approximate each area as a trapezoid? Figure 1.3 shows how an improved integration algorithm can be implemented. This is called modified Euler integration, or trapezoidal integration. A comparison of Figures 1.2 and 1.3 shows that trapezoidal integration 

![27_image_0.png](27_image_0.png)

An illustration of rectangular integration. We have i = f(x), so x(t) is the Figure 1.2 area under the f(x) curve. This area can be approximated as the sum of the rectangular areas A1. That is, x(0.5) ~ A1, x(1) ~ A1 + A2, ···.

![27_image_1.png](27_image_1.png)

Figure 1.3 An illustration of trapezoidal integration. We have x = f(x), so x(t) is the area under the f(x) curve. This area can be approximated as the sum of trapezoidal areas A1. That is, x(1) ~ A1, x(2) ~ A1 + A2, and x(3) ~ A1 + A2 + A3.
appears to give a better approximation than rectangular integration, even though the time axis is only divided into half as many intervals in trapezoidal integration.

With rectangular integration we approximated f[x(t), u(t), t] as a constant in the interval t E [tn, tn+1]. With trapezoidal integration, we instead approximate f [x(t), u(t), t] as a linear function in the interval t E [tn, tn+1]. That is,

$$f[x(t)]\approx f[x(t_{n}),u(t_{n}),t_{n}]+\tag{1.113}$$ $$\left(\frac{f[x(t_{n+1}),u(t_{n+1}),t_{n+1}]-f[x(t_{n}),u(t_{n}),t_{n}]}{T}\right)(t-t_{n})$$ $$\mbox{for}t\in[t_{n},t_{n+1}]$$
$$x(t_{n+1})\approx x(t_{n})+\int_{t_{n}}^{t_{n+1}}\biggl{\{}f[x(t_{n}),u(t_{n}),t_{n}]+\tag{1.114}$$ $$\left(\frac{f[x(t_{n+1}),u(t_{n+1}),t_{n+1}]-f[x(t_{n}),u(t_{n}),t_{n}]}{T}\right)(t-t_{n})\biggr{\}}\ dt$$ $$=x(t_{n})+\left(\frac{f[x(t_{n}),u(t_{n}),t_{n}]+f[x(t_{n+1}),u(t_{n+1}),t_{n+1}]}{2}\right)T$$ $$=x(t_{n})+\frac{1}{2}\bigl{(}f[x(t_{n}),u(t_{n}),t_{n}]T+f[x(t_{n+1}),u(t_{n+1}),t_{n+1}]T\bigr{)}$$

This equation to approximate z(tn+l), however, has z(t,+l) on the right side of the equation. How can we plug z(tn+l) into the right side of the equation if we do not yet know z(t,+l)? The answer is that we can use the rectangular integrs tion approximation from the previous section for z(tn+l) on the right side of the equation. The above equation can therefore be written as 

$$\Delta x_{1}=f[x(t_{n}),u(t_{n}),t_{n}]T$$ $$\Delta x_{2}=f[x(t_{n+1}),u(t_{n+1}),t_{n+1}]T$$ $$\approx f[x(t_{n})+\Delta x_{1},u(t_{n+1}),t_{n+1}]T$$ $$x(t_{n+1})\approx x(t_{n})+\frac{1}{2}\left(\Delta x_{1}+\Delta x_{2}\right)\tag{1.115}$$

This gives the following algorithm for integrating continuous-time dynamics The time loop in the algorithm is executed for 

using trapezoidal integration. 
t = 0, T, *2T,* . . . , tf - T. 
$21,\cdots,\upsilon_{f}=1$.  **Trapezoidal integration**  Assume that $x(0)$ is given  for t = 0 : $T:t_{f}-T$  $\Delta x_{1}=f[x(t),u(t),t]T$  $\Delta x_{2}=f[x(t)+\Delta x_{1},u(t+T),t+T]T$  $x(t+T)=x(t)+(\Delta x_{1}+\Delta x_{2})/2$  end

## 1.5.3 Runge-Kutta Integration

From the previous sections, we see that rectangular integration involves the calculation of one function value at each time step, and trapezoidal integration involves the calculation of two function values at each time step. In order to further improve the integral approximation, we can perform additional function calculations at each time step. nth-order Runge-Kutta integration is the approximation of an integral by performing n function calculations at each time step. Rectangular integration is therefore equivalent to first-order Runge-Kutta integration, and trapezoidal integration is equivalent to second-order Runge-Kutta integration. 

The most commonly used integration scheme of this type is fourth-order Runge-
Kutta integration. We present the fourth-order Runge-Kutta integration algorithm 
(without derivation) as follows: 

$f[x(t_{k}),u(t_{k}),t_{k}]T$  $f[x(t_{k})+\Delta x_{1}/2,u(t_{k+1/2}),t_{k+1/2}]T$  $f[x(t_{k})+\Delta x_{2}/2,u(t_{k+1/2}),t_{k+1/2}]T$  $f[x(t_{k})+\Delta x_{3},u(t_{k+1}),t_{k+1}]T$  $x(t_{k})+(\Delta x_{1}+2\Delta x_{2}+2\Delta x_{3}+\Delta x_{4})$ /6
$$\Delta x_{1}\quad=$$
$$\Delta x_{2}$$

$$\begin{array}{r l}{\Delta x_{3}}&{{}=}\\ {\Delta x_{4}}&{{}=}\end{array}$$
$$(1.116)$$
$$x(t_{k+1})$$
x(tk+i) M *z(tk)* + (hi + 2Ax2 + 2AX3 + **A24)** /6 (1.116) 
where *tk+1/2* = tk + **T/2.** Fourth-order Runge-Kutta integration is more computationally demanding than rectangular or trapezoidal integration, but it also provides far greater accuracy. This gives the following algorithm for integrating continuoustime dynamics using fourth-order Runge-Kutta integration. The time loop in the algorithm is executed for t = 0, **T, 2T,** . 

, tf - T. 

Fourt h-order Runge-Kutta integration Assume that z(0) is given fort=O: **T: tf-T** 
ti = t +T/2 Ax1 = f[z(t), w, t]T 
AXZ = *.f[X(t)* + **AxI/~,** U(ti), ti]T 
Ax3 = f[.(t) + **Ax2/2,** U(tl), tl]T 
A24 = f[z(t) + **Az3,** *u(t* + T), t + **TIT** 
z(t + T) = *z(t)* + (A21 + 2Ax2 + 2Ax3 + **A24)** /6 end Runge-Kutta integration was invented by Carl Runge, a German mathematician and physicist, in 1895. It was independently invented and generalized by Wilhelm Kutta, a German mathematician and aerodynamicist, in 1901. More accurate integration algorithms have also been derived and are sometimes used, but fourth-order Runge-Kutta integration is generally considered a good trade-off between accuracy and computational effort. Further information and derivations of numerical integration algorithms can be found in many numerical analysis texts, including [Atk89]. 

Suppose we want to numerically compute *z(t)* at t = 1 based on the differential equation x =cost (1.117) 
with the initial condition z(0) = 0. We can analytically integrate the equation to find out that z(1) = sin1 M 0.8415. If we use a numerical integration scheme, we have to choose the step size T. Table 1.1 shows the error of the rectangular, trapezoidal, and fourth-order Runge-Kutta integration methods for this example for various values of T. As expected, Runge-Kutta is more accurate than trapezoidal, and trapezoidal is more accurate than rectangular. 

Also as expected, the error for given method decreases as T decreases. However, perhaps the most noteworthy feature of Table 1.1 is *how* the integration error decreases with T. We can *see* that with rectangular integration, when T 
is halved, the integration error is also halved. With trapezoidal integration, when T is halved, the integration error decreases by a factor of four. With Runge-Kutta integration, when T is halved, the integration error decreases by a factor of 16. We conclude that (in general) the error of rectangular integration is proportional to T, the error of trapezoidal integration is proportional to *T2,* and the error of Runge-Kutta integration is proportional to **T4.** 
Table **1.1** 
x = cos t kom t = 0 to t = 1, for various integration algorithms, and for various time step sizes T. 

Example **1.5** results. Percent errors when numerically integrating 

|                          | T = 0.1   | T = 0.05   | T = 0.025   |
|--------------------------|-----------|------------|-------------|
| Rectangular              | 2.6       | 1.3        | 0.68        |
| Trapezoidal              | 0.083     | 0.021      | 0.0052      |
| Fourth-order Runge-Kutta | 3.5 x     | 2.2 x      | 1.4 x       |

## Vvv 1.6 Stability

In this section, we review the concept of stability for linear time-invariant systems. We first deal with continuous-time systems in Section 1.6.1, and then discrete-time systems in Section 1.6.2. We state the important results here without proof. The interested reader can refer to standard books on linear systems for more details and additional results [Kai80, Bay99, Che991. 

## 1.6.1 Continuous-Time Systems

Consider the zero-input, linear, continuous-time system 

$${\dot{x}}\quad=\quad A x$$

$$(1.118)$$
$$C x$$
$\mathfrak{M}$
y = ex (1.118) 
The definitions of marginal stability and asymptotic stability are as follows. 

Definition 1 A linear continuous-time, time-invariant system is marginally stable if the state x(t) is bounded **for** all t and **for** *all bounded initial states x(0).* Marginal stability is also called Lyapunov stability. Definition 2 *A linear continuous-time, time-invariant system is asymptotically* stable if, **for** *all bounded initial states x(O),* 

$$\operatorname*{lim}_{t\to\infty}x(t)=0$$
$$(1.119)$$
t+w (1 * 119) 
The above two definitions show that a system is marginally stable if it is asymptotically stable. That is, asymptotic stability is a subset of marginal stability. 

Marginal stability and asymptotic stability are types of internal stability. This is because they deal with only the state of the system (i.e., the internal condition of the system) and do not consider the output of the system. More specific categories of internal stability (e.g., uniform stability and exponential stability) are given in some books on linear systems. 

Since the solution of Equation (1.118) is given as 

$$(1.120)$$
$$x(t)=\exp(A t)x(0).$$
$$\operatorname*{lim}_{t\to\infty}\exp(A t)\leq M<\infty$$
$$(1.121)$$
z(t) = exp(At)z(O) (1.120) 
we can state the following theorem. 

Theorem 1 A linear continuous-time, time-invariant system is marginally stable if and only if lim exp(At) *5 M* < 00 (1.121) 
t+w for some constant matrix M. This is just a way of *saying that the matrix exponential* does not increase without bound. 

The "less than or equal to" relation in the above theorem raises some questions, because the quantities on either side of this mathematical symbol are matrices. What does it mean for a matrix to be less than another matrix? It can be interpreted several ways. For example, to say that A < B is usually interpreted to mean that 
(B - A) is positive definite.5 In the above theorem we can use any reasonable definition for the matrix inequality and the theorem still holds. 

A similar theorem can be stated by combining Definition (2) with Equation (1.120). 

Theorem 2 A linear continuous-time, time-invariant system is asymptotically stable if and only if 

$$(1.122)$$

lim exp(At) = 0 (1.122) 
$$\operatorname*{lim}_{t\to\infty}\exp(A t)=0$$

Now recall that exp(At) = Qexp(At)Q-', where Q is a constant matrix containing the eigenvectors of A, and A is the Jordan form of A. The exponential eXp(At) therefore contains terms like exp(Ait), texp(Ait), *t2exp(Ait),* and so on, where A, is an eigenvalue of A. The boundedness of exp(At) is therefore related to the eigenvalues of A as stated by the following theorems. 

Theorem 3 A linear continuous-time, time-invariant system is marginally stable if and only if one of *the following conditions holds.* 
1. **All** of the eigenvalues of A *have negative real parts.* 
2. **All** of the eigenvalues of A have negative or zero real parts, and those with real parts equal to zero have a geometric multiplicity equal to their algebraic multiplicity. That is, the Jordan blocks that are associated with the eigenvalues that have real parts equal to zero are first order. 

Theorem 4 A linear continuous-time, time-invariant system is asymptotically stable if and only if all of the eigenvalues of A *have negative real parts.* 

5Sometime5 the statement A < B means that every element of A is less than the corresponding element of B. However, we will not use that definition in this book. 
Consider the system 

$$\begin{array}{c c c}{{0}}&{{1}}&{{0}}\\ {{0}}&{{0}}&{{0}}\\ {{0}}&{{0}}&{{-1}}\end{array}\Bigg]\,x\qquad\qquad\qquad\qquad(1.123)$$
$${\dot{x}}=$$

Since the A matrix is upper triangular, we know that its eigenvalues are on the diagonal; that is, the eigenvalues of A are equal to 0, 0, and -1. We see that the system is asymptotically unstable since some of the eigenvalues are nonnegative. We also note that the A matrix is already in Jordan form, and we see that the Jordan block corresponding to the 0 eigenvalue is second order. Therefore, the system is also marginally unstable. The solution of this system is 

$$\begin{array}{r c l}{{x(t)}}&{{=}}&{{\exp(A t)x(0)}}\\ {{}}&{{}}&{{=}}&{{\left[\begin{array}{l l l}{{1}}&{{t}}&{{0}}\\ {{0}}&{{1}}&{{0}}\\ {{0}}&{{0}}&{{e^{-t}}}\end{array}\right]x(0)}}\end{array}$$
$$(1.124)$$

The element in the first row and second column of exp(At) increases without bound as t increases, so there are some initial states *x(0)* that will result in unbounded *x(t).* However, there are also some initial kates z(0) that will result in bounded *z(t).* For example, if z(0) = [ 1 T 0 1 ] , then 

$$x(t)=\left[\begin{array}{ccc}1&t&0\\ 0&1&0\\ 0&0&e^{-t}\end{array}\right]\left[\begin{array}{c}1\\ 0\\ 1\end{array}\right]\tag{1.125}$$ $$=\left[\begin{array}{c}1\\ 0\\ e^{-t}\end{array}\right]$$
$$\begin{array}{r l}{x(t)}&{{}=\ }\\ {\ }&{}\\ {\ }&{}\\ {\ }&{}\\ {\ }&{}\end{array}$$

and *z(t)* will be bounded for all t. However, this does not say anything about the stability of the system; it only says that there exists some z(0) that results in a bounded *z(t).* If we instead choose *x(0)* = [ 0 T 1 0 ] , then 

$\left[\begin{array}{ccc}1&t&0\\ 0&1&0\\ 0&0&e^{-t}\end{array}\right]\left[\begin{array}{c}0\\ 1\\ 0\end{array}\right]$  $\left[\begin{array}{c}t\\ 1\\ 0\end{array}\right]$
and *z(t)* increases without bound. This proves that the system is asymptotically unstable and marginally unstable. 

vvv 

Consider the system 

$${\dot{x}}={\left[\begin{array}{l l l}{0}&{0}&{0}\\ {0}&{0}&{0}\\ {0}&{0}&{-1}\end{array}\right]}\,x$$

The eigenvalues of A are equal to 0, 0, and -1. We *see* that the system is asymptotically unstable since some of the eigenvalues are nonnegative. In order to see if the system is marginally stable, we need to compute the geometric multiplicity of the 0 eigenvalue. (This can be done by noticing that A 
is already in Jordan form, but we will go through the exercise more completely for the sake of illustration.) Solving the equation 

$$\begin{array}{l}{{0}}\\ {{0}}\\ {{0}}\end{array}$$
$$(\lambda I-A)v=\left[\begin{array}{l}{{}}\\ {{}}\end{array}\right]$$
(XI - A). = [ i] 
$$(1.127)$$
$$(1.128)$$
$$(1.129)$$

(where X = 0) for nonzero vectors 21, we see that there are two linearly independent solutions given as 

$$\begin{array}{l}{{0}}\\ {{1}}\\ {{0}}\end{array}$$
$$\left[\begin{array}{l}{{1}}\\ {{0}}\\ {{0}}\end{array}\right],\left[\begin{array}{l}{{1}}\\ {{0}}\\ {{1}}\end{array}\right]$$
$$v=$$
.=[%],[%I (1.129) 
This shows that the geometric multiplicity of the 0 eigenvalue is equal to 2, which means that the system is marginally stable. The solution of this system is 
~(t) = exp(At)x(O) 

$$\left.{\begin{array}{l}{x(0)}\\ {0}\\ {0}\\ {e^{-t}}\end{array}}\right]x(0)$$
$$\pi(t)$$
$$\mathbf{\Sigma}=$$
= [ : ; : ] *x(0)* 
$$(1.130)$$
$$\begin{array}{l l l}{\exp(A t)x(0)}\\ {\left[\begin{array}{l l l}{1}&{0}&{0}\\ {0}&{1}&{0}\\ {0}&{0}&{e^{-}}\end{array}\right]}\end{array}$$

Regardless of x(O), we see that x(t) will always be bounded, which means that the system is marginally stable. Note that x(t) may approach 0 as t increases, depending on the value of x(0). For example, if x(0) = [ 0 0 -1 ] , then T 

$$\left[\begin{array}{c c}{{0}}&{{0}}\\ {{1}}&{{0}}\\ {{0}}&{{e^{-t}}}\end{array}\right]\left[\begin{array}{c c}{{0}}\\ {{0}}\\ {{-1}}\end{array}\right]=\left[\begin{array}{c c}{{0}}\\ {{1}}\\ {{0}}\end{array}\right]$$
$$x(t)={\left[\begin{array}{l}{1}\\ {0}\\ {0}\end{array}\right]}$$
x(t> = [ 0 o o 1 0 ] [ !l] = [ -!-t] *e-t* 
$$\left[\begin{array}{l l l}{{\ }}&{{\ }}&{{\ }}\\ {{0}}&{{\ }}&{{\ }}\\ {{0}}&{{\ }}&{{\ }}\\ {{\cdot e^{-t}}}&{{\ }}&{{\ }}\end{array}\right]$$
$$(1.131)$$

and x(t) approaches 0 as t increases. However, this does not say anything about the asymptotic stability of the system; it only says that there exists some x(0) that results in state *z(t)* that asymptotically approaches 0. If we instead choose x(0) = [ 0 T 1 0 ] , then 

$$\left[\begin{array}{l l l}{{-}}&{{}}\\ {{1}}&{{0}}&{{0}}\\ {{0}}&{{1}}&{{0}}\\ {{0}}&{{0}}&{{e^{-t}}}\end{array}\right]\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right]$$
$$\left[\begin{array}{c}{{0}}\\ {{1}}\\ {{0}}\end{array}\right]=\left[\begin{array}{c}{{\ }}\\ {{\ }}\\ {{\ }}\end{array}\right]$$
$$x(t)=$$
.O=[o 0 0 1 *e-t* o][;]=[;] 
$$\begin{array}{l}{{0}}\\ {{1}}\\ {{0}}\end{array}\right]\qquad\qquad(1.132)$$

and x(t) does not approach 0. This proves that the system is asymptotically unstable. 

vvv 

## 1.6.2 Discrete-Time Systems

$$\begin{array}{r c l}{{x_{k+1}}}&{{=}}&{{F x_{k}}}\\ {{}}&{{y_{k}}}&{{=}}&{{H x_{k}}}\end{array}$$

Consider the zero-input, linear, discretetime, timeinvariant system 

$$\left({1.133}\right)$$... 
$$(1.134)$$

The definitions of marginal stability (also called Lyapunov stability) and asymptotic stability are analogous to the definitions for continuous-time systems that were given in Section 1.6.1. 

Definition 3 A linear discrete-time, time-invariant system is marginally stable if the state Xk is bounded **for** all k and for all bounded initial states *XO.* 
Definition 4 A *linear discrete-time, time-invariant system is asymptotically stable* 

$$\operatorname*{lim}_{k\to\infty}x_{k}=0$$

if for all bounded initial states *XO.* 
Marginal stability and asymptotic stability are types of internal stability. This is because they deal with only the state of the system (i.e., the internal condition of the system) and do not consider the output of the system. More specific categories of internal stability (e.g., uniform stability and exponential stability) are given in some books on linear systems. 

Since the solution of Equation **(1.133)** is given as 

$$(1.135)$$
$$x_{k}=A^{k}x_{0}$$

$$(1.136)$$
xk = *A k* XO **(1.135)** 
we can state the following theorems. 

Theorem 5 A *linear discrete-time, time-invariant system is marginally stable if* and only if 

$$\operatorname*{lim}_{k\to\infty}A^{k}\leq M<\infty$$

for some constant matrix M. This is just a way of saying that the powers of A do not increase without bound. 

Theorem 6 A *linear discrete-time, time-invariant system is asymptotically stable* af *and only if* lim Ak = 0 **(1.137)** 

$$\operatorname*{lim}_{k\to\infty}A^{k}=0$$

$$(1.137)$$

Now recall that Ak = QAkQ-l, where Q is a constant mFtrix containing the eigenvectors of A, and A is the Jordan form of A. The matrix Ak therefore contains terms like A!, *kA;, k2$,* and so on, where A, is an eigenvalue of A. The boundedness of Ak is therefore related to the eigenvalues of A as stated by the following theorems. 

Theorem 7 A linear discrete-time, time-invariant system is marginally stable if and only if one of *the following conditions holds.* 
1. **All** of the eigenvalues of A have magnitude less than one. 

2. **All** of the eigenvalues of A have magnitude less than or equal to one, and those with magnitude equal to one have a geometric multiplicity equal to their algebraic multiplicity. That is, the Jordan blocks that are associated with the eigenvalues that have magnitude equal to one are first order. 

Theorem 8 A *linear discrete-time, time-invariant system is asymptotically stable* if and only if all of the eigenvalues of A *have magnitude less than one.* 

## 1.7 Co Ntro Llab I Ll Ty And 0 Bs E Rva Bi Llty

The concepts of controllability and observability are fundamental to modern control theory. These concepts define how well we can control a system (i.e., drive the state to a desired value) and how well we can observe a system (i.e., determine the initial conditions after measuring the outputs). These concepts are also important to some of the theoretical results related to optimal state estimation that we will encounter later in this book. 

## 1.7.1 Controllability

The following definitions and theorems give rigorous definitions for controllability for linear systems in the both the continuous-time and discretetime cases. 

Definition 5 A continuous-time system is controllable if for any initial state x(0) 
and any final time t > 0 there exists a control that transfers the state to any desired value at time t. 

Definition 6 A discrete-time system is controllable if for any initial state xo and some final time k there exists a control that transfers the state to any desired value at time k. 

Note the controllability definition in the continuous-time case is much more demanding than the definition in the discretetime case. In the continuous-time case, the existence of a control is required for any final time. In the discretetime case, the existence of a control is required for *some* final time. In both cases, controllability is independent of the output equation. 

There are several tests **for** controllability. The following equivalent theorems can be used to test for the controllability of continuous linear timeinvariant systems. 

Theorem 9 *The n-state6 continuous linear time-invariant system x* = Ax + Bu has the controllability matrix P defined by 

$$P={\left[\begin{array}{l l l l}{B}&{A B}&{\cdots}&{A^{n-1}B}\end{array}\right]}$$
$$(1.138)$$
$$(1.139)$$

The system is controllable if and only if *p(P)* = n. 

Theorem 10 The n-state continuous linear time-invariant system x = Ax + Bu is controllable if and only if the controllability grammian defined by it 

$$\int_{0}^{t}e^{A\tau}B B^{T}e^{A^{T}\tau}\,d\tau$$

6The notation *n-state system* indicates a system that has n elements in its state variable z. 

is positive definite for some t E (0,~). 

Theorem 11 *The n-state continuous linear time-invariant system x* = Ax + Bu is controllable if and only if *the differential Lyapunov equation* 

$$\begin{array}{r c l}{{W(0)}}&{{=}}&{{0}}\\ {{\dot{W}}}&{{=}}&{{W A^{T}+A W+B B^{T}}}\end{array}\tag{1.140}$$

has a positive definite solution W(t) for *some t* E (0,~). This is also called a Sylvester equation. 

Similar to the continuous-time case, the following equivalent theorems can be used to test for the controllability of discrete linear timeinvariant systems. 

Theorem 12 The n-state discrete linear time-invariant system Xk = *Fxk-1* + 
Guk-1 *has the controllability matrix P defined by* 

$$P={\left[\begin{array}{l l l l}{G}&{F G}&{\cdots}&{F^{n-1}G}\end{array}\right]}$$

The system is controllable af *and only if p(P)* = n. 

Theorem 13 The n-state discrete hear time-invariant system Xk = FXk-1 + 
Guk-1 *is controllable if and only if the controllability grammian defined by* 

$$(1.141)$$
$$\sum_{i=0}^{k}A^{k-i}B B^{T}(A^{T})^{k-i}$$
$$(1.142)$$

is positive definite for some k E (0,~). 

Theorem 14 The n-state discrete hear tame-invariant system Xk = *Fxk-1* + 
GUk-1 *is controllable if and only if the difference Lyapunov equation* 

$$\begin{array}{r c l}{{W_{0}}}&{{=}}&{{0}}\\ {{W_{\mathrm{t+1}}}}&{{=}}&{{F W_{\mathrm{t}}F^{T}+G G^{T}}}\end{array}$$

has a positive definite solution wk *for some* k E (0, w). This is also called a Stein equation. 

Note that Theorems 9 and 12 give identical tests for controllability for both continuous-time and discretetime systems. In general, these are the simplest controllability tests. Controllability tests for timevarying linear systems can be obtained by generalizing the above theorems. Controllability for nonlinear systems is much more difficult to formalize. 

$${\left[\begin{array}{l}{{\dot{v}}_{C}}\\ {{\dot{i}}_{L}}\end{array}\right]}={\left[\begin{array}{l l}{-2/R C}&{1/C}\\ {-1/L}&{0}\end{array}\right]}{\left[\begin{array}{l}{v_{C}}\\ {i_{L}}\end{array}\right]}+{\left[\begin{array}{l}{1/R C}\\ {1/L}\end{array}\right]}\,u$$

The RLC circuit of Figure *1.4* has the system description 

$$(1.143)$$
$$(1.144)$$

where vc is the voltage across the capacitor, i~ is the current through the inductor, and u is the applied voltage. We will use Theorem 9 to determine the conditions under which this system is controllable. The controllability matrix is computed as 

$$P=\left[\begin{array}{cc}B&AB\end{array}\right]\tag{1.145}$$ $$=\left[\begin{array}{cc}1/RC&1/LC-2/R^{2}C^{2}\\ 1/L&-1/RLC\end{array}\right]$$

From this we can compute the determinant of P as 

$$|P|=1/R^{2}L C^{2}-1/L^{2}C$$

![37_image_0.png](37_image_0.png)

$$(1.146)$$

The determinant of P is 0 only if R = fl. 

So the system is controllable unless R = m. It would be very difficult to obtain this result from Theorems 10 and 11. 

Figure **1.4 RLC** circuit for Example **1.8.** 

## Vvv 1.7.2 0 **Bserva Bility**

The following definitions and theorems give rigorous definitions for observability for linear systems in both the continuous-time and discrete-time cases. 

Definition 7 A continuous-time system is observable if **for** any initial state x(0) 
and any final time t > 0 the initial state x(0) can be uniquely determined by knowledge of the input U(T) and output y(~) for all T E *[0, t].* 
Definition 0 A discrete-time system is observable if **for** any initial state xo and some final time k the initial state XIJ can be uniquely determined by knowledge of the input uz and output yd **for** all i E *[0, k].* 
Note the observability definition in the continuous-time case is much more demanding than the definition in the discrete-time case. In the continuous-time case, the initial state must be able to be determined at *any* final time. In the discretetime case, the initial state must be able to be determined at *some* final time. If a system is observable then the initial state can be determined, and if the initial state can be determined then all states between the initial and final times can be determined. 

There are several tests for controllability. The following equivalent theorems can be used to test for the controllability of continuous linear time-invariant systems. 

Theorem 15 The n-state continuous linear time-invariant system 

$\begin{array}{ccc}\dot{x}&=&0\\ y&=&0\end{array}$
$$\begin{array}{l}{A x+B u}\\ {C x}\end{array}$$
k = Ax+Bu 
y = cx 
$$(1.147)$$
has the observability matrix Q defined by 

$$Q={\left[\begin{array}{l}{\begin{array}{l}{C}\\ {C A}\\ {\vdots}\\ {C A^{n-1}}\end{array}\right]}\end{array}}$$
$$(1.148)$$

The system is observable if and only if *p(Q)* = n. 

Theorem 16 The n-state continuous linear time-invariant system 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A x+B u}}\\ {{y}}&{{=}}&{{C x}}\end{array}$$
$$(1.149)$$

is observable if *and only if the observability grammian defined by* 

$$\int_{0}^{t}e^{A^{T}\tau}C^{T}C e^{A\tau}\,d\tau$$
$$(1.150)$$

is positive definite for some t E (0,m). Theorem 17 *The n-state continuous linear time-invariant system* 

$\begin{array}{ccc}\dot{x}&=&0\\ y&=&0\end{array}$
$$\begin{array}{l}{A x+B u}\\ {C x}\end{array}$$
k = Ax+Bu 
y = cx 
$$(1.151)$$
$$(1.152)$$
is observable if and only if the differential Lyapunov equation 

$$\begin{array}{r c l}{{W(t)}}&{{=}}&{{0}}\\ {{-\dot{W}}}&{{=}}&{{W A+A^{T}W+C^{T}C}}\end{array}$$
$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F x_{k-1}+G u_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H x_{k}}}\end{array}$$

has a positive definite solution W(T) for some T E (0,t). This is also called a Sylvester equation. 

Similar to the continuous-time case, the following equivalent theorems can be used to test for the observability of discrete linear time-invariant systems. 

Theorem 18 *The n-state discrete linear time-invariant system* 

$$(1.153)$$

has the observability matrix Q defined by 

$$Q=\left[\begin{array}{c}H\\ H F\\ \vdots\\ H F^{n-1}\end{array}\right]\tag{1.154}$$

The system is observable if and only if *p(Q)* = n. 

Theorem 19 *The n-state discrete linear time-invariant system* 

$$\begin{array}{r c l}{{x_{k}}}&{{=}}&{{F x_{k-1}+G u_{k-1}}}\\ {{y_{k}}}&{{=}}&{{H x_{k}}}\end{array}$$
$$(1.155)$$

is observable if and only if the observability grammian defined by 

$$\sum_{i=0}^{k}(F^{T})^{i}H^{T}H F^{i}$$

$$(1.156)$$

is positive definite for some k E *(0,* m). 

Theorem 20 *The n-state discrete linear time-invariant system* 

?4k = *Hxk* 
$$\begin{array}{l}{{F x_{k-1}+G u_{k-1}}}\\ {{H x_{k}}}\end{array}$$
$$\begin{array}{r l}{x_{k}}&{{}=1}\\ {y_{k}}&{{}=1}\end{array}$$
xk = FXk-1 + GUk-1 
$$(1.157)$$
is observable if and only if the difference Lyapunov equation 
$$\begin{array}{r c l}{{W_{k}}}&{{=}}&{{0}}\\ {{W_{\mathrm{t}}}}&{{=}}&{{F^{T}W_{\mathrm{t+1}}F+H^{T}H}}\end{array}$$
$$(1.158)$$
has a positive definite solution Wo *for some* k E (0,m). This is also called a Stein equation. 

Note that Theorems 15 and 18 give identical tests for observability for both continuoustime and discretetime systems. In general, these are the simplest observability tests. Observability tests for timevarying linear systems can be obtained by generalizing the above theorems. Observability for nonlinear systems is much more difficult to formalize. 

The RLC circuit of Example 1.8 has the system description 

$$\left[\begin{array}{c}\dot{v}_{C}\\ \dot{i}_{L}\end{array}\right]=\left[\begin{array}{cc}-2/RC&1/C\\ -1/L&0\end{array}\right]\left[\begin{array}{c}v_{C}\\ i_{L}\end{array}\right]+\left[\begin{array}{c}1/RC\\ 1/L\end{array}\right]u$$ $$y=\left[\begin{array}{cc}-1&0\end{array}\right]\left[\begin{array}{c}v_{C}\\ i_{L}\end{array}\right]\tag{1.159}$$

where vc is the voltage acrom the capacitor, iL is the current through the inductor, and u is the applied voltage. We will use Theorem 15 to determine 

the conditions under which this system is observable. The observability matrix is computed as 

$$(1.160)$$
$$(1.161)$$

The determinant of the observability matrix can be computed as IQI = 1/C (1.161) 
The determinant of Q is nonzero, so the system is observable. On the other hand, suppose that R = L = C = 1 and the output equation is 

$$y={\left[\begin{array}{l l}{-1}&{1}\end{array}\right]}\left[\begin{array}{l}{v_{C}}\\ {i_{L}}\end{array}\right]$$
Then the observability matrix can be computed as 
$$(1.162)$$
$$|Q|=1/C$$
$$\begin{array}{r c l}{{}}&{{}}&{{}}\\ {{}}&{{}}&{{Q}}\\ {{}}&{{}}&{{=}}\end{array}\left[\begin{array}{c c}{{-1}}&{{1}}\\ {{1}}&{{-1}}\end{array}\right]$$
$$(1.163)$$
$$(1.164)$$
$$(1.165)$$

So the system is unobservable. It would be very difficult to obtain this result from Theorems 16 and **17.** 
vvv 

## 1.7.3 Stabilizability And Detectability

The concepts of stabilizability and detectability are closely related to controllability and observability, respectively. These concepts are also related to the modes of a system. The modes of a system are all of the decoupled states after the system is transformed into Jordan form. A system can be transformed into Jordan form as follows. Consider the system 

$$\begin{array}{r l}{{\dot{x}}}&{{}=\quad A x+B u}\\ {y}&{{}=\quad C x+D u}\end{array}$$

First find the eigendata of the system matrix A. Suppose the eigenvectors are denoted as *v1,.* . . , v,. Create an n x n matrix M by augmenting the eigenvectors as follows. Define a new system as 

$$M={\left[\begin{array}{l l l}{v_{1}}&{\cdots}&{v_{n}}\end{array}\right]}$$
$$=M^{-1}AM\bar{x}+M^{-1}B$$ $$=\bar{A}\bar{x}+\bar{B}u$$ $$=CM\bar{x}+Du$$ $$=\bar{C}\bar{x}+Du\tag{1.166}$$
$$\mathbf{\mu}_{J}$$

The new system is called the Jordan form representation of the original system. 

Note that the matrix M will always be invertible because the eigenvectors of a matrix can always be chosen to be linearly independent. The two systems of Equations (1.164) and (1.166) are called algebraically equivalent systems. This is because they have the same input and the same output (and therefore they have the same transfer function) but they have different states. 

Consider the system 

$$\begin{array}{r c l}{{\dot{x}}}&{{=}}&{{A}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\\ {{y}}\end{array}\right.}}&{{=}}&{{C}}\\ {{}}&{{}}&{{=}}&{{\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right.}}\end{array}$$
i = Ax+Bu 
$\begin{array}{c}Ax+Bu\\ \\ \left[\begin{array}{ccc}1&1&2\\ 0&1&3\\ 0&0&-2\end{array}\right]x+\left[\begin{array}{c}\\ \\ \end{array}\right]\\ Cx+Du\\ \left[\begin{array}{ccc}1&0&0\end{array}\right]+2u\end{array}$  . 
$${\begin{array}{l}{1}\\ {1}\\ {0}\end{array}}\Bigg|\ u$$
y = *CX+DU* 
$$(1.167)$$

This system has the same transfer function as 

$$\begin{array}{r c l}{{\dot{\bar{x}}}}&{{=}}&{{\bar{A}\bar{x}+\bar{B}u}}\\ {{}}&{{}}&{{}}\\ {{}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{1}}\\ {{0}}&{{1}}\\ {{0}}&{{0}}\end{array}\right]}}\\ {{y}}&{{=}}&{{\bar{C}\bar{x}+D u}}\\ {{}}&{{}}&{{=}}&{{\left[\begin{array}{l l}{{1}}&{{0}}\end{array}\right]}}\end{array}$$
= [ *1 0 1]Z+2u* 
$\begin{array}{l}u\\ \begin{array}{cc}0\\ 0\\ -2\end{array}\end{array}$ $x+\left[\begin{array}{cc}1\\ 1\\ 0\end{array}\right]u$  $\begin{array}{l}u\\ \begin{array}{cc}1\end{array}\end{array}$ $\begin{array}{cc}\bar{x}+2u\end{array}$
= [; 0 0 ; -2 "].+[a]. 
$$(1.168)$$

The eigenvector matrix of A is 

$$\begin{array}{r c l}{{M}}&{{=}}&{{\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right]}}\\ {{}}&{{=}}&{{\left[\begin{array}{l}{{}}\\ {{}}\\ {{}}\end{array}\right]}}\end{array}$$
M = [ 'u1 **'u2 'un** ] 
$$\left[\begin{array}{l l l}{v_{1}}&{v_{2}}&{v_{n}}\end{array}\right]$$ $$\left[\begin{array}{l l l}{1}&{0}&{1}\\ {0}&{1}&{3}\\ {0}&{0}&{-3}\end{array}\right]$$
$$(1.169)$$

Note the equivalences 

$$\begin{array}{l}{{M^{-1}A M}}\\ {{M^{-1}B}}\\ {{C M}}\end{array}$$
$$\begin{array}{r l}{{\bar{A}}}&{{}=}\\ {\bar{B}}&{{}=}\\ {\bar{C}}&{{}=}\end{array}$$
A = *M-~AM* 
B = *M-~B* 
C' = CM 
$$(1.170)$$

The Jordan form system has two decoupled modes. The first mode is 

Y1 = [ *1 0151* 
$$\begin{array}{r c l}{{\dot{\bar{x}}_{1}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{0}}\end{array}\right]}}\\ {{y_{1}}}&{{=}}&{{\left[\begin{array}{l}{{1}}\\ {{1}}\end{array}\right]}}\end{array}$$
$$\begin{array}{l}{{1\ \ }}\\ {{1\ \ }}\end{array}\Biggr]\,\bar{x}_{1}+\left[\begin{array}{l}{{1\ \ }}\\ {{1\ \ }}\end{array}\right]u$$ $$0\ \ \Bigr]\,\bar{x}_{1}$$
$1 = [o 11- l]xl+[;]u 
$$(1.171)$$
The second mode is 

$$\begin{array}{l}{{-2\bar{x}_{2}+0\,u}}\\ {{\bar{x}_{2}}}\end{array}$$
$$\begin{array}{r l}{{\dot{\bar{x}}}_{2}}&{{}=}\\ {y_{2}}&{{}=}\end{array}$$
52 = *-252+0u* 
92 = 52 
$$(1.172)$$

vvv Definition 9 If a system is controllable or *stable, then it is also stabilizable. If* a system is uncontrollable OT unstable, then it is stabilizable if its uncontrollable modes are stable. 

In Example 1.10, the first mode is unstable (both eigenvalues at +1) but controllable. The second mode is stable (eigenvalue at **-2)** but uncontrollable. Therefore, the system is stabilizable. 

Definition 10 *If a system is observable or stable, then it is also detectable. If a* system is unobservable or unstable, then it is detectable if its unobservable modes are stable. 

In Example 1.10, the first mode is unstable but observable. The second mode is both stable and observable. Therefore, the system is detectable. 

Controllability and observability were introduced by Rudolph Kalman at a conference in 1959 whose proceedings were published in an obscure Mexican journal in 1960 [KalGOb]. The material was also presented at an **IFAC** conference in 1960 [KalGOc] , and finally published in a more widely accessible format in 1963 [Ka163]. 

## 1.8 Summary

In this chapter we have reviewed some of the basic concepts of linear systems theory that are fundamental to many approaches to optimal state estimation. We began with a review of matrix algebra and matrix calculus, which proves to be indispensable in much of the theory of state estimation techniques. For additional information on matrix theory, the reader can refer to several excellent texts [Hor85, Go189, Ber051. We continued in this chapter with a review of linear and nonlinear systems, in both continuous time and discrete time. We regard time as continuous for physical systems, but our simulations and estimation algorithms operate in discrete time because of the popularity of digital computing. We discussed the discretization of continuous-time systems, which is a way of obtaining a discretetime mathematical representation of a continuoustime system. The concept of stability can be used to tell us if a system's states will always remain bounded. Controllability tells us if it is possible to find a control input to force system states to our desired values, and observability tells us if it is possible to determine the initial state of a system on the basis of output measurements. State-space theory in general, and linear systems theory in particular, is a wideranging discipline that is typically covered in a one-semester graduate course, but there is easily enough material to fill up a two-semester course. Many excellent textbooks have been written on the subject, including [Bay99, Che99, KaiOO] and others. A solid understanding of linear systems will provide a firm foundation for further studies in areas such as control theory, estimation theory, and signal processing. 

## Problems

Written exercises 1.1 Find the rank of the matrix 1.2 Find two 2 x 2 matrices A and diagonal, A \# cB for any scalar c, and B such that A \# B, neither A nor B are AB = *BA.* Find the eigenvectors of A and B. Note that they share an eigenvector. Interestingly, every pair of commuting matrices shares at least one eigenvector [Hor85, p. 511. 

1.3 Prove the three identities of Equation (1.26). 

1.4 Find the partial derivative of the trace of AB with respect to A. 

1.5 Consider the matrix 

$$A={\left[\begin{array}{l l}{a}&{b}\\ {b}&{c}\end{array}\right]}$$

Recall that the eigenvalues of A are found by find the roots of the polynomial P(A) = 1x1 - *A[.* Show that *P(A)* = 0. (This is an illustration of the Cayley-
Hamilton theorem [Bay99, Che99, KaiOO] .) 

$${\begin{array}{l l}{\mathbf{\partial}\cdot}&{A}&{A}\\ {\mathbf{\partial}\cdot}&{B}&{A}\end{array}}\right]\left[\begin{array}{l}{A}\\ {C}\end{array}\right]=\left[\begin{array}{l}{0}\\ {I}\end{array}\right]$$

1.6 Suppose that A is invertible and Find B and C in terms of A [Lie67]. 

1.7 metric. 

Show that AB may not be symmetric even though both A and B are sym-

$$A={\left[\begin{array}{l}{a}\\ {b}\end{array}\right]}$$

1.8 Consider the matrix .=I; !A 
L J 
where a, b, and c are real, and a and c are nonnegative. 

a) Compute the solutions of the characteristic polynomial of A to prove that the eigenvalues of A are real. 

b) For what values of b is A positive semidefinite? 

1.g 1.12 Derive the properties of the state transition matrix given in Equation (1.72). 

Suppose that the matrix A has eigenvalues A, and eigenvectors *wi (i* = 
1.10 1, . - . , *n).* What are the eigenvalues and eigenvectors of *-A?* 
Show that leAtl = *elAlt* for any square matrix A. 

1.11 Show that if A = *BA,* then 

$$\left.\begin{array}{l}{{b}}\\ {{c}}\end{array}\right]$$
$${\frac{d|A|}{d t}}=\mathrm{Tr}(B)|A|$$

1.13 The linear position p of an object under constant acceleration is 

$$p=p_{0}+\dot{p}t+\frac{1}{2}\dot{p}t^{2}$$

where po is the initial position of the object. 

T 

a) Define a state vector as z = [ p p p ] and write the state space equs tion h = Az for this system. 

b) Use all three expressions in Equation (1.71) to find the state transition matrix *eAt* for the system. 

c) Prove for the state transition matrix found above that *eAo* = I. 
1.14 Consider the following system matrix. 

$$A={\left[\begin{array}{l l}{1}&{0}\\ {0}&{-1}\end{array}\right]}$$
$$S(t)={\left[\begin{array}{l l}{e^{t}}&{0}\\ {0}&{2e^{-t}}\end{array}\right]}$$

satisfies the relation *S(t)* = AS(t), but S(t) is not the state transition matrix of the system. 

1.15 Give an example of a discrete-time system that is marginally stable but not asymptotically stable. 

1.16 Show (H, F) is an observable matrix pair if and only if *(H, F-')* is observable 
(assuming that F is nonsingular). 

## Computer Exercises

1.17 The dynamics of a DC motor can be described as 
~e + ~e = T 
where t9 is the angular position of the motor, J is the moment of inertia, F is the coefficient of viscous friction, and T is the torque applied to the motor. 

a) Generate a two-state linear system equation for this motor in the form 

$\mu$, $\nu$. 
X = AX + BU 
b) Simulate the system for 5 s and plot the angular position and velocity. 

Use J = 10 kg m2, F = 100 kg m2/s, z(0) = [ 0 0 ] , and T = 10 N 
m. Use rectangular integration with a step size of 0.05 s. Do the output plots look correct? What happens when you change the step size At to 0.2 s? What happens when you change the step size to 0.5 s? What are the eigenvalues of the A matrix, and how can you relate their magnitudes to the step size that is required for a correct simulation? 

T 
1.18 The dynamic equations for a series RLC circuit can be written as 

$$\begin{array}{r c l}{{u}}&{{=}}&{{I R+L\dot{I}+V_{c}}}\\ {{I}}&{{=}}&{{C\dot{V}_{c}}}\end{array}$$

where u is the applied voltage, I is the current through the circuit, and V, is the voltage across the capacitor. 

a) Write a state-space equation in matrix form for this system with 21 as the capacitor voltage and 22 as the current. 

b) Suppose that R = 3, L = 1, and C = 0.5. Find an analytical expression for the capacitor voltage for t 2 0, assuming that the initial state is zero, and the input voltage is u(t) = e-2t. 

c) Simulate the system using rectangular, trapezoidal, and fourth-order Runge-
Kutta integration to obtain a numerical solution for the capacitor voltage. 

Simulate from t = 0 to t = 5 using step sizes of 0.1 and **0.2.** Tabulate the RMS value of the error between the numerical and analytical solutions for the capacitor voltage for each of your *six* simulations. 

1.19 The vertical dimension of a hovering rocket can be modeled as 

$$\begin{array}{r c l}{{\dot{x}_{1}}}&{{=}}&{{x_{2}}}\\ {{\dot{x}_{2}}}&{{=}}&{{\frac{K u-g x_{2}}{x_{3}}-\frac{G M}{(R+x_{1})^{2}}}}\\ {{\dot{x}_{3}}}&{{=}}&{{-u}}\end{array}$$

where 21 is the vertical position of the rocket, 22 is the vertical velocity, 23 is the mass of the rocket, u is the control input (the **flow** rate of rocket propulsion), 
K = 1000 is the thrust constant of proportionality, g = 50 is the drag constant, G = **6.6733** - 11 m3/kg/s2 is the universal gravitational constant, M = **5.98324** 
kg is the mass of the earth, and R = **6.3736** m is the radius of the earth radius. 

a) Find u(t) = *u~(t)* such that the system is in equilibrium at *q(t)* = 0 and x2(t) = 0. 

b) Find x3(t) when *zl(t)* = 0 and x2(t) = 0. 

c) Linearize the system around the state trajectory found above. 

d) Simulate the nonlinear system for five seconds and the linearized system for five seconds with u(t) = *ug(t)* + Aucos(t). Plot the altitude of the rocket for the nonlinear simulation and the linear simulation (on the same plot) when Au = 10. Repeat for Au = 100 and Au = **300.** Hand in your source code and your three plots. What do you conclude about the accuracy of your linearization? 