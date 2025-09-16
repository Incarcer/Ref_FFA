# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# 1. Install dependencies AS ROOT.
# Copy only the requirements file first to leverage Docker layer caching.
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2. Now, create the non-root user.
RUN adduser --system --group appuser

# 3. Copy the rest of the application code and set ownership.
# This ensures the application files are owned by the user who will run them.
COPY --chown=appuser:appuser . .

# 4. Switch to the non-root user for runtime.
# From this point on, commands run as 'appuser'.
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Use --host 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]