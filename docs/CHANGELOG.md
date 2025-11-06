# Changelog

All notable changes to PageMaster will be documented in this file.

## [0.0.1] - 2025-11-06

### Added
- **Initial Release**
- Extract CBZ files with automatic image extraction
- Organize chapters by volume with intelligent grouping
- Support for decimal chapter numbers (e.g., Chapter 14.5)
- Create new CBZ files from organized chapters
- Interactive menu-driven interface
- Configuration management with persistent config.json
- Multi-archive support (process multiple manga in one session)
- Auto-volume calculation when metadata is missing
- Fallback handling for unmatched images
- Error handling for corrupted CBZ files
- Support for JPG, PNG, and WebP image formats

### Features
- **main.py** - Central hub with interactive menu
- **extract_cbz.py** - Extract images from CBZ archives
- **organize_chapters.py** - Organize chapters by volume
- **create_cbz.py** - Generate CBZ files from organized chapters
- **config.json** - Persistent configuration storage

### Documentation
- README.md - Project overview and quick start guide
- CHANGELOG.md - Version history (this file)
- DOCS.md - Detailed technical documentation

## [Unreleased]

### Planned Features
- Batch processing with progress bar
- Support for RAR and 7Z archives
- Web interface for easier configuration
- Automatic metadata fetching from online sources
- Duplicate detection and handling
- Custom chapter naming patterns
- Merge multiple volumes into single CBZ
- Split large chapters into multiple files
- Image quality optimization
- Metadata editing interface

### Improvements
- Performance optimization for large archives
- Better error messages and logging
- Unit tests and integration tests
- Command-line arguments for non-interactive mode
- Support for custom image sorting within chapters
