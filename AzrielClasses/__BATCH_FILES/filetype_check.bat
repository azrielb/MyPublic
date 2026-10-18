@echo off
rem Detect file type by content. Usage: filetype_check.bat <file> [file...]
rem Also works by dragging files onto this .bat
python "%~dp0filetype_check.py" %*
pause
