from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Missing field 'name' in json")
    argumentos.add_argument('estrelas', type=float, required=True, help="Missing field 'estrelas' in json")
    argumentos.add_argument('diaria', type=float, required=True, help="Missing field 'diaria' in json")
    argumentos.add_argument('cidade', type=str, required=True, help="Missing field 'cidade' in json")

    def get(self, hotel_id):
        hotel =  HotelModel.find_hotel(hotel_id)
        
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message':'Hotel id "{}" already exists.'}, 400

        dados = Hotel.argumentos.parse_args()
        
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'Internal Error while saving in Database'}, 500
        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        

        found_hotel =  HotelModel.find_hotel(hotel_id)

        if found_hotel:
            found_hotel.update_hotel(**dados)
            found_hotel.save_hotel()
            return found_hotel.json(), 200
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Internal Error while saving in Database'}, 500
        
        return hotel.json(), 201


    def delete(self, hotel_id):
        hotel  = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Internal Error while tring to delete'}, 500
            return {'message': 'Hotel Deleted'}, 200
        return {'message': 'Hotel not found'}, 400