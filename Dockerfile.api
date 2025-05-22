FROM python:3.10.17-alpine3.21

WORKDIR /app

COPY api/requirements.txt api/api.py ./

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "-m", "flask", "--app", "api.py", "run", "--host=0.0.0.0", "--port=5000"]