#!/bin/bash
pip3 freeze > requirements.txt
python3 -m pytest ./src/tests -vv
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload



# docker run --name docker-mysql -e MYSQL_HOST=host -e MYSQL_ROOT_PASSWORD=password -e MYSQL_USER=user -e MYSQL_PASSWORD=password -d mysql:latest
