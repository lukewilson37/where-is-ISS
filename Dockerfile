FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT05.xml

COPY requirements.txt /app/requirements.txt
COPY python_requirements.txt /app/python_requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip3 install -r /app/python_requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]

