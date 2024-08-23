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


## Adding Data

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
## Update Data

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
## Deleting Data

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