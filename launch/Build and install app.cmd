@echo off
rem  Build the Android app from the current book and install it on the tablet.
rem
rem    "Build and install app.cmd"          build, then install if plugged in
rem    "Build and install app.cmd" build    build only, no install
rem
rem  Assumes the facsimile and the flip pages are current. If you have revised
rem  a story, run this from the repo root first:
rem
rem      bash render/build.sh
rem
rem  Java: Gradle 8.14 cannot run on Android Studio's bundled JDK 25, and
rem  Capacitor declares Java 21, which JDK 17 cannot target. app/android/
rem  build.gradle pins every module back to 17 to resolve that, so this points
rem  JAVA_HOME at the system Temurin 17. See the comment in that file.

setlocal enabledelayedexpansion
cd /d "%~dp0..\app"

if not exist "..\flip\app.js" (
  echo.
  echo   flip\app.js is missing - that is the reader itself, not a build product.
  echo.
  pause
  exit /b 1
)

set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot"
if not exist "!JAVA_HOME!\bin\java.exe" (
  echo.
  echo   No JDK at !JAVA_HOME!
  echo   Edit this script to point JAVA_HOME at a JDK 21 or newer.
  echo.
  pause
  exit /b 1
)
set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"

echo.
echo   == copying the reader into the app ==
call npx --yes cap sync android
if errorlevel 1 goto :failed

rem  The app ships no books at all: flip/ is the reader and nothing else.
rem  Every book lives in the app's own folder on the device. Put them there
rem  with launch/Push books.cmd.

echo.
echo   == building the apk ==
rem  Remove the previous apk first. Gradle rewrites the zip in place, which
rem  leaves the old payload orphaned inside the file: after the books were
rem  taken out of the apk it still measured 18.8 MB, of which only 4.1 MB
rem  was real content. Zip readers find the central directory at the end and
rem  skip the dead bytes, so nothing breaks and nothing says so - the file
rem  is simply four times the size it should be for anyone copying it.
set "OLDAPK=%CD%\android\app\build\outputs\apk\debug\app-debug.apk"
if exist "%OLDAPK%" erase /q "%OLDAPK%"
rem  Absolute path, and "call" because it is a batch file. Some environments
rem  set NoDefaultCurrentDirectoryInExePath=1, under which cmd will not find
rem  gradlew.bat sitting in the current directory and the build dies with
rem  "not recognized as an internal or external command".
set "PROJ=%CD%"
cd /d "!PROJ!\android"
call "!PROJ!\android\gradlew.bat" assembleDebug -q
if errorlevel 1 goto :failed
cd /d "!PROJ!"

set "APK=!PROJ!\android\app\build\outputs\apk\debug\app-debug.apk"
if not exist "!APK!" (
  echo   Build reported success but there is no apk at:
  echo     !APK!
  goto :failed
)
echo.
echo   apk: !APK!

if /i "%~1"=="build" (
  echo.
  echo   Built only, as asked. Copy that apk to the tablet and tap it to
  echo   install, or re-run without "build" with the cable in.
  echo.
  pause
  exit /b 0
)

set "ADB=%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
if not exist "!ADB!" (
  echo.
  echo   adb not found; skipping install. The apk above can be copied to the
  echo   tablet and installed by tapping it.
  echo.
  pause
  exit /b 0
)

for /f "skip=1 tokens=1,2" %%a in ('"!ADB!" devices') do if "%%b"=="device" set "SERIAL=%%a"
if not defined SERIAL (
  echo.
  echo   No tablet detected, so the apk was not installed. Plug it in with
  echo   USB debugging on and re-run, or copy the apk across by hand.
  echo.
  pause
  exit /b 0
)

echo.
echo   == installing on !SERIAL! ==
"!ADB!" install -r "!APK!"
if errorlevel 1 goto :failed

echo.
rem  Reinstalling clears the app's data directory, and the library lives in
rem  it -- Android/data/<pkg>/files/books. A reinstall therefore empties the
rem  shelf, silently: the app comes up saying "No books yet" and the books
rem  look lost rather than deleted. So the books go back on straight away,
rem  every time, rather than being a step anyone has to remember.
if exist "%~dp0..\books" (
  echo.
  echo   == restoring the library ==
  set "NOPAUSE=1"
  call "%~dp0Push books.cmd"
  set "NOPAUSE="
)

echo   Done. Open "Facsimile" from the tablet's app drawer.
echo   The books it reads are in its own folder on the device; put them
echo   there with launch\Push books.cmd.
echo.
pause
exit /b 0

:failed
echo.
echo   FAILED. Scroll up for the reason.
echo.
pause
exit /b 1
