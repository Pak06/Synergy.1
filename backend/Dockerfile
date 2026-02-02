# Usa una versione leggera di Python
FROM python:3.10-slim

# Imposta la cartella di lavoro dentro il contenitore
WORKDIR /app

# Installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice
COPY . .

# Comando per avviare l'app
CMD ["python", "app.py"]
