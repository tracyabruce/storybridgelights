# StoryBridge

MicroPython code for a Raspberry Pi Pico W bridge lighting project. The program reads the current date, retrieves a date/colour sequence from a web-hosted JSON file, and lights a 15 LED NeoPixel strand in 5 groups of 3 LEDs.

If the online table cannot be fetched, today's date is missing, or a colour name is not recognised, the program uses the built-in fallback sequence:

```text
blue, gold, blue, gold, blue
```

## Files

- `StoryBridge.py` - main MicroPython program for the Pico W.
- `storybridge-dates.example.json` - example online date/colour table.
- `config.example.py` - template for local WiFi and table URL settings.
- `.gitignore` - keeps `config.py` and generated files out of GitHub.

## Setup

1. Copy `config.example.py` to `config.py`.
2. Edit `config.py` with your WiFi name, WiFi password, and hosted date table URL.
3. Upload these files to the Pico W:
   - `StoryBridge.py`
   - `config.py`
   - `lcd_api.py`
   - `pico_i2c_lcd.py`
   - `dht20.py`
4. Host `storybridge-dates.example.json` somewhere public and update `DATES_URL` in `config.py`.

Example `config.py`:

```python
SSID = "My WiFi"
PASSWORD = "My Password"
DATES_URL = "https://example.com/storybridge-dates.json"
```

## Date Table Format

The JSON file uses `MM-DD` as the date key. Each date must contain exactly five colour names:

```json
{
  "05-01": ["blue", "gold", "blue", "gold", "blue"],
  "05-02": ["blue", "gold", "blue", "gold", "blue"],
  "06-30": ["blue", "gold", "blue", "gold", "blue"]
}
```

The available colour names are:

```text
off, green, red, maroon, blue, teal, yellow, orange, gold, purple, pink, white
```

## Notes

- Do not commit your real `config.py` because it contains your WiFi password.
- If your web server does not allow `.json`, the content can still be JSON as long as the URL returns plain text containing the JSON table.
- The timezone offset is set to Sydney daylight saving time in `StoryBridge.py`. Adjust `TIME_OFFSET` if needed.
