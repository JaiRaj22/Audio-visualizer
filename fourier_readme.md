# Fourier Transform Animations in Python

This collection contains 4 different animations that visualize the Fourier Transform in various ways.

## Installation

First, install the required libraries:

```bash
pip install numpy matplotlib scipy --break-system-packages
```

## Animations

### 1. Basic Fourier Transform (`fourier_basic.py`)
**What it shows:** How adding different frequency waves together creates complex signals, and how the Fourier Transform reveals those hidden frequencies.

**Run it:**
```bash
python fourier_basic.py
```

**What you'll see:**
- Top plot: Signal being built by adding sine waves
- Bottom plot: The frequency spectrum showing which frequencies are present

### 2. Epicycles (`fourier_epicycles.py`)
**What it shows:** The famous "drawing with rotating circles" visualization. Circles of different sizes rotate at different speeds, and their combined motion traces out a shape (a heart!).

**Run it:**
```bash
python fourier_epicycles.py
```

**What you'll see:**
- Multiple circles rotating and connected
- The end point traces out a heart shape
- This demonstrates how ANY shape can be created using Fourier series!

### 3. Spectrogram (`fourier_spectrogram.py`)
**What it shows:** How frequency content changes over time. Perfect for understanding audio analysis!

**Run it:**
```bash
python fourier_spectrogram.py
```

**What you'll see:**
- Top: Time-domain signal
- Middle: Current frequency spectrum
- Bottom: Spectrogram showing how frequencies change over time

### 4. 2D Fourier Transform (`fourier_2d.py`)
**What it shows:** Fourier Transform works on images too! This shows how patterns in images translate to the frequency domain.

**Run it:**
```bash
python fourier_2d.py
```

**What you'll see:**
- Top-left: Original image with patterns
- Top-right: 2D Fourier Transform (bright spots show dominant frequencies)
- Bottom: Low and high frequency components separated

## Tips for Learning

1. **Start with `fourier_basic.py`** - it's the easiest to understand
2. **Watch `fourier_epicycles.py`** for the "wow" factor
3. **Study `fourier_spectrogram.py`** to understand audio analysis
4. **Explore `fourier_2d.py`** to see how images are processed

## Customization Ideas

### Modify the frequencies:
In `fourier_basic.py`, change this line:
```python
freqs_to_add = [2, 5, 7]  # Try [1, 3, 5] or [10, 20, 30]
```

### Change the shape in epicycles:
In `fourier_epicycles.py`, modify the path equations:
```python
# For a circle:
x = np.cos(t) * 10
y = np.sin(t) * 10

# For a star:
r = 10 * (1 + 0.5 * np.sin(5*t))
x = r * np.cos(t)
y = r * np.sin(t)
```

### Adjust animation speed:
In any file, change the `interval` parameter:
```python
anim = FuncAnimation(fig, animate, frames=90, interval=50, ...)
# Lower interval = faster animation (interval is in milliseconds)
```

### Change number of epicycles:
In `fourier_epicycles.py`:
```python
num_circles = 10  # Try 5 for simpler, 20 for more detailed
```

## Understanding the Code

### Key numpy.fft functions:
- `np.fft.fft(signal)` - Computes the Fast Fourier Transform
- `np.fft.fftfreq(n, d)` - Generates frequency values for the FFT
- `np.fft.fft2(image)` - 2D FFT for images
- `np.fft.fftshift()` - Shifts zero frequency to center (for visualization)

### Animation with matplotlib:
- `FuncAnimation` - Creates animations by repeatedly calling a function
- `interval` - Time between frames in milliseconds
- `frames` - Total number of animation frames
- `blit=True` - Faster rendering (only updates changed parts)

## Troubleshooting

**Animation is slow:**
- Reduce the number of data points
- Increase the `interval` parameter
- Set `blit=True` in FuncAnimation

**Window doesn't appear:**
- Make sure you have a GUI backend for matplotlib
- Try adding `plt.ion()` before creating the figure

**Import errors:**
- Ensure all packages are installed: `pip install numpy matplotlib scipy --break-system-packages`

## Next Steps

Once you understand these animations, try:
1. Creating your own signal with custom frequencies
2. Loading and analyzing real audio files
3. Processing actual images with 2D FFT
4. Implementing filters (low-pass, high-pass, band-pass)
5. Creating your own custom shapes with epicycles

## Resources

- **Fourier Transform explained:** Look up "3Blue1Brown Fourier Transform" on YouTube
- **NumPy FFT documentation:** https://numpy.org/doc/stable/reference/routines.fft.html
- **SciPy Signal Processing:** https://docs.scipy.org/doc/scipy/reference/signal.html

Happy learning! 🎵📊