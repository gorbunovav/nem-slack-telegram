FROM python:2-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./slack-telegram/requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./slack-telegram/src/* /usr/src/app/

CMD [ "python", "./bridge.py" ]