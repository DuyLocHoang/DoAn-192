import mysql.connector
import datetime
import json

################################################################
###                Insert sensor data to MySQL               ###
################################################################
def sensors_data_handler(jsonData):
    mydb = mysql.connector.connect(
        host='localhost',
        user="root",
        passwd="duyloc123456",
        database="IoT"
    )
    mycursor = mydb.cursor()

	#Parse Data 
    json_Dict = json.loads(jsonData)                    # parse jsonData
    PH = json_Dict["PH"]
    EC = json_Dict["EC"]
    WaterTemp = 0
    TEMP = json_Dict["Temperature"]
    HUD = json_Dict["Humidity"]
    LIGHT = json_Dict["Light"]
    NuA = json_Dict["NuA"]
    NuB = json_Dict["NuB"]
    WaterIn = json_Dict["WIn"]

    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%Y-%m-%d")
    time = currentDT.strftime("%H:%M:%S")

    sql = "INSERT INTO data (Date, Time, PH, EC, WaterTemp, TEMP, HUD, LIGHT, NuA, NuB, WaterIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (date, time, PH, EC, WaterTemp, TEMP, HUD, LIGHT, NuA, NuB, WaterIn)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "sensors data inserted.")

def control_data_handler(jsonData):
    mydb = mysql.connector.connect(
        host='localhost',
        user="root",
        passwd="duyloc123456",
        database="IoT"
    )
    mycursor = mydb.cursor()

	#Parse Data 
    json_Dict = json.loads(jsonData)                    # parse jsonData
    pump1 = json_Dict["Control_Pump1"]
    pump2 = json_Dict["Control_Pump2"]
    water = json_Dict["Control_Water"]
    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%Y-%m-%d")
    time = currentDT.strftime("%H:%M:%S")

    sql = "INSERT INTO control (date, time, pump1, pump2, water) VALUES (%s,%s,%s,%s,%s)"
    val = (date, time, pump1, pump2, water)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "control data inserted.")


def data_handler(Topic,jsonData):
    print("Inserting data into database.....")
    if Topic == "Sensor":
        sensors_data_handler(jsonData)
    elif Topic == "Control" :
        control_data_handler(jsonData)

#===============================================================
