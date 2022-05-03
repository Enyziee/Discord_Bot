FROM ubuntu:20.04

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3.9 python3-pip -y
RUN pip install -r requirements.txt

CMD ["python3", "discord_bot.py"]