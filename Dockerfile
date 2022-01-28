#Install Python
FROM python:3.9

WORKDIR /app

#Install requirements
COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY src .

#Run the app
CMD ["python", "-u", "src/run.py"]