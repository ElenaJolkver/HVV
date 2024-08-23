from sqlalchemy import Column, Integer, String, Float, create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class AirPollutionData(Base):
    __tablename__ = 'air_pollution_data'

    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, index=True)
    code = Column(String)
    year = Column(Integer)
    nitrogen_oxide = Column(Float)
    sulphur_dioxide = Column(Float)
    carbon_monoxide = Column(Float)
    organic_carbon = Column(Float)
    nmvoc = Column(Float)
    black_carbon = Column(Float)
    ammonia = Column(Float)


DATABASE_URL = "sqlite:///./data/airpollution.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
