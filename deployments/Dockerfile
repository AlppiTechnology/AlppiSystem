# Use the official Python base image
FROM python:3.11-alpine3.18
LABEL mantainer='patrickbpiccini@hotmail.com'

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project files to the container
COPY . /alppisystem
COPY /scripts /scripts

# Set work directory
WORKDIR /alppisystem

# Set port to access
EXPOSE 7002

# Install Python dependencies in VENV
RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r /alppisystem/requirements/develop.txt

RUN chmod -R +x /scripts
RUN chmod -R 755 /alppisystem

ENV PATH="/scripts:/venv/bin:$PATH"

# Command to run the application
CMD [ "startapp.sh" ]