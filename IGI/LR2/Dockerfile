FROM python:latest

LABEL description="Калькулятор геометрических фигур"

WORKDIR /app

COPY geometric_lib/ ./geometric_lib/

COPY calculate.py .

RUN chmod +x calculate.py

STOPSIGNAL SIGTERM

CMD ["python", "calculate.py"]