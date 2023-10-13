# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

WORKDIR /home

COPY . .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80


# Run app.py when the container launches
CMD ["python", "app.py"]