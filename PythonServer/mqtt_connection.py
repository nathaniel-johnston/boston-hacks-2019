import paho.mqtt.client as mqtt
import json


class MQTTConnection(object):

    def __init__(self, params):
        self.client = mqtt.Client(params["client"])
        self.client.loop_start()
        self.client.connect(params["host"])
        self.topic = params["topic"]

    def publish(self, payload, topic=None):
        if topic is None:
            topic = self.topic
        json_payload = json.dumps(payload)
        print(json_payload)
        self.client.publish(topic, json_payload)