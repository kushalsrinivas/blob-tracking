#!/usr/bin/env python3
"""
Example of using the BlobTracker class programmatically.
This shows how to integrate blob tracking into your own Python scripts.
"""

from blob_tracker import BlobTracker, process_video


def example_basic_usage():
    """Basic example: process a video file."""
    print("Example 1: Basic Usage")
    print("-" * 50)
    
    process_video(
        input_path='input.mp4',
        output_path='output.mp4',
        detect_bright=True,
        detect_dark=False,
        trail_length=30,
        preview=False
    )


def example_custom_tracker():
    """Example: Create a custom tracker with specific settings."""
    print("\nExample 2: Custom Tracker")
    print("-" * 50)
    
    import cv2
    
    # Create tracker with custom settings
    tracker = BlobTracker(
        trail_length=50,      # Longer trails
        min_blob_size=20,     # Larger minimum blob size
        max_blob_size=300     # Smaller maximum blob size
    )
    
    # Open video
    cap = cv2.VideoCapture('input.mp4')
    
    # Process just one frame as example
    ret, frame = cap.read()
    if ret:
        # Process frame with both bright and dark detection
        processed = tracker.process_frame(frame, detect_bright=True, detect_dark=True)
        
        # Save result
        cv2.imwrite('example_frame.jpg', processed)
        print("Saved example_frame.jpg")
    
    cap.release()


def example_real_time_webcam():
    """Example: Real-time blob tracking from webcam."""
    print("\nExample 3: Real-time Webcam (press Q to quit)")
    print("-" * 50)
    
    import cv2
    
    # Create tracker
    tracker = BlobTracker(trail_length=20, min_blob_size=15)
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam opened. Press 'Q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame (only bright blobs for webcam)
        processed = tracker.process_frame(frame, detect_bright=True, detect_dark=False)
        
        # Show result
        cv2.imshow('Blob Tracking - Press Q to quit', processed)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def example_batch_processing():
    """Example: Process multiple videos in batch."""
    print("\nExample 4: Batch Processing")
    print("-" * 50)
    
    videos = [
        ('video1.mp4', 'output1.mp4'),
        ('video2.mp4', 'output2.mp4'),
        ('video3.mp4', 'output3.mp4'),
    ]
    
    for input_path, output_path in videos:
        print(f"\nProcessing {input_path} -> {output_path}")
        try:
            process_video(
                input_path=input_path,
                output_path=output_path,
                detect_bright=True,
                detect_dark=False,
                trail_length=30,
                preview=False
            )
        except Exception as e:
            print(f"Error processing {input_path}: {e}")


def main():
    """Show usage examples."""
    print("\n" + "="*60)
    print("Blob Tracker - Programmatic Usage Examples")
    print("="*60)
    
    print("\n1. Basic Usage - Process a single video file")
    print("   Code: process_video('input.mp4', 'output.mp4')")
    
    print("\n2. Custom Settings - Create tracker with specific parameters")
    print("   Code: tracker = BlobTracker(trail_length=50, min_blob_size=20)")
    
    print("\n3. Real-time - Use with webcam")
    print("   Code: See example_real_time_webcam() function")
    
    print("\n4. Batch Processing - Process multiple videos")
    print("   Code: See example_batch_processing() function")
    
    print("\n" + "="*60)
    print("\nTo run these examples, uncomment them in the code below:")
    print("  - example_basic_usage()")
    print("  - example_custom_tracker()")
    print("  - example_real_time_webcam()")
    print("  - example_batch_processing()")
    print("="*60 + "\n")
    
    # Uncomment the examples you want to run:
    
    # example_basic_usage()
    # example_custom_tracker()
    # example_real_time_webcam()
    # example_batch_processing()


if __name__ == '__main__':
    main()
