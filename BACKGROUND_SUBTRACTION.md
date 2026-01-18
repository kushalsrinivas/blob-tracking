# Background Subtraction Feature

## Overview

Background subtraction has been added to `blob_tracker.py` as an alternative detection method. Instead of detecting only bright or dark spots, it detects **anything that differs from the background** by building a model of the static background and tracking changes.

## How It Works

1. **Background Model**: Collects the first N frames (default 30) and computes a median to create a background model
2. **Difference Detection**: Each new frame is compared against this background
3. **Mask Creation**: Pixels that differ by more than the threshold are marked
4. **Blob Detection**: Blobs are detected from the difference mask

## Usage

### Basic Usage

```bash
# Use background subtraction instead of bright/dark detection
python blob_tracker.py input.mp4 output.mp4 --background-subtraction
```

### Adjust Sensitivity

```bash
# Lower threshold = more sensitive (detects smaller movements)
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --threshold 0.1

# Higher threshold = less sensitive (only detects larger movements)
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --threshold 0.3
```

### Adjust Background Model

```bash
# Use more frames for background (slower adaptation, more stable)
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --bg-frames 60

# Use fewer frames (faster adaptation, less stable)
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --bg-frames 15
```

### Combined Examples

```bash
# Background subtraction with trails only
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --no-boxes --no-connections

# Background subtraction with limited blobs
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --max-blobs 5

# Background subtraction with preview
python blob_tracker.py input.mp4 output.mp4 --background-subtraction --preview
```

## Parameters

### `--background-subtraction`
- **Type**: Flag
- **Description**: Enable background subtraction mode
- **Note**: When enabled, `--bright-only` and `--dark-only` are ignored

### `--threshold`
- **Type**: Float (0.0 - 1.0)
- **Default**: 0.15
- **Description**: Difference threshold for detection
- **Lower values**: More sensitive, detects smaller changes
- **Higher values**: Less sensitive, only detects larger changes
- **Only applies when**: `--background-subtraction` is enabled

### `--bg-frames`
- **Type**: Integer
- **Default**: 30
- **Description**: Number of frames to use for building the background model
- **More frames**: More stable background, slower adaptation
- **Fewer frames**: Faster adaptation, less stable
- **Only applies when**: `--background-subtraction` is enabled

## When to Use Background Subtraction

**Use background subtraction when:**
- You want to track movement or changes in the scene
- The camera is stationary (or mostly stationary)
- You want to detect objects regardless of their brightness
- You're tracking hands, objects, or people moving in front of a static background

**Use bright/dark detection when:**
- You specifically want to track bright lights or dark objects
- The camera is moving
- The background is constantly changing
- You want to track specific features based on intensity

## Comparison

| Feature | Bright/Dark Detection | Background Subtraction |
|---------|----------------------|------------------------|
| **Detects** | Bright/dark regions | Any movement/change |
| **Camera** | Can be moving | Should be stationary |
| **Background** | Any | Should be mostly static |
| **Setup** | None | Builds model from first frames |
| **Sensitivity** | Fixed threshold (200/255) | Adjustable (0.0-1.0) |

## Tips for Best Results

1. **Keep camera still** during the first second while background model is built
2. **Start with default threshold** (0.15) and adjust if needed
3. **Lower threshold** if not detecting enough movement
4. **Higher threshold** if detecting too much noise
5. **More bg-frames** (60+) for very stable backgrounds
6. **Fewer bg-frames** (15-20) for slightly changing backgrounds

## Implementation Details

The implementation uses:
- **Median background model**: Robust to temporary changes
- **Morphological operations**: Cleans up noise in the mask
- **Frame buffer**: Stores recent frames for background computation
- **Normalized difference**: Compares frames in 0.0-1.0 range

## Code Example

```python
from blob_tracker import BlobTracker

# Create tracker with background subtraction
tracker = BlobTracker(
    use_background_subtraction=True,
    diff_threshold=0.15,
    background_frames=30
)

# Process frames
for frame in video_frames:
    processed = tracker.process_frame(frame)
```
