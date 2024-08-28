# Importing necessary SQLAlchemy components for defining models and creating the engine
from sqlalchemy import Column, Float, Integer, String, create_engine

# Importing sessionmaker for session creation and declarative_base for model base class
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

# Create a base class for declarative class definitions
Base: DeclarativeMeta = declarative_base()


# Define the AirPollutionData model
class AirPollutionData(Base):
    __tablename__ = "air_pollution_data"  # Name of the table in the database

    # Define columns in the table
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    entity = Column(String, index=True)  # Entity column with an index
    code = Column(String)  # Code column
    year = Column(Integer)  # Year column
    nitrogen_oxide = Column(Float)  # Nitrogen oxide emissions column
    sulphur_dioxide = Column(Float)  # Sulphur dioxide emissions column
    carbon_monoxide = Column(Float)  # Carbon monoxide emissions column
    organic_carbon = Column(Float)  # Organic carbon emissions column
    nmvoc = Column(Float)  # Non-methane volatile organic compounds emissions column
    black_carbon = Column(Float)  # Black carbon emissions column
    ammonia = Column(Float)  # Ammonia emissions column


# Database URL for SQLite database
DATABASE_URL = "sqlite:///./../airpollution.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
