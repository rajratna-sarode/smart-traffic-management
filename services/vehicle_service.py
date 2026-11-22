from pymongo.errors import DuplicateKeyError
from services.common import now
from config.db import get_db

def all_vehicles(q=''):
    db=get_db(); query={'registration_number':{'$regex':q,'$options':'i'}} if q else {}
    return list(db.vehicles.find(query).sort('created_at',-1))
def create(data):
    db=get_db(); data.update(created_at=now(),updated_at=now())
    return db.vehicles.insert_one(data).inserted_id
def update(vid,data):
    from services.common import oid
    data['updated_at']=now(); return get_db().vehicles.update_one({'_id':oid(vid)},{'$set':data})
def delete(vid):
    from services.common import oid
    db=get_db(); oidv=oid(vid)
    if db.bookings.count_documents({'vehicle_id':oidv,'status':{'$in':['confirmed','active']}}): raise ValueError('Vehicle has a current booking')
    return db.vehicles.delete_one({'_id':oidv})
