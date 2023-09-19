FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
RUN if [ ! -f requirements.txt ]; then pip install matplotlib==3.7.1 networkx==3.1; fi

COPY trains.py .

CMD ["python", "trains.py"]