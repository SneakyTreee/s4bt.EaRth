import getData
import time
import json

    
    
def postRes():
    
    info = {
        "text":text,
        "device_id": device,
        "soil_raw": value,
        "soil_percent": value_percent,
        "temperature": temperature,
        "humidity": humidity,
        "battery": battery,
        "watering_status": watering,
        "last_watered": last_watered,
        "timestamp": timestamp
}
    
    
    
    with open('res.json',"w") as file:
        json.dump(info,file ,indent=4,ensure_ascii=False)
        
    
def Trocken():
    global text
    text = (
        f"⚠️ {name} benötigt dringend Wasser. "
        "Die Erde ist zu trocken und die Pflanze sollte möglichst bald gegossen werden, "
        "damit sie gesund bleibt."
  
    )
    postRes()


def Normal():
    global text
    text = (
        f"✅ {name} geht es hervorragend. "
        "Die Bodenfeuchtigkeit ist optimal und die Pflanze befindet sich in einem gesunden Zustand. "
        "Im Moment ist kein Gießen erforderlich."
      
    )
    postRes()


def SehrFeucht():
    global text
    text = (
        f"💧 {name} hat aktuell ausreichend Wasser. "
        "Die Erde ist etwas feuchter als ideal. Bitte vor dem nächsten Gießen warten, "
        "damit die Wurzeln nicht zu nass werden."
 
    )
    postRes()


################# Temp ##########################

def wueste():
    global text
    text = (
        f"🚨 {name} ist extrem trocken! "
        "Die Bodenfeuchtigkeit ist kritisch niedrig. "
        "Bitte die Pflanze sofort gründlich gießen, um Trockenschäden zu vermeiden."
  
    )
    postRes()
    


def wasser():
    global text
    text = (
        f"🌊 {name} hat deutlich zu viel Wasser. "
        "Die Erde ist stark durchnässt. Bitte vorerst nicht mehr gießen und überschüssiges Wasser "
        "ablaufen lassen, um Staunässe und Wurzelfäule zu verhindern."


    )
    postRes()

###############################################
    
    
def start():    
    while True:
        try:
            
            data=getData.getData()

            
            global name       
            global device 
            global value
            global value_percent
            global temperature
            global humidity
            global battery
            global watering
            global last_watered
            global timestamp
            global info

              
            device = data["device-id"]
            name = data["plant_name"]
            value = data["soil_moisture_raw"]
            value_percent = data["soil_moisture"]
            temperature = data["temperature"]
            humidity = data["air_humidity"]
            battery = data["battery_voltage"]
            watering = data["watering_required"]
            last_watered = data["last_watered"]
            timestamp = data["timestamp"]
            
            
  
            #time.sleep(300 * 3) # 15 min
            time.sleep(2)

            if value >= 3500:
                wueste()
            elif 3000 <= value < 3500:
                Trocken()
            elif 1800 <= value < 3000:
                Normal()
            elif 900 <= value < 1800:
                SehrFeucht()
            elif 0 <= value < 900:
                wasser()
                
                
        except Exception as error:
            print(error)
            
            


    

start()