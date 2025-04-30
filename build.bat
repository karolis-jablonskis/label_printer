@echo off
echo Building your EXE...

pyinstaller main.py --hidden-import=win32print --hidden-import=win32api --onefile --noconsole --name=LabelPrinter --icon=logo.ico --additional-hooks-dir=.

echo.
echo Build complete!
pause