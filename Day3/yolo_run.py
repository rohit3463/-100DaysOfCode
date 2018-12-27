#to download yolov2.h5 foloow the procedure mentioned at https://github.com/miranthajayatilake/YOLOw-Keras

import argparse
import os
import matplotlib.pyplot as plt 
import os
from matplotlib.pyplot import imshow
import scipy.io 
import scipy.misc
import numpy as np 
import pandas as pd 
from PIL import Image
import tensorflow as tf 
from keras import backend as K 
from keras.layers import Input, Lambda, Conv2D
from keras.models import load_model, Model 
from yolo_utils import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes, scale_boxes
from yad2k.models.keras_yolo import yolo_head, yolo_boxes_to_corners, preprocess_true_boxes, yolo_loss, yolo_body, yolo_eval

input_image_name = "person.jpg"

input_image = Image.open("images/" + input_image_name)
width, height = input_image.size
width = np.array(width, dtype=float)
height = np.array(height, dtype=float)

image_shape = (height, width)

class_names = read_classes("model_data/coco_classes.txt")
anchors = read_anchors("model_data/yolov2_anchors.txt")

yolo_model = load_model("model_data/yolov2.h5")

yolo_model.summary()

yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))


boxes, scores, classes = yolo_eval(yolo_outputs, image_shape)

sess = K.get_session()

image, image_data = preprocess_image("images/"+input_image_name, model_image_size = (608, 608))

out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes], feed_dict = {yolo_model.input:image_data,K.learning_phase():0})

print('Found {} boxes for {}'.format(len(out_boxes), input_image_name))

colors = generate_colors(class_names)

draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)

image.save(os.path.join("out", input_image_name), quality=90)
output_image = scipy.misc.imread(os.path.join("out", input_image_name))
imshow(output_image)