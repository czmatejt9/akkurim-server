# Use an official Python runtime as a parent image
FROM python:3.12.7-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run FastAPI
ENTRYPOINT ["uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]