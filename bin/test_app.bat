@echo off
@echo SCRIPT: windows_prefix
if "%1"=="" goto default_value_python:
if "%1"=="default" goto default_value_python:
set pythonexe=%1
goto start_script:

:default_value_python:
set pathserver=this,%~dp0..


rem QCM

python -m mathenjeu qcm_local --cookie_key=dummypwd --start=1 --port=8889 --userpwd=abc
rem python -m mathenjeu create_self_signed_cert --keyfile=key.pem --certfile=cert.pem
rem python -m mathenjeu qcm_https --debug=1 --start=1 --port=8892 --userpwd=abc --keyfile=key.pem --certfile=cert.pem --cookie_key=dummypwd

rem daphne -e ssl:interface=127.0.0.1:port=8443:privateKey=key.pem:certKey=cert.pem apphyper:app
rem hypercorn apphyper:app --keyfile=key.pem --certfile=cert.pem --bind=127.0.0.1:9443
rem gunicorn apphyper:app --keyfile=key.pem --certfile=cert.pem --bind=127.0.0.1:9443

rem LOCAL

rem python -m mathenjeu static_local --cookie_key=dummypwd --start=1 --port=8877 --userpwd=abc --content=%pathserver%
rem python -m mathenjeu create_self_signed_cert --keyfile=key.pem --certfile=cert.pem
rem python -m mathenjeu static_https --debug=1 --start=1 --port=8892 --userpwd=abc --keyfile=key.pem --certfile=cert.pem --cookie_key=dummypwd --content=site,C:/site
rem hypercorn apphyper:app --keyfile=key.pem --certfile=cert.pem --bind=127.0.0.1:9443