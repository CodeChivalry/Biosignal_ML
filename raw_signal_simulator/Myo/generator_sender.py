import numpy as np
import pandas as pd
import neurokit2 as nk
import time
from pylsl import StreamInfo, StreamOutlet

def generate_synthetic_emg(duration, sampling_rate, noise, burst_number, burst_duration, random_state=None):
    return nk.emg_simulate(duration=duration, 
                           sampling_rate=sampling_rate, 
                           noise=noise, 
                           burst_number=burst_number, 
                           burst_duration=burst_duration, 
                           random_state=random_state)
# Parameters
duration = 10  # seconds
sampling_rate = 250  # Hz
noise = 0.1
burst_number = 3
burst_duration = [0.5, 1, 0.75]  # Different durations for each burst
num_electrodes = 8  # Number of electrodes (channels)

# Generate EMG signals for each electrode
electrode_columns = [f'Electrode {i+1}' for i in range(num_electrodes)]
emg_data = {col: generate_synthetic_emg(duration, sampling_rate, noise, burst_number, burst_duration, random_state=i) for i, col in enumerate(electrode_columns)}

# Convert to DataFrame
emg_df = pd.DataFrame(emg_data)

# Get the number of channels from the data
num_channels = emg_df.shape[1]

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('myo', 'EMG', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
try:
    print("Streaming synthetic EMG data... Press Ctrl+C to stop.")
     
    while True:
        # Stream the data via LSL
        for i in range(0, len(emg_df), sampling_rate):
            chunk = emg_df.iloc[i:i+sampling_rate].values  # Get a chunk of data
            for sample in chunk:
                outlet.push_sample(sample.tolist())  # Push the sample to the LSL outlet
        
        # Wait for one second to simulate real-time sampling rate
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user.")
