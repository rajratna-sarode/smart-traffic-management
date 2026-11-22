from flask import Blueprint,request,jsonify
from services import booking_service as svc
from services.common import docs,error
bp=Blueprint('bookings',__name__)
@bp.get('/')
def listing():
    try:return jsonify(docs(svc.all_bookings(request.args.get('q',''))))
    except Exception as e:return error(str(e),503)
@bp.post('/')
def create():
    try:return jsonify({'id':str(svc.create(request.get_json() or {}))}),201
    except Exception as e:return error(str(e),409)
@bp.put('/<bid>')
def update(bid):
    try:
        r=svc.update(bid,request.get_json() or {}); return ({'updated':True},200) if r.matched_count else error('Booking not found or not editable',404)
    except Exception as e:return error(str(e),409)
@bp.patch('/<bid>/status')
def status(bid):
    try:
        r=svc.set_status(bid,(request.get_json() or {}).get('status')); return ({'updated':True},200) if r.matched_count else error('Booking not found or already final',404)
    except Exception as e:return error(str(e))
