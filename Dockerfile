FROM python:3.10-alpine

MAINTAINER PufferOverflow

WORKDIR /var/bot

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["/var/bot/main.py"]