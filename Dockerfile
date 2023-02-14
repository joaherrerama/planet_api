# syntax=docker/dockerfile:1
FROM osgeo/gdal:ubuntu-small-3.4.2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update \
    && apt-get install -y python3-pip libpq-dev\
    && rm -rf /var/lib/apt/lists/*

RUN apt-get upgrade

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD /code/
# ENTRYPOINT [ "python", "/code/main.py"]
