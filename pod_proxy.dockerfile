FROM python:3.7
MAINTAINER Jingyi Zhu <t-jinzhu@microsoft.com>

RUN pip install pyzmq
RUN pip install pymongo
RUN pip install APScheduler
RUN pip install docker kubernetes

RUN mkdir Gaze
ADD pod_proxy.py Gaze/
ADD client/ Gaze/client/
WORKDIR /Gaze
EXPOSE 5001
CMD ["python", "pod_proxy.py"]