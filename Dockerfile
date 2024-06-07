# Use the official Python image from the Docker Hub with Python 3.9
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY src ./src

ENV PYTHONPATH /app/src

# Set the default command to run the application
CMD ["python", "src/beam_app/covid_tweets_pipeline.py"]
