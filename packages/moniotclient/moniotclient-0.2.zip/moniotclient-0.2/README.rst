PAHO MQTT IOT CLIENT

>RAILMON
-----------------
:USAGE
simple usage is that:

#import lib
from moniotclient import IotMqttClient

#initilaze a client
client=IotMqttClient.Mqttclient(ipadress,port)#example s=IotMqttClient.Mqttclient("192.168.1.242","32383")


#for sending command to a device
client.pub_Message("open")


//example subscription

from moniotclient import IotMqttClient

//do this when a message comes to the topic
def dothis(client,userdata,message):
    message=str(message.payload.decode("utf-8"))
    print("message received: "+message)


client=IotMqttClient.Mqttclient("192.168.1.242","32383","192.168.1.242","32562")

//add a callback function when a message comes
client.subClient.on_message=dothis

//subscription to a topic(apikey)
client.sub_Server("dev1","/123456/newdevice0/cmd")