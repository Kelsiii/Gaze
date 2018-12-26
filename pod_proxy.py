from apscheduler.schedulers.background import BackgroundScheduler
import zmq
from client import DBClient
import time

pods_dict = {}
PUSH_PORT = 5001
db_client = DBClient()

def get_pod_info():
    global pods_dict
    pods_dict = {}
    pods_list = db_client.get_pods()
    context = zmq.Context()

    for pod in pods_list:
        push_sock = context.socket(zmq.PUSH)
        push_sock.connect('tcp://'+pod['pod_IP']+':'+str(PUSH_PORT))
        pods_dict[pod['key']] = push_sock
    print("updated at "+ time.ctime(), len(pods_dict))

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_pod_info, 'interval', minutes=5)
    scheduler.start()

    get_pod_info()
    context = zmq.Context()
    pull_sock = context.socket(zmq.PULL)
    pull_sock.setsockopt(zmq.CONFLATE, 1)
    pull_sock.bind('tcp://0.0.0.0:5001')

    while True:
        data = pull_sock.recv()
        key = data[0:8].decode()
        msg = data[8:]
        try:
            pods_dict[key].send(msg)
            print("send to", key, len(msg), time.ctime())
        except:
            print("drop"+key + " "+ time.ctime())
