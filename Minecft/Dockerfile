FROM python:3.9-slim

RUN pip install pyanvil

COPY MineCTF /app/MineCTF
COPY generate.py /app/generate.py

ENTRYPOINT [ "python3", "/app/generate.py" ]