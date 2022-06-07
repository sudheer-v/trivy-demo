FROM jiahangli/python3centos6:1.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py app.py

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
