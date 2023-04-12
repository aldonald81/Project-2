import sounddevice as sd
import soundfile as sf

# Define the sampling frequency and duration of the recording
sample_rate = 44100
duration = 5  # seconds

# Use sounddevice to record the audio from the headphone jack
print("Recording started")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)

# Wait for the recording to finish
sd.wait()

# Save the recording to a WAV file
sf.write("recording.wav", recording, sample_rate)

# Print a message to indicate that the recording has finished
print("Recording finished")
