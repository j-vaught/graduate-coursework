#import "../figures/dynamics.typ": coordinates, drag

= Hull dynamics

The simulator advances a planar hull state from body-frame velocities and two independently commanded propulsors. This chapter defines its coordinate convention, derives the implemented equations, and relates the linear baseline to the nonlinear hull model.

== Frames and state

The inertial frame uses east $E$ and north $N$ position coordinates. The body frame uses forward $x_b$ and port/left $y_b$ axes, with heading $psi$ measured counterclockwise from east. Consequently, a zero-heading boat points east, while a positive heading rotates its forward axis toward north. Surge $u$, sway $v$, and yaw rate $r$ are body-frame velocities. The six-state hull vector is $eta=(E,N,psi)$ and $nu=(u,v,r)$.

#figure(coordinates(), caption: [Body forward and left axes rotate with heading, while east and north remain fixed.]) <dyn-coordinates>

That convention fixes both the position rotation and the sign of differential thrust. The exact kinematic relation is

$
  dot(E) = cos(psi) u - sin(psi) v, quad
  dot(N) = sin(psi) u + cos(psi) v, quad
  dot(psi) = r.
$

In matrix form, $dot(eta)=J(psi)nu$, where the planar rotation block is

$
  J(psi) = mat(cos(psi), -sin(psi), 0; sin(psi), cos(psi), 0; 0, 0, 1).
$

The two frames keep position and velocity descriptions consistent as the craft turns.

- The earth frame records where the hull is, while the body frame records how it moves relative to its own axes.
  - Surge is forward and sway is left, so the body axes rotate together with heading.
  - Applying $J(psi)$ resolves these velocities into east and north components at every step.
- Heading is positive counterclockwise from east.
  - At $psi=0$, forward points east; at positive $psi$, forward has a northward component.
  - This sign convention makes positive yaw and a larger starboard thrust produce a counterclockwise turn.

== Nonlinear planar force balance

The force model follows the standard marine-craft decomposition of inertia, velocity coupling, damping, and applied effort. Here each term is specified by the implementation and configuration; the general modeling framework is consistent with Fossen's marine craft formulation @Fossen2026MarineModel.

The effective diagonal inertia is $M="diag"(m_x,m_y,I_z)$. The nominal rigid-body yaw inertia is $I$, while $I_z$ denotes its effective value after the optional added-inertia contribution. With rigid-body mass $m$ and added-mass flag $a in {0,1}$, code sets

$
 m_x=m(1+0.10a), quad m_y=m(1+0.50a), quad I_z=I(1+0.20a).
$

The implemented velocity-coupling vector added on the right-hand side is $c(nu)=(m_y v r,-m_x u r,(m_x-m_y) u v)^T$. Under the conventional left-hand-side form $M dot(nu)+C(nu)nu=tau$, this is $c(nu)=-C(nu)nu$. Its structure exchanges energy between surge, sway, and yaw without adding or removing total kinetic energy, since

$
  nu^T c(nu) = u m_y v r - v m_x u r + r(m_x-m_y) u v = 0.
$

This cancellation is a useful structural check on the cross-coupling signs. The model's body-frame equations are

$
  m_x dot(u) = T_p + T_s + m_y v r - D_u(u) + tau_u.
$

$
  m_y dot(v) = -m_x u r - D_v(v) + tau_v.
$

$
  I_z dot(r) = b/2 (T_s - T_p) + (m_x - m_y) u v - D_r(r) + tau_r.
$

Here $T_p$ and $T_s$ are port and starboard thrust in newtons, $b$ is their lateral separation, and $(tau_u,tau_v,tau_r)$ denotes environmental surge force, sway force, and yaw moment in body coordinates. Positive differential effort means starboard thrust exceeds port thrust and therefore produces positive, counterclockwise yaw.

The drag laws are signed so that they oppose velocity. In nonlinear mode they are

$
 D_u(u)=d_1u+d_2u|u|, quad
 D_v(v)=d_v v+k_v v |v|, quad
 D_r(r)=d_r r+k_r r |r|.
$

Configuration defaults set $k_v=k_r=0$. Thus default lateral and yaw drag are linear, while surge drag combines linear and quadratic terms. The quadratic surge term captures increasing resistance with speed while retaining the correct sign in reverse.

#figure(drag(), caption: [The straight-line approximation matches nonlinear surge drag and slope at the one-meter-per-second operating point.]) <dyn-drag>

== Hull and coefficient values

The numeric hull begins with the 1.2 m length and 0.93 m beam of the configured platform. The implementation computes a 21.9 kg rigid-body mass as 14.5 kg bare hull plus 2.4 kg for two batteries and a 5.0 kg equipment allowance. The nominal yaw inertia uses a uniform rectangular-envelope approximation, $I=m(L^2+B^2)/12=4.2064425$ kg m². This is a geometry-based modeling choice, not a measured mass distribution. Thruster spacing is configured as $b=0.75$ m.

The configured values combine platform dimensions, mass accounting, and assumed resistance coefficients.

