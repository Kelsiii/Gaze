from client import K8SClient, DBClient
from apscheduler.schedulers.background import BackgroundScheduler
import time

db_client = DBClient()
k8s_client = K8SClient()

def update_pod_info():
    try:
        k8s_pods = k8s_client.get_all_pods()
        print(len(k8s_pods))
        db_pods = db_client.get_pods()

        for db_pod in db_pods:
            find = False
            for k8s_pod in k8s_pods:
                if k8s_pod['name'] == db_pod['name']:
                    if k8s_pod['phase'] != db_pod['status'] or k8s_pod['ip'] != db_pod['pod_IP']:
                        ctx={
                            "$set": {
                                "status": k8s_pod['phase'],
                                "pod_IP": k8s_pod['ip']
                            }
                        }
                        db_client.update_pod(name=db_pod['name'], new_values=ctx)
                        print("update pod "+ k8s_pod['name']+" "+ k8s_pod['phase']+" "+ k8s_pod['ip'])
                    find = True
                    break
            if not find:
                db_client.update_pod(name=db_pod['name'], new_values={
                    "$set": {"status": "Pod Not Exist" }
                })
                print("pod "+ db_pod['name']+" doesn't exist in k8s")
        print("update pod info at "+time.ctime())
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    update_pod_info()

    scheduler = BackgroundScheduler()
    scheduler.add_job(update_pod_info, 'interval', minutes=2)
    scheduler.start()

    while True:
        pass