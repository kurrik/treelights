.PHONY: test install restart start stop requirements develop
.EXPORT_ALL_VARIABLES:

SERVER_DIRECTORY = $(shell pwd)
GUNICORN_PATH = $(shell which gunicorn)
SOCKET = $(shell pwd)/treelights.sock
HOSTNAME = $(shell hostname)

test:
	python test_lights.py

develop: stop
	FLASK_APP=server FLASK_ENV=development flask run --host=0.0.0.0 --port=5000

requirements:
	pip3 install -r requirements.txt

# Commands below need sudo, e.g. `sudo make install`

# Install all the systemd and nginx files.
install:
	envsubst \
		< treelights.nginx \
		> /etc/nginx/sites-available/treelights
	-ln -s /etc/nginx/sites-available/treelights /etc/nginx/sites-enabled
	envsubst \
		< treelights.service \
		> /etc/systemd/system/treelights.service
	sudo nginx -t
	sudo systemctl enable treelights.service
	sudo systemctl restart treelights.service
	sudo systemctl restart nginx

# Restart the systemd service.
restart:
	systemctl restart treelights.service

start:
	systemctl start treelights.service

stop:
	systemctl stop treelights.service