from chat import *
import threading
import keyboard
import creds
import pygame
from twitchio.ext import commands
from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import time
import nltk
import os
import threading

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds.GOOGLE_JSON_PATH

def play_audio(audio_file):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load(audio_file)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

def captions(mark_array, response):
    count = 0
    current = 0
    for i in range(len(response.timepoints)):
        count += 1
        current += 1
        with open("output.txt", "a", encoding="utf-8") as out:
            out.write(mark_array[int(response.timepoints[i].mark_name)] + " ")
        if i != len(response.timepoints) - 1:
            total_time = response.timepoints[i + 1].time_seconds
            time.sleep(total_time - response.timepoints[i].time_seconds)
        if current == 25:
                open('output.txt', 'w', encoding="utf-8").close()
                current = 0
                count = 0
        elif count % 7 == 0:
            with open("output.txt", "a", encoding="utf-8") as out:
                out.write("\n")
    time.sleep(2)
    open('output.txt', 'w').close()

# download the words corpus
nltk.download('words')

response = "Hi, welcome to the stream"

client = texttospeech.TextToSpeechClient()

# response = message.content + "? " + response
ssml_text = '<speak>'
response_counter = 0
mark_array = []
for s in response.split(' '):
    ssml_text += f'<mark name="{response_counter}"/>{s}'
    mark_array.append(s)
    response_counter += 1
ssml_text += '</speak>'

input_text = texttospeech.SynthesisInput(ssml = ssml_text)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name= "en-US-Neural2-F",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(    
    audio_encoding=texttospeech.AudioEncoding.MP3,
)


response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
)


# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

audio_file = os.path.dirname(__file__) + '/output.mp3'


time_thread = threading.Thread(target=play_audio, args=(audio_file,))
time2_thread = threading.Thread(target=captions, args=(mark_array, response))

time2_thread.start()
time_thread.start()

time_thread.join()
time2_thread.join()

time.sleep(3)

response = "Sure, lets play dino"

client = texttospeech.TextToSpeechClient()

# response = message.content + "? " + response
ssml_text = '<speak>'
response_counter = 0
mark_array = []
for s in response.split(' '):
    ssml_text += f'<mark name="{response_counter}"/>{s}'
    mark_array.append(s)
    response_counter += 1
ssml_text += '</speak>'

input_text = texttospeech.SynthesisInput(ssml = ssml_text)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name= "en-US-Neural2-F",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(    
    audio_encoding=texttospeech.AudioEncoding.MP3,
)


response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
)


# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

audio_file = os.path.dirname(__file__) + '/output.mp3'


time_thread = threading.Thread(target=play_audio, args=(audio_file,))
time2_thread = threading.Thread(target=captions, args=(mark_array, response))

time2_thread.start()
time_thread.start()

time_thread.join()
time2_thread.join()


time.sleep(3)

response = "I'm Vivi, a girl from the year 2030 where Thomas Edison has ressurrected himself from the dead and has changed every single physical thing into digital code"

client = texttospeech.TextToSpeechClient()

# response = message.content + "? " + response
ssml_text = '<speak>'
response_counter = 0
mark_array = []
for s in response.split(' '):
    ssml_text += f'<mark name="{response_counter}"/>{s}'
    mark_array.append(s)
    response_counter += 1
ssml_text += '</speak>'

input_text = texttospeech.SynthesisInput(ssml = ssml_text)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name= "en-US-Neural2-F",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(    
    audio_encoding=texttospeech.AudioEncoding.MP3,
)


response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
)


# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

audio_file = os.path.dirname(__file__) + '/output.mp3'


time_thread = threading.Thread(target=play_audio, args=(audio_file,))
time2_thread = threading.Thread(target=captions, args=(mark_array, response))

time2_thread.start()
time_thread.start()

time_thread.join()
time2_thread.join()

time.sleep(3)

response = "Oh no, I died!"

client = texttospeech.TextToSpeechClient()

# response = message.content + "? " + response
ssml_text = '<speak>'
response_counter = 0
mark_array = []
for s in response.split(' '):
    ssml_text += f'<mark name="{response_counter}"/>{s}'
    mark_array.append(s)
    response_counter += 1
ssml_text += '</speak>'

input_text = texttospeech.SynthesisInput(ssml = ssml_text)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name= "en-US-Neural2-F",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(    
    audio_encoding=texttospeech.AudioEncoding.MP3,
)


response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
)


# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

audio_file = os.path.dirname(__file__) + '/output.mp3'


time_thread = threading.Thread(target=play_audio, args=(audio_file,))
time2_thread = threading.Thread(target=captions, args=(mark_array, response))

time2_thread.start()
time_thread.start()

time_thread.join()
time2_thread.join()



