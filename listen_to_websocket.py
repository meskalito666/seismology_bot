import json
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado import gen
from typing import Generator
from data_handler import check_location
from send_message import format_string, send_message
from consts import WEB_SOCKET_URL, PING_INTERVAL, TEST_MODE



def processing(message: str) -> None:
    try:
        data = json.loads(message)
        info = data['data']['properties']
        info['action'] = data['action']
        info['location'] = data['data']['geometry']['coordinates']
        latitude, longitude = info['location'][1], info['location'][0]
        
        if TEST_MODE == 'test':
            # send notifications from all over the world (earthquakes happen every ~5 minutes)
            tg_message = format_string(info)
            send_message(tg_message)
        else:
            # send notifications only from Armenia (and from a small area around)
            if check_location(latitude, longitude, info['flynn_region']):
                tg_message = format_string(info)
                send_message(tg_message)

    except Exception:
        print("Unable to parse json message")


@gen.coroutine
def listen(ws) -> Generator:
    while True:
        message = yield ws.read_message()
        if message is None:
            ws = None
            break
        processing(message)


@gen.coroutine
def launch_client() -> Generator:
    try:
        print(f"Open WebSocket connection to {WEB_SOCKET_URL}")
        ws = yield websocket_connect(WEB_SOCKET_URL, ping_interval=PING_INTERVAL)
    except Exception:
        print("connection error")
    else:
        print("Waiting for messages...")
        listen(ws)


if __name__ == '__main__':
    ioloop = IOLoop.instance()
    launch_client()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        print("Close WebSocket")
        ioloop.stop()