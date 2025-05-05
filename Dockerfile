# Use official Python image
FROM python:3.9-slim

# Set environment variables (fixed format)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the whole project
COPY . /app/

# Expose port (if needed)
EXPOSE 8000

# Start the Django app (you can adjust this)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
