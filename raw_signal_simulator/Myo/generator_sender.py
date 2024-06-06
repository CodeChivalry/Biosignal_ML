import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet

# Parameters
num_channels = 8
sampling_rate = 250  # Hz

# Time vector for one second of data
t = np.linspace(0, 1, sampling_rate, endpoint=False)

# Generate synthetic EMG signals for each channel
def generate_emg_signal(t):
    noise = np.random.normal(0, 0.1, len(t))
    muscle_activity = np.sin(2 * np.pi * 10 * t) * (np.random.rand(len(t)) > 0.98)
    return noise + muscle_activity

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('marker', 'marker', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
try:
    print("Streaming EMG data... Press Ctrl+C to stop.")
    while True:
        # Generate new signals for each channel
        emg_signals = np.array([generate_emg_signal(t) for _ in range(num_channels)])
        
        # Stream the data via LSL
        for i in range(sampling_rate):
            sample = emg_signals[:, i].tolist()  # Convert the current sample to a list
            outlet.push_sample(sample)           # Push the sample to the LSL outlet

        # Wait for one second to simulate real-time sampling rate
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user.")
