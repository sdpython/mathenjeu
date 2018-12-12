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
rem python -m mathenjeu create_self_signed_cert --keyfile=key.pem --certfile=cert.pem
python -m mathenjeu https_webapp --debug=1 --start=1 --port=8892 --userpwd=abc --keyfile=key.pem --certfile=cert.pem --cookie_key=dummypwd

rem daphne -e ssl:interface=127.0.0.1:port=8443:privateKey=key.pem:certKey=cert.pem apphyper:app
rem hypercorn apphyper:app --keyfile=key.pem --certfile=cert.pem --bind=127.0.0.1:9443