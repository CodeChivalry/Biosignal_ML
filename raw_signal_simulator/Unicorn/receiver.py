from pylsl import StreamInlet, resolve_stream
print("Looking for an unicorn stream...")
streams = resolve_stream('name', 'Unicorn')




inlet = StreamInlet(streams[0])

print("Receiving unicorn data... Press Ctrl+C to stop.")

try:
    while True:
        # Get a new sample (sample is a list of float values)
        sample, timestamp = inlet.pull_sample()
        print(f"Timestamp: {timestamp}, Sample: {sample}")
except KeyboardInterrupt:
    print("Data reception stopped by user.")