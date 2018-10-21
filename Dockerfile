FROM python:3.7-alpine

RUN pip install requests flask geopy

COPY server.py /
COPY static /static
COPY templates /templates

ENV BIND_PORT=8080
ENV TZ=America/Boise

# Boise, ID
ENV GPS_COORDINATES=43.6166,-116.2008

CMD python /server.py
