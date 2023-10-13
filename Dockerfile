# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

WORKDIR /home

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 5000

CMD ["python", "app.py"]