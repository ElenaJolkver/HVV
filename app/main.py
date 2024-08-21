from fastapi import FastAPI, Form, Depends

from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session

from app.models import AirPollutionData, SessionLocal, engine, Base

import pandas as pd

import os

app = FastAPI()

# Define the path to the database


db_path = os.path.join(os.path.dirname(__file__), 'airpollution.db')

DATABASE_URL = f"sqlite:///{db_path}"


# Create the SQLAlchemy engine

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Create a configured "Session" class

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


@app.get("/", response_class=HTMLResponse)
async def main(db: Session = Depends(get_db)):
    entities = db.query(AirPollutionData.entity).distinct().all()

    entity_options = "".join([f'<option value="{entity[0]}">{entity[0]}</option>' for entity in entities])

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
    data = db.query(AirPollutionData).filter(AirPollutionData.entity == entity).all()

    if not data:
        return HTMLResponse(content="<p>Data not found</p>")

    df = pd.DataFrame([d.__dict__ for d in data])

    mean = df[parameter].mean()

    median = df[parameter].median()

    stddev = df[parameter].std()

    return HTMLResponse(content=f""" 

    <p>Statistics for {parameter.replace('_', ' ')} for {entity} for all years:</p> 

    <ul> 

        <li>Mean: {mean}</li> 

        <li>Median: {median}</li> 

        <li>Standard Deviation: {stddev}</li> 

    </ul> 

    """)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000) 