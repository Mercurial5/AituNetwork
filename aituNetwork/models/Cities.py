from aituNetwork.models import db

import mongoengine
from bson.objectid import ObjectId

class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    @staticmethod
    def get_cities():
        return Cities.query.order_by(Cities.id.asc()).all()

    @staticmethod
    def get_city(city_id: int):
        return Cities.query.get(city_id)


class CitiesCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    name = mongoengine.StringField(unique=True, max_length=255, required=True)

    @staticmethod
    def get_cities():
        return db.cities.find({})

    @staticmethod
    def get_city(city_id: int):
        return db.cities.find({"id": city_id})
