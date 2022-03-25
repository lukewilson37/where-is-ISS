from flask import Flask
#from flask import jsonify
import xmltodict
import requests
import json
import logging

app = Flask(__name__)

logging.basicConfig()

# initialize epochs and signtings
# epoch and sightings are global variables used throughout the app
global epochs 
epochs = {}
global sightings
sightings = {}

def read_data():
	with open('XMLsightingData_citiesINT05.xml', 'r') as f:
		SD = xmltodict.parse(f.read())

	with open('ISS.OEM_J2K_EPH.xml', 'r') as f:	
		PDF = xmltodict.parse(f.read())
	logging.info('SD and PDF variables declared')

	# we orgonize the sightings data into a embedded dictionary for data retreival purposes
	for sight in SD['visible_passes']['visible_pass']:
		country = sight['country']
		region = sight['region']
		city = sight['city']
		if country not in sightings:
			sightings[country] = {}
		if region not in sightings[country]:
			sightings[country][region] = {}
		if city not in sightings[country][region]:
			sightings[country][region][city] = []
			sightings[country][region][city].append(sight)
	
	if len(sightings) == 0:
		logging.error('Sightings Data not retreived properly')
	else:
		logging.info('Sightings retreived')	

	# store epochs data so parsing becomes much easier
	epochs_raw = PDF['ndm']['oem']['body']['segment']['data']['stateVector']   
	for index in range(len(epochs_raw)):
		epoch_id = epochs_raw[index]['EPOCH']
		epochs[epoch_id] = epochs_raw[index]
	# check if epochs is empty
	if len(epochs) == 0:
		logging.error('Public Distribution Data not retreived properly')
	else:
		logging.info('Public Distribution retreived')

def return_epochs():
	return epochs

def return_sightings():
	return sightings	
		
@app.route('/',methods=['GET'])
def hello_world():
	return 'hello, world\n'

@app.route('/init',methods=['POST'])
def initialize_data():
	"""
	The initialize_data function pulls ISS position and sightings data from the web.
	Data is formated into an embedded dictionary format that will make future data reterival easier.
	
	Args:
		No Arguments

	Returns:
		confirmation (strings): indicating the data was stored
	"""
	# Gather and store Public Distribution File
	# store raw public distribution file contents into r
	r = requests.get('https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml')
	# orgonize the raw data into a dictonary format
	PDF = xmltodict.parse(r.content) 
	# store epochs data so parsing becomes much easier
	epochs_raw = PDF['ndm']['oem']['body']['segment']['data']['stateVector']   
	for index in range(len(epochs_raw)):
		epoch_id = epochs_raw[index]['EPOCH']
		epochs[epoch_id] = epochs_raw[index]
	# check if epochs is empty
	if len(epochs) == 0:
		logging.error('Public Distribution Data not retreived properly')
	else:
		logging.info('Public Distribution retreived')
	# Gather and sort Sighting Data (SD)
	# Note we use same process as above
	r = requests.get('https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT05.xml')
	SD = xmltodict.parse(r.content)
	# we orgonize the sightings data into a embedded dictionary for data retreival purposes
	for sight in SD['visible_passes']['visible_pass']:
		country = sight['country']
		region = sight['region']
		city = sight['city']
		if country not in sightings:
			sightings[country] = {}
		if region not in sightings[country]:
			sightings[country][region] = {}
		if city not in sightings[country][region]:
			sightings[country][region][city] = []
		sightings[country][region][city].append(sight)
	if len(epochs) == 0:
		logging.error('Public Distribution Data not retreived properly')
	else:
		logging.info('Public Distribution retreived')	
	return 'stored\n'

@app.route('/epochs',methods=['GET'])
def return_epoch_ids():
	"""
	This function returns a strings of all the epoch ids.

	Args:
		No Arguments

	Returns:
		epoch_ids (dict): dictionary with one key pair. 'epoch_ids' pairs to the list of epoch_ids (strings)
	"""
	epoch_ids = {'epoch_ids':[]}
	for epoch_id in list(epochs.keys()):
		epoch_ids['epoch_ids'].append(epoch_id)
	logging.info('epoch ids viewed')
	return epoch_ids

