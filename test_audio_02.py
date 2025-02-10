from DMXLights import DMXLights
import time
import sounddevice as sd
import numpy as np

light_count = 44
dmx = DMXLights()

threshold = 0.5
light_index = 1
dmx.setLight(0, [0,0,0])

def audio_callback(indata, frames, time, status):
    global light_index, threshold
    volume_norm = np.linalg.norm(indata)
    print(f"volume: {(volume_norm)}")

    if volume_norm > threshold:
        val = 255        
        dmx.setLight(0, [0,0,0], updateImmediately=False)
        r = 0
        g = 0
        b = 0

        if ((light_index % 3) == 0): 
            r = val
        elif ((light_index % 3) == 1): 
            g = val
        else: 
            b = val

        dmx.setLight(light_index, [r,g,b])
    
        light_index += 1
        
        if light_index > light_count:
            light_index = 1


stream = sd.InputStream(callback=audio_callback)
with stream:
    sd.sleep(1000000000) #sleeping for a long time, you can adjust it for your own need

# Turn all off
dmx.setLight(0, [0,0,0])
