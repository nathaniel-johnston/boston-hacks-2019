import paho.mqtt.client as mqtt
import time
import serial
import json

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
time.sleep(2)

def on_message(client, userdata, message):
  jsonPayload = json.loads(message.payload.decode("utf-8"))
  
  numPills = jsonPayload["numPills"]
  pillId = jsonPayload["pillId"] + 1

  ser.write(str(numPills*pillId).encode('ascii'))

broker = "broker.hivemq.com"
client = mqtt.Client()
client.on_message = on_message
client.connect(broker)

client.subscribe("pills")

client.loop_forever() #start the loop
