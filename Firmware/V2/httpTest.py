import requests
import json
import time

#================================
devID = 0
contID = 0
SN = 0
humanInfo = 0
cadaInfo = 0
interval = 0
#================================

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

def main():
    while True:
        response_text = send_data(devID, contID, SN, humanInfo, cadaInfo)
        print(f"responce: {response_text}")
        
        time.sleep(interval)

if __name__ == "__main__":
    main()
