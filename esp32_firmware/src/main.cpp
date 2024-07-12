#include <Arduino.h>
#include <driver/adc.h>
#include "EmonLib.h"   
#include <math.h>     
#include <PubSubClient.h> 
#include <WiFi.h>


// WiFi Credentials 
const char* ssid = "wash_samos_aegean_net";
const char* password = "xe98asp4519_aegean!";

// MQTT essentials
const char* mqttServer = "10.10.10.151";
const int mqttPort = 1883;
const char* mqtt_topic_1 = "wash_samos_1/ampere";
const char* mqtt_topic_2 = "wash_samos_2/ampere";

// Initialize WiFi client
WiFiClient wifiClient;
// Initialize PubSub client
PubSubClient pubSubClient(wifiClient);

//CT Clamp 
EnergyMonitor emon1;   // Create an instance
EnergyMonitor emon2;   // Create an instance
#define ADC_CURRENT_INPUT_1 34
#define ADC_CURRENT_INPUT_2 32
#define HOME_VOLTAGE 232


// WiFi Setup Function
void setup_wifi() {
  Serial.println("121");
  delay(20);
  // Start connection to wifi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP Address: ");
  Serial.println(WiFi.localIP());
}


void setup() {
  // <-- CT Clamp Sensor Code Setup --> //
 //adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
 //analogReadResolution(10);
 emon1.current(ADC_CURRENT_INPUT_1, 6.4);
 emon2.current(ADC_CURRENT_INPUT_2, 6.4);

  // Start the serial monitor
  Serial.begin(115200);  
    // setup wifi && connect
  setup_wifi();
  // setup mqtt broker details
  pubSubClient.setServer(mqttServer, mqttPort);
  delay(1000);
}

// Reconnect in MQTT Broker 
void mqtt_reconnect () {
  // Run until we get reconnected
  while (!pubSubClient.connected()) {
    Serial.print("Attempting MQTT connection....");
    // Attempt to connect
    if (pubSubClient.connect("ESP32Client")) {
      Serial.println("connected");
    }
    else {
      Serial.print("Failed rc= ");
      Serial.print(pubSubClient.state());
      Serial.print(" try again in 5 seconds");
      Serial.println("");
      // Wait 5 sec
      delay(5000);  
    }
  }
  
}

void loop() {
    // Connect to MQTT Broker
  if (!pubSubClient.connected()) {
    mqtt_reconnect();
  }

  // Maintain connection to the server
  pubSubClient.loop();

// <-- CT Clamp Sensor -->  // 

  double Irms1 = emon1.calcIrms(1480); 
  double Irms2 = emon2.calcIrms(1480); 
  // Display Current
  Serial.print("I = : ");
  Serial.println(Irms1);
  Serial.print("I = : ");
  Serial.println(Irms2);
  // Display Power
  Serial.print("Power: ");
  Serial.println(Irms1*HOME_VOLTAGE);
  Serial.print("Power: ");
  Serial.println(Irms2*HOME_VOLTAGE);
   // Typecasting float to String
  String IrmsToString1 = String(Irms1);
  String IrmsToString2 = String(Irms2);

  // Send temperature to MQTT topic
  pubSubClient.publish(mqtt_topic_1, IrmsToString1.c_str());
  pubSubClient.publish(mqtt_topic_2, IrmsToString2.c_str());


  delay(500);
}