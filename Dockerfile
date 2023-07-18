# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /dp_sales_analysis

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python code to the container
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
