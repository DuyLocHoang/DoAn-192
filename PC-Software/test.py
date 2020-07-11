from tkinter import *
import paho.mqtt.client as mqtt
from datetime import datetime
import gui
import json
MQTT_Topic_Control = "Control"

def Sensor_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)
    PH = json_Dict['PH']
    Humidity = json_Dict['Humidity']
    EC = json_Dict['EC']
    Light = json_Dict['Light']
    Date = json_Dict['Date']
    Temperature = json_Dict['Temperature']
    Pump1 = json_Dict['NuA']
    Pump2 = json_Dict['NuB']
    Water = json_Dict['WIn']
    garden_Temperature.reading.set(Temperature)
    garden_PH.reading.set(PH)
    garden_EC.reading.set(EC)
    garden_Humidity.reading.set(Humidity)
    garden_Light.reading.set(Light)
    garden_Date.reading.set(Date)
    garden_Pump1.reading.set(Pump1)
    garden_Pump2.reading.set(Pump2)
    garden_Water.reading.set(Water)

def update_meters(topic, value):
    if topic == "Sensor":
        Sensor_Data_Handler(value)

def Pulish_To_Topic(topic, message1,message2, message3):
    message_dict = {}
    message_dict['Control_Pump1'] = message1
    message_dict['Control_Pump2'] = message2
    message_dict['Control_Water'] = message3
    message_dict['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S")
    message_json = json.dumps(message_dict)
    client.publish(topic,message_json)
    print("Published:" + str(message_json) + " " + "on MQTT Topic: " + str(topic))




def send_message1( en1,en2):
    msg1 = en1.get()
    msg2 = en2.get()
    msg3 = "u"
    if msg1 == '' :
        msg1 = 0    
    if msg2 == '' :
        msg2 = 0
    Pulish_To_Topic(MQTT_Topic_Control,msg1,msg2,msg3)
def send_message2(en3):
    msg1 = "u"
    msg2 = "u"
    msg3 = en3.get()
    Pulish_To_Topic(MQTT_Topic_Control,msg1,msg2,msg3) 

def quit_program(client):
    client.loop_stop()
    client.disconnect()
    print("Closed connection")
    exit()
def on_connect(client, userdata, flags, rc):
    if rc == 0 :
        status_data.set("Connected")
    else :
        status_data.set("Not Connected")
    print("Connected With Result Code "+str(rc))
    print("Connecting to MQTT BROKER : {}".format(MQTT_Broker))


def on_message(client, userdata, message):
    print(message.topic + " Received: " + message.payload.decode())
    update_meters(message.topic, message.payload.decode())
def on_publish(client, userdata, rc):
    pass

# Establishing Connection
broker_url = "192.168.100.11"
broker_port = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("Sensor", qos=1)
###########

# Initiating Main Application Window
iot = Tk()
iot.geometry("900x400")


iot.title("DO_AN_192_Team1")

###########

# Office Frame

garden_Temperature = gui.ReadingMeter(550, 50, "Temp","Celcius")
garden_PH = gui.ReadingMeter(550, 80, "PH","pH")
garden_Humidity = gui.ReadingMeter(550, 110, "Humidity","%")
garden_EC = gui.ReadingMeter(550, 140, "EC","mS/cm")
garden_Light = gui.ReadingMeter(550, 170, "Light","Lux")
garden_Pump1 = gui.ReadingMeter(200, 50, "","l")
garden_Pump2 = gui.ReadingMeter(200, 80, "","l")
garden_Water = gui.ReadingMeter(200, 110, "","l")
# garden_Temperature.reading.set(Temperature)
# garden_PH.reading.set(PH)
# garden_EC.reading.set(EC)
# garden_Humidity.reading.set(Humidity)
# garden_Light.reading.set(Light)
# garden_Date.reading.set(Date)
# garden_Pump1.reading.set(Pump1)
# garden_Pump2.reading.set(Pump2)
# garden_Water.reading.set(Water)
# ###########

# Bedroom Frame

###########
# Tạo các Label
lb1 = Label (iot, text = "Set", font =("consolas", 14, "bold"))
lb1.place (x = 145, y=10)
lb2 = Label (iot, text = "Pumped", font =("consolas", 14, "bold"))
lb2.place (x = 310, y=10)
lb3 = Label (iot, text = "Nutrition A", font =("consolas", 13, "bold"))
lb3.place (x = 6, y=50)
lb4 = Label (iot, text = "l",font =("consolas", 13, "bold"))
lb4.place (x = 210, y=50)
lb5 = Label (iot, text = "Nutrition B", font =("consolas", 13, "bold"))
lb5.place (x = 6, y=80)
lb6 = Label (iot, text = "l",font =("consolas", 13, "bold") )
lb6.place (x = 210, y=80)
lb7 = Label (iot, text = "Water In", font =("consolas", 13, "bold") )
lb7.place (x = 6, y=110)
lb8 = Label (iot, text = "l" ,font =("consolas", 13, "bold"))
lb8.place (x = 210, y=110)

# Khung nhập số liệu
en1 = Entry(iot, font = "Times 13")
en1.place (x = 125, y=50, width = 80 )
en2 = Entry(iot, font = "Times 13")
en2.place (x = 125, y=80, width = 80 ) 
en3 = Entry(iot, font = "Times 13")
en3.place (x = 125, y=110, width = 80 )

#Button
bt1 = Button(iot, text = "PUMB NUTRITION", font = ("consolas", 14, "bold"), bg = "cyan", fg = "white")
bt1.place(x = 80, y = 180, width = 170, height = 30)
bt1['command'] = lambda : send_message1( en1,en2) 
bt2 = Button(iot, text = "PUMP WATER", font = ("consolas", 14, "bold"), bg = "cyan", fg = "white")
bt2.place(x = 270, y = 180, width = 120, height = 30)
bt2['command'] = lambda : send_message2(en3)
q_button = Button(iot, text = "Exit", font = ("consolas",14,"bold"), bg = "cyan", fg = "white")
q_button.place(x = 20, y= 350 , width = 120 , height = 30)
q_button['command'] = lambda: quit_program(client)

# Date_time
garden_Date = gui.DateTime(300, 350, "Date: ")
#Status
status_data = DoubleVar()
status = Label (iot, textvariable = status_data,  font =("consolas", 13, "bold") )
status.place(x= 700 , y =350)
status_label = Label (iot, text = 'Status: ', font =("consolas", 13, "bold") )
status_label.place(x = 610 , y = 350)

client.loop_start()
iot.mainloop()

        