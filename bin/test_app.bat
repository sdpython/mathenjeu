@echo off
@echo SCRIPT: windows_prefix
if "%1"=="" goto default_value_python:
if "%1"=="default" goto default_value_python:
set pythonexe=%1
goto start_script:

:default_value_python:
set pythonexe=c:\Python370_x64\python

@echo ~SET pythonexe=%pythonexe%

rem python -m mathenjeu local_webapp --cookie_key=dummypwd --start=1 --port=8889 --userpwd=abc
python -m mathenjeu https_webapp --cookie_key=dummypwd --start=1 --port=8889 --userpwd=abc