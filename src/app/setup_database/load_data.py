# Importing pandas for data manipulation and analysis
import pandas as pd

# Importing Session for database session management
from sqlalchemy.orm import Session

# Importing the AirPollutionData model and SessionLocal session factory
from app.setup_database.models import AirPollutionData, SessionLocal


def load_data() -> None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv("../../../data/air-pollution_cleaned.csv")

    # Remove any leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # Create a new database session
    db: Session = SessionLocal()

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Create a new AirPollutionData object for each row
        db_item = AirPollutionData(
            entity=row["Entity"],
            code=row["Code"],
            year=row["Year"],
            nitrogen_oxide=row["Nitrogen oxide (NOx)"],
            sulphur_dioxide=row["Sulphur dioxide (SO₂) emissions"],
            carbon_monoxide=row["Carbon monoxide (CO) emissions"],
            organic_carbon=row["Organic carbon (OC) emissions"],
            nmvoc=row["Non-methane volatile organic compounds (NMVOC) emissions"],
            black_carbon=row["Black carbon (BC) emissions"],
            ammonia=row["Ammonia (NH₃) emissions"],
        )

        # Add the new object to the session
        db.add(db_item)

        # Commit the session to save the objects to the database
    db.commit()

    # Close the session
    db.close()


if __name__ == "__main__":
    # Call the load_data function when the script is executed
    load_data()
