# Image officielle Python
FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Installation de uv
RUN pip install --no-cache-dir uv

# Copie des fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installation des dépendances
RUN uv sync --frozen

# Copie du reste du projet
COPY . .

# Expose le port de FastAPI
EXPOSE 8000

# Lancement de l'API
CMD ["uv", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]