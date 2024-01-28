import alsaaudio as alsa
import numpy as np
from queue import Queue
from datetime import datetime, timedelta
from time import sleep
import threading
import os
import wave
import soundfile as sf

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

i = 0

while True:
    try:
        now = datetime.utcnow()
        if not data_queue.empty():
            audio_data = data_queue.get()
            data_queue.queue.clear()
            
            # Convert in-ram buffer to something the model can use directly without needing a temp file.
            # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            reshape_np = audio_np.reshape(-1, 2)
            #print(.shape)
            sf.write(f"temp/coba_{i}.wav", reshape_np, 44100)
            # with wave.open(f"temp/coba_{i}.wav", "wb") as out_wav:
            #     out_wav.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
            #     out_wav.writeframesraw(audio_data)
            
            i += 1

            # Infinite loops are bad for processors, must sleep.
            sleep(0.25)
    except KeyboardInterrupt:
        break