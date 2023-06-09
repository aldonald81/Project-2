import speech_recognition as sr
import pyaudio
import wave
import os
import openai


import RPi.GPIO as GPIO
import time

# set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT) #led
GPIO.output(6, GPIO.LOW)

# define the pin number for the button
button_pin = 15

# Get keys
keys_file = open("keys.txt")
keys = keys_file.readlines()
openai.api_key = keys[0].rstrip('\n')
auth_token = keys[1]

# set the pin as input with a pull-down resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    # wait for button press
    if GPIO.input(button_pin) == GPIO.HIGH:
        # button is pressed, do something here
        print("Button pressed!")

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
        GPIO.output(6, GPIO.HIGH)
        frames = []

        # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)
            frames.append(data)

        print("finished recording")
        GPIO.output(6, GPIO.LOW)

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

        print(response.choices[0].text)


        from twilio.rest import Client

        account_sid = 'AC99bf8490ba05338f759736951da345e4'
        client = Client(account_sid, auth_token)

        text = response.choices[0].text

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

            message = client.messages.create(
            from_='+18777194710',
            body=text,
            to=phone_number
            )

            #print(message.sid)
        else:
            print("No phone number found in the response.")
            # extract the phone number

            message = client.messages.create(
            from_='+17046518034',
            body=text,
            to=phone_number
            )

            #print(message.sid)

        

        # add a small delay to avoid multiple detections
        time.sleep(0.2)

"""
# create a Button object that represents the button on pin 12
button = Button(12)



# define a function to execute when the button is pressed
def on_button_pressed():
    

 



# attach the function to the button's 'when_pressed' event
button.when_pressed = on_button_pressed

# keep the program running
while True:
    pass

"""
