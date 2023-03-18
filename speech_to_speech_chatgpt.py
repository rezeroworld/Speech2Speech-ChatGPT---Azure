import azure.cognitiveservices.speech as speechsdk

import openai

import time
import keyboard
import os

def start_recognition_from_microphone():
    speech_recognizer.start_continuous_recognition()
    print('vocal recording started...')
    global speech_recognition_active
    speech_recognition_active = True

def stop_recognition_from_microphone():
    speech_recognizer.stop_continuous_recognition()
    print('vocal recording stoped...')
    global speech_recognition_active
    speech_recognition_active = False

def create_message_to_openai(content, role):
    message = {"role": role, "content": content}
    return message

def recording_handler(evt):
    global user_vocal_input
    user_vocal_input = evt.result.text

#############################################################################
#############################################################################
#############################################################################

if __name__=='__main__':
    # OpenAi
    openai_key_var_name = "OPENAI_KEY"
    openai.api_key = os.getenv(openai_key_var_name)

    # Microsoft Azur
    azur_key_var_name, region = "AZUR_KEY", 'canadacentral'
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv(azur_key_var_name), region=region)

    # Text to Speech #############################################################
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Speech to Text ############################################################
    speech_config.speech_recognition_language="en-US"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognizer.recognized.connect(lambda evt: recording_handler(evt))

    #############################################################################
    speech_recognition_active = False
    recording_key = 'alt' 
    chat_log = []

    print(f'Speech recognition is currently inactive... Press {recording_key} to start...')
    keyboard.wait(recording_key)
    start_recognition_from_microphone()

    for _ in range(4):
        user_vocal_input = ""
        if speech_recognition_active:
            print(f'Press {recording_key} to stop...')
            keyboard.wait(recording_key)
            stop_recognition_from_microphone()
            time.sleep(0.5)
            print('--------------------------------------------------')
            print(f'user: {user_vocal_input}')
            print('--------------------------------------------------')
            chat_log.append(create_message_to_openai(user_vocal_input, 'user'))
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_log[-2000:])
            system_message_content = (response['choices'][0]['message']['content']).strip(' \n')
            chat_log.append(create_message_to_openai(system_message_content, 'system'))
        else:
            print('--------------------------------------------------')
            print(f'system: {system_message_content}')
            print('--------------------------------------------------')
            speech_synthesizer.speak_text(system_message_content)
            print(f'Press {recording_key} to start...')
            keyboard.wait(recording_key)
            start_recognition_from_microphone()

    print('--------------------------------------------------')
    print("here is the complete chat log: ")
    for dict_ in chat_log:
        print(f"{dict_['role']}: {dict_['content']}")
