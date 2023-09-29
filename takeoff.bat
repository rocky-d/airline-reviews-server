@echo off

cd C:\rocky_d\code\databases\dmd-presentation
start "Airline Reviews Visualization" "http://localhost:63342/dmd-presentation/templates/redirect.html"
C:\rocky_d\code\databases\dmd-presentation\dmd-presentation\Scripts\python.exe app.py

exit