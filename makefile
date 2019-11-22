build:
	docker build -t fs_scrapper:latest .

run:	
	docker run -it --rm --network host fs_scrapper:latest

remove:
	docker rmi fs_scrapper:latest