# Blob Tracker - Control Parameters Quick Guide

## 🎯 New Parameters Added

### 1. `--max-blobs N`
**Controls**: Maximum number of blobs to track
**Default**: Unlimited
**How it works**: Keeps only the N largest blobs
**Recommended**: 2-10 for clean results

```bash
# Track only 5 largest blobs
python blob_tracker.py input.mp4 output.mp4 --max-blobs 5
```

### 2. `--max-distance PIXELS`
**Controls**: Maximum distance for connection lines
**Default**: 500 pixels
**How it works**: Lines only drawn between blobs within this distance
**Recommended**: 
- 100-200px: Very close only
- 200-300px: Moderate
- 300-500px: Wider connections

```bash
# Only connect blobs within 200px
python blob_tracker.py input.mp4 output.mp4 --max-distance 200
```

## 🚀 Practical Examples

### Reduce Clutter - Clean Minimal Look
```bash
# 3 blobs max, close connections only, no trails
python blob_tracker.py input.mp4 output.mp4 --max-blobs 3 --max-distance 150 --no-trails --preview
```
**Result**: Clean, minimal with just a few connected boxes

### Medium Density
```bash
# 5-8 blobs with moderate connections
python blob_tracker.py input.mp4 output.mp4 --max-blobs 5 --max-distance 250 --no-trails
```
**Result**: Balanced amount of elements

### Test Different Settings
```bash
# Preview to find your sweet spot
python blob_tracker.py input.mp4 output.mp4 --preview --max-blobs 3 --max-distance 200
```
**Press Q to quit and adjust numbers**

## 📊 Comparison

| Setting | Lines | Effect |
|---------|-------|--------|
| Default | Many | Shows everything detected |
| `--max-blobs 10` | Fewer | Only 10 largest blobs |
| `--max-blobs 5` | Minimal | Only 5 largest blobs |
| `--max-distance 500` | Long | Connects distant blobs |
| `--max-distance 200` | Short | Only close blobs connect |
| `--max-distance 100` | Minimal | Very close only |

## 💡 Tips

1. **Start with preview**: Use `--preview` to test settings
   ```bash
   python blob_tracker.py input.mp4 test.mp4 --preview --max-blobs 5 --max-distance 200
   ```

2. **Too many lines?** 
   - Reduce `--max-blobs` (try 3-5)
   - Reduce `--max-distance` (try 150-250)
   - Add `--no-trails`

3. **Not enough connections?**
   - Increase `--max-distance` (try 400-600)
   - Remove `--max-blobs` limit

4. **Video-specific recommendations**:
   - **Busy scenes**: `--max-blobs 3 --max-distance 200`
   - **Sparse scenes**: `--max-blobs 10 --max-distance 400`
   - **Medium scenes**: `--max-blobs 5 --max-distance 300`

## 🎨 Aesthetic Presets

### Minimal Clean
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --max-blobs 3 \
  --max-distance 150 \
  --no-trails \
  --bright-only
```

### Moderate
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --max-blobs 5 \
  --max-distance 250 \
  --no-trails
```

### Busy (More elements)
```bash
python blob_tracker.py input.mp4 output.mp4 \
  --max-blobs 10 \
  --max-distance 400
```

## 📝 All Options Summary

```bash
python blob_tracker.py INPUT OUTPUT [OPTIONS]

Visual Control:
  --no-trails              Disable motion trails
  --no-connections         Disable connection lines
  --no-boxes              Disable blob boxes

Quantity Control:
  --max-blobs N           Limit to N largest blobs
  --max-distance PIXELS   Max distance for connections

Detection:
  --bright-only           Only detect bright regions
  --dark-only             Only detect dark regions

Other:
  --trail-length N        Trail length in frames (default: 30)
  --preview              Show preview window
```

## 🔍 Finding Your Perfect Settings

1. **Try the minimal preset first**:
   ```bash
   python blob_tracker.py input.mp4 test1.mp4 --preview --max-blobs 3 --max-distance 150 --no-trails
   ```

2. **If too sparse, increase gradually**:
   ```bash
   python blob_tracker.py input.mp4 test2.mp4 --preview --max-blobs 5 --max-distance 250 --no-trails
   ```

3. **If still too sparse**:
   ```bash
   python blob_tracker.py input.mp4 test3.mp4 --preview --max-blobs 8 --max-distance 350 --no-trails
   ```

4. **Once you like it, render without preview**:
   ```bash
   python blob_tracker.py input.mp4 final.mp4 --max-blobs 5 --max-distance 250 --no-trails
   ```

Happy tracking! 🎬✨
