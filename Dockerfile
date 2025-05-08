#FROM python:3.12-slim
FROM selenium/standalone-chrome

RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip python3.12-venv && \
    sudo rm -rf /var/lib/apt/lists/*

WORKDIR /agente_investimento

RUN python3 -m venv venv

COPY requirements.txt .

# Install the dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

COPY ./agente_investimento ./agente_investimento

COPY Makefile .

COPY ./app ./app

EXPOSE 3000

#CMD ["uvicorn", "app.fastapi_main:app", "--host", "0.0.0.0", "--port", "3000"]
CMD ["venv/bin/python", "-m", "uvicorn", "app.fastapi_postgree_main:app", "--host", "0.0.0.0", "--port", "3000"]