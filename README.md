# REST API for air pollution data

This application makes the air-pollution dataset from
https://www.kaggle.com/datasets/rejeph/air-pollution accessible.
It provides a landing page where the user can select a country
from the dataset, the air pollutant and a year range (optional).
Selecting the parameters and pressing "Go" directs the user to a result page,
showing the mean, median, and standard deviation for 7 core airpollution parameters.

## Project Setup

The project is packaged within a docker container. The project structure is:

```
air_pollution_project
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── data
│   ├── air-pollution.csv
│   ├── air-pollution_cleaned.csv
│   └── check_clean_airpollution.py
├── src
│   ├── app
│   │   ├── airpollution.db
│   │   ├── main.py
│   │   └── __init__.py
│   └── setup_database
│       ├── load_data.py
│       ├── models.py
│       ├── verify_data.py
│       └── __init__.py
└── tests
    ├── test_main.py
    └── __init__.py
```


### Root Directory



- **Dockerfile**: Instructions to build a Docker image for the project.

- **Makefile**: Automates build tasks.

- **poetry.lock**: Ensures exact versions of dependencies.

- **pyproject.toml**: Configuration for Poetry.

- **README.md**: Project overview and instructions.



### [`data`](command:_github.copilot.openSymbolFromReferences?%5B%22data%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22Untitled-2%22%2C%22_sep%22%3A1%2C%22external%22%3A%22untitled%3AUntitled-2%22%2C%22path%22%3A%22Untitled-2%22%2C%22scheme%22%3A%22untitled%22%7D%2C%22pos%22%3A%7B%22line%22%3A23%2C%22character%22%3A28%7D%7D%5D%5D "Go to definition") Directory



- **air-pollution.csv**: Raw air pollution data.

- **air-pollution_cleaned.csv**: Cleaned air pollution data.

- **check_clean_airpollution.py**: Script to clean and verify data.



### `src` Directory



- **`app` Directory**:

  - **airpollution.db**: SQLite database file.

  - **main.py**: Main application script to control FastAPI REST API.

  - **__init__.py**: Initialization file for the `app` package.



- **`setup_database` Directory**:

  - **load_data.py**: Script to load data into the database.
It populates the airpollution.db from the data/air-pollution_cleaned.csv file,
  after downloading data from https://www.kaggle.com/datasets/rejeph/air-pollution?resource=download and cleaning it with data/check_clean_airpollution.py

  - **models.py**: SQLAlchemy models for database tables.
  Script to define the database schema and to set up the connection to the SQLite database airpollution.db using SQLAlchemy.

  - **verify_data.py**: Script to verify that the database has been populated.

  - **__init__.py**: Initialization file for the `setup_database` package.



### `tests` Directory



- **test_main.py**: Unit tests for the main application logic.

- **__init__.py**: Initialization file for the `tests` package.



## Application Execution

To start the application from within docker, you need the docker daemon to run.

```
#Go to directory containing “Dockerfile”, build docker container by running in terminal:
docker build -t hvv_docker .

#Running the app in docker while exposing the logs folder
docker run -d -p 8000:8000 -v "$(pwd)/logs:/app/src/app/logs" hvv_docker

```
Your app is now running at http://localhost:8000/.
The app is equipped with a logging documentation, which you can access via

```
cat logs/app.log
```


To stop the container, head back to the terminal where docker is running and press ctrl+c.

## Adding Data to Database

Adding data with curl

```
curl -X POST "http://localhost:8000/data" -H "Content-Type: application/json" -d '{
  "entity": "An Example Entity",
  "year": 2023,
  "nitrogen_oxide": 10.5,
  "sulphur_dioxide": 5.2,
  "carbon_monoxide": 3.1,
  "organic_carbon": 2.0,
  "nmvoc": 1.5,
  "black_carbon": 0.8,
  "ammonia": 0.6
}'
```

Adding data with windows powershell

```
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    entity = "An Example Entity"
    year = 2023
    nitrogen_oxide = 100.5
    sulphur_dioxide = 50.2
    carbon_monoxide = 30.1
    organic_carbon = 20.0
    nmvoc = 10.5
    black_carbon = 00.8
    ammonia = 00.6
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/data" -Method POST -Headers $headers -Body $body
```

