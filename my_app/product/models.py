from my_app import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lati = db.Column(db.Float(asdecimal=True))
    longi = db.Column(db.Float(asdecimal=True))
    acc = db.Column(db.Float(precision=2))

    def __init__(self, lati, longi, acc):
        self.longi = longi
        self.lati = lati
        self.acc = acc

    def __repr__(self):
        return '<Location for driver {} {} {}'.format(self.id, self.lati, self.longi)

