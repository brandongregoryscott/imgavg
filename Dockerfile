FROM ubuntu
MAINTAINER Brandon Scott

RUN apt-get update -y -q && apt-get install -y -q git python3 python3-pip && git clone https://github.com/brandongregoryscott/twitterbot
RUN pip3 install --upgrade pip setuptools
RUN pip3 install twython pillow
RUN cd twitterbot && python3 setup.py install && cd ..
WORKDIR /bot/
CMD ["python3", "bot.py"]

# docker build --no-cache -t imgavg ~/imgavg/
# docker run --name imgavg -e TZ=America/New_York --env-file=imgavgbot.env --log-opt max-size=256kb --volume ~/output/imgavg/:/out/ --volume ~/imgavg/:/bot/ -d imgavg

