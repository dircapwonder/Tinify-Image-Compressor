# Tinify Image Compressor

A small Python project that compresses and resizes images with the [TinyPNG (Tinify) API](https://tinypng.com/developers). It comes in two versions: a desktop app built with Tkinter and a minimal terminal script.

## Features

- Compresses JPG, PNG and WebP images while keeping the original file type
- **Optimized compress:** converts the image to the smallest format (WebP, PNG or JPEG) automatically
- Resizes an image to a given width and height (`fit` method, aspect ratio is preserved)
- Validates the API key before processing and shows your remaining monthly quota (GUI)
- Saves the result next to the original file, so nothing gets overwritten
- Ready-to-use Windows `.exe` of the GUI, no Python installation needed

## Example Output

| Operation | Output file name |
|:---------:|:----------------:|
| Compress (same type) | `compressed_<name>.<ext>` |
| Optimized compress | `optimized_<name>.<best ext>` |
| Resize | `resized_<name>.<ext>` |

The terminal version uses `optimized_`, `most_optimized_` and `resized_` as prefixes.

## Project Structure

```
.
├── TinifyImageGUI.py    # Tkinter desktop app (JPG, JPEG, PNG, WebP)
└──TinifyTerminal.py    # Command-line version (JPG only)
```

## Requirements

- Python 3.8+
- A free [Tinify API key](https://tinypng.com/developers) (500 compressions per month on the free plan)
- Library: `tinify`

```
pip install tinify
```

Tkinter comes with most Python installations. On some Linux distributions you may need `sudo apt install python3-tk`.

## Setup

### GUI

No setup needed. You enter your API key inside the app each time you run it, so it is never stored in the code.

The window icon is loaded from `favicon.ico`. Keep the file in the same folder as the script. If it is missing, the app still starts, just without the custom icon. In the `.exe` build the icon is bundled inside the file, so nothing else is needed.

### Terminal

The terminal version reads the API key from an environment variable named `API_KEY`.

Windows (PowerShell):

```
$env:API_KEY="YOUR API KEY HERE"
```

Linux / macOS:

```
export API_KEY="YOUR API KEY HERE"
```

## Usage

### GUI

```
python TinifyImageGUI.py
```

1. Enter your Tinify API key
2. Click **Select Image** and choose a file
3. Pick **Compress Image** or **Resize Image** and adjust the settings
4. Click **Start Processing**

### Windows Executable

If you don't have Python installed, download `TinifyImageGUI.exe` and double-click it. It works exactly like the GUI version above.

Windows SmartScreen or your antivirus may warn you the first time, because the app is not code-signed. This is common for unsigned PyInstaller builds. If you prefer, you can read the source and run the `.py` file instead.

### Terminal

```
python TinifyTerminal.py
```

1. Choose `1` to compress or `2` to resize
2. Type the image name **without** the `.jpg` extension (the file must be in the current folder)
3. Follow the prompts for the compression type or the new width and height

## Building the Executable

The `.exe` is built with [PyInstaller](https://pyinstaller.org/):

```
pip install pyinstaller
python -m PyInstaller TinifyImageGUI.py --onefile --noconsole --icon=favicon.ico --add-data "favicon.ico;."
```

- `--icon` sets the icon of the `.exe` file itself
- `--add-data` bundles `favicon.ico` into the executable, so the window icon also works when the `.exe` is moved to another folder or computer
- On Linux/macOS use `:` instead of `;` in `--add-data`

The result is created in the `dist` folder.

## How It Works

- **API key check:** the GUI calls `tinify.validate()` first, so a wrong key fails fast with a clear message.
- **Compression:** the image is uploaded with `tinify.from_file()` and the result is saved with `to_file()`.
- **Optimized compress:** `convert()` is given a list of types (`image/webp`, `image/png`, `image/jpeg`) and Tinify returns the smallest one. The file extension is then fixed to match the real output type.
- **Resize:** uses the `fit` method, which scales the image to fit inside the given width and height without cropping or stretching.
- **Quota:** the remaining limit is calculated from `tinify.compression_count`.

## Limitations

- **Terminal version is JPG only:** the `.jpg` extension is hardcoded, and there is no error handling for missing files or API errors.
- **Free plan assumed:** the remaining quota in the GUI is calculated from a fixed limit of 500.
- **Windows only:** the `.exe` is built for Windows. On Linux and macOS, run the `.py` files directly.
- **GUI freezes while processing:** the API call runs on the main thread, so the window does not respond until it finishes.

## Ideas for Improvement

- Support PNG and WebP in the terminal version
- Run the API call in a separate thread so the GUI stays responsive
- Process multiple images or a whole folder at once
- Let the user choose the output folder and file name
- Show the original and compressed file sizes after processing
- Add a "Scale by percentage" option for resizing

## Credits

- Image compression by [TinyPNG / Tinify](https://tinypng.com/)

## Disclaimer

This project is for personal and educational use. It is not affiliated with TinyPNG or Tinify.
