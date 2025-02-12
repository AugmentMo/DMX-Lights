from DMXLights import DMXLights
import time
import sounddevice as sd
import numpy as np

light_count = 44
dmx = DMXLights()

adj_factor = 0.5

dmx.setLight(0, [0,0,0])

import librosa

def audio_callback(indata, frames, time, status):
    
    # Assuming indata is an array of audio data
    audio_data = indata[:, 0]
    
    # Get the sample rate, 'sr' is typically 22050
    sr = 22050
    
    # Firstly calculate a Short-Time Fourier Transform
    stft_result = np.abs(librosa.stft(audio_data, n_fft=4096, hop_length=512))
    
    # Then calculate pitch using librosa's piptrack function
    pitches, magnitudes = librosa.piptrack(S=stft_result, sr=sr)
    
    # Find the pitch with the highest magnitude
    max_value = np.max(magnitudes)                          # find max value of magnitudes
    max_index = np.where(magnitudes == max_value)           # find index of this max value
    pitch = pitches[max_index]                              # extract the corresponding pitch

    if len(pitch) == 1:
        print("pitch", pitch)
        val = abs(int(pitch/4))
        dmx.setLight(0, [abs(255-val),val,0])

stream = sd.InputStream(callback=audio_callback)
with stream:
    sd.sleep(1000000000) #sleeping for a long time, you can adjust it for your own need

# Turn all off
dmx.setLight(0, [0,0,0])
