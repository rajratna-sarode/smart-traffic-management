from flask import Blueprint,jsonify
from services.analytics_service import dashboard
from config.db import get_db
from services.common import error
bp=Blueprint('dashboard',__name__)
@bp.get('/')
def overview():
    try:return jsonify(dashboard())
    except Exception as e:return error(str(e),503)
@bp.get('/aggregations')
def aggregations():
    try:
        db=get_db()
        return jsonify({'booking_status':list(db.bookings.aggregate([{'$group':{'_id':'$status','count':{'$sum':1}}},{'$sort':{'_id':1}}])),'completed_revenue':list(db.bookings.aggregate([{'$match':{'status':'completed'}},{'$group':{'_id':None,'revenue':{'$sum':'$total_amount'}}}])),'revenue_by_slot':list(db.bookings.aggregate([{'$match':{'status':'completed'}},{'$group':{'_id':'$slot_number','revenue':{'$sum':'$total_amount'}}},{'$sort':{'revenue':-1}}])),'average_duration':list(db.bookings.aggregate([{'$match':{'status':'completed'}},{'$group':{'_id':None,'average_hours':{'$avg':'$duration_hours'},'min_hours':{'$min':'$duration_hours'},'max_hours':{'$max':'$duration_hours'}}}])),'slot_utilization_note':'Utilization over a reporting period is occupied booking-hours divided by non-maintenance slot-hours; see docs/aggregation_queries.md for period pipeline.'})
    except Exception as e:return error(str(e),503)
