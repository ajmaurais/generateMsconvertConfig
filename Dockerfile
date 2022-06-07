from python:3.9

MAINTAINER "Aaron Maurais -- MacCoss Lab"

RUN mkdir -p /code/generateMsconvertConfig/src /data

COPY src /code/generateMsconvertConfig/src
COPY setup.py /code/generateMsconvertConfig

RUN cd /code/generateMsconvertConfig && \
    python setup.py build && \
    pip install .

WORKDIR /data

CMD ["generateMsconvertConfig"]

