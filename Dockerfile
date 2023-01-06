# Get the python 3.9.13 base docker image
FROM python:3.9.13

WORKDIR /app
COPY . /app

# Install all the dependencies from lock file directly into the container
RUN pip install Flask
RUN pip install install flask_restful
EXPOSE 5005

ENTRYPOINT ["python3"]
CMD ["app.py"]
