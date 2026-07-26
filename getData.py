import json

def getData():
    global data
    with open('data.json') as jsonData:
        return json.load(jsonData)
        
   
    
