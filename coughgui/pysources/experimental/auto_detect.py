#pip install xgboost==0.90 scipy==0.22.1

import alsaaudio as alsa
import numpy as np
from queue import Queue
from datetime import datetime, timedelta
from time import sleep
import threading
import os
import wave
import soundfile as sf

from src.DSP import classify_cough
import pickle

model = pickle.load(open(os.path.join('./models', 'cough_classifier'), 'rb'))
scaler = pickle.load(open(os.path.join('./models', 'cough_classification_scaler'), 'rb'))

AudioLong = 1024
to_checkAudio = np.zeros(3 * AudioLong, dtype='i2')

aslsa_pcm = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, channels=2, rate=44100,format=alsa.PCM_FORMAT_S16_LE, periodsize=AudioLong)

data_queue = Queue()
phrase_time = None
phrase_timeout = 3

def capture_audio():
    phrase_time = datetime.utcnow()
    total_indata = bytearray()
    while True:
        now = datetime.utcnow()
        _, indata = aslsa_pcm.read()

        if now - phrase_time > timedelta(seconds=phrase_timeout):
            phrase_time = now
            data_queue.put(bytes(total_indata))
            total_indata = bytearray(indata)
        else:
            total_indata += indata

capture_thread = threading.Thread(target=capture_audio)
capture_thread.daemon = True
capture_thread.start()

while True:
    try:
        now = datetime.utcnow()
        if not data_queue.empty():
            audio_data = data_queue.get()
            data_queue.queue.clear()
            
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            reshape_np = audio_np.reshape(-1, 2)

            prob = classify_cough(reshape_np, 44100, model, scaler)
            #print(f"has probability of cough: {prob}")
            if prob > 0.75:
                print(f"Batuk")            
            
            sleep(0.25)
    except KeyboardInterrupt:
        break