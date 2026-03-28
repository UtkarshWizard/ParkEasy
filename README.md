# Vehicle-Parking-App---V2
It is a multi-user app (one requires an administrator and other users) that manages different parking lots, parking spots and parked vehicles. Assume that this parking app is for 4-wheeler parking.

## Features
- Admin and user roles
- Parking lot and spot management
- Real-time spot reservation and release
- Analytics and charts
- Background jobs for reminders and reports

## To run the app -

# Frontend - 
- cd frontend/ 
- npm run dev - starts on localhost:5173

# Backend -
- Open vs code in wsl using below 
    cd /mnt/c/vehicle_parking_app_23f3001747/backend
    code .
- Then create a venv if not already-
    python3 -m venv venv
- Install dependencies from pip install -r requirements.txt
- Run python3 init_db.py to initialize the database
- Run python3 app.py

# Redis and Celery
- Open new terminal in wsl itself and go in venv
- For Redis do redis-server start to start a redis server and check redis-cli ping You get Pong means server is running.
- For celery use - 
    celery -A celery_worker worker --loglevel=info (for worker)
    celery -A celery_worker beat --loglevel=info (for beat used in schedule task)