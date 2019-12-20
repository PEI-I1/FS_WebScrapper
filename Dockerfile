FROM python

EXPOSE 5000

RUN apt-get update && apt-get install -y git firefox-esr

WORKDIR /home

#install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz
RUN tar -xvzf geckodriver-v0.24.0-linux32.tar.gz
RUN chmod +x geckodriver
ENV PATH="/home:${PATH}"

WORKDIR /home/scrapper

RUN git clone https://github.com/PEI-I1/FS_WebScrapper.git
WORKDIR /home/scrapper/FS_WebScrapper/fs_scrapper

RUN pip3 install -r requirements.txt

CMD make run
