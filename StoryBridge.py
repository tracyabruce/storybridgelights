# Story Bridge
# Reads an online date/colour table and lights a 15 LED strand in 5 groups of 3.
# Strand colour order is GBR.

from machine import I2C, Pin
from neopixel import NeoPixel
from pico_i2c_lcd import I2cLcd
from dht20 import DHT20
import network
import ntptime
import time
import ujson
import urequests

try:
    from config import SSID, PASSWORD, DATES_URL
except ImportError:
    SSID = ""
    PASSWORD = ""
    DATES_URL = ""

# Buttons
redbutton = Pin(6, Pin.IN, Pin.PULL_DOWN)
greenbutton = Pin(7, Pin.IN, Pin.PULL_DOWN)

# LED strand
GPIOnumber = 2
LEDcount = 15
strand = NeoPixel(Pin(GPIOnumber), LEDcount)

# Sydney daylight saving offset in seconds.
# Adjust if needed outside daylight saving time, or for different location. 39600 for AEDT (11 hours) 36000 for AEST (10 hours)
TIME_OFFSET = 36000

# LCD/sensor I2C pins/BUS/address
SDA = 14
SCL = 15
I2C_BUS = 1
LCD_ADDR = 0x27
TEMP_ADDR = 0x38

LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16

# Set up LCD I2C
lcdi2c = I2C(I2C_BUS, sda=Pin(SDA), scl=Pin(SCL), freq=400000)
lcd = I2cLcd(lcdi2c, LCD_ADDR, LCD_NUM_ROWS, LCD_NUM_COLS)

# Set up temperature sensor I2C
tempi2c = I2C(I2C_BUS, sda=Pin(SDA), scl=Pin(SCL))
dht20 = DHT20(TEMP_ADDR, tempi2c)

# New Farm, QLD coordinates
LAT = -27.4689
LON = 153.0480

API_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude={}&longitude={}&current_weather=true"
).format(LAT, LON)

# Colours - strand is GBR
off = 0, 0, 0
green = 255, 0, 0
red = 0, 0, 255
maroon = 0, 10, 180
blue = 0, 255, 0
teal = 128, 128, 0
yellow = 150, 0, 255
orange = 30, 0, 255
gold = 80, 0, 200
purple = 9, 149, 140
pink = 20, 147, 220
white = 255, 255, 255

COLOUR_MAP = {
    "off": off,
    "green": green,
    "red": red,
    "maroon": maroon,
    "blue": blue,
    "teal": teal,
    "yellow": yellow,
    "orange": orange,
    "gold": gold,
    "purple": purple,
    "pink": pink,
    "white": white,
}

# Used if the web table cannot be fetched, today's date is missing,
# or a colour name in the web table is not recognised.
FALLBACK_COLOUR_NAMES = ["blue", "gold", "blue", "gold", "blue"]


def connect_wifi():
    if SSID == "" or PASSWORD == "":
        print("WiFi details missing. Create config.py from config.example.py.")
        return False

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    start = time.time()

    while not wlan.isconnected():
        if time.time() - start > 20:
            print("WiFi connection timed out")
            return False

        time.sleep(0.5)

    print("WiFi connected")
    print(wlan.ifconfig())
    return True


def sync_time():
    try:
        print("Syncing time with NTP...")
        ntptime.settime()
        print("Time synced")
    except Exception as e:
        print("NTP sync failed:", e)


def get_dates_table():
    if DATES_URL == "":
        print("DATES_URL missing. Create config.py from config.example.py.")
        return None

    try:
        response = urequests.get(DATES_URL)
        text = response.text
        response.close()
        return ujson.loads(text)
    except Exception as e:
        print("Error fetching dates table:", e)
        return None


def get_colour_names_for_date(dates_table, month, day):
    key = "{:02d}-{:02d}".format(month, day)

    if dates_table is not None and key in dates_table:
        colour_names = dates_table[key]

        if len(colour_names) == 5:
            print("Using colours from web table for", key)
            return colour_names

        print("Wrong number of colours for", key)

    else:
        print("No web colours found for", key)

    print("Using fallback colours")
    return FALLBACK_COLOUR_NAMES


def show_colour_sequence_from_names(colour_names):
    for group in range(5):
        colour_name = colour_names[group]
        colour = COLOUR_MAP.get(colour_name, None)

        if colour is None:
            print("Unknown colour:", colour_name)
            colour = COLOUR_MAP[FALLBACK_COLOUR_NAMES[group]]

        start = group * 3
        strand[start] = colour
        strand[start + 1] = colour
        strand[start + 2] = colour

    strand.write()


def get_current_temp():
    try:
        response = urequests.get(API_URL)
        data = response.json()
        response.close()
        return data["current_weather"]["temperature"]
    except Exception as e:
        print("Error fetching temperature:", e)
        return None


# Connect to network and load online date table.
wifi_connected = connect_wifi()

if wifi_connected:
    sync_time()

dates_table = get_dates_table() if wifi_connected else None

# Get the current date and apply local offset.
current_time_tuple = time.localtime(time.time() + TIME_OFFSET)
month = current_time_tuple[1]
day = current_time_tuple[2]

# Write static LCD text.
lcd.putstr("Local Temp:")
lcd.move_to(0, 1)
lcd.putstr("New Farm:")

# Turn off all LEDs before program start.
strand.fill(off)
strand.write()

# Weather refresh settings.
WEATHER_REFRESH_SECONDS = 60 * 60
last_weather_call = None
intQtemp = None

while True:
    time.sleep(0.1)

    if greenbutton.value() == 1:
        print("Green button pressed")

        now = time.time()

        if wifi_connected and (
            last_weather_call is None
            or now - last_weather_call >= WEATHER_REFRESH_SECONDS
        ):
            Qtemp = get_current_temp()
            last_weather_call = now

            if Qtemp is not None:
                intQtemp = round(Qtemp)

        colour_names = get_colour_names_for_date(dates_table, month, day)
        show_colour_sequence_from_names(colour_names)

    if redbutton.value() == 1:
        print("Red button pressed")
        strand.fill(off)
        strand.write()

    measurements = dht20.measurements

    inttemp = round(measurements["t"])
    lcd.move_to(12, 0)
    lcd.putstr(str(inttemp))

    lcd.move_to(12, 1)

    if intQtemp is not None:
        lcd.putstr(str(intQtemp))
