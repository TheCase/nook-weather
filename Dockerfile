FROM python:3.7
#-alpine

RUN pip install requests flask geopy

COPY server.py /
COPY static /static
COPY templates /templates

# Boise, ID
ENV GPS_COORDINATES=43.6166,-116.2008
ENV BIND_PORT=8080
# us = imperial units
ENV DARKSKY_API_UNITS=us
# en = english language
ENV DARKSKY_API_LANG=en

CMD python /server.py
