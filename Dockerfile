FROM python:3.6

WORKDIR /app

# Intall dependencies
COPY . /app/

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt update
RUN apt install -y git ruby-dev nodejs postgresql-client redis-server wkhtmltopdf
RUN apt-get install chinese*; exit 0
RUN apt-get install fonts-arphic-ukai fonts-arphic-uming fonts-ipafont-mincho fonts-ipafont-gothic fonts-unfonts-core
RUN apt clean
RUN gem install compass sass
RUN npm -g install less
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir redis
RUN dpkg -i /app/wkhtmltox_0.12.6-1.buster_amd64.deb; exit 0
RUN apt-get install -f; exit 0

RUN chmod +x /app/entrypoint.sh \
  /app/wait-for-postgres.sh
ENTRYPOINT ["/app/entrypoint.sh"]