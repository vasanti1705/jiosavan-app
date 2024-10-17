# Use an official Python runtime as a parent image
FROM python:latest
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5100 available to the world outside this container
EXPOSE 5100

# Define environment variable for Flask
ENV FLASK_APP=project-app.py
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5100"]
