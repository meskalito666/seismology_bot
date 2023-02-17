import asyncio
from send_message import send_message
from consts import ADMIN_ID, WAIT_FOR_SOCKET



class shutdown_alert():
    """
    the context manager sends an alert to ADMIN_ID in case of: \n
        1. error
        2. if the app terminated without an error 
        3. if the socket is silent for WAIT_FOR_SOCKET sec
    """
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: 
            try:
                tg_message = (
                    "\nException type: " + str(exc_type) + \
                    "\nException value: " + str(exc_val) + \
                    "\nTraceback: " + str(exc_tb)
                    ).replace('<', '').replace('>', '')
                send_message(tg_message, ADMIN_ID)

            except:
                send_message('smth went wrong...', ADMIN_ID)
        else:
            send_message('graceful exit', ADMIN_ID)
    
    @staticmethod
    async def timer():
        """
        every iteration in the main loop, the timer is started \n
        if the socket returns None or does not respond within WAIT_FOR_SOCKET sec - an alert will be sent \n
        else - timer will be updated
        """
        await asyncio.sleep(WAIT_FOR_SOCKET)
        send_message(f'socket returns None or is silent for more than {WAIT_FOR_SOCKET/60} min.', ADMIN_ID)
                        
