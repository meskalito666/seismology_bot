FROM python:3.8-slim-buster
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "listen_to_websocket.py"]