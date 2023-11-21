from twitchio.ext import commands
from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import nltk
import creds
import pygame
# import sounddevice as sd    # something wrong with this
import speech_recognition as sr
import threading
import keyboard
from game_changer import *
import pyaudio
import wave

CONVERSATION_LIMIT = 20

speech = False

model = Model() 

# download the words corpus
nltk.download('words')

class Bot(commands.Bot):

    conversation = list()

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        
        Bot.conversation.append({ 'role': 'system', 'content': open_file('prompt_chat.txt') })
        super().__init__(token= creds.TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])

        self.conv_count = 0

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

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

        
        # initial listenining for keybind
        program_thread = threading.Thread(target=speech_mode, args=(os.path.dirname(__file__) + '/output22.mp3',))
        program_thread.start()

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        # if message.type == 'JOIN':
        #     print(f"User {message.author.name} joined the stream!")

        if message.echo:
            return
        print(speech)
        # If the AI is listening to speech input instead of reading twitch chat
        if speech:
            return

        self.text_to_text(message)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    def text_to_text(self, message):

        # we are appending the personality txt file to the conversation array after every 5 back and forths so the model doesn't forget what it is
       
        Bot.conversation.append({ 'role': 'system', 'content': open_file('prompt_chat.txt') })

        new_message = message

        if type(message) != str:
            new_message = message.content
        
        # # Check if the message contains english words
        # if not any(word in new_message for word in nltk.corpus.words.words()):
        #     return
        
        # Check if the message is too long or short
        if len(new_message) > 150 or len(new_message) < 1:
            return
        
        print('------------------------------------------------------')
        # print(message.content)
        # print(message.author.name)
        # print(Bot.conversation)

        # I think this is turning message into a string???
        content = new_message.encode(encoding='ASCII',errors='ignore').decode()

        # using our game changer AI to see it should switch games
        output = model(content)

        if output == 0:
            print("switch to dino")
        elif output == 1:
            print("switch to flappy bird")
        elif output == 2:
            print("switch to donkey kong")
        elif output == 3:
            print("switch to asteroids")
        else:
            print("keep talking(don't switch)")

        Bot.conversation.append({ 'role': 'user', 'content': content })

        response = gpt3_completion(Bot.conversation, tokens=100)
        print('Someone:' , response)
        
        # expression changing AI
        sentiment = []
        sentiment.append({ 'role': 'system', 'content': open_file('emotion.txt')})
        sentiment.append({ 'role': 'user', 'content': response})

        emotion = gpt3_completion(sentiment)
        
        print(emotion)

        if emotion == "Neutral":
            keyboard.press('ctrl+1')
            
        elif emotion == "Fun":
            keyboard.press('ctrl+2')

        elif emotion == "Angry":
            keyboard.press('ctrl+3')

        elif emotion == "Joy":
            keyboard.press('ctrl+4')

        elif emotion == "Sorrow":
            keyboard.press('ctrl+5')

        elif emotion == "Surprise":
            keyboard.press('ctrl+6')
        
        keyboard.release('ctrl')


        if(Bot.conversation.count({ 'role': 'assistant', 'content': response }) == 0):
            Bot.conversation.append({ 'role': 'assistant', 'content': response })
        
        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]
        
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

        # play_audio(audio_file)

        # captions(mark_array, response)

        


        # Print the contents of our message to console...
        
        print('------------------------------------------------------')
        os.remove(audio_file)
        
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

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


# waiting for a certain key input
def speech_mode(file_name):
    global speech
    print("Text Mode")

    while not speech:
        time.sleep(1)
        if keyboard.is_pressed('o') and keyboard.is_pressed('q'):
            record_audio(file_name)
            speech = True
            break

    program_thread2 = threading.Thread(target=stop_speech, args=(os.path.dirname(__file__) + '/output22.mp3',))
    program_thread2.start()

# wait for a certain key input to stop the speech model(model listening to speech instead of twitch chat)
def stop_speech(file_name):
    global speech    
    print("Speech Mode")

    while speech:
        start_time = time.time()
        timeout = 5  # seconds

        while time.time() - start_time < timeout:
            if keyboard.is_pressed('o') and keyboard.is_pressed('q'):
                speech = False
                break

        if time.time() - start_time >= timeout:
            record_audio(file_name)
        else:
            break
    
    program_thread = threading.Thread(target=speech_mode, args=(os.path.dirname(__file__) + '/output22.mp3',))
    program_thread.start()


# RECORDING AUDIO FOR SPEECH TO TEXT
# # Example usage
# file_name = 'recorded_audio.wav'
# record_audio(file_name, duration=10)  # Record for 5 seconds

def record_audio(file_name, duration=5, samplerate=44100):
    # Define parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    SILENCE_THRESHOLD = 20  # Adjust this value as needed

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording audio...")

    frames = []
    recording = False

    start_time = time.time()

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert data to a list of integers for RMS calculation
        data_int = [int.from_bytes(data[i:i+2], byteorder='little', signed=True) for i in range(0, len(data), 2)]
        
        # Calculate the root mean square (RMS) of the audio data
        rms = max(data_int)

        print(rms)

        if rms < SILENCE_THRESHOLD and recording:
            time.sleep(1.5)
            if rms < SILENCE_THRESHOLD and recording:
                break

        if rms >= SILENCE_THRESHOLD and not recording:
            recording = True

    end_time = time.time()

    print(f"* Finished recording in {end_time - start_time:.2f} seconds")

    # Stop the stream and close it
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

    # Save the audio data as a .wav file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    audio_file = open(file_name, "rb")
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print(text)
    
    except:
        text = "Say \"I didn't understand what you said, could you please repeat your sentence.\""


    bot.text_to_text(text)
 

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

print("hi")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds.GOOGLE_JSON_PATH
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.



