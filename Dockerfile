FROM python:3.9-alpine3.14

RUN set -xe; \
    apk add \
      ttf-freefont \
      g++ \
      libnl3 \
      libnl3-dev \
      linux-headers \
      make \
      ; \
    pip install \
      Adafruit-Blinka \
      adafruit_ssd1306 \
      adafruit-circuitpython-busdevice \
      adafruit-circuitpython-framebuf \
      psutil \
      rpi-gpio \
      ;

ADD display.py /display.py

ENTRYPOINT ["python3", "/display.py"]