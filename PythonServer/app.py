from flask import Flask, request
from configparser import ConfigParser
from mqtt_connection import MQTTConnection
from twilio_connection import TwilioConnection
import json


def config(section, filename='config.ini'):
    parser = ConfigParser()
    parser.read(filename)

    values = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    print(values)
    return values


publisher = MQTTConnection(config("mqtt"))
twilio = TwilioConnection(config("twilio"))

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route("/publish/", methods=['POST'])
def publish():
    payload = json.dumps(request.get_json())
    publisher.publish(payload)
    twilio.send_message("Hi there!", '+15199659801')
    return "Success!"


if __name__ == '__main__':
   app.run("localhost", 8000)
