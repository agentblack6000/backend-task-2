# Dockerfile for metroapp
# Tells Docker what is the base image to start from, python:3.12-slim is an official
# Python image, and pretty minimal, enabling fast builds 
FROM python:3.12-slim

# Prevents Python from writing .pyc files, reduces image size
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures Python outputs to the terminal directly, important for debugging
ENV PYTHONUNBUFFERED=1

# Confines the files to a directory called app, keeps the container clean
# (avoids mixing with the system files like /bin). Some other name could also be chosen like 
# /src or /project, but /app is the convention
WORKDIR /app

# Copies requirements.txt into /app
# This is done for Docker to cache the dependency installation layer, helps in faster
# rebuilds when the codebase is updated but the requirements stay the same.
COPY requirements.txt .

# Installs the Python dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Copies the project folder into the /app directory
COPY . .

# Sets the port the container will watch as 8000
EXPOSE 8000

# This starts gunicorn
CMD ["gunicorn", "metroapp.wsgi:application", "--bind", "0.0.0.0:8000"]
