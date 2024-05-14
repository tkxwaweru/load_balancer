FROM python:3.11-slim

# Set environment variables
ENV ACTIVE_SERVERS="1 2 3"

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the rest of the application code into the container
COPY . /

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the Flask application with a random server ID from the list of active servers
CMD ["python", "server.py"]
