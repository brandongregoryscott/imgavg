FROM ubuntu
MAINTAINER Brandon Scott

RUN apt update -y -q
RUN apt install -y -q git python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install twython
RUN pip3 install pillow

CMD ["python3", "/bot/PollingService.py"]

# docker build -t imgavg ~/imgavg/
# docker run --name imgavg --restart=always -v /home/brandon/imgavg/:/bot/ -d imgavg

