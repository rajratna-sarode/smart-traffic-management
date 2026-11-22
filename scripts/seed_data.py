"""Insert a deterministic sample dataset once; reruns do not duplicate it."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from datetime import datetime,timedelta,timezone
from config.db import get_db
from scripts.init_db import main as init

def seed():
    init(); db=get_db()
    if db.vehicles.count_documents({'seed_batch':'cce5-v1'}):
        print('Seed data already present; no changes made.'); return
    now=datetime.now(timezone.utc); vehicles=[]
    for i in range(10):vehicles.append({'owner_name':f'Sample Owner {i+1}','registration_number':f'KA05MN{1000+i}','vehicle_type':'Car' if i%2==0 else 'Bike','mobile':f'90000000{i:02d}','created_at':now,'updated_at':now,'seed_batch':'cce5-v1'})
    db.vehicles.insert_many(vehicles); vehicles=list(db.vehicles.find({'seed_batch':'cce5-v1'}).sort('registration_number',1))
    slots=[]
    for i in range(20):slots.append({'slot_number':f'{"C" if i<10 else "B"}{i%10+1:02d}','slot_type':'Car' if i<10 else 'Bike','floor':i//5,'hourly_rate':60 if i<10 else 25,'status':'Maintenance' if i in (9,19) else 'Available','created_at':now,'updated_at':now,'seed_batch':'cce5-v1'})
    db.parking_slots.insert_many(slots); slots=list(db.parking_slots.find({'seed_batch':'cce5-v1'}).sort('slot_number',1))
    bookings=[]
    for i in range(15):
        start=now-timedelta(days=15-i,hours=3); end=start+timedelta(hours=1+i%4); v=vehicles[i%len(vehicles)]; s=slots[i]
        bookings.append({'vehicle_id':v['_id'],'vehicle_number':v['registration_number'],'slot_id':s['_id'],'slot_number':s['slot_number'],'start_time':start,'end_time':end,'duration_hours':round((end-start).total_seconds()/3600,2),'hourly_rate':s['hourly_rate'],'total_amount':round((end-start).total_seconds()/3600*s['hourly_rate'],2),'status':'completed' if i<12 else 'cancelled','created_at':start-timedelta(hours=1),'updated_at':end,'seed_batch':'cce5-v1'})
    db.bookings.insert_many(bookings)
    print(f'Inserted {len(vehicles)} vehicles, {len(slots)} slots, {len(bookings)} bookings.')
if __name__=='__main__':seed()
