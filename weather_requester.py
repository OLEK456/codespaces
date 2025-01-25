import json
import requests
import time
import os
from paho.mqtt import client as mqtt
from mqtt_sender import MqttSender as mqtt_sender

DATA_FOLDER = "data"
api_key = "71b03d5fa7a6f146e4afa78cb4aa1495949f655d28f8c1d0440b2779634c7ffd"

location = os.environ["location"]#="10566"    #wrocław
broker = os.environ["broker"]#= "broker.hivemq.com" #='167.172.164.168'
port = int(os.environ["port"])
#client_id = f'Aleksander'
username = os.environ["username"] = "261293"
password = os.environ["password"] = "sys.wbud"

class WeatherRequester:

    def __init__(self, city, mqtt_sender):
        self.location = city
        self.mqtt = mqtt_sender


    def loop(self):
        while 1: 
            params = {
                "limit": 1,
                }
            headers = {
                "X-API-Key": api_key
            }

            response = requests.get(f"https://api.openaq.org/v3/locations/{location}",headers=headers, params = params)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results",[])
            
                if results:
                    location_name = results[0].get("name", "Brak nazwy")
                    location_time = results[0].get("datetimeLast", {}).get("local", "Brak wskazania")
                    message = json.dumps({
                        "location": location_name,
                        "timestamp": location_time
                    })
                    print(f"location: {location_name}\ntimestamp: {location_time}\n")
                    self.mqtt.publish("261293/location",message)
                else:
                    print("Brak wyników dla podanej lokalizacji.")
            
            else:
                print(f"Błąd! Status HTTP: {response.status_code}")
                print(response.text)

           
            #exit()
            time.sleep(30)

def save_to_file(nr_indeksu, location, data):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    filename = os.path.join(DATA_FOLDER, f"{nr_indeksu}-{location}.txt")
    try:
        with open(filename, 'a') as file:
            file.write(f"{data}\n")
        print(f"Dane zapisane w pliku: {filename}")
    except Exception as e:
        print(f"Błąd zapisu do pliku {filename}: {e}")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 2:
        nr_indeksu = topic_parts[0]
        locat = topic_parts[1]
        message = msg.payload.decode()
        save_to_file(nr_indeksu, locat, message)

mqtt_client = mqtt_sender(broker,port, username, password)
mqtt_client.connect()

mqtt_client.subscribe("+/location", on_message)
mqtt_client.sub_loop()

requester = WeatherRequester(location, mqtt_client)
requester.loop()