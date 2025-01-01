# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /work

# Install required Python packages
COPY requirements.txt .
COPY requirements.dev.txt .
RUN pip install --no-cache-dir --upgrade pip wheel setuptools
RUN pip install --no-cache-dir --upgrade -r /work/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /work/requirements.dev.txt
