@echo off
cd /d "%~dp0"
set PIP_CACHE_DIR=%~dp0pipcache
set TMP=%~dp0tmp
set TEMP=%~dp0tmp
mkdir tmp 2>nul
echo Ornatilyapti, 10-20 daqiqa... (oyna ozi yopiladi)
if not exist venv\Scripts\python.exe "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m venv venv > urnatish_log.txt 2>&1
venv\Scripts\python -m pip install --upgrade pip >> urnatish_log.txt 2>&1
venv\Scripts\python -m pip install torch >> urnatish_log.txt 2>&1
venv\Scripts\python -m pip install numpy opencv-python dxcam mss pywin32 pynput comtypes >> urnatish_log.txt 2>&1
venv\Scripts\python -c "import torch,cv2,pynput,mss;print('TAYYOR',torch.__version__,torch.cuda.is_available(),torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')" >> urnatish_log.txt 2>&1
echo tugadi >> urnatish_log.txt
