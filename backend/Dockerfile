#Install Python
FROM python:3.9

WORKDIR /app

#Install requirements
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#Run the app
CMD ["python", "-u", "run.py"]