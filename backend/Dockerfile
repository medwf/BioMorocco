FROM python:3.10.12-slim

WORKDIR /home/BioMorocco/backend

COPY . /home/BioMorocco/backend

RUN pip install -r requirements.txt

# Define environment variable
ENV FLASK_APP=api/v1/app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