- Platform geometry and mass determine the rigid-body terms.
  - The 1.2 m length, 0.93 m beam, 14.5 kg bare hull, and 2.4 kg battery total are platform specifications; the 5.0 kg equipment allowance is a configuration assumption.
  - Together they produce $m=21.9$ kg; the 0.75 m thruster separation is also a configuration assumption.
- The inertia proxy converts the platform envelope into yaw resistance.
  - The model uses $I=m(L^2+B^2)/12=4.2064425$ kg m², giving $I_z=I$ when added mass is off.
  - With added mass on, the configured fractions give $m_x=24.09$ kg, $m_y=32.85$ kg, and $I_z=5.047731$ kg m².
- Drag coefficients set the resistance used by the hull equations.
  - The assumed surge terms are $d_1=4$ N s/m and $d_2=10$ N s²/m²; sway and yaw use $d_v=35$ N s/m and $d_r=12$ N m s.
  - The configuration defaults omit quadratic sway and yaw drag, so $k_v=k_r=0$.

Thrust allocation maps the two motors to generalized effort as

$
  tau_T = mat(1, 1; 0, 0; -b/2, b/2) mat(T_p; T_s).
$

At $b=0.75$ m, equal thrust changes surge without yaw, while an equal-and-opposite change creates yaw with no net surge. Installed thrust is based on a signed static motor curve scaled so the pair reaches the platform's stated 8.2 kgf forward maximum. Reverse scaling and between-point values remain assumptions in that map; the hull force equations themselves consume thrust in newtons.

== Local linear model and feature switches

The initial configuration holds $U=1$ m/s and $psi_0=0$. The nominal position evolves as $E_0(t)=U t$ and $N_0(t)=0$, so $tilde(E)=E-E_0(t)$ and $tilde(N)=N-N_0(t)$ describe departures from that moving reference. For small velocity and heading perturbations $tilde(u),tilde(v),tilde(r),tilde(psi)$, with trim thrust balancing drag, the linearized equations are

$
  dot(tilde(E)) = tilde(u).
$

$
  dot(tilde(N)) = tilde(v) + U tilde(psi).
$

$
  dot(tilde(psi)) = tilde(r).
$

$
  dot(tilde(u)) = -((d_1 + 2 d_2 U)/m_x) tilde(u) + (tilde(T_p) + tilde(T_s))/m_x.
$

$
  dot(tilde(v)) = -(d_v/m_y) tilde(v) - (m_x U/m_y) tilde(r).
$

$
  dot(tilde(r)) = ((m_x - m_y) U/I_z) tilde(v) - (d_r/I_z) tilde(r) + b(tilde(T_s) - tilde(T_p))/(2 I_z).
$

These equations give a readable state-space model $dot(tilde(x))=A tilde(x)+B tilde(T)$ for $tilde(x)=(tilde(E),tilde(N),tilde(psi),tilde(u),tilde(v),tilde(r))$ and $tilde(T)=(tilde(T_p),tilde(T_s))$. For the default no-added-mass coefficients, the nonzero entries of $A$ are $A_{E,u}=1$, $A_{N,v}=1$, $A_{N,psi}=U=1$ m/s, $A_{psi,r}=1$, $A_{u,u}=-1.0959$ s⁻¹, and $A_{v,v}=-1.5982$ s⁻¹, $A_{v,r}=-1.0000$ m/s, $A_{r,r}=-2.8523$ s⁻¹. The input matrix rows for $u$ are $(0.04566,0.04566)$ kg⁻¹; rows for $r$ are $(-0.08915,0.08915)$ with units kg⁻¹ m⁻¹. All other entries of $A$ are zero.

The feature flags select whether this local approximation or the corresponding nonlinear relation supplies each component.

- `nonlinear_kinematics` switches from the local position approximation to exact rotation at the current heading. At heading zero it uses lateral velocity $v+U(psi-psi_0)$, retaining the first-order effect of heading on cross-track motion.
  - Near $U=1$ m/s and small heading error, this agrees to first order with exact rotation. Large heading changes require the nonlinear rotation.
- `nonlinear_coupling` replaces the constant-speed linear terms $(-m_x U r,(m_x-m_y)U v)$ with the full state-dependent terms $(m_y v r,-m_x u r,(m_x-m_y) u v)$.
  - The local coupling evaluates sway/yaw cross terms at trim speed $U$ and discards nonlinear state products.
- `nonlinear_drag` replaces the tangent drag law around $U$ with signed quadratic surge drag and configured sway/yaw quadratic terms.
  - In surge, linear mode evaluates $D_u(U)+(d_1+2d_2|U|)(u-U)$. It is accurate near the trim speed and diverges increasingly from the nonlinear curve farther away.
- `added_mass` scales the diagonal effective inertia by the configured fractions and changes the coupling coefficients through $m_x,m_y,I_z$.

Accordingly, the baseline is a local model for small perturbations around its selected speed and heading. Turning on the `01_hull` preset restores exact position rotation, nonlinear coupling, and nonlinear drag, while preserving the same mass and nominal coefficient choices. These equations describe the implemented hull dynamics; motor response, command timing, sensors, and disturbances are separate simulator layers.
