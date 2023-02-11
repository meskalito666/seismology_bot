import requests
from typing import Dict
from consts import TOKEN_TG_BOT, TG_API_URL, CHANEL_ID
from data_handler import get_location_name, get_map_link, get_time



def format_string(info: Dict) -> str:
    # get type of action
    if info['action'] == 'create':
        action = 'New earthquake! \n'
    elif info['action'] == 'update':
        action = 'Update. \n'
    else:
        action = ''
        
    # get magnitude
    if info['mag']:
        mag = f'mag: {info["mag"]} \n'
    else:
        mag = ''

    # get time from json
    # if info['time']:
    #     time = f'time: {info["time"]} \n'
    # else:
    #     time = ''

    # get Armeninan local time
    time = get_time()
    # get location
    lacation_name = get_location_name(info['location'][1], info['location'][0])
    # get map link
    map_link = get_map_link(info['location'][1], info['location'][0])

    return action + time + mag + lacation_name + map_link


def send_message(message: str) -> None:
    url = TG_API_URL + TOKEN_TG_BOT
    method = url + "/sendMessage"

    r = requests.post(
       method, 
       data={
        "chat_id": CHANEL_ID,
        "text": message,
        "parse_mode": "HTML"
        })

    if r.status_code != 200:
        raise Exception("post_text error")

if __name__ == '__main__':
    send_message('test msg')