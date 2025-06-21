# Use an official Python runtime as a parent image
FROM python:3.13.3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app/

# Run the Python script when the container starts
CMD ["python", "app.py"]
