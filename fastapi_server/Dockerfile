# Use a base Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary code into the container directory
COPY . .

# Copy the storage folder into the FastAPI server directory
COPY storage /app/storage

# Copy the utils folder into the FastAPI server directory
COPY utils /app/utils

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to start the FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
