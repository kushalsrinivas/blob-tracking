#!/usr/bin/env python3
"""
Video Downloader Script
Downloads videos from URLs to use with the blob tracker.
Supports various video platforms and direct video links.
"""

import sys
import os
import argparse
from urllib.parse import urlparse
import subprocess


def is_yt_dlp_installed():
    """Check if yt-dlp is installed."""
    try:
        subprocess.run(['yt-dlp', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_with_yt_dlp(url, output_path=None, quality='best'):
    """
    Download video using yt-dlp (supports YouTube, Vimeo, and many other platforms).
    
    Args:
        url: Video URL
        output_path: Output file path (optional)
        quality: Video quality ('best', 'worst', or specific format)
    """
    if not is_yt_dlp_installed():
        print("Error: yt-dlp is not installed")
        print("\nTo install yt-dlp:")
        print("  pip install yt-dlp")
        print("\nOr using homebrew (macOS):")
        print("  brew install yt-dlp")
        return False
    
    cmd = ['yt-dlp']
    
    # Add quality option
    if quality == 'best':
        cmd.extend(['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'])
    elif quality == 'worst':
        cmd.extend(['-f', 'worst'])
    else:
        cmd.extend(['-f', quality])
    
    # Add output template
    if output_path:
        cmd.extend(['-o', output_path])
    else:
        cmd.extend(['-o', '%(title)s.%(ext)s'])
    
    # Add URL
    cmd.append(url)
    
    print(f"Downloading video from: {url}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        subprocess.run(cmd, check=True)
        print("-" * 60)
        print("✓ Download complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading video: {e}")
        return False


def download_with_curl(url, output_path):
    """
    Download video using curl (for direct video links).
    
    Args:
        url: Direct video URL
        output_path: Output file path
    """
    print(f"Downloading video from: {url}")
    print(f"Saving to: {output_path}")
    print("-" * 60)
    
    cmd = [
        'curl',
        '-L',  # Follow redirects
        '-o', output_path,
        '--progress-bar',
        url
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("-" * 60)
        print(f"✓ Download complete: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading video: {e}")
        return False


def download_with_wget(url, output_path):
    """
    Download video using wget (alternative to curl).
    
    Args:
        url: Direct video URL
        output_path: Output file path
    """
    print(f"Downloading video from: {url}")
    print(f"Saving to: {output_path}")
    print("-" * 60)
    
    cmd = [
        'wget',
        '-O', output_path,
        '--show-progress',
        url
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("-" * 60)
        print(f"✓ Download complete: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading video: {e}")
        return False


def download_with_python(url, output_path):
    """
    Download video using Python's requests library (fallback method).
    
    Args:
        url: Direct video URL
        output_path: Output file path
    """
    try:
        import requests
    except ImportError:
        print("Error: requests library is not installed")
        print("Install with: pip install requests")
        return False
    
    print(f"Downloading video from: {url}")
    print(f"Saving to: {output_path}")
    print("-" * 60)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Show progress
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"Progress: {downloaded}/{total_size} bytes ({percent:.1f}%)", end='\r')
        
        print("\n" + "-" * 60)
        print(f"✓ Download complete: {output_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading video: {e}")
        return False


def is_direct_video_url(url):
    """Check if URL is a direct video link."""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in video_extensions)


def is_supported_platform(url):
    """Check if URL is from a supported video platform."""
    supported_domains = [
        'youtube.com', 'youtu.be',
        'vimeo.com',
        'dailymotion.com',
        'twitter.com', 'x.com',
        'facebook.com',
        'instagram.com',
        'tiktok.com',
        'twitch.tv',
        'reddit.com'
    ]
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace('www.', '')
    return any(supported in domain for supported in supported_domains)


def download_video(url, output_path=None, method='auto', quality='best'):
    """
    Download video from URL using the best available method.
    
    Args:
        url: Video URL
        output_path: Output file path (optional)
        method: Download method ('auto', 'yt-dlp', 'curl', 'wget', 'python')
        quality: Video quality for yt-dlp ('best', 'worst', or format code)
    
    Returns:
        bool: True if download successful
    """
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        print("Error: Invalid URL (must start with http:// or https://)")
        return False
    
    # Generate output path if not provided
    if not output_path:
        if is_direct_video_url(url):
            # Extract filename from URL
            parsed = urlparse(url)
            output_path = os.path.basename(parsed.path)
            if not output_path:
                output_path = 'downloaded_video.mp4'
        else:
            output_path = 'downloaded_video.mp4'
    
    # Ensure output path has an extension
    if not os.path.splitext(output_path)[1]:
        output_path += '.mp4'
    
    # Auto-detect best method
    if method == 'auto':
        if is_supported_platform(url):
            method = 'yt-dlp'
        elif is_direct_video_url(url):
            method = 'curl'
        else:
            # Try yt-dlp first, fallback to curl
            method = 'yt-dlp' if is_yt_dlp_installed() else 'curl'
    
    # Download using selected method
    print(f"Using method: {method}")
    print("")
    
    if method == 'yt-dlp':
        return download_with_yt_dlp(url, output_path, quality)
    elif method == 'curl':
        return download_with_curl(url, output_path)
    elif method == 'wget':
        return download_with_wget(url, output_path)
    elif method == 'python':
        return download_with_python(url, output_path)
    else:
        print(f"Error: Unknown method '{method}'")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Download videos from URLs for blob tracking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download from YouTube (requires yt-dlp)
  python download_video.py "https://www.youtube.com/watch?v=..." -o my_video.mp4
  
  # Download direct video link
  python download_video.py "https://example.com/video.mp4" -o downloaded.mp4
  
  # Auto-detect best method
  python download_video.py "https://vimeo.com/..." -o vimeo_video.mp4
  
  # Specify quality (for yt-dlp)
  python download_video.py "https://youtube.com/..." -q worst
  
  # Force specific download method
  python download_video.py "https://example.com/video.mp4" -m curl

Supported platforms (with yt-dlp):
  - YouTube, Vimeo, Dailymotion
  - Twitter/X, Facebook, Instagram
  - TikTok, Twitch, Reddit
  - And many more!

For direct video links, curl/wget/python methods work without yt-dlp.
        """
    )
    
    parser.add_argument('url', help='Video URL to download')
    parser.add_argument('-o', '--output', 
                       help='Output file path (default: auto-generated)')
    parser.add_argument('-m', '--method', 
                       choices=['auto', 'yt-dlp', 'curl', 'wget', 'python'],
                       default='auto',
                       help='Download method (default: auto)')
    parser.add_argument('-q', '--quality',
                       default='best',
                       help='Video quality for yt-dlp (default: best)')
    parser.add_argument('--list-formats',
                       action='store_true',
                       help='List available formats for the video (yt-dlp only)')
    
    args = parser.parse_args()
    
    # List formats if requested
    if args.list_formats:
        if not is_yt_dlp_installed():
            print("Error: yt-dlp is required to list formats")
            print("Install with: pip install yt-dlp")
            sys.exit(1)
        
        print(f"Available formats for: {args.url}\n")
        subprocess.run(['yt-dlp', '-F', args.url])
        sys.exit(0)
    
    # Download video
    success = download_video(args.url, args.output, args.method, args.quality)
    
    if success:
        print("\n✓ Video ready for blob tracking!")
        if args.output:
            print(f"\nNext step:")
            print(f"  python blob_tracker.py {args.output} output.mp4 --preview")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
