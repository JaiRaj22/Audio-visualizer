import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import struct
from collections import deque

# Audio parameters
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Spectrogram parameters
SPECTROGRAM_WIDTH = 200  # Number of time slices to keep

# Initialize PyAudio
p = pyaudio.PyAudio()

# Check available input devices
print("Available audio input devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"  [{i}] {info['name']}")

# Open microphone stream
try:
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    print("\n🎤 Microphone is active!")
    print("Try whistling, humming, or playing an instrument!")
    print("Close the window to stop.\n")
except Exception as e:
    print(f"Error opening microphone: {e}")
    print("Please check your microphone connection and permissions.")
    exit()

# Musical note detection
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def freq_to_note(freq):
    """Convert frequency to musical note"""
    if freq < 20:
        return "Too low"
    
    # Calculate note number (A4 = 440 Hz is note number 69)
    note_number = 12 * np.log2(freq / 440.0) + 69
    note_number = int(round(note_number))
    
    # Get note name and octave
    note_name = NOTE_NAMES[note_number % 12]
    octave = (note_number // 12) - 1
    
    # Calculate cents off (for tuning)
    exact_note_freq = 440.0 * 2**((note_number - 69) / 12.0)
    cents = 1200 * np.log2(freq / exact_note_freq)
    
    return f"{note_name}{octave}", cents

# Create figure with subplots
fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 1.5, 0.5])

ax1 = fig.add_subplot(gs[0, :])  # Time domain
ax2 = fig.add_subplot(gs[1, :])  # Frequency spectrum
ax3 = fig.add_subplot(gs[2, :])  # Spectrogram
ax4 = fig.add_subplot(gs[3, :])  # Note/info display

fig.suptitle('Advanced Real-Time Audio Analyzer', fontsize=16, fontweight='bold')

# Time domain plot
x_time = np.arange(0, CHUNK) / RATE * 1000  # Convert to milliseconds
line_time, = ax1.plot(x_time, np.zeros(CHUNK), 'b-', linewidth=1)
ax1.set_ylim(-32768, 32768)
ax1.set_xlim(0, x_time[-1])
ax1.set_xlabel('Time (ms)', fontsize=10)
ax1.set_ylabel('Amplitude', fontsize=10)
ax1.set_title('Time Domain Waveform', fontsize=12)
ax1.grid(True, alpha=0.3)

# Frequency spectrum
x_freq = np.fft.fftfreq(CHUNK, 1/RATE)[:CHUNK//2]
line_freq, = ax2.plot(x_freq, np.zeros(CHUNK//2), 'r-', linewidth=1.5)
ax2.set_ylim(0, 100)
ax2.set_xlim(0, 4000)
ax2.set_xlabel('Frequency (Hz)', fontsize=10)
ax2.set_ylabel('Magnitude', fontsize=10)
ax2.set_title('Frequency Spectrum (Fourier Transform)', fontsize=12)
ax2.grid(True, alpha=0.3)

# Vertical line for dominant frequency
vline = ax2.axvline(x=0, color='green', linestyle='--', linewidth=2, alpha=0.7)

# Spectrogram
spectrogram_data = deque(maxlen=SPECTROGRAM_WIDTH)
for _ in range(SPECTROGRAM_WIDTH):
    spectrogram_data.append(np.zeros(CHUNK//2))

spectrogram_array = np.zeros((CHUNK//2, SPECTROGRAM_WIDTH))
spectrogram_img = ax3.imshow(spectrogram_array, aspect='auto', origin='lower',
                              cmap='viridis', interpolation='nearest',
                              extent=[0, SPECTROGRAM_WIDTH, 0, RATE//2])
ax3.set_ylim(0, 4000)
ax3.set_xlabel('Time (frames)', fontsize=10)
ax3.set_ylabel('Frequency (Hz)', fontsize=10)
ax3.set_title('Spectrogram (Frequency over Time)', fontsize=12)

# Info display
ax4.axis('off')
text_info = ax4.text(0.5, 0.5, '', transform=ax4.transAxes,
                     fontsize=14, verticalalignment='center',
                     horizontalalignment='center',
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Volume meter
volume_history = deque(maxlen=50)

def animate(frame):
    try:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        data_int = struct.unpack(str(CHUNK) + 'h', data)
        audio_data = np.array(data_int, dtype='float64')
        
        # Calculate volume (RMS)
        rms = np.sqrt(np.mean(audio_data**2))
        volume_history.append(rms)
        avg_volume = np.mean(volume_history)
        
        # Update time domain
        line_time.set_ydata(audio_data)
        
        # Apply window and compute FFT
        windowed_data = audio_data * np.hamming(CHUNK)
        fft_data = np.fft.fft(windowed_data)
        fft_magnitude = np.abs(fft_data[:CHUNK//2]) / CHUNK
        
        # Smooth the spectrum
        fft_magnitude = np.convolve(fft_magnitude, np.ones(5)/5, mode='same')
        
        # Update frequency spectrum
        line_freq.set_ydata(fft_magnitude)
        
        # Auto-scale
        max_mag = np.max(fft_magnitude)
        if max_mag > 0:
            ax2.set_ylim(0, max_mag * 1.3)
        
        # Find dominant frequency
        threshold = max_mag * 0.4
        if max_mag > avg_volume * 0.1:  # Check if there's significant sound
            peaks_idx = np.where(fft_magnitude > threshold)[0]
            
            if len(peaks_idx) > 0:
                # Get the strongest peak
                dominant_idx = peaks_idx[np.argmax(fft_magnitude[peaks_idx])]
                dominant_freq = x_freq[dominant_idx]
                dominant_mag = fft_magnitude[dominant_idx]
                
                # Update vertical line
                vline.set_xdata([dominant_freq])
                
                # Get musical note
                if dominant_freq > 20 and dominant_freq < 4000:
                    note, cents = freq_to_note(dominant_freq)
                    
                    # Create tuning indicator
                    if abs(cents) < 10:
                        tuning = "🎯 Perfect!"
                    elif cents > 0:
                        tuning = f"↑ {cents:.0f} cents sharp"
                    else:
                        tuning = f"↓ {abs(cents):.0f} cents flat"
                    
                    info_text = (f"🎵 Note: {note}  |  Frequency: {dominant_freq:.1f} Hz\n"
                               f"Tuning: {tuning}  |  Volume: {int(avg_volume)}")
                else:
                    info_text = f"Frequency: {dominant_freq:.1f} Hz  |  Volume: {int(avg_volume)}"
                
                text_info.set_text(info_text)
            else:
                text_info.set_text(f"Listening... Volume: {int(avg_volume)}")
                vline.set_xdata([0])
        else:
            text_info.set_text("🔇 Too quiet or no sound detected")
            vline.set_xdata([0])
        
        # Update spectrogram
        spectrogram_data.append(fft_magnitude)
        spectrogram_array = np.array(spectrogram_data).T
        
        # Apply log scale for better visualization
        spectrogram_log = 20 * np.log10(spectrogram_array + 1e-10)
        spectrogram_img.set_data(spectrogram_log)
        spectrogram_img.set_clim(vmin=np.percentile(spectrogram_log, 10),
                                 vmax=np.percentile(spectrogram_log, 99))
        
    except Exception as e:
        print(f"Error: {e}")
        text_info.set_text(f"Error: {e}")
    
    return line_time, line_freq, vline, spectrogram_img, text_info

# Create animation
anim = FuncAnimation(fig, animate, interval=50, blit=True, cache_frame_data=False)

plt.tight_layout()

# Show plot
try:
    plt.show()
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("✅ Microphone closed. Thanks for using the analyzer! 👋")