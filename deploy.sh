#!/bin/bash

echo "Остановка текущего контейнера..."
docker stop karta-snov-container || true

echo "Выполнение git pull..."
git pull

echo "Сборка нового образа..."
docker build -t karta-snov .

echo "Запуск нового контейнера..."
docker run -d --rm -p 8050:8050 --name karta-snov-container karta-snov

echo "Деплой завершен."
