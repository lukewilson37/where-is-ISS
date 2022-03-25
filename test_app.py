import pytest
import app

from app import initialize_data
from app import return_epochs
from app import return_sightings
from app import return_epoch_ids
from app import return_epoch_info
from app import return_countries
from app import return_country_info
from app import return_regions
from app import return_region_info
from app import return_cities
from app import return_city_info

def test_initialize_data():
	# define global varibales to be used throuhout the test
	# we do this so we dont have to fetch data everytime we test a function
	global epochs
	global sightings
	initialize_data()
	epochs = return_epochs()
	sightings = return_sightings()
	assert(len(epochs) > 1)
	assert(len(sightings) > 1)
	
def test_return_epoch_ids():
	assert(len(return_epoch_ids()['epoch_ids']) > 0)
	# all epoch ids have a length of 22
	assert(len(return_epoch_ids()['epoch_ids'][1]) == 22)

def test_return_epoch_info():
	test_id = return_epoch_ids()['epoch_ids'][1]
	# each epoch key has is paired to a list of 7 dictionaries.	
	assert(len(return_epoch_info(test_id)) == 7)
	# this tests if 'Z_DOT' key exists (which it should)
	# also tests that there are two items in list paired
	assert(len(return_epoch_info(test_id)['Z_DOT']) == 2)
	
def test_return_countries():
	# hard to run tests on a list of names. We check that its not empty.
	assert(len(return_countries()['countries']) > 0)

def test_return_country_info():
	test_country = return_countries()['countries'][0]	
	assert(len(return_country_info(test_country)[test_country]) > 0)
	# this checks for the 'utc_time' key. also makes sure its has length5
	# len("18:30") == 5
	assert(len(return_country_info(test_country)[test_country][0]['utc_time']) == 5)

def test_return_regions():
	test_country = return_countries()['countries'][0]
	assert(len(return_regions(test_country)['regions']) > 0)

def test_return_region_info():
	test_country = return_countries()['countries'][0]
	test_region = return_regions(test_country)['regions'][0]	
	assert(len(return_region_info(test_country,test_region)[test_region]) > 0)
	assert(len(return_region_info(test_country,test_region)[test_region][0]['utc_time']) == 5)

def test_return_cities():
	test_country = return_countries()['countries'][0]
	test_region = return_regions(test_country)['regions'][0]
	assert(len(return_cities(test_country,test_region)['cities']) > 0)

def test_return_city_info():
	# as we go on, we need more test variables. 
	test_country = return_countries()['countries'][0]
	test_region = return_regions(test_country)['regions'][0]
	test_city = return_cities(test_country,test_region)['cities'][0]	
	assert(len(return_city_info(test_country,test_region,test_city)[test_city]) > 0)
	assert(len(return_city_info(test_country,test_region,test_city)[test_city][0]['utc_time']) == 5)



	
