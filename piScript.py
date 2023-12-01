import time

import cv2
import numpy as np

from picamera2 import Picamera2
import socket

import RPi.GPIO as GPIO
import ADC0834
import dht11
import json
import base64
from libcamera import controls as controls2

GPIO.setmode(GPIO.BCM)
ADC0834.setup()
myDHT = dht11.DHT11(pin = 23)

TCP_IP ='172.20.10.7'#'192.168.137.166' #'192.168.137.134' #'192.168.137.99' #'1                                                                                      72.20.10.7' #'192.168.1.209'
TCP_PORT = 2222
BUFFER_SIZE = 8192

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((TCP_IP, TCP_PORT))
except OSError as error:
    print(error)
s.listen(1)
print(f"Server is listening on {TCP_IP}:{TCP_PORT}")


RATIO = 3.0

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0}                                                                                      )
#exposure_long = int(exposure_normal * RATIO)
#picam2.set_controls({"ExposureTime": exposure_long, "AnalogueGain": gain})

with open('test.jpg','rb') as f:
    image_data = f.read()

image_data_base = base64.b64encode(image_data).decode('utf-8')
while True:
    client_socket, client_address =  s.accept()
    print(f"Connection address: {client_address}")

    lightVal = ADC0834.getResult(0)
    result = myDHT.read()
    lightValToSend = str(lightVal)
    lightValToSend = lightValToSend.encode('utf-8')
    while result.is_valid() is False:
        result = myDHT.read()
    tempValToSend = str(result.temperature)
    tempValToSend = tempValToSend.encode('utf-8')

    trigger_char = client_socket.recv(1).decode()

    data_dict ={'Light':lightVal,
                'Temp': result.temperature,
                'image_data': image_data_base}


    if trigger_char == 'R':
        picam2.start()
        #print(data_dict['Light'])
        #print(data_dict['Temp'])
        # Run for a second to get middle exposure level.
        time.sleep(1)
        metadata = picam2.capture_metadata()
        exposure_normal = metadata["ExposureTime"]
        gain = metadata["AnalogueGain"] * metadata["DigitalGain"]
        picam2.stop()
        controls = {"ExposureTime": int(exposure_normal*RATIO), "AnalogueGain": gain,
                    "AfMode": controls2.AfModeEnum.Manual, "LensPosition": 0.0}
        #(1024, 768)
        capture_config = picam2.create_preview_configuration(main={"size": (4608 , 2592),
                                                                  "format": "RGB 888"},
                                                             controls=controls)
        picam2.configure(capture_config)
        picam2.start()
        long = picam2.capture_array()
        picam2.stop()
        cv2.imwrite("test.jpg", long)
        with open('test.jpg','rb') as f:
            image_data = f.read()
        image_data_base = base64.b64encode(image_data).decode('utf-8')
        data_dict['image_data'] = image_data_base
        serial_data = json.dumps(data_dict)
        client_socket.send(serial_data.encode('utf-8'))



    client_socket.close()
