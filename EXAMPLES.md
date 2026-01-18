# Complete Usage Examples

This document shows complete end-to-end examples of using the blob tracking suite.

## Example 1: Quick Test (No Video Required)

Perfect for testing the system without any video files.

```bash
# 1. Create test video
python create_test_video.py

# 2. Process it
python blob_tracker.py test_input.mp4 test_output.mp4 --preview

# 3. View the result
# Open test_output.mp4 in your video player
```

**What you'll see:** Multiple bright blobs moving in different patterns with trails and connection lines.

---

## Example 2: Download and Process YouTube Video

Download a video from YouTube and add effects.

```bash
# 1. Download video (requires yt-dlp: pip install yt-dlp)
python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -o youtube_video.mp4

# 2. Check video properties
python video_info.py youtube_video.mp4

# 3. Process with effects
python blob_tracker.py youtube_video.mp4 output.mp4 --bright-only --trail-length 50 --preview

# 4. Done! Check output.mp4
```

**Best for:** LED performances, light shows, night traffic videos

---

## Example 3: Direct Video Link Download

Download from a direct video URL and process.

```bash
# 1. Download
python download_video.py "https://example.com/sample.mp4" -o sample.mp4

# 2. Process
python blob_tracker.py sample.mp4 output.mp4 --preview

# 3. If you like the settings, process without preview for speed
python blob_tracker.py sample.mp4 final_output.mp4 --bright-only --trail-length 40
```

---

## Example 4: Batch Processing Multiple Videos

Process several videos with the same settings.

```bash
# Method 1: Using a loop
for video in video1.mp4 video2.mp4 video3.mp4; do
    echo "Processing $video"
    python blob_tracker.py "$video" "tracked_$video" --bright-only --trail-length 40
done

# Method 2: Using the examples.py script (uncomment batch processing section)
python examples.py
```

---

## Example 5: Experimenting with Settings

Find the best settings for your video.

```bash
# 1. Start with preview to see what's detected
python blob_tracker.py input.mp4 test1.mp4 --preview --trail-length 20

# 2. Try longer trails
python blob_tracker.py input.mp4 test2.mp4 --preview --trail-length 60

# 3. Try only bright regions
python blob_tracker.py input.mp4 test3.mp4 --preview --bright-only --trail-length 40

# 4. Once you find settings you like, process without preview
python blob_tracker.py input.mp4 final.mp4 --bright-only --trail-length 40
```

---

## Example 6: Real-time Webcam (Using examples.py)

Use your webcam for real-time blob tracking.

```bash
# Edit examples.py and uncomment: example_real_time_webcam()
python examples.py
```

Press 'Q' to quit.

**Best for:** Testing with your own light sources (phone flashlight, LED, etc.)

---

## Example 7: Complete Workflow - Night Traffic

Full workflow for processing a night traffic video.

```bash
# 1. Download night traffic video
python download_video.py "https://www.youtube.com/watch?v=NIGHT_TRAFFIC_VIDEO" -o traffic.mp4

# 2. Check video info
python video_info.py traffic.mp4

# Output example:
# Resolution:    1920 x 1080
# FPS:           30.00
# Total Frames:  900
# Duration:      30.00 seconds

# 3. Test with preview (shorter trail for fast-moving objects)
python blob_tracker.py traffic.mp4 test.mp4 --preview --bright-only --trail-length 25

# 4. Looks good! Process full video
python blob_tracker.py traffic.mp4 tracked_traffic.mp4 --bright-only --trail-length 25

# 5. Done! Open tracked_traffic.mp4
```

**Expected result:** Car headlights and taillights with flowing trails and connections

---

## Example 8: Light Painting / Sparklers

Perfect for videos with light painting or sparklers.

```bash
# 1. Get video
python download_video.py "LIGHT_PAINTING_URL" -o light_painting.mp4

# 2. Process with longer trails for dramatic effect
python blob_tracker.py light_painting.mp4 output.mp4 --bright-only --trail-length 60 --preview

# 3. Final render
python blob_tracker.py light_painting.mp4 final.mp4 --bright-only --trail-length 60
```

**Expected result:** Beautiful long trails following the light sources

---

## Example 9: Fireworks

Process fireworks video.

```bash
# 1. Download fireworks video
python download_video.py "FIREWORKS_URL" -o fireworks.mp4

# 2. Process (detect both bright and dark for best results)
python blob_tracker.py fireworks.mp4 output.mp4 --trail-length 35 --preview

# 3. Final
python blob_tracker.py fireworks.mp4 tracked_fireworks.mp4 --trail-length 35
```

