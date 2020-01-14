FROM python

RUN apt-get update && apt-get install -y firefox-esr

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
