# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Linux uchun kerakli kutubxonalar
RUN apt-get update \
  && apt-get install -y gcc libpq-dev curl netcat \
  && apt-get clean

# Ish katalogi
WORKDIR /app

# Kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani nusxalash
COPY . .

# Faylga ruxsat berish
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
