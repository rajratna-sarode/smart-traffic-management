"""Create the project collections and indexes. Safe to run repeatedly."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from config.db import get_db

def main():
    db=get_db()
    for name in ('vehicles','parking_slots','bookings','users'):
        if name not in db.list_collection_names(): db.create_collection(name)
    db.vehicles.create_index([('registration_number',1)],unique=True,name='uq_vehicle_registration')
    db.vehicles.create_index([('mobile',1)],name='ix_vehicle_mobile')
    db.parking_slots.create_index([('slot_number',1)],unique=True,name='uq_slot_number')
    db.bookings.create_index([('vehicle_number',1),('start_time',-1)],name='ix_booking_vehicle_time')
    db.bookings.create_index([('slot_id',1),('status',1),('start_time',1),('end_time',1)],name='ix_booking_conflict')
    print('Collections ready:',', '.join(db.list_collection_names()))
    print('Vehicle indexes:',db.vehicles.index_information())
    print('Booking indexes:',db.bookings.index_information())
if __name__=='__main__':main()
