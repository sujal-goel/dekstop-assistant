@echo off
echo Intializing the project
REM Check if the marker file exists
if exist "marker.txt" (
    echo Project has already initialized
) else (
    call :initialize
)
call :run
pause

:run
call env\Scripts\activate.bat
echo Getting into the virtual environment
echo Running the programs
py run.py
goto :EOF

:initialize

echo Creating virtual environment.....
python -m venv env
echo Building required dependices.....
call env\Scripts\activate.bat
pip install -r requirements.txt
echo setting up database....
python engine\db.py

echo Project is initialized successfully  > "marker.txt"
echo The project is initialized successfully
goto :EOF