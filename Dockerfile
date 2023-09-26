FROM python:3.6

RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends apt-utils && \
  apt-get install -y --no-install-recommends libmagic1 locales && \
  apt-get install -yqq apt-transport-https gettext

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
  locale-gen

RUN \
  echo "deb https://deb.nodesource.com/node_12.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs yarn && \
  apt-get install -y poppler-utils && \
  pip install -U pip && pip install pipenv && \
  npm i -g npm@^6 && \
  rm -rf /var/lib/apt/lists/*


RUN mkdir -p /app
RUN mkdir -p /etc
ADD etc/uwsgi.conf /etc/
ADD iwex_crm /app/

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app/static/
RUN npm install --silent
RUN npm run build

WORKDIR /app/
RUN pip install -r requirements.txt
