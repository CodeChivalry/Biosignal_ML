from pylsl import StreamInlet, resolve_stream

print("Looking for a shimmer stream...")
streams = resolve_stream('type', 'shimmer')

inlet = StreamInlet(streams[0])

print("Receiving shimmer data... Press Ctrl+C to stop.")

try:
    while True:
        # Get a new sample (sample is a list of float values)
        sample, timestamp = inlet.pull_sample()
        # Print the timestamp and sample
        print(f"Timestamp: {timestamp}, Sample: {sample}")
except KeyboardInterrupt:
    print("Data reception stopped by user.")
