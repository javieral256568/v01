@echo off
for /f "tokens=2" %%a in ('tasklist ^| findstr uvicorn') do taskkill /PID %%a /F