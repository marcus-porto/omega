# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
COPY ./api /app/api

# Define a variável de ambiente para o Flask
ENV FLASK_APP=api.celery_worker

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0"]
