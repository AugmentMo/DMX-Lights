import socket
import binascii
import time


class DMXLights:

    def __init__(self, ip_address="10.0.39.107", port=6038):
        self.__ip_address = ip_address
        self.__port = port

        self.__light_data = {}
        self.__max_light_ports = 8
        self.__max_lights_per_port = 170
        self.__initLightData()

        # Create a UDP socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __initLightData(self):
        for port_index in range(self.__max_light_ports):
            self.__light_data[port_index] = []

            for _ in range(self.__max_lights_per_port):
                self.__light_data[port_index].append([0,0,0])


    def updateLights(self):
        full_payload_length = 48 + 1024
        for port_index in range(self.__max_light_ports):
            hex_data = f"0401dc4a0100080162820100ffffffff0{port_index+1}00000000020000"
            full_payload_length = 48 + 1024

            for rgb_vals in self.__light_data[port_index]: 
                for val in rgb_vals:        
                    hex_str = format(val, '02x')
                    hex_data += hex_str
        
            remaining_payload_length = full_payload_length - len(hex_data) 

            # Fill up remaining bytes
            for i in range(remaining_payload_length):
                hex_data += "0"

            # Convert hex data to bytes
            message = binascii.unhexlify(hex_data)

            # Send the packet
            self.__socket.sendto(message, (self.__ip_address, self.__port))

    # configures the lights for each specified light port in the light_port_numebers value according to the specified rgb data array [[255,0,0], ..] which corresponds to the RGB colors for each light index
    def setLight(self, light_number, lights_rgb_data, light_ports=[1,2,3,4,5,6,7,8], updateImmediately=True):
        for light_port_number in light_ports:
            if light_port_number < 1:
                print(f"Error: light port must be from 1 - {self.__max_light_ports}")
                break 
            else:
                if light_number == 0:
                    for i in range(self.__max_lights_per_port):
                        self.__light_data[light_port_number-1][i] = lights_rgb_data
                else:
                    self.__light_data[light_port_number-1][light_number-1] = lights_rgb_data

        if updateImmediately:
            self.updateLights()

dmx = DMXLights()
dmx.setLight(0, [255,0,0])
time.sleep(1)
dmx.setLight(0, [0,255,0])
time.sleep(1)
dmx.setLight(0, [0,0,255])
time.sleep(1)
dmx.setLight(0, [0,0,0])