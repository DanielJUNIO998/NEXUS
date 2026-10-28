
@echo off
title NEXUS AI - Inicializador
cd /d "D:\phynton\NEXUS.IA"

echo Iniciando o NEXUS...

start "NEXUS - Flask" cmd /k "cd /d D:\phynton\NEXUS.IA && py app.py"

timeout /t 3 /nobreak >nul

py nexus_hologram.py

pause
