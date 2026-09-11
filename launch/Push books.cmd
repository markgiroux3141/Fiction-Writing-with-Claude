@echo off
rem  Copy the built book bundles onto the tablet.
rem
rem    "Push books.cmd"              push everything in books/
rem    "Push books.cmd" <id>         push just that one bundle
rem
rem  The app ships with no books in it. Every book it reads lives in its own
rem  folder on the device, so putting a book on the tablet is copying a
rem  directory and nothing else - no rebuild, no reinstall.
rem
rem  Build the bundles first, from the repo root:  bash render/build.sh
rem
rem  The destination needs no storage permission and is visible over USB and in
rem  My Files, so a bundle can also just be dragged across by hand. To remove a
rem  book, delete its folder there; the shelf is whatever is in that directory.

setlocal enabledelayedexpansion
cd /d "%~dp0.."

if not exist "books" (
  echo.
  echo   No books built yet.  From the repo root:  bash render/build.sh
  echo.
  if not defined NOPAUSE pause
  exit /b 1
)

set "ADB=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
if not exist "!ADB!" for /f "delims=" %%p in ('where adb 2^>nul') do set "ADB=%%p"
if not exist "!ADB!" (
  echo.
  echo   adb not found. Install Android platform-tools, or copy the folders in
  echo   books\ to this path on the tablet by hand:
  echo     Android\data\com.standingwater.facsimile\files\books\
  echo.
  if not defined NOPAUSE pause
  exit /b 1
)

for /f "skip=1 tokens=1,2" %%a in ('"!ADB!" devices') do (
  if "%%b"=="unauthorized" (
    echo.
    echo   Tablet says UNAUTHORIZED. There is an "Allow USB debugging?" prompt
    echo   on its screen. Tap Allow, then run this again.
    echo.
    pause
    exit /b 1
  )
  if "%%b"=="device" set "SERIAL=%%a"
)
if not defined SERIAL (
  echo.
  echo   No tablet detected. Check the cable and that USB debugging is on.
  echo.
  if not defined NOPAUSE pause
  exit /b 1
)

set "DEST=/sdcard/Android/data/com.standingwater.facsimile/files/books"
echo.
echo   tablet: !SERIAL!
echo   dest:   !DEST!
echo.

rem  The app creates this on first run; make it anyway, in case the app has
rem  never been opened on a fresh install.
"!ADB!" shell mkdir -p "!DEST!" >nul 2>&1

set "COUNT=0"
for /d %%d in (books\*) do (
  set "NAME=%%~nxd"
  if "%~1"=="" (
    call :push "%%d" "!NAME!"
  ) else if /i "%~1"=="!NAME!" (
    call :push "%%d" "!NAME!"
  )
)

echo.
if "!COUNT!"=="0" (
  echo   Nothing pushed.
  if not "%~1"=="" echo   No bundle in books\ is called "%~1".
) else (
  echo   !COUNT! book^(s^) on the tablet. Open the app - they are on the shelf.
)
echo.
if not defined NOPAUSE pause
exit /b 0

:push
echo   pushing %~2 ...
"!ADB!" push "%~1" "!DEST!/" >nul 2>&1
if errorlevel 1 (
  echo     FAILED
) else (
  set /a COUNT+=1
)
goto :eof
