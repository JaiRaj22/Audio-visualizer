# Real-Time Microphone Fourier Transform Applications 🎤

Three different applications for capturing audio from your microphone and visualizing the Fourier Transform in real-time!

## 🔧 Installation

You need to install PyAudio (for microphone access) along with the other libraries:

### Windows:
```bash
pip install pyaudio numpy matplotlib scipy
```

### Mac:
```bash
brew install portaudio
pip install pyaudio numpy matplotlib scipy
```

### Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio numpy matplotlib scipy --break-system-packages
```

### If PyAudio installation fails:
Try using a pre-built wheel:
```bash
pip install pipwin
pipwin install pyaudio
```

## 📱 Applications

### 1. Real-Time Analyzer (`realtime_mic_fourier.py`)
**Best for:** Quick testing, simple visualization

**What it does:**
- Shows live audio waveform
- Displays full frequency spectrum
- Zoomed view of human voice range (0-2000 Hz)
- Identifies dominant frequency

**Run it:**
```bash
python realtime_mic_fourier.py
```

**Features:**
- ✅ Simple 3-plot display
- ✅ Real-time frequency detection
- ✅ Auto-scaling for better visibility
- ✅ Noise filtering

---

### 2. Advanced Analyzer (`advanced_mic_analyzer.py`)
**Best for:** Musicians, detailed analysis, note detection

**What it does:**
- Everything from the basic version PLUS:
- Musical note detection (identifies which note you're playing/singing!)
- Tuning indicator (shows if you're sharp or flat)
- Spectrogram (shows frequency changes over time)
- Volume meter
- Better peak detection

**Run it:**
```bash
python advanced_mic_analyzer.py
```

**Features:**
- ✅ Musical note identification (C, D, E, F, G, A, B with sharps/flats)
- ✅ Tuning accuracy in cents
- ✅ Spectrogram visualization
- ✅ 4 synchronized plots
- ✅ Perfect for instrument tuning!

**Try this:**
- Whistle or hum a note - it will tell you what note it is!
- Play an instrument and see if you're in tune
- Watch the spectrogram to see how frequencies change

---

### 3. Interval Recorder (`interval_recorder.py`)
**Best for:** Recording and analyzing audio clips at fixed intervals

**What it does:**
- Records audio for a fixed duration (default: 3 seconds)
- Automatically analyzes each recording
- Saves audio files (.wav)
- Saves analysis plots (.png)
- Shows comprehensive Fourier analysis
- Lists top 5 dominant frequencies

**Run it:**
```bash
python interval_recorder.py
```

**Features:**
- ✅ Automatic recording at intervals
- ✅ Saves WAV files with timestamps
- ✅ Saves analysis plots
- ✅ Detailed frequency breakdown
- ✅ Perfect for documenting audio experiments
- ✅ Works like a scientific data logger

**Customize the interval:**
Edit line 10 in the file:
```python
RECORD_SECONDS = 3  # Change to 5, 10, etc.
```

---

## 🎯 Which One Should I Use?

| Use Case | Recommended App |
|----------|----------------|
| Just want to see frequencies live | `realtime_mic_fourier.py` |
| Tuning an instrument | `advanced_mic_analyzer.py` |
| Analyzing singing/voice | `advanced_mic_analyzer.py` |
| Recording audio samples for analysis | `interval_recorder.py` |
| Educational demo of Fourier Transform | `realtime_mic_fourier.py` |
| Music practice/training | `advanced_mic_analyzer.py` |
| Scientific experiments | `interval_recorder.py` |

---

## 🔊 Usage Tips

### Getting the best results:

1. **Microphone position:** Keep it 6-12 inches from the sound source
2. **Reduce noise:** Close windows, turn off fans/AC
3. **Test your mic first:** Make sure it's working in your system settings
4. **Volume:** Speak/play at normal volume (not too loud, not too quiet)
5. **Single sounds:** Works best with one clear sound at a time

### What to try:

- **Whistle** - You'll see a clean, single frequency peak
- **Hum different notes** - Watch the frequency change
- **Say "Aaaah"** - See the harmonics (multiple peaks)
- **Play a musical instrument** - Identify the note
- **Tap on a glass** - See the resonant frequency
- **Clap** - See a brief burst across many frequencies

---

## 🎼 Understanding the Display

### Time Domain (Waveform)
- Shows the raw audio signal over time
- Up and down waves = sound vibrations
- Bigger waves = louder sound

### Frequency Spectrum (Fourier Transform)
- Shows WHICH frequencies are present
- X-axis = frequency (Hz)
- Y-axis = how strong that frequency is
- Peaks = dominant frequencies in the sound

### Spectrogram (Advanced version only)
- Shows how frequencies change over TIME
- X-axis = time
- Y-axis = frequency
- Color brightness = frequency strength
- Great for seeing melodies, pitch changes

### Musical Notes (Advanced version only)
- Converts frequency to musical note names
- Shows octave number (e.g., A4 = 440 Hz)
- "Cents" = fine-tuning (100 cents = 1 semitone)
- Within ±10 cents = perfectly in tune!

---

## 🎵 Musical Note Reference

| Note | Frequency (Hz) | Note | Frequency (Hz) |
|------|---------------|------|---------------|
| C4   | 261.63        | C5   | 523.25        |
| D4   | 293.66        | D5   | 587.33        |
| E4   | 329.63        | E5   | 659.25        |
| F4   | 349.23        | F5   | 698.46        |
| G4   | 392.00        | G5   | 783.99        |
| A4   | 440.00        | A5   | 880.00        |
| B4   | 493.88        | B5   | 987.77        |

**Note:** A4 (440 Hz) is the standard tuning reference

---

## ⚙️ Customization

### Change the recording length (interval_recorder.py):
```python
RECORD_SECONDS = 5  # Record for 5 seconds instead
```

### Change frequency range to display:
```python
ax2.set_xlim(0, 5000)  # Show 0-5000 Hz instead of 0-2000 Hz
```

### Adjust sensitivity:
```python
CHUNK = 4096  # Larger = better frequency resolution, slower updates
CHUNK = 1024  # Smaller = faster updates, lower resolution
```

### Change sample rate:
```python
RATE = 48000  # Higher = better quality, more CPU
RATE = 22050  # Lower = faster, less CPU
```

---

## 🐛 Troubleshooting

### "No module named 'pyaudio'"
- Install PyAudio using the installation instructions above
- On Windows, try: `pip install pipwin` then `pipwin install pyaudio`

### "Error opening microphone"
- Check microphone permissions in your system settings
- Make sure your microphone is plugged in
- Try selecting a different device (check the list when program starts)

### "Input overflowed"
- This is normal and usually harmless
- Reduce your microphone input volume
- Move mic further from sound source

### Application freezes or crashes
- Close the window and restart
- Reduce CHUNK size for faster processing
- Check if other apps are using the microphone

### No plots showing
- Make sure matplotlib backend is installed
- Try: `pip install pyqt5`
- Or: `pip install tkinter`

### Can't see any frequencies
- Check if sound is actually reaching the microphone
- Increase volume or move closer
- Make a louder sound (whistle, clap)

---

## 📚 Learning Resources

### Understanding Fourier Transform:
- 3Blue1Brown's video: "But what is the Fourier Transform?"
- Interactive tutorial: betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/

### Audio DSP Basics:
- Digital Signal Processing: theory and practice
- Nyquist frequency: Why we sample at 44,100 Hz

### Python Audio:
- PyAudio documentation: people.csail.mit.edu/hubert/pyaudio/
- NumPy FFT documentation: numpy.org/doc/stable/reference/routines.fft.html

---

## 🚀 Advanced Projects to Try

Once you're comfortable with these apps, try:

1. **Add recording capabilities** to the real-time analyzer
2. **Create a pitch-tracking game** (sing and follow a melody)
3. **Build a voice-controlled application** (detect specific frequencies)
4. **Make a basic tuner app** for your instrument
5. **Analyze and compare different musical instruments**
6. **Create a "sound fingerprint"** for different voices
7. **Build a real-time auto-tune effect**
8. **Detect beats and tempo** in music

---

## 📝 Technical Details

### Audio Parameters:
- **CHUNK**: Number of samples per frame (2048 typical)
- **FORMAT**: Audio bit depth (16-bit = pyaudio.paInt16)
- **CHANNELS**: 1 = mono, 2 = stereo
- **RATE**: Sample rate (44,100 Hz = CD quality)

### FFT Details:
- Uses NumPy's Fast Fourier Transform (FFT)
- Applies Hamming window to reduce spectral leakage
- Frequency resolution = RATE / CHUNK
- Maximum detectable frequency = RATE / 2 (Nyquist limit)

### Performance:
- Real-time processing: ~50ms update interval
- CPU usage: 5-15% on modern processors
- Memory: ~50MB typical

---

## ❓ FAQ

**Q: Can I use this with recorded audio files?**
A: The interval recorder saves WAV files. You can modify the code to read from files instead of mic.

**Q: Why 44,100 Hz sample rate?**
A: This is CD-quality audio, can capture frequencies up to 22,050 Hz (above human hearing).

**Q: What's the lowest frequency it can detect?**
A: About 20-30 Hz, limited by CHUNK size and window length.

**Q: Can it detect multiple notes at once?**
A: Yes! The spectrum will show multiple peaks. The advanced version highlights the strongest one.

**Q: Is this accurate enough for professional music production?**
A: It's great for learning and basic tuning. Professional apps have more sophisticated algorithms.

---

## 🎉 Have Fun!

These tools are perfect for:
- 🎸 Musicians learning their instruments
- 🎤 Singers working on pitch
- 👨‍🏫 Teachers demonstrating sound waves
- 🔬 Students studying physics/acoustics
- 🎮 Game developers working with audio
- 🤓 Anyone curious about the science of sound!

**Happy analyzing!** 🎵📊

---

*Created with ❤️ using Python, NumPy, Matplotlib, and PyAudio*
