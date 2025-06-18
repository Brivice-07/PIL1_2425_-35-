@echo off

echo --------------------------------------
echo Démarrage de l'application MotoShare
echo --------------------------------------

call npm install
start http://localhost:5173/
call npm run dev

pause