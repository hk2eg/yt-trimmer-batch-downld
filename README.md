# YouTube Batch Downloader GUI

A simple Python/Tkinter application that lets you download multiple YouTube videos (or trimmed clips) in one go. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for fetching and [FFmpeg](https://ffmpeg.org/) for on-the-fly trimming.

## Features
- **Table-based input**: Add/Edit/Delete rows of  
  - **Video URL**  
  - **Start (HH:MM:SS)** (optional)  
  - **End   (HH:MM:SS)** (optional)
- **Full or trimmed download**:  
  - If “Start” & “End” are blank → full video  
  - Otherwise → ffmpeg downloads only that segment
- **Choose output folder** via file dialog
- **Real-time log** shown in the GUI

## Requirements
- Python 3.10+  
- [yt-dlp](https://pypi.org/project/yt-dlp/)  
- [FFmpeg](https://ffmpeg.org/) (in PATH)  
- Tkinter (included with most Python installs;  
  on Conda: `conda install tk`)

## Installation
1. Clone or download this repo.  
2. (Optional) Create & activate a virtual environment:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install yt-dlp
   ```
4. Ensure `ffmpeg` is in your PATH:
   ```bash
   ffmpeg -version
   ```

## Usage
```bash
python yt_batch_downloader.py
```
1. Click **Add Row** to insert a new URL entry.  
2. Double-click the URL, Start, or End cell to edit.  
3. (Optional) Click **Choose Output Dir** to set a save folder (defaults to `./downloads`).  
4. Click **Start Download** to fetch each video or trimmed clip.

## Current State
- Prototype version with basic GUI table and logging.  
- Full‐video download and segment trim via ffmpeg.  
- Tested on standard YouTube videos.

## Future Improvements
- Validate time format (HH:MM:SS).  
- Show per-row progress bars.  
- Save/load URL/trim presets (CSV/JSON).  
- Drag‐and‐drop URL lists.  
- Localize UI (e.g., Arabic).  
- Build standalone executables with PyInstaller.  
- Add unit tests for download/trim logic.

## License
Choose an open‐source license (e.g., MIT, Apache 2.0) by adding a `LICENSE` file.

## Contributing
Issues and pull requests are welcome.
