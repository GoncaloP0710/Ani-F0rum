# Use an official Python runtime as a parent image
FROM python:3.13.3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall -y connexion flask werkzeug  # Add the -y flag to skip confirmation
RUN pip install "connexion[flask]"
RUN pip install "connexion[uvicorn]"

# Set PYTHONPATH to include the project root
ENV PYTHONPATH=/app

# Run the service
CMD ["python", "python/Tests/TopicRelated/client.py"]