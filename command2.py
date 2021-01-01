import dht
import network
import ntptime
import ujson
import utime

from machine import RTC
from machine import Pin
from time import sleep
from third_party import rd_jwt

from umqtt.simple import MQTTClient


# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "Nama"
AP_PASSWORD = "2020agustus"

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "raspberrypi"
MQTT_BRIDGE_PORT = 1883

# ID of the Device
DEVICE_ID = "esp32_dht22"


dht22_obj = dht.DHT22(Pin(4))
led_obj = Pin(23, Pin.OUT)
def read_dht22():
    pesan = input("pesan: ")
    print("Sending command to device")
    command = 'PING!'
    data = command.encode("utf-8")
    if(pesan == 'PING!'):
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)

    
    

def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
        wlan.active(True)
        wlan.connect(AP_SSID, AP_PASSWORD)
        # Loop until connected
        while not wlan.isconnected():
            pass
    
    # Connected
    print("  Connected:", wlan.ifconfig())


def set_time():
    # Update machine with NTP server
    print("Updating machine time...")

    # Loop until connected to NTP Server
    while True:
        try:
            # Connect to NTP server and set machine time
            ntptime.settime()
            # Success, break out off loop
            break
        except OSError as err:
            # Fail to connect to NTP Server
            print("  Fail to connect to NTP server, retrying (Error: {})....".format(err))
            # Wait before reattempting. Note: Better approach exponential instead of fix wiat time
            utime.sleep(0.5)
    
    # Succeeded in updating machine time
    print("  Time set to:", RTC().datetime())


def on_message(topic, message):
    print((topic,message))


def get_client():
    #Create our MQTT client.
    client = MQTTClient(client_id=DEVICE_ID,
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/temperature'
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)

# Connect to Wifi
connect()
# Set machine time to now
set_time()


# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client()
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")

# Read from DHT22
print("Reading from DHT22")
result = read_dht22()
#print("  Temperature:", result)

# Publish a message
print("Publishing message...")
if result == None:
    result = "PING!"
publish(client, result)
# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()