import sys
sys.path.append("..")
from gaze.pipes import Graph
from gaze.nodes import DefaultDeviceSource
from gaze.nodes import NetworkSink
from gaze.nodes import JPGEncode, IMGDecode
from client import DBClient

'''
This function shows you how to get a video stream from your webcam and send it to the analysis platform.
Firstly remember to configure the external endpoint of mongoDB in file client/db_service.py
'''
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
        x = NetworkSink(ip="Input the external endpoint of the k8s service 'gaze-server' here", port=5001, key=key)(x)

        graph = Graph(x)
        graph.run()

if __name__ == "__main__":
    webcam_example("source1")