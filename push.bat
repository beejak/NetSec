@echo off
echo Pushing to GitHub...
git add .
git commit -m "Add container security scanner"
git push origin main
pause
