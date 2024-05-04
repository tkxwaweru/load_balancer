FROM python:3.11-slim

# Set environment variable for server ID
# Default value is 1, but can be changed during container startup
ENV SERVER_ID=1

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the rest of the application code into the container
COPY . /

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the Flask application
CMD ["python", "server.py"]
