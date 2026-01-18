#!/usr/bin/env python3
"""
Utility script to display video file information.
"""

import cv2
import sys


def get_video_info(video_path):
    """Display information about a video file."""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return False
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"Video Information: {video_path}")
    print(f"{'='*50}")
    print(f"Resolution:    {width} x {height}")
    print(f"FPS:           {fps:.2f}")
    print(f"Total Frames:  {total_frames}")
    print(f"Duration:      {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"{'='*50}\n")
    
    cap.release()
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python video_info.py <video_file>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    get_video_info(video_path)
