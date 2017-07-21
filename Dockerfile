FROM ubuntu
MAINTAINER Brandon Scott

RUN apt-get update -y -q && apt-get install -y -q git python3 python3-pip
RUN pip3 install --upgrade pip setuptools
RUN pip3 install twython pillow
RUN git clone https://github.com/brandongregoryscott/twitterbot
RUN cd twitterbot && python3 setup.py install && cd ..
WORKDIR /imgavg/
CMD ["python3", "bot.py"]

# docker build -t imgavg ~/imgavg/
# docker run --name imgavg      \
# --restart=always              \
# --log-opt max-size=1024kb     \
# --volume ~/output/imgavg/:/out/     \
# --volume ~/imgavg/:/imgavg/         \
# -d imgavg

