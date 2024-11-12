import requests
import json
url = "http://23.172.40.177:8000/translate"
#url = "http://104.160.19.60:8000/translate"
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
