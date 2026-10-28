@echo off
TITLE Hindustan Unilever - Executive Decision Intelligence Engine (Port 5012)
echo ==============================================================================
echo  PROJECT - 12: EXECUTIVE DECISION INTELLIGENCE
echo  Hindustan Unilever Limited - AI Causal KPI Attribution & Financial Dashboard
echo ==============================================================================

set PYTHON_CMD=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHON_CMD="C:\Users\hp\AppData\Local\Programs\Orange\python.exe"
)

echo Starting Executive Decision Intelligence Server on Port 5012...
%PYTHON_CMD% run_project.py
pause

