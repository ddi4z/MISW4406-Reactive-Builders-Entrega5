FROM python:3.12

EXPOSE 5000/tcp

COPY eventos-requirements.txt ./
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r eventos-requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/eventos_y_atribucion/api", "run", "--host=0.0.0.0"]
