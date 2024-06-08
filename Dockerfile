# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 80 available to the world outside this container (optional for GUI apps)
# EXPOSE 80

# Define environment variable (optional)
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
