# Use an official Python image as a base
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your FastAPI app runs on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000"]
