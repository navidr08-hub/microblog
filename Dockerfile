FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (for layer caching)
COPY requirements.txt .

# Install system dependencies required for psycopg2 and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn pymysql cryptography

# Copy the rest of the application files
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./

# Make boot script executable
RUN chmod a+x boot.sh

# Environment variables
ENV FLASK_APP=microblog.py

# Compile translations (Flask-Babel)
RUN flask translate compile || true

# Expose port 5000
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["./boot.sh"]

