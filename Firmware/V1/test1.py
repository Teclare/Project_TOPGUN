
#Common
import time

#================================

#Base Setting

originalDevID = '0'
originalSN = '001'

interval = 5

#================================

#HTTP connection
import requests
import json

def send_data(devID, contID, SN, humanInfo, cadaInfo):
    url = "http://104.248.99.126:10540/send_data"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "devID": str(devID),
        "contID": str(contID),
        "SN": str(SN),
        "humanInfo": str(humanInfo),
        "cadaInfo": str(cadaInfo)
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.text

#=================================

#Xbee recieve
import serial

uart_port = '/dev/ttyS0'
baud_rate = 9600 

ser = serial.Serial(uart_port, baud_rate, timeout=1)

#=================================


def main():
    while True:
    
        #XBee Recieved and Upload
        if ser.inWaiting():
              recieved_info = ser.readline().decode('utf-8').strip()
              print("Received: ", recieved_info)
    
              devID, SN, humanInfo, cadaInfo = str(recieved_info).split('@')[:-1]
              
          
              response_text = send_data(devID, originalDevID, SN, humanInfo, cadaInfo)
              
              print("===============\n devID: ", devID, "\n contID: ", originalDevID, "\n SN: ", SN, "\n humanInfo: ", humanInfo, "\n cadaInfo: ", cadaInfo, "\n ===============")
              print(f"responce: {response_text}")
                      

        



if __name__ == "__main__":
    main()
