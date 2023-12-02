"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations

import logging
import os
import pymongo


###
# Globals
###

app = flask.Flask(__name__)


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
#######
# Replace every database related code in brevets/ with calls to the new API.
# Remember: AutoGrader will ensure there is NO CONNECTION between brevets and db services. 
#  brevets should only operate through api and still function the way it did in project 5.
# Hint: Submit should send a POST request to the API to insert, Display should send a GET request, 
#  and display the last entry.

# The post in api/resources/brevets.py should replace my submit
# pose function below. so have the button call that instead?

# The get I have here only gets the most recent, so I should have the 
# display button call get in api/resources/brevet.py with the most recent id


#############

if __name__ == "__main__":
    port = os.environ["PORT"]
    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
