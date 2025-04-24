FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY app.py .
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Expose the Streamlit port
EXPOSE 8502

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
