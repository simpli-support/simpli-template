FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /app/src /app/src

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

USER appuser

EXPOSE 8019

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8019/health')"

CMD ["uvicorn", "simpli_template.app:app", "--host", "0.0.0.0", "--port", "8019"]
