#define BLYNK_PRINT Serial
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <SparkFunTSL2561.h>
#include <Wire.h>
#include <SPI.h>



// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "70b99a6da3334fd5814021939f1187fb";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "EB8212";
char pass[] = "MBUL7BA323492";
BlynkTimer moisture;
BlynkTimer uv;
BlynkTimer sunlight;

float uvIndex;
int val = 0; //value for storing moisture value 
int soilPin = A0;//Declare a variable for the soil moisture sensor 
int soilPower = 4;//Variable for Soil moisture Power

// Create an SFE_TSL2561 object, here called "light":

SFE_TSL2561 light;
double lux;
// Global variables:

boolean gain;    
unsigned int ms; 

void soilEvent()
{
  Blynk.virtualWrite(V4, val);
}

void uvEvent()
{
  Blynk.virtualWrite(V2, uvIndex);
}

void luxEvent()
{
  Blynk.virtualWrite(V1, lux);
}

//Rather than powering the sensor through the 3.3V or 5V pins, 
//we'll use a digital pin to power the sensor. This will 
//prevent corrosion of the sensor as it sits in the soil. 

void setup() 
{
  Serial.begin(9600);   // open serial over USB
  Blynk.begin(auth, ssid, pass);

  pinMode(soilPower, OUTPUT);
  digitalWrite(soilPower, LOW);//Set to LOW so no power is flowing through the sensor
  moisture.setInterval(1000L, soilEvent);
  uv.setInterval(1000L, uvEvent);
  sunlight.setInterval(1000L, luxEvent);
  
  Wire.begin();
  enableUVBSensing(); //UVB + UV_COMP channels activated

  light.begin();

  gain = 0;
  unsigned char time = 2;
  Serial.println("Set timing...");
  light.setTiming(gain,time,ms);
  Serial.println("Powerup...");
  light.setPowerUp();
}

void loop() 
{
  
Serial.print("Soil Moisture = ");    
//get soil moisture value from the function below and print it
Serial.println(readSoil());

delay(1000);//take a reading every second

 Blynk.run();
 moisture.run(); // Initiates BlynkTimer

//--------------------------------------------------------
 uvIndex = getUVIndex();

  Serial.print("UV Index: ");
  Serial.println(uvIndex);
  uv.run();

//--------------------------------------------------------

  unsigned int data0, data1;
  
  if (light.getData(data0,data1))
  {
    boolean good;  // True if neither sensor is saturated
    good = light.getLux(gain,ms,data0,data1,lux);
    Serial.print(" lux: ");
    Serial.print(lux);
    sunlight.run();

  }

}
//This is a function used to get the soil moisture content
int readSoil()
{
    digitalWrite(soilPower, HIGH);//turn D7 "On"
    //delay(10);//wait 10 milliseconds 
    val = analogRead(soilPin);//Read the SIG value form sensor 
    digitalWrite(soilPower, LOW);//turn D7 "Off"
    return val;//send current moisture value
}


