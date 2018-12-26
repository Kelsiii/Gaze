import sys
sys.path.append("..")
from gaze.pipes import Graph
from gaze.nodes import VideoTestSource, FileSource, DefaultDeviceSource, UdpSource, NetworkSource
from gaze.nodes import FileSink, UdpSink, AutoVideoSink
from gaze.nodes import IMGDecode, JPGEncode
import zmq

x = NetworkSource(port=5001,ip="0.0.0.0")
x = IMGDecode()(x)
x = AutoVideoSink()(x)

graph = Graph(x)
graph.run()
'''

context = zmq.Context()
pull_sock = context.socket(zmq.PULL)
pull_sock.setsockopt(zmq.CONFLATE, 1)
pull_sock.bind('tcp://0.0.0.0:5002')

while True:
    data = pull_sock.recv()
    #key = data[0:8].decode()
    msg = data.decode()
    print(msg)
'''