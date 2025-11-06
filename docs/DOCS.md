# PageMaster - Technical Documentation

Comprehensive documentation for developers and advanced users.

## Table of Contents

1. [Architecture](#architecture)
2. [File Structure](#file-structure)
3. [Module Reference](#module-reference)
4. [Configuration](#configuration)
5. [Data Formats](#data-formats)
6. [Workflow Details](#workflow-details)
7. [Error Handling](#error-handling)
8. [Advanced Usage](#advanced-usage)

## Architecture

MangaSort follows a modular pipeline architecture:

```
┌─────────────┐
│  main.py    │ (Menu & Config)
└──────┬──────┘
       │
       ├─→ extract_cbz.py (Extract images from CBZ)
       │
       ├─→ organize_chapters.py (Organize by volume/chapter)
       │
       └─→ create_cbz.py (Create new CBZ files)
```

Each module is independent and can be imported separately for custom workflows.

## File Structure

### Directory Layout

```
MangaSort/
├── main.py                    # Entry point and menu
├── extract_cbz.py             # CBZ extraction logic
├── organize_chapters.py       # Chapter organization logic
├── create_cbz.py              # CBZ creation logic
├── config.json                # Configuration (auto-generated)
├── README.md                  # User guide
├── CHANGELOG.md               # Version history
├── DOCS.md                    # This file
├── extracted/                 # Extracted images (default)
├── organized/                 # Organized chapters (default)
└── manga/                     # Source CBZ files (default)
```

### Runtime Directories

**extracted/** - Contains extracted images
```
extracted/
└── Manga_Title/
    ├── 00000000_00010000.jpg
    ├── 00000000_00020000.jpg
    └── index.json
```

**organized/** - Contains organized chapters
```
organized/
└── Manga_Title/
    ├── Volume 1/
    │   ├── Chapter 1/
    │   │   ├── image1.jpg
    │   │   └── image2.jpg
    │   └── Chapter 2/
    └── cbz_output/
        └── Manga_Title/
            └── Volume 1/
                ├── Chapter 1.cbz
                └── Chapter 2.cbz
```

## Module Reference

### main.py

**Purpose:** Central hub for configuration and menu navigation

**Key Functions:**

- `load_config()` - Load configuration from config.json
- `save_config(config)` - Save configuration to config.json
- `setup_config()` - Interactive configuration wizard
- `display_menu(config)` - Show main menu
- `run_extract_cbz(config)` - Launch extract_cbz module
- `run_organize_chapters(config)` - Launch organize_chapters module
- `run_create_cbz(config)` - Launch create_cbz module
- `main()` - Main loop

**Configuration Keys:**
- `SOURCE_DIR` - Directory containing CBZ files
- `EXTRACT_DIR` - Directory for extracted images
- `OUTPUT_DIR` - Directory for organized chapters

### extract_cbz.py

**Purpose:** Extract images from CBZ archives

**Key Function:**

```python
def run(config):
    """Extract CBZ files using provided configuration"""
```

**Process:**
1. Validates SOURCE_DIR exists and is a directory
2. Lists all .cbz files in SOURCE_DIR
3. For each CBZ file:
   - Creates subdirectory in EXTRACT_DIR with archive name
   - Extracts all files to that directory
   - Skips if already extracted
4. Handles corrupted files gracefully

**Error Handling:**
- `BadZipFile` - Corrupted CBZ files are skipped
- `FileNotFoundError` - Missing SOURCE_DIR is reported
- `NotADirectoryError` - File path instead of directory is reported

### organize_chapters.py

**Purpose:** Organize extracted images by volume and chapter

**Key Function:**

```python
def run(config):
    """Organize chapters using provided configuration"""
```

**Process:**
1. Finds all subdirectories in EXTRACT_DIR
2. For each archive:
   - Loads index.json metadata
   - Groups chapters by volume
   - Sorts chapters by number
   - Creates volume/chapter directory structure
   - Moves images to corresponding chapter folders
   - Handles unmatched images (→ Volume 1, Chapter 1)

**Volume Calculation:**
- If all chapters have `volume: 0`, auto-calculates volumes
- Formula: `volume = (chapter_number - 1) // 10 + 1`
- Results in ~10 chapters per volume

**Chapter Naming:**
- Extracts chapter number from JSON `name` field
- Supports decimal chapters (14.5, 14.6, etc.)
- Format: `Chapter X` or `Chapter X.Y`
- Falls back to sequential number if name not found

**Image Matching:**
- Uses regex patterns from JSON `entries` field
- Matches against image filename (without extension)
- Unmatched images go to Volume 1, Chapter 1

### create_cbz.py

**Purpose:** Create CBZ archives from organized chapters

**Key Function:**

```python
def run(config):
    """Create CBZ files using provided configuration"""
```

**Process:**
1. Finds organized archive in OUTPUT_DIR
2. Walks through volume and chapter structure
3. For each chapter:
   - Collects all image files (.jpg, .png, .webp)
   - Creates CBZ file with chapter name
   - Stores in `cbz_output/Manga_Title/Volume X/`
4. Skips empty chapters

**Output Structure:**
```
OUTPUT_DIR/
└── Manga_Title/
    └── cbz_output/
        └── Manga_Title/
            ├── Volume 1/
            │   ├── Chapter 1.cbz
            │   └── Chapter 2.cbz
            └── Volume 2/
                └── Chapter 3.cbz
```

## Configuration

### config.json Format

```json
{
  "SOURCE_DIR": "path/to/cbz/files",
  "EXTRACT_DIR": "path/to/extracted",
  "OUTPUT_DIR": "path/to/organized"
}
```

### Path Types

- **Absolute paths** - `/home/user/manga` (recommended)
- **Relative paths** - `./manga` (relative to script location)
- **Home directory** - `~/manga` (not expanded, use absolute)

### Modifying Configuration

**Option 1: Interactive Menu**
```bash
python main.py
# Select option 4: Reconfigure paths
```

**Option 2: Direct Edit**
```bash
# Edit config.json directly
nano config.json
```

**Option 3: Programmatic**
```python
import json

config = {
    "SOURCE_DIR": "manga",
    "EXTRACT_DIR": "extracted",
    "OUTPUT_DIR": "organized"
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
```

## Data Formats

### index.json Structure

Generated by manga reader, contains chapter metadata:

```json
{
  "id": -92268805245372035,
  "title": "Manga Title",
  "author": "Author Name",
  "chapters": {
    "chapter_id_1": {
      "number": 1,
      "volume": 0,
      "name": "Ch. 1 - Chapter Name",
      "entries": "00000000_0001\\d{4}",
      "url": "/manga/url/",
      "uploadDate": 1744059600000
    },
    "chapter_id_2": {
      "number": 2,
      "volume": 0,
      "name": "Ch. 2 - Chapter Name",
      "entries": "00000000_0002\\d{4}",
      "url": "/manga/url/",
      "uploadDate": 1744059600000
    }
  }
}
```

### Key Fields

- **number** - Sequential chapter number (1, 2, 3, ...)
- **volume** - Volume number (0 if not specified)
- **name** - Display name (e.g., "Ch. 14.5 - Name")
- **entries** - Regex pattern for matching image filenames
- **url** - Source URL
- **uploadDate** - Timestamp in milliseconds

### Regex Pattern Examples

- `00000000_0001\\d{4}` - Matches `00000000_00010000.jpg`
- `00000000_0014\\d{4}` - Matches `00000000_00140000.jpg`
- `00000000_0014_5\\d{2}` - Matches `00000000_0014_50000.jpg` (for 14.5)

## Workflow Details

### Complete Workflow Example

**Step 1: Extract**
```bash
$ python main.py
# Select option 1: Extract CBZ files

🔄 Running extract_cbz.py...
Extracting One_Piece.cbz → extracted/One_Piece
✅ Extraction complete.
```

Result:
```
extracted/One_Piece/
├── 00000000_00010000.jpg
├── 00000000_00020000.jpg
└── index.json
```

**Step 2: Organize**
```bash
$ python main.py
# Select option 2: Organize chapters

🔄 Running organize_chapters.py...
Found 1 archive(s) to organize

📚 Organizing One_Piece...
ℹ️  Auto-calculating volumes (148 chapters found)...
  Moved 20 images → organized/One_Piece/Volume 1/Chapter 1
  Moved 20 images → organized/One_Piece/Volume 1/Chapter 2
  ...
✅ One_Piece organized.
```

Result:
```
organized/One_Piece/
├── Volume 1/
│   ├── Chapter 1/
│   │   ├── 00000000_00010000.jpg
│   │   └── ...
│   └── Chapter 2/
└── Volume 2/
```

**Step 3: Create CBZ**
```bash
$ python main.py
# Select option 3: Create CBZ files

🔄 Running create_cbz.py...
Creating organized/One_Piece/cbz_output/One_Piece/Volume 1/Chapter 1.cbz
Creating organized/One_Piece/cbz_output/One_Piece/Volume 1/Chapter 2.cbz
...
✅ CBZ creation complete.
```

Result:
```
organized/One_Piece/cbz_output/One_Piece/
├── Volume 1/
│   ├── Chapter 1.cbz
│   └── Chapter 2.cbz
└── Volume 2/
```

## Error Handling

### Common Errors and Solutions

**BadZipFile: Bad CRC-32**
- **Cause:** Corrupted CBZ file
- **Solution:** Re-download the file or verify integrity
- **Behavior:** File is skipped, processing continues

**FileNotFoundError: [Errno 2] No such file or directory**
- **Cause:** SOURCE_DIR/EXTRACT_DIR/OUTPUT_DIR doesn't exist
- **Solution:** Create the directory or update config.json
- **Behavior:** Script reports error and exits

**NotADirectoryError: [Errno 20] Not a directory**
- **Cause:** Path points to a file instead of directory
- **Solution:** Update config to point to correct directory
- **Behavior:** Script reports error and exits

**JSON file not found**
- **Cause:** Extracted folder missing index.json
- **Solution:** Verify extraction completed successfully
- **Behavior:** Archive is skipped, processing continues

**No CBZ files found**
- **Cause:** SOURCE_DIR is empty or has no .cbz files
- **Solution:** Add CBZ files to SOURCE_DIR
- **Behavior:** Script reports warning and exits

### Error Recovery

The scripts are designed to be resilient:

1. **Corrupted files** - Skipped automatically, processing continues
2. **Missing metadata** - Falls back to sequential numbering
3. **Unmatched images** - Placed in Volume 1, Chapter 1
4. **Empty chapters** - Skipped during CBZ creation

## Advanced Usage

### Custom Workflows

**Import as Module:**
```python
import extract_cbz
import organize_chapters
import create_cbz

config = {
    "SOURCE_DIR": "manga",
    "EXTRACT_DIR": "extracted",
    "OUTPUT_DIR": "organized"
}

# Run extraction
extract_cbz.run(config)

# Run organization
organize_chapters.run(config)

# Run CBZ creation
create_cbz.run(config)
```

### Batch Processing

```python
import os
import json
from extract_cbz import run as extract
from organize_chapters import run as organize
from create_cbz import run as create_cbz_files

config = {
    "SOURCE_DIR": "manga",
    "EXTRACT_DIR": "extracted",
    "OUTPUT_DIR": "organized"
}

# Process all manga
for manga in os.listdir(config["SOURCE_DIR"]):
    if manga.lower().endswith(".cbz"):
        print(f"Processing {manga}...")
        extract(config)
        organize(config)
        create_cbz_files(config)
```

### Modifying Volume Calculation

Edit `organize_chapters.py` line 51:
```python
chapters_per_volume = 10  # Change this value
```

Common values:
- `10` - Standard (default)
- `12` - Typical manga volume
- `20` - Larger volumes

### Custom Chapter Naming

Edit `organize_chapters.py` line 58:
```python
# Current format
ch_name = f"Chapter {ch_num}"

# Custom format examples
ch_name = f"Ch {ch_num}"  # Shorter
ch_name = f"{ch_num:03d}"  # Zero-padded
ch_name = f"Ch. {ch_num:05.1f}"  # Formatted
```

## Performance Considerations

### Memory Usage
- Minimal memory footprint
- Processes one file at a time
- Suitable for large archives

### Disk Space
- Requires space for: extracted + organized + cbz_output
- Estimate: 3x the original CBZ size
- Example: 500MB CBZ → ~1.5GB total

### Processing Speed
- Extraction: ~50-100 MB/s (depends on disk speed)
- Organization: ~1000 files/s
- CBZ creation: ~50-100 MB/s

### Optimization Tips
- Use SSD for faster processing
- Organize before creating CBZ (saves time)
- Process one manga at a time
- Close other applications to free memory

## Troubleshooting Guide

### Issue: Script hangs on large files

**Solution:**
- Check disk space availability
- Monitor system resources
- Try processing smaller files first

### Issue: Images in wrong chapter

**Possible Causes:**
- Regex pattern doesn't match filename
- Image filename format unexpected
- JSON metadata incorrect

**Solution:**
- Check image filenames in extracted folder
- Verify regex patterns in index.json
- Manually move images if needed

### Issue: Missing chapters

**Possible Causes:**
- Chapter metadata missing from JSON
- Images don't match regex patterns
- Corrupted extraction

**Solution:**
- Check index.json for all chapters
- Verify image filenames
- Re-extract the CBZ file

### Issue: CBZ files won't open

**Possible Causes:**
- Corrupted images in archive
- Invalid ZIP structure
- Unsupported image format

**Solution:**
- Verify images in chapter folder
- Try opening with different reader
- Check image file integrity

## Support & Debugging

### Enable Verbose Output

Add to any script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check File Integrity

```bash
# Verify CBZ file
unzip -t manga.cbz

# List CBZ contents
unzip -l manga.cbz

# Check extracted images
ls -lh extracted/Manga_Title/
```

### Validate JSON

```bash
python -m json.tool extracted/Manga_Title/index.json
```

## Contributing

To contribute improvements:

1. Test changes thoroughly
2. Maintain backward compatibility
3. Update documentation
4. Follow existing code style
5. Add error handling for edge cases

## License

This project is open source and available for personal use.
