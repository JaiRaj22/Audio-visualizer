import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def compute_fourier_coefficients(path, num_coefficients):
    """Compute Fourier coefficients for a given path"""
    N = len(path)
    coefficients = []
    
    for n in range(-num_coefficients, num_coefficients + 1):
        coefficient = 0
        for k in range(N):
            coefficient += path[k] * np.exp(-2j * np.pi * n * k / N)
        coefficient /= N
        coefficients.append((n, coefficient))
    
    # Sort by magnitude for better visualization
    coefficients.sort(key=lambda x: abs(x[1]), reverse=True)
    return coefficients

# Create a simple path - a heart shape!
t = np.linspace(0, 2*np.pi, 200)
# Heart equation in parametric form
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
path = x + 1j * y  # Complex representation

# Compute Fourier coefficients
num_circles = 10
coefficients = compute_fourier_coefficients(path, num_circles)

# Setup plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title('Fourier Epicycles Drawing a Heart', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)

# Store drawn path
drawn_path = []
path_line, = ax.plot([], [], 'r-', linewidth=2, alpha=0.7)

# Circle and line objects
circles = []
lines = []
for _ in range(len(coefficients)):
    circle, = ax.plot([], [], 'b-', linewidth=1, alpha=0.4)
    line, = ax.plot([], [], 'g-', linewidth=1.5)
    circles.append(circle)
    lines.append(line)

# Dot at the end
dot, = ax.plot([], [], 'ro', markersize=8)

def animate(frame):
    time = 2 * np.pi * frame / len(t)
    
    # Calculate positions of epicycles
    x_pos, y_pos = 0, 0
    positions = [(0, 0)]
    
    for n, coeff in coefficients:
        # Calculate the rotation
        radius = abs(coeff)
        angle = np.angle(coeff) + n * time
        
        x_new = x_pos + radius * np.cos(angle)
        y_new = y_pos + radius * np.sin(angle)
        
        # Draw circle
        circle_t = np.linspace(0, 2*np.pi, 50)
        circle_x = x_pos + radius * np.cos(circle_t)
        circle_y = y_pos + radius * np.sin(circle_t)
        circles[len(positions)-1].set_data(circle_x, circle_y)
        
        # Draw line from center to edge
        lines[len(positions)-1].set_data([x_pos, x_new], [y_pos, y_new])
        
        x_pos, y_pos = x_new, y_new
        positions.append((x_pos, y_pos))
    
    # Update the dot
    dot.set_data([x_pos], [y_pos])
    
    # Add to drawn path
    drawn_path.append((x_pos, y_pos))
    if len(drawn_path) > len(t):
        drawn_path.pop(0)
    
    # Update drawn path
    if drawn_path:
        path_x, path_y = zip(*drawn_path)
        path_line.set_data(path_x, path_y)
    
    return circles + lines + [dot, path_line]

# Create animation
anim = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=True, repeat=True)

plt.tight_layout()
plt.show()