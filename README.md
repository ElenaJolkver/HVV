# REST API for air pollution data

This application makes the air-pollution dataset from https://www.kaggle.com/datasets/rejeph/air-pollution accessible. It provides a landing page where the user can select a country from the dataset, the air pollutant and a year range (optional). Selecting the parameters and pressing "Go" directs the user to a result page.

## Project Setup

The project is packaged within a docker container. The project structure is:

```
air_pollution_project
│   README.md
│   requirements.txt
│   Dockerfile    
│
└───app
│   │   main.py
│   │
│   └───setup_database
│       │   models.py
│       │   load_data.py
│       │   verify_data.py
│   
└───data
    │   air-pollution.csv

```


main.py script to control FastAPI REST API.
The other files are not needed to run the API, but were used to setup the database. 
models.py is responsible for defining the database schema and setting up the connection to the SQLite database airpollution.db using SQLAlchemy.
load_data.py script populates the airpollution.db from the data/air-pollution.csv file, downloaded from https://www.kaggle.com/datasets/rejeph/air-pollution?resource=download
verify_data.py checks that the database has been populated properly

## Application Execution

To start the application from within docker, you need the docker daemon to run.

#Go to directory containing “Dockerfile”, build docker container by running in terminal:

docker build -t hvv_docker .

#Running the app in docker
docker run -p 8000:8000  --rm hvv_docker

Your app is now running at http://localhost:8000/

#To stop the container, head back to the terminal where docker is running and press ctrl+c.
