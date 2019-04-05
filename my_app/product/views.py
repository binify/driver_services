import json
import geopy.distance
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from my_app import db, app
from my_app.product.models import Location
from my_app.product.utils import create_random_point

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome, nothing here actually."


def bad_request(message):
    res = jsonify({'errors': message})
    res.status_code = 402
    return res


class LocationView(MethodView):

    def get(self, radius, limit):
        # radius = request.args.get('radius')
        # limit = request.args.get('limit')
        customer = (request.args.get('latitude'),
                    request.args.get('longitude'))
        locations = Location.query.all()
        print(len(locations))
        res = {}
        for loc in locations:
            driver = (loc.lati, loc.longi)
            print(driver)
            distance = geopy.distance.vincenty(customer, driver).m
            i = 0
            if distance <= radius:
                while i <= limit:
                    res[loc.id] = {
                        'latitude': str(loc.lati),
                        'longitude': str(loc.longi),
                        'distance': str(distance),
                    }
                    i += 1
        # else:
        #     loc = Location.query.filter_by(id=id).first()
        #     if not loc:
        #         abort(404)
        #     res = {
        #         'latitude': str(loc.lati),
        #         'longitude': str(loc.longi),
        #         'accuracy': str(loc.acc),
        #     }
        return jsonify(res)

    def post(self, id):
        return

    def put(self, id):
        loc = Location.query.get_or_404(id)
        lati = request.form.get('lati')
        longi = request.form.get('longi')
        acc = request.form.get('acc')
        if float(lati) < -90 or float(lati) > 90:
            return bad_request("Latitude should be between +/- 90")
        if float(longi) < -180 or float(longi) > 180:
             return bad_request("Longitude should be between +/- 180")
        if float(acc) < 0 or float(acc) > 1:
            return bad_request("Accuracy should be between 0 and 1")
        loc.lati = lati
        loc.longi = longi
        loc.acc = acc
        db.session.commit()
        return jsonify({loc.id: {
            'latitude': str(loc.lati),
            'longitude': str(loc.longi),
            'accuracy': str(loc.acc),
        }})

    def delete(self, id):
        return


view_func = LocationView.as_view('location_view')
app.add_url_rule('/drivers/<int:id>/location',
                 view_func=view_func, methods=['PUT'])
app.add_url_rule('/drivers', view_func=view_func,
                 defaults={'radius': 500, 'limit': 10}, methods=['GET'])
