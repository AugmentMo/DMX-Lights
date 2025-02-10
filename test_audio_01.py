from DMXLights import DMXLights
import time
import sounddevice as sd
import numpy as np

light_count = 44
dmx = DMXLights()

adj_factor = 0.5

dmx.setLight(0, [0,0,0])

def audio_callback(indata, frames, time, status):
    volume_norm = int(min(np.linalg.norm(indata) * 255 * adj_factor, 255))
    print(f"volume: {(volume_norm/255)}")
    dmx.setLight(0, [volume_norm,volume_norm,volume_norm])


stream = sd.InputStream(callback=audio_callback)
with stream:
    sd.sleep(1000000000) #sleeping for a long time, you can adjust it for your own need

# Turn all off
dmx.setLight(0, [0,0,0])
