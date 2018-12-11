from gaze.pipes import Graph
from gaze.nodes import VideoTestSource, FileSource, DefaultDeviceSource, UdpSource, NetworkSource
from gaze.nodes import FileSink, UdpSink, AutoVideoSink

x = NetworkSource(port=5002,ip="0.0.0.0")
x = AutoVideoSink()(x)

graph = Graph(x)
graph.run()
    