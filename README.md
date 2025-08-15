# Запуск

docker compose up --build -d

# Подключить Loki и Tempo в Grafana

Добавь Loki (http://loki:3100) и Tempo (http://tempo:3200) как источники данных.

# Проверить работу 

curl http://localhost:8000/process

Jaeger: http://localhost:16686
Grafana: http://localhost:3000

