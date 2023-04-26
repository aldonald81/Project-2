import speech_recognition as sr

import os
import openai

# Set the file path for the .wav file to transcribe
wav_file_path = "audio.wav"


# Initialize recognizer class                                       
r = sr.Recognizer()
# audio object                                                         
audio = sr.AudioFile("recipe.wav")
#read audio object and transcribe
with audio as source:
    audio = r.record(source)                  
    result = r.recognize_google(audio)
    
print(result)


openai.api_key = "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"

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=result,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)

print(response.choices[0].text)
"""
# Open the .wav file
with sr.AudioFile(wav_file_path) as source:
    # Read the audio data from the file
    audio_data = r.record(source)

    # Use the recognizer to transcribe the audio to text
    text = r.recognize_google(audio_data)

# Print the transcribed text
print("Transcribed text:")
print(text)
"""