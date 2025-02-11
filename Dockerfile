# Use an official Python image as the base
FROM python:3.14.0a4-bookworm

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get update && apt-get install -y wget xvfb unzip


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Copy the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 5000

# Set the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
