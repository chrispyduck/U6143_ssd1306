#!/usr/bin/env python3 

import math
import time
import subprocess
import psutil
import sys

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306

i2c = busio.I2C(SCL, SDA)
disp = Adafruit_SSD1306.SSD1306_128_32(14)

disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 30)
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)

# display adjustment
padding = -2
top = padding
bottom = height - padding
x = 0
y = 0

cpu_count = psutil.cpu_count()

def print_temp(): 
  temp = psutil.sensors_temperatures()
  temp = temp['cpu_thermal'][0].current
  draw_stat("Temperature")
  draw_stat(f'{temp:.2f}C')

def print_cpu():
  cpu = psutil.getloadavg()
  draw_stat(f"CPU: {cpu[0] / cpu_count:.1%}")

  mem = psutil.virtual_memory()
  draw_stat(f'RAM: {((100 - mem.percent) / 100):.1%}')

def draw_stat(text):
  global y
  draw.text((x, y), text, font=font, fill=255)
  y = y + 16

loop_config = {
  0: print_temp,
  1: print_cpu
}
# time adjustment
loop_time = 10 # number of seconds taken for a loop of all stats
loop_parts = len(loop_config) # number of different screens in each loop
loop_divisor = loop_time / loop_parts
sys.stdout.write(f'loop config: {loop_parts} parts, over {loop_time} seconds = {loop_divisor} seconds per part\n')

while True:
  x = 0
  y = 0

  # clear the stat image
  draw.rectangle((0, 0, width, height), outline=0, fill=0)

  # determine which function to execute for the stat display
  t = time.time()
  loop = math.floor((t % loop_time) / loop_divisor)
  #sys.stdout.write(f'loop: {t % loop_time} / {loop_divisor} = {loop}\n')
  #sys.stdout.flush()
  fn = loop_config.get(loop, print_cpu)

  # execute it to render the stat image
  fn()

  # display the computed image
  disp.image(image)
  disp.display()
  time.sleep(0.5)


