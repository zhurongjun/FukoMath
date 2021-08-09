@echo off
python3 ./codegen/main.py
start /B /W premake/win/premake5 --file=premake.lua vs2010
pause