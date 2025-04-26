@echo off
setlocal enabledelayedexpansion

:: Set desired path
set "desiredPath=C:\C2_AIAgents\AIAgents\GridLoadManGEN5"

:: Set desired window size
set "width=120"
set "height=30"

:: Define arrays
set myArray=OPENAI OPENAIMINI OPENAIO3 GROK GOOGLE OPENAI45 LAMA CLAUDE DEEPSEEK BROKER
set myCommand0=python .\runchatserver.py --broker ON --model OPENAI
set myCommand1=python .\runchatserver.py --broker ON --model OPENAIMINI
set myCommand2=python .\runchatserver.py --broker ON --model OPENAIO3
set myCommand3=python .\runchatserver.py --broker ON --model GROK
set myCommand4=python .\runchatserver.py --broker ON --model GOOGLE
set myCommand5=python .\runchatserver.py --broker ON --model OPENAI45
set myCommand6=python .\runchatserver.py --broker ON --model LAMA
set myCommand7=python .\runchatserver.py --broker ON --model CLAUDE
set myCommand8=python .\runchatserver.py --broker ON --model DEEPSEEK
set myCommand9=python .\runbroker.py --confidence high

:: Initialize counter
set i=0

for %%A in (%myArray%) do (
    set "title=%%A"
    call set "command=%%myCommand!i!%%"

    start "Launching !title!" cmd.exe /k ^
        title !title! ^&^& ^
        mode con: cols=%width% lines=%height% ^&^& ^
        cd /d "%desiredPath%" ^&^& ^
        echo !command!
        @REM doskey PRELOADED_COMMAND=!command! ^&^& ^
        @REM echo Press UP-Arrow then Enter to run the command.

    set /a i+=1
)

endlocal
exit /b
