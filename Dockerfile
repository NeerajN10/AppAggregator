FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN git clone https://github.com/NeerajN10/AppAggregator.git /app_agg

WORKDIR /app_agg

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]