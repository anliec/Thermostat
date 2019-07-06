#include <dht.h>

dht DHT;

#define DHT11_PIN 7
#define RELAY1_PIN 6
#define RELAY2_PIN 5
#define LOOP_DELAY 200
#define MESURE_DELAY 2000

int relay1_status, relay2_status;
float last_temperature, last_humidity;

void setup(){
  Serial.begin(9600);
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  relay1_status = LOW;
  relay2_status = LOW;
  digitalWrite(RELAY1_PIN, relay1_status);
  digitalWrite(RELAY2_PIN, relay2_status);
}

void print_status(){
  Serial.print("t:");
  Serial.println(last_temperature);
  Serial.print("h:");
  Serial.println(last_humidity);
  Serial.print("1:");
  Serial.println(relay1_status);
  Serial.print("2:");
  Serial.println(relay2_status);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  last_temperature = DHT.temperature;
  last_humidity = DHT.humidity;
  print_status();
  int i;
  for(i=0 ; i<MESURE_DELAY ; i+=LOOP_DELAY){
    int v = Serial.read();
    if(v == 48){ // 0
      relay1_status = LOW;
      digitalWrite(RELAY1_PIN, relay1_status);
    }
    else if(v == 49){ // 1
      relay1_status = HIGH;
      digitalWrite(RELAY1_PIN, relay1_status);
    }
    else if(v == 50){ // 2
      relay2_status = LOW;
      digitalWrite(RELAY2_PIN, relay2_status);
    }
    else if(v == 51){ // 3
      relay2_status = HIGH;
      digitalWrite(RELAY2_PIN, relay2_status);
    }
    else if (v != -1){
      Serial.print("ErrorUnknowInput:");
      Serial.println(v);
    }
    if (v != -1){
      print_status();
    }
    delay(LOOP_DELAY);
  }
}

