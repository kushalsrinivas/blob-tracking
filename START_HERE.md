# 🎬 Blob Tracking Video Effects - Complete Package

## What You Have

A complete Python-based video processing suite that adds stunning visual effects to videos through blob tracking.

## 📦 All Files Created

### Scripts (Executable)
1. **`blob_tracker.py`** - Main video processor with blob tracking effects
2. **`download_video.py`** - Download videos from URLs (YouTube, Vimeo, etc.)
3. **`create_test_video.py`** - Generate test videos with moving blobs
4. **`video_info.py`** - Display video file information
5. **`examples.py`** - Code examples for programmatic usage
6. **`setup.sh`** - Automated installation script

### Documentation
- **`README.md`** - Main documentation
- **`QUICKSTART.md`** - Quick start guide
- **`DOWNLOAD_GUIDE.md`** - Complete video download guide
- **`PROJECT_SUMMARY.md`** - Technical overview
- **`EXAMPLES.md`** - 12+ complete usage examples
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Git ignore rules

## 🚀 Getting Started (3 Steps)

### Step 1: Install Dependencies

```bash
# Easy way - run setup script
./setup.sh

# Or manually
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Create Test Video

```bash
python create_test_video.py
```

### Step 3: Process It

```bash
python blob_tracker.py test_input.mp4 test_output.mp4 --preview
```

**Press 'Q' to quit preview or let it finish!**

## ⚡ Quick Commands

```bash
# Download a video
python download_video.py "VIDEO_URL" -o video.mp4

# Check video info
python video_info.py video.mp4

# Process with effects
python blob_tracker.py video.mp4 output.mp4 --preview

# Advanced processing
python blob_tracker.py video.mp4 output.mp4 --bright-only --trail-length 50
```

## 🎨 What The Effects Look Like

### Motion Trails
- Flowing trails follow each detected blob
- Trails fade out gradually (ghosting effect)
- Thickness increases toward the newest position
- Creates a sense of movement and flow

### Connection Lines
- Dynamic lines connect all detected blobs
- Line brightness based on distance (closer = brighter)
- Creates a network/web effect
- Won't connect blobs that are too far apart

### Blob Markers
- Square markers around each blob
- White color for all elements
- Inner filled square and outer border
- Clean, minimalist design

## 📊 Command Options Reference

### blob_tracker.py
```bash
python blob_tracker.py INPUT OUTPUT [OPTIONS]

Options:
  --preview          Show preview while processing (press Q to quit)
  --bright-only      Only detect bright regions
  --dark-only        Only detect dark regions
  --trail-length N   Length of trails in frames (default: 30)
```

### download_video.py
```bash
python download_video.py URL [OPTIONS]

Options:
  -o FILE           Output file path
  -m METHOD         Download method (auto, yt-dlp, curl, wget, python)
  -q QUALITY        Video quality (best, worst, or format code)
  --list-formats    Show available formats
```

### create_test_video.py
```bash
python create_test_video.py [OPTIONS]

Options:
  --output FILE     Output file (default: test_input.mp4)
  --duration N      Duration in seconds (default: 10)
  --fps N          Frames per second (default: 30)
