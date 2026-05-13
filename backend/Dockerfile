FROM python:3.12-slim

WORKDIR /app

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Installer les dépendances (en root, avant de switcher d'user)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copier le code source
COPY . .

# Créer l'utilisateur non-root et transférer la propriété
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

# Rendre le venv accessible
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]