"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),

# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.

class Brevet(Resource):
    # get a specified brevet
    def get(self, brevet_id: str):
        try:
            return Response(
                # convert it from a MongoEngine query object to a JSON 
                Brevet.objects.get(id=brevet_id).to_json(),
                # return Response(json_object, mimetype="application/json", status=200)
                mimetype="application/json",
                status=200
            )
        except: # TODO
            # something went wronge, do something here
            return
        
    # put a specified brevet (like update, replace)
    def put(self, brevet_id: str):
        try:
            Brevet(**request.json).validate()  # make sure the new document is valid before updating
            updated_brevet = Brevet.objects.get(id=brevet_id).update(
                __raw__={"$set": request.json}  # replace the entire document with what's in request.json
            )
            if updated_brevet == 1:  # one document was updated
                return {"success": True}, 200
            else: #TODO
                # something went wronge, do something here
                return
        except: #TODO
            # something went wronge, do something here
            return

    # delete a specified brevet
    def delete(self, brevet_id: str):
        try:
            Brevet.objects.get(id=brevet_id).delete()
            return {"success": True}, 200
        except: #TODO
            # something went wronge, do something here
            return 
