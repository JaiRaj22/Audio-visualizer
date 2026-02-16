import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Time domain setup
t = np.linspace(0, 2, 1000)
freqs_to_add = [2, 10, 20]  # We'll add these frequencies one by one

# Frequency domain setup
freq = np.fft.fftfreq(len(t), t[1] - t[0])
freq_positive = freq[:len(freq)//2]

# Initialize empty signal
signal = np.zeros_like(t)

# Plot setup
line1, = ax1.plot(t, signal, 'b-', linewidth=2)
ax1.set_xlim(0, 2)
ax1.set_ylim(-3, 3)
ax1.set_xlabel('Time (seconds)', fontsize=12)
ax1.set_ylabel('Amplitude', fontsize=12)
ax1.set_title('Time Domain: Building a Complex Signal', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

line2, = ax2.plot(freq_positive, np.zeros_like(freq_positive), 'r-', linewidth=2)
ax2.set_xlim(0, 15)
ax2.set_ylim(0, 600)
ax2.set_xlabel('Frequency (Hz)', fontsize=12)
ax2.set_ylabel('Magnitude', fontsize=12)
ax2.set_title('Frequency Domain: Fourier Transform', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Text to show which frequencies are added
text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, 
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

def animate(frame):
    global signal
    
    # Add frequencies gradually
    if frame < 30:  # Add first frequency
        progress = frame / 30
        signal = progress * np.sin(2 * np.pi * freqs_to_add[0] * t)
        text.set_text(f'Adding {freqs_to_add[0]} Hz')
    elif frame < 60:  # Add second frequency
        progress = (frame - 30) / 30
        signal = np.sin(2 * np.pi * freqs_to_add[0] * t) + \
                 progress * 0.7 * np.sin(2 * np.pi * freqs_to_add[1] * t)
        text.set_text(f'Adding {freqs_to_add[0]} Hz + {freqs_to_add[1]} Hz')
    else:  # Add third frequency
        progress = min((frame - 60) / 30, 1)
        signal = np.sin(2 * np.pi * freqs_to_add[0] * t) + \
                 0.7 * np.sin(2 * np.pi * freqs_to_add[1] * t) + \
                 progress * 0.5 * np.sin(2 * np.pi * freqs_to_add[2] * t)
        text.set_text(f'Adding {freqs_to_add[0]} Hz + {freqs_to_add[1]} Hz + {freqs_to_add[2]} Hz')
    
    # Update time domain
    line1.set_ydata(signal)
    
    # Calculate and update Fourier Transform
    fft_values = np.fft.fft(signal)
    fft_magnitude = np.abs(fft_values[:len(fft_values)//2])
    line2.set_ydata(fft_magnitude)
    
    return line1, line2, text

# Create animation
anim = FuncAnimation(fig, animate, frames=90, interval=50, blit=True, repeat=True)

plt.tight_layout()
plt.show()