# Sound File Splitter Service

A CLI-assisted tool for audio file segmentation: parses METS XML metadata to extract timecode ranges and splits corresponding MP4 audio files into individual tracks with structured file naming and CSV output for reference.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Core Workflow](#2-core-workflow)
3. [Architecture](#3-architecture)
4. [Environment & Dependencies](#4-environment--dependencies)
5. [Setup](#5-setup)
6. [Usage](#6-usage)
7. [File & Naming Conventions](#7-file--naming-conventions)
8. [Output Files](#8-output-files)
9. [Service Limitations](#9-service-limitations)

---

## 1. Overview

The Sound File Splitter Service automates the process of segmenting audio files based on metadata contained in METS XML files. The service:

- Extracts timecode ranges from METS XML files for audio segmentation
- Splits MP4 audio files using SMPTE25 timecode data
- Generates structured filenames using shelfmark and title information
- Produces CSV reports of processed timecode ranges
- Validates data integrity before processing

---

## 2. Core Workflow

### 2.1 Audio File Splitting Process

Steps:
1. User launches service and selects directory containing METS XML and MP4 files
2. Service scans for matching XML and audio file pairs
3. METS XML files are parsed to extract:
   - Original file references and IDs
   - Recorded area timecode ranges (BEGIN/END)
   - Record titles and physical identifiers
   - Structural link mappings
4. Data validation ensures all required fields are present
5. Audio files are split using FFmpeg with SMPTE25 timecode conversion
6. Output files are renamed using "Shelfmark, Title.mp4" convention
7. CSV files are generated for each processed XML containing timecode data
8. Split files are saved to `_split_files_ranges/` subdirectory
9. Summary of processing results and any errors are displayed

---

## 3. Architecture

| Module | Responsibility |
|--------|----------------|
| `main.py` | Orchestrates the splitting workflow & user interface |
| `xml_parser.py` | METS XML parsing and data extraction |
| `file_splitter.py` | Audio splitting operations using FFmpeg |
| `csv_writer.py` | CSV report generation |
| `file_service.py` | File discovery and validation operations |
| `datamodels.py` | Data structures for audio file objects and metadata |
| `service_messages.py` | User interface messages and prompts |

External dependencies: `ffmpeg` (must be on PATH for audio processing).

---

## 4. Environment & Dependencies

**Python:** See `requirements.txt` for required packages.

**External executables must be on PATH:**
- `ffmpeg` (for audio file splitting operations)

**Key Python dependencies:**
- `rich` - Console formatting and user interface
- `tqdm` - Progress bars during processing
- Standard library: `xml.etree.ElementTree`, `tkinter`, `subprocess`

---

## 5. Setup

```bash
git clone https://github.com/British-Library-Technical-Services/sound-file-splitter.git
cd sound-file-splitter
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Install FFmpeg:**
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html and add to PATH

---

## 6. Usage

Run the interactive service:

```bash
python main.py
```

**Interactive Process:**
1. Press Enter at the welcome screen
2. Select source directory containing METS XML and MP4 files via file dialog
3. Review file counts and press any key to continue
4. Monitor processing progress via progress bar
5. Review results and any error notifications

**File Dialog:** The service will open a system file dialog to select the source directory. Ensure this directory contains both the METS XML files and their corresponding MP4 audio files.

---

## 7. File & Naming Conventions

| Item | Convention |
|------|------------|
| Input XML files | METS XML format with `mediaMD` namespace |
| Input audio files | MP4 format with matching filenames (minus extension) |
| Output audio files | `<Shelfmark>, <Title>.mp4` |
| Output CSV files | `<original_xml_filename>.csv` |
| Output directory | `_split_files_ranges/` (created in source directory) |
| Timecode format | SMPTE25 (25 fps) converted to `hh:mm:ss.ms` |

**Filename Matching:** Audio files should have the same base name as referenced in the METS XML `mediaMD:fileName` elements, with `.mp4` extension instead of `.wav`.

**Shelfmark Parsing:** Extracted from record title using pattern: `"Call Number: Title"` where call number becomes the shelfmark with `/` and spaces converted to `_`.

---

## 8. Output Files

### 8.1 Split Audio Files
- **Location:** `<source_directory>/_split_files_ranges/`
- **Format:** MP4 (copied without re-encoding for quality preservation)
- **Naming:** `<Shelfmark>, <Title>.mp4`
- **Content:** Audio segments based on METS timecode ranges

### 8.2 CSV Reports
- **Location:** Same directory as source XML files
- **Naming:** `<original_xml_file>.csv`
- **Content:** Tabular data with columns:
  - `filename` - Original audio filename
  - `file_id` - METS file identifier
  - `physical_id` - Physical structure identifier
  - `timecode_in` - Start timecode (SMPTE25)
  - `timecode_out` - End timecode (SMPTE25)
  - `record_title` - Extracted record title

---

## 9. Service Limitations

**Current Constraints:**
- Only processes recordings with simple Parent/Child timecode mappings to single files
- Complex logical structures with multiple file associations are not supported
- Requires METS XML files to follow specific namespace conventions (`mets` and `mediaMD`)
- Audio files must be in MP4 format (WAV references in XML are converted to MP4 for processing)


Files that cannot be processed will be skipped and listed in the final error report for manual review.
