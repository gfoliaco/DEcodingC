# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port number that Streamlit listens on
EXPOSE 8080

# Run app.py when the container launches
CMD ["streamlit", "run", "--server.port", "8080", "main.py"]