---

## Example 10: Low Quality Test (Faster Download & Processing)

Quick test with low quality video for speed.

```bash
# 1. Download worst quality (smallest file)
python download_video.py "VIDEO_URL" -q worst -o test.mp4

# 2. Quick process
python blob_tracker.py test.mp4 output.mp4 --bright-only --preview

# 3. If it works well, download better quality
python download_video.py "VIDEO_URL" -q best -o high_quality.mp4
python blob_tracker.py high_quality.mp4 final_output.mp4 --bright-only --trail-length 40
```

---

## Example 11: Check Available Formats Before Downloading

See what quality options are available.

```bash
# 1. List available formats
python download_video.py "VIDEO_URL" --list-formats

# Output example:
# ID   EXT   RESOLUTION  FPS  FILESIZE
# 22   mp4   1280x720    30   50.5MiB
# 18   mp4   640x360     30   25.3MiB
# ...

# 2. Download specific format
python download_video.py "VIDEO_URL" -q 22 -o video.mp4

# 3. Process
python blob_tracker.py video.mp4 output.mp4 --preview
```

---

## Example 12: Programmatic Use (Advanced)

Use the BlobTracker class in your own Python scripts.

```python
# my_script.py
from blob_tracker import BlobTracker
import cv2

# Create tracker
tracker = BlobTracker(trail_length=40, min_blob_size=15)

# Open video
cap = cv2.VideoCapture('input.mp4')
out = cv2.VideoWriter('output.mp4', 
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       30, (1280, 720))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame
    processed = tracker.process_frame(frame, detect_bright=True)
    out.write(processed)

cap.release()
out.release()
```

---

## Tips for Best Results

### Video Selection
- **High contrast scenes** work best
- **Dark backgrounds** make bright objects pop
- **2-5 moving objects** create the best connection effects
- **Consistent lighting** helps with detection

### Settings to Try

**Fast moving objects (traffic, sports):**
```bash
--bright-only --trail-length 20
```

**Slow artistic motion (light painting):**
```bash
--bright-only --trail-length 60
```

**Multiple objects with connections:**
```bash
--bright-only --trail-length 35
```

**Testing/experimenting:**
```bash
--preview
```

### Processing Time

- 1080p 30fps video: ~1-2x real-time (30s video = 30-60s processing)
- 4K video: ~3-5x real-time
- With preview: adds ~10-20% overhead

### Recommended YouTube Search Terms

Try searching for these to find good test videos:

- "LED poi performance"
- "light painting time lapse"
- "night traffic 4k"
- "car lights highway night"
- "sparkler writing"
- "glow stick dance"
- "fireflies at night"
- "concert lights"
- "laser light show"

---

## Troubleshooting Examples

### No Blobs Detected

```bash
# Problem: No blobs showing up
# Solution: Try preview mode to see what's happening
python blob_tracker.py input.mp4 output.mp4 --preview

# If video is too bright/dark, the default threshold might not work
# You may need to edit blob_tracker.py lines 77 & 83 to adjust thresholds
```

### Download Fails

```bash
# Problem: yt-dlp not installed
# Solution: Install it
pip install yt-dlp

# Problem: Geographic restriction
# Solution: yt-dlp usually handles this, but may need VPN for some regions

# Problem: Platform not supported
# Solution: Try direct download method
python download_video.py "URL" -m curl -o video.mp4
```

### Too Many Blobs

```bash
# Problem: Everything is being detected as a blob
# Solution: The video might not be suitable, or needs different settings
# Try bright-only mode to reduce noise
python blob_tracker.py input.mp4 output.mp4 --bright-only --preview
```

---

## Complete Beginner Workflow

Never used the command line? Start here:

```bash
# 1. Open Terminal (Mac) or Command Prompt (Windows)

# 2. Navigate to the project folder
cd /Users/kushalsrinivas/apps/touch

# 3. Activate virtual environment
source venv/bin/activate

# 4. Run the simple test
python create_test_video.py
python blob_tracker.py test_input.mp4 test_output.mp4

# 5. Find and open test_output.mp4 in the folder
# Double-click to watch!

# 6. Try with your own video
python blob_tracker.py your_video.mp4 tracked.mp4 --preview
```

That's it! Enjoy creating cool effects! 🎨✨
