FROM python:3.9.12

RUN mkdir /opt/app
COPY app.py /opt/app
COPY requirements.txt /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["/opt/app/app.py"]