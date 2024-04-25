FROM python:3.12-slim-bullseye
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Create venv, add it to path
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy backend folder
COPY /backend /app/backend
WORKDIR /app/backend

# Export requirements from poetry files
RUN pip install poetry poetry-plugin-export
RUN poetry config virtualenvs.create false
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

# Install requirements
WORKDIR /app/backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Create new user to run app process as unprivilaged user
RUN addgroup --gid 1001 --system uvicorn && \
    adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 uvicorn

# Change ownership of the /app directory to the uvicorn user
RUN chown -R uvicorn:uvicorn /app/backend

# Switch to the uvicorn user and run the app
USER uvicorn

# Expose the port the app runs on
EXPOSE ${BACKEND_PORT}