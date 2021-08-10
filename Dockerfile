FROM python:3.9

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt 

EXPOSE 8080

ENV PORT="${PORT:-8080}"

CMD gunicorn main:app --bind 0.0.0.0:$PORT --workers=4 --threads 4 --timeout 60 -k uvicorn.workers.UvicornWorker
