# UO CS322 - Project 6 #
## Erin Szabo
#### Fall 2023
### eszabo@uoregon.edu

Brevet time calculator with MongoDB, and a RESTful API!


## Review

For an understanding of the calculator itself, vist 
 - https://github.com/erinszabo/project-4
 - https://github.com/erinszabo/project-5

## Overview
This is a continuation of project 5, except...

## Now using Flask RESTful

* Summary of RESTful API in `api/`:
	* The following describes the new data schema using MongoEngine for Checkpoints and Brevets:
		* `Checkpoint`:
			* `distance`: float, required, (checkpoint distance in kilometers), 
			* `location`: string, optional, (checkpoint location name), 
			* `open_time`: datetime, required, (checkpoint opening time), 
			* `close_time`: datetime, required, (checkpoint closing time).
		* `Brevet`:
			* `length`: float, required, (brevet distance in kilometers),
			* `start_time`: datetime, required, (brevet start time),
			* `checkpoints`: list of `Checkpoint`s, required, (checkpoints).
	* resource `/brevets/`:
		* GET `http://API:PORT/api/brevets` should display all brevets stored in the database.
	
		* POST `http://API:PORT/api/brevets` should insert brevet object in request into the database.
		
	* resource `/brevet/ID`:
		* GET `http://API:PORT/api/brevet/ID` should display brevet with id `ID`.
		* DELETE `http://API:PORT/api/brevet/ID` should delete brevet with id `ID`.
		* PUT `http://API:PORT/api/brevet/ID` should update brevet with id `ID` with object in request.

* `brevets/` copied from completed project 5.
	* Every database related code in `brevets/` is replaced with calls to the new API.
		
	* Now `env.` is used exclusivly and `config.py` has been removed




## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
