# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR app/

# Create an Environment variable for the app to use
ENV AM_I_IN_A_DOCKER_CONTAINER="1"

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files (if available) into the container
COPY . .

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]