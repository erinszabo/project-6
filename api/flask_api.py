"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect

# You need to implement two resources: Brevet and Brevets.
# Uncomment when done:
from resources.brevet import Brevet
from resources.brevets import Brevets



# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)

# Bind resources to paths here:
# api.add_resource(...)
api.add_resource(Brevet, "/api/brevet/<string:brevet_id>") # brevet resource
api.add_resource(Brevets, "/api/brevets") # brevets resource



if __name__ == "__main__":
    # Run flask app normally
    # Read DEBUG and PORT from environment variables.
    port = os.environ['API_PORT']

    # TODO Im not confident in this commented part, but if it works, include it
    #debug = os.environ['DEBUG']
    #if debug:
    #    app.logger.setLevel(logging.DEBUG)

    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
