FROM python:3.8.6-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /app/dockerrun.sh
CMD /app/dockerrun.sh


