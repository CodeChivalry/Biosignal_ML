from enum import Enum, auto

class DevicesEnum(Enum):
    shimmer = auto()
    unicorn = auto()
    myo = auto()
    marker = auto()

base_dir = 'Dataset'

header_maps = {
    DevicesEnum.shimmer.name: ['Timestamp_outlet','Timestamp_inlet','TimeStampRaw', 'TimeStampCAL(ms)','SystemTimeStamp(ms)','InternalADC_A13','InternalADC_A13(mv)','GSR','GSR(Kohms)','GSR conductance(uSiemens)','HeartRatePPG(beats/min)','IBIPPG(ms)'],

    DevicesEnum.unicorn.name: ['Timestamp_outlet','Timestamp_inlet', "FZ", "C3", "CZ", "C4", "PZ", "PO7", "OZ", "PO8",
        "AccX","AccY", "AccZ", "Gyro1", "Gyro2","Gyro3","Battery", "Counter","Validation"],
    
    DevicesEnum.myo.name: ['Timestamp_outlet','Timestamp_inlet','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8'],

    DevicesEnum.marker.name: ['Timestamp_outlet','Timestamp_inlet','Marker']

    # add more when there is new devices streaming data and need to save to csv

}


NUM_SAMPLES = 1000




