# Blob Tracking Video Effects

A cool Python script that adds awesome visual effects to videos using blob tracking!

## Features

- 🎯 **Blob Detection**: Tracks bright and/or dark regions in your video
- 🌈 **Motion Trails**: Creates flowing trails that follow detected blobs
- 🔗 **Connection Lines**: Draws dynamic lines connecting multiple blobs
- 🎨 **Visual Effects**: Glowing circles, fading trails, and distance-based connections

## Installation

1. Make sure you have Python 3.7+ installed

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install opencv-python numpy
```

## Usage

### Getting a Video

**Option 1: Use your own video file**

**Option 2: Download from a URL**
```bash
# Download from YouTube, Vimeo, or other platforms (requires yt-dlp)
python download_video.py "VIDEO_URL" -o my_video.mp4

# Download direct video link
python download_video.py "https://example.com/video.mp4" -o video.mp4
```

See [DOWNLOAD_GUIDE.md](DOWNLOAD_GUIDE.md) for detailed download instructions.

### Basic Usage

Process a video with default settings (tracks both bright and dark regions):

```bash
python blob_tracker.py input.mp4 output.mp4
```

### Advanced Options

**Only track bright regions:**
```bash
python blob_tracker.py input.mp4 output.mp4 --bright-only
```

**Only track dark regions:**
```bash
python blob_tracker.py input.mp4 output.mp4 --dark-only
```

**Adjust trail length (longer trails = more dramatic effect):**
```bash
python blob_tracker.py input.mp4 output.mp4 --trail-length 50
```

**Show preview while processing:**
```bash
python blob_tracker.py input.mp4 output.mp4 --preview
```

**Combine options:**
```bash
python blob_tracker.py input.mp4 output.mp4 --bright-only --trail-length 60 --preview
```

## How It Works

1. **Blob Detection**: Uses OpenCV's SimpleBlobDetector to find bright/dark regions
2. **Trail Tracking**: Maintains a history of blob positions to create motion trails
3. **Visual Effects**:
   - Motion trails with fading intensity (white, fades to darker)
   - Connecting lines between blobs (white, brighter when closer)
   - Square markers around each blob
   - Clean minimalist white aesthetic

## Tips for Best Results

- **Bright blobs work best**: Videos with bright moving objects (lights, reflections, etc.)
- **High contrast**: Videos with good contrast between foreground and background
- **Moving objects**: The trail effect looks cooler with motion
- **Multiple objects**: Connection lines shine when tracking 2-5 blobs
- **Experiment with trail length**: Try values between 20-60 for different looks

## Examples

Great video types to try:
- Light painting or sparklers
- Night traffic (car lights)
- Fireworks
- Sports with bright balls/equipment
- Dancing with LED props
- Screen recordings with cursor movement

## Customization

You can modify the script to adjust:
- Blob size thresholds (`min_blob_size`, `max_blob_size`)
- Detection sensitivity (threshold values)
- Colors and visual styles
- Maximum connection distance
- Trail opacity and thickness

## Troubleshooting

**No blobs detected?**
- Try adjusting the brightness threshold in the code (line with `cv2.threshold`)
- Use `--preview` to see what's being detected
- Make sure your video has sufficient contrast

**Output file won't play?**
- Try a different video player (VLC works well)
- Check that the output path is writable
- Ensure enough disk space is available

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy

## License

Free to use and modify for any purpose!
# blob-tracking
