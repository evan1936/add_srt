import requests
import json
url = "http://ip:8000/translate"
#https://github.com/xiaozhou26/deeplx-pro
def invoke_deeplx_api(text):

    payload = json.dumps({
        "text": text,
        "source_lang": "auto",
        "target_lang": "ZH"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).text
    # print(response)
    data = json.loads(response )
    data=data['data']
    # print(data)
    return data


# if __name__ == "__main__":
#     text="world"
#     invoke_deeplx_api(text)
