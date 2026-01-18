#!/usr/bin/env python3
"""
Example script to create a test video with moving bright blobs
for demonstrating the blob tracker effects.
"""

import cv2
import numpy as np
import math


def create_test_video(output_path='test_input.mp4', duration_seconds=10, fps=30):
    """
    Create a test video with moving bright blobs.
    
    Args:
        output_path: Path to save the test video
        duration_seconds: Duration of the video in seconds
        fps: Frames per second
    """
    width, height = 1280, 720
    total_frames = duration_seconds * fps
    
    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Creating test video: {width}x{height} @ {fps}fps, {total_frames} frames")
    
    for frame_num in range(total_frames):
        # Create dark background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 20, 30)  # Dark blue background
        
        # Calculate time for smooth animation
        t = frame_num / fps
        
        # Create multiple moving bright blobs
        
        # Blob 1: Circular motion
        x1 = int(width/2 + 200 * math.cos(t * 2))
        y1 = int(height/2 + 200 * math.sin(t * 2))
        cv2.circle(frame, (x1, y1), 30, (255, 255, 255), -1)
        
        # Blob 2: Figure-8 motion
        x2 = int(width/2 + 300 * math.sin(t * 1.5))
        y2 = int(height/2 + 150 * math.sin(t * 3))
        cv2.circle(frame, (x2, y2), 25, (255, 255, 200), -1)
        
        # Blob 3: Horizontal oscillation
        x3 = int(width/4 + 100 * math.sin(t * 3))
        y3 = int(height/3)
        cv2.circle(frame, (x3, y3), 20, (255, 200, 255), -1)
        
        # Blob 4: Vertical oscillation
        x4 = int(3 * width/4)
        y4 = int(height/2 + 150 * math.cos(t * 2.5))
        cv2.circle(frame, (x4, y4), 22, (200, 255, 255), -1)
        
        # Blob 5: Diagonal motion
        x5 = int((width/4) + (width/2) * ((frame_num % fps) / fps))
        y5 = int((height/4) + (height/2) * ((frame_num % fps) / fps))
        cv2.circle(frame, (x5, y5), 18, (255, 255, 150), -1)
        
        # Add some random sparkles
        for _ in range(5):
            rx = np.random.randint(50, width - 50)
            ry = np.random.randint(50, height - 50)
            size = np.random.randint(5, 15)
            cv2.circle(frame, (rx, ry), size, (255, 255, 255), -1)
        
        # Write frame
        out.write(frame)
        
        # Progress indicator
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"Progress: {frame_num}/{total_frames} frames ({progress:.1f}%)", end='\r')
    
    out.release()
    print(f"\nTest video created: {output_path}")
    print(f"\nNow run: python blob_tracker.py {output_path} test_output.mp4 --preview")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Create a test video with moving blobs')
    parser.add_argument('--output', default='test_input.mp4', help='Output video file path')
    parser.add_argument('--duration', type=int, default=10, help='Duration in seconds (default: 10)')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second (default: 30)')
    
    args = parser.parse_args()
    
    create_test_video(args.output, args.duration, args.fps)
