# Video Downloader Guide

A flexible script to download videos from various sources for use with the blob tracker.

## Features

- 🎬 **Multiple Platforms**: YouTube, Vimeo, Twitter, Instagram, TikTok, and more (via yt-dlp)
- 🔗 **Direct Links**: Download from direct video URLs
- 🔄 **Auto-Detection**: Automatically chooses the best download method
- ⚙️ **Multiple Methods**: yt-dlp, curl, wget, or Python requests
- 📊 **Quality Options**: Choose video quality when using yt-dlp

## Installation

### Basic (for direct video links)

Already included! Uses curl (or wget/Python as fallback).

### Full (for YouTube, Vimeo, etc.)

Install yt-dlp for platform support:

```bash
# Using pip
pip install yt-dlp requests

# Or using homebrew (macOS)
brew install yt-dlp
```

Then install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Download video (auto-detects best method)
python download_video.py "https://example.com/video.mp4" -o my_video.mp4

# Then process with blob tracker
python blob_tracker.py my_video.mp4 output.mp4 --preview
```

### YouTube Videos

```bash
# Download best quality
python download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o youtube_video.mp4

# Download worst quality (smaller file, faster download)
python download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q worst -o youtube_video.mp4

# List available formats first
python download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --list-formats

# Download specific format
python download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 22 -o youtube_video.mp4
```

### Other Platforms

```bash
# Vimeo
python download_video.py "https://vimeo.com/123456789" -o vimeo_video.mp4

# Twitter/X
python download_video.py "https://twitter.com/user/status/..." -o twitter_video.mp4

# TikTok
python download_video.py "https://www.tiktok.com/@user/video/..." -o tiktok_video.mp4

# Instagram
python download_video.py "https://www.instagram.com/p/..." -o instagram_video.mp4
```

### Direct Video Links

```bash
# MP4 file
python download_video.py "https://example.com/video.mp4" -o downloaded.mp4

# Auto-generates filename from URL if not specified
python download_video.py "https://example.com/sample.mp4"
```

### Force Specific Method

```bash
# Force curl
python download_video.py "https://example.com/video.mp4" -m curl -o video.mp4

# Force wget
python download_video.py "https://example.com/video.mp4" -m wget -o video.mp4

# Force Python requests (fallback)
python download_video.py "https://example.com/video.mp4" -m python -o video.mp4
```

## Supported Platforms (with yt-dlp)

- **Video Platforms**: YouTube, Vimeo, Dailymotion
- **Social Media**: Twitter/X, Facebook, Instagram, TikTok
- **Streaming**: Twitch, Reddit videos
- **And 1000+ more sites!**

See [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for the full list.

## Download Methods

### 1. yt-dlp (Best for platforms)

**Pros:**
- Supports 1000+ video platforms
- Handles authentication and geo-restrictions
- Quality selection
- Format conversion

**Cons:**
- Requires separate installation
- Slightly slower for direct links

### 2. curl (Best for direct links)

**Pros:**
- Fast and efficient
- Pre-installed on most systems
- Good for direct video URLs

**Cons:**
- Only works with direct video links

### 3. wget (Alternative to curl)

**Pros:**
- Similar to curl
- Pre-installed on many Linux systems

**Cons:**
- May need installation on macOS/Windows

### 4. Python requests (Fallback)

**Pros:**
- Works anywhere Python works
- No external dependencies (if requests is installed)

**Cons:**
- Slower than curl/wget
- Basic progress indication

## Complete Workflow Example

```bash
# 1. Download a video
python download_video.py "https://www.youtube.com/watch?v=..." -o night_traffic.mp4

# 2. Check video info
python video_info.py night_traffic.mp4

# 3. Process with blob tracker
python blob_tracker.py night_traffic.mp4 tracked_output.mp4 --bright-only --preview

# 4. Done! Watch tracked_output.mp4
```

## Tips for Good Results

### Best Video Types to Download:

1. **Light Shows**: Search YouTube for "led light show", "light painting"
2. **Night Traffic**: "night traffic timelapse", "car lights night"
3. **Fireworks**: "fireworks display", "sparklers"
4. **Sports**: "tennis ball tracking", "soccer highlights"
5. **Dance/Performance**: "LED poi", "light stick performance"

### Search Terms to Try:

- "LED poi performance"
- "light painting tutorial"
- "night traffic 4k"
- "sparkler writing"
- "glow stick dance"
- "firefly timelapse"
- "city lights night"

## Troubleshooting

### yt-dlp not found

```bash
# Install with pip
pip install yt-dlp

# Or with homebrew (macOS)
brew install yt-dlp
```

### curl not found

```bash
# macOS (should be pre-installed, but if not)
brew install curl

# Ubuntu/Debian
sudo apt install curl
```

### Download fails

1. **Check URL**: Make sure it's valid and accessible
2. **Try different method**: Use `-m` flag to specify method
3. **Check internet**: Ensure stable connection
4. **Platform restrictions**: Some platforms block downloads
5. **Use yt-dlp**: For platform videos, yt-dlp usually works best

### Video format not supported

```bash
# List available formats
python download_video.py "URL" --list-formats

# Download specific format (format code from list above)
python download_video.py "URL" -q FORMAT_CODE -o output.mp4
```

## Command-Line Options

```
positional arguments:
  url                   Video URL to download

optional arguments:
  -h, --help            Show help message
  -o, --output OUTPUT   Output file path (default: auto-generated)
  -m, --method METHOD   Download method: auto, yt-dlp, curl, wget, python
  -q, --quality QUALITY Video quality for yt-dlp (default: best)
  --list-formats        List available formats (yt-dlp only)
```

## Examples with Blob Tracker

### Example 1: YouTube Light Show

```bash
# Download
python download_video.py "https://www.youtube.com/watch?v=..." -o light_show.mp4

# Process
python blob_tracker.py light_show.mp4 output.mp4 --bright-only --trail-length 50 --preview
```

### Example 2: Direct Link Night Traffic

```bash
# Download
python download_video.py "https://example.com/traffic.mp4" -o traffic.mp4

# Process
python blob_tracker.py traffic.mp4 output.mp4 --bright-only --trail-length 40
```

### Example 3: Quick Test

```bash
# Download a short video
python download_video.py "VIDEO_URL" -q worst -o test.mp4

# Quick test with preview
python blob_tracker.py test.mp4 test_output.mp4 --preview
```

## Security Note

Always be cautious when downloading videos:
- Only download from trusted sources
- Respect copyright and terms of service
- Don't download private or restricted content
- Use downloaded videos responsibly

Enjoy downloading and tracking! 🎥✨
