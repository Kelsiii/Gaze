from .base_node import Node
import cv2 as cv
import socket
import numpy as np
import zmq


class SourceNode(Node):
    # Node to be used as an entry point into a pipeline.
    def __init__(self, name=None):
        if not name:
            prefix = 'source'
            name = prefix + '_' + str(1)
        super(SourceNode, self).__init__(name=name)

    def call(self, inputs=None, **kwargs):
        return None


class VideoTestSource(SourceNode):
    def __init__(self, name=None):
        super(VideoTestSource, self).__init__(name=name)
        self._cap = cv.VideoCapture(
            'videotestsrc pattern=snow ! video/x-raw,width=320,height=240 ! appsink sync=false ', 
            cv.CAP_GSTREAMER)

    def call(self, inputs=None, **kwargs):
        return self._cap.read()

class DefaultDeviceSource(SourceNode):
    def __init__(self, name=None):
        super(DefaultDeviceSource, self).__init__(name=name)
        self._cap = cv.VideoCapture(
            'autovideosrc ! decodebin ! videoconvert ! queue ! appsink sync=false',
            cv.CAP_GSTREAMER
        )
    def call(self, input=None, **kwargs):
        return self._cap.read()

class NetworkSource(SourceNode):
    def __init__(self, ip="0.0.0.0", port=5001):
        super(NetworkSource, self).__init__(name=None)
        context = zmq.Context()
        self.sock = context.socket(zmq.PULL)
        self.sock.setsockopt(zmq.CONFLATE, 1)
        self.sock.bind('tcp://'+ ip +':'+ str(port))


    def call(self, inputs=None, **kwargs):
        data = self.sock.recv()
        return True, data

class FileSource(SourceNode):
    def __init__(self, location):
        super(FileSource, self).__init__()
        command = 'filesrc location={} ! decodebin ! videoconvert ! queue ! appsink sync=false '.format(location)
        self._cap = cv.VideoCapture(command, cv.CAP_GSTREAMER)

    def call(self, inputs=None, **kwargs):
        return self._cap.read()
