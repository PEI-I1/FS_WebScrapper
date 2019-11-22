FROM python

EXPOSE 5000

RUN apt-get install git

WORKDIR /home/scrapper

RUN git clone https://github.com/PEI-I1/FS_WebScrapper.git
WORKDIR /home/scrapper/FS_WebScrapper/fs_scrapper

RUN pip3 install -r requirements.txt

CMD make run