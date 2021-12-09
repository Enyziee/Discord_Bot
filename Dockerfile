FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN apt-get update && apt-get install ffmpeg -y
RUN pip install -r requirements.txt

CMD ["python3", "discord_bot.py"]
