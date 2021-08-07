FROM python:buster

RUN set -xe; \
    apt-get update; \
    apt-get install -y \
      g++ \
      make \
      ; \
    pip install \
      Adafruit-Blinka \
      Adafruit-SSD1306 \
      adafruit-circuitpython-busdevice \
      adafruit-circuitpython-framebuf \
      Pillow \
      psutil \
      rpi-gpio \
      ;

ADD display.py /display.py

ENTRYPOINT ["python3", "/display.py"]