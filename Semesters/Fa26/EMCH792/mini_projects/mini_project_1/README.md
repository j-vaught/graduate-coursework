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

The function `build_learning_visuals.m` converts the saved Multibody trajectory into a full-duration animation, a slow-motion first-swing animation, and four explanatory screenshots. The cart-centered camera keeps the mechanism large while the numbered world-position ruler moves beneath the cart to make its translation visible.

Run the learning-visual build from MATLAB with the following command.

```matlab
build_learning_visuals("all")
```

The native Mechanics Explorer version is built into the Simscape Multibody model by `add_multibody_learning_geometry.m`. It adds a slender physical cylindrical rod from the revolute pivot to the bob and a fixed world-frame ruler beneath the cart. All solids use the Simscape library's default color. The function `record_mechanics_explorer_videos.m` uses `smwritevideo` to record the actual Mechanics Explorer playback and uses MATLAB `VideoReader` to save still frames from that recording.

The recorder uses `ffprobe` to count the native frames and `ffmpeg` to wrap MATLAB's Motion JPEG frame stream into MP4. These tools do not reconstruct animation from simulation data; every image originates in the Simscape Multibody renderer.

The primary native recording is `mechanics_explorer_full_motion.mp4`, a 20-second, 1600-by-900 video at 30 frames per second. The file `mechanics_explorer_first_swing_slow_motion.mp4` provides a 16-second slow-motion view of the first eight simulated seconds.

Record the native Multibody visualization from MATLAB with the following command.

```matlab
record_mechanics_explorer_videos("all")
```
