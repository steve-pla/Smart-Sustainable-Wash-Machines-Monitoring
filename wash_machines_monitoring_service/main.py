import flask
import sys
import os
from flask_mqtt import Mqtt
from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
from flaskr.utils.email_sender import send_email
from paho.mqtt.client import Client as MQTTClient
from datetime import datetime
from flaskr.utils.configurator import read_config


configuration = read_config('config.yaml')
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

app = Flask(__name__, static_url_path='', static_folder='flaskr/static', template_folder='flaskr/templates')
app.config['MQTT_BROKER_URL'] = configuration['mqtt_info']['broker']['ip']
app.config['MQTT_BROKER_PORT'] = configuration['mqtt_info']['broker']['port']
mqtt = Mqtt(app)
mqtt_topics = configuration['mqtt_info']['broker']['topics']
topic_names = [topic['name'] for topic in mqtt_topics]
mqtt_client = MQTTClient()
mqtt_client.connect(app.config['MQTT_BROKER_URL'], app.config['MQTT_BROKER_PORT'])

wash_state_1 = False
wash_state_2 = False
static_counter_start_wash_1 = 0
static_counter_complete_wash_1 = 0
static_counter_complete_wash_1_b = 0
flag1 = 0
wash_1_timestamp_state = None
static_counter_start_wash_2 = 0
static_counter_complete_wash_2 = 0
static_counter_complete_wash_2_b = 0
flag2 = 0
wash_2_timestamp_state = None


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    client.subscribe([(topic_names[0], 0), (topic_names[1], 0)])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    global wash_state_1, static_counter_start_wash_1, static_counter_complete_wash_1, \
        flag1, static_counter_complete_wash_1_b, wash_1_timestamp_state
    global wash_state_2, static_counter_start_wash_2, static_counter_complete_wash_2, \
        static_counter_complete_wash_2_b, flag2, wash_2_timestamp_state

    topic = message.topic
    payload = message.payload.decode()
    val = float(payload)

    if topic == 'wash_samos_1/ampere':
        if 0.16 >= val > 0.01:
            if flag1 == 1:
                if static_counter_complete_wash_1 == 12:
                    flag1 = 0
                    static_counter_complete_wash_1 = 0
                    wash_state_1 = False
                else:
                    static_counter_complete_wash_1 = static_counter_complete_wash_1 + 1
        if val >= 0.17:
            if flag1 == 0:
                if static_counter_complete_wash_1_b == 5:
                    flag1 = 1
                    wash_state_1 = True
                    static_counter_complete_wash_1_b = 0
                    wash_1_timestamp_state = datetime.now().strftime("%H:%M:%S")
                else:
                    static_counter_complete_wash_1_b = static_counter_complete_wash_1_b + 1
    elif topic == 'wash_samos_2/ampere':
        if 0.16 >= val > 0.01:
            if flag2 == 1:
                if static_counter_complete_wash_2 == 12:
                    flag2 = 0
                    static_counter_complete_wash_2 = 0
                    wash_state_2 = False
                else:
                    static_counter_complete_wash_2 = static_counter_complete_wash_2 + 1
        if val >= 0.17:
            if flag2 == 0:
                if static_counter_complete_wash_2_b == 5:
                    flag2 = 1
                    wash_state_2 = True
                    static_counter_complete_wash_2_b = 0
                    wash_2_timestamp_state = datetime.now().strftime("%H:%M:%S")
                else:
                    static_counter_complete_wash_2_b = static_counter_complete_wash_2_b + 1


@app.route('/email_action', methods=["GET", "POST"])
def email_call():
    if request.method == "POST":
        result = send_email(request.form.get('email'), request.form.get('name'),
                            request.form.get('subject'), request.form.get('message'),
                            configuration['email']['sender']['email_s'],
                            configuration['email']['sender']['email_s_pass'])
        return render_template('index.html', email_status=result)


@app.route('/check_status', methods=['GET'])
def check_wash_status():
    global wash_state_1, wash_1_timestamp_state
    global wash_state_2, wash_2_timestamp_state
    return jsonify(state1=wash_state_1, state2=wash_state_2,
                   time1=wash_1_timestamp_state, time2=wash_2_timestamp_state)


@app.route('/', methods=['GET'])
def init():
    return render_template('index.html')


app.run(host='0.0.0.0', port=configuration['web_info']['flask']['port'], debug=True)
