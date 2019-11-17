import paho.mqtt.client as mqtt
import time
import serial
import json

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

def on_message(client, userdata, message):
  print(message.payload)
  jsonPayload = json.loads(message.payload.decode("utf-8"))
  
  numPills = jsonPayload["numPills"]
  print("num of pills:",numPills)
  pillId = jsonPayload["pillId"]
  print("id:",pillId)
  
  if(pillId == 1):
    pillId = 4

  ser.write(str(numPills+pillId).encode('ascii'))

broker = "broker.hivemq.com"
client = mqtt.Client()
client.on_message = on_message
client.connect(broker)

client.subscribe("pills")

client.loop_start() #start the loop

while True:
  if(ser.in_waiting >0):
    takenId = ser.read()
    print("Pills taken")
    client.publish("pillsTaken", "1")

