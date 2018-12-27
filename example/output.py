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
