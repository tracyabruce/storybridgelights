# Security Notes

## Secrets

`config.py` is the only place real WiFi credentials should live. It is ignored by Git and should stay local to the Pico W setup machine.

Never commit:

- real WiFi names or passwords
- `.env` files
- private keys or certificates
- generated package archives that may contain stale files

If credentials were ever pushed to GitHub or shared publicly, rotate the WiFi password. Removing the value from the latest commit is not enough if it exists in Git history.

## Location Privacy

Local weather coordinates should be stored in `config.py`. The public source uses the example Brisbane coordinates so a GitHub upload does not reveal a private device location.

## Network Data

The date table is fetched over the network and should be treated as untrusted input. `StoryBridge.py` validates that the downloaded JSON is an object and that the first five colour values are known colour names before using them.

## Dependencies

This project depends on MicroPython firmware plus device libraries for NeoPixel, PiicoDev SSD1306, and DHT20. Only add third-party drivers to the repository when their license allows redistribution.

## Reporting

For a private hobby project, report security issues directly to the repository owner. Avoid posting live credentials, private coordinates, or device network details in public issues.
