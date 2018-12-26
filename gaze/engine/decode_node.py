from .base_node import Node
import cv2 as cv
import numpy as np

class DecodeNode(Node):
    def __init__(self, **kwargs):
        super(DecodeNode, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        return self

class IMGDecode(DecodeNode):
    def __init__(self):
        super(DecodeNode, self).__init__()

    def call(self, inputs, **kwargs):
        if inputs is not None:
            array = np.frombuffer(inputs, dtype=np.dtype('uint8'))
            img = cv.imdecode(array, 1)
            return img