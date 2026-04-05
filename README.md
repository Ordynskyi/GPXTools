# GPX Merger Tool

## Overview
This tool merges extension parameters from one GPX file into another, synchronizing by time. It is useful for combining sensor data (like heart rate or cadence) from one device with GPS data from another.

## Usage
Run the `run_merger.bat` batch file. You will be prompted for:
- Source File Name (default: from.gpx)
- Second File Name (default: to.gpx)
- Output File Name (default: merged.tpx)
- GPX creator attribute value (leave blank to keep original)
- Space separated extension names (e.g. `hr cad`)

Example:
```
run_merger.bat
```

## How it works
- The script synchronizes track points by their `<time>` value.
- For each matching time, it copies the specified extension parameters (e.g., `<gpxtpx:hr>`) from the second file to the first.
- The merged file is saved with the name you provide.
- If you enter a creator value, the output GPX will have its `creator` attribute set to that value.

## Requirements
- Python 3.x
- The `Merger.py` script must be in the same directory.

## Notes
- The tool preserves all other data in the first file and only adds/updates the specified extensions.
- The batch file provides defaults for convenience, but you can enter any file names you wish.
