@echo off
python3 ./Codegen/main.py
start /B /W premake/win/premake5 --file=premake.lua vs2010
pause