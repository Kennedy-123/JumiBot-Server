# Use an official Python image as the base
FROM python:3.14.0a4-bookworm

# Install system dependencies, including Chrome and necessary tools
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver dynamically based on the installed version of Chrome
RUN wget https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 5000

# Set the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
