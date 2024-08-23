from sqlalchemy.orm import Session

from app.setup_database.models import AirPollutionData, SessionLocal


def verify_data():
    db: Session = SessionLocal()

    records = db.query(AirPollutionData).limit(10).all()

    for record in records:
        print(record.__dict__)

    db.close()


if __name__ == "__main__":
    verify_data()