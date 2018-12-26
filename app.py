import json
import random
import string
from flask import Flask, render_template, request, jsonify
from client import K8SClient, DockerClient, DBClient

app = Flask(__name__)
docker_client = DockerClient()
db_client = DBClient()
k8s_client = K8SClient()

@app.route('/')
def index():
    return render_template('PodList.html')

@app.route('/imageList')
def show_image_list():
    return render_template('ImageList.html')

@app.route('/upload', methods=['GET', 'POST'])
def show_upload():
    return render_template('upload.html')

@app.route('/deploy', methods=['GET', 'POST'])
def show_deploy():
    return render_template('deploy.html')

@app.route('/pods', methods=['GET', 'POST'])
def show_pod_list():
    return render_template('PodList.html')

@app.route('/_get_pods', methods=['GET', 'POST'])
def get_pods():
    pod_list = db_client.get_pods()
    return jsonify(pod_list)

@app.route('/_get_images', methods=['GET', 'POST'])
def get_images():
    image_list = db_client.get_image()
    return jsonify(image_list)

@app.route('/_add_image', methods=['POST'])
def add_image():
    name = request.form['name']
    image = request.form['image']
    description = request.form['description']

    try:
        db_client.insert_image(container_name=name, image=image, description=description)
        return "True"
    except Exception as e:
        return "False"
    '''
    res, msg = docker_client.pull_image(image)
    if res:
        new_values = { "$set": { "status": "success" } }
        db_client.update_image(image=image,new_values=new_values)
        return "True"
    else:
        new_values = { "$set": { "status": "error", "msg":msg } }
        db_client.update_image(image=image,new_values=new_values)
        return "False"
    '''

@app.route('/_add_pod', methods=['POST'])
def add_port():
    image = request.form['image']
    source_name = request.form['source']

    if len(db_client.query_pod_by_src(srcname=source_name))!=0:
        return jsonify({"res":"False","msg":"duplicated source"})
    else:
        env = request.form['env']
        if env is None or env == "":
            env = {}
        else:
            env = json.loads(env)
        output_ip = request.form['ip']
        output_port = request.form['port']

        env['OUT_IP'] = output_ip
        env['OUT_PORT'] = output_port

        key = ''.join(random.sample(string.ascii_letters + string.digits, 8)).lower()
        new_pod = k8s_client.create_pod_object(
            name=image.split(r'/')[1]+'-'+source_name+'-'+key ,
            image=image, key=key, env=env)
        res, msg = k8s_client.create_pod(new_pod)
        if res:
            db_client.insert_pod(source_name,key,image,env)
            new_values = {"$inc": {"pods":1}}
            db_client.update_image(image=image, new_values=new_values)
            return jsonify({"res":"True"})
        else:
            return jsonify({"res":"False","msg":msg})

@app.route('/_delete_pod/<pod_name>', methods=['GET','POST'])
def delete_pod(pod_name):
    pod = db_client.query_pod_by_name(pod_name)[0]

    if pod['status'] == "Pod Not Exist":
        db_client.delete_pod(pod_name)
        new_values = {"$inc": {"pods":-1}}
        db_client.update_image(image=pod['image'], new_values=new_values)
        return jsonify({"res":"True"})
    else :
        res, msg = k8s_client.delete_pod(pod_name)
        if res:
            db_client.delete_pod(pod_name)
            new_values = {"$inc": {"pods":-1}}
            db_client.update_image(image=pod['image'], new_values=new_values)
            return jsonify({"res":"True"})
        else:
            return jsonify({"res":"False","msg":msg})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)