import json
import asyncio
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado import gen
from typing import Generator
from data_handler import check_location, check_time, prepare_msg_for_tg
from send_message import send_message
from shutdown_alert import shutdown_alert
from consts import WEB_SOCKET_URL, PING_INTERVAL, TEST_MODE, ADMIN_ID



def processing(message: str) -> None:
    try:
        data = json.loads(message)
        info = data['data']['properties']
        info['action'] = data['action']
        longitude, latitude, _ = data['data']['geometry']['coordinates']

        if TEST_MODE == 'test':
            # send notifications from all over the world (earthquakes happen every ~5 minutes)
            tg_message = prepare_msg_for_tg(latitude, longitude, info)
            send_message(tg_message)
        else:
            # send notifications only from Armenia (and from a small area around)
            if check_location(latitude, longitude, info['flynn_region']) and check_time(info):
                tg_message = prepare_msg_for_tg(latitude, longitude, info)
                send_message(tg_message)

    except Exception:
        print("Unable to parse json message")


@gen.coroutine
def listen(ws) -> Generator:
    with shutdown_alert() as sa:
        while True:
            time_cheker = asyncio.create_task(sa.timer()) #timer started
            message = yield ws.read_message() #listening to socket
            if message:
                processing(message)
                time_cheker.cancel() # cancel task in order to restart timer 


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
        send_message('service started', ADMIN_ID)
        ioloop.start()
    except KeyboardInterrupt:
        print("Close WebSocket")
        ioloop.stop()