```

### video_info.py
```bash
python video_info.py VIDEO_FILE
```

## 🎯 Best Video Types

### ✅ Works Great
- LED/light performances
- Night traffic (car lights)
- Light painting, sparklers
- Fireworks
- Sports with bright equipment
- Screen recordings
- Concert lights

### ❌ Not Ideal
- Evenly lit daytime scenes
- Low contrast videos
- Static images (no motion)
- Too many objects (gets messy)

## 📚 Documentation Guide

**New user?** Start here:
1. `QUICKSTART.md` - Get running in 5 minutes
2. `EXAMPLES.md` - See 12+ complete examples

**Want to download videos?**
- `DOWNLOAD_GUIDE.md` - Complete download guide

**Need technical details?**
- `PROJECT_SUMMARY.md` - Technical overview
- `README.md` - Full documentation

**Want to code?**
- `examples.py` - Programmatic usage examples

## 🔧 Installation Requirements

### Required
- Python 3.7+
- opencv-python
- numpy

### Optional (for downloading)
- yt-dlp (for YouTube, Vimeo, etc.)
- requests (for Python-based downloads)

### Pre-installed on Most Systems
- curl or wget (for direct video links)

## 💡 Pro Tips

1. **Always start with `--preview`** to see what's being detected
2. **Use `video_info.py`** before processing to check video properties
3. **Shorter trails (20-30)** for fast motion, **longer trails (50-60)** for slow artistic motion
4. **Bright-only mode** works better for most videos
5. **Download worst quality first** for quick testing, then upgrade to best quality

## 🎬 Complete Example Workflow

```bash
# 1. Setup (first time only)
source venv/bin/activate
pip install -r requirements.txt

# 2. Download a video
python download_video.py "https://www.youtube.com/watch?v=..." -o video.mp4

# 3. Check it
python video_info.py video.mp4

# 4. Test with preview
python blob_tracker.py video.mp4 test.mp4 --preview --bright-only --trail-length 40

# 5. Final render
python blob_tracker.py video.mp4 final.mp4 --bright-only --trail-length 40

# 6. Watch final.mp4!
```

## 🎓 Learning Path

### Beginner
1. Run `setup.sh`
2. Create test video: `python create_test_video.py`
3. Process it: `python blob_tracker.py test_input.mp4 output.mp4`
4. Watch output.mp4

### Intermediate
1. Download a real video
2. Experiment with different trail lengths
3. Try bright-only vs dark-only
4. Use preview mode to test settings

### Advanced
1. Edit `blob_tracker.py` to customize effects
2. Use `examples.py` for programmatic control
3. Batch process multiple videos
4. Integrate into your own projects

## 🆘 Help & Troubleshooting

### Common Issues

**"yt-dlp not found"**
```bash
pip install yt-dlp
```

**"No blobs detected"**
```bash
# Use preview to see what's happening
python blob_tracker.py video.mp4 output.mp4 --preview
```

**"Video won't play"**
- Try VLC media player
- Check disk space
- Verify output path is writable

**"Download fails"**
- Check internet connection
- Verify URL is correct
- Try different download method: `-m curl`

### Get More Help

- Check `EXAMPLES.md` for 12+ complete examples
- Read `DOWNLOAD_GUIDE.md` for download issues
- See `README.md` for full documentation

## 🌟 Cool Things to Try

### YouTube Search Terms
- "LED poi performance"
- "light painting tutorial"
- "night traffic 4k"
- "sparkler writing"
- "fireworks display"
- "concert laser show"

### Experiment with Settings
```bash
# Super long trails (artistic)
--trail-length 80

# Short trails (fast action)
--trail-length 15

# Both bright and dark (complex scenes)
# (omit --bright-only and --dark-only)
```

## 📁 Project Structure

```
touch/
├── blob_tracker.py          # Main processor
├── download_video.py        # Video downloader
├── create_test_video.py     # Test video generator
├── video_info.py           # Video info utility
├── examples.py             # Code examples
├── setup.sh                # Setup script
├── requirements.txt        # Dependencies
├── README.md              # Main docs
├── QUICKSTART.md          # Quick start
├── DOWNLOAD_GUIDE.md      # Download guide
├── PROJECT_SUMMARY.md     # Technical overview
├── EXAMPLES.md            # Usage examples
└── venv/                  # Virtual environment
```

## 🎉 You're All Set!

Everything is ready to use. Pick a starting point:

- **Total beginner?** → Run `./setup.sh` then see `QUICKSTART.md`
- **Want examples?** → Check out `EXAMPLES.md`
- **Need to download?** → See `DOWNLOAD_GUIDE.md`
- **Want details?** → Read `README.md` and `PROJECT_SUMMARY.md`

Have fun creating amazing visual effects! 🎨✨🎬
