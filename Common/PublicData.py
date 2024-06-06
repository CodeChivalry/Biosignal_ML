from enum import Enum

class DevicesEnum(str, Enum):
    Shimmer = "shimmer"
    Unicorn = "unicorn"
    Myo = "myo"

base_dir = 'Dataset'
shimmer_header = ['Timestamp_lsl','Timestamp_inlet','TimeStampRaw', 'TimeStampCAL(ms)','SystemTimeStamp(ms)','InternalADC_A13','InternalADC_A13(mv)','GSR','GSR(Kohms)','GSR conductance(uSiemens)','HeartRatePPG(beats/min)','IBIPPG(ms)']

unicorn_header = ['Timestamp_lsl', "FZ", "C3", "CZ", "C4", "PZ", "PO7", "OZ", "PO8",
        "AccX","AccY", "AccZ", "Gyro1", "Gyro2","Gyro3","Battery", "Counter","Validation"]

myo_header = ['Timestamp_lsl','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8']

NUM_SAMPLES = 1000

def get_header(device_name):
    if device_name == DevicesEnum.Shimmer.value:
        return shimmer_header
    elif device_name ==  DevicesEnum.Unicorn.value:
        return unicorn_header
    elif device_name ==  DevicesEnum.Myo.value:
        return myo_header
    else:
        return ""



