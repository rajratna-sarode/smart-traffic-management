from config.db import get_db
from datetime import datetime,timedelta,timezone
def dashboard():
    db=get_db(); slots=list(db.parking_slots.find()); bookings=list(db.bookings.find()); done=[b for b in bookings if b['status']=='completed']
    current=datetime.now(timezone.utc)
    busy=db.bookings.distinct('slot_id',{'status':{'$in':['confirmed','active']},'start_time':{'$lte':current},'end_time':{'$gt':current}})
    daily=[]
    for i in range(6,-1,-1):
        day=(datetime.now(timezone.utc)-timedelta(days=i)).date(); low=datetime.combine(day,datetime.min.time(),timezone.utc); high=low+timedelta(days=1)
        total=sum(b.get('total_amount',0) for b in done if low<=b.get('updated_at',b['start_time'])<high)
        daily.append({'date':day.isoformat(),'revenue':round(total,2)})
    available=sum(s['status']=='Available' and s['_id'] not in busy for s in slots)
    occupied=sum(s['_id'] in busy for s in slots)
    return {'total_slots':len(slots),'available_slots':available,'occupied_slots':occupied,'maintenance_slots':sum(s['status']=='Maintenance' for s in slots),'vehicles':db.vehicles.count_documents({}),'bookings':len(bookings),'completed_bookings':len(done),'revenue':round(sum(b.get('total_amount',0) for b in done),2),'utilization':round(occupied/len(slots)*100,1) if slots else 0,'daily_revenue':daily}
