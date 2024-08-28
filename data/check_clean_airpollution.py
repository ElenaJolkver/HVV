import os

import pandas as pd

# Set the working directory to the 'data/' directory within the FastAPI project
os.chdir(os.path.dirname(__file__))


def clean_airpollution():
    # Reading data
    air = pd.read_csv("air-pollution.csv")
    print(air.head())

    # Removing empty column
    air = air.iloc[:, :-1]

    # Summary of the data
    print(air.describe())

    # Check for missing data
    print(air.isna().sum())

    # check which entries do not have a code
    air_codes_na = air[air["Code"].isna()]
    print(air_codes_na.groupby("Entity").size().reset_index(name="count"))

    # Adding missing codes to the air dataframe
    air.loc[air["Entity"] == "Africa", "Code"] = "AFRICA"
    air.loc[air["Entity"] == "Asia", "Code"] = "ASIA"
    air.loc[air["Entity"] == "World", "Code"] = "WORLD"
    air.loc[air["Entity"] == "Europe", "Code"] = "EUROPE"
    air.loc[air["Entity"] == "High-income countries", "Code"] = "HIC"
    air.loc[air["Entity"] == "Low-income countries", "Code"] = "LIC"
    air.loc[air["Entity"] == "Lower-middle-income countries", "Code"] = "LMIC"
    air.loc[air["Entity"] == "North America", "Code"] = "NAM"
    air.loc[air["Entity"] == "Oceania", "Code"] = "OCEANINA"
    air.loc[air["Entity"] == "South America", "Code"] = "SAM"
    air.loc[air["Entity"] == "Timor", "Code"] = "TIM"
    air.loc[air["Entity"] == "Upper-middle-income countries", "Code"] = "UMIC"

    # Remove rows where Code is NaN
    air = air.dropna(subset=["Code"])

    # Writing files
    air.to_csv("air-pollution_cleaned.csv", index=False, quotechar='"')

    # Return finish message
    print("cleaning done")


if __name__ == "__main__":
    clean_airpollution()
