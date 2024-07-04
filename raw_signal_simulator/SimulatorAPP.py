import subprocess
import subprocess
import os

# Define the paths to the simulation code folders
myo_folder = os.path.join(os.path.dirname(__file__), 'Myo')
shimmer_folder = os.path.join(os.path.dirname(__file__), 'Shimmer')
unicorn_folder = os.path.join(os.path.dirname(__file__), 'Unicorn')

# Start the Myo simulation code
myo_process = subprocess.Popen(['python', 'generator_sender.py'], cwd=myo_folder)

# Start the Shimmer simulation code
shimmer_process = subprocess.Popen(['python', 'generator_sender.py'], cwd=shimmer_folder)

# Start the Unicorn simulation code
unicorn_process = subprocess.Popen(['python', 'generator_sender.py'], cwd=unicorn_folder)

# Wait for user input to exit
try:
    input("Press any key to exit...")
except KeyboardInterrupt:
    pass
myo_process.terminate()
shimmer_process.terminate()
unicorn_process.terminate()