#!/usr/bin/env python3
"""
Real-time Blob Tracking with Webcam
Tracks bright/dark blobs from your webcam in real-time with visual effects:
- Motion trails following blobs
- Connecting lines between multiple blobs
- Live preview with effects
"""

import cv2
import numpy as np
from collections import deque
import argparse
import sys


class RealtimeBlobTracker:
    def __init__(self, trail_length=30, min_blob_size=10, max_blob_size=500, 
                 max_blobs=None, max_connection_distance=500, 
                 background_frames=30, diff_threshold=0.15):
        """
        Initialize the real-time blob tracker with visual effects.
        
        Args:
            trail_length: Number of frames to keep in motion trail
            min_blob_size: Minimum area of blob to track (pixels)
            max_blob_size: Maximum area of blob to track (pixels)
            max_blobs: Maximum number of blobs to track (None = unlimited)
            max_connection_distance: Maximum distance to draw connection lines (pixels)
            background_frames: Number of frames to use for background model
            diff_threshold: Threshold for background difference (0.0-1.0)
        """
        self.trail_length = trail_length
        self.min_blob_size = min_blob_size
        self.max_blob_size = max_blob_size
        self.max_blobs = max_blobs
        self.max_connection_distance = max_connection_distance
        self.diff_threshold = diff_threshold
        
        # Store blob positions history for trails
        self.blob_trails = {}
        self.next_blob_id = 0
        
        # Background subtraction model
        self.background_model = None
        self.background_frames = background_frames
        self.frame_buffer = deque(maxlen=background_frames)
        self.is_background_initialized = False
        
        # Setup blob detector
        params = cv2.SimpleBlobDetector_Params()
        
        # Filter by area
        params.filterByArea = True
        params.minArea = min_blob_size
        params.maxArea = max_blob_size
        
        # Filter by circularity (0.0 to 1.0)
        params.filterByCircularity = False
        
        # Filter by convexity
        params.filterByConvexity = False
        
        # Filter by inertia
        params.filterByInertia = False
        
        # Filter by color (detect white blobs in mask)
        params.filterByColor = True
        params.blobColor = 255
        
        self.detector = cv2.SimpleBlobDetector_create(params)
    
    def _update_background(self, frame):
        """
        Update the background model with new frame.
        Uses median of recent frames for robust background estimation.
        """
        # Convert to grayscale and normalize to 0-1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        normalized = gray.astype(np.float32) / 255.0
        
        # Add frame to buffer
        self.frame_buffer.append(normalized)
        
        # Once we have enough frames, compute the median background
        if len(self.frame_buffer) >= self.background_frames:
            self.background_model = np.median(np.array(self.frame_buffer), axis=0)
            self.is_background_initialized = True
    
    def _create_difference_mask(self, frame):
        """
        Create a binary mask of pixels that differ from the background.
        
        Args:
            frame: Input frame (BGR)
            
        Returns:
            Binary mask (255 where difference > threshold, 0 otherwise)
        """
        # Convert to grayscale and normalize
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        normalized = gray.astype(np.float32) / 255.0
        
        # Calculate absolute difference from background
        diff = np.abs(normalized - self.background_model)
        
        # Create binary mask where difference > threshold
        mask = (diff > self.diff_threshold).astype(np.uint8) * 255
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill holes
        
        return mask
    
    def process_frame(self, frame, show_trails=True, show_connections=True, 
                     show_boxes=True, marker_style='both', use_points=False, 
                     invert_regions=False, show_numbers=False, show_mask=False):
        """
        Process a single frame and add visual effects using background subtraction.
        
        Args:
            frame: Input frame (BGR)
            show_trails: Whether to show motion trails
            show_connections: Whether to show connection lines between blobs
            show_boxes: Whether to show blob boxes/markers
            marker_style: 'both', 'outer', or 'inner' square
            use_points: Use points instead of squares
            invert_regions: Invert the region colors (negative effect)
            show_numbers: Show blob numbers as text
            show_mask: Show the difference mask in corner for debugging
            
        Returns:
            Processed frame with effects
        """
        # Update background model
        self._update_background(frame)
        
        # Create output frame
        output = frame.copy()
        
        # If background not initialized yet, just return original frame
        if not self.is_background_initialized:
            # Show initialization message
            cv2.putText(output, "Initializing background model...", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            progress = len(self.frame_buffer) / self.background_frames
            cv2.rectangle(output, (10, 50), (10 + int(300 * progress), 70), (0, 255, 255), -1)
            return output
        
        # Create difference mask
        mask = self._create_difference_mask(frame)
        
        # Detect blobs in the mask
        blobs = self.detector.detect(mask)
        all_blobs = [(blob, (255, 255, 255)) for blob in blobs]
        
        # Limit number of blobs if max_blobs is set
        if self.max_blobs is not None and len(all_blobs) > self.max_blobs:
            # Sort by blob size (larger blobs first) and take top N
            all_blobs = sorted(all_blobs, key=lambda x: x[0].size, reverse=True)[:self.max_blobs]
        
        # If no blobs detected, clean up old trails
        if not all_blobs:
            # Don't clear trails immediately - let them fade
            pass
        else:
            # Extract blob centers
            current_positions = [(blob.pt, color) for blob, color in all_blobs]
            
            # Update trails
            if show_trails:
                self._update_trails(current_positions)
        
        # Draw trails
        if show_trails:
            self._draw_trails(output)
        
        # Draw connecting lines between blobs
        if show_connections and all_blobs:
            current_positions = [(blob.pt, color) for blob, color in all_blobs]
            self._draw_connections(output, current_positions)
        
        # Draw blob markers
        if show_boxes and all_blobs:
            self._draw_blobs(output, all_blobs, marker_style, use_points, 
                           invert_regions, show_numbers)
        
        # Show mask in corner if requested
        if show_mask:
            # Resize mask to fit in corner
            mask_small = cv2.resize(mask, (160, 120))
            mask_color = cv2.cvtColor(mask_small, cv2.COLOR_GRAY2BGR)
            output[10:130, 10:170] = mask_color
            cv2.rectangle(output, (10, 10), (170, 130), (255, 255, 255), 1)
        
        return output
    
    def _update_trails(self, current_positions):
        """Update the position history for each blob."""
        # Simple assignment: assign current positions to trail IDs
        # For more complex tracking, you could use distance-based matching
        
        # Clear old trails if we have too many
        if len(self.blob_trails) > 50:
            self.blob_trails.clear()
            self.next_blob_id = 0
        
        # Add current positions to trails
        for i, (pos, color) in enumerate(current_positions):
            trail_id = i % 20  # Cycle through 20 trail IDs
            
            if trail_id not in self.blob_trails:
                self.blob_trails[trail_id] = deque(maxlen=self.trail_length)
            
            self.blob_trails[trail_id].append((pos, color))
    
    def _draw_trails(self, frame):
        """Draw motion trails for each blob."""
        for trail_id, positions in self.blob_trails.items():
            if len(positions) < 2:
                continue
            
            # Draw trail without fading effect
            for i in range(len(positions) - 1):
                if positions[i] is None or positions[i + 1] is None:
                    continue
                
                pos1, color1 = positions[i]
                pos2, color2 = positions[i + 1]
                
                # White color (no fading)
                trail_color = (255, 255, 255)
                
                cv2.line(frame, 
                        (int(pos1[0]), int(pos1[1])),
                        (int(pos2[0]), int(pos2[1])),
                        trail_color, 
                        1,  # 1px thick
                        cv2.LINE_AA)
    
    def _draw_connections(self, frame, positions):
        """Draw connecting lines between all detected blobs."""
        if len(positions) < 2:
            return
        
        # Draw lines between all pairs of blobs
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                pos1, color1 = positions[i]
                pos2, color2 = positions[j]
                
                # Calculate distance
                dist = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                
                # Only connect if distance is within max_connection_distance
                if dist < self.max_connection_distance:
                    # White color (no fading)
                    line_color = (255, 255, 255)
                    
                    cv2.line(frame,
                            (int(pos1[0]), int(pos1[1])),
                            (int(pos2[0]), int(pos2[1])),
                            line_color,
                            1,  # 1px thick
                            cv2.LINE_AA)
    
    def _draw_blobs(self, frame, blobs, marker_style='both', use_points=False, 
                   invert_regions=False, show_numbers=False):
        """Draw markers on detected blobs."""
        for idx, (blob, color) in enumerate(blobs, 1):
            x, y = blob.pt
            size = blob.size
            
            # Determine color (inverted or normal)
            marker_color = (0, 0, 0) if invert_regions else (255, 255, 255)
            
            if use_points:
                # Draw as points (small circles)
                cv2.circle(frame, (int(x), int(y)), 3, marker_color, -1, cv2.LINE_AA)
                # Outer ring
                cv2.circle(frame, (int(x), int(y)), 6, marker_color, 1, cv2.LINE_AA)
            else:
                # Draw as squares
                if marker_style in ['both', 'outer']:
                    # Draw outer square
                    half_size_outer = int(size * 1.5)
                    top_left_outer = (int(x - half_size_outer), int(y - half_size_outer))
                    bottom_right_outer = (int(x + half_size_outer), int(y + half_size_outer))
                    cv2.rectangle(frame, top_left_outer, bottom_right_outer, marker_color, 1, cv2.LINE_AA)
                
                if marker_style in ['both', 'inner']:
                    # Draw inner square
                    half_size_inner = int(size * 0.5)
                    top_left_inner = (int(x - half_size_inner), int(y - half_size_inner))
                    bottom_right_inner = (int(x + half_size_inner), int(y + half_size_inner))
                    cv2.rectangle(frame, top_left_inner, bottom_right_inner, marker_color, 1, cv2.LINE_AA)
            
            # Draw blob number
            if show_numbers:
                text = str(idx)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                
                # Get text size for positioning
                (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                
                # Position text above the blob
                text_x = int(x - text_width / 2)
                text_y = int(y - size * 2)
                
                # Draw text
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, 
                          marker_color, thickness, cv2.LINE_AA)


def run_realtime(camera_id=1, trail_length=30, show_trails=True, 
                 show_connections=True, show_boxes=True, max_blobs=None, 
                 max_connection_distance=500, marker_style='both', use_points=False, 
                 invert_regions=False, show_numbers=False, save_output=None, 
                 fps=30, background_frames=30, diff_threshold=0.15, show_mask=False):
    """
    Run real-time blob tracking from webcam using background subtraction.
    
    Args:
        camera_id: Camera device ID (0 for default webcam)
        trail_length: Length of motion trails
        show_trails: Whether to show motion trails
        show_connections: Whether to show connection lines
        show_boxes: Whether to show blob boxes
        max_blobs: Maximum number of blobs to track (None = unlimited)
        max_connection_distance: Maximum distance for connection lines (pixels)
        marker_style: 'both', 'outer', or 'inner' for squares
        use_points: Use points instead of squares
        invert_regions: Invert colors (negative effect)
        show_numbers: Show blob numbers as text
        save_output: Path to save video output (None = no recording)
        fps: FPS for saved video output
        background_frames: Number of frames for background model
        diff_threshold: Threshold for background difference (0.0-1.0)
        show_mask: Show the difference mask in corner
    """
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        print("Try a different camera ID (e.g., 0, 1, 2)")
        sys.exit(1)
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Camera opened: {width}x{height}")
    print(f"Detection: Background subtraction (threshold: {diff_threshold})")
    print(f"Background model: {background_frames} frames")
    print(f"Effects: {'trails ' if show_trails else ''}{'connections ' if show_connections else ''}{'boxes' if show_boxes else ''}")
    print(f"Trail length: {trail_length} frames")
    if max_blobs:
        print(f"Max blobs: {max_blobs}")
    if show_connections:
        print(f"Max connection distance: {max_connection_distance}px")
    print("\nControls:")
    print("  Q - Quit")
    print("  R - Start/Stop recording")
    print("  SPACE - Take screenshot")
    print("  T - Toggle trails")
    print("  C - Toggle connections")
    print("  B - Toggle boxes")
    print("  M - Toggle mask view")
    print("  + - Increase threshold")
    print("  - - Decrease threshold")
    print("  BACKSPACE - Reset background model")
    
    # Setup video writer if save_output is specified
    video_writer = None
    recording = False
    if save_output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(save_output, fourcc, fps, (width, height))
        recording = True
        print(f"\nRecording to: {save_output}")
    
    # Create blob tracker
    tracker = RealtimeBlobTracker(
        trail_length=trail_length, 
        max_blobs=max_blobs,
        max_connection_distance=max_connection_distance,
        background_frames=background_frames,
        diff_threshold=diff_threshold
    )
    
    # Runtime toggles
    toggle_trails = show_trails
    toggle_connections = show_connections
    toggle_boxes = show_boxes
    toggle_mask = show_mask
    screenshot_count = 0
    current_threshold = diff_threshold
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to grab frame")
                break
            
            # Process frame
            processed = tracker.process_frame(
                frame, 
                toggle_trails, 
                toggle_connections, 
                toggle_boxes, 
                marker_style, 
                use_points, 
                invert_regions, 
                show_numbers,
                toggle_mask
            )
            
            # Add recording indicator
            if recording and video_writer is not None:
                cv2.circle(processed, (30, 30), 10, (0, 0, 255), -1)
                cv2.putText(processed, "REC", (50, 40), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Show threshold value
            cv2.putText(processed, f"Threshold: {current_threshold:.3f}", 
                       (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Write frame if recording
            if recording and video_writer is not None:
                video_writer.write(processed)
            
            # Display frame
            cv2.imshow('Real-time Blob Tracker (Press Q to quit)', processed)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('r'):
                if video_writer is None:
                    # Start new recording
                    timestamp = cv2.getTickCount()
                    filename = f"recording_{int(timestamp)}.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                    recording = True
                    print(f"\nStarted recording to: {filename}")
                else:
                    # Stop recording
                    recording = not recording
                    if recording:
                        print("\nResumed recording")
                    else:
                        print("\nPaused recording")
            elif key == ord(' '):
                # Take screenshot
                screenshot_count += 1
                screenshot_name = f"screenshot_{screenshot_count}.png"
                cv2.imwrite(screenshot_name, processed)
                print(f"\nScreenshot saved: {screenshot_name}")
            elif key == ord('t'):
                toggle_trails = not toggle_trails
                print(f"\nTrails: {'ON' if toggle_trails else 'OFF'}")
            elif key == ord('c'):
                toggle_connections = not toggle_connections
                print(f"\nConnections: {'ON' if toggle_connections else 'OFF'}")
            elif key == ord('b'):
                toggle_boxes = not toggle_boxes
                print(f"\nBoxes: {'ON' if toggle_boxes else 'OFF'}")
            elif key == ord('m'):
                toggle_mask = not toggle_mask
                print(f"\nMask view: {'ON' if toggle_mask else 'OFF'}")
            elif key == ord('+') or key == ord('='):
                current_threshold = min(1.0, current_threshold + 0.01)
                tracker.diff_threshold = current_threshold
                print(f"\nThreshold increased: {current_threshold:.3f}")
            elif key == ord('-') or key == ord('_'):
                current_threshold = max(0.0, current_threshold - 0.01)
                tracker.diff_threshold = current_threshold
                print(f"\nThreshold decreased: {current_threshold:.3f}")
            elif key == 8 or key == 127:  # Backspace/Delete
                # Reset background model
                tracker.frame_buffer.clear()
                tracker.is_background_initialized = False
                tracker.blob_trails.clear()
                print("\nBackground model reset")
    
    finally:
        # Cleanup
        cap.release()
        if video_writer is not None:
            video_writer.release()
            if recording:
                print(f"\nRecording saved")
        cv2.destroyAllWindows()
    
    print("Done!")


def main():
    parser = argparse.ArgumentParser(
        description='Real-time blob tracking with webcam using background subtraction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python realtime_blob_tracker.py
  
  # Adjust detection threshold (lower = more sensitive)
  python realtime_blob_tracker.py --threshold 0.1
  
  # Use more frames for background model (slower adaptation)
  python realtime_blob_tracker.py --bg-frames 60
  
  # Show mask view for debugging
  python realtime_blob_tracker.py --show-mask
  
  # Longer trails with limited blobs
  python realtime_blob_tracker.py --trail-length 50 --max-blobs 5
  
  # Record output to file
  python realtime_blob_tracker.py --save output.mp4
  
  # Use external camera
  python realtime_blob_tracker.py --camera 1

Interactive Controls:
  Q          - Quit
  R          - Start/Stop recording
  SPACE      - Take screenshot
  T          - Toggle trails on/off
  C          - Toggle connections on/off
  B          - Toggle boxes on/off
  M          - Toggle mask view (for debugging)
  +/=        - Increase threshold (less sensitive)
  -/_        - Decrease threshold (more sensitive)
  BACKSPACE  - Reset background model

How it works:
  The tracker builds a background model from the first 30 frames (default).
  Anything that differs from this background by more than the threshold
  (default 0.15 or 15%) is detected as a blob. This allows tracking of
  any movement or changes, not just bright spots.
        """
    )
    
    parser.add_argument('--camera', type=int, default=1,
                       help='Camera device ID (default: 1)')
    parser.add_argument('--threshold', type=float, default=0.15,
                       help='Background difference threshold 0.0-1.0 (default: 0.15)')
    parser.add_argument('--bg-frames', type=int, default=30,
                       help='Number of frames for background model (default: 30)')
    parser.add_argument('--trail-length', type=int, default=30,
                       help='Length of motion trails in frames (default: 30)')
    parser.add_argument('--no-trails', action='store_true',
                       help='Disable motion trails')
    parser.add_argument('--no-connections', action='store_true',
                       help='Disable connection lines between blobs')
    parser.add_argument('--no-boxes', action='store_true',
                       help='Disable blob boxes/markers')
    parser.add_argument('--max-blobs', type=int, default=None,
                       help='Maximum number of blobs to track (default: unlimited)')
    parser.add_argument('--max-distance', type=int, default=500,
                       help='Maximum distance for connection lines in pixels (default: 500)')
    parser.add_argument('--marker-style', choices=['both', 'outer', 'inner'], default='both',
                       help='Square marker style: both (inner+outer), outer only, or inner only (default: both)')
    parser.add_argument('--use-points', action='store_true',
                       help='Use points instead of squares for blob markers')
    parser.add_argument('--invert', action='store_true',
                       help='Invert marker colors (black instead of white)')
    parser.add_argument('--show-numbers', action='store_true',
                       help='Show blob numbers as text labels')
    parser.add_argument('--show-mask', action='store_true',
                       help='Show difference mask in corner for debugging')
    parser.add_argument('--save', type=str, default=None,
                       help='Save output to video file (e.g., output.mp4)')
    parser.add_argument('--fps', type=int, default=30,
                       help='FPS for saved video output (default: 30)')
    
    args = parser.parse_args()
    
    # Determine what to show
    show_trails = not args.no_trails
    show_connections = not args.no_connections
    show_boxes = not args.no_boxes
    
    # Run real-time tracking
    run_realtime(
        camera_id=args.camera,
        trail_length=args.trail_length,
        show_trails=show_trails,
        show_connections=show_connections,
        show_boxes=show_boxes,
        max_blobs=args.max_blobs,
        max_connection_distance=args.max_distance,
        marker_style=args.marker_style,
        use_points=args.use_points,
        invert_regions=args.invert,
        show_numbers=args.show_numbers,
        save_output=args.save,
        fps=args.fps,
        background_frames=args.bg_frames,
        diff_threshold=args.threshold,
        show_mask=args.show_mask
    )


if __name__ == '__main__':
    main()
