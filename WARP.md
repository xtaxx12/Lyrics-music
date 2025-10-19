# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a terminal-based music player with synchronized lyrics display and real-time audio visualization. It's a Python application that fetches lyrics from online sources (LRCLIB, NetEase Music) and displays them synchronized with audio playback.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Alternative manual installation
pip install numpy>=1.21.0 sounddevice>=0.4.4 soundfile>=0.10.3 pyfiglet>=0.8.0 requests>=2.25.1
```

### Running the Application
```bash
# Run the music player
python lyrics.py

# The application requires configuring AUDIO_FILE variable in lyrics.py before running
```

### Development Workflow
```bash
# No automated tests or linting configured - manual testing required
# Test by running with different audio files and checking:
# - Lyrics synchronization accuracy
# - Audio visualization quality
# - Online lyrics fetching functionality
```

## Code Architecture

### Core Components

**Main Script (`lyrics.py`)**
- Single-file architecture with all functionality in one module
- Configuration constants at the top (AUDIO_FILE, START_TIME, LYRIC_OFFSET, etc.)
- Modular function design for different responsibilities

### Key Architectural Patterns

**Lyrics Pipeline:**
1. **Parsing**: Extract artist/title from filename (`Artist - Title.mp3` format)
2. **Fetching**: Multi-source lyrics retrieval (LRCLIB → NetEase → Local files)
3. **Processing**: LRC format parsing with time synchronization
4. **Rendering**: Real-time display with visual effects

**Audio Processing:**
- Uses NumPy for audio data manipulation and visualization
- SoundDevice/SoundFile for audio I/O
- Real-time callback-based audio processing with visualization

**Visual System:**
- Terminal-based UI with ANSI color codes and positioning
- HSV color space for dynamic color transitions
- Multi-layer text rendering (previous/current/next lyrics)
- Audio level visualization with sparkle effects

### Configuration System

**Runtime Configuration** (modify in `lyrics.py`):
- `AUDIO_FILE`: Target MP3 file path
- `START_TIME`: Playback start position (seconds)
- `LYRIC_OFFSET`: Sync adjustment for lyrics timing
- `LRC_FOLDER`: Local lyrics cache directory

**Important Constants:**
- `BLOCKSIZE = 2048`: Audio processing chunk size
- Terminal width auto-detection with fallback to 80 columns
- 6-row audio visualizer height

### External Dependencies

**Lyrics Sources:**
- LRCLIB API (primary): `https://lrclib.net/api/search`
- NetEase Music API (fallback): `https://music.163.com/api/`
- Local LRC files in `~/lyrics` directory

**Critical Functions:**
- `fetch_lrc_from_lrclib()` / `fetch_lrc_from_netease()`: Online lyrics retrieval
- `parse_lrc()`: LRC format parsing with time offset application
- `callback()`: Real-time audio processing and display rendering
- `render_lyrics_block()`: Multi-line lyrics display with effects

### File Naming Conventions

**Audio Files**: Use `Artist - Title.mp3` format for automatic metadata extraction
**Local Lyrics**: Store as `Song Title.lrc` in `~/lyrics` directory for local matching

### Development Notes

- No automated testing framework - requires manual validation
- Single-threaded design with callback-based audio processing
- Heavy use of global variables for state management
- Windows PowerShell environment compatibility (based on file paths)
- No build system - direct Python script execution