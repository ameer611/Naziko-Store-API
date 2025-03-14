# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Chrome va ChromeDriver o‘rnatish
RUN apt-get update && apt-get install -y wget unzip \
    && wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Ishchi direktoriyani sozlash
WORKDIR .

# Loyihani ko‘chirish va kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani ko‘chirish
COPY . .

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]