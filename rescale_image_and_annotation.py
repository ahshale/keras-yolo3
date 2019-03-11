import os
import re
import copy
import xml.etree.ElementTree as ET
import scipy.misc as misc

INPUT_WIDTH = 4160
INPUT_HEIGHT = 2340
OUTPUT_HEIGHT = 300
SCALE = INPUT_HEIGHT / OUTPUT_HEIGHT


def resize_image(image_dir, image_name, output_image_dir):
    image_file = os.path.join(image_dir, image_name)
    image = misc.imread(image_file)
    image = misc.imresize(image, [OUTPUT_HEIGHT, OUTPUT_HEIGHT])
    misc.imsave(os.path.join(output_image_dir, image_name), image)


def rescale_image_and_annotation(image_dir, ann_dir, output_image_dir, output_ann_dir, txt_file):

    for sub_dir in [output_image_dir, output_ann_dir]:
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
    
    with open(txt_file, 'r') as f:
        imgs = [line.strip() for line in f.readlines()]
    
    for img in imgs:
        
        ann = img.replace('.jpg', '.xml')
        try:
            tree = ET.parse(os.path.join(ann_dir, ann))
        except Exception as e:
            print(e)
            print('Ignore this bad annotation: ' + ann_dir + ann)
            continue
        
        for obj in tree.findall('object'): 
            bbox = obj.find('bndbox') 
            bbox.find('ymin').text = str(round(float(bbox.find('ymin').text) / SCALE))
            bbox.find('ymax').text = str(round(float(bbox.find('ymax').text) / SCALE))
            bbox.find('xmin').text = str(round(float(bbox.find('xmin').text) / SCALE))
            bbox.find('xmax').text = str(round(float(bbox.find('xmax').text) / SCALE))
        resize_image(image_dir, img, output_image_dir)
        tree.write(os.path.join(output_ann_dir, ann))   
        

if __name__ == '__main__':
    INPUT_IMAGE_DIR = 'D:/xgl/dataset'
    INPUT_ANN_DIR = 'D:/xgl/xml'

    train_file = 'D:/xgl/trainset.txt'
    TRAIN_OUTPUT_IMAGE_DIR = 'D:/xgll/dataset/yolo_train_data_'+str(OUTPUT_HEIGHT)
    TRAIN_OUTPUT_ANN_DIR = 'D:/xgll/dataset/yolo_train_xml_'+str(OUTPUT_HEIGHT)

    rescale_image_and_annotation(INPUT_IMAGE_DIR, INPUT_ANN_DIR, TRAIN_OUTPUT_IMAGE_DIR, TRAIN_OUTPUT_ANN_DIR, train_file)

    val_file = 'D:/xgl/valset.txt'
    VAL_OUTPUT_IMAGE_DIR = 'D:/xgll/dataset/yolo_val_data_'+str(OUTPUT_HEIGHT)
    VAL_OUTPUT_ANN_DIR = 'D:/xgll/dataset/yolo_val_xml_'+str(OUTPUT_HEIGHT)

    rescale_image_and_annotation(INPUT_IMAGE_DIR, INPUT_ANN_DIR, VAL_OUTPUT_IMAGE_DIR, VAL_OUTPUT_ANN_DIR, val_file)
    