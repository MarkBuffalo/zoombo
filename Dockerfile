FROM python:3.7.4

ADD zoombo.py /tmp
ADD requirements.txt /tmp
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

CMD [ "python3", "./tmp/zoombo.py" ]
