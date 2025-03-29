@echo off
setlocal

chcp 65001 >nul

echo ========================================
echo Проверка наличия FFmpeg
echo ========================================
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg не найден. Устанавливаем...
    curl -L https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-release-essentials.zip -o ffmpeg.zip
    tar -xf ffmpeg.zip
    move /Y ffmpeg-* ffmpeg
    setx PATH "%CD%\ffmpeg\bin;%PATH%"
    echo FFmpeg установлен.
) else (
    echo FFmpeg уже установлен.
)

echo ========================================
echo Установка виртуального окружения Python
echo ========================================
xcopy /Y /E /I shared speech_recorder\shared
copy /Y .env speech_recorder\.env
cd speech_recorder
python -m venv venv
call venv\Scripts\activate

echo ==============================
echo Установка зависимостей
echo ==============================
pip install -r requirements.txt


cd ..

echo ======================================
echo Запуск Docker-контейнеров
echo ======================================
docker-compose up -d --build

echo ==============================
echo Запуск Python-приложения
echo ==============================
cd speech_recorder
set RABBITMQ_USER=test
set RABBITMQ_PASSWORD=test
python main.py

endlocal
pause