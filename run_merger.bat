@echo off
setlocal enabledelayedexpansion

REM Load defaults from template if it exists
if exist merger_template.txt (
    for /f "usebackq tokens=1,2 delims==" %%A in (merger_template.txt) do (
        set "%%A=%%B"
    )
) else (
    set "FROM=from.gpx"
    set "TO=to.gpx"
    set "OUTPUT=merged.gpx"
    set "CREATOR="
    set "PARAMS=hr"
)

set /p INPUT_FROM="Enter FROM file (source of extensions) [default: !FROM!]: "
if not "!INPUT_FROM!"=="" set "FROM=!INPUT_FROM!"
set /p INPUT_TO="Enter TO file (base geometry/track) [default: !TO!]: "
if not "!INPUT_TO!"=="" set "TO=!INPUT_TO!"
set /p INPUT_OUTPUT="Enter Output File Name with extension [default: !OUTPUT!]: "
if not "!INPUT_OUTPUT!"=="" set "OUTPUT=!INPUT_OUTPUT!"
set /p INPUT_CREATOR="Enter GPX creator attribute value [default: (!CREATOR!)]: "
if not "!INPUT_CREATOR!"=="" set "CREATOR=!INPUT_CREATOR!"
set /p INPUT_PARAMS="Enter space separated extension names (e.g. hr cad) [default: !PARAMS!]: "
if not "!INPUT_PARAMS!"=="" set "PARAMS=!INPUT_PARAMS!"

REM Call the Python merger script
if not "!CREATOR!"=="" (
    python Merger.py "!FROM!" "!TO!" "!OUTPUT!" !PARAMS! --creator "!CREATOR!"
) else (
    python Merger.py "!FROM!" "!TO!" "!OUTPUT!" !PARAMS!
)

echo Merge complete. Output written to !OUTPUT!
pause
