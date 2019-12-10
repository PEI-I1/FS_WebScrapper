build:
	docker build -t fs_scrapper:latest .

run:	
	docker run -p 5002:5002 -it fs_scrapper:latest

remove:
	docker rmi fs_scrapper:latest
