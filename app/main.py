# FastAPI is used to create the web application and handle HTTP requests.
from fastapi import FastAPI, Form, Depends

# HTMLResponse and RedirectResponse are used to return HTML content and handle redirects.
from fastapi.responses import HTMLResponse, RedirectResponse

# SQLAlchemy ORM is used to interact with the database in an object-oriented way.
from sqlalchemy.orm import sessionmaker, Session

# SQLAlchemy core is used to create the database engine and perform SQL queries.
from sqlalchemy import create_engine, select, func, text

# Importing the database models and session configuration.
from app.setup_database.models import AirPollutionData, SessionLocal, Base

# Pandas is used for data manipulation and analysis.
import pandas as pd

# OS module is used to handle file paths and directory operations.
import os

# Initialize the FastAPI application.
app = FastAPI()

# Define the path to the database, construct the database URL using the file path.
db_path = os.path.join(os.path.dirname(__file__), 'airpollution.db')

# Define the database URL for SQLAlchemy.
DATABASE_URL = f"sqlite:///{db_path}"

# Create the database engine with SQLite.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configure the session class for database interactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables based on the models.
Base.metadata.create_all(bind=engine)





def get_db():
    # Create a new database session.
    db = SessionLocal()
    try:
        yield db        # Yield the session for dependency injection.

    finally:
        db.close()      # Ensure the session is closed after use.


@app.get("/", response_class=HTMLResponse)
async def main(db: Session = Depends(get_db)):
    # Query distinct entities from the database.
    entities = db.execute(select(AirPollutionData.entity).distinct()).fetchall()

    # Generate HTML options for the entities.
    entity_options = "".join([f'<option value="{entity[0]}">{entity[0]}</option>' for entity in entities])

    # Generate the HTML content for the form.
    content = f"""   

    <body>   

      <header>   

        <h1>Welcome to Air Pollution Data Viewer</h1>   

        <p>Select an entity, parameter, and optionally a year range to view the summary statistics</p>   

      </header>   

      <form action="/get_stats/" method="post">   

        <label for="entity">Select an entity:</label>   

        <select name="entity" id="entity">   

          {entity_options}   

        </select>   

        <br><br>   

        <label for="parameter">Select a parameter:</label>   

        <select name="parameter" id="parameter">   

          <option value="nitrogen_oxide">Nitrogen oxide (NOx)</option>   

          <option value="sulphur_dioxide">Sulphur dioxide (SO₂) emissions</option>   

          <option value="carbon_monoxide">Carbon monoxide (CO) emissions</option>   

          <option value="organic_carbon">Organic carbon (OC) emissions</option>   

          <option value="nmvoc">Non-methane volatile organic compounds (NMVOC) emissions</option>   

          <option value="black_carbon">Black carbon (BC) emissions</option>   

          <option value="ammonia">Ammonia (NH₃) emissions</option>   

        </select>   

        <br><br>   

        <label for="start_year">Select start year (optional):</label>   

        <input type="number" name="start_year" id="start_year" min="1750" max="2022">   

        <br><br>   

        <label for="end_year">Select end year (optional):</label>   

        <input type="number" name="end_year" id="end_year" min="1750" max="2022">   

        <br><br>   

        <input type="submit" value="GO">   

      </form>   

    </body>   

    """

    # Return the HTML content as a response.
    return HTMLResponse(content=content)


@app.post("/get_stats/")
async def get_stats(entity: str = Form(...), parameter: str = Form(...), start_year: int = Form(None),
                    end_year: int = Form(None)):
    if parameter in ["nitrogen_oxide", "sulphur_dioxide", "carbon_monoxide", "organic_carbon", "nmvoc", "black_carbon",
                     "ammonia"]:

        if start_year and end_year:

            if start_year < 1750 or end_year > 2022:
                return HTMLResponse(content="<p>Year range must be between 1750 and 2022</p>")

            return RedirectResponse(url=f"/data/{entity}/{start_year}/{end_year}/{parameter}/stats", status_code=303)

        else:

            return RedirectResponse(url=f"/data/{entity}/all/{parameter}/stats", status_code=303)

    else:

        return HTMLResponse(content="<p>Invalid parameter selected</p>")


@app.get("/data/{entity}/{start_year}/{end_year}/{parameter}/stats", response_class=HTMLResponse)
async def get_stats(entity: str, start_year: int, end_year: int, parameter: str, db: Session = Depends(get_db)):
    data = db.query(AirPollutionData).filter(

        AirPollutionData.entity == entity,

        AirPollutionData.year >= start_year,

        AirPollutionData.year <= end_year

    ).all()

    if not data:
        return HTMLResponse(content="<p>Data not found</p>")

    df = pd.DataFrame([d.__dict__ for d in data])

    mean = df[parameter].mean()

    median = df[parameter].median()

    stddev = df[parameter].std()

    return HTMLResponse(content=f""" 

    <p>Statistics for {parameter.replace('_', ' ')} for {entity} from {start_year} to {end_year}:</p> 

    <ul> 

        <li>Mean: {mean}</li> 

        <li>Median: {median}</li> 

        <li>Standard Deviation: {stddev}</li> 

    </ul> 

    """)




@app.get("/data/{entity}/all/{parameter}/stats", response_class=HTMLResponse)
async def get_stats_all(entity: str, parameter: str, db: Session = Depends(get_db)):
    # Define the route to display statistics for all years.

    # Calculate the mean for the parameter directly in the database.
    mean = db.query(func.avg(getattr(AirPollutionData, parameter))).filter(AirPollutionData.entity == entity).scalar()

    # Custom SQL query to calculate the median
    median_query = text(f""" 
        SELECT {parameter} FROM air_pollution_data 
        WHERE entity = :entity 
        ORDER BY {parameter} 
        LIMIT 1 OFFSET (SELECT COUNT(*) FROM air_pollution_data WHERE entity = :entity) / 2 
    """)

    median_result = db.execute(median_query, {"entity": entity}).fetchone()
    median = median_result[0] if median_result else None

    # Custom SQL query to calculate the standard deviation
    stddev_query = text(f""" 
        SELECT sqrt(avg((t.{parameter} - m.avg_{parameter}) * (t.{parameter} - m.avg_{parameter}))) as stddev
        FROM air_pollution_data t,  
        (SELECT avg({parameter}) as avg_{parameter} FROM air_pollution_data WHERE entity = :entity) m 
        WHERE t.entity = :entity 
    """)

    stddev_result = db.execute(stddev_query, {"entity": entity}).fetchone()
    stddev = stddev_result[0] if stddev_result else None

    # Return an error message if no data is found.
    if mean is None or median is None or stddev is None:
        return HTMLResponse(content="<p>Data not found</p>")

    # Return the statistics as an HTML response.
    return HTMLResponse(content=f""" 
    <p>Statistics for {parameter.replace('_', ' ')} for {entity} for all years:</p> 
    <ul> 
        <li>Mean: {mean}</li> 
        <li>Median: {median}</li> 
        <li>Standard Deviation: {stddev}</li> 
    </ul> 
    """)


if __name__ == "__main__":
    # Uvicorn is used to run the FastAPI application.
    import uvicorn

    # Run the FastAPI application on host 0.0.0.0 and port 8000.
    uvicorn.run(app, host="0.0.0.0", port=8000)

