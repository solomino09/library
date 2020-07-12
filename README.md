		Main library
	Django Rest Framework - for creating an API
	Django rest_framework.authtoken  - for Implement Token Authentication
	django_filters - for get filtered list of books (by year and by title)

______________________________________________________________________

		Environment deployment
	sudo apt-get update 
	sudo apt-get -y upgrade
	sudo apt-get install -y python3-pip
	sudo apt-get install build-essential libssl-dev libffi-dev python-dev

	git clone git@github.com:solomino09/library.git
	cd library/

		Virtual Environment
	python3 -m venv env_py36
	source env_py36/bin/activate

		Ыoftware installation
	pip3 install -r requirements.txt
		
		DataBase dump
	sqlite3 db.sqlite3 < dump-2020-07-13_01-53.sql

	./manage.py migrate

		Launch
	./manage.py runserver

		User - admin
		Password - admin
___________________________________________________________________


	API:
     - Receive a list of authors
	GET /api/authors/ HTTP/1.1
    Host: 127.0.0.1:8000
    Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa

     - Get a list of books
	GET /api/books/ HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa

     - Receive detailed information about the author
	GET /api/author/1 HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa

     - Get detailed book information
	GET /api/book/3 HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa

     - Receive a list of books by the author
	GET /api/author_books/1 HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa

     - Receive a filtered list of books filtered by year of publication and title
	GET /api/books_copy/?publishing_year_min=1903&publishing_year_max=2010&book=The%20Sea-Wolf HTTP/1.1
	Host: 127.0.0.1:8000
	Authorization: Token 9f8fdca1044f2938d05eb88b276b5b0edd6af2aa




