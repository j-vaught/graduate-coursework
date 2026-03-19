# EMCH 792: Optimal State Estimation - Homework 4

## B. Computer Portion

In this homework you will learn how to implement a Linear Kalman Filter in **MATLAB**. All the files that you will need for this homework are in the **ws** folder. You are expected to work inside this folder only. Open **MATLAB** and set the current folder to **ws**, and do the following:

- Start by opening the live script file "HW_4_manual.mlx" using **MATLAB**. This will guide you through the basic implementation of Kalman filter in MATLAB.
- Open the file "HW_4.m" and follow the instructions in the file to solve the following problem:

Consider the mass-spring-damper system shown in the picture above. The state of the system is position and velocity of the mass. Assume that both states are affected by zero mean random fluctuations both with variance of 0.01. Also assume that you can measure the position of the mass with an error with zero mean and variance of 0.01.

1. For m=1kg, b=2.5Nsec/m and k=5.0N/m derive the discrete time system dynamics for Ts = 0.1sec.
2. Set the initial true and estimated state to [0, 0], and the initial error covariance to [1, 0; 0, 2]. Simulate the system for 10 seconds while collecting the true and estimated states, the measurements and the *a priori* and *a posteriori* error covariance. Consider that the input to the system is u = 10 * sin(t).
3. Calculate the mean and standard deviation of the error between the true and estimated state. What can you comment about the calculated values? How does the calculated std compare to the steady state theoretical std from the *a posteriori* error covariance matrix?
4. Plot the true, estimated, and measured position. Plot the true and estimated velocity.
5. Plot the position error and the expected bounds. Plot the velocity error and the expected bounds.
6. Plot the *a priori* and *a posteriori* error covariance (it should look like Figure 5.4, page 134 of the textbook).

---

## Submission Instructions

Your submission must include the following files:

- "HW_4.m" -> The edited MATLAB script with your solutions
- PDF document with the scanned solutions

Upload all files on Blackboard in a single submission.

Make sure that the scripts you submit can run. Do not copy the results that appear in the command window in your scripts and make sure that if you add any comments in your scripts that they follow the proper **MATLAB** syntax. **Scripts that do not run will not be graded.**

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A.1     | 20     |
| A.2     | 20     |
| B.1     | 15     |
| B.2     | 15     |
| B.3     | 15     |
| B.4     | 5      |
| B.5     | 5      |
| B.6     | 5      |
