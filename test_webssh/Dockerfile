FROM python:3.7.4

ENV PYTHONUMBUFFERED 1

RUN mkdir /app \
&& mkdir /app/dockermysql \
&& apt-get -y update \
&& apt-get -qq -y install cron \
&& apt-get install -y --no-install-recommends \
		sshpass \
		vim \
&& rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

EXPOSE 8002

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

CMD ["sh", "-c", "/app/start.sh"]