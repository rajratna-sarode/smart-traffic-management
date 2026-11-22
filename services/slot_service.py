from services.common import now
from config.db import get_db
from bson import ObjectId
from datetime import datetime, timezone

def all_slots(filters=None):
    filters=filters or {}; query={k:v for k,v in filters.items() if v}
    return list(get_db().parking_slots.find(query).sort('slot_number',1))
def create(data):
    data['created_at']=now(); data['updated_at']=now(); return get_db().parking_slots.insert_one(data).inserted_id
def update(sid,data):
    from services.common import oid
    data['updated_at']=now(); return get_db().parking_slots.update_one({'_id':oid(sid)},{'$set':data})
def delete(sid):
    from services.common import oid
    db=get_db(); key=oid(sid)
    if db.bookings.count_documents({'slot_id':key,'status':{'$in':['confirmed','active']}}): raise ValueError('Slot has a current booking')
    return db.parking_slots.delete_one({'_id':key})
def availability(start,end,slot_type=None):
    db=get_db(); query={'status':{'$ne':'Maintenance'}}
    if slot_type: query['slot_type']=slot_type
    slots=list(db.parking_slots.find(query)); a=datetime.fromisoformat(start); b=datetime.fromisoformat(end)
    if a.tzinfo is None:a=a.replace(tzinfo=timezone.utc)
    if b.tzinfo is None:b=b.replace(tzinfo=timezone.utc)
    busy={x['slot_id'] for x in db.bookings.find({'status':{'$in':['confirmed','active']},'start_time':{'$lt':b},'end_time':{'$gt':a}},{'slot_id':1})}
    return [s for s in slots if s['_id'] not in busy]
