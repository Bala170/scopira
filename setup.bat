@echo off
echo Setting up Scopira Development Environment...
echo.

echo Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo Installing ML Dependencies...
cd ml
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd ..

echo.
echo Installing Database Dependencies...
cd database
pip install -r requirements.txt
cd ..

echo.
echo Setting up Frontend Dependencies...
cd frontend
if exist package.json (
    echo Installing npm packages...
    npm install
) else (
    echo No package.json found, skipping npm install
)
cd ..

echo.
echo Setup completed!
echo.
echo To run the development servers:
echo 1. Make sure PostgreSQL is installed and running
echo 2. Create the database by running: python database/init_db.py
echo 3. Start the development servers: run_dev.bat
echo.
pause