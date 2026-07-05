# 🖼️ Auto-Wallpaper Changer for Windows

Automatically change your Windows desktop wallpaper every 5 minutes with beautiful images from Unsplash or Bing.

## Features

✨ **Automatic Wallpaper Changes** - Changes wallpaper every 5 minutes (configurable)
🎨 **Multiple Image Sources** - Unsplash or Bing wallpapers
⚙️ **Highly Configurable** - JSON config file for easy customization
💾 **Local Storage** - Keeps wallpapers locally for offline use
🧹 **Auto Cleanup** - Automatically removes old wallpapers to save disk space
🔧 **Simple to Use** - Just run and forget

## Requirements

- Windows OS
- Python 3.7+
- Internet connection (for fetching images)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shashank536/auto-wallpaper.git
cd auto-wallpaper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Unsplash API Key (Optional)

If you want to use Unsplash as your image source:

1. Go to https://unsplash.com/api/
2. Click "Register as a developer"
3. Create an application
4. Copy your **Access Key**
5. Update `config.json` with your API key

## Configuration

Edit `config.json` to customize the application:

```json
{
  "interval_minutes": 5,
  "image_source": "unsplash",
  "unsplash_api_key": "your_api_key_here",
  "wallpaper_directory": "./wallpapers",
  "image_query": "nature",
  "image_size": "1920x1080",
  "keep_wallpapers": true,
  "max_wallpapers_to_keep": 50
}
```

### Configuration Options

- **interval_minutes** - How often to change wallpaper (in minutes)
- **image_source** - Image source: `"unsplash"` or `"bing"`
- **unsplash_api_key** - Your Unsplash API key (required for Unsplash)
- **wallpaper_directory** - Where to save wallpapers
- **image_query** - Search query for Unsplash (e.g., "nature", "space", "city")
- **image_size** - Desired image size (width x height)
- **keep_wallpapers** - Keep downloaded wallpapers for offline use
- **max_wallpapers_to_keep** - Maximum wallpapers to store locally

## Usage

### Run the Application

```bash
python main.py
```

The wallpaper will change immediately, then every 5 minutes.

### Stop the Application

Press `Ctrl+C` to stop the application.

## Quick Start

1. **Using Bing (No API Key Required):**
   - Change `"image_source"` to `"bing"` in `config.json`
   - Run `python main.py`

2. **Using Unsplash (Recommended):**
   - Get API key from https://unsplash.com/api/
   - Update `config.json` with your API key
   - Run `python main.py`

## Example Searches for Unsplash

Try these in the `image_query` field:
- `nature` - Beautiful nature scenes
- `space` - Space and astronomy
- `city` - Urban landscapes
- `abstract` - Abstract art
- `mountains` - Mountain scenery
- `ocean` - Beach and ocean
- `sunset` - Sunset scenes
- `forest` - Forest photography

## Running as a Background Service

### Option 1: Create a Startup Shortcut

1. Press `Win + R`, type `shell:startup` and press Enter
2. Right-click in the folder → New → Shortcut
3. Paste: `C:\path\to\python.exe C:\path\to\main.py`
4. Name it "Auto Wallpaper Changer"

### Option 2: Use Task Scheduler

1. Open Task Scheduler
2. Right-click "Task Scheduler Library" → Create Basic Task
3. Name: "Auto Wallpaper Changer"
4. Trigger: At startup (or your preference)
5. Action: Start a program → `C:\path\to\python.exe C:\path\to\main.py`
6. Check "Run with highest privileges"

## Troubleshooting

### "API key not configured" Error
- Make sure you've set `unsplash_api_key` in `config.json`
- Get a key from https://unsplash.com/api/

### Wallpaper not changing
- Check that the image file exists in the wallpaper directory
- Try running as Administrator
- Verify the image format (JPG, PNG, BMP supported)

### Network errors
- Check your internet connection
- Verify the API is responding (check Unsplash/Bing website)
- Try switching to a different image source

### Disk space issues
- Set `keep_wallpapers` to `false` to delete old wallpapers immediately
- Reduce `max_wallpapers_to_keep` value

## Project Structure

```
auto-wallpaper/
├── main.py                 # Main application file
├── wallpaper_manager.py    # Windows wallpaper control
├── image_fetcher.py        # Image fetching from APIs
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)

## System Requirements

- Windows 7 or newer
- Minimum 100 MB disk space
- Internet connection for fetching images

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements!

## Issues & Suggestions

If you encounter any issues or have suggestions, please open an issue on GitHub.

## Author

Created by [shashank536](https://github.com/shashank536)

---

Enjoy your beautiful rotating wallpapers! 🎨
