FROM python:3.8.1

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list
RUN echo "Package: *\nPin: release a=stable\nPin-Priority: 900\n\nPackage: *\nPin release a=unstable\nPin-Priority: 10" > /etc/apt/preferences.d/99pin-unstable
RUN apt-get update && apt-get install -t unstable -y firefox

WORKDIR /home

#install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.24.0-linux64.tar.gz
RUN chmod +x geckodriver
ENV PATH="/home:${PATH}"

COPY . /home/scrapper/FS_WebScrapper
WORKDIR /home/scrapper/FS_WebScrapper/fs_scrapper

RUN pip3 install -r requirements.txt

CMD make run
