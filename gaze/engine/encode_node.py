from .base_node import Node
import cv2 as cv

class EncodeNode(Node):
    def __init__(self, **kwargs):
        super(EncodeNode, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        return self

class JPGEncode(EncodeNode):
    def __init__(self, jpeg_quality = 50):
        super(EncodeNode, self).__init__()
        self.encode_param = [int(cv.IMWRITE_JPEG_QUALITY), jpeg_quality]

    def call(self, inputs, **kwargs):
        if inputs is not None:
            result, buffer = cv.imencode('.jpg', inputs, self.encode_param)
            if buffer is None:
                pass
        return buffer