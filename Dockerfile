FROM python:3.8.6-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python ./app/bot.py 

# volume
VOLUME /app
