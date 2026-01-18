#!/usr/bin/env python3
"""
Blob Tracking Video Effect Script
Tracks bright/dark blobs in a video and adds cool visual effects:
- Motion trails following blobs
- Connecting lines between multiple blobs
"""

import cv2
import numpy as np
from collections import deque
import argparse
import sys


class BlobTracker:
    def __init__(self, trail_length=30, min_blob_size=10, max_blob_size=500, 
                 max_blobs=None, max_connection_distance=500, 
                 use_background_subtraction=False, background_frames=30, 
                 diff_threshold=0.15):
        """
        Initialize the blob tracker with visual effects.
        
        Args:
            trail_length: Number of frames to keep in motion trail
            min_blob_size: Minimum area of blob to track (pixels)
            max_blob_size: Maximum area of blob to track (pixels)
            max_blobs: Maximum number of blobs to track (None = unlimited)
            max_connection_distance: Maximum distance to draw connection lines (pixels)
            use_background_subtraction: Use background subtraction instead of bright/dark detection
            background_frames: Number of frames for background model
            diff_threshold: Threshold for background difference (0.0-1.0)
        """
        self.trail_length = trail_length
        self.min_blob_size = min_blob_size
        self.max_blob_size = max_blob_size
        self.max_blobs = max_blobs
        self.max_connection_distance = max_connection_distance
        self.use_background_subtraction = use_background_subtraction
        self.diff_threshold = diff_threshold
        
        # Store blob positions history for trails
        self.blob_trails = {}
        self.next_blob_id = 0
        
        # Background subtraction model (if enabled)
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
    
    def process_frame(self, frame, detect_bright=True, detect_dark=False, 
                     show_trails=True, show_connections=True, show_boxes=True,
                     marker_style='both', use_points=False, invert_regions=False, 
                     show_numbers=False):
        """
        Process a single frame and add visual effects.
        
        Args:
            frame: Input frame (BGR)
            detect_bright: Whether to detect bright regions (ignored if using background subtraction)
            detect_dark: Whether to detect dark regions (ignored if using background subtraction)
            show_trails: Whether to show motion trails
            show_connections: Whether to show connection lines between blobs
            show_boxes: Whether to show blob boxes/markers
            marker_style: 'both', 'outer', or 'inner' square
            use_points: Use points instead of squares
            invert_regions: Invert the region colors (negative effect)
            show_numbers: Show blob numbers as text
            
        Returns:
            Processed frame with effects
        """
        # Create output frame
        output = frame.copy()
        
        all_blobs = []
        
        if self.use_background_subtraction:
            # Use background subtraction method
            self._update_background(frame)
            
            # If background not initialized yet, return frame without effects
            if not self.is_background_initialized:
                return output
            
            # Create difference mask
            mask = self._create_difference_mask(frame)
            
            # Detect blobs in the mask
            blobs = self.detector.detect(mask)
            all_blobs = [(blob, (255, 255, 255)) for blob in blobs]
        else:
            # Use original bright/dark detection method
            # Convert to grayscale for blob detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect bright blobs
            if detect_bright:
                # Apply threshold to get bright regions
                _, bright_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
                bright_blobs = self.detector.detect(bright_mask)
                all_blobs.extend([(blob, (255, 255, 255)) for blob in bright_blobs])  # White
            
            # Detect dark blobs
            if detect_dark:
                # Invert for dark regions
                dark_mask = cv2.bitwise_not(gray)
                _, dark_mask = cv2.threshold(dark_mask, 200, 255, cv2.THRESH_BINARY)
                dark_blobs = self.detector.detect(dark_mask)
                all_blobs.extend([(blob, (255, 255, 255)) for blob in dark_blobs])  # White
        
        # Limit number of blobs if max_blobs is set
        if self.max_blobs is not None and len(all_blobs) > self.max_blobs:
            # Sort by blob size (larger blobs first) and take top N
            all_blobs = sorted(all_blobs, key=lambda x: x[0].size, reverse=True)[:self.max_blobs]
        
        # If no blobs detected, clean up old trails
        if not all_blobs:
            self.blob_trails.clear()
            return output
        
        # Extract blob centers
        current_positions = [(blob.pt, color) for blob, color in all_blobs]
        
        # Update trails
        if show_trails:
            self._update_trails(current_positions)
        
        # Draw trails
        if show_trails:
            self._draw_trails(output)
        
        # Draw connecting lines between blobs
        if show_connections:
            self._draw_connections(output, current_positions)
        
        # Draw blob markers
        if show_boxes:
            self._draw_blobs(output, all_blobs, marker_style, use_points, 
                           invert_regions, show_numbers)
        
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
                
                # Draw text background for readability (optional black background)
                # if not invert_regions:
                #     cv2.rectangle(frame, 
                #                 (text_x - 2, text_y - text_height - 2),
                #                 (text_x + text_width + 2, text_y + baseline),
                #                 (0, 0, 0), -1)
                
                # Draw text
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, 
                          marker_color, thickness, cv2.LINE_AA)


