"""Render the HW6 RPRP manipulator schematic via Peter Corke's Robotics Toolbox."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import RevoluteDH, PrismaticDH

L1, L2, L3 = 1.0, 0.8, 0.6

robot = rtb.DHRobot(
    [
        RevoluteDH(d=L1, a=L2, alpha=np.pi / 2),       # theta_1
        PrismaticDH(theta=0.0, a=0.0, alpha=-np.pi / 2),  # d_2
        RevoluteDH(d=0.0, a=L3, alpha=0.0),            # theta_3
        PrismaticDH(theta=0.0, a=0.0, alpha=0.0),      # d_4
    ],
    name="HW6_RPRP",
)

print(robot)

q = [np.deg2rad(30), 0.4, np.deg2rad(-25), 0.3]

env = robot.plot(
    q,
    backend="pyplot",
    block=False,
    jointaxes=True,
    eeframe=True,
    shadow=True,
    name=True,
)

fig = plt.gcf()
fig.set_size_inches(8, 6)
out_pdf = "/Users/user/Downloads/graduate-coursework/Sp26/EMCH792/HW6/robot_schematic.pdf"
out_png = "/Users/user/Downloads/graduate-coursework/Sp26/EMCH792/HW6/robot_schematic.png"
fig.savefig(out_pdf, bbox_inches="tight")
fig.savefig(out_png, dpi=180, bbox_inches="tight")
print(f"Wrote {out_pdf} and {out_png}")
