@echo off

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main_windows.py

echo Done!
pause
