from MyMyo import Listener
import numpy as np
from pylsl import StreamInfo, StreamOutlet
import os
import time

if __name__ == '__main__':
    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)
    # Construct the path to the same_level_folder within the current directory
    sdkpath = os.path.join(current_directory, 'myo-sdk-win-0.9.0')
    listener = Listener(sdkpath)

    # Parameters
    num_channels = 8
    sampling_rate = 200  # Hz
    # Create a new stream info (name, type, number of channels, sampling rate, data format, source id)
    info = StreamInfo('myo', 'myo', num_channels,sampling_rate, 'float32', 'myuid34234')

    # Create an outlet to stream the data
    outlet = StreamOutlet(info)

    with listener.hub.run_in_background(listener.on_event):
        while True:
            if listener.emg_data_queue:
                emg_data = listener.emg_data_queue.pop(0)
                outlet.push_sample(emg_data)
            time.sleep(0.01)


