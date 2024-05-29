import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count

# Parameters
num_channels = 8
sampling_rate = 250  # Hz
duration = 10  # seconds
num_samples = sampling_rate * duration

# Time vector for one second of data
t = np.linspace(0, 1, sampling_rate)

# Generate initial synthetic EMG signals for one second
def generate_emg_signal(t):
    noise = np.random.normal(0, 0.1, len(t))
    muscle_activity = np.sin(2 * np.pi * 10 * t) * (np.random.rand(len(t)) > 0.98)
    return noise + muscle_activity

# Initialize EMG signals
emg_signals = np.array([generate_emg_signal(t) for _ in range(num_channels)])

# Set up the plot
fig, axes = plt.subplots(num_channels, 1, figsize=(10, 8), sharex=True)
lines = []
for i in range(num_channels):
    line, = axes[i].plot(t, emg_signals[i])
    lines.append(line)
    axes[i].set_ylabel(f'Channel {i+1}')
axes[-1].set_xlabel('Time (s)')
plt.tight_layout()

# Update function for animation
def update(frame):
    global emg_signals
    new_signals = np.array([generate_emg_signal(t) for _ in range(num_channels)])
    for i in range(num_channels):
        emg_signals[i] = np.roll(emg_signals[i], -len(t))
        emg_signals[i][-len(t):] = new_signals[i]
        lines[i].set_ydata(emg_signals[i])
    return lines

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=count(), blit=True, interval=1000/sampling_rate * len(t), repeat=False)

plt.show()
