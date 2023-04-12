import os
import time
import wave
import pyaudio
import speech_recognition as sr
import RPi.GPIO as GPIO

# Set up GPIO button
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

# Set up speech recognition
r = sr.Recognizer()

while True:
    input_state = GPIO.input(12)
    if input_state == False:
        print("Recording started...")
        p = pyaudio.PyAudio()
        frames = []
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        while input_state == False:
            data = stream.read(CHUNK)
            frames.append(data)
            input_state = GPIO.input(12)
            
        print("Recording stopped...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save audio file
        filename = "recording.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        # Transcribe audio file
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            print("Transcription: " + text)
        except sr.UnknownValueError:
            print("Transcription could not be understood")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        # Wait for button release to prevent multiple recordings
        while input_state == False:
            input_state = GPIO.input(12)
    time.sleep(0.1)
