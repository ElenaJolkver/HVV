# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Set the working directory in the container
WORKDIR app/
# Create an Environment variable for the app to use
ENV AM_I_IN_A_DOCKER_CONTAINER="1"

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the current directory contents into the container at /app
COPY . .

# Configure Poetry and install dependencies in a single RUN step
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    # Remove Poetry after installing dependencies to save space
    pip uninstall -y poetry && \
    # Clean up pip cache and other unnecessary files
    rm -rf /root/.cache/pip && \
    rm -rf /root/.cache/pypoetry


# Expose port 8000 to the outside world
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
