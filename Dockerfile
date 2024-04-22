FROM python:3.9-slim-buster

WORKDIR /Final_Task_Luxonis

COPY  requirements.txt  ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "app.py"]