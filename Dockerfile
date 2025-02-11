# Use an official Python image as the base
FROM python:3.10-slim

# Install system dependencies for Chrome and Selenium
RUN apt-get update -y && \
    apt-get install -y wget gnupg unzip && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Set the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
