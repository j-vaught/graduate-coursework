# Mini-Project 1. Inverted Pendulum on a Cart.

J.C. Vaught.

The project models an unforced inverted pendulum mounted on a freely translating cart. The pendulum angle $\theta$ is measured clockwise from the upright vertical, the cart coordinate $x$ is positive to the right, and the pendulum mass is treated as a point mass at distance $\ell$ from the pivot. The initial condition is $\theta(0)=5^\circ$ with zero translational and angular velocity.

The nonlinear equations of motion are

$$
(M+m)\ddot{x}+m\ell\cos(\theta)\ddot{\theta}-m\ell\sin(\theta)\dot{\theta}^{2}=0,
$$

and

$$
m\ell\cos(\theta)\ddot{x}+m\ell^{2}\ddot{\theta}+c_{\theta}\dot{\theta}-mg\ell\sin(\theta)=0.
$$

The script `build_mini_project_1.m` builds two editable models. The first solves this nonlinear mass-matrix system directly in Simulink. The second represents the cart, prismatic translation, damped revolute pivot, rigid pendulum length, gravity, and pendulum point mass with Simscape Multibody components. It then simulates both implementations, writes their responses to CSV and MAT files, and exports the required comparison plot and model diagrams.

Run the project from MATLAB with the following command.

```matlab
run("build_mini_project_1.m")
```
