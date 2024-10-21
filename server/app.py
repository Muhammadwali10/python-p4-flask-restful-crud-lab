from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
migrate = Migrate(app, db)

db.init_app(app)

class PlantsResource(Resource):
    def get(self, plant_id):
        plant = db.session.get(Plant, plant_id)
        if plant:
            return jsonify(plant.to_dict())
        return {'message': 'Plant not found'}, 404

    def patch(self, plant_id):
        plant = db.session.get(Plant, plant_id)
        if plant:
            data = request.get_json()
            plant.is_in_stock = data.get('is_in_stock', plant.is_in_stock)
            db.session.commit()
            return jsonify(plant.to_dict())
        return {'message': 'Plant not found'}, 404

    def delete(self, plant_id):
        plant = db.session.get(Plant, plant_id)
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return '', 204
        return {'message': 'Plant not found'}, 404

api.add_resource(PlantsResource, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
