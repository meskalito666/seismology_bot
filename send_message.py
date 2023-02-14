import requests
from consts import TOKEN_TG_BOT, TG_API_URL, CHANEL_ID



def send_message(message: str, chat_id: str=CHANEL_ID) -> None:
    url = TG_API_URL + TOKEN_TG_BOT
    method = url + "/sendMessage"

    r = requests.post(
       method, 
       data={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
        })
    
    if r.status_code != 200:
        print("Error sending message")

if __name__ == '__main__':
    send_message('test msg')