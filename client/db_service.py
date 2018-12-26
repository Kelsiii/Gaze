from pymongo import MongoClient
import os

class DBClient(object):
    def __init__(self):
        MONGO_IP = os.getenv("MONGO_SERVICE_HOST") if os.getenv("MONGO_SERVICE_HOST") else "23.100.31.20" #input the mongodb endpoint here
        MONGO_PORT = os.getenv("MONGO_SERVICE_PORT") if os.getenv("MONGO_SERVICE_PORT") else 27017
        mongo_uri = "mongodb://"+MONGO_IP+":"+str(MONGO_PORT)
        
        client = MongoClient(mongo_uri)
        db = client.gazedb
        self.image_collection = db.image
        self.pod_collection = db.pod
    
    def insert_pod(self, src, key, image, env):
        pod_info = {
            "_id": (image.split(r'/')[1]+'-'+src+'-'+key).replace("_","-"),
            "name": (image.split(r'/')[1]+'-'+src+'-'+key).replace("_","-"),
            "srcname": src,
            "key": key,
            "image": image,
            "env": env,
            "status": "Pending",
            "pod_IP": ""
        }
        self.pod_collection.insert_one(pod_info)

    def delete_pod(self, name):
        self.pod_collection.delete_one({"name":name})

    def query_pod_by_src(self, srcname):
        query = {"srcname": srcname}
        results = list(self.pod_collection.find(query))
        return results
    
    def query_pod_by_name(self, name):
        query = {"name": name}
        results = list(self.pod_collection.find(query))
        return results

    def get_pods(self):
        results = list(self.pod_collection.find())
        return results

    def update_pod(self, name, new_values):
        query = {
            "name": name
        }
        self.pod_collection.update_many(query, new_values)
    
    def insert_image(self, container_name, image, description):
        image_info = {
            "_id": image,
            "name": container_name,
            "image": image,
            "description": description,
            "status": "success",
            "pods": 0
        }
        self.image_collection.insert_one(image_info)
    
    def update_image(self, image, new_values):
        query = {
            "image": image
        }
        self.image_collection.update_many(query, new_values)
    
    def get_image(self):
        results = list(self.image_collection.find())
        return results
        