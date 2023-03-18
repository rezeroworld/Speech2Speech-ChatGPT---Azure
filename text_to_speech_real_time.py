import azure.cognitiveservices.speech as speechsdk

import keyboard
import time
import os

def recognize_from_microphone():
    result = ''

    def recording_handler(evt):
        nonlocal result
        result = evt.result.text
        print(f'res{result}')

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    azur_key_var_name, region = "AZUR_KEY", 'canadacentral'
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv(azur_key_var_name), region=region)
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognizer.recognized.connect(lambda evt: recording_handler(evt))

    recording_key = 'alt'

    print(f"press {recording_key} to start recording...")
    keyboard.wait(recording_key)

    speech_recognizer.start_continuous_recognition_async()
    
    print(f"press {recording_key} to stop recording...")
    keyboard.wait(recording_key)

    speech_recognizer.stop_continuous_recognition()

    time.sleep(2)

    print(f'result: {result}')

recognize_from_microphone()