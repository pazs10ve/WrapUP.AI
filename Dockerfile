# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
