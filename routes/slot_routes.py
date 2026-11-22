from flask import Blueprint,request,jsonify
from services import slot_service as svc
from services.common import docs,error
bp=Blueprint('slots',__name__)
@bp.get('/')
def listing():
    try:return jsonify(docs(svc.all_slots({'slot_type':request.args.get('type'),'status':request.args.get('status')})))
    except Exception as e:return error(str(e),503)
@bp.get('/availability')
def availability():
    try:
        a=request.args['start']; b=request.args['end']; return jsonify(docs(svc.availability(a,b,request.args.get('type'))))
    except KeyError:return error('start and end are required')
    except Exception as e:return error(str(e))
@bp.post('/')
def create():
    d=request.get_json(silent=True) or {}
    try:
        d={'slot_number':str(d['slot_number']).strip().upper(),'slot_type':d['slot_type'],'floor':int(d['floor']),'hourly_rate':float(d['hourly_rate']),'status':d.get('status','Available')}
        if d['slot_type'] not in ('Car','Bike') or d['status'] not in ('Available','Occupied','Maintenance') or d['floor']<0 or d['hourly_rate']<0:raise ValueError('Invalid slot type, status, floor or rate')
        return jsonify({'id':str(svc.create(d))}),201
    except Exception as e:return error(str(e))
@bp.put('/<sid>')
def update(sid):
    d=request.get_json(silent=True) or {}; allowed={'slot_number','slot_type','floor','hourly_rate','status'}; d={k:v for k,v in d.items() if k in allowed}
    try:
        if not d:return error('No valid fields supplied')
        if 'hourly_rate' in d:d['hourly_rate']=float(d['hourly_rate'])
        if 'floor' in d:d['floor']=int(d['floor'])
        if d.get('slot_type', 'Car') not in ('Car','Bike') or d.get('status','Available') not in ('Available','Occupied','Maintenance') or d.get('hourly_rate',0)<0:return error('Invalid slot fields')
        r=svc.update(sid,d); return ({'updated':True},200) if r.matched_count else error('Slot not found',404)
    except Exception as e:return error(str(e))
@bp.delete('/<sid>')
def delete(sid):
    try:
        r=svc.delete(sid); return ({'deleted':True},200) if r.deleted_count else error('Slot not found',404)
    except Exception as e:return error(str(e),409)
