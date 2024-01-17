FROM python:3.10.9

ENV PYTHONUNBUFFERED 1

RUN git clone https://github.com/NeerajN10/AppAggregator.git /app_agg

WORKDIR /app_agg

RUN ls

RUN pip install -r requirements.txt

VOLUME /app_agg

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]