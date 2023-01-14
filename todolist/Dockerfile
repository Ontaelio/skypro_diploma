FROM python:3.10-slim

WORKDIR /opt/

EXPOSE 8000

# Enable venv - but is it needed here?
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "entrypoint.sh"]

CMD ["gunicorn", "todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]
