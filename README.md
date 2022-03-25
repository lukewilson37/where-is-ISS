# Where is the International Space Station?

## *The Flask Application that can help you track the worlds most famous spacecraft*

### Description

This project aims to produce a containerized flask application that can be used to organize and gather public data on the location of ISS. The project utilizes Flask and Docker with their various dependencies to create such an application. 

The source code for the project can be pulled with:
```bash
$ git pull https://github.com/lukewilson37/where-is-ISS.git
```


### Accessing the Data

If we want to track teh ISS, we are going to need some data on its whereabouts. For this we look to NASA's Open Data Portal. The portal's website can be found [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq). We will gether the public distribution file and one of the sightings files to do our analysis. You can download these two files from the command line with
```bash
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
```
```bash
$ wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT05.xml
```
These files will be parsed and orgonized for retreival by an application user.

### Building the Container

Inside the source code you will find a ```Dockerfile```. This is the main script you will use to build your container. Many commands using Docker can get very logn and cumbersome to always recall. Because of that we use a ```Makefile``` to automate some of the process for us. Now, instead of having to type
```bash
$ docker build -t ${NAME}/whereisiss-flask:latest .
```
we only need to writre
```bash
$ make build
```
Note to use the ```Makefile``` properly you will need to adjust its first line 
```bash
NAME ?= <yourDockerName>
```
When it comes to the ```Dockerfile``` we should be mindful of a couple things. First, note we use the ```wget``` command twice in order to pull the data mentioned above. If you do not want this data, or want different data (from the same [site](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq)), you can edit ```Dockerfile``` to do so. Also note the two requirement files ```requirements.txt``` and ```python_requirements```. The formal contains all the command line packages we will need and the latter the python packages. Finally, note the entry point ```CMD ["app.py"]```. If you are looking to use any different scripts for the flask app, this line must be changed.

### Pulling a Container

You may also want to pull a working container from the web. This can be done with the general command:
```bash
$ docker pull docker.io/username/whereisiss-flask:version
```
To pull my most recent working container:
```
$ docker pull docker.io/lukewilson37/whereisiss-flask
```

### Interacting with Flask

To start the flask application on ```isp02``` you will run
```bash
$ make build
$ make run
```
This runs the container on containerized flask application on port ```5037```. If you with to use a different port, you can edit the build command in the makefile.
Once the application is running in the background, we can now interact with it inline. To do so we use ```curl```. there are 9 curl commands you can use to interact with the application most of which return dictionaries.
```bash
$ curl localhost:5037/                              # returns this README.md
$ curl localhost:5037/epochs                        # returns list of epoch_ids
$ curl localhost:5037/<epoch_id>.                   # returns epoch data
$ curl localhost:5037/countries                     # returns list of countries
$ curl localhost:5037/<country>                     # returns sightings in country
$ curl localhost:5037/<country>/regions             # returns list of regions in country
$ curl localhost:5037/<country>/<region>            # returns sightings in region
$ curl localhost:5037/<country>/<region>/cities     # returns list of cities in region
$ curl localhost:5037/<country>/<region>/<city>     # returns sighting in city
```
These are the commands used to interact with the application.

