.PHONY: test server install
.EXPORT_ALL_VARIABLES:

SERVER_DIRECTORY = $(shell pwd)
GUNICORN_PATH = $(shell which gunicorn)
SOCKET = $(shell pwd)/treelights.sock
HOSTNAME = $(shell hostname)

test:
	python test_lights.py

server:
	FLASK_APP=server flask run --host=0.0.0.0 --port=5000

requirements:
	pip3 install -r requirements.txt

# Needs sudo, e.g. `sudo make install`
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

