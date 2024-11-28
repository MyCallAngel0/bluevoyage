
FROM python:3.10

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
# TODO: Change the runserver to something else 
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
