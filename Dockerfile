FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
RUN if [ ! -f requirements.txt ]; then pip install matplotlib==3.7.1 networkx==3.1; fi

COPY connections.txt .
COPY connections2.txt .
COPY stations.txt .
COPY stations2.txt .
COPY test_connections.txt .
COPY test_stations.txt .
COPY test_stations2.txt .

COPY trains.py .
COPY testtrains.py .
COPY originaltrains.py .

# Run the other train programs by inputting "docker run *TRAIN APP NAME* python *PROGRAM NAME*.py" into the terminal.
CMD ["python", "trains.py"]