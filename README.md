# REST API for air pollution data

This application makes the air-pollution dataset from https://www.kaggle.com/datasets/rejeph/air-pollution accessible. It provides a landing page where the user can select a country from the dataset, the air pollutant and a year range (optional). Selecting the parameters and pressing "Go" directs the user to a result page.

## Project Setup

air_pollution_project/

├── main.py

├── models.py

├── load_data.py

├── verify_data.py

├── data/air-pollution.csv

└── airpollution.db

main.py script to control FastAPI REST API
models.py is responsible for defining the database schema and setting up the connection to the SQLite database airpollution.db using SQLAlchemy.
load_data.py script populates the airpollution.db from the data/air-pollution.csv file, downloaded from https://www.kaggle.com/datasets/rejeph/air-pollution?resource=download
verify_data.py checks that the database has been populated properly

## Application Execution

start application with uvicorn main:app --reload

