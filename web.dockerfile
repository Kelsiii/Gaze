FROM python:3.7
MAINTAINER Jingyi Zhu <t-jinzhu@microsoft.com>

RUN pip install flask
RUN pip install pymongo
RUN pip install docker kubernetes

RUN mkdir Gaze
ADD app.py Gaze/
ADD client/ Gaze/client/
ADD templates/ Gaze/templates/
ADD static/ Gaze/static/
WORKDIR /Gaze
EXPOSE 5000
CMD [ "python", "app.py" ]