def process_video(input_path, output_path, detect_bright=True, detect_dark=True, 
                  trail_length=30, preview=False, show_trails=True, 
                  show_connections=True, show_boxes=True, max_blobs=None,
                  max_connection_distance=500, marker_style='both', use_points=False,
                  invert_regions=False, show_numbers=False, 
                  use_background_subtraction=False, background_frames=30, 
                  diff_threshold=0.15):
    """
    Process a video file with blob tracking effects.
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file
        detect_bright: Whether to detect bright regions
        detect_dark: Whether to detect dark regions
        trail_length: Length of motion trails
        preview: Show preview window during processing
        show_trails: Whether to show motion trails
        show_connections: Whether to show connection lines
        show_boxes: Whether to show blob boxes
        max_blobs: Maximum number of blobs to track (None = unlimited)
        max_connection_distance: Maximum distance for connection lines (pixels)
        marker_style: 'both', 'outer', or 'inner' for squares
        use_points: Use points instead of squares
        invert_regions: Invert colors (negative effect)
        show_numbers: Show blob numbers as text
        use_background_subtraction: Use background subtraction instead of bright/dark detection
        background_frames: Number of frames for background model
        diff_threshold: Threshold for background difference (0.0-1.0)
    """
    # Open input video
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{input_path}'")
        sys.exit(1)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Input video: {width}x{height} @ {fps}fps, {total_frames} frames")
    
    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print(f"Error: Could not create output video file '{output_path}'")
        sys.exit(1)
    
    # Create blob tracker
    tracker = BlobTracker(
        trail_length=trail_length, 
        max_blobs=max_blobs,
        max_connection_distance=max_connection_distance,
        use_background_subtraction=use_background_subtraction,
        background_frames=background_frames,
        diff_threshold=diff_threshold
    )
    
    print(f"Processing video...")
    if use_background_subtraction:
        print(f"Detection: Background subtraction (threshold: {diff_threshold})")
        print(f"Background model: {background_frames} frames")
    else:
        print(f"Detecting: {'bright regions ' if detect_bright else ''}{'dark regions' if detect_dark else ''}")
    print(f"Effects: {'trails ' if show_trails else ''}{'connections ' if show_connections else ''}{'boxes' if show_boxes else ''}")
    print(f"Trail length: {trail_length} frames")
    if max_blobs:
        print(f"Max blobs: {max_blobs}")
    if show_connections:
        print(f"Max connection distance: {max_connection_distance}px")
    
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Process frame
            processed = tracker.process_frame(frame, detect_bright, detect_dark,
                                            show_trails, show_connections, show_boxes,
                                            marker_style, use_points, invert_regions, 
                                            show_numbers)
            
            # Write frame
            out.write(processed)
            
            # Show preview if requested
            if preview:
                cv2.imshow('Blob Tracking Preview (press Q to quit)', processed)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nProcessing interrupted by user")
                    break
            
            frame_count += 1
            
            # Progress indicator
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {frame_count}/{total_frames} frames ({progress:.1f}%)", end='\r')
    
    finally:
        # Cleanup
        cap.release()
        out.release()
        if preview:
            cv2.destroyAllWindows()
    
    print(f"\nDone! Processed {frame_count} frames")
    print(f"Output saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Add cool blob tracking visual effects to videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process video with default settings (both bright and dark regions)
  python blob_tracker.py input.mp4 output.mp4
  
  # Use background subtraction to detect any movement
  python blob_tracker.py input.mp4 output.mp4 --background-subtraction
  
  # Background subtraction with custom threshold (lower = more sensitive)
  python blob_tracker.py input.mp4 output.mp4 --background-subtraction --threshold 0.1
  
  # Only track bright regions with longer trails
  python blob_tracker.py input.mp4 output.mp4 --bright-only --trail-length 50
  
  # Show only connection lines (no trails or boxes)
  python blob_tracker.py input.mp4 output.mp4 --no-trails --no-boxes
  
  # Show only boxes (no trails or connections)
  python blob_tracker.py input.mp4 output.mp4 --no-trails --no-connections
  
  # Limit to 5 blobs max with shorter connection distance
  python blob_tracker.py input.mp4 output.mp4 --max-blobs 5 --max-distance 200
  
  # Use points instead of squares with numbering
  python blob_tracker.py input.mp4 output.mp4 --use-points --show-numbers
  
  # Only outer squares with inverted colors
  python blob_tracker.py input.mp4 output.mp4 --marker-style outer --invert
  
  # Show preview while processing
  python blob_tracker.py input.mp4 output.mp4 --preview

Detection Methods:
  By default, the script detects bright and dark regions in the video.
  Use --background-subtraction to detect anything that differs from the 
  background, which is better for tracking movement and changes.
        """
    )
    
    parser.add_argument('input', help='Input video file path')
    parser.add_argument('output', help='Output video file path')
    parser.add_argument('--bright-only', action='store_true',
                       help='Only detect bright regions (default: both bright and dark)')
    parser.add_argument('--dark-only', action='store_true',
                       help='Only detect dark regions (default: both bright and dark)')
    parser.add_argument('--background-subtraction', action='store_true',
                       help='Use background subtraction to detect movement (ignores --bright-only/--dark-only)')
    parser.add_argument('--threshold', type=float, default=0.15,
                       help='Background difference threshold 0.0-1.0 (default: 0.15, only for --background-subtraction)')
    parser.add_argument('--bg-frames', type=int, default=30,
                       help='Number of frames for background model (default: 30, only for --background-subtraction)')
    parser.add_argument('--trail-length', type=int, default=30,
                       help='Length of motion trails in frames (default: 30)')
    parser.add_argument('--preview', action='store_true',
                       help='Show preview window during processing')
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
    
    args = parser.parse_args()
    
    # Determine what to detect
    if args.bright_only and args.dark_only:
        print("Error: Cannot specify both --bright-only and --dark-only")
        sys.exit(1)
    
    detect_bright = not args.dark_only
    detect_dark = not args.bright_only
    
    # Determine what to show
    show_trails = not args.no_trails
    show_connections = not args.no_connections
    show_boxes = not args.no_boxes
    
    # Process video
    process_video(
        args.input,
        args.output,
        detect_bright=detect_bright,
        detect_dark=detect_dark,
        trail_length=args.trail_length,
        preview=args.preview,
        show_trails=show_trails,
        show_connections=show_connections,
        show_boxes=show_boxes,
        max_blobs=args.max_blobs,
        max_connection_distance=args.max_distance,
        marker_style=args.marker_style,
        use_points=args.use_points,
        invert_regions=args.invert,
        show_numbers=args.show_numbers,
        use_background_subtraction=args.background_subtraction,
        background_frames=args.bg_frames,
        diff_threshold=args.threshold
    )


if __name__ == '__main__':
    main()
