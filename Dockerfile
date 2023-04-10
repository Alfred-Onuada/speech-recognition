FROM python:3.9.16

WORKDIR /speech_auth

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000:5000

CMD ["flask", "--app", "app", "run"]
