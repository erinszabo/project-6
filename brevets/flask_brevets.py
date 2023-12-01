"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
#from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
import os
import pymongo

#from pymongo import MongoClient

###
# Globals
###

app = flask.Flask(__name__)
CONFIG = config.configuration()

client = pymongo.MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

db = client.brevets
collection = db.collection 


##################################################
################## Flask routes ################## 
##################################################

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.get("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    control_dist = flask.request.args.get('control', None, type=float)
    start_time = flask.request.args.get('start', None, type=arrow.get)
    brevet_dist = flask.request.args.get('brevet', None, type=int)


    app.logger.debug(f"control={control_dist}")
    app.logger.debug(f"request.args: {flask.request.args}")

    open_time = acp_times.open_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    return {"open": open_time, "close": close_time}


###
# Buttons
###


@app.post('/submit')
def submit():
  try:
    collection.controls.insert_one(flask.request.json)
    return {"success": True}
  
  except:
    message = "Unknown Error"
    response = flask.jsonify({"error": message,
                              "success": False})
    return response



@app.get('/display')
def display():
  try:
    controls = collection.controls.find_one(
        sort=[('_id', -1)], # -1 so I get the most recent brevet 
        projection={"_id": 0} )
        # after lots of googling I realized the issue was that it was including the id
        # and found in this link how to make it exclude id
        # https://stackoverflow.com/questions/48294613/mongo-find-function-wont-exc    
        
    if controls is not None:
        # this is not working, for some reason controls is not None
        # but there are no controls submitted?
        return controls
    else: 
        message = "Zero brevets have been submitted."
        return flask.jsonify({"error": message,
                              "success": False})

  except:
    message = "Unknown Error." # server error I think but not sure
    return flask.jsonify({"error": message,
                          "success": False})

# nothing needs to change here, front end staying exactly the same 
#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
