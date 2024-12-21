# Dockerfile for Django
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port and start server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
