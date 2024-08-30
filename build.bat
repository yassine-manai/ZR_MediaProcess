@echo off

REM Read the current version from version.txt
set /p version=<version.txt

REM Split the version into components
for /f "tokens=1-3 delims=." %%a in ("%version%") do (
    set major=%%a
    set minor=%%b
    set patch=%%c
)

REM Increment the patch version
set /a patch=patch+1

REM Update the version
set new_version=%major%.%minor%.%patch%

REM Save the new version to version.txt
echo %new_version% > version.txt

REM Create the executable with the updated version in the name
pyinstaller --noconfirm --onefile --console --name Import_Tool_v%new_version%.exe main.py

REM Notify the user
REM echo Created Import_Tool_v%new_version%.exe
REM pause
