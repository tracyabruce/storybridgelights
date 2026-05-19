# StoryBridge OLED

MicroPython code for a Raspberry Pi Pico W bridge lighting project. The program fetches a date-based colour table, lights a 15 LED NeoPixel strand in 5 groups of 3 LEDs, and shows local weather/temperature information on a PiicoDev SSD1306 OLED.

## Security First

Do not put real WiFi details in `StoryBridge.py`.

1. Copy `config.example.py` to `config.py`.
2. Edit `config.py` with your WiFi name, WiFi password, hosted `dates.json` URL, and any private location coordinates.
3. Keep `config.py` private. It is ignored by `.gitignore` and should not be uploaded to GitHub.

If real credentials were ever committed or shared, rotate the WiFi password before publishing the repository.

## Files

- `StoryBridge.py` - main MicroPython program for the Pico W.
- `config.example.py` - safe template for private `config.py` settings.
- `dates.json` - current date/colour table that can be hosted with GitHub raw content.
- `storybridge-dates.example.json` - smaller example date/colour table.
- `PiicoDev_SSD1306.py` and `PiicoDev_Unified.py` - PiicoDev OLED support files.
- `sunny1.pbm`, `cloudy1.pbm`, `rainy1.pbm`, `stormy1.pbm` - OLED weather icons.
- `.gitignore` - excludes secrets, generated files, and packaging output.
- `SECURITY.md` - project security notes.
- `GITHUB_UPLOAD_CHECKLIST.md` - pre-upload checklist.

## Pico W Setup

Upload these files to the Pico W:

- `StoryBridge.py`
- `config.py`
- `PiicoDev_SSD1306.py`
- `PiicoDev_Unified.py`
- `sunny1.pbm`
- `cloudy1.pbm`
- `rainy1.pbm`
- `stormy1.pbm`
- a compatible MicroPython `dht20.py` driver

This repository does not include `dht20.py`; add the DHT20 driver you use on your Pico W, making sure its license allows redistribution if you later commit it.

## Example Config

```python
SSID = "My WiFi"
PASSWORD = "My Password"
DATES_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY/main/dates.json"

BRISBANE_LAT = -27.4689
BRISBANE_LON = 153.0480
LOCAL_LAT = -27.4689
LOCAL_LON = 153.0480
```

## Date Table Format

The JSON file uses `MM-DD` as the date key. Each date must contain at least five colour names. The program reads the first five values; an optional sixth label may be present for future display text.

```json
{
  "05-01": ["blue", "gold", "blue", "gold", "blue"],
  "05-19": ["purple", "purple", "purple", "purple", "purple", "World IBD"]
}
```

Available colour names:

```text
off, green, red, maroon, blue, teal, yellow, orange, gold, purple, pink, white
```

If the online table cannot be fetched, today's date is missing, or a colour name is not recognised, the program uses:

```text
blue, gold, blue, gold, blue
```

## GitHub Upload Notes

Before publishing, confirm the repository contains only placeholders for credentials. Do not upload `config.py`, `__pycache__/`, `.env` files, or any package created under `dist/`.
