FROM python

COPY . .

RUN pip install -r /dependencies

WORKDIR /app

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", ":80" ]
