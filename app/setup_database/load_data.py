import pandas as pd

from sqlalchemy.orm import Session

from models import AirPollutionData, SessionLocal


def load_data():
    df = pd.read_csv('../../data/air-pollution.csv')

    df.columns = df.columns.str.strip()  # Remove any leading/trailing whitespace from column names

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        db_item = AirPollutionData(

            entity=row['Entity'],

            code=row['Code'],

            year=row['Year'],

            nitrogen_oxide=row['Nitrogen oxide (NOx)'],

            sulphur_dioxide=row['Sulphur dioxide (SO₂) emissions'],

            carbon_monoxide=row['Carbon monoxide (CO) emissions'],

            organic_carbon=row['Organic carbon (OC) emissions'],

            nmvoc=row['Non-methane volatile organic compounds (NMVOC) emissions'],

            black_carbon=row['Black carbon (BC) emissions'],

            ammonia=row['Ammonia (NH₃) emissions']

        )

        db.add(db_item)

    db.commit()

    db.close()


if __name__ == "__main__":
    load_data()