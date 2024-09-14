from enum import Enum, auto
import pandas as pd
import os
class DevicesEnum(Enum):
    shimmer = auto()
    unicorn = auto()
    myo = auto()
    marker = auto()

base_dir = os.path.join(os.path.dirname(__file__), '..', 'Dataset')

header_maps = {
    DevicesEnum.shimmer.name: ['Timestamp_outlet','Timestamp_inlet','TimeStampRaw', 'TimeStampCAL(ms)','SystemTimeStamp(ms)','InternalADC_A13','InternalADC_A13(mv)','GSR','GSR(Kohms)','GSR conductance(uSiemens)','HeartRatePPG(beats/min)','IBIPPG(ms)'],

    DevicesEnum.unicorn.name: ['Timestamp_outlet','Timestamp_inlet', "FZ", "C3", "CZ", "C4", "PZ", "PO7", "OZ", "PO8",
        "AccX","AccY", "AccZ", "Gyro1", "Gyro2","Gyro3","Battery", "Counter","Validation"],
    
    DevicesEnum.myo.name: ['Timestamp_outlet','Timestamp_inlet','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8'],

    DevicesEnum.marker.name: ['Timestamp_outlet','Timestamp_inlet','Marker']

    # add more when there is new devices streaming data and need to save to csv
}

biosignal_maps = {
    DevicesEnum.shimmer.name: ['eda', 'ppg'],

    DevicesEnum.unicorn.name: ['eeg'],
    
    DevicesEnum.myo.name: ['emg'],
}

# this will be automatically filled by the feature extraction functions
biosignal_feature_maps = {
    biosignal_maps[DevicesEnum.shimmer.name][0]: [], # eda features
    biosignal_maps[DevicesEnum.shimmer.name][1]: [], # ppg features
    biosignal_maps[DevicesEnum.unicorn.name][0]: [], # eeg features
    biosignal_maps[DevicesEnum.myo.name][0]: [], # emg features
}
NUM_SAMPLES = 1000
shimmer_sample_rate = 256
unicorn_sample_rate = 250
myo_sample_rate = 200

