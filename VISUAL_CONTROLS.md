# Blob Tracker - Visual Controls Guide

## Command-Line Options

You can now control exactly what visual elements are shown and how many!

### Control Visual Elements

```bash
--no-trails        # Disable motion trails
--no-connections   # Disable connection lines between blobs
--no-boxes         # Disable blob boxes/markers
```

### Control Quantity & Distance

```bash
--max-blobs N            # Limit to N largest blobs (default: unlimited)
--max-distance PIXELS    # Max distance for connection lines (default: 500)
```

## Usage Examples

### Limit Number of Blobs

```bash
# Track only the 5 largest blobs
python blob_tracker.py input.mp4 output.mp4 --max-blobs 5

# Track only 3 blobs with connections
python blob_tracker.py input.mp4 output.mp4 --max-blobs 3 --no-trails

# Track 10 blobs, no boxes
python blob_tracker.py input.mp4 output.mp4 --max-blobs 10 --no-boxes
```

### Control Connection Distance

```bash
# Only connect very close blobs (within 100px)
python blob_tracker.py input.mp4 output.mp4 --max-distance 100

# Connect blobs within 300px
python blob_tracker.py input.mp4 output.mp4 --max-distance 300

# Only nearby blobs with limited number
python blob_tracker.py input.mp4 output.mp4 --max-blobs 5 --max-distance 200
```

## Combined Examples

```bash
# Clean look: 3 blobs max, close connections only, no trails
python blob_tracker.py input.mp4 output.mp4 --max-blobs 3 --max-distance 150 --no-trails

# Only 2 blobs with close connections and boxes
python blob_tracker.py input.mp4 output.mp4 --max-blobs 2 --max-distance 200 --no-trails

# Preview with limited blobs
python blob_tracker.py input.mp4 output.mp4 --preview --max-blobs 5 --max-distance 250
```

### Show Only Visual Elements
```bash
python blob_tracker.py input.mp4 output.mp4 --no-trails --no-boxes
```
Result: Only white lines connecting blobs (no trails, no squares)

### Show Only Boxes
```bash
python blob_tracker.py input.mp4 output.mp4 --no-trails --no-connections
```
Result: Only white square boxes around blobs (no trails, no connections)

### Show Only Trails
```bash
python blob_tracker.py input.mp4 output.mp4 --no-connections --no-boxes
```
Result: Only motion trails (no connections, no squares)

### Show Boxes + Connections (No Trails)
```bash
python blob_tracker.py input.mp4 output.mp4 --no-trails
```
Result: Square boxes with connection lines between them

### Show Everything (Default)
```bash
python blob_tracker.py input.mp4 output.mp4
```
Result: Trails + connections + boxes

## Combined with Other Options

```bash
# Only bright regions, only show connections
python blob_tracker.py input.mp4 output.mp4 --bright-only --no-trails --no-boxes

# Preview mode, only boxes and connections
python blob_tracker.py input.mp4 output.mp4 --preview --no-trails

# Longer trails, no connections
python blob_tracker.py input.mp4 output.mp4 --trail-length 60 --no-connections
```

## Understanding Connection Lines

Connection lines now ONLY connect the detected blob squares (the current frame positions).

- Lines appear between blobs that are within 500 pixels of each other
- All lines are 1px thick, solid white
- No lines appear in the trails (only between current blob positions)

## Quick Reference

| Want to see...                | Command |
|-------------------------------|---------|
| Only connections              | `--no-trails --no-boxes` |
| Only boxes                    | `--no-trails --no-connections` |
| Only trails                   | `--no-connections --no-boxes` |
| Boxes + connections           | `--no-trails` |
| Trails + boxes                | `--no-connections` |
| Trails + connections          | `--no-boxes` |
| Everything (default)          | (no flags needed) |

| Want to limit...              | Command |
|-------------------------------|---------|
| Max 5 blobs                   | `--max-blobs 5` |
| Only close connections        | `--max-distance 200` |
| 3 blobs, close connections    | `--max-blobs 3 --max-distance 150` |

## How It Works

### Max Blobs (`--max-blobs`)
- When you have too many detected blobs, this limits it to the N **largest** blobs
- Larger blobs are prioritized (more visible/important)
- Default: unlimited (all blobs shown)
- **Recommended values**: 2-10 for clean results

### Max Distance (`--max-distance`)
- Connection lines only drawn between blobs within this distance
- Measured in pixels
- Default: 500px
- **Recommended values**: 
  - 100-200px: Very close connections only
  - 200-300px: Moderate connections
  - 300-500px: Wider connections

## Visual Style Summary

All elements are:
- ✅ White color (255, 255, 255)
- ✅ 1px thick lines
- ✅ No fading or transparency
- ✅ Clean, minimal aesthetic

Connection lines:
- ✅ Only between detected blobs (current frame)
- ✅ Not in the motion trails
- ✅ Max distance: 500px
