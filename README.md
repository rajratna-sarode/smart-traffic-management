<<<<<<< HEAD
# Parkwise Smart Parking Management (CCE5)

A MongoDB-backed parking management web application built with Flask, PyMongo, Bootstrap and Chart.js. All dashboard figures and tables are queried from MongoDB. The API validates inputs and checks booking time overlaps server-side.

## Requirements

- Python 3.10 or newer
- MongoDB Community Server running locally on port 27017
- A browser with internet access for Bootstrap and Chart.js CDN assets

## Install and run (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python scripts\init_db.py
python scripts\seed_data.py
python app.py
```

Open <http://127.0.0.1:5000>. The database defaults to `smart_parking_db`; set `MONGODB_URI` and `MONGODB_DB` in `.env` to change it. MongoDB Community Server should be running before initialization. On Windows, start the MongoDB service from an elevated PowerShell with `Start-Service MongoDB`, or start `mongod.exe` with the configured data directory. If MongoDB is not installed, install MongoDB Community Server and optionally MongoDB Compass from MongoDB's official download pages.

## Verify data in Compass

Connect Compass to `mongodb://127.0.0.1:27017/`, open `smart_parking_db`, and inspect `vehicles`, `parking_slots`, `bookings`, and `users`. The seed script inserts 10 vehicles, 20 slots and 15 bookings once. `/health` reports whether Flask can ping MongoDB.

## Features

- Dashboard KPIs and seven-day completed-revenue chart.
- Vehicle create, list/search, update and safe delete, with unique registration index.
- Slot create, list/filter, update and safe delete; availability checks exclude maintenance and overlapping confirmed/active reservations.
- Booking create, history/search, automatic duration and price, overlap prevention, start/complete/cancel workflow.
- MongoDB initialization, repeat-safe seed data, indexes and aggregation API.
- Report/query material in `docs/`.

## API overview

- `GET/POST /api/vehicles/`; `PUT/DELETE /api/vehicles/<id>`
- `GET/POST /api/slots/`; `GET /api/slots/availability?start=ISO&end=ISO&type=Car`; `PUT/DELETE /api/slots/<id>`
- `GET/POST /api/bookings/`; `PUT /api/bookings/<id>`; `PATCH /api/bookings/<id>/status`
- `GET /api/dashboard/`; `GET /api/dashboard/aggregations`; `GET /health`

The occupied/available dashboard counts use live booking records in confirmed/active state. Slot status is an administrative availability flag: a slot with status `Occupied` or `Maintenance` is not offered for new bookings. Edit forms are available for vehicle and slot details; booking lifecycle transitions are exposed in the history table.

See `docs/test_cases.md` for test procedures. Database-backed verification requires a running MongoDB server.
=======
# smart-traffic-management
smart traffic management using mongodb CRUD operation ,indexes and aggregation
>>>>>>> 45bc5d9dd72bd9d0cf49eaa2de605db175ad20e3
