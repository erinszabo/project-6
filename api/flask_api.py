"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
from flask_cors import CORS


# You need to implement two resources: Brevet and Brevets.
# Uncomment when done:
from resources.brevet import Brevet
from resources.brevets import Brevets



# Connect MongoEngine to mongodb
mongo_db = os.environ['MONGODB_HOSTNAME']
connect(host="mongodb://"+mongo_db+":27017/brevetsdb")
#{os.environ['MONGODB_HOSTNAME']}

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5002"}})  
# It looks like this should connect the two resources and let them run together?

################

# Bind resources to paths here:
# api.add_resource(...)
api.add_resource(Brevet, "/api/brevet/<string:brevet_id>") 
# I think <string:brevet_id> will let it be variable
api.add_resource(Brevets, "/api/brevets") 



if __name__ == "__main__":
    # Run flask app normally
    # Read DEBUG and PORT from environment variables.
    port = os.environ['PORT']

    # TODO Im not confident in this commented part, but if it works, include it
    #debug = os.environ['DEBUG']
    #if debug:
    #    app.logger.setLevel(logging.DEBUG)

    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
