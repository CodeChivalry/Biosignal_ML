import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet

# Parameters
sampling_rate = 250  # Hz

# Read data from the CSV file
csv_file = 'P01_Unicorn.csv'
data = pd.read_csv(csv_file)

# Strip leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Extract the relevant columns
relevant_columns = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 
                    'AccX', 'AccY', 'AccZ', 'Gyro1', 'Gyro2', 'Gyro3',
                    'Battery', 'Counter', 'Validation']

# Verify the columns are present in the DataFrame
missing_columns = [col for col in relevant_columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the CSV file: {missing_columns}")

unicorn_data = data[relevant_columns]

# Get the number of channels from the data
num_channels = unicorn_data.shape[1]

# Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
info = StreamInfo('unicorn', 'unicorn', num_channels, sampling_rate, 'float32', 'myuid34234')

# Create an outlet to stream the data
outlet = StreamOutlet(info)

# Main loop to simulate real-time data acquisition
try:
    print("Streaming unicorn data from CSV... Press Ctrl+C to stop.")
    while True:
        # Stream the data via LSL
        for i in range(0, len(unicorn_data), sampling_rate):
            chunk = unicorn_data.iloc[i:i+sampling_rate].values  # Get a chunk of data
            for sample in chunk:
                outlet.push_sample(sample.tolist())  # Push the sample to the LSL outlet

        # Wait for one second to simulate real-time sampling rate
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user.")
