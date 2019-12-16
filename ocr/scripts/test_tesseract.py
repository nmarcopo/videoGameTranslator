from PIL import Image
import subprocess
import xml.etree.ElementTree as ET
from collections import namedtuple
from itertools import combinations
import glob
import os
from time import sleep
import googletrans
from cer import cer

# GLOBALS
tesseract_binary = '/home/nmarcopo/local/bin/tesseract'
tessdata_dir = '../pxj_output/'
tessconfig_dir = '../tesseract_config/'
tessconfig_file = 'jpnconf'
confidence = 0


# rectangle from https://stackoverflow.com/questions/27152904/calculate-overlapped-area-between-two-rectangles
# rectangle object to calculate intersections
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
def intersection_percent(a, b):  # returns None if rectangles don't intersect
    areaA = (a.xmax - a.xmin) * (a.ymax - a.ymin)
    areaB = (b.xmax - b.xmin) * (b.ymax - b.ymin)
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return (dx*dy) / (areaA + areaB) * 100
    else:
        return 0

def getOCRString(ocr_info):
    tree = ET.fromstring(ocr_info)
    existWord = False
    rectangles = []
    string = ''
    for line in tree.findall(".//*[@class='ocrx_word']/.."):
        for word in line:
            for char in word:
                if char.text.strip() != '':
                    existWord = True
                    # make sure algorithm is confident
                    if float(char.attrib['title'].split('; ')[1].split()[1]) > confidence:
                        # get bboxes for item
                        bboxes = char.attrib['title'].split('; ')[0].split()[1:]
                        rectangles.append((char.text, Rectangle(int(bboxes[0]), int(bboxes[1]), int(bboxes[2]), int(bboxes[3]))))
                        string += char.text
        if existWord == True:
            string += '\n' # print newline between lines that aren't blank
            existWord = False
    return string

def print_intersection(rectangles):
    for pair in combinations(rectangles, 2):
        intersection = intersection_percent(pair[0][1], pair[1][1])
        if intersection > 20:
            print(intersection, pair[0][0], pair[1][0])

def get_ocr_info(img_path, trainedTess=True):
    invert = False
    if float(subprocess.check_output(['convert', img_path, '-colorspace', 'Gray', '-format', '"%[fx:image.mean]"', 'info:']).decode('utf-8').replace('"', '')) < .3:
        invert = True

    with open('stderr.txt', 'w') as f:
        if not trainedTess:
            # quick and dirty way to test the original, untrained tesseract
            if invert:
                # convert image to light background dark text if it isn't already
                invertedImage = subprocess.Popen(('convert', img_path, '-channel', 'RGB', '-negate', '-'), stdout=subprocess.PIPE)
                out = subprocess.check_output([tesseract_binary, '-', 'stdout', '-l', 'jpn', tessconfig_dir + tessconfig_file, '--psm', '11'], stdin=invertedImage.stdout, stderr=f).decode('utf-8')
                invertedImage.wait()
                return out
            else:
                return subprocess.check_output([tesseract_binary, img_path, 'stdout', '-l', 'jpn', tessconfig_dir + tessconfig_file, '--psm', '11'], stderr=f).decode('utf-8')
        else:
            if invert:
                # convert image to light background dark text if it isn't already
                invertedImage = subprocess.Popen(('convert', img_path, '-channel', 'RGB', '-negate', '-'), stdout=subprocess.PIPE)
                out = subprocess.check_output([tesseract_binary, '--tessdata-dir', tessdata_dir, '-', 'stdout', '-l', 'pxj', tessconfig_dir + tessconfig_file, '--psm', '11'], stdin=invertedImage.stdout, stderr=f).decode('utf-8')
                invertedImage.wait()
                return out
            else:
                return subprocess.check_output([tesseract_binary, '--tessdata-dir', tessdata_dir, img_path, 'stdout', '-l', 'pxj', tessconfig_dir + tessconfig_file, '--psm', '11'], stderr=f).decode('utf-8')

if __name__ == "__main__":
    # img_path = '../test/いつまでも　さみしがって　いられないわよね！おにいちゃん　だもんね！！.png'
    # ocr_info = get_ocr_info(img_path)
    # ocr_string = getOCRString(ocr_info).replace('\n', '')
    # print(ocr_string)

    for trained in [True, False]:
        for root, dirs, files in os.walk('../test/'):
            cers = []
            for img_path in files:
                ocr_info = get_ocr_info(root + img_path, trained)
                ocr_string = getOCRString(ocr_info).replace('\n', '')
                # print(ocr_string)
                # format string by removing all whitespace and file type
                img_path = ''.join(img_path.split()).replace('.png', '')
                cers.append((img_path, ocr_string))

            break # don't go more than one directory deep
        print("trained:", trained, "cer:", cer(cers))