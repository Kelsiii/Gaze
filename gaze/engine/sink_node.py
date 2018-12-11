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

class UdpSink(SinkNode):
    def __init__(self, ip="localhost", port=5001, jpeg_quality = 50):
        super(UdpSink, self).__init__()
        '''
        Args:
            jpeg_quality (:obj:`int`): Quality of JPEG encoding, in 0, 100.
            ip (:obj:`str`): IP address to send streaming. default localhost.
            port (:obj:`int`): default 5001
        '''
        self.encode_param = [int(cv.IMWRITE_JPEG_QUALITY), jpeg_quality]
        self.buffer = None
        self.lock = Lock()
        self.address = (ip, port)
        self.key = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def call(self, inputs, **kwargs):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if inputs is not None:
            self.lock.acquire()
            result, self.buffer = cv.imencode('.jpg', inputs, self.encode_param)
            self.lock.release()

            if self.buffer is None:
                pass
            if len(self.buffer) > 65507:
                print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
                sock.sendto("FAILFAIL".encode(),address)
                pass
            sock.sendto(bytes(self.key, 'utf8')+self.buffer.tobytes(),  self.address)
            print(self.address, len(self.buffer))
            #sock.sendto(self.buffer.tobytes(),  self.address)
        return None
    
class NetworkSink(SinkNode):
    def __init__(self, ip="127.0.0.1", port=5001, jpeg_quality = 50):
        super(NetworkSink, self).__init__()
        context = zmq.Context()
        self.sock = context.socket(zmq.PUSH)
        self.sock.connect('tcp://'+ip+':'+str(port))
        self.encode_param = [int(cv.IMWRITE_JPEG_QUALITY), jpeg_quality]
        self.key = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    def call(self, inputs, **kwargs):
        if inputs is not None:
            result, buffer = cv.imencode('.jpg', inputs, self.encode_param)

            if buffer is None:
                pass
            self.sock.send(bytes(self.key, 'utf8')+buffer.tobytes())
            print(len(buffer))
            #sock.sendto(self.buffer.tobytes(),  self.address)
        return None