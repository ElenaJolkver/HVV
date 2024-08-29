# Importing Session for database session management
# Importing the AirPollutionData model and SessionLocal session factory
from models import AirPollutionData, SessionLocal
from sqlalchemy.orm import Session


def verify_data() -> None:
    # Create a new database session
    db: Session = SessionLocal()

    # Query the first 10 records from the AirPollutionData table
    records = db.query(AirPollutionData).limit(10).all()

    # Iterate over the records and print their dictionary representation
    for record in records:
        print(record.__dict__)
        # Close the session
    db.close()


if __name__ == "__main__":
    # Call the verify_data function when the script is executed
    verify_data()
