@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ========================================
echo  Aurora 4x 日本語化SQL 一括適用ツール
echo ========================================
echo.
py apply_japanese.py %*
