# Story Bridge Lights

MicroPython project for driving a Story Bridge themed LED strand with OLED weather and date information.

## Files

- `StoryBridge.py` - main program for WiFi, date lookup, LEDs, buttons, OLED, and weather display.
- `PiicoDev_*.py`, `ssd1306.py`, `dht20.py` - hardware support modules.
- `sunny1.pbm`, `cloudy1.pbm`, `rainy1.pbm`, `stormy1.pbm` - OLED weather icons.
- `secrets.example.py` - placeholder credential template.

## Before running

Set your local WiFi details in `StoryBridge.py`:

```python
ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'
```

Do not commit real passwords, API keys, or local credential files. `secrets.py` and `.env` files are ignored by `.gitignore`.

The online dates table URL in `StoryBridge.py` is intentionally left unchanged because it points to the public dates data used by the project.
