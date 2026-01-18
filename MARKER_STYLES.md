# Blob Marker Styles - Advanced Options

## New Marker Customization Features

You now have full control over how blob markers are displayed!

## 1. Square Marker Styles (`--marker-style`)

Control which squares are shown around each blob.

### Options:
- `both` - Inner and outer squares (default)
- `outer` - Only outer square
- `inner` - Only inner square

```bash
# Only outer squares
python blob_tracker.py input.mp4 output.mp4 --marker-style outer

# Only inner squares
python blob_tracker.py input.mp4 output.mp4 --marker-style inner

# Both squares (default)
python blob_tracker.py input.mp4 output.mp4 --marker-style both
```

## 2. Points Instead of Squares (`--use-points`)

Replace square markers with small circular points.

```bash
# Use points instead of squares
python blob_tracker.py input.mp4 output.mp4 --use-points

# Points with numbering
python blob_tracker.py input.mp4 output.mp4 --use-points --show-numbers
```

**What you get:**
- Small filled circle (3px)
- Outer ring (6px)
- Minimal, clean look

## 3. Invert Colors (`--invert`)

Change markers from white to black (negative effect).

```bash
# Black markers instead of white
python blob_tracker.py input.mp4 output.mp4 --invert

# Black points with numbers
python blob_tracker.py input.mp4 output.mp4 --use-points --invert --show-numbers
```

**Use cases:**
- White/bright backgrounds
- Different aesthetic
- Better visibility on light videos

## 4. Blob Numbering (`--show-numbers`)

Add numbered labels to each blob (1, 2, 3, etc.)

```bash
# Show blob numbers
python blob_tracker.py input.mp4 output.mp4 --show-numbers

# Numbers with outer squares only
python blob_tracker.py input.mp4 output.mp4 --marker-style outer --show-numbers

# Numbers with points
python blob_tracker.py input.mp4 output.mp4 --use-points --show-numbers
```

**Features:**
- Numbers appear above each blob
- Black background for readability (white markers)
- Numbered 1, 2, 3... based on detection order
- Works with `--max-blobs` to show only top N

## Complete Examples

### Minimal Points with Numbers
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --use-points \
  --show-numbers \
  --max-blobs 5 \
  --no-trails
```
**Result:** 5 numbered points with connections

### Outer Squares Only with Inverted Colors
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --marker-style outer \
  --invert \
  --no-trails \
  --max-blobs 3
```
**Result:** 3 black outer squares with black connections

### Inner Squares with Numbering
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --marker-style inner \
  --show-numbers \
  --max-blobs 10 \
  --max-distance 300
```
**Result:** Numbered inner squares with moderate connections

### Clean Numbered System
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --use-points \
  --show-numbers \
  --max-blobs 5 \
  --max-distance 200 \
  --no-trails \
  --no-connections
```
**Result:** Just 5 numbered points, nothing else

## Visual Comparison

| Style | Command | Appearance |
|-------|---------|------------|
| Default | (none) | Two white squares (inner + outer) |
| Outer only | `--marker-style outer` | One white outer square |
| Inner only | `--marker-style inner` | One white inner square |
| Points | `--use-points` | White dots with rings |
| Inverted | `--invert` | Black instead of white |
| Numbered | `--show-numbers` | Text labels (1,2,3...) |

## Combining Features

All these features work together!

### Example Combinations:

**Professional tracking:**
```bash
--marker-style outer --show-numbers --max-blobs 5 --no-trails
```

**Minimal aesthetic:**
```bash
--use-points --max-blobs 3 --max-distance 150 --no-trails
```

**High contrast (bright video):**
```bash
--invert --marker-style outer --show-numbers
```

**Research/analysis:**
```bash
--show-numbers --marker-style both --max-blobs 10
```

**Artistic minimal:**
```bash
--use-points --invert --no-connections --no-trails
```

## Tips

### When to use each style:

**`--marker-style outer`**
- Less cluttered
- Cleaner look
- Better for many blobs

**`--marker-style inner`**
- More subtle
- Good for large blobs
- Minimal visual impact

**`--use-points`**
- Most minimal
- Best for many blobs
- Clean, modern look

**`--invert`**
- Bright backgrounds
- Light-colored videos
- Different aesthetic

**`--show-numbers`**
- Tracking specific blobs
- Analysis/research
- Debugging detection
- Better understanding of blob order

## Quick Reference

```bash
# All marker customization options
python blob_tracker.py INPUT OUTPUT \
  --marker-style {both,outer,inner}  # Square style
  --use-points                       # Points instead of squares
  --invert                          # Black instead of white
  --show-numbers                    # Show blob numbers
  --max-blobs N                     # Limit to N blobs
  --max-distance PIXELS             # Connection distance
  --no-trails                       # Hide trails
  --no-connections                  # Hide connections
  --no-boxes                        # Hide markers entirely
```

## Recommended Presets

### Clean Tracking
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --use-points --show-numbers --max-blobs 5 --max-distance 200 --no-trails
```

### Minimal Aesthetic
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --marker-style outer --max-blobs 3 --max-distance 150 --no-trails
```

### Analysis/Research
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --show-numbers --marker-style both --max-blobs 10 --max-distance 300
```

### Bright Video
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --invert --use-points --show-numbers --max-blobs 5
```

Try them with `--preview` first to see which style you prefer! 🎨
