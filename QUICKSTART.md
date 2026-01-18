# Quick Start Guide

## Setup (One-time)

1. **Activate your virtual environment:**
```bash
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Quick Test

Want to see it in action right away? Create a test video:

```bash
# Create a test video with moving bright blobs
python create_test_video.py

# Process it with blob tracking effects
python blob_tracker.py test_input.mp4 test_output.mp4 --preview
```

Press 'Q' to stop the preview early, or let it finish processing.

## Use With Your Own Video

### Option 1: Use a video file you already have

```bash
python blob_tracker.py your_video.mp4 output.mp4
```

## Common Options

```bash
# Show preview while processing (press Q to quit early)
python blob_tracker.py input.mp4 output.mp4 --preview

# Only track bright regions
python blob_tracker.py input.mp4 output.mp4 --bright-only

# Longer motion trails (more dramatic effect)
python blob_tracker.py input.mp4 output.mp4 --trail-length 60

# All together
python blob_tracker.py input.mp4 output.mp4 --bright-only --trail-length 50 --preview
```

## What Makes Good Input Videos?

✅ **Great:**
- Videos with bright moving objects (lights, LEDs, sparklers)
- Night scenes with car lights
- Light painting
- Fireworks
- High contrast scenes

❌ **Not ideal:**
- Evenly lit scenes
- Low contrast
- Static images (no motion = no trails!)

## Tips

- Start with `--preview` to see what's being detected
- Adjust `--trail-length` (try 20-60) for different looks
- Bright blobs usually work better than dark ones
- 2-5 blobs create the coolest connection effects

Enjoy! 🎨✨