Please remember, if you are executing this app from within docker, to add an entry to the database, execute the curl command via docker:
```
#get docker container ID
docker ps
# add entry
docker exec -it <your docker container ID> curl -X POST "http://localhost:8000/data" -H "Content-Type: application/json" -d '{\"entity\": \"An Example Entity\", \"year\": 2023, \"nitrogen_oxide\": 10.5, \"sulphur_dioxide\": 5.2, \"carbon_monoxide\": 3.1, \"organic_carbon\": 2.0, \"nmvoc\": 1.5, \"black_carbon\": 0.8, \"ammonia\": 0.6}'
```
## Update Database

Updating data with curl:
```
curl -X PUT "http://localhost:8000/data/An%Example%20Entity/2023" -H "Content-Type: application/json" -d '{
  "entity": "An Example Entity",
  "year": 2023,
  "nitrogen_oxide": 12.0,
  "sulphur_dioxide": 6.0,
  "carbon_monoxide": 4.0,
  "organic_carbon": 2.5,
  "nmvoc": 1.8,
  "black_carbon": 0.9,
  "ammonia": 0.7
}'
```

Updating data with windows powershell:
```
$entity = "An Example Entity"
$year = 2023
$url = "http://localhost:8000/data/$($entity)/$($year)"  

$headers = @{
    "Content-Type" = "application/json"
}  

$body = @{
    entity = $entity
    year = $year
    nitrogen_oxide = 12.0
    sulphur_dioxide = 6.0
    carbon_monoxide = 4.0
    organic_carbon = 2.5
    nmvoc = 1.8
    black_carbon = 0.9
    ammonia = 0.7
} | ConvertTo-Json  

$response = Invoke-WebRequest -Uri $url -Method PUT -Headers $headers -Body $body  

# Output the response
$response.Content
```

Please remember, if you are executing this app from within docker, to update an entry in the database, execute the curl command via docker:
```
#get docker container ID
docker ps
# update entry
docker exec -it <your docker container ID> curl -X PUT "http://localhost:8000/data/An%20Example%20Entity/2023" -H "Content-Type: application/json" -d '{\"entity\": \"An Example Entity\", \"year\": 2023, \"nitrogen_oxide\": 100.5, \"sulphur_dioxide\": 55.2, \"carbon_monoxide\": 34.1, \"organic_carbon\": 27.0, \"nmvoc\": 1.5, \"black_carbon\": 0.8, \"ammonia\": 0.6}'
```
## Deleting Data from Database

Delete data with curl

```
curl -X DELETE "http://localhost:8000/data/An%Example%20Entity/2023"
```

Delete data with windows powershell
```
# Define the entity and year to delete
$entity = "An Example Entity"
$year = 2023  

# Construct the URL for the DELETE request
$url = "http://localhost:8000/data/$($entity)/$($year)"

# Send the DELETE request
$response = Invoke-WebRequest -Uri $url -Method DELETE

# Check the response status
if ($response.StatusCode -eq 200) {
    Write-Output "Data point for $entity in $year has been deleted successfully."
} else {
    Write-Output "Failed to delete data point. Status code: $($response.StatusCode)"
}
```
Please remember, if you are executing this app from within docker, to delete an entry in the database, execute the curl command via docker:
```
#get docker container ID
docker ps
# delete entry
docker exec -it <your docker container ID> curl -X DELETE "http://localhost:8000/data/An%20Example%20Entity/2023"
```

## Initial Setup of the Database

The dataset from https://www.kaggle.com/datasets/rejeph/air-pollution was
initially checked and missing data (country codes) were manually cleaned.
The output is stored under data/air-pollution_cleaned.csv. The editing is
documented in data/check_clean_airpollution.py.

In order to demonstrate the app's interaction with a database, an SQLite
database, airpollution.db was created from data/air-pollution_cleaned.csv.
The interaction with the DB is performed via SQLAlchemy, which is a SQL toolkit library for
Python. It is used here to create the database, manage database sessions and to
query the database.
To setup the database, execute the scripts setup_database/models.py and
setup_models/load_data.py. If you want to check that the database has been
filled, run setup_models/verify_data.py.
