# REST API for air pollution data

This application makes the air-pollution dataset from 
https://www.kaggle.com/datasets/rejeph/air-pollution accessible. 
It provides a landing page where the user can select a country 
from the dataset, the air pollutant and a year range (optional).
Selecting the parameters and pressing "Go" directs the user to a result page, 
showing the mean, median, and standard deviation for 7 core airpollution parameters.

## API Framework

To implement the REST API for accessing an example database and demonstrating 
basic functionalities, the Python framework FastAPI has been selected. 
is a state-of-the-art choice for developing fast, lightweight web applications.

FastAPI is designed for high performance, leveraging Python's asynchronous 
capabilities to efficiently handle concurrent requests. This makes it ideal for 
building APIs that need to scale. Its performance rivals that of Node.js and Go, 
thanks to its use of Starlette and Pydantic. FastAPI is one of the fastest 
Python frameworks available, allowing for the creation of production-ready code 
and automatic interactive documentation. Additionally, it is based on and fully 
compatible with open standards for APIs, such as OpenAPI (formerly Swagger) 
and JSON Schema.

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
 

## Security Measures

Protecting access to the API and underlying database from unauthorized users 
and potential threats is critical. The security measures outlined below are 
categorized into API access control, database protection, and monitoring and 
testing.

The implemented case study protects the database by using Pydantic models and by performing  
database interactions via SQLAlchemy ORM. It also makes use of logging. Further security
measures as outlined below need to be implemented before exposing the application to the real world.

### API Access

#### Authentication
To protect the application from unauthorized access, secure authentication 
mechanisms must be in place. One common and robust method is 
**OAuth2 with JWT (JSON Web Tokens)**, which provides secure, stateless 
authentication. Upon successful authentication, the user receives a JWT token, 
which is included in each request. FastAPI verifies this token to authenticate 
the user. This method is widely adopted for securing APIs.

#### Authorization
Beyond authentication, **Role-Based Access Control (RBAC)** can be implemented 
to enforce authorization policies. For instance, only users with the 'admin' 
role may be allowed to access DELETE endpoints. This ensures that only users 
with the appropriate permissions can perform certain actions. Although not 
implemented in the case study, **Access Control Lists (ACLs)** can further 
refine permissions by allowing or denying access to specific resources based 
on user roles or groups.

#### Rate Limiting
To mitigate **Denial of Service (DoS) attacks**, which aim to overload the 
API by flooding it with excessive requests, rate limiting should be implemented. 
Rate limiting controls the number of requests a user can make within a specified 
time frame, protecting your API from abuse. This can be implemented in FastAPI 
using frameworks like `fastapi-limiter` or by leveraging external services such 
as Redis for rate limiting management.

#### Secure API Documentation
By default, FastAPI provides publicly accessible interactive documentation 
(e.g., Swagger UI). In a production environment, it is crucial to secure 
or disable this documentation to prevent unauthorized access to API endpoints 
and potential security vulnerabilities.

### Database Protection

#### SQL Injection Prevention
**SQL injection** is a common attack vector that targets databases by 
injecting malicious SQL code through user inputs. To safeguard the database 
from such attacks, input validation and sanitization are essential. 
FastAPI's integration with **Pydantic models** allows for strict input 
validation, ensuring that only data conforming to the expected type and 
format is accepted. Restricting input length and types further strengthens 
this defense.

Sanitization involves filtering and cleaning input data to eliminate any 
potentially harmful content. This can be achieved using 
**parameterized queries** and escaping special characters to 
prevent them from being interpreted as executable code. 
Additionally, using an ORM (Object-Relational Mapping) tool like 
**SQLAlchemy** or **Tortoise-ORM** abstracts the database interactions, 
reducing the risk of SQL injection by avoiding direct SQL query execution.

#### Secure Data Transmission
To protect data during transit between the application and the database, 
**Man-in-the-Middle (MITM) attacks** must be mitigated. This is especially 
critical if the database contains sensitive information. Ensuring secure 
communication can be achieved by serving the FastAPI application over 
**HTTPS** (using TLS/SSL). Implementing a **Strict-Transport-Security (HSTS)** 
header ensures that browsers communicate with the server only over HTTPS, even 
if the user attempts to access the site via HTTP.

### Monitoring and Testing

#### Logging and Monitoring
Even with the aforementioned security measures in place, continuous monitoring 
of the system for suspicious activity is crucial. This includes logging all 
significant actions and security-related events, such as failed login attempts 
and data modifications. Tracking API usage and identifying anomalies in real-time
can help detect and respond to potential security threats promptly.

#### Penetration Testing
After implementing these security measures, it is advisable to conduct 
**penetration testing** to uncover any vulnerabilities. Penetration testing 
simulates attacks on the system to identify and address weaknesses before they 
can be exploited by malicious actors.
