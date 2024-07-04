import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet

# Parameters
sampling_rate = 250  # Hz
duration = 10  # seconds
num_samples = sampling_rate * duration

# Generate synthetic EMG signal
def generate_emg_signal(t):
    noise = np.random.normal(0, 0.1, len(t))
    muscle_activity = np.sin(2 * np.pi * 10 * t) * (np.random.rand(len(t)) > 0.98)
    return noise + muscle_activity

# Time vector for the duration of the signal
t = np.linspace(0, duration, num_samples)

# Columns for synthetic data
columns = ['TimeStampRaw', 'TimeStampCAL(ms)','SystemTimeStamp(ms)','InternalADC_A13','InternalADC_A13(mv)','GSR','GSR(Kohms)','GSR conductance(uSiemens)','HeartRatePPG(beats/min)','IBIPPG(ms)']
# Generate synthetic data for each electrode
shimmer_data = pd.DataFrame({col: generate_emg_signal(t) for col in columns})

# Get the number of channels from the data
num_channels = shimmer_data.shape[1]

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('shimmer', 'PPGEDA', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
if __name__ == "__main__":
    try:
        print("Streaming synthetic shimmer data... Press Ctrl+C to stop.")
        while True:
            # Stream the data via LSL
            for i in range(0, len(shimmer_data), sampling_rate):
                chunk = shimmer_data.iloc[i:i+sampling_rate]  # Get a chunk of data
                for index, row in chunk.iterrows():
                    sample = row.values.tolist()  # Convert the row to a list of values
                    sample_dict_list = [{col: row[col]} for col in columns] # List of dictionaries for logging 
                    outlet.push_sample(sample)  # Push the sample to the LSL outlet
                    timestamp = time.time()
                    print(f"Timestamp: {timestamp}, Sample: {sample_dict_list}")
            # Wait for one second to simulate real-time sampling rate
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
