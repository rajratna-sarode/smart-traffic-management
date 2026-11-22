from bson import ObjectId
from datetime import datetime, timezone
from flask import jsonify

def oid(value):
    if not ObjectId.is_valid(value): raise ValueError('Invalid record id')
    return ObjectId(value)
def now(): return datetime.now(timezone.utc)
def json_doc(doc):
    if not doc: return doc
    return {('_id' if k=='_id' else k): (str(v) if isinstance(v,ObjectId) else v.isoformat() if isinstance(v,datetime) else v) for k,v in doc.items()}
def docs(items): return [json_doc(d) for d in items]
def error(message, code=400): return jsonify({'error':message}),code
