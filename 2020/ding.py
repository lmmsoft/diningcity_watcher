import requests


class Dingding:
    access_token = "xxx"
    URL = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'

    def send_message(self, text):
        data = {
            "msgtype": "text",
            "text": {
                "content": text,
            },
            # "at": {
            #     "atMobiles": [
            #         "156xxxx8827",
            #         "189xxxx8325"
            #     ],
            #     "isAtAll": False
            # }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(self.URL, json=data, headers=headers)
        print(res.status_code, res.text)
