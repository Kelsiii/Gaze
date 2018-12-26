import docker

class DockerClient(object):
    def __init__(self):
        self.client = docker.from_env()

    def pull_image(self, image_name):
        try:
            resp = self.client.images.pull(image_name)
            if len(resp)>0:
                return True , ''
        except Exception as e:
            return False , str(e)
