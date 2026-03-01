#!/usr/bin/env python3
"""
Interactive shape editor for Problem 2 diagram.
Fast version - no real-time shading computation.
Displays coordinates on screen for easy capture.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import numpy as np

# Shape parameters
shapes = {
    'A': {'x': 0.5, 'y': 1.3, 'base': 1.0, 'height': 1.5},
    'B': {'x': 1.7, 'y': 1.5, 'width': 1.66, 'height': 1.0},
    'D': {'x': 1.5, 'y': 0.8, 'radius': 0.8},
    'C': {'x': 2.2, 'y': 0.7, 'radius': 0.5},
}

selected_shape = None
offset = (0, 0)

fig, ax = plt.subplots(figsize=(12, 9))
plt.subplots_adjust(bottom=0.35, right=0.75)

# Text display for coordinates
coord_text = None

def draw():
    global coord_text
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 4)
    ax.grid(True, alpha=0.3)
    ax.set_title('Drag shapes to position. Values shown on right.')

    # A - Triangle (isoceles)
    s = shapes['A']
    tri_x = [s['x'] - s['base']/2, s['x'] + s['base']/2, s['x'], s['x'] - s['base']/2]
    tri_y = [s['y'], s['y'], s['y'] + s['height'], s['y']]
    ax.plot(tri_x, tri_y, 'b-', linewidth=2)
    ax.fill(tri_x, tri_y, alpha=0.1, color='blue')
    ax.text(s['x'] - 0.3, s['y'] + s['height']/2, 'A', fontsize=14, fontweight='bold')

    # B - Rectangle
    s = shapes['B']
    rect = patches.Rectangle((s['x'], s['y']), s['width'], s['height'],
                               linewidth=2, edgecolor='blue', facecolor='blue', alpha=0.1)
    ax.add_patch(rect)
    ax.text(s['x'] + s['width'] - 0.2, s['y'] + s['height'] - 0.15, 'B', fontsize=14, fontweight='bold')

    # D - Circle
    s = shapes['D']
    circle = plt.Circle((s['x'], s['y']), s['radius'], linewidth=2,
                         edgecolor='blue', facecolor='blue', alpha=0.1)
    ax.add_patch(circle)
    ax.text(s['x'] - s['radius'] - 0.3, s['y'] - s['radius'], 'D', fontsize=14, fontweight='bold')

    # C - Hexagon
    s = shapes['C']
    angles = np.linspace(0, 2*np.pi, 7)
    hex_x = s['x'] + s['radius'] * np.cos(angles)
    hex_y = s['y'] + s['radius'] * np.sin(angles)
    ax.plot(hex_x, hex_y, 'b-', linewidth=2)
    ax.fill(hex_x, hex_y, alpha=0.1, color='blue')
    ax.text(s['x'], s['y'], 'C', fontsize=14, fontweight='bold', ha='center', va='center')

    # Display coordinates on the plot
    info = "=== SHAPE PARAMETERS ===\n\n"

    s = shapes['A']
    info += f"A (Triangle):\n"
    info += f"  x = {s['x']:.3f}\n"
    info += f"  y = {s['y']:.3f}\n"
    info += f"  base = {s['base']:.3f}\n"
    info += f"  height = {s['height']:.3f}\n\n"

    s = shapes['B']
    info += f"B (Rectangle):\n"
    info += f"  x = {s['x']:.3f}\n"
    info += f"  y = {s['y']:.3f}\n"
    info += f"  width = {s['width']:.3f}\n"
    info += f"  height = {s['height']:.3f}\n\n"

    s = shapes['D']
    info += f"D (Circle):\n"
    info += f"  x = {s['x']:.3f}\n"
    info += f"  y = {s['y']:.3f}\n"
    info += f"  radius = {s['radius']:.3f}\n\n"

    s = shapes['C']
    info += f"C (Hexagon):\n"
    info += f"  x = {s['x']:.3f}\n"
    info += f"  y = {s['y']:.3f}\n"
    info += f"  radius = {s['radius']:.3f}\n"

    # Add text box on the right side
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
    ax.text(5.2, 3.5, info, transform=ax.transData, fontsize=10,
            verticalalignment='top', fontfamily='monospace', bbox=props)

    fig.canvas.draw_idle()

def find_shape_at(x, y):
    # Check triangle
    s = shapes['A']
    # Simple bounding box check for triangle
    if (s['x'] - s['base']/2 <= x <= s['x'] + s['base']/2 and
        s['y'] <= y <= s['y'] + s['height']):
        return 'A'

    # Check rectangle
    s = shapes['B']
    if s['x'] <= x <= s['x'] + s['width'] and s['y'] <= y <= s['y'] + s['height']:
        return 'B'

    # Check circle
    s = shapes['D']
    if (x - s['x'])**2 + (y - s['y'])**2 <= s['radius']**2:
        return 'D'

    # Check hexagon (approximate as circle)
    s = shapes['C']
    if (x - s['x'])**2 + (y - s['y'])**2 <= s['radius']**2:
        return 'C'

    return None

def on_press(event):
    global selected_shape, offset
    if event.inaxes != ax:
        return
    shape = find_shape_at(event.xdata, event.ydata)
    if shape:
        selected_shape = shape
        offset = (shapes[shape]['x'] - event.xdata, shapes[shape]['y'] - event.ydata)

def on_release(event):
    global selected_shape
    selected_shape = None

def on_motion(event):
    if selected_shape is None or event.inaxes != ax:
        return
    shapes[selected_shape]['x'] = event.xdata + offset[0]
    shapes[selected_shape]['y'] = event.ydata + offset[1]
    draw()

# Create sliders
slider_color = 'lightgoldenrodyellow'

# Row 1: A controls
ax_a_base = plt.axes([0.1, 0.22, 0.35, 0.03], facecolor=slider_color)
ax_a_height = plt.axes([0.55, 0.22, 0.35, 0.03], facecolor=slider_color)
slider_a_base = Slider(ax_a_base, 'A base', 0.3, 3.0, valinit=shapes['A']['base'])
slider_a_height = Slider(ax_a_height, 'A height', 0.3, 3.0, valinit=shapes['A']['height'])

# Row 2: B controls
ax_b_width = plt.axes([0.1, 0.17, 0.35, 0.03], facecolor=slider_color)
ax_b_height = plt.axes([0.55, 0.17, 0.35, 0.03], facecolor=slider_color)
slider_b_width = Slider(ax_b_width, 'B width', 0.3, 3.0, valinit=shapes['B']['width'])
slider_b_height = Slider(ax_b_height, 'B height', 0.3, 3.0, valinit=shapes['B']['height'])

# Row 3: D and C radius
ax_d_radius = plt.axes([0.1, 0.12, 0.35, 0.03], facecolor=slider_color)
ax_c_radius = plt.axes([0.55, 0.12, 0.35, 0.03], facecolor=slider_color)
slider_d_radius = Slider(ax_d_radius, 'D radius', 0.2, 2.0, valinit=shapes['D']['radius'])
slider_c_radius = Slider(ax_c_radius, 'C radius', 0.1, 1.5, valinit=shapes['C']['radius'])

def update_a_base(val):
    shapes['A']['base'] = val
    draw()
def update_a_height(val):
    shapes['A']['height'] = val
    draw()
def update_b_width(val):
    shapes['B']['width'] = val
    draw()
def update_b_height(val):
    shapes['B']['height'] = val
    draw()
def update_d_radius(val):
    shapes['D']['radius'] = val
    draw()
def update_c_radius(val):
    shapes['C']['radius'] = val
    draw()

slider_a_base.on_changed(update_a_base)
slider_a_height.on_changed(update_a_height)
slider_b_width.on_changed(update_b_width)
slider_b_height.on_changed(update_b_height)
slider_d_radius.on_changed(update_d_radius)
slider_c_radius.on_changed(update_c_radius)

# Connect mouse events
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

draw()
plt.show()
