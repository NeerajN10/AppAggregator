FROM python:3.10.9

RUN git clone https://github.com/NeerajN10/AppAggregator.git /app_agg

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app_agg"

WORKDIR /app_agg

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]