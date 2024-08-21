# Use an official Python runtime as a parent image

FROM python:3.12



# Set the working directory in the container

WORKDIR /app



# Copy the current directory contents into the container at /app

COPY . /app



# Install any needed packages specified in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt



# Expose port 8000 to the outside world

EXPOSE 8000



# Run the FastAPI app with Uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]