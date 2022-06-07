from proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses:latest

MAINTAINER "Aaron Maurais -- MacCoss Lab"

ENV PATH="/root/miniconda3/bin:${PATH}"
 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    mkdir /root/.conda && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    rm -f Miniconda3-latest-Linux-x86_64.sh

RUN mkdir -p /code/generateMsconvertConfig/src /data

COPY src /code/generateMsconvertConfig/src
COPY setup.py /code/generateMsconvertConfig

RUN cd /code/generateMsconvertConfig && \
    /root/miniconda3/bin/python3 setup.py build && \
    /root/miniconda3/bin/pip install .

WORKDIR /data

CMD ["generateMsconvertConfig"]

