from gaze.pipes import Graph
from gaze.nodes import NetworkSource
from gaze.nodes import NetworkSink
import os

IN_IP="0.0.0.0"
IN_PORT=5001

OUT_IP = os.getenv("OUT_IP") if os.getenv("OUT_IP") else "127.0.0.1"
OUT_PORT = int(os.getenv("OUT_PORT")) if os.getenv("OUT_PORT") else 5001

print(IN_IP,IN_PORT,OUT_IP,OUT_PORT)

x = NetworkSource(ip=IN_IP,port=IN_PORT)
x = NetworkSink(ip=OUT_IP,port=OUT_PORT)(x)

graph = Graph(x)
graph.run()
