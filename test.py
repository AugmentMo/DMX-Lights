from DMXLights import DMXLights
import time

light_count = 44
dmx = DMXLights()

# Light up each one once
for i in range(light_count):
    dmx.setLight(i, [255,255,255])
    time.sleep(0.05)
    dmx.setLight(0, [0,0,0])
    time.sleep(0.05)

# Light up all together in red, green, blue, white
dmx.setLight(0, [255,0,0])
time.sleep(1)
dmx.setLight(0, [0,255,0])
time.sleep(1)
dmx.setLight(0, [0,0,255])
time.sleep(1)
dmx.setLight(0, [255,255,255])
time.sleep(1)
dmx.setLight(0, [0,0,0])
