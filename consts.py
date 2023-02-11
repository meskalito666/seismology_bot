import os



TEST_MODE = os.environ['TEST_MODE'] # should be 'test' if mode ON 

TOKEN_TG_BOT = os.environ['TOKEN_TG_BOT']
CHANEL_ID = os.environ['CHANEL_ID']

WEB_SOCKET_URL = 'wss://www.seismicportal.eu/standing_order/websocket'
TG_API_URL = 'https://api.telegram.org/bot'
GOOGLE_MAP_URL = 'https://maps.google.com/?q={},{}' # 1st - latitude, 2nd - longitude
GEOCODE_URL = 'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={}&longitude={}&localityLanguage=en'

PING_INTERVAL = 15

polygon = {
    'top_left':[40.906133, 40.614540], 
    'top_right':[42.366360, 45.423088],
    'bottom_left':[38.949654, 49.197543],
    'bottom_right':[36.866288, 44.935578]
}

polygon_list = [
    polygon['top_left'],
    polygon['top_right'],
    polygon['bottom_left'],
    polygon['bottom_right']
    ]
