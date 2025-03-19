from pathlib import Path
import subprocess
import os

def build_exe():
    build_command = [
        "python", "-m", "nuitka",
        "--mingw64",
        "--follow-imports",
        "--windows-disable-console",
        "--standalone",
        "--enable-plugin=tk-inter",
        "--include-data-dir=assets=assets",
        "--windows-icon-from-ico=assets/Fetdy.ico",
        "--output-dir=build",
        "--show-memory",
        "--show-progress",
        # Exclude problematic modules
        "--nofollow-import-to=numpy,PIL,yt_dlp.extractor.lazy_extractors",
        "--nofollow-import-to=yt_dlp.extractor._extractors",
        # Performance optimizations
        "--low-memory",
        "--disable-console",
        "--assume-yes-for-downloads",
        "--windows-company-name=Fetdy",
        "--windows-product-name=Fetdy",
        "--windows-file-version=1.0.0",
        "--jobs=4",
        "--remove-output",  # Clean previous builds
        "main.py"
    ]
    
    subprocess.run(build_command)

if __name__ == "__main__":
    build_exe()