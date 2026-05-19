# GitHub Upload Checklist

Use this checklist before creating a public GitHub repository or uploading the zip package.

- Confirm `StoryBridge.py` does not contain real WiFi credentials.
- Confirm private coordinates are in `config.py`, not committed source.
- Confirm `config.py` is not included in the upload.
- Confirm generated files such as `__pycache__/`, `.pyc`, `.mpy`, and `dist/` are not included.
- Search for accidental secrets before upload:

```powershell
rg -n -i "(password|secret|token|api[_-]?key|ssid|credential|private[_-]?key|bearer)" .
```

- Review any matches and keep only placeholders or documentation examples.
- If real credentials were ever shared publicly, rotate them before publishing.
- Add a license file before making the project public if you want others to reuse the code.

Suggested GitHub upload contents:

- `.gitignore`
- `README.md`
- `SECURITY.md`
- `GITHUB_UPLOAD_CHECKLIST.md`
- `StoryBridge.py`
- `config.example.py`
- `dates.json`
- `storybridge-dates.example.json`
- `PiicoDev_SSD1306.py`
- `PiicoDev_Unified.py`
- `sunny1.pbm`
- `cloudy1.pbm`
- `rainy1.pbm`
- `stormy1.pbm`
