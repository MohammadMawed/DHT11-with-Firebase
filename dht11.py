import pyrebase  
import os
import time
from datetime import datetime

# initializing the  GPIOS of the raspberry pi



UPLOADING_TIME = "23:05"
UPLOADING_RATE = 60

firebaseConfig = {
    'apiKey': "AIzaSyDVoFl4w7UsQCMS6Di16ryTG5rwRQLkJ0g",
    'authDomain': "weatherdata-e114b.firebaseapp.com",
    'databaseURL': "https://weatherdata-e114b-default-rtdb.firebaseio.com",
    'projectId': "weatherdata-e114b",
    'storageBucket': "weatherdata-e114b.appspot.com",
    'messagingSenderId': "140725281827",
    'appId': "1:140725281827:web:2bd47dbaaa0b66e9cfbd96",
    'measurementId': "G-PEY711HCPD"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def dailyDataUpdate():
    
    TemperatureSumList = []
    HumiditySumList = []

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    dateOfToday = datetime.today().strftime("%Y-%m-%d")
    

    hourData = db.child("data/hourlyData/").get()
    for data in hourData.each(): 
        dataEach = data.val()["temperature"]
        #print(dataEach)
        key = data.key()
        #Updating the data every hour
        if(key == current_time):
            db.child("data/hourlyData/" + key).update({
                    "humidity": "18",
                    "temperature": "10",
                    "time": current_time,
                    "date": dateOfToday})
            print("Updated!") 

        ##################################
        #Change the time in debugging mode
        ##################################

    if(current_time == UPLOADING_TIME): 
        #updating the daily data at 23:05 every day to prevent calculating data from the previous day
        #At 23:05 every will every child in the database updated   
        temperatureDataHourEach = db.child("data/hourlyData/").child(key).get().val()["temperature"]
        HumidityDataHourEach = db.child("data/hourlyData/").child(key).get().val()["humidity"]

        TemperatureSumList.append(temperatureDataHourEach)
        HumiditySumList.append(HumidityDataHourEach)
    
        #Calculating the average temperature 
        totalStr = [int(item) for item in TemperatureSumList]
        total = sum(totalStr)
        aveTemperature = total / len(totalStr)

        print("================")

        print("ave. temperature: ", aveTemperature)
            
        #Calculating the minimum temperature 
        minTemperature = min(totalStr)
        print("min. temperature: ", minTemperature)
            
        #Calculating minimum temperature time
        hourData1 = db.child("data/hourlyData/").get()
        for data in hourData1.each(): 
            dataEach = data.val()["temperature"]
            
            if(minTemperature == int(dataEach)):
                key = data.key()
                temperatureMinTime = db.child("data/hourlyData/").child(key).get().val()["time"]
                print("min. temperature time: ", temperatureMinTime)


        #Calculating the maximum temperature 
        maxTemperature = max(totalStr)
        print("max. temperature: ", maxTemperature)

        #Calculating the maximum temperature time 
        hourData2 = db.child("data/hourlyData/").get()
        for data in hourData2.each(): 
            dataEach = data.val()["temperature"]
            
            if(maxTemperature == int(dataEach)):
                key = data.key()
                temperatureMaxTime = db.child("data/hourlyData/").child(key).get().val()["time"]
                print("max. temperature time: ", temperatureMaxTime)

        print("================")        

        #######################

        #Calculating the average humidity 
        totalStrHumidity = [int(item) for item in HumiditySumList]
        totalHumidity = sum(totalStrHumidity)
        aveHumidity = totalHumidity / len(totalStrHumidity)
        print("ave. humidity: ", aveHumidity)
            
        #Calculating the minimum humidity 
        minHumidity = min(totalStrHumidity)
        print("min. humidity: ", minHumidity)
            
        #Calculating minimum humidity time    
        hourData3 = db.child("data/hourlyData/").get()
        for data in hourData3.each(): 
            dataEach = data.val()["humidity"]
            
            if(minHumidity == int(dataEach)):
                key = data.key()
                humidityMinTime = db.child("data/hourlyData/").child(key).get().val()["time"]
                print("min. humidity time: ", humidityMinTime)

        #Calculating the maximum humidity 
        maxHumidity = max(totalStrHumidity)
        print("max. humidity: ", maxHumidity)

        #Calculating maximum humidity time
        hourData4 = db.child("data/hourlyData/").get()
        for data in hourData4.each(): 
            dataEach = data.val()["humidity"]
            
            if(maxHumidity == int(dataEach)):
                key = data.key()
                humidityMaxTime = db.child("data/hourlyData/").child(key).get().val()["time"]
                print("max. humidity time: ", humidityMaxTime)
            
        #Uploading result data and the calculations to day child to visualize it in the android app
        db.child("/data/averageData/").push({
                        "maxTemperature": str(maxTemperature),
                        "minTemperature": str(minTemperature),
                        "minTemperatureTime": temperatureMinTime,
                        "maxTemperatureTime": temperatureMaxTime,
                        "aveTemperature": str(aveTemperature),

                        "maxHumidity": str(maxHumidity),
                        "minHumidity": str(minHumidity),
                        "minHumidityTime": humidityMinTime,
                        "maxHumidityTime": humidityMaxTime,
                        "aveHumidity": str(aveHumidity),
                        "date": dateOfToday,
                        "time": current_time})

        print("================")
    else:
        print("Waiting til ", UPLOADING_TIME)

while True:  
        dailyDataUpdate()
        
        time.sleep(UPLOADING_RATE) 

         