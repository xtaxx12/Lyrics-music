import os, sys, re, shutil, difflib, tempfile, requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import pyfiglet

AUDIO_FILE   = "Wham! - Last Christmas.mp3" #nombre de la cancion
START_TIME   = 232
BLOCKSIZE    = 2048


LYRIC_OFFSET = -1.7


def fetch_lrc_from_lrclib(title: str, artist: str = "") -> str | None:
    try:
        r = requests.get(
            "https://lrclib.net/api/search",
            params={"q": f"{title} {artist}".strip()},
            timeout=10,
        )
        r.raise_for_status()
        for item in r.json():
            if item.get("syncedLyrics"):
                return item["syncedLyrics"]
    except Exception as e:
        print("LRCLIB fetch failed:", e)
    return None

def fetch_lrc_from_netease(title: str, artist: str = "") -> str | None:
    """Fetch lyrics from NetEase Music API"""
    try:
        search_url = "https://music.163.com/api/search/get/web"
        search_params = {
            "s": f"{title} {artist}".strip(),
            "type": 1,
            "offset": 0,
            "total": True,
            "limit": 10
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        r = requests.get(search_url, params=search_params, headers=headers, timeout=10)
        r.raise_for_status()
        
        data = r.json()
        if data.get("result", {}).get("songs"):
            song_id = data["result"]["songs"][0]["id"]
            
            lyric_url = f"https://music.163.com/api/song/lyric"
            lyric_params = {"id": song_id, "lv": 1, "tv": 1}
            
            r2 = requests.get(lyric_url, params=lyric_params, headers=headers, timeout=10)
            r2.raise_for_status()
            
            lyric_data = r2.json()
            if lyric_data.get("lrc", {}).get("lyric"):
                return lyric_data["lrc"]["lyric"]
                
    except Exception as e:
        print("NetEase fetch failed:", e)
    return None

def find_closest_lrc(song_title: str, folder: str) -> str | None:
    if not os.path.isdir(folder):
        return None
    bases = [os.path.splitext(f)[0] for f in os.listdir(folder)
             if f.lower().endswith(".lrc")]
    closest = difflib.get_close_matches(song_title, bases, n=1, cutoff=0.4)
    return os.path.join(folder, closest[0] + ".lrc") if closest else None

def parse_lrc(path: str):
    pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                mins, secs, txt = m.groups()
                t = int(mins)*60 + float(secs) + LYRIC_OFFSET
                out.append((max(0.0, t), txt.strip()))
    return sorted(out)

base = os.path.splitext(os.path.basename(AUDIO_FILE))[0]
artist_guess, title_guess = ("", base)
if "-" in base:
    artist_guess, title_guess = [x.strip() for x in base.split("-", 1)]

lyrics_path = None
lrc_text = None


# Try LRCLIB first
lrc_text = fetch_lrc_from_lrclib(title_guess, artist_guess)
if lrc_text:
    print("✓ Found lyrics on LRCLIB")
else:
    print("✗ LRCLIB: No lyrics found")
    
    # Try NetEase as backup
    lrc_text = fetch_lrc_from_netease(title_guess, artist_guess)
    if lrc_text:
        print("✓ Found lyrics on NetEase Music")
    else:
        print("✗ NetEase: No lyrics found")

if lrc_text:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".lrc")
    tmp.write(lrc_text.encode("utf-8")); tmp.close()
    lyrics_path = tmp.name
    print("Synced lyrics loaded successfully!")
else:
    # Try local files as last resort
    match = find_closest_lrc(title_guess, LRC_FOLDER)
    if match:
        lyrics_path = match
        print(f"Using closest local match: {match}")
    else:
        print("No lyrics found online or locally.")
        print("Try:")
        print("1. Check the song name format")
        print("2. Download .lrc file manually to ~/lyrics folder")
        print("3. Adjust AUDIO_FILE name to match online databases")

lyrics = parse_lrc(lyrics_path) if lyrics_path else []

data, samplerate = sf.read(AUDIO_FILE, dtype="float32")
if data.ndim > 1:
    data = np.mean(data, axis=1)
data = data / np.max(np.abs(data))
start_idx = int(START_TIME * samplerate)

# No need for visualizer variables anymore
lyric_index = 0
for i, (t, _) in enumerate(lyrics):
    if t >= START_TIME:
        lyric_index = max(0, i - 1)
        break



def hsv_to_rgb(h,s,v):
    i = int(h*6); f = h*6 - i
    p = int(255*v*(1-s)); q = int(255*v*(1-f*s)); t = int(255*v*(1-(1-f)*s))
    v = int(255*v); i = i % 6
    return [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)][i]

def colorize(text, r,g,b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def dim_color(text, r, g, b, factor=0.4):
    rr = int(r*factor); gg = int(g*factor); bb = int(b*factor)
    return f"\033[38;2;{rr};{gg};{bb}m{text}\033[0m"

def center_text(text, width):
    """Center text within given width"""
    if len(text) >= width:
        return text
    padding = (width - len(text)) // 2
    return " " * padding + text + " " * (width - len(text) - padding)

def add_text_effects(text, effect_type="glow"):
    """Add visual effects to text"""
    if not text.strip():
        return text
    
    if effect_type == "glow":
        return f"✨ {text} ✨"
    elif effect_type == "highlight":
        return text  # Sin símbolos ▶ ◀
    elif effect_type == "box":
        return f"┃ {text} ┃"
    return text

def create_christmas_tree(play_time):
    """Create animated Christmas tree with changing colors"""
    # Christmas colors
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 165, 0),  # Orange
        (255, 255, 255) # White
    ]
    
    # Tree structure with ornament positions marked as 'o'
    tree_pattern = [
        "       ⭐       ",
        "      ooo      ",
        "     ooooo     ",
        "    ooooooo    ",
        "   ooooooooo   ",
        "  ooooooooooo  ",
        " ooooooooooooo ",
        "ooooooooooooooo",
        "      |||      ",
        "      |||      ",
        "      |||      "
    ]
    
    # Animation speed - change colors every 0.5 seconds
    time_factor = int(play_time * 2)
    
    tree_lines = []
    for line in tree_pattern:
        colored_line = ""
        ornament_count = 0
        
        for char in line:
            if char == 'o':
                # Alternate colors for each ornament
                color_index = (ornament_count + time_factor) % len(colors)
                r, g, b = colors[color_index]
                colored_line += f"\033[38;2;{r};{g};{b}m✦\033[0m"
                ornament_count += 1
            elif char == '⭐':
                # Star at top - golden color with sparkle effect
                if time_factor % 2 == 0:
                    colored_line += f"\033[38;2;255;215;0m⭐\033[0m"
                else:
                    colored_line += f"\033[38;2;255;255;255m✨\033[0m"
            elif char == '|':
                # Brown trunk
                colored_line += f"\033[38;2;139;69;19m|\033[0m"
            else:
                colored_line += char
        
        tree_lines.append(colored_line)
    
    return tree_lines





def render_lyrics_block(idx, r, g, b, play_time):
    lines = []
    term_width = min(80, shutil.get_terminal_size().columns)
    
    # Previous line (dimmed)
    if idx > 0:
        prev_text = lyrics[idx-1][1]
        if prev_text.strip():
            centered = center_text(prev_text, term_width)
            lines.append(dim_color(centered, r, g, b, 0.3))
    
    # Current line (bright with effects)
    if idx < len(lyrics):
        current_text = lyrics[idx][1]
        if current_text.strip():
            # Add pulsing effect based on time
            pulse_intensity = 0.8 + 0.2 * abs(np.sin(play_time * 3))
            effect_text = add_text_effects(current_text, "highlight")
            centered = center_text(effect_text, term_width)
            
            # Make current line brighter
            bright_r = min(255, int(r * pulse_intensity))
            bright_g = min(255, int(g * pulse_intensity))
            bright_b = min(255, int(b * pulse_intensity))
            
            lines.append(colorize(centered, bright_r, bright_g, bright_b))
        else:
            lines.append("")
    
    lines.append("")  # Spacing
    
    # Next 2 lines (preview, dimmed)
    for n in range(1, 3):
        if idx + n < len(lyrics):
            next_text = lyrics[idx + n][1]
            if next_text.strip():
                centered = center_text(next_text, term_width)
                lines.append(dim_color(centered, r, g, b, 0.5))
            else:
                lines.append("")
    
    # Add song info at bottom
    if idx == 0:  # Show song info only at start
        lines.append("")
        song_info = f"♪ {title_guess} - {artist_guess} ♪"
        centered_info = center_text(song_info, term_width)
        lines.append(dim_color(centered_info, r, g, b, 0.6))
    
    return "\n".join(lines)

def render_lyrics_with_christmas_tree(idx, r, g, b, play_time):
    """Render lyrics with animated Christmas tree on the left"""
    # Get Christmas tree
    tree_lines = create_christmas_tree(play_time)
    
    # Get lyrics content
    lyrics_content = render_lyrics_block(idx, r, g, b, play_time).split('\n')
    
    # Combine tree and lyrics
    combined_lines = []
    max_lines = max(len(tree_lines), len(lyrics_content))
    
    for i in range(max_lines):
        tree_part = tree_lines[i] if i < len(tree_lines) else " " * 16
        lyric_part = lyrics_content[i] if i < len(lyrics_content) else ""
        
        # Add spacing between tree and lyrics
        spacing = "    "
        combined_line = tree_part + spacing + lyric_part
        combined_lines.append(combined_line)
    
    return "\n".join(combined_lines)





def create_progress_bar(current_time, total_time, width=40):
    """Create a progress bar for the song"""
    if total_time <= 0:
        return ""
    
    progress = min(1.0, current_time / total_time)
    filled = int(progress * width)
    bar = "█" * filled + "░" * (width - filled)
    
    # Format time
    current_min, current_sec = divmod(int(current_time), 60)
    total_min, total_sec = divmod(int(total_time), 60)
    time_str = f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}"
    
    return f"[{bar}] {time_str}"

def callback(outdata, frames, time_info, status):
    global start_idx, lyric_index
    if status: print(status, file=sys.stderr)

    chunk = data[start_idx:start_idx+frames]
    if len(chunk) < frames:
        outdata[:len(chunk),0] = chunk
        outdata[len(chunk):] = 0
        raise sd.CallbackStop
    else:
        outdata[:,0] = chunk

    play_time = start_idx / samplerate
    if lyrics:
        while lyric_index + 1 < len(lyrics) and play_time >= lyrics[lyric_index + 1][0]:
            lyric_index += 1

    # More dynamic color transitions
    hue = (play_time * 0.1) % 1.0  # Smooth color transition
    saturation = 0.7 + 0.3 * np.sin(play_time * 0.5)  # Pulsing saturation
    r,g,b = hsv_to_rgb(hue, saturation, 0.9)

    screen=[]
    
    # Add title at top
    title_text = f"🎵 {title_guess} - {artist_guess} 🎵"
    term_width = min(120, shutil.get_terminal_size().columns)
    centered_title = center_text(title_text, term_width)
    screen.append(colorize(centered_title, r, g, b))
    screen.append("")

    # Progress bar
    total_time = len(data) / samplerate
    progress_bar = create_progress_bar(play_time, total_time)
    centered_progress = center_text(progress_bar, term_width)
    screen.append("")
    screen.append(dim_color(centered_progress, r, g, b, 0.7))

    if lyrics:
        screen.append("")
        
        # Show Christmas tree with lyrics
        screen.append(render_lyrics_with_christmas_tree(lyric_index, r, g, b, play_time))

    sys.stdout.write("\033[H\033[J" + "\n".join(screen))
    sys.stdout.flush()
    start_idx += frames

with sd.OutputStream(channels=1, samplerate=samplerate,
                     callback=callback, blocksize=BLOCKSIZE, latency="low"):
    sd.sleep(int((len(data) - start_idx) / samplerate * 1000))
