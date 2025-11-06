# PageMaster

A powerful Python tool for extracting, organizing, and converting manga CBZ files into a well-structured library with automatic volume and chapter management.

## Features

- **Extract CBZ Files** - Automatically extract images from CBZ archives
- **Organize by Volume & Chapter** - Intelligently organize chapters into volumes with proper naming
- **Handle Decimal Chapters** - Support for chapters like 14.5, 14.6, etc.
- **Create CBZ Archives** - Generate new CBZ files from organized chapters
- **Auto-Volume Calculation** - Automatically calculate volumes when metadata is missing
- **Fallback Image Handling** - Unmatched images automatically go to Volume 1, Chapter 1
- **Multi-Archive Support** - Process multiple manga archives in one session
- **Interactive Menu** - User-friendly command-line interface
- **Persistent Configuration** - Save and reuse your directory paths

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. No external dependencies required (uses only Python standard library)

```bash
git clone https://github.com/yourusername/PageMaster.git
cd PageMaster
python main.py
```

## Quick Start

```bash
python main.py
```

On first run, you'll be prompted to configure:
- **SOURCE_DIR** - Directory containing your CBZ files
- **EXTRACT_DIR** - Where extracted images will be stored
- **OUTPUT_DIR** - Where organized chapters will be stored

## Project Structure

```
PageMaster/
├── main.py                 # Main menu and configuration
├── extract_cbz.py          # CBZ extraction script
├── organize_chapters.py    # Chapter organization script
├── create_cbz.py          # CBZ creation script
├── config.json            # Configuration file (auto-generated)
├── README.md              # This file
├── CHANGELOG.md           # Version history
└── DOCS.md               # Detailed documentation
```

## Workflow

### Step 1: Extract CBZ Files
```
SOURCE_DIR/
└── Manga_Title.cbz
        ↓
EXTRACT_DIR/
└── Manga_Title/
    ├── 00000000_00010000.jpg
    ├── 00000000_00020000.jpg
    └── index.json
```

### Step 2: Organize Chapters
```
EXTRACT_DIR/
└── Manga_Title/
        ↓
OUTPUT_DIR/
└── Manga_Title/
    ├── Volume 1/
    │   ├── Chapter 1/
    │   ├── Chapter 2/
    │   └── Chapter 3/
    └── Volume 2/
        ├── Chapter 4/
        └── Chapter 5/
```

### Step 3: Create CBZ Files
```
OUTPUT_DIR/
└── Manga_Title/
        ↓
OUTPUT_DIR/
└── Manga_Title/
    └── cbz_output/
        └── Manga_Title/
            ├── Volume 1/
            │   ├── Chapter 1.cbz
            │   ├── Chapter 2.cbz
            │   └── Chapter 3.cbz
            └── Volume 2/
                ├── Chapter 4.cbz
                └── Chapter 5.cbz
```

## Configuration

The `config.json` file stores your directory paths:

```json
{
  "SOURCE_DIR": "manga",
  "EXTRACT_DIR": "extracted",
  "OUTPUT_DIR": "organized"
}
```

You can edit this file directly or use the "Reconfigure paths" option in the main menu.

## Usage

### Main Menu Options

1. **Extract CBZ files** - Extract images from all CBZ files in SOURCE_DIR
2. **Organize chapters** - Organize extracted images by volume and chapter
3. **Create CBZ files** - Generate new CBZ files from organized chapters
4. **Reconfigure paths** - Update directory paths
5. **Exit** - Close the application

### Example Session

```
$ python main.py

==================================================
MANGA SORT - Main Menu
==================================================

Current Configuration:
  SOURCE_DIR:  manga
  EXTRACT_DIR: extracted
  OUTPUT_DIR:  organized

Options:
  1. Extract CBZ files
  2. Organize chapters
  3. Create CBZ files
  4. Reconfigure paths
  5. Exit
--------------------------------------------------
Enter your choice (1-5): 1

🔄 Running extract_cbz.py...
Extracting One_Piece_Vol1.cbz → extracted/One_Piece_Vol1
✅ Extraction complete.
```

## Supported Image Formats

- JPG / JPEG
- PNG
- WebP

## Supported Archive Formats

- CBZ (Comic Book Zip)

## Features in Detail

### Auto-Volume Calculation
If the JSON metadata doesn't contain volume information, the script automatically calculates volumes based on chapter count (default: 10 chapters per volume).

### Chapter Naming
Chapters are named based on the JSON metadata:
- Regular chapters: `Chapter 1`, `Chapter 2`, etc.
- Decimal chapters: `Chapter 14.5`, `Chapter 14.6`, etc.

### Unmatched Images
Images that don't match any chapter regex pattern are automatically placed in `Volume 1/Chapter 1`.

### Multiple Archives
Process multiple manga archives in sequence. Each archive is organized independently.

## Troubleshooting

### "No CBZ files found"
- Check that SOURCE_DIR is a directory (not a file)
- Verify CBZ files are in the correct location
- Ensure file extensions are lowercase (.cbz)

### "JSON file not found"
- Verify the extracted folder contains an `index.json` file
- Check that extraction completed successfully

### Empty chapter folders
- Images may not match the regex patterns in the JSON
- Check that image filenames match the expected format
- Unmatched images should be in Volume 1, Chapter 1

### Corrupted CBZ files
- The script will skip corrupted files and continue with others
- Try re-downloading the CBZ file
- Verify the file integrity with another tool

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## License

This project is open source and available for personal use.

## Contributing

Feel free to fork, modify, and improve this project!

## Support

For issues or questions, please check the DOCS.md file for detailed documentation.

## About PageMaster

PageMaster is designed to streamline your manga library management workflow. Whether you're organizing a single series or managing multiple collections, PageMaster handles the heavy lifting with intelligent chapter detection, automatic volume organization, and clean CBZ archive creation.
