#!/usr/bin/env python3
"""
HTML to MP4 video converter — fast pipeline using Playwright's native video recording.
Records the browser viewport in real-time, then re-encodes to exact specs.

Usage:
    python3 html2mp4.py input.html output.mp4 [--duration 10] [--fps 30] [--orientation portrait|landscape] [--width 1080] [--height 1920]
"""
import argparse
import os
import subprocess
import sys
import time
import tempfile
import shutil


def convert(input_html, output_mp4, duration=10, fps=30, orientation='portrait', crf=18):
    from playwright.sync_api import sync_playwright

    if orientation == 'portrait':
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    file_url = 'file://' + os.path.abspath(input_html)

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Recording {duration}s {orientation} video ({width}x{height})...")

        with sync_playwright() as p:
            # Use native video recording — records viewport in real-time
            browser = p.chromium.launch(
                args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
            )
            context = browser.new_context(
                viewport={'width': width, 'height': height},
                record_video_dir=tmpdir,
                record_video_size={'width': width, 'height': height},
            )
            page = context.new_page()

            page.goto(file_url, wait_until='networkidle')
            page.wait_for_timeout(500)

            # Start animation via setVideoFrame OR startVideo
            # Frame-based: advance frames in real-time
            has_frame_api = page.evaluate('typeof window.setVideoFrame === "function"')
            has_start_api = page.evaluate('typeof window.startVideo === "function"')

            start = time.time()

            if has_frame_api:
                # Frame-by-frame in real-time at target fps
                total_frames = duration * fps
                frame_interval = 1.0 / fps  # seconds per frame

                for i in range(total_frames):
                    target_time = start + (i + 1) * frame_interval
                    page.evaluate(f'window.setVideoFrame({i})')

                    # Sleep to maintain real-time pace
                    now = time.time()
                    sleep_time = target_time - now
                    if sleep_time > 0:
                        time.sleep(sleep_time)

                    if (i + 1) % (fps * 2) == 0:
                        pct = ((i + 1) / total_frames) * 100
                        print(f"  Frame {i+1}/{total_frames} ({pct:.0f}%)")

            elif has_start_api:
                page.evaluate('window.startVideo()')
                time.sleep(duration)
            else:
                # No API — just wait for CSS/JS animations to play
                time.sleep(duration)

            elapsed = time.time() - start

            # Close context to flush video
            video_path = page.video.path()
            page.close()
            context.close()
            browser.close()

        print(f"Recorded in {elapsed:.1f}s (real-time)")

        # Get raw video info
        probe = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', video_path],
            capture_output=True, text=True
        )
        print(f"Raw video: {video_path}")

        # Re-encode to exact specs: H.264, correct resolution, yuv420p
        print(f"Encoding to H.264 MP4 (CRF {crf})...")
        result = subprocess.run([
            'ffmpeg', '-y',
            '-i', video_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', str(crf),
            '-pix_fmt', 'yuv420p',
            '-r', str(fps),
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black',
            '-movflags', '+faststart',
            '-an',
            output_mp4
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr[-500:]}")
            sys.exit(1)

        size = os.path.getsize(output_mp4)
        print(f"Done! {output_mp4} ({size/1024:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(description='Convert HTML animation to MP4 video')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('output', help='Output MP4 file')
    parser.add_argument('--duration', type=int, default=10, help='Duration in seconds (default: 10)')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS (default: 30)')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], default='portrait')
    parser.add_argument('--crf', type=int, default=18, help='H.264 CRF quality (default: 18)')
    args = parser.parse_args()
    convert(args.input, args.output, args.duration, args.fps, args.orientation, args.crf)


if __name__ == '__main__':
    main()
