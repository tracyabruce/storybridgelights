# Story Bridge - read table and date for colour of LEDs in strand - strand is GRB
# Tracy Bruce 29 November 2025, latest edit 19 May 2026

# Input buttons code from Pi Hut Day 3 Let it Glow
# LED strand code based on Pi Hut Let it Glow Day 10
# OLED code from Core Electronics PiicoDev-SSD1306
# current weather code from ChatGPT
# logic to call API only hourly from Codex
# logic to call dates.json file from GitHub raw from Codex

# buttons, temp sensor, and OLED powered by pin 5 (3.3v)
# LED strand powered by pin 40 (vbus 5v)

# Red button going to pin 22 (gp 17)
# Green button going to pin 21 (gp 16)

# Story Bridge - read web table and date for colour of LEDs in strand - strand is GRB

from machine import I2C, Pin
from neopixel import NeoPixel
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms
from dht20 import DHT20
import time
import network
import ntptime
import urequests
import ujson

# Buttons
redbutton = Pin(17, Pin.IN, Pin.PULL_DOWN)
greenbutton = Pin(16, Pin.IN, Pin.PULL_DOWN)

# LED strand details
GPIOnumber = 2
LEDcount = 15
strand = NeoPixel(Pin(GPIOnumber), LEDcount)

# Timezone offset in seconds
TIME_OFFSET = 36000 # Sydney 10 hours ahead

# OLED/sensor I2C pins/BUS/address
SDA = 26
SCL = 27
I2C_BUS = 1
TEMP_ADDR = 0x38

# setup OLED I2C
#oledi2c = I2C(I2C_BUS, sda=Pin(SDA), scl=Pin(SCL))
display = create_PiicoDev_SSD1306(0x3C,1,400000,26,27,0)

# Set up temperature sensor I2C
tempi2c = I2C(I2C_BUS, sda=Pin(SDA), scl=Pin(SCL), freq=400000)
dht20 = DHT20(TEMP_ADDR, tempi2c)

# WiFi details
ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'

# Online dates table
DATES_URL = "https://raw.githubusercontent.com/tracyabruce/storybridgelights/main/dates.json"

# New Farm, QLD coordinates
LATQ = -27.4689
LONQ = 153.0480

# Hornsby, NSW coordinates
LAT = -33.7047
LON = 151.0987

#api call for queensland weather
API_URLQ = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude={}&longitude={}&current_weather=true"
).format(LATQ, LONQ)

#api call for daily forecast for local weather
API_URLL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude={}&longitude={}"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min"
    "&forecast_days=1&timezone=auto"
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

colour_map = {
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
    "white": white
}

# Used if web table fails or date is missing
fallback_colour_names = ["blue", "gold", "blue", "gold", "blue"]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(0.5)

    print("WiFi connected")
    print(wlan.ifconfig())

def sync_time():
    try:
        print("Syncing time with NTP...")
        ntptime.settime()
        print("Time synced")
    except Exception as e:
        print("NTP sync failed:", e)

def get_dates_table():
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
        print("Using colours from web table for", key)
        return dates_table[key]

    print("No web colours found for", key)
    print("Using fallback colours")
    return fallback_colour_names

def show_colour_sequence_from_names(colour_names):
    for group in range(5):
        colour_name = colour_names[group]

        if colour_name in colour_map:
            colour = colour_map[colour_name]
        else:
            colour = colour_map["off"]

        start = group * 3

        strand[start] = colour
        strand[start + 1] = colour
        strand[start + 2] = colour

    strand.write()

def get_current_temp():
    try:
        response = urequests.get(API_URLQ)
        data = response.json()
        response.close()

        temp = data["current_weather"]["temperature"]
        return temp

    except Exception as e:
        print("Error fetching temperature:", e)
        return None

def get_json(url):
    r = urequests.get(url)
    try:
        return r.json()
    finally:
        r.close()

