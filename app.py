import os
from flask import Flask, render_template
from config.db import init_db
from routes.vehicle_routes import bp as vehicles_bp
from routes.slot_routes import bp as slots_bp
from routes.booking_routes import bp as bookings_bp
from routes.dashboard_routes import bp as dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
    app.register_blueprint(slots_bp, url_prefix='/api/slots')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    @app.get('/')
    def home(): return render_template('dashboard.html')
    @app.get('/<page>')
    def pages(page):
        if page not in ('vehicles','slots','bookings'): return render_template('dashboard.html')
        return render_template(page+'.html')
    @app.get('/health')
    def health():
        try:
            db=init_db(); db.command('ping')
            return {'status':'ok','database':db.name}
        except Exception as exc: return {'status':'error','message':str(exc)},503
    return app

app=create_app()
if __name__ == '__main__': app.run(host='127.0.0.1', port=int(os.getenv('PORT',5000)), debug=os.getenv('FLASK_DEBUG')=='1')
