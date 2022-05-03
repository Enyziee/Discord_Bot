FROM python:3.9.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install ffmpeg -y
RUN pip install -r requirements.txt

CMD ["python3", "discord_bot.py"]