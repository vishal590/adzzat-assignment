FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 INVENTORY_CSV=/workspace/inventory.csv
WORKDIR /workspace
COPY workspace/ /workspace/
COPY LICENSE.bottle /LICENSE.bottle
CMD ["sh", "-c", "sleep infinity"]
