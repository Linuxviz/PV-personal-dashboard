FROM python:3.10
WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade -r requirements.txt

EXPOSE 8080

COPY ./ /app

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]