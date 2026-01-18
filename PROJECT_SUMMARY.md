# Blob Tracking Video Effects - Project Summary

## 🎯 What This Does

This Python project adds stunning visual effects to videos by tracking bright and dark blobs (regions). It creates:

- **Motion trails** that follow detected blobs with a beautiful fading effect
- **Dynamic connection lines** between multiple blobs (brighter when closer)
- **Glowing markers** around each detected blob

## 📁 Project Files

### Main Scripts

1. **`blob_tracker.py`** - The main script that processes videos
   - Takes input video and outputs processed video with effects
   - Command-line interface with lots of options
   - Highly customizable blob detection and visual effects

2. **`download_video.py`** - Download videos from URLs
   - Supports YouTube, Vimeo, Twitter, TikTok, and 1000+ sites (via yt-dlp)
   - Works with direct video links
   - Multiple download methods (auto-detection)

3. **`create_test_video.py`** - Creates a test video for quick demos
   - Generates a video with moving bright blobs
   - Perfect for testing the blob tracker

4. **`video_info.py`** - Utility to check video properties
   - Shows resolution, FPS, duration, etc.

### Documentation

- **`README.md`** - Full documentation with examples
- **`QUICKSTART.md`** - Quick start guide for immediate use
- **`DOWNLOAD_GUIDE.md`** - Comprehensive video download guide
- **`PROJECT_SUMMARY.md`** - Detailed technical overview (this file)
- **`requirements.txt`** - Python dependencies

## 🚀 How to Use

### 1. Install Dependencies (first time only)

```bash
# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Quick Test

```bash
# Create test video
python create_test_video.py

# Process it
python blob_tracker.py test_input.mp4 test_output.mp4 --preview
```

### 3. Use Your Own Video

```bash
python blob_tracker.py your_video.mp4 output_video.mp4
```

## 🎨 Key Features Explained

### Blob Detection
- Automatically finds bright/dark regions in each frame
- Configurable size filters to ignore tiny or huge blobs
- Can detect bright-only, dark-only, or both

### Motion Trails
- Tracks blob positions over time (default: 30 frames)
- Creates smooth fading trails
- Trail opacity decreases with age for a ghosting effect
- Thickness increases toward the newest position

### Connection Lines
- Draws lines between all detected blobs
- Line brightness based on distance (closer = brighter)
- Won't connect blobs that are too far apart
- Creates a dynamic web/network effect

### Visual Styling
- Bright blobs: Magenta color
- Dark blobs: Yellow color
- Glowing circles with inner core and outer ring
- Anti-aliased rendering for smooth edges

## ⚙️ Command-Line Options

```bash
# Basic usage
python blob_tracker.py input.mp4 output.mp4

# Show preview while processing
python blob_tracker.py input.mp4 output.mp4 --preview

# Only detect bright regions
python blob_tracker.py input.mp4 output.mp4 --bright-only

# Only detect dark regions
python blob_tracker.py input.mp4 output.mp4 --dark-only

# Adjust trail length (20-60 recommended)
python blob_tracker.py input.mp4 output.mp4 --trail-length 50

# Combine options
python blob_tracker.py input.mp4 output.mp4 --bright-only --trail-length 60 --preview
```

## 💡 Best Input Videos

Works best with:
- ✅ Bright moving objects (LEDs, lights, sparklers)
- ✅ Night scenes with car lights/traffic
- ✅ Light painting
- ✅ Fireworks
- ✅ High contrast scenes
- ✅ Videos with 2-5 moving objects

Less effective with:
- ❌ Evenly lit scenes
- ❌ Low contrast videos
- ❌ Static images (no motion)
- ❌ Too many objects (becomes messy)

## 🔧 Customization

The script can be easily modified to adjust:
- Blob size thresholds (lines 26-27 in `blob_tracker.py`)
- Detection sensitivity (lines 77, 83)
- Visual colors (lines 73, 79)
- Maximum connection distance (line 150)
- Trail styling (thickness, opacity)

## 📦 Dependencies

- **OpenCV (cv2)** - Video processing and blob detection
- **NumPy** - Array operations and math
- Python 3.7+

## 🎓 How It Works Technically

1. **Frame Processing**: Each video frame is processed individually
2. **Grayscale Conversion**: Converts to grayscale for blob detection
3. **Thresholding**: Applies threshold to isolate bright/dark regions
4. **Blob Detection**: Uses SimpleBlobDetector with area filtering
5. **Trail Management**: Maintains deque of recent positions per blob
6. **Rendering**: Draws trails, connections, and markers on the frame
7. **Video Output**: Writes processed frames to output video

## 🐛 Troubleshooting

**No blobs detected?**
- Use `--preview` to see what's being detected
- Video might not have enough contrast
- Try adjusting threshold values in the code

**Slow processing?**
- Normal for high-resolution videos
- Progress indicator shows frame-by-frame progress
- Preview mode adds some overhead

**Output file won't play?**
- Try VLC media player
- Check disk space
- Ensure output path is writable

## 🎉 Example Workflow

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Download a video (optional)
python download_video.py "https://www.youtube.com/watch?v=..." -o night_traffic.mp4

# 3. Check your video info
python video_info.py night_traffic.mp4

# 4. Process with preview to test settings
python blob_tracker.py night_traffic.mp4 output.mp4 --preview --trail-length 40

# 5. If you like it, let it finish processing
# (or re-run without preview for faster processing)
python blob_tracker.py night_traffic.mp4 final_output.mp4 --trail-length 40

# 6. Done! Check final_output.mp4
```

Enjoy creating cool visual effects! 🌟
