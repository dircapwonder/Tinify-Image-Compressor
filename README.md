# Tinify Image Compressor

A small Python project that compresses and resizes images with the [TinyPNG (Tinify) API](https://tinypng.com/developers). It comes in two versions: a desktop app built with Tkinter and a minimal terminal script.

<img width="558" height="627" alt="Image" src="https://github.com/user-attachments/assets/af209ed2-439f-4074-bfc5-e56f9031f8f8" />

## Features

- Compresses JPG, PNG and WebP images while keeping the original file type
- Optimized compress: converts the image to the smallest format (WebP, PNG or JPEG) automatically
- Resizes an image to a given width and height (`fit` method, aspect ratio is preserved)
- Validates the API key before processing and shows your remaining monthly quota (GUI)
- Lets you choose where to save the result and what to name it (GUI). The real file extension is always appended automatically, so the extension never changes by accident
- The window stays responsive while an image is being processed, because the API call runs in a background thread (GUI)
- The **Start Processing** and **Select Image** buttons are disabled during processing, so you cannot start a second job or change the file halfway (GUI)
- The **Save As** dialog has a file type filter for JPG, PNG and WebP (GUI)
- Clear, separate error messages for an invalid API key, a connection problem and other errors (GUI)
- Ready-to-use Windows `.exe` of the GUI, no Python installation needed

## Example Output

### GUI

You choose the folder and the file name in the **Save As** dialog. The real extension of the result is added to the end of whatever you type, unless the name already ends with it.

| Result type | You type | Saved as |
|:-----------:|:--------:|:--------:|
| PNG | `photo` | `photo.png` |
| PNG | `photo.png` | `photo.png` |
| PNG | `photo.jpg` | `photo.jpg.png` |
| JPG | `photo` | `photo.jpg` |

In **Optimized compress**, the extension is taken from the format Tinify actually returns (WebP, PNG or JPEG).

### Terminal

The terminal version uses `optimized_`, `most_optimized_` and `resized_` as prefixes.

## Project Structure

```
.
├── TinifyImageGUI.py    # Tkinter desktop app (JPG, JPEG, PNG, WebP)
├── TinifyTerminal.py    # Command-line version (JPG only)
├── favicon.ico          # Window icon (bundled into the .exe)
└── .gitignore           # Keeps build files (build, dist, .spec) out of the repository
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
5. In the **Save As** window, choose the folder and type a file name. The real extension is added automatically
6. Wait for the **Completed** message. The window stays usable, and the buttons are enabled again when the process finishes

### Windows Executable

If you don't have Python installed, download `TinifyImageGUI.exe` from the [latest release](https://github.com/dircapwonder/Tinify-Image-Compressor/releases/latest) and double-click it. It works exactly like the GUI version above.

The `.exe` is only distributed through the Releases page and is not stored in the repository itself.

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
python -m PyInstaller TinifyImageGUI.py --onefile --noconsole --icon=favicon.ico --add-data "favicon.ico;." --collect-data tinify
```

- `--icon` sets the icon of the `.exe` file itself
- `--add-data` bundles `favicon.ico` into the executable, so the window icon also works when the `.exe` is moved to another folder or computer
- `--collect-data tinify` bundles the certificate file (`cacert.pem`) that the `tinify` library needs for HTTPS. Without it the `.exe` cannot connect to the API, even though the script works fine in Python
- On Linux/macOS use `:` instead of `;` in `--add-data`

The finished `.exe` is created in the `dist` folder. The build also creates a `build` folder and a `TinifyImageGUI.spec` file. These are temporary build files, so `build/`, `dist/` and `*.spec` are listed in `.gitignore` and are not part of the repository. The finished `.exe` is uploaded to the Releases page instead.

## How It Works

- **Threading:** everything that talks to the user (input checks, error dialogs, the **Save As** window) runs on the main thread. Only the slow network work (API key validation, upload, compression, saving) runs in a background thread. When it finishes, the result is handed back to the main thread with `after()`, because Tkinter is not thread-safe.
- **API key check:** the worker thread calls `tinify.validate()` first, so a wrong key fails fast with a clear message. An invalid key and a connection problem show different error messages.
- **Compression:** the image is uploaded with `tinify.from_file()` and the result is saved with `to_file()`.
- **Optimized compress:** `convert()` is given a list of types (`image/webp`, `image/png`, `image/jpeg`) and Tinify returns the smallest one. The real extension of that result is then appended to the name you typed.
- **Resize:** uses the `fit` method, which scales the image to fit inside the given width and height without cropping or stretching.
- **Save name:** the extension of the original file (or the real output type in optimized mode) is appended to your file name, unless the name already ends with it.
- **Quota:** the remaining limit is calculated from `tinify.compression_count`. (It's based on a free plan, which is 500)

## Limitations

- **Terminal version is JPG only:** the `.jpg` extension is hardcoded, and there is no error handling for missing files or API errors.
- **Free plan assumed:** the remaining quota in the GUI is calculated from a fixed limit of 500.
- **Windows only:** the `.exe` is built for Windows. On Linux and macOS, run the `.py` files directly.
- **No progress indicator:** the window stays responsive during processing, but there is no progress bar. You only see the result message when it finishes.
- **Overwrite warning:** the Save As dialog checks the name you typed, but the real extension is added afterwards, so an existing file with the final name may be overwritten without a warning.

## Ideas for Improvement

- Support PNG and WebP in the terminal version
- ~~Run the API call in a separate thread so the GUI stays responsive~~
- Add a progress indicator while processing
- Process multiple images or a whole folder at once
- ~~Let the user choose the output folder and file name~~
- Show the original and compressed file sizes after processing
- Add a "Scale by percentage" option for resizing

## Credits

- Image compression by [TinyPNG / Tinify](https://tinypng.com/)

## Disclaimer

This project is for personal and educational use. It is not affiliated with TinyPNG or Tinify.
