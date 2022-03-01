FROM python:3.9

COPY ./aio-proxy /app

WORKDIR /app

RUN pip install -r requirements.pip

ENV color=blue

EXPOSE 4500

CMD [ "make", "run" ] 
