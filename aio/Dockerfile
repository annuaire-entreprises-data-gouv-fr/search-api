FROM python:3.11

COPY ./aio-proxy /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.pip

EXPOSE 4500

CMD [ "make", "run" ] 
