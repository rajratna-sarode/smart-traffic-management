from datetime import datetime,timezone
from services.common import now,oid
from config.db import get_db

LIVE=['confirmed','active']
def parse_dt(s):
    d=datetime.fromisoformat(s.replace('Z','+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d
def payload(data, booking_id=None):
    db=get_db(); vehicle=db.vehicles.find_one({'_id':oid(data['vehicle_id'])}); slot=db.parking_slots.find_one({'_id':oid(data['slot_id'])})
    if not vehicle or not slot: raise ValueError('Choose an existing vehicle and slot')
    start,end=parse_dt(data['start_time']),parse_dt(data['end_time'])
    if end<=start: raise ValueError('End time must be later than start time')
    if slot['slot_type'] != vehicle['vehicle_type']: raise ValueError('Slot type must match vehicle type')
    conflict={'slot_id':slot['_id'],'status':{'$in':LIVE},'start_time':{'$lt':end},'end_time':{'$gt':start}}
    if booking_id: conflict['_id']={'$ne':oid(booking_id)}
    if db.bookings.find_one(conflict): raise ValueError('Slot is already booked during this time')
    hours=(end-start).total_seconds()/3600; rate=float(slot['hourly_rate'])
    return {'vehicle_id':vehicle['_id'],'vehicle_number':vehicle['registration_number'],'slot_id':slot['_id'],'slot_number':slot['slot_number'],'start_time':start,'end_time':end,'duration_hours':round(hours,2),'hourly_rate':rate,'total_amount':round(hours*rate,2)}
def create(data):
    db=get_db(); doc=payload(data); doc.update(status='confirmed',created_at=now(),updated_at=now()); return db.bookings.insert_one(doc).inserted_id
def update(bid,data):
    db=get_db(); patch=payload(data,bid); patch['updated_at']=now(); return db.bookings.update_one({'_id':oid(bid),'status':{'$in':LIVE}},{'$set':patch})
def set_status(bid,status):
    if status not in ('cancelled','completed','active'): raise ValueError('Unsupported status')
    return get_db().bookings.update_one({'_id':oid(bid),'status':{'$in':LIVE}},{'$set':{'status':status,'updated_at':now()}})
def all_bookings(q=''):
    query={'vehicle_number':{'$regex':q,'$options':'i'}} if q else {}
    return list(get_db().bookings.find(query).sort('start_time',-1))
