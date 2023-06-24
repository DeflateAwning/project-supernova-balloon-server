
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app source code to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the environment variable to run the Flask app
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
