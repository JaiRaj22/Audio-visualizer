import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import signal

# Generate a signal with changing frequencies (like a chirp)
duration = 4  # seconds
sample_rate = 1000  # Hz
t = np.linspace(0, duration, duration * sample_rate)

# Create a signal that changes frequency over time
# Plus some constant tones
freq1 = 50 + 100 * (t / duration)  # Chirp from 50 to 150 Hz
freq2 = 200  # Constant tone
signal_wave = (np.sin(2 * np.pi * freq1 * t) + 
               0.5 * np.sin(2 * np.pi * freq2 * t) +
               0.3 * np.sin(2 * np.pi * 75 * t))

# Calculate spectrogram
f, t_spec, Sxx = signal.spectrogram(signal_wave, sample_rate, nperseg=256)

# Setup figure
fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.5])

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

# Plot 1: Time domain signal
line1, = ax1.plot([], [], 'b-', linewidth=1.5)
vline1 = ax1.axvline(x=0, color='r', linestyle='--', linewidth=2)
ax1.set_xlim(0, duration)
ax1.set_ylim(-2, 2)
ax1.set_xlabel('Time (seconds)', fontsize=11)
ax1.set_ylabel('Amplitude', fontsize=11)
ax1.set_title('Signal in Time Domain', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Plot 2: Current frequency spectrum
line2, = ax2.plot([], [], 'r-', linewidth=2)
ax2.set_xlim(0, 300)
ax2.set_ylim(0, 1)
ax2.set_xlabel('Frequency (Hz)', fontsize=11)
ax2.set_ylabel('Magnitude', fontsize=11)
ax2.set_title('Current Frequency Spectrum (Fourier Transform)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Plot 3: Spectrogram (frequency over time)
spectrogram_img = ax3.imshow(10 * np.log10(Sxx), aspect='auto', origin='lower',
                              extent=[t_spec[0], t_spec[-1], f[0], f[-1]],
                              cmap='viridis', vmax=np.max(10 * np.log10(Sxx)))
vline3 = ax3.axvline(x=0, color='r', linestyle='--', linewidth=2)
ax3.set_xlim(0, duration)
ax3.set_ylim(0, 300)
ax3.set_xlabel('Time (seconds)', fontsize=11)
ax3.set_ylabel('Frequency (Hz)', fontsize=11)
ax3.set_title('Spectrogram (Frequency vs Time)', fontsize=13, fontweight='bold')
cbar = plt.colorbar(spectrogram_img, ax=ax3)
cbar.set_label('Power (dB)', fontsize=10)

# Window size for FFT
window_size = 1000  # samples

def animate(frame):
    # Current time
    current_time = t[frame * 50] if frame * 50 < len(t) else t[-1]
    current_idx = min(frame * 50, len(t) - 1)
    
    # Update time domain plot (show a moving window)
    start_idx = max(0, current_idx - 2000)
    end_idx = min(len(t), current_idx + 500)
    line1.set_data(t[start_idx:end_idx], signal_wave[start_idx:end_idx])
    vline1.set_xdata([current_time])
    
    # Calculate FFT for current window
    start_window = max(0, current_idx - window_size // 2)
    end_window = min(len(signal_wave), current_idx + window_size // 2)
    window_signal = signal_wave[start_window:end_window]
    
    if len(window_signal) > 0:
        # Pad if necessary
        if len(window_signal) < window_size:
            window_signal = np.pad(window_signal, 
                                  (0, window_size - len(window_signal)), 
                                  'constant')
        
        # Compute FFT
        fft_values = np.fft.fft(window_signal)
        fft_freq = np.fft.fftfreq(len(window_signal), 1/sample_rate)
        
        # Take only positive frequencies
        positive_freq_idx = fft_freq > 0
        fft_freq_positive = fft_freq[positive_freq_idx]
        fft_magnitude = np.abs(fft_values[positive_freq_idx])
        
        # Normalize
        fft_magnitude = fft_magnitude / np.max(fft_magnitude) if np.max(fft_magnitude) > 0 else fft_magnitude
        
        # Update frequency plot
        line2.set_data(fft_freq_positive, fft_magnitude)
    
    # Update spectrogram vertical line
    vline3.set_xdata([current_time])
    
    return line1, vline1, line2, vline3

# Create animation
total_frames = len(t) // 50
anim = FuncAnimation(fig, animate, frames=total_frames, interval=50, blit=True, repeat=True)

plt.tight_layout()
plt.show()