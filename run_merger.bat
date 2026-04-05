@echo off
setlocal enabledelayedexpansion

REM Load defaults from template if it exists
if exist merger_template.txt (
    for /f "usebackq tokens=1,2 delims==" %%A in (merger_template.txt) do (
        set "%%A=%%B"
    )
) else (
    set "FILE1=from.gpx"
    set "FILE2=to.gpx"
    set "OUTPUT=merged.gpx"
    set "CREATOR="
    set "PARAMS=hr"
)

set /p FILE1="Enter Source File Name with extension [default: !FILE1!]: "
if "!FILE1!"=="" set FILE1=!FILE1!
set /p FILE2="Enter Second File Name with extension [default: !FILE2!]: "
if "!FILE2!"=="" set FILE2=!FILE2!
set /p OUTPUT="Enter Output File Name with extension [default: !OUTPUT!]: "
if "!OUTPUT!"=="" set OUTPUT=!OUTPUT!
set /p CREATOR="Enter GPX creator attribute value [default: (!CREATOR!)]: "
REM If left blank, do not pass --creator argument
set "CREATOR_ARG="
if not "!CREATOR!"=="" set "CREATOR_ARG=--creator=\"!CREATOR!\""
set /p PARAMS="Enter space separated extension names (e.g. hr cad) [default: !PARAMS!]: "
if "!PARAMS!"=="" set PARAMS=!PARAMS!

REM Call the Python merger script
if not "!CREATOR!"=="" (
    python Merger.py "!FILE1!" "!FILE2!" "!OUTPUT!" !PARAMS! --creator "!CREATOR!"
) else (
    python Merger.py "!FILE1!" "!FILE2!" "!OUTPUT!" !PARAMS!
)

echo Merge complete. Output written to !OUTPUT!
pause
