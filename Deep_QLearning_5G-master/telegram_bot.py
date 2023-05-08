import requests

token = "6178571310:AAEZgSL7naBapMdK1M6Es0lut1LQCcUILGE" 
url="https://api.telegram.org/bot"+token+"/sendMessage"

def sendMessage(message):
    #'chat_id': '787248960' Dani
    
    data = {
        'chat_id': '835968219',  
        'text': message
    }

    response = requests.post(url, data=data)
    print(response)