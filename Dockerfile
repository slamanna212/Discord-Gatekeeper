FROM python:3.8.6-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN sed -i '/token/c\  \"token\" : \"TOKEN\",' settings.json
RUN sed -i '/role/c\  \"role\" : \"CHANNEL\",' settings.json
RUN sed -i '/channel/c\  \"channel\" : \"ROLE\",' settings.json
CMD /app/dockerrun.sh


