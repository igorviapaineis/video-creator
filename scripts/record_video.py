#!/usr/bin/env python3
"""
Video Creator — Record HTML animation to PNG frames via Playwright
Usage:
  python3 record_video.py --input video.html --output ./frames/ --duration 10 --fps 30 --orientation portrait
"""

import argparse
import os
import sys
import time

def record(args):
    from playwright.sync_api import sync_playwright

    # Dimensions
    if args.orientation == 'portrait':
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    # Output dir
    os.makedirs(args.output, exist_ok=True)

    html_path = os.path.abspath(args.input)
    if not os.path.exists(html_path):
        print(f"ERROR: {html_path} not found")
        sys.exit(1)

    file_url = f"file://{html_path}"
    total_frames = args.duration * args.fps
    interval_ms = 1000.0 / args.fps

    print(f"Recording {total_frames} frames ({args.duration}s @ {args.fps}fps, {args.orientation})")
    print(f"HTML: {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
        )
        page = browser.new_page(viewport={'width': width, 'height': height})

        page.goto(file_url, wait_until='networkidle')

        # Wait for fonts and initial render
        page.wait_for_timeout(1000)

        # Start recording in frame-by-frame mode
        # The HTML exposes window.setVideoFrame(n) to control animation
        rec_start = time.time()

        for i in range(total_frames):
            # Tell HTML which frame we're on (0-based)
            page.evaluate(f'window.setVideoFrame && window.setVideoFrame({i})')
            page.wait_for_timeout(16)  # ~1 frame for render to settle

            frame_path = os.path.join(args.output, f"frame_{i+1:04d}.png")
            page.screenshot(path=frame_path, type='png')

            if (i + 1) % 30 == 0:
                pct = ((i + 1) / total_frames) * 100
                print(f"  Frame {i+1}/{total_frames} ({pct:.0f}%)")

        browser.close()

    elapsed = time.time() - rec_start
    print(f"Done! {total_frames} frames in {elapsed:.1f}s ({total_frames/elapsed:.1f} fps)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Record HTML animation to PNG frames')
    parser.add_argument('--input', required=True, help='Path to HTML file')
    parser.add_argument('--output', required=True, help='Output directory for frames')
    parser.add_argument('--duration', type=int, default=10, help='Duration in seconds')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], default='portrait')

    args = parser.parse_args()
    record(args)
