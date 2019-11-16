import paho.mqtt.client as mqtt
import time
import serial

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
time.sleep(2)

def on_message(client, userdata, message):
  ser.write(message.payload.encode("ascii"))
  #ser.write(b'1')

broker = "broker.hivemq.com"
client = mqtt.Client("P1")
client.on_message=on_message
client.connect(broker)

client.loop_start() #start the loop
client.subscribe("pills")

while True:
  time.sleep(1)
