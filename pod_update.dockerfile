FROM python:3.7
MAINTAINER Jingyi Zhu <t-jinzhu@microsoft.com>

RUN pip install pymongo
RUN pip install docker kubernetes
RUN pip install APScheduler

RUN mkdir Gaze
ADD pod_update.py Gaze/
ADD client/ Gaze/client/
WORKDIR /Gaze
CMD [ "python", "pod_update.py" ]