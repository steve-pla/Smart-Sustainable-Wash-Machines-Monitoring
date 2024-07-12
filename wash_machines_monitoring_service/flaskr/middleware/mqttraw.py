import os
from paho.mqtt.client import Client as MQTTClient
from pymongo import MongoClient
from flaskr.utils.configurator import read_config
# Get the absolute path to the root directory
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# Path to the config.yaml file
config_path = os.path.join(root_dir, 'config.yaml')

configuration = read_config(config_path)
config['MQTT_BROKER_URL'] = configuration['mqtt_info']['broker']['ip']
config['MQTT_BROKER_PORT'] = configuration['mqtt_info']['broker']['port']
mqtt = Mqtt()
mqtt_topics = configuration['mqtt_info']['topics']
topic_names = [topic['name'] for topic in mqtt_topics]
mqtt_client = MQTTClient()
mqtt_client.connect(config['MQTT_BROKER_URL'], config['MQTT_BROKER_PORT'])
wash_object = Wash()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    client.subscribe([(topic_names[0], 0), (topic_names[1], 0)])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    val = float(payload)
    raw_writer(topic, payload, wash_timestamp_state)


def raw_writer(topic, payload, wash_timestamp_state):
    global wash_object
    wash_object.set(topic, payload, wash_timestamp_state)
    wash_object.write_to_db(configuration['data_source']['mongodb']['ip'],
                            configuration['data_source']['mongodb']['port'],
                            configuration['data_source']['mongodb']['db_name'])