FROM python:3.7
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY src/ /code/
RUN python manage.py migrate
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
