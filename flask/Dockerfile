FROM python:3.10

ENV TZ=Asia/Seoul

RUN apt-get update 

WORKDIR /home

COPY . .

RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]