# Connect to network
connect_wifi()
sync_time()

# Turn off LEDs before program start
strand.fill((0, 0, 0))
strand.write()

forecast = get_json(API_URLL)
daily = forecast.get("daily", {})
wcode = daily.get("weather_code",[])
max_temps = daily.get("temperature_2m_max", [])
min_temps = daily.get("temperature_2m_min", [])

max_temp = round(max_temps[0]) if max_temps else None
min_temp = round(min_temps[0]) if min_temps else None

# Download dates table once at startup
dates_table = get_dates_table()

# Get current date
current_time_tuple = time.localtime(time.time() + TIME_OFFSET)
month = current_time_tuple[1]
day = current_time_tuple[2]

# write static OLED text
display.fill(0)
display.text("Brisbane:",0,1)
display.text("Local Temp:",0,16)
display.text("Mx {}".format(max_temp if max_temp is not None else "--"), 0, 31)
display.text("Mn {}".format(min_temp if min_temp is not None else "--"), 0, 45)
display.fill_rect(100,0,20,10,0) #clear previous temp from display
display.fill_rect(100,16,20,10,0) #clear previous temp from display
display.show()

# Simplify WMO codes from open-meteo into 5 broad weather forecasts to display icon
if wcode[0] < 2:
    # display sunny
    display.load_pbm('sunny.pbm',1)
elif wcode[0] < 3:
    # display partly cloudy
    display.load_pbm('partly.pbm',1)
elif wcode[0] < 4:
    # display cloudy
    display.load_pbm('cloudy.pbm',1)
elif wcode[0] < 80:
    # display rain
    display.load_pbm('rainy.pbm',1)
else:
    # display stormy
    display.load_pbm('stormy.pbm',1)
display.show()

# Weather refresh settings
WEATHER_REFRESH_SECONDS = 60 * 60
LOCAL_DISPLAY_REFRESH_SECONDS = 10 * 60

last_weather_call = None
last_local_display_refresh = None
intQtemp = None
event_text = ""

previous_green_value = 0
while True:
    time.sleep(0.1)
    now = time.time()
    
    green_value = greenbutton.value()
    green_pressed = green_value == 1 and previous_green_value == 0
    
    if green_pressed:
        print("Green button pressed")

                    
        if last_weather_call is None or now - last_weather_call >= WEATHER_REFRESH_SECONDS:
            Qtemp = get_current_temp()
            last_weather_call = now

            if Qtemp is not None:
                intQtemp = round(Qtemp)

        date_info = get_colour_names_for_date(dates_table, month, day)
        colour_names = date_info[:5]
        event_text = date_info[5] if len(date_info) > 5 else ""
        
        show_colour_sequence_from_names(colour_names)
        
     
    if redbutton.value() == 1:
        print("Red button pressed")
        strand.fill((0, 0, 0))
        strand.write()
    
    previous_green_value = green_value    
    
    #only refresh local temp and humidity every 10 minutes, or if green button pressed:
    
    if (
        green_pressed
        or last_local_display_refresh is None
        or now - last_local_display_refresh >= LOCAL_DISPLAY_REFRESH_SECONDS
    ):
        
        last_local_display_refresh = now    
        
        measurements = dht20.measurements

        inttemp = round(measurements["t"])
        inthum = round(measurements["rh"])
        
        display.fill_rect(100,16,20,10,0) #clear previous temp from display
        display.fill_rect(100,45,20,10,0) #clear previous hum from display
        display.show()
            
        display.text(str(inttemp),100,16)
        display.text("H",110,36)
        display.text(str(inthum),100,45)
        display.text("%",116,45)
                    
        if intQtemp is not None:
            display.fill_rect(100,1,20,10,0) #clear previous temp from display
            display.text(str(intQtemp),100,1)
        
        display.fill_rect(0,56,128,8,0)
        
        if event_text:
            display.text(event_text,27,56)
                
        display.show()
