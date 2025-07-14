#!/bin/bash
# FFmpeg herunterladen
wget https://ffmpeg.org/releases/ffmpeg-5.1.2-full_build.zip -O ffmpeg.zip
unzip ffmpeg.zip -d backend/
# Python-Abhängigkeiten installieren
python -m pip install -r requirements.txt