@echo off

REM Create virtual environment
echo Creating venv with name ''myenv''
echo ------------------------------------------------
pause
python -m venv myenv

REM Activate virtual environment
echo Activating virtual environment
echo ------------------------------------------------
pause
call myenv\Scripts\activate.bat

REM Install required dependencies
echo Installing requirements.txt
echo ------------------------------------------------
pause
pip install -r requirements.txt
pause

REM Run main.py
echo Running main.py
echo ------------------------------------------------
pause
python main.py
