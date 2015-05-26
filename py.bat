@echo off

set package_time=%date:~0,4%%date:~5,2%%date:~8,2%
set version=%package_time%
echo %version%

set source_file=bav_tool.py
sed -i "s/'v0.0.1\..*'/'v0.0.1.%version%'/g" %source_file%


pyinstaller -F %source_file% --icon=python.ico
