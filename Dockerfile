FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg python3-pip -y
RUN pip install -r requirements.txt

CMD ["python3", "discord_bot.py"]