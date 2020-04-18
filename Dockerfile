FROM python:3.6-buster
COPY . /app
WORKDIR /app
RUN pip install -U python-dotenv
RUN pip install -r requirements.txt
CMD [ "python", "./run.py" ]