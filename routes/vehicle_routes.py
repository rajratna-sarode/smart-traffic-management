from flask import Blueprint,request,jsonify
from services import vehicle_service as svc
from services.common import docs,json_doc,error,oid
from config.db import get_db
bp=Blueprint('vehicles',__name__)
@bp.get('/')
def listing():
    try:return jsonify(docs(svc.all_vehicles(request.args.get('q',''))))
    except Exception as e:return error(str(e),503)
@bp.post('/')
def create():
    d=request.get_json(silent=True) or {}; required=['owner_name','registration_number','vehicle_type','mobile']
    if any(not str(d.get(k,'')).strip() for k in required):return error('All fields are required')
    if d['vehicle_type'] not in ('Car','Bike'):return error('Vehicle type must be Car or Bike')
    d={k:str(d[k]).strip() for k in required}; d['registration_number']=d['registration_number'].upper()
    try:return jsonify({'id':str(svc.create(d))}),201
    except Exception as e:
        from pymongo.errors import DuplicateKeyError
        if isinstance(e,DuplicateKeyError):return error('Registration number already exists',409)
        return error(str(e),503)
@bp.put('/<vid>')
def update(vid):
    d=request.get_json(silent=True) or {}; allowed=['owner_name','registration_number','vehicle_type','mobile']; d={k:v for k,v in d.items() if k in allowed}
    if not d:return error('No valid fields supplied')
    if 'registration_number' in d:d['registration_number']=str(d['registration_number']).strip().upper()
    if d.get('vehicle_type') not in (None,'Car','Bike'):return error('Vehicle type must be Car or Bike')
    try:
        r=svc.update(vid,d); return ({'updated':True},200) if r.matched_count else error('Vehicle not found',404)
    except Exception as e:return error(str(e),409)
@bp.delete('/<vid>')
def delete(vid):
    try:
        r=svc.delete(vid); return ({'deleted':True},200) if r.deleted_count else error('Vehicle not found',404)
    except Exception as e:return error(str(e),409)
