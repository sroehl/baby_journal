from flask_restful import Resource

class Diaper(Resource):
  def get(self, diaper_id):
    if diaper_id is None:
      
