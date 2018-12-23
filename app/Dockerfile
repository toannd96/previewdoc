FROM python:2

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev unoconv libreoffice-script-provider-python \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ADD . /doc-to-pdf

WORKDIR /doc-to-pdf

RUN pip install -r requirements.txt

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 app:serve
