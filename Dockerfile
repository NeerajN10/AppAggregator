FROM python:3.10.9

# RUN git clone https://github.com/NeerajN10/AppAggregator.git /app_agg
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV PYTHONPATH "${PYTHONPATH}:/app_agg"
# WORKDIR /app_agg
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Django will run on
EXPOSE 8000

# Command to run your application
# Docker file is used to make only images, so no point in running manage.py here. Instead do it in docker-compose
#CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000

