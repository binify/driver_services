import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from my_app import db, app
from my_app.product.models import Location

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome, nothing here actually."


class LocationView(MethodView):

    def get(self, id=None, page=1):
        if not id:
            locations = Location.query.paginate(page, 10).items
            res = {}
            for loc in locations:
                res[loc.id] = {
                    'latitude': str(loc.lati),
                    'longitude': str(loc.longi),
                    'accuracy': str(loc.acc),
                }
        else:
            loc = Location.query.filter_by(id=id).first()
            if not loc:
                abort(404)
            res = {
                'latitude': str(loc.lati),
                'longitude': str(loc.longi),
                'accuracy': str(loc.acc),
            }
        return jsonify(res)

    def post(self,id):
        loc = Location.query.get_or_404(id)
        loc.lati = request.form.get('lati')
        loc.longi = request.form.get('longi')
        loc.acc = request.form.get('acc')
        db.session.commit()
        return jsonify({loc.id: {
            'latitude': str(loc.lati),
            'longitude': str(loc.longi),
            'accuracy': str(loc.acc),
        }})

    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id):
        # Delete the record for the provided id.
        return


location_view = LocationView.as_view('location_view')
# app.add_url_rule('/locations/', view_func=location_view, methods=['GET', 'POST'])
app.add_url_rule('/drivers/<int:id>/location',
                 view_func=location_view, methods=['GET','POST'])
