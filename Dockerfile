# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disk
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose port 8080 for Flask
EXPOSE 8080

# Run the main script when the container launches
CMD ["python", "main.py"]
