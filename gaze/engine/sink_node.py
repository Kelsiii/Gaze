import cv2 as cv
import socket
from threading import Thread, Lock
from .base_node import Node
import random
import string
import json
import numpy as np
import zmq

class SinkNode(Node):
    def __init__(self, **kwargs):
        super(SinkNode, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        return self


class AutoVideoSink(SinkNode):
    def __init__(self, **kwargs):
        super(AutoVideoSink, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        buffer = None
        if inputs is not None:
            encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 50]
            result, buffer = cv.imencode('.jpg', inputs, encode_param)
            cv.imshow('AutoVideoSink', inputs)
        return None

class FileSink(SinkNode):
    def __init__(self, **kwargs):
        super(FileSink, self).__init__(**kwargs)
        fourcc = cv.VideoWriter_fourcc(*'MPEG')
        self.out = cv.VideoWriter(filename='output.avi', fourcc=fourcc, fps=20.0, frameSize=(960, 720), isColor=True)

        
    def call(self, inputs, **kwargs):
        frame_width = int( inputs.shape[1])
        frame_height =int( inputs.shape[0])
        #print(inputs.shape[0],inputs.shape[1])
        #self.out.set(frameSize, (frame_width,frame_height))
        inputs = cv.resize(inputs,(960,720))
        if inputs is not None:
            self.out.write(inputs)
        return None

class NetworkSink(SinkNode):
    def __init__(self, ip="127.0.0.1", port=5001, key=""):
        super(NetworkSink, self).__init__()
        context = zmq.Context()
        self.sock = context.socket(zmq.PUSH)
        self.sock.setsockopt(zmq.CONFLATE, 1)
        self.sock.connect('tcp://'+ip+':'+str(port))
        self.key = key

    def call(self, inputs, **kwargs):
        if inputs is not None:
            self.sock.send(bytes(self.key, 'utf8')+inputs.tobytes())
            print(len(inputs))
        return None