import speech_recognition as sr
import pyaudio
import wave
import os
import openai

# Get keys
keys_file = open("keys.txt")
keys = keys_file.readlines()
openai.api_key = keys[0].rstrip('\n')
auth_token = keys[1]

# RECORD AUDIO
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 15 # seconds to record
dev_index = 1 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'audio1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
########################3


# Set the file path for the .wav file to transcribe
wav_file_path = "audio1.wav"


# Initialize recognizer class                                       
r = sr.Recognizer()
# audio object                                                         
audio = sr.AudioFile(wav_file_path)
#read audio object and transcribe
with audio as source:
    audio = r.record(source)                  
    result = r.recognize_google(audio)
    
print(result)





prompt = "Give me a drink recipe based off this input: " + result + "Also, tell me what their phone number is in the first line of the response and in the format: Number: +17046518034" 
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)

print(response.choices[0].text)


from twilio.rest import Client

account_sid = 'AC99bf8490ba05338f759736951da345e4'
client = Client(account_sid, auth_token)

text = response.choices[0].text
print(type(text))

text = '''
From your Bot Tender:
''' + text

## FIND PHONE NUMBER
# search for the key phrase "Number: "
key_phrase = "Number: "
index = text.find(key_phrase)

if index != -1:
    # extract the phone number
    phone_number = text[index + len(key_phrase):].split()[0]
    print("Phone number:", phone_number)
else:
    print("No phone number found in the response.")

print(phone_number)

message = client.messages.create(
  from_='+18777194710',
  body=text,
  to=phone_number
)

print(message.sid)

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