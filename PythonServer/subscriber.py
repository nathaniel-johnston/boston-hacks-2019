import paho.mqtt.client as mqtt
from db_connection import DBConnection
from app import config

db = DBConnection(config("postgresql"))


def on_message(client, userdata, message):
    pill_id = message.payload.decode("utf-8")
    pill_id = int(pill_id)
    if pill_id:
        dose, quantity = db.execute_query("SELECT dose, quantity FROM pills WHERE id='{}';".format(pill_id))[0]
        new_quantity = quantity - dose
        db.execute("UPDATE pills SET quantity={0} WHERE id={1};"
                   .format(new_quantity, pill_id))


client = mqtt.Client("subscriber-taken")
client.on_message = on_message
client.connect("broker.hivemq.com")
client.subscribe("pillsTaken")
client.loop_forever()
