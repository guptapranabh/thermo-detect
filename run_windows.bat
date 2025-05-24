@echo off

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python TrainedVideoGIF.py

echo Done!
pause
