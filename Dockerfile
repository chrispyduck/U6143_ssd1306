FROM python:3.9-alpine3.14

RUN set -xe; \
    apk add \
      font-go-mono-nerd-2.1.0-r6 \
      g++ \
      make \
      ; \
    pip install \
      Adafruit-Blinka \
      Adafruit-SSD1306 \
      adafruit-circuitpython-busdevice \
      adafruit-circuitpython-framebuf \
      ethtool \
      rpi-gpio \
      ;

ADD display.py /display.py

ENTRYPOINT ["python3", "/display.py"]