import myo

class Listener(myo.DeviceListener):
    def __init__(self, sdkpath):
        super().__init__()
        myo.init(sdk_path= sdkpath)
        self.hub = myo.Hub()
        self.observers = []
        self.emg_data_queue = []
    def fetch_emg(self):
        while self.hub.run(self.on_event,10000):
            pass
    def register_observer(self, observer):
        self.observers.append(observer)
    def notify(self, data):
        for observer in self.observers:
            observer(data)
    
    def on_paired(self, event):
        print("Hello, {}!".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)
        event.device.stream_emg(myo.StreamEmg.enabled)
    def on_unpaired(self, event):
        return False  # Stop the hub
    def on_orientation(self, event):
        orientation = event.orientation
        acceleration = event.acceleration
        gyroscope = event.gyroscope
    # ... do something with that

    def on_emg(self, event):
        try:
            emg = []
            emg = event.emg
            self.emg_data_queue.append(emg)
            self.notify(emg)
            print(emg)
        except AttributeError:
            pass
        
    def on_connected(self, event):
        print("connected!")
        event.device.stream_emg(True)
    def on_disconnected(self, event):
        print("Disconnected!")
    

    