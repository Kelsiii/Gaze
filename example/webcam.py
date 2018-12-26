import sys
sys.path.append("..")
from gaze.pipes import Graph
from gaze.nodes import DefaultDeviceSource
from gaze.nodes import NetworkSink
from gaze.nodes import JPGEncode, IMGDecode
from client import DBClient

def webcam_example(source_name):
    db_client = DBClient()
    res = db_client.query_pod_by_src(srcname=source_name)
    if(len(res)==0):
        print("wrong source name")
    else:
        src = res[0]
        key = src['key']
        print(key)

        x = DefaultDeviceSource()
        x = JPGEncode()(x)
        x = NetworkSink(ip="157.56.181.123", port=5001, key=key)(x)

        graph = Graph(x)
        graph.run()

if __name__ == "__main__":
    webcam_example("source1")