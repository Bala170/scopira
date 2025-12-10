@echo off
echo Running Scopira Tests...
echo.

echo Running ML Component Tests...
cd ml
python test_ml.py
cd ..

echo.
echo Running Frontend Tests...
cd frontend
python test_frontend.py
cd ..

echo.
echo Running Database Tests...
cd database
python init_db.py
cd ..

echo.
echo All tests completed!
echo.
echo Note: Backend API tests require the server to be running.
echo To test backend API:
echo 1. Start the server with 'python backend/app.py'
echo 2. Run 'python backend/test_api.py' in another terminal
echo.
pause