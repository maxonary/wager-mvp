# Imported from https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi
FROM python:3.9

# 
WORKDIR /code

# Docker Cache
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["fastapi", "run", "app/main.py", "--port", "80"]