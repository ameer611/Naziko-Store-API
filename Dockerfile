# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
FROM python:3.10

# Root user sifatida ishlash
USER root

# Kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y wget unzip curl gnupg2

# Google Chrome'ni qo'shish
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google-chrome.asc && \
    echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/google-chrome.asc] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Chrome va ChromeDriver versiyasini sinxronizatsiya qilish
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Foydalanuvchi o'zgartirish (Kerak bo'lsa)
USER python

# ChromeDriver yo‘lini tekshirish
RUN which chromedriver


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