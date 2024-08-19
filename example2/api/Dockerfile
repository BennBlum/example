FROM python:3.10

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./models /models
COPY ./mainapp /mainapp

CMD ["uvicorn", "mainapp.app:app", "--host", "0.0.0.0", "--port", "8000"]