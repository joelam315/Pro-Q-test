FROM python:3.6

WORKDIR /app

# Intall dependencies
COPY . /app/

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
  apt update && \
  apt install -y git ruby-dev nodejs postgresql-client redis-server wkhtmltopdf && \
  apt-get install chinese* && \
  apt-get install fonts-arphic-ukai fonts-arphic-uming fonts-ipafont-mincho fonts-ipafont-gothic fonts-unfonts-core && \
  apt clean && \
  gem install compass sass && \
  npm -g install less && \
  pip install --no-cache-dir -r requirements.txt && \
  pip install --no-cache-dir redis && \
  dpkg -i /app/wkhtmltox_0.12.6-1.buster_amd64.deb && \
  apt-get install -f

RUN chmod +x /app/entrypoint.sh \
  /app/wait-for-postgres.sh
ENTRYPOINT ["/app/entrypoint.sh"]