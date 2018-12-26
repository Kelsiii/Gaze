FROM python:3.7

RUN pip install opencv-python
RUN pip install numpy
RUN pip install pyzmq

RUN mkdir Gaze
ADD core_pipeline.py Gaze/
ADD gaze/ Gaze/gaze/
WORKDIR /Gaze
EXPOSE 5001
ENTRYPOINT ["python", "core_pipeline.py"]