@app.route('/epochs/<epoch_id>',methods=['GET'])
def return_epoch_info(epoch_id):
	"""
	This function returns all the information regarding a given epoch_id

	Args:
		epoch_id (dict): epoch identification 
	
	Returns:
		epoch_info (json): jsoninified dictionary of epoch info
	"""
	#epoch_info = jsonify(json.dumps(epochs[epoch_id]))
	epoch_info = epochs[epoch_id]
	logging.info('epoch ' + epoch_id + ' viewed')
	return epoch_info

@app.route('/countries',methods=['GET'])
def return_countries():
	"""
	This function returns a string of all the countries in the sightings data

	Args:
		No Arguments

	Returns:
		list of countries (dict): dictionary with one key pair. 'countries' pairs to the list of countries (strings)
	"""
	output = {'countries':[]}
	for country in list(sightings.keys()):
		output['countries'].append(country)
	logging.info('list of countries viewed')
	return output

@app.route('/<country>',methods=['GET'])
def return_country_info(country):
	"""
	This function returns all the sightings information in a certain country of the sightings data set.
	The function loops through the embedded dictionary (sightings) to find all sightings in certain country.

	Args:
		country name (string): name of requested country

	Returns:
		country info (dict): dictionary of all sightings in the desired country
	"""
	country_info = {country:[]}
	for region in list(sightings[country].keys()):
		for city in list(sightings[country][region].keys()):
			country_info[country].extend(sightings[country][region][city])
	#country_info = jsonify(json.dumps(country_info))
	logging.info(country + ' info viewed')
	return country_info

@app.route('/<country>/regions',methods=['GET'])
def return_regions(country):
	"""
	This function returns the full list of regions within a given country.

	Args: 
		country (string): country name

	Returns:
		output (dict): dictionary with one key pair. 'regions' pairs to the list of regions (strings)
	"""
	output = {'regions':[]}
	for region in list(sightings[country].keys()):
		output['regions'].append(region)
	logging.info('regions of '+ country + ' viewed')
	return output

@app.route('/<country>/<region>',methods=['GET'])
def return_region_info(country,region):
	"""
	This function returns all the sighting information of a region of a country.
	The function loops through the embedded dictionary (sightings) to find all sightings in certain country.

	Args:
		country (string): country name
		region (string): region name

	Returns:
		region_info (dict): dictionary of all sightings in desired region
	"""
	region_info = {region:[]}
	for city in list(sightings[country][region].keys()):
		region_info[region].extend(sightings[country][region][city])
	logging.info(region + ' region of ' + country + ' info viewed')
	#return jsonify(json.dumps(region_info))
	return region_info

@app.route('/<country>/<region>/cities',methods=['GET'])
def return_cities(country,region):
	"""
	This function returns a list of cities within a certain region of a country

	Args:
		country (string): country name
		region (string): region name

	Returns:
		city_list (dict): dictionary with one key pair. 'cities' pairs to the list of cities (strings)
	"""
	city_list = {'cities':[]}
	for city in list(sightings[country][region].keys()):
		city_list['cities'].append(city)
	logging.info('list of cities in ' + region + ', ' + country + ' viewed')
	return city_list

@app.route('/<country>/<region>/<city>',methods=['GET'])
def return_city_info(country,region,city):
	"""
	This function returns sighting information for a given city

	Args:
		country (string): country name
		region (string): region name
		city (string): city name

	Returns:
		city_info (dict): dictionary of all sightings in desired city	
	"""
	city_info = {city:[]}     
	city_info[city].extend(sightings[country][region][city])
	#city_info =  jsonify(json.dumps(city_info))
	logging.info(city + ', ' + country + ' info viewed')
	return city_info

if __name__ == '__main__':
	read_data()
	app.run(debug=True, host='0.0.0.0')
