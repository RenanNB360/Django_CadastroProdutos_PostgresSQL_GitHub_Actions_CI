#!/bin/sh

echo "Aguardando o banco de dados ficar disponível..."

until nc -z localhost 5432; do
    echo "Ainda aguardando o banco de dados..."
    sleep 1
done

echo "Confirma se o banco esta disponível..."
if [ $? -ne 0 ]; then
    echo "Erro: O banco de dados não está acessível."
    exit 1
fi

echo "Aplicando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Iniciando o servidor..."
exec gunicorn -b 0.0.0.0:8080 backend.wsgi:application -w